#!/usr/bin/env python3
"""Deterministic, untrusted PHY-007 phase-polynomial H--CCZ compiler.

Input: explicit XOR of Boolean monomials of degree >=3.
Output: a circuit plus replayable block contracts and resource claims.
Use verify_certificate.py, which does NOT import this module, to certify.
No universal arbitrary-unitary, optimal-count, fault-tolerant, or Lean claim.
"""
import argparse
import hashlib
import json
from pathlib import Path

SCHEMA = "phy007-phase-pcc-v1"


def canonical_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha(obj):
    return hashlib.sha256(canonical_json(obj).encode("ascii")).hexdigest()


def integer(x, label, minimum=0):
    if type(x) is not int or x < minimum:
        raise ValueError("%s must be an integer >= %d" % (label, minimum))
    return x


def canonical_terms(terms, n):
    if type(terms) is not list:
        raise ValueError("monomials must be an explicit list")
    parity = set()
    for term in terms:
        if type(term) is not list or len(term) < 3:
            raise ValueError("only monomials of degree >= 3 are supported")
        if any(type(i) is not int or i < 0 or i >= n for i in term):
            raise ValueError("data index out of range")
        if len(set(term)) != len(term):
            raise ValueError("repeated wire within a monomial")
        t = tuple(sorted(term))
        if t in parity:
            parity.remove(t)
        else:
            parity.add(t)
    return [list(t) for t in sorted(parity, key=lambda x: (len(x), x))]


def ccx(a, b, t):
    return [["H", t], ["CCZ", a, b, t], ["H", t]]


def clean_block(term, clean):
    k = len(term)
    if k == 3:
        return [["CCZ", *term]]
    scratch = clean[:k-3]
    pieces = []
    # The jth scratch holds the conjunction of the first j+2 data bits.
    pieces.append(ccx(term[0], term[1], scratch[0]))
    for j in range(1, k-3):
        pieces.append(ccx(scratch[j-1], term[j+1], scratch[j]))
    result = [gate for p in pieces for gate in p]
    result.append(["CCZ", scratch[-1], term[-2], term[-1]])
    return result + [gate for p in reversed(pieces) for gate in p]


def borrowed4_block(term, borrowed):
    a, b, c, d = term
    return ccx(a, b, borrowed) + [["CCZ", borrowed, c, d]] + \
        ccx(a, b, borrowed) + [["CCZ", borrowed, c, d]]


def compile_task(task):
    if type(task) is not dict:
        raise ValueError("task must be an object")
    allowed = {"data_wires", "monomials", "clean_capacity",
               "borrowed_capacity", "policy"}
    if set(task) != allowed:
        raise ValueError("task keys must be exactly " + repr(sorted(allowed)))
    n = integer(task["data_wires"], "data_wires", 3)
    clean_cap = integer(task["clean_capacity"], "clean_capacity")
    borrowed_cap = integer(task["borrowed_capacity"], "borrowed_capacity")
    policy = task["policy"]
    if policy not in ("auto", "clean_only", "prefer_borrowed"):
        raise ValueError("unknown compiler policy")
    canonical = canonical_terms(task["monomials"], n)
    clean = list(range(n, n+clean_cap))
    dirty = list(range(n+clean_cap, n+clean_cap+borrowed_cap))
    gates = []
    blocks = []
    peak_clean = 0
    peak_dirty = 0
    for term in canonical:
        k = len(term)
        if k == 3:
            scheme = "ccz3"
            used_clean, used_dirty = [], []
            chunk = [["CCZ", *term]]
        elif k == 4 and dirty and policy == "prefer_borrowed":
            scheme = "borrowed4"
            used_clean, used_dirty = [], [dirty[0]]
            chunk = borrowed4_block(term, dirty[0])
        elif clean_cap >= k-3:
            scheme = "clean_ladder"
            used_clean, used_dirty = clean[:k-3], []
            chunk = clean_block(term, clean)
        elif k == 4 and dirty and policy != "clean_only":
            scheme = "borrowed4"
            used_clean, used_dirty = [], [dirty[0]]
            chunk = borrowed4_block(term, dirty[0])
        else:
            raise ValueError("insufficient clean ancillas for degree %d" % k)
        lo = len(gates)
        gates.extend(chunk)
        blocks.append({"term": term, "scheme": scheme,
                       "start": lo, "stop": len(gates),
                       "clean_used": used_clean, "borrowed_used": used_dirty})
        peak_clean = max(peak_clean, len(used_clean))
        peak_dirty = max(peak_dirty, len(used_dirty))
    resources = {
        "ccz": sum(g[0] == "CCZ" for g in gates),
        "h": sum(g[0] == "H" for g in gates),
        "serial_depth": len(gates),
        "clean_peak": peak_clean,
        "borrowed_peak": peak_dirty,
        "physical_wires": n+clean_cap+borrowed_cap,
        "block_count": len(blocks),
    }
    cert = {"schema": SCHEMA, "task": task, "canonical_terms": canonical,
            "blocks": blocks, "gates": gates, "resources": resources,
            "certificate_semantics": "exact on clean=zero, arbitrary borrowed"}
    cert["sha256"] = sha(cert)
    return cert


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--task", type=Path, help="input task JSON; otherwise --n/--term")
    p.add_argument("--n", type=int, default=5)
    p.add_argument("--term", action="append", default=[],
                   help="comma-separated data indices; can repeat for XOR cancellation")
    p.add_argument("--clean", type=int, default=2)
    p.add_argument("--borrowed", type=int, default=0)
    p.add_argument("--policy", default="auto")
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    if args.task:
        task = json.loads(args.task.read_text(encoding="utf-8"))
    else:
        terms = [[int(t) for t in x.split(",")] for x in args.term]
        if not terms:
            terms = [list(range(args.n))]
        task = {"data_wires": args.n, "monomials": terms,
                "clean_capacity": args.clean, "borrowed_capacity": args.borrowed,
                "policy": args.policy}
    cert = compile_task(task)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(cert, indent=2, sort_keys=True)+"\n",
                        encoding="utf-8")
    print("EMITTED", len(cert["blocks"]), "blocks;", cert["resources"],
          "digest", cert["sha256"])
    print("UNVERIFIED BY COMPILER: run independent verify_certificate.py", args.out)


if __name__ == "__main__":
    main()
