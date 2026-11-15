# Exact Low-Area Center-Flux Surfaces and Strong-Coupling Coefficients in Four-Dimensional Lattice Gauge Theory

This is the third numbered PHYSICS2026 paper and a **different physics subject** from the EMHD investigations PHY-001 and PHY-002.

## Precise results

Every finite mod-two closed plaquette surface in Z^4 with fewer than 12 faces is a single cube boundary of area 6 or the unique symmetric-difference boundary of two face-sharing elementary cubes of area 10. A fixed plaquette belongs to N6=4 six-face surfaces and N10=60 ten-face surfaces. The latter split into 20 same-orientation and 40 mixed-orientation two-cube pairs.

Per lattice site, the 4D area-six and area-ten counts are 4 and 36. For a periodic L^4 torus with L>=4, V=L^4, and t=tanh(beta), the Z2 gauge partition function obeys

Z/(2^(4V) cosh(beta)^(6V)) = 1 + 4V*t^6 + 36V*t^10 + O_L(t^12).

In SU(2) Wilson character expansions, half-integer-spin plaquettes must obey mod-two closure by link-center parity, but Z2 coefficients are NOT SU(2) character coefficients.

## Reproduce all exact checks

Requirements: Python 3.11+, standard library only. Run:

    python verify.py
    python verify_independent.py

The first program explores 30,259 rooted partial states and regenerates the exact 4+60 catalogue by a separate cube-pair method. The second uses periodic L=4 cell incidence: 1,536 plaquettes, 1,024 cubes, and 9,216 distinct face-sharing pairs.

The full proof appears in paper.tex. AUDIT.md records the two-pass proof audit. PDF_FILENAME.txt names the compiled PDF after the manuscript's full title. GitHub Actions independently executes the scripts and compiles the PDF.

## Prior art and limitations

Wegner (1971), Kogut (1979) and Drouffe--Zuber (1983) established lattice strong-coupling surface methods. Forsstrom (2022) gives rigorous 4D abelian small-support analysis. The six and ten cube terms are therefore NOT claimed as a breakthrough. This package is an independently verified finite combinatorial theorem and rigorous abelian gauge-theory check, not a proof of SU(2) confinement or the continuum Yang--Mills mass gap.

The next open target is a much sharper uniform all-area closed-surface entropy estimate and true nonabelian mixed-spin/intertwiner control.
