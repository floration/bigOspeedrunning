# Unit-distance grid: max gamified vs as intended (2026-11-21)

The metric is the "number of selected edges Nj in the final algebraic-grid proof
step". The current record is 8×4 = 32.

| Version | Number | What it counts | Why it is or isn't fair |
|---|---|---|---|
| **As intended** | **30** | complete 6×5 grid, N·j | It covers every case, reads the metric literally as N·j, and relies on the same imported lemmas as the record. |
| Mild gaming | 29 | 6×5 grid minus one edge | The edges actually used. Defensible ("selected edges"), but it isn't of the form N·j. |
| Gamed: branch picking | 12 | common-line branch only (4×3) | The general case still needs 29 or 30. Rohan's README lists the 12 too and doesn't headline it. |
| Gamed: conditional branch | 10 | 2×5 grid, derivative chosen to kill anchor coordinates | Only valid when some λ is transcendental over k₀(anchors), so it is a conditional result. |
| Max gamified | 5 | edges at the surviving point in the final sign-change step | The literal "final step" uses one point × 5 anchors. That ignores the grid needed to make that point exist. Rohan's 32 would equally become 4. |

Parameter gaming tried:
- I tried every N×j ≤ 31 and every 28-edge subgraph. None is rigid on plane loci,
  so nothing below 29 survives without changing what is counted.
- 5×6 and 6×5 tie at 30, and 4×8 and 8×4 tie at 32.

Recommendation: submit **30** (complete grid), and mention **29** as the edge-pattern
refinement. The numbers 12, 10 and 5 would misstate the result if posted as a record.
