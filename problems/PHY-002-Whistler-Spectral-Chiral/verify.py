#!/usr/bin/env python3
"""PHY-002: exact whistler and nonlinear chiral structure checks (SymPy 1.14)."""
import sympy as s
x,y,t=s.symbols("x y t",real=True)
B=s.symbols("B",real=True,nonzero=True)
checks=[]
def ok(name,expr):
    value=expr.applyfunc(lambda z:s.trigsimp(s.simplify(s.expand(z)))) if isinstance(expr,s.MatrixBase) else s.trigsimp(s.simplify(s.expand(expr)))
    goal=s.zeros(*value.shape) if isinstance(value,s.MatrixBase) else 0
    assert value==goal,(name,value)
    checks.append(name)
    print("PASS:",name)
def br(f,g):
    return s.diff(f,x)*s.diff(g,y)-s.diff(f,y)*s.diff(g,x)
def lap(f):
    return s.diff(f,x,2)+s.diff(f,y,2)
kx,ky,z=s.symbols("kx ky z")
P=kx**2+ky**2
A=s.Matrix([[0,-s.I*B*kx],[-s.I*B*kx*P,0]])
ok("local 2x2 characteristic polynomial",(z*s.eye(2)-A).det()-(z*z+B*B*kx*kx*P))
ok("local 2x2 quadratic minimal polynomial",A*A+s.eye(2)*B*B*kx*kx*P)
ok("distinct complex factors",s.expand((kx+s.I*ky)*(kx-s.I*ky)-P))
r=s.symbols("r")
Ar=s.Matrix([[0,-s.I*B*kx],[-s.I*B*kx*r*r,0]])
S=s.Matrix([[r,1],[-r,1]])
D=s.diag(-s.I*B*kx*r,s.I*B*kx*r)
ok("algebraic square-root diagonalizer",S*Ar-D*S)
psi=s.cos(x)+s.cos(2*y)
beta=s.cos(x)+2*s.cos(2*y)
ok("real two-mode b-nonlinearity",br(lap(psi),psi)-6*s.sin(x)*s.sin(2*y))
ok("real two-mode a-nonlinearity",br(psi,beta)-2*s.sin(x)*s.sin(2*y))
ok("real two-mode leakage",br(lap(psi),psi)-2*s.sqrt(5)*s.sin(x)*s.sin(2*y)-(6-2*s.sqrt(5))*s.sin(x)*s.sin(2*y))
assert s.simplify(6-2*s.sqrt(5))>0
checks.append("strict real leakage positivity")
print("PASS: strict real leakage positivity")
p=(2,1);q=(1,3)
sp=s.sqrt(p[0]**2+p[1]**2)
sq=s.sqrt(q[0]**2+q[1]**2)
sk=s.sqrt((p[0]+q[0])**2+(p[1]+q[1])**2)
cross=p[0]*q[1]-p[1]*q[0]
ok("ordered Fourier symmetrization",cross*(sp**2-sq**2+sk*(sq-sp))-cross*(sp-sq)*(sp+sq-sk))
# The two Fourier wavevectors (1,2) and (2,-1) have the same length sqrt(5).
psi0=s.cos(x+2*y)+3*s.sin(2*x-y)
ok("noncollinear equal-radius Helmholtz shell",lap(psi0)+5*psi0)
ok("equal-radius nonlinear a-channel",br(psi0,s.sqrt(5)*psi0))
ok("equal-radius nonlinear b-channel",br(lap(psi0),psi0))
for sigma in (1,-1):
    speed=sigma*B*s.sqrt(5)
    wave=s.cos((x-speed*t)+2*y)+3*s.sin(2*(x-speed*t)-y)
    pol=sigma*s.sqrt(5)*wave
    ok("exact psi PDE for helicity "+str(sigma),s.diff(wave,t)+B*s.diff(pol,x)-br(wave,pol))
    ok("exact beta PDE for helicity "+str(sigma),s.diff(pol,t)-B*s.diff(lap(wave),x)-br(lap(wave),wave))
print("ALL EXACT CHECKS PASS:",len(checks))
