# Sharp Derivative Loss and Singular Sound-Speed Symmetrizers for Eulerian Dust–Radiation Cauchy Systems

**PHY-005 — a new Einstein–matter Cauchy-theory investigation**, separate from electron magnetohydrodynamics (PHY-001/002), lattice gauge theory (PHY-003), and Sol scalar topology (PHY-004).

## Exact mathematical findings

Consider comoving pressureless dust plus a separate, noninteracting barotropic perfect radiation fluid with p_r=rho_r/3, on a smooth FLRW background with both densities positive. In the orthonormal rest frame, freeze the principal coefficients of the standard Eulerian first-order density–velocity system. Its equations are:

    (delta_d)_t + div v_d = 0,       (v_d)_t = 0
    (delta_r)_t + div v_r = 0,       (v_r)_t + (1/3) grad delta_r = 0

For any nonzero spatial covector n, the 8×8 matter symbol has characteristic polynomial z^6 (z^2 - |n|^2/3), but zero-eigenvalue geometric multiplicity 5, not 6. A 2×2 nilpotent dust Jordan block persists in every direction. No bounded pointwise invertible change of these Eulerian unknowns can cure this principal-symbol failure.

The exact pressureless solution is v_d(t)=v_d(0), delta_d(t)=delta_d(0)-t div v_d(0). It obeys a bounded mixed Sobolev estimate delta_d in H^s and dust velocity in H^(s+1). **One derivative is sharp**: every H^(s+alpha) dust-velocity assumption with alpha<1 fails to yield a uniform same-index H^s bound on the evolved density. The radiation block independently conserves ||v_r||_Hs^2+(1/3)||delta_r||_Hs^2.

A positive dust sound speed c gives the symmetric longitudinal block [[0,1],[c²,0]] with best-condition-number positive symmetrizer diag(c²,1) and condition number **exactly c^(-2)** for 0<c<=1. Its Fourier propagator is cos(ckt)I-i sin(ckt) A_c/c; in the c->0 limit the dust Jordan shear returns. Uniform H^s propagation is lost as c->0.

Under separate smooth matter conservation, generalized-harmonic Einstein gauge constraints satisfy the **conditional** subsidiary equation box(C)_nu+R_nu^mu C_mu=0. This is not a construction of a smooth coupled solution.

## Files and reproduction

- [paper.tex](paper.tex): manuscript, full proofs, conditional Einstein harmonic constraints, and **Appendix A: Precise Mathematical Formulation of the Main Result**
- [verify.py](verify.py): **25 exact SymPy assertions** for the 3D characteristic, Jordan, radiation and pressure-regularization identities
- [verify_independent.py](verify_independent.py): separately coded **standard-library exact Fraction** Gaussian elimination and matrix arithmetic
- [AUDIT.md](AUDIT.md): limitations, structural counterexamples and proof boundaries
- [PDF_FILENAME.txt](PDF_FILENAME.txt): title-named compiled PDF
- [requirements.txt](requirements.txt): SymPy pinned to 1.14.0

Reproduce:

    python -m pip install -r requirements.txt
    python verify.py
    python verify_independent.py

GitHub Actions runs both verifiers for every commit, then compiles the full PDF.

## Prior art and scientific classification

**Known conceptual ingredients**: pressureless Euler is weakly hyperbolic (Bouchut–Jin–Li, SIAM J Numer Anal 2003); Friedrich (Phys Rev D 1998) established a Lagrangian symmetric-hyperbolic Einstein–fluid formulation including dust; Normann–Valiente Kroon (Gen Rel Grav 2020) developed an Einstein–matter frame formulation and constraint propagation; Hadzic–Speck (J Hyperbolic Differ Equat 2015) solved substantial nonlinear Einstein–dust stability questions despite derivative loss.

**Claim:** a precise, self-contained, exact and independently reproduced *Eulerian frozen-principal* obstruction and regularization benchmark. **Not claimed:** new weak hyperbolicity phenomenon, all-gauge Einstein–matter no-go, nonlinear dust-radiation existence theorem, physical radiation transport, Einstein–Boltzmann cosmology, or a new astrophysical prediction. Originality of this specialized packaging remains unverified.

## Next meaningful goal

Construct a constraint-propagating, Lagrangian or mixed-regularity **fully evolving** Einstein–dust–radiation formulation, prove a closed nonlinear energy estimate and then add a conservative photon kinetic/Thomson sector. The present frozen-symbol result alone does not solve that problem.
