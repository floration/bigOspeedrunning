"""Refined nondirect residual bound for the OpenAI Sidorenko construction.

Uses the sequential count of rohanarun/sidorenko-template-refinements
(proof.tex, Prop. residual-189, eq. sequential-remainder):
  R = -2m + sum_{(111),(000)} pi + sum_{(001)} (v_i+v_j) + sum_{(011)} (w'+v_i+v_j)
and replaces pi <= (v_i+v_j)/2 by the rank bound
  pi(x) <= sum_{y earlier, e(y) meets e(x)} ([i in e(y)] l_i(y) + [j in e(y)] l_j(y) - g(y)).
Per earlier vector y the summand is: (111) 1 only if same pair, else 0;
(000) 0; (001) with l_b=1: 1 at pairs through b, 0 through a only; (011) 1 at
pairs through a or b, 2 at its own pair.  Hence (bound "B")
  R <= -m + sum_{001 at (a,b), new at b} [(2d_b - 1) + k_a + k_b - 1]
          + sum_{011 at (a,b)} [(2(d_a+d_b) - 2) + k + k_a + k_b - 2],
with k_i <= min(k, 2 d_i), k <= 2m - n1 - n2, and the (111)-own-pair base <= m.
Bound "A" is the published one: R <= 178 + sum_001 (k_a+k_b-1)/2 + sum_011 (k + (k_a+k_b-2)/2).
Both are upper bounds on the same R, so R <= min(A, B).
We maximise min(A,B)/d over all m <= 28, n1, n2, k (ignoring the two-vectors-per-pair
cap, which only loosens the bound), using the full allowed-graph degrees as caps.
"""
import json, sys
from collections import defaultdict
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path

base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("original-baseline.json")
b = json.loads(base.read_text())
inc = defaultdict(list)
for t, f in enumerate(b["faces"]):
    for e in combinations(sorted(f), 2):
        inc[e].append(t)
allowed = sorted(e for e, (s, t) in inc.items()
                 if sum(x != y for x, y in zip(b["bits"][s], b["bits"][t])) == 1)
n = b["points"]
deg = [sum(v in e for e in allowed) for v in range(n)]
assert len(allowed) == 28 and sum(d * d for d in deg) - 3 * 28 == 178

def val001(k):
    best = Q(-10**9), Q(-10**9)
    for a, c in allowed:
        for (p, q) in ((a, c), (c, a)):   # q is the endpoint with l=1
            ka, kq = min(k, 2 * deg[p]), min(k, 2 * deg[q])
            B = (2 * deg[q] - 1) + ka + kq - 1
            A = Q(ka + kq - 1, 2)
            best = max(best[0], Q(B)), max(best[1], A)
    return best

def val011(k):
    bB = bA = Q(-10**9)
    for a, c in allowed:
        ka, kc = min(k, 2 * deg[a]), min(k, 2 * deg[c])
        bB = max(bB, Q((2 * (deg[a] + deg[c]) - 2) + k + ka + kc - 2))
        bA = max(bA, k + Q(ka + kc - 2, 2))
    return bB, bA

best = (Q(0), None)
best_d1 = (Q(-10**9), None)
for m in range(1, 29):
    for n1 in range(0, 2 * m + 1):
        for n2 in range(0, 2 * m + 1 - n1):
            d = n1 + 2 * n2
            if d == 0:
                continue
            for k in range(2, 2 * m - n1 - n2 + 1):
                B1, A1 = val001(k)
                B2, A2 = val011(k)
                B = -m + n1 * B1 + n2 * B2
                A = 178 + n1 * A1 + n2 * A2
                R = min(A, B)
                if R / d > best[0]:
                    best = (R / d, dict(m=m, n1=n1, n2=n2, k=k, A=str(A), B=str(B)))
                if d == 1 and R > best_d1[0]:
                    best_d1 = (R, dict(m=m, k=k, A=str(A), B=str(B)))
print("max R for d=1:", best_d1[0], best_d1[1])
print("max R/d over all d>=1:", best[0], float(best[0]), best[1])
