"""Randomized check of the rank inequality used in the refined residual bound.

For a list of vectors placed pair by pair (u_t, w_t at pair e_t), with
S_i = earlier vectors at pairs containing i, we claim for each vector x at {i,j}:
  pi(x) = dim(span S_i cap span S_j)
        <= sum_{y earlier, e(y) meets e(x)} ([i in e(y)] l_i(y) + [j in e(y)] l_j(y) - g(y)).
Over GF(p), with small ambient dimension to force many dependencies.
"""
import random, itertools

P = 3

def rank(vs, n):
    rows = [list(v) for v in vs]
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, len(rows)) if rows[i][c] % P), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = pow(rows[r][c], P - 2, P)
        rows[r] = [x * inv % P for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] % P:
                f = rows[i][c]
                rows[i] = [(a - f * b) % P for a, b in zip(rows[i], rows[r])]
        r += 1
    return r

def in_span(x, vs, n):
    return rank(vs + [x], n) == rank(vs, n)

def trial(rng):
    nv = rng.randint(3, 6)
    edges = [e for e in itertools.combinations(range(nv), 2) if rng.random() < 0.6] or [(0, 1)]
    rng.shuffle(edges)
    n = rng.randint(2, 7)
    basis_pool = [[rng.randrange(P) for _ in range(n)] for _ in range(rng.randint(1, n))]
    def rvec():
        # random combination of a small pool forces dependencies
        if rng.random() < 0.5:
            cs = [rng.randrange(P) for _ in basis_pool]
            return [sum(c * b[k] for c, b in zip(cs, basis_pool)) % P for k in range(n)]
        return [rng.randrange(P) for _ in range(n)]
    placed = []  # (vector, edge, g, l dict)
    worst = 0
    for e in edges:
        for _ in range(2):
            x = rvec()
            i, j = e
            S = {v: [p[0] for p in placed if v in p[1]] for v in (i, j)}
            W = [p[0] for p in placed]
            ri, rj = rank(S[i], n), rank(S[j], n)
            rij = rank(S[i] + [y for y in S[j]], n)
            pi = ri + rj - rij
            bound = 0
            for (y, ey, gy, ly) in placed:
                if set(ey) & {i, j}:
                    bound += sum(ly[v] for v in (i, j) if v in ey) - gy
            assert pi <= bound, (pi, bound)
            worst = max(worst, pi - bound)
            g = 0 if in_span(x, W, n) else 1
            l = {v: 0 if in_span(x, S[v], n) else 1 for v in (i, j)}
            placed.append((x, e, g, l))
    return worst

rng = random.Random(1)
for _ in range(20000):
    trial(rng)
print("rank inequality held in 20000 random trials over GF(3)")
