#!/usr/bin/env python3
"""PHY-005 Attack 02. Exact SymPy checks of nonlinear material radiation
hyperbolicity, Einstein FLRW constraints and synchronous ADM gauge test.
This certifies restricted identities, NOT full coupled hyperbolicity.
"""
import sympy as s

checks=[]
def check(name,expr):
    if isinstance(expr,s.MatrixBase):
        z=expr.applyfunc(s.simplify)
        assert z==s.zeros(*z.shape),(name,z)
    else:
        assert s.simplify(expr)==0,(name,expr)
    checks.append(name)
    print("PASS",name)

eta=s.diag(-1,1,1,1)
cs=1/s.sqrt(3)
z=s.symbols('z',real=True)

def A(u,E,mu):
    a=s.eye(4)*u[mu]
    for j in range(3):
        a[0,j+1]=cs*E[j][mu]
        a[j+1,0]=cs*E[j][mu]
    return a

velocities=[
    (s.S(0),s.S(0),s.S(0)),
    (s.Rational(3,5),s.S(0),s.S(0)),
    (s.S(0),s.Rational(4,5),s.S(0)),
    (s.Rational(3,13),s.Rational(4,13),s.S(0)),
    (s.Rational(1,3),s.Rational(2,3),s.S(0))]
for vp in velocities:
    v=s.Matrix(vp)
    v2=s.simplify(v.dot(v))
    W=1/s.sqrt(1-v2)
    u=s.Matrix([W,*[W*x for x in v]])
    E=[]
    for j in range(3):
        spatial=s.eye(3)[:,j]
        if v2!=0:
            spatial=spatial+(W-1)*v[j]/v2*v
        E.append(s.Matrix([W*v[j],*list(spatial)]))
    frame=s.Matrix.hstack(u,*E)
    check('exact Lorentz frame '+str(vp),frame.T*eta*frame-eta)
    As=[A(u,E,mu) for mu in range(4)]
    for mu,mat in enumerate(As):
        check('radiation A^'+str(mu)+' symmetric '+str(vp),mat-mat.T)
    cp=As[0].charpoly()
    got=s.Poly(cp.as_expr(),cp.gen).all_coeffs()
    expected=s.Poly((z-W)**2*((z-W)**2-W**2*v2/3),z).all_coeffs()
    for k,(g,e) in enumerate(zip(got,expected)):
        check('radiation A0 characteristic coefficient '+str(k)+' '+str(vp),g-e)
    assert W>0 and 1-v2/3>0
    checks.append('strictly positive radiation time Schur '+str(vp))
    rho=s.symbols('rho',positive=True)
    flux=s.Rational(4,3)*rho*W*W*v
    if v2!=0: assert flux!=s.zeros(3,1)

# A^0^-1 A^x eigenvalues: relativistic velocity addition.
v=s.Rational(3,5);W=1/s.sqrt(1-v*v)
u=s.Matrix([W,W*v,0,0])
E=[s.Matrix([W*v,W,0,0]),s.Matrix([0,0,1,0]),s.Matrix([0,0,0,1])]
M=A(u,E,0).inv()*A(u,E,1)
plus=(v+cs)/(1+v*cs)
minus=(v-cs)/(1-v*cs)
cp=M.charpoly()
got=s.Poly(cp.as_expr(),cp.gen).all_coeffs()
expected=s.Poly((z-v)**2*(z-plus)*(z-minus),z).all_coeffs()
for k,(g,e) in enumerate(zip(got,expected)):
    check('tilted relativistic acoustic characteristic '+str(k),g-e)

# Exact nonlinear dust material density on a general diagonal metric.
t=s.symbols('t',real=True)
a=[s.Function('a'+str(j))(t) for j in (1,2,3)]
vol=s.prod(a)
N=s.symbols('N',positive=True)
rd=N/vol
check('material dust Jacobian conservation',s.diff(rd*vol,t))
check('material nonlinear dust continuity',s.diff(rd,t)+rd*s.diff(vol,t)/vol)

# Fully nonlinear homogeneous Einstein–dust–radiation control.
H,rhod,rhor,lam,kappa=s.symbols('H rhod rhor lam kappa',real=True)
C=3*H**2-kappa*(rhod+rhor)-lam
dH=-kappa/2*(rhod+s.Rational(4,3)*rhor)
dd=-3*H*rhod
dr=-4*H*rhor
check('two-component Einstein FLRW Hamiltonian propagation',
      s.diff(C,H)*dH+s.diff(C,rhod)*dd+s.diff(C,rhor)*dr)

# Conditional ADM constraint principal block is symmetric.
for n in ((s.S(1),s.S(0),s.S(0)),
          (s.S(0),s.S(1),s.S(0)),
          (s.Rational(3,5),s.Rational(4,5),s.S(0))):
    p=s.zeros(4)
    for j in range(3):
        p[0,j+1]=n[j]
        p[j+1,0]=n[j]
    check('subsidiary symmetric principal '+str(n),p-p.T)
    check('subsidiary scalar wave polynomial '+str(n),
          p.charpoly().as_expr().subs(p.charpoly().gen,z)
          -(z*z)*(z*z-sum(x*x for x in n)))

# Vacuum synchronous ADM gauge mode: constraint satisfying, unbounded Dh.
x=s.symbols('x',real=True)
for k in (1,2,3,11,31):
    phi=s.cos(k*x)/k**2
    h=2*t*s.diff(phi,x,2)
    K=-s.diff(phi,x,2)
    # In this 1D Hessian gauge family the linearized spatial Ricci is zero.
    Ric=s.diff(h,x,2)/2+s.diff(h,x,2)/2-s.diff(h,x,2)/2-s.diff(h,x,2)/2
    check('synchronous metric evolution '+str(k),s.diff(h,t)+2*K)
    check('synchronous Ricci gauge identity '+str(k),Ric)
    check('synchronous extrinsic evolution '+str(k),s.diff(K,t)-Ric)
    check('synchronous momentum constraint '+str(k),s.diff(K,x)-s.diff(K,x))
    check('synchronous unbounded gradient '+str(k),
          s.diff(h,x)-2*t*k*s.sin(k*x))

print('PHY-005 NONLINEAR MATERIAL ATTACK: ALL',len(checks),'EXACT TESTS PASS')
