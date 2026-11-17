# Supplemental observation certificate (post-base manuscript)

The latest 26-page edition adds the exact-integer certificate for the difference between the stored four-mode rational interpolant `J_PL` and the observation of the *archived full-field Hermite surrogate* `J(n_tilde P_tilde)`.

```
|J(n_tilde P_tilde) - J_PL| < 8.78e-5
```

This bound concerns a *specified numerical surrogate* treated as exact dyadic input. It does not compare that surrogate with the continuum Einstein–scalar solution.

Its documented error contributions are:
- spatial aliasing/Nyquist term: `< 8.75259e-5`;
- Hermite observation interpolation: `< 2.65839e-7`;
- stored FFT versus exact selected DFT: `< 3.914e-13`.

The four-mode interpolant has exact-rational witness `J_PL>0.000437821879636209272`. Consequently, `J_Einstein>1/3600` would follow from the *as-yet-unproved* condition `|J_Einstein-J(n_tilde P_tilde)|<7.2e-5`.

**Do not promote the implication to a completed continuum proof.** The 26-page revised PDF and original 37 MB+ source-array verification archive are maintained by the author; the README states the present repository limitations.
