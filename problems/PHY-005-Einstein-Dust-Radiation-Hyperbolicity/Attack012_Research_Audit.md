# PHY-005: First-jet hyperbolicity and off-shell Weyl--radiation resonance

**Scope:** A new exact statement about the *frozen, comoving, partially prolonged* sourceful Weyl/radiation system; a general established first-jet prolongation argument. Neither is a complete reduction of Einstein--dust--radiation.

## Primary result

The comoving Weyl principal system with radiation-velocity-gradient source is

\[
E_t+\mathrm{curl}_{\rm STF}H=-b\,\mathrm{STF}(V),\qquad
H_t-\mathrm{curl}_{\rm STF}E=0,\quad b\neq0.
\]

Promote the ten directional first jets \(X_E=\partial_1 E\), \(X_H=\partial_1H\) without independently prolonging all twelve radiation first-jet variables \(W_i=(S_i,V_{i1},V_{i2},V_{i3})\). The resulting off-shell 22-field first-order principal symbol in the \(n=e_1\) direction has characteristic polynomial

\[
\chi(z)=z^8(z^2-1)^2(z^2-1/4)^2(z^2-1/3)^3.
\]

The nullity is exactly **7**, whereas the algebraic zero multiplicity is **8**. The source projection responsible is \(\langle E_L,\mathrm{STF}(V)\rangle=V_{22}+V_{33}\) on the transverse radiation zero eigenspace, with \(E_L=\mathrm{diag}(-2,1,1)\). The matrix has an off-shell Jordan block and no positive definite symmetrizer, for any \(b\ne 0\).

This is not a no-go theorem for the Einstein equations. The projected source uses freely evolved off-shell jet components; geometric and matter defining constraints could exclude or modify those modes on the physical constraint surface. The obstruction is to *this unadjusted partial prolongation*, not to all possible hyperbolic formulations.

## Constructive but conditional statement

For any **fully specified and already symmetric-hyperbolic** quasilinear first-order system \(A^\mu(U)\partial_\mu U=F(U)\), the complete spatial first-jet variables \(Q_i=\partial_i U\) obey a closed differentiated system. Its principal matrices are \(\mathrm{diag}(A^\mu,A^\mu,A^\mu,A^\mu)\). All first-jet defining constraints propagate homogeneously. This is a standard fact from classical symmetric-hyperbolic theory, not a new physical theorem. In particular, the 33-field *restricted, synthetic* material/shear/Weyl/radiation principal skeleton gives an exact 132-field positive block system. This does **not** certify the 58-field Einstein frame skeleton, whose complete nonlinear equations and constraint adjustments are not yet specified. Were a closed symmetric 58-field base established, the same abstract prolongation would yield 232 variables, with possible redundancy.

## Replay

- `verify_attack012.py` uses exact SymPy tensor and matrix computations. It independently constructs the five-element STF Weyl basis, the 10x10 curl symbol, the 12-field acoustic block, the exact 22x22 partial prolongation, the projected zero-mode pairing, the exact rank/nullity and the 132x132 complete-jet principal matrices.
- `verify_attack012_independent.py` uses only Python standard-library `fractions.Fraction`, building the independent 22x22 matrix and performing a hand-coded rational Gaussian elimination. It does not import SymPy or the first verifier.
- `Execution_Log.txt` contains the full rerun outputs.

**Scientific status:** restricted off-shell obstruction exact, conditional standard finite-jet theorem exact, proposed complete nonlinear Einstein--dust--radiation hyperbolicity and full constraint propagation **remain unproved**. Prior-art and specialist priority assessment are not complete. No email has been sent to Todd Oliynyk; no GitHub file was modified.
