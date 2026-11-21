-- LOCAL STUB: same statement as the Proved platform theorem; heavy imports trimmed, proof replaced by sorry.
import Definitions.Def_SensitivitySeparation
set_option autoImplicit false
set_option maxHeartbeats 0
set_option maxRecDepth 200000

theorem Sensitivity213981.actual_seeds :
∀ (m : Nat),
  @Exists.{1} Nat fun (n : Nat) =>
    @Exists.{1} ((Fin n → Bool) → Bool) fun (f : (Fin n → Bool) → Bool) =>
      And
        (@LE.le.{0} Nat instLENat
          (@HPow.hPow.{0, 0, 0} Nat Nat Nat
            (@instHPow.{0, 0} Nat Nat (@NPow.toPow.{0} Nat (@Monoid.toNPow.{0} Nat Nat.instMonoid)))
            (@OfNat.ofNat.{0} Nat (nat_lit 16) (instOfNatNat (nat_lit 16))) m)
          (@OAI.Paper320.sensitivity (Fin n) (Fin.fintype n) f))
        (And
          (@LE.le.{0} Nat instLENat (@OAI.Paper320.sensitivity (Fin n) (Fin.fintype n) f)
            (@HMul.hMul.{0, 0, 0} Nat Nat Nat (@instHMul.{0} Nat instMulNat)
              (@HPow.hPow.{0, 0, 0} Nat Nat Nat
                (@instHPow.{0, 0} Nat Nat (@NPow.toPow.{0} Nat (@Monoid.toNPow.{0} Nat Nat.instMonoid)))
                (@OfNat.ofNat.{0} Nat (nat_lit 10) (instOfNatNat (nat_lit 10)))
                (@OfNat.ofNat.{0} Nat (nat_lit 15) (instOfNatNat (nat_lit 15))))
              (@HPow.hPow.{0, 0, 0} Nat Nat Nat
                (@instHPow.{0, 0} Nat Nat (@NPow.toPow.{0} Nat (@Monoid.toNPow.{0} Nat Nat.instMonoid)))
                (@OfNat.ofNat.{0} Nat (nat_lit 10121928) (instOfNatNat (nat_lit 10121928))) m)))
          (@LE.le.{0} Nat instLENat
            (@HPow.hPow.{0, 0, 0} Nat Nat Nat
              (@instHPow.{0, 0} Nat Nat (@NPow.toPow.{0} Nat (@Monoid.toNPow.{0} Nat Nat.instMonoid)))
              (@HPow.hPow.{0, 0, 0} Nat Nat Nat
                (@instHPow.{0, 0} Nat Nat (@NPow.toPow.{0} Nat (@Monoid.toNPow.{0} Nat Nat.instMonoid)))
                (@OfNat.ofNat.{0} Nat (nat_lit 5591) (instOfNatNat (nat_lit 5591)))
                (@OfNat.ofNat.{0} Nat (nat_lit 4) (instOfNatNat (nat_lit 4))))
              m)
            (@OAI.Paper320.blockSensitivity (Fin n) (Fin.fintype n) f))) := by sorry
