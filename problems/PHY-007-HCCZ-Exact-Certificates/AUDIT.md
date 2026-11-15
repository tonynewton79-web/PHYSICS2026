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
43773055923 passed 108 deterministic/randomized compiled instances,
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
