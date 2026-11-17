#!/usr/bin/env python3
"""PHY-009: exact limited-scope proof-gate regression (not a PDE certificate)."""
from fractions import Fraction
from itertools import product
from math import sqrt

e = [(s if i == j else 0 for i in range(3)) for j in range(3) for s in (-1, 1)]
K1 = {tuple(x) for x in e}
K3 = {tuple(a[i] + b[i] + c[i] for i in range(3))
      for a, b, c in product(K1, repeat=3)}
F3 = {(-1,0,0),(1,0,0),(-3,0,0),(3,0,0)}
F3.update((sx,sy,sz) for sx,sy,sz in product((-1,1), repeat=3))
assert len(K1) == 6 and len(K3) == 44
assert F3 <= K3 and len(F3) == 12 and len(K3-F3) == 32

# Frobenius norm squared of antisymmetric momentum-constraint adjustment is 4|M|².
for M in product(range(-3,4), repeat=3):
    actual = sum(((1 if i == j else 0)*M[b]
                  -(1 if i == b else 0)*M[j])**2
                 for i,j,b in product(range(3), repeat=3))
    assert actual == 4*sum(x*x for x in M)

from decimal import Decimal
J = Decimal("0.000437821879636209272")
ceiling = Decimal(1)/Decimal(3600)
gate = J - ceiling
assert gate > Decimal("0.0001600441018584")
assert Decimal("0.0000878") + Decimal("0.000072") < gate

print("PASS: 44 cubic candidates, 12 forbidden, 32 permitted")
print("PASS: ||A[M]||_F^2 = 4 ||M||_2^2")
print("PASS: rational witness margin and conditional two-term error budget")
print("NOT TESTED: nonlinear Einstein PDE, continuum existence, stability or novelty")
