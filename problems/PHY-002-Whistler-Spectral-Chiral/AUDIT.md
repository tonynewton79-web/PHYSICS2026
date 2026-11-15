# PHY-002 — Proof and originality audit

## First pass: independent mathematical claims

**(A) Algebraic spectral barrier.** Over `K=C(kx,ky)`, `kx²+ky²=(kx+i ky)(kx-i ky)` has two distinct prime factors of odd valuation; it is not a square in K. Multiplication by the square `(i B0 kx)²` does not change square class (B0≠0). The characteristic polynomial is irreducible over K. Its roots lie in `K(sqrt(kx²+ky²))`, a degree-two extension. The explicit symbol matrix `S=[[s,1],[-s,1]]` diagonalizes whenever s≠0. The theorem is **not** a no-go for matrix evolution or general pseudodifferential Lax operators.

**(B) Exact Fourier defect.** With Fourier Jacobian bracket `{f,g}_k=-sum_(p+q=k)(p×q)f_p g_q`, the normal derivative of the subspace `beta=Lambda psi` is `D={Delta psi,psi}-Lambda{psi,Lambda psi}`. The raw ordered coefficient is `(p×q)(|p|²+|k||q|)`. Swapping p and q and averaging yields half of `(p×q)(|p|-|q|)(|p|+|q|-|k|)`. For a two-wave input, both orders restore the full pair coefficient. The nonzero condition is exact and uses the strict triangle inequality.

**(C) Real counterexample.** `psi=cos(x)+cos(2y)`, `beta=cos(x)+2cos(2y)`, so `D=(6-2sqrt(5))sin(x)sin(2y)`. Strict positivity follows from `9>5`. This is an instantaneous formal result; energy second derivative assumes an existing sufficiently smooth solution.

**(D) Equal-radius solutions.** On a Laplacian eigenfunction `Delta psi=-kappa² psi` with `beta=sigma kappa psi`, both quadratic brackets vanish identically. The proposed translation with speed `sigma B0 kappa` satisfies both PDE components exactly for arbitrary finite amplitude. This is a known-type Beltrami mechanism and is *not* an original nonlinear wave claim.

**(E) Point-potential matrix gate.** The spatial flatness equation contains independently selectable `psi_x,psi_y,beta_x,beta_y,q_x,q_y` with `q=Delta psi`. All U and V state derivatives vanish before using any temporal equation. Then xt and yt flatness force W constant in state, pairwise commutation. This grammar excludes spatial derivative dependent pure-gauge and nontrivial higher-jet constructions; it does not prove nonintegrability.

## Second pass: independent adversarial checks

- Exact symbolic verifier tests characteristic polynomial **and** minimal polynomial as matrices, the conjugating similarity **as a matrix identity**, all nonlinear channel signs, the factorized Fourier symbol, and travelling equal-radius waves for both helicities.
- Independent `verify_independent.py` uses only integer arithmetic and standard-library functions to test the Cauchy/Gram determinant and strict noncollinearity across 2,304 ordered nonzero integer vector pairs; it also reproduces positive leakage and the noncollinear equal-radius exception.
- Counterexample-first cases checked analytically: `B0=0` is outside the field-theorem hypotheses; `kx=0` is a degenerate dispersion branch; `k=0` makes Lambda noninvertible; collinear p,q, equal-radius p,q and p=-q have zero pairwise leakage; the amplitude product `AC` must be nonzero.
- Global cancellations among **many** Fourier interactions are possible. The theorem is a coefficientwise pair statement, not a classification of all chiral-invariant finite Fourier supports.
- The flatness gate is a generic unconstrained-spatial-jet fact, not a deep EMHD-specific phenomenon. Its assumptions exclude explicit derivative dependence and nonlocal coverings.

## Prior-art and publication calibration

The reduced model: Qirui Peng (2026, arXiv:2605.20845). Whistler turbulence, nonlinear harmonic whistlers and interactions: Maxim Lyutikov (2013, DOI 10.1103/PhysRevE.88.053103). Exact wave propagation: D. Shaikh (2009). Related Lax representations of **ideal MHD**, not EMHD: Oleg I. Morozov (2025, DOI 10.1007/s13324-025-01119-w).

No exhaustive originality search, expert independent review, or formal Lean proof was performed. The conclusions are exact but restricted. No general integrability verdict, new nonlinear whistler discovery, priority certificate or scientific breakthrough is claimed.

## Reproduction instructions

Run `python -m pip install -r requirements.txt`; `python verify.py`; `python verify_independent.py`. The numerical grid is only regression testing; the universal strict triangle and square-class arguments are in the written proof. The reader must assess those arguments independently.
