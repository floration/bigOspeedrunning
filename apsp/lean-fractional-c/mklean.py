import json
from fractions import Fraction as F
E=json.load(open('encl.json')); D=json.load(open('derived.json'))
c=F(502,25); th=F(225677,1996332); w=1-th; cm1=c-1; s=cm1+th; r=s/cm1
def fr(x): return f"{x.numerator} / {x.denominator}" if x.denominator!=1 else f"{x.numerator}"
C,TH,W,CM1,S,R=fr(c),fr(th),fr(w),fr(cm1),fr(s),fr(r)
def fine(name,key):
    y,z,a,b=E[key]; y=F(y); z=F(z)
    return f"""private theorem {name} :
    ({a} / 10^24 : ℝ) < Real.log ({fr(y)} : ℝ) ∧
    Real.log ({fr(y)} : ℝ) < ({b} / 10^24 : ℝ) := by
  have h := refinedAtanhLogBounds ({fr(z)} : ℝ) (by norm_num) (by norm_num) 40
  norm_num [Finset.sum_range_succ] at h ⊢
  constructor <;> linarith [h.1, h.2]
"""
def icc(k): a,b=D[k]; return f"Set.Icc ({a} / 10^20 : ℝ) ({b} / 10^20 : ℝ)"
two=F(2); 
txt=f"""/-
Copyright (c) 2026 Anthropic, PBC. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
SPDX-License-Identifier: Apache-2.0
Parameter and numerical refinements (c) 2026 Joshua Wharton, QFEX.
Author of modifications: Joshua Wharton <joshua@qfex.com>
Fractional c = 502/25 refinement, 2026.
-/
module

public import Submission.ThreeSumApsp.Pruned.Costs
public import Mathlib.Analysis.SpecialFunctions.Log.Deriv

/-!
# Refined numbers for `c = 502/25`, `θ = {TH}`

The logarithms are proved from forty terms of the positive atanh series, with
Mathlib's geometric remainder bound. Python selected the rational endpoints;
it supplies no assumptions to Lean. The public bounds are
`Γ > 0.0663089654688`, `q < 0.4336910345308`, `(477/25) ln 3 / ln 4 < 15.12054225688`
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

{fine('fineLogTwo','Two')}
{fine('fineLogThreeHalf','ThreeHalf')}
{fine('fineLogCompTwice','W2')}
{fine('fineLogNearOne','R')}
{fine('fineLogTheta16','Theta16')}
{fine('fineLogHighOver16','S16')}
{fine('fineLogCOver16','C16')}
{fine('fineLogCm1Over16','Cm116')}
private theorem refinedLogSixteen : Real.log 16 = 4 * Real.log 2 := by
  convert Real.log_pow (2 : ℝ) 4 using 1 <;> norm_num

private lemma logB_a : Real.log ({W} : ℝ) ∈ {icc('a')} := by
  have hr := Real.log_mul (by norm_num : (2 : ℝ) ≠ 0)
    (by norm_num : ({W} : ℝ) ≠ 0)
  norm_num at hr
  have h1 := fineLogCompTwice
  have h2 := fineLogTwo
  constructor <;> linarith [h1.1, h1.2, h2.1, h2.2]

private lemma logB_b : Real.log ({R} : ℝ) ∈ {icc('b')} := by
  have h1 := fineLogNearOne
  constructor <;> linarith [h1.1, h1.2]

private lemma logB_c : Real.log ({S} : ℝ) ∈ {icc('c')} := by
  have hr := Real.log_mul (by norm_num : (16 : ℝ) ≠ 0)
    (by norm_num : ({fr(s/16)} : ℝ) ≠ 0)
  rw [refinedLogSixteen] at hr
  norm_num at hr
  have h1 := fineLogHighOver16
  have h2 := fineLogTwo
  constructor <;> linarith [h1.1, h1.2, h2.1, h2.2]

private lemma logB_3 : Real.log (3 : ℝ) ∈ {icc('3')} := by
  have hr := Real.log_mul (by norm_num : (2 : ℝ) ≠ 0)
    (by norm_num : (3 / 2 : ℝ) ≠ 0)
  norm_num at hr
  have h1 := fineLogThreeHalf
  have h2 := fineLogTwo
  constructor <;> linarith [h1.1, h1.2, h2.1, h2.2]

private lemma logB_theta : Real.log ({TH} : ℝ) ∈ {icc('theta')} := by
  have hr := Real.log_mul (by norm_num : (16 : ℝ) ≠ 0)
    (by norm_num : ({TH} : ℝ) ≠ 0)
  rw [refinedLogSixteen] at hr
  norm_num at hr
  have h1 := fineLogTheta16
  have h2 := fineLogTwo
  constructor <;> linarith [h1.1, h1.2, h2.1, h2.2]

private lemma logB_cc : Real.log ({C} : ℝ) ∈ {icc('cc')} := by
  have hr := Real.log_mul (by norm_num : (16 : ℝ) ≠ 0)
    (by norm_num : ({fr(c/16)} : ℝ) ≠ 0)
  rw [refinedLogSixteen] at hr
  norm_num at hr
  have h1 := fineLogCOver16
  have h2 := fineLogTwo
  constructor <;> linarith [h1.1, h1.2, h2.1, h2.2]

private lemma logB_cm1 : Real.log ({CM1} : ℝ) ∈ {icc('cm1')} := by
  have hr := Real.log_mul (by norm_num : (16 : ℝ) ≠ 0)
    (by norm_num : ({fr(cm1/16)} : ℝ) ≠ 0)
  rw [refinedLogSixteen] at hr
  norm_num at hr
  have h1 := fineLogCm1Over16
  have h2 := fineLogTwo
  constructor <;> linarith [h1.1, h1.2, h2.1, h2.2]

private lemma logB_9 : Real.log (9 : ℝ) ∈ {icc('9')} := by
  rw [Real.log_nine]
  have h := logB_3
  constructor <;> linarith [h.1, h.2]

private lemma logB_4 : Real.log (4 : ℝ) ∈ {icc('4')} := by
  rw [Real.log_four]
  have h := fineLogTwo
  constructor <;> linarith [h.1, h.2]

/-- Cancellation of the large entropy terms, exactly at the new rational point. -/
private lemma GammaOf_B_eq :
    GammaOf ({C}) ({TH}) * Real.log 4
      = {W} * Real.log ({W})
        + {CM1} * Real.log ({R})
        + {TH} * Real.log ({S})
        - {TH} * Real.log 9 := by
  rw [GammaOf_mul_log_four (by norm_num) (by norm_num) (by norm_num)]
  have h1 : (1 : ℝ) - {TH} = {W} := by norm_num
  have h2 : ({C} : ℝ) - 1 + {TH} = {S} := by norm_num
  have h3 : ({C} : ℝ) - 1 = {CM1} := by norm_num
  rw [h1, h2, h3, show ({R} : ℝ) = ({S}) / ({CM1}) by
    norm_num, Real.log_div (x := {S}) (y := {CM1}) (by norm_num) (by norm_num)]
  ring

/-- The certified lower bound used for preprocessing boxes. -/
theorem GammaOf_B : (0.0663089654688 : ℝ) < GammaOf ({C}) ({TH}) := by
  refine lt_of_mul_lt_mul_right ?_ log_four_pos.le
  rw [GammaOf_B_eq]
  have h1 := logB_a; have h2 := logB_b; have h3 := logB_c; have h4 := logB_9
  have h5 := logB_4
  simp only [Set.mem_Icc] at *
  linarith

/-- A coarse upper bound. -/
theorem GammaOf_B_lt : GammaOf ({C}) ({TH}) < (0.0664 : ℝ) := by
  refine lt_of_mul_lt_mul_right ?_ log_four_pos.le
  rw [GammaOf_B_eq]
  have h1 := logB_a; have h2 := logB_b; have h3 := logB_c; have h4 := logB_9
  have h5 := logB_4
  simp only [Set.mem_Icc] at *
  linarith

theorem GammaOf_B_pos : 0 < GammaOf ({C}) ({TH}) :=
  lt_trans (by norm_num) GammaOf_B

/-- The certified upper bound used for queries. -/
theorem qOf_B : qOf ({TH}) < (0.4336910345308 : ℝ) := by
  unfold qOf entropy
  rw [div_lt_iff₀ log_four_pos]
  have h1 := logB_theta; have h2 := logB_a; have h3 := logB_9; have h4 := logB_4
  norm_num only [show (1 : ℝ) - {TH} = {W} by norm_num]
  simp only [Set.mem_Icc] at *
  linarith

/-- The certified upper bound used for pruned encodings. -/
theorem bExp_B : {CM1} * Real.log 3 / Real.log 4 < (15.12054225688 : ℝ) := by
  rw [div_lt_iff₀ log_four_pos]
  have h3 := logB_3; have h5 := logB_4
  simp only [Set.mem_Icc] at *
  linarith

/-- The coarse binomial coefficient bound. -/
theorem kappa_B : ({C} : ℝ) * entropy (1 / ({C})) / Real.log 4 < (2.9 : ℝ) := by
  rw [div_lt_iff₀ log_four_pos, PrunedAux.mul_entropy_inv (by norm_num)]
  have h1 := logB_cc; have h2 := logB_cm1; have h5 := logB_4
  rw [show ({C} : ℝ) - 1 = {CM1} by norm_num]
  simp only [Set.mem_Icc] at *
  linarith

end ThreeSumApsp
"""
open('Numbers.lean','w').write(txt)
