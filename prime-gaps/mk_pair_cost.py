# Like mk2, plus the double-erasure (pair) form D = int_{R_{k-2}} (int int F dt_a dt_b)^2 at the optimal F.
import sys
from mk_signatures import *
def inner_poly(p):
    r={}
    for (a,l),c in p.items():
        for key,v in inner(a,l).items(): r[key]=r.get(key,0)+c*v
    return r
k=int(sys.argv[1]); amax=int(sys.argv[2]); sdeg=int(sys.argv[3])
sigs=[s for d in range(0,sdeg+1) for s in parts_ge2(d)]
basis=[(a,s) for s in sigs for a in range(amax+1)]
n=len(basis)
G=[inner(a,l) for a,l in basis]; G2=[inner_poly(g) for g in G]
I=[[Phi(k,basis[i][0]+basis[j][0],tuple(sorted(basis[i][1]+basis[j][1]))) for j in range(n)] for i in range(n)]
J=[[integ(k-1,mul(G[i],G[j])) for j in range(n)] for i in range(n)]
Dm=[[integ(k-2,mul(G2[i],G2[j])) for j in range(n)] for i in range(n)]
cv=lambda x: mp.mpf(x.numerator)/x.denominator
Im=mp.matrix([[cv(x) for x in r] for r in I]); Jm=mp.matrix([[cv(x) for x in r] for r in J]); Dmm=mp.matrix([[cv(x) for x in r] for r in Dm])
L=mp.cholesky(Im); Li=mp.inverse(L)
E,Q=mp.eigsy(Li*Jm*Li.T)
idx=max(range(n),key=lambda i:E[i]); y=Q[:,idx]; c=Li.T*y
Ival=(c.T*Im*c)[0]; Jval=(c.T*Jm*c)[0]; Dval=(c.T*Dmm*c)[0]
print(f"k={k} sig<={sdeg} M={mp.nstr(k*Jval/Ival,10)} J/I={mp.nstr(Jval/Ival,10)} D/I={mp.nstr(Dval/Ival,10)} D/J={mp.nstr(Dval/Jval,10)}",flush=True)
