-- Solution for prove2.me campaign block-sensitivity-vs-sensitivity.
-- Compiled 2026-11-21: Lean v4.33.1, Mathlib 0df444a360eaa60ab8c11dca51a86af692955474, against
-- verbatim statement stubs of the two imported Proved theorems. No errors; axioms: propext,
-- sorryAx (from the stubs only), Classical.choice, Quot.sound.
--
-- Claimed value: log(5591^4) / log(10121928) = log(977142648636961)/log(10121928)
--              = 2.13981365831627068590...
-- Previous best: SensitivityCampaign.reach_213981365 (dmilosch), 2.13981365.
-- Gain: about 8.3e-9. This is the exact limiting exponent of the existing
-- construction, not a new construction.
--
-- Credit:
--   * Seed construction: the twenty-two-level family of yousofy with Codex,
--     Sensitivity213981.actual_seeds
--     (https://prove2.me/theorems/e4a62ddd-b529-418d-98c1-9e04556d9a83),
--     which keeps the OpenAI/math, Robin Kothari with Codex, and community
--     attributions.
--   * `achieves_of_seed_bounds` is copied verbatim from dmilosch's accepted
--     submission 235a7781-0233-4d58-a08b-4b1cc918be52
--     (SensitivityCampaign.reach_213981365). Its logarithmic argument is
--     attributed there to submission a9d25c46-43bd-4fb1-826b-0ed075b8cf0a
--     (yousofy with Codex).
--   * New here: only the final epsilon/2 step that passes from every
--     beta < L to L itself.
--
-- Imports are exactly those of the accepted 2.13981365 solution.

import Theorems.Thm_Sensitivity213981_actual_seeds
import Theorems.Thm_SensitivityCampaign_finite_certificate

set_option autoImplicit false
set_option maxHeartbeats 0
set_option maxRecDepth 200000

namespace SensitivityExactLimit213981
open OAI.Paper320

-- Verbatim from dmilosch, submission 235a7781-0233-4d58-a08b-4b1cc918be52.
theorem achieves_of_seed_bounds (c r g : ℕ) (β : ℝ)
    (hc : 1 < c) (hr : 1 < r) (hg : 1 < g) (hβ : 0 ≤ β)
    (hstrict : β < Real.log (g : ℝ) / Real.log (r : ℝ))
    (hseed : ∀ m : ℕ, ∃ (n : ℕ) (f : (Fin n → Bool) → Bool),
      sensitivity f ≤ c * r ^ m ∧ g ^ m ≤ blockSensitivity f) :
    SensitivityCampaign.AchievesExponent β := by
  classical
  have hcp : (0 : ℝ) < c := by exact_mod_cast (by omega : 0 < c)
  have hr1 : (1 : ℝ) < r := by exact_mod_cast hr
  have hlr : 0 < Real.log (r : ℝ) := Real.log_pos hr1
  have hgap : 0 < Real.log (g : ℝ) - β * Real.log (r : ℝ) := by
    have hh := (lt_div_iff₀ hlr).mp hstrict
    linarith
  let δ := Real.log (g : ℝ) - β * Real.log (r : ℝ)
  obtain ⟨m, hm⟩ := exists_nat_gt (max 0 (β * Real.log (c : ℝ) / δ))
  have hmposr : (0 : ℝ) < m := (le_max_left _ _).trans_lt hm
  have hmpos : 0 < m := by exact_mod_cast hmposr
  have hmul : β * Real.log (c : ℝ) < (m : ℝ) * δ :=
    (div_lt_iff₀ hgap).mp ((le_max_right _ _).trans_lt hm)
  obtain ⟨n, f, hs, hb⟩ := hseed m
  obtain ⟨x, _, hx⟩ := Finset.exists_mem_eq_sup
    (Finset.univ : Finset (Fin n → Bool)) Finset.univ_nonempty (blockSensitivityAt f)
  have hsup : blockSensitivity f =
      (Finset.univ : Finset (Fin n → Bool)).sup (blockSensitivityAt f) := by
    unfold blockSensitivity
    congr 1
    ext y
    simp
  have hbx : g^m ≤ blockSensitivityAt f x := by
    exact hb.trans_eq (hsup.trans hx)
  have hA : 1 < c * r ^ m :=
    hc.trans_le (Nat.le_mul_of_pos_right c (pow_pos (by omega : 0 < r) m))
  have hB : 1 < g ^ m := one_lt_pow₀ hg (Nat.ne_of_gt hmpos)
  apply SensitivityCampaign.finite_certificate f x
    (c * r ^ m) (g ^ m) β hA hB hβ hs hbx
  have hrp : (0 : ℝ) < r := by linarith
  have hp : (0 : ℝ) < (c * r ^ m : ℕ) := by
    exact_mod_cast (by omega : 0 < c * r ^ m)
  have hbp : (0 : ℝ) < (g ^ m : ℕ) := by
    exact_mod_cast (by omega : 0 < g ^ m)
  apply (Real.rpow_le_iff_le_log hp hbp).2
  push_cast
  rw [Real.log_mul (ne_of_gt hcp) (ne_of_gt (pow_pos hrp m)),
    Real.log_pow, Real.log_pow]
  dsimp only [δ] at hmul
  nlinarith

/-- Every exponent strictly below the seed family's rate is achievable. -/
theorem achieves_below (β : ℝ) (hβ : 0 ≤ β)
    (hstrict : β < Real.log (977142648636961 : ℝ) / Real.log (10121928 : ℝ)) :
    SensitivityCampaign.AchievesExponent β := by
  have hcast : ((5591 ^ 4 : ℕ) : ℝ) = (977142648636961 : ℝ) := by norm_num
  have hstrict' : β < Real.log ((5591 ^ 4 : ℕ) : ℝ) / Real.log (10121928 : ℝ) := by
    rw [hcast]
    exact hstrict
  apply achieves_of_seed_bounds (10^15) 10121928 (5591^4) β
    (by norm_num) (by norm_num) (by norm_num) hβ hstrict'
  intro m
  obtain ⟨n, f, _, hs, hb⟩ := Sensitivity213981.actual_seeds m
  exact ⟨n, f, hs, hb⟩

/-- The exact limiting exponent: use the strict result at `L - ε/2` with slack `ε/2`. -/
theorem reaches_exact :
    SensitivityCampaign.AchievesExponent
      (Real.log (977142648636961 : ℝ) / Real.log (10121928 : ℝ)) := by
  unfold SensitivityCampaign.AchievesExponent
  intro ε hε S hS
  have hLpos : 0 < Real.log (977142648636961 : ℝ) / Real.log (10121928 : ℝ) :=
    div_pos (Real.log_pos (by norm_num)) (Real.log_pos (by norm_num))
  have hβ0 : (0 : ℝ) ≤
      max 0 (Real.log (977142648636961 : ℝ) / Real.log (10121928 : ℝ) - ε / 2) :=
    le_max_left _ _
  have hβL : max 0 (Real.log (977142648636961 : ℝ) / Real.log (10121928 : ℝ) - ε / 2) <
      Real.log (977142648636961 : ℝ) / Real.log (10121928 : ℝ) :=
    max_lt hLpos (by linarith)
  have hβge : Real.log (977142648636961 : ℝ) / Real.log (10121928 : ℝ) - ε / 2 ≤
      max 0 (Real.log (977142648636961 : ℝ) / Real.log (10121928 : ℝ) - ε / 2) :=
    le_max_right _ _
  have hach := achieves_below _ hβ0 hβL
  unfold SensitivityCampaign.AchievesExponent at hach
  obtain ⟨n, f, hSs, hpow⟩ := hach (ε / 2) (by linarith) S hS
  refine ⟨n, f, hSs, le_trans ?_ hpow⟩
  have hs1 : (1 : ℝ) ≤ (OAI.Paper320.sensitivity f : ℝ) := by
    have h1 : 1 ≤ OAI.Paper320.sensitivity f := le_trans (by omega) hSs
    exact_mod_cast h1
  apply Real.rpow_le_rpow_of_exponent_le hs1
  linarith

end SensitivityExactLimit213981

theorem solution :
    SensitivityCampaign.AchievesExponent
      (Real.log (977142648636961 : ℝ) / Real.log (10121928 : ℝ)) :=
  SensitivityExactLimit213981.reaches_exact

#print axioms solution
