import Submission.DijkstraRowC
import Frontier.CHD.Final
import Mathlib.Analysis.MeanInequalitiesPow

/-!
# Submission.PadCHD — C-HD above its density cap, by padding with isolated vertices

DRAFT, NOT YET BUILT (written 2026-11-21). Build inside `darkhipo/sssp-nlogn` @ 1129aca, with
`Submission/DijkstraRowB.lean` and `Submission/DijkstraRowC.lean` present.

Idea. `Frontier.CHD.Final.chd_exact_within` bounds the C-HD program on EVERY graph by
`K · Tdisp F n m`, and `Tdisp F n m = Tchd n m` once `m ≤ n · F n`, `F n = ⌊⌊log₂ n⌋^{3/4}⌋`.
On a dense graph we add `⌊m / F n⌋ + 1` isolated vertices (`n' = n + ⌊m/F n⌋ + 1`), which puts
the graph under C-HD's own cap and leaves every distance unchanged. Then

    Tchd n' m = O(n + m·(log n)^{1/6} + m^{1/3}·(n log n)^{2/3}),

so on `m ≤ n·⌊log₂ n⌋^b` with `3/4 ≤ b ≤ 2` the time is `O(n·(log n)^{b+1/6})`, and on
`m ≤ n^a` with `1 < a ≤ 2` it is `O(n^a·(log n)^{1/6})`.

The program `p3` (word exponent 321, procedure table of `chdProgram`):

    if n < 65536 then prog2                       -- darkhipo-style Dijkstra / Bellman–Ford
    else if n < m / n then prog2                  -- m > n²: Bellman–Ford inside prog2
    else  logProg; thrProg;                       -- pa := ⌊log₂ n⌋, pr := F n
          zzPadN0 := n; n := n + m / pr + 1;      -- save n, pad
          px, pa, py, pr := 0;                    -- the state is now C-HD's initial state of G'
          chdProgram.body;                        -- (up to cap, cost and register zzPadN0)
          copy reach[0..n), dist[0..n) back into arrays of length n

The splice needs one general fact about the machine (`exec_tw`): a run that does not mention a
register `x` is unchanged by raising the word cap, shifting the cost counter, and setting `x`.
`x ∉ names chdProgram` is checked by `decide`.
-/

open scoped NNReal ENNReal

namespace Submission.PadCHD

open Frontier Frontier.RAM WExpr Stmt
open BigOSpeedrun.DirectedSSSP
open Submission.DijkstraProg Submission.DijkstraModel Submission.DijkstraDecode
open Submission.DijkstraSim Submission.DijkstraHeap Submission.DijkstraMain Submission.DijkstraRow
open Submission.DijkstraRowC
open Frontier.CHD.Dispatch (root4 root4_le lt_root4_succ_pow F_eq_root4 logProg thrProg
  logProg_runs thrProg_runs Agree)

/-! ## 1. A frame lemma for the machine -/

section Frame

variable {V : Type} {ops : VOps V}

/-- Word registers read by a word expression. -/
def wv : WExpr → List String
  | .lit _ => []
  | .var y => [y]
  | .add a b => wv a ++ wv b
  | .sub a b => wv a ++ wv b
  | .mul a b => wv a ++ wv b
  | .div a b => wv a ++ wv b
  | .lt a b => wv a ++ wv b
  | .eq a b => wv a ++ wv b
  | .load _ i => wv i

/-- Word registers read by a value expression. -/
def vv : VExpr → List String
  | .zero => []
  | .var _ => []
  | .add a b => vv a ++ vv b
  | .load _ i => wv i

/-- Word registers read or written by a statement (not following calls). -/
def names : Stmt → List String
  | .skip => []
  | .wset y e => y :: wv e
  | .vset _ e => vv e
  | .vle y a b => y :: (vv a ++ vv b)
  | .wstore _ i e => wv i ++ wv e
  | .vstore _ i e => wv i ++ vv e
  | .walloc _ e => wv e
  | .valloc _ e => wv e
  | .seq a b => names a ++ names b
  | .ite c a b => wv c ++ (names a ++ names b)
  | .while c b => wv c ++ names b
  | .call _ => []

/-- Raise the cap to `c`, add `k` to the cost, and set register `x` to `a`. -/
def tw (t : State V) (x : String) (a c k : ℕ) : State V :=
  { t with w := fun y => if y = x then a else t.w y, cap := c, cost := t.cost + k }

@[simp] theorem tw_w (t : State V) (x : String) (a c k : ℕ) (y : String) :
    (tw t x a c k).w y = if y = x then a else t.w y := rfl
@[simp] theorem tw_v (t : State V) (x : String) (a c k : ℕ) : (tw t x a c k).v = t.v := rfl
@[simp] theorem tw_wa (t : State V) (x : String) (a c k : ℕ) : (tw t x a c k).wa = t.wa := rfl
@[simp] theorem tw_va (t : State V) (x : String) (a c k : ℕ) : (tw t x a c k).va = t.va := rfl
@[simp] theorem tw_wlen (t : State V) (x : String) (a c k : ℕ) :
    (tw t x a c k).wlen = t.wlen := rfl
@[simp] theorem tw_vlen (t : State V) (x : String) (a c k : ℕ) :
    (tw t x a c k).vlen = t.vlen := rfl
@[simp] theorem tw_cap (t : State V) (x : String) (a c k : ℕ) : (tw t x a c k).cap = c := rfl
@[simp] theorem tw_cost (t : State V) (x : String) (a c k : ℕ) :
    (tw t x a c k).cost = t.cost + k := rfl
@[simp] theorem tw_space (t : State V) (x : String) (a c k : ℕ) :
    (tw t x a c k).space = t.space := rfl
@[simp] theorem tw_procs (t : State V) (x : String) (a c k : ℕ) :
    (tw t x a c k).procs = t.procs := rfl

theorem st_ext {s t : State V} (hw : ∀ y, s.w y = t.w y) (hv : s.v = t.v) (hwa : s.wa = t.wa)
    (hva : s.va = t.va) (hwl : s.wlen = t.wlen) (hvl : s.vlen = t.vlen) (hc : s.cap = t.cap)
    (hco : s.cost = t.cost) (hs : s.space = t.space) (hp : s.procs = t.procs) : s = t := by
  cases s
  cases t
  simp only [State.mk.injEq]
  exact ⟨funext hw, hv, hwa, hva, hwl, hvl, hc, hco, hs, hp⟩

theorem tw_setW {t : State V} {x y : String} {a c k v : ℕ} (hy : y ≠ x) :
    (tw t x a c k).setW y v = tw (t.setW y v) x a c k := by
  refine st_ext (fun z => ?_) rfl rfl rfl rfl rfl rfl rfl rfl rfl
  simp only [State.setW, tw]
  by_cases h1 : z = y <;> by_cases h2 : z = x <;> simp_all

theorem tw_charge {t : State V} {x : String} {a c k j : ℕ} :
    (tw t x a c k).charge j = tw (t.charge j) x a c k := by
  refine st_ext (fun _ => rfl) rfl rfl rfl rfl rfl rfl ?_ rfl rfl
  simp only [State.charge, tw]
  omega

theorem tw_enter {t : State V} {x : String} {a c k : ℕ} :
    (tw t x a c k).enter = tw t.enter x a c k := by
  refine st_ext (fun _ => rfl) rfl rfl rfl rfl rfl rfl ?_ rfl rfl
  simp only [State.enter, tw]
  omega

theorem tw_setV {t : State V} {x z : String} {a c k : ℕ} {v : V} :
    (tw t x a c k).setV z v = tw (t.setV z v) x a c k := rfl

theorem tw_storeW {t : State V} {x arr : String} {a c k i v : ℕ} :
    (tw t x a c k).storeW arr i v = tw (t.storeW arr i v) x a c k := rfl

theorem tw_storeV {t : State V} {x arr : String} {a c k i : ℕ} {v : V} :
    (tw t x a c k).storeV arr i v = tw (t.storeV arr i v) x a c k := rfl

theorem tw_allocW {t : State V} {x arr : String} {a c k n : ℕ} :
    (tw t x a c k).allocW arr n = tw (t.allocW arr n) x a c k := rfl

theorem tw_allocV {t : State V} {x arr : String} {a c k n : ℕ} {z : V} :
    (tw t x a c k).allocV arr n z = tw (t.allocV arr n z) x a c k := rfl

theorem fit_mono {c1 c2 b v : ℕ} (h : fit c1 b = some v) (hc : c1 ≤ c2) : fit c2 b = some v := by
  unfold fit at h ⊢
  by_cases h1 : b < c1
  · rw [if_pos h1] at h
    rw [if_pos (by omega)]
    exact h
  · rw [if_neg h1] at h
    exact absurd h (by simp)

theorem evalW_tw {t : State V} {x : String} {a c k : ℕ} (hc : t.cap ≤ c) :
    ∀ {e : WExpr} {v : ℕ}, x ∉ wv e → evalW t e = some v → evalW (tw t x a c k) e = some v := by
  intro e
  induction e with
  | lit b =>
    intro v _ h
    simp only [evalW, tw_cap] at h ⊢
    exact fit_mono h hc
  | var y =>
    intro v hx h
    simp only [wv, List.mem_singleton] at hx
    simp only [evalW] at h ⊢
    rw [tw_w, if_neg (fun h' => hx h'.symm)]
    exact h
  | add p q ihp ihq =>
    intro v hx h
    simp only [wv, List.mem_append, not_or] at hx
    simp only [evalW, Option.bind_eq_bind, Option.bind_eq_some_iff] at h ⊢
    obtain ⟨u1, h1, u2, h2, h3⟩ := h
    exact ⟨u1, ihp hx.1 h1, u2, ihq hx.2 h2, by simpa only [tw_cap] using fit_mono h3 hc⟩
  | sub p q ihp ihq =>
    intro v hx h
    simp only [wv, List.mem_append, not_or] at hx
    simp only [evalW, Option.bind_eq_bind, Option.bind_eq_some_iff] at h ⊢
    obtain ⟨u1, h1, u2, h2, h3⟩ := h
    exact ⟨u1, ihp hx.1 h1, u2, ihq hx.2 h2, h3⟩
  | mul p q ihp ihq =>
    intro v hx h
    simp only [wv, List.mem_append, not_or] at hx
    simp only [evalW, Option.bind_eq_bind, Option.bind_eq_some_iff] at h ⊢
    obtain ⟨u1, h1, u2, h2, h3⟩ := h
    exact ⟨u1, ihp hx.1 h1, u2, ihq hx.2 h2, by simpa only [tw_cap] using fit_mono h3 hc⟩
  | div p q ihp ihq =>
    intro v hx h
    simp only [wv, List.mem_append, not_or] at hx
    simp only [evalW, Option.bind_eq_bind, Option.bind_eq_some_iff] at h ⊢
    obtain ⟨u1, h1, u2, h2, h3⟩ := h
    exact ⟨u1, ihp hx.1 h1, u2, ihq hx.2 h2, h3⟩
  | lt p q ihp ihq =>
    intro v hx h
    simp only [wv, List.mem_append, not_or] at hx
    simp only [evalW, Option.bind_eq_bind, Option.bind_eq_some_iff] at h ⊢
    obtain ⟨u1, h1, u2, h2, h3⟩ := h
    exact ⟨u1, ihp hx.1 h1, u2, ihq hx.2 h2, by simpa only [tw_cap] using fit_mono h3 hc⟩
  | eq p q ihp ihq =>
    intro v hx h
    simp only [wv, List.mem_append, not_or] at hx
    simp only [evalW, Option.bind_eq_bind, Option.bind_eq_some_iff] at h ⊢
    obtain ⟨u1, h1, u2, h2, h3⟩ := h
    exact ⟨u1, ihp hx.1 h1, u2, ihq hx.2 h2, by simpa only [tw_cap] using fit_mono h3 hc⟩
  | load arr i ih =>
    intro v hx h
    simp only [wv] at hx
    simp only [evalW, Option.bind_eq_bind, Option.bind_eq_some_iff] at h ⊢
    obtain ⟨j, h1, h2⟩ := h
    exact ⟨j, ih hx h1, h2⟩

theorem evalV_tw {t : State V} {x : String} {a c k : ℕ} (hc : t.cap ≤ c) :
    ∀ {e : VExpr} {v : V}, x ∉ vv e → evalV ops t e = some v →
      evalV ops (tw t x a c k) e = some v := by
  intro e
  induction e with
  | zero => intro v _ h; exact h
  | var y => intro v _ h; exact h
  | add p q ihp ihq =>
    intro v hx h
    simp only [vv, List.mem_append, not_or] at hx
    simp only [evalV, Option.bind_eq_bind, Option.bind_eq_some_iff] at h ⊢
    obtain ⟨u1, h1, u2, h2, h3⟩ := h
    exact ⟨u1, ihp hx.1 h1, u2, ihq hx.2 h2, h3⟩
  | load arr i =>
    intro v hx h
    simp only [vv] at hx
    simp only [evalV, Option.bind_eq_bind, Option.bind_eq_some_iff] at h ⊢
    obtain ⟨j, h1, h2⟩ := h
    exact ⟨j, evalW_tw hc hx h1, h2⟩

/-- **The frame lemma.** -/
theorem exec_tw {x : String} {a c k : ℕ} :
    ∀ (f : ℕ) (st : Stmt) (t r : State V), exec ops f st t = some r → t.cap ≤ c →
      x ∉ names st → (∀ q ∈ t.procs, x ∉ names q) →
      exec ops f st (tw t x a c k) = some (tw r x a c k) ∧ r.cap = t.cap ∧ r.procs = t.procs
  | 0, _, _, _, h, _, _, _ => by simp [exec] at h
  | f + 1, st, t, r, h, hc, hx, hp => by
    cases st with
    | skip =>
      simp [exec] at h
      subst h
      refine ⟨?_, rfl, rfl⟩
      show some ((tw t x a c k).charge 1) = some (tw (t.charge 1) x a c k)
      rw [tw_charge]
    | wset y e =>
      simp only [exec, Option.bind_eq_bind, Option.bind_eq_some_iff] at h
      obtain ⟨v, hv, h⟩ := h
      simp at h
      subst h
      simp only [names, List.mem_cons, not_or] at hx
      refine ⟨?_, rfl, rfl⟩
      have hv' := evalW_tw (a := a) (k := k) hc hx.2 hv
      simp [exec, hv', tw_setW (fun h' => hx.1 h'.symm), tw_charge]
    | vset y e =>
      simp only [exec, Option.bind_eq_bind, Option.bind_eq_some_iff] at h
      obtain ⟨v, hv, h⟩ := h
      simp at h
      subst h
      simp only [names] at hx
      refine ⟨?_, rfl, rfl⟩
      have hv' := evalV_tw (ops := ops) (a := a) (k := k) hc hx hv
      simp [exec, hv', tw_setV, tw_charge]
    | vle y p q =>
      simp only [exec, Option.bind_eq_bind, Option.bind_eq_some_iff] at h
      obtain ⟨pv, hpv, qv, hqv, bit, hb, h⟩ := h
      simp at h
      subst h
      simp only [names, List.mem_cons, List.mem_append, not_or] at hx
      refine ⟨?_, rfl, rfl⟩
      have hp' := evalV_tw (ops := ops) (a := a) (k := k) hc hx.2.1 hpv
      have hq' := evalV_tw (ops := ops) (a := a) (k := k) hc hx.2.2 hqv
      have hb' := fit_mono hb hc
      simp [exec, hp', hq', hb', tw_setW (fun h' => hx.1 h'.symm), tw_charge]
    | wstore arr i e =>
      simp only [exec, Option.bind_eq_bind, Option.bind_eq_some_iff] at h
      obtain ⟨j, hj, v, hv, h⟩ := h
      split_ifs at h with hlt
      simp at h
      subst h
      simp only [names, List.mem_append, not_or] at hx
      refine ⟨?_, rfl, rfl⟩
      have hj' := evalW_tw (a := a) (k := k) hc hx.1 hj
      have hv' := evalW_tw (a := a) (k := k) hc hx.2 hv
      simp [exec, hj', hv', hlt, tw_storeW, tw_charge]
    | vstore arr i e =>
      simp only [exec, Option.bind_eq_bind, Option.bind_eq_some_iff] at h
      obtain ⟨j, hj, v, hv, h⟩ := h
      split_ifs at h with hlt
      simp at h
      subst h
      simp only [names, List.mem_append, not_or] at hx
      refine ⟨?_, rfl, rfl⟩
      have hj' := evalW_tw (a := a) (k := k) hc hx.1 hj
      have hv' := evalV_tw (ops := ops) (a := a) (k := k) hc hx.2 hv
      simp [exec, hj', hv', hlt, tw_storeV, tw_charge]
    | walloc arr e =>
      simp only [exec, Option.bind_eq_bind, Option.bind_eq_some_iff] at h
      obtain ⟨kk, hk, h⟩ := h
      simp at h
      subst h
      simp only [names] at hx
      refine ⟨?_, rfl, rfl⟩
      have hk' := evalW_tw (a := a) (k := k) hc hx hk
      simp [exec, hk', tw_allocW, tw_charge]
    | valloc arr e =>
      simp only [exec, Option.bind_eq_bind, Option.bind_eq_some_iff] at h
      obtain ⟨kk, hk, h⟩ := h
      simp at h
      subst h
      simp only [names] at hx
      refine ⟨?_, rfl, rfl⟩
      have hk' := evalW_tw (a := a) (k := k) hc hx hk
      simp [exec, hk', tw_allocV, tw_charge]
    | seq p q =>
      rw [exec_seq, Option.bind_eq_some_iff] at h
      obtain ⟨s', h1, h2⟩ := h
      simp only [names, List.mem_append, not_or] at hx
      obtain ⟨e1, c1, p1⟩ := exec_tw (x := x) (a := a) (c := c) (k := k) f p t s' h1 hc hx.1 hp
      obtain ⟨e2, c2, p2⟩ := exec_tw (x := x) (a := a) (c := c) (k := k) f q s' r h2
        (c1.trans_le hc) hx.2 (by rw [p1]; exact hp)
      refine ⟨?_, c2.trans c1, p2.trans p1⟩
      rw [exec_seq, e1]
      exact e2
    | ite cnd p q =>
      rw [exec_ite, Option.bind_eq_some_iff] at h
      obtain ⟨xv, hxv, h2⟩ := h
      simp only [names, List.mem_append, not_or] at hx
      have hxv' := evalW_tw (a := a) (k := k) hc hx.1 hxv
      split_ifs at h2 with hz
      · obtain ⟨e1, c1, p1⟩ := exec_tw (x := x) (a := a) (c := c) (k := k) f p (t.charge 1) r h2
          hc hx.2.1 hp
        refine ⟨?_, c1, p1⟩
        rw [exec_ite, hxv']
        simp only [Option.bind_some, ne_eq, hz, not_false_eq_true, ite_true]
        rw [tw_charge]
        exact e1
      · obtain ⟨e1, c1, p1⟩ := exec_tw (x := x) (a := a) (c := c) (k := k) f q (t.charge 1) r h2
          hc hx.2.2 hp
        refine ⟨?_, c1, p1⟩
        rw [exec_ite, hxv']
        simp only [Option.bind_some]
        rw [if_neg hz, tw_charge]
        exact e1
    | «while» cnd b =>
      rw [exec_while, Option.bind_eq_some_iff] at h
      obtain ⟨xv, hxv, h2⟩ := h
      have hx' := hx
      simp only [names, List.mem_append, not_or] at hx'
      have hxv' := evalW_tw (a := a) (k := k) hc hx'.1 hxv
      split_ifs at h2 with hz
      · rw [Option.bind_eq_some_iff] at h2
        obtain ⟨s', h3, h4⟩ := h2
        obtain ⟨e1, c1, p1⟩ := exec_tw (x := x) (a := a) (c := c) (k := k) f b (t.charge 1) s' h3
          hc hx'.2 hp
        obtain ⟨e2, c2, p2⟩ := exec_tw (x := x) (a := a) (c := c) (k := k) f (.while cnd b) s' r h4
          (c1.trans_le hc) hx (by rw [p1]; exact hp)
        refine ⟨?_, c2.trans c1, p2.trans p1⟩
        rw [exec_while, hxv']
        simp only [Option.bind_some, ne_eq, hz, not_false_eq_true, ite_true]
        rw [tw_charge, e1]
        exact e2
      · simp at h2
        subst h2
        refine ⟨?_, rfl, rfl⟩
        rw [exec_while, hxv']
        simp only [Option.bind_some]
        rw [if_neg hz, tw_charge]
    | call pn =>
      rw [exec_call] at h
      cases hb : t.procs[pn]? with
      | none => rw [hb] at h; exact absurd h (by simp)
      | some body =>
        rw [hb] at h
        have hbody : x ∉ names body := hp body (List.mem_of_getElem? hb)
        obtain ⟨e1, c1, p1⟩ := exec_tw (x := x) (a := a) (c := c) (k := k) f body t.enter r h hc
          hbody hp
        refine ⟨?_, c1, p1⟩
        rw [exec_call, show (tw t x a c k).procs = t.procs from rfl, hb]
        rw [tw_enter]
        exact e1

end Frame

/-- The register that keeps the original vertex count across the C-HD run. -/
def ZN : String := "zzPadN0"

/-- `ZN` is never mentioned by the C-HD program text (checked by the kernel). -/
theorem names_body : ZN ∉ names Frontier.CHD.Final.chdProgram.body := by decide +kernel

theorem names_procs : ∀ q ∈ Frontier.CHD.Final.chdProgram.procs, ZN ∉ names q := by
  decide +kernel

/-! ## 2. The padded graph -/

/-- `G` with `n' - G.n` extra isolated vertices. -/
def pad (G : Graph) (n' : ℕ) (h : G.n ≤ n') : Graph :=
  ⟨n', G.m, fun e => Fin.castLE h (G.src e), fun e => Fin.castLE h (G.dst e), G.w⟩

theorem walk_pad_of {G : Graph} {n' : ℕ} {h : G.n ≤ n'} {u v : Fin G.n} {p : List (Fin G.m)}
    (hw : G.IsWalk u v p) : (pad G n' h).IsWalk (Fin.castLE h u) (Fin.castLE h v) p := by
  induction hw with
  | nil u => exact Graph.IsWalk.nil _
  | cons _ ih => exact Graph.IsWalk.cons ih

theorem walk_of_pad {G : Graph} {n' : ℕ} {h : G.n ≤ n'} {v' : Fin n'} (v : Fin G.n)
    (hv : (v' : ℕ) = v) :
    ∀ (p : List (Fin G.m)) (u' : Fin n'), (pad G n' h).IsWalk u' v' p →
      ∃ u : Fin G.n, (u : ℕ) = u' ∧ G.IsWalk u v p
  | [], u', hw => by
    have huv : u' = v' := (Graph.isWalk_nil_iff (G := pad G n' h)).mp hw
    subst huv
    exact ⟨v, hv.symm, Graph.IsWalk.nil v⟩
  | e :: q, u', hw => by
    obtain ⟨hsrc, hw'⟩ := (Graph.isWalk_cons_iff (G := pad G n' h)).mp hw
    obtain ⟨u0, hu0, hw0⟩ := walk_of_pad v hv q _ hw'
    have hu : u0 = G.dst e := Fin.ext (by simpa [pad] using hu0)
    subst hu
    refine ⟨G.src e, ?_, Graph.IsWalk.cons hw0⟩
    rw [← hsrc]
    rfl

theorem walk_pad_iff {G : Graph} {n' : ℕ} {h : G.n ≤ n'} {u v : Fin G.n} {p : List (Fin G.m)} :
    (pad G n' h).IsWalk (Fin.castLE h u) (Fin.castLE h v) p ↔ G.IsWalk u v p := by
  constructor
  · intro hw
    obtain ⟨u0, hu0, hw0⟩ := walk_of_pad (n' := n') (h := h) (v' := Fin.castLE h v) v rfl p _ hw
    have : u0 = u := Fin.ext hu0
    subst this
    exact hw0
  · exact walk_pad_of

theorem pad_dist (G : Graph) (n' : ℕ) (h : G.n ≤ n') (s v : Fin G.n) :
    (pad G n' h).dist (Fin.castLE h s) (Fin.castLE h v) = G.dist s v := by
  unfold Graph.dist
  refine iInf_congr (fun p => ?_)
  exact iInf_congr_Prop walk_pad_iff (fun _ => rfl)

/-! ## 3. The program -/

/-- The padded vertex count `n + ⌊m / F n⌋ + 1`. -/
def npad (n m : ℕ) : ℕ := n + m / GateCCalc.F n + 1

/-- Save `n`, pad, and clear the dispatcher scratch registers. -/
def padSetup : Stmt :=
  seq logProg
    (seq thrProg
      (seq (wset ZN (var "n"))
        (seq (wset "n" (add (add (var "n") (div (var "m") (var "pr"))) (lit 1)))
          (seq (wset "px" (lit 0))
            (seq (wset "pa" (lit 0))
              (seq (wset "py" (lit 0)) (wset "pr" (lit 0))))))))

/-- One copy step `A[i] := B[i]; C[i] := D[i]; i := i + 1`. -/
def copyStep (A B C D : String) : Stmt :=
  seq (wstore A (var "zzI") (load B (var "zzI")))
    (seq (vstore C (var "zzI") (VExpr.load D (var "zzI")))
      (wset "zzI" (add (var "zzI") (lit 1))))

def copy1 : Stmt := copyStep "zzR" "reach" "zzD" "dist"
def copy2 : Stmt := copyStep "reach" "zzR" "dist" "zzD"

/-- Truncate the output arrays to the original `n` (kept in `ZN`). -/
def post : Stmt :=
  seq (walloc "zzR" (var ZN))
    (seq (valloc "zzD" (var ZN))
      (seq (wset "zzI" (lit 0))
        (seq (.while (lt (var "zzI") (var ZN)) copy1)
          (seq (walloc "reach" (var ZN))
            (seq (valloc "dist" (var ZN))
              (seq (wset "zzI" (lit 0)) (.while (lt (var "zzI") (var ZN)) copy2)))))))

def padPath : Stmt := seq padSetup (seq Frontier.CHD.Final.chdProgram.body post)

def body3 : Stmt :=
  ite (lt (var "n") (lit 65536)) prog2
    (ite (lt (var "n") (div (var "m") (var "n"))) prog2 padPath)

def p3 : Program :=
  { body := body3, wordExp := 321, procs := Frontier.CHD.Final.chdProgram.procs }

/-! ## 4. The padded instance -/

theorem npad_ge (n m : ℕ) : n ≤ npad n m := by
  unfold npad
  rw [Nat.add_assoc]
  exact Nat.le_add_right _ _

/-- The padded graph `G'` (vertex count `npad n m`, same edges). -/
def padG (G : Graph) : Graph := pad G (npad G.n G.m) (npad_ge G.n G.m)

/-- The source, viewed in `G'`. -/
def padS (G : Graph) (s : Fin G.n) : Fin (padG G).n := Fin.castLE (npad_ge G.n G.m) s

theorem padG_dist (G : Graph) (s v : Fin G.n) :
    (padG G).dist (padS G s) (Fin.castLE (npad_ge G.n G.m) v) = G.dist s v :=
  pad_dist G (npad G.n G.m) (npad_ge G.n G.m) s v

theorem F_mono {a b : ℕ} (h : a ≤ b) : GateCCalc.F a ≤ GateCCalc.F b := by
  unfold GateCCalc.F
  exact Nat.sqrt_le_sqrt (Nat.sqrt_le_sqrt (Nat.pow_le_pow_left (Nat.log_mono_right h) 3))

theorem F_le_log (n : ℕ) : GateCCalc.F n ≤ Nat.log 2 n := by
  rw [F_eq_root4]
  exact root4_le _

theorem F_ge_eight {n : ℕ} (hn : 65536 ≤ n) : 8 ≤ GateCCalc.F n := by
  have hL : 16 ≤ Nat.log 2 n := Nat.le_log_of_pow_le (by norm_num) (by norm_num; omega)
  rw [F_eq_root4]
  by_contra h
  push_neg at h
  have h1 := lt_root4_succ_pow (Nat.log 2 n * Nat.log 2 n * Nat.log 2 n)
  have h2 : (root4 (Nat.log 2 n * Nat.log 2 n * Nat.log 2 n) + 1) ^ 4 ≤ 4096 :=
    le_trans (Nat.pow_le_pow_left (by omega) 4) (by norm_num : 8 ^ 4 ≤ 4096)
  have h3 : 4096 ≤ Nat.log 2 n * Nat.log 2 n * Nat.log 2 n :=
    le_trans (by norm_num : 4096 ≤ 16 * 16 * 16) (Nat.mul_le_mul (Nat.mul_le_mul hL hL) hL)
  omega

/-- `(F+1)^4 ≤ 2 F^4` once `F ≥ 8`. -/
theorem succ_pow4_le {F : ℕ} (h8 : 8 ≤ F) : (F + 1) ^ 4 ≤ 2 * F ^ 4 := by
  have a1 : 8 * (F * F * F) ≤ F * (F * F * F) := Nat.mul_le_mul_right _ h8
  have a2 : 8 * (F * F) ≤ F * (F * F) := Nat.mul_le_mul_right _ h8
  have a3 : 8 * F ≤ F * F := Nat.mul_le_mul_right _ h8
  have e1 : (F + 1) ^ 4 = F * (F * F * F) + 4 * (F * F * F) + 6 * (F * F) + 4 * F + 1 := by ring
  have e2 : 2 * F ^ 4 = 2 * (F * (F * F * F)) := by ring
  rw [e1, e2]
  nlinarith

/-! ## 5. `prog2` from any input-frame state -/

variable {G : Graph} {s : Fin G.n}

theorem prog2_dij_from (st : State ℝ≥0) (hF : F0 G s st) (hdiv : G.m / G.n ≤ G.n) :
    Runs realOps prog2 st (fun r => r.Solves G s ∧
      r.cost ≤ st.cost + 4 * Nat.log 2 G.n + 6 + 1 + (4 * G.n + 3 * G.m + 9) + (6 * G.m + 2) + 4
        + (12 * rk 0 + 13) + (Kc G * (2 * G.m + 3) + 1)) := by
  refine runs_seq ((calcPa_runs (G := G) (s := s) st hF).mono ?_)
  rintro st1 ⟨hF1, hpa1, hc1⟩
  have htest : evalW st1 (lt (var "n") (div (var "m") (var "n"))) = some 0 := by
    rw [test_eval2 hF1, if_neg (by omega)]
  refine runs_ite_false (a := Frontier.RAM.BF.prog) htest ?_
  refine (dijkstra_branch_from (G := G) (s := s) (st := st1) hF1).mono ?_
  rintro r ⟨hsv, hc⟩
  exact ⟨hsv, by omega⟩

theorem prog2_bf_from (st : State ℝ≥0) (hF : F0 G s st) (hdiv : G.n < G.m / G.n) :
    Runs realOps prog2 st (fun r => r.Solves G s ∧
      r.cost ≤ st.cost + 4 * Nat.log 2 G.n + 6 + 1 + 2 * G.n + 4 + (9 * G.m + 4) * G.n + 1) := by
  refine runs_seq ((calcPa_runs (G := G) (s := s) st hF).mono ?_)
  rintro st1 ⟨hF1, hpa1, hc1⟩
  have htest : evalW st1 (lt (var "n") (div (var "m") (var "n"))) = some 1 := by
    rw [test_eval2 hF1, if_pos hdiv]
  refine runs_ite_true (b := dijkstraBody) htest (by decide) ?_
  refine (bf_branch_from (G := G) (s := s) (st := st1) hF1).mono ?_
  rintro r ⟨hsv, hc⟩
  exact ⟨hsv, by omega⟩

/-- `prog2` from any input-frame state, with the polynomial bound. -/
theorem prog2_poly_from (st : State ℝ≥0) (hF : F0 G s st) :
    Runs realOps prog2 st (fun r => r.Solves G s ∧
      (r.cost : ℝ) ≤ (st.cost : ℝ) + 2000 * ((G.n : ℝ) + 1) * ((G.m : ℝ) + 1)) := by
  have hnR : (0 : ℝ) ≤ (G.n : ℝ) := Nat.cast_nonneg _
  have hmR : (0 : ℝ) ≤ (G.m : ℝ) := Nat.cast_nonneg _
  have hL0 : (0 : ℝ) ≤ (Nat.log 2 G.n : ℝ) := by positivity
  have hLle : (Nat.log 2 G.n : ℝ) ≤ (G.n : ℝ) := Nat.cast_le.mpr (Nat.log_le_self 2 G.n)
  have hnpos : 0 < G.n := by have := s.isLt; omega
  by_cases hdiv : G.n < G.m / G.n
  · refine (prog2_bf_from st hF hdiv).mono ?_
    rintro r ⟨hsv, hc⟩
    refine ⟨hsv, ?_⟩
    have hexp : (9 * G.m + 4) * G.n = 9 * G.m * G.n + 4 * G.n := by ring
    have hcostN : r.cost ≤ st.cost + (4 * Nat.log 2 G.n + 9 * G.m * G.n + 6 * G.n + 12) := by
      omega
    have hcostR : (r.cost : ℝ) ≤
        ((st.cost + (4 * Nat.log 2 G.n + 9 * G.m * G.n + 6 * G.n + 12) : ℕ) : ℝ) := by
      exact_mod_cast hcostN
    push_cast at hcostR
    linarith [arith_clause2_bf hnR hmR hL0 hLle]
  · push_neg at hdiv
    have hm3 := m_add_two_le (G := G) hnpos hdiv
    have hKc : Kc G ≤ 60 * Nat.log 2 G.n + 123 := Kc_le2 (G := G) hm3
    have hKcn : Kc G ≤ 60 * G.n + 123 := by
      have hLn : Nat.log 2 G.n ≤ G.n := Nat.log_le_self 2 G.n
      omega
    refine (prog2_dij_from st hF hdiv).mono ?_
    rintro r ⟨hsv, hc⟩
    refine ⟨hsv, ?_⟩
    have hrk0 : rk 0 = 0 := rfl
    have hmul := Nat.mul_le_mul_right (2 * G.m + 3) hKcn
    have hcostN : r.cost ≤ st.cost + (4 * Nat.log 2 G.n + 9 * G.m + 4 * G.n + 36
        + (60 * G.n + 123) * (2 * G.m + 3)) := by omega
    have hcostR : (r.cost : ℝ) ≤ ((st.cost + (4 * Nat.log 2 G.n + 9 * G.m + 4 * G.n + 36
        + (60 * G.n + 123) * (2 * G.m + 3)) : ℕ) : ℝ) := by exact_mod_cast hcostN
    push_cast at hcostR
    linarith [arith_clause2_dij hnR hmR hL0 hLle]

/-! ## 6. The two dispatch tests of `body3` -/

theorem p3_cap : (initState p3 G s).cap = (G.n + G.m + 2) ^ 322 := rfl

theorem test1_eval : evalW (initState p3 G s) (lt (var "n") (lit 65536))
    = some (if G.n < 65536 then 1 else 0) := by
  have hc : 65536 < (initState p3 G s).cap := by
    rw [p3_cap]
    exact lt_of_lt_of_le
      (lt_of_lt_of_le (by norm_num : 65536 < 2 ^ 17) (Nat.pow_le_pow_right (by norm_num) (by norm_num)))
      (Nat.pow_le_pow_left (by omega : 2 ≤ G.n + G.m + 2) 322)
  exact evalW_lt_of (by rw [evalW_var, (F0.init_state (G := G) p3 s).hn]) (evalW_lit_of hc)
    (by omega)

theorem body3_small (hn : G.n < 65536) :
    Runs realOps body3 (initState p3 G s) (fun r => r.Solves G s ∧
      (r.cost : ℝ) ≤ 1 + 2000 * ((G.n : ℝ) + 1) * ((G.m : ℝ) + 1)) := by
  unfold body3
  have ht : evalW (initState p3 G s) (lt (var "n") (lit 65536)) = some 1 := by
    rw [test1_eval, if_pos hn]
  refine runs_ite_true ht one_ne_zero ?_
  refine (prog2_poly_from _ ((F0.init_state (G := G) p3 s).charge 1)).mono ?_
  rintro r ⟨hS, hc⟩
  refine ⟨hS, ?_⟩
  have h1 : ((initState p3 G s).charge 1).cost = 1 := rfl
  rw [h1] at hc
  push_cast at hc
  linarith

theorem body3_dense (hn : 65536 ≤ G.n) (hd : G.n < G.m / G.n) :
    Runs realOps body3 (initState p3 G s) (fun r => r.Solves G s ∧
      (r.cost : ℝ) ≤ 2 + 2000 * ((G.n : ℝ) + 1) * ((G.m : ℝ) + 1)) := by
  unfold body3
  have ht : evalW (initState p3 G s) (lt (var "n") (lit 65536)) = some 0 := by
    rw [test1_eval, if_neg (by omega)]
  refine runs_ite_false ht ?_
  have hF1 := (F0.init_state (G := G) p3 s).charge 1
  have ht2 : evalW ((initState p3 G s).charge 1) (lt (var "n") (div (var "m") (var "n")))
      = some 1 := by rw [test_eval2 hF1, if_pos hd]
  refine runs_ite_true ht2 one_ne_zero ?_
  refine (prog2_poly_from _ (hF1.charge 1)).mono ?_
  rintro r ⟨hS, hc⟩
  refine ⟨hS, ?_⟩
  have h1 : (((initState p3 G s).charge 1).charge 1).cost = 2 := rfl
  rw [h1] at hc
  push_cast at hc
  linarith

/-! ## 7. `padSetup` turns the state into C-HD's initial state of `G'` (up to `tw`) -/

/-- The setup's cost from the post-dispatch state (2 tests already charged). -/
def kSetup (n : ℕ) : ℕ := 14 + 3 * Nat.log 2 n + 2 * GateCCalc.F n

theorem padSetup_runs (hn : 65536 ≤ G.n) :
    Runs realOps padSetup (((initState p3 G s).charge 1).charge 1) (fun X =>
      X = tw (initState Frontier.CHD.Final.chdProgram (padG G) (padS G s)) ZN G.n ((G.n + G.m + 2) ^ 322)
        (kSetup G.n)) := by
  unfold padSetup
  set st2 := ((initState p3 G s).charge 1).charge 1 with hst2
  set c := (G.n + G.m + 2) ^ 322 with hc
  set L := Nat.log 2 G.n with hLdef
  set Fr := root4 (L * L * L) with hFrdef
  have hFr : GateCCalc.F G.n = Fr := F_eq_root4 G.n
  have hF8 : 8 ≤ Fr := by rw [← hFr]; exact F_ge_eight hn
  have hcap2 : st2.cap = c := rfl
  have hst2n : st2.w "n" = G.n := (F0.init_state (G := G) p3 s).hn
  have hst2m : st2.w "m" = G.m := (F0.init_state (G := G) p3 s).hm
  have hLn : L ≤ G.n := Nat.log_le_self 2 G.n
  -- the cap is huge
  set B := G.n + G.m + 2 with hB
  have hB4 : B ^ 4 ≤ c := Nat.pow_le_pow_right (by omega) (by norm_num)
  have hB1 : B ≤ B ^ 4 := Nat.le_self_pow (by norm_num) B
  have hB2 : 2 * B ≤ B ^ 4 := by
    have e : B ^ 4 = B ^ 3 * B := by ring
    rw [e]
    exact Nat.mul_le_mul_right B (le_trans (by omega : 2 ≤ B) (Nat.le_self_pow (by norm_num) B))
  have hcube : 16 * (L * L * L) + 16 < B ^ 4 := by
    have hLB : L ≤ B := by omega
    have h1 : L * L * L ≤ B * B * B := Nat.mul_le_mul (Nat.mul_le_mul hLB hLB) hLB
    have h4 : B ^ 4 = B * (B * B * B) := by ring
    have h17 : 17 * (B * B * B) ≤ B * (B * B * B) := Nat.mul_le_mul_right _ (by omega)
    have hB17 : 17 ≤ B := by omega
    have hpos : 17 ≤ B * B * B := by nlinarith
    rw [h4]
    linarith
  -- logProg
  refine runs_seq ((logProg_runs (ops := realOps) st2 G.n hst2n (by rw [hcap2]; omega)).mono ?_)
  rintro r1 ⟨hpa1, hA1, hc1⟩
  obtain ⟨a1w, a1v, a1wa, a1va, a1wl, a1vl, a1c, a1s, a1p⟩ := hA1
  -- thrProg
  refine runs_seq ((thrProg_runs (ops := realOps) r1 L hpa1 (by rw [a1c, hcap2]; omega)).mono ?_)
  rintro r2 ⟨hpr2, hA2, hc2⟩
  obtain ⟨a2w, a2v, a2wa, a2va, a2wl, a2vl, a2c, a2s, a2p⟩ := hA2
  have hr2cap : r2.cap = c := by rw [a2c, a1c, hcap2]
  have hr2n : r2.w "n" = G.n := by
    rw [a2w "n" (by simp), a1w "n" (by simp), hst2n]
  have hr2m : r2.w "m" = G.m := by
    rw [a2w "m" (by simp), a1w "m" (by simp), hst2m]
  -- ZN := n
  refine runs_seq (runs_wset (a := G.n) (by rw [evalW_var, hr2n]) ?_)
  set r3 := (r2.setW ZN G.n).charge 1 with hr3
  have hr3cap : r3.cap = c := hr2cap
  have e_n : evalW r3 (var "n") = some G.n := by
    rw [evalW_var]
    show some (if "n" = ZN then G.n else r2.w "n") = some G.n
    rw [if_neg (by simp [ZN]), hr2n]
  have e_m : evalW r3 (var "m") = some G.m := by
    rw [evalW_var]
    show some (if "m" = ZN then G.n else r2.w "m") = some G.m
    rw [if_neg (by simp [ZN]), hr2m]
  have e_pr : evalW r3 (var "pr") = some Fr := by
    rw [evalW_var]
    show some (if "pr" = ZN then G.n else r2.w "pr") = some Fr
    rw [if_neg (by simp [ZN]), hpr2]
  have hq : G.m / Fr ≤ G.m := Nat.div_le_self _ _
  have e_div : evalW r3 (div (var "m") (var "pr")) = some (G.m / Fr) :=
    evalW_div_of e_m e_pr (by omega)
  have e_add1 : evalW r3 (add (var "n") (div (var "m") (var "pr"))) = some (G.n + G.m / Fr) :=
    evalW_add_of e_n e_div (by rw [hr3cap]; omega)
  have e_all : evalW r3 (add (add (var "n") (div (var "m") (var "pr"))) (lit 1))
      = some (npad G.n G.m) := by
    have : npad G.n G.m = G.n + G.m / Fr + 1 := by unfold npad; rw [hFr]
    rw [this]
    exact evalW_add_of e_add1 (evalW_lit_of (by rw [hr3cap]; omega)) (by rw [hr3cap]; omega)
  refine runs_seq (runs_wset e_all ?_)
  have hc0 : 0 < c := by omega
  refine runs_seq (runs_wset (evalW_lit_of (by show 0 < r2.cap; omega)) ?_)
  refine runs_seq (runs_wset (evalW_lit_of (by show 0 < r2.cap; omega)) ?_)
  refine runs_seq (runs_wset (evalW_lit_of (by show 0 < r2.cap; omega)) ?_)
  refine runs_wset (evalW_lit_of (by show 0 < r2.cap; omega)) ?_
  -- the final state is C-HD's initial state of `G'`, up to `tw`
  refine st_ext (fun y => ?_) ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_
  · simp only [State.setW, State.charge, tw_w]
    by_cases h1 : y = "pr"
    · subst h1; simp [ZN, initState]
    by_cases h2 : y = "py"
    · subst h2; simp [ZN, initState]
    by_cases h3 : y = "pa"
    · subst h3; simp [ZN, initState]
    by_cases h4 : y = "px"
    · subst h4; simp [ZN, initState]
    by_cases h5 : y = "n"
    · subst h5; simp [ZN, initState, padG, pad]
    by_cases h6 : y = ZN
    · subst h6; simp [hr3, State.setW, State.charge, ZN]
    simp only [h1, h2, h3, h4, h5, h6, if_false, hr3, State.setW, State.charge]
    rw [a2w y (by simp [h1, h2]), a1w y (by simp [h3, h4])]
    simp [hst2, State.charge, initState, h5, padG, pad, padS]
  · show r2.v = (initState Frontier.CHD.Final.chdProgram (padG G) (padS G s)).v
    rw [a2v, a1v]
    rfl
  · show r2.wa = (initState Frontier.CHD.Final.chdProgram (padG G) (padS G s)).wa
    rw [a2wa, a1wa]
    rfl
  · show r2.va = (initState Frontier.CHD.Final.chdProgram (padG G) (padS G s)).va
    rw [a2va, a1va]
    rfl
  · show r2.wlen = (initState Frontier.CHD.Final.chdProgram (padG G) (padS G s)).wlen
    rw [a2wl, a1wl]
    funext a
    simp [hst2, State.charge, initState, padG, pad]
    try (split_ifs <;> rfl)
  · show r2.vlen = (initState Frontier.CHD.Final.chdProgram (padG G) (padS G s)).vlen
    rw [a2vl, a1vl]
    funext a
    simp [hst2, State.charge, initState, padG, pad]
    try (split_ifs <;> rfl)
  · show r2.cap = c
    exact hr2cap
  · show r2.cost + 1 + 1 + 1 + 1 + 1 + 1 = 0 + kSetup G.n
    have hs2c : st2.cost = 2 := rfl
    unfold kSetup
    rw [hFr]
    omega
  · show r2.space = 0
    rw [a2s, a1s]
    rfl
  · show r2.procs = Frontier.CHD.Final.chdProgram.procs
    rw [a2p, a1p]
    rfl

/-! ## 8. The C-HD run on `G'`, spliced -/

theorem chd_cap_le : (initState Frontier.CHD.Final.chdProgram (padG G) (padS G s)).cap ≤ (G.n + G.m + 2) ^ 322 := by
  show (npad G.n G.m + G.m + 2) ^ (160 + 1) ≤ (G.n + G.m + 2) ^ 322
  have hq : G.m / GateCCalc.F G.n ≤ G.m := Nat.div_le_self _ _
  have h1 : npad G.n G.m + G.m + 2 ≤ (G.n + G.m + 2) ^ 2 := by
    unfold npad
    have : 2 * (G.n + G.m + 2) ≤ (G.n + G.m + 2) ^ 2 := by
      rw [sq]; exact Nat.mul_le_mul_right _ (by omega)
    omega
  calc (npad G.n G.m + G.m + 2) ^ (160 + 1) ≤ ((G.n + G.m + 2) ^ 2) ^ 161 :=
        Nat.pow_le_pow_left h1 _
    _ = (G.n + G.m + 2) ^ 322 := by rw [← pow_mul]

/-! ## 9. The copy-back loops -/

theorem copy_loop (A B C D : String) (hAB : A ≠ B) (hCD : C ≠ D) (t0 : State ℝ≥0) (n : ℕ)
    (hI : t0.w "zzI" = 0) (hZ : t0.w ZN = n) (hA : t0.wlen A = n) (hB : n ≤ t0.wlen B)
    (hC : t0.vlen C = n) (hD : n ≤ t0.vlen D) (hcap : n + 1 < t0.cap) :
    Runs realOps (.while (lt (var "zzI") (var ZN)) (copyStep A B C D)) t0 (fun r =>
      (∀ j < n, r.wa A j = t0.wa B j) ∧ (∀ j < n, r.va C j = t0.va D j) ∧
      (∀ X, X ≠ A → r.wa X = t0.wa X) ∧ (∀ X, X ≠ C → r.va X = t0.va X) ∧
      r.w ZN = n ∧ r.wlen = t0.wlen ∧ r.vlen = t0.vlen ∧ r.cap = t0.cap ∧
      r.cost = t0.cost + 4 * n + 1) := by
  have hZI : ZN ≠ "zzI" := by simp [ZN]
  refine runs_while (fun k t => t.w "zzI" = k ∧ t.w ZN = n ∧
      (∀ j < k, t.wa A j = t0.wa B j) ∧ (∀ j < k, t.va C j = t0.va D j) ∧
      (∀ X, X ≠ A → t.wa X = t0.wa X) ∧ (∀ X, X ≠ C → t.va X = t0.va X) ∧
      t.wlen = t0.wlen ∧ t.vlen = t0.vlen ∧ t.cap = t0.cap ∧ t.cost = t0.cost + 4 * k)
    n _ ?_ ?_ t0
    ⟨hI, hZ, fun j hj => absurd hj (Nat.not_lt_zero _), fun j hj => absurd hj (Nat.not_lt_zero _),
      fun _ _ => rfl, fun _ _ => rfl, rfl, rfl, rfl, by simp⟩
  · intro k hk t ⟨h1, h2, h3, h4, h5, h6, h7, h8, h9, h10⟩
    have hc1 : 1 < t.cap := by rw [h9]; omega
    refine ⟨1, ?_, one_ne_zero, ?_⟩
    · rw [evalW_lt_of (by rw [evalW_var, h1]) (by rw [evalW_var, h2]) hc1, if_pos hk]
    · unfold copyStep
      have hiu : evalW (t.charge 1) (var "zzI") = some k := by
        rw [evalW_var]; exact congrArg some h1
      have hBl : k < (t.charge 1).wlen B := by show k < t.wlen B; rw [h7]; omega
      have hAl : k < (t.charge 1).wlen A := by show k < t.wlen A; rw [h7]; omega
      refine runs_seq (runs_wstore hiu (evalW_load_of hiu hBl) hAl ?_)
      set u1 := ((t.charge 1).storeW A k ((t.charge 1).wa B k)).charge 1 with hu1
      have hiu1 : evalW u1 (var "zzI") = some k := by rw [evalW_var]; exact congrArg some h1
      have hDl : k < u1.vlen D := by show k < t.vlen D; rw [h8]; omega
      have hCl : k < u1.vlen C := by show k < t.vlen C; rw [h8]; omega
      refine runs_seq (runs_vstore hiu1 (evalV_load_of hiu1 hDl) hCl ?_)
      set u2 := (u1.storeV C k (u1.va D k)).charge 1 with hu2
      have hcap2 : u2.cap = t0.cap := h9
      have hadd : evalW u2 (add (var "zzI") (lit 1)) = some (k + 1) :=
        evalW_add_of (by rw [evalW_var]; exact congrArg some h1)
          (evalW_lit_of (by rw [hcap2]; omega)) (by rw [hcap2]; omega)
      refine runs_wset hadd ?_
      refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
      · show (if "zzI" = "zzI" then k + 1 else u2.w "zzI") = k + 1
        simp
      · show (if ZN = "zzI" then k + 1 else t.w ZN) = n
        rw [if_neg hZI]; exact h2
      · intro j hj
        show (if A = A ∧ j = k then t.wa B k else t.wa A j) = t0.wa B j
        by_cases hjk : j = k
        · rw [if_pos ⟨rfl, hjk⟩, hjk]; exact congrFun (h5 B (Ne.symm hAB)) k
        · rw [if_neg (by tauto)]; exact h3 j (by omega)
      · intro j hj
        show (if C = C ∧ j = k then t.va D k else t.va C j) = t0.va D j
        by_cases hjk : j = k
        · rw [if_pos ⟨rfl, hjk⟩, hjk]; exact congrFun (h6 D (Ne.symm hCD)) k
        · rw [if_neg (by tauto)]; exact h4 j (by omega)
      · intro X hX
        show (fun j => if X = A ∧ j = k then t.wa B k else t.wa X j) = t0.wa X
        funext j
        rw [if_neg (by tauto)]
        exact congrFun (h5 X hX) j
      · intro X hX
        show (fun j => if X = C ∧ j = k then t.va D k else t.va X j) = t0.va X
        funext j
        rw [if_neg (by tauto)]
        exact congrFun (h6 X hX) j
      · exact h7
      · exact h8
      · exact h9
      · show t.cost + 1 + 1 + 1 + 1 = t0.cost + 4 * (k + 1)
        omega
  · intro t ⟨h1, h2, h3, h4, h5, h6, h7, h8, h9, h10⟩
    have hc1 : 1 < t.cap := by rw [h9]; omega
    refine ⟨?_, h3, h4, h5, h6, h2, h7, h8, h9, ?_⟩
    · rw [evalW_lt_of (by rw [evalW_var, h1]) (by rw [evalW_var, h2]) hc1, if_neg (lt_irrefl n)]
    · show t.cost + 1 = t0.cost + 4 * n + 1
      omega

theorem post_runs (Y : State ℝ≥0) (n : ℕ) (hZ : Y.w ZN = n) (hR : n ≤ Y.wlen "reach")
    (hD : n ≤ Y.vlen "dist") (hcap : n + 1 < Y.cap) :
    Runs realOps post Y (fun r => r.wlen "reach" = n ∧ r.vlen "dist" = n ∧
      (∀ j < n, r.wa "reach" j = Y.wa "reach" j) ∧ (∀ j < n, r.va "dist" j = Y.va "dist" j) ∧
      r.cost = Y.cost + 12 * n + 8) := by
  have hZI : ZN ≠ "zzI" := by simp [ZN]
  unfold post
  have hZe : evalW Y (var ZN) = some n := by rw [evalW_var, hZ]
  refine runs_seq (runs_walloc hZe ?_)
  set a1 := (Y.allocW "zzR" n).charge (n + 1) with ha1
  have hZe1 : evalW a1 (var ZN) = some n := by rw [evalW_var]; exact congrArg some hZ
  refine runs_seq (runs_valloc hZe1 ?_)
  set a2 := (a1.allocV "zzD" n realOps.zero).charge (n + 1) with ha2
  have h0 : evalW a2 (lit 0) = some 0 := evalW_lit_of (by show 0 < Y.cap; omega)
  refine runs_seq (runs_wset h0 ?_)
  set a3 := (a2.setW "zzI" 0).charge 1 with ha3
  have L1 := copy_loop "zzR" "reach" "zzD" "dist" (by simp) (by simp) a3 n
    (by show (if "zzI" = "zzI" then 0 else a2.w "zzI") = 0; simp)
    (by show (if ZN = "zzI" then 0 else Y.w ZN) = n; rw [if_neg hZI]; exact hZ)
    (by show (if "zzR" = "zzR" then n else Y.wlen "zzR") = n; simp)
    (by show n ≤ (if "reach" = "zzR" then n else Y.wlen "reach"); rw [if_neg (by simp)]; exact hR)
    (by show (if "zzD" = "zzD" then n else Y.vlen "zzD") = n; simp)
    (by show n ≤ (if "dist" = "zzD" then n else Y.vlen "dist"); rw [if_neg (by simp)]; exact hD)
    (by show n + 1 < Y.cap; exact hcap)
  refine runs_seq (L1.mono ?_)
  rintro r1 ⟨c1, c2, c3, c4, c5, c6, c7, c8, c9⟩
  have hZr1 : evalW r1 (var ZN) = some n := by rw [evalW_var, c5]
  refine runs_seq (runs_walloc hZr1 ?_)
  set b1 := (r1.allocW "reach" n).charge (n + 1) with hb1
  have hZb1 : evalW b1 (var ZN) = some n := by rw [evalW_var]; exact congrArg some c5
  refine runs_seq (runs_valloc hZb1 ?_)
  set b2 := (b1.allocV "dist" n realOps.zero).charge (n + 1) with hb2
  have hr1cap : r1.cap = Y.cap := c8
  have h0' : evalW b2 (lit 0) = some 0 := evalW_lit_of (by show 0 < r1.cap; rw [hr1cap]; omega)
  refine runs_seq (runs_wset h0' ?_)
  set b3 := (b2.setW "zzI" 0).charge 1 with hb3
  have hr1R : r1.wlen "zzR" = n := by rw [c6]; show (if "zzR" = "zzR" then n else Y.wlen "zzR") = n; simp
  have hr1D : r1.vlen "zzD" = n := by rw [c7]; show (if "zzD" = "zzD" then n else Y.vlen "zzD") = n; simp
  have L2 := copy_loop "reach" "zzR" "dist" "zzD" (by simp) (by simp) b3 n
    (by show (if "zzI" = "zzI" then 0 else b2.w "zzI") = 0; simp)
    (by show (if ZN = "zzI" then 0 else r1.w ZN) = n; rw [if_neg hZI]; exact c5)
    (by show (if "reach" = "reach" then n else r1.wlen "reach") = n; simp)
    (by show n ≤ (if "zzR" = "reach" then n else r1.wlen "zzR"); rw [if_neg (by simp), hr1R])
    (by show (if "dist" = "dist" then n else r1.vlen "dist") = n; simp)
    (by show n ≤ (if "zzD" = "dist" then n else r1.vlen "zzD"); rw [if_neg (by simp), hr1D])
    (by show n + 1 < r1.cap; rw [hr1cap]; exact hcap)
  refine L2.mono ?_
  rintro r2 ⟨d1, d2, d3, d4, d5, d6, d7, d8, d9⟩
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · rw [d6]; show (if "reach" = "reach" then n else r1.wlen "reach") = n; simp
  · rw [d7]; show (if "dist" = "dist" then n else r1.vlen "dist") = n; simp
  · intro j hj
    rw [d1 j hj]
    show (if "zzR" = "reach" then 0 else r1.wa "zzR" j) = Y.wa "reach" j
    rw [if_neg (by simp), c1 j hj]
    show (if "reach" = "zzR" then 0 else Y.wa "reach" j) = Y.wa "reach" j
    rw [if_neg (by simp)]
  · intro j hj
    rw [d2 j hj]
    show (if "zzD" = "dist" then realOps.zero else r1.va "zzD" j) = Y.va "dist" j
    rw [if_neg (by simp), c2 j hj]
    show (if "dist" = "zzD" then realOps.zero else Y.va "dist" j) = Y.va "dist" j
    rw [if_neg (by simp)]
  · have e1 : b3.cost = r1.cost + (n + 1) + (n + 1) + 1 := rfl
    have e2 : a3.cost = Y.cost + (n + 1) + (n + 1) + 1 := rfl
    omega

/-! ## 10. The padding branch, end to end -/

theorem body3_pad (K : ℝ) (hE : Frontier.CHD.Final.chdProgram.Exact)
    (hW : ∀ (H : Graph) (z : Fin H.n),
      Frontier.CHD.Final.chdProgram.RunsWithin H z (K * GateCTarget.Tdisp GateCCalc.F H.n H.m))
    (hn : 65536 ≤ G.n) (hmn : G.m / G.n ≤ G.n) :
    ∃ fuel r, p3.run fuel G s = some r ∧ r.Solves G s ∧
      (r.cost : ℝ) ≤ ((kSetup G.n + 12 * G.n + 8 : ℕ) : ℝ)
        + K * GateCTarget.Tdisp GateCCalc.F (npad G.n G.m) G.m := by
  set c := (G.n + G.m + 2) ^ 322 with hc
  set k := kSetup G.n with hk
  obtain ⟨f, R, hR, hS⟩ := hE (padG G) (padS G s)
  have hRc : (R.cost : ℝ) ≤ K * GateCTarget.Tdisp GateCCalc.F (npad G.n G.m) G.m :=
    Program.runsWithin_unique (hW (padG G) (padS G s)) hR
  have hR' : exec realOps f Frontier.CHD.Final.chdProgram.body
      (initState Frontier.CHD.Final.chdProgram (padG G) (padS G s)) = some R := hR
  obtain ⟨e1, -, -⟩ := exec_tw (ops := realOps) (x := ZN) (a := G.n) (c := c) (k := k) f _ _ R hR'
    (chd_cap_le (G := G) (s := s)) names_body (fun q hq => names_procs q hq)
  have hRn : R.wlen "reach" = npad G.n G.m := hS.1
  have hRd : R.vlen "dist" = npad G.n G.m := hS.2.1
  have hcapn : G.n + 1 < c := by
    have : G.n + G.m + 2 ≤ c := Nat.le_self_pow (by norm_num) _
    omega
  have hpost := post_runs (tw R ZN G.n c k) G.n (by simp)
    (by rw [tw_wlen, hRn]; exact npad_ge _ _) (by rw [tw_vlen, hRd]; exact npad_ge _ _)
    (by rw [tw_cap]; exact hcapn)
  have hRun : Runs realOps body3 (initState p3 G s) (fun r => r.Solves G s ∧
      r.cost = R.cost + k + 12 * G.n + 8) := by
    unfold body3
    have ht1 : evalW (initState p3 G s) (lt (var "n") (lit 65536)) = some 0 := by
      rw [test1_eval, if_neg (by omega)]
    refine runs_ite_false ht1 ?_
    have hF1 := (F0.init_state (G := G) p3 s).charge 1
    have ht2 : evalW ((initState p3 G s).charge 1) (lt (var "n") (div (var "m") (var "n")))
        = some 0 := by rw [test_eval2 hF1, if_neg (by omega)]
    refine runs_ite_false ht2 ?_
    unfold padPath
    refine runs_seq ((padSetup_runs (G := G) (s := s) hn).mono ?_)
    rintro X rfl
    refine runs_seq ⟨f, _, e1, ?_⟩
    refine hpost.mono ?_
    rintro r ⟨h1, h2, h3, h4, h5⟩
    refine ⟨⟨h1, h2, fun v => ?_⟩, ?_⟩
    · have hv := hS.2.2 (Fin.castLE (npad_ge G.n G.m) v)
      rw [padG_dist] at hv
      simp only [Fin.coe_castLE] at hv
      show r.label v = G.dist s v
      unfold State.label at hv ⊢
      rw [h3 v v.isLt, h4 v v.isLt, tw_wa, tw_va]
      exact hv
    · rw [h5, tw_cost]
  obtain ⟨fuel, r, hr, hS', hcost⟩ := hRun
  refine ⟨fuel, r, hr, hS', ?_⟩
  have hcR : (r.cost : ℝ) = (R.cost : ℝ) + ((k + 12 * G.n + 8 : ℕ) : ℝ) := by
    rw [hcost]; push_cast; ring
  rw [hcR]
  have : ((k + 12 * G.n + 8 : ℕ) : ℝ) = ((kSetup G.n + 12 * G.n + 8 : ℕ) : ℝ) := rfl
  linarith

/-! ## 11. Arithmetic -/

theorem ell_le_L (hn : 16 ≤ G.n) : Real.log (G.n : ℝ) ≤ ((Nat.log 2 G.n : ℕ) : ℝ) := by
  have h1 : G.n < 2 ^ (Nat.log 2 G.n + 1) := Nat.lt_pow_succ_log_self (by norm_num) G.n
  have h1R : (G.n : ℝ) < (2 : ℝ) ^ (Nat.log 2 G.n + 1) := by exact_mod_cast h1
  have hpos : (0 : ℝ) < G.n := by
    have : (16 : ℝ) ≤ G.n := by exact_mod_cast hn
    linarith
  have h2 : Real.log G.n < Real.log ((2 : ℝ) ^ (Nat.log 2 G.n + 1)) := Real.log_lt_log hpos h1R
  rw [Real.log_pow] at h2
  have hlog2 : Real.log 2 < 0.6931471808 := Real.log_two_lt_d9
  have hL4 : (4 : ℝ) ≤ ((Nat.log 2 G.n : ℕ) : ℝ) := by
    exact_mod_cast (Nat.le_log_of_pow_le (by norm_num) (by simpa using hn) : 4 ≤ Nat.log 2 G.n)
  push_cast at h2
  have h3 : ((Nat.log 2 G.n : ℝ) + 1) * Real.log 2 ≤ ((Nat.log 2 G.n : ℝ) + 1) * 0.6931471808 :=
    mul_le_mul_of_nonneg_left hlog2.le (by linarith)
  linarith

theorem Tchd_nonneg (n m : ℕ) : 0 ≤ GateCCalc.Tchd n m := by
  unfold GateCCalc.Tchd
  have hn : (0 : ℝ) ≤ n := Nat.cast_nonneg _
  have hm : (0 : ℝ) ≤ m := Nat.cast_nonneg _
  have h1 : 0 ≤ Real.log ((m : ℝ) / ((n : ℝ) + 1) + 2) :=
    Real.log_nonneg (by have : 0 ≤ (m : ℝ) / ((n : ℝ) + 1) := by positivity
                        linarith)
  have h2 : 0 ≤ Real.log ((n : ℝ) + 2) := Real.log_nonneg (by linarith)
  have h3 : 0 ≤ (m : ℝ) ^ ((1 : ℝ) / 3) * ((n : ℝ) * Real.log ((n : ℝ) + 2)) ^ ((2 : ℝ) / 3) :=
    mul_nonneg (Real.rpow_nonneg hm _) (Real.rpow_nonneg (mul_nonneg hn h2) _)
  have h4 : 0 ≤ (m : ℝ) * Real.log ((m : ℝ) / ((n : ℝ) + 1) + 2) := mul_nonneg hm h1
  linarith

theorem Tdisp_nonneg (n m : ℕ) : 0 ≤ GateCTarget.Tdisp GateCCalc.F n m := by
  unfold GateCTarget.Tdisp
  split_ifs
  · exact Tchd_nonneg n m
  · have hn : (0 : ℝ) ≤ n := Nat.cast_nonneg _
    have hm : (0 : ℝ) ≤ m := Nat.cast_nonneg _
    positivity

/-- C-HD's theorem with a nonnegative constant. -/
theorem chd_K : ∃ K : ℝ, 0 ≤ K ∧ Frontier.CHD.Final.chdProgram.Exact ∧ ∀ (H : Graph) (z : Fin H.n),
    Frontier.CHD.Final.chdProgram.RunsWithin H z (K * GateCTarget.Tdisp GateCCalc.F H.n H.m) := by
  obtain ⟨hE, hW⟩ := Frontier.CHD.Final.chd_exact_within
  have key : ∀ K : ℝ, (∀ (H : Graph) (z : Fin H.n),
      Frontier.CHD.Final.chdProgram.RunsWithin H z (K * GateCTarget.Tdisp GateCCalc.F H.n H.m)) →
      ∃ K' : ℝ, 0 ≤ K' ∧ ∀ (H : Graph) (z : Fin H.n),
        Frontier.CHD.Final.chdProgram.RunsWithin H z (K' * GateCTarget.Tdisp GateCCalc.F H.n H.m) := by
    intro K hK
    refine ⟨max K 0, le_max_right _ _, fun H z => ?_⟩
    obtain ⟨f, r, h, hc⟩ := hK H z
    exact ⟨f, r, h, hc.trans (mul_le_mul_of_nonneg_right (le_max_left _ _) (Tdisp_nonneg _ _))⟩
  obtain ⟨K', hK', hW'⟩ := key _ hW
  exact ⟨K', hK', hE, hW'⟩

/-- **The padding estimate** (pure reals). -/
theorem master {n m ℓ pr np : ℝ} (hn : 1 ≤ n) (hl : 2 ≤ ℓ) (hm : 0 ≤ m) (hpr : 1 ≤ pr)
    (hpl : ℓ ^ 4 ≤ 3 * ℓ * pr ^ 4) (hprl : pr ≤ 1.5 * ℓ) (hnp0 : 0 ≤ np)
    (hnp : np ≤ 2 * n + m / pr) (hlog : Real.log (np + 2) ≤ 3 * ℓ) (hq : m / (np + 1) ≤ pr) :
    np + m + m * Real.log (m / (np + 1) + 2)
      + m ^ ((1 : ℝ) / 3) * (np * Real.log (np + 2)) ^ ((2 : ℝ) / 3)
    ≤ 2 * n + 2 * m + 27 * (m * ℓ ^ ((1 : ℝ) / 6))
      + 6 * (m ^ ((1 : ℝ) / 3) * (n * ℓ) ^ ((2 : ℝ) / 3)) := by
  have hl0 : 0 < ℓ := by linarith
  have hpr0 : 0 < pr := by linarith
  have hn0 : 0 ≤ n := by linarith
  set e := ℓ ^ ((1 : ℝ) / 6) with he
  have he1 : 1 ≤ e := Real.one_le_rpow (by linarith) (by norm_num)
  have he0 : 0 ≤ e := by linarith
  have h3a : (3 : ℝ) ^ ((1 : ℝ) / 6) ≤ 3 := by
    calc (3 : ℝ) ^ ((1 : ℝ) / 6) ≤ (3 : ℝ) ^ (1 : ℝ) :=
          Real.rpow_le_rpow_of_exponent_le (by norm_num) (by norm_num)
      _ = 3 := Real.rpow_one 3
  -- (i) `m / pr ≤ m`
  have hmp : m / pr ≤ m := div_le_self hm hpr
  -- (ii) the logarithmic term
  have hlog3 : Real.log (m / (np + 1) + 2) ≤ 18 * e := by
    have hx0 : 0 < m / (np + 1) + 2 := by positivity
    have hx : m / (np + 1) + 2 ≤ 3 * ℓ := by linarith
    have h1 : Real.log (m / (np + 1) + 2) ≤ Real.log (3 * ℓ) := Real.log_le_log hx0 hx
    have h2 : Real.log (3 * ℓ) ≤ (3 * ℓ) ^ ((1 : ℝ) / 6) / ((1 : ℝ) / 6) :=
      Real.log_le_rpow_div (by positivity) (by norm_num)
    have h3 : (3 * ℓ) ^ ((1 : ℝ) / 6) = (3 : ℝ) ^ ((1 : ℝ) / 6) * e :=
      Real.mul_rpow (by norm_num) hl0.le
    rw [h3] at h2
    have h4 : (3 : ℝ) ^ ((1 : ℝ) / 6) * e / ((1 : ℝ) / 6) ≤ 18 * e := by
      rw [div_le_iff₀ (by norm_num)]
      nlinarith
    linarith
  have hlogt : m * Real.log (m / (np + 1) + 2) ≤ 18 * (m * e) := by
    have := mul_le_mul_of_nonneg_left hlog3 hm
    linarith [show m * (18 * e) = 18 * (m * e) by ring]
  -- (iii) the last term
  set W := m ^ ((1 : ℝ) / 3) * (n * ℓ) ^ ((2 : ℝ) / 3) with hW
  have hlogn : 0 ≤ Real.log (np + 2) := Real.log_nonneg (by linarith)
  have hX : np * Real.log (np + 2) ≤ 3 * (2 * (n * ℓ) + m * (ℓ / pr)) := by
    have h1 : np * Real.log (np + 2) ≤ np * (3 * ℓ) := mul_le_mul_of_nonneg_left hlog hnp0
    have h2 : np * (3 * ℓ) ≤ (2 * n + m / pr) * (3 * ℓ) :=
      mul_le_mul_of_nonneg_right hnp (by linarith)
    have h3 : (2 * n + m / pr) * (3 * ℓ) = 3 * (2 * (n * ℓ) + m * (ℓ / pr)) := by
      field_simp
      try ring
    linarith
  have hA0 : 0 ≤ 2 * (n * ℓ) := by positivity
  have hB0 : 0 ≤ m * (ℓ / pr) := by positivity
  have h23 : (0 : ℝ) ≤ (2 : ℝ) / 3 := by norm_num
  have hY : (np * Real.log (np + 2)) ^ ((2 : ℝ) / 3)
      ≤ (3 : ℝ) ^ ((2 : ℝ) / 3) * ((2 * (n * ℓ)) ^ ((2 : ℝ) / 3) + (m * (ℓ / pr)) ^ ((2 : ℝ) / 3)) := by
    calc (np * Real.log (np + 2)) ^ ((2 : ℝ) / 3)
        ≤ (3 * (2 * (n * ℓ) + m * (ℓ / pr))) ^ ((2 : ℝ) / 3) :=
          Real.rpow_le_rpow (mul_nonneg hnp0 hlogn) hX h23
      _ = (3 : ℝ) ^ ((2 : ℝ) / 3) * (2 * (n * ℓ) + m * (ℓ / pr)) ^ ((2 : ℝ) / 3) :=
          Real.mul_rpow (by norm_num) (by positivity)
      _ ≤ (3 : ℝ) ^ ((2 : ℝ) / 3) * ((2 * (n * ℓ)) ^ ((2 : ℝ) / 3) + (m * (ℓ / pr)) ^ ((2 : ℝ) / 3)) :=
          mul_le_mul_of_nonneg_left (Real.rpow_add_le_add_rpow hA0 hB0 h23 (by norm_num))
            (by positivity)
  have h3c : (3 : ℝ) ^ ((2 : ℝ) / 3) ≤ 3 := by
    calc (3 : ℝ) ^ ((2 : ℝ) / 3) ≤ (3 : ℝ) ^ (1 : ℝ) :=
          Real.rpow_le_rpow_of_exponent_le (by norm_num) (by norm_num)
      _ = 3 := Real.rpow_one 3
  have h2c : (2 * (n * ℓ)) ^ ((2 : ℝ) / 3) ≤ 2 * (n * ℓ) ^ ((2 : ℝ) / 3) := by
    rw [Real.mul_rpow (by norm_num) (by positivity)]
    have h22 : (2 : ℝ) ^ ((2 : ℝ) / 3) ≤ 2 := by
      calc (2 : ℝ) ^ ((2 : ℝ) / 3) ≤ (2 : ℝ) ^ (1 : ℝ) :=
            Real.rpow_le_rpow_of_exponent_le (by norm_num) (by norm_num)
        _ = 2 := Real.rpow_one 2
    have : 0 ≤ (n * ℓ) ^ ((2 : ℝ) / 3) := by positivity
    nlinarith
  have hmm : m ^ ((1 : ℝ) / 3) * (m * (ℓ / pr)) ^ ((2 : ℝ) / 3) ≤ 3 * (m * e) := by
    have hq0 : 0 ≤ ℓ / pr := by positivity
    rw [Real.mul_rpow hm hq0]
    have hm13 : m ^ ((1 : ℝ) / 3) * m ^ ((2 : ℝ) / 3) = m := by
      rw [← Real.rpow_add' hm (by norm_num)]
      norm_num
    have hq4 : (ℓ / pr) ^ ((2 : ℝ) / 3) ≤ 3 * e := by
      have h4 : (ℓ / pr) ^ (4 : ℕ) ≤ 3 * ℓ := by
        rw [div_pow, div_le_iff₀ (by positivity)]
        linarith
      have e1 : (ℓ / pr) ^ ((2 : ℝ) / 3) = ((ℓ / pr) ^ (4 : ℕ)) ^ ((1 : ℝ) / 6) := by
        rw [← Real.rpow_natCast, ← Real.rpow_mul hq0]
        norm_num
      rw [e1]
      calc ((ℓ / pr) ^ (4 : ℕ)) ^ ((1 : ℝ) / 6) ≤ (3 * ℓ) ^ ((1 : ℝ) / 6) :=
            Real.rpow_le_rpow (by positivity) h4 (by norm_num)
        _ = (3 : ℝ) ^ ((1 : ℝ) / 6) * e := Real.mul_rpow (by norm_num) hl0.le
        _ ≤ 3 * e := by nlinarith
    calc m ^ ((1 : ℝ) / 3) * (m ^ ((2 : ℝ) / 3) * (ℓ / pr) ^ ((2 : ℝ) / 3))
        = m * (ℓ / pr) ^ ((2 : ℝ) / 3) := by rw [← mul_assoc, hm13]
      _ ≤ m * (3 * e) := mul_le_mul_of_nonneg_left hq4 hm
      _ = 3 * (m * e) := by ring
  have hm0' : 0 ≤ m ^ ((1 : ℝ) / 3) := Real.rpow_nonneg hm _
  have hlast : m ^ ((1 : ℝ) / 3) * (np * Real.log (np + 2)) ^ ((2 : ℝ) / 3)
      ≤ 6 * W + 9 * (m * e) := by
    have hS0 : 0 ≤ (2 * (n * ℓ)) ^ ((2 : ℝ) / 3) + (m * (ℓ / pr)) ^ ((2 : ℝ) / 3) := by positivity
    have hstep : (3 : ℝ) ^ ((2 : ℝ) / 3)
          * ((2 * (n * ℓ)) ^ ((2 : ℝ) / 3) + (m * (ℓ / pr)) ^ ((2 : ℝ) / 3))
        ≤ 3 * (2 * (n * ℓ) ^ ((2 : ℝ) / 3) + (m * (ℓ / pr)) ^ ((2 : ℝ) / 3)) :=
      mul_le_mul h3c (by linarith) hS0 (by norm_num)
    calc m ^ ((1 : ℝ) / 3) * (np * Real.log (np + 2)) ^ ((2 : ℝ) / 3)
        ≤ m ^ ((1 : ℝ) / 3) * ((3 : ℝ) ^ ((2 : ℝ) / 3)
            * ((2 * (n * ℓ)) ^ ((2 : ℝ) / 3) + (m * (ℓ / pr)) ^ ((2 : ℝ) / 3))) :=
          mul_le_mul_of_nonneg_left hY hm0'
      _ ≤ m ^ ((1 : ℝ) / 3) * (3 * (2 * (n * ℓ) ^ ((2 : ℝ) / 3) + (m * (ℓ / pr)) ^ ((2 : ℝ) / 3))) :=
          mul_le_mul_of_nonneg_left hstep hm0'
      _ = 6 * W + 3 * (m ^ ((1 : ℝ) / 3) * (m * (ℓ / pr)) ^ ((2 : ℝ) / 3)) := by rw [hW]; ring
      _ ≤ 6 * W + 9 * (m * e) := by linarith [hmm]
  linarith [hlogt, hlast, hnp, hmp]

/-- Young's inequality for the last term, the shape used by the `n log^b` rows. -/
theorem young_P {m n ℓ : ℝ} (hm : 0 ≤ m) (hn : 0 ≤ n) (hl : 0 < ℓ) :
    m ^ ((1 : ℝ) / 3) * (n * ℓ) ^ ((2 : ℝ) / 3)
      ≤ m * ℓ ^ ((1 : ℝ) / 6) + n * ℓ ^ ((11 : ℝ) / 12) := by
  have hp1 : 0 ≤ m * ℓ ^ ((1 : ℝ) / 6) := by positivity
  have hp2 : 0 ≤ n * ℓ ^ ((11 : ℝ) / 12) := by positivity
  have h := Real.geom_mean_le_arith_mean2_weighted (w₁ := (1 : ℝ) / 3) (w₂ := (2 : ℝ) / 3)
    (p₁ := m * ℓ ^ ((1 : ℝ) / 6)) (p₂ := n * ℓ ^ ((11 : ℝ) / 12))
    (by norm_num) (by norm_num) hp1 hp2 (by norm_num)
  have e1 : (m * ℓ ^ ((1 : ℝ) / 6)) ^ ((1 : ℝ) / 3) = m ^ ((1 : ℝ) / 3) * ℓ ^ ((1 : ℝ) / 18) := by
    rw [Real.mul_rpow hm (by positivity), ← Real.rpow_mul hl.le]
    norm_num
  have e2 : (n * ℓ ^ ((11 : ℝ) / 12)) ^ ((2 : ℝ) / 3)
      = n ^ ((2 : ℝ) / 3) * ℓ ^ ((11 : ℝ) / 18) := by
    rw [Real.mul_rpow hn (by positivity), ← Real.rpow_mul hl.le]
    norm_num
  have e3 : (n * ℓ) ^ ((2 : ℝ) / 3) = n ^ ((2 : ℝ) / 3) * ℓ ^ ((2 : ℝ) / 3) := Real.mul_rpow hn hl.le
  have e4 : ℓ ^ ((2 : ℝ) / 3) = ℓ ^ ((1 : ℝ) / 18) * ℓ ^ ((11 : ℝ) / 18) := by
    rw [← Real.rpow_add hl]
    norm_num
  rw [e1, e2] at h
  rw [e3, e4]
  have e5 : m ^ ((1 : ℝ) / 3) * (n ^ ((2 : ℝ) / 3) * (ℓ ^ ((1 : ℝ) / 18) * ℓ ^ ((11 : ℝ) / 18)))
      = m ^ ((1 : ℝ) / 3) * ℓ ^ ((1 : ℝ) / 18) * (n ^ ((2 : ℝ) / 3) * ℓ ^ ((11 : ℝ) / 18)) := by ring
  rw [e5]
  linarith

/-- Young's inequality, the shape used by the polynomial fallback. -/
theorem young_13 {m n ℓ : ℝ} (hm : 0 ≤ m) (hn : 0 ≤ n) (hl : 0 ≤ ℓ) :
    m ^ ((1 : ℝ) / 3) * (n * ℓ) ^ ((2 : ℝ) / 3) ≤ m * ℓ ^ 2 + n := by
  have hp1 : 0 ≤ m * ℓ ^ 2 := by positivity
  have h := Real.geom_mean_le_arith_mean2_weighted (w₁ := (1 : ℝ) / 3) (w₂ := (2 : ℝ) / 3)
    (p₁ := m * ℓ ^ 2) (p₂ := n) (by norm_num) (by norm_num) hp1 hn (by norm_num)
  have e1 : (m * ℓ ^ 2) ^ ((1 : ℝ) / 3) = m ^ ((1 : ℝ) / 3) * ℓ ^ ((2 : ℝ) / 3) := by
    rw [Real.mul_rpow hm (by positivity)]
    congr 1
    rw [← Real.rpow_natCast, ← Real.rpow_mul hl]
    norm_num
  have e3 : (n * ℓ) ^ ((2 : ℝ) / 3) = n ^ ((2 : ℝ) / 3) * ℓ ^ ((2 : ℝ) / 3) := Real.mul_rpow hn hl
  rw [e1] at h
  rw [e3]
  have e5 : m ^ ((1 : ℝ) / 3) * (n ^ ((2 : ℝ) / 3) * ℓ ^ ((2 : ℝ) / 3))
      = m ^ ((1 : ℝ) / 3) * ℓ ^ ((2 : ℝ) / 3) * n ^ ((2 : ℝ) / 3) := by ring
  rw [e5]
  linarith

/-- The padded C-HD time, on the padding branch (`n ≥ 65536`, `m/n ≤ n`). -/
theorem pad_tchd (hn : 65536 ≤ G.n) (hmn : G.m / G.n ≤ G.n) :
    GateCTarget.Tdisp GateCCalc.F (npad G.n G.m) G.m
      ≤ 2 * (G.n : ℝ) + 2 * (G.m : ℝ) + 27 * ((G.m : ℝ) * Real.log (G.n : ℝ) ^ ((1 : ℝ) / 6))
        + 6 * ((G.m : ℝ) ^ ((1 : ℝ) / 3) * ((G.n : ℝ) * Real.log (G.n : ℝ)) ^ ((2 : ℝ) / 3)) := by
  have hn16 : 16 ≤ G.n := by omega
  have hnpos : 0 < G.n := by omega
  set Fn := GateCCalc.F G.n with hFn
  have hF8 : 8 ≤ Fn := F_ge_eight hn
  have hFL : Fn ≤ Nat.log 2 G.n := F_le_log G.n
  have hF4 : Nat.log 2 G.n * Nat.log 2 G.n * Nat.log 2 G.n < 2 * Fn ^ 4 := by
    have h1 := lt_root4_succ_pow (Nat.log 2 G.n * Nat.log 2 G.n * Nat.log 2 G.n)
    rw [← F_eq_root4] at h1
    exact lt_of_lt_of_le h1 (succ_pow4_le hF8)
  -- the padded size
  set q := G.m / Fn with hqdef
  have hnp : npad G.n G.m = G.n + q + 1 := rfl
  have hmF : G.m < Fn * (q + 1) := by
    have h1 := Nat.div_add_mod G.m Fn
    have h2 := Nat.mod_lt G.m (by omega : Fn > 0)
    have h3 : Fn * (q + 1) = Fn * q + Fn := by ring
    rw [← hqdef] at h1
    rw [h3]
    linarith
  have hcond : G.m ≤ npad G.n G.m * GateCCalc.F (npad G.n G.m) := by
    have h1 : Fn * (q + 1) ≤ Fn * npad G.n G.m := Nat.mul_le_mul_left _ (by rw [hnp]; omega)
    have h2 : Fn * npad G.n G.m ≤ GateCCalc.F (npad G.n G.m) * npad G.n G.m :=
      Nat.mul_le_mul_right _ (F_mono (npad_ge _ _))
    rw [Nat.mul_comm (npad G.n G.m)]
    omega
  have hmFn : G.m ≤ Fn * npad G.n G.m := by
    have h1 : Fn * (q + 1) ≤ Fn * npad G.n G.m := Nat.mul_le_mul_left _ (by rw [hnp]; omega)
    omega
  have hmlt : G.m < (G.n + 1) * G.n := (Nat.div_lt_iff_lt_mul hnpos).mp (Nat.lt_succ_of_le hmn)
  have hq_le : q ≤ G.m := Nat.div_le_self _ _
  have hcube : npad G.n G.m + 2 ≤ G.n ^ 3 := by
    rw [hnp]
    have e1 : (G.n + 1) * G.n = G.n * G.n + G.n := by ring
    have e2 : G.n ^ 3 = G.n * (G.n * G.n) := by ring
    have h1 : 16 * (G.n * G.n) ≤ G.n * (G.n * G.n) := Nat.mul_le_mul_right _ hn16
    have h2 : 16 * G.n ≤ G.n * G.n := Nat.mul_le_mul_right _ hn16
    rw [e2]
    linarith
  -- now the reals
  unfold GateCTarget.Tdisp
  rw [if_pos hcond]
  unfold GateCCalc.Tchd
  set ℓ := Real.log (G.n : ℝ) with hℓdef
  have hℓ : (2.7 : ℝ) ≤ ℓ := log_ge (G := G) hn16
  have hℓL : ℓ ≤ ((Nat.log 2 G.n : ℕ) : ℝ) := ell_le_L (G := G) hn16
  have hLb : ((Nat.log 2 G.n : ℕ) : ℝ) ≤ 1.5 * ℓ := L_le_one_five (G := G) hn16
  have hpr1 : (1 : ℝ) ≤ (Fn : ℝ) := by exact_mod_cast (by omega : 1 ≤ Fn)
  have hprL : (Fn : ℝ) ≤ ((Nat.log 2 G.n : ℕ) : ℝ) := by exact_mod_cast hFL
  have hL3 : ((Nat.log 2 G.n : ℕ) : ℝ) ^ 3 ≤ 2 * (Fn : ℝ) ^ 4 := by
    have h1 : ((Nat.log 2 G.n * Nat.log 2 G.n * Nat.log 2 G.n : ℕ) : ℝ) ≤ ((2 * Fn ^ 4 : ℕ) : ℝ) := by
      exact_mod_cast hF4.le
    push_cast at h1
    have e : ((Nat.log 2 G.n : ℕ) : ℝ) ^ 3
        = ((Nat.log 2 G.n : ℕ) : ℝ) * ((Nat.log 2 G.n : ℕ) : ℝ) * ((Nat.log 2 G.n : ℕ) : ℝ) := by ring
    linarith
  have hℓ0 : 0 ≤ ℓ := by linarith
  have hpl : ℓ ^ 4 ≤ 3 * ℓ * (Fn : ℝ) ^ 4 := by
    have h1 : ℓ ^ 3 ≤ ((Nat.log 2 G.n : ℕ) : ℝ) ^ 3 := pow_le_pow_left₀ hℓ0 hℓL 3
    have e : ℓ ^ 4 = ℓ * ℓ ^ 3 := by ring
    have hF0 : 0 ≤ (Fn : ℝ) ^ 4 := by positivity
    have h2 := mul_le_mul_of_nonneg_left h1 hℓ0
    have h3 := mul_le_mul_of_nonneg_left hL3 hℓ0
    nlinarith
  have hprl : (Fn : ℝ) ≤ 1.5 * ℓ := le_trans hprL hLb
  have hnpR : ((npad G.n G.m : ℕ) : ℝ) ≤ 2 * (G.n : ℝ) + (G.m : ℝ) / (Fn : ℝ) := by
    have h1 : ((q : ℕ) : ℝ) ≤ (G.m : ℝ) / (Fn : ℝ) := Nat.cast_div_le
    have h2 : (1 : ℝ) ≤ (G.n : ℝ) := by exact_mod_cast (by omega : 1 ≤ G.n)
    rw [hnp]
    push_cast
    linarith
  have hlogR : Real.log ((npad G.n G.m : ℝ) + 2) ≤ 3 * ℓ := by
    have h1 : ((npad G.n G.m : ℝ) + 2) ≤ (G.n : ℝ) ^ 3 := by exact_mod_cast hcube
    have h2 := Real.log_le_log (by positivity) h1
    rw [Real.log_pow] at h2
    push_cast at h2
    linarith
  have hqR : (G.m : ℝ) / ((npad G.n G.m : ℝ) + 1) ≤ (Fn : ℝ) := by
    rw [div_le_iff₀ (by positivity)]
    have h1 : (G.m : ℝ) ≤ (Fn : ℝ) * (npad G.n G.m : ℝ) := by exact_mod_cast hmFn
    nlinarith
  exact master (by exact_mod_cast (by omega : 1 ≤ G.n)) (by linarith) (Nat.cast_nonneg _) hpr1
    hpl hprl (Nat.cast_nonneg _) hnpR hlogR hqR

/-- Closing arithmetic for the `n log^b` rows. -/
theorem final_P {n m ℓ L pr K q e f W T c : ℝ} (hn : 1 ≤ n) (hln : ℓ ≤ n) (hL : L ≤ 1.5 * ℓ)
    (hpr : pr ≤ L) (hK : 0 ≤ K) (hm0 : 0 ≤ m) (hq : 1 ≤ q) (he : 1 ≤ e)
    (hm : m ≤ 2.25 * n * q) (hf : f ≤ q * e) (hW : W ≤ m * e + n * f)
    (hT : T ≤ 2 * n + 2 * m + 27 * (m * e) + 6 * W)
    (hc : c ≤ 22 + 3 * L + 2 * pr + 12 * n + K * T) :
    c ≤ (2100 + 100 * K) * (n * (q * e)) := by
  have hqe : 1 ≤ q * e := by nlinarith
  have hn0 : 0 ≤ n := by linarith
  set X := n * (q * e) with hX
  have hX1 : n ≤ X := by nlinarith
  have hme : m * e ≤ 2.25 * X := by
    calc m * e ≤ (2.25 * n * q) * e := mul_le_mul_of_nonneg_right hm (by linarith)
      _ = 2.25 * X := by rw [hX]; ring
  have hmX : m ≤ 2.25 * X := by
    have : m ≤ m * e := by nlinarith
    linarith
  have hnf : n * f ≤ X := mul_le_mul_of_nonneg_left hf hn0
  have hT' : T ≤ 100 * X := by linarith
  have hKT : K * T ≤ K * (100 * X) := mul_le_mul_of_nonneg_left hT' hK
  have hfix : 22 + 3 * L + 2 * pr + 12 * n ≤ 2000 * X := by linarith
  have e1 : (2100 + 100 * K) * X = 2100 * X + 100 * (K * X) := by ring
  have e2 : K * (100 * X) = 100 * (K * X) := by ring
  linarith

/-- Closing arithmetic for the polynomial fallback on the padding branch. -/
theorem final_C2 {n m ℓ L pr K e W T c : ℝ} (hn : 1 ≤ n) (hl1 : 1 ≤ ℓ) (hln : ℓ ≤ n)
    (hll : ℓ ^ 2 ≤ n) (hL : L ≤ n) (hpr : pr ≤ L) (hK : 0 ≤ K) (hm0 : 0 ≤ m) (he : e ≤ ℓ)
    (hW : W ≤ m * ℓ ^ 2 + n) (hT : T ≤ 2 * n + 2 * m + 27 * (m * e) + 6 * W)
    (hc : c ≤ 22 + 3 * L + 2 * pr + 12 * n + K * T) :
    c ≤ (2100 + 100 * K) * (n + 1) * (m + 1) := by
  set Y := (n + 1) * (m + 1) with hY
  have hY1 : 1 ≤ Y := by nlinarith
  have hnY : n ≤ Y := by nlinarith
  have hmY : m ≤ Y := by nlinarith
  have hmnY : m * n ≤ Y := by nlinarith
  have hme : m * e ≤ Y := by
    have h1 : m * e ≤ m * n := mul_le_mul_of_nonneg_left (le_trans he hln) hm0
    linarith
  have hml : m * ℓ ^ 2 ≤ Y := by
    have h1 : m * ℓ ^ 2 ≤ m * n := mul_le_mul_of_nonneg_left hll hm0
    linarith
  have hT' : T ≤ 50 * Y := by linarith
  have hKT : K * T ≤ K * (50 * Y) := mul_le_mul_of_nonneg_left hT' hK
  have hfix : 22 + 3 * L + 2 * pr + 12 * n ≤ 2000 * Y := by linarith
  have e1 : (2100 + 100 * K) * (n + 1) * (m + 1) = 2100 * Y + 100 * (K * Y) := by rw [hY]; ring
  have e2 : K * (50 * Y) = 50 * (K * Y) := by ring
  have hKY : 0 ≤ K * Y := by positivity
  linarith

/-! ## 12. The clauses -/

/-- Polynomial fallback, every graph. -/
theorem clause2_p3 (K : ℝ) (hK0 : 0 ≤ K) (hE : Frontier.CHD.Final.chdProgram.Exact)
    (hW : ∀ (H : Graph) (z : Fin H.n),
      Frontier.CHD.Final.chdProgram.RunsWithin H z (K * GateCTarget.Tdisp GateCCalc.F H.n H.m)) :
    ∀ (G : Graph) (s : Fin G.n),
      CorrectWithin p3 G s ((2100 + 100 * K) * ((G.n : ℝ) + 1) * ((G.m : ℝ) + 1)) := by
  intro G s
  have hnR : (0 : ℝ) ≤ (G.n : ℝ) := Nat.cast_nonneg _
  have hmR : (0 : ℝ) ≤ (G.m : ℝ) := Nat.cast_nonneg _
  have hY1 : (1 : ℝ) ≤ ((G.n : ℝ) + 1) * ((G.m : ℝ) + 1) := by nlinarith
  have hCY : 2002 * (((G.n : ℝ) + 1) * ((G.m : ℝ) + 1))
      ≤ (2100 + 100 * K) * ((G.n : ℝ) + 1) * ((G.m : ℝ) + 1) := by
    have : 0 ≤ K * (((G.n : ℝ) + 1) * ((G.m : ℝ) + 1)) := by positivity
    nlinarith
  by_cases h1 : G.n < 65536
  · obtain ⟨f, r, hr, hS, hc⟩ := body3_small (G := G) (s := s) h1
    exact ⟨f, r, hr, hS, by nlinarith⟩
  push_neg at h1
  by_cases h2 : G.n < G.m / G.n
  · obtain ⟨f, r, hr, hS, hc⟩ := body3_dense (G := G) (s := s) h1 h2
    exact ⟨f, r, hr, hS, by nlinarith⟩
  push_neg at h2
  obtain ⟨f, r, hr, hS, hc⟩ := body3_pad (G := G) (s := s) K hE hW h1 h2
  refine ⟨f, r, hr, hS, ?_⟩
  have hn16 : 16 ≤ G.n := by omega
  have hT := pad_tchd (G := G) h1 h2
  set ℓ := Real.log (G.n : ℝ) with hℓdef
  have hℓ : (2.7 : ℝ) ≤ ℓ := log_ge (G := G) hn16
  have hn1 : (1 : ℝ) ≤ (G.n : ℝ) := by exact_mod_cast (by omega : 1 ≤ G.n)
  have hℓn : ℓ ≤ (G.n : ℝ) := by
    have := Real.log_le_sub_one_of_pos (by linarith : (0 : ℝ) < G.n)
    linarith
  have hℓL : ℓ ≤ ((Nat.log 2 G.n : ℕ) : ℝ) := ell_le_L (G := G) hn16
  have hL4 : 4 ≤ Nat.log 2 G.n := Nat.le_log_of_pow_le (by norm_num) (by simpa using hn16)
  have hLLn : ((Nat.log 2 G.n : ℕ) : ℝ) * ((Nat.log 2 G.n : ℕ) : ℝ) ≤ (G.n : ℝ) := by
    have h1 : Nat.log 2 G.n ^ 2 ≤ 2 ^ Nat.log 2 G.n := sq_le_two_pow _ hL4
    have h2 : 2 ^ Nat.log 2 G.n ≤ G.n := Nat.pow_log_le_self 2 (by omega)
    have h3 : Nat.log 2 G.n * Nat.log 2 G.n ≤ G.n := by nlinarith
    exact_mod_cast h3
  have hℓ0 : 0 ≤ ℓ := by linarith
  have hll : ℓ ^ 2 ≤ (G.n : ℝ) := by nlinarith
  have hLn : ((Nat.log 2 G.n : ℕ) : ℝ) ≤ (G.n : ℝ) := Nat.cast_le.mpr (Nat.log_le_self 2 G.n)
  have hFL : (GateCCalc.F G.n : ℝ) ≤ ((Nat.log 2 G.n : ℕ) : ℝ) := by exact_mod_cast F_le_log G.n
  have he : ℓ ^ ((1 : ℝ) / 6) ≤ ℓ := by
    calc ℓ ^ ((1 : ℝ) / 6) ≤ ℓ ^ (1 : ℝ) :=
          Real.rpow_le_rpow_of_exponent_le (by linarith) (by norm_num)
      _ = ℓ := Real.rpow_one ℓ
  have hW := young_13 (Nat.cast_nonneg G.m) hnR hℓ0
  have hc' : (r.cost : ℝ) ≤ 22 + 3 * ((Nat.log 2 G.n : ℕ) : ℝ) + 2 * (GateCCalc.F G.n : ℝ)
      + 12 * (G.n : ℝ) + K * GateCTarget.Tdisp GateCCalc.F (npad G.n G.m) G.m := by
    unfold kSetup at hc
    push_cast at hc
    linarith
  exact final_C2 hn1 (by linarith) hℓn hll hLn hFL hK0 hmR he hW hT hc'

/-- Clause 1 for the rows `D = n·⌊⌊log₂ n⌋^b⌋`, `T = n·(log n)^(b + 1/6)`, `3/4 ≤ b ≤ 2`. -/
theorem clause1_P (K : ℝ) (hK0 : 0 ≤ K) (hE : Frontier.CHD.Final.chdProgram.Exact)
    (hW : ∀ (H : Graph) (z : Fin H.n),
      Frontier.CHD.Final.chdProgram.RunsWithin H z (K * GateCTarget.Tdisp GateCCalc.F H.n H.m))
    (b b' : ℚ) (hb0 : 3 / 4 ≤ b) (hb2 : b ≤ 2) (hb' : b' = b + 1 / 6) :
    ∀ (G : Graph) (s : Fin G.n), 65536 ≤ G.n → Sparse ((1 : ℚ) / 1) b G.n G.m →
      CorrectWithin p3 G s ((2100 + 100 * K) * Time ((1 : ℚ) / 1) b' ((0 : ℚ) / 1) G.n) := by
  intro G s hn hsp
  have hn16 : 16 ≤ G.n := by omega
  have hbR0 : (3 / 4 : ℝ) ≤ (b : ℝ) := by
    have h := (Rat.cast_le (K := ℝ)).mpr hb0
    push_cast at h
    linarith
  have hbR2 : (b : ℝ) ≤ 2 := by
    have h := (Rat.cast_le (K := ℝ)).mpr hb2
    push_cast at h
    linarith
  set L : ℝ := ((Nat.log 2 G.n : ℕ) : ℝ) with hLdef
  set ℓ : ℝ := Real.log (G.n : ℝ) with hℓdef
  have hnR : (16 : ℝ) ≤ (G.n : ℝ) := by exact_mod_cast hn16
  have hℓ : (2.7 : ℝ) ≤ ℓ := log_ge (G := G) hn16
  have hℓ0 : 0 < ℓ := by linarith
  have hLb : L ≤ 1.5 * ℓ := L_le_one_five (G := G) hn16
  have hL0 : 0 ≤ L := by positivity
  have hL4 : (4 : ℕ) ≤ Nat.log 2 G.n := Nat.le_log_of_pow_le (by norm_num) (by simpa using hn16)
  have hL1 : (1 : ℝ) ≤ L := by
    have : (4 : ℝ) ≤ L := by rw [hLdef]; exact_mod_cast hL4
    linarith
  have hsp' : (G.m : ℝ) ≤ (G.n : ℝ) * (⌊L ^ (b : ℝ)⌋₊ : ℝ) := by
    have := hsp; rw [Sparse, cap_one_b'] at this; exact this
  have hfl : (⌊L ^ (b : ℝ)⌋₊ : ℝ) ≤ L ^ (b : ℝ) := Nat.floor_le (by positivity)
  have hnR0 : (0 : ℝ) ≤ (G.n : ℝ) := Nat.cast_nonneg _
  have hmLb : (G.m : ℝ) ≤ (G.n : ℝ) * L ^ (b : ℝ) :=
    le_trans hsp' (mul_le_mul_of_nonneg_left hfl hnR0)
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
  have hq : L ^ (b : ℝ) ≤ 2.25 * ℓ ^ (b : ℝ) := by
    have h1 : L ^ (b : ℝ) ≤ (1.5 * ℓ) ^ (b : ℝ) := Real.rpow_le_rpow hL0 hLb (by linarith)
    have h2 : (1.5 * ℓ) ^ (b : ℝ) = (1.5 : ℝ) ^ (b : ℝ) * ℓ ^ (b : ℝ) :=
      Real.mul_rpow (by norm_num) hℓ0.le
    have h3 : (1.5 : ℝ) ^ (b : ℝ) ≤ 2.25 := by
      calc (1.5 : ℝ) ^ (b : ℝ) ≤ (1.5 : ℝ) ^ (2 : ℝ) :=
            Real.rpow_le_rpow_of_exponent_le (by norm_num) hbR2
        _ = 2.25 := by rw [Real.rpow_two]; norm_num
    have h4 : 0 ≤ ℓ ^ (b : ℝ) := by positivity
    rw [h2] at h1
    nlinarith
  have hq1 : (1 : ℝ) ≤ ℓ ^ (b : ℝ) := Real.one_le_rpow (by linarith) (by linarith)
  have hm225 : (G.m : ℝ) ≤ 2.25 * (G.n : ℝ) * ℓ ^ (b : ℝ) := by
    have := mul_le_mul_of_nonneg_left hq hnR0
    nlinarith [hmLb, this]
  have hdiv : G.m / G.n ≤ G.n := Nat.div_le_of_le_mul hmN
  obtain ⟨fuel, r, hr, hsv, hc⟩ := body3_pad (G := G) (s := s) K hE hW hn hdiv
  refine ⟨fuel, r, hr, hsv, ?_⟩
  have hT := pad_tchd (G := G) hn hdiv
  have hW' := young_P (Nat.cast_nonneg G.m) hnR0 hℓ0
  have hℓn : ℓ ≤ (G.n : ℝ) := by
    have := Real.log_le_sub_one_of_pos (by linarith : (0 : ℝ) < G.n)
    linarith
  have hFL : (GateCCalc.F G.n : ℝ) ≤ L := by rw [hLdef]; exact_mod_cast F_le_log G.n
  have he1 : (1 : ℝ) ≤ ℓ ^ ((1 : ℝ) / 6) := Real.one_le_rpow (by linarith) (by norm_num)
  have hf : ℓ ^ ((11 : ℝ) / 12) ≤ ℓ ^ (b : ℝ) * ℓ ^ ((1 : ℝ) / 6) := by
    rw [← Real.rpow_add hℓ0]
    exact Real.rpow_le_rpow_of_exponent_le (by linarith) (by linarith)
  have hc' : (r.cost : ℝ) ≤ 22 + 3 * L + 2 * (GateCCalc.F G.n : ℝ) + 12 * (G.n : ℝ)
      + K * GateCTarget.Tdisp GateCCalc.F (npad G.n G.m) G.m := by
    unfold kSetup at hc
    push_cast at hc
    rw [hLdef]
    linarith
  have hfin := final_P (by linarith) hℓn hLb hFL hK0 (Nat.cast_nonneg _) hq1 he1 hm225 hf hW' hT hc'
  have htime : Time ((1 : ℚ) / 1) b' ((0 : ℚ) / 1) G.n
      = (G.n : ℝ) * (ℓ ^ (b : ℝ) * ℓ ^ ((1 : ℝ) / 6)) := by
    rw [time_one_b', hb']
    push_cast
    rw [Real.rpow_add hℓ0]
  rw [htime]
  exact hfin

/-! ## 13. The rows -/

/-- **Family P**: `Bound 1 b 1 (b + 1/6) 0` for every `3/4 ≤ b ≤ 2`, from one program. -/
theorem pad_bound_P (b b' : ℚ) (hb0 : 3 / 4 ≤ b) (hb2 : b ≤ 2) (hb' : b' = b + 1 / 6) :
    Bound ((1 : ℚ) / 1) b ((1 : ℚ) / 1) b' ((0 : ℚ) / 1) := by
  obtain ⟨K, hK0, hE, hW⟩ := chd_K
  have c2 := clause2_p3 K hK0 hE hW
  refine ⟨p3, ?_, 2100 + 100 * K, by linarith, 65536, by norm_num,
    clause1_P K hK0 hE hW b b' hb0 hb2 hb', c2⟩
  intro G s
  obtain ⟨f, r, hr, hs, _⟩ := c2 G s
  exact ⟨f, r, hr, hs⟩

end Submission.PadCHD

/-- `n log ; n log^7/6`. -/
example : BigOSpeedrun.DirectedSSSP.Bound ((1 : ℚ) / 1) ((1 : ℚ) / 1) ((1 : ℚ) / 1)
    ((7 : ℚ) / 6) ((0 : ℚ) / 1) :=
  Submission.PadCHD.pad_bound_P _ _ (by norm_num) (by norm_num) (by norm_num)

#print axioms Submission.PadCHD.pad_bound_P
