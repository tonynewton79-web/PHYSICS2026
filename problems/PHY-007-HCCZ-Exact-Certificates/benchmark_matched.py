#!/usr/bin/env python3
"""PHY-007 physically matched, exact H/CCZ gate benchmark.

Independent of untrusted prior compiler for competitors, except its
actual emitted shared circuit is obtained through its public API.
The semantic checker below is independently reimplemented as a Boolean ANF
interpreter, and a small-width exact Hadamard amplitude replay is independent.

The cited Khattar-Gidney primitive bound is a literature *analytic* comparison,
NOT an executable same-gate-set benchmark. SPARE likewise not executed.
"""
from __future__ import annotations
import csv, json, math, random, hashlib
from pathlib import Path
from collections import defaultdict
try:
    from shared_prefix_compiler import compile_task  # repository source
except ImportError:
    from shared_prefix_data_compiler import compile_task  # standalone packet


OUT=Path(__file__).resolve().parent

def ccx(a,b,t): return [('H',t),('CCZ',a,b,t),('H',t)]
def borrow4(q,a,b,c,z):
    return ccx(q,a,z)+[('CCZ',z,b,c)]+ccx(q,a,z)+[('CCZ',z,b,c)]
def ladder(data, scratch):
    assert len(scratch)==len(data)-1
    seq=[ccx(data[0],data[1],scratch[0])]
    for j in range(1,len(scratch)):
        seq.append(ccx(scratch[j-1],data[j+1],scratch[j]))
    return seq

def emit_shared(t):
    cert=compile_task(t)
    return [tuple(g) for g in cert['gates']]

def emit_unshared(t):
    p=t['prefix'];tails=sorted(map(tuple,t['tails']));n=t['data_wires']
    stack=ladder(p,list(range(n,n+len(p)-1)))
    g=[]
    for a,b,c in tails:
        g.extend(x for group in stack for x in group)
        g.extend(borrow4(n+len(p)-2,a,b,c,p[0]))
        g.extend(x for group in reversed(stack) for x in group)
    return g

def emit_full_ladder(t):
    p=t['prefix'];tails=sorted(map(tuple,t['tails']));n=t['data_wires']
    scratch=list(range(n,n+len(p)))
    g=[]
    for tail in tails:
        data=p+list(tail)
        stack=ladder(data[:-2],scratch)
        g.extend(x for group in stack for x in group)
        g.append(('CCZ',scratch[-1],data[-2],data[-1]))
        g.extend(x for group in reversed(stack) for x in group)
    return g

def barenco_dirty_ccx(controls, target, dirty):
    # Faithful exact CCX cascade of Barenco et al. (1995), Lemma 7.2:
    # 4(c-2) 3-bit Toffolis for c controls and c-2 borrowed wires.
    c=len(controls)
    assert c>=3 and len(dirty)==c-2
    operations=[(controls[0],controls[1],dirty[0])]
    for j in range(1,c-2):
        operations.append((dirty[j-1],controls[j+1],dirty[j]))
    operations.append((dirty[-1],controls[-1],target))
    # Four alternating ladders with exact dirty-ancilla restoration.
    schedule=(operations + list(reversed(operations[:-1])) +
              operations[1:] + list(reversed(operations[1:-1])))
    assert len(schedule)==4*(c-2)
    return [ccx(a,b,t) for a,b,t in schedule]

def barenco_terms(t, width):
    # Every full monomial is implemented as H_target MCX_control H_target.
    # Borrow scratch only from data outside the term, then from allocated
    # clean wires if needed. The borrowed data must be restored exactly.
    p=t['prefix'];tails=sorted(map(tuple,t['tails']));n=t['data_wires']
    blocks=[]
    for tail in tails:
        controls=p+list(tail[:2]);target=tail[2]
        needed=len(controls)-2
        protected=set(controls+[target])
        unused=[i for i in range(n) if i not in protected]
        clean=[i for i in range(n,width)]
        dirty=(unused+clean)[:needed]
        if len(dirty)<needed:return None
        blocks.append((controls,target,dirty))
    return blocks

def emit_barenco(t):
    n=t['data_wires'];width=n+len(t['prefix'])-1
    blocks=barenco_terms(t,width)
    assert blocks is not None
    g=[]
    for controls,target,dirty in blocks:
        g.append(('H',target))
        for part in barenco_dirty_ccx(controls,target,dirty):g.extend(part)
        g.append(('H',target))
    return g

def verify_barenco(g,t,width):
    # Independently check source-derived Barenco CCX semantics and exact H conjugation,
    # then execute literal gate amplitudes below. This check does NOT presume an
    # expected resource count, nor use the synthesis function's gate schedule.
    blocks=barenco_terms(t,width)
    assert blocks is not None
    source_terms=[];offset=0;touches=set()
    for controls,target,dirty in blocks:
        assert g[offset]==('H',target)
        st=offset+1;ops=4*(len(controls)-2)
        sub=g[st:st+ops*3]
        assert g[st+ops*3]==('H',target)
        # Barenco guarantees restoration even if EVERY scratch wire is dirty.
        B=[frozenset({frozenset({i})}) for i in range(width)]
        initial=B[:]
        for j in range(ops):
            a,h,c=sub[3*j:3*j+3]
            assert a[0]=='H' and h[0]=='CCZ' and c==a and a[1] in h[1:]
            target_ccx=a[1];xx,yy=[i for i in h[1:] if i!=target_ccx]
            B[target_ccx]=B[target_ccx].symmetric_difference(M(B[xx],B[yy]))
            touches.update(h[1:])
        assert all(B[i]==initial[i] for i in range(width) if i!=target)
        delta=B[target].symmetric_difference(initial[target])
        exp=frozenset({frozenset(controls)})
        assert delta==exp,(delta,exp)
        source_terms.append(frozenset(controls+[target]))
        touches.add(target)
        offset=st+ops*3+1
    assert offset==len(g)
    expected=frozenset(frozenset(t['prefix']+tail) for tail in t['tails'])
    assert frozenset(source_terms)==expected
    return {'CCZ':sum(op[0]=='CCZ' for op in g),
            'H':sum(op[0]=='H' for op in g),
            'serial_depth':len(g),
            'active_clean':len(set(range(t['data_wires'],width)) & touches),
            'extra_dirty':0,
            'borrowed_data_active':len({q for _,_,dirty in blocks for q in dirty if q<t['data_wires']}),
            'physical':width}

def emit_shared_extra_clean(t):
    p=t['prefix'];tails=sorted(map(tuple,t['tails']));n=t['data_wires']
    prefix_scratch=list(range(n,n+len(p)-1))
    suffix_scratch=n+len(p)-1
    stack=ladder(p,prefix_scratch)
    g=[x for group in stack for x in group]
    for a,b,c in tails:
        g.extend(ccx(a,b,suffix_scratch))
        g.append(('CCZ',prefix_scratch[-1],suffix_scratch,c))
        g.extend(ccx(a,b,suffix_scratch))
    g.extend(x for group in reversed(stack) for x in group)
    return g

def emit_shared_recycled(t):
    # One clean prefix intermediate is vacated by reversible uncomputation
    # and later recomputed to uncompute the final prefix AND. Works k>=3.
    p=t['prefix'];tails=sorted(map(tuple,t['tails']));n=t['data_wires']
    prefix_scratch=list(range(n,n+len(p)-1));stack=ladder(p,prefix_scratch)
    g=[x for group in stack for x in group]
    g.extend(x for group in reversed(stack[:-1]) for x in group)
    reused=prefix_scratch[0]
    for a,b,c in tails:
        g.extend(ccx(a,b,reused))
        g.append(('CCZ',prefix_scratch[-1],reused,c))
        g.extend(ccx(a,b,reused))
    g.extend(x for group in stack[:-1] for x in group)
    g.extend(x for group in reversed(stack) for x in group)
    return g

# Completely independent GF2 Boolean ring simulator.
ONE=frozenset({frozenset()})
ZERO=frozenset()
def M(P,Q):
    out=set()
    for p in P:
        for q in Q:
            mon=p|q
            if mon in out:out.remove(mon)
            else:out.add(mon)
        if len(out)>200000:raise ValueError('ANF resource budget exceeded')
    return frozenset(out)

def verify(g, t, physical_wires):
    n=t['data_wires']; p=t['prefix']; tails=t['tails']
    B=[frozenset({frozenset({i})}) if i<n else ZERO for i in range(physical_wires)]
    initial=B.copy();phase=ZERO;h=ccz=0;i=0;touches=set();data_targets=set()
    while i<len(g):
        gate=g[i]
        assert gate[0] in ('H','CCZ')
        if gate[0]=='CCZ':
            assert len(gate)==4 and len(set(gate[1:]))==3 and all(0<=j<physical_wires for j in gate[1:])
            a,b,c=gate[1:];phase=phase.symmetric_difference(M(M(B[a],B[b]),B[c]));ccz+=1;touches.update(gate[1:]);i+=1
        else:
            assert i+2<len(g)
            assert g[i+2]==gate and g[i+1][0]=='CCZ'
            v=gate[1];cc=g[i+1][1:]
            assert len(set(cc))==3 and v in cc
            a,b=[x for x in cc if x!=v]
            B[v]=B[v].symmetric_difference(M(B[a],B[b]));h+=2;ccz+=1;touches.update(cc);
            if v<n:data_targets.add(v)
            i+=3
    assert B==initial, 'Not all scratch and data restored'
    expected=frozenset(frozenset(p+tail) for tail in tails)
    assert phase==expected, 'Wrong phase polynomial'
    return {'CCZ':ccz,'H':h,'serial_depth':ccz+h,
            'active_clean':len({j for j in touches if j>=n}),
            'extra_dirty':0,'borrowed_data_active':len(data_targets),'physical':physical_wires}

def amplitude(g, t, physical_wires, cap=1024):
    # actual H amplitudes not just Boolean-Toffoli reinterpretation
    n=t['data_wires'];N=physical_wires
    if n>10:return 0
    data_inputs=list(range(1<<n))
    if len(data_inputs)>cap:
        rng=random.Random(115);data_inputs=rng.sample(data_inputs,cap)
    bitcount=0
    for x in data_inputs:
        state={x:1}; h=0
        for op in g:
            if op[0]=='CCZ':
                mask=sum(1<<q for q in op[1:]);state={q:(-v if q&mask==mask else v) for q,v in state.items()}
            else:
                bit=1<<op[1];new=defaultdict(int);h+=1
                for q,v in state.items():
                    if q&bit:new[q&~bit]+=v;new[q]-=v
                    else:new[q]+=v;new[q|bit]+=v
                state={q:v for q,v in new.items() if v}
        assert h%2==0
        exponent=sum(all(x>>z&1 for z in t['prefix']+tail) for tail in t['tails'])%2
        assert state=={x:(-1 if exponent else 1)*(1<<(h//2))}
        bitcount+=1
    return bitcount

def standard_case(k,m):
    # Suffix triples genuinely disjoint, with no hidden extra shared prefix.
    return {'data_wires':k+3*m,'prefix':list(range(k)),
        'tails':[list(range(k+3*i,k+3*i+3)) for i in range(m)],
        'clean_capacity':k-1}

def overlapping_case(k):
    # Each suffix overlap is allowed, but the global suffix intersection is empty.
    tails=[[k,k+1,k+2],[k,k+3,k+4],[k+1,k+3,k+4]]
    return {'data_wires':k+5,'prefix':list(range(k)),
            'tails':tails,'clean_capacity':k-1}

def benchmark_case(t, matrix_budget=1024):
    k=len(t['prefix']);m=len(t['tails']);n=t['data_wires']
    candidates=[
       ('matched_no_prefix_cache',emit_unshared,n+k-1,'same wire budget'),
       ('phy007_shared_data_borrow',emit_shared,n+k-1,'same wire budget'),
       ('matched_recycled_prefix_ancilla',emit_shared_recycled,n+k-1,'same wire budget'),
       ('classic_independent_clean_ladder',emit_full_ladder,n+k,'one more clean wire'),
       ('shared_prefix_extra_clean',emit_shared_extra_clean,n+k,'one more clean wire'),
       ('phy007_shared_data_borrow_padded',emit_shared,n+k,'same larger wire budget'),
       ('published_barenco_l72_dirty',emit_barenco,n+k-1,'same wire budget')
    ]
    rows=[]; inputs=0
    for name,func,width,capnote in candidates:
        gates=func(t)
        chk=verify_barenco(gates,t,width) if name=='published_barenco_l72_dirty' else verify(gates,t,width)
        checked=amplitude(gates,t,width,matrix_budget)
        inputs+=checked
        rows.append({'k':k,'m':m,'data_wires':n,'method':name,
            'same_target':True,'native_H_CCZ':True,'verified_semantics':True,
            'basis_tests':checked,'allocation':capnote,**chk})
    return rows,inputs

def main():
    instances=[standard_case(k,m) for k,m in ((3,2),(4,2),(4,3),(5,2),(5,4),(8,5),(10,8),(16,12))]
    instances+=[overlapping_case(3),overlapping_case(4)]
    rows=[];totalamps=0
    for t in instances:
        r,c=benchmark_case(t);rows.extend(r);totalamps+=c
    # Spot-check exact threshold for matched-wire recycled-ancilla CCZ
    # improvement vs data-borrowing (at the expense of more H gates).
    for k,m in ((3,5),(4,6),(5,10),(8,16)):
        r,c=benchmark_case(standard_case(k,m));rows.extend(r);totalamps+=c
        sh=[z for z in r if z['method']=='phy007_shared_data_borrow'][0]
        rec=[z for z in r if z['method']=='matched_recycled_prefix_ancilla'][0]
        assert rec['CCZ']<sh['CCZ'] and rec['H']>sh['H']
    for r in rows:
        k,m=r['k'],r['m'];s=r['method']
        if s=='matched_no_prefix_cache':exp=(m*(2*k+2),m*(4*k))
        elif s in ('phy007_shared_data_borrow','phy007_shared_data_borrow_padded'):exp=(2*(k-1)+4*m,4*(k-1)+4*m)
        elif s=='matched_recycled_prefix_ancilla':exp=(4*k-6+3*m,8*k-12+4*m)
        elif s=='classic_independent_clean_ladder':exp=(m*(2*k+1),4*k*m)
        elif s=='shared_prefix_extra_clean':exp=(2*(k-1)+3*m,4*(k-1)+4*m)
        elif s=='published_barenco_l72_dirty':exp=(4*k*m,m*(8*k+2))
        else:raise ValueError(s)
        assert (r['CCZ'],r['H'])==exp,(r,exp)
    p=OUT/'matched_gate_results.csv'
    with p.open('w',newline='') as fh:
        w=csv.DictWriter(fh,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    result={'schema':'phy007-matched-benchmark-v1','tests':len(instances)+4,
            'rows':len(rows),'amplitude_basis_executions':totalamps,
            'methods':sorted(set(r['method'] for r in rows)),
            'raw_native_comparison':True,
            'literature_qualifications':{
                'Barenco_1995':'Lemma 7.2 dirty-ancilla CCX cascade implemented and verified in strict H/CCZ; actual schedule 4(c-2) CCX for each c-controlled X, with c-2 untouched borrowed data or scratch wires',
                'Khattar_Gidney_2025':'published 1-clean multicontrolled X Toffoli count 2c-3; published circuits also use X/negative controls and RCCX; no executable strict H/CCZ conversion in this package',
                'SPARE_2025':'benchmark frontend and exact native H/CCZ mapping not supplied by reviewed paper/artifact; not run; no claim to beat SPARE',
                'Lee_Kang_2026':'different controlled-NOT depth/Clifford+T cost model, not executed for this phase workload'
            }}
    (OUT/'matched_gate_summary.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS native H/CCZ matched target and clean restoration across',len(rows),'circuits')
    print('PASS independent actual Hadamard exact-amplitude basis cases:',totalamps)
    print('PASS strict CCZ/H/resources and alternative Pareto boundaries')
    for r in rows:
        if r['k']==4 and r['m']==3 and r['data_wires']==13:
            print('k=4 m=3:',r['method'], 'CCZ',r['CCZ'],'H',r['H'],
                  'clean-active',r['active_clean'],'physical',r['physical'])
    print('PASS: Barenco (1995) Lemma 7.2 published dirty-Toffoli comparator instantiated natively and checked')
    print('AUDIT: KG (2025), SPARE (2025), Lee-Kang (2026) not instantiated in strict H/CCZ')
if __name__=='__main__':main()