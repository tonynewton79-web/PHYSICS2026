# PHY-005 — Independent proof-state and scientific-priority audit

## Scope fixed before testing

Spacetime signature (-,+,+,+), c_light=1. Exact equations are Einstein with separate perfect-dust and barotropic-perfect-radiation tensors, dust pressure 0, radiation p=rho/3, each tensor conserved. Background is a smooth co-moving FLRW solution with strictly positive component densities. The mathematical tests concern **local orthonormal frozen coefficients** and a **standard first-order Eulerian density/velocity principal grammar**. Radiation is not a photon kinetic distribution or Thomson-scattering closure. Einstein harmonic gauge source is required to be algebraic in metric, with no matter-derivative dependence.

## Core proofs (complete in paper.tex)

1. Covariant conservation decomposes into u·grad rho + (rho+p) div u=0 and (rho+p)u·grad u+projection grad p=0. Freeze at a positive-density common-rest event and scale the two density perturbations by rho_d and rho_r+p_r, respectively. Obtain the 8-equation fluid principal system.
2. For nonzero direction n, the dust 4×4 symbol is a rank-one nonzero nilpotent matrix with square zero; radiation 4×4 symbol has ±|n|/sqrt(3) longitudinal eigenvalues and two transverse zeros. Therefore det(zI-A)=z^6(z²-|n|²/3), rank(A)=3, dim ker(A)=5, and the zero root has algebraic multiplicity 6. This proves a genuine Jordan defect. Similarity under a bounded pointwise invertible change cannot remove it.
3. A first-order generalized harmonic Einstein wave reduction with independent metric derivative variables has no spatial derivatives of matter fields in the metric principal part (stress is algebraic) and no spatial derivatives of metric first-order variables in the matter principal part (metric Christoffel terms become lower order). The matter Jordan defect is thus inherited by that specified coupled unconstrained **principal symbol**. This is not a universal theorem about Lagrangian formulations or constraint-restricted Einstein dynamics.
4. The exact frozen dust solution is v(t)=v(0), delta(t)=delta(0)-t div v(0). Fourier multiplier bound gives one derivative sufficient. For initial longitudinal v_N amplitude (1+N²)^(-(s+alpha)/2), H^(s+alpha) velocity norm is one while H^s density(t) equals |t| N(1+N²)^(-alpha/2); it diverges for every alpha<1. This is exact, not a finite numerical scaling fit.
5. Radiation energy (1/3)||delta_r||² + ||v_r||² is conserved by integration by parts in any H^s.
6. For positive artificial dust sound speed c, A_c=[[0,1],[c²,0]]. H_c=diag(c²,1) is positive symmetrizer, with condition number c^-2. Any Hermitian positive symmetrizer H must have h11=c² h22, and Rayleigh quotients imply cond(H)>=c^-2; c=0 forces h11=0 and positivity fails.
7. Since A_c²=c²I, the propagator is cos(ckt)I-i sin(ckt)A_c/c. Pointwise c->0 yields dust Jordan shear. For fixed t>0 choose integer N nearest pi/(2ct), giving same-index multiplier norm >=cos(ct/2)/c. Hence no uniform sound-speed-independent diagonalization estimate.
8. Reduced trace-reversed Einstein equations with harmonic constraint C, plus covariant stress conservation, imply the homogeneous subsidiary wave equation box(C)_nu+R_nu^mu C_mu=0 by trace, contracted Bianchi and Ricci commutator. Zero C and zero normal derivative propagate **conditionally** if a smooth reduced solution exists.

## Adversarial controls / counterexamples

- Dust symbol nonzero Jordan at all directions n!=0; radiation has real ±acoustic speeds and transverse zero eigenvalues, but cannot cure dust Jordan rank defect.
- Adding positive dust sound speed restores strong hyperbolicity, but the best available pointwise positive symmetrizer condition number diverges c^-2, and the Fourier evolution multiplier diverges c^-1 at fixed t as c->0.
- A derivative-dependent or nonlocal variable transformation may change the PDE order or unknown topology; the pointwise similarity obstruction does NOT apply to that broader class.
- Lagrangian Einstein–dust reductions are known to be symmetric hyperbolic: the manuscript does not claim otherwise.
- A conditional harmonic gauge subsidiary equation does not independently prove Hamiltonian/momentum initial-data consistency or global/nonlinear existence.
- Dust caustics, pressure discontinuities, viscosity, kinetic photon distributions, Thomson collisions, and radiation anisotropic stress are outside the model.
- Background positive densities exclude vacuum dust interfaces; the density normalization would fail there.
- The Jordan issue is a *principal* frozen-coefficient property; nontrivial lower-order gravity and cosmological expansion terms are not evolved here.

## Two genuinely different verifiers

- Exact SymPy script: 25 asserted identities, including four rational unit directions (3D characteristic polynomial, nullity, minimal polynomial annihilator, radiation symmetrizer) and full c→0 propagator limit.
- Independent Fraction script: hand-coded rational Gaussian elimination, matrix multiplication, rank and chain checks, four rational directions, exact symmetrizers at c=1/10,1/5,1/2,1, and high-frequency growth tests at alpha=0,1/2,3/4. It does not import SymPy.
- These are regression controls; the analytical proof handles all directions, all Sobolev indices, all positive c<=1, and arbitrary finite times.

## Prior art and publication verdict

Bouchut–Jin–Li, SIAM J Numer Anal 41, 135–158 (2003) establishes pressureless weak hyperbolicity. Friedrich, Phys Rev D 57, 2317–2322 (1998), constructs Lagrangian symmetric-hyperbolic Einstein-fluid equations, including pressure-free matter. Normann–Valiente Kroon, Gen Rel Grav 52, 103 (2020), covers first-order Einstein–matter evolutions and constraint propagation. Hadzic–Speck, J Hyperbolic Differ Equat 12, 87–188 (2015), overcomes an exact derivative-loss obstacle in nonlinear Einstein–dust stability. Originality and specialist review remain unverified.

**Verdict: rigorous restricted principal-symbol and regularity benchmark; NOT a new full Einstein–matter Cauchy theorem or physics breakthrough.**
