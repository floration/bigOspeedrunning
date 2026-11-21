# Tilted-window bound for simple zeros on the critical line

**Result (certified finite step, unrefereed argument):**

    liminf N0s(T,2T)/N(T,2T) >= (100000/98959) * (H(3/2) - 29997/5000000) = 0.6734096571...   (11 zeros)

Earlier 10-zero step: (20000/19807) * (H(3/2) - 13749/2500000) = 0.6733975489...

where H(3/2) = 2 - R(psi) for the window psi(t) = cos(3t/2) on [-1/2,1/2]:

    H(3/2) = (-69 + 72 cos(3/2) + 34 sin(3/2)) / (48 (cos(3/2) - 1)) = 0.6723988625986842...

Previous: 0.6731134 (leaderboard #1, Bhattacharjee–Bhattacharya v1.0.0), 0.6732896 (their unposted
release 1.3.0, github.com/creelie/mh-phys), H_MT = 0.6725007 (Alpöge–Furman, Lean verified).

## What changed versus creelie/mh-phys 1.3.0

Their argument: S >= H*N + Defect - o(N), with the defect bounded below by a window inequality
F(g) >= c0 over R consecutive zeros (weights a_{r,i}, b_i with linear total mu), giving (H - mu)/(1 - c0).
They used the Montgomery–Taylor window cos(sqrt2 t), which maximises H alone.

With the defect term present, the MT window is no longer optimal. Tilting to cos(a t), a = 3/2,
lowers H by 1.0e-4 but raises the window minimum c0 enough to net +1.1e-4. (Their paper tested tilts
only for uniform 7-zero windows and reported +0.00004, then did not apply it.)

Every ingredient carries over for psi = cos(3t/2)1_{[-1/2,1/2]}:
1. **Alpöge–Furman input.** AF §2.2 allows any even C^2 window positive on [-1/2,1/2]; the chain gives
   ||G||_HS^2 = (R(psi)+o(1))N with R(psi) from their Lemma 5.6 (5.13). cos(3t/2) is positive there
   (3/4 < pi/2). AF §7.3 itself uses cos(8s/5). `Hexact.py` evaluates 2 - R(psi) in closed form (matches
   MT value at a = sqrt2).
2. **Kernel.** k(x) = K(x)/K(0), K(x) = (1/2)[sinc((a-2 pi x)/2) + sinc((a+2 pi x)/2)], K(0) = sinc(a/2) = 0.9088517.
   k is decreasing on [0,1] by the same argument (cos(at) > 0 on the window).
3. **Eigenvalue lemma** with delta1 = 57/100: sinc^2(pi delta1 u) >= cos(3u/2) on |u| <= 1/2 (Taylor
   endpoint proof in Arb, `eig_tilt.py`), so 0.57-separated points have Gram eigenvalues <= 1/(delta1 K0)
   = 1.93033 < 2. Lattice check: 1.930331 (sharp). w(delta1) = 0.33466.
4. **Block condition** (R+1)c0 <= (4/3) w(delta1): 11 * 0.00965 = 0.106 <= 0.446. OK.
5. **Window inequality** R = 10, weights `weights10_a15.txt` (symmetric, pair sums <= 2, linear total
   13749/2500000): F >= 193/20000, VERIFIED by the authors' unchanged verifier `verify/bbp_cf.c`
   (second-order interval branch and bound, round-down arithmetic) on tables rebuilt for a = 3/2 by
   `table_a.py` / `dtable_a.py` (the authors' table scripts with sqrt2 -> 3/2, Arb 128-bit):
   3,659,042,858 nodes, log `bbpcf10_a15_193.log`. Table sha256 in `tables.log`.
   Numerical minimum of F with these rounded weights: 0.009655039 (`minF.py`).

**Tighter target (max gamified, same weights):** F >= 4827/500000 also VERIFIED (3,768,836,024 nodes,
`bbpcf10_a15_4827.log`), giving (500000/495173)(H(3/2) - 13749/2500000) = 0.6734002688. The next step,
1931/200000, fails at one cell (lb 0.00965498), so grid 1/4000 is exhausted for these weights.

**11 zeros:** weights `weights11_a15.txt` (linear total 29997/5000000, numerical min 0.01042322),
F >= 1041/100000 VERIFIED (53,246,449,737 nodes, `bbpcf11_a15_1041.log`). Block condition 12 * 0.01041 = 0.125 <= 0.446.
Bound 0.6734096571. Tighter targets up to ~0.010422 (-> ~0.673418) untried; each run takes hours.

## Reproduce

    python3 table_a.py 4000 80000 wA_80k.bin ; python3 dtable_a.py 4000 80000 4 dA_80k.bin
    gcc -O2 -frounding-math -fopenmp -o bbp_cf <creelie/mh-phys>/verify/bbp_cf.c -lm
    OMP_NUM_THREADS=4 ./bbp_cf 10 4000 wA_80k.bin dA_80k.bin weights10_a15.txt 193 20000

Sanity checks done first: rebuilt the authors' MT tables (sha256 match), re-ran their 10-zero
certificate (VERIFIED, identical node count 1,424,333,714), and my weight LP (`mylp_a.py`) reproduced
their 0.6732900 at a = sqrt2.

## Caveats
- Rests on Alpöge–Furman (preprint; Lean-checked only for the MT window) and on the creelie/Jo stability
  framework (unrefereed). The changes above are mechanical but have not been written up as a paper or
  checked by anyone else.
- Method ceiling (periodic patterns, R -> infinity) rises from ~0.67357 (a = sqrt2) to ~0.67365 (a ~ 1.53).
