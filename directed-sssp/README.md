# Directed SSSP: Dijkstra gap-fill rows

These rows extend the binary-heap Dijkstra row from darkhipo/sssp-nlogn @ 1129aca to more densities. Each one beats the best Lean Verified time at its density. All files built on 2026-11-20 inside that repo with Lean v4.34.1 and Mathlib d13f23b. None contains `sorry`, and the only axioms are propext, Classical.choice and Quot.sound.

| File | Program | Rows |
|---|---|---|
| `DijkstraRowB.lean` + `SubmissionB.lean` | darkhipo's `p1`, unchanged | `Bound 1 b 1 (1+b) 0` for 0 ≤ b ≤ 1. Submitted row: m ≤ n log^{7/8} n in time n log^{15/8} n (vs n log² n) |
| `DijkstraRowC.lean` + `SubmissionC.lean` | `p2`: dispatch threshold raised to m/n ≤ n | `Bound 1 b 1 (1+b) 0` for 0 ≤ b ≤ 2, e.g. n log² n density in time n log³ n (vs n²). Also `Bound a 0 a 1 0` for 1 ≤ a ≤ 2, e.g. n^{3/2} density in time n^{3/2} log n (vs n²) |

Place `DijkstraRow*.lean` under `Submission/` next to `DijkstraRow.lean`; `Submission*.lean` export `Race.bound` (SubmissionC's second row is an `example`, for a separate submission).

Credit: the model, Dijkstra/Bellman-Ford programs and most of the proof are darkhipo's. Status: Claimed.

## On paper only: O(m log^{1/6} n) above C-HD's density (`five-ideas.md`)
This extends C-HD past m ≤ n log^{3/4} n, giving T = O(n log^{b+1/6} n) at density n log^b n. It is a written argument, not built in Lean, and isn't part of any submission yet.

## Padding row (Family D): n·log^{7/6} n at m ≤ n log n
`Race.bound = Bound 1 1 1 (7/6) 0`. This pads the C-HD algorithm (bigospeedrun/c-hd-proof) to density n log n. `Submission.PadCHD` and `Submission.SubmissionD` built on q's PC with only the standard axioms. The built `PadCHD.lean` has sha256 starting b01faa9a and ending e864. It will be added here once it's copied off the PC; the earlier draft isn't the built version.
