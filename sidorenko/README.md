# Sidorenko nondirect residual constant: 189 -> 43

Builds on rohanarun/sidorenko-template-refinements (commit 5ca68cb), `proof.tex`,
Prop. "residual-189". Everything upstream of its remainder formula is unchanged
(same graph, cuts, 28 allowed pairs, same type-sequence count, same order u_1,w_1,u_2,w_2,...).

## The slack
The 189 proof bounds pi(x) = dim(V'_i ∩ V'_j) by (v'_i + v'_j)/2. That is very loose:
V'_i and V'_j are spanned by *different* earlier vectors (they share only pair {i,j}),
so their intersection can only come from earlier linear dependencies, which the type
sequence already records.

## Rank lemma
Let S_i be the earlier vectors at pairs containing i. Processing S_i in order,
rank S_i = #{y in S_i : l_i(y)=1} exactly, and rank(S_i ∪ S_j) >= #{y : g(y)=1}
since a g=1 vector is independent of everything earlier. So

    pi(x) = rank S_i + rank S_j - rank(S_i ∪ S_j)
          <= sum_{y earlier, e(y) meets e(x)} ([i∈e(y)] l_i(y) + [j∈e(y)] l_j(y) - g(y)).

Per earlier y the summand is: (1,1,1) -> 1 only for y = u_t when x = w_t, else 0;
(0,0,0) -> 0; (0,0,1) new at b -> 1 for x at pairs through b, else 0;
(0,1,1) -> 1 for x at pairs through a or b, 2 within its own pair.
(Randomized sanity check over GF(3): `rank_bound_check.py`.)

## New remainder
Summing over the non-defect x (and keeping the paper's terms for defect vectors):

    R <= -m + Σ_{(0,0,1) at (a,b), new at b} [(2δ_b - 1) + k_a + k_b - 1]
            + Σ_{(0,1,1) at (a,b)} [2(δ_a+δ_b) - 2 + k + k_a + k_b - 2],

with k_i <= min(k, 2δ_i), k <= 2m - n1 - n2. Taking the min with the published bound
and maximising R/d over every m <= 28, n1, n2, k (`audit_rank_refinement.py`, exact rationals):

* d = 1: R <= 27 (was 189).
* all d (v1): R/d <= 44.7, attained in the relaxation at m=28, five (0,1,1) vectors, k=51.

So -Dd + R <= -D + 45 for every d >= 1 once D >= 45: the contribution is
O_D(q^{-D+45}), and this step needs only even D >= 46 (was 190).

## Final push (v2, v3): 45 -> 43
Three further exact savings, all from the same type-sequence data:
1. **Per-pair base.** The (1,1,1) u_t -> w_t weights total at most m minus the number of
   pairs carrying a defect vector (such a pair has u_t defective or w_t excluded), and a
   (0,1,1) u_t has weight 2 on its own w_t, (0,0,1) weight 1. Two defects in one pair share
   the -1 and lose the own-pair weight. `audit_rank_refinement_v2.py` does an exact DP over
   all 28 pairs: d=1 gives R <= 26, all d give R/d <= 43.625.
2. **Defect-defect exclusion.** The pi-sum runs only over non-defect x, so two (0,1,1)
   vectors at distinct pairs sharing a vertex save 1 whatever their order.
3. **Distinct local dimensions.** All (0,1,1) vectors at a vertex a have l_a = 1, so their
   v'_a are distinct values in {0..k_a-1}; c of them lose at least c(c-1)/2 from the caps.

`audit_rank_refinement_v3.py` adds 2 and 3. It reduces to n1 = 0, k = 2m - n2, m = 28
(each (0,0,1) vector adds <= 33 per defect unit and lowers k; B and A increase in m),
and to the 15 pairs with d_a+d_b >= 10 (a (0,1,1) at any other pair adds <= 86 = 2*43 to
both A and B). It enumerates all 3^15 multiplicities exactly: **max R/d = 42.75**
(two (0,1,1) vectors at each of {1,9} and {3,11}, k = 52, R <= 342).

Hence R_d <= 43 d for every d >= 1, so -Dd + R_d <= -D + 43 once D >= 43:
the contribution is **O_D(q^{-D+43})**, and even D >= 44 suffices for this step.

## Caveats
* Inherits the "Claimed" status of the 189 argument: no Lean proof, upstream sequential
  framework not independently reviewed by us beyond re-deriving its remainder identity.
* Only this one counting step; other dimension thresholds of the construction unchanged.
* Bottleneck now is the (0,1,1) w' <= k term; tightening it is the next lever.
