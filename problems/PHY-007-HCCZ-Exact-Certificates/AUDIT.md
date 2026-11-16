# PHY-007 — proof and reproducibility audit

## Domain and contracts

Only H on one valid wire and CCZ on three pairwise distinct valid wires are allowed. Input circuits are exactly unitary, without measurement, complex phase gates, work/storage or hardware noise. Clean auxiliary qubits begin in |0> and end in |0>; borrowed qubits may have arbitrary initial quantum state and must be returned identically. Comparisons use strict matrix equality; global sign is considered only as a separate convention.

## Proof chains

1. H diag(1,(-1)^ab) H = X^ab establishes CCX exactly on all control/target values, including superpositions.
2. A clean chain a1=x0x1, aj=a_(j-1)xj through a_(n-3) produces the data conjunction; central CCZ with the final two bits adds the required phase. Reverse Toffoli chain restores every scratch. CCZ count 2(n-3)+1; H count 4(n-3). Count is constructive, not optimal.
3. For borrowed z, the two CCZ phases in the four-body circuit are (z XOR ab)cd and zcd. Their XOR is abcd; both Toffolis restore z. Thus the full five-wire matrix is P4 tensor identity, including arbitrary entanglement.
4. Every H adds an exact common 1/sqrt2 to integer amplitudes; CCZ is integer signs. U=2^(-h/2)M and opposite H-count parities cannot express equal nonzero matrices. When h counts match in parity, use integer powers-of-two normalization to compare columns. Not an efficient large-scale equivalence algorithm.
5. CCZ-only diagonal phase consists of degree-3 squarefree Boolean monomials. Unique algebraic normal form over F2 (Möbius inversion) proves rank binomial(n,3). A quartic or higher monomial cannot be generated *without H*. This does not bound ancilla-free H/CCZ circuits.

## Independent regression

Primary checker: exact signed integer basis simulation, n=3..12 all 8184 clean input strings, all 32 borrowed strings, 321 diagonal words, H parity, several wrong rewrites, gate validation. Second checker: independent 2x2 conjugation identity and XOR circuit interpreter, n=3..14 all 32760 clean data strings, all borrowed values, independent ANF n=3..9 and gate count n=3..99.

## Adversarial witnesses

- Omit final borrowed correction: (a,b,c,d,z)=(0,0,1,1,1) erroneously acquires minus phase.
- Reuse the clean circuit with nonzero scratch on the same data input: spurious phase.
- Omit uncomputation: all-ones data leaves nonzero scratch.
- Treat shared-line H and CCZ as commuting: matrix inequality.
- S/T/CZ unknown opcodes or repeated/negative indices: rejected rather than accepted.

## Prior art and limitations

Barenco et al. (1995) and Khattar/Gidney (2025) developed related generalized Toffoli and clean/dirty/conditionally-clean ancilla synthesis. Exact quantum circuit equivalence is a mature subject. The manuscript's proved restricted identities should be treated as transparent independently verified constructions, not an unqualified novel result. There is no Lean verification, formal proof of global optimality, quantum advantage, asymptotic complexity lower bound or implemented scalable compiler. Independent human peer review and exhaustive priority study remain open.


## Uniform proof-carrying phase-polynomial compiler (2026-11-15)

This continuation constructs a deterministic compiler for explicitly
enumerated Boolean phase polynomials with monomial degrees >=3,
emitting only H and CCZ. Source monomials are canonically XOR-cancelled,
then sequentially lowered by CCZ, clean-ladder, or borrowed-four-body
blocks. A clean scratch register is reusable after every proven
uncompute; therefore the actual clean scratch cost is the maximum
k-3 among clean-ladder terms, not the sum. Borrowed-four-body blocks
reuse a single unknown borrowed qubit, restored even if externally
entangled.

**Soundness statement:** Any certificate accepted by the separate
verify_certificate.py checker within its finite size limits implements
the source phase polynomial on the declared subspace and restores
all ancillas. This claim rests on the exact quantum identity
H-target CCZ H-target = CCX, exact GF2 algebraic normal form,
the check of every actual emitted block, and linearity. The checker
does not import the compiler or accept expected phases as evidence.
General unmatched H patterns are UNSUPPORTED, not disproved.

**Exact construction resources:** For cubic term count t3, clean
ladder terms C with degree >=4 and borrowed quartic count b4,
CCZ=t3+sum_C(2k-5)+4b4,
H=4 sum_C(k-3)+4b4,
clean=max_C(k-3) (zero if none), borrowed=1 if b4>0.
These are upper bounds of a serial schedule, not lower bounds,
hardware resource estimates, or proven optimal syntheses.

**Independent tests:** Dedicated GitHub Actions run
43773055923 passed 112 deterministic/randomized compiled instances,
1,712 exact basis-amplitude executions using the older, separate
H/CCZ integer simulator, 12 deliberately malformed/rehashed
certificates, and source/ancilla insufficiency rejections. It
also emitted two standalone sample JSON certificates and ran
the independent verifier CLI successfully. Previous original
PHY-007 tests were rerun. The complete continuous-integration
result confirms functional reproducibility, not Lean/Coq
formalization, historical priority or external specialist
proof review.

**Adversarial safety:** A recomputed SHA-256 digest does not bypass
semantic verification. Wrong or absent borrowed compensation,
changed CCZ operands, resource forgery, changed task, undeclared
clean/borrowed wires, unverified trailing gates, and unmatched
Hadamards are rejected or explicitly unsupported.
The checker enforces bounded symbolic resource limits, and may
decline to certify otherwise correct circuits.

**Publication priority:** Recent VOQC/Coq work (Hietala et al.,
2023), Khattar--Gidney (2025) on conditional ancillas,
AlchemQ (Laabs, arXiv:2609.19160, 2026) for proof-carrying
per-result equivalence certificates, and Li et al.
(arXiv:2608.13099, 2026) on ancilla safety are close prior art.
This work is a transparent narrow specialization, not a
generally novel proof-carrying quantum compiler.

**Unresolved:** arbitrary-unitary H/CCZ equality, context-sensitive
rewrites, ancilla-free high-degree synthesis, general dirty-ancilla
resource tradeoffs, authenticated signatures, verified checker
code in a proof assistant, fault-tolerant cost optimization,
hardware connectivity and noise.


## Shared-prefix/data-borrowed phase construction (15 November 2026)

A restricted family of m>=2 diagonal phase monomials with one
common k>=3 data prefix and distinct three-variable suffixes
admits a strict constructive improvement over PHY-007's
original independent clean-ladder synthesis. Compute
the AND of the prefix once using k-1 clean scratch wires.
For each three-variable suffix, apply the exact borrowed
four-body phase using the computed prefix scratch and
the three suffix variables as active operands, with the
**original first prefix data bit** as the temporary borrowed
target. The borrowed data bit is NOT one of the four
active phase operands: the computed prefix is stored in
a separate scratch wire. The four-body operator identity
acts as the identity on its borrowed wire even if
entangled with the computed conjunction. Return the
borrowed data bit after every phase, then uncompute the
common prefix ladder.

**Exactly proven resources:** CCZ=2(k-1)+4m,
H=4(k-1)+4m, clean=k-1, added borrowed qubits=0.
The previous independent clean-ladder baseline uses
CCZ=m(2k+1), H=4km, clean=k.
The exact savings m(2k-3)-2(k-1)>0 CCZ,
4(k-1)(m-1)>0 H, and one initialized/total
physical qubit hold for all k>=3, m>=2.
This is a strict Pareto improvement ONLY relative
to that specified prior PHY-007 compiler, not global
optimality against 2025-2026 cond-clean literature.

**Independent proof replay:** The untrusted
shared_prefix_compiler.py is interpreted by a distinct
verify_shared_prefix.py module importing no compiler
code. It symbolically tracks every data wire as an
independent GF2 ANF variable, every clean scratch as
zero, every actual CCZ phase, and every exact H-CCZ-H
reversible Toffoli update. It requires the original
data bits and all clean scratch bits to be returned,
the exact desired diagonal phase, and independent
recounting of gates/physical wires. Mutants with
recomputed SHA-256 digests are rejected. The separate
verify_shared_prefix_suite.py invokes the old signed-
integer exact H/CCZ simulator for smaller circuits.

**GitHub CI certificate:** 266 program instances
(including n=256 symbolic input), 1,408 actual
basis-amplitude executions, and 14/14 mutated
certificates rejected. A compiler-generated JSON
certificate for k=4,m=3 is also independently
verified by a distinct CLI invocation. These tests
support, but are not a substitute for, the written
general operator proof.

**External priority boundary:** Khattar--Gidney
(Quantum 2025) already have one-clean/two-clean
multicontrolled gates with strong linear counts;
Dutta et al. (PRA 2025), Lee--Kang (QIP 2026)
study depth-space tradeoffs; SPARE (PLDI 2025)
shares compute/uncompute structure; Jung et al.
(Constraints 2026) optimize multiple controls.
No claim is made that this particular borrowing
trick is historically new, a globally optimal
resource frontier, or a formally verified
Lean/Coq development.


## Matched-workload native-gate literature benchmark

The [five-page report](PHY007_Matched_Workload_Literature_Audit.tex)
and [standalone executable](benchmark_matched.py) were developed as
a direct challenge to PHY-007's conditional advantage. The unit of
comparison is *the exact same diagonal phase target* with a
k-control shared prefix and m distinct three-control suffixes.
All implementations use only native H and CCZ gates and are
checked for exact phase and every scratch-wire restoration.

**Reproduced published algorithm:** Barenco et al. (1995),
Lemma 7.2, provides a multi-controlled NOT using 4(c−2) Toffolis
and c−2 dirty work wires. We independently reconstructed its
four-pass alternating cascade, sandwiched the target with H
to realize controlled phase, then compiled each Toffoli to
H–CCZ–H. All *borrowed* work bits are represented by
independent Boolean variables, rather than assumed initialized.
The independent actual-amplitude H–CCZ simulator confirms
the operator on accessible small benchmark instances.

**Seven exact serial circuits:** no-prefix-sharing borrowed-suffix,
PHY-007 shared-prefix data borrowing, same-width recycling a
prefix intermediate, published Barenco dirty cascade,
traditional independent clean ladder, extra-clean shared-prefix
suffix, and zero-padded data-borrowing.

**Concrete canonical 13-data-qubit test (k=4,m=3):**
at 16 physical qubits, 3 active clean: shared data-borrowing
18 CCZ/24 H vs no-prefix-sharing 30 CCZ/48 H vs
recycled 19 CCZ/32 H. Published Barenco dirty method
48 CCZ/102 H but **zero initialized clean**; it therefore
does not match active-ancilla preconditions, although the
physical qubit allocation may be padded to match.
At 17 physical qubits, a four-clean shared suffix
needs only 15 CCZ/24 H, beating the padded data-borrowing
circuit's 18 CCZ/24 H, while using one additional initialized
scratch bit. Thus there is **no unconditional dominance**.

**Exact conditional trade-off for k>=3:** Recycled-prefix
CCZ=4k−6+3m vs PHY-007 borrow CCZ=2k−2+4m, so
recycling wins on CCZ for m>2k−4, loses on H
by 4k−8 for every k>=3. Data-borrowing and recycling
are distinct Pareto construction points. At a fixed
additional clean ancilla, 2k−2+3m CCZ shared-clean
phase synthesis beats the PHY-007 2k−2+4m count.

**Verification gate:** The [passing dedicated run](https://github.com/tonynewton79-web/PHYSICS2026/actions/runs/43783279201)
checked 14 source instances, seven circuits each (98
distinct circuits), all symbolic phase and ancilla-restoration
contracts, **16,128 independent exact H/CCZ amplitude
basis executions**, exact gate/wire counts and the published
Barenco source. Full repo CI [passed](https://github.com/tonynewton79-web/PHYSICS2026/actions/runs/43783279276).
The individual 98 gate/cost records and JSON metrics are
artifacts of the dedicated workflow.

**Unresolved/priority-sensitive:** Khattar–Gidney (2025),
SPARE (2025), and Lee–Kang (2026) have not been
faithfully instantiated as executable native H/CCZ
circuits for this identical workload under matching ancilla
rules. Their Toffoli-equivalent/relative-phase and
Clifford+T quantities cannot be translated by fiat.
Published prior art already treats controlled operations,
conditional ancillas and reuse. No full modern-state-of-the-art,
optimal lower bound or originality claim can be released.
