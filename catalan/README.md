# Catalan's constant: μ(G) bound, assessment (2026-11-20)

Problem: https://bigospeedrun.com/other/catalan. Target (verifier `challenges/catalan/Statement.lean`):
`Bound r := 0 ≤ r ∧ ∀ s > r, eventually in b, ∀ a, b^(-s) < |G − a/b|`.

## State of play
- Best claimed: μ(G) ≤ 270, S. Litsey, repo `slitsey/catalan-irrationality-measure` (HEAD `3797a70c`, Lean v4.35.0-rc2).
  Not Lean Verified on the site: the verifier profile pins Lean v4.34.1 + Mathlib `d13f23b`, so the proof needs a toolchain backport
  (Litsey did this for 295 in verifier#187; that check ran as a multi-job chain, ~3 h Lean check alone).
- Other: Carreira 280.59 (not formalized).

## Two versions (2026-11-21)
| Version | μ(G) ≤ | What it does |
|---|---|---|
| **Max gamified** | **269.7816584** | [`mu-2697816584-gamified.patch`](mu-2697816584-gamified.patch): every free numeric knob pushed to the edge of what Lean can still certify. δ = 10⁻³⁰; η = 54.68846441 (3.6·10⁻⁹ under the ceiling set by Mathlib's 9-digit log 2 bounds); μ is the 7-decimal rational just above dρ/(η − 4dδ) = 269.78165832. Not built. |
| **As intended** | **269.78167** | [`mu-26978167.patch`](mu-26978167.patch): the same idea with round, comfortable margins (η = 54.688464, δ = 10⁻¹², μ = 269.78167). Rebuild queued on the PC. |
| Honest reading of the race | 270 → ~269.78 is bookkeeping | Neither version adds mathematics. Both only remove rounding and safety margins from Litsey's proof. A real improvement needs new certified estimates for ρ or η. |

The gap between the two versions is 1.2·10⁻⁵. Exact log 2 would gain a further 2·10⁻⁶ (ceiling 269.7816561), using a 10-digit log 2 lemma.

## Five-idea round (2026-11-21): 269.78667 → 269.78167
Patch [`mu-26978167.patch`](mu-26978167.patch) against `3797a70c` (supersedes the earlier two). Not yet built.
1. **Novel (audit the certified constants for unused safety margins):** `eta295 = … − 1/1000` carries a 0.001 margin that the
   gain inequality `η < 58²(T − log2/2) − gD` does not need (true slack 0.0010149). New `etaC = 54.688464` (margin 4.1·10⁻⁷ with
   Mathlib's 9-digit `log 2` bounds), new lemma `Count.WinCertGlue.etaC_lt_of_gain`, `δ = 10⁻¹²`, so μ = 26978167/100000. All
   `PayW'` inequalities rechecked in exact rationals (last margin 5·10⁻⁴).
2. **Crazy (change the design (58,9,3,5,3) or ζ = 3/4):** μ ≈ dρ/η moves with every certificate; regenerating them is days of
   certified computation. Not attempted.
3. **Borrowed (interval arithmetic: tighter log 2 bounds):** the only thing between η and its ceiling 54.6884649 is the log 2
   interval; even exact log 2 gains about 1·10⁻⁵. Not worth a change.
4. **Reverse (start from the obstruction):** the T4 cover needs only σ ≥ 0.338704, but `sigmaC = 0.33871`. Backing σ off to
   0.338704 would cut ρ by 3.5·10⁻⁴ and μ by about 3.4·10⁻⁴ (to ≈ 269.7813). σ feeds the polynomial-nonnegativity
   certificates in 38 files, so this needs a full rebuild to know if they still pass. Not applied.
5. **Breaking (break "degree ≤ 53N"):** μ is proportional to d = n0 − g0 = 53. A proof that the determinant has smaller degree
   in the constant would be the biggest lever, but nothing in the code suggests the bound is loose. Not attempted.
Floor for the current certificates (η at its ceiling, δ → 0): 53ρ/η_max = 269.78166.

## Final push (2026-11-20): 270 → 269.78667
The prime-window parameter `δ` (`delta296`, was 2.9·10⁻⁷) appears only in the payment inequalities `PayW'`, and every one of them
improves as `δ` shrinks. Setting `δ = 10⁻¹²` lowers the threshold `dρ/(η − 4dδ)` to 269.7866626, so μ = 26978667/100000 works
(margin in the last inequality: 4·10⁻⁴, exact rationals). Patch: [`mu-26978667.patch`](mu-26978667.patch) (supersedes the 269.787 one).
This is the floor for the current numbers: `dρ/η = 269.786662564`. Anything lower needs a new η or ρ.
Build check running on the user's computer (Remote Control), result pending.

## First pass: 270 → 269.787
`CatalanMeasure/GenD/Signed/RouteI/TerminalC.lean:1148` already proves `measure_of_data (μ : ℚ)` for every
rational `μ ∈ [269.787, 400]`. The criterion's last condition is `μ > dρ/(η − 4dδ) = 269.78696…`; the stated 270 is
just a round-up. `measure_270` (line 1164) instantiates it at 270.

Patch [`mu-269787.patch`](mu-269787.patch) (against `3797a70c`) adds to `Measure270.lean`:
- `catalan_irrationalityMeasure_269787`: `measure_of_data (269787/1000) ...` with the same data records.
- `catalan_upperBound_269787`: the race form (∀ s > 269.787), by rpow monotonicity.

**Not yet built.** The cloud container cannot download the Lean toolchain (GitHub release downloads are blocked by the
network policy), and a full build of this repo takes hours. Gain beyond 269.787 is < 0.0001 (would need re-proving
`pay_designC` at a lower threshold).

## Difficulty
- Claimed 269.787: easy (one-line instantiation; needs one build to confirm).
- Lean Verified below 528.23: medium. Port the 270 development to the v4.34.1 profile pin (as done for 295) and run the verifier chain.
- Real progress (e.g. < 260): hard. Needs a better design / sharper corank profile (η) or energy bound (ρ); each piece is a large
  certified computation in Lean.

## Build status (2026-11-21)
- 269.78667 (`mu-26978667.patch`): full Lean build passes, standard axioms only.
- 269.78167 and 269.7816584 (gamified): builds running.
