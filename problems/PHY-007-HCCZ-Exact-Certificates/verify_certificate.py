#!/usr/bin/env python3
"""Standalone proof checker for PHY-007; imports NOTHING from proof_compiler.

Accepted theorem: an explicit XOR of Boolean phase monomials (degree>=3)
acts on data; all declared clean ancillas start/end in |0>, and every
borrowed ancilla is exactly unchanged even if externally entangled.

Restricted certificate language: CCZ and H-CCZ-H (exact CCX) blocks.
A generic circuit containing unmatched H is UNSUPPORTED, not proved wrong.
The checker uses its own exact GF(2) ANF state interpreter, not an
expected-gate template or the compiler's claimed phases.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

SCHEMA = "phy007-phase-pcc-v1"
MAX_GATES = 200000
MAX_POLY_TERMS = 8192
MAX_DATA = 256


class InvalidCertificate(Exception):
    pass


class UnsupportedCertificate(Exception):
    pass


def require(cond, message):
    if not cond:
        raise InvalidCertificate(message)


def uint(v, name, minimum=0):
    require(type(v) is int and v >= minimum, name+" must be integer >= "+str(minimum))
    return v


def xor(p, q):
    return p ^ q


def multiply(p, q):
    # Polynomials over F_2[x_0,..,x_{m-1}]/(x_i^2-x_i).
    result = set()
    for a in p:
        for b in q:
            monom = a | b
            if monom in result:
                result.remove(monom)
            else:
                result.add(monom)
        if len(result) > MAX_POLY_TERMS:
            raise UnsupportedCertificate("ANF term resource cap")
    return frozenset(result)


def single(wire):
    return frozenset({frozenset({wire})})


def phase_monomial(wires):
    return frozenset({frozenset(wires)})


def canonicalize(terms, n):
    require(type(terms) is list, "monomials list required")
    phase = set()
    for term in terms:
        require(type(term) is list and len(term) >= 3, "unsupported monomial degree")
        require(all(type(x) is int and 0 <= x < n for x in term),
                "invalid data wire")
        require(len(set(term)) == len(term), "duplicate wire within monomial")
        t = tuple(sorted(term))
        if t in phase:
            phase.remove(t)
        else:
            phase.add(t)
    return [list(x) for x in sorted(phase, key=lambda t:(len(t),t))]


def validate_gate(g, width):
    require(type(g) is list and len(g) >= 2, "malformed gate")
    op = g[0]
    if op == "CCZ":
        require(len(g) == 4, "CCZ arity")
        wires = g[1:]
        require(all(type(x) is int and 0 <= x < width for x in wires),
                "CCZ invalid wire")
        require(len(set(wires)) == 3, "CCZ requires distinct wires")
    elif op == "H":
        require(len(g) == 2 and type(g[1]) is int and 0 <= g[1] < width,
                "H invalid wire")
    else:
        raise UnsupportedCertificate("gate outside H/CCZ language: "+repr(op))


def interpret(chunk, current, phase, width):
    """Semantically independent Boolean ANF interpreter with local CCX lemma.

    H_t CCZ_(a,b,t) H_t exactly equals CCX_(a,b)->t as an operator.
    In this certificate grammar arbitrary unmatched H is not handled.
    """
    before = current[:]
    old_phase = phase
    h = 0
    ccz = 0
    i = 0
    touched = set()
    while i < len(chunk):
        gate = chunk[i]
        validate_gate(gate, width)
        if gate[0] == "CCZ":
            a,b,c = gate[1:]
            phase = xor(phase, multiply(multiply(current[a],current[b]),current[c]))
            touched.update((a,b,c))
            ccz += 1
            i += 1
        else:
            if i + 2 >= len(chunk):
                raise UnsupportedCertificate("unmatched H")
            first, middle, last = chunk[i:i+3]
            validate_gate(middle, width)
            validate_gate(last, width)
            t = gate[1]
            if not (middle[0] == "CCZ" and last == ["H",t] and
                    t in middle[1:]):
                raise UnsupportedCertificate("H not in exact H-CCZ-H/CCX pattern")
            ctrl = [x for x in middle[1:] if x != t]
            require(len(ctrl) == 2, "CCX controls")
            a,b=ctrl
            current[t] = xor(current[t],multiply(current[a],current[b]))
            touched.update((t,a,b))
            h += 2
            ccz += 1
            i += 3
    require(current == before, "block fails to restore data/ancilla wires")
    delta = phase ^ old_phase
    return current,phase,delta,h,ccz,touched


def validate_certificate(cert):
    require(type(cert) is dict, "certificate must be an object")
    require(set(cert) == {"schema","task","canonical_terms","blocks",
                         "gates","resources","certificate_semantics","sha256"},
            "unexpected/missing certificate fields")
    require(cert["schema"] == SCHEMA, "unknown certificate protocol")
    require(cert["certificate_semantics"] ==
            "exact on clean=zero, arbitrary borrowed", "incorrect semantic contract")
    digest = cert["sha256"]
    require(type(digest) is str and len(digest) == 64, "missing SHA-256 field")
    payload = {k:v for k,v in cert.items() if k != "sha256"}
    encoded = json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=True)
    require(hashlib.sha256(encoded.encode("ascii")).hexdigest() == digest,
            "certificate digest mismatch (integrity only)")
    t = cert["task"]
    require(type(t) is dict and set(t) ==
            {"data_wires","monomials","clean_capacity","borrowed_capacity","policy"},
            "bad task schema")
    n=uint(t["data_wires"],"data",3)
    if n>MAX_DATA:
        raise UnsupportedCertificate("data-wire resource limit")
    nc=uint(t["clean_capacity"],"clean capacity")
    nb=uint(t["borrowed_capacity"],"borrowed capacity")
    require(n+nc+nb<=1024,"physical wire cap")
    require(t["policy"] in ("auto","clean_only","prefer_borrowed"),
            "unknown policy")
    terms=canonicalize(t["monomials"],n)
    require(cert["canonical_terms"]==terms,"canonical XOR source mismatch")
    gates=cert["gates"]; blocks=cert["blocks"]; r=cert["resources"]
    require(type(gates) is list and type(blocks) is list,"missing gates/blocks")
    if len(gates)>MAX_GATES:
        raise UnsupportedCertificate("gate resource cap")
    require(len(blocks)==len(terms),"one block per canonical monomial")
    width=n+nc+nb
    for g in gates:
        validate_gate(g,width)
    clean_wires=set(range(n,n+nc))
    borrowed_wires=set(range(n+nc,width))
    bit=[single(j) if j<n or j in borrowed_wires else frozenset()
         for j in range(width)]
    original=bit[:]
    phase=frozenset()
    offset=0
    h_count=ccz_count=0
    used_clean=set()
    used_borrowed=set()
    for block,term in zip(blocks,terms):
        require(type(block) is dict and set(block) ==
                {"term","scheme","start","stop","clean_used","borrowed_used"},
                "invalid block schema")
        require(block["term"]==term,"block's claimed source monomial changed")
        lo=uint(block["start"],"block start")
        hi=uint(block["stop"],"block stop")
        require(lo==offset and lo<hi<=len(gates),"noncontiguous block windows")
        uc=block["clean_used"];ub=block["borrowed_used"]
        require(type(uc) is list and type(ub) is list,"ancilla lists missing")
        require(all(type(x) is int and x in clean_wires for x in uc),
                "wrong clean precondition")
        require(all(type(x) is int and x in borrowed_wires for x in ub),
                "wrong borrowed precondition")
        require(len(set(uc))==len(uc) and len(set(ub))==len(ub),
                "duplicate ancillary roles")
        scheme=block["scheme"]; k=len(term)
        if scheme=="ccz3":
            require(k==3 and not uc and not ub,"ccz3 ancilla/degree")
            expected_h,expected_ccz=0,1
        elif scheme=="clean_ladder":
            require(k>=4 and len(uc)==k-3 and not ub,
                    "clean ladder contract")
            expected_h,expected_ccz=4*(k-3),2*k-5
        elif scheme=="borrowed4":
            require(k==4 and not uc and len(ub)==1,
                    "borrowed4 contract")
            require(t["policy"]!="clean_only","borrowed prohibited by policy")
            expected_h,expected_ccz=4,4
        else:
            raise UnsupportedCertificate("unknown certificate block scheme")
        before=phase
        bit,phase,delta,h,c,touched=interpret(
            gates[lo:hi],bit,phase,width)
        require(delta==phase_monomial(term),
                "actual gate semantics differs from target phase monomial")
        require(h==expected_h and c==expected_ccz,
                "block violates claimed constructive gate bound")
        actual_c=touched & clean_wires
        actual_b=touched & borrowed_wires
        require(actual_c==set(uc) and actual_b==set(ub),
                "ancilla use differs from block preconditions")
        used_clean |= actual_c
        used_borrowed |= actual_b
        h_count+=h; ccz_count+=c
        offset=hi
    require(offset==len(gates),"unverified trailing gates")
    require(bit==original,"non-restored wire under symbolic execution")
    required_phase=frozenset(
        frozenset(term) for term in terms
    )
    require(phase==required_phase,"global phase polynomial mismatch")
    require(type(r) is dict and set(r) ==
            {"ccz","h","serial_depth","clean_peak","borrowed_peak",
             "physical_wires","block_count"},"invalid resource record")
    require(r["ccz"]==ccz_count and r["h"]==h_count,
            "incorrect independently counted gate resources")
    require(r["serial_depth"]==len(gates) and r["physical_wires"]==width,
            "invalid serial depth/width")
    require(r["block_count"]==len(terms),"incorrect block count")
    require(r["clean_peak"]==len(used_clean)
            and r["borrowed_peak"]==len(used_borrowed),
            "incorrect ancilla resource claim")
    return {"status":"CERTIFIED","schema":SCHEMA,"blocks":len(terms),
            "ccz":ccz_count,"h":h_count,"serial_depth":len(gates),
            "clean_peak":len(used_clean),"borrowed_peak":len(used_borrowed),
            "physical_wires":width,"sha256":digest}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("certificate",type=Path)
    args=p.parse_args()
    try:
        cert=json.loads(args.certificate.read_text(encoding="utf-8"))
        result=validate_certificate(cert)
        print(json.dumps(result,sort_keys=True))
    except UnsupportedCertificate as exc:
        print("UNSUPPORTED:",exc,file=sys.stderr)
        sys.exit(2)
    except (InvalidCertificate,ValueError,TypeError,KeyError) as exc:
        print("REJECTED:",exc,file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
