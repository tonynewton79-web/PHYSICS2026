#!/usr/bin/env python3
"""Independent PHY-007 shared-prefix compiler regression and falsification.

The main proof checker imports NO compiler code. This test harness
imports both and checks small instances with the older, separate exact
H/CCZ signed-integer amplitude simulator from verify.py.
"""
import copy,hashlib,json,random
from shared_prefix_compiler import compile_task
from verify_shared_prefix import verify,Rejected,Unsupported,digest
from verify import apply, equal

def source(k,m):
    n=k+2+m
    return {"data_wires":n,"prefix":list(range(k)),
            "tails":[[k,k+1,k+2+j] for j in range(m)],
            "clean_capacity":k-1}

def exact_amplitudes(c):
    n=c["task"]["data_wires"];N=c["resources"]["physical_wires"]
    p=c["task"]["prefix"]
    gates=[tuple(g) for g in c["gates"]]
    count=0
    for x in range(1<<n):
        exponent=sum(all(x>>q&1 for q in p+t)
                     for t in c["canonical_tails"])%2
        wanted=(0,{x:-1 if exponent else 1})
        assert equal(apply(gates,N,x),wanted)
        count+=1
    return count

def altered(c,mutation):
    z=copy.deepcopy(c)
    mutation(z)
    z["sha256"]=digest(z)  # do not treat checksum as semantic proof
    try:verify(z)
    except (Rejected,Unsupported,ValueError,TypeError):return
    raise AssertionError("semantically mutated certificate was accepted")

def main():
    accepted=0;amplitudes=0
    for k,m in [(3,2),(3,3),(4,3),(5,2)]:
        c=compile_task(source(k,m))
        assert verify(c)["status"]=="CERTIFIED"
        amplitudes+=exact_amplitudes(c)
        accepted+=1
    for k in list(range(3,26))+[32,48,64,96,246]:
        for m in (2,3,5,8):
            c=compile_task(source(k,m))
            result=verify(c)
            r=c["resources"];old=c["baseline"]
            assert result["status"]=="CERTIFIED"
            assert old["ccz"]-r["ccz"]==m*(2*k-3)-2*(k-1)
            assert old["h"]-r["h"]==4*(k-1)*(m-1)
            assert old["physical_wires"]-r["physical_wires"]==1
            accepted+=1
    rng=random.Random(20261115)
    for _ in range(150):
        k=rng.randint(3,12);n=k+rng.randint(4,12)
        choices=set()
        m=rng.randint(2,min(8,__import__("math").comb(n-k,3)))
        while len(choices)<m:
            choices.add(tuple(sorted(rng.sample(range(k,n),3))))
        t={"data_wires":n,"prefix":list(range(k)),
           "tails":[list(q) for q in choices],"clean_capacity":k-1}
        assert verify(compile_task(t))["status"]=="CERTIFIED"
        accepted+=1
    c=compile_task(source(3,2))
    mutants=[
        lambda x:x["gates"].pop(),
        lambda x:x["gates"].__setitem__(3,["CCZ",0,5,6]),
        lambda x:x["gates"].__setitem__(0,["H",0]),
        lambda x:x["resources"].__setitem__("ccz",0),
        lambda x:x["resources"].__setitem__("physical_wires",99),
        lambda x:x["task"].__setitem__("prefix",[1,2,3]),
        lambda x:x["task"].__setitem__("clean_capacity",1),
        lambda x:x["task"].__setitem__("tails",[[3,4,5],[3,5,6]]),
        lambda x:x["canonical_tails"].__setitem__(0,[3,5,6]),
        lambda x:x.__setitem__("borrowed_data_wire",50),
        lambda x:x["baseline"].__setitem__("ccz",999),
        lambda x:x["gates"].append(["CCZ",0,1,2]),
        lambda x:x.__setitem__("contract","borrowed initialized"),
    ]
    for change in mutants:altered(c,change)
    z=copy.deepcopy(c);z["sha256"]="0"*64
    try:verify(z)
    except Rejected:pass
    else:raise AssertionError("invalid SHA-256 accepted")
    bad=[
        {"data_wires":7,"prefix":[0,1,2],
         "tails":[[3,4,5]],"clean_capacity":2},
        {"data_wires":7,"prefix":[0,1,2],
         "tails":[[3,4,5],[3,4,5]],"clean_capacity":2},
        {"data_wires":7,"prefix":[0,1,2],
         "tails":[[3,4,5],[3,4,6]],"clean_capacity":1},
        {"data_wires":7,"prefix":[0,1,2],
         "tails":[[3,4,5],[0,4,6]],"clean_capacity":2},
    ]
    for t in bad:
        try:compile_task(t)
        except ValueError:pass
        else:raise AssertionError("unsupported source compiled")
    print("PASS independently certified shared-prefix circuits:",accepted)
    print("PASS independent exact H/CCZ amplitudes:",amplitudes)
    print("PASS modified/rehashed certificates rejected:",len(mutants)+1)
    print("PASS exact formula, full 256 data-wire stress, no added borrowed qubit")
    print("ALL SHARED-PREFIX H/CCZ TESTS PASS")

if __name__=="__main__":
    main()
