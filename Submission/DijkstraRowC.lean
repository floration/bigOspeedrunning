import Submission.DijkstraRow

/-!
# Submission.DijkstraRowC — binary-heap Dijkstra at every density up to `n²`

Built and checked 2026-11-20 inside `darkhipo/sssp-nlogn` @ 1129aca (Lean v4.34.1, Mathlib d13f23b): axioms propext, Classical.choice, Quot.sound.

Program `p2`: darkhipo's `prog` with the dispatch threshold raised from `m/n ≤ ⌊log₂ n⌋` to
`m/n ≤ n`, i.e. `seq calcPa (ite (n < m/n) BF.prog dijkstraBody)`. Dijkstra (exact, cost
`O((n+m)·log(m+2))`) now runs on every graph with `m ≤ n²`; Bellman–Ford above that. Since
`log(m+2) = O(log n)` for `m ≤ n²`, the polynomial fallback clause still holds.

Two families of rows (each beats the best Lean Verified time at its density):

* `dijkstra_bound_A`: `Bound 1 b 1 (1+b) 0` for `0 ≤ b ≤ 2` — e.g. `n log^2 ; n log^3`
  (best Lean Verified there today: `n²`).
* `dijkstra_bound_poly`: `Bound a 0 a 1 0` for `1 ≤ a ≤ 2` — e.g. `n^3/2 ; n^3/2 log`
  (best Lean Verified there today: `n²`).
-/

namespace Submission.DijkstraRowC

open Frontier Frontier.RAM WExpr Stmt NNReal ENNReal
open BigOSpeedrun.DirectedSSSP
open Submission.DijkstraProg Submission.DijkstraModel Submission.DijkstraDecode
open Submission.DijkstraSim Submission.DijkstraHeap Submission.DijkstraMain Submission.DijkstraRow

/-! ## The program -/

/-- Dispatch: Bellman–Ford when `n < m/n`, Dijkstra otherwise. -/
def prog2 : Stmt :=
  seq calcPa
    (ite (lt (var "n") (div (var "m") (var "n"))) Frontier.RAM.BF.prog dijkstraBody)

/-- The program (words below `n + m + 2`, no procedures). -/
def p2 : Program := { body := prog2, wordExp := 0 }

variable {G : Graph} {s : Fin G.n}

/-! ## Runs on both sides of the dispatch -/

theorem test_eval2 {st1 : State ℝ≥0} (hF1 : F0 G s st1) :
    evalW st1 (lt (var "n") (div (var "m") (var "n")))
      = some (if G.n < G.m / G.n then 1 else 0) := by
  have hcap1 : 1 < st1.cap := by have := hF1.hcap; omega
  have hmE : evalW st1 (var "m") = some G.m := by rw [evalW_var, hF1.hm]
  have hnE : evalW st1 (var "n") = some G.n := by rw [evalW_var, hF1.hn]
  have hnne : G.n ≠ 0 := by have := s.isLt; omega
  have hdivE : evalW st1 (div (var "m") (var "n")) = some (G.m / G.n) :=
    evalW_div_of hmE hnE hnne
  exact evalW_lt_of hnE hdivE hcap1

theorem prog2_runs_dij (hdiv : G.m / G.n ≤ G.n) :
    Runs realOps prog2 (initState p2 G s) (fun r => r.Solves G s ∧
      r.cost ≤ 4 * Nat.log 2 G.n + 6 + 1 + (4 * G.n + 3 * G.m + 9) + (6 * G.m + 2) + 4
        + (12 * rk 0 + 13) + (Kc G * (2 * G.m + 3) + 1)) := by
  refine runs_seq ((calcPa_runs (G := G) (s := s) (initState p2 G s)
    (F0.init_state (G := G) p2 s)).mono ?_)
  rintro st1 ⟨hF1, hpa1, hc1⟩
  have htest : evalW st1 (lt (var "n") (div (var "m") (var "n"))) = some 0 := by
    rw [test_eval2 hF1, if_neg (by omega)]
  refine runs_ite_false (a := Frontier.RAM.BF.prog) htest ?_
  refine (dijkstra_branch_from (G := G) (s := s) (st := st1) hF1).mono ?_
  rintro r ⟨hsv, hc⟩
  have hinit : (initState p2 G s).cost = 0 := rfl
  exact ⟨hsv, by omega⟩

theorem prog2_runs_bf (hdiv : G.n < G.m / G.n) :
    Runs realOps prog2 (initState p2 G s) (fun r => r.Solves G s ∧
      r.cost ≤ 4 * Nat.log 2 G.n + 6 + 1 + 2 * G.n + 4 + (9 * G.m + 4) * G.n + 1) := by
  refine runs_seq ((calcPa_runs (G := G) (s := s) (initState p2 G s)
    (F0.init_state (G := G) p2 s)).mono ?_)
  rintro st1 ⟨hF1, hpa1, hc1⟩
  have htest : evalW st1 (lt (var "n") (div (var "m") (var "n"))) = some 1 := by
    rw [test_eval2 hF1, if_pos hdiv]
  refine runs_ite_true (b := dijkstraBody) htest (by decide) ?_
  refine (bf_branch_from (G := G) (s := s) (st := st1) hF1).mono ?_
  rintro r ⟨hsv, hc⟩
  have hinit : (initState p2 G s).cost = 0 := rfl
  exact ⟨hsv, by omega⟩

/-! ## The heap constant on `m ≤ n²` -/

theorem log_m_add_two2 (h : G.m + 2 ≤ (G.n + 1) * (G.n + 1)) :
    Nat.log 2 (G.m + 2) ≤ 2 * Nat.log 2 G.n + 3 := by
  have hnlt : G.n < 2 ^ (Nat.log 2 G.n + 1) := by
    have := Nat.lt_pow_succ_log_self (b := 2) (by norm_num) G.n
    simpa [Nat.succ_eq_add_one] using this
  have h1 : G.n + 1 ≤ 2 ^ (Nat.log 2 G.n + 1) := hnlt
  have h2 : (G.n + 1) * (G.n + 1) ≤ 2 ^ (Nat.log 2 G.n + 1) * 2 ^ (Nat.log 2 G.n + 1) :=
    Nat.mul_le_mul h1 h1
  have h3 : 2 ^ (Nat.log 2 G.n + 1) * 2 ^ (Nat.log 2 G.n + 1) < 2 ^ (2 * Nat.log 2 G.n + 4) := by
    rw [← pow_add]
    exact Nat.pow_lt_pow_right (by norm_num) (by omega)
  have hlt : G.m + 2 < 2 ^ (2 * Nat.log 2 G.n + 4) := lt_of_le_of_lt (le_trans h h2) h3
  have hpos : G.m + 2 ≠ 0 := by omega
  have := Nat.log_lt_of_lt_pow (b := 2) (x := 2 * Nat.log 2 G.n + 4) hpos hlt
  omega

theorem Kc_le2 (h : G.m + 2 ≤ (G.n + 1) * (G.n + 1)) :
    Kc G ≤ 60 * Nat.log 2 G.n + 123 := by
  have h3 : Nat.log 2 (G.m + 2) ≤ 2 * Nat.log 2 G.n + 3 := log_m_add_two2 (G := G) h
  have h2 : Nat.log 2 (G.m + 1) ≤ 2 * Nat.log 2 G.n + 3 :=
    le_trans (Nat.log_mono_right (by omega)) h3
  have h4 : rkD (G.m + 1) 0 = Nat.log 2 (G.m + 1) := rkD_zero _
  have h5 : rk (G.m + 1) = Nat.log 2 (G.m + 2) := rfl
  simp only [Kc, h4, h5]
  omega

/-- On the Dijkstra side (`m/n ≤ n`), `m + 2 ≤ (n+1)²`. -/
theorem m_add_two_le (hnpos : 0 < G.n) (hdiv : G.m / G.n ≤ G.n) :
    G.m + 2 ≤ (G.n + 1) * (G.n + 1) := by
  have hlt : G.m < (G.n + 1) * G.n :=
    (Nat.div_lt_iff_lt_mul hnpos).mp (Nat.lt_succ_of_le hdiv)
  nlinarith

/-! ## Clause 2 (polynomial fallback) for `p2` -/

theorem clause2' : ∀ (G : Graph) (s : Fin G.n),
    CorrectWithin p2 G s (2000 * ((G.n : ℝ) + 1) * ((G.m : ℝ) + 1)) := by
  intro G s
  have hnR : (0 : ℝ) ≤ (G.n : ℝ) := Nat.cast_nonneg _
  have hmR : (0 : ℝ) ≤ (G.m : ℝ) := Nat.cast_nonneg _
  have hL0 : (0 : ℝ) ≤ (Nat.log 2 G.n : ℝ) := by positivity
  have hLle : (Nat.log 2 G.n : ℝ) ≤ (G.n : ℝ) := Nat.cast_le.mpr (Nat.log_le_self 2 G.n)
  have hnpos : 0 < G.n := by have := s.isLt; omega
  by_cases hdiv : G.n < G.m / G.n
  · obtain ⟨fuel, r, hr, hsv, hc⟩ := prog2_runs_bf (G := G) (s := s) hdiv
    refine ⟨fuel, r, hr, hsv, ?_⟩
    have hexp : (9 * G.m + 4) * G.n = 9 * G.m * G.n + 4 * G.n := by ring
    have hcostN : r.cost ≤ 4 * Nat.log 2 G.n + 9 * G.m * G.n + 6 * G.n + 12 := by omega
    have hcostR : (r.cost : ℝ) ≤ ((4 * Nat.log 2 G.n + 9 * G.m * G.n + 6 * G.n + 12 : ℕ) : ℝ) := by
      exact_mod_cast hcostN
    push_cast at hcostR
    exact le_trans hcostR (arith_clause2_bf hnR hmR hL0 hLle)
  · push_neg at hdiv
    have hm3 := m_add_two_le (G := G) hnpos hdiv
    have hKc : Kc G ≤ 60 * Nat.log 2 G.n + 123 := Kc_le2 (G := G) hm3
    have hKcn : Kc G ≤ 60 * G.n + 123 := by
      have hLn : Nat.log 2 G.n ≤ G.n := Nat.log_le_self 2 G.n
      omega
    obtain ⟨fuel, r, hr, hsv, hc⟩ := prog2_runs_dij (G := G) (s := s) hdiv
    refine ⟨fuel, r, hr, hsv, ?_⟩
    have hrk0 : rk 0 = 0 := rfl
    have hmul := Nat.mul_le_mul_right (2 * G.m + 3) hKcn
    have hcostN : r.cost ≤ 4 * Nat.log 2 G.n + 9 * G.m + 4 * G.n + 36
        + (60 * G.n + 123) * (2 * G.m + 3) := by omega
    have hcostR : (r.cost : ℝ) ≤ ((4 * Nat.log 2 G.n + 9 * G.m + 4 * G.n + 36
        + (60 * G.n + 123) * (2 * G.m + 3) : ℕ) : ℝ) := by exact_mod_cast hcostN
    push_cast at hcostR
    exact le_trans hcostR (arith_clause2_dij hnR hmR hL0 hLle)

/-! ## Shared clause-1 tail: from `m ≤ n²` to the Dijkstra cost -/

/-- On `m ≤ n·n`, the run is exact and costs at most the Dijkstra total with `Kc ≤ 60L+123`. -/
theorem dij_tail (hn : 16 ≤ G.n) (hmN : G.m ≤ G.n * G.n) :
    ∃ fuel r, p2.run fuel G s = some r ∧ r.Solves G s ∧
      (r.cost : ℝ) ≤ 4 * (Nat.log 2 G.n : ℝ) + 9 * G.m + 4 * G.n + 36
        + (60 * (Nat.log 2 G.n : ℝ) + 123) * (2 * G.m + 3) := by
  have hnpos : 0 < G.n := by omega
  have hdiv : G.m / G.n ≤ G.n := Nat.div_le_of_le_mul hmN
  have hm3 := m_add_two_le (G := G) hnpos hdiv
  have hKc : Kc G ≤ 60 * Nat.log 2 G.n + 123 := Kc_le2 (G := G) hm3
  obtain ⟨fuel, r, hr, hsv, hc⟩ := prog2_runs_dij (G := G) (s := s) hdiv
  refine ⟨fuel, r, hr, hsv, ?_⟩
  have hrk0 : rk 0 = 0 := rfl
  have hmul := Nat.mul_le_mul_right (2 * G.m + 3) hKc
  have hcostN : r.cost ≤ 4 * Nat.log 2 G.n + 9 * G.m + 4 * G.n + 36
      + (60 * Nat.log 2 G.n + 123) * (2 * G.m + 3) := by omega
  have hcostR : (r.cost : ℝ) ≤ ((4 * Nat.log 2 G.n + 9 * G.m + 4 * G.n + 36
      + (60 * Nat.log 2 G.n + 123) * (2 * G.m + 3) : ℕ) : ℝ) := by exact_mod_cast hcostN
  push_cast at hcostR
  exact hcostR

/-! ## Family A: `D = n·⌊⌊log₂ n⌋^b⌋`, `T = n·(log n)^(1+b)`, `0 ≤ b ≤ 2` -/

theorem cap_one_b' (b : ℚ) (n : ℕ) :
    Cap ((1 : ℚ) / 1) b n = (n : ℝ) * (⌊((Nat.log 2 n : ℕ) : ℝ) ^ (b : ℝ)⌋₊ : ℝ) := by
  simp [Cap]

theorem time_one_b' (b' : ℚ) (n : ℕ) :
    Time ((1 : ℚ) / 1) b' ((0 : ℚ) / 1) n = (n : ℝ) * Real.log (n : ℝ) ^ (b' : ℝ) := by
  simp [Time]

/-- `k² ≤ 2^k` for `k ≥ 4`. -/
theorem sq_le_two_pow : ∀ k : ℕ, 4 ≤ k → k ^ 2 ≤ 2 ^ k := by
  intro k hk
  induction k, hk using Nat.le_induction with
  | base => norm_num
  | succ k hk ih =>
    rw [pow_succ 2 k]
    nlinarith

theorem arith_A {n m L ℓ q : ℝ} (hn : 16 ≤ n) (hl : 2.7 ≤ ℓ) (hL0 : 0 ≤ L)
    (hLb : L ≤ 1.5 * ℓ) (hm0 : 0 ≤ m) (hq : 1 ≤ q) (hm : m ≤ 2.25 * n * q) :
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
  have hmN : m ≤ 2.25 * (n * (ℓ * q)) := by nlinarith
  have hLm : L * m ≤ 3.375 * (n * (ℓ * q)) := by
    have h := mul_le_mul hLb hm hm0 (by linarith : (0:ℝ) ≤ 1.5 * ℓ)
    nlinarith [h]
  nlinarith [hLm, hLN, hmN, hN, hN1]

theorem clause1_A (b b' : ℚ) (hb0 : 0 ≤ b) (hb2 : b ≤ 2) (hb' : b' = 1 + b) :
    ∀ (G : Graph) (s : Fin G.n), 16 ≤ G.n →
      Sparse ((1 : ℚ) / 1) b G.n G.m →
      CorrectWithin p2 G s (2000 * Time ((1 : ℚ) / 1) b' ((0 : ℚ) / 1) G.n) := by
  intro G s hn hsp
  have hbR0 : (0 : ℝ) ≤ (b : ℝ) := by exact_mod_cast hb0
  have hbR2 : (b : ℝ) ≤ 2 := by exact_mod_cast hb2
  set L : ℝ := ((Nat.log 2 G.n : ℕ) : ℝ) with hLdef
  set ℓ : ℝ := Real.log (G.n : ℝ) with hℓdef
  have hnR : (16 : ℝ) ≤ (G.n : ℝ) := by exact_mod_cast hn
  have hℓ : (2.7 : ℝ) ≤ ℓ := log_ge (G := G) hn
  have hℓ0 : 0 < ℓ := by linarith
  have hLb : L ≤ 1.5 * ℓ := L_le_one_five (G := G) hn
  have hL0 : 0 ≤ L := by positivity
  have hL4 : (4 : ℕ) ≤ Nat.log 2 G.n := Nat.le_log_of_pow_le (by norm_num) (by simpa using hn)
  have hL1 : (1 : ℝ) ≤ L := by
    have : (4 : ℝ) ≤ L := by rw [hLdef]; exact_mod_cast hL4
    linarith
  -- the cap
  have hsp' : (G.m : ℝ) ≤ (G.n : ℝ) * (⌊L ^ (b : ℝ)⌋₊ : ℝ) := by
    have := hsp; rw [Sparse, cap_one_b'] at this; exact this
  have hfl : (⌊L ^ (b : ℝ)⌋₊ : ℝ) ≤ L ^ (b : ℝ) := Nat.floor_le (by positivity)
  have hnR0 : (0 : ℝ) ≤ (G.n : ℝ) := Nat.cast_nonneg _
  have hmLb : (G.m : ℝ) ≤ (G.n : ℝ) * L ^ (b : ℝ) :=
    le_trans hsp' (mul_le_mul_of_nonneg_left hfl hnR0)
  -- L^b ≤ L² ≤ n
  have hLb2 : L ^ (b : ℝ) ≤ L * L := by
    calc L ^ (b : ℝ) ≤ L ^ (2 : ℝ) := Real.rpow_le_rpow_of_exponent_le hL1 hbR2
      _ = L * L := by rw [Real.rpow_two, sq]
  have hLLn : L * L ≤ (G.n : ℝ) := by
    have h1 : Nat.log 2 G.n ^ 2 ≤ 2 ^ Nat.log 2 G.n := sq_le_two_pow _ hL4
    have h2 : 2 ^ Nat.log 2 G.n ≤ G.n := Nat.pow_log_le_self 2 (by omega)
    have h3 : Nat.log 2 G.n * Nat.log 2 G.n ≤ G.n := by nlinarith
    rw [hLdef]; exact_mod_cast h3
  have hmNN : (G.m : ℝ) ≤ (G.n : ℝ) * (G.n : ℝ) :=
    le_trans hmLb (mul_le_mul_of_nonneg_left (le_trans hLb2 hLLn) hnR0)
  have hmN : G.m ≤ G.n * G.n := by exact_mod_cast hmNN
  -- L^b ≤ 2.25 · ℓ^b
  have hq : L ^ (b : ℝ) ≤ 2.25 * ℓ ^ (b : ℝ) := by
    have h1 : L ^ (b : ℝ) ≤ (1.5 * ℓ) ^ (b : ℝ) := Real.rpow_le_rpow hL0 hLb hbR0
    have h2 : (1.5 * ℓ) ^ (b : ℝ) = (1.5 : ℝ) ^ (b : ℝ) * ℓ ^ (b : ℝ) :=
      Real.mul_rpow (by norm_num) hℓ0.le
    have h3 : (1.5 : ℝ) ^ (b : ℝ) ≤ 2.25 := by
      calc (1.5 : ℝ) ^ (b : ℝ) ≤ (1.5 : ℝ) ^ (2 : ℝ) :=
            Real.rpow_le_rpow_of_exponent_le (by norm_num) hbR2
        _ = 2.25 := by rw [Real.rpow_two]; norm_num
    have h4 : 0 ≤ ℓ ^ (b : ℝ) := by positivity
    rw [h2] at h1
    nlinarith
  have hq1 : (1 : ℝ) ≤ ℓ ^ (b : ℝ) := Real.one_le_rpow (by linarith) hbR0
  have hm225 : (G.m : ℝ) ≤ 2.25 * (G.n : ℝ) * ℓ ^ (b : ℝ) := by
    have := mul_le_mul_of_nonneg_left hq hnR0
    nlinarith [hmLb, this]
  obtain ⟨fuel, r, hr, hsv, hcostR⟩ := dij_tail (G := G) (s := s) hn hmN
  refine ⟨fuel, r, hr, hsv, ?_⟩
  have htime : Time ((1 : ℚ) / 1) b' ((0 : ℚ) / 1) G.n = (G.n : ℝ) * (ℓ * ℓ ^ (b : ℝ)) := by
    rw [time_one_b', hb']
    push_cast
    rw [Real.rpow_add hℓ0, Real.rpow_one]
  rw [htime]
  exact le_trans hcostR (arith_A hnR hℓ hL0 hLb (Nat.cast_nonneg _) hq1 hm225)

/-- **Family A**: `Bound 1 b 1 (1+b) 0` for every `0 ≤ b ≤ 2`. -/
theorem dijkstra_bound_A (b b' : ℚ) (hb0 : 0 ≤ b) (hb2 : b ≤ 2) (hb' : b' = 1 + b) :
    Bound ((1 : ℚ) / 1) b ((1 : ℚ) / 1) b' ((0 : ℚ) / 1) := by
  refine ⟨p2, ?_, 2000, by norm_num, 16, by norm_num, clause1_A b b' hb0 hb2 hb', clause2'⟩
  intro G s
  obtain ⟨f, r, hr, hs, _⟩ := clause2' G s
  exact ⟨f, r, hr, hs⟩

/-! ## Family B: `D = n^a`, `T = n^a·log n`, `1 ≤ a ≤ 2` -/

theorem arith_poly {n m L ℓ M : ℝ} (hn : 16 ≤ n) (hl : 2.7 ≤ ℓ) (hL0 : 0 ≤ L)
    (hLb : L ≤ 1.5 * ℓ) (hm0 : 0 ≤ m) (hnM : n ≤ M) (hm : m ≤ M) :
    4 * L + 9 * m + 4 * n + 36 + (60 * L + 123) * (2 * m + 3) ≤ 2000 * (M * ℓ) := by
  have hM : 16 ≤ M := by linarith
  have hM0 : 0 ≤ M := by linarith
  have hl1 : 1 ≤ ℓ := by linarith
  have hX1 : 1 ≤ M * ℓ := by nlinarith
  have hXM : M ≤ M * ℓ := by nlinarith
  have hXl : ℓ ≤ M * ℓ := by nlinarith
  have hLm : L * m ≤ 1.5 * (M * ℓ) := by
    have h := mul_le_mul hLb hm hm0 (by linarith : (0:ℝ) ≤ 1.5 * ℓ)
    nlinarith [h]
  nlinarith [hLm, hX1, hXM, hXl]

theorem clause1_poly (a : ℚ) (ha1 : 1 ≤ a) (ha2 : a ≤ 2) :
    ∀ (G : Graph) (s : Fin G.n), 16 ≤ G.n →
      Sparse a ((0 : ℚ) / 1) G.n G.m →
      CorrectWithin p2 G s (2000 * Time a ((1 : ℚ) / 1) ((0 : ℚ) / 1) G.n) := by
  intro G s hn hsp
  have haR1 : (1 : ℝ) ≤ (a : ℝ) := by exact_mod_cast ha1
  have haR2 : (a : ℝ) ≤ 2 := by exact_mod_cast ha2
  have hnR : (16 : ℝ) ≤ (G.n : ℝ) := by exact_mod_cast hn
  have hn1 : (1 : ℝ) ≤ (G.n : ℝ) := by linarith
  have hℓ : (2.7 : ℝ) ≤ Real.log (G.n : ℝ) := log_ge (G := G) hn
  have hLb : ((Nat.log 2 G.n : ℕ) : ℝ) ≤ 1.5 * Real.log (G.n : ℝ) := L_le_one_five (G := G) hn
  have hcap : Cap a ((0 : ℚ) / 1) G.n = (G.n : ℝ) ^ (a : ℝ) := by simp [Cap]
  have hsp' : (G.m : ℝ) ≤ (G.n : ℝ) ^ (a : ℝ) := by
    have := hsp; rw [Sparse, hcap] at this; exact this
  have hnM : (G.n : ℝ) ≤ (G.n : ℝ) ^ (a : ℝ) := by
    calc (G.n : ℝ) = (G.n : ℝ) ^ (1 : ℝ) := (Real.rpow_one _).symm
      _ ≤ (G.n : ℝ) ^ (a : ℝ) := Real.rpow_le_rpow_of_exponent_le hn1 haR1
  have hMn2 : (G.n : ℝ) ^ (a : ℝ) ≤ (G.n : ℝ) * (G.n : ℝ) := by
    calc (G.n : ℝ) ^ (a : ℝ) ≤ (G.n : ℝ) ^ (2 : ℝ) := Real.rpow_le_rpow_of_exponent_le hn1 haR2
      _ = (G.n : ℝ) * (G.n : ℝ) := by rw [Real.rpow_two, sq]
  have hmN : G.m ≤ G.n * G.n := by
    have : (G.m : ℝ) ≤ (G.n : ℝ) * (G.n : ℝ) := le_trans hsp' hMn2
    exact_mod_cast this
  obtain ⟨fuel, r, hr, hsv, hcostR⟩ := dij_tail (G := G) (s := s) hn hmN
  refine ⟨fuel, r, hr, hsv, ?_⟩
  have htime : Time a ((1 : ℚ) / 1) ((0 : ℚ) / 1) G.n
      = (G.n : ℝ) ^ (a : ℝ) * Real.log (G.n : ℝ) := by simp [Time]
  rw [htime]
  exact le_trans hcostR
    (arith_poly hnR hℓ (by positivity) hLb (Nat.cast_nonneg _) hnM hsp')

/-- **Family B**: `Bound a 0 a 1 0` for every `1 ≤ a ≤ 2`. -/
theorem dijkstra_bound_poly (a : ℚ) (ha1 : 1 ≤ a) (ha2 : a ≤ 2) :
    Bound a ((0 : ℚ) / 1) a ((1 : ℚ) / 1) ((0 : ℚ) / 1) := by
  refine ⟨p2, ?_, 2000, by norm_num, 16, by norm_num, clause1_poly a ha1 ha2, clause2'⟩
  intro G s
  obtain ⟨f, r, hr, hs, _⟩ := clause2' G s
  exact ⟨f, r, hr, hs⟩

end Submission.DijkstraRowC
