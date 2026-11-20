# Directed SSSP: gap-fill row n·log^{15/8} n at density m ≤ n·log^{7/8} n

The binary-heap Dijkstra row from darkhipo/sssp-nlogn, extended to every density n·log^b n with 0 ≤ b ≤ 1. The program `p1` is unchanged; only the clause-1 arithmetic is new. At density n·log^{7/8} n it gives time n·log^{15/8} n, which beats the best Lean Verified time at that density (n log² n).

- `DijkstraRowB.lean` goes next to `Submission/DijkstraRow.lean` in darkhipo/sssp-nlogn @ 1129aca.
- `SubmissionB.lean` exports `Race.bound : Bound 1 (7/8) 1 (15/8) 0`.
- Built 2026-11-20 with Lean v4.34.1 and Mathlib d13f23b: `lake build Submission.DijkstraRowB` passes with no `sorry`, and the only axioms are propext, Classical.choice and Quot.sound.

Credit: the program, model and the rest of the proof are darkhipo's. Status: Claimed.
