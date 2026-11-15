#!/usr/bin/env python3
"""Symbolic certificates for PHY-005: 3D matter principal symbol and pressure limit."""
import sympy as s
c,k,t=s.symbols('c k t', positive=True,real=True)
z=s.Symbol('z')
checks=[]
def test(name,pred):
    assert bool(pred),name
    checks.append(name);print('PASS',name)
def A3(n,q=s.Rational(1,3)):
    """Variables (density_d,v_d[3], density_r,v_r[3])."""
    A=s.zeros(8)
    for j in range(3):
        A[0,1+j]=n[j]
        A[4,5+j]=n[j]
        A[5+j,4]=q*n[j]
    return A
for n in [(s.Integer(1),s.Integer(0),s.Integer(0)),
          (s.Integer(0),s.Integer(1),s.Integer(0)),
          (s.Rational(3,5),s.Rational(4,5),s.Integer(0)),
          (s.Rational(1,3),s.Rational(2,3),s.Rational(2,3))]:
    a=A3(n)
    n2=sum(v*v for v in n)
    test('characteristic '+str(n),s.simplify(a.charpoly(z).as_expr()-z**6*(z**2-n2/3))==0)
    test('Jordan geometric nullity '+str(n),8-a.rank()==5)
    test('minimal annihilator '+str(n),a*a*(a*a-s.eye(8)*n2/3)==s.zeros(8))
    h=s.diag(1,1,1,1,s.Rational(1,3),1,1,1)
    rad=a[4:8,4:8];hr=h[4:8,4:8]
    test('radiation symmetrizer '+str(n),hr*rad==(hr*rad).T)
ad=s.Matrix([[0,1],[0,0]])
test('dust Jordan',ad**2==s.zeros(2) and ad.rank()==1)
a=s.Matrix([[0,1],[c**2,0]])
h=s.diag(c**2,1)
test('pressure symmetrizer',h*a==(h*a).T)
test('pressure eigen',s.simplify(a*a-c*c*s.eye(2))==s.zeros(2))
U=s.eye(2)*s.cos(c*k*t)-s.I*s.sin(c*k*t)*a/c
test('pressure propagator exponential ODE',s.simplify(s.diff(U,t)+s.I*k*a*U)==s.zeros(2))
test('pressure propagator initial',U.subs(t,0)==s.eye(2))
test('pressureless limit',U.applyfunc(lambda entry: s.limit(entry,c,0))==s.Matrix([[1,-s.I*k*t],[0,1]]))
p=s.symbols('p',real=True)
H=s.Matrix([[c**2,p],[p,1]])
test('all symmetric pressure symmetrizer family',H*a==(H*a).T)
Ar=s.Matrix([[0,1],[s.Rational(1,3),0]])
Hr=s.diag(s.Rational(1,3),1)
test('radiation characteristic',s.simplify(Ar.charpoly(z).as_expr()-(z**2-s.Rational(1,3)))==0)
test('radiation symmetrizer 1D',Hr*Ar==(Hr*Ar).T)
print('ALL',len(checks),'SYMBOLIC CHECKS PASS')
