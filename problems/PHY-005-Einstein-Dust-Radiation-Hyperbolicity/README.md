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

## Attack 03: explicit curvature–radiation principal block, with auxiliary stress gradients

**Completed restricted theorem:** At a point of a background solution, freeze the metric/frame and radiation coefficients. The local ten-variable electric/magnetic Weyl block has STF curl symbol W(n)=[[0,-C(n)],[C(n),0]], where C(n) is the explicit 5×5 basis matrix of the trace-free tensor curl (given in the manuscript). In its basis the positive Weyl Gram symmetrizer is H_W=diag(D,D), D=diag(2,6,2,2,2), and W(n) has characteristic speeds 0, ±|n|/2, ±|n|.

The radiation perturbation U=(sigma,v1,v2,v3) obeys a symmetric acoustic principal equation with sound speed 1/sqrt(3). Introduce twelve extra variables W_i=∂_i U (i=1,2,3). In the radiation stress's Schouten tensor, **all first spacetime stress derivatives can then be written algebraically in W_i** after using the Euler equations to eliminate time derivatives. The stress Cotton source still exists, but it is *lower differential order* in the enlarged system.

The exact frozen **26-field** principal matrix is

    A(n) = diag(W(n), R(n), R(n), R(n), R(n)),

where R(n)=c_s[[0,n^T],[n,0_3]]. It has explicit positive symmetrizer

    H26 = diag(H_W, I4, I4, I4, I4).

The exact characteristic polynomial at a comoving background is

    z^10 (z^2-|n|^2)^2 (z^2-|n|^2/4)^2 (z^2-|n|^2/3)^4.

For a **frozen tilted radiation** state with |v|<1, each R^mu is replaced by the known symmetric relativistic-Euler principal block. Its time eigenvalues gamma twice and gamma(1±c_s|v|) are positive. This certifies the coupled **local curvature–radiation principal skeleton**, not the entire Einstein frame or its gauge.

The auxiliary gradient and curl constraints Z_i=W_i-∂_i U and F_ij=∂_i W_j-∂_j W_i satisfy *homogeneous acoustic subsidiary equations* in the constant-coefficient system. This does **not** prove propagation of geometric Weyl-divergence, torsion, tetrad, harmonic/dust-coordinate or complete Einstein constraints.

**Prior-art gate:** Normann--Valiente Kroon's existing symmetric-hyperbolic Einstein–matter construction introduces Z-type stress derivative fields, but its matter stress ansatz is spatial in the selected material frame. Independently tilted radiation carries nonzero dust-frame heat flux J_i=(4/3)rho_r gamma^2 v_i, so its theorem cannot be invoked unchanged. Derivative prolongation and Weyl curls are established methods; no new general-relativistic breakthrough is claimed.

### Exact Attack 03 scripts

- [verify_curvature_radiation.py](verify_curvature_radiation.py): SymPy STF Weyl curl matrices, 26×26 weighted symmetries, relative-tilt time positivity, stress/Schouten identities, and actual symbolic auxiliary-constraint propagation.
- [verify_curvature_radiation_independent.py](verify_curvature_radiation_independent.py): separate Fraction-only 5×5 STF curl reconstruction, Gram-adjoint/minimal-polynomial audit, rational stress derivatives, acoustic and constraint tests.

Run both after the four previous verifiers. GitHub Actions automatically executes all six and compiles the single cumulative paper.

### Remaining decisive proof gates

1. Specify all dust-adapted tetrad/frame and connection unknowns, including their derivative sources and gauge choices.
2. Certify one positive **combined gravitational + radiation + auxiliary jet** time symmetrizer in those equations, not only its 26-field Weyl–radiation subset.
3. Prove a homogeneous well-posed subsidiary system for **all** torsion, Weyl-divergence, Einstein, frame, gauge, stress-jet and material constraints, without tacit special initial constraints.
4. Close an inhomogeneous nonlinear energy estimate and local existence theorem, plus eventually a constraint-convergent numerical evolution.

**STATUS:** proved restricted combined principal skeleton + 30-field sourceful Weyl-divergence/radiation-jet subsidiary; complete Einstein–dust–radiation theorem remains OPEN.

## Attack 04: sourced Weyl divergence and 30-component homogeneous subsidiary

The previous curvature–radiation principal system alone only propagated the defining gradient constraints. This continuation now closes an additional **six genuine Weyl-divergence constraints** in the comoving, constant-coefficient *sourceful* model, without imposing a false vacuum divergence-free condition on radiation-sourced curvature.

Let E,H be the STF Weyl electric and magnetic fields, U=(sigma,v), and W_i=(S_i,V_ij) with S_i=∂i sigma and V_ij=∂i v_j. Let cs=1/sqrt(3), b=2κ rho_r/3 and define

    C_E,i = ∂^j E_ij − 2b cs S_i
    C_H,i = ∂^j H_ij − b epsilon_ijk V_jk

and the existing radiation-jet curl constraints F_ij=∂i W_j−∂j W_i and defining constraints Z_i=W_i−∂i U. With E_t+curl_STF H=−b STF(V), H_t−curl_STF E=0, and the prolonged acoustic system, the **exact subsidiary equations** are

    (C_E)_t + (1/2) curl C_H = (b/3) G(F)
    (C_H)_t − (1/2) curl C_E = 0
    (Z_i)_t + R^k ∂k Z_i = 0
    (F_ij)_t + R^k ∂k F_ij = 0

where [G(F)]_i=Σ_j (F_ij)_(velocity j). Importantly, the source G(F) is algebraic and **contains no derivative** of F. The full 30-variable principal is symmetric hyperbolic with identity symmetrizer; the exact algebraic map GG^T=2I gives, for each Sobolev index s,

    E_s(t) <= exp[sqrt(2)*|b|*|t|/3] E_s(0),

with E_s one half of the sum of squared H^s norms of C_E,C_H,Z_i,F_ij. Thus zero sourceful Weyl divergence and radiation-jet constraints propagate in this frozen model.

The theorem reconstructs all 24 components of the contracted Weyl Bianchi identity from the ten Weyl evolution equations plus six constraints, not just a selected projection. In vacuum, imposing divergence-free E,H on a nonzero Fourier mode removes the Weyl zero and half-light-speed branches, leaving exactly two physical light-speed polarizations (four real first-order field variables).

### New exact independent tests

- [verify_weyl_subsidiary.py](verify_weyl_subsidiary.py): independently reconstructs the 4-index Weyl tensor, checks all 24 sourced contracted-Bianchi residuals, both sourceful subsidiary identities, 30×30 spatial matrix symmetries and exact GG^T=2I.
- [verify_weyl_subsidiary_independent.py](verify_weyl_subsidiary_independent.py): implements the entire calculation again using only standard-library rational Fraction arithmetic, with a different density coordinate chi=sigma/cs, independently rebuilt Weyl tensors and a weighted 30×30 symmetrizer.

**Scope:** A new *restricted fixed-coefficient Weyl geometric-subsidiary certificate*, not a full nonlinear geometric constraint closure or complete Einstein Cauchy theorem. Nonlinear moving-frame, torsion, connection, gauge, dust and Einstein constraints remain open. The gravitoelectromagnetic constraint machinery and Weyl light-speed physical polarization restriction have major prior art, including van Elst–Ellis (1999), so this is a transparent exact reproducibility/extension benchmark, not an originality claim.

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
    python verify_curvature_radiation.py
    python verify_curvature_radiation_independent.py
    python verify_weyl_subsidiary.py
    python verify_weyl_subsidiary_independent.py

GitHub Actions runs all eight verifiers for every commit, then compiles the cumulative PDF.

## Prior art and scientific classification

**Known conceptual ingredients**: pressureless Euler is weakly hyperbolic (Bouchut–Jin–Li, SIAM J Numer Anal 2003); Friedrich (Phys Rev D 1998) established a Lagrangian symmetric-hyperbolic Einstein–fluid formulation including dust; Normann–Valiente Kroon (Gen Rel Grav 2020) developed an Einstein–matter frame formulation and constraint propagation; Hadzic–Speck (J Hyperbolic Differ Equat 2015) solved substantial nonlinear Einstein–dust stability questions despite derivative loss.

**Claim:** a precise, self-contained, exact and independently reproduced *Eulerian frozen-principal* obstruction and regularization benchmark. **Not claimed:** new weak hyperbolicity phenomenon, all-gauge Einstein–matter no-go, nonlinear dust-radiation existence theorem, physical radiation transport, Einstein–Boltzmann cosmology, or a new astrophysical prediction. Originality of this specialized packaging remains unverified.

## Next meaningful goal

Build a unified, constraint-propagating, strongly hyperbolic **dynamical Einstein + material-dust + tilted-radiation** first-order reduction, extending the now-certified 26-field Weyl–radiation principal block to the actual connection, frame and geometric constraints. Prove a closed nonlinear energy estimate and only then add a photon kinetic/Thomson sector. The completed nonlinear **matter-sector** repair is necessary but does not solve that coupled gravitational PDE problem.
