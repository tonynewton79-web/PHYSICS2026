#!/usr/bin/env python3
"""Independent all-rational 26-field Weyl + prolonged radiation principal audit.
No SymPy; explicit Levi-Civita, Gram and integer/fraction matrix algebra.
Does not certify the full nonlinear Einstein frame reduction.
"""
from fractions import Fraction as Q
from itertools import permutations

B=[
[[1,0,0],[0,-1,0],[0,0,0]],
[[1,0,0],[0,1,0],[0,0,-2]],
[[0,1,0],[1,0,0],[0,0,0]],
[[0,0,1],[0,0,0],[1,0,0]],
[[0,0,0],[0,0,1],[0,1,0]]]
D=[Q(v) for v in (2,6,2,2,2)]
def eps(i,j,k):
    if len({i,j,k})!=3:return 0
    return 1 if ((i,j,k) in ((0,1,2),(1,2,0),(2,0,1))) else -1
def mat(h,w):return [[Q(0) for _ in range(w)] for _ in range(h)]
def mul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def sub(a,b):
    return [[a[i][j]-b[i][j] for j in range(len(a[0]))] for i in range(len(a))]
def trans(a):return [list(r) for r in zip(*a)]
def diag(v):
    a=mat(len(v),len(v))
    for i,k in enumerate(v):a[i][i]=k
    return a
def identity(n):return diag([Q(1)]*n)
def scaled(a,z):return [[z*y for y in row] for row in a]
def weyl_c(n):
    C=mat(5,5)
    for k in range(5):
        curl=mat(3,3)
        for i in range(3):
            for j in range(3):
                curl[i][j]=sum(
                    Q(eps(q,l,i))*n[q]*B[k][j][l]/2+
                    Q(eps(q,l,j))*n[q]*B[k][i][l]/2
                    for q in range(3) for l in range(3))
        for row in range(5):
            C[row][k]=sum(Q(B[row][i][j])*curl[i][j] for i in range(3) for j in range(3))/D[row]
    return C
def A_weyl(n):
    C=weyl_c(n);A=mat(10,10)
    for i in range(5):
        for j in range(5):
            A[i][5+j]=-C[i][j]
            A[5+i][j]=C[i][j]
    return A
for n in ((Q(1),Q(0),Q(0)),(Q(0),Q(1),Q(0)),
          (Q(0),Q(0),Q(1)),(Q(3,5),Q(4,5),Q(0))):
    C=weyl_c(n)
    # The 5x5 intrinsic curl is Gram-skew, so the 10x10
    # electric/magnetic off-diagonal combination is Gram-symmetric.
    for i in range(5):
        for j in range(5):
            assert D[i]*C[i][j]==-D[j]*C[j][i]
    A=A_weyl(n)
    G=diag(D+D)
    assert mul(G,A)==mul(trans(A),G)
    n2=sum(q*q for q in n)
    # The exact Weyl polynomial has roots 0, +/-|n|/2, +/-|n|.
    # Its minimal annihilating polynomial is z(z²-n²)(z²-n²/4).
    A2=mul(A,A)
    m0=mul(A, mul(sub(A2,scaled(identity(10),n2)),
                   sub(A2,scaled(identity(10),n2/4))))
    assert m0==mat(10,10)
    print("PASS independent Gram-skew curl and 10-field Weyl polynomial",n)

# Independent Schouten stress-derivative calculation with real
# rational variable chi = sigma/c_s: chi_t=-div(v), v_t=-(1/3)grad(chi).
# Work with unit factor b, since the coupling b=2 kappa rho_r/3
# scales every identity homogeneously.
S=[Q(3),Q(-5),Q(11)]
V=[[Q(2),Q(-3),Q(7)],[Q(11),Q(13),Q(-17)],[Q(19),Q(23),Q(29)]]
def DL(mu):
    if mu==0:
        ds=-sum(V[j][j] for j in range(3))
        dv=[-S[j]/3 for j in range(3)]
    else:
        ds=S[mu-1]
        dv=V[mu-1]
    L=mat(4,4)
    L[0][0]=ds
    for j in range(3):
        L[0][j+1]=L[j+1][0]=-dv[j]
        L[j+1][j+1]=ds/3
    return L
L=[DL(i) for i in range(4)]
for k in range(4):
    assert -L[k][0][0]+sum(L[k][i][i] for i in range(1,4))==0
for nu in range(4):
    assert -L[0][0][nu]+sum(L[j+1][j+1][nu] for j in range(3))==0
assert L[1][0][2]-L[0][1][2]==-V[0][1]
print("PASS independent all-rational Schouten divergence/Cotton jet identity")

# Propagate gradient defining and curl constraints by exact matrix
# equations at a rational frequency without using complex arithmetic:
# if U_t=-i R(n)U and W_i,t=-i R(n)W_i,
# Z_i=W_i-i n_i U and F_ij=i(n_i W_j-n_j W_i) obey same equations.
# This is coefficientwise true because R(n) commutes with scalar n_i.
for n in ((Q(1),Q(0),Q(0)),(Q(2,3),Q(1,3),Q(-2,3))):
    cs2=Q(1,3)
    # Radiation eigenpolynomial is z²(z²-c_s²|n|²).
    n2=sum(v*v for v in n)
    R=mat(4,4)
    for i in range(3):
        R[0][i+1]=n[i]
        R[i+1][0]=cs2*n[i]
    R2=mul(R,R)
    assert mul(R,sub(R2,scaled(identity(4),cs2*n2)))==mat(4,4)
    for i,j in ((0,1),(0,2),(1,2)):
        for u in ((Q(2),Q(-1),Q(5),Q(7)),):
            ui=list(u)
            wi=[Q(3+j),Q(5-i),Q(-7),Q(11)]
            wj=[Q(-2),Q(13),Q(i+1),Q(-5)]
            rui=[sum(R[k][l]*ui[l] for l in range(4)) for k in range(4)]
            rwi=[sum(R[k][l]*wi[l] for l in range(4)) for k in range(4)]
            rwj=[sum(R[k][l]*wj[l] for l in range(4)) for k in range(4)]
            # Real coefficient equality for i times the Fourier symbol
            assert [sum(R[k][l]*(wi[l]-n[i]*ui[l]) for l in range(4)) for k in range(4)]==\
                   [rwi[k]-n[i]*rui[k] for k in range(4)]
            assert [sum(R[k][l]*(n[i]*wj[l]-n[j]*wi[l]) for l in range(4)) for k in range(4)]==\
                   [n[i]*rwj[k]-n[j]*rwi[k] for k in range(4)]
    print("PASS independent radiation acoustic polynomial and derivative constraints",n)
print("ALL INDEPENDENT 26-FIELD GRAM AND COTTON TESTS PASS")
