# bigospeedrun results

Claimed improvements to bounds listed on https://bigospeedrun.com. They aren't Lean Verified. Most of them tighten the parameters in another author's published construction, and that construction's proof is the original authors' work. Sidorenko and the unit-distance grid are exceptions, because they add new arguments: a rank lemma in one counting step, and a 29-edge 6×5 grid in place of 8×4. Each folder credits them and says what was and wasn't checked.

| Problem | New bound | Previous listed bound | Builds on | Evidence |
|---|---|---|---|---|
| Binary polynomial multiplication over F2 | kappa = 2/2599 (1/1299.5) | 1/1302 | Csizmadia, arpcs/finite-field-polynomial-multiplication v0.2.1 | `binary-polymul/` (moment checks, incl. interval check) |
| Van der Waerden lower bound | c = 1249/10000 (gamed: parameter tuning only; not in the as-intended submission) | 1/9 | DaysSky, commit 987c96c | `van-der-waerden/` (parameter inequalities + sp_check.py) |
| Catalan's constant, irrationality measure | mu(G) <= 269.78167 (build pending; 269.78667 patch also included) | 270 | S. Litsey, slitsey/catalan-irrationality-measure @ 3797a70c | `catalan/` (Lean patch, not built yet) |
| One-sample matroid prophet inequality | **As intended: C = 5.116809e-10** (`certify_as_intended.py`). Gamed: 5.168434e-10 (`certify_final_tau.py`, re-tunes the algorithm's free numbers) | 5.11494e-10 | Chen; darkhipo | `matroid-prophet/` (exact-rational `certify_final_tau.py`, PASS) |
| Sidorenko nondirect residual constant | C <= 33 | 189 | rohanarun/sidorenko-template-refinements @ 5ca68cb | `sidorenko/` (new rank lemma, exact-rational audit) |
| Unit-distance obstruction, selected edges | **As intended: 30** (complete 6×5 grid). Gamed: 29 (6×5 minus one edge; not of the form N·j) | 32 (8×4) | Rohan Arun; OpenAI power-saving paper @ fd4aeeb2 | `unit-distance-grid/` (proof draft + check_grid.py, check_29.py; same imported lemmas) |
| Heilbronn triangle problem (eta) | 1/39,569,962 (~2.527e-8) | ~1.98e-8 | Blinov, littleBro/heilbronn-triangle-bounds PR #13 @ e29a291 | `heilbronn/` (smaller 3-AP-free packing + verify scripts) |
| Subset Sum threshold T | 0.4875739537 | 0.4875755 | Jennifer Voitle, jv1000/subset-sum @ 38e5335 | `subset-sum/` (tightened slack constants + certify scripts) |
| Contingency tables (FPRAS repair coefficient) | 12,062·d^17 (both Lean files compile); 11,232·d^17 candidate, build pending | 80,000·d^17 | Upstream Math115 PhysicalRepairRefinement development | `contingency-tables/` (Lean refinement + chk.py) |
| Directed SSSP gap-fill rows (gamed: not in the as-intended submission) | e.g. n log^{15/8} n at m <= n log^{7/8} n; n log^3 n at m <= n log^2 n; n^{3/2} log n at m <= n^{3/2} | n log^2 n / n^2 / n^2 (Lean Verified) | darkhipo/sssp-nlogn @ 1129aca | `directed-sssp/` (Lean, builds with no sorry; plus a paper-only O(m log^{1/6} n) extension of C-HD) |
| Integer multiplication (kappa, conditional) | kappa >= 0.00387992804606 | 0.00387992803556 (#7830) | CrocSwap/integer-mult-bounds P104 mixed-cutoff BIT supplier (#7830) | `integer-multiplication/` (verify.py replay + independent review) |
| Haldane gap (spin-one Heisenberg chain) | gamma_L > 0.151707 for L >= 24 | 0.1515 | amachino/haldane-gap-refinement v1.7 @ 15909bdc | `haldane-gap/` (sharper tail invariant, exact receipt) |

## Caveats
- "Gamed" marks values that stretch how the metric is read (free parameters, partial edge counts, gap-fill densities). They're kept here for reference, but the as-intended values are the ones claimed.
- None of these is independently reviewed. Each rests on the upstream proof it modifies.
- Van der Waerden: the site already says every c < 1/8 is reachable by this method, and the change wasn't run through DaysSky's audit_math.py.
- Catalan: the Lean patch hasn't been built.
