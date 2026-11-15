# PHY-001 — Two-pass proof audit

## First pass: derivation

1. Start from B_t+curl((curl B) cross B)=0 with B=(a_y,-a_x,b).
2. Compute curl B=(b_y,-b_x,-Delta(a)). Fix the spatially constant gauge in a_t.
3. Derive a_t={a,b}; b_t={Delta(a),a}.
4. Let L=F(a,b,q), M=G(a,b,q), q=Delta(a). The time derivative of F contains F_q Delta{a,b}, which has third derivatives of b absent from {G,F}. Therefore F_q=0.
5. Match three independent gradient channels: F_a=G_a F_b-G_b F_a; F_b=G_q F_a; 0=G_q F_b. It follows F_b=0, and on F_a!=0, G_q=0 and G_b=-1.
6. The converse identity {-b+h(a), f(a)}=f'(a){a,b} is exact.

## Independent adversarial second pass

- A direct polynomial spatial-jet witness holds all state values and first derivatives fixed while varying b_yyy: a=a0+x+q0(x²+y²)/4, b=b0+s*y³/6. At the origin, Delta{a,b}=s. This independently rules out any F_q dependence.
- Saturate the two necessary polynomial equations by the assumption F_b != 0, implemented using an inverse variable. The exact Groebner basis is [1], independently showing the nondegenerate scalar grammar is inconsistent.
- Independently substitute a nonconstant f(a), h(a) to check the existence of the degenerate first-equation representation, so the no-go cannot be mistakenly read as forbidding every scalar identity.
- Verify the parent magnetic equation and exact nonlinear whistler directly using a three-dimensional curl, separately from the reduced derivation.
- Check Fourier determinant of the linearized two-field system.

## Scope and caveats

The theorem concerns a single scalar evolution identity L_t={M,L} whose two potentials depend only on pointwise (a,b,Delta a); the spectral variable is a parameter. It does not prove nonintegrability, absence of complete integrability, absence of a matrix Lax pair, or impossibility of richer spectral schemes. It makes no global-in-time existence assertion.

The reduced equation and nonlinear whistler are established prior art. The restricted classification is internally proved but may have antecedents. No human peer review, priority determination, or formal Lean certificate is claimed.

## Reproduction

Python 3.11+ and SymPy 1.14.0. Run verify.py and require all checks to pass. No floating-point input is used. The tests are finite exact consistency checks; the mathematical proof of universal quantification remains the manuscript.
