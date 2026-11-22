import Submission.SsspStatement
import Submission.PadCHD

/-!
The `n·log n ; n·log^{7/6} n` row for the Big O Speedrun directed shortest paths race.
One uniform program: Dijkstra / Bellman–Ford below `n = 65536` or above `m = n²`; otherwise it
pads the graph with `⌊m / F n⌋ + 1` isolated vertices (`F n = ⌊⌊log₂ n⌋^{3/4}⌋`), runs the
Lean-verified C-HD program (Vals AI) on the padded graph, and copies the first `n` labels back.
Any `3/4 ≤ b ≤ 2` gives `n log^b ; n log^{b+1/6}` from the same proof (`pad_bound_P`).
-/

theorem Race.bound :
    BigOSpeedrun.DirectedSSSP.Bound ((1 : ℚ) / 1) ((1 : ℚ) / 1) ((1 : ℚ) / 1) ((7 : ℚ) / 6)
      ((0 : ℚ) / 1) :=
  Submission.PadCHD.pad_bound_P _ _ (by norm_num) (by norm_num) (by norm_num)
