# PHY-007 — Exact equivalence and ancilla contracts in Hadamard–CCZ quantum circuits

**Author:** Tony Newton · tony.newton79@gmail.com

## Main results

For every integer n>=3, the n-body phase (-1)^(x0 ... x(n-1)) is realized by an explicit Toffoli-compute, central-CCZ and reverse-uncompute construction using **n-3 clean ancillas**, **2n-5 CCZ** gates and **4(n-3) Hadamards**. These are constructive upper bounds, not claimed optimality.

For four data qubits, a *separate borrowed-ancilla* circuit implements the same four-body phase on **all five-qubit input states**, leaving one unknown auxiliary qubit completely unchanged: CCX(0,1;4), CCZ(4,2,3), CCX(0,1;4), CCZ(4,2,3). Each CCX is compiled to H-target, CCZ, H-target, giving four CCZ and four H total.

For CCZ-only diagonal circuits the Boolean phase has a **unique cubic algebraic normal form**, and the group has rank binomial(n,3); an n-body sign phase for n>=4 is impossible within that CCZ-only subclass. For *arbitrary H–CCZ circuits*, if h is the number of H gates, the matrix is 2^(-h/2) times an integer matrix; **equivalent circuits must have the same H-count parity**, and same-parity candidates admit exact integer-matrix comparison.

The verifier explicitly rejects omitted borrowed-ancilla compensation, treating an unknown scratch qubit as clean, missing uncomputation, false shared-wire H/CCZ commutation and invalid/unsupported S/T/CZ gates.


## Shared-prefix synthesis with temporary DATA borrowing

For a family of m>=2 distinct three-variable suffixes having the same
prefix of k>=3 data controls, the new circuit computes the prefix
conjunction just once. During each compensated four-body phase it borrows
an **existing prefix data qubit**, restoring that data qubit immediately.
Finally the common conjunction is uncomputed. **No additional dirty
physical qubit is needed.**

| Resource | Previous independent clean ladders | Shared prefix |
|---|---:|---:|
| CCZ | m(2k+1) | 2(k-1)+4m |
| H | 4km | 4(k-1)+4m |
| Clean ancillas | k | k-1 |
| Additional borrowed qubits | 0 | 0 |
| Total physical qubits | n+k | n+k-1 |

The exact gate savings are m(2k-3)-2(k-1) CCZ and
4(k-1)(m-1) H, strictly positive for all k>=3,m>=2.
This is a **strict Pareto improvement over PHY-007's previous
independent clean-ladder compiler**, NOT a general best-known
ancilla/gate bound. Khattar--Gidney (2025), Dutta et al. (2025),
SPARE (2025), Lee--Kang (2026) and Jung et al. (2026) are relevant
prior art and preclude a blanket novelty claim.

New independently reproducible files:

- [shared_prefix_compiler.py](shared_prefix_compiler.py): untrusted compiler.
- [verify_shared_prefix.py](verify_shared_prefix.py): independent GF2 ANF
  semantic checker; does not import compiler code.
- [verify_shared_prefix_suite.py](verify_shared_prefix_suite.py): 266
  certified circuit cases, 1,408 exact H/CCZ basis-amplitude checks
  using the earlier separate simulator, 14 rehashed/invalid-digest
  adversarial mutations rejected, and a 256-data-wire symbolic stress case.

Example input JSON:

    {"data_wires":11,"prefix":[0,1,2,3],
     "tails":[[4,5,6],[4,7,8],[5,9,10]],"clean_capacity":3}

Reproduce with these commands:

    python shared_prefix_compiler.py --task /tmp/phy007-shared-input.json --out /tmp/phy007-shared-certificate.json
    python verify_shared_prefix.py /tmp/phy007-shared-certificate.json
    python verify_shared_prefix_suite.py

The checker replays the ACTUAL emitted H/CCZ gates, including complete
data and scratch restoration, rather than trusting synthesis templates.
Its proof uses exact gate semantics, not finite basis sampling.
It is tested independent Python code, not formally certified Lean/Coq.
The detailed mathematical proof is added to [paper.tex](paper.tex).
For k=4,m=3, counts improve from 27 CCZ/48 H/4 clean to
18 CCZ/24 H/3 clean, with no added borrowed qubits.

## Uniform proof-carrying compiler (restricted phase-polynomial language)

The new [proof_compiler.py](proof_compiler.py) emits H/CCZ circuits and
machine-readable certificates for explicit XORs of Boolean phase monomials
with degree >= 3. [verify_certificate.py](verify_certificate.py) is an
**independent executable proof checker**: it does **not** import the
compiler, trust its claimed semantics, or test its circuit against a
compiler-supplied expected matrix. Every accepted certificate is checked
through a separate exact Boolean algebraic normal-form (ANF) interpreter.

### Reproducible command line

Generate and verify a seven-body phase using four initialized scratch bits:

```bash
python proof_compiler.py --n 7 --term 0,1,2,3,4,5,6 --clean 4 --out /tmp/clean.json
python verify_certificate.py /tmp/clean.json
```

Generate and verify a four-body phase with **one borrowed qubit of
arbitrary unknown quantum state** and no clean scratch:

```bash
python proof_compiler.py --n 4 --term 0,1,2,3 --clean 0 --borrowed 1 --policy prefer_borrowed --out /tmp/borrowed.json
python verify_certificate.py /tmp/borrowed.json
```

For a compound source, repeat `--term`; duplicated monomials cancel
exactly modulo two. For a JSON task file, use
`python proof_compiler.py --task task.json --out certificate.json`.
Its required keys are `data_wires`, `monomials`,
`clean_capacity`, `borrowed_capacity` and `policy`.
Modes are `auto`, `clean_only`, or `prefer_borrowed`.

### Precise soundness and resource theorem

Let `T` be the canonical surviving monomials after F2 cancellation,
`C` the monomials of degree >=4 lowered by clean ladders,
`t3` the number of cubic monomials and `b4` the number
of quartic monomials lowered by the borrowed qubit. The emitted
circuit has **exact** serial gate counts

```text
CCZ = t3 + sum_{S in C}(2|S|-5) + 4*b4
H   = 4*sum_{S in C}(|S|-3) + 4*b4
depth_serial = CCZ + H
clean_scratch = max_{S in C}(|S|-3), default 0
borrowed_scratch = 1 if b4>0 else 0
```

These are valid **constructive upper bounds**, not optimality statements.
For all quantum input states on data and borrowed wires, including
borrowed wires entangled with external systems, the checked circuit
implements the exact target diagonal phase, returns every clean
ancilla to |0>, and returns every borrowed wire to its original state.

The checker parses the gates independently, recognizes the **exact**
H-target / CCZ / H-target identity as CCX, and symbolically propagates
Boolean expressions for **each output bit and accumulated sign**. Each
block must restore every bit, induce the indicated target monomial, and
satisfy its declared ancilla and resource contract. This method avoids
exponential basis enumeration for the generated family. The finite
checker imposes safety limits (256 data wires, 200,000 gates, 8,192
intermediate ANF monomials); larger instances are **UNSUPPORTED**,
not silently certified. The source list itself can be exponentially
long in the number of data wires.

The embedded SHA-256 digest checks file integrity only. A malicious
party can recompute it; **the independent semantic proof replay**
is what validates the claim. Unmatched/general H patterns,
unrecognized quantum gates, arbitrary input quantum programs and
general equivalence up to global phase are **outside** this limited
certificate grammar, even if some are perfectly correct.

### Verification and provenance

- [verify_proof_compiler.py](verify_proof_compiler.py) runs 112
  deterministic family/randomized instances, 1,712 independent exact
  H/CCZ amplitude-basis executions and 12 checksum-recomputed mutations,
  including missing borrowed compensation, altered gates, incorrect
  preconditions and resource counts.
- The isolated [GitHub Actions workflow](../../.github/workflows/phy007.yml)
  runs all three verifiers and emits independent machine-checked
  example certificate JSON files. Correct workflow link:
  [PHY-007 proof-carrying CI](https://github.com/tonynewton79-web/PHYSICS2026/actions/workflows/phy007.yml).
- [CERTIFICATE_PROTOCOL.md](CERTIFICATE_PROTOCOL.md) specifies the
  certificate language and trust model.

**Priority warning.** Verified circuit compilation is established
literature: Hietala et al.'s VOQC (2023), Khattar--Gidney (2025),
AlchemQ (arXiv:2609.19160, 2026) and formal ancilla safety work
(arXiv:2608.13099, 2026). The present tool is an intentionally
small H--CCZ phase-polynomial construction, not the first
proof-carrying quantum compiler, a verified general optimizer,
a Lean/Coq development or an optimal resource bound.


## Identical-workload matched-native-gate benchmark (16 November 2026)

The [five-page literature audit](PHY007_Matched_Workload_Literature_Audit.tex),
[reproducibility script](benchmark_matched.py), and
[methods/caveats](BENCHMARK_README.md) now compare seven **concrete native
H–CCZ circuit constructions** on the exact same phase polynomial:
a shared k-control prefix XORed across m distinct three-control tails.
All tested tails are disjoint from the prefix, and the canonical example
also has pairwise disjoint tails to remove hidden shared-subexpression
advantages. Every generated circuit is verified against the same
Boolean phase and each auxiliary-wire restoration contract.
A separate signed-integer-amplitude implementation checks actual
H and CCZ gates, not merely effective Toffolis.

### Canonical 13-data-qubit workload: k=4, m=3

| Native circuit | CCZ | H | Active clean scratch | Physical wires |
|---|---:|---:|---:|---:|
| Independent no-prefix-sharing, borrowed suffix | 30 | 48 | 3 | 16 |
| **Shared prefix with prefix-data borrowing** | **18** | **24** | **3** | **16** |
| Recycling a prefix intermediate | 19 | 32 | 3 | 16 |
| Barenco et al. (1995) Lemma 7.2 dirty cascade | 48 | 102 | 0 | <=16 |
| Independent full clean ladders | 27 | 48 | 4 | 17 |
| Shared prefix with additional clean suffix bit | **15** | **24** | 4 | 17 |
| Data-borrowing with idle fourth clean bit | 18 | 24 | 3 | 17 |

The published Barenco circuit was reconstructed as a native H–CCZ
implementation of Lemma 7.2's borrowed-work multi-controlled NOT
cascade. Its borrowed scratch wires are tested as **arbitrary unknown
inputs** and shown to be restored. It consumes no initialized
work qubits, unlike the three-clean-qubit data-borrowing scheme;
therefore this published comparator does **not** prove strict
fixed-precondition dominance. The classic-independent and no-sharing
rows are familiar elementary constructions, not attributed to
a newly published optimization algorithm.

With a shared k-prefix, exactly m distinct three-bit tails, and
k-1 initialized scratch wires, the resource formulas are:

- Data-borrowed shared prefix: CCZ=2(k-1)+4m; H=4(k-1)+4m.
- Recycled intermediate: CCZ=4k-6+3m; H=8k-12+4m.

The recycled construction uses fewer CCZ when m>2k-4 but
always uses 4k-8 more H (for k>=3). The two are a
**nontrivial Pareto tradeoff within the tested constructions**.
At one extra clean scratch bit, the shared-extra-clean
construction uses CCZ=2(k-1)+3m, H=4(k-1)+4m:
it consumes m fewer CCZ than the padded data-borrower
at the same *total* physical-wire allocation.

The completed [dedicated CI run](https://github.com/tonynewton79-web/PHYSICS2026/actions/runs/43783279201)
passed **14 workload instances × 7 circuits = 98**, including all
ancilla/restoration symbolic checks, **16,128 separate exact-amplitude
basis cases**, and a reproduced published Barenco dirty-ancilla
circuit. [Repository-wide PDF verification](https://github.com/tonynewton79-web/PHYSICS2026/actions/runs/43783279276)
also passed.

**Unresolved modern source-level comparison:** Khattar–Gidney
(Quantum, 2025), SPARE (PLDI 2025), and Lee–Kang (2026) do not yet
have independently obtained native H–CCZ circuits for these same
instances under matched allocation/restoration conditions.
Their reported Toffoli/relative-phase/Clifford+T or
conditional-ancilla costs cannot simply be equated to native
CCZ/H counts. A complete state-of-the-art comparison and a
priority/novelty theorem remain **OPEN**. No general optimality,
published-best claim, or universal Pareto dominance is implied.

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
