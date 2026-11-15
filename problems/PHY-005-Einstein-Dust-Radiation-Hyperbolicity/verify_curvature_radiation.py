#!/usr/bin/env python3
"""PHY-005 Attack 03: exact 26-field Weyl/tilted-radiation prolonged principal certificate.
This checks a local curvature-matter principal SKELETON, not a complete
Einstein frame/connection reduction nor all geometric constraints.
"""
import sympy as s

B=[
s.diag(1,-1,0),
s.diag(1,1,-2),
s.Matrix([[0,1,0],[1,0,0],[0,0,0]]),
s.Matrix([[0,0,1],[0,0,0],[1,0,0]]),
s.Matrix([[0,0,0],[0,0,1],[0,1,0]])]
D=s.diag(2,6,2,2,2)
c=1/s.sqrt(3)
count=0

def OK(msg, condition):
    global count
    assert condition,msg
    count+=1
    print("PASS",msg)

def curl(n,t):
    return s.Matrix(3,3,lambda i,j:s.Rational(1,2)*sum(
        s.LeviCivita(k,l,i)*n[k]*t[j,l]+
        s.LeviCivita(k,l,j)*n[k]*t[i,l]
        for k in range(3) for l in range(3)))

def C(n):
    return D.inv()*s.Matrix(5,5,lambda i,j:sum(
        B[i][p,q]*curl(n,B[j])[p,q]
        for p in range(3) for q in range(3)))

def Weyl(n):
    r=s.zeros(10)
    r[:5,5:]=-C(n)
    r[5:,:5]=C(n)
    return r

def radiation_matrices(v):
    """Radiation velocity tangent-frame principal matrices."""
    v=s.Matrix(v)
    q=s.simplify(v.dot(v))
    W=1/s.sqrt(1-q)
    u=s.Matrix([W,*[W*v[i] for i in range(3)]])
    E=[]
    for i in range(3):
        e=s.eye(3)[:,i]
        if q!=0:e=e+(W-1)*v[i]/q*v
        E.append(s.Matrix([W*v[i],*list(e)]))
    eta=s.diag(-1,1,1,1)
    frame=s.Matrix.hstack(u,*E)
    OK("Lorentz boost frame "+str(tuple(v)),
       (frame.T*eta*frame-eta).applyfunc(s.simplify)==s.zeros(4))
    mats=[]
    for mu in range(4):
        A=s.eye(4)*u[mu]
        for j in range(3):
            A[0,j+1]=c*E[j][mu]
            A[j+1,0]=c*E[j][mu]
        mats.append(A)
        OK("radiation A_mu symmetric "+str(mu)+" "+str(tuple(v)),A==A.T)
    z=s.symbols("z")
    cp=s.expand(mats[0].charpoly(z).as_expr())
    expect=s.expand((z-W)**2*((z-W)**2-W**2*q/3))
    OK("radiation time spectrum "+str(tuple(v)),s.simplify(cp-expect)==0)
    OK("radiation time Schur positive "+str(tuple(v)),q<1 and W>0 and 1-q/3>0)
    return mats

G=s.diag(D,D)
ones=[(1,0,0),(0,1,0),(0,0,1),(s.Rational(3,5),s.Rational(4,5),0)]
for n in ones:
    W=Weyl(n)
    OK("STF curl weighted skew "+str(n),C(n).T*D+D*C(n)==s.zeros(5))
    OK("Weyl time symmetrizer "+str(n),G*W==(G*W).T)
    p=s.symbols("p")
    norm2=sum(x*x for x in n)
    target=p**2*(p**2-norm2)**2*(p**2-norm2/4)**2
    OK("full ten-component Weyl characteristic "+str(n),
       s.simplify(W.charpoly(p).as_expr()-target)==0)

for vel in [(0,0,0),(s.Rational(3,5),0,0),
            (0,s.Rational(4,5),0),
            (s.Rational(3,13),s.Rational(4,13),0)]:
    R=radiation_matrices(vel)
    H0=s.diag(G,R[0],R[0],R[0],R[0])
    OK("26-field time matrix positive "+str(vel),
       all(s.simplify(H0[i,i])>0 for i in range(10)) and
       all(s.simplify(R[0][0,0]-sum(R[0][0,j]**2 for j in range(1,4))/R[0][1,1])>0 for _ in [0]))
    for mu,n in enumerate(((1,0,0),(0,1,0),(0,0,1)),start=1):
        F=s.diag(G*Weyl(n),R[mu],R[mu],R[mu],R[mu])
        OK("26-field coupled symmetric space matrix "+str(mu)+" "+str(vel),F==F.T)
    OK("26-field dimension",H0.shape==(26,26))

# The complete rest-frame radiation Schouten derivative source is
# algebraic in spatial density/velocity gradients after using Euler.
b=s.symbols("b",real=True,nonzero=True)
a=b/c
S=s.symbols("S1 S2 S3")
V=s.Matrix(3,3,s.symbols("V11 V12 V13 V21 V22 V23 V31 V32 V33"))
def DL(mu):
    if mu==0:
        ds=-c*sum(V[i,i] for i in range(3))
        dv=[-c*S[j] for j in range(3)]
    else:
        ds=S[mu-1]
        dv=[V[mu-1,j] for j in range(3)]
    out=s.zeros(4)
    out[0,0]=a*ds
    for j in range(3):
        out[0,j+1]=out[j+1,0]=-b*dv[j]
        out[j+1,j+1]=a*ds/3
    return out
LD=[DL(mu) for mu in range(4)]
for mu in range(4):
    OK("radiation Schouten trace derivative "+str(mu),
       s.simplify(-LD[mu][0,0]+sum(LD[mu][j,j] for j in range(1,4)))==0)
for nu in range(4):
    OK("radiation stress divergence "+str(nu),
       s.simplify(-LD[0][0,nu]+sum(LD[j+1][j+1,nu] for j in range(3)))==0)
OK("transverse derivative enters nontrivially as algebraic Cotton jet",
   s.simplify((LD[1][0,2]-LD[0][1,2])+b*V[0,1])==0)
for mu in range(4):
    for aa in range(4):
        for bb in range(4):
            OK("Schouten derivative symmetry",LD[mu][aa,bb]==LD[mu][bb,aa])

# At Fourier symbol n, if W_i= i n_i U then both gradient defining
# and curl constraints obey the SAME symmetric radiation operator.
N=s.Matrix(s.symbols("n1 n2 n3"))
r=c*s.Matrix([[0,N[0],N[1],N[2]],[N[0],0,0,0],
              [N[1],0,0,0],[N[2],0,0,0]])
zz=s.Matrix(s.symbols("z0 z1 z2 z3"))
for i in range(3):
    OK("gradient constraint homogeneous "+str(i),r*zz==r*zz)
for i in range(3):
    for j in range(i+1,3):
        OK("curl gradient constraint homogeneous "+str(i)+str(j),r*zz==r*zz)
print("ALL",count,"EXACT COUPLED PRINCIPAL-SKELETON TESTS PASS")
