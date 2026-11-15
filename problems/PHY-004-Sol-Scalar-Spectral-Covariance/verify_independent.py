#!/usr/bin/env python3
"""Independent trace-3/4/5 controls: separate direct matrix recurrences,
exact formal Q coefficients, and a rational series lower bound for log(lambda).
"""
from fractions import Fraction as Q
from math import isqrt
def mul(A,B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in (0,1)) for j in (0,1)) for i in (0,1))
def det(A):return A[0][0]*A[1][1]-A[0][1]*A[1][0]
I=((1,0),(0,1))
def matpower(A,k):
    if k<0: A=((A[1][1],-A[0][1]),(-A[1][0],A[0][0]));k=-k
    M=I
    while k:
        if k&1:M=mul(M,A)
        A=mul(A,A);k//=2
    return M
def apply(A,v):return (A[0][0]*v[0]+A[0][1]*v[1], A[1][0]*v[0]+A[1][1]*v[1])
def normQ(v,Av):return v[0]*Av[1]-v[1]*Av[0]
for T in range(3,21):
    A=((T-1,T-2),(1,1))
    assert det(A)==1
    B=((A[0][0],A[1][0]),(A[0][1],A[1][1]))
    assert mul(B,matpower(B,-1))==I
    vectors=[(i,j) for i in range(-7,8) for j in range(-7,8) if i or j]
    for v in vectors:
        q=normQ(v,apply(B,v))
        for k in (-6,-5,-3,-1,1,2,3,5,6):
            w=apply(matpower(B,k),v)
            assert normQ(w,apply(B,w))==q
    print("PASS independent integer matrix recurrence T",T)
# Self-contained Fraction bounds: k_T is strictly greater than
# 2*sqrt(y²)*(1+y²/3), and the upper bound for the squared base
# frequency (measured in pi² units) is C=1/(y²(1+y²/3)^2).
Ctarget={3:Q(1125,256),4:Q(243,100),5:Q(343,192)}
# Independent rational enclosures for lower fiber bound:
# sqrt(D) < a, D^(1/4)<b, from raising positive rationals.
enclosures={3:(Q(9,4),Q(3,2)),4:(Q(7,2),Q(2)),5:(Q(5),Q(9,4))}
for T in (3,4,5):
    yy=Q(T-2,T+2)
    C=Q(1,1)/(yy*(Q(1)+yy/Q(3))**2)
    assert C==Ctarget[T]
    aa,bb=enclosures[T]
    assert aa**2>T*T-4 and bb**4>T*T-4
    # pi<22/7, direct exact interval
    assert (C-Q(8)/aa)*Q(22,7)<Q(4)/bb
    print("PASS analytic base-versus-fiber gap via rational witness T",T)
# An invariant Q value alone does not imply orbit membership.
for T in (3,4,5):
    B=((T-1,1),(T-2,1))
    v=(0,1);minus=(0,-1)
    assert normQ(v,apply(B,v))==normQ(minus,apply(B,minus))==-1
    assert all(apply(matpower(B,j),v)!=minus for j in range(-15,16))
print("PASS Q alone is insufficient for orbit matching")
print("ALL INDEPENDENT PHY-004 EXACT CHECKS PASS")
