# Directed SSSP: Dijkstra gap-fill rows

These rows extend the binary-heap Dijkstra row from darkhipo/sssp-nlogn @ 1129aca to more densities. Each one beats the best Lean Verified time at its density. All files built on 2026-11-20 inside that repo with Lean v4.34.1 and Mathlib d13f23b. None contains `sorry`, and the only axioms are propext, Classical.choice and Quot.sound.

| File | Program | Rows |
|---|---|---|
| `DijkstraRowB.lean` + `SubmissionB.lean` | darkhipo's `p1`, unchanged | `Bound 1 b 1 (1+b) 0` for 0 ≤ b ≤ 1. Submitted row: m ≤ n log^{7/8} n in time n log^{15/8} n (vs n log² n) |
| `DijkstraRowC.lean` + `SubmissionC.lean` | `p2`: dispatch threshold raised to m/n ≤ n | `Bound 1 b 1 (1+b) 0` for 0 ≤ b ≤ 2, e.g. n log² n density in time n log³ n (vs n²). Also `Bound a 0 a 1 0` for 1 ≤ a ≤ 2, e.g. n^{3/2} density in time n^{3/2} log n (vs n²) |

Place `DijkstraRow*.lean` under `Submission/` next to `DijkstraRow.lean`; `Submission*.lean` export `Race.bound` (SubmissionC's second row is an `example`, for a separate submission).

Credit: the model, Dijkstra/Bellman-Ford programs and most of the proof are darkhipo's. Status: Claimed.
