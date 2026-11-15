# Exact Scalar Spectral Gaps and Topology-Selected Heat Covariances on Compact Sol Manifolds

**PHY-004 is a standalone investigation in compact spatial topology and scalar mathematical physics.** It is unrelated to the electron-MHD and SU(2) lattice-gauge manuscripts in PHY-001--003.

## Main theorems

For every integer T>=3, form the hyperbolic torus-bundle monodromy A_T=[[T-1,T-2],[1,1]]. Choose its determinant-one real eigenframe P_T and the locally trace-independent Sol metric ds^2=dw^2+exp(-2w)dy_1^2+exp(2w)dy_2^2, with deck shift k_T=acosh(T/2).

1. **Exact arithmetic sector separation.** The integer form Q_T(m)=det(m,A_T^T m)=(T-2)m_1^2-(T-2)m_1 m_2-m_2^2 is constant on each dual-lattice orbit and never vanishes on a nonzero integer vector. Different Q values guarantee different orbits, but equal Q does not guarantee the same orbit.
2. **Explicit nonbase spectral barrier.** Every nonzero fiber Fourier sector of -Delta has operator lower bound nu_T+sqrt(2 nu_T), where nu_T=8 pi^2/sqrt(T^2-4). The bound comes from an exactly confining one-dimensional potential and a harmonic-oscillator comparison, not a numerical eigenvalue fit.
3. **Exact first eigenvalue.** For T=3,4,5, the first positive scalar eigenvalue is (2 pi/k_T)^2, achieved only by two real base-circle modes sin(2 pi w/k_T) and cos(2 pi w/k_T). The strict comparison is checked by exact rational inequalities using pi<22/7.
4. **Heat-Gaussian covariance.** A centered real scalar with prescribed heat covariance exp(tau Delta) has exact zero cross-covariance between different A_T^T orbits. Within one orbit the covariance is strictly positive and bounded by
   (4 pi tau)^(-1/2)*exp[-8 pi^2 |Q| tau/sqrt(T^2-4) -(j-l)^2*k_T^2/(4 tau)].
5. **Trace discrimination for one fixed coordinate pair.** For m=(1,0), n=(2,1), the model covariance is strictly positive at T=3, but exactly zero at T=4 and T=5. This is a coordinate-basis-dependent scalar prior statement, NOT an observer-invariant CMB result.

## Reproduce and obtain the manuscript

- [paper.tex](paper.tex): full self-contained LaTeX proof, table, orbit diagram and bibliography
- [verify.py](verify.py): primary exact integer + rational certificate over 17,500 mode/trace pairs
- [verify_independent.py](verify_independent.py): independent integer matrix recurrences and rational gap test
- [AUDIT.md](AUDIT.md): counterexample-first proof audit
- [PDF_FILENAME.txt](PDF_FILENAME.txt): descriptive manuscript filename, used by GitHub Actions.

Use Python 3.11+ standard library only:

    python verify.py
    python verify_independent.py

The same scripts are run by GitHub Actions, which compiles a PDF using LaTeX.

## Priority and physics limitations

The global spectral arithmetic of compact Sol manifolds is established in Bolsinov--Dullin--Veselov (Commun. Math. Phys. 264, 583--611, 2006). COMPACT has developed CMB topology covariance tools for **different Euclidean topologies**, with physical transfer and observer modelling beyond this note. This paper is a rigorous restricted scalar model and a reproducible benchmark. Priority of its particularly chosen spectral comparison is not certified.

**No coupled Einstein--Vlasov/Boltzmann evolution, physical CMB T/E/B predictions, new observational detection or Einstein-gravity discovery is claimed.**
