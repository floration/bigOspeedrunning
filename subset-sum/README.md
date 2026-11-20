# Subset Sum: tightened-slack point, T = 0.4875739649

Base: Jennifer Voitle's self-contained proof (repo jv1000/subset-sum, `selfcontained-2026/`, HEAD 38e5335, 17 Nov 2026),
threshold T = 0.4875754036 (listed on bigospeedrun as 0.4875755, Claimed).

## What changed (loose constants only; same algorithm, same proof, same filter)
| Constant | Voitle | Here | Constraint it must satisfy |
|---|---|---|---|
| eps (pattern accuracy) | 1e-8 | 1e-10 | (N13) (18+6max(p))eps < eta - rho_f; T = tau0 + 20 eps |
| zeta, 1/G0 | 1e-8 each | 1e-10 each | (N1) zeta + 1/G0 < eps0 |
| eps0 (common slack of C2-C5) | 1.3156e-6 | 1e-9 | only (N1) and (E0) |
| eta - rho_f | 1.5e-6 | 1e-8 | (N13) |
| rho_f - rho_c | 1e-6 | 1e-9 | (N14); enters only P0 (log2 P0 = 336.7 < 339, aux X7 still passes) |

These constants enter the proof only through "for large n" thresholds (Chebyshev 8/(zeta^2 n), guard G0 log b <= n,
(eps0 - zeta - 1/G0) n >> n^0.6, pattern-grid size 8C0/eps+9), so shrinking them raises n_0 but not the exponent.
Scalars (tau0, eta, mu, a, gamma, l, q_m) re-optimized with the filter, kappa and p held fixed (SLSQP, float, `opt1.py`).

## Result
tau0 = 0.4875739629, T = tau0 + 20 eps = 0.4875739649  ->  O(2^{0.487574 n}); 1.4387e-6 below Voitle.
Ball-arithmetic certificate (Voitle's own script with the five constants changed; see `certify_tight.diff`):
all 39 premise lines, 8 auxiliary bounds and exact facts pass (exit 0) at 512x32 nodes, and again at 1024x32
(moments agree to 20 digits). Tightest margins: E0 2.2e-10, C3 1.22e-9, M2 3.1e-9, N13 3.1e-9.

## Caveats
* Same dependency as the record: Voitle's self-contained proof, unrefereed, no Lean.
* This is a constant-squeeze of someone else's construction (credit: Voitle; Base = A. Kapila). Gain is 1.4e-6.
* Not attempted/certified: re-optimizing the 64 filter coefficients under the tight slacks (my try was ill-conditioned),
  or Voitle's 2-filter family (paper estimates a further ~3e-6, uncertified).

Reproduce: `pip install python-flint==0.9.0; python certify_tight.py candidate_tight.json 512 32 0.1 0.25`
