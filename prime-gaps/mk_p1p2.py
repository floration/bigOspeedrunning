# Maynard M_k lower bounds with symmetric weights F = sum c_{a,b} (1-P1)^a P2^b on the simplex.
import sys
from fractions import Fraction as Fr
from math import factorial as fa, comb
from functools import lru_cache
import mpmath as mp
mp.mp.dps=250
def partitions(n,maxp=None):
    if maxp is None: maxp=n
    if n==0: yield (); return
    for p in range(min(n,maxp),0,-1):
        for r in partitions(n-p,p): yield (p,)+r
@lru_cache(None)
def Phi(k,A,B):  # int over {t>=0, sum t<=1} in R^k of (1-P1)^A P2^B
    tot=Fr(0)
    for lam in partitions(B):
        l=len(lam)
        if l>k: continue
        mult={}
        for x in lam: mult[x]=mult.get(x,0)+1
        arr=fa(k)//fa(k-l)
        for m in mult.values(): arr//=fa(m)
        coef=Fr(fa(B))
        for x in lam: coef/=fa(x)
        num=fa(A)
        for x in lam: num*=fa(2*x)
        tot+=coef*arr*Fr(num, fa(k+A+2*B))
    return tot
def mult_poly(p,q):  # polys as dict {(A,B):coef} in (1-P1), P2
    r={}
    for (a1,b1),c1 in p.items():
        for (a2,b2),c2 in q.items():
            key=(a1+a2,b1+b2); r[key]=r.get(key,0)+c1*c2
    return r
def integ(k,p): return sum(c*Phi(k,A,B) for (A,B),c in p.items())
def inner(a,b):  # int_0^{1-s} F dt_k as poly in (1-P1'),P2' (k-1 dims)
    return {(a+2*j+1,b-j): Fr(comb(b,j)*fa(a)*fa(2*j),fa(a+2*j+1)) for j in range(b+1)}
def Mk(k,basis):
    n=len(basis)
    I=[[integ(k,{(basis[i][0]+basis[j][0],basis[i][1]+basis[j][1]):1}) for j in range(n)] for i in range(n)]
    G=[inner(*bb) for bb in basis]
    J=[[integ(k-1,mult_poly(G[i],G[j])) for j in range(n)] for i in range(n)]
    Im=mp.matrix([[mp.mpf(x.numerator)/x.denominator for x in r] for r in I])
    Jm=mp.matrix([[mp.mpf(x.numerator)/x.denominator for x in r] for r in J])
    L=mp.cholesky(Im); Li=mp.inverse(L)
    S=Li*Jm*Li.T
    ev=mp.eigsy(S)[0]
    return k*max(ev)
if __name__=="__main__":
    k=int(sys.argv[1]); D=int(sys.argv[2])  # total degree a+2b<=D
    bmax=int(sys.argv[3]) if len(sys.argv)>3 else 99
    basis=[(a,b) for b in range(0,D//2+1) if b<=bmax for a in range(0,D-2*b+1)]
    print(k,D,bmax,len(basis),mp.nstr(Mk(k,basis),12))
