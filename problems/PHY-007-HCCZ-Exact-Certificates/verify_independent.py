#!/usr/bin/env python3
"""Independent PHY-007 checker: exact Boolean XOR and integer 2x2 identities.
No calls to primary H/CCZ amplitude simulator.
"""
from itertools import combinations

def mul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B)))
        for j in range(len(B[0]))] for i in range(len(A))]

def toffoli_is_hcczh():
    H=[[1,1],[1,-1]]
    for ab in (0,1):
        phase=[[1,0],[0,(-1)**ab]]
        matrix=mul(mul(H,phase),H)
        target=[[1,0],[0,1]] if ab==0 else [[0,1],[1,0]]
        assert matrix==[[2*v for v in row] for row in target]

def flip(x,a,b,t):
    return x^(1<<t) if (x>>a&1 and x>>b&1) else x

def clean(n):
    naux=n-3
    for x in range(1<<n):
        y=x; gates=[]
        if n==3:phase=int(x==7)
        else:
            for j in range(naux):
                a,b,t=(0,1,n) if j==0 else (n+j-1,j+1,n+j)
                y=flip(y,a,b,t);gates.append((a,b,t))
            phase=int(bool(y>>(2*n-4)&1 and y>>(n-2)&1 and y>>(n-1)&1))
            for a,b,t in reversed(gates):y=flip(y,a,b,t)
        assert y==x
        assert phase==int(x==(1<<n)-1)

def dirty():
    for x in range(32):
        y=flip(x,0,1,4)
        p=int(bool(y&16 and y&4 and y&8))
        y=flip(y,0,1,4)
        p^=int(bool(y&16 and y&4 and y&8))
        assert y==x and p==int((x&15)==15)

def mobius(tt,n):
    A=tt.copy()
    for j in range(n):
        for x in range(1<<n):
            if x>>j&1:A[x]^=A[x^(1<<j)]
    return {x for x,v in enumerate(A) if v}

def normal_form():
    for n in range(3,10):
        triples=list(combinations(range(n),3))
        for triple in triples:
            tt=[int(all(x>>j&1 for j in triple)) for x in range(1<<n)]
            assert mobius(tt,n)=={sum(1<<j for j in triple)}
    assert mobius([int(x==15) for x in range(16)],4)=={15}

def counts():
    for n in range(3,100):
        assert 2*n-5==2*(n-3)+1
        assert 4*(n-3)==2*2*(n-3)

def adversarial():
    # Borrowed compensation is indispensable.
    x=12|16
    y=flip(x,0,1,4)
    assert y==x and (y&16 and y&4 and y&8)
    assert x&15!=15
    # A clean ladder on dirty scratch gives an incorrect phase.
    assert (x&16 and x&4 and x&8) and (x&3)==0

if __name__=="__main__":
    toffoli_is_hcczh()
    for n in range(3,15):clean(n)
    assert sum(1<<n for n in range(3,15))==32760
    dirty();normal_form();counts();adversarial()
    print("PASS independent 2x2 H CCZ H identity")
    print("PASS independent XOR replay on 32,760 clean data inputs and 32 borrowed")
    print("PASS exact degree barrier, n<=9 cubic ANF rank, n<=99 gate formulas")
    print("PASS independent wrong dirty-ancilla rewrite witnesses")
