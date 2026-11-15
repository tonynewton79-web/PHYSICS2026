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
