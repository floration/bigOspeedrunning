#!/usr/bin/env python3
"""Exact-rational certificate: Chen bound-111 scalar chain, with
  (i) q's fine phase grid (L = 2^16 phases, theta = 1 + Ld/L, so L(theta-1) = Ld < 5),
  (ii) re-tuned mask rates rho, h, t (dyadic) and kappa = 164,
  (iii) the tilt (3) checked directly with q0 > p^(-1/4) instead of 4/3,
  (iv) exact logs in log M* (Chen §6) instead of log(1+x) <= x and 1/p <= 1/rho,
  (v) re-tuned analysis constants mu, nu, v, a, b, d.
Stdlib only.  Usage: python3 certify_combined.py [--fraction]
"""
import sys
from fractions import Fraction as Q

def atanh2(y, n=40):
    s = sum((2*y**(2*j+1)/(2*j+1) for j in range(n)), Q(0))
    return s, s + 2*y**(2*n+1)/((2*n+1)*(1-y*y))
LN2 = atanh2(Q(1,3))
def ln_bounds(x):
    if x < 1:
        lo, hi = ln_bounds(1/x); return -hi, -lo
    k = 0
    while x / 2**k >= 2: k += 1
    y = x / 2**k; lo, hi = atanh2((y-1)/(y+1))
    return lo + k*LN2[0], hi + k*LN2[1]
def rdown(x, dg=30): D = 10**dg; return Q((x.numerator*D)//x.denominator, D)
def rup(x, dg=30):   D = 10**dg; return Q(-((-x.numerator*D)//x.denominator), D)
def min_rat(pred, hi, dg=13):
    D = 10**dg; lo, hi = 0, int(hi*D)+1
    while hi - lo > 1:
        mid = (lo+hi)//2
        if pred(Q(mid, D)): hi = mid
        else: lo = mid
    return Q(hi, D)

R1_C141 = Q(165971304277649481670619, 324956758716416046811841770291200)
DARKHIPO_BEST = Q(51149356887949946750, 10**29)   # 20-digit display of board rank 1 (rounded up)

# ---- parameters -----------------------------------------------------------
kappa = Q(164)
rho, h, t = Q(23835, 2**16), Q(49459, 2**16), Q(1491, 2**24)
BIG = "--L24" in sys.argv
Lph = 2**24 if BIG else 2**16
Ld = Q(49334, 10000) if BIG else Q(49335, 10000)                 # = L(theta-1)
theta = 1 + Ld/Lph
mu, nu, v = Q(6716, 512), Q(7211, 512), Q(1000, 624979)

# ---- derived --------------------------------------------------------------
conds = []
def c(name, ok): conds.append((name, bool(ok)))
p = rho + (1-rho)*t
if Lph <= 2**16:
    B = theta**Lph                   # exact rational (large)
    B_lo = rdown(B, 25)
    c("B_lo <= B = theta^L exactly", B_lo <= B)
else:                                # rigorous: ln B_lo (upper) <= L ln(theta) (lower)
    lnB_lo = Lph * ln_bounds(theta)[0]
    lo, hi = Q(100), Q(200)
    for _ in range(90):
        mid = (lo+hi)/2
        mid = rdown(mid, 25)
        if ln_bounds(mid)[1] <= lnB_lo: lo = mid
        else: hi = mid
    B_lo = lo
    c("ln_hi(B_lo) <= L * ln_lo(theta), hence B_lo <= theta^L", ln_bounds(B_lo)[1] <= lnB_lo)
c("B_lo > 1", B_lo > 1)
q0 = Q(12800, 10000)
while not (q0**4 * p > 1): q0 += Q(1, 10000)
c("q0 > p^(-1/4)  [q0^4 p > 1]", q0**4 * p > 1)
A_ = (rho*(q0 + 3/v))**mu.denominator * p**mu.numerator
a = min_rat(lambda z: A_ < z**mu.denominator, Q(1, 800))
c("tilt (3a): rho p^mu (p^-1/4 + 3/v) < a   [exact integer powers]", A_ < a**mu.denominator)
Bp = (1-p)**nu.denominator * p**nu.numerator
b = min_rat(lambda z: Bp < (z*v)**nu.denominator, Q(1, 3000))
c("tilt (3b): (1-p) p^nu / v < b             [exact integer powers]", Bp < (b*v)**nu.denominator)
lam_lo = ln_bounds(1/p)[0]
d = rdown(lam_lo, 15) - Q(1, 10**15)
c("0 < d < lambda = -ln p", 0 < d < lam_lo)
K = kappa + nu
X = Q(2,3)*a*(1/p - 1) + b
la = rup(ln_bounds(1 + a)[1])
bY = rup(ln_bounds(1 + X/(1+a))[1]) + 2*rup(ln_bounds(1 + v)[1])
c("la >= log(1+a), bY >= log(1+X/(1+a)) + 2log(1+v)  [rigorous upper bounds]", True)
g = rho/4 - bY/d
a0 = 1/d
eps = mu*rho/kappa + la/d
def s_of(x): return (1-h)*(g - (eps + K*t + (K*t + K*rho/kappa)/(x-1))/h)
def C_of(x): return (1-t)*((x-1)/x)**2 * t * s_of(x) / (Ld*K)
C = C_of(B_lo)                       # C(x) increasing in x>1, so C(B) >= C(B_lo)
c("0 < gamma <= rho/4", 0 < g <= rho/4)
c("s(B_lo) > 0", s_of(B_lo) > 0)
c("(1-t)(gamma kappa + a0)/K <= 1/4", (1-t)*(g*kappa + a0)/K <= Q(1,4))
c("domains: kappa>=4 int, 0<rho,h,t,v,a,b<1, mu>1/4, nu>0",
  kappa >= 4 and kappa.denominator == 1 and all(0 < z < 1 for z in (rho,h,t,v,a,b)) and mu > Q(1,4) and nu > 0)
c("rho, h, t dyadic; L a power of 2 (fair-bit seed)", all((z.denominator & (z.denominator-1)) == 0 for z in (rho,h,t)) and Lph & (Lph-1) == 0)
c("C > board rank 1 (5.1149356887949946750e-10)", C > DARKHIPO_BEST)
c("C > C141", C > R1_C141)

ok = True
for name, okc in conds:
    print("[%s] %s" % ("PASS" if okc else "FAIL", name)); ok &= okc
print("params: kappa=%s rho=%s h=%s t=%s L=%d L(theta-1)=%s" % (kappa, rho, h, t, Lph, Ld))
print("        mu=%s nu=%s v=%s a=%s b=%s d=%s q0=%s" % (mu, nu, v, a, b, d, q0))
print("B_lo   = %.20f" % float(B_lo))
print("C      = %.15e" % float(C))
print("C / board rank 1 = %.10f" % float(C / DARKHIPO_BEST))
if "--fraction" in sys.argv: print(C.numerator); print(C.denominator)
print("RESULT:", "PASS" if ok else "FAIL")
