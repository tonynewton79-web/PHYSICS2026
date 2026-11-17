# PHY-009 — claim and reproducibility audit

| Claim | Current evidence | Release status |
|---|---|---|
| Exact prescribed CMC initial constraints | Direct analytic identities | PROVED (scope-limited) |
| Glide-reflection Fourier selection | Discrete isometry and reflection action | PROVED |
| 32 of 44 cubic scalar modes nonzero | Exact rational coefficient calculation | PROVED for initial cubic data |
| Bessel scattering and quadratic lapse memory | Perturbative equations | Analytic result; specialist audit pending |
| Four-orbit reference-free lower-bound reduction | Fourier support and norm duality | PROVED as reduction |
| Saved-interpolant value above 1/3600 | Exact rational arithmetic on saved dyadic data | CERTIFIED only for interpolant |
| Surrogate positive metric and elliptic coercivity | Finite polynomial Fourier coefficient checks | CERTIFIED only for surrogate |
| Scalar/connection/frame residual identities | Exact algebra plus sampled checks | Exact identities; full numerical enclosure missing |
| Rotational first/second derivative stability | Orthogonal-transport argument | PROVED for stated smooth system |
| Updated observation reconstruction bound | Integer Fourier/Hermite certificate | CERTIFIED only for named surrogate |
| Full Einstein–scalar continuum residual and H^4 stability coefficient | Neither obtained | OPEN |
| Strict continuum refutation of 1/3600 | Requires error bound <7.2e-5 | OPEN |
| Fixed-amplitude curvature blow-up | Requires further continuation theorem | OPEN |
| Priority, publication novelty, peer review | Not independently concluded | OPEN |

## Tests

Run `python verify.py`; this tests only the exact *small algebraic reductions* and the arithmetic margins. It does **not** re-run the full numerical PDE, reproduce large archived array certificates or validate the continuum.

The 26-page updated paper should be supplied as an email attachment for specialist scrutiny. The repository includes the full base-paper LaTeX text, but not yet the binary figures, updated TeX source or large numerical replay archive.
