#!/usr/bin/env python3
"""PHY-003 second verifier: periodic cell incidence, not rooted DFS."""
from itertools import combinations,product
D=4; L=4; V=L**4
def faces(base,axes):
    F=[]
    for i in axes:
        for offset in (0,1):
            x=list(base); x[i]=(x[i]+offset)%L
            F.append((tuple(x),tuple(j for j in axes if j!=i)))
    return frozenset(F)
plaquettes={(x,axes):set() for x in product(range(L),repeat=D)
            for axes in combinations(range(D),2)}
cubes={}
for x in product(range(L),repeat=D):
    for axes in combinations(range(D),3):
        c=(x,axes)
        cubes[c]=faces(x,axes)
        for p in cubes[c]: plaquettes[p].add(c)
assert len(plaquettes)==6*V and len(cubes)==4*V
assert all(len(a)==4 for a in plaquettes.values())
assert all(len(a)==6 for a in cubes.values())
print("PASS periodic cells:",len(plaquettes),"plaquettes and",len(cubes),"cubes")
pairs={}
for shared,inc in plaquettes.items():
    for a,b in combinations(sorted(inc),2):
        pair=(a,b)
        assert pair not in pairs
        surface=cubes[a]^cubes[b]
        assert len(surface)==10
        pairs[pair]=surface
assert len(pairs)==36*V
assert len(set(pairs.values()))==len(pairs)
same=sum(a[1]==b[1] for a,b in pairs)
assert (same,len(pairs)-same)==(12*V,24*V)
print("PASS all ten-face cycles:",len(pairs),"same",same,"mixed",len(pairs)-same)
root=((0,0,0,0),(0,1))
n6=sum(root in s for s in cubes.values())
n10=sum(root in s for s in pairs.values())
n10same=sum(root in s and a[1]==b[1] for (a,b),s in pairs.items())
assert (n6,n10,n10same,n10-n10same)==(4,60,20,40)
print("PASS anchored independent multiplicities:",n6,n10,n10same,n10-n10same)
print("PASS finite-torus Z2 gauge coefficients: 4 and 36 per site")
print("PHY-003 INDEPENDENT PERIODIC SUITE: ALL PASS")
