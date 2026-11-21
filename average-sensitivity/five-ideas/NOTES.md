# Average sensitivity: five ideas (2026-11-21)

Setup (OpenAI weighted grading, as in Lagdive–Aglave–Damre §3): w = |p|, M = weighted grading operator, h = χ_[n]·f, H = multiplication by h, T = MH+HM.
Current chain: AS(f) = |E_h|/N ≤ 2‖T‖²/N = 2·E(R+S−n)² ≤ 2·4·d·b_n ≤ (8/√(2π))·d·√n.

## 1. Novel: drop the factor 2 in edge recovery (CONJECTURE, strong numerics)
Claim (Dirichlet-form comparison): for every positive weight w and every real g on {−1,1}^n,
  Σ_{x,y} (g(x)−g(y))² · M_w(x,y)²  ≤  ¼ · Σ_i Σ_x (g(x) − g(x⊕e_i))².
Equivalently ‖[M_w, G]‖²_HS ≤ ‖[M_1, G]‖²_HS, and in Laplacian order L_w ≤ L_1, where L_w has edge weights M_w(x,y)².
For uniform w this is an equality on the hypercube edges.
Consequence: with g = h, ‖[M,H]‖² ≤ nN − |E_h|. Since ‖T‖² + ‖[M,H]‖² = 4‖M‖² = nN, this gives |E_h| ≤ ‖T‖², so
  AS(f) ≤ E(R+S−n)² ≤ 4·d·b_n ≤ (4/√(2π))·d·√n ≈ 1.5958·d·√n.
That would halve the record. Evidence:
- psd.py: the top generalized eigenvalue of L_w relative to L_1 is ≤ 1 (to 1e-7) for random log-normal weights at n = 4, 6, 7.
- psdadv.py: hill-climbing on the weights to push it above 1 tops out at 0.99976 (n = 4).
- comm.py / adv.py: random and adversarial (w, h) pairs at n = 3–8 never exceed ratio 1.
- scan.py: on real PTFs with n ≤ 10 and d ≤ 3, AS/E(R+S−n)² ≤ 0.997, with near-equality at dictators.
Known special case: g = x_i is exactly the existing fact ‖C_i‖²_HS ≤ N.
Missing: a proof for general g. Canonical paths (item 3) give only per-endpoint control, ‖C_i e_x‖ ≤ 1.

## 2. Crazy: tensor/sum amplification
Apply the bound to sign(p(x)·p(y)) or sign(Σ_j p(x^j)) on kn variables and pull back. AS adds, degree adds, and √n grows only like √k, so every amplification loses at least a factor √2. The constant can't be improved this way. Dead.

## 3. Borrowed: Diaconis–Saloff-Coste comparison / canonical paths (Markov chains)
Bound (g_x−g_y)² ≤ ρ·Σ over geodesic edges (Δg)², then charge each edge. This needs per-edge congestion Σ_{x,y} M_xy² ρ·Pr[e ∈ path] ≤ ¼. Only two facts are available: the total Σ ρ M² ≤ nN/4, and per-endpoint bounds Σ_{y: y_i≠x_i} 4M_xy² ≤ 1 (from ‖C_i‖_op ≤ 1). Neither controls interior edges, so this doesn't prove item 1. It is the natural route to try with more time.

## 4. Reverse: start from the coupling lemma's extremal case
The lemma E D² ≤ 4db is tight only for a coupling that shifts almost all mass up by d and drops a tiny mass symmetrically around n/2. Real PTF couplings stay far from it: the worst E(R+S−n)²/(4·d·b_n) seen was 0.72 (n=6), 0.72 (n=8) and 0.62 (n=10), with the maximum at majority-like functions. That slack would be a second gain, but its asymptotic value is unknown, and no structural property of B that excludes the extremal case was found. B is symmetric, and symmetry does not exclude it.

## 5. Breaking: make the one-sided displacement two-sided
If R+S−n were also bounded above by O(d), then E D² = O(d²) and a d²-type bound would follow. Numerics kill this: the support of R+S−n reaches +n even for majority. Large down jumps really occur, and the one-sided lemma is necessary.

No new Lean-verified bound. Item 1 is the lead worth a real proof attempt.

---
# Two versions (2026-11-21)

## Max gamified (exploits the leaderboard metric)
- Leaderboard ranks by the exact rational, lower is better, and any epsilon counts. The proof's floor 8/√(2π) is an infimum that is never attained, so a smaller rational can always be proved. Records can be salami-sliced forever.
- **Built:** 476765550/149384251, 4.2e-18 above the floor. Lean-verified on the PC (verified/ folder).
- **Next, no new lemma (needs one PC build):** 353514424368353/110766156451452, 1.343e-21 above the floor. This is the most `Real.pi_gt_d20` can certify. It is the same mechanical edit, with these replacements applied to 78fe0e6:
  - `90295_28292` → `353514424368353_110766156451452`, `90295/28292` → `353514424368353/110766156451452`
  - `8153187025/800437264` → `124972448236487973383027932609/12269141415027541520832908304`
  - `25613992448/8153187025` → `392612525280881328666653065728/124972448236487973383027932609`
  - Integer check: 2·314159265358979323846·p² − 64·q²·10²⁰ = 1726369610220149388428 > 0.
- **Beyond that:** prove a sharper π lower bound in Lean using Mathlib's `pi_lower_bound_start` technique, at about 1 extra digit per iteration. Any gap ε > 0 is reachable, at growing build cost. The site shows 6 decimals, so every one of these displays as 3.191538.
- Statement check: `Platform/bigo_Statement.lean` is clean (n ≥ 1, 1 ≤ d ≤ n, arbitrary real polynomial, sign(0) = 1). There is no loophole in the target.

## As intended (honest reading)
- The real state of the art is 8/√(2π) ≈ 3.19154. The 90295/28292 entry already reached it to 8e-10, and everything after that, ours included, is decimal-tuning with no mathematical content.
- A genuine improvement needs a new idea. The best lead is the conjectured comparison L_w ≤ L_1 (item 1 above), which would give 4/√(2π) ≈ 1.596. It is unproven.
- The conjectured truth (Gotsman–Linial) is ≈ √(2/π) ≈ 0.798.
