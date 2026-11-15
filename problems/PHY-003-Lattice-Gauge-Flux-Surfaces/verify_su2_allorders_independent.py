#!/usr/bin/env python3
"""Independent interval evaluation of SU2 all-spin majorant from
the original positive Bessel and exponential series (no 1/(1-r)
shortcut, no rational substitution used in the first checker).
This is a separate certified calculation, all intervals rational.
"""
from fractions import Fraction as Q
from math import factorial
r=Q(1,250)
# Bessel c0(r) via direct positive coefficient series and tail.
N=6
term=lambda n: r**(2*n)/Q(4**n*factorial(n)*factorial(n+1))
clo=sum((term(n) for n in range(N+1)),Q(0))
nextterm=term(N+1)
chi=clo+nextterm/(1-r*r/Q(4*(N+2)*(N+3)))
# e^r series and ratio bounded tail
M=8
elo=sum((r**n/Q(factorial(n)) for n in range(M+1)),Q(0))
nextE=r**(M+1)/Q(factorial(M+1))
ehi=elo+nextE/(1-r/Q(M+2))
assert 1<clo<chi<2
assert 1<elo<ehi<2
# q=(e^r-c0)/(2-c0), decreasing in c0 (because e^r<2)
qlow=(elo-chi)/(2-chi)
qhigh=(ehi-clo)/(2-clo)
assert 0<qlow<qhigh
# independent factorial lower/upper interval for Euler e
M=12
e0=sum((Q(1,factorial(n)) for n in range(M+1)),Q(0))
e1=e0+Q(1,factorial(M+1))/(1-Q(1,M+2))
assert Q(2718,1000)<e0<e1<Q(272,100)
xhigh=80*e1*qhigh
assert xhigh<1
# Evaluate Kotecky-Preiss majorant as a recurrence of terms:
# 21 * sum_{h>=6} 80^{h-1} (e q)^h
# exact geometric tail, independent of polynomial residual check.
t6=Q(21)*80**5*(e1*qhigh)**6
tail=t6/(1-xhigh)
assert tail<1
print("certified q interval: ",float(qlow),"< q <",float(qhigh))
print("certified root growth parameter x <",float(xhigh))
print("independent KP inequality <",float(tail),"<1")
print("PASS: rational-interval Bessel/exp direct-series replay")
