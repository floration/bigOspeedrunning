import Submission.SsspStatement
import Submission.DijkstraRowC

-- Row `n log^2 ; n log^3` (Family A, b = 2).
theorem Race.bound :
    BigOSpeedrun.DirectedSSSP.Bound ((1 : ℚ) / 1) ((2 : ℚ) / 1) ((1 : ℚ) / 1) ((3 : ℚ) / 1)
      ((0 : ℚ) / 1) :=
  Submission.DijkstraRowC.dijkstra_bound_A _ _ (by norm_num) (by norm_num) (by norm_num)

-- Row `n^3/2 ; n^3/2 log` (Family B, a = 3/2), for a separate submission.
example :
    BigOSpeedrun.DirectedSSSP.Bound ((3 : ℚ) / 2) ((0 : ℚ) / 1) ((3 : ℚ) / 2) ((1 : ℚ) / 1)
      ((0 : ℚ) / 1) :=
  Submission.DijkstraRowC.dijkstra_bound_poly _ (by norm_num) (by norm_num)
