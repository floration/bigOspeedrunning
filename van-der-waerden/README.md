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

## Five-ideas round (2026-11-21). Heuristic only, no new certified bound
Reading of the bottleneck: N = k^{c k log2 r}, a rich progression has probability about k^{-gamma*b*k*log2 r},
and a union bound over the ~N^2 progressions in [N] gives 2c < gamma*b. The "2" is the progression count.
1. Novel: replace the union bound on rich events by the Lovasz local lemma (each event then pays ~kN, not N^2),
   which would turn 2c < gamma*b into c < gamma*b, i.e. c < 1/4. Obstacle: rich events are driven by shared random
   keys, so the dependency degree may itself be ~N^2. Best lead; needs short-period-runs-proof.md to test.
2. Crazy: push gamma past 1/2 with an unbalanced or multi-colour outer colouring. Dead: gamma is the minority-colour
   fraction, which is at most 1/2 for two colours, and less for more colours.
3. Borrowed (coding theory): treat the key word as a code. b < a < 1/2 is a rate limit from 2a < m < 1 (again a
   pair count). A Gilbert-Varshamov style expurgation (delete bad keys, don't union-bound them) could relax 2a < m
   to a < m, allowing b up to ~1. Unchecked; same blocker as idea 1.
4. Reverse: from the target down. Nothing known caps c at 1/8 or even 1 (upper bounds on W are tower-type), so 1/8
   is a method barrier only. Getting 1/4 needs exactly one factor-2 saving (idea 1 or 3); getting 1/2 needs both.
5. Breaking: drop the floor(log2 r) binary-digit encoding and colour with r colours directly. For r = 2^j it gives the
   same exponent; for r between powers of 2 it only helps the floor, not c. No gain under this scoring.

## Two versions (2026-11-21)
MAX GAMIFIED: c = 1/8 - 10^-11 = 0.12499999999.
  a = 1/2 - t, m = 1 - t, b = 1/2 - 2t, gamma = 1/2 - 4t, eps = eps_reg = delta = t = 10^-12, delta_s = 1/2.
  Passes all 16 short-period checks in sp_check.py (margin gamma*b/2 - c = 8.5e-12). Any c < 1/8 can be dialled in
  the same way; 1/8 itself is rejected by the script.
AS INTENDED: no new result. The site already credits DaysSky's region as "every fixed c < 1/8"; picking a larger c
  inside it is not new math and still rests on DaysSky's unreviewed lemmas. Honest standing: 1/9 Claimed (DaysSky),
  1/100000 Lean Verified (OpenAI). A real gain needs a new argument, e.g. the local-lemma idea (would give < 1/4).
