# PHY-009 — Einstein–scalar CMC four-mode reduction

**Paper:** *Four-Mode Reduction and Exact Scattering for Einstein–Scalar Cauchy Data*  
**Author:** Tony Newton  
**Field:** Mathematical general relativity, hyperbolic–elliptic PDE, rigorous numerics  
**Status:** Restricted exact results; numerical finite-time excess; **continuum error certificate OPEN**.  
**Version:** 17 November 2026.

## Main result, plainly stated

For explicit three-cosine Einstein–massless-scalar data on a three-torus, discrete isometries restrict the scalar cubic Fourier support to 32 of 44 candidates. The exact initial data saturate all 32 permitted scalar frequencies. First variations have Bessel scattering profiles, and the spatially homogeneous quadratic CMC lapse has a closed time-integral.

For a proposed weighted fixed-amplitude error ceiling of `1/3600`, a four-orbit Fourier-matrix functional provides an exact *reference-free lower bound*. Exact-rational arithmetic shows that the saved **numerical interpolant** has a witness above that ceiling. The stored polynomial **surrogate** is certified positive definite and elliptically coercive for logarithmic time `0 ≤ rho ≤ 9`. These statements do **not** establish the continuum Einstein–scalar counterexample.

## Quantitative audit

- Exact-rational saved-interpolant witness: `J_PL > 0.000437821879636209272`.
- Proposed auxiliary bound: `1/3600 = 0.000277777777777...`.
- Original sufficient PDE-output gate: `|J_Einstein - J_PL| < 1.60044101858e-4`.
- Later exact-integer surrogate observation certificate: `|J(n_tilde P_tilde) - J_PL| < 8.78e-5`.
- Therefore a sufficient but **unproved** continuum-to-surrogate gate is `|J_Einstein-J(n_tilde P_tilde)| < 7.2e-5`.
- The exact continuum residual, stability coefficient, constraint propagation and existence through rho=9 **remain uncertified**.

## Files

- [Revised 26-page PDF](Four_Mode_Einstein_Scalar_Updated_Observation_Bound.pdf): complete current paper including the exact observation-reconstruction certificate.
- [paper.tex](paper.tex): the earlier full 25-page base manuscript source, including exact results through FT13 (the PDF contains an additional later section; see addendum).
- [OBSERVATION_ADDENDUM.md](OBSERVATION_ADDENDUM.md): mathematical record of the subsequent exact-integer reconstruction bound.
- [AUDIT.md](AUDIT.md): distinctions between theorems, saved-data certificates, numerical diagnostics and open results.
- [verify.py](verify.py): no-dependency reproducer for finite Fourier combinatorics, the momentum-adjustment norm and arithmetic proof thresholds.
- [PDF_FILENAME.txt](PDF_FILENAME.txt): required PDF stem for the repository build.
- [requirements.txt](requirements.txt): verifier dependencies.

**Figure/source caveat:** the revised **26-page PDF is now committed in this folder**. The accompanying LaTeX text is the earlier 25-page base edition; [OBSERVATION_ADDENDUM.md](OBSERVATION_ADDENDUM.md) documents the subsequent result. The separate figure/source arrays and 37 MB+ replay archive have not yet been pushed, so the TeX file alone is not a complete figure-bearing build.

## Related literature

1. G. Fournodavlos, I. Rodnianski and J. Speck (2023), *Stable Big Bang formation for Einstein's equations: The complete sub-critical regime*.
2. L. Andersson and A. D. Rendall (2001), *Quiescent cosmological singularities*.
3. L. Andersson and V. Moncrief (2003), *Elliptic–hyperbolic systems and the Einstein equations*.
4. I. Rodnianski and J. Speck (2018), two papers on Einstein–scalar stability and Big Bang formation.
5. M. Neher, K. R. Jackson and N. S. Nedialkov (2007), *On Taylor model based integration of ODEs*.

## Release boundary

This is **PHY-009** by the author's requested numbering. `PHY-008` is not currently recorded in the repository and is not silently invented here.

No new curvature-singularity theorem, Hawking chronology-protection theorem, or rigorous counterexample to `1/3600` is claimed. Independent priority/expert review is pending.
