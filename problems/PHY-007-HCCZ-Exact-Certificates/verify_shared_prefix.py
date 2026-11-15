#!/usr/bin/env python3
"""Independent exact GF(2) checker for PHY-007 prefix-data borrowing.

Does NOT import the compiler. It replays actual H/CCZ operator semantics,
including an unknown original data bit temporarily used as borrowed scratch.
Unmatched H patterns are UNSUPPORTED, not claimed mathematically wrong.
"""
import json,hashlib,argparse,sys

class Rejected(Exception):pass
class Unsupported(Exception):pass

def need(test,reason):
    if not test:raise Rejected(reason)

def digest(d):
    t={k:v for k,v in d.items() if k!="sha256"}
    return hashlib.sha256(json.dumps(
        t,sort_keys=True,separators=(",",":"),ensure_ascii=True
    ).encode("ascii")).hexdigest()

def mul(p,q):
    z=set()
    for a in p:
        for b in q:
            v=a|b
            if v in z:z.remove(v)
            else:z.add(v)
            if len(z)>50000:raise Unsupported("ANF resource limit")
    return frozenset(z)

def verify(c):
    need(type(c)==dict and set(c)=={
        "schema","task","canonical_tails","gates","borrowed_data_wire",
        "resources","baseline","contract","sha256"},"wrong certificate schema")
    need(c["schema"]=="phy007-shared-prefix-data-v2","unknown protocol")
    need(c["sha256"]==digest(c),"digest mismatch")
    t=c["task"]
    need(type(t)==dict and set(t)=={
        "data_wires","prefix","tails","clean_capacity"},"wrong task schema")
    n=t["data_wires"];p=t["prefix"];tails=t["tails"];cap=t["clean_capacity"]
    need(type(n)==int and 6<=n<=256 and type(cap)==int and
         cap>=0 and n+cap<=512,"wire limit")
    need(type(p)==list and len(p)>=3 and
         all(type(i)==int and 0<=i<n for i in p) and
         len(set(p))==len(p),"invalid prefix")
    k=len(p)
    need(cap==k-1,"unsupported clean allocation (exact k-1 required)")
    need(type(tails)==list and len(tails)>=2,"need multiple tails")
    for tail in tails:
        need(type(tail)==list and len(tail)==3 and
             len(set(tail))==3 and all(type(i)==int and
             0<=i<n and i not in p for i in tail),"invalid suffix")
    tails0=sorted(set(tuple(sorted(z)) for z in tails))
    need(len(tails0)==len(tails) and
         c["canonical_tails"]==[list(x) for x in tails0],
         "incorrect canonical source")
    need(type(c["borrowed_data_wire"])==int and
         c["borrowed_data_wire"] in p,
         "borrowed target must be prefix data")
    need(c["contract"]=="all data unchanged except phase; clean initial zero and restored; borrowed prefix-data arbitrary and restored",
         "incorrect ancilla contract")
    N=n+cap
    gates=c["gates"]
    need(type(gates)==list,"bad gate list")
    if len(gates)>30000:raise Unsupported("max gate count")
    bit=[frozenset({frozenset({i})}) if i<n else frozenset()
         for i in range(N)]
    initial=bit[:]
    phase=frozenset()
    H=CCZ=0
    i=0
    targets=set()
    clean_touched=set()
    while i<len(gates):
        g=gates[i]
        need(type(g)==list and len(g)>=2,"malformed gate")
        if g[0]=="CCZ":
            need(len(g)==4 and len(set(g[1:]))==3 and
                 all(type(j)==int and 0<=j<N for j in g[1:]),
                 "invalid CCZ")
            a,b,q=g[1:]
            phase ^= mul(mul(bit[a],bit[b]),bit[q])
            CCZ+=1
            clean_touched.update(j for j in g[1:] if j>=n)
            i+=1
        elif g[0]=="H":
            if i+2>=len(gates):raise Unsupported("unmatched H")
            v=g[1];mid=gates[i+1];last=gates[i+2]
            need(len(g)==2 and type(v)==int and 0<=v<N,
                 "bad H target/arity")
            if not(type(mid)==list and len(mid)==4 and mid[0]=="CCZ"
                   and len(set(mid[1:]))==3 and
                   all(type(j)==int and 0<=j<N for j in mid[1:])
                   and type(last)==list and last==["H",v]
                   and v in mid[1:]):
                raise Unsupported("unmatched H-CCZ-H pattern")
            a,b=[j for j in mid[1:] if j!=v]
            bit[v] ^= mul(bit[a],bit[b])
            H+=2;CCZ+=1;targets.add(v)
            clean_touched.update(j for j in mid[1:] if j>=n)
            i+=3
        else:
            raise Unsupported("gate outside exact H/CCZ language")
    need(bit==initial,"data or clean ancilla not restored")
    target=frozenset(frozenset(set(p)|set(tail)) for tail in tails0)
    need(phase==target,"incorrect phase polynomial")
    need(targets & set(range(n))=={c["borrowed_data_wire"]},
         "incorrect borrowed-data target use")
    need(clean_touched==set(range(n,n+k-1)),
         "incorrect scratch allocation")
    m=len(tails0)
    counted={"ccz":CCZ,"h":H,"serial_depth":len(gates),
             "clean_peak":len(clean_touched),
             "extra_borrowed_peak":0,
             "borrowed_data_peak":len(targets&set(range(n))),
             "physical_wires":N}
    need(c["resources"]==counted,"resource claim does not match circuit")
    need(CCZ==2*(k-1)+4*m and H==4*(k-1)+4*m,
         "incorrect constructive gate formula")
    baseline={"ccz":m*(2*k+1),"h":4*k*m,
              "clean_peak":k,"physical_wires":n+k}
    need(c["baseline"]==baseline,"incorrect independent-ladder baseline")
    need(CCZ<baseline["ccz"] and H<baseline["h"] and
         N<baseline["physical_wires"],
         "no strict improvement over declared reference circuit")
    return {"status":"CERTIFIED","k":k,"m":m,
            "counts":counted,"baseline":baseline,
            "ccz_saved":baseline["ccz"]-CCZ,
            "h_saved":baseline["h"]-H,
            "clean_saved":1,"borrowed_data_wire":c["borrowed_data_wire"]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("certificate")
    args=p.parse_args()
    try:
        with open(args.certificate,encoding="utf8") as f:c=json.load(f)
        print(json.dumps(verify(c),sort_keys=True))
    except Rejected as exc:
        print("REJECTED:",exc,file=sys.stderr);sys.exit(1)
    except Unsupported as exc:
        print("UNSUPPORTED:",exc,file=sys.stderr);sys.exit(2)

if __name__=="__main__":
    main()
