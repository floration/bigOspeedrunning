# Block sensitivity: profile-cycle experiments (2026-11-20)

- `model.py`: an exact Python port of the recurrences in `Def_SensitivityProfileCycle.lean` (prove2me/formalpedia, env 0df444a). It reproduces yousofy's 2.1308255794 record exactly: the 16-state constant recipe at K=14055 gives R = 3738277295413674 over 8 steps.
- `fast.py`: a float growth-rate evaluator. `search2.py`: simulated annealing over valid recipes.
- Results:
  - K=14055 parameters: annealing from the record recipe finds nothing better. The record recipe is a local optimum.
  - K=5591 parameters (cutoffs 21,29,35,41,47,52,57,63,68; source 19; degree 2795): every run with 16, 20 or 24 states levels off at about 2.12817. That is below the 14055 result.
  - Cutoff sensitivity at K=14055 (`sens.py`): each unit of source cutoff w is worth about 0.0003 in exponent. Ordinary cutoffs and t are worth almost nothing. Reaching 2.1399 inside this framework would need roughly 30 fewer units of cutoff, which isn't plausible.
- Conclusion: the profile-cycle framework is saturated near 2.131. The 2.1398 record comes from a much richer framework (the "ThreeBound" hybrid min-max analysis with marked labels and dominator families, checked with about 141 MB of certificate data). Going further needs new combinatorial ideas, not parameter tuning.

## Five-idea round (2026-11-21)
1. Novel, period-2 and period-3 recipe words at K=14055 (`idea1.py`): annealing returns to the constant recipe. Best is 2.1308256, no gain.
2. Crazy, alternating tournaments K=14055 and K=5591 by level (`ideas235.py`): 2.044 for A,B alternation and 2.128 for A,A,B. Both are worse than either graph alone.
3. Borrowed from random graph theory: cutoffs grow about 2.26 per doubling of K, fitted from 5591, 10007 and 14055. Scanning K from 10^3 to 10^8 peaks at K≈14k (2.1308). The existing choice is already optimal in this framework.
4. Reverse, from 2.15 back to the cutoffs: each unit of source cutoff is worth about 0.0003. 2.15 would need w below 0, which is impossible. This matches dmilosch's disproof.
5. Breaking, oriented graphs of density p<1 in place of tournaments (`fastp.py`, `idea5b.py`): the model gives 2.17 at p=0.8 and 2.33 at p=0.4. That's an artifact. As p goes to 0 the model's exponent grows without bound, which violates Huang's theorem (bs ≤ s^4). So the cost formulas depend on the tournament property and don't carry over.
Gamified: the exact-log form of the current construction, log(5591^4)/log(10121928) = 2.1398136583, about 8.3e-9 above 2.13981365 (draft Lean file in this folder, not compiled). The AchievesExponent and bs/s definitions are faithful, so there is no loophole.

## Submitted value: alpha = log(5591^4)/log(10121928) = 2.1398136583 (exact limit)
`Sol_reach_exact_log_5591_10121928.lean` is a solution for the prove2.me campaign block-sensitivity-vs-sensitivity. It compiles (Lean v4.33.1, Mathlib 0df444a) against verbatim stubs of the two imported Proved theorems, and the only `sorry` is in those stubs. Gamed: it's the exact limiting exponent of the existing construction, about 8.3e-9 above dmilosch's 2.13981365, not a new construction. Credit: yousofy with Codex for the seed construction (which keeps the OpenAI/math and Robin Kothari attributions), and dmilosch for the copied helper `achieves_of_seed_bounds`. New here: only the final ε/2 step.
