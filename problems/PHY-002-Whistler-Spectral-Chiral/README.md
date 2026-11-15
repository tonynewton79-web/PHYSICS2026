# PHY-002: Whistler spectral square class and nonlinear chiral coupling

**Scope:** Ideal inertia-free 2.5D electron magnetohydrodynamics, periodic perturbations around a constant in-plane magnetic field.  
**Evidence tier:** INTERNAL PROOF (restricted theorems; originality and external peer review not established).  
**Physics claim:** No new experimental physics, no full nonlinear Lax representation and no general nonintegrability theorem.

## Scientific results

1. The exact linearized local 2×2 EMHD Fourier generator has characteristic polynomial `z²+B0² kx²(kx²+ky²)`. It cannot be diagonalized by an invertible matrix of rational Fourier symbols in two formal wavevector variables. Its minimal splitting field adjoins `sqrt(kx²+ky²)`.
2. Chiral variables `w± = beta ± sqrt(-Delta) psi` diagonalize the linear system, but the nonlinear system generically leaks between them.
3. For two Fourier modes `p,q` in one chiral sector, the coefficient generated at `p+q` is `A C (p×q)(|p|-|q|)(|p|+|q|-|p+q|)`. For nonzero amplitudes it vanishes exactly for collinear or equal-length modes.
4. Equal-radius Fourier shells admit exact, potentially noncollinear, arbitrary finite-amplitude Beltrami-whistler solutions. This belongs to known whistler/Beltrami physics and serves as a positive control.
5. For a 2+1 flat matrix connection with potentials depending *pointwise only* on `(psi,beta,Delta psi)`, arbitrary matrix size and spectator spectral parameter, flatness at all spatial solution jets forces constant commuting matrices. This result is a **declared-grammar** gate, not a general matrix Lax obstruction.

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
- [O. I. Morozov, Analysis and Mathematical Physics 15, 120 (2025)](https://doi.org/10.1007/s13324-025-01119-w) — Lax representations of ideal MHD, **not** the same equations as ideal electron MHD.
- [D. Shaikh, J. Plasma Phys. 75, 117–132 (2009)](https://doi.org/10.1017/S0022377808007198) — whistler propagation theory.

## Outstanding work

A real derivative-dependent matrix or pseudodifferential spectral construction for **both complete nonlinear EMHD equations**, with explicit gauge handling and an independent compatibility certificate. This investigation is not a proof of its existence or absence.
