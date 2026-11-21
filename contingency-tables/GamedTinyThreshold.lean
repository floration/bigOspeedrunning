/-
SPDX-License-Identifier: Apache-2.0
MAX-GAMED VARIANT. Not the intended result: see the scope note.

The "ideal auxiliary chain" Poincare theorem proved upstream and by EcoDataLab
(`PhysicalRepairRefinement.selectedChain_poincare_polynomial_refined`) holds for
EVERY threshold U ≥ 2 and padding L ≥ 3d. Nothing in that statement ties U to
the unpadding step. Taking the smallest admissible threshold U = 2 gives
inverse gap ≤ 128 d^5 · 2^4 = 2048 d^5 for the same chain constructor.

Scope / why this games the metric: the padding-count lemma (unpadding succeeds
with probability ≥ 1/2) needs U ≳ 4.33 d^3. At U = 2 no such lemma holds, and
unpadding can fail with overwhelming probability, so the chain no longer
yields a polynomial-time sampler. The headline gap theorem is still a true,
kernel-checked statement about an actual chain, but it says nothing useful
about sampling contingency tables.
-/
import Math115.PhysicalRepairRefinement
import Math115.PhysicalStateNonempty

namespace Math115.GamedTinyThreshold

open OAI.ContingencyTables OAI.CommonBasesFPRAS
open CompletionCounts SmallGraphProfiles
open scoped BigOperators Classical

universe u
variable {I J : Type u} [Fintype I] [Fintype J] [LinearOrder I] [LinearOrder J]

noncomputable abbrev gamedL : ℕ := 3 * dimensionAllowance (I := I) (J := J)

theorem gamedFeasibleChain_poincare_d5 (r : I → ℕ) (c : J → ℕ)
    (htotal : ∑ i, r i = ∑ j, c j)
    (H : ReducedSmallChain.States r c 2 (gamedL (I := I) (J := J)) → ℝ) :
    letI := PhysicalStateNonempty.states_nonempty r c 2 (gamedL (I := I) (J := J)) htotal
    (ReducedAllSmallChain.selectedChain r c 2 (gamedL (I := I) (J := J))).variance H ≤
      ((2048 : ℝ) * (dimensionAllowance (I := I) (J := J) : ℝ) ^ 5) *
        (ReducedAllSmallChain.selectedChain r c 2 (gamedL (I := I) (J := J))).energy H := by
  letI := PhysicalStateNonempty.states_nonempty r c 2 (gamedL (I := I) (J := J)) htotal
  have h := PhysicalRepairRefinement.selectedChain_poincare_polynomial_refined r c 2
    (gamedL (I := I) (J := J)) (le_refl 2) (le_refl _) H
  convert h using 2
  push_cast
  ring

end Math115.GamedTinyThreshold
