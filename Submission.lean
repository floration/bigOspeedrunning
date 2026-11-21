import Submission.SsspStatement
import Submission.DijkstraRowB

theorem Race.bound :
    BigOSpeedrun.DirectedSSSP.Bound ((1 : ℚ) / 1) ((7 : ℚ) / 8) ((1 : ℚ) / 1) ((15 : ℚ) / 8)
      ((0 : ℚ) / 1) :=
  Submission.DijkstraRowB.dijkstra_bound_b _ _ (by norm_num) (by norm_num) (by norm_num)
