from mpmath import mp, mpf, log, findroot
from fractions import Fraction as F
mp.dps=50
H=lambda x: -x*log(x)-(1-x)*log(1-x)
c=mpf(502)/25
def Gam(t): return (c*H(1/c)-c*H((1-t)/c)-t*log(9))/log(4)
def q(t): return (H(t)+t*log(9))/log(4)
B=(c-1)*log(3)/log(4)
t=findroot(lambda t: Gam(t)+q(t)-mpf(1)/2, 0.113)
print("theta*",t)
# rational theta: continued fraction approx with denom ~1e6-1e7
th=F(str(t)).limit_denominator(3_000_000); tm=mpf(th.numerator)/th.denominator
print("theta",th, float(tm-t))
G=Gam(tm); Q=q(tm); print("G",G,"Q",Q,"G+Q-1/2",G+Q-mpf(1)/2, "B",B)
# certified rounding: G down, Q up, B up at 13 decimals
import math
def dn(x,k=13): return mp.floor(x*10**k)/10**k
def up(x,k=12): return mp.ceil(x*10**k)/10**k
Gl=dn(G); Qh=dn(Q)+mpf(10)**-13; Bh=up(B)
print("Gl",Gl,"Qh",Qh,"Bh",Bh)
eps=mpf(10)**-13
def exps(s):
    return (3-2*Gl*s+eps*(1-Gl), 2+s*(2*Bh-mpf(1)/2)+eps*(Bh+mpf(1)/2), 3-s*(1-2*Qh)+Qh*eps, 3-s)
s0=findroot(lambda s: exps(s)[0]-exps(s)[1], 0.0335)
print("sigma*",s0, exps(s0))
sg=F(str(s0)).limit_denominator(5_000_000); sm=mpf(sg.numerator)/sg.denominator
print("sigma",sg, [mp.nstr(e,16) for e in exps(sm)])
