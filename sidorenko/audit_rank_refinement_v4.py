"""v3: add the defect-defect exclusion and the distinct-local-dimension saving to v2 and solve the high-degree part exactly.

Extra observation over v2: the pi-sum runs over non-defect vectors only, so when two
(0,1,1) vectors sit at distinct pairs sharing a vertex, the earlier one's weight 1 on
the later one is not used.  Whatever the order, this saves 1 per such adjacent couple.

Reduction (argued in NOTE.md):
 * n1 = 0 is worst once R/d > 33, since a (001) vector adds at most 2d_b-2+k_a+k_b-1 <= 33
   per defect unit and lowers the k available to the (011) vectors.
 * k = 2m - n2 with m = 28 is worst (B grows by n2 - 1/2 per unit of k, A grows too).
 * a (011) vector at a pair with s = d_a+d_b <= 9 adds at most 2s-3 + k + 2s-2 <= 31+55
   = 86 = 43*2, so it cannot lift R/d above 43; only the 15 pairs with s >= 10 matter.
We enumerate all 3^15 multiplicities (0,1,2 (011) vectors per high pair).
"""
import json, sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path
import numpy as np

base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("original-baseline.json")
b = json.loads(base.read_text())
inc = defaultdict(list)
for t, f in enumerate(b["faces"]):
    for e in combinations(sorted(f), 2):
        inc[e].append(t)
allowed = sorted(e for e, (s, t) in inc.items()
                 if sum(x != y for x, y in zip(b["bits"][s], b["bits"][t])) == 1)
deg = [sum(v in e for e in allowed) for v in range(b["points"])]
H = [e for e in allowed if deg[e[0]] + deg[e[1]] >= 10]
low_max = max(2 * (deg[a] + deg[c]) - 5 + 55 + 2 * deg[a] + 2 * deg[c] - 2
              for a, c in allowed if deg[a] + deg[c] <= 9)
n001_max = max(2 * deg[q] - 3 + 2 * deg[p] + 2 * deg[q] - 1
               for a, c in allowed for p, q in ((a, c), (c, a)))
print("high pairs:", len(H), " low (011) max per vector:", low_max, " (001) max:", n001_max)
print("target per defect unit:", low_max / 2)

L = len(H)
s = np.array([deg[a] + deg[c] for a, c in H])
caps = np.array([2 * deg[a] + 2 * deg[c] for a, c in H])
adj = np.array([[1 if (i != j and set(H[i]) & set(H[j])) else 0 for j in range(L)] for i in range(L)])

best = (0.0, None)
idx = np.arange(3 ** L, dtype=np.int64)
C = np.zeros((3 ** L, L), dtype=np.int8)
x = idx.copy()
for j in range(L):
    C[:, j] = x % 3
    x //= 3
n2 = C.sum(axis=1).astype(np.int64)
k = 56 - n2
ok = (n2 > 0) & (n2 <= 28)
# per-pair values, linear in k:  one: 2(s-2)+1 + (k + cap - 2);  two: 4(s-2)-1 + 2(k + cap - 2)
one = (C == 1).astype(np.int64)
two = (C == 2).astype(np.int64)
lin = one @ (2 * (s - 2) - 1 + caps - 2) + two @ (4 * (s - 2) - 1 + 2 * (caps - 2)) + n2 * k
Cf = C.astype(np.int64)
sav = ((Cf @ adj) * Cf).sum(axis=1) // 2
# (011) vectors at a common vertex a all have l_a = 1, so their v'_a are distinct
# values in {0,...,k_a-1}: c vectors there lose at least 0+1+...+(c-1) from the caps.
inc_v = np.zeros((L, b["points"]), dtype=np.int64)
for j, (a, c) in enumerate(H):
    inc_v[j, a] = inc_v[j, c] = 1
cv = Cf @ inc_v
sav = sav + (cv * (cv - 1) // 2).sum(axis=1)
B = -28 + lin - sav
A2 = 178 + n2 * (k + 11)          # published bound, (k_a+k_b-2)/2 <= 11
R = np.minimum(B * 2, A2 * 2) / 2  # both integers here
ratio = np.where(ok, R / np.maximum(2 * n2, 1), -1)
i = int(ratio.argmax())
print("max R/d:", ratio[i], "config:", {str(H[j]): int(C[i, j]) for j in range(L) if C[i, j]},
      "n2 =", int(n2[i]), "B =", int(B[i]), "A =", int(A2[i]))
