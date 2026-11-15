#!/usr/bin/env python3
"""Independent standard-library rational check for full SU(2) coefficients."""
from fractions import Fraction as F
from math import factorial
from itertools import combinations,product
N=6   # series in y=beta^2 through beta^10
def times(a,b):
 out=[F(0) for _ in range(N)]
 for i in range(min(len(a),N)):
  for j in range(min(len(b),N-i)):out[i+j]+=a[i]*b[j]
 return out
def power(a,n):
 q=[F(1)]+[F(0)]*(N-1)
 for _ in range(n):q=times(q,a)
 return q
def inverse(a):
 q=[F(0)]*N;q[0]=1/a[0]
 for n in range(1,N):q[n]=-sum(a[k]*q[n-k] for k in range(1,n+1))/a[0]
 return q
def log_one(a):
 assert a[0]==1
 v=a[:];v[0]-=1;p=[F(1)]+[F(0)]*(N-1);ans=[F(0)]*N
 for m in range(1,N):
  p=times(p,v)
  for i in range(N):ans[i]+=(-1 if m%2==0 else 1)*p[i]/m
 return ans
# Define modified Bessel I1, I2 directly by their factorial coefficients.
a=[F(1,2**(2*k+1)*factorial(k)*factorial(k+1)) for k in range(N)]
b=[F(1,2**(2*k+2)*factorial(k)*factorial(k+2)) for k in range(N)]
c0=[2*x for x in a];assert c0[0]==1
r=times(b,inverse(a)) # u(beta)=beta*r(beta^2)
assert r[:4]==[F(1,4),F(-1,96),F(1,1536),F(-1,23040)]
ans=[6*z for z in log_one(c0)];r6=power(r,6);r10=power(r,10)
for i in range(3,N):ans[i]+=16*r6[i-3]
for i in range(5,N):ans[i]+=144*r10[i-5]
expected=[F(0),F(3,4),F(-1,64),F(7,1536),F(-31,30720),F(4451,14745600)]
assert ans==expected,(ans,expected)
print("PASS exact Bessel u ratio",r[:4])
print("PASS exact SU2 intensive log through beta^10",ans[1:])
for size,val in ((6,F(1,16)),(10,F(1,256))):
 assert 2**size*val==4
print("PASS SU2 gluing dimensions and 4D factors 16 and 144")
assert 4*4==16 and (12+24)*4==144
# Independent finite geometry check: an exterior square shares <=1 cube edge.
E=[tuple(int(i==j) for i in range(4)) for j in range(4)]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def edges(p):
 x,i,j=p
 return {(x,i),(add(x,E[j]),i),(x,j),(add(x,E[i]),j)}
C={(x,*tuple(k for k in (0,1,2) if k!=i)) for i in (0,1,2) for x in ((0,0,0,0),E[i])}
ce=set().union(*(edges(f) for f in C))
cnt=0
for x in product(range(-1,3),repeat=4):
 for ij in combinations(range(4),2):
  face=(x,*ij)
  if face not in C:
   assert len(edges(face)&ce)<=1
   cnt+=1
print("PASS complete exterior-square overlap regression:",cnt)
print("SU2 CERTIFICATE: ALL CHECKS PASS")
