# Map-preserving rewrites to create a third helper split: negative result (2026-11-23)

I used only our own scripts. They read the #8027 data as data and run none of the package's code. The base is the final word from `/home/claude/work/words.pkl` (raw κ 0.0038984814465, checked by `chk.check`). **No candidate word came out of this, so κ is unchanged.**

## 1. Cross edits (idea 1: free edits)
**Edit family (`rw_lib.cross_edit`, `rw_lib.input_edit`).** Pick a (class G, chart c) pair where both a G-supported resident combination μ (form s0) and a G-supported row combination λ (adjoint h0) exist (the 46 pairs from scan.py). Then:
- add δ·λ_k·(μ-combination) to each row k in λ. The map changes by δ h0⊗s0.
- cancel that change, either
  - **O** at the shared final chart z: output_j -= δ h0_j Σ s0_i · (output_i's row), or
  - **I** at the shared initial chart: every use of input j gets −δ q h0_j Σ s0_i x_i. This is exact because s0·h0 = 0.

Both variants preserve the map exactly. On the 599 example (G = 3→1091, s0 = e640, h0 = e1195), `chk.check` gives bad_outputs 0 and the same κ.

**First-order screen (`rw_screen.py`).** For a cross edit at (c; s0,h0), the pairing between (s2,h2) at another chart c2 of the same class changes by

    Δ = δ[ (α − s2·h0)(s0·h2) + β (s2·h0) ],   α = ∂S2/∂ρ0,  β = ∂S0/∂ρ2

The formula is the same for O and I. Over all 1,942 (edit, target) basis combinations the result is **Δ = 0 in every case**:
- In 1,902 combinations every term is already zero: s2·h0 = s0·h2 = 0 across charts. All G-supported resident forms and all G-supported row adjoints of a class are mutually orthogonal, not just those at the same chart.
- In the other 40, the terms that are nonzero cancel exactly:
  - α = s2·h0 in all 4+10 cases where α ≠ 0;
  - β = s0·h2 in all 4+10 cases where β ≠ 0.

So "injecting at ρ0" and "perturbing the inputs by h0" move every G-supported resident identically.

**Exact brute force (`rw_drive1.py`).** I applied each single cross edit (O and I, δ = 3/7) and rescanned the class. In the 57 edits finished before I stopped, no pairing appeared (log: `rw_drive1.partial.out`). The worked example at 599 shows why: the new resident at 261 becomes e1195 − δ e640 and the new adjoint becomes e640 + δ e1195, so the pairing stays 0. These edits act as a gauge transform (T on the forms, T^{-T} on the adjoints) along every path they touch.

**Consequence for link merges.** To make two transfers on one link parallel under such an edit, some combination of them would need sensitivity to ρ0 equal to s·h0, and that is 0. So this family cannot produce link merges either.

## 2. Rank structure (`rw_rank.py`)
At all 1,103 charts:
- the outgoing adjoints (moves out plus outputs) have full rank;
- the incoming forms (moves in plus inputs) have full rank.

There are no type-(a) or type-(b) free edits at any chart. Across the 1,826 links with ≥2 transfers (4,563 transfers in all), no link has dependent forms or dependent adjoints. So no transfer can be removed or merged locally for free.

## 3. #8027 coordinates (`rw_xcoords.py`; idea 2)
Here u_X is the form on the 384 inputs outside chart 3, and z_X is M⁻¹·adjoint restricted to X.
- Of the 5,674 transfers, 1,674 have u_X = 0, 1,645 have z_X = 0, and 907 have both.
- **680 links still carry the exact #8027 pattern:** one (0,z) transfer and one (u,0) transfer on the same link. By grade: {1: 542, 2: 49, 3: 19, 4: 39, 5: 31}. **None is above grade 5**, so this word has no 8+8-type high-grade merge sitting on a single link.
- Each such merge needs its flow (u1⊗z2) absorbed around a cycle with per-chart conservation. With full-rank incoming forms, conservation plus "outgoing forms lie in the span of incoming" is sufficient for K. I did not build this cycle search within the budget. It is the natural next step and needs #8027's chart-equation solver.

## Files
| File | Contents |
|---|---|
| `rw_lib.py` | scan with vectors, cross_edit / input_edit, ratvec / realize, κ root |
| `rw_screen.py` | first-order identity screen |
| `rw_drive1.py` | exact brute force |
| `rw_rank.py` | rank census |
| `rw_xcoords.py` | #8027-coordinate census |
| `rw_info.py`, `rw_sub.py` | support dumps |
