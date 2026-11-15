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

## Limitations and provenance
The early strong-coupling terms and 4D abelian plaquette analysis have prior art: Wegner (1971); Kogut (1979); Drouffe--Zuber (1983); Forsstrom (2022). Scientific originality is not established. The Z2 pressure coefficients 4 and 36 are not SU2 Wilson coefficients. The finite-volume remainder O_L(t^12) is not continuum-uniform. The all-area rooted animal bound 80^(h-1) is too weak for any continuum Yang--Mills claim. No peer review or priority certificate is claimed.

## Reproduction
Python 3.11+ standard library: run python verify.py and python verify_independent.py. Compile paper.tex with pdflatex twice. These programs are independent numerical-free finite exact checks, not formal proof certificates for the universal statements.
