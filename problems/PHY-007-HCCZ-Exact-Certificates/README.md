# PHY-007 — Exact equivalence and ancilla contracts in Hadamard–CCZ quantum circuits

**Author:** Tony Newton · tony.newton79@gmail.com

## Main results

For every integer n>=3, the n-body phase (-1)^(x0 ... x(n-1)) is realized by an explicit Toffoli-compute, central-CCZ and reverse-uncompute construction using **n-3 clean ancillas**, **2n-5 CCZ** gates and **4(n-3) Hadamards**. These are constructive upper bounds, not claimed optimality.

For four data qubits, a *separate borrowed-ancilla* circuit implements the same four-body phase on **all five-qubit input states**, leaving one unknown auxiliary qubit completely unchanged: CCX(0,1;4), CCZ(4,2,3), CCX(0,1;4), CCZ(4,2,3). Each CCX is compiled to H-target, CCZ, H-target, giving four CCZ and four H total.

For CCZ-only diagonal circuits the Boolean phase has a **unique cubic algebraic normal form**, and the group has rank binomial(n,3); an n-body sign phase for n>=4 is impossible within that CCZ-only subclass. For *arbitrary H–CCZ circuits*, if h is the number of H gates, the matrix is 2^(-h/2) times an integer matrix; **equivalent circuits must have the same H-count parity**, and same-parity candidates admit exact integer-matrix comparison.

The verifier explicitly rejects omitted borrowed-ancilla compensation, treating an unknown scratch qubit as clean, missing uncomputation, false shared-wire H/CCZ commutation and invalid/unsupported S/T/CZ gates.

## Reproduce

Run Python 3.11+ with no third-party dependencies:

```bash
python verify.py
python verify_independent.py
```

The first program applies actual H/CCZ matrices in an exact signed-integer amplitude representation and validates **8,184** basis inputs over n=3..12, 32 borrowed inputs, 321 ANF tests and negative cases. The independent program instead derives CCX from an integer 2x2 conjugation identity and uses reversible XOR/Boolean Möbius transforms to check **32,760** data inputs n=3..14, the borrowed case and diagonal ranks through n=9. The programs do not test against a conjectured identity derived from the same implementation.

## Documents

- [paper.tex](paper.tex): public, self-contained LaTeX proof edition. 
- [verify.py](verify.py) / [verify_independent.py](verify_independent.py): independent executable checks.
- [AUDIT.md](AUDIT.md): explicit source boundaries and adversarial cases.

A longer, independently compiled and visually inspected five-page paper and its full source/proof ZIP were also prepared for the current conversation.

## Prior art and release scope

Barenco et al., *Phys. Rev. A* **52**, 3457 (1995), https://doi.org/10.1103/PhysRevA.52.3457. Khattar and Gidney, *Quantum* **9**, 1752 (2025), https://doi.org/10.22331/q-2025-05-21-1752. Quantum equivalence checking has substantial prior work, including [MQT QCEC](https://github.com/munich-quantum-toolkit/qcec).

**Scientific status:** internally proved restricted identities and independent exact checks, not a novel asymptotically optimal H–CCZ compiler, complexity lower bound, quantum speedup, formal Lean verification or refereed breakthrough. 
