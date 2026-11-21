/-
Copyright (c) 2026 Anthropic, PBC. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
SPDX-License-Identifier: Apache-2.0
Parameter and numerical refinements (c) 2026 Joshua Wharton, QFEX.
Author of modifications: Joshua Wharton <joshua@qfex.com>
Fractional c = 1807/90 refinement, 2026.
-/
module

public import Submission.ThreeSumApsp.Pruned.Costs
public import Mathlib.Analysis.SpecialFunctions.Log.Deriv

/-!
# Refined numbers for `c = 1807/90`, `θ = 290417 / 2568962`

The logarithms are proved from forty terms of the positive atanh series, with
Mathlib's geometric remainder bound. Python selected the rational endpoints;
it supplies no assumptions to Lean. The public bounds are
`Γ > 0.066301113347407`, `q < 0.433698886652977`, `(1717/90) ln 3 / ln 4 < 15.118781187434585`
and `κ < 2.9`.
-/

@[expose] public section

set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option exponentiation.threshold 2048

namespace ThreeSumApsp
open scoped BigOperators

private theorem refinedAtanhLogBounds (z : ℝ) (hz0 : 0 ≤ z) (hz1 : z < 1) (n : ℕ) :
    2 * (∑ i ∈ Finset.range n, z ^ (2 * i + 1) / (2 * (i : ℝ) + 1))
        ≤ Real.log ((1 + z) / (1 - z)) ∧
    Real.log ((1 + z) / (1 - z)) ≤
      2 * ((∑ i ∈ Finset.range n, z ^ (2 * i + 1) / (2 * (i : ℝ) + 1)) +
        z ^ (2 * n + 1) / (1 - z ^ 2)) := by
  have hlo := Real.sum_range_le_log_div hz0 hz1 n
  have hhi := Real.log_div_le_sum_range_add hz0 hz1 n
  constructor <;> linarith

private theorem fineLogTwo :
    (693147180559945309417232 / 10^24 : ℝ) < Real.log (2 : ℝ) ∧
    Real.log (2 : ℝ) < (693147180559945309417233 / 10^24 : ℝ) := by
  have h := refinedAtanhLogBounds (1 / 3 : ℝ) (by norm_num) (by norm_num) 40
  norm_num [Finset.sum_range_succ] at h ⊢
  constructor <;> linarith [h.1, h.2]

private theorem fineLogThreeHalf :
    (405465108108164381978013 / 10^24 : ℝ) < Real.log (3 / 2 : ℝ) ∧
    Real.log (3 / 2 : ℝ) < (405465108108164381978014 / 10^24 : ℝ) := by
  have h := refinedAtanhLogBounds (1 / 5 : ℝ) (by norm_num) (by norm_num) 40
  norm_num [Finset.sum_range_succ] at h ⊢
  constructor <;> linarith [h.1, h.2]

private theorem fineLogCompTwice :
    (573182335651552332019232 / 10^24 : ℝ) < Real.log (2278545 / 1284481 : ℝ) ∧
    Real.log (2278545 / 1284481 : ℝ) < (573182335651552332019233 / 10^24 : ℝ) := by
  have h := refinedAtanhLogBounds (497032 / 1781513 : ℝ) (by norm_num) (by norm_num) 40
  norm_num [Finset.sum_range_succ] at h ⊢
  constructor <;> linarith [h.1, h.2]

private theorem fineLogNearOne :
    (5908170153809070955895 / 10^24 : ℝ) < Real.log (2218522642 / 2205453877 : ℝ) ∧
    Real.log (2218522642 / 2205453877 : ℝ) < (5908170153809070955896 / 10^24 : ℝ) := by
  have h := refinedAtanhLogBounds (13068765 / 4423976519 : ℝ) (by norm_num) (by norm_num) 40
  norm_num [Finset.sum_range_succ] at h ⊢
  constructor <;> linarith [h.1, h.2]

private theorem fineLogTheta16 :
    (592649338169207313777485 / 10^24 : ℝ) < Real.log (2323336 / 1284481 : ℝ) ∧
    Real.log (2323336 / 1284481 : ℝ) < (592649338169207313777486 / 10^24 : ℝ) := by
  have h := refinedAtanhLogBounds (1038855 / 3607817 : ℝ) (by norm_num) (by norm_num) 40
  norm_num [Finset.sum_range_succ] at h ⊢
  constructor <;> linarith [h.1, h.2]

private theorem fineLogHighOver16 :
    (181843638481238297612218 / 10^24 : ℝ) < Real.log (1109261321 / 924826320 : ℝ) ∧
    Real.log (1109261321 / 924826320 : ℝ) < (181843638481238297612219 / 10^24 : ℝ) := by
  have h := refinedAtanhLogBounds (184435001 / 2034087641 : ℝ) (by norm_num) (by norm_num) 40
  norm_num [Finset.sum_range_succ] at h ⊢
  constructor <;> linarith [h.1, h.2]

private theorem fineLogCOver16 :
    (227024898022182188764861 / 10^24 : ℝ) < Real.log (1807 / 1440 : ℝ) ∧
    Real.log (1807 / 1440 : ℝ) < (227024898022182188764862 / 10^24 : ℝ) := by
  have h := refinedAtanhLogBounds (367 / 3247 : ℝ) (by norm_num) (by norm_num) 40
  norm_num [Finset.sum_range_succ] at h ⊢
  constructor <;> linarith [h.1, h.2]

private theorem fineLogCm1Over16 :
    (175935468327429226656322 / 10^24 : ℝ) < Real.log (1717 / 1440 : ℝ) ∧
    Real.log (1717 / 1440 : ℝ) < (175935468327429226656323 / 10^24 : ℝ) := by
  have h := refinedAtanhLogBounds (277 / 3157 : ℝ) (by norm_num) (by norm_num) 40
  norm_num [Finset.sum_range_succ] at h ⊢
  constructor <;> linarith [h.1, h.2]

private theorem refinedLogSixteen : Real.log 16 = 4 * Real.log 2 := by
  convert Real.log_pow (2 : ℝ) 4 using 1 <;> norm_num

private lemma logB_a : Real.log (2278545 / 2568962 : ℝ) ∈ Set.Icc (-11996484490839297740 / 10^20 : ℝ) (-11996484490839297739 / 10^20 : ℝ) := by
  have hr := Real.log_mul (by norm_num : (2 : ℝ) ≠ 0)
    (by norm_num : (2278545 / 2568962 : ℝ) ≠ 0)
  norm_num at hr
  have h1 := fineLogCompTwice
  have h2 := fineLogTwo
  constructor <;> linarith [h1.1, h1.2, h2.1, h2.2]

private lemma logB_b : Real.log (2218522642 / 2205453877 : ℝ) ∈ Set.Icc (590817015380907095 / 10^20 : ℝ) (590817015380907096 / 10^20 : ℝ) := by
  have h1 := fineLogNearOne
  constructor <;> linarith [h1.1, h1.2]

private lemma logB_c : Real.log (1109261321 / 57801645 : ℝ) ∈ Set.Icc (295443236072101953528 / 10^20 : ℝ) (295443236072101953529 / 10^20 : ℝ) := by
  have hr := Real.log_mul (by norm_num : (16 : ℝ) ≠ 0)
    (by norm_num : (1109261321 / 924826320 : ℝ) ≠ 0)
  rw [refinedLogSixteen] at hr
  norm_num at hr
  have h1 := fineLogHighOver16
  have h2 := fineLogTwo
  constructor <;> linarith [h1.1, h1.2, h2.1, h2.2]

private lemma logB_3 : Real.log (3 : ℝ) ∈ Set.Icc (109861228866810969139 / 10^20 : ℝ) (109861228866810969140 / 10^20 : ℝ) := by
  have hr := Real.log_mul (by norm_num : (2 : ℝ) ≠ 0)
    (by norm_num : (3 / 2 : ℝ) ≠ 0)
  norm_num at hr
  have h1 := fineLogThreeHalf
  have h2 := fineLogTwo
  constructor <;> linarith [h1.1, h1.2, h2.1, h2.2]

private lemma logB_theta : Real.log (290417 / 2568962 : ℝ) ∈ Set.Icc (-217993938407057392390 / 10^20 : ℝ) (-217993938407057392389 / 10^20 : ℝ) := by
  have hr := Real.log_mul (by norm_num : (16 : ℝ) ≠ 0)
    (by norm_num : (290417 / 2568962 : ℝ) ≠ 0)
  rw [refinedLogSixteen] at hr
  norm_num at hr
  have h1 := fineLogTheta16
  have h2 := fineLogTwo
  constructor <;> linarith [h1.1, h1.2, h2.1, h2.2]

private lemma logB_cc : Real.log (1807 / 90 : ℝ) ∈ Set.Icc (299961362026196342643 / 10^20 : ℝ) (299961362026196342644 / 10^20 : ℝ) := by
  have hr := Real.log_mul (by norm_num : (16 : ℝ) ≠ 0)
    (by norm_num : (1807 / 1440 : ℝ) ≠ 0)
  rw [refinedLogSixteen] at hr
  norm_num at hr
  have h1 := fineLogCOver16
  have h2 := fineLogTwo
  constructor <;> linarith [h1.1, h1.2, h2.1, h2.2]

private lemma logB_cm1 : Real.log (1717 / 90 : ℝ) ∈ Set.Icc (294852419056721046432 / 10^20 : ℝ) (294852419056721046433 / 10^20 : ℝ) := by
  have hr := Real.log_mul (by norm_num : (16 : ℝ) ≠ 0)
    (by norm_num : (1717 / 1440 : ℝ) ≠ 0)
  rw [refinedLogSixteen] at hr
  norm_num at hr
  have h1 := fineLogCm1Over16
  have h2 := fineLogTwo
  constructor <;> linarith [h1.1, h1.2, h2.1, h2.2]

private lemma logB_9 : Real.log (9 : ℝ) ∈ Set.Icc (219722457733621938278 / 10^20 : ℝ) (219722457733621938280 / 10^20 : ℝ) := by
  rw [Real.log_nine]
  have h := logB_3
  constructor <;> linarith [h.1, h.2]

private lemma logB_4 : Real.log (4 : ℝ) ∈ Set.Icc (138629436111989061883 / 10^20 : ℝ) (138629436111989061884 / 10^20 : ℝ) := by
  rw [Real.log_four]
  have h := fineLogTwo
  constructor <;> linarith [h.1, h.2]

/-- Cancellation of the large entropy terms, exactly at the new rational point. -/
private lemma GammaOf_B_eq :
    GammaOf (1807 / 90) (290417 / 2568962) * Real.log 4
      = 2278545 / 2568962 * Real.log (2278545 / 2568962)
        + 1717 / 90 * Real.log (2218522642 / 2205453877)
        + 290417 / 2568962 * Real.log (1109261321 / 57801645)
        - 290417 / 2568962 * Real.log 9 := by
  rw [GammaOf_mul_log_four (by norm_num) (by norm_num) (by norm_num)]
  have h1 : (1 : ℝ) - 290417 / 2568962 = 2278545 / 2568962 := by norm_num
  have h2 : (1807 / 90 : ℝ) - 1 + 290417 / 2568962 = 1109261321 / 57801645 := by norm_num
  have h3 : (1807 / 90 : ℝ) - 1 = 1717 / 90 := by norm_num
  rw [h1, h2, h3, show (2218522642 / 2205453877 : ℝ) = (1109261321 / 57801645) / (1717 / 90) by
    norm_num, Real.log_div (x := 1109261321 / 57801645) (y := 1717 / 90) (by norm_num) (by norm_num)]
  ring

/-- The certified lower bound used for preprocessing boxes. -/
theorem GammaOf_B : (0.066301113347407 : ℝ) < GammaOf (1807 / 90) (290417 / 2568962) := by
  refine lt_of_mul_lt_mul_right ?_ log_four_pos.le
  rw [GammaOf_B_eq]
  have h1 := logB_a; have h2 := logB_b; have h3 := logB_c; have h4 := logB_9
  have h5 := logB_4
  simp only [Set.mem_Icc] at *
  linarith

/-- A coarse upper bound. -/
theorem GammaOf_B_lt : GammaOf (1807 / 90) (290417 / 2568962) < (0.0664 : ℝ) := by
  refine lt_of_mul_lt_mul_right ?_ log_four_pos.le
  rw [GammaOf_B_eq]
  have h1 := logB_a; have h2 := logB_b; have h3 := logB_c; have h4 := logB_9
  have h5 := logB_4
  simp only [Set.mem_Icc] at *
  linarith

theorem GammaOf_B_pos : 0 < GammaOf (1807 / 90) (290417 / 2568962) :=
  lt_trans (by norm_num) GammaOf_B

/-- The certified upper bound used for queries. -/
theorem qOf_B : qOf (290417 / 2568962) < (0.433698886652977 : ℝ) := by
  unfold qOf entropy
  rw [div_lt_iff₀ log_four_pos]
  have h1 := logB_theta; have h2 := logB_a; have h3 := logB_9; have h4 := logB_4
  norm_num only [show (1 : ℝ) - 290417 / 2568962 = 2278545 / 2568962 by norm_num]
  simp only [Set.mem_Icc] at *
  linarith

/-- The certified upper bound used for pruned encodings. -/
theorem bExp_B : 1717 / 90 * Real.log 3 / Real.log 4 < (15.118781187434585 : ℝ) := by
  rw [div_lt_iff₀ log_four_pos]
  have h3 := logB_3; have h5 := logB_4
  simp only [Set.mem_Icc] at *
  linarith

/-- The coarse binomial coefficient bound. -/
theorem kappa_B : (1807 / 90 : ℝ) * entropy (1 / (1807 / 90)) / Real.log 4 < (2.9 : ℝ) := by
  rw [div_lt_iff₀ log_four_pos, PrunedAux.mul_entropy_inv (by norm_num)]
  have h1 := logB_cc; have h2 := logB_cm1; have h5 := logB_4
  rw [show (1807 / 90 : ℝ) - 1 = 1717 / 90 by norm_num]
  simp only [Set.mem_Icc] at *
  linarith

end ThreeSumApsp
