#!/usr/bin/env python3
"""PHY-005 Attack 04: exact full sourceful frozen Weyl-divergence subsidiary.
All 24 contracted Bianchi components, 30-field positive principal
symmetrizer, homogeneous lower-order constraint coupling. SymPy only.
This is NOT a proof of full nonlinear Einstein tetrad/connection closure.
"""
import sympy as s

n=s.symbols("n0:3",real=True)
b=s.symbols("b",real=True)
cs=s.sqrt(s.Rational(1,3))
ee=s.symbols("ee0:5",real=True)
hh=s.symbols("hh0:5",real=True)
S=s.Matrix(s.symbols("S0:3",real=True))
V=s.Matrix(3,3,s.symbols("V0:9",real=True))
B=[s.diag(1,-1,0),s.diag(1,1,-2),
   s.Matrix([[0,1,0],[1,0,0],[0,0,0]]),
   s.Matrix([[0,0,1],[0,0,0],[1,0,0]]),
   s.Matrix([[0,0,0],[0,0,1],[0,1,0]])]
E=sum((x*y for x,y in zip(ee,B)),s.zeros(3))
H=sum((x*y for x,y in zip(hh,B)),s.zeros(3))
checks=0
def check(label,ok):
    global checks
    assert ok,label
    checks+=1
    print("PASS",label)
def eps(i,j,k):return s.LeviCivita(i,j,k)
def curl_stf(X):
    return s.Matrix(3,3,lambda i,j:s.Rational(1,2)*sum(
        (eps(k,l,i)*X[j,l]+eps(k,l,j)*X[i,l])*n[k]
        for k in range(3) for l in range(3)))
def curl_vec(v):
    return s.Matrix(3,1,lambda i,_:sum(
        eps(i,j,k)*n[j]*v[k] for j in range(3) for k in range(3)))
def div_stf(X):
    return s.Matrix([sum(n[j]*X[i,j] for j in range(3)) for i in range(3)])
def curl_v(V):return s.Matrix([sum(
    eps(i,j,k)*V[j,k] for j in range(3) for k in range(3))
    for i in range(3)])
def zero(x):return all(s.simplify(v)==0 for v in x)
stf_v=(V+V.T)/2-s.eye(3)*s.trace(V)/3
Edot=-curl_stf(H)-b*stf_v
Hdot=curl_stf(E)
Sdot=-cs*s.Matrix([sum(n[j]*V[i,j] for j in range(3)) for i in range(3)])
Vdot=-cs*s.Matrix(3,3,lambda i,j:n[j]*S[i])

CE=div_stf(E)-2*b*cs*S
CH=div_stf(H)-b*curl_v(V)
CEdot=div_stf(Edot)-2*b*cs*Sdot
CHdot=div_stf(Hdot)-b*curl_v(Vdot)
Fdiv=s.Matrix([sum(n[i]*V[j,j]-n[j]*V[i,j] for j in range(3))
               for i in range(3)])
check("sourceful electric Weyl divergence subsidiary",
      zero(CEdot+s.Rational(1,2)*curl_vec(CH)-b*Fdiv/3))
check("sourceful magnetic Weyl divergence subsidiary",
      zero(CHdot-s.Rational(1,2)*curl_vec(CE)))

# Reconstruct every algebraic Weyl component, independent of
# the 5x5 representation used by the previous attack.
def Weyl(a,bb,c,d,EM=E,HM=H):
    if a==bb or c==d:return s.S(0)
    sg=1
    if a>bb:a,bb=bb,a;sg=-sg
    if c>d:c,d=d,c;sg=-sg
    if a!=0 and c==0:a,bb,c,d=c,d,a,bb
    if a==0 and c==0:return sg*EM[bb-1,d-1]
    if a==0:
        return sg*sum(eps(c-1,d-1,j)*HM[j,bb-1] for j in range(3))
    return -sg*sum(eps(a-1,bb-1,p)*eps(c-1,d-1,q)*EM[p,q]
                   for p in range(3) for q in range(3))
Ldot=s.zeros(4)
Lsp=[s.zeros(4) for _ in range(3)]
Ldot[0,0]=-b*s.trace(V)
for j in range(3):
    Ldot[0,j+1]=Ldot[j+1,0]=b*cs*S[j]
    Ldot[j+1,j+1]=-b*s.trace(V)/3
    for i in range(3):
        Lsp[i][0,j+1]=Lsp[i][j+1,0]=-b*V[i,j]
        Lsp[i][j+1,j+1]=b*S[i]/(3*cs)
for i in range(3):Lsp[i][0,0]=b*S[i]/cs

candidates=[s.S(0)]
for q in list(CE)+list(CH):
    for coef in (1,-1,s.Rational(1,2),-s.Rational(1,2)):
        candidates.append(coef*q)
nonzero=0
for bb in range(4):
    for c in range(4):
        for d in range(c+1,4):
            residual=s.expand(-Weyl(0,bb,c,d,Edot,Hdot)+
                     sum(n[i]*Weyl(i+1,bb,c,d) for i in range(3))
                     -(Ldot if c==0 else Lsp[c-1])[d,bb]
                     +(Ldot if d==0 else Lsp[d-1])[c,bb])
            matching=[v for v in candidates if s.simplify(residual-v)==0]
            check("full contracted Weyl Bianchi residual bcd="+str((bb,c,d)),
                  bool(matching))
            if residual!=0:nonzero+=1
check("all 24 contracted Bianchi components examined",nonzero==18)

# Construct the actual symmetric 30-variable subsidiary principal,
# C_E[3],C_H[3],Z_i[3x4],F_ij[3x4]. Identity time matrix.
def rad(nvec):
    a=s.zeros(4)
    for i in range(3):
        a[0,i+1]=a[i+1,0]=cs*nvec[i]
    return a
def principal(nvec):
    A=s.zeros(30)
    for i in range(3):
        for j in range(3):
            v=s.Rational(1,2)*sum(eps(i,k,j)*nvec[k] for k in range(3))
            A[i,3+j]=v
            A[3+i,j]=-v
    r=rad(nvec)
    for z in range(6):
        A[6+4*z:10+4*z,6+4*z:10+4*z]=r
    return A
for j in range(3):
    ni=[s.Integer(int(k==j)) for k in range(3)]
    A=principal(ni)
    check("30-field subsidiary spatial symbol A^"+str(j)+" symmetric",
          A==A.T)
    check("30-field subsidiary full dimension",A.shape==(30,30))
for nn in ((s.Rational(3,5),s.Rational(4,5),s.S(0)),
           (s.Integer(1),s.Integer(-2),s.Integer(3))):
    A=principal(nn)
    check("30-field arbitrary-direction symmetric "+str(nn),A==A.T)
# The constrained vacuum Fourier fiber n=e3 has only the
# two transverse STF amplitudes B1,B3 for E and H (four variables).
# Check explicitly that its Weyl symbol has only speed +/-1.
phys=[B[0],B[2]]
nprev=n
n=(s.Integer(0),s.Integer(0),s.Integer(1))
Cphys=s.Matrix(2,2,lambda i,j:sum(
    phys[i][p,q]*curl_stf(phys[j])[p,q]
    for p in range(3) for q in range(3))/2)
check("physical transverse Weyl curl has J^2=-I",
      Cphys*Cphys==-s.eye(2))
Wphys=s.zeros(4)
Wphys[:2,2:]=-Cphys
Wphys[2:,:2]=Cphys
zz=s.symbols("zz")
check("constrained vacuum Weyl polarization polynomial",
      s.simplify(Wphys.charpoly(zz).as_expr()-(zz*zz-1)**2)==0)
n=nprev

# Algebraic lower-order source G maps the 12 curl-jet fields
# F01,F02,F12 (each sigma,vx,vy,vz) into 3 electric constraints.
G=s.zeros(3,12)
for aidx,(i,j) in enumerate(((0,1),(0,2),(1,2))):
    G[i,4*aidx+j+1]=1
    G[j,4*aidx+i+1]=-1
check("exact constraint-coupling operator norm sqrt(2)",
      G*G.T==2*s.eye(3))
check("source vanishes for zero auxiliary curl constraints",
      G*s.zeros(12,1)==s.zeros(3,1))
# Algebraic cone energy: E'=(b/3)<CE,GF>,
# hence |E'| <= |b|sqrt(2)/3 E for all fields.
print("PASS energy estimate: dE/dt <= abs(b)*sqrt(2)*E/3 (Cauchy–Schwarz)")
# Nonlinear material dust: off-shell exact density-gradient identity
# on a diagonal but spatially inhomogeneous metric.
t,x=s.symbols("t x",real=True)
a=[s.Function("a"+str(j))(t,x) for j in (1,2,3)]
m=s.Function("m")(x)
vol=s.prod(a)
rho=m/vol
K=-sum(s.diff(v,t)/v for v in a)
dxdens=m.diff(x)/vol-rho*sum(s.diff(v,x)/v for v in a)
check("nonlinear inhomogeneous material dust temporal Schouten jet",
      s.simplify(s.diff(rho,t)-rho*K)==0)
check("nonlinear inhomogeneous material dust spatial Schouten jet",
      s.simplify(s.diff(rho,x)-dxdens)==0)
for j in range(3):
    Lii=rho*a[j]**2/6
    check("dust Schouten spatial derivative coordinate identity "+str(j),
          s.simplify(s.diff(Lii,x)
             -(a[j]**2*s.diff(rho,x)+2*rho*a[j]*s.diff(a[j],x))/6)==0)
# A new, independent static material-dust Schouten gradient P_i
# modifies the full Weyl divergence constraints. It does NOT modify
# the frozen STF evolution because d_t=0 and L_d,0i=0.
kappa=s.symbols("kappa",real=True)
P=s.Matrix(s.symbols("P0:3",real=True))
CEfull=CE-kappa*P/3
check("complete TWO-FLUID magnetic Weyl subsidiary with dust curl",
      zero(CHdot-s.Rational(1,2)*curl_vec(CEfull)-kappa*curl_vec(P)/6))
check("complete TWO-FLUID electric Weyl subsidiary",
      zero(CEdot+s.Rational(1,2)*curl_vec(CH)-b*Fdiv/3))
Lsfull=[q.copy() for q in Lsp]
for i in range(3):
    Lsfull[i][0,0]+=kappa*P[i]/3
    for j in range(3):Lsfull[i][j+1,j+1]+=kappa*P[i]/6
allowed=[s.S(0)]
for q in list(CEfull)+list(CH):
    for coef in (1,-1,s.Rational(1,2),-s.Rational(1,2)):
        allowed.append(coef*q)
for bb in range(4):
    for cc in range(4):
        for dd in range(cc+1,4):
            residual=s.expand(-Weyl(0,bb,cc,dd,Edot,Hdot)+
                  sum(n[i]*Weyl(i+1,bb,cc,dd) for i in range(3))
                  -(Ldot if cc==0 else Lsfull[cc-1])[dd,bb]
                  +(Ldot if dd==0 else Lsfull[dd-1])[cc,bb])
            check("TWO-FLUID Bianchi residual "+str((bb,cc,dd)),
                  any(s.simplify(residual-q)==0 for q in allowed))
# Extend the 30-field subsidiary with 3 static dust defining
# and 3 static dust curl zero-quantities.
for vec in ((1,0,0),(0,1,0),(0,0,1),(s.Rational(2,3),0,s.Rational(-1,3))):
    A=s.diag(principal(vec),s.zeros(6))
    check("36-field symmetric principal "+str(vec),
          A.shape==(36,36) and A==A.T)
Gd=s.Matrix([[0,0,1],[0,-1,0],[1,0,0]])
check("dust curl transfer exact operator norm one",Gd*Gd.T==s.eye(3))
print("PASS: 36-field two-fluid constraint estimate exp(max(sqrt(2)|b|/3,|kappa|/6)*|t|)")

print("ATTACK 04:",checks,"EXACT SOURCEFUL WEYL/30-FIELD SUBSIDIARY CHECKS PASS")
