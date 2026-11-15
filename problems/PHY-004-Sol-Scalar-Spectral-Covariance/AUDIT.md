# PHY-004 — Two-pass mathematical and physics audit

## Model and gauge/coordinate boundary

Monodromy A_T=[[T-1,T-2],[1,1]] has det1, positive real eigenvalues lambda=(T+sqrt(D))/2, 1/lambda, D=T^2-4, and k=log lambda. The explicit P_T eigenvectors have determinant1. The quotient of the universal Sol metric ds^2=dw^2+exp(-2w)dy1^2+exp(2w)dy2^2 by Z² fibers and the deck map (x,w)->(A_T x,w+k) is compact and smooth, and has volume measure dx dw. All T have the same local metric, but NOT the same global identifications or observer-independent Fourier labels.

## First pass: proof dependencies

1. Q_T(m)=det(m,A_T^T m) has integer coefficients and discriminant T^2-4. This is a nonsquare integer strictly between (T-1)^2 and T^2 for all T>=3. Hence Q !=0 for each nonzero m in Z², and Q is monodromy invariant.
2. Fiber Fourier deck condition f_(A^T m)(w)=f_m(w+k) turns each nonzero dual-lattice orbit into a unitary L²(R) sector. The scalar Laplacian is H_m=-d²/dw²+4 pi²(alpha1² e^(2w)+alpha2² e^(-2w)), alpha=P_T^T m. Exact identity alpha1 alpha2=-Q_T(m)/sqrt(D) makes H confining.
3. V=mu cosh(2(w-w0)), mu=8 pi² |Q|/sqrt(D) >= nu=8 pi²/sqrt(D). The inequality cosh(2s)>=1+2s² and exact harmonic-oscillator ground state imply H>=mu+sqrt(2 mu)>=nu+sqrt(2nu). This is an operator bound, not a claim of attained fiber eigenvalues.
4. Base scalar modes are ordinary length-k circle harmonics. For T=3,4,5, let r=(T-2)/(T+2); k>2sqrt(r)(1+r/3). Thus base first eigenvalue B < C pi² where C=1/[r(1+r/3)^2] is 1125/256, 243/100, 343/192. Enclosing sqrt(D) and D^(1/4) by rational pairs (9/4,3/2), (7/2,2), (5,9/4), the oscillator lower bound is >a pi²+b pi with (a,b)=(32/9,8/3),(16/7,2),(8/5,16/9). The exact margins b-(C-a)*22/7 are 241/8064,3789/2450,12013/10080. All positive, with pi<22/7, so every nonzero fiber mode lies strictly above the base first eigenvalue. First eigenvalue and multiplicity two are exact for traces 3,4,5.
5. The centered real smooth Gaussian field with covariance exp(-tau(-Delta)) is a **specified mathematical prior**, not a physical primordial state. The Laplacian decomposition implies zero covariance between different dual-lattice orbits. Within the same orbit the covariance is the positive 1D Schrodinger heat kernel evaluated at jk and lk; standard Feynman--Kac gives strict positivity and the Gaussian upper bound multiplied by exp(-mu tau).
6. Mode pair (1,0),(2,1): trace3 satisfies A_3^T (1,0)=(2,1). At T4 and T5 the Q values differ and the heat cross-covariance is exactly zero. Equal Q need not mean same orbit: (0,1) and (0,-1) both have Q=-1 but positive-eigenvalue A^T powers cannot exchange signs.

## Adversarial second pass

- Primary pure-Python exact integer verifier tests Q invariance and nonsquare discriminants for T=3..30 and all (m,n) in [-12,12]^2, including 17,500 mode/trace pairs, plus positive/negative power recurrence and the trace contrast.
- Second verifier independently computes 2x2 integer matrix products and positive/negative powers for T=3..20, all nonzero integer vectors in [-7,7]^2, the same-Q/opposite-vector counterexample, and independently derives the rational gap inequalities from r and radical upper bounds.
- These are finite regression checks of universal **proved** algebraic facts. The continuum heat positivity and operator min-max steps are certified analytically, not by simulation.
- Bounds are in exactly specified local Sol length units. A common rescaling of the spatial metric rescales eigenvalues as inverse length squared. No physical frequency or observational significance follows without a dynamical metric and transfer model.
- The Q invariant is necessary but not sufficient for orbit membership; the manuscripts and verifier explicitly guard this false shortcut.

## Prior art, novelty, and open work

A. V. Bolsinov, H. R. Dullin and A. P. Veselov (2006) established Sol spectral arithmetic and monodromy, and modern COMPACT analyses develop actual cosmic covariance techniques for Euclidean topologies. Feynman--Kac positivity is classical. A full novelty/priority search and independent specialist refereeing have not been completed. No physical Einstein-matter dynamics, perturbation constraint propagation, Thomson collision operator, observer-marginalized sky covariance, or detected cosmic topology is established.

## Reproduction

Run python verify.py and python verify_independent.py with Python >=3.11; compile paper.tex with pdflatex twice. GitHub Actions runs the exact checks and compiles the PDF.
