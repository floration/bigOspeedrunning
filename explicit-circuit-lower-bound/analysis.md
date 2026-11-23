# Explicit circuit lower bound: difficulty and slack analysis

**Problem:** largest c such that an explicit (NP) function needs B2 circuits of size cn − o(n).
**Current best (Claimed):** 4n − O(log n), Mishra and Santhanam, ECCC TR26-260 rev. 1 (3 Nov 2026).
**Difficulty: Hard.** No easy improvement found.

## What the proof does
- Hard function: Li's explicit affine disperser for dimension d = O(log n) (in P).
- State: injective affine map Φ(u) = b + Lu from m parameters, a set of q disjoint "pairs" {p, r} with constraint p·r = 0, and a circuit of size s (gates plus affine equations). a = m − q.
- Potential W = s + 4q + 6·(number of used unpaired parameters).
- Each step (Lemma 4.2) keeps Δa ∈ {0, −1} and ΔW ≤ 10·Δa. Start: W ≤ |C| + 6n. If |C| < 4n − 10d, then a > d at the end, giving an affine subspace of dimension ≥ d where C is constant but f is not. So c = 10 − 6 = 4. The O(log n) term is just 10d.
- Five cases. Tight ones:
  - Case 4 (minimal AND G = (x+α)(y+β)+γ, x, y unpaired): add pair {x,y}, delete G and one child. ΔW = −2 + 4 − 12 = −10.
  - Case 1 (paired p with deg ≥ 2) and Case 3 (paired p in the affine system): ΔW = −2 − 4 + 6 = 0 with Δa = 0.
  - Case 5 (k = 2): ΔW = −10 (tight at these weights, but not a true bottleneck, see below).

## Reweighting analysis (my check)
With W = s + βq + αI, write g1 = gates removed in Cases 1/3 (now 2) and g4 = gates removed in tight Case 4 (now 2). The constraints are
- Case 1/3: α − β ≤ g1
- Case 4: D ≤ 2α − β + g4
- Case 5: D ≤ 2β + 2 and D ≤ α + β + 2

and c = D − α. Then c ≤ (α − β) + g4 ≤ g1 + g4 = 4, whatever Case 5 does. A grid search over (α, β) confirms the optimum is exactly g1 + g4: (2,2) → 4, (2.5,2) → 4.5, (3,2) → 5. That matches the authors' Remark 4.3 (α = 6, β = 4 optimal).

**What this means:**
- Reweighting the same potential cannot help. Case 5 slack is irrelevant.
- Any gain has to come from removing more gates (amortised) in exactly two places: the hard Case 4 configuration, or Case 1/Case 3.
- One full extra gate in either place gives 5n, which is the known limit of Golovnev–Hirsch–Knop–Kulikov for this kind of gate elimination. A realistic target is a fractional amortised gain (e.g. 4.5n from half a gate on average). That needs a new idea, not a local fix.

## Easy fixes I tried (none work)
- Fix x by an affine substitution (UF) instead of adding a pair in Case 4. It is better when deg(x) = 1 or deg(y) = 1 (ΔW ≤ −14 or −3 − 2α), so the hard subcase is deg(x), deg(y) ≥ 2 and G has one child. There UF gives only −3 − α, which caps c at 3. So no gain.
- Delete all children of G in Case 4 instead of one. This only helps when deg(G) ≥ 2. The tight case is deg(G) = 1, where its single child H can be a pass-through. So no gain in the worst case.
- Split weights by degree (like rev. 0's 6/7). Pairs of degree ≥ 2 are cleared by Case 1 at once, so the worst case still costs α − β − 2 ≤ 0. Same bound.
- Better disperser dimension d. This only changes the O(log n) term, not c.

## Leads if someone wants to push
1. Amortise Case 1 with the deletion that caused it. A paired parameter's degree grows only when a D1 pass-through reroutes children onto it. Charging that growth to the earlier step might recover part of a gate.
2. In hard Case 4 (deg x, deg y ≥ 2, G with one child H), look at H's other input and children. Rev. 0 looked one level deeper in a similar bottleneck.

Caveat: I read the case analysis via a verbatim-text extraction of the PDF. The gate counts above are as stated in the paper. I did not re-verify every case of their proof.

## Second attempt (Keep pushing, 20 Nov 2026)
Goal: get a fractional gain in one of the two binding constraints (Case 4 with α − β + 2, or Cases 1/3 with α − β ≤ 2).

**Hard Case 4** (deg x, deg y ≥ 2, G has one child H), all options at weights (α, β):
- Pair {x,y} (the paper's move): 2 gates, ΔW = −2 + β − 2α.
- Fix x ← α: G, H and x's other child K go, so 3 gates (4 if K turns constant). ΔW = −3 − α.
- Fix x ← α + 1: G becomes a pass-through, but K then turns constant. Also ≥ 3 gates.
- Other pair orientations, e.g. (x+α+1)(y+β) = 0, turn G into a literal of y. That is worse.

The fix-x branches cap c at 3. So Case 4 needs an extra gate under the pair move, and the adversary can make H a pass-through. No gain here.

**Case 1, banking deletion slack (partial lead):** A paired p reaches deg ≥ 2 only by rerouting after a pass-through deletion (ΔW = −1, while the proof only needs ≤ 0), or by a Case 4 pair whose inputs had deg ≥ 3. Add +1 to W for each paired parameter of deg ≥ 2. Rerouting deletions then cost 0, and Case 1 becomes −3 − β + α ≤ 0, which relaxes the constraint to α ≤ β + 3. (When deg(x) ≥ 3, Case 4 can switch to fixing x, with 4 gates.)

**Blocker: Case 3** (a paired p appears in the affine system). It arises from moving an XOR-type child of p into the affine system. That move has ΔW = 0, so there is no slack to bank. The alternatives (fix p = 1 and r = 0; reparametrise p) either cost a unit of a for 2 gates or break the rule that pairs sit on parameters. Case 3 still forces α ≤ β + 2, so c stays 4.

**Result: still no new bound.** The partial lead only pays off if Case 3 can be handled with an extra gate, or with banked slack from the move that creates it. That is a real research step, not a local fix.

## Five-idea round (21 Nov 2026)
The scripts are in `scripts/`. Each one is a weight-optimisation LP or grid search over my model of the case analysis, and each reproduces c = 4 for the paper's own model.

1. **Novel: degree-split weights, plus trying both constants for high-degree inputs.** Use weights w1 (deg 1) and w2 (deg ≥ 2), and a pair surcharge. I first assumed x's other children are AND-type, so one of x ← α or x ← α+1 forces a cascade (≥ 5 gates for deg ≥ 3). Under that assumption the LP gives **c = 5** (w1 = 8, w2 = 9, β = 6, D = 14; `novel2.py`). **But the assumption is false:** in the paper's model, x's other children can be XOR gates or equations in the affine system, which neither constant forces. With 4 gates in that case, the optimum falls back to exactly 4, even with four degree classes (`novel4.py`). **The new precise blocker:** hard Case 4 where x has degree 3 and its other two children are XOR. One extra gate there (amortised) would give 5 in this model, but the model is mine and unchecked.
2. **Crazy: a disperser for the pair varieties Z(P), not just affine subspaces.** A pair then costs only λ = 2 − log2 3 ≈ 0.415 of a dimension, or 0 in the limit. LP (`crazy.py`): c = 4 for every λ in [0, 1]. Cheaper pairs don't help at all. (Such explicit dispersers don't exist anyway.)
3. **Borrowed (LP duality from optimisation, and the Kojevnikov–Kulikov degree-1 penalty from earlier circuit work):** The `novel4.py` grid allows w1 > w2, which is the KK-style weighting. Max c = 4. The dual certificate is just Case 4 + Case 1/3: c ≤ (α − β + 2) + 0 with α − β ≤ 2.
4. **Reverse: assume every step is tight and rebuild the configuration.** The tight step is an input of degree 2–3 whose AND child G has a single pass-through child, and whose other children are XOR. That is easy to realise locally, so there is no local contradiction to exploit. Any gain would need a global counting argument.
5. **Breaking: drop the rule Δa ∈ {0, −1}.** Take two-dimension steps, e.g. fix x and also substitute the XOR partner w ← x + c to collapse K1. This gives about 6 gates for Δa = −2, so D ≤ 3 + w and c ≤ 3 on that case. Worse.

**Result: no new bound.** The best conditional lead is idea 1. Handle "degree-3 input with XOR children" with one more amortised gate, and the reweighted potential would reach 5n in my model. That would need a full re-proof and is not a result.

## Max gamified vs as intended (21 Nov 2026)
**As intended:** c = 4 (Mishra–Santhanam). I have nothing better.

**Max gamified.** These are loopholes in how the metric could be read. None of them is valid under the page's statement (single-output f_n: {0,1}^n → {0,1} in NP, full basis B2, size = gates).
| Gamed reading | Value | Why it is not valid |
|---|---|---|
| Change the basis to U2 / De Morgan (no XOR, no XNOR gates) | 5n − o(n) (Iwama–Lachish–Morizumi–Raz) | The page fixes B2 |
| Multi-output functions, e.g. n² distinct output bits | superlinear, trivially | The page fixes one output bit |
| Formula size instead of circuit size | ~n³ (Andreev / Håstad / Tal) | Not circuits |
| Tune the exact parameters (lower-order term) | 4n − 10d with d = Li's disperser dimension, so 4n − O(log n) | Only the lower-order term moves. The ranked value c stays 4, so it is at most a tie-break |
| Pad or re-index n | only lowers c | Not useful |

The proof has no parameter that moves the leading constant. α = 6 and β = 4 are already optimal, and the disperser dimension only touches the o(n) term.
