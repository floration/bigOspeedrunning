"""v6: v5 plus the distinct-local-dimension saving, solved exactly by branch and bound.

(0,1,1) vectors at a common vertex a have l_a = 1, so their v'_a are distinct values in
{0..k_a-1}: c of them lose at least c(c-1)/2 from the caps.  (0,0,1) vectors add at most
max(2 d_b - 2 + 2 d_a + 2 d_b - 1) <= 33 per defect unit and lower K = 2m - n1 - n2, so
they cannot lift R/d above 33; likewise m = 28 is worst once n2 >= 1.  So it suffices to
maximise, over multiplicities c_e in {0,1,2} of (0,1,1) vectors on the 28 allowed pairs,
   R = -28 + sum_e [c_e (2 d_a + 2 d_c - 2) - [c_e = 2]] + n2 (56 - n2) - sum_v C(c_v, 2).
"""
import json, sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from fractions import Fraction as Q

base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("original-baseline.json")
b = json.loads(base.read_text())
inc = defaultdict(list)
for t, f in enumerate(b["faces"]):
    for e in combinations(sorted(f), 2):
        inc[e].append(t)
allowed = sorted(e for e, (s, t) in inc.items()
                 if sum(x != y for x, y in zip(b["bits"][s], b["bits"][t])) == 1)
deg = [sum(v in e for e in allowed) for v in range(b["points"])]
n001 = max(2 * deg[q] - 2 + 2 * deg[p] + 2 * deg[q] - 1 for a, c in allowed for p, q in ((a, c), (c, a)))
assert n001 <= 33
E = sorted(allowed, key=lambda e: -(deg[e[0]] + deg[e[1]]))
val = [2 * deg[a] + 2 * deg[c] - 2 for a, c in E]
suffix_best = [max(val[i:]) if i < len(E) else 0 for i in range(len(E) + 1)]

best = [Q(0), None]
def run(N):
    """max of sum_e(...) - savings with exactly N vectors."""
    top = [-10**9, None]
    cv = [0] * b["points"]
    mult = [0] * len(E)
    def dfs(i, left, acc):
        if left == 0:
            if acc > top[0]:
                top[0], top[1] = acc, list(mult)
            return
        if i == len(E) or acc + left * suffix_best[i] <= top[0]:
            return
        a, c = E[i]
        for m_ in (2, 1, 0):
            if m_ > left:
                continue
            gain = m_ * val[i] - (1 if m_ == 2 else 0)
            # saving: adding m_ vectors at a raises C(c_a,2) by m_*c_a + C(m_,2)
            loss = m_ * cv[a] + m_ * (m_ - 1) // 2 + m_ * cv[c] + m_ * (m_ - 1) // 2
            cv[a] += m_; cv[c] += m_; mult[i] = m_
            dfs(i + 1, left - m_, acc + gain - loss)
            cv[a] -= m_; cv[c] -= m_; mult[i] = 0
    dfs(0, N, 0)
    return top

for N in range(1, 15):
    v, mult = run(N)
    R = -28 + v + N * (56 - N)
    r = Q(R, 2 * N)
    print(N, R, float(r), {str(E[i]): mult[i] for i in range(len(E)) if mult[i]})
    if r > best[0]:
        best = [r, N]
# beyond 14 vectors: each adds at most 22 + 56 - N <= 63 < 2*33, so the ratio only falls
print("max R/d over (0,1,1)-only strata:", best[0], float(best[0]), "at n2 =", best[1])
