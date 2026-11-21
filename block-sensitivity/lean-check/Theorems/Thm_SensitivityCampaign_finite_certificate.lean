-- LOCAL STUB of the Proved platform theorem (statement verbatim, proof sorry).

import Mathlib
import Definitions.Def_SensitivityCampaign
open OAI.Paper320

theorem SensitivityCampaign.finite_certificate
    {n : ℕ} (f : (Fin n → Bool) → Bool) (x : Fin n → Bool)
    (A B : ℕ) (a : ℝ)
    (hA : 1 < A) (hB : 1 < B) (ha : 0 ≤ a)
    (hs : sensitivity f ≤ A) (hb : B ≤ blockSensitivityAt f x)
    (hpow : (A : ℝ) ^ a ≤ (B : ℝ)) :
    SensitivityCampaign.AchievesExponent a := by sorry
