# Referee report: Yianni & Allahyar, "The first lower bound improvement on the unrestricted circuit complexity of 3-SAT" (17/7)

Source: https://github.com/sahibzada-allahyar/math/blob/main/preprint/3SAT_Circuit_Lower_Bound.pdf (19 pp.). Page numbers are the printed ones.

## 0. Verdict in one paragraph

I found no fatal error. The lower bound C_B2(F_w) >= (17/7)n - O(n loglog n / log n) holds for the paper's own encoding, as far as a careful read can tell. The gate-elimination case analysis (Lemma 7.1) closes, and I checked every case. The transfer through the restriction is honest. The 17/7 comes out exactly from the stated case gains, and it is LP-optimal for that case structure: re-weighting gives nothing more. The result is narrow, though:

- It is a constant-factor bound for one particular binary encoding.
- Its hard function is an AND/OR read-once composition of short (about log n-bit) strongly two-dependent full-degree blocks.
- The technique is the Kojevnikov–Kulikov "gate elimination plus multiplicative complexity" method with one more credit level. The sequence 7/3, 12/5, 17/7 = 3 - (j+1)/(2j+1) tends to 5/2.
- The embedding cannot carry affine dispersers or other known >3n hard functions. The sections below explain why.
- The marketing ("A step towards P != NP", credentials of quoted researchers, priority claims) is editorial fluff and should be cut.

## 1. Exact statements

**Encoding (Sec. 2, p.3–4).**
- Fix w >= 5. There are m = 2^w - 1 variables and exactly m clauses.
- Each literal field has w identifier bits b_0..b_{w-1} (v = sum 2^j b_j) plus a sign bit s. v = 0 is invalid. s = 0 means X_v and s = 1 means ¬X_v.
- Each clause is 3 fields, so n = 3m(w+1).
- F_w = 0 if any identifier is 0. Otherwise F_w = 1 iff the 3-CNF is satisfiable.
- Model: B2 (all 2-input gates). Size counts all gates.

**Main theorem (Thm 8.2, p.15).**
- C_B2(F_w) >= (17/7)n - O(n loglog n / log n).
- Finite form: for 4 <= r <= w-1, 3 <= k <= r-2 and 2^{k-2} > log2(6r(r-1)) + r log2 3,
  C_B2(F_w) >= n + ceil(((30r - 42(k+1))(m - 2^r) - 3)/7).
- Explicit version with the modular blocks: (17/7)n - O(n/sqrt(log n)).

**Embedding (Lemma 3.1, p.4–5).**
- Take any g: {0,1}^r -> {0,1} with r <= w-1, and call identifier 2^{w-1}+a forbidden iff g(a) = 0.
- Each forbidden identifier gets one helper clause (¬X_v ∨ ¬X_v ∨ ¬X_v), fully fixed.
- The other M = m - |g^{-1}(0)| clauses are positive. In each of their fields:
  - the top bit is set to 1,
  - bits r..w-2 are set to 0,
  - the low r bits are free,
  - the sign is 0.
- The restricted function is G = AND_{c=1}^{M} (g(x_{c,1}) ∨ g(x_{c,2}) ∨ g(x_{c,3})) on L = 3Mr free bits.

**Transfer (Lemma 4.6).** C(F_w) >= (n - L) + C(G). This uses Lemma 3.2 (every bit of F_w is essential) and Lemma 4.5 (fixing t essential inputs of a normalized circuit removes at least t gates).

**Hard blocks (Sec. 5).**
- Definition 5.7, k-robust: every restriction leaving at least k free inputs satisfies (S4), i.e. the four cofactors on every pair are pairwise distinct. This is Lachish–Raz strong two-dependence.
- Lemma 5.8: an AND/OR composition of restricted k-robust blocks has (E1), (E2) and (S4) whenever every leaf keeps at least k+2 bits.
- Proposition 5.9 (counting): a k-robust block of full degree r exists if 2^{k-2} > log2(6r(r-1)) + r log2 3. Then k = log r + O(1).
- Proposition 5.10 (explicit): g_{r,t} = [sum_i i·a_i ≡ t mod p], with p the least prime > 2r and k = m_p + 2 <= ceil(sqrt(8r)) + 2.
- Lemma 5.4 (Schnorr): #nonlinear gates >= deg_F2 - 1.
- Proposition 5.5: the degree of a read-once AND/OR composition is the sum of the block degrees. So A >= L - 1.

**Potential (Def. 6.9).** Ψ2 = 7X + 4A - D - D*, where:
- X = number of parity gates, A = number of nonlinear (AND-type) gates;
- D = inputs whose only successor is one nonlinear gate W_z;
- D* = those z in D with succ(W_z) = {W_z^2} and W_z^2 nonlinear.

**Lemmas used in the inductive step.**
- Lemma 4.4 (normalization): removes degenerate gates and input triangles.
- Lemma 6.4 (resolution preserves gate types).
- Lemma 6.5 (passing sets S_N).
- Lemma 6.7 (no D-gate has two primary operands under (E1); a successor of a two-input gate T is not a D-gate under (E2)).
- Lemma 6.10 (role exclusions).
- Lemma 6.11 (charging):
  - Ψ2(C) - Ψ2(C^ρ) = Σ_elim (w2 - χ2) + Γ, with χ2 <= 2;
  - χ2 <= 1, and charged gates are never constant, when no D-variable is fixed.
- Lemma 6.12 (normalization does not raise Ψ2).
- Lemma 7.1 (one step): some input x with d(x) >= 2 and some value c give a drop in Ψ2 of at least 14.
- Thm 8.1:
  - Ψ2(C) >= 14(L - (k+1)B);
  - 7|C| = Ψ2 + 3A + D + D* >= 14(L - (k+1)B) + 3(L - 1), so |C| >= (17L - 14(k+1)B - 3)/7.

## 2. Does it hold up?

### (a) Reduction / accounting — FINE

- **Lemma 3.1 is correct.**
  - Helper clauses force the forbidden variables false.
  - Positive clauses only mention identifiers in [2^{w-1}, 2^{w-1} + 2^r - 1], which is inside [1, m], so all are valid.
  - Setting every non-forbidden variable true satisfies the formula iff each positive clause names a non-forbidden identifier.
  - Record count: |g^{-1}(0)| + M = m. Fixed bits: n - 3Mr.
- **Lemma 3.2 (essentiality) is correct.** Flipping bit j of identifier m gives m - 2^j >= 2^{w-1} - 1 >= 1.
- **Lemma 4.5 is the standard counting and is correct.**
  - Let d >= t be the out-wires of the fixed inputs. Then e <= 2h and e + b >= d + h, so h + b >= d.
  - The b receiving gates are distinct and degenerate.
- **"Restriction accounting also credits the fixed bits"** means exactly: each fixed bit pays for at least one gate.
  - This is legitimate. It is the trivial n - 1-type count applied to the n - L fixed bits, added to C(G).
  - Nothing is credited at the 17/7 rate except the L free bits. The bound is (n - L) + (17/7)L - lower order = (17/7)n - (10/7)(n - L) - ...
  - Since n - L = Θ(n log w / w) = o(n), the leading constant is legitimately 17/7 with respect to the full n.
  - I found no illegitimate crediting.

### (b) Gate-elimination case analysis (Lemma 7.1, pp.12–14) — FINE, with minor presentation gaps

**Common facts.** I re-derived every case. The facts used throughout are:
- x and y have fan-out >= 2, so no D-variable is fixed. Every eliminated nonlinear gate then has χ <= 1 and contributes at least 3. A constant one, or one that plays no role, contributes 4. Parity gates contribute 7.
- Successors of a fan-out->=2 input play no role (Lemma 6.10(a)).
- Successors of T play no role (Lemma 6.10(b), using (E2)).
- There are no input triangles.

**Gains by case.**

| Case | Gain |
|---|---|
| Parity T, all x-successors parity | 7+7 = 14 |
| Parity T, nonlinear successor P blocked | 7 + 4 + (>= 3) = 14 |
| Nonlinear T, d(v) >= 3 | 4·4 = 16 |
| U (or V) parity | 4+7+4 = 15 |
| x blocks T and U together | 4+4+4+3 = 15 |
| T has >= 2 successors | 16 |
| T's unique successor R is parity | 15 |
| R is blocked by c_T | 4+4+4+3 = 15 |
| R unblocked: x-step removes T, U, R | 12 base |
| U = V | impossible: (T, U) takes only 3 values, contradicting (S4) |
| V good, two successors | 4+4+3+3 = 14 |
| V good, parity successor | 4+4+7 = 15 |
| V good, nonlinear blocked successor | 4+4+4+3 = 15 |
| Both bad, V2 ∉ {R, U} | 12 + gain of y as D and D* = 14, or 12 + 3 = 15 if another gate dies |
| Both bad, V2 = U | 4+4+4+3 = 15 |
| Both bad, V2 = R, U2 ∉ {R, V} | symmetric, 14 |
| Both bad, V2 = R, U2 = V | impossible (verified): under x = ¬ε, R is blocked for both values of y, so y is disconnected, contradicting (E1) |
| Both bad, U2 = R | V2 ≠ R by in-degree 2, so it reduces to the cases above |

The "critical step", the both-bad case, is sound:
- With T, U, R eliminated and nothing else, Lemma 6.5(c) gives S_y = {y} and S_V = {V}.
- So in C^ρ, y has the unique nonlinear successor V, and V has the unique nonlinear successor V2.
- Hence Γ >= 2. T, U and R play no roles, so no loss is charged.
- This is a legitimate potential argument. The credit y gains is paid back later through χ when V or V2 is eliminated, and Lemma 6.11 accounts for that.

**Gaps (presentational, not fatal).**
- **G1 (Lemma 7.1, "V2 ∉ {T,U,R} ... by assumption").** The case split leaves implicit that V2 can equal U2, or be a successor of U. Neither matters, because any further elimination gives at least 15.
- **G2 (Lemma 6.12).** It applies Lemma 6.11 to a circuit containing a degenerate gate ψ, after the triangle replacement. Lemmas 6.7 and 6.10 still go through, because only nonlinear-gate blocking is used, but the paper does not say so.
- **G3 (Lemma 4.4) termination.** The claim that "the sum of predecessor indices strictly decreases" is sketchy but standard.
- **G4 (Def. 5.7).** "Testing restrictions down to exactly k inputs suffices" needs a one-line justification. It is true: equal cofactors stay equal under any further common restriction.

**Small typo-level issue.** In Thm 8.1, the paper uses D <= 2A where Lemma 6.7(a) gives D <= A under (E1). Either works.

### (c) The 17/7 arithmetic — FINE, and the case structure is LP-tight

Generalise the weights: parity a, nonlinear b, credits c1 = c2 = c. The worst-case step gain is then

s = min(2a, a + 2b - c, 4b - 2c, 3b + min(b - c, 2c), 4b - c, a + 2b, 4b).

The size bound is |C| >= ((s + a - b)/a)·L. This needs b <= a, and b >= 2c so that Ψ >= 0 at the end. Normalise a = 1 and maximise s + 1 - b:
- Setting s = 2 forces 2b - c >= 1 and 3b + 2c >= 2.
- This gives c >= 1/7 and b >= 4/7, so the value is 2 + 1 - 4/7 = 17/7.
- Lowering s by δ allows b = (4 - 2δ)/7 at best, for a value of 17/7 - 5δ/7.
- With c1 ≠ c2, the charge is max(c1, c2) but the gain is c1 + c2, so equal credits are optimal.

The paper's choice (7, 4, 1, 1) has four simultaneously tight cases at 14:
- all-parity x;
- parity T with nonlinear P;
- V good with two successors;
- both bad.

**So 17/7 is the exact optimum of this case analysis.** Any improvement must refine one of those four cases. The 7/3 and 12/5 companions fit the same family, 3 - (j+1)/(2j+1). The limit 5/2 would need infinitely many credit levels, and is the natural ceiling of the method.

### (d) Strong two-dependence across restrictions — FINE

- Robustness is only used blockwise.
- Lemma 7.1 needs (E2) and (S4) only for the current function. Lemma 5.8 supplies them while every block has at least k+2 free bits.
- A block reaching k+1 bits is killed: it is set to the neutral value of its parent. The potential does not increase then (χ <= 2 < 4). The cost is (k+1) per block.
- So the number of restrictions is irrelevant. Each block loses at most r - k - 1 bits individually, and robustness is a property of each block's restrictions.

Propositions 5.9 and 5.10 are both correct:
- Union bound: 3^r · C(r,2) · 6 · 2^{-2^{k-2}} < 1/2.
- Balandraud's theorem is applied correctly: H ⊂ [1, r] ⊂ (0, p/2), so H ∩ -H = ∅.
- The Φ_p non-divisibility argument for odd N_t is correct.

### (e) Schnorr / degree part — FINE

- Lemma 5.4 is the standard multiplicative-complexity >= degree - 1 bound, and its proof is correct.
- Proposition 5.5 is correct: the top-degree part of f ∨ g = f + g + fg is top(f)·top(g) on disjoint variables.
- G has degree L, so A >= L - 1.

## 3. Quick fixes / free improvements

**1. Constant.** None free. 17/7 is LP-optimal for the stated cases (§2c). To move it, one must split one of the four tight cases:
- all-parity successors of x;
- parity T plus nonlinear P with a charged successor;
- V good with two charged successors;
- both bad.

Adding a third credit level (D**, a chain of three) would plausibly give the next term, 22/9 ≈ 2.444, following the authors' own pattern. That is not free; it requires a new case analysis.

**2. A >= L.** Raising the multiplicative-complexity lower bound to αL would give (14 + 3α)/7, for example 20/7 at α = 2. But no explicit function is known to have multiplicative complexity >= (1+ε)n. Not free.

**3. Lower-order term.**
- The loss is (10/7)(n - L) + 2(k+1)B, with B = 3M = Θ(n/w) and k = log r + O(1). So it is Θ(n log w / w) = Θ(n loglog n / log n).
- One could take r = w - 1 with a robust g whose zero set has density about 1/r. That brings n - L down to O(n/w).
- But the 2(k+1)B term still dominates. So the order of the lower-order term does not change; only its constant improves.
- The term k ≈ log r is intrinsic to blocks of length at most w (per field).
- The explicit version is O(n/sqrt(log n)), as printed on p.16. The text extraction garbles it.

**4. Transferring stronger known bounds (key question). Answer: no.**
- **What the embedding realises.** Lemma 3.1 realises exactly G = AND_{c<=M} OR_{j<=3} g(x_{c,j}): one global test g on disjoint r-bit blocks with r <= w-1, read once, as a monotone depth-2 AND-of-3-ORs.
- **Region trick.** Using different fixed high bits per field could give a different test g_p per prefix region. That widens the class to AND_c OR_j g_{p(c,j)}(x_{c,j}), and the shape is still the same.
- **Why affine dispersers fail.** Every such G is constantly 0 on a subcube of codimension 3r = O(log n): fix one clause's three blocks to forbidden values. An affine disperser for dimension d must be nonconstant on every affine subspace of dimension >= d. Known B2 bounds (DK 3n, FGHK 3.01n, Li–Yang 3.1n, Mishra–Santhanam) need d = o(n). Here d >= L - 3r would be required, which makes those bounds vacuous.
- **The same holds for F_w itself.** Two fully fixed records (X_a∨X_a∨X_a) and (¬X_a∨¬X_a∨¬X_a) make F_w ≡ 0 on a subcube of codimension 6(w+1).
- **Satisfiability needs mixed signs.** If every clause has a positive literal, the all-true assignment satisfies it. So unsatisfiability needs an all-negative clause, which the embedding supplies by fixing it.
- **Other known hard functions do not fit either.** Blum's 3n, Stockmeyer/Paul's 2.5n and MOD-function bounds are not of this AND-of-3-ORs read-once form.
- **What the transfer lemma does give.** Lemma 4.6 itself is fully general: C(F_w) >= n - L + C(G) for any realisable G. The obstacle is the realisable class, not the transfer.
- **Discrepancy.** The paper cites Mishra–Santhanam ECCC TR26-260 as 3.5n - o(n). The request said 4n - O(log n). I did not verify which is right. Either way, the bound does not transfer.

**5. Possible cheap win in a different model (speculative).**
- Lachish–Raz (4.5n) and Iwama–Morizumi (5n - o(n)) are U2 (De Morgan basis) arguments.
- Their only per-step requirement is strong two-dependence of the current function, plus the adversary choosing the variable.
- That is exactly what the block-killing invariant here maintains, at a cost of (k+1) per block, i.e. o(n).
- So C_U2(F_w) >= 5n - o(n) for this encoding may follow almost verbatim. It needs checking that Iwama–Morizumi never fix more than about 2 variables per step and never need global (S4) on fewer than k+2 bits per block.
- This is not a B2 result.

## 4. Numbers summary

| Quantity | Value |
|---|---|
| Weights | parity 7, nonlinear 4, D credit 1, D* credit 1 |
| Per-step drop | >= 14 |
| Per-case gains | 14 (all-parity), 14 (parity T + P), 16 (d >= 3), 15 (U parity), 15 (same block), 16/15/15 (T fan-out/R cases), 14 (V good), 14 (both bad, via credits), 15 (V2 = U) |
| Potential bound | Ψ2 >= 14(L - (k+1)B) |
| Gate count | 7|C| = Ψ2 + 3A + D + D* with A >= L - 1, so |C| >= (17L - 14(k+1)B - 3)/7 |
| Transfer | C(F_w) >= n + ceil(((30r - 42(k+1))M - 3)/7), with M >= m - 2^r, B = 3M, L = 3Mr |
| Parameters | r = w - ceil(log w) - 1; k = log r + O(1) (counting) or O(sqrt r) (explicit) |
| Final | (17/7)n - O(n loglog n / log n); explicit (17/7)n - O(n/sqrt(log n)) |
| LP optimum for this case structure | exactly 17/7, at (a, b, c) = (1, 4/7, 1/7) |
| No justified improvement in B2 | likely next stage with a third credit level: 22/9 (unproven) |

## 5. Editorial

- The title's "A step towards P ≠ NP" overstates the result. The novelty is the encoding-preserving embedding.
- Pages 1–2 spend a paragraph on the credentials of Arora, Barak, Fortnow and Goldreich. Remove it.
- The priority claim rests on companion manuscripts that have not been reviewed [25].
- The technique should credit Kojevnikov–Kulikov (CiE 2010, 7n/3 via multiplicative complexity) more explicitly as the direct template.
