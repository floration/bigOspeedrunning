# A 6×5 final grid (30 edges) for the unit-distance obstruction

Draft, 2026-11-20. Conditional on the same imported lemmas as the current record
(Rohan Arun, 8×4 = 32): the source's generic-grid lemma, private-valuation lemma and
quadratic Kummer statement (OpenAI, *A power saving for planar unit distances*,
commit `fd4aeeb2`, section `07-algebra.tex`). It does not change the headline
exponent. AI-generated; not independently reviewed or formalised.

## Idea

The source and the 8×4 refinement both use subadditivity: adjoin all anchor
derivative data to the coefficient field (3j−5 generators after gauge fixing), then
need N > 3j−5 left points so one stays generic. That forces j = 4, N = 8.

Instead, never adjoin the derivative data. Look at the *linear system* the data
satisfies. Its coefficients involve only positions and radicals, so each new left
point is generic over the field of definition of the solution space so far. One
anchor more (j = 5) lets each new point cut the solution space by **two**
dimensions instead of one, which reaches the trivial floor after six points.

## Setup

Notation as in the source: for a grid edge (i, ℓ),

  (E_iℓ) 2(p_i − r_ℓ)·(H_i − U_ℓ) − R_iℓ (A_i − A'_ℓ) = 0,  A_i − A'_ℓ ≠ 0,

with R_iℓ² = D_iℓ = L_ℓ(p_i)(L_ℓ(p_i) − 4).

Fix anchors r_1, …, r_5 and left points p_1, …, p_N from the generic-grid lemma with
j = 5. For k ≤ N, let 𝒦_k ⊂ 𝒰^{15+3k} be the solution space of (E_iℓ), i ≤ k,
ℓ ≤ 5, in the unknowns (U_ℓ, A'_ℓ)_ℓ, (H_i, A_i)_{i≤k}. Let K_k be the algebraic
closure in 𝒰 of B_0(r_1..r_5, p_1..p_k). Then:

* The coefficients 2(p_i − r_ℓ), R_iℓ lie in K_k, so 𝒦_k has a basis in K_k.
* The actual derivative data X* (restricted) lies in 𝒦_k.
* 𝒦_k contains the 4-dimensional trivial space H_i = T + ωJp_i, U_ℓ = T + ωJr_ℓ,
  A_i = A'_ℓ = β. It is 4-dimensional because r_1 ≠ r_2. So dim 𝒦_k ≥ 4.
* 𝒦_0 = 𝒰^{15}.
* p_{k+1} is generic on V_1 over K_k, by joint genericity.

No gauge normalisation and no adjoining of derivative data is used.

## Step lemma

Let p = p_{k+1}, M = K_k(p), and L = M(R_1, …, R_5), where R_ℓ = R_{k+1,ℓ}. Assume
the rows p − r_1, p − r_2, p − r_3 have rank two. **Then either
dim 𝒦_{k+1} = dim 𝒦_k − 2, or A_{k+1} = A'_4 for the actual data**, which is
the contradiction.

*Proof.* Private valuations over K_k (the source's construction uses only joint
genericity of the anchors over B_0, so it applies over K_k) make D_1, …, D_5
independent mod squares in M. Kummer theory then gives every sign change of the
R_ℓ as an automorphism of L/M, and distinct single radicals are M-independent.

Take x ∈ 𝒦_k. Solve equations ℓ = 1, 2, 3 for (H, A) at p by Cramer's rule. The
determinant is a nonzero M-combination of R_1, R_2, R_3. The solution is unique and
linear in x. On a K_k-basis b_1, …, b_d of 𝒦_k its values lie in M(R_1,R_2,R_3).
The map x ↦ (x, H(x), A(x)) identifies 𝒦_{k+1} with {x ∈ 𝒦_k : c_4(x) = c_5(x) = 0},
where c_ℓ(x) is the residual of equation ℓ. On the basis,

  c_4(b_m) = α_m − R_4 β_m,  α_m = 2(p − r_4)·(H − U_4)(b_m),  β_m = (A − A'_4)(b_m),

with α_m, β_m ∈ M(R_1,R_2,R_3). Likewise c_5(b_m) = γ_m − R_5 δ_m, with
δ = A − A'_5 and entries in M(R_1,R_2,R_3).

So dim 𝒦_{k+1} = d − rank_L(c_4; c_5). Suppose the rank is at most 1.

* If the vector c_4 is 0, then β = 0, because R_4 ∉ M(R_1,R_2,R_3). So A ≡ A'_4 on
  𝒦_k, and in particular A_{k+1} = A'_4 for X*. That is the contradiction. In the
  same way, c_5 = 0 gives A_{k+1} = A'_5.
* Otherwise c_5 = μ c_4 with μ ∈ L^×. The flip σ_4 (R_4 ↦ −R_4, fixing
  R_1, R_2, R_3, R_5) fixes c_5, so σ_4(c_4) = α + R_4 β is also proportional to
  c_5, hence to c_4 = α − R_4 β. So α and β span at most a line. If β = 0 we have the
  contradiction. Otherwise α = κβ with κ ∈ M(R_1,R_2,R_3), and κ ≠ R_4. Then
  c_4 = (κ − R_4)β with a nonzero scalar, so 𝒦_{k+1} ≅ ker c_4 = ker β. For X* this
  gives A_{k+1} = A'_4, the contradiction. ∎

## Theorem (6×5 suffices)

Conditional on the source lemmas, the final algebraic contradiction runs on a
**6-by-5 grid, i.e. 30 selected edges** (the transpose 5×6 also works with a step
lemma for six anchors, not needed here).

*Proof.* Suppose first that V_1 and V_2 are not the same line. Then the rank-two
condition holds for every step; this is the source's argument, using
noncollinearity of generic anchors, or p ∉ the anchor line. If no step gives the
contradiction, each of the 6 steps drops the dimension by exactly 2. Then
dim 𝒦_6 = 15 − 12 = 3 < 4, which is impossible.

If V_1 = V_2 is a single line, use the existing common-line argument on a 4×3
sub-grid (12 edges, from the 8×4 note). The 6×5 grid contains it. ∎

## Sharpness for this differential system

The same linear system on a generic **5×5** (25 edges), **7×4** or **4×7** (28
edges) plane–plane grid has a 5-dimensional kernel. Its extra direction has
A_i ≠ A'_ℓ on every edge, so no argument using only (E_iℓ) and A_i ≠ A'_ℓ can
conclude on those grids. A counting check (Nj ≥ 3(N+j) − 4) shows 30 is the
least complete grid for which the system can be rigid. Going lower needs extra
input, such as derivatives of the locus equations. Using several derivations only
recovers the known "trdeg ≤ 1 over k_0" obstruction.

## Checks

`python3 check_grid.py` runs these numerical sanity checks in floating point. They
are not a proof.

* The step lemma holds on 160 random configurations over 8 locus pairs (plane,
  parabola, two lines, concentric and equal non-unit circles).
* The contradiction is forced for 6×5, 5×6, 8×4 and 4×8.
* The contradiction is not forced for 5×5, 7×4 and 4×7.
