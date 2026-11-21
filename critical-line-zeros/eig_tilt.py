"""Eigenvalue lemma for the tilted window cos(a t), a = 3/2: majorant sinc^2(pi d1 u) >= cos(a u) on |u| <= 1/2,
so spec(k(x_i-x_j)) lies in [0, 1/(d1 K0)] for d1-separated points.  Rigorous part in Arb with exact rationals."""
import numpy as np
from flint import arb, ctx, fmpq
ctx.prec = 128
A = fmpq(3, 2); d1 = fmpq(57, 100)
pi = arb.pi(); a = arb(A); K0 = 2*(a/2).sin()/a
print("K0 =", K0, " 1/(d1 K0) =", 1/(arb(d1)*K0), " critical 1/(2K0) =", 1/(2*K0))
# cos x <= 1 - x^2/2 + x^4/24 (all real x); sinc^2 t >= 1 - t^2/3 + 2t^4/45 - t^6/315 for |t| <= 1 (alternating, decreasing)
# With s = u^2: need  (P/3 - a^2/2) + (a^4/24 - 2P^2/45) s + (P^3/315) s^2 <= 0 on [0,1/4], P = (pi d1)^2.  Convex in s -> endpoints.
P = (pi*d1)**2
e0 = P/3 - a**2/2; e1 = e0 + (a**4/24 - 2*P**2/45)/4 + (P**3/315)/16
print("endpoint values (must be < 0):", e0, e1, " t_max = pi d1/2 =", pi*d1/2)
assert e0 < 0 and e1 < 0 and pi*d1/2 < 1 and 1/(arb(d1)*K0) < 2
af = 1.5; dd = 0.57
u = np.linspace(1e-3, .5, 100000); print("float check min (sinc^2-cos)/u^2:", ((np.sinc(dd*u)**2 - np.cos(af*u))/u**2).min())
t0 = af/(2*np.pi); k = lambda x: 0.5*(np.sinc(x - t0) + np.sinc(x + t0))/np.sinc(t0)
for m in [100, 1000]:
    y = dd*np.arange(m); print(f"lattice {dd}, {m} pts: lambda_max = {np.linalg.eigvalsh(k(y[:,None]-y[None,:]))[-1]:.6f}")
# w(d1) lower bound, k decreasing on [0,1] (K' = -int 2 pi t cos(a t) sin(2 pi x t) dt < 0 since cos(a t) > 0 on |t|<=1/2 as a/2 < pi/2)
x = arb(d1); f = 2*pi*x; kd1 = (((a - f)/2).sinc() + ((a + f)/2).sinc())/2/K0
print("k(d1) =", kd1, " w(d1) =", kd1**2)
