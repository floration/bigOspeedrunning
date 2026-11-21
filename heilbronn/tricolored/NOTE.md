# Heilbronn: tricolored packing (the "breaking" idea)

## Idea
Blinov's reserved-tag checkpoint puts each norm word at the same position u in rows 1 and 2 (i_a = j_a), so the matching condition becomes "S has no 3-term progression". The manuscript only needs the matching property

    i_a + j_b + ℓ_c = k − 1  ⇔  a = b = c

and the pinned manuscript itself uses i_a = a, j_a = T·a, so the rows differ there. Dropping i_a = j_a turns the problem into finding a **tricolored sum-free family** of pairs (x_a, y_a), with ℓ_a = K − x_a − y_a. These families are strictly denser than 3-AP-free sets. For example, mod 21 the best family has 7 pairs where a 3-AP-free set has 6, and mod 25 the best has 8. The cap-set analogue in F_3^n (Kleinberg–Sawin–Speyer) behaves the same way.

## Construction
The pairs are triples (x, y) of the form x = x1 + 25·x2 + 625·x3 + 13125·x4 (y likewise), where:

* (x1, y1) and (x2, y2) range over the exact-optimal 8-pair family mod 25, after a translation and unit scaling,
* (x3, y3) ranges over the 7-pair family mod 21,
* (x4, y4) ranges over a 7-pair integer family with x + y ≤ 18.

A mod-25, mod-25, mod-21 descent shows the product family is tricolored. We keep the 2,916 pairs with x, y ≥ 10 and smallest x + y, then shift ℓ so that K = max(x + y). The 5 tag positions in [0, 10) are chosen afterwards so that every tag exclusion holds. The verifier checks this directly.

| version | tags | k | η = 2/(249k+5) |
|---|---|---|---|
| tricolored, tag span 10 (Blinov's text) | {0,1,2,3,4} | 246,191 | 1/30,650,782 ≈ 3.2626·10^-8 |
| tricolored, tag span 6 (gamified) | {0,1,2,3,5} | 246,176 | 2/61,297,829 ≈ 3.2628·10^-8 |
| 3-AP-free, i = j (../NOTE.md) | {0,2,3,5,9} | 317,831 | 1/39,569,962 ≈ 2.5272·10^-8 |

The verifier `verify_tricolored.py` checks all 2916² (row 1, row 2) pairs against the row-3 positions, the tag exclusions (each tag paired with any row-1/row-2 position or with another tag), injectivity, ranges and k ≥ 2L. It finds 0 violations for both files.

## Audit (2026-11-21): nothing in the proof needs i_a = j_a
I applied `patches/reserved-tags.patch` to the pinned manuscript and read every section that refers to positions.

* **§3, setup and Lemma norm:decomposition.** The f_{1a}, f_{2a} and f_{3a} are separate polynomials placed at (row 1, i_a), (row 2, j_a) and (row 3, ℓ_a). The pinned manuscript itself uses i_a = a, j_a = T·a. The only thing about positions that is used is the matching equation (norm:matching), injectivity in each row, and positions in [0, k).
* **§3, Lemma norm:obstruction.** Modulo r, the nonzero positions are row 1: {0} ∪ {i_a}, row 2: {t_s} ∪ {j_a}, and row 3: {ℓ_a}. γ_{k−1} survives exactly when the triples summing to k−1 are (i_a, j_a, ℓ_a). The three cases to exclude, (0, j_b, ℓ_c), (i_a, t_s, ℓ_c) and (0, t_s, ℓ_c), are all checked by the verifier, since 0 is a tag. The coefficient bound only needs positions < k.
* **§4, Lemmas orb:conditional and orb:tagged-moment.** These use row lengths L1 = L2 = r, the low coefficients below 10 (row 1 is 1 at 0 and r elsewhere, row 2 holds the tags and r elsewhere), the first differing tag a < 10, and the fresh row-3 position k−1−a ≥ 10. All of this holds because every norm position in rows 1 and 2 is ≥ 10, and the tags 0 < 1 < 2 < 3 < 4 are increasing. None of it compares i_a with j_a.
* **§5–§9.** These sections never refer to the positions. k enters only through the scales (L3 = 400k²r⁴, B, and ρ = 249k+3).
* **Lean.** `FiveTagged.tagged_small_residue_moment` assumes A and A′ agree up to a, A₀ = 1, Q and Q′ agree below a, and coefficient ranges. None of these involve i = j. `ReservedPacking` is standalone and imported by nothing else. A tricolored version of it would replace the midpoint lemma with a finite or structured check.

Verdict: the tricolored packing fits the argument as written, with only the definition of the positions in §3 changing. η = 1/30,650,782 is therefore the as-intended bound, and 2/61,297,829 (tag span 6, which changes the constant 10 in §4) is the gamed variant.
