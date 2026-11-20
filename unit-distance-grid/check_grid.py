"""Numerical sanity checks for the 6x5 witness (30 edges) in the unit-distance
final algebraic grid.  Not a proof: the proof is in proof_6x5.md.

The linear system, one row per edge (i, l):
    2(p_i - r_l).(H_i - U_l) - R_il (A_i - A'_l) = 0,   R_il^2 = L(L-4), L = |p_i - r_l|^2
Unknowns: H_i (2), A_i (1) per left point, U_l (2), A'_l (1) per anchor.
Trivial kernel (4-dim): H = T + w J p, U = T + w J r, A = A' = b.

Checks, over random configurations on several loci:
  1. step lemma: adding a left point with 5 anchors drops the kernel dimension by 2,
     until the trivial floor; at the step where it cannot, A_k = A'_l is forced.
  2. the full grid forces A_i = A'_l (the contradiction) for 6x5, 5x6, 8x4, 4x8,
     and does NOT for 5x5, 7x4, 4x7 on plane loci (so 30 is the floor for this system).
Run: python3 check_grid.py
"""
import numpy as np

def sample(rng, locus, n):
    if locus == 'plane':
        return rng.normal(size=(n, 2)) * 1.5
    if locus.startswith('circ'):
        rad = float(locus[4:]); t = rng.uniform(0, 2 * np.pi, n)
        return np.c_[rad * np.cos(t), rad * np.sin(t)]
    if locus == 'lineA':
        t = rng.normal(size=n) * 2; return np.c_[t, 0.3 * t + 0.1]
    if locus == 'lineB':
        t = rng.normal(size=n) * 2; return np.c_[t, -1.1 * t + 0.7]
    if locus == 'parab':
        t = rng.normal(size=n); return np.c_[t, t * t]
    raise ValueError(locus)

def matrix(rng, P, Q):
    N, j = len(P), len(Q); V = 3 * (N + j); rows = []
    for i in range(N):
        for l in range(j):
            d = P[i] - Q[l]; L = d @ d
            R = np.sqrt(complex(L * (L - 4))) * rng.choice([-1, 1])
            row = np.zeros(V, complex)
            row[3*i:3*i+2] = 2 * d; row[3*i+2] = -R
            o = 3 * N + 3 * l; row[o:o+2] = -2 * d; row[o+2] = R
            rows.append(row)
    return np.array(rows)

def kernel(Mx):
    _, s, vh = np.linalg.svd(Mx)
    r = int((s > 1e-9 * s[0]).sum())
    return Mx.shape[1] - r, vh[r:].conj().T

def forced(K, N, i, l):
    f = np.zeros(K.shape[0]); f[3*i+2] = 1; f[3*N+3*l+2] = -1
    return np.linalg.norm(f @ K) < 1e-7

LOCI = [('plane', 'plane'), ('circ1.7', 'circ1.7'), ('parab', 'plane'),
        ('lineA', 'lineB'), ('circ1.7', 'circ0.6'), ('plane', 'lineA'),
        ('lineA', 'plane'), ('parab', 'parab')]

def step_check(trials=20):
    bad = 0
    for seed in range(trials):
        rng = np.random.default_rng(seed)
        for l1, l2 in LOCI:
            Q = sample(rng, l2, 5); P = sample(rng, l1, 6); prev = 15
            for k in range(1, 7):
                d, K = kernel(matrix(rng, P[:k], Q))
                if prev - d < 2:
                    if not all(forced(K, k, k - 1, l) for l in range(5)):
                        bad += 1; print('FAIL', seed, l1, l2, k)
                    break
                prev = d
            else:
                bad += 1; print('no contradiction', seed, l1, l2)
    print(f'step lemma: {trials*len(LOCI)} configurations, {bad} failures')
    return bad == 0

def grid_check():
    ok = True
    expect = {(6, 5): True, (5, 6): True, (8, 4): True, (4, 8): True,
              (5, 5): False, (7, 4): False, (4, 7): False}
    rng = np.random.default_rng(12345)
    for (N, j), want in expect.items():
        d, K = kernel(matrix(rng, sample(rng, 'plane', N), sample(rng, 'plane', j)))
        anyforced = any(forced(K, N, i, l) for i in range(N) for l in range(j))
        print(f'{N}x{j} = {N*j:2d} edges, plane/plane: kernel dim {d}, contradiction forced: {anyforced}')
        ok &= (anyforced == want)
    return ok

if __name__ == '__main__':
    a = step_check(); b = grid_check()
    print('ALL OK' if a and b else 'MISMATCH')
