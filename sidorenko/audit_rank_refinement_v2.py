"""Refined nondirect residual bound, v2 (per-pair accounting).

Same setting as audit_rank_refinement.py (read NOTE.md).  Starting from
  R = -2m + sum_{nondefect x} pi(x) + sum_{(001)} (v_a+v_b) + sum_{(011)} (w'+v_a+v_b)
and the rank bound pi(x) <= sum_{y earlier, e(y) meets e(x)} c_x(y) with
  c_x(y) = [i in e(y)] l_i(y) + [j in e(y)] l_j(y) - g(y),
group the contributions by pair.  For y = u_t (first vector of pair t), its weight
on x = w_t is l_a+l_b-g: 1 for (111), 0 for (000), 1 for (001), 2 for (011).  The
(111)->w_t weights total at most m minus the number of pairs carrying a defect vector,
because such a pair has either u_t defective or w_t defective (so excluded from the
pi-sum).  Weights on other pairs: (011) gives 1 to every vector at a pair through a
or b; (001) new at b gives 1 at pairs through b only.  Per pair carrying defects:
  one (011):        2(s-2) + 2 - 1          + (k + k_a + k_b - 2)
  one (001)@b:      2(d_b-1) + 1 - 1        + (k_a + k_b - 1)
  two defects:      neighbour weights of both - 1 + both defect terms
with s = d_a + d_b, k_i <= min(k, 2 d_i), w' <= k, and k <= 2m - n1 - n2.
Bound A (published): R <= 178 + n1*(k_a+k_b-1)/2 + n2*(k + (k_a+k_b-2)/2), maxima over edges.
R <= min(A, B).  We maximise min(A, B)/d by an exact DP over the 28 allowed pairs.
"""
import json, sys
from collections import defaultdict
from fractions import Fraction as Q
from itertools import combinations
from math import ceil
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

def options(e, k):
    """(n1, n2, value) for every defect configuration of one pair."""
    a, c = e
    da, dc = deg[a], deg[c]
    s = da + dc
    ka, kc = min(k, 2 * da), min(k, 2 * dc)
    t011 = k + ka + kc - 2
    t001 = ka + kc - 1
    nb011 = 2 * (s - 2)                       # neighbour weight of a (011)
    nb001 = [2 * (dc - 1), 2 * (da - 1)]      # new at c / new at a
    out = [(0, 0, 0)]
    out.append((0, 1, nb011 + 2 - 1 + t011))
    for w in nb001:
        out.append((1, 0, w + 1 - 1 + t001))
    # two defect vectors at the same pair: own weights excluded, base -1 once
    out.append((0, 2, 2 * nb011 - 1 + 2 * t011))
    for w in nb001:
        out.append((1, 1, nb011 + w - 1 + t011 + t001))
    for w1 in nb001:
        for w2 in nb001:
            out.append((2, 0, w1 + w2 - 1 + 2 * t001))
    return out

NMAX = 24
best = (Q(0), None)
best1 = (-10**9, None)
for k in range(2, 56):
    # DP over pairs: state (n1, n2, used) -> max value
    dp = {(0, 0, 0): 0}
    for e in allowed:
        new = dict(dp)
        for (n1, n2, u), v in dp.items():
            for (a1, a2, w) in options(e, k):
                if a1 == a2 == 0:
                    continue
                key = (n1 + a1, n2 + a2, u + 1)
                if key[0] + key[1] > NMAX:
                    continue
                if new.get(key, -10**9) < v + w:
                    new[key] = v + w
        dp = new
    A1 = max(Q(min(k, 2*deg[a]) + min(k, 2*deg[c]) - 1, 2) for a, c in allowed)
    A2 = max(k + Q(min(k, 2*deg[a]) + min(k, 2*deg[c]) - 2, 2) for a, c in allowed)
    for (n1, n2, u), v in dp.items():
        d = n1 + 2 * n2
        if d == 0:
            continue
        m = max(u, ceil((k + n1 + n2) / 2), 2)
        if m > 28:
            continue
        B = -m + v
        A = 178 + n1 * A1 + n2 * A2
        R = min(Q(B), A)
        if R / d > best[0]:
            best = (R / d, dict(k=k, n1=n1, n2=n2, pairs=u, m=m, A=str(A), B=B))
        if d == 1 and R > best1[0]:
            best1 = (R, dict(k=k, m=m, B=B, A=str(A)))
print("d=1 max R:", best1)
print("max R/d:", best[0], float(best[0]), best[1])
