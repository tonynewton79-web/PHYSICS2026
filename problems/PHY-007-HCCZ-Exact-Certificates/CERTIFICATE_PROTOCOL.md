# PHY-007 proof-carrying H–CCZ certificate protocol

Protocol tag: phy007-phase-pcc-v1.

The only certified action is an explicitly listed XOR of Boolean
monomials of degree >=3, with clean wires initialized and returned to
zero and borrowed wires arbitrary and restored exactly. An arbitrary
superposition, including a borrowed register entangled with an external
reference, is covered by the operator identity.

## Task and grammar

A task JSON object has exactly five fields: data_wires, monomials,
clean_capacity, borrowed_capacity and policy. The latter is one of
auto, clean_only or prefer_borrowed. Each monomial is a list of
distinct data-wire indices of length at least three. Repetition
between monomial entries cancels modulo two.

A certificate JSON object contains schema, task, canonical_terms,
blocks, gates, resources, certificate_semantics and sha256. Each
block carries term, scheme, start, stop, clean_used and borrowed_used.
Start and stop delimit contiguous half-open intervals in the gate
list. The permitted gates are ["H",wire] and
["CCZ",control1,control2,target], with no duplicated CCZ wires.
A valid lowered H–CCZ–H block must act on the same Hadamard
target on both sides, which is one exact CCX gate.

The resource record contains ccz, h, serial_depth, clean_peak,
borrowed_peak, physical_wires and block_count.
The semantics field must literally be
"exact on clean=zero, arbitrary borrowed".

The SHA-256 field is the digest of the object excluding that field
under sorted-key compact-separator ASCII JSON canonicalization.
It detects modifications but is **not a mathematical certificate
or a digital signature**.

## Independent semantic soundness check

The checker does not import the compiler and does not trust
compiler-provided expected circuit actions. It constructs exact
Boolean ANF polynomials from the *actual* H–CCZ gate sequence.

Every initial data and borrowed bit is a distinct Boolean variable;
every initial clean bit is the constant zero. CCZ adds the product
of the current three input-bit polynomials to an accumulating sign
polynomial. The contiguous H-target/CCZ/H-target operator is exactly
CCX and updates its target bit by XOR of the two control polynomials.

The checker requires every block to (i) restore every output bit
polynomial to its pre-block value, (ii) contribute precisely the
monomial claimed in the input phase polynomial, (iii) touch exactly
the declared clean and borrowed wires, and (iv) meet independently
counted H and CCZ costs. It recomputes canonical XOR source
cancellation from the original task, checks contiguous block coverage
and no trailing gates, and verifies the total polynomial.

The result CERTIFIED means these checks passed. By uniqueness of
Boolean ANF and exactness of H–CCZ–H = CCX, the gate sequence has the
claimed quantum operator action on every permitted basis state.
Linearity proves the same identity on all superpositions and
externally entangled borrowed states.

The checker is currently trusted Python code tested separately
against exact gate-amplitude simulation; it is **not** a mechanized
Lean or Coq checker, and the compiler source code is untrusted.

## Fail-closed status and resource limits

- CERTIFIED: accepted and verified under the stated contract.
- REJECTED: malformed or false contract, phase, gate or resource claim.
- UNSUPPORTED: unmatched/general Hadamard grammar, unsupported gates
  or exceeded symbolic resource limits; no assertion of incorrectness.

The checker currently caps data wires at 256, all wires at 1024,
gate count at 200,000 and intermediate ANF terms at 8,192.

Let t3 denote cubic terms, C the set of noncubic clean-ladder terms,
and b4 the number of borrowed-ancilla quartic terms. Exact counts
of this **specific serial circuit** are

    CCZ = t3 + sum_{S in C}(2|S|-5) + 4*b4
    H   = 4*sum_{S in C}(|S|-3) + 4*b4
    clean scratch = max_{S in C}(|S|-3), default zero
    borrowed scratch = 1 if b4>0, else zero
    serial depth = CCZ + H

These are valid constructive bounds, **not optimality bounds**.
The explicit polynomial input support can itself be exponential in
the number of data wires. No device routing, T-count, noisy circuit
fidelity, arbitrary-unitary equivalence or general compiler
optimization is certified.

## Prior art

Hietala et al., A Verified Optimizer for Quantum Circuits (2023);
Khattar–Gidney, Rise of Conditionally Clean Ancillae (2025);
Laabs, AlchemQ, arXiv:2609.19160 (2026);
Li et al., Formal Verification of Quantum Ancilla Safety,
arXiv:2608.13099 (2026).

This restricted protocol does not claim first discovery of
proof-carrying compilation or ancilla-safety verification.
