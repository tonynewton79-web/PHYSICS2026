#!/usr/bin/env python3
"""PHY-003 all-orders SU(2) Wilson KP gate: exact rational certificate.
This verifies a SU(2) *sufficient* analyticity condition, not any
continuum-limit Yang--Mills statement. Python standard library only.
"""
from fractions import Fraction as Q
from math import factorial
r=Q(1,250)
# e < 68/25, proved directly using a positive-tail factorial bound.
E5=sum((Q(1,factorial(n)) for n in range(6)),Q(0))
E_tail=Q(1,factorial(6))/(1-Q(1,7))
assert E5+E_tail < Q(68,25)
# c0(z) = sum_{n>=0} z^(2n)/(4^n n! (n+1)!).
# Terms for n>=1 have successive ratio <= r^2/24.
c0tail=(r*r/Q(8))/(1-r*r/Q(24))
assert 0<c0tail<Q(1,100000)
# For |beta| <= r, |c0(beta)| >= 1-c0tail.
# The normalized SU2 nontrivial character mass is bounded by:
# (exp(r)-c0(r))/(2-c0(r)) <= (exp(r)-1)/(1-c0tail)
# exp(r)-1 <= r/(1-r).
mass_upper=r/((1-r)*(1-c0tail))
alpha=Q(68,25)*mass_upper
x=80*alpha
assert 0<x<1
# The root-connected set Catalan majorant is:
# sum_{h>=6} 80^(h-1)alpha^h = (x^6/80)/(1-x)
# Each plaquette of a polymer excludes at most 21 root positions.
kp=Q(21,80)*x**6/(1-x)
assert kp<1,(kp,float(kp))
assert 1-x-Q(21,80)*x**6>0
print("certified radius r =",r)
print("c0(r)-1 upper bound",float(c0tail))
print("all-spin character mass upper bound",float(mass_upper))
print("80 e upper times character mass",float(x))
print("Kotecky-Preiss bound (exact rational) <",float(kp),"<1")
print("rigorous quantitative slack >",float(1-kp))
print("PASS: volume-uniform SU(2) Wilson analytic disk, |beta|<=1/250")
