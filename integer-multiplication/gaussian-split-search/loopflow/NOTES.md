# Loop-flow merge search on #8027's final word: partial result, stopped early (2026-11-23)

The coordinator stopped this work, because another thread's shortcut word (raw root 0.0039014662) is already above the binary ceiling. **No merge word was built or installed.** All code is our own and runs no package code.

## Candidates (`lf_cands.py`, saved in `cands.pkl`)
- There are **680 pattern links**, which give **708 (v1, v2) pairs**. Here v1 has u_X ≠ 0 and z_X = 0, and v2 has u_X = 0 and z_X ≠ 0. The grades are {1: 542, 2: 49, 3: 19, 4: 39, 5: 31}, and none is above 5.
- **Error from a plain merge.** Merging the two into w = v1 + t·v2, with v2's readers taking β·w, leaves a recovered-map error of t·z1⊗u2 + β·z2⊗u1 + (βt−1)·z2⊗u2.
  - The z1⊗u2 term lies in the chart-3 × chart-3 block. Re-encoding the chart-3 inputs by B⁻¹ absorbs it, as #8027 does.
  - The z2 terms have to be cancelled elsewhere.
- **Single third-chart closure.** This needs a chart c, other than a or b, where u1 (the full form of v1) is in the span of the resident forms and b_v2 (the full adjoint of v2) is in the span of the row adjoints. Matching the X-3 and 3-X blocks forces both vectors to be matched exactly.
  - In 708 of 708 pairs, u1 lies in the resident span at some chart (counting a and b).
  - Only **202 pairs** have such a third chart c. By grade: {1: 185, 2: 8, 3: 4, 4: 5}. There are no grade-5 pairs.
- **Exact solvability.** Let the cancelling edit subtract σ·(μ-combination) from the λ rows at c. Let p1 and p2 be the sensitivity of μ to the v1 and v2 slots, and q1 and q2 the sensitivity of those slots to λ. Working the error out exactly gives:
  - **c downstream (q = 0):** σ·(t·(1 − p1) + p2) = 1 and β = σ/(1 − σ·p2). This is impossible when p1 = 1 and p2 = 0.
  - **c upstream (p = 0):** q2 = 0 is required, and then β = 1/t and σ = 1/(q1 + t).
  - **Both nonzero:** a loop, not handled.

## Built so far (`lf_build.py`, saved in `results.pkl`)
- I tested the first 3 pairs in grade order. All are grade 4 with c = 127: (242→477), (242→517) and (235→518).
- All 3 have p1 = 1 and p2 = 0, so the equation has no solution: the only copy of u1 at c arrives through v1 itself. None of them reached a built word.
- The screen of p and q over all 202 pairs (`lf_screen.py`) was stopped before it finished, so I have no counts from it.

## Open work
- Finish the screen.
- Build the upstream case where q2 = 0.
- Allow closures over two charts (u1 split between two charts) and full cycle solves in the #8027 style.
