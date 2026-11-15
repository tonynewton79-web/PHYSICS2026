# Eulerian Hyperbolicity Obstructions and Nonlinear Material-Frame Repairs for Einstein–Dust–Radiation Cauchy Systems

**PHY-005 — a new Einstein–matter Cauchy-theory investigation**, separate from electron magnetohydrodynamics (PHY-001/002), lattice gauge theory (PHY-003), and Sol scalar topology (PHY-004).

## Exact mathematical findings

Consider comoving pressureless dust plus a separate, noninteracting barotropic perfect radiation fluid with p_r=rho_r/3, on a smooth FLRW background with both densities positive. In the orthonormal rest frame, freeze the principal coefficients of the standard Eulerian first-order density–velocity system. Its equations are:

    (delta_d)_t + div v_d = 0,       (v_d)_t = 0
    (delta_r)_t + div v_r = 0,       (v_r)_t + (1/3) grad delta_r = 0

For any nonzero spatial covector n, the 8×8 matter symbol has characteristic polynomial z^6 (z^2 - |n|^2/3), but zero-eigenvalue geometric multiplicity 5, not 6. A 2×2 nilpotent dust Jordan block persists in every direction. No bounded pointwise invertible change of these Eulerian unknowns can cure this principal-symbol failure.

The exact pressureless solution is v_d(t)=v_d(0), delta_d(t)=delta_d(0)-t div v_d(0). It obeys a bounded mixed Sobolev estimate delta_d in H^s and dust velocity in H^(s+1). **One derivative is sharp**: every H^(s+alpha) dust-velocity assumption with alpha<1 fails to yield a uniform same-index H^s bound on the evolved density. The radiation block independently conserves ||v_r||_Hs^2+(1/3)||delta_r||_Hs^2.

A positive dust sound speed c gives the symmetric longitudinal block [[0,1],[c²,0]] with best-condition-number positive symmetrizer diag(c²,1) and condition number **exactly c^(-2)** for 0<c<=1. Its Fourier propagator is cos(ckt)I-i sin(ckt) A_c/c; in the c->0 limit the dust Jordan shear returns. Uniform H^s propagation is lost as c->0.

Under separate smooth matter conservation, generalized-harmonic Einstein gauge constraints satisfy the **conditional** subsidiary equation box(C)_nu+R_nu^mu C_mu=0. This is not a construction of a smooth coupled solution.

## Nonlinear continuation: an exact matter-sector repair, not a complete Einstein Cauchy theorem

For **irrotational geodesic dust before caustics**, choose synchronous material coordinates with metric -dτ²+h_ij(τ,X)dX^i dX^j and u_d=∂τ. The *exact fully nonlinear* dust conservation law reduces to

    ∂τ m(X)=0,  m=ρ_d sqrt(det h),  ρ_d=m(X)/sqrt(det h).

Allow radiation to have a **separate tilted four-velocity** u_r=γ(n+v), with γ=(1-|v|²)^(-1/2), |v|<1, and sound speed cs=1/sqrt(3). In an orthonormal radiation velocity-tangent basis, the radiation principal matrices are symmetric and the time-matrix eigenvalues are

    γ, γ, γ(1-cs|v|), γ(1+cs|v|).

These are positive for every strictly subluminal tilt. Consequently the **combined material-dust plus tilted-radiation subsystem** is locally symmetrizable hyperbolic on a *prescribed smooth metric*, with the dust mass label contributing a trivial positive one-dimensional time block.

The paper now also writes the full nonlinear Einstein ADM sources, including the **nonzero radiation momentum flux** J_i=(4/3)ρ_r γ² v_i, and proves **conditional** Hamiltonian and momentum constraint propagation by the contracted Bianchi identity. The exact homogeneous FLRW dust+radiation equations provide a nonlinear positive control.

### Why the complete problem is still open

The raw synchronous ADM metric subsystem admits high-frequency gauge modes and cannot be declared strongly hyperbolic merely by coupling it to a symmetric matter block. In a curvature/frame Einstein reduction, the Schouten/Cotton source contains derivatives of the **tilted radiation stress**, which introduce off-diagonal principal couplings requiring a new symmetrizer, auxiliary fields, and a full torsion/frame/gauge constraint closure.

The missing result is therefore **one unified nonlinear strongly hyperbolic gravitational + material system**, not the material repair by itself. Separate prior art includes Friedrich (1998), Normann--Valiente Kroon (2020), Walton's symmetric relativistic Euler treatment (2005), and Fournodavlos--Marshall--Oliynyk's July 2026 tilted two-positive-sound-speed theorem; that 2026 result does **not** include a pressureless dust species at cs=0. No originality, full two-velocity Einstein existence theorem, numerical coupled evolution or CMB prediction is claimed here.

## Files and reproduction

- [paper.tex](paper.tex): manuscript, full proofs, conditional Einstein harmonic constraints, and **Appendix A: Precise Mathematical Formulation of the Main Result**
- [verify.py](verify.py): **25 exact SymPy assertions** for the 3D characteristic, Jordan, radiation and pressure-regularization identities
- [verify_independent.py](verify_independent.py): separately coded **standard-library exact Fraction** Gaussian elimination and matrix arithmetic
- [verify_material.py](verify_material.py): symbolic Lorentz-frame, radiation positivity, nonlinear FLRW constraint and synchronous gauge-mode checks
- [verify_material_independent.py](verify_material_independent.py): independently derived exact Fraction cross-checks
- [AUDIT.md](AUDIT.md): limitations, structural counterexamples and proof boundaries
- [PDF_FILENAME.txt](PDF_FILENAME.txt): title-named compiled PDF
- [requirements.txt](requirements.txt): SymPy pinned to 1.14.0

Reproduce:

    python -m pip install -r requirements.txt
    python verify.py
    python verify_independent.py
    python verify_material.py
    python verify_material_independent.py

GitHub Actions runs all four verifiers for every commit, then compiles the cumulative PDF.

## Prior art and scientific classification

**Known conceptual ingredients**: pressureless Euler is weakly hyperbolic (Bouchut–Jin–Li, SIAM J Numer Anal 2003); Friedrich (Phys Rev D 1998) established a Lagrangian symmetric-hyperbolic Einstein–fluid formulation including dust; Normann–Valiente Kroon (Gen Rel Grav 2020) developed an Einstein–matter frame formulation and constraint propagation; Hadzic–Speck (J Hyperbolic Differ Equat 2015) solved substantial nonlinear Einstein–dust stability questions despite derivative loss.

**Claim:** a precise, self-contained, exact and independently reproduced *Eulerian frozen-principal* obstruction and regularization benchmark. **Not claimed:** new weak hyperbolicity phenomenon, all-gauge Einstein–matter no-go, nonlinear dust-radiation existence theorem, physical radiation transport, Einstein–Boltzmann cosmology, or a new astrophysical prediction. Originality of this specialized packaging remains unverified.

## Next meaningful goal

Build a unified, constraint-propagating, strongly hyperbolic **dynamical Einstein + material-dust + tilted-radiation** first-order reduction, including the curvature--stress derivative couplings. Prove a closed nonlinear energy estimate and only then add a photon kinetic/Thomson sector. The completed nonlinear **matter-sector** repair is necessary but does not solve that coupled gravitational PDE problem.
