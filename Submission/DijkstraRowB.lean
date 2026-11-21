import Submission.DijkstraRow

/-!
# Submission.DijkstraRowB — the binary-heap Dijkstra row at every density `n·log^b n`, `0 ≤ b ≤ 1`

Built and checked 2026-11-20 inside `darkhipo/sssp-nlogn` @ 1129aca (Lean v4.34.1, Mathlib d13f23b):
`lake build Submission.DijkstraRowB` passes; axioms are propext, Classical.choice, Quot.sound.

Same program `p1` as `Submission.DijkstraRow` (dispatch `ite (⌊log₂ n⌋ < m/n) BF Dijkstra`),
unchanged. Only the clause-1 arithmetic changes: with `m ≤ n·⌊⌊log₂ n⌋^b⌋` and `b ≤ 1` the run
still takes the Dijkstra branch, and its cost `O((n+m)·log n)` is `O(n·(log n)^(1+b))`.

Instances that beat the best Lean Verified time at their density (currently `n log² n`, covered
down from the `n log n` row, for every `3/4 < b < 1`):

* `Bound 1 (7/8) 1 (15/8) 0`   — `n log^7/8 ; n log^15/8`
* `Bound 1 (5/6) 1 (11/6) 0`   — `n log^5/6 ; n log^11/6`
-/

namespace Submission.DijkstraRowB

open Frontier Frontier.RAM NNReal ENNReal
open BigOSpeedrun.DirectedSSSP
open Submission.DijkstraProg Submission.DijkstraModel Submission.DijkstraDecode
open Submission.DijkstraHeap Submission.DijkstraMain Submission.DijkstraRow

variable {G : Graph} {s : Fin G.n}

/-- Pure real core: with `q ≥ 1`, `L ≤ 1.5ℓ`, `m ≤ 1.5·n·q`, `ℓ ≥ 2.7`, `n ≥ 16`, the Dijkstra
branch's total is at most `2000·n·ℓ·q`. -/
theorem arith_clause1_b {n m L ℓ q : ℝ} (hn : 16 ≤ n) (hl : 2.7 ≤ ℓ) (hL0 : 0 ≤ L)
    (hLb : L ≤ 1.5 * ℓ) (hm0 : 0 ≤ m) (hq : 1 ≤ q) (hm : m ≤ 1.5 * n * q) :
    4 * L + 9 * m + 4 * n + 36 + (60 * L + 123) * (2 * m + 3) ≤ 2000 * (n * (ℓ * q)) := by
  have hn0 : 0 ≤ n := by linarith
  have hl1 : 1 ≤ ℓ := by linarith
  have hq0 : 0 ≤ q := by linarith
  have hlq : 1 ≤ ℓ * q := by nlinarith
  have hN : n ≤ n * (ℓ * q) := by nlinarith
  have hN1 : 1 ≤ n * (ℓ * q) := by nlinarith
  have hq1 : n * q ≤ n * (ℓ * q) := by nlinarith
  have hLN : L ≤ 1.5 * (n * (ℓ * q)) := by
    have : ℓ ≤ n * (ℓ * q) := by nlinarith
    linarith
  have hmN : m ≤ 1.5 * (n * (ℓ * q)) := by nlinarith
  have hLm : L * m ≤ 2.25 * (n * (ℓ * q)) := by
    have h := mul_le_mul hLb hm hm0 (by linarith : (0:ℝ) ≤ 1.5 * ℓ)
    nlinarith [h]
  nlinarith [hLm, hLN, hmN, hN, hN1]

theorem cap_one_b (b : ℚ) (n : ℕ) :
    Cap ((1 : ℚ) / 1) b n = (n : ℝ) * (⌊((Nat.log 2 n : ℕ) : ℝ) ^ (b : ℝ)⌋₊ : ℝ) := by
  simp [Cap]

theorem time_one_b (b' : ℚ) (n : ℕ) :
    Time ((1 : ℚ) / 1) b' ((0 : ℚ) / 1) n = (n : ℝ) * Real.log (n : ℝ) ^ (b' : ℝ) := by
  simp [Time]

/-- Clause 1 at density `n·⌊⌊log₂ n⌋^b⌋`, time `n·(log n)^b'` with `b' = 1 + b`. -/
theorem clause1_b (b b' : ℚ) (hb0 : 0 ≤ b) (hb1 : b ≤ 1) (hb' : b' = 1 + b) :
    ∀ (G : Graph) (s : Fin G.n), 16 ≤ G.n →
      Sparse ((1 : ℚ) / 1) b G.n G.m →
      CorrectWithin p1 G s (2000 * Time ((1 : ℚ) / 1) b' ((0 : ℚ) / 1) G.n) := by
  intro G s hn hsp
  have hbR0 : (0 : ℝ) ≤ (b : ℝ) := by exact_mod_cast hb0
  have hbR1 : (b : ℝ) ≤ 1 := by exact_mod_cast hb1
  set L : ℝ := ((Nat.log 2 G.n : ℕ) : ℝ) with hLdef
  set ℓ : ℝ := Real.log (G.n : ℝ) with hℓdef
  have hnR : (16 : ℝ) ≤ (G.n : ℝ) := by exact_mod_cast hn
  have hℓ : (2.7 : ℝ) ≤ ℓ := log_ge (G := G) hn
  have hℓ0 : 0 < ℓ := by linarith
  have hLb : L ≤ 1.5 * ℓ := L_le_one_five (G := G) hn
  have hL0 : 0 ≤ L := by positivity
  have hL4 : (4 : ℕ) ≤ Nat.log 2 G.n := by
    exact Nat.le_log_of_pow_le (by norm_num) (by simpa using hn)
  have hL1 : (1 : ℝ) ≤ L := by
    have : (4 : ℝ) ≤ L := by rw [hLdef]; exact_mod_cast hL4
    linarith
  -- the cap
  have hsp' : (G.m : ℝ) ≤ (G.n : ℝ) * (⌊L ^ (b : ℝ)⌋₊ : ℝ) := by
    have := hsp; rw [Sparse, cap_one_b] at this; exact this
  have hfl : (⌊L ^ (b : ℝ)⌋₊ : ℝ) ≤ L ^ (b : ℝ) := Nat.floor_le (by positivity)
  have hLbL : L ^ (b : ℝ) ≤ L := by
    calc L ^ (b : ℝ) ≤ L ^ (1 : ℝ) := Real.rpow_le_rpow_of_exponent_le hL1 hbR1
      _ = L := Real.rpow_one L
  have hnR0 : (0 : ℝ) ≤ (G.n : ℝ) := Nat.cast_nonneg _
  have hmLb : (G.m : ℝ) ≤ (G.n : ℝ) * L ^ (b : ℝ) :=
    le_trans hsp' (mul_le_mul_of_nonneg_left hfl hnR0)
  have hmL : (G.m : ℝ) ≤ (G.n : ℝ) * L :=
    le_trans hmLb (mul_le_mul_of_nonneg_left hLbL hnR0)
  -- L^b ≤ 1.5 · ℓ^b
  have hq : L ^ (b : ℝ) ≤ 1.5 * ℓ ^ (b : ℝ) := by
    have h1 : L ^ (b : ℝ) ≤ (1.5 * ℓ) ^ (b : ℝ) := Real.rpow_le_rpow hL0 hLb hbR0
    have h2 : (1.5 * ℓ) ^ (b : ℝ) = (1.5 : ℝ) ^ (b : ℝ) * ℓ ^ (b : ℝ) :=
      Real.mul_rpow (by norm_num) hℓ0.le
    have h3 : (1.5 : ℝ) ^ (b : ℝ) ≤ 1.5 := by
      calc (1.5 : ℝ) ^ (b : ℝ) ≤ (1.5 : ℝ) ^ (1 : ℝ) :=
            Real.rpow_le_rpow_of_exponent_le (by norm_num) hbR1
        _ = 1.5 := Real.rpow_one _
    have h4 : 0 ≤ ℓ ^ (b : ℝ) := by positivity
    rw [h2] at h1
    nlinarith
  have hq1 : (1 : ℝ) ≤ ℓ ^ (b : ℝ) := Real.one_le_rpow (by linarith) hbR0
  have hm15 : (G.m : ℝ) ≤ 1.5 * (G.n : ℝ) * ℓ ^ (b : ℝ) := by
    have := mul_le_mul_of_nonneg_left hq hnR0
    nlinarith [hmLb, this]
  -- dispatch to Dijkstra, same as `DijkstraRow.clause1`
  have hmN : G.m ≤ G.n * Nat.log 2 G.n := by
    have h : (G.m : ℝ) ≤ (G.n : ℝ) * ((Nat.log 2 G.n : ℕ) : ℝ) := by rw [← hLdef]; exact hmL
    exact_mod_cast h
  have hm3 : G.m + 2 ≤ 3 * G.n * (Nat.log 2 G.n + 1) := by
    have hn1 : 1 ≤ G.n := by omega
    nlinarith
  have hKc : Kc G ≤ 60 * Nat.log 2 G.n + 123 := Kc_le (G := G) hm3
  have hdiv : G.m / G.n ≤ Nat.log 2 G.n := Nat.div_le_of_le_mul hmN
  obtain ⟨fuel, r, hr, hsv, hc⟩ := prog_runs_dij (G := G) (s := s) hdiv
  refine ⟨fuel, r, hr, hsv, ?_⟩
  have hrk0 : rk 0 = 0 := rfl
  have hmul := Nat.mul_le_mul_right (2 * G.m + 3) hKc
  have hcostN : r.cost ≤ 4 * Nat.log 2 G.n + 9 * G.m + 4 * G.n + 36
      + (60 * Nat.log 2 G.n + 123) * (2 * G.m + 3) := by omega
  have hcostR : (r.cost : ℝ) ≤ ((4 * Nat.log 2 G.n + 9 * G.m + 4 * G.n + 36
      + (60 * Nat.log 2 G.n + 123) * (2 * G.m + 3) : ℕ) : ℝ) := by exact_mod_cast hcostN
  push_cast at hcostR
  -- the time function
  have htime : Time ((1 : ℚ) / 1) b' ((0 : ℚ) / 1) G.n = (G.n : ℝ) * (ℓ * ℓ ^ (b : ℝ)) := by
    rw [time_one_b, hb']
    push_cast
    rw [Real.rpow_add hℓ0, Real.rpow_one]
  rw [htime]
  exact le_trans hcostR
    (arith_clause1_b hnR hℓ hL0 hLb (Nat.cast_nonneg _) hq1 hm15)

/-- **The family**: `Bound 1 b 1 (1+b) 0` for every `0 ≤ b ≤ 1`, from one program. -/
theorem dijkstra_bound_b (b b' : ℚ) (hb0 : 0 ≤ b) (hb1 : b ≤ 1) (hb' : b' = 1 + b) :
    Bound ((1 : ℚ) / 1) b ((1 : ℚ) / 1) b' ((0 : ℚ) / 1) := by
  refine ⟨p1, ?_, 2000, by norm_num, 16, by norm_num, clause1_b b b' hb0 hb1 hb', clause2⟩
  intro G s
  obtain ⟨f, r, hr, hs, _⟩ := clause2 G s
  exact ⟨f, r, hr, hs⟩

end Submission.DijkstraRowB

/-- Example instance for `Submission.lean`: `n log^7/8 ; n log^15/8`. -/
example : BigOSpeedrun.DirectedSSSP.Bound ((1 : ℚ) / 1) ((7 : ℚ) / 8) ((1 : ℚ) / 1)
    ((15 : ℚ) / 8) ((0 : ℚ) / 1) :=
  Submission.DijkstraRowB.dijkstra_bound_b _ _ (by norm_num) (by norm_num) (by norm_num)
