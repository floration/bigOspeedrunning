"""Randomized check over GF(3) of the trade-off (T) used in v5:
for every (0,1,1) vector y,  w'(y) + sum_{x later, non-defect, e(x) meets e(y)} c_x(y)
   <= k + n0 + 1,  the +1 only from y = u_t's own partner w_t."""
import random, itertools, importlib.util, sys
spec = importlib.util.spec_from_file_location("rb", __file__.replace("tradeoff_check.py", "rank_bound_check.py"))
src = open(spec.origin).read().split("rng = random.Random(1)")[0]
ns = {}; exec(src, ns)
rank, in_span = ns["rank"], ns["in_span"]
P = ns["P"]
rng = random.Random(7)
viol = 0; tested = 0
for _ in range(6000):
    nv = rng.randint(3, 6)
    edges = [e for e in itertools.combinations(range(nv), 2) if rng.random() < 0.6] or [(0, 1)]
    rng.shuffle(edges)
    n = rng.randint(3, 8)
    pool = [[rng.randrange(P) for _ in range(n)] for _ in range(rng.randint(2, n))]
    def rvec():
        if rng.random() < 0.6:
            cs = [rng.randrange(P) for _ in pool]
            return [sum(c * bb[q] for c, bb in zip(cs, pool)) % P for q in range(n)]
        return [rng.randrange(P) for _ in range(n)]
    placed = []
    for t, e in enumerate(edges):
        for pos in range(2):
            x = rvec()
            S = {v: [p[0] for p in placed if v in p[1]] for v in e}
            g = 0 if in_span(x, [p[0] for p in placed], n) else 1
            l = {v: 0 if in_span(x, S[v], n) else 1 for v in e}
            placed.append((x, e, g, l, len(placed)))
    k = sum(p[2] for p in placed)
    def typ(p):
        return p[2], sum(p[3].values())
    defect = lambda p: sum(p[3].values()) - 2 * p[2] > 0
    n0 = sum(1 for p in placed if p[2] == 0 and not defect(p))
    for idx, y in enumerate(placed):
        if not (y[2] == 0 and sum(y[3].values()) == 2):
            continue
        tested += 1
        wprime = sum(p[2] for p in placed[:idx])
        weight = 0
        for x in placed[idx + 1:]:
            if defect(x) or not (set(x[1]) & set(y[1])):
                continue
            weight += sum(y[3][v] for v in x[1] if v in y[1]) - y[2]
        if wprime + weight > k + n0 + 1:
            viol += 1
print("tested", tested, "(0,1,1) vectors; violations:", viol)
