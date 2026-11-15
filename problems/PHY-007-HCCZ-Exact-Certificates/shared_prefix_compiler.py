#!/usr/bin/env python3
"""Untrusted PHY-007 shared-prefix phase compiler with temporary DATA borrowing.

A common k-bit conjunction is computed once using k-1 clean scratch
wires; the first input prefix wire is borrowed and restored during each
compensated four-body phase. Independent semantics: verify_shared_prefix.py.
"""
import argparse
import hashlib
import json

SCHEMA = "phy007-shared-prefix-data-v2"

def digest(c):
    return hashlib.sha256(json.dumps(
        c, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")).hexdigest()

def ccx(a,b,t):
    return [["H",t], ["CCZ",a,b,t], ["H",t]]

def borrowed4(q,a,b,c,z):
    return (ccx(q,a,z) + [["CCZ",z,b,c]] +
            ccx(q,a,z) + [["CCZ",z,b,c]])

def compile_task(t):
    if type(t)!=dict or set(t)!={"data_wires","prefix","tails","clean_capacity"}:
        raise ValueError("source schema")
    n=t["data_wires"]; p=t["prefix"]; tails=t["tails"]; cap=t["clean_capacity"]
    if type(n)!=int or n<6 or type(cap)!=int or cap<0:
        raise ValueError("invalid width/capacity")
    if (type(p)!=list or len(p)<3 or len(set(p))!=len(p)
            or any(type(i)!=int or not 0<=i<n for i in p)):
        raise ValueError("invalid common prefix")
    k=len(p)
    if cap!=k-1:
        raise ValueError("compiler requires exactly k-1 clean scratch bits")
    if type(tails)!=list or len(tails)<2:
        raise ValueError("need at least two suffixes")
    for tail in tails:
        if (type(tail)!=list or len(tail)!=3 or len(set(tail))!=3
                or any(type(i)!=int or not 0<=i<n or i in p for i in tail)):
            raise ValueError("bad suffix")
    canonical=sorted(set(tuple(sorted(tail)) for tail in tails))
    if len(canonical)!=len(tails):
        raise ValueError("repeated suffixes must be cancelled before compilation")
    scratch=list(range(n,n+k-1))
    borrowed=p[0]  # existing DATA wire, not an added borrowed ancilla
    ladder=[ccx(p[0],p[1],scratch[0])]
    for j in range(1,k-1):
        ladder.append(ccx(scratch[j-1],p[j+1],scratch[j]))
    gates=[g for block in ladder for g in block]
    for a,b,c in canonical:
        gates.extend(borrowed4(scratch[-1],a,b,c,borrowed))
    gates.extend(g for block in reversed(ladder) for g in block)
    m=len(canonical)
    r={"ccz":sum(g[0]=="CCZ" for g in gates),
       "h":sum(g[0]=="H" for g in gates),
       "serial_depth":len(gates),"clean_peak":k-1,
       "extra_borrowed_peak":0,"borrowed_data_peak":1,
       "physical_wires":n+cap}
    baseline={"ccz":m*(2*k+1),"h":4*k*m,
              "clean_peak":k,"physical_wires":n+k}
    out={"schema":SCHEMA,"task":t,
         "canonical_tails":[list(x) for x in canonical],
         "gates":gates,"borrowed_data_wire":borrowed,
         "resources":r,"baseline":baseline,
         "contract":"all data unchanged except phase; clean initial zero and restored; borrowed prefix-data arbitrary and restored"}
    out["sha256"]=digest(out)
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--task",required=True)
    p.add_argument("--out",required=True)
    args=p.parse_args()
    with open(args.task,encoding="utf8") as f:task=json.load(f)
    cert=compile_task(task)
    with open(args.out,"w",encoding="utf8") as f:
        json.dump(cert,f,indent=2,sort_keys=True)
    print("EMITTED",cert["resources"],"BASELINE",cert["baseline"])
    print("NOT VERIFIED: invoke independent verify_shared_prefix.py")

if __name__=="__main__":
    main()
