#!/usr/bin/env python3
"""Second-pass geometric checks using Python standard library only."""
from math import isqrt
def cross(p,q): return p[0]*q[1]-p[1]*q[0]
def norm2(p): return p[0]*p[0]+p[1]*p[1]
count=0
for px in range(-3,4):
 for py in range(-3,4):
  p=(px,py)
  if norm2(p)==0: continue
  for qx in range(-3,4):
   for qy in range(-3,4):
    q=(qx,qy)
    if norm2(q)==0: continue
    c=cross(p,q)
    dot=p[0]*q[0]+p[1]*q[1]
    S2,T2=norm2(p),norm2(q)
    assert S2*T2-dot*dot==c*c
    if c:
      assert S2*T2>dot*dot
      assert S2>0 and T2>0
    pair_symbol_zero=(c==0 or S2==T2)
    if c!=0 and S2!=T2: assert not pair_symbol_zero
    count+=1
print("PASS integer vector determinant and strict triangle gates:",count)
assert 9>5  # 6-2sqrt(5)>0
print("PASS real two-mode strict leakage positivity")
p=(1,2);q=(2,-1)
assert norm2(p)==norm2(q)==5 and cross(p,q)==-5
print("PASS noncollinear equal-radius shell")
print("SECOND PASS COMPLETE")
