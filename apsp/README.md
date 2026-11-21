# APSP (bigospeedrun.com/apsp): difficulty and easy improvements

Checked 2026-11-20.

## Leaderboard right now
- Best Claimed: 2.9929479187094 (Wharton). It retunes the parameters of shreshth-s's aligned-cache construction. The word-RAM program is not formalized.
- Best Lean Verified: 2.9955607647814 (fringewidth, Oct 20). It retunes θ and σ in Li Xuanji's complete Lean proof, with c = 20.
- The site states no minimum improvement. To be Lean Verified, a result must match or beat the best Lean Verified entry and pass the bigospeedrun/verifier rebuild.

## Difficulty
- Real algorithmic progress (a new lemma that improves one of the four balanced costs): **hard**.
- Parameter tightening on the Claimed track: **easy, but it is already exhausted** (see A).
- Making c fractional on the Lean track: **medium** (see B). This is the one improvement worth pursuing.

## A. Claimed track: the remaining slack is about 9e-14
The construction's limiting optimum is 3 − δ* = 2.99294791870930934672 (optimization.txt in the Wharton repo). The current claim stops at δ = 0.0070520812906 and uses R = 10^12 stages.
I raised R to 10^24, used the stationary point to 36 digits, and set δ = 0.007052081290690653. The repo's own exact rational checker passes all 47 checks:

**O(n^2.992947918709309347)**, a gain of 9.07e-14 (files in `claimed-witness/`).

This is the ceiling of the construction. It is a trivial retune and would still only be Claimed.

## B. Lean track: making c fractional gains about 5e-8
In the verified proof, the exponent is max(3 − 2Γσ, 2 + (2B − ½)σ, 3 − (1 − 2q)σ). Here B = (c−1)·ln3/ln4, Γ = GammaOf c θ, and q = qOf θ. The three terms come from the `boxes`, `encodings` and `queries` bounds in Batch/OBound.lean. Balancing them gives α(c). At c = 20 this is 2.99556076477889, which matches the current record, so there is only about 2.5e-12 left at c = 20.
Integer c = 20 is the best integer. But the paper's machinery already uses L = ⌈c·m⌉ (`levelsOf c m`) for real c, and the tail and binomial lemmas (`tail_div_M_le`, `K_le_exp`, `rho_lt`) take a general c. The only place c = 20 is hard-coded is the batch program (`oL = 20*m`) and its constants.

| c | α(c) |
|---|---|
| 20 | 2.9955607647789 |
| 20.0778 (optimum) | 2.9955607132246 |

Expected result: about **2.99556071 to 2.995560714**, which beats the Lean Verified record by about 5e-8. That is roughly 40 times the last Lean step.
The work: change `oL` to ⌈(a/b)·m⌉ in the word-RAM program (the same ceil-div pattern `oT` already uses), retune θ and σ, re-prove the log enclosures in Numbers.lean for the new rationals, update every constant in the 17 files the earlier retunes touched plus the `oL`/`N₀` uses, then rebuild and verify. Not yet attempted. The scan script is `lean_track_c_scan.py`.
