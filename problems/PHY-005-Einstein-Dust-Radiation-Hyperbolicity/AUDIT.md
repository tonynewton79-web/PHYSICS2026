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

## Attack 02 — nonlinear irrotational material gauge and tilted radiation

**New domain:** Smooth, positive-density, hypersurface-orthogonal geodesic dust whose worldlines form a noncaustic local material-coordinate foliation; radiation is a separate barotropic perfect fluid (not collisionless photons) with pressure rho_r/3 and a possibly tilted four-velocity. On a given synchronous metric g=-dτ²+h_ij(τ,X)dX^i dX^j, these matter equations are fully nonlinear, not frozen.

**Exact dust conservation:** u_d=∂τ and Γ^μ_{ττ}=0. Mass conservation is ∂τ(ρ_d sqrt(det h))=0, with positive fixed material mass m(X)=ρ_d sqrt(det h). Dust momentum conservation is automatic in this gauge. This replaces the *Eulerian matter* Jordan chain by a scalar zero-spatial-principal material label; it does not solve the metric evolution.

**Independent-velocity perfect-radiation equations:** For c_s=1/sqrt(3), σ=c_s log(rho_r/rho*)/(1+c_s²), radiation conservation is equivalent to u_r·∇σ+c_s div u_r=0 and u_r·∇u_{rν}+c_s(g_ν^μ+u_{rν}u_r^μ)∂μσ=0, with u_r·u_r=-1. For a local orthonormal frame (u_r,E_a), the symmetric *principal bilinear form* on the 4 radiation state variations is A(ξ)=[[u_r·ξ,c_s E_b·ξ],[c_s E_a·ξ,(u_r·ξ)I3]]. For material time covector τ, A^0 has exact eigenvalues γ twice and γ(1±c_s|v|). Positivity is strict whenever |v|<1. Smooth congruence into local velocity coordinates gives a genuine symmetrizer for the nonlinear radiation matter PDE. Dust mass transport adds a positive identity time block. This is strongly/symmetrically hyperbolic **only as the matter subsystem on a prescribed metric**.

**Tilted Einstein sources and constraints:** E=ρ_d+(4/3)ρ_r γ²-(1/3)ρ_r; J_i=(4/3)ρ_r γ² v_i; S_ij=(4/3)ρ_r γ² v_i v_j+(1/3)ρ_r h_ij. These are full nonlinear expressions. Spatial ADM equations are written explicitly and the Hamiltonian and momentum constraints contain both sources. Total stress conservation plus Bianchi gives a homogeneous subsidiary system, with principal part ∂τ H≈-2 D^i M_i, ∂τ M_i≈-(1/2) D_i H. It is symmetric after using (H,2M_i), so constraint propagation follows **conditional on existence of a smooth solution**.

**Nonlinear positive control:** Flat FLRW with H= a_dot/a, rho_d∝a^-3 and rho_r∝a^-4 solves the exact homogeneous Einstein–matter equations. Hamiltonian C=3H²-κ(rho_d+rho_r)-Λ obeys Cdot=0 under Hdot=-(κ/2)(rho_d+4rho_r/3), with κ=8πG.

**Adversarial gravitational gate:** Raw synchronous ADM is not itself a strongly hyperbolic first-order metric scheme: the constraint-satisfying vacuum linearization h_11=-2τ cos(NX^1), K_11=cos(NX^1), other components zero, obeys the linearized equations and constraints yet has |∂_1 h_11(τ)|/|K_11(0)|=2|τ|N in L2. This is a gauge mode of raw Gaussian ADM, and does NOT prove the same defect in every genuinely dust-material, constraint-augmented frame reduction.

**Unclosed source-derivative gate:** The Schouten tensor L_μν=(κ/2)(T_μν-T g_μν/3)+(Λ/6)g_μν obeys Cotton/Bianchi equations involving ∇_[α L_{β]ν}; this contains derivatives of the independently tilted radiation density/velocity. The full Einstein frame curvature principal matrix therefore has off-diagonal derivative couplings not present in the *given-metric matter* test. No combined positive symmetrizer, torsion/frame/gauge constraint propagation, general nonlinearly well-posed inhomogeneous Einstein evolution or ADM constraint-convergent numerical solution has been constructed here.

**Two more independent replay scripts:**
- verify_material.py uses exact SymPy Lorentz boosts for five rational velocity vectors, radiation A^μ symmetry and characteristic polynomials, relative acoustic speeds, nonlinear material volume conservation, nonlinear FLRW Hamiltonian propagation, symmetric ADM subsidiary principal matrices, and exact synchronous gauge-mode identities.
- verify_material_independent.py uses only Python Fraction arithmetic for five independently reconstructed boost tetrads, exact Schur positivity and tilted momentum flux, rational FLRW constraint propagation at three separate state points, and frequency-dependent Gaussian ADM gauge-mode growth through N=1009. It neither imports SymPy nor assumes the primary test matrix.

**Priority:** Friedrich's 1998 Lagrangian Einstein fluid theorem already includes pressureless dust; Walton's relativistic Euler symmetric system (2005) is earlier. Normann and Valiente Kroon (2020) use a Fermi-propagated frame with geometric auxiliary fields, but their published generic spatial-stress assumption does not directly authorize simply dropping a tilted radiation flux into a single-fluid dust closure. Fournodavlos, Marshall and Oliynyk (Ann. Henri Poincare, July 2026) establish symmetric-hyperbolic and global stability results for two positive-sound-speed fluids, with **strictly 1/3<K_a<5/7**, not the (K_d,K_r)=(0,1/3) endpoint. The new combination of formulas is not claimed historically original. No external expert review has occurred.

**Release verdict:** EXACT NONLINEAR MATERIAL DUST IDENTITY / TILTED RADIATION SYMMETRIZABLE SUBSYSTEM / CONDITIONAL EINSTEIN CONSTRAINT PROPAGATION; FULL COUPLED STRONGLY HYPERBOLIC EINSTEIN–DUST–RADIATION SYSTEM REMAINS OPEN.

## Attack 03 — complete frozen 26-field curvature–radiation principal certificate

**Source compatibility:** The source is the contracted Bianchi Cotton term ∇_[a L_{b]c} where L_{mu nu}=(κ/2)(T_{mu nu}-T g_{mu nu}/3)+(Λ/6)g_{mu nu}. Trace-free radiation contributes L^r=(κ/2)T^r. In the radiation rest frame, with sound speed c_s=1/sqrt(3), σ=c_s δrho/((1+c_s²)rho), b=2κrho/3, the linearized Schouten components are L00=b σ/c_s, L0i=-b v_i, Lij=b σ δij/(3c_s). Radiation Euler is σ_t=-c_s div v and v_t=-c_s grad σ, so EVERY spacetime derivative of these components is algebraic in the gradients S_i=∂iσ and V_ij=∂i v_j. The transverse Cotton component (∂x L_0y - ∂t L_xy)=-b V_xy is generically nonzero; it has not been discarded. Exact stress divergence ∂^μ L_{μν}=0 and trace ∂_α L^μ_μ=0 were independently checked.

**Uncorrected prior-work restriction:** A dust-frame stress decomposition T_ab=ρ n_a n_b+Π_ab with n^aΠ_ab=0 forces J_i=0. Tilted radiation has J_i=(4/3)rho_r gamma² v_i, generally nonzero. Normann--Valiente Kroon (2020) specifically require spatial Π; their general theorem cannot be substituted without an extension retaining heat flux. The auxiliary stress-derivative method itself is established prior art.

**Explicit Weyl STF matrices:** The five tensors B_i are diag(1,-1,0), diag(1,1,-2), e1e2+e2e1, e1e3+e3e1, e2e3+e3e2 (symmetric products). The Frobenius metric is D=diag(2,6,2,2,2). With (curl_n X)_ij=(epsilon_{kli} n_k X_jl+epsilon_{klj} n_k X_il)/2, the coordinate C_j satisfy C_j^T D = -D C_j exactly. The 10x10 Weyl electric/magnetic symbol W(n)=[[0,-C(n)],[C(n),0]] is Gram-symmetric and has charpoly z²(z²-|n|²)²(z²-|n|²/4)². The +/-half-light and zero branches include unconstrained Weyl components.

**Twenty-six-field principal:** Add four radiation fields U plus 3x4 independent spatial gradients W_i. In the local frozen rest frame, the scalar R(n)=c_s[[0,n^T],[n,0]] is symmetric and, after using Euler to eliminate temporal stress derivatives, the Bianchi Cotton source has zero derivatives of W_i. The whole frozen Weyl–radiation principal is A26(n)=diag(W(n),R(n),R(n),R(n),R(n)), with positive symmetrizer diag(D,D,I4,I4,I4,I4) and polynomial z^10(z²-|n|²)²(z²-|n|²/4)²(z²-|n|²/3)^4. At frozen nonzero tilt replace each R^mu with the radiation tetrad symmetric principal forms; its time eigenvalues are gamma twice and gamma(1±c_s|v|), positive for |v|<1. No claimed positivity extends to the unconstructed Einstein *connection/frame* variables.

**Actual homogeneous auxiliary constraints:** Z_i=W_i-∂iU and F_ij=∂iW_j-∂jW_i propagate under the SAME symmetric radiation operator ∂t+R^j∂j at constant coefficients. Both symbolic Fourier identities are explicitly evaluated, not merely asserted. Define P_(alpha|mu nu)=∂alpha L^r_mu nu algebraically using the listed 12 gradients; on Z=0 and Euler solutions the stress-jet constraints hold. Weyl divergence, geometric Einstein, torsion, moving-frame, harmonic, and material coordinate zero quantities have NOT been assembled into one homogeneous system.

**Nonlinear obstruction:** Covariant Euler differentiation gives A^mu ∇_mu W_i + (∇_i A^mu)W_mu + A^mu[∇_i,∇_mu]U=0, with curvature commutators algebraic in the Riemann tensor, but this identity alone does not supply the moving-frame connection equations, global first-order reduction or nonlinear energy estimate.

**Independent verification:**
1. A SymPy-only tool builds all five STF basis matrices, Gram D, every C_i, the 10x10 Weyl and 26x26 principal matrices in four spatial directions and four radiation velocities, their exact symmetries, positivity conditions, exact 10x10 characteristic polynomials, trace and divergence of all Schouten derivatives, a transverse nonzero Cotton coefficient, and actual symbolic gradient/curl constraint propagation. **139 exact checks passed** in the initial GitHub CI replay.
2. A separate Python Fraction-only tool reconstructs curl matrices from Levi-Civita coefficients, verifies Gram-skewness and the exact minimal annihilating polynomial, stress-divergence and transverse Cotton identities, the rational acoustic polynomial and commutation of the gradient/curl constraints. It imports no symbolic algebra package.
3. Both scripts are run by GitHub Actions together with the prior four exact verifiers, then the manuscript is compiled. Finite rational/symbolic checks support but do not replace the universal mathematical derivation.

**Release gate:** Coupled Weyl--radiation PRINCIPAL-SKELETON SYMMETRIZER CERTIFIED; HOMOGENEOUS RADIATION-GRADIENT SUBSIDIARY CERTIFIED; FULL EINSTEIN–DUST–RADIATION FIRST-ORDER REDUCTION AND ALL GEOMETRIC SUBSIDIARY CONSTRAINTS: HOLD / OPEN. No full nonlinear existence, constraint-convergent evolution, physically transported radiation, or novel gravity breakthrough asserted.

## Prior art and publication verdict

Bouchut–Jin–Li, SIAM J Numer Anal 41, 135–158 (2003) establishes pressureless weak hyperbolicity. Friedrich, Phys Rev D 57, 2317–2322 (1998), constructs Lagrangian symmetric-hyperbolic Einstein-fluid equations, including pressure-free matter. Normann–Valiente Kroon, Gen Rel Grav 52, 103 (2020), covers first-order Einstein–matter evolutions and constraint propagation. Hadzic–Speck, J Hyperbolic Differ Equat 12, 87–188 (2015), overcomes an exact derivative-loss obstacle in nonlinear Einstein–dust stability. Originality and specialist review remain unverified.

**Verdict: rigorous restricted principal-symbol and regularity benchmark; NOT a new full Einstein–matter Cauchy theorem or physics breakthrough.**
