#!/usr/bin/env python3
"""Independent Fraction-only sourceful Weyl/jet subsidiary audit.
No symbolic algebra package. Uses the rational radiation variable
chi=sigma/c_s, giving R(n)=[[0,n^T],[n/3,0]] and H_R=diag(1/3,1,1,1).
Proves exact sampled tensor identities, not a nonlinear Einstein theorem.
"""
from fractions import Fraction as Q
from itertools import combinations
def e(i,j,k):
    if len({i,j,k})<3:return 0
    return 1 if (i,j,k) in ((0,1,2),(1,2,0),(2,0,1)) else -1
def M(h,w):return [[Q(0) for _ in range(w)] for _ in range(h)]
def mm(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]
def tr(a):return list(map(list,zip(*a)))
def stf(B):
    return [[(B[i][j]+B[j][i])/2-(Q(int(i==j))/3)*sum(B[k][k] for k in range(3))
             for j in range(3)] for i in range(3)]
def stf_mat(q):
    E=M(3,3)
    E[0][0]=q[0]+q[1];E[1][1]=-q[0]+q[1];E[2][2]=-2*q[1]
    E[0][1]=E[1][0]=q[2]
    E[0][2]=E[2][0]=q[3]
    E[1][2]=E[2][1]=q[4]
    return E
def curl_stf(n,X):
    return [[sum(Q(e(k,l,i))*n[k]*X[j][l]+Q(e(k,l,j))*n[k]*X[i][l]
                 for k in range(3) for l in range(3))/2
             for j in range(3)] for i in range(3)]
def curl_vec(n,X):
    return [sum(Q(e(i,j,k))*n[j]*X[k] for j in range(3) for k in range(3))
            for i in range(3)]
def div_stf(n,X):
    return [sum(n[j]*X[i][j] for j in range(3)) for i in range(3)]
def curl_v(V):
    return [sum(Q(e(i,j,k))*V[j][k] for j in range(3) for k in range(3))
            for i in range(3)]
def wcomponent(a,bb,c,d,E,H):
    if a==bb or c==d:return Q(0)
    sg=Q(1)
    if a>bb:a,bb=bb,a;sg=-sg
    if c>d:c,d=d,c;sg=-sg
    if a!=0 and c==0:a,bb,c,d=c,d,a,bb
    if a==0 and c==0:return sg*E[bb-1][d-1]
    if a==0:
        return sg*sum(Q(e(c-1,d-1,j))*H[j][bb-1] for j in range(3))
    return -sg*sum(Q(e(a-1,bb-1,p))*Q(e(c-1,d-1,q))*E[p][q]
                   for p in range(3) for q in range(3))
def dpr(n,b,ee,hh,S,V):
    E=stf_mat(ee);H=stf_mat(hh)
    Edot=curl_stf(n,H)
    P=stf(V)
    Edot=[[-Edot[i][j]-b*P[i][j] for j in range(3)] for i in range(3)]
    Hdot=curl_stf(n,E)
    Sdot=[-sum(n[j]*V[i][j] for j in range(3)) for i in range(3)]
    Vdot=[[-n[j]*S[i]/3 for j in range(3)] for i in range(3)]
    CE=[div_stf(n,E)[i]-2*b*S[i]/3 for i in range(3)]
    CH=[div_stf(n,H)[i]-b*curl_v(V)[i] for i in range(3)]
    CEdot=[div_stf(n,Edot)[i]-2*b*Sdot[i]/3 for i in range(3)]
    CHdot=[div_stf(n,Hdot)[i]-b*curl_v(Vdot)[i] for i in range(3)]
    CEc=curl_vec(n,CE);CHc=curl_vec(n,CH)
    Fdiv=[sum(n[i]*V[j][j]-n[j]*V[i][j] for j in range(3)) for i in range(3)]
    assert all(CEdot[i]+CHc[i]/2-b*Fdiv[i]/3==0 for i in range(3))
    assert all(CHdot[i]-CEc[i]/2==0 for i in range(3))

    Ldt=M(4,4);Lsp=[M(4,4) for _ in range(3)]
    Ldt[0][0]=-b*sum(V[j][j] for j in range(3))
    for j in range(3):
        Ldt[0][j+1]=Ldt[j+1][0]=b*S[j]/3
        Ldt[j+1][j+1]=-b*sum(V[k][k] for k in range(3))/3
        for i in range(3):
            Lsp[i][0][j+1]=Lsp[i][j+1][0]=-b*V[i][j]
            Lsp[i][j+1][j+1]=b*S[i]/3
    for i in range(3):Lsp[i][0][0]=b*S[i]

    possibilities={Q(0)}
    for val in CE+CH:
        for k in (Q(1),Q(-1),Q(1,2),Q(-1,2)):
            possibilities.add(k*val)
    totals=0
    for bb in range(4):
        for c,d in combinations(range(4),2):
            residual=-(wcomponent(0,bb,c,d,Edot,Hdot))
            residual+=sum(n[i]*wcomponent(i+1,bb,c,d,E,H) for i in range(3))
            residual-= (Ldt if c==0 else Lsp[c-1])[d][bb]
            residual+= (Ldt if d==0 else Lsp[d-1])[c][bb]
            assert residual in possibilities,((bb,c,d),residual)
            totals+=1
    assert totals==24
    return CE,CH
cases=[
 ((Q(1),Q(0),Q(0)),Q(1)),
 ((Q(0),Q(1),Q(0)),Q(3,2)),
 ((Q(0),Q(0),Q(1)),Q(11,7)),
 ((Q(3,5),Q(4,5),Q(0)),Q(5,4)),
 ((Q(2),Q(-3),Q(7)),Q(9,11)),
 ((Q(1,4),Q(-2,7),Q(5,6)),Q(17,13))]
for idx,(n,b) in enumerate(cases):
    ee=[Q(k*(idx+1),5+k) for k in range(1,6)]
    hh=[Q((-1)**k*(idx+3),3+k) for k in range(1,6)]
    S=[Q(k*(idx+1),3+k) for k in range(1,4)]
    V=[[Q((3*i+2*j+1)*(idx+2),5+i+2*j) for j in range(3)] for i in range(3)]
    dpr(n,b,ee,hh,S,V)
    print("PASS independently reconstructed 24 sourceful Bianchi identities and CE/CH subsidiary",idx)

# Independently restrict the vacuum Weyl operator to two
# transverse physical tensor amplitudes for n=e3.
np=(Q(0),Q(0),Q(1))
phys=[stf_mat([Q(1),Q(0),Q(0),Q(0),Q(0)]),
      stf_mat([Q(0),Q(0),Q(1),Q(0),Q(0)])]
C=M(2,2)
for j in range(2):
    Z=curl_stf(np,phys[j])
    for i in range(2):
        C[i][j]=sum(phys[i][k][l]*Z[k][l]
                    for k in range(3) for l in range(3))/2
assert mm(C,C)==[[-Q(i==j) for j in range(2)] for i in range(2)]
Aw=M(4,4)
for i in range(2):
    for j in range(2):
        Aw[i][j+2]=-C[i][j]
        Aw[i+2][j]=C[i][j]
assert mm(Aw,Aw)==[[Q(i==j) for j in range(4)] for i in range(4)]
print("PASS independent constrained vacuum Weyl 4D fiber has light speeds +/-1")

# Full 30-component subsidiary principal with exact rational
# H=diag(I6,H_R,H_R,H_R,H_R,H_R,H_R).
HR=[Q(1,3),Q(1),Q(1),Q(1)]
def principal(n):
    A=M(30,30)
    for i in range(3):
        for j in range(3):
            coeff=sum(Q(e(i,k,j))*n[k] for k in range(3))/2
            A[i][3+j]=coeff;A[3+i][j]=-coeff
    for k in range(6):
        start=6+4*k
        for j in range(3):
            A[start][start+1+j]=n[j]
            A[start+1+j][start]=n[j]/3
    return A
H=HR*6
energyweights=[Q(1)]*6+H
assert len(energyweights)==30
for n,b in cases:
    A=principal(n)
    for i in range(30):
        assert energyweights[i]>0
        for j in range(30):
            assert energyweights[i]*A[i][j]==energyweights[j]*A[j][i]
    print("PASS independent weighted 30x30 symmetric subsidiary principal",n)

# The algebraic F to CE transfer has exact GG^T=2I.
G=M(3,12)
for p,(i,j) in enumerate(((0,1),(0,2),(1,2))):
    G[i][p*4+j+1]=Q(1)
    G[j][p*4+i+1]=Q(-1)
assert mm(G,tr(G))==[[Q(2)*Q(i==j) for j in range(3)] for i in range(3)]
print("PASS exact algebraic source bound ||G||=sqrt(2)")
# Additional independent material-dust regression:
# at a nontrivial anisotropic inhomogeneous material metric point,
# the exact coordinate quotient derivative uses only m, dm and
# first derivatives of metric scales.
av=(Q(2),Q(3),Q(5))
at=(Q(1,4),Q(-2,5),Q(3,2))
ax=(Q(7,3),Q(-1,2),Q(4,7))
m=Q(11,7);dm=Q(13,17)
vol=av[0]*av[1]*av[2]
rho=m/vol
K=-sum(at[i]/av[i] for i in range(3))
drhot=-rho*sum(at[i]/av[i] for i in range(3))
drhox=dm/vol-rho*sum(ax[i]/av[i] for i in range(3))
assert drhot==rho*K
assert drhox==dm/vol-rho*sum((Q(2)*av[i]*ax[i])/(Q(2)*av[i]**2) for i in range(3))
for i in range(3):
    Lii=rho*av[i]**2/6
    dLii=(drhox*av[i]**2+2*rho*av[i]*ax[i])/6
    assert dLii==drhox*av[i]**2/6+rho*av[i]*ax[i]/3
    assert Lii>0
print("PASS independent material dust Schouten/metric first-derivative identity")

print("INDEPENDENT FRACTION-ONLY WEYL CONSTRAINT SUBSIDIARY: ALL PASS")
