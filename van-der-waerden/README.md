# Van der Waerden lower bound: notes (2026-11-20)

Problem: largest c with W_r(k) > k^{c k floor(log2 r)}, k large, uniform in r.
Board top: c = 1/9 (DaysSky, Claimed, Oct 12). Only Lean Verified row: c = 1/100000 (OpenAI).
Page note: "The current region allows every fixed c < 1/8; 1/8 is not an attained value."

## How 1/9 arises (DaysSky commit 987c96c, from the commit message and README diff)
Constraints: 2a < m < 1, b < a, a + b < 1, outer margin (1/2 - eps)(1 - eps_r)(1 - delta) > gamma,
rich condition c < gamma*b/2. So gamma < 1/2, b < 1/2, which gives c < 1/8.
Their parameters: a = 49/100, m = 99/100, b = gamma = 97/200, eps = eps_r = delta = 1/200 -> gamma*b/2 = 0.1176; they report c = 1/9.

## Easy fix: parameter tuning only (same lemmas)
eps = eps_r = delta = 1/2000, a = 4995/10000, m = 9995/10000, b = 499/1000, gamma = 4989/10000:
- outer margin = 0.4990006 > gamma
- m - 2a = 1/2000, 1 - m = 1/2000, a - b = 1/2000, 1 - a - b = 3/2000
- gamma*b/2 = 0.1244756 > c = 31/250 = 0.124 (margin 9511/20000000)
So c = 31/250 is admitted by the stated inequalities. Any c < 1/8 works the same way.

Caveats:
- Checked against the inequalities as quoted in the commit, NOT against audit_math.py
  (GitHub rate-limited every fetch). Its LP may carry an extra constraint.
- Relies on DaysSky's unreviewed lemmas ("written only"). Adds no new math; the site already
  says the region covers every c < 1/8. Whether the site would rank it is uncertain.

## Beyond 1/8
Needs gamma > 1/2 (beat the outer color margin), b > 1/2 (impossible with these keys since b < a < 1/2),
or a new idea for rich progressions without repeated keys. Hard.

## Final push (2026-11-20, second round)
The audit script's short-period checks were read this time (sp_margins / sp_valid, 16 margins),
and are re-implemented exactly in sp_check.py next to this file.

Final proposal, c = 1249/10000 = 0.1249:
a = 49999/100000, m = 99999/100000, b = 24999/50000, gamma = 49997/100000,
eps = eps_reg = delta = 1/100000, delta_s = 1/2.
- All 16 short-period margins are positive (gamma*b/2 = 0.1249875 > 0.1249).
- DaysSky's own 1/9 parameters also pass (sanity check).
- All five rejection controls (b=a, m=2a, c=gamma*b/2, gamma at bound, c=1/8) are rejected.
- c = 0.12499 fails with these margins. Going further only means smaller margins; 1/8 itself is unreachable.
Same caveats as above: parameter tuning only, on unreviewed lemmas.
