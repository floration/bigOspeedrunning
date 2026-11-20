/-
SPDX-License-Identifier: Apache-2.0
A sharper polynomial envelope for the unchanged refined repair coefficient
at the unchanged ideal-only scales U=5*d^3, L=3*d.

The chains, scales, proposal and exact Poincare coefficients
`2 * refinedConstant p U / smallProposal d` are exactly those of
`Math115.PhysicalRepairRefinement`; only the final scalar estimate changes.
The earlier envelope used `U(U+1)/2 ≤ 3U^2/4` and `(U+1)^2 ≤ 9U^2/4`, valid
for every `U ≥ 2`. At `U = 5d^3 ≥ 6655` both are nearly equalities with
leading constants `1/2` and `1`, which gives `refinedConstant ≤ d^3 U^4 / 4`
instead of `d^3 U^4`. The reference/selected/feasible coefficient falls
from `80000*d^17` to `20000*d^17`, and the unit branch from `40000*d^17`
to `10000*d^17`.
-/
import Math115.PhysicalRepairRefinement
import Math115.IdealOracleScales

namespace Math115.IdealQuarterRefinement

open OAI.ContingencyTables OAI.CommonBasesFPRAS
open CompletionCounts SmallGraphProfiles Math115.IdealOracleScales
open scoped BigOperators Classical
open SmallContextCoordinates SmallContextFibres PhysicalCompletionFibres FirstPaperProfiles
open FirstPaperPhysicalMarginal PaddedCompletions
open SmallContextEnumeration RowMajorEnumeration FiniteExposureVariance IntegerWeightedTransport
open Math115.PhysicalExposureVariance Math115.PhysicalFullVariance
open Math115.PhysicalRepairRefinement

/-- Pure polynomial step: for `x ≥ 4 D^3` and `D ≥ 11`. -/
lemma quarter_polynomial (D x : ℝ) (hD : 11 ≤ D) (hx : 4 * D^3 ≤ x) :
    (D^2 + D + 1) * ((x * (x + 1) / 2) * (2 + (D - 1) * (x + 1)^2 / 2)) + 1 + D ≤
      D^3 * x^4 / 4 := by
  have hD0 : 0 ≤ D := by linarith
  have hDsq : 121 ≤ D^2 := by nlinarith [mul_le_mul hD hD (by norm_num) hD0]
  have hcube : D^3 = D * D^2 := by ring
  have h11 : 11 * D^2 ≤ D^3 := by
    rw [hcube]; exact mul_le_mul_of_nonneg_right hD (sq_nonneg D)
  have hDD : 121 * D ≤ D^3 := by
    rw [hcube]; nlinarith [mul_le_mul_of_nonneg_left hDsq hD0]
  have hD3 : 1331 ≤ D^3 := by linarith
  have hx0 : 5324 ≤ x := by linarith
  have hxp : 0 ≤ x := by linarith
  have hsmall : D^2 + D + 1 ≤ D^3 := by linarith
  -- Rewrite the target as a nonnegativity statement.
  have key : (D^3 - 1) * (3 * x^3 + 3 * x^2 + x) + 4 * (D^2 + D + 1) * (x^2 + x) + 4 * (1 + D)
      ≤ x^4 := by
    have hx2 : 0 ≤ x^2 := sq_nonneg x
    have hx3 : 0 ≤ x^3 := by positivity
    -- x^4 ≥ 4 D^3 x^3
    have h4 : 4 * D^3 * x^3 ≤ x^4 := by
      have := mul_le_mul_of_nonneg_right hx hx3
      nlinarith [this]
    -- D^3 x^3 dominates the lower-order terms.
    have hxx : 5324 * x^2 ≤ x^3 := by
      have := mul_le_mul_of_nonneg_right hx0 hx2
      nlinarith [this]
    have hx1 : 5324 * x ≤ x^2 := by nlinarith [mul_le_mul_of_nonneg_right hx0 hxp]
    have hD3x2 : D^3 * (5324 * x^2) ≤ D^3 * x^3 := mul_le_mul_of_nonneg_left hxx (by positivity)
    have hD3x1 : D^3 * (5324 * x) ≤ D^3 * x^2 := mul_le_mul_of_nonneg_left hx1 (by positivity)
    have hsm2 : (D^2 + D + 1) * (x^2 + x) ≤ D^3 * (x^2 + x) :=
      mul_le_mul_of_nonneg_right hsmall (by positivity)
    have hlast : 4 * (1 + D) ≤ D^3 * x := by
      have : D^3 * 5324 ≤ D^3 * x := mul_le_mul_of_nonneg_left hx0 (by positivity)
      linarith
    have hneg : (D^3 - 1) * (3 * x^3 + 3 * x^2 + x) ≤ D^3 * (3 * x^3 + 3 * x^2 + x) := by
      nlinarith [hx3, hx2, hxp]
    nlinarith [hneg, hsm2, hlast, hD3x2, hD3x1, h4]
  have hexp : (D^2 + D + 1) * ((x * (x + 1) / 2) * (2 + (D - 1) * (x + 1)^2 / 2)) + 1 + D =
      ((D^3 - 1) * (x^4 + 3 * x^3 + 3 * x^2 + x) + 4 * (D^2 + D + 1) * (x^2 + x) + 4 * (1 + D)) / 4 := by
    ring
  rw [hexp]
  have : (D^3 - 1) * (x^4 + 3 * x^3 + 3 * x^2 + x) + 4 * (D^2 + D + 1) * (x^2 + x) + 4 * (1 + D) ≤
      D^3 * x^4 := by nlinarith [key]
  linarith

/-- Quarter envelope for the unchanged refined coefficient. -/
theorem refinedConstant_le_quarter (p d U : ℕ)
    (hd : 11 ≤ d) (hU : 4 * d^3 ≤ U) (hp : p ≤ d) :
    refinedConstant p U ≤ (d : ℝ)^3 * (U : ℝ)^4 / 4 := by
  have hdR : (11 : ℝ) ≤ d := by exact_mod_cast hd
  have hd0 : (0 : ℝ) < d := by linarith
  have hUR : 4 * (d : ℝ)^3 ≤ U := by exact_mod_cast hU
  have hU0 : (0 : ℝ) ≤ U := Nat.cast_nonneg U
  have hpR : (p : ℝ) ≤ d := by exact_mod_cast hp
  have hpminus : ((p - 1 : ℕ) : ℝ) ≤ (d : ℝ) - 1 := by
    have h : ((p - 1 : ℕ) : ℝ) ≤ ((d - 1 : ℕ) : ℝ) := by
      exact_mod_cast Nat.sub_le_sub_right hp 1
    simpa only [Nat.cast_sub (show 1 ≤ d by omega), Nat.cast_one] using h
  have hinner : 2 + ((p - 1 : ℕ) : ℝ) * ((U : ℝ) + 1)^2 / 2 ≤
      2 + ((d : ℝ) - 1) * ((U : ℝ) + 1)^2 / 2 := by
    have := mul_le_mul_of_nonneg_right hpminus (sq_nonneg ((U : ℝ) + 1))
    linarith
  have htrans : transversalConstant p U ≤
      ((U : ℝ) * ((U : ℝ) + 1) / 2) * (2 + ((d : ℝ) - 1) * ((U : ℝ) + 1)^2 / 2) := by
    unfold transversalConstant
    exact mul_le_mul_of_nonneg_left hinner (by positivity)
  have hp2 : (p : ℝ)^2 ≤ (d : ℝ)^2 := by gcongr
  have hm : 1 + (1 + 1 / (d : ℝ)) * (p : ℝ)^2 ≤ (d : ℝ)^2 + d + 1 := by
    have hmul := mul_le_mul_of_nonneg_left hp2 (show 0 ≤ 1 + 1 / (d : ℝ) by positivity)
    have he : (1 + 1 / (d : ℝ)) * (d : ℝ)^2 = (d : ℝ)^2 + d := by
      field_simp [ne_of_gt hd0]
    linarith
  calc
    refinedConstant p U ≤ (1 + (1 + 1 / (d : ℝ)) * (p : ℝ)^2) *
        transversalConstant p U + 1 + d :=
      sqrt_coefficient_le_young _ _ _ (sq_nonneg _) (transversalConstant_nonnegative p U) hd0
    _ ≤ ((d : ℝ)^2 + d + 1) *
        (((U : ℝ) * ((U : ℝ) + 1) / 2) * (2 + ((d : ℝ) - 1) * ((U : ℝ) + 1)^2 / 2)) + 1 + d := by
      have h := mul_le_mul hm htrans (transversalConstant_nonnegative p U) (by positivity)
      linarith only [h]
    _ ≤ _ := quarter_polynomial (d : ℝ) (U : ℝ) hdR hUR

/-- Proposal budget with the quarter envelope. -/
theorem quarterProposal_budget (p d U : ℕ)
    (hd : 11 ≤ d) (hU : 4 * d^3 ≤ U) (hp : p ≤ d) :
    refinedConstant p U / smallProposal d ≤ 16 * (d : ℝ)^5 * (U : ℝ)^4 := by
  have hproposal := smallProposal_bounds d (show 1 ≤ d by omega)
  have hrecip : 1 / smallProposal d ≤ 64 * (d : ℝ)^2 := by
    apply (div_le_iff₀ hproposal.1).mpr
    have h := (div_le_iff₀ (show (0 : ℝ) < 64 * (d : ℝ)^2 by positivity)).mp hproposal.2.1
    nlinarith only [h]
  calc
    _ = refinedConstant p U * (1 / smallProposal d) := by ring
    _ ≤ refinedConstant p U * (64 * (d : ℝ)^2) :=
      mul_le_mul_of_nonneg_left hrecip (refinedConstant_nonnegative p U)
    _ ≤ ((d : ℝ)^3 * (U : ℝ)^4 / 4) * (64 * (d : ℝ)^2) :=
      mul_le_mul_of_nonneg_right (refinedConstant_le_quarter p d U hd hU hp) (by positivity)
    _ = _ := by ring

theorem quarterReferenceProposal_budget (p d U : ℕ)
    (hd : 11 ≤ d) (hU : 4 * d^3 ≤ U) (hp : p ≤ d) :
    2 * refinedConstant p U / smallProposal d ≤ 32 * (d : ℝ)^5 * (U : ℝ)^4 := by
  have h := mul_le_mul_of_nonneg_left (quarterProposal_budget p d U hd hU hp)
    (show (0 : ℝ) ≤ 2 by norm_num)
  convert h using 1 <;> ring

theorem ideal_threshold_large (d : ℕ) : 4 * d^3 ≤ idealU d := by
  unfold idealU; omega

universe u
variable {I J : Type u} [Fintype I] [Fintype J] [LinearOrder I] [LinearOrder J]

theorem referenceChain_poincare_d17_quarter (r : I → ℕ) (c : J → ℕ) [Nonempty (IdealStates r c)]
    (i₀ : LargeRows r (cutoff (I := I) (J := J)))
    (j₀ : LargeColumns c (cutoff (I := I) (J := J))) (H : IdealStates r c → ℝ) :
    (referenceChain r c i₀ j₀).variance H ≤
      ((32 * 5^4 : ℝ) * (dimensionAllowance (I := I) (J := J) : ℝ)^17) *
        (referenceChain r c i₀ j₀).energy H := by
  let d := dimensionAllowance (I := I) (J := J)
  have hd : 11 ≤ d := PhysicalRepairRefinement.dimension_at_least_eleven
  have hU : 2 ≤ idealU d := threshold_at_least_two d (by omega)
  have hp : Fintype.card (Cells (firstPaperSmall r c (idealU d))) ≤ d :=
    (small_card_le_dimension (firstPaperSmall r c (idealU d))).trans dimension_le_allowance
  have h := (chain_poincare_exact_refined r c (idealU d) (idealL d) i₀ j₀ hU
    (padding_at_least_three_dimension d) H).trans
    (mul_le_mul_of_nonneg_right
      (quarterReferenceProposal_budget _ d (idealU d) hd (ideal_threshold_large d) hp)
      ((ReducedSmallChain.chain r c (idealU d) (idealL d) i₀ j₀).energy_nonneg H))
  change (ReducedSmallChain.chain r c (idealU d) (idealL d) i₀ j₀).variance H ≤
    ((32 * 5^4 : ℝ) * (d : ℝ)^17) *
      (ReducedSmallChain.chain r c (idealU d) (idealL d) i₀ j₀).energy H
  convert h using 1
  unfold idealU
  push_cast
  ring

theorem unitChain_poincare_d17_quarter (r : I → ℕ) (c : J → ℕ) [Nonempty (IdealStates r c)]
    (hempty : IsEmpty (LargeRows r (cutoff (I := I) (J := J))) ∨
      IsEmpty (LargeColumns c (cutoff (I := I) (J := J)))) (H : IdealStates r c → ℝ) :
    (ReducedAllSmallChain.unitChain r c (cutoff (I := I) (J := J))
      (padding (I := I) (J := J))).variance H ≤
      ((16 * 5^4 : ℝ) * (dimensionAllowance (I := I) (J := J) : ℝ)^17) *
        (ReducedAllSmallChain.unitChain r c (cutoff (I := I) (J := J))
          (padding (I := I) (J := J))).energy H := by
  let d := dimensionAllowance (I := I) (J := J)
  have hd : 11 ≤ d := PhysicalRepairRefinement.dimension_at_least_eleven
  have hU : 2 ≤ idealU d := threshold_at_least_two d (by omega)
  have hp : Fintype.card (Cells (firstPaperSmall r c (idealU d))) ≤ d :=
    (small_card_le_dimension (firstPaperSmall r c (idealU d))).trans dimension_le_allowance
  have h := (unitChain_poincare_exact_refined r c (idealU d) (idealL d) hempty hU H).trans
    (mul_le_mul_of_nonneg_right
      (quarterProposal_budget _ d (idealU d) hd (ideal_threshold_large d) hp)
      ((ReducedAllSmallChain.unitChain r c (idealU d) (idealL d)).energy_nonneg H))
  change (ReducedAllSmallChain.unitChain r c (idealU d) (idealL d)).variance H ≤
    ((16 * 5^4 : ℝ) * (d : ℝ)^17) *
      (ReducedAllSmallChain.unitChain r c (idealU d) (idealL d)).energy H
  convert h using 1
  unfold idealU
  push_cast
  ring

theorem selectedChain_poincare_d17_quarter (r : I → ℕ) (c : J → ℕ) [Nonempty (IdealStates r c)]
    (H : IdealStates r c → ℝ) :
    (selectedChain r c).variance H ≤
      ((32 * 5^4 : ℝ) * (dimensionAllowance (I := I) (J := J) : ℝ)^17) *
        (selectedChain r c).energy H := by
  let d := dimensionAllowance (I := I) (J := J)
  have hd : 11 ≤ d := PhysicalRepairRefinement.dimension_at_least_eleven
  have hU : 2 ≤ idealU d := threshold_at_least_two d (by omega)
  have hp : Fintype.card (Cells (firstPaperSmall r c (idealU d))) ≤ d :=
    (small_card_le_dimension (firstPaperSmall r c (idealU d))).trans dimension_le_allowance
  have h := (selectedChain_poincare_exact_refined r c (idealU d) (idealL d) hU
    (padding_at_least_three_dimension d) H).trans
    (mul_le_mul_of_nonneg_right
      (quarterReferenceProposal_budget _ d (idealU d) hd (ideal_threshold_large d) hp)
      ((ReducedAllSmallChain.selectedChain r c (idealU d) (idealL d)).energy_nonneg H))
  change (ReducedAllSmallChain.selectedChain r c (idealU d) (idealL d)).variance H ≤
    ((32 * 5^4 : ℝ) * (d : ℝ)^17) *
      (ReducedAllSmallChain.selectedChain r c (idealU d) (idealL d)).energy H
  convert h using 1
  unfold idealU
  push_cast
  ring

/-- Headline: every equal-total ordinary margin pair, inverse gap ≤ 20000*d^17. -/
theorem feasibleChain_poincare_d17_quarter (r : I → ℕ) (c : J → ℕ)
    (htotal : ∑ i, r i = ∑ j, c j) (H : IdealStates r c → ℝ) :
    (feasibleChain r c htotal).variance H ≤
      ((32 * 5^4 : ℝ) * (dimensionAllowance (I := I) (J := J) : ℝ)^17) *
        (feasibleChain r c htotal).energy H := by
  letI := PhysicalStateNonempty.states_nonempty r c (cutoff (I := I) (J := J))
    (padding (I := I) (J := J)) htotal
  exact selectedChain_poincare_d17_quarter r c H

end Math115.IdealQuarterRefinement
