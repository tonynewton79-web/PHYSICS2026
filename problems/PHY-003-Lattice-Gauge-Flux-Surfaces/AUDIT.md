# PHY-003 — Second verification and originality audit

## First mathematical proof
1. Minimum finite cubical k-cycle size: at least 2(k+1), by slicing and induction, so the smallest two-cycle has six faces, and the smallest nonzero three-cycle has eight cubes.
2. Parity: the one-cochain eta(x,j)=sum_(i<j) x_i mod 2 has coboundary 1 on every plaquette. Every finite closed two-chain has even area.
3. Through area ten, horizontal cap decomposition forces either one cube boundary at size six or two face-sharing cube boundaries at size ten. Three active coordinate slabs already require at least fourteen faces.
4. Pair representation uniqueness: two different pairs with equal boundary would give a nonzero three-cycle of at most four cells, contrary to the eight-cell minimum.
5. Four-dimensional counting: four cubes meet each plaquette. The six unordered pairs split 2 same-orientation and 4 mixed. Double-counting incidences gives rooted counts 4,20,40 and per-site densities 4,12,24.
6. Periodic L>=4 tori have no nontrivial homology two-cycle below L^2>=16 faces. Small connected cycles unwrap; the Z2 partition expansion follows exactly by summing link signs.
7. Independent SU2 center transformation at every link proves necessary even incidence of half-integer representation plaquettes. It does not give their nonabelian weights.

## Adversarial second verification
- Rooted edge-closure DFS: 30,259 exact partial states, 4 six-face and 60 ten-face closed surfaces. Exact set equality with an independent root-cube-pair constructor; counts 20 same-orientation plus 40 mixed.
- Completeness of the rooted DFS through area ten: any proper closed partial subcycle plus nonempty closed complement would have at least 12 faces; so closure cannot stop the search prematurely.
- Independent periodic implementation on 4^4: exactly 1,536 plaquettes; 1,024 cubes; 9,216 ten-face pairs, split 3,072 same and 6,144 mixed. Every pair has unique ten-face boundary; fixed-root multiplicity checks agree 4,60,20,40.
- The twelve-face four-facet boundary verifies that the classification deliberately stops at size ten.

## Nonabelian SU(2) attack: separate proof obligations and independent replay

**Normalization:** On L^4, L>=4, with normalized Haar measure and Wilson Boltzmann factor exp[(beta/2)Tr U_p), the one-plaquette character expansion has c0=2 I1(beta)/beta, and spin-j ratio u_j=I_(2j+1)(beta)/I1(beta). Each spin costs at least beta^(2j). The exact fundamental factor is 2u with u=I2/I1.

**Exhaustion through order beta^11:** Any nontrivial half-integer support is mod-two closed and, with total representation degree <=11, has area 6 or 10. When half support is empty, a set of integer-spin faces with every link Haar-nonzero has no dangling edge and therefore at least six faces; its total degree is at least 12. For area-6 half support, there can be at most two additional integer faces; each new face shares at most one edge of the cube, and two new faces share at most one edge, leaving a forbidden singly occupied edge away from the cube. Without integer faces, the cube's two-valent links force a constant spin on all six faces, and only spin 1/2 fits the cutoff. For area-10 half support, all ten faces must have spin 1/2. Thus there are no missing character terms through order 11.

**Group factors:** On a five-face cube cap, conditional integration at fixed missing-face holonomy gives d_r^(-4) chi_r(g) by the standard character convolution identity. One complete six-face cube therefore integrates to 2^(-4)=1/16 in the SU2 fundamental. A same- or mixed-orientation face-sharing pair is two such caps joined along their four shared edges, giving 2^(-8)=1/256. Both orientations have identical group factors despite the mixed geometry's four-valent edges. Combined with 2u per plaquette and the geometric multiplicities 4V and 36V, the normalized partition is 1+16V u^6+144V u^10+O_L(beta^12).

**Independent second-pass tests:**
1. Standard-library rational Bessel checker derives coefficients directly from factorial definitions, rather than testing a target formula against itself. It reproduces u=beta/4-beta^3/96+beta^5/1536-beta^7/23040+..., and the intensive logarithm coefficients 3/4,-1/64,7/1536,-31/30720,4451/14745600 for beta^2,beta^4,...,beta^10.
2. Fully exhaustive 4D exterior-square overlap check over 1530 exterior plaquettes confirms the cube-edge exclusion used in the representation-degree argument.
3. Independent finite-group check uses the non-Abelian standard 2D representation of S3, tree-gauge-fixes the plaquette complexes and exhausts 7776 cube assignments and 10077696 assignments for each ten-face type. Exact integer character-product sums are 486,39366,39366 respectively, yielding averages 1/16,1/256,1/256. Since the conditional gluing law is group-independent, agreement is a strong cross-check of the topology and group integration. It does **not** directly enumerate continuous SU2 configurations.

**Priority limitation:** The SU2 low-order series and general group integration method are not claimed to be newly discovered; Kogut and Drouffe--Zuber give foundational and higher-order strong-coupling results. This is a transparent, independently reproduced finite-volume specialization. No all-area convergence, uniform thermodynamic bound, continuum mass-gap proof, or external peer review is implied.

## Limitations and provenance
The early strong-coupling terms and 4D abelian plaquette analysis have prior art: Wegner (1971); Kogut (1979); Drouffe--Zuber (1983); Forsstrom (2022). Scientific originality is not established. The Z2 pressure coefficients 4 and 36 are not SU2 Wilson coefficients. The finite-volume remainder O_L(t^12) is not continuum-uniform. The all-area rooted animal bound 80^(h-1) is too weak for any continuum Yang--Mills claim. No peer review or priority certificate is claimed.

## Reproduction
Python 3.11+ standard library: run python verify.py, python verify_independent.py and python verify_su2_coefficients.py. Compile verify_su2_gluing_s3.cpp with g++ -O2 -std=c++17 and execute it. Compile paper.tex with pdflatex twice. These programs are independent numerical-free finite exact checks, not formal proof certificates for the universal statements.
