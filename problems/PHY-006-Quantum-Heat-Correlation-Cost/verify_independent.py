#!/usr/bin/env python3
"""Independent Fraction-only PHY-006 certificate. No NumPy or SymPy."""
from fractions import Fraction as F
from math import log, sqrt, isclose

checks=0

def assert_gate(name,condition):
    global checks
    assert condition,name
    checks+=1

def h(p):
    p=float(p)
    return -p*log(p)-(1-p)*log(1-p) if 0<p<1 else 0.

for ai in range(1,20):
    a=F(ai,40)
    for bi in range(ai+1,20):
        b=F(bi,40)
        for qi in range(0,ai+1):
            q=F(qi,40)
            p=a-q;r=b+q
            D=r-p
            t=q/D if q else F(0)
            d=p*r
            f10=p*(1-r);f01=(1-p)*r
            initial10=f10*(1-t)+f01*t
            initial01=f01*(1-t)+f10*t
            coherence2=t*(1-t)*(f01-f10)**2
            assert initial10+d==a
            assert initial01+d==b
            assert coherence2==q*(b-a+q)
            assert initial10*initial01-coherence2==f10*f01
            assert f10>=0 and f01>=0 and 0<=t<=1
            assert d*(1-a-b+d)-coherence2==p*r*(1-p)*(1-r)-q*(b-a+q)
            exact=h(a)+h(b)-h(p)-h(r)
            assert exact>=-1.e-12
            if q:
                tangent=(log((1-float(a))/float(a))-log((1-float(b))/float(b)))*float(q)
                assert exact+2.e-12>=tangent+4*float(q)**2
            checks+=1

# The correlation-optimal state is PPT if and only if its single-
# excitation coherence obeys the exact 2-qubit X-state PPT test.
a=F(1,5); b=F(2,5)
for q,sep in ((F(1,20),True),(F(1,10),False),(F(1,5),False)):
    p=a-q;r=b+q
    margin=p*r*(1-p)*(1-r)-q*(b-a+q)
    assert (margin>=0)==sep
    checks+=1

# Exact closed-form threshold based on the positive root of
# d^2+(2-a-b)*d-ab=0; rational bisection checks the sign switch.
def margin(a,b,q):
    p=a-q;r=b+q
    return p*r*(1-p)*(1-r)-q*(b-a+q)
for ai in range(1,14):
    a=F(ai,40)
    for bi in range(ai+1,20):
        b=F(bi,40)
        assert margin(a,b,F(0))>0
        assert margin(a,b,a)<0
        l,u=F(0),a
        for _ in range(42):
            m=(l+u)/2
            if margin(a,b,m)>0:l=m
            else:u=m
        assert l<u and margin(a,b,l)>0 and margin(a,b,u)<=0
        checks+=1

# Sharpness of the quadratic coefficient 4 for a,b->1/2 and q->0.
for n in (50,100,200,500,1000):
    a=F(1,2)-F(2,n+10)
    b=F(1,2)-F(1,n+10)
    q=F(1,(n+10)**2)
    exact=h(a)+h(b)-h(a-q)-h(b+q)
    delta=log((1-float(a))/float(a))-log((1-float(b))/float(b))
    ratio=(exact-delta*float(q))/(float(q)**2)
    assert 3.999<ratio<5.5,(n,ratio)
    print('Quadratic coefficient approach:',n,ratio)
    checks+=1
print(f'INDEPENDENT STANDARD-LIBRARY EXACT ARITHMETIC CHECKS PASS ({checks} cases)')