# PHY-001: Zero-order scalar Poisson–Lax obstruction in ideal EMHD

**Scope:** two-and-a-half-dimensional ideal electron magnetohydrodynamics, reduced fields a(x,y,t), b(x,y,t), q=Delta(a).  
**Status:** INTERNAL PROOF (not peer-reviewed or priority-certified).  
**Date:** 15 November 2026.  
**Author:** Tony Newton.

## The proved scoped result

Let {f,g}=f_x g_y-f_y g_x. The known 2.5D ideal EMHD reduction is

a_t = {a,b}; b_t = {Delta(a),a}.

Suppose a scalar identity L_t={M,L} holds as a universal differential identity under these equations, with L=F(a,b,Delta(a);lambda) and M=G(a,b,Delta(a);lambda), and F,G arbitrary C² functions of these pointwise state variables. Then F is independent of b and Delta(a). Wherever F_a != 0, necessarily

L=f(a;lambda); M=-b+h(a;lambda).

These identities encode the a-equation only. No nondegenerate two-field representation exists **in precisely this scalar, zero-order grammar**. This does not prove that ideal EMHD is nonintegrable or exclude matrix/higher-jet/nonlocal Lax representations.

## Evidence

- Full proof: [paper.tex](paper.tex) (source of the PDF).
- Exact, independent checking code: [verify.py](verify.py).
- All test assumptions and outcomes: [AUDIT.md](AUDIT.md).
- Pinned SymPy dependency: [requirements.txt](requirements.txt).

Run: python -m pip install -r requirements.txt  
Then: python verify.py

CI also compiles the manuscript and uploads the PDF as a build artifact.

## Prior art

- Q. Peng (2026), arXiv:2605.20845: 2.5D EMHD equations and dissipative well-posedness (the reduction is known).
- M. Lyutikov, Phys. Rev. E 88, 053103 (2013): exact nonlinear harmonic whistlers (known).
- Abdelhamid, Kawazura and Yoshida, J. Phys. A 48, 235502 (2015): functional Hamiltonian formalism for extended MHD (distinct from the present scalar spatial Poisson bracket).

**Novelty:** the precise state-dependent scalar no-go classification has not been priority-certified against all prior work.
