# One-sample matroid prophet inequality: scalar-slack improvement

**Result (claimed, not yet independently reviewed):** C = 5.1165809143775089·10⁻¹⁰,
exact rational in `certify_output.txt`. That is +0.0322 % over the current board best
(darkhipo, 5.1149356887949947·10⁻¹⁰) and +0.178 % over Chen's C₁₄₁.

## Difficulty: hard (for a material gain); easy only for epsilon gains

The bound is C = (1−t)β²·t·s(B)/(5K) with t = 23/2¹⁸, K ≈ 178, s ≈ 0.0053. The tiny
size comes from the structure (mask rate t, the 1/K charge, the 1/5 phase loss), not
from loose arithmetic. Every row since Oct 11 has been re-tuning the same scalar chain,
which is now nearly saturated. A float optimisation that also frees the algorithm
constants (κ, ρ, h, t) tops out near 5.1167·10⁻¹⁰. Going meaningfully higher (2× or
more) needs a new structural argument in the fixed-vector analysis of OpenAI/Shea.

## What changed (algorithm unchanged: κ=164, ρ=93/256, h=3/4, t=23/2¹⁸, θ=261/256, L=256)

1. **Tilt (3) checked directly.** The incumbents bound p^(−1/4) < 4/3 (actual value
   ≈ 1.2878). We use q₀ = 12881/10000 with q₀⁴p > 1, which lets the generator tilt `a` be
   smaller.
2. **Exact logs in the tail bound (Chen §6).** The paper bounds
   log M* = n·log(1+a) + y·log(1 + X/(1+a)) + 2y·log(1+v) using log(1+x) ≤ x and 1/p ≤ 1/ρ.
   We keep the exact expression and use rigorous rational upper bounds on each log, so
   `a/d` in ε becomes `log(1+a)/d` and bY becomes the log expression. The rest of the
   argument only uses E[e_err | H] ≤ (log M* + 1)/d, so nothing downstream changes.
   This is the one place the written proof text changes, and it is a one-line tightening.
3. **Re-tuned analysis constants** (μ, ν are real coefficients in the error charge
   e_err, not restricted to a 1/8 grid): μ = 6705/512, ν = 1801/128, v = 1/622,
   a = 148016971/125000000000, b = 257703833/1000000000000,
   d = 1012424185728961/10¹⁵ (< rigorous lower bound of −ln p).

Gain split: items 1+3 give about +0.008 %, item 2 gives about +0.024 %.

## Final push (Nov 20): Variant A is at its ceiling; Variant B goes further

- **Variant A (recommended to submit), algorithm unchanged:** C = 5.1165809143775·10⁻¹⁰.
  A float optimum over all analysis constants gives 5.1165811·10⁻¹⁰, so this certificate
  sits at the ceiling of the same-algorithm chain.
- **Variant B (optional, larger claim surface):** C = 5.1179354903163·10⁻¹⁰, which is
  +0.059 % over darkhipo. It also changes three mask rates of the algorithm:
  ρ = 745/2048, h = 1545/2048, t = 373/2²², with κ, θ, L unchanged. The seed budget
  becomes 67|E|+31 bits instead of 47|E|+27. All scalar conditions (3)–(4) pass exactly. The risk:
  the structural argument is written for symbolic ρ, h, t, but nobody has re-checked
  it at other values. darkhipo declined a similar κ change for that reason.
  Run `python3 certify.py --variant-b --fraction`. Output: `certify_output_variant_b.txt`.

## Combined with q's fine phase grid (Nov 20, after q's work log)

q's Variant R swaps the phase grid θ = 261/256, L = 256 (so L(θ−1) = 5) for
L = 2¹⁶ phases with L(θ−1) ≈ 4.95. That cuts the 1/(L(θ−1)) rounding loss toward
1/ln B. Stacking it with items 1–3 above, plus re-tuned ρ, h, t, gives:

| Version | C | vs board rank 1 |
|---|---|---|
| L = 2¹⁶ (`certify_combined.py`) | 5.1677088608·10⁻¹⁰ | +1.0317 % |
| L = 2²⁴ (`certify_combined.py --L24`) | 5.1679026178·10⁻¹⁰ | +1.0355 % |

Parameters (L = 2¹⁶): κ = 164, ρ = 23835/2¹⁶, h = 49459/2¹⁶, t = 1491/2²⁴,
L(θ−1) = 9867/2000, μ = 1679/128, ν = 7211/512, v = 1000/624979. a, b and d are
computed and printed by the script. The L = 2²⁴ run bounds B from below through rigorous
logs, because the exact power is too large. Both pass all 15 exact checks.

**Discrepancy to resolve before submitting either set:** using Chen's formulas, which this
code reproduces digit for digit (C₁₄₁), q's Variant R parameters evaluate to
5.16626·10⁻¹⁰, not the 5.16775·10⁻¹⁰ in q's log. q's shuffler best (5.16794·10⁻¹⁰) is
also above the ceiling of the formula as reproduced here. q's `certify.py` probably uses a
slightly different (or extra-tightened) chain, and it should be compared line by line
against Chen §1 and App. A.

## Checking

`python3 certify.py --fraction` (stdlib only, under a second). It first reproduces
Chen's published C₁₄₁ exactly from the incumbent formulas and darkhipo's C(B), then
checks every scalar condition of (3)–(4) at the new constants as exact rational
inequalities, and prints the exact numerator/denominator.

Not checked: the universal matroid argument itself (inherited from OpenAI, Shea, Chen;
no Lean proof exists for any row).

## Reconciled with q's checker; final value (Nov 20, late)

q's `certify.py` is sound, and its chain is slightly tighter than the one above. It uses
α₁ directly in the log M* bound, where Chen bounds it by a/3, and that accounts for the
whole gap between the two checkers. With q's chain and the phase grid refined from
L = 2¹⁶ to L = 2²⁴ (24 phase bits instead of 16):

**C = 5.168130984950750·10⁻¹⁰**, which is +1.0400 % over the board's best and +0.0037 % over
q's shuffler best. Run `python3 certify_final.py --fraction`, which passes 11 exact checks
(output in `certify_final_output.txt`). Going to L = 2³² adds only about 1.5·10⁻⁷ relative,
so this is the ceiling of the chain.

## Five-idea round (Nov 21)

- **Novel, decoupling the max-branch coin (gain):** Chen's max-branch probability is t,
  the same as the C/T mask rate. Inequality (30) only needs τ/4 ≥ (1−τ)·t·(γκ+a₀)/K, and
  the smallest such τ is about 0.34·t. With τ = 32399/2³⁰ (30 shared branch bits), the
  bound is **C = 5.1684343637·10⁻¹⁰** (+1.0459 % over the board). See
  `certify_final_tau.py`; all exact checks pass. It is an algorithm change, but a
  one-line one.
- **Crazy, drop the max branch or use one huge phase:** dead. Without the branch, the
  −t(γκ+a₀)/K·m* term (γκ+a₀ ≈ 15) swamps the βts/K·W term (s ≈ 0.005). With L = 1,
  the rounding loss becomes B−1.
- **Borrowed, sharper tail integration (large deviations) and equidistribution for
  the rounding:** no gain. ∫min(1, M e^(−λx)) dx is exact for that tail shape, and the
  phase-rounding bound βx/(L(θ−1)) is tight at the worst position x → θ^(k+1).
- **Reverse, start from a 2× target:** s/(1−h) = 0.0211 is a small difference:
  ρ/4 = 0.0909 minus losses of 0.0698. The largest loss is the activation charge
  μρ/(κh) = 0.0385, followed by Kt/h = 0.0210. Halving the activation charge alone would
  roughly double C. That needs a new tilt or overlap argument, because μ is pinned by
  the tilt p^μ ≈ a·v/(3ρ).
- **Breaking, non-uniform phase law:** dead. Minimax over cyclic shifts makes the
  uniform phase optimal for worst-case rounding.

## Max gamified vs as intended (Nov 21)

| Version | What may change | C | vs board |
|---|---|---|---|
| **As intended** (`certify_as_intended.py`) | Nothing in the algorithm. Only proof-internal steps are tightened (exact logs, α₁ direct, 1/p, d → λ) and the analysis constants are re-optimised | 5.1168092217·10⁻¹⁰ | +0.0366 % |
| **Max gamified** (`certify_final_tau.py`) | Every free number: mask rates ρ, h, t, phase grid L = 2²⁴ with L(θ−1) ≈ 4.933, decoupled max-branch coin τ, more seed bits | 5.1684343637·10⁻¹⁰ | +1.0459 % |

The max-gamified value sits at its ceiling. The float optimum with L = 2³² and κ re-searched
over 163–165 is 5.1684351·10⁻¹⁰, which differs by 1.5·10⁻⁷ relative. Almost all of the
+1 % comes from the finer phase grid, which replaces the factor 1/5 with roughly 1/ln B.
That is a genuine re-instantiation of the same construction, not a different theorem.
