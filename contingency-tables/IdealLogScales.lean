/-
SPDX-License-Identifier: Apache-2.0
Threshold U = ⌊30000 d^3 / 6931⌋, L = 3d. The existing padding-growth budget
`47 q e ≤ 32 (U+1)` asks `q e/(U+1) ≤ 32/47 ≈ 0.681`; the sharp requirement for
`(1 + e/(U+1))^q ≤ 2` is `q e/(U+1) ≤ log 2 ≈ 0.6931`. Using
`1 + x ≤ exp x` and Mathlib's `log 2 > 0.6931471803`, the budget
`10000 q e ≤ 6931 (U+1)` suffices. With the quarter envelope this gives
inverse gap ≤ 32 (30000/6931)^4 d^17 < 11232 d^17 (unit branch: half).
Same scope as `IdealTunedScales`: actual-chain Poincare bound plus the
padding count at the new threshold; the finite-bit sampler modules remain
instantiated only at U = 5 d^3.
-/
import Math115.IdealQuarterRefinement

namespace Math115.IdealLogScales

open OAI.ContingencyTables OAI.CommonBasesFPRAS
open CompletionCounts SmallGraphProfiles
open scoped BigOperators Classical
open SmallContextCoordinates SmallContextFibres PhysicalCompletionFibres FirstPaperProfiles
open FirstPaperPhysicalMarginal PaddedCompletions
open SmallContextEnumeration RowMajorEnumeration FiniteExposureVariance IntegerWeightedTransport
open Math115.PhysicalExposureVariance Math115.PhysicalFullVariance
open Math115.PhysicalRepairRefinement Math115.IdealQuarterRefinement

def logL (d : ℕ) : ℕ := 3 * d
def logU (d : ℕ) : ℕ := 30000 * d ^ 3 / 6931

/-- `(1+x)^q ≤ 2` whenever `q x ≤ 0.6931`. -/
theorem one_add_pow_le_two_of_log (q : ℕ) (x : ℝ) (hx : 0 ≤ x)
    (hqx : (q : ℝ) * x ≤ 6931 / 10000) : (1 + x) ^ q ≤ 2 := by
  have h1 : (1 + x) ^ q ≤ (Real.exp x) ^ q := by
    apply pow_le_pow_left₀ (by linarith)
    have := Real.add_one_le_exp x
    linarith
  have h2 : (Real.exp x) ^ q = Real.exp ((q : ℝ) * x) := (Real.exp_nat_mul x q).symm
  have hlog : (6931 / 10000 : ℝ) < Real.log 2 := by
    have := Real.log_two_gt_d9
    linarith
  have h3 : Real.exp ((q : ℝ) * x) ≤ Real.exp (Real.log 2) :=
    Real.exp_le_exp.mpr (by linarith)
  rw [Real.exp_log (by norm_num)] at h3
  calc (1 + x) ^ q ≤ (Real.exp x) ^ q := h1
    _ = Real.exp ((q : ℝ) * x) := h2
    _ ≤ 2 := h3

/-- Count recurrence to twice-original under the log-2 budget. -/
theorem count_le_twice_of_growth_log (enlarged original q U e : ℕ)
    (hgrowth : enlarged * (U + 1) ^ q ≤ original * (U + 1 + e) ^ q)
    (hbudget : 10000 * q * e ≤ 6931 * (U + 1)) : enlarged ≤ 2 * original := by
  let D : ℝ := U + 1
  let x : ℝ := e / D
  have hD : 0 < D := by dsimp [D]; positivity
  have hx : 0 ≤ x := by dsimp [x]; positivity
  have hbudgetR : (10000 : ℝ) * q * e ≤ 6931 * D := by
    dsimp only [D]
    exact_mod_cast hbudget
  have hqx : (q : ℝ) * x ≤ 6931 / 10000 := by
    dsimp [x]
    rw [← mul_div_assoc]
    apply (div_le_iff₀ hD).mpr
    nlinarith only [hbudgetR]
  have hpow := one_add_pow_le_two_of_log q x hx hqx
  have hbase : (U : ℝ) + 1 + e = (1 + x) * D := by
    dsimp only [x]
    rw [add_mul, one_mul, div_mul_cancel₀ _ (ne_of_gt hD)]
  have hcount : (enlarged : ℝ) * D ^ q ≤ (original : ℝ) * ((U : ℝ) + 1 + e) ^ q := by
    dsimp only [D]
    exact_mod_cast hgrowth
  rw [hbase, mul_pow] at hcount
  have hcancel : (enlarged : ℝ) ≤ (original : ℝ) * (1 + x) ^ q := by
    apply (mul_le_mul_iff_left₀ (pow_pos hD q)).mp
    simpa only [mul_assoc] using hcount
  have hfinal : (enlarged : ℝ) ≤ 2 * (original : ℝ) :=
    hcancel.trans (by nlinarith only [mul_le_mul_of_nonneg_left hpow (Nat.cast_nonneg original)])
  exact_mod_cast hfinal

lemma cube_large (d : ℕ) (hd : 11 ≤ d) : 1331 ≤ d ^ 3 := by
  have h := Nat.pow_le_pow_left hd 3
  norm_num at h
  exact h

theorem logU_large (d : ℕ) (hd : 11 ≤ d) : 4 * d ^ 3 ≤ logU d := by
  have ht := cube_large d hd
  unfold logU
  generalize d ^ 3 = t at ht ⊢
  omega

theorem logU_two (d : ℕ) (hd : 11 ≤ d) : 2 ≤ logU d := by
  have h := logU_large d hd
  have ht := cube_large d hd
  omega

theorem logU_real_le (d : ℕ) : (logU d : ℝ) ≤ 30000 / 6931 * (d : ℝ) ^ 3 := by
  have h : logU d * 6931 ≤ 30000 * d ^ 3 := by
    unfold logU
    exact Nat.div_mul_le_self _ _
  have hR : (logU d : ℝ) * 6931 ≤ 30000 * (d : ℝ) ^ 3 := by exact_mod_cast h
  linarith

theorem padding_three_dimension (d : ℕ) : 3 * d ≤ logL d := le_refl _

theorem log_sequential_budget (d g e : ℕ) (hg : g ≤ d) (he : e ≤ d) :
    10000 * (g * logL d) * e ≤ 6931 * (logU d + 1) := by
  have hge : g * e ≤ d * d := Nat.mul_le_mul hg he
  have h1 : 10000 * (g * logL d) * e = 30000 * d * (g * e) := by unfold logL; ring
  have h2 : 30000 * d * (g * e) ≤ 30000 * d * (d * d) := Nat.mul_le_mul_left _ hge
  have h3 : 30000 * d * (d * d) = 30000 * d ^ 3 := by ring
  have h4 : 30000 * d ^ 3 ≤ 6931 * (logU d + 1) := by
    unfold logU
    generalize d ^ 3 = t
    omega
  omega

/-- Actual ordinary-table counts at the new scales. -/
theorem log_padded_count_le_twice_original
    {I J : Type*} [Fintype I] [Fintype J] [DecidableEq I] [DecidableEq J]
    (r : I → ℕ) (c : J → ℕ) (K : Finset (I × J)) (d : ℕ)
    (hsize : Fintype.card I * Fintype.card J ≤ d)
    (hrow : ∀ p ∈ K, logU d ≤ r p.1)
    (hcol : ∀ p ∈ K, logU d ≤ c p.2) :
    Fintype.card (Table (paddedRows r (largePadding K (logL d)))
      (paddedColumns c (largePadding K (logL d)))) ≤ 2 * Fintype.card (Table r c) := by
  classical
  have hK : K.card ≤ d :=
    (show K.card ≤ Fintype.card I * Fintype.card J by
      simpa only [Fintype.card_prod] using K.card_le_univ).trans hsize
  have he : (Fintype.card I - 1) * (Fintype.card J - 1) ≤ d :=
    (Nat.mul_le_mul (Nat.sub_le _ _) (Nat.sub_le _ _)).trans hsize
  exact count_le_twice_of_growth_log _ _ _ _ _
    (PaddingGrowth.large_padding_count_growth r c K (logL d) (logU d) hrow hcol)
    (log_sequential_budget d K.card _ hK he)

theorem log_coefficient (d : ℕ) :
    32 * (d : ℝ) ^ 5 * (logU d : ℝ) ^ 4 ≤ (32 * 30000 ^ 4 / 6931 ^ 4 : ℝ) * (d : ℝ) ^ 17 := by
  have h0 : (0 : ℝ) ≤ logU d := Nat.cast_nonneg _
  have h4 : (logU d : ℝ) ^ 4 ≤ (30000 / 6931 * (d : ℝ) ^ 3) ^ 4 :=
    pow_le_pow_left₀ h0 (logU_real_le d) 4
  calc
    _ ≤ 32 * (d : ℝ) ^ 5 * (30000 / 6931 * (d : ℝ) ^ 3) ^ 4 :=
      mul_le_mul_of_nonneg_left h4 (by positivity)
    _ = _ := by ring

theorem log_coefficient_half (d : ℕ) :
    16 * (d : ℝ) ^ 5 * (logU d : ℝ) ^ 4 ≤ (16 * 30000 ^ 4 / 6931 ^ 4 : ℝ) * (d : ℝ) ^ 17 := by
  have h := log_coefficient d
  have e1 : 16 * (d : ℝ) ^ 5 * (logU d : ℝ) ^ 4 = (32 * (d : ℝ) ^ 5 * (logU d : ℝ) ^ 4) / 2 := by ring
  have e2 : (16 * 30000 ^ 4 / 6931 ^ 4 : ℝ) * (d : ℝ) ^ 17 =
      ((32 * 30000 ^ 4 / 6931 ^ 4 : ℝ) * (d : ℝ) ^ 17) / 2 := by ring
  rw [e1, e2]
  linarith

theorem log_constant_lt : (32 * 30000 ^ 4 / 6931 ^ 4 : ℝ) < 11232 := by norm_num

universe u
variable {I J : Type u} [Fintype I] [Fintype J] [LinearOrder I] [LinearOrder J]

noncomputable abbrev logCutoff : ℕ := logU (dimensionAllowance (I := I) (J := J))
noncomputable abbrev logPadding : ℕ := logL (dimensionAllowance (I := I) (J := J))

abbrev LogStates (r : I → ℕ) (c : J → ℕ) :=
  ReducedSmallChain.States r c (logCutoff (I := I) (J := J)) (logPadding (I := I) (J := J))

theorem logUnitChain_poincare (r : I → ℕ) (c : J → ℕ) [Nonempty (LogStates r c)]
    (hempty : IsEmpty (LargeRows r (logCutoff (I := I) (J := J))) ∨
      IsEmpty (LargeColumns c (logCutoff (I := I) (J := J)))) (H : LogStates r c → ℝ) :
    (ReducedAllSmallChain.unitChain r c (logCutoff (I := I) (J := J))
      (logPadding (I := I) (J := J))).variance H ≤
      ((16 * 30000 ^ 4 / 6931 ^ 4 : ℝ) * (dimensionAllowance (I := I) (J := J) : ℝ) ^ 17) *
        (ReducedAllSmallChain.unitChain r c (logCutoff (I := I) (J := J))
          (logPadding (I := I) (J := J))).energy H := by
  let d := dimensionAllowance (I := I) (J := J)
  have hd : 11 ≤ d := PhysicalRepairRefinement.dimension_at_least_eleven
  have hp : Fintype.card (Cells (firstPaperSmall r c (logU d))) ≤ d :=
    (small_card_le_dimension (firstPaperSmall r c (logU d))).trans dimension_le_allowance
  have hE := (ReducedAllSmallChain.unitChain r c (logU d) (logL d)).energy_nonneg H
  have hb := quarterProposal_budget _ d (logU d) hd (logU_large d hd) hp
  exact (unitChain_poincare_exact_refined r c (logU d) (logL d) hempty (logU_two d hd) H).trans
    (mul_le_mul_of_nonneg_right (hb.trans (log_coefficient_half d)) hE)

theorem logSelectedChain_poincare (r : I → ℕ) (c : J → ℕ) [Nonempty (LogStates r c)]
    (H : LogStates r c → ℝ) :
    (ReducedAllSmallChain.selectedChain r c (logCutoff (I := I) (J := J))
      (logPadding (I := I) (J := J))).variance H ≤
      ((32 * 30000 ^ 4 / 6931 ^ 4 : ℝ) * (dimensionAllowance (I := I) (J := J) : ℝ) ^ 17) *
        (ReducedAllSmallChain.selectedChain r c (logCutoff (I := I) (J := J))
          (logPadding (I := I) (J := J))).energy H := by
  let d := dimensionAllowance (I := I) (J := J)
  have hd : 11 ≤ d := PhysicalRepairRefinement.dimension_at_least_eleven
  have hp : Fintype.card (Cells (firstPaperSmall r c (logU d))) ≤ d :=
    (small_card_le_dimension (firstPaperSmall r c (logU d))).trans dimension_le_allowance
  have hE := (ReducedAllSmallChain.selectedChain r c (logU d) (logL d)).energy_nonneg H
  have hb := quarterReferenceProposal_budget _ d (logU d) hd (logU_large d hd) hp
  exact (selectedChain_poincare_exact_refined r c (logU d) (logL d) (logU_two d hd)
    (padding_three_dimension d) H).trans
    (mul_le_mul_of_nonneg_right (hb.trans (log_coefficient d)) hE)

/-- Headline: all equal-total margins, inverse gap ≤ 32(30000/6931)^4 d^17 < 11232 d^17. -/
theorem logFeasibleChain_poincare (r : I → ℕ) (c : J → ℕ)
    (htotal : ∑ i, r i = ∑ j, c j) (H : LogStates r c → ℝ) :
    letI := PhysicalStateNonempty.states_nonempty r c (logCutoff (I := I) (J := J))
      (logPadding (I := I) (J := J)) htotal
    (ReducedAllSmallChain.selectedChain r c (logCutoff (I := I) (J := J))
      (logPadding (I := I) (J := J))).variance H ≤
      ((32 * 30000 ^ 4 / 6931 ^ 4 : ℝ) * (dimensionAllowance (I := I) (J := J) : ℝ) ^ 17) *
        (ReducedAllSmallChain.selectedChain r c (logCutoff (I := I) (J := J))
          (logPadding (I := I) (J := J))).energy H := by
  letI := PhysicalStateNonempty.states_nonempty r c (logCutoff (I := I) (J := J))
    (logPadding (I := I) (J := J)) htotal
  exact logSelectedChain_poincare r c H

end Math115.IdealLogScales
