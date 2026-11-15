#!/usr/bin/env python3
"""PHY-004 primary certificate: integer monodromy and exact-rational spectral gap.
No floating-point arithmetic is used in any mathematical accept/reject gate.
"""
from fractions import Fraction as F
from math import isqrt

def mat(T):
    return ((T-1,T-2),(1,1))
def dual(T,v):
    x,y=v
    return ((T-1)*x+y,(T-2)*x+y)
def invdual(T,v):
    # (A^T)^-1 = [[1,-1],[-(T-2),T-1]]
    x,y=v
    return (x-y, -(T-2)*x+(T-1)*y)
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def qform(T,v):
    x,y=v
    return (T-2)*x*x-(T-2)*x*y-y*y
def iterate(T,v,j):
    for _ in range(abs(j)):
        v=dual(T,v) if j>=0 else invdual(T,v)
    return v

count=0
for T in range(3,31):
    D=T*T-4
    assert isqrt(D)**2<D<(isqrt(D)+1)**2
    for x in range(-12,13):
      for y in range(-12,13):
        v=(x,y)
        q=qform(T,v)
        if v!=(0,0):assert q!=0,(T,v)
        assert q==cross(v,dual(T,v))
        assert q==qform(T,dual(T,v))==qform(T,invdual(T,v))
        assert iterate(T,v,0)==v
        if -3<=x<=3 and -3<=y<=3:
            for j in range(-7,8):
                assert q==qform(T,iterate(T,v,j))
                assert iterate(T,iterate(T,v,j),-j)==v
        count+=1
    print("PASS trace",T,"integer Q invariant and discriminant non-square")
print("checked",count,"lattice mode/trace pairs")
m=(1,0);n=(2,1)
assert iterate(3,m,1)==n and qform(3,m)==qform(3,n)==1
for T in (4,5):
    assert qform(T,m)!=qform(T,n)
    assert all(iterate(T,m,j)!=n for j in range(-15,16))
assert all(iterate(3,m,j)!=(-1,0) for j in range(-15,16))
print("PASS trace-3 same-orbit / trace-4,5 different-orbit discriminator")
# Trace T spectral inequality. Let y^2=(T-2)/(T+2).
# k=2atanh(y) > 2y(1+y^2/3) = k_lower
# (2pi/k)^2 < C_T*pi^2, C_T=1/[y^2(1+y^2/3)^2].
# For the nonbase sector H >= -d²+mu+2mu(w-w0)²,
# mu >= 8pi²/sqrt(T²-4), osc ground mu+sqrt(2mu).
# Rigorous upper rational envelopes for sqrt(D), D^(1/4):
sqrts={3:F(9,4),4:F(7,2),5:F(5,1)}
fourths={3:F(3,2),4:F(2,1),5:F(9,4)}
for T in (3,4,5):
    D=T*T-4
    sq=sqrts[T];four=fourths[T]
    assert sq*sq>D and four**4>D
    yy=F(T-2,T+2)
    C=1/(yy*(1+yy/F(3))**2)
    a=F(8)/sq
    b=F(4)/four
    # suffices C*pi² < a*pi²+b*pi, via pi < 22/7
    margin=b-(C-a)*F(22,7)
    assert margin>0,(T,C,a,b,margin)
    print(f"PASS trace-{T} exact first positive eigenvalue certificate:",
          "C=",C,"a=",a,"b=",b,"rational slack=",margin)
print("ALL PHY-004 EXACT PRIMARY CHECKS PASS")
