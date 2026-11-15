#!/usr/bin/env python3
"""PHY-003 exact rooted F2 plaquette closure test; Python standard library."""
from collections import Counter
D=4
E=[tuple(int(i==j) for i in range(D)) for j in range(D)]
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def edges(p):
    x,i,j=p
    return {(x,i),(add(x,E[j]),i),(x,j),(add(x,E[i]),j)}
def around(e):
    x,i=e
    return {(shift,min(i,j),max(i,j)) for j in range(D) if j!=i
            for shift in (x,sub(x,E[j]))}
def faces(c):
    x,axes=c
    return frozenset((shift,*tuple(j for j in axes if j!=i))
                     for i in axes for shift in (x,add(x,E[i])))
def containing(p):
    x,i,j=p
    return {(shift,tuple(sorted((i,j,k)))) for k in range(D)
            if k not in (i,j) for shift in (x,sub(x,E[k]))}
def boundary(S):
    odd=set()
    for p in S: odd.symmetric_difference_update(edges(p))
    return odd
root=((0,0,0,0),0,1)
seen={frozenset([root])}; found=set()
def search(S,odd):
    if not odd:
        found.add(S)
        return
    if len(S)>=10 or len(odd)>4*(10-len(S)): return
    pivot=min(odd)
    for p in around(pivot):
        if p in S: continue
        nxt=S|{p}
        if nxt in seen: continue
        seen.add(nxt)
        search(nxt,odd.symmetric_difference(edges(p)))
search(frozenset([root]),edges(root))
counts=Counter(map(len,found))
assert counts=={6:4,10:60},counts
assert len(seen)==30259, len(seen)
assert all(not boundary(s) for s in found)
print("PASS root-complete closure DFS:",counts,"states",len(seen))
rootcubes=containing(root)
six={faces(c) for c in rootcubes}
pairs={}
for c in rootcubes:
    for shared in faces(c):
        for d in containing(shared):
            if c==d: continue
            pair=frozenset((c,d))
            shell=faces(c)^faces(d)
            if root in shell:
                assert len(shell)==10
                pairs[pair]=shell
assert len(pairs)==60 and len(set(pairs.values()))==60
assert six|set(pairs.values())==found
same=sum(len({c[1] for c in pair})==1 for pair in pairs)
assert (same,60-same)==(20,40)
print("PASS independent root pair construction: coplanar=20 mixed=40")
facets=[((0,0,0,0),tuple(j for j in range(D) if j!=omit)) for omit in range(D)]
s12=frozenset()
for c in facets: s12=s12^faces(c)
assert len(s12)==12 and not boundary(s12)
print("PASS four-coordinate 12-face cycle")
print("PHY-003 ROOTED EXACT SUITE: ALL PASS")
