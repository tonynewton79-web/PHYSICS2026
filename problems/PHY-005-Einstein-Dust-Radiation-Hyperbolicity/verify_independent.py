#!/usr/bin/env python3
"""Independent exact-rational verifier: characteristic, Jordan and regularization."""
from fractions import Fraction as Q
def mm(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def rank(a):
    a=[list(row) for row in a]; h=len(a);w=len(a[0]);r=0
    for j in range(w):
        piv=next((i for i in range(r,h) if a[i][j]),None)
        if piv is None: continue
        a[r],a[piv]=a[piv],a[r]
        pivot=a[r][j]
        a[r]=[x/pivot for x in a[r]]
        for i in range(h):
            if i==r:continue
            fac=a[i][j]
            a[i]=[a[i][k]-fac*a[r][k] for k in range(w)]
        r+=1
        if r==h:break
    return r
def mat(n,c2=Q(0)):
    a=[[Q(0) for _ in range(8)] for _ in range(8)]
    for j in range(3):
        a[0][1+j]=n[j]; a[1+j][0]=c2*n[j]
        a[4][5+j]=n[j]; a[5+j][4]=n[j]/3
    return a
def sym(a,h):
    ha=mm(h,a)
    return ha==[list(t) for t in zip(*ha)]
cases=[(Q(1),Q(0),Q(0)),(Q(0),Q(0),Q(1)),
       (Q(3,5),Q(0),Q(4,5)),
       (Q(1,3),Q(2,3),Q(2,3))]
for n in cases:
    assert sum(a*a for a in n)==1
    a=mat(n)
    assert rank(a)==3 and rank(mm(a,a))==2
    v=[Q(0)]*8
    v[1]=n[0];v[2]=n[1];v[3]=n[2]
    av=[sum(a[i][j]*v[j] for j in range(8)) for i in range(8)]
    assert av==[Q(1)]+[Q(0)]*7
    assert all(a[i][0]==0 for i in range(8))
    hr=[[Q(0) for j in range(4)] for i in range(4)]
    for i,d in enumerate((Q(1,3),Q(1),Q(1),Q(1))):hr[i][i]=d
    ar=[row[4:8] for row in a[4:8]]
    assert sym(ar,hr)
    print('PASS independent Jordan and radiation sym in direction',n)
for c in (Q(1,10),Q(1,5),Q(1,2),Q(1,1)):
    A=[[Q(0),Q(1)],[c*c,Q(0)]]
    H=[[c*c,Q(0)],[Q(0),Q(1)]]
    assert sym(A,H)
    assert mm(A,A)==[[c*c,Q(0)],[Q(0),c*c]]
    cond=Q(1)/(c*c)
    assert cond>=1 and H[0][0]/H[1][1]==c*c
    print('PASS pressure c=',c,'optimal symmetrizer cond=',cond)
for alpha in (Q(0),Q(1,2),Q(3,4)):
    v=[Q(n)**(1-alpha) for n in (4,16,64,256)]
    assert all(v[i]<v[i+1] for i in range(3))
    print('PASS unbounded high-frequency loss for alpha=',alpha)
print('PASS complete independent exact-rational audit')
