# ℤ is Diophantine in ℚ: findings (2026-11-20)

**Leaderboard:** 257 variables (Jose Brox, Nov 16), degree 4, 3,679 terms, height 149^19366.

## Result: the leaderboard is stale. An explicit 179-variable quartic is already public.
- Commit 4bdace6758a342daa98d6d4baf722758e33bf8ff (2026-11-19 4:38 PM PT), JoseBrox/diophantine-z-q_improvements
  - Paper: papers/quartic/scalar_point163_179_20261120_v82.tex
  - Table: computation/variable_reductions_v82/general/quartic179/polynomial.json (+ quadrics.json)
  - https://github.com/JoseBrox/diophantine-z-q_improvements/commit/4bdace6758a342daa98d6d4baf722758e33bf8ff
- 179 variables (input is x1), degree exactly 4, 3,036 nonzero terms, max |coeff| = A_a^2 (748 bits).
  A_a = A0·B^4, A0 = 645904574641049503754777843805872291231896003979, B = 14904184670611231.
- Premises: the same kind as the 257 entry (pole realization, simultaneous-prime and height interfaces retained and not proved by computation). No added abc assumption. Status would be "Claimed".
- Better on every tiebreak than 257: fewer variables, fewer terms, far smaller coefficients.

### Independent check (my own script, check_sos.py, not the authors' code)
- polynomial.json is exactly the sum of squares of its 151 quadratic residuals: True.
- Degree 4, all 179 variables used, 3,036 terms, max coefficient 748 bits.
- Soundness (defines ℤ exactly) rests on the paper's proof plus retained premises. I did not verify that math.

### Intermediate explicit entries also missing from the board
- 229 variables, explicit at N=15: commit 9a7673e (Nov 17), compact form 7ab8458. Adopted as Version 21 in elliotglazer/diophantine-z-q (Nov 19).
- 180 variables (Conant notes with Astra 6.2, v78, Nov 19), superseded by 179.

### Not eligible under site rules
- 163 variables: coefficients involve BB(t1), t1 < 2^826. Busy Beaver values do not count.
- 56 variables / 11 variables: need abc and ineffective thresholds.
- 25/27-variable entries: degree far above 4, so they rank below every quartic.

## Difficulty of beating 179 myself: hard
- Scan of the 179 system: no variable appears only linearly (no free substitutions), and the 9 variables used in a single residual are square witnesses (y² = a·b), which cannot be dropped.
- Further gains need new arithmetic ideas (the authors list eliminating the R² register as open, and a parity obstruction blocks one compression).
- The research group is posting reductions daily, so any hand-found trick is likely overtaken quickly.

## Push below 179 (2026-11-20, second pass): no new bound
Mechanical searches over the 179 system, each a sound reduction if it had found anything:
- **Linear-only directions** (kern.py): directions d with A_i·d = 0 for every residual's quadratic part, d_1 = 0. These would let a coordinate be solved out or dropped. Result: none (nullity 0), with or without the linear parts.
- **Scaling symmetries** (weights.py): weights making every residual weighted-homogeneous with the input fixed. These would let a nonzero coordinate such as c = x162 be normalised to 1, saving it and its inverses. Result: the weight space is 0.
- **Trivial substitutions** (scan.py): no variable appears only linearly, and the 9 single-use variables are square witnesses y² = a·b.

Structure: 179 = the 163 family + a third native-pole detector (detector2, about 15 coordinates) + R⁻¹ (x91). These are added only so the defining threshold is effective (no Busy Beaver). So the real lever is effectivity, not algebra:
- An effective constant in the weighted trace-height theorem would make the 163 family's threshold explicit. That gives about 163 with a numeric (non-BB) parameter, or 178 if you keep detector2.
- The authors themselves flag that 178 is blocked only by this ineffective constant.
- Removing the R² register (x89) is listed by the authors as open.

These are research problems, not easy fixes.

## Attempt at an explicit 163 (2026-11-21): blocked by an open problem
- **Where the threshold fails to be effective:** the uniform weighted height inequality B_0² ≤ A(h(R)+h(T)) + J. It comes from von Buhren's semi-effective Mordell–Lang bound (JTNB 29 (2017), Thm 1.1). Its additive constant J is ineffective (docs/explicit_BB_threshold_20261120_v85.md).
- **Everything else is already explicit:** their v85 lemma shows that any proved numeral M bounding A, K_0, C_1, C_4, D_Δ, D_X gives the defining parameter N = max(3, M) with no Busy Beaver.
- **Why they use Busy Beaver:** von Buhren's quantitative theorem bounds how many exceptional "records" there are, but not their heights. v86/v87 hardwire the unknown last record into a Turing machine, which gives BB(t1) with t1 < 2^826. The paper also proves that no computable cutoff follows from that count alone.
- **What an explicit numeral needs:** an effective height bound for the relevant points on that subvariety. That is effective Mordell–Lang for this case, a famous open problem.
- **The 179 route:** Brox gets an explicit polynomial by avoiding the weighted theorem, using an effective unweighted estimate. That costs the third detector plus R⁻¹ (16 variables).
- **Site rules:** they exclude Busy-Beaver-fixed coefficients, so 163 cannot be submitted as it stands.

Conclusion: no explicit 163 is reachable without a breakthrough. The submittable bound stays at 179.

## Five-idea round (2026-11-21): no new bound
1. **Novel (solve out a guarded variable):** look for a variable that, after linear recombination of residuals, appears in a single residual only as v·ℓ with no v² term. With ℓ guarded nonzero, v could be solved out and dropped. Exact search (ideas.py): 0 candidates.
2. **Crazy (normalise c to 1):** c = x162 looks like a gauge, and fixing it would save x162, x163 and x164. But scalar.forced_prime says c² = −x78(A + 25R). So c is a square-root witness, not a gauge, and the weight-symmetry search already showed there is no scaling to exploit. Dead.
3. **Borrowed (compiler register coalescing):** merge registers that have identical definitions. Exact search: no duplicate definitions. The three detectors share x89, x158 and x164 already.
4. **Reverse (start from the overhead):** diffing 179 against 163 shows the whole 16-variable gap is detector2 plus R⁻¹. Both exist only to dodge von Buhren's ineffective constant, so no algebraic trick recovers them.
5. **Breaking (break SOS of quadrics / degree 4):**
   - The R² register x89 appears as σ in the detector conics. Rescaling to σ = R pushes those rows to degree 3–4, so the squared polynomial exceeds degree 4.
   - Dropping the degree-4 constraint does give fewer variables (Brox has 25 at enormous degree), but the site ranks degree first, so it loses.

## Max-gamified vs as-intended (2026-11-21)
Site ranking: degree, then variables, then nonzero terms, then largest |coefficient|.

| Version | Vars | Degree | Terms | Height | What it is |
|---|--:|--:|--:|--:|---|
| As intended | 179 | 4 | 3,036 | 748 bits | Brox's v82 fixed member, unchanged |
| Max gamified | 179 | 4 | **2,841** | 903 bits | the same construction, re-encoded to win the term tiebreak |

How the gamed version is made. Each step preserves the rational zero set exactly.
1. **Residual sparsification:** replace f_i by f_i − t·f_j when that shrinks f_i's support. These are invertible row operations, so the common zero set is unchanged. Support goes from 920 to 848.
2. **Positive weights:** P = κ·Σ w_i f_i² with w_i > 0, chosen so that more cross monomials cancel.
3. **Rescale existential variables:** x_j → p^{±1}·x_j, with x1 never scaled, to bring the height back down (964 → 903 bits).

verify_gamed.py checks all of this exactly over ℚ:
- the new residuals span the same space as Brox's 151;
- the weights are positive and the scalings are nonzero, with x1 untouched;
- P is exactly κ·Σ w f(s·x)²;
- the result is integer, content 1, degree 4, with all 179 variables used.

Honest framing: this adds no mathematics. It would outrank Brox's own 179 only through the term-count tiebreak. Credit must stay with Brox, Conant and the project. Files: gamed179.json and gamed179_expanded.txt.

## Reproduce
`python3 verify_gamed.py <dir with Brox's quadrics.json> gamed179.json`. The first argument is `computation/variable_reductions_v82/general/quartic179/` from JoseBrox/diophantine-z-q_improvements @ 4bdace6.
