/-
Copyright (c) 2026 Anthropic, PBC. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
SPDX-License-Identifier: Apache-2.0
Parameter and numerical refinements (c) 2026 Joshua Wharton, QFEX.
Author of modifications: Joshua Wharton <joshua@qfex.com>
-/
module

public import Submission.ThreeSumApsp.Pruned.Costs
public import Mathlib.Analysis.SpecialFunctions.Log.Deriv

/-!
# Refined numbers for `c = 502/25`, `θ = 225677/1996332`

The logarithms are proved from forty terms of the positive atanh series, with
Mathlib's geometric remainder bound. Python selected the rational endpoints;
it supplies no assumptions to Lean. The public bounds are
`Γ > 0.0663089654688`, `q < 0.4336910345308`, and `(477/25) ln 3 / ln 4 < 15.12054225688`.
The coarse `κ < 2.9` certificate retains ample slack.

This module refines the certificate by Hrishik Sai Bojnal (fringewidth), built
on Li Xuanji's deterministic batched APSP proof and the Anthropic development;
the fractional tensor depth `c = 502/25` replaces the integer depth `c = 20`.
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
    (573185218465981181272841 / 10^24 : ℝ) < Real.log (1770655 / 998166 : ℝ) ∧
    Real.log (1770655 / 998166 : ℝ) < (573185218465981181272842 / 10^24 : ℝ) := by
  have h := refinedAtanhLogBounds (772489 / 2768821 : ℝ) (by norm_num) (by norm_num) 40
  norm_num [Finset.sum_range_succ] at h ⊢
  constructor <;> linarith [h.1, h.2]

private theorem fineLogNearOne :
    (5907350844420586176246 / 10^24 : ℝ) < Real.log (957892289 / 952250364 : ℝ) ∧
    Real.log (957892289 / 952250364 : ℝ) < (5907350844420586176247 / 10^24 : ℝ) := by
  have h := refinedAtanhLogBounds (5641925 / 1910142653 : ℝ) (by norm_num) (by norm_num) 40
  norm_num [Finset.sum_range_succ] at h ⊢
  constructor <;> linarith [h.1, h.2]

private theorem fineLogHighOver16 :
    (181959294624779816240759 / 10^24 : ℝ) < Real.log (957892289 / 798532800 : ℝ) ∧
    Real.log (957892289 / 798532800 : ℝ) < (181959294624779816240760 / 10^24 : ℝ) := by
  have h := refinedAtanhLogBounds (159359489 / 1756425089 : ℝ) (by norm_num) (by norm_num) 40
  norm_num [Finset.sum_range_succ] at h ⊢
  constructor <;> linarith [h.1, h.2]

private theorem fineLogTheta16 :
    (592626719981716895588269 / 10^24 : ℝ) < Real.log (902708 / 499083 : ℝ) ∧
    Real.log (902708 / 499083 : ℝ) < (592626719981716895588270 / 10^24 : ℝ) := by
  have h := refinedAtanhLogBounds (403625 / 1401791 : ℝ) (by norm_num) (by norm_num) 40
  norm_num [Finset.sum_range_succ] at h ⊢
  constructor <;> linarith [h.1, h.2]

private theorem fineLogCOver16 :
    (227135572583747208765370 / 10^24 : ℝ) < Real.log (251 / 200 : ℝ) ∧
    Real.log (251 / 200 : ℝ) < (227135572583747208765371 / 10^24 : ℝ) := by
  have h := refinedAtanhLogBounds (51 / 451 : ℝ) (by norm_num) (by norm_num) 40
  norm_num [Finset.sum_range_succ] at h ⊢
  constructor <;> linarith [h.1, h.2]

private theorem fineLogC1Over16 :
    (176051943780359230064512 / 10^24 : ℝ) < Real.log (477 / 400 : ℝ) ∧
    Real.log (477 / 400 : ℝ) < (176051943780359230064513 / 10^24 : ℝ) := by
  have h := refinedAtanhLogBounds (77 / 877 : ℝ) (by norm_num) (by norm_num) 40
  norm_num [Finset.sum_range_succ] at h ⊢
  constructor <;> linarith [h.1, h.2]

private theorem refinedLogSixteen : Real.log 16 = 4 * Real.log 2 := by
  convert Real.log_pow (2 : ℝ) 4 using 1 <;> norm_num

/-- `ln w`, `w = 1 - θ = 1770655/1996332`. -/
private lemma logB_a : Real.log (1770655 / 1996332 : ℝ) ∈
    Set.Icc (-11996196209396412815 / 10^20 : ℝ) (-11996196209396412814 / 10^20 : ℝ) := by
  have hr := Real.log_mul (by norm_num : (2 : ℝ) ≠ 0)
    (by norm_num : (1770655 / 1996332 : ℝ) ≠ 0)
  norm_num at hr
  have h1 := fineLogCompTwice
  have h2 := fineLogTwo
  constructor <;> linarith [h1.1, h1.2, h2.1, h2.2]

/-- `ln r`, `r = (c - 1 + θ)/(c - 1) = 957892289/952250364`. -/
private lemma logB_b : Real.log (957892289 / 952250364 : ℝ) ∈
    Set.Icc (590735084442058617 / 10^20 : ℝ) (590735084442058618 / 10^20 : ℝ) := by
  have h1 := fineLogNearOne
  constructor <;> linarith [h1.1, h1.2]

/-- `ln s`, `s = c - 1 + θ = 957892289/49908300`. -/
private lemma logB_c : Real.log (957892289 / 49908300 : ℝ) ∈
    Set.Icc (295454801686456105390 / 10^20 : ℝ) (295454801686456105391 / 10^20 : ℝ) := by
  have hr := Real.log_mul (by norm_num : (16 : ℝ) ≠ 0)
    (by norm_num : (957892289 / 798532800 : ℝ) ≠ 0)
  rw [refinedLogSixteen] at hr
  norm_num at hr
  have h1 := fineLogHighOver16
  have h2 := fineLogTwo
  constructor <;> linarith [h1.1, h1.2, h2.1, h2.2]

private lemma logB_3 : Real.log (3 : ℝ) ∈
    Set.Icc (109861228866810969139 / 10^20 : ℝ) (109861228866810969140 / 10^20 : ℝ) := by
  have hr := Real.log_mul (by norm_num : (2 : ℝ) ≠ 0)
    (by norm_num : (3 / 2 : ℝ) ≠ 0)
  norm_num at hr
  have h1 := fineLogThreeHalf
  have h2 := fineLogTwo
  constructor <;> linarith [h1.1, h1.2, h2.1, h2.2]

private lemma logB_theta : Real.log (225677 / 1996332 : ℝ) ∈
    Set.Icc (-217996200225806434209 / 10^20 : ℝ) (-217996200225806434208 / 10^20 : ℝ) := by
  have hr := Real.log_mul (by norm_num : (16 : ℝ) ≠ 0)
    (by norm_num : (225677 / 1996332 : ℝ) ≠ 0)
  rw [refinedLogSixteen] at hr
  norm_num at hr
  have h1 := fineLogTheta16
  have h2 := fineLogTwo
  constructor <;> linarith [h1.1, h1.2, h2.1, h2.2]

private lemma logB_9 : Real.log (9 : ℝ) ∈
    Set.Icc (219722457733621938278 / 10^20 : ℝ) (219722457733621938281 / 10^20 : ℝ) := by
  rw [Real.log_nine]
  have h := logB_3
  constructor <;> linarith [h.1, h.2]

private lemma logB_4 : Real.log (4 : ℝ) ∈
    Set.Icc (138629436111989061882 / 10^20 : ℝ) (138629436111989061885 / 10^20 : ℝ) := by
  rw [Real.log_four]
  have h := fineLogTwo
  constructor <;> linarith [h.1, h.2]

/-- `ln c`, `c = 502/25`. -/
private lemma logB_cc : Real.log (502 / 25 : ℝ) ∈
    Set.Icc (299972429482352844643 / 10^20 : ℝ) (299972429482352844644 / 10^20 : ℝ) := by
  have hr := Real.log_mul (by norm_num : (16 : ℝ) ≠ 0)
    (by norm_num : (251 / 200 : ℝ) ≠ 0)
  rw [refinedLogSixteen] at hr
  norm_num at hr
  have h1 := fineLogCOver16
  have h2 := fineLogTwo
  constructor <;> linarith [h1.1, h1.2, h2.1, h2.2]

/-- `ln (c - 1)`, `c - 1 = 477/25`. -/
private lemma logB_cc1 : Real.log (477 / 25 : ℝ) ∈
    Set.Icc (294864066602014046773 / 10^20 : ℝ) (294864066602014046774 / 10^20 : ℝ) := by
  have hr := Real.log_mul (by norm_num : (16 : ℝ) ≠ 0)
    (by norm_num : (477 / 400 : ℝ) ≠ 0)
  rw [refinedLogSixteen] at hr
  norm_num at hr
  have h1 := fineLogC1Over16
  have h2 := fineLogTwo
  constructor <;> linarith [h1.1, h1.2, h2.1, h2.2]

/-- Cancellation of the large entropy terms, exactly at the new rational point. -/
private lemma GammaOf_B_eq :
    GammaOf (502 / 25) (225677 / 1996332) * Real.log 4
      = 1770655 / 1996332 * Real.log (1770655 / 1996332)
        + 477 / 25 * Real.log (957892289 / 952250364)
        + 225677 / 1996332 * Real.log (957892289 / 49908300)
        - 225677 / 1996332 * Real.log 9 := by
  rw [GammaOf_mul_log_four (by norm_num) (by norm_num) (by norm_num)]
  have h1 : (1 : ℝ) - 225677 / 1996332 = 1770655 / 1996332 := by norm_num
  have h2 : (502 / 25 : ℝ) - 1 + 225677 / 1996332 = 957892289 / 49908300 := by norm_num
  have h3 : (502 / 25 : ℝ) - 1 = 477 / 25 := by norm_num
  rw [h1, h2, h3, show (957892289 / 952250364 : ℝ) = (957892289 / 49908300) / (477 / 25) by
    norm_num, Real.log_div (x := 957892289 / 49908300) (y := 477 / 25) (by norm_num) (by norm_num)]
  ring

/-- The certified lower bound used for preprocessing boxes. -/
theorem GammaOf_B : (0.0663089654688 : ℝ) < GammaOf (502 / 25) (225677 / 1996332) := by
  refine lt_of_mul_lt_mul_right ?_ log_four_pos.le
  rw [GammaOf_B_eq]
  have h1 := logB_a; have h2 := logB_b; have h3 := logB_c; have h4 := logB_9
  have h5 := logB_4
  simp only [Set.mem_Icc] at *
  linarith

/-- A coarse upper bound (not used by the final assembly). -/
theorem GammaOf_B_lt : GammaOf (502 / 25) (225677 / 1996332) < (0.0664 : ℝ) := by
  refine lt_of_mul_lt_mul_right ?_ log_four_pos.le
  rw [GammaOf_B_eq]
  have h1 := logB_a; have h2 := logB_b; have h3 := logB_c; have h4 := logB_9
  have h5 := logB_4
  simp only [Set.mem_Icc] at *
  linarith

theorem GammaOf_B_pos : 0 < GammaOf (502 / 25) (225677 / 1996332) :=
  lt_trans (by norm_num) GammaOf_B

/-- The certified upper bound used for queries. -/
theorem qOf_B : qOf (225677 / 1996332) < (0.4336910345308 : ℝ) := by
  unfold qOf entropy
  rw [div_lt_iff₀ log_four_pos]
  have h1 := logB_theta; have h2 := logB_a; have h3 := logB_9; have h4 := logB_4
  norm_num only [show (1 : ℝ) - 225677 / 1996332 = 1770655 / 1996332 by norm_num]
  simp only [Set.mem_Icc] at *
  linarith

/-- The certified upper bound used for pruned encodings: `B = (c - 1) ln 3 / ln 4`. -/
theorem bExp_B : 477 / 25 * Real.log 3 / Real.log 4 < (15.12054225688 : ℝ) := by
  rw [div_lt_iff₀ log_four_pos]
  have h3 := logB_3; have h5 := logB_4
  simp only [Set.mem_Icc] at *
  linarith

/-- The coarse binomial coefficient bound. -/
theorem kappa_B : 502 / 25 * entropy (1 / (502 / 25)) / Real.log 4 < (2.9 : ℝ) := by
  rw [div_lt_iff₀ log_four_pos, PrunedAux.mul_entropy_inv (by norm_num)]
  have h1 := logB_cc; have h2 := logB_cc1; have h5 := logB_4
  rw [show (502 / 25 : ℝ) - 1 = 477 / 25 by norm_num]
  simp only [Set.mem_Icc] at *
  linarith

end ThreeSumApsp
