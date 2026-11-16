# PHY-007 — Matched-workload H–CCZ synthesis audit

**Researcher:** Tony Newton  
**Result:** 14 input work cases × 7 concrete native-gate circuit variants = **98 semantically certified circuits**, together with **16,128 independent exact Hadamard-amplitude basis executions** on smaller cases. The benchmark is a *restricted construction comparison*, **not** a global state-of-the-art claim.

## Key scientific findings

The target is the common-prefix Boolean phase

\[
F(x)=\big(\prod_{p\in P}x_p\big)
\bigoplus_{j=1}^{m}\big(\prod_{t\in T_j}x_t\big),
\]

with \(|P|=k\ge3\), distinct three-wire suffixes \(T_j\) disjoint from the prefix, exact native gates `H` and `CCZ`, and **unconditionally restored** clean and borrowed data wires. The test cases include fully disjoint triples to prevent an artificially under-declared shared prefix.

For the canonical test \(k=4,m=3\) with 13 data wires:

| Same total allocation | Method | CCZ | H | Active clean | Extra dirty allocation |
|--:|---|--:|--:|--:|--:|
| 16 | no shared prefix | 30 | 48 | 3 | 0 |
| 16 | **PHY-007 shared, data-borrowed** | **18** | **24** | **3** | 0 |
| 16 | recycled-prefix intermediate | 19 | 32 | 3 | 0 |
| 16 | **Barenco et al. (1995), Lemma 7.2**, borrowed controlled-NOT cascade | 48 | 102 | 0 | 0 |
| 17 | PHY-007 shared, padded by one idle clean wire | 18 | 24 | 3 | 0 |
| 17 | independent clean ladders | 27 | 48 | 4 | 0 |
| 17 | **shared prefix with one additional clean suffix scratch** | **15** | **24** | 4 | 0 |

**Critical conclusion:** at a fixed 16-wire budget the shared data-borrowed construction is cheaper in both CCZ and H than the other tested circuits; at a 17-wire budget the extra-clean construction has fewer CCZ and equal H. Barenco's published dirty method needs no initialized clean scratch but uses more gates. These are distinct valid resource tradeoffs; none establishes global superiority.

With only \(k-1\) clean scratch, an additional *recycled-prefix* strategy (free an intermediate scratch by uncomputation, use it for suffix pairs, then recompute it) has

- `CCZ = 4k-6+3m`,
- `H = 8k-12+4m`.

The original data-borrowing method has `CCZ = 2(k-1)+4m` and `H = 4(k-1)+4m`. Thus for \(m>2k-4\) recycling uses **fewer CCZ but more H** at the same physical budget. This crossover is exact, not fitted.

## Source-first comparison with published work

**Actually reconstructed and executed:** Barenco et al., *Elementary gates for quantum computation*, *Physical Review A* 52, 3457 (1995), **Lemma 7.2**. Their arbitrarily borrowed scratch cascade uses \(4(c-2)\) Toffolis for \(c\) controlled-NOT controls. Our reimplementation maps every Toffoli to exact `H-CCZ-H` and conjugates the phase target with two further H operations. The implemented circuit is independently verified with **arbitrary borrowed input bits**, including whenever they are wires from other suffix terms.

**Reported in the literature but NOT an executable matched native-gate benchmark here:** Khattar--Gidney, *Quantum* 9, 1752 (2025), provides a more resource-efficient one-clean-ancilla controlled-NOT family with \(2c-3\) Toffoli-equivalent gates, but its source circuit and implementation include conditional X operations and/or relative-phase Toffoli decompositions. A reported Toffoli count alone cannot be substituted for an emitted native `H/CCZ` circuit without extra gate conversion and phase verification. Lee--Kang (2026) uses a different MCT depth/resource model. The PLDI 2025 SPARE compiler handles compute--uncompute optimization but was **not run** on the exact input source in the required gate language; its software archive does not include the named Tower/Unqomp source frontends. **No claim that PHY-007 beats KG, SPARE or Lee--Kang is warranted.**

Sources:

- Barenco et al. (1995): https://doi.org/10.1103/PhysRevA.52.3457
- Khattar & Gidney (2025): https://doi.org/10.22331/q-2025-05-21-1752
- Lee & Kang (2026): https://doi.org/10.1007/s11128-026-05056-w
- Sharma & Achour, SPARE (2025): https://doi.org/10.1145/3729253
- SPARE reproducibility artifact: https://doi.org/10.5281/zenodo.15307149

## Reproduce

```bash
python3 benchmark_matched.py
pdflatex PHY007_Matched_Workload_Literature_Audit.tex
pdflatex PHY007_Matched_Workload_Literature_Audit.tex
```

Dependencies: Python >=3.10; no third-party Python packages for core verification. The optional `make_figure.py` requires matplotlib; the PDF figure is already included. `benchmark_matched.py` imports `shared_prefix_data_compiler.py` to obtain the untrusted PHY-007 candidate circuit, but independently reconstructs all comparators. Its separate exact Boolean ANF interpreter checks **actual emitted gate semantics** and full restoration. A distinct sparse signed-integer H simulator verifies the actual Hadamard amplitudes on small instances; it is not derived from the ANF checker.

**Outputs:**

- `matched_gate_results.csv`: full per-instance, per-method gate resource ledger (98 rows).
- `matched_gate_summary.json`: schema, checks, source comparability and explicit non-run limitations.
- `resource_tradeoff.pdf`: vector chart of the CCZ crossover for prefix size k=4.
- `PHY007_Matched_Workload_Literature_Audit.pdf`: restrained five-page technical report with full derivations and literature comparison.

**Limitations:** All tests are ideal closed-system unitary gates. No parallel scheduling, hardware connectivity, Clifford+T/T-cost, relative phases from RCCX, measurement/feed-forward, optimal search, or arbitrary H–CCZ compiler equivalence is certified. All circuits implement the same Boolean phase; the external modern compiler match is still incomplete. Historical novelty and priority remain unresolved.