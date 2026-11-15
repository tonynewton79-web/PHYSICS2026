# PHY-006 — Sharp Information Cost of Correlation-Assisted Heat Reversal

**Project:** Quantum thermodynamics of two initially thermal, equal-gap qubits.

**Main exact theorem.** Let `0 < a < b < 1/2` be the initial excited-state probabilities of the colder qubit A and hotter qubit B. For any initial joint state with those local Gibbs marginals and any unitary commuting with the free Hamiltonian that transfers `epsilon*q` from A to B (`0 <= q <= a`),

    I(A:B)_initial >= C(a,b;q) = h(a)+h(b)-h(a-q)-h(b+q),

where `h` is the binary entropy in natural logarithms. Equality is attained for every feasible `q` by an explicit energy-preserving one-excitation exchange rotation and a suitable initial correlated state. The output is a product of local energy-diagonal states.

**Sharp universal quadratic refinement.**

    I_initial >= C(a,b;q) >= (beta_A-beta_B)*epsilon*q + 4*q^2.

The coefficient 4 is optimal over this two-qubit family. The exact endpoint also admits a closed separability threshold: in every equality protocol, the initial state is separable iff

    q*(b-a+q) <= (a-q)*(b+q)*(1-a+q)*(1-b-q).

Thus energy-sector coherence is needed for reversal but entanglement is unnecessary at sufficiently small optimal transfer.

## Files

- [`paper.tex`](paper.tex): complete restrained five-page research manuscript, equations, proofs, exact example and prior-art discussion.
- [`verify_optimal.py`](verify_optimal.py): exact SymPy 4x4 gate and marginal checks, PPT controls, 3,500 randomized inequality checks and 1,100 correlated-state tests.
- [`verify_independent.py`](verify_independent.py): independently structured Python standard-library `Fraction` verification of 1,475 rational cases including the closed separability threshold.
- [`AUDIT.md`](AUDIT.md): claim boundaries, exact proof dependencies and reasons for withholding any novelty claim.
- [`PDF_FILENAME.txt`](PDF_FILENAME.txt): name of compiled GitHub Actions PDF.

Run

    python -m pip install sympy==1.14.0 numpy>=2.0
    python verify_optimal.py
    python verify_independent.py

The repository-wide Actions workflow runs the two independent tests and compiles the manuscript. The local PDF is also part of the downloadable source/proof packet in the ChatGPT conversation where this research package was prepared.

## Scientific scope and prior art

Correlation-assisted reversed heat flow is long known: Partovi, *Physical Review E* 77 021110 (2008); Jennings and Rudolph, *Physical Review E* 81 061130 (2010); Jevtic, Jennings and Rudolph, *Physical Review Letters* 108 110403 and *Physical Review A* 85 052121 (2012); and Micadei *et al.*, *Nature Communications* 10 2456 (2019). The two-qubit energy-constrained unitary-orbit problem has already been investigated in depth. This is a **restricted exact resource-bound benchmark, not a claim of historic priority or experimental discovery**. It assumes equal gaps, initially Gibbs local states, an isolated energy-conserving global unitary, and average energy exchange; it does not calculate state-preparation work or noise.

**Open follow-up:** quantify constrained control time and energy-sector dephasing noise while retaining rigorous resource bounds, then prove statements for unequal gaps with realistic work-storage systems rather than silently treating an energy-nonconserving local swap as free.