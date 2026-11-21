# Unit-distance grid: five-idea round (2026-11-21)

The bound stays at **29 selected edges** (6×5 grid minus one edge).
Script: `check_five_ideas.py` (floating-point sanity checks, not proofs).

1. **Novel: second-order prolongation.**
   - The idea was to differentiate the system twice, to get extra constraints on the
     first-order data.
   - The second-order unknowns see the same coefficient matrix. On 5×5, 7×4 and 4×7
     that matrix has full row rank (25/25, 28/28, 28/28), so the inhomogeneous terms
     are always solvable.
   - Result: no new constraint. Dead.
2. **Crazy: let one point sit on both sides of the grid.**
   - Then H_i = U_ℓ, which saves 2 unknowns per shared vertex.
   - The pattern then needs triangles, or a vertex used in both copies. A dense
     bipartite G with disjoint sides contains neither, and the supersaturation count
     only finds bipartite patterns.
   - Result: not available.
3. **Borrowed (rigidity theory): treat the system as a rigidity matroid.**
   - Trivial motions span 4 dimensions, so a contradiction needs E ≥ 3V − 4. Henneberg
     style vertex additions give the step lemma.
   - This confirms 29 (V = 11) as the floor for any edge pattern. No pattern on
     V ≤ 10 fits, and no 28-edge subgraph of 6×5 works (all 435 tested).
4. **Reverse: start from the obstruction kernel vector y.**
   - On a 5×5 grid, every k₀-derivation's data is (trivial) + s·y. So
     trdeg_{k₀} k₀(λ) ≤ 1.
   - Derivations that also kill t act on positions only as rigid motions, so the
     positions have trdeg ≤ 4 over k₀.
   - That is a clean structural dichotomy, but contradicting it needs height
     information on positions, which the source does not supply.
   - Result: no unconditional gain.
5. **Breaking: drop "∂ arbitrary" and pick ∂ to kill the anchor coordinates
   (U_ℓ = 0).**
   - Only the shift remains as a trivial motion, and the count becomes E ≥ 3N + j − 1.
   - Numerically **2×5 = 10** and **3×4 = 12** force the contradiction on all 5 locus
     pairs tested. 2×4 and 1×5 do not.
   - It is only valid in the branch where some λ is transcendental over k₀(anchor
     coordinates). In the other branch all λ are algebraic over k₀(r), and the
     argument says nothing there.
   - Result: a conditional 10-edge branch, not an unconditional bound.
