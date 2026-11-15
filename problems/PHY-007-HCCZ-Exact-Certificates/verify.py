#!/usr/bin/env python3
"""PHY-007 exact H/CCZ verification, using signed integer amplitudes only."""
from collections import defaultdict
from itertools import combinations

def validate(G,N):
    for g in G:
        if not isinstance(g,tuple) or not g or g[0] not in ("H","CCZ"):
            raise ValueError("unsupported gate")
        w=g[1:]; size=1 if g[0]=="H" else 3
        if len(w)!=size or len(set(w))!=size or any(type(q)!=int or q<0 or q>=N for q in w):
            raise ValueError("invalid gate arity/indices")

def toff(a,b,t):
    return [("H",t),("CCZ",a,b,t),("H",t)]

def clean(n):
    assert n>=3
    if n==3:return [("CCZ",0,1,2)]
    anc=list(range(n,2*n-3))
    ladder=[toff(0,1,anc[0])]
    for j in range(1,len(anc)):
        ladder.append(toff(anc[j-1],j+1,anc[j]))
    return ([g for b in ladder for g in b]+
        [("CCZ",anc[-1],n-2,n-1)]+
        [g for b in reversed(ladder) for g in b])

def borrowed():
    return toff(0,1,4)+[("CCZ",4,2,3)]+toff(0,1,4)+[("CCZ",4,2,3)]

def apply(G,N,x):
    validate(G,N)
    A={x:1};h=0
    for gate in G:
        if gate[0]=="CCZ":
            mask=sum(1<<q for q in gate[1:])
            A={i:-v if i&mask==mask else v for i,v in A.items()}
        else:
            h+=1; bit=1<<gate[1]; B=defaultdict(int)
            for i,v in A.items():
                if i&bit:
                    B[i&~bit]+=v;B[i]-=v
                else:
                    B[i]+=v;B[i|bit]+=v
            A={i:v for i,v in B.items() if v}
    return h,A

def equal(a,b):
    h,A=a; k,B=b
    if (h-k)%2:return False
    m=max(h,k);p=1<<((m-h)//2);q=1<<((m-k)//2)
    return {i:p*v for i,v in A.items()}=={i:q*v for i,v in B.items()}

def anf(tt,n):
    z=list(tt)
    for j in range(n):
        for i in range(1<<n):
            if i>>j&1:z[i]^=z[i^(1<<j)]
    return [i for i,v in enumerate(z) if v]

def main():
    total=0
    for n in range(3,13):
        G=clean(n);N=2*n-3
        assert sum(g[0]=="H" for g in G)==4*(n-3)
        assert sum(g[0]=="CCZ" for g in G)==2*n-5
        for x in range(1<<n):
            y={x:-1 if x==(1<<n)-1 else 1}
            assert equal(apply(G,N,x),(0,y)),(n,x)
            total+=1
    assert total==8184
    G=borrowed()
    for x in range(32):
        assert equal(apply(G,5,x),(0,{x:-1 if x&15==15 else 1}))
    # Adversarial: omitted borrowed correction fails.
    wrong=G[:-1]
    assert any(not equal(apply(wrong,5,x),(0,{x:-1 if x&15==15 else 1}))
               for x in range(32))
    # Adversarial: clean scratch cannot be borrowed; missing uncompute fails.
    C=clean(4)
    assert any(not equal(apply(C,5,x),(0,{x:-1 if x&15==15 else 1}))
               for x in range(16,32))
    assert any(not equal(apply(C[:-3],5,x),(0,{x:-1 if x&15==15 else 1}))
               for x in range(16))
    # CCZ-only Boolean phase normal form and the quartic barrier.
    tested=0
    for n in range(3,8):
        tr=list(combinations(range(n),3))
        for mask in range(min(101,1<<len(tr))):
            chosen=[t for j,t in enumerate(tr) if mask>>j&1]
            tt=[sum(all(x>>j&1 for j in t) for t in chosen)%2 for x in range(1<<n)]
            assert anf(tt,n)==sorted(sum(1<<j for j in t) for t in chosen)
            tested+=1
    assert tested==321
    assert anf([int(x==15) for x in range(16)],4)==[15]
    # Invariant h mod 2 and noncommutativity of a shared H/CCZ pair.
    assert not equal((0,{0:1}),(1,{0:1}))
    for n in range(3,8):
        A=clean(n); B=[("H",0),("H",0)]+A
        assert all(equal(apply(A,2*n-3,x),apply(B,2*n-3,x))
                   for x in range(1<<n))
    A=[("H",2),("CCZ",0,1,2)]
    B=[("CCZ",0,1,2),("H",2)]
    assert any(not equal(apply(A,3,x),apply(B,3,x)) for x in range(8))
    rejected=0
    for G in [[("S",0)],[("T",0)],[("CZ",0,1)],[("CCZ",0,0,1)],[("H",-1)]]:
        try:validate(G,3)
        except ValueError:rejected+=1
    assert rejected==5
    print("PASS:",total,"full clean H-CCZ basis states, 32 borrowed states")
    print("PASS:",tested,"CCZ phase normal-form tests; quartic excluded")
    print("PASS: H parity, wrong rewrites, all unsupported gates rejected")
if __name__=="__main__":main()
