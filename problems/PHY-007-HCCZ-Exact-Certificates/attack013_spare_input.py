#!/usr/bin/env python3
"""PHY007 Attack013: generate exact SPARE DOT inputs. NOT a SPARE optimizer."""
import sys,json,hashlib,collections
from pathlib import Path
import pydot
sys.path.insert(0,str(Path(__file__).resolve().parent))
import benchmark_matched as bm
TASK=bm.standard_case(4,3)
TAILS=TASK['tails']
def oneclean():
    links=[(0,1,4),(4,2,7),(7,3,13)]
    comp=links+list(reversed(links[:-1]))+links[1:]+list(reversed(links[1:-1]))
    assert len(comp)==8
    seq=[('CCX',*v) for v in comp]
    for a,b,c in TAILS:
        seq += [('CCX',13,a,0),('CCZ',0,b,c),('CCX',13,a,0),('CCZ',0,b,c)]
    seq += [('CCX',*v) for v in reversed(comp)]
    return seq
def to_highlevel(g):
    out=[];i=0
    while i<len(g):
        op=g[i]
        if op[0]=='H':
            assert i+2<len(g) and g[i+2]==op and g[i+1][0]=='CCZ'
            target=op[1];a,b=[x for x in g[i+1][1:] if x!=target]
            out.append(('CCX',a,b,target));i+=3
        else:
            assert op[0]=='CCZ';out.append(op);i+=1
    return out
def models():
    return {
      'PHY007_shared_3clean_16w':(to_highlevel(bm.emit_shared(TASK)),16,[13,14,15]),
      'PHY007_shared_4clean_17w':(to_highlevel(bm.emit_shared_extra_clean(TASK)),17,[13,14,15,16]),
      'PHY007_independent_4clean_17w':(to_highlevel(bm.emit_full_ladder(TASK)),17,[13,14,15,16]),
      'PHY007_one_clean_14w':(oneclean(),14,[13]),
      'PHY007_one_clean_padded_16w':(oneclean(),16,[13])
    }
def check(ops,width,clean):
    assert width in (14,16,17) and all(13<=a<width for a in clean)
    for x in range(8192):
        bits=x;phase=0
        for op,a,b,t in ops:
            assert len({a,b,t})==3 and max(a,b,t)<width
            if op=='CCX':
                if (bits>>a)&1 and (bits>>b)&1:bits^=1<<t
            elif op=='CCZ':phase^=((bits>>a)&1)&((bits>>b)&1)&((bits>>t)&1)
            else:raise ValueError(op)
        expected=int(bool(all((x>>i)&1 for i in range(4)) and (sum(all((x>>j)&1 for j in T) for T in TAILS)%2)))
        assert (bits,phase)==(x,expected),(x,bits,phase,expected)
def write_graph(name,ops,width,clean,dest):
    lines=['digraph G {'];cur={i:i for i in range(width)}
    for i in range(width):
        lines.append(f'{i} [ancilla={str(i in clean)}, label="q({i}) (d=2), op=in", matrix="None", qubits="{i}"];')
    for j,(op,a,b,t) in enumerate(ops):
        i=width+j
        matrix='[[0, 1], [1, 0]]' if op=='CCX' else '[[1, 0], [0, -1]]'
        lines.append(f'{i} [label="Instruction(name=\x27{op}\x27, num_qubits=3, num_clbits=0, params=[])", matrix="{matrix}", qubits="{a},{b},{t}"];')
        for v in (a,b,t):
            lines.append(f'{cur[v]} -> {i} [label={v}];');cur[v]=i
    for v in range(width):
        i=width+len(ops)+v
        lines.append(f'{i} [ancilla={str(v in clean)}, label="q({v}) (d=2), op=out", matrix="None", qubits="{v}"];')
        lines.append(f'{cur[v]} -> {i} [label={v}];')
    lines.append('}')
    path=dest/(name+'_graph.dot')
    path.write_text('\n'.join(lines)+'\n')
    g=pydot.graph_from_dot_file(str(path))[0]
    assert len(g.get_nodes())==2*width+len(ops)
    assert len(g.get_edges())==3*len(ops)+width
    return path
def main():
    dest=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent/'input_dot'
    dest.mkdir(parents=True,exist_ok=True)
    ledger={}
    for name,(ops,width,clean) in models().items():
        check(ops,width,clean)
        p=write_graph(name,ops,width,clean,dest)
        c=collections.Counter(o[0] for o in ops)
        ledger[name]={'width':width,'clean':clean,'CCX':c['CCX'],'CCZ':c['CCZ'],'strict_CCZ':c['CCX']+c['CCZ'],'strict_H':2*c['CCX'],'basis_checks':8192,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
        print('PASS_INPUT',name,ledger[name],flush=True)
    (dest/'input_ledger.json').write_text(json.dumps(ledger,indent=2))
if __name__=='__main__':main()
