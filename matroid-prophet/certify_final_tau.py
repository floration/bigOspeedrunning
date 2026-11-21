#!/usr/bin/env python3
"""Exact-rational certificate, one-sample matroid prophet (Chen bound-111 chain), final push
+ decoupled max-branch probability tau (algorithm change: branch indicator uses its own
30 shared fair bits; Chen (30) with tau in place of t: (1-tau)beta t s/K W + [tau/4 - (1-tau)t(gamma kappa+a0)/K] m*).

Same chain as q's certify.py (T1-T5: 1/p kept, exact logs in log M*, alpha1 used directly,
d at a proven lower bound of lambda, fine phase grid theta = 1 + c/L), with L = 2^24 phases
instead of 2^16. B = theta^L is replaced by a proven rational lower bound (C increases in B).
Stdlib only.  Usage: python3 certify_final.py [--fraction]
"""
import sys
from fractions import Fraction as Q

def atanh2(y, n=60):
    s = sum((2*y**(2*j+1)/(2*j+1) for j in range(n)), Q(0))
    return s, s + 2*y**(2*n+1)/((2*n+1)*(1-y*y))
LN2 = atanh2(Q(1,3))
def ln_bounds(x):                      # rigorous (lo, hi) for ln x, x > 0 rational
    if x < 1:
        lo, hi = ln_bounds(1/x); return -hi, -lo
    k = 0
    while x / 2**k >= 2: k += 1
    y = x / 2**k; lo, hi = atanh2((y-1)/(y+1))
    return lo + k*LN2[0], hi + k*LN2[1]
def exp_neg_hi(y, N=80):               # upper bound on e^-y, y >= 0 (e^y >= partial sum)
    term = tot = Q(1)
    for k in range(1, N):
        term = term*y/k; tot += term
    return 1/tot
def rdown(x, dg=40): D = 10**dg; return Q((x.numerator*D)//x.denominator, D)
def rup(x, dg=40):   D = 10**dg; return Q(-((-x.numerator*D)//x.denominator), D)

LEADER = Q(51149356887949946750, 10**29)          # board rank 1, 20-digit display rounded up
Q_SHUFFLE_BEST = Q(516793722969405164601, 10**30)  # q's shuffler best (L = 2^16), display

# ---- parameters -----------------------------------------------------------------
kappa = Q(164)
rho, h, t = Q(6101750, 2**24), Q(12661469, 2**24), Q(1491, 2**24)
Lph = 2**24
c = Q(4933397, 10**6)                  # L(theta - 1)
theta = 1 + c/Lph
tau = Q(32399, 2**30)                # max-branch probability (dyadic)
mu, nu, v = Q(131168066, 10**7), Q(140836288, 10**7), Q(16005537, 10**10)

conds = []
def chk(name, ok): conds.append((name, bool(ok)))
p = rho + (1-rho)*t
lam_lo, lam_hi = ln_bounds(1/p)
d = rdown(lam_lo)
# B lower bound: ln B >= L * ln_lo(theta); pick B_lo with ln_hi(B_lo) <= that.
lnB = Lph * ln_bounds(theta)[0]
lo, hi = Q(100), Q(200)
for _ in range(80):
    mid = rdown((lo+hi)/2, 30)
    if ln_bounds(mid)[1] <= lnB: lo = mid
    else: hi = mid
B = lo
chk("ln_hi(B_lo) <= L ln_lo(theta)  =>  B_lo <= theta^L", ln_bounds(B)[1] <= lnB and B > 1)
al0 = rup(rho*exp_neg_hi((mu - Q(1,4))*d))        # >= rho p^(mu-1/4)
al1 = rup(rho*exp_neg_hi(mu*d)/v)                 # >= rho p^mu / v
om  = rup((1-p)*exp_neg_hi(nu*d)/v)               # >= (1-p) p^nu / v
a, b = al0 + 3*al1, om                            # tilts (3) hold by construction
X = (2*al1*(1/p - 1) + b)/(1 + a)
def log1p_hi(x): return x - x*x/2 + x**3/3       # ln(1+x) <= this for x >= 0
bY = rup(log1p_hi(X) + 2*log1p_hi(v))
la = rup(log1p_hi(a))
K = kappa + nu
g = rho/4 - bY/d
a0 = 1/d
eps = mu*rho/kappa + la/d
s = (1-h)*(g - (eps + K*t + (K*t + K*rho/kappa)/(B-1))/h)
C = (1-tau)*((B-1)/B)**2 * t * s / (c*K)

chk("0 < d <= lam_lo < lambda", 0 < d <= lam_lo < lam_hi)
chk("tilt 1: a >= rho(p^(mu-1/4) + 3p^mu/v)", a >= al0 + 3*al1)
chk("tilt 2: b >= (1-p)p^nu/v", b >= om)
chk("0 < gamma <= rho/4", 0 < g <= rho/4)
chk("s(B) > 0", s > 0)
chk("max branch: tau/4 >= (1-tau) t (gamma kappa + a0)/K", tau/4 >= (1-tau)*t*(g*kappa + a0)/K)
chk("0 < tau < 1, tau dyadic", 0 < tau < 1 and tau.denominator & (tau.denominator-1) == 0)
chk("domains: kappa>=4 int; 0<rho,h,t,v<1; mu>1/4; nu>0; theta>1",
    kappa >= 4 and kappa.denominator == 1 and all(0 < z < 1 for z in (rho,h,t,v)) and mu > Q(1,4) and nu > 0 and theta > 1)
chk("rho, h, t dyadic; L a power of 2", all((z.denominator & (z.denominator-1)) == 0 for z in (rho,h,t)) and Lph & (Lph-1) == 0)
chk("C > board rank 1", C > LEADER)
chk("C > q's shuffler best (L = 2^16)", C > Q_SHUFFLE_BEST)

ok = True
for n_, o in conds:
    print("[%s] %s" % ("PASS" if o else "FAIL", n_)); ok &= o
print("kappa=%s rho=%s h=%s t=%s L=2^24 L(theta-1)=%s" % (kappa, rho, h, t, c))
print("mu=%s nu=%s v=%s" % (mu, nu, v))
print("B >= %.15f" % float(B))
print("C = %.18e" % float(C))
print("C / board rank 1 = %.12f ; C / q shuffler best = %.12f" % (float(C/LEADER), float(C/Q_SHUFFLE_BEST)))
if "--fraction" in sys.argv: print(C.numerator); print(C.denominator)
print("RESULT:", "PASS" if ok else "FAIL")
