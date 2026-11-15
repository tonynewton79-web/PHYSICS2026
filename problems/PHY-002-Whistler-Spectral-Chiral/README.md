# PHY-002: Whistler spectral square class and nonlinear chiral coupling

**Scope:** Ideal inertia-free 2.5D electron magnetohydrodynamics, periodic perturbations around a constant in-plane magnetic field.  
**Evidence tier:** INTERNAL PROOF (restricted theorems; originality and external peer review not established).  
**Physics claim:** No new experimental physics, no full nonlinear Lax representation and no general nonintegrability theorem.

## Scientific results

1. The exact linearized local 2×2 EMHD Fourier generator has characteristic polynomial `z²+B0² kx²(kx²+ky²)`. It cannot be diagonalized by an invertible matrix of rational Fourier symbols in two formal wavevector variables. Its minimal splitting field adjoins `sqrt(kx²+ky²)`.
2. Chiral variables `w± = beta ± sqrt(-Delta) psi` diagonalize the linear system, but the nonlinear system generically leaks between them.
3. For two Fourier modes `p,q` in one chiral sector, the coefficient generated at `p+q` is `A C (p×q)(|p|-|q|)(|p|+|q|-|p+q|)`. For nonzero amplitudes it vanishes exactly for collinear or equal-length modes.
4. Equal-radius Fourier shells admit exact, potentially noncollinear, arbitrary finite-amplitude Beltrami-whistler solutions. This belongs to known whistler/Beltrami physics and serves as a positive control.
5. A restricted point-potential flatness calculation is retained only as a brief example of standard zero-curvature jet reasoning. In line with Professor Morozov's criticism, **it is no longer asserted as an independent theorem**; the general context is attributed to Marvan (1993, 2002). It does not obstruct derivative-dependent or nonlocal Lax representations.

## Reproducible source and checks

- [Complete LaTeX paper](paper.tex)
- [Exact SymPy verifier](verify.py) — 16 exact checks of symbols, chirality and nonlinear wave residuals
- [Independent standard-library verifier](verify_independent.py) — 2,304 integer mode-pair checks plus exact edge cases
- [Audit and prior-art limitations](AUDIT.md)
- [Requirements](requirements.txt), [PDF manuscript filename](PDF_FILENAME.txt)

Run:

```bash
python -m pip install -r requirements.txt
python verify.py
python verify_independent.py
```

GitHub Actions runs the exact main verifier and compiles the manuscript; the independent verifier is run in the paper-level audit and may be run directly as shown.

## Relevant established research

- [Qirui Peng, arXiv:2605.20845](https://arxiv.org/abs/2605.20845) — 2.5D EMHD reduction with dissipation.
- [Maxim Lyutikov, Phys. Rev. E 88, 053103 (2013)](https://doi.org/10.1103/PhysRevE.88.053103) — nonlinear harmonic whistlers and interactions.
- [O. I. Morozov, Analysis and Mathematical Physics 15, 120 (2025)](https://doi.org/10.1007/s13324-025-01119-w) — Lax representations and Poisson structures for reduced and ideal MHD; related techniques, but not an explicit construction for the EMHD system of this paper.
- M. Marvan, *On zero-curvature representations of partial differential equations*, in *Differential Geometry and Its Applications* (Opava conference, 1992), Silesian University (1993), pp. 103–122 — foundational jet-space, gauge and ZCR framework.
- [M. Marvan, *On the horizontal gauge cohomology and nonremovability of the spectral parameter*, Acta Appl. Math. 72, 51–65 (2002)](https://doi.org/10.1023/A:1015218422059) — spectral-parameter removability and gauge cohomology.
- [D. Shaikh, J. Plasma Phys. 75, 117–132 (2009)](https://doi.org/10.1017/S0022377808007198) — whistler propagation theory.

## Expert-feedback revision (15 November 2026)

Professor Oleg Morozov identified the original Section 5 result as a straightforward corollary of prior zero-curvature work by M. Marvan and indicated that Lax representations with non-removable parameters for the EMHD equations could be constructed using methods akin to his own. The manuscript now removes the independent-theorem treatment of Section 5, cites bibliographically verified Marvan works, and makes clear that our rational Fourier diagonalization barrier is **not** a nonlinear Lax obstruction. The precise Marvan paper described in correspondence as written in 1991 has not yet been identified conclusively; the verifiable Opava paper appeared in 1993 (conference 1992). No explicit Morozov-style EMHD Lax pair or proof of non-removability is included here.

## Outstanding work

Construct and verify an explicit derivative-dependent or nonlocal Lax representation for **both complete nonlinear EMHD equations**, including a full admissible gauge/covering-equivalence analysis and an independent compatibility certificate. Determine what it implies beyond known EMHD conservation and energy-transfer identities. This manuscript neither proves nor excludes such representations.
