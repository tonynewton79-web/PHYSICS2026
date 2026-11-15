#!/usr/bin/env python3
"""Adversarial integration/regression suite for PHY-007 proof-carrying compiler.

The certifier is independent: verify_certificate.py never imports compiler.
The *tests* may call both and separately call the earlier exact H/CCZ
integer amplitude simulator for a small-width exhaustive control.
"""
import copy
import hashlib
import json
import random
from pathlib import Path
from tempfile import TemporaryDirectory

from proof_compiler import compile_task
from verify_certificate import (
    validate_certificate, InvalidCertificate, UnsupportedCertificate
)
from verify import apply as exact_hccz_apply, equal as exact_equal

def digest(data):
    rest={k:v for k,v in data.items() if k!="sha256"}
    data["sha256"]=hashlib.sha256(
        json.dumps(rest,sort_keys=True,separators=(",",":"),ensure_ascii=True
                   ).encode("ascii")).hexdigest()
    return data

def task(n, monomials, clean=0, borrowed=0, policy="auto"):
    return {"data_wires":n,"monomials":monomials,
            "clean_capacity":clean,"borrowed_capacity":borrowed,
            "policy":policy}

def accepted(data):
    cert=compile_task(data)
    result=validate_certificate(cert)
    assert result["status"]=="CERTIFIED"
    assert result["h"]==sum(g[0]=="H" for g in cert["gates"])
    assert result["ccz"]==sum(g[0]=="CCZ" for g in cert["gates"])
    return cert

def rejected(data,description):
    try:
        validate_certificate(digest(copy.deepcopy(data)))
    except (InvalidCertificate,UnsupportedCertificate,ValueError,TypeError):
        return
    raise AssertionError("incorrectly certified mutant "+description)

def exact_matrix_control(cert):
    """Actual exact 2^-h/2 H/CCZ amplitudes, independent of ANF checker."""
    n=cert["task"]["data_wires"]
    clean=cert["task"]["clean_capacity"]
    borrowed=cert["task"]["borrowed_capacity"]
    N=n+clean+borrowed
    if N>8:
        return 0
    cphase={tuple(x) for x in cert["canonical_terms"]}
    inputs=0
    for bits in range(1<<N):
        if any((bits>>(n+i))&1 for i in range(clean)):
            continue
        sign=(-1)**sum(all((bits>>j)&1 for j in term) for term in cphase)
        target=(0,{bits:sign})
        assert exact_equal(exact_hccz_apply([tuple(g) for g in cert["gates"]],
                                           N,bits),target)
        inputs+=1
    return inputs

def main():
    rng=random.Random(61023)
    tests=inputs=0
    for k in range(3,24):
        g=accepted(task(k,[list(range(k))],clean=max(0,k-3)))
        assert g["resources"]["ccz"]==2*k-5
        assert g["resources"]["h"]==4*(k-3)
        assert g["resources"]["clean_peak"]==max(0,k-3)
        tests+=1;inputs+=exact_matrix_control(g)
    # Parametric high-wire stress test without exponential basis enumeration.
    # Covers the checker's declared 256-data-wire cap, not unbounded runtime.
    for k in (32,64,128,256):
        cert=accepted(task(k,[list(range(k))],clean=k-3))
        assert cert["resources"]["ccz"]==2*k-5
        assert cert["resources"]["h"]==4*(k-3)
        assert cert["resources"]["serial_depth"]==6*k-17
        tests+=1
    # Four-body borrowed contract, including arbitrary initial borrowed bit.
    dirty=accepted(task(4,[[0,1,2,3]],borrowed=1,policy="prefer_borrowed"))
    assert dirty["resources"]["ccz"]==4 and dirty["resources"]["h"]==4
    assert dirty["resources"]["borrowed_peak"]==1
    tests+=1;inputs+=exact_matrix_control(dirty)
    # Shared clean scratch, duplicates cancel as an F2 phase polynomial.
    combos=[
        task(6,[[0,1,2],[0,1,2,3],[0,2,3,4,5],[1,2,3],
                [0,1,2],[1,2,3]],clean=2),
        task(7,[[0,1,2,3],[2,3,4,5],[1,4,6],[0,1,2,3],
                [0,1,2,3,4,5]],clean=3),
        task(5,[[0,1,2,3],[0,2,3,4]],borrowed=1,policy="prefer_borrowed"),
        task(5,[[0,1,2,3],[0,2,3,4]],clean=1,borrowed=1,policy="auto"),
        task(5,[[0,1,2,3],[0,2,3,4]],clean=1,borrowed=1,policy="prefer_borrowed"),
        task(4,[[0,1,2],[0,1,2]],clean=0),
    ]
    for spec in combos:
        cert=accepted(spec);tests+=1;inputs+=exact_matrix_control(cert)
    # Randomly generated small mixed polynomial tasks.
    for _ in range(80):
        n=rng.randint(3,7)
        m=rng.randint(1,8)
        terms=[sorted(rng.sample(range(n),rng.randint(3,n))) for __ in range(m)]
        spec=task(n,terms,clean=n-3,borrowed=rng.randint(0,1),
                  policy=rng.choice(("auto","clean_only","prefer_borrowed")))
        cert=accepted(spec)
        tests+=1;inputs+=exact_matrix_control(cert)
    # Fail-closed compilation boundaries.
    for spec in [
        task(4,[[0,1,2,3]],clean=0,borrowed=0),
        task(5,[[0,1,2,3,4]],clean=1,borrowed=1),
        task(5,[[0,1,2,3]],clean=0,borrowed=1,policy="clean_only"),
        task(3,[[0,1]]),task(4,[[0,1,1]]),
        task(4,[[0,1,5]]),task(4,[[0,1,True]]),
    ]:
        try:compile_task(spec)
        except ValueError:pass
        else:raise AssertionError("invalid source compiled: "+repr(spec))
    # Mutations rehash first, to challenge actual proof rather than checksum.
    mutants=0
    baseline=accepted(task(4,[[0,1,2,3]],borrowed=1,
                           policy="prefer_borrowed"))
    def mutated(label,modify):
        nonlocal mutants
        x=copy.deepcopy(baseline)
        modify(x)
        rejected(x,label)
        mutants+=1
    mutated("missing borrowed compensation",
            lambda x: x["gates"].pop())
    mutated("incorrect CCZ operand",
            lambda x: x["gates"].__setitem__(3,["CCZ",0,2,3]))
    mutated("fake clean precondition",
            lambda x: x["blocks"][0].__setitem__("clean_used",[4]))
    mutated("wrong resource count",
            lambda x: x["resources"].__setitem__("ccz",3))
    mutated("unmatched H pattern",
            lambda x: x["gates"].__setitem__(0,["H",1]))
    mutated("source replaced",
            lambda x: x["task"].__setitem__("monomials",[[0,1,2]]))
    mutated("borrowed flag disabled",
            lambda x: x["task"].__setitem__("borrowed_capacity",0))
    mutated("incorrect block offset",
            lambda x: x["blocks"][0].__setitem__("stop",len(x["gates"])-1))
    mutated("spurious appended phase",
            lambda x: x["gates"].append(["CCZ",0,1,2]))
    mutated("unsupported S gate",
            lambda x: x["gates"].__setitem__(0,["S",1]))
    mutated("incorrect block monomial",
            lambda x: x["blocks"][0].__setitem__("term",[0,1,2]))
    mutant=copy.deepcopy(baseline);mutant["sha256"]="0"*64
    try:validate_certificate(mutant)
    except InvalidCertificate:mutants+=1
    else:raise AssertionError("bad digest accepted")
    # Certified artifacts preserve available ancilla registers even
    # if clean wires are unused and borrowed wires are entangled.
    with TemporaryDirectory() as tmp:
        p=Path(tmp)/"certificate.json"
        p.write_text(json.dumps(baseline))
        assert validate_certificate(json.loads(p.read_text()))["status"]=="CERTIFIED"
    print("PASS proof-carrying family and randomized tests:",tests)
    print("PASS independent exact H/CCZ amplitude basis executions:",inputs)
    print("PASS adversarial mutated certificates rejected:",mutants)
    print("PASS malformed source and insufficient ancilla requirements rejected")
    print("ALL PHY007 PROOF-CARRYING COMPILER TESTS PASS")


if __name__=="__main__":
    main()
