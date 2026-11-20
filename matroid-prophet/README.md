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

## Checking

`python3 certify.py --fraction` (stdlib only, under a second). It first reproduces
Chen's published C₁₄₁ exactly from the incumbent formulas and darkhipo's C(B), then
checks every scalar condition of (3)–(4) at the new constants as exact rational
inequalities, and prints the exact numerator/denominator.

Not checked: the universal matroid argument itself (inherited from OpenAI, Shea, Chen;
no Lean proof exists for any row).
