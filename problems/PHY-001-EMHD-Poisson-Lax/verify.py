#!/usr/bin/env python3
"""PHY-001: exact, deterministic independent checks. SymPy 1.14.0."""
import sympy as S

x, y, z, t = S.symbols("x y z t", real=True)
PASS = []

def zero(expr, name):
    reduced = S.trigsimp(S.simplify(S.expand(expr)))
    assert reduced == 0, (name, reduced)
    PASS.append(name)
    print("PASS:", name)

def bracket(f, g):
    return S.diff(f, x) * S.diff(g, y) - S.diff(f, y) * S.diff(g, x)

def lap(f):
    return S.diff(f, x, 2) + S.diff(f, y, 2)

def curl(v):
    return S.Matrix([
        S.diff(v[2], y) - S.diff(v[1], z),
        S.diff(v[0], z) - S.diff(v[2], x),
        S.diff(v[1], x) - S.diff(v[0], y),
    ])

# A: Direct 3D parent equation --> gauge-fixed 2.5D PDE.
a = x**2*y + 3*x*y**2 + x*y + y**3
b = x*y**3 - 2*x**2*y + y + x**3
q = lap(a)
B = S.Matrix([S.diff(a, y), -S.diff(a, x), b])
J = curl(B)
hall = curl(J.cross(B))
divergence = S.diff(B[0], x) + S.diff(B[1], y) + S.diff(B[2], z)
zero(divergence, "2.5D divergence-free ansatz")
zero(hall[0] + S.diff(bracket(a, b), y), "2.5D horizontal x equation")
zero(hall[1] - S.diff(bracket(a, b), x), "2.5D horizontal y equation")
zero(hall[2] + bracket(q, a), "2.5D vertical equation")

# B: Linearization in independent perturbations.
eps, B0 = S.symbols("eps B0", real=True)
psi = x**3 + x*y + y**2
beta = x*y**2 + y**3
a_lin = B0*y + eps*psi
b_lin = eps*beta
zero(S.diff(bracket(a_lin, b_lin), eps).subs(eps, 0) + B0*S.diff(beta, x),
     "linearized potential equation")
zero(S.diff(bracket(lap(a_lin), a_lin), eps).subs(eps, 0)
     - B0*S.diff(lap(psi), x), "linearized vertical equation")

# C: The nontrivial whistler characteristic polynomial.
kx, ky, omega = S.symbols("kx ky omega", real=True)
symbol = S.Matrix([[-omega, B0*kx],
                   [B0*kx*(kx**2 + ky**2), -omega]])
zero(symbol.det() - (omega**2 - B0**2*kx**2*(kx**2+ky**2)),
     "linear whistler principal symbol")

# D: Known nonlinear positive control in the 3D parent system.
A, k = S.symbols("A k", real=True)
theta = k*z + B0*k**2*t   # omega = -B0*k**2.
wave = S.Matrix([A*S.cos(theta), A*S.sin(theta), B0])
res = wave.diff(t) + curl(curl(wave).cross(wave))
assert all(S.trigsimp(S.simplify(v)) == 0 for v in res), res
zero(S.diff(wave[0], x) + S.diff(wave[1], y) + S.diff(wave[2], z),
     "known nonlinear whistler divergence")
PASS.append("known nonlinear whistler EMHD residual")
print("PASS: known nonlinear whistler EMHD residual")

# E: Third-jet witness forces the coefficient of Delta(a_t) to vanish.
a0, b0, q0, s = S.symbols("a0 b0 q0 s", real=True)
aa = a0+x+q0*(x**2+y**2)/4
bb = b0+s*y**3/6
qq = lap(aa)
jet = S.simplify(lap(bracket(aa, bb)).subs({x:0, y:0}))
zero(jet-s, "third-jet isolation of F_q")
assert S.simplify(qq.subs({x:0,y:0})-q0) == 0

# F: Eliminate G_q under F_b != 0 using exact polynomial arithmetic.
Fa, Fb, Gq, invFb = S.symbols("Fa Fb Gq invFb")
gb = S.groebner([Fb-Gq*Fa, Gq*Fb, invFb*Fb-1],
                Fa, Fb, Gq, invFb, order="lex")
assert gb.is_zero_dimensional and list(gb) == [S.Integer(1)], list(gb)
PASS.append("Groebner contradiction for F_b nonzero")
print("PASS: Groebner contradiction for F_b nonzero")

# G: Positive example for scalar first-equation transport.
f = a**3 + 2*a
h = a**2 + a
L, M = f, -b+h
zero(bracket(M, L) - S.diff(f, a) * bracket(a,b)
     if False else bracket(M,L) - (3*a**2+2)*bracket(a,b),
     "classification positive example")

print("ALL PASSED:", len(PASS), "exact checks")
