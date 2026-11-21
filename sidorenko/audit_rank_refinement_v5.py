"""v5: generic bases + time-reversal trade-off between w' and the pi-weights.

Two new rigorous savings over v2/v3 (see NOTE.md, "Five ideas"):
 (G) Generic bases.  Count only ordered bases (u_t, w_t) with u_t outside every proper
     subspace among H_t cap W', H_t cap V'_a, H_t cap V'_b, and w_t outside span(u_t).
     Each 2-space still has >= (q^2-4q)(q^2-q) such bases, so the family count changes
     by a constant factor only.  Then a pair with exactly one defect vector has u_t of
     type (1,1,1) and the defect at w_t; a pair with u_t defective has H_t inside W'.
 (T) Trade-off.  For a (0,1,1) vector y, w'(y) = #earlier g=1 vectors
        = k - #(later g=1 vectors), and y's pi-weight goes only to later non-defect
     vectors (types (1,1,1), (0,0,0)).  Hence
        w'(y) + weight(y) <= k + n0 = 2m - n1 - n2.
Bound:  R <= -2m + (m - P) + n2 (2m - n1 - n2) + sum_{011} (k_a + k_b - 2)
            + sum_{001 new at b} (2 d_b - 2 + k_a + k_b - 1),
with P = number of pairs carrying a defect vector, k_i <= 2 d_i.  Exact DP over the 28
allowed pairs (<= 2 defect vectors per pair), all m <= 28, all n1, n2.
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
deg = [sum(v in e for e in allowed) for v in range(b["points"])]
assert len(allowed) == 28

def opts(e):
    a, c = e
    cap = 2 * deg[a] + 2 * deg[c]
    v011 = cap - 2
    v001 = [2 * deg[c] - 2 + cap - 1, 2 * deg[a] - 2 + cap - 1]
    # Single defect: either at w_t (u_t is (1,1,1), base for this pair lost: -1), or at
    # u_t with H_t inside W' and w_t of type (0,0,0), when u_t's own weight on w_t
    # (2 for (011), 1 for (001)) exceeds the trade-off count by at most 1 and the
    # base is lost (-1).  The worse of the two is +0, so no -1 here.
    out = [(0, 1, v011)] + [(1, 0, v) for v in v001]
    out.append((0, 2, 2 * v011 - 1))
    out += [(1, 1, v011 + v - 1) for v in v001]
    out += [(2, 0, v1 + v2 - 1) for v1 in v001 for v2 in v001]
    return out

dp = {(0, 0, 0): 0}            # (n1, n2, pairs used) -> max sum
for e in allowed:
    new = dict(dp)
    for (n1, n2, u), v in dp.items():
        for a1, a2, w in opts(e):
            key = (n1 + a1, n2 + a2, u + 1)
            if new.get(key, -10**9) < v + w:
                new[key] = v + w
    dp = new

best, best1 = (Q(-1), None), (-10**9, None)
for (n1, n2, u), v in dp.items():
    d = n1 + 2 * n2
    if d == 0:
        continue
    for m in range(max(u, 2), 29):
        if 2 * m - n1 - n2 < 2:
            continue
        R = -m + v + n2 * (2 * m - n1 - n2)
        if Q(R, d) > best[0]:
            best = (Q(R, d), dict(n1=n1, n2=n2, pairs=u, m=m, R=R))
        if d == 1 and R > best1[0]:
            best1 = (R, dict(m=m, n1=n1))
print("d=1 max R:", best1)
print("max R/d:", best[0], float(best[0]), best[1])
