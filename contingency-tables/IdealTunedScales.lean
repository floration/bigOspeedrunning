/-
SPDX-License-Identifier: Apache-2.0
Retuned ideal-only threshold U = ⌊141 d^3 / 32⌋ with the unchanged padding
L = 3d. This is the smallest threshold of this form that the existing
sequential padding-count budget `47 (g L) e ≤ 32 (U + 1)` permits for all
g, e ≤ d, so unpadding still succeeds with probability at least one half on
the enlarged ordinary fibre. Combined with the quarter envelope of
`Math115.IdealQuarterRefinement`, the reference/selected/feasible chains at
these scales have inverse-gap allowance (141^4 / 32^3) d^17 < 12063 d^17, and
the unit branch half of that.

Scope: like the original `IdealOracleScales` d^17 statement, this proves the
actual-chain Poincare bound and the padding count at the new scales. The later
completion-program and finite-bit sampler modules are instantiated only at
U = 5 d^3 and are NOT re-proved here.
-/
import Math115.IdealQuarterRefinement

namespace Math115.IdealTunedScales

open OAI.ContingencyTables OAI.CommonBasesFPRAS
open CompletionCounts SmallGraphProfiles
open scoped BigOperators Classical
open SmallContextCoordinates SmallContextFibres PhysicalCompletionFibres FirstPaperProfiles
open FirstPaperPhysicalMarginal PaddedCompletions
open SmallContextEnumeration RowMajorEnumeration FiniteExposureVariance IntegerWeightedTransport
open Math115.PhysicalExposureVariance Math115.PhysicalFullVariance
open Math115.PhysicalRepairRefinement Math115.IdealQuarterRefinement

def tunedL (d : ℕ) : ℕ := 3 * d
def tunedU (d : ℕ) : ℕ := 141 * d ^ 3 / 32

lemma cube_large (d : ℕ) (hd : 11 ≤ d) : 1331 ≤ d ^ 3 := by
  have h := Nat.pow_le_pow_left hd 3
  norm_num at h
  exact h

theorem tunedU_large (d : ℕ) (hd : 11 ≤ d) : 4 * d ^ 3 ≤ tunedU d := by
  have ht := cube_large d hd
  unfold tunedU
  generalize d ^ 3 = t at ht ⊢
  omega

theorem tunedU_two (d : ℕ) (hd : 11 ≤ d) : 2 ≤ tunedU d := by
  have h := tunedU_large d hd
  have ht := cube_large d hd
  omega

theorem tunedU_real_le (d : ℕ) : (tunedU d : ℝ) ≤ 141 / 32 * (d : ℝ) ^ 3 := by
  have h : tunedU d * 32 ≤ 141 * d ^ 3 := by
    unfold tunedU
    exact Nat.div_mul_le_self _ _
  have hR : (tunedU d : ℝ) * 32 ≤ 141 * (d : ℝ) ^ 3 := by exact_mod_cast h
  linarith

theorem padding_three_dimension (d : ℕ) : 3 * d ≤ tunedL d := le_refl _

/-- The existing sequential budget holds at the retuned threshold. -/
theorem tuned_sequential_budget (d g e : ℕ) (hg : g ≤ d) (he : e ≤ d) :
    47 * (g * tunedL d) * e ≤ 32 * (tunedU d + 1) := by
  have hge : g * e ≤ d * d := Nat.mul_le_mul hg he
  have h1 : 47 * (g * tunedL d) * e = 141 * d * (g * e) := by unfold tunedL; ring
  have h2 : 141 * d * (g * e) ≤ 141 * d * (d * d) := Nat.mul_le_mul_left _ hge
  have h3 : 141 * d * (d * d) = 141 * d ^ 3 := by ring
  have h4 : 141 * d ^ 3 ≤ 32 * (tunedU d + 1) := by
    unfold tunedU
    generalize d ^ 3 = t
    omega
  omega

/-- Actual ordinary-table counts at the retuned scales: unpadding still
succeeds on at least half of the enlarged fibre. -/
theorem tuned_padded_count_le_twice_original
    {I J : Type*} [Fintype I] [Fintype J] [DecidableEq I] [DecidableEq J]
    (r : I → ℕ) (c : J → ℕ) (K : Finset (I × J)) (d : ℕ)
    (hsize : Fintype.card I * Fintype.card J ≤ d)
    (hrow : ∀ p ∈ K, tunedU d ≤ r p.1)
    (hcol : ∀ p ∈ K, tunedU d ≤ c p.2) :
    Fintype.card (Table (paddedRows r (largePadding K (tunedL d)))
      (paddedColumns c (largePadding K (tunedL d)))) ≤ 2 * Fintype.card (Table r c) := by
  classical
  have hK : K.card ≤ d :=
    (show K.card ≤ Fintype.card I * Fintype.card J by
      simpa only [Fintype.card_prod] using K.card_le_univ).trans hsize
  have he : (Fintype.card I - 1) * (Fintype.card J - 1) ≤ d :=
    (Nat.mul_le_mul (Nat.sub_le _ _) (Nat.sub_le _ _)).trans hsize
  exact PaddingGrowthAlgebra.count_le_twice_of_growth _ _ _ _ _
    (PaddingGrowth.large_padding_count_growth r c K (tunedL d) (tunedU d) hrow hcol)
    (tuned_sequential_budget d K.card _ hK he)

/-- Scalar step: 32 d^5 U^4 ≤ (141^4/32^3) d^17 at the retuned threshold. -/
theorem tuned_coefficient (d : ℕ) :
    32 * (d : ℝ) ^ 5 * (tunedU d : ℝ) ^ 4 ≤ (141 ^ 4 / 32 ^ 3 : ℝ) * (d : ℝ) ^ 17 := by
  have h0 : (0 : ℝ) ≤ tunedU d := Nat.cast_nonneg _
  have h4 : (tunedU d : ℝ) ^ 4 ≤ (141 / 32 * (d : ℝ) ^ 3) ^ 4 :=
    pow_le_pow_left₀ h0 (tunedU_real_le d) 4
  have h5 : 32 * (d : ℝ) ^ 5 * (tunedU d : ℝ) ^ 4 ≤
      32 * (d : ℝ) ^ 5 * (141 / 32 * (d : ℝ) ^ 3) ^ 4 :=
    mul_le_mul_of_nonneg_left h4 (by positivity)
  calc
    _ ≤ 32 * (d : ℝ) ^ 5 * (141 / 32 * (d : ℝ) ^ 3) ^ 4 := h5
    _ = _ := by ring

theorem tuned_coefficient_half (d : ℕ) :
    16 * (d : ℝ) ^ 5 * (tunedU d : ℝ) ^ 4 ≤ (141 ^ 4 / (2 * 32 ^ 3) : ℝ) * (d : ℝ) ^ 17 := by
  have h := tuned_coefficient d
  have e1 : 16 * (d : ℝ) ^ 5 * (tunedU d : ℝ) ^ 4 =
      (32 * (d : ℝ) ^ 5 * (tunedU d : ℝ) ^ 4) / 2 := by ring
  have e2 : (141 ^ 4 / (2 * 32 ^ 3) : ℝ) * (d : ℝ) ^ 17 =
      ((141 ^ 4 / 32 ^ 3 : ℝ) * (d : ℝ) ^ 17) / 2 := by ring
  rw [e1, e2]
  linarith

theorem tuned_constant_lt : (141 ^ 4 / 32 ^ 3 : ℝ) < 12063 := by norm_num

universe u
variable {I J : Type u} [Fintype I] [Fintype J] [LinearOrder I] [LinearOrder J]

noncomputable abbrev tunedCutoff : ℕ := tunedU (dimensionAllowance (I := I) (J := J))
noncomputable abbrev tunedPadding : ℕ := tunedL (dimensionAllowance (I := I) (J := J))

abbrev TunedStates (r : I → ℕ) (c : J → ℕ) :=
  ReducedSmallChain.States r c (tunedCutoff (I := I) (J := J)) (tunedPadding (I := I) (J := J))

theorem tunedReferenceChain_poincare (r : I → ℕ) (c : J → ℕ) [Nonempty (TunedStates r c)]
    (i₀ : LargeRows r (tunedCutoff (I := I) (J := J)))
    (j₀ : LargeColumns c (tunedCutoff (I := I) (J := J))) (H : TunedStates r c → ℝ) :
    (ReducedSmallChain.chain r c _ _ i₀ j₀).variance H ≤
      ((141 ^ 4 / 32 ^ 3 : ℝ) * (dimensionAllowance (I := I) (J := J) : ℝ) ^ 17) *
        (ReducedSmallChain.chain r c _ _ i₀ j₀).energy H := by
  let d := dimensionAllowance (I := I) (J := J)
  have hd : 11 ≤ d := PhysicalRepairRefinement.dimension_at_least_eleven
  have hp : Fintype.card (Cells (firstPaperSmall r c (tunedU d))) ≤ d :=
    (small_card_le_dimension (firstPaperSmall r c (tunedU d))).trans dimension_le_allowance
  have hE := (ReducedSmallChain.chain r c (tunedU d) (tunedL d) i₀ j₀).energy_nonneg H
  have hb := quarterReferenceProposal_budget _ d (tunedU d) hd (tunedU_large d hd) hp
  exact (chain_poincare_exact_refined r c (tunedU d) (tunedL d) i₀ j₀ (tunedU_two d hd)
    (padding_three_dimension d) H).trans
    (mul_le_mul_of_nonneg_right (hb.trans (tuned_coefficient d)) hE)

theorem tunedUnitChain_poincare (r : I → ℕ) (c : J → ℕ) [Nonempty (TunedStates r c)]
    (hempty : IsEmpty (LargeRows r (tunedCutoff (I := I) (J := J))) ∨
      IsEmpty (LargeColumns c (tunedCutoff (I := I) (J := J)))) (H : TunedStates r c → ℝ) :
    (ReducedAllSmallChain.unitChain r c (tunedCutoff (I := I) (J := J))
      (tunedPadding (I := I) (J := J))).variance H ≤
      ((141 ^ 4 / (2 * 32 ^ 3) : ℝ) * (dimensionAllowance (I := I) (J := J) : ℝ) ^ 17) *
        (ReducedAllSmallChain.unitChain r c (tunedCutoff (I := I) (J := J))
          (tunedPadding (I := I) (J := J))).energy H := by
  let d := dimensionAllowance (I := I) (J := J)
  have hd : 11 ≤ d := PhysicalRepairRefinement.dimension_at_least_eleven
  have hp : Fintype.card (Cells (firstPaperSmall r c (tunedU d))) ≤ d :=
    (small_card_le_dimension (firstPaperSmall r c (tunedU d))).trans dimension_le_allowance
  have hE := (ReducedAllSmallChain.unitChain r c (tunedU d) (tunedL d)).energy_nonneg H
  have hb := quarterProposal_budget _ d (tunedU d) hd (tunedU_large d hd) hp
  exact (unitChain_poincare_exact_refined r c (tunedU d) (tunedL d) hempty (tunedU_two d hd) H).trans
    (mul_le_mul_of_nonneg_right (hb.trans (tuned_coefficient_half d)) hE)

theorem tunedSelectedChain_poincare (r : I → ℕ) (c : J → ℕ) [Nonempty (TunedStates r c)]
    (H : TunedStates r c → ℝ) :
    (ReducedAllSmallChain.selectedChain r c (tunedCutoff (I := I) (J := J))
      (tunedPadding (I := I) (J := J))).variance H ≤
      ((141 ^ 4 / 32 ^ 3 : ℝ) * (dimensionAllowance (I := I) (J := J) : ℝ) ^ 17) *
        (ReducedAllSmallChain.selectedChain r c (tunedCutoff (I := I) (J := J))
          (tunedPadding (I := I) (J := J))).energy H := by
  let d := dimensionAllowance (I := I) (J := J)
  have hd : 11 ≤ d := PhysicalRepairRefinement.dimension_at_least_eleven
  have hp : Fintype.card (Cells (firstPaperSmall r c (tunedU d))) ≤ d :=
    (small_card_le_dimension (firstPaperSmall r c (tunedU d))).trans dimension_le_allowance
  have hE := (ReducedAllSmallChain.selectedChain r c (tunedU d) (tunedL d)).energy_nonneg H
  have hb := quarterReferenceProposal_budget _ d (tunedU d) hd (tunedU_large d hd) hp
  exact (selectedChain_poincare_exact_refined r c (tunedU d) (tunedL d) (tunedU_two d hd)
    (padding_three_dimension d) H).trans
    (mul_le_mul_of_nonneg_right (hb.trans (tuned_coefficient d)) hE)

/-- Headline: every equal-total ordinary margin pair, retuned scales,
inverse gap ≤ (141^4/32^3) d^17 < 12063 d^17. -/
theorem tunedFeasibleChain_poincare (r : I → ℕ) (c : J → ℕ)
    (htotal : ∑ i, r i = ∑ j, c j) (H : TunedStates r c → ℝ) :
    letI := PhysicalStateNonempty.states_nonempty r c (tunedCutoff (I := I) (J := J))
      (tunedPadding (I := I) (J := J)) htotal
    (ReducedAllSmallChain.selectedChain r c (tunedCutoff (I := I) (J := J))
      (tunedPadding (I := I) (J := J))).variance H ≤
      ((141 ^ 4 / 32 ^ 3 : ℝ) * (dimensionAllowance (I := I) (J := J) : ℝ) ^ 17) *
        (ReducedAllSmallChain.selectedChain r c (tunedCutoff (I := I) (J := J))
          (tunedPadding (I := I) (J := J))).energy H := by
  letI := PhysicalStateNonempty.states_nonempty r c (tunedCutoff (I := I) (J := J))
    (tunedPadding (I := I) (J := J)) htotal
  exact tunedSelectedChain_poincare r c H

end Math115.IdealTunedScales
