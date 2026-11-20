#!/usr/bin/env python3
"""Exact-rational certificate for a re-tuned scalar chain of the one-sample matroid
prophet construction (Chen bound-111 / Shea / OpenAI). Stdlib only.

Changes vs. the incumbent scalar chain (algorithm constants kappa,rho,h,t,theta,L unchanged):
 1. tilt (3) checked directly with a tight rational bound q0 > p^(-1/4) instead of 4/3;
 2. log M* bounded with rigorous upper bounds on log(1+a), log(1+X/(1+a)), log(1+v)
    instead of log(1+x) <= x, and with 1/p kept instead of the weaker 1/rho;
 3. analysis constants mu, nu, v, a, b, d re-optimised (rationals, not on a 1/8 grid);
 4. evaluated at x = B exactly.
"""
import sys
from fractions import Fraction as Q

def atanh2(y, n=40):   # rigorous bounds for ln((1+y)/(1-y)), 0<=y<1/2
    s = sum((2*y**(2*j+1)/(2*j+1) for j in range(n)), Q(0))
    return s, s + 2*y**(2*n+1)/((2*n+1)*(1-y*y))
LN2 = atanh2(Q(1,3))
def ln_bounds(x):      # rigorous rational (lo, hi) for ln x
    if x < 1:
        lo, hi = ln_bounds(1/x); return -hi, -lo
    k = 0
    while x / 2**k >= 2: k += 1
    y = x / 2**k; lo, hi = atanh2((y-1)/(y+1))
    return lo + k*LN2[0], hi + k*LN2[1]

def ratdown(x, digits):   # rational just below/at x with given decimal precision
    D = 10**digits; return Q((x.numerator*D)//x.denominator, D)
def ratup(x, digits):
    D = 10**digits; return Q(-((-x.numerator*D)//x.denominator), D)

# algorithm constants (unchanged from the incumbent)
kappa, rho, h, t = Q(164), Q(93,256), Q(3,4), Q(23,2**18)
theta, Lph = Q(261,256), 256
B = theta**Lph
p = rho + (1-rho)*t

def chain(mu, nu, v, a, b, d, exactlog=True, x=None, q0=None):
    """Return dict with C, conditions. exactlog=False reproduces the incumbent's formulas."""
    x = B if x is None else x
    K = kappa + nu
    if exactlog:
        X = Q(2,3)*a*(1/p - 1) + b
        la = ratup(ln_bounds(1 + a)[1], 30)
        bY = ratup(ln_bounds(1 + X/(1+a))[1], 30) + 2*ratup(ln_bounds(1 + v)[1], 30)
    else:
        la = a
        bY = (Q(2,3)*a*(1/rho - 1) + b)/(1 + a) + 2*v
    g = rho/4 - bY/d
    a0 = 1/d
    eps = mu*rho/kappa + la/d
    Lx = eps + K*t + (K*t + K*rho/kappa)/(x - 1)
    s = (1-h)*(g - Lx/h)
    Cx = (1-t)*((x-1)/x)**2 * t * s / (Lph*(theta-1)*K)
    lam_lo = ln_bounds(1/p)[0]
    conds = []
    def c(name, ok): conds.append((name, bool(ok)))
    # tilt (3a): rho p^mu (p^-1/4 + 3/v) <= a, mu = m/qd rational
    m, qd = mu.numerator, mu.denominator
    if q0 is not None:
        c("q0 > p^(-1/4)  [q0^4 p > 1]", q0**4 * p > 1)
        c("tilt a: (rho(q0+3/v))^qd p^m < a^qd", (rho*(q0+3/v))**qd * p**m < a**qd)
    # tilt (3b): (1-p) p^nu / v <= b
    m2, q2 = nu.numerator, nu.denominator
    c("tilt b: (1-p)^q p^m < (b v)^q", (1-p)**q2 * p**m2 < (b*v)**q2)
    c("0 < d <= lambda (d < rigorous lower bound of -ln p)", 0 < d < lam_lo)
    c("0 < gamma <= rho/4", 0 < g <= rho/4)
    c("s(B) > 0", s > 0)
    c("(1-t)(gamma kappa + a0)/K <= 1/4", (1-t)*(g*kappa + a0)/K <= Q(1,4))
    c("domains: mu>1/4, nu>0, 0<v,a,b<1", mu > Q(1,4) and nu > 0 and 0<v<1 and 0<a<1 and 0<b<1)
    c("B = (261/256)^256 > 141 and L(theta-1) = 5", B > 141 and Lph*(theta-1) == 5)
    return dict(C=Cx, conds=conds, gamma=g, s=s, eps=eps, bY=bY)

R1_C141 = Q(165971304277649481670619, 324956758716416046811841770291200)

def selftest():
    r = chain(Q(105,8), Q(113,8), Q(1,624), Q(1,864), Q(1,4000), Q(253,250), exactlog=False, x=Q(141))
    ok1 = r["C"] == R1_C141
    r2 = chain(Q(105,8), Q(113,8), Q(1,624), Q(1,867), Q(1,4088), Q(2024848371,2000000000), exactlog=False)
    print("selftest C(141) at bound-111 params == published C141:", ok1)
    print("selftest darkhipo params C(B) = %.16e" % float(r2['C']))
    return ok1, r2["C"]

if __name__ == "__main__":
    ok, Cdark = selftest()
    if "--variant-b" in sys.argv:
        # Variant B: also re-tunes the algorithm's mask rates (kappa, theta, L unchanged).
        # Seed budget becomes 67|E|+31 fair bits (rho, h: 11 bits; t: 22 bits).
        rho, h, t = Q(745, 2048), Q(1545, 2048), Q(373, 2**22)
        p = rho + (1-rho)*t
        mu, nu, v = Q(6717, 512), Q(7212, 512), Q(1, 625)
        print("VARIANT B: rho=%s h=%s t=%s" % (rho, h, t))
    else:
        # Variant A: algorithm identical to the incumbent.
        mu, nu, v = Q(6705, 512), Q(1801, 128), Q(1, 622)
        print("VARIANT A: algorithm constants unchanged")
    # tight rational q0 > p^(-1/4): search
    q0 = Q(12800, 10000)
    while not (q0**4 * p > 1): q0 += Q(1, 10000)
    # minimal a, b: compute via bisection on rationals with 12 digits
    def min_rat(pred, lo, hi, digits=12):
        D = 10**digits; lo, hi = int(lo*D), int(hi*D)+1
        while hi - lo > 1:
            mid = (lo+hi)//2
            if pred(Q(mid, D)): hi = mid
            else: lo = mid
        return Q(hi, D)
    m, qd = mu.numerator, mu.denominator
    A_ = (rho*(q0+3/v))**qd * p**m
    a = min_rat(lambda z: A_ < z**qd, Q(0), Q(1,800))
    Bp = (1-p)**nu.denominator * p**nu.numerator
    b = min_rat(lambda z: Bp < (z*v)**nu.denominator, Q(0), Q(1,3000))
    d = ratdown(ln_bounds(1/p)[0], 15) - Q(1, 10**15)
    r = chain(mu, nu, v, a, b, d, exactlog=True, q0=q0)
    allok = ok
    for name, okc in r["conds"]:
        print("[%s] %s" % ("PASS" if okc else "FAIL", name)); allok &= okc
    C = r["C"]
    print("params: mu=%s nu=%s v=%s a=%s b=%s d=%s q0=%s" % (mu, nu, v, a, b, d, q0))
    print("C      = %.17e" % float(C))
    print("C/C141 = %.10f   C/darkhipo = %.10f" % (float(C/R1_C141), float(C/Cdark)))
    print("C > darkhipo (exact):", C > Cdark, " C > C141:", C > R1_C141)
    if "--fraction" in sys.argv: print(C.numerator); print(C.denominator)
    print("RESULT:", "PASS" if allok and C > Cdark else "FAIL")
