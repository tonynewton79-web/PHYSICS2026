# PHY-006 mathematical and editorial audit

## Exact assumptions

Two distinguishable qubits with the SAME positive bare energy gap epsilon. Both initial local density matrices are exactly diagonal thermal Gibbs with excited populations 0<a<b<1/2. Global initial state arbitrary positive density matrix with those marginals. Closed-system U commutes H0=epsilon(n_A+n_B). Reversed mean-energy transfer q means E_A(final)-E_A(initial)=-epsilon*q, 0<=q<=a. All information is in natural-log nats.

## Proof dependencies

1. Joint entropy invariant under U. Initially S_A=h(a), S_B=h(b). For fixed final excitation populations p=a-q, r=b+q, qubit entropy satisfies S_A(final)<=h(p), S_B(final)<=h(r), with equality for energy-diagonal marginals. Since final mutual information is >=0, initial I>=h(a)+h(b)-h(p)-h(r). No assumption on global inter-sector coherences is used.
2. Set rho_f=diag(1-p,p) tensor diag(1-r,r). D=r-p=b-a+2q>q for q>0. Set sin^2(theta)=q/D, U=exp[-i theta (|01><10|+|10><01|)], rho_i=U^dagger rho_f U. This commutes with H0, preserves positivity and total energy. Exact input populations are a,b: initial P10=p(1-r)+q, P01=(1-p)r-q, P11=pr. Final product gives I_f=0; hence equality at all q, including q=a (A final pure ground).
3. The initial one-excitation coherence has |z|^2=q(b-a+q). For any equality protocol, zero final mutual information forces exactly the product final state, and equality in the qubit entropy bound forces energy-diagonal final marginals. Energy conservation fixes the 00 and 11 populations, while determinant invariance of the one-excitation block fixes |z|. The universal 2-qubit PPT criterion thus yields separability iff q(b-a+q)<=(a-q)(b+q)(1-a+q)(1-b-q).
4. Put d=(a-q)(b+q)=ab-q(b-a+q), t=a+b. The PPT margin is d(2-t+d)-ab. It decreases strictly as q increases 0 to a, from ab(1-a)(1-b)>0 to -ab<0; exactly one threshold exists, given in the paper by nested quadratics.
5. C''(q)=1/[(a-q)(1-a+q)]+1/[(b+q)(1-b-q)]>=8. C'(0)=epsilon(beta_A-beta_B). Thus C(q)>=epsilon(beta_A-beta_B)q+4q^2. Coefficient 4 is optimal by a,b->1/2, a<b, and q->0.
6. Energy-basis diagonal initial states cannot reverse energy flow under any H0-commuting two-qubit unitary, because their one-excitation populations are ordered b-d>a-d and any 2x2 unitary output is a convex combination of the two populations. Coherence, not necessarily entanglement, is needed.

## Independent verification

SymPy exact checks cover arbitrary symbolic population identities, exact finite 4x4 unitary calculations with rational population examples, and the rational PPT criterion. Numerical adversarial controls sample 3,500 random (a,b,q) values and 1,100 random correlated density matrices. A separate Python standard-library Fraction program checks 1,475 rational cases and an independent separability sign-crossing procedure. Finite tests are diagnostic; the written universal proofs are decisive.

## Prior art and publication boundaries

Partovi (2008), Jennings-Rudolph (2010), Jevtic-Jennings-Rudolph (2012 PRL and PRA), and Micadei et al. (2019) establish broad correlation-assisted heat reversals and energy-constrained two-qubit mutual-information optimization. The exact tight binary-entropy boundary may be derivable from established unitary-orbit methods; no priority or novelty beyond a compact explicit restricted characterization is asserted. No experimental evidence or full resource cost of preparation/interaction is claimed.

## Editorial

Title is mathematical/physical, Tony Newton is sole listed author, no institutional trading-name footnote, no manuscript date, compact professional theorem/proof narrative, citations to foundational prior art, one small numerical table, no solver or internal release chatter in the paper. PDF compiled with pdflatex twice, A4, five pages, and rendered for inspection.