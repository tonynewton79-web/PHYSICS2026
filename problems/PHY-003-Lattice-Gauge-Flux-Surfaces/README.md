# Exact Low-Area Center-Flux Surfaces and Strong-Coupling Coefficients in Four-Dimensional Lattice Gauge Theory

This is the third numbered PHYSICS2026 paper and a **different physics subject** from the EMHD investigations PHY-001 and PHY-002.

## Precise results

Every finite mod-two closed plaquette surface in Z^4 with fewer than 12 faces is a single cube boundary of area 6 or the unique symmetric-difference boundary of two face-sharing elementary cubes of area 10. A fixed plaquette belongs to N6=4 six-face surfaces and N10=60 ten-face surfaces. The latter split into 20 same-orientation and 40 mixed-orientation two-cube pairs.

Per lattice site, the 4D area-six and area-ten counts are 4 and 36. For a periodic L^4 torus with L>=4, V=L^4, and t=tanh(beta), the Z2 gauge partition function obeys

Z/(2^(4V) cosh(beta)^(6V)) = 1 + 4V*t^6 + 36V*t^10 + O_L(t^12).

In SU(2) Wilson character expansions, half-integer-spin plaquettes must obey mod-two closure by link-center parity, but Z2 coefficients are NOT SU(2) character coefficients.

## Second attack: the full low-order SU(2) Wilson series

For normalized SU(2) Haar integration with the standard plaquette factor exp[(beta/2) Tr U_p], write
c0(beta)=2 I1(beta)/beta and u(beta)=I2(beta)/I1(beta). Then for fixed L>=4, V=L^4,

    Z_SU2(beta)/c0(beta)^(6V) = 1 + 16V u^6 + 144V u^10 + O_L(beta^12).

This is an actual SU(2) Wilson coefficient calculation, unlike the Z2 formula above. The fundamental character-integral weights are 1/16 for a cube and **1/256 for either same- or mixed-orientation two-cube surfaces**. The full coefficient statement follows by additionally ruling out every other SU(2) character assignment through representation order 11, using center parity, a no-dangling-edge lemma, and explicit cube-edge exclusion.

The finite-volume intensive logarithm is

    (1/V)log Z_SU2 = 6 log c0 + 16u^6 + 144u^10 + O_L(beta^12).

Its raw-beta series through order 10 is 3 beta^2/4 - beta^4/64 + 7 beta^6/1536 - 31 beta^8/30720 + 4451 beta^10/14745600.

**These are known-type strong-coupling coefficients, not a new confinement or continuum mass-gap theorem.** The Drouffe--Zuber review already develops the general group-factor and higher-order series machinery.

### New independent SU(2) checks

- verify_su2_coefficients.py: exact rational factorial/Bessel series and exhaustive local exterior-plaquette geometry (no third-party modules)
- verify_su2_gluing_s3.cpp: a separate 2-dimensional non-Abelian representation of S3; exhaustive 7776 + 10077696 + 10077696 group assignments. Its exact cube, coplanar-pair and mixed-pair averages are 1/16, 1/256 and 1/256. This is an independent check of the group-independent gluing identity, not an assertion that S3 equals SU2.

## Third attack: an all-orders volume-uniform SU(2) analytic window

The cumulative manuscript now goes beyond the exact order-ten coefficients. Expanding the fully normalized Wilson plaquette factors as 1+v_beta(U) yields an **exact** hard-core gas of edge-connected plaquette polymers. Its integrated activities include every nontrivial SU(2) spin and every allowed Haar/intertwiner contraction, with no spin cutoff.

An incident edge occupied by exactly one nontrivial plaquette makes that polymer activity vanish by the zero Haar average of v_beta. Therefore every contributing polymer uses at least six faces.

For complex |beta|<=r, let c0(r)=2I1(r)/r and
q(r)=(exp(r)-c0(r))/(2-c0(r)). Then every polymer gamma satisfies
|w_gamma|<=q(r)^|gamma|. Every connected rooted plaquette set of size h is bounded by 80^(h-1); combining this with the minimum six-face support and the maximum 21 incompatible rooted positions per plaquette gives the explicit Kotecky-Preiss condition

    x=80 e q(r)<1,      (21/80)*x^6/(1-x) < 1.

At **r=1/250**, a first exact rational certificate bounds the last quantity by **<93/100**, and a second independently recomputes the Bessel and exponential intervals from the positive factorial series. The abstract KP theorem yields a **volume-uniform zero-free partition function** on |beta|<=1/250 and convergence of the infinite-volume analytic pressure on its interior.

This is a very small fixed-lattice strong-coupling window, obtained using long-established polymer convergence theory. It is NOT a continuum Yang-Mills theorem, a novel optimal bound, or a claim of a physical-scale mass gap.

## Reproduce all exact checks

Requirements: Python 3.11+, standard library only. Run:

    python verify.py
    python verify_independent.py
    python verify_su2_coefficients.py
    python verify_su2_allorders_kp.py
    python verify_su2_allorders_independent.py
    g++ -O2 -std=c++17 verify_su2_gluing_s3.cpp -o /tmp/phy003_s3 && /tmp/phy003_s3

The first program explores 30,259 rooted partial states and regenerates the exact 4+60 catalogue by a separate cube-pair method. The second uses periodic L=4 cell incidence: 1,536 plaquettes, 1,024 cubes, and 9,216 distinct face-sharing pairs.

The full proof appears in paper.tex. AUDIT.md records the two-pass proof audit. PDF_FILENAME.txt names the compiled PDF after the manuscript's full title. GitHub Actions independently executes the scripts and compiles the PDF.

## Prior art and limitations

Wegner (1971), Kogut (1979) and Drouffe--Zuber (1983) established lattice strong-coupling surface methods. Forsstrom (2022) gives rigorous 4D abelian small-support analysis. The six and ten cube terms are therefore NOT claimed as a breakthrough. This package is an independently verified finite combinatorial theorem and rigorous abelian gauge-theory check, not a proof of SU(2) confinement or the continuum Yang--Mills mass gap.

The next open target is a much sharper uniform all-area closed-surface entropy estimate and true nonabelian mixed-spin/intertwiner control.
