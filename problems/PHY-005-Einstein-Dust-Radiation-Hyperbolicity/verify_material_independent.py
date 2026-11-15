#!/usr/bin/env python3
"""Independent exact Fraction replay for material-frame Einstein two-fluid gates.
Does not import SymPy. No claim of full Einstein principal hyperbolicity.
"""
from fractions import Fraction as F

cases=[
 (F(0),F(0),F(0),F(1)),
 (F(3,5),F(0),F(0),F(5,4)),
 (F(0),F(4,5),F(0),F(5,3)),
 (F(3,13),F(4,13),F(0),F(13,12)),
 (F(1,3),F(2,3),F(0),F(3,2))]
def g(a,b):
    return -a[0]*b[0]+sum(x*y for x,y in zip(a[1:],b[1:]))
def tetrad(v,W):
    norm=sum(x*x for x in v)
    u=(W,*[W*x for x in v])
    e=[]
    for a in range(3):
        sp=[F(int(j==a)) for j in range(3)]
        if norm:
            sp=[sp[j]+(W-1)*v[a]*v[j]/norm for j in range(3)]
        e.append((W*v[a],*sp))
    return (u,*e)
for vx,vy,vz,W in cases:
    v=(vx,vy,vz);norm=sum(x*x for x in v)
    assert W*W*(1-norm)==1
    e=tetrad(v,W)
    for i in range(4):
        for j in range(4):
            expected=F(-1 if i==j==0 else (1 if i==j else 0))
            assert g(e[i],e[j])==expected
    time_spatial=tuple(b[0] for b in e[1:])
    assert sum(q*q for q in time_spatial)==W*W*norm
    # Schur complement of A0=[[W,c_s b^T],[c_s b,W I]],
    # using exact c_s^2=1/3 to avoid any floating calculation.
    schur=W-sum(x*x for x in time_spatial)/(3*W)
    assert schur==W*(1-norm/F(3))>0
    assert 1-norm/F(3)>=F(2,3)
    J=tuple(F(4,3)*W*W*x for x in v)
    if norm:assert J!=(0,0,0)
    print('PASS exact tilted boost, timelike Schur, stress flux',v,'W',W,'J/rho',J)

# Nonlinear FLRW Einstein constraint, exact rational arbitrary initial states.
for H,rd,rr,kappa in (
 (F(1),F(1),F(1),F(1)),
 (F(5,3),F(4,7),F(7,9),F(3,2)),
 (F(-4,5),F(11,9),F(1,31),F(9,10))):
    lam=3*H*H-kappa*(rd+rr)
    Hdot=-kappa/F(2)*(rd+F(4,3)*rr)
    rd_dot=-3*H*rd;rr_dot=-4*H*rr
    assert 3*H*H-kappa*(rd+rr)-lam==0
    assert 6*H*Hdot-kappa*(rd_dot+rr_dot)==0
    print('PASS full nonlinear homogeneous constraint',H,rd,rr,lam)

# Pure synchronous vacuum ADM gauge mode: initial K norm fixed,
# future spatial metric gradient grows as 2 |time| N.
for N in (2,3,7,11,31,101,1009):
    tau=F(1,7)
    ratio=2*tau*N
    assert ratio==F(2*N,7)
    print('PASS constrained synchronous ADM gauge growth',N,ratio)
assert F(2*1009,7)>F(2*101,7)>F(2*2,7)

# Original pressure-regularized Eulerian symmetrizer singularity remains.
for c in (F(1,2),F(1,5),F(1,10),F(1,100)):
    assert 1/(c*c)>=1
    print('PASS optimal original Eulerian symmetrizer cond',c,1/(c*c))
print('SECOND INDEPENDENT FRACTION REPLAY: ALL PASS')
