# M_k with F = sum c (1-P1)^a * prod_j P_{lam_j} (power sums, parts>=2), exact integrals.
import sys, itertools
from fractions import Fraction as Fr
from math import factorial as fa
from functools import lru_cache
import mpmath as mp
mp.mp.dps=300
def set_partitions(lst):
    if not lst: yield []; return
    first,rest=lst[0],lst[1:]
    for p in set_partitions(rest):
        for i in range(len(p)): yield p[:i]+[[first]+p[i]]+p[i+1:]
        yield [[first]]+p
@lru_cache(None)
def Phi(k,A,lam):  # lam sorted tuple
    tot=Fr(0)
    for sp in set_partitions(list(lam)):
        l=len(sp)
        if l>k: continue
        num=fa(A)
        for b in sp: num*=fa(sum(b))
        tot+=Fr(fa(k)//fa(k-l)*num, fa(k+A+sum(lam)))
    return tot
def mul(p,q):
    r={}
    for (a1,l1),c1 in p.items():
        for (a2,l2),c2 in q.items():
            key=(a1+a2,tuple(sorted(l1+l2))); r[key]=r.get(key,0)+c1*c2
    return r
def integ(k,p): return sum(c*Phi(k,A,l) for (A,l),c in p.items())
def inner(a,lam):
    r={}
    n=len(lam)
    for mask in range(1<<n):
        m=sum(lam[i] for i in range(n) if mask>>i&1)
        rest=tuple(sorted(lam[i] for i in range(n) if not mask>>i&1))
        key=(a+m+1,rest); r[key]=r.get(key,0)+Fr(fa(a)*fa(m),fa(a+m+1))
    return r
def parts_ge2(n,maxp=None):
    if maxp is None: maxp=n
    if n==0: yield (); return
    for p in range(min(n,maxp),1,-1):
        for r in parts_ge2(n-p,p): yield (p,)+r
def Mk(k,basis):
    n=len(basis)
    G=[inner(a,l) for a,l in basis]
    I=[[Phi(k,basis[i][0]+basis[j][0],tuple(sorted(basis[i][1]+basis[j][1]))) for j in range(n)] for i in range(n)]
    J=[[integ(k-1,mul(G[i],G[j])) for j in range(n)] for i in range(n)]
    cv=lambda x: mp.mpf(x.numerator)/x.denominator
    Im=mp.matrix([[cv(x) for x in r] for r in I]); Jm=mp.matrix([[cv(x) for x in r] for r in J])
    L=mp.cholesky(Im); Li=mp.inverse(L)
    return k*max(mp.eigsy(Li*Jm*Li.T)[0])
if __name__=="__main__":
    k=int(sys.argv[1]); amax=int(sys.argv[2]); sdeg=int(sys.argv[3])
    sigs=[s for d in range(0,sdeg+1) for s in parts_ge2(d)]
    basis=[(a,s) for s in sigs for a in range(amax+1)]
    print(f"k={k} radial_deg<={amax} sig_deg<={sdeg} nsig={len(sigs)} n={len(basis)} M={mp.nstr(Mk(k,basis),12)}",flush=True)
