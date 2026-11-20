# bigospeedrun results

Claimed improvements to bounds listed on https://bigospeedrun.com. They aren't Lean Verified. Most of them tighten the parameters in another author's published construction, and that construction's proof is the original authors' work. Sidorenko and the unit-distance grid are exceptions, because they add new arguments: a rank lemma in one counting step, and a 6×5 grid in place of 8×4. Each folder credits them and says what was and wasn't checked.

| Problem | New bound | Previous listed bound | Builds on | Evidence |
|---|---|---|---|---|
| Binary polynomial multiplication over F2 | kappa = 1/1300 | 1/1302 | Csizmadia, arpcs/finite-field-polynomial-multiplication v0.2.1 | `binary-polymul/` (100-digit moment check) |
| Van der Waerden lower bound | c = 31/250 | 1/9 | DaysSky, commit 987c96c | `van-der-waerden/` (parameter inequalities) |
| Catalan's constant, irrationality measure | mu(G) <= 269.787 | 270 | S. Litsey, slitsey/catalan-irrationality-measure @ 3797a70c | `catalan/` (Lean patch, not built yet) |
| One-sample matroid prophet inequality | C = 5.11658e-10 | 5.11494e-10 | Chen; darkhipo | `matroid-prophet/` (exact-rational `certify.py`, PASS) |
| Sidorenko nondirect residual constant | C <= 45 | 189 | rohanarun/sidorenko-template-refinements @ 5ca68cb | `sidorenko/` (new rank lemma, exact-rational audit) |
| Unit-distance obstruction, final grid size | N·j <= 30 (6×5) | 32 (8×4) | Rohan Arun; OpenAI power-saving paper @ fd4aeeb2 | `unit-distance-grid/` (proof draft + check_grid.py; same imported lemmas) |
| Heilbronn triangle problem (eta) | 1/40,251,724 (~2.484e-8) | ~1.98e-8 | Blinov, littleBro/heilbronn-triangle-bounds PR #13 @ e29a291 | `heilbronn/` (smaller 3-AP-free packing + verify scripts) |
| Subset Sum threshold T | 0.4875739649 | 0.4875755 | Jennifer Voitle, jv1000/subset-sum @ 38e5335 | `subset-sum/` (tightened slack constants + certify scripts) |
| Contingency tables (FPRAS repair coefficient) | 20,000·d^17 | 80,000·d^17 | Upstream Math115 PhysicalRepairRefinement development | `contingency-tables/` (Lean refinement + chk.py) |

## Caveats
- None of these is independently reviewed. Each rests on the upstream proof it modifies.
- Van der Waerden: the site already says every c < 1/8 is reachable by this method, and the change wasn't run through DaysSky's audit_math.py.
- Catalan: the Lean patch hasn't been built.
