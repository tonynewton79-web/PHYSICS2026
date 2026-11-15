#!/usr/bin/env python3
"""PHY-006: exact symbolic and numerical checks of optimal heat reversal.

The proof in paper.tex is analytic; these tests are independent diagnostics.
SymPy 1.14, NumPy >=2 and the Python standard library.
"""
import math
from fractions import Fraction as F
import numpy as np
import sympy as s

checks=0

def check(name, predicate):
    global checks
    assert bool(predicate), name
    checks += 1
    print('PASS', name)

# Exact algebraic protocol, for arbitrary rational marginal populations.
a, b, q = s.symbols('a b q', real=True)
D = b-a+2*q
p, r = a-q, b+q
t = q/D
lam10 = p*(1-r)
lam01 = (1-p)*r
initial_10 = s.factor(lam10*(1-t)+lam01*t)
initial_01 = s.factor(lam01*(1-t)+lam10*t)
check('arbitrary reversal q reproduces initial Gibbs marginal A',
      s.simplify(initial_10+p*r-a)==0)
check('arbitrary reversal q reproduces initial Gibbs marginal B',
      s.simplify(initial_01+p*r-b)==0)
check('one-excitation offdiagonal modulus squared',
      s.factor(t*(1-t)*(lam01-lam10)**2-q*(b-a+q))==0)
check('initial one-excitation block determinant is preserved',
      s.factor(initial_10*initial_01-
               t*(1-t)*(lam01-lam10)**2-lam10*lam01)==0)
check('total excitation conservation',s.simplify(p+r-a-b)==0)
check('PPT test factorization into product endpoint',s.factor(
      p*r*(1-p)*(1-r)-q*(b-a+q)
      - (p*r*(2-a-b+p*r)-a*b))==0)

# Check explicit full unitary construction exactly (not just scalar formulas).
examples=[(F(1,5),F(2,5),F(1,20)),
          (F(1,5),F(2,5),F(1,10)),
          (F(1,5),F(2,5),F(1,5)),
          (F(1,9),F(1,3),F(1,18)),
          (F(1,20),F(2,5),F(1,100)),
          (F(1,3),F(2,5),F(1,12))]
for ar,br,qr in examples:
    a0,b0,q0=map(lambda x:s.Rational(x.numerator,x.denominator),(ar,br,qr))
    p0,r0=a0-q0,b0+q0
    t0=q0/(r0-p0)
    cos=s.sqrt(1-t0)
    sin=s.sqrt(t0)
    U=s.eye(4)
    U[1,1]=cos;U[2,2]=cos
    U[1,2]=-s.I*sin;U[2,1]=-s.I*sin
    rho_f=s.diag((1-p0)*(1-r0),(1-p0)*r0,p0*(1-r0),p0*r0)
    rho_i=(U.conjugate().T*rho_f*U).applyfunc(s.simplify)
    check(f'exact energy-preserving unitary a={ar},b={br},q={qr}',
          U*s.diag(0,1,1,2)==s.diag(0,1,1,2)*U)
    check(f'exact U rho_i U^dagger=rho_product a={ar},q={qr}',
          (U*rho_i*U.conjugate().T-rho_f).applyfunc(s.simplify)==s.zeros(4))
    check(f'exact input local Gibbs marginal A, q={qr}',
          s.simplify(rho_i[2,2]+rho_i[3,3]-a0)==0)
    check(f'exact input local Gibbs marginal B, q={qr}',
          s.simplify(rho_i[1,1]+rho_i[3,3]-b0)==0)
    check(f'exact output cold-to-hot transfer, q={qr}',
          s.simplify(rho_f[2,2]+rho_f[3,3]-(a0-q0))==0)
    z2=s.simplify(rho_i[1,2]*rho_i[2,1])
    check(f'exact global coherence from unitary, q={qr}',
          s.simplify(z2-q0*(b0-a0+q0))==0)

# Quantum separability of X-state via Peres-Horodecki PPT 2x2 block.
a0,b0=s.Rational(1,5),s.Rational(2,5)
for q0,expect in [(s.Rational(1,20),True),(s.Rational(1,10),False),
                  (s.Rational(1,5),False)]:
    p0,r0=a0-q0,b0+q0
    pp=p0*r0*(1-p0)*(1-r0)
    coh=q0*(b0-a0+q0)
    check(f'exact PPT/separability witness q={q0}',bool(pp>=coh)==expect)

# The strengthened estimate is universal since h''(x)<=-4.
# Investigate a broad range of parameters and endpoints independently.
def h(x):
    return 0.0 if x<=0 or x>=1 else -x*math.log(x)-(1-x)*math.log1p(-x)

rng=np.random.default_rng(261115)
for k in range(3500):
    a0=float(rng.uniform(.001,.48))
    b0=float(rng.uniform(a0+1.e-4,.499999))
    q0=float(rng.uniform(0,a0))
    cost=h(a0)+h(b0)-h(a0-q0)-h(b0+q0)
    linear=math.log((1-a0)/a0)*q0-math.log((1-b0)/b0)*q0
    assert cost>=linear+4*q0*q0-2.e-12,(a0,b0,q0,cost,linear)
    assert cost>=-1.e-12
check('3500 random exact-theorem entropy and quadratic margin controls',True)

# General thermal-marginal states with energy-conserving U, and even
# potential off-energy-sector coherences are covered by the proof.
# This control samples arbitrary positive states inside the 01/10 block.
for j in range(1100):
    aa=float(rng.uniform(.002,.46));bb=float(rng.uniform(aa+1.e-4,.49))
    d=float(rng.uniform(0,aa))
    zzmax=math.sqrt((aa-d)*(bb-d))
    radius=float(rng.random()**.5)*zzmax
    phi=float(rng.uniform(-math.pi,math.pi))
    z=radius*complex(math.cos(phi),math.sin(phi))
    rho=np.diag([1-aa-bb+d,bb-d,aa-d,d]).astype(complex)
    rho[1,2]=z;rho[2,1]=z.conjugate()
    theta=float(rng.uniform(0,math.pi/2))
    U=np.eye(4,dtype=complex)
    U[1:3,1:3]=np.array([[math.cos(theta),-1j*math.sin(theta)],
                          [-1j*math.sin(theta),math.cos(theta)]])
    fin=U@rho@U.conj().T
    shift=float(fin[2,2].real+fin[3,3].real-aa)
    if shift< -1.e-10:
        qq=-shift
        eig=np.linalg.eigvalsh(rho)
        eig=eig[eig>1.e-14]
        Si=float(-np.sum(eig*np.log(eig)))
        Ii=h(aa)+h(bb)-Si
        exact=h(aa)+h(bb)-h(aa-qq)-h(bb+qq)
        assert Ii+2.e-12>=exact,(aa,bb,qq,Ii,exact)
check('1100 random correlated two-qubit states: no violation of exact lower bound',True)
print(f'ALL PHY-006 PRIMARY CHECKS PASS ({checks} named gates plus random sweeps)')