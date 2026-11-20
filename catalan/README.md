# Catalan's constant: μ(G) bound, assessment (2026-11-20)

Problem: https://bigospeedrun.com/other/catalan. Target (verifier `challenges/catalan/Statement.lean`):
`Bound r := 0 ≤ r ∧ ∀ s > r, eventually in b, ∀ a, b^(-s) < |G − a/b|`.

## State of play
- Best claimed: μ(G) ≤ 270, S. Litsey, repo `slitsey/catalan-irrationality-measure` (HEAD `3797a70c`, Lean v4.35.0-rc2).
  Not Lean Verified on the site: the verifier profile pins Lean v4.34.1 + Mathlib `d13f23b`, so the proof needs a toolchain backport
  (Litsey did this for 295 in verifier#187; that check ran as a multi-job chain, ~3 h Lean check alone).
- Other: Carreira 280.59 (not formalized).

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
