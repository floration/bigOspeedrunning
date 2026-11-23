# Bounded prime gaps (H₁)

Board: https://bigospeedrun.com/other/prime-gaps. **No new bound here.** This folder has a review of the
180 preprint, an exact tuple search, and a sieve-weight model that points at two routes to 176.

## The 180 preprint (Allahyar–Yianni, 22 Nov 2026)

Source: `sahibzada-allahyar/math`, `preprint/prime-gaps-180/prime_gaps_at_most_180.pdf` (Zenodo 10.5281/zenodo.24430219).
It makes the same conditional assumptions as the 182 entry (A4 is Proposition 3.1 of the 182 companion paper, which isn't an
established theorem), plus 14 numerical statements.

- **Idea:** it keeps the 39-tuple of diameter 182 but proves Σ 1_P(n+h_i) − 1 − B(n) > 0, where B(n) = 1 if n and n+182 are both prime.
  The only pair farther apart than 180 is {0, 182}, so positivity gives two primes at distance ≤ 180.
- **Numbers (Table 1):** N(F) ≥ 1.0011666 M (net of the endpoint term), restriction loss R ≤ 0.001121271547 M, debit Ξ(G) ≤ 0.0000443013 M,
  so the margin is 1.027153 × 10⁻⁶ M. The endpoint cost is p/m = 151252/98747690 ≈ 0.00153 M. Before paying for it, the prime count is about 1.0027 M.

### Free points? None that change the integer.
- **Tuple:** 180 is optimal for excluding one pair. An exhaustive search finds no admissible 39-tuple, of any diameter, in which only one pair is
  more than 178 apart (`one_pair_exclusion_exact.c 39 D 178` finds none for D = 180..200, and D > 2·178 − H(37) = 188 is impossible anyway).
- **Constants:** the debit split (α−β)² ≤ (27/20)α² + (27/7)β² uses t = 7/20. The optimal t = √(Ξ(D)/Ξ(F)) ≈ 0.3586 gives
  (√0.000024 + √(0.01815·0.00017))² = 4.42967 × 10⁻⁵ M instead of 4.43012 × 10⁻⁵ M. That adds about 4.5 × 10⁻⁹ M to the margin (+0.4%), which is cosmetic.
- The margin (10⁻⁶ M) is far below the cost of excluding even one more pair (~0.0015 M).

## What is new here: 176 needs only 2 excluded pairs

`pair_exclusion_tuples.c k D G` searches every admissible k-tuple in [0, D] (sieving all primes ≤ k) for the fewest pairs more than G apart.

| shifts k | target gap G | fewest pairs > G | tuple diameter |
|---|---|---|---|
| 39 | 180 | 1 (the 180 paper) | 182 |
| 39 | 178 | 2 | 182 |
| **39** | **176** | **2**, both at site 0: (0,180), (0,182) | 182 |
| 39 | 174 | 4 | 182 |
| 38 | 176 | 0 (H(38) = 176) | 176 |
| 38 | 174 | 1 | 176 |
| 38 | 172 / 170 | 2 | 176 |
| 40 | 178 / 176 | 5 / 6 | 186 |

The 176 tuple, 39 shifts:
`0 6 14 20 24 26 30 36 42 44 50 54 62 66 72 80 84 86 92 96 104 110 114 120 126 132 134 140 146 150 152 156 162 164 170 174 176 180 182`.
It is admissible mod every prime ≤ 37, and its only pairs more than 176 apart are (0,180) and (0,182). Both contain 0, so the bad-pair graph
has no triangle, and the 180 paper's Lemma 2.1 argument carries over with B(n) = 1_P(n)(1_P(n+180) + 1_P(n+182)).

**Cost:** two pair terms instead of one, roughly 2 × 0.00153 M. Against the 180 paper's accounting, that is about 0.0015 M short.

## Where the extra 0.15% could come from

`mk_signatures.py` gives exact lower bounds for Maynard's M_k with weights Σ c·(1−P1)^a·Π P_λ. It reproduces Maynard's M₁₀₅ = 4.002069.
The 182 and 180 trials use only angular signatures of degree ≤ 6. In this plain simplex model:

| k | sig ≤ 6 | sig ≤ 8 | gain |
|---|---|---|---|
| 39 | 3.58899 | 3.64083 | +1.44% |
| 38 | 3.57273 | 3.62274 | +1.40% |
| 37 | | 3.60393 | |

Radial degree is saturated: going from 8 to 12 at k=38 changes M by 0.003%.

Two candidate routes to **176** (as intended), neither certified:
1. 39 shifts with the tuple above, two excluded pairs and degree-8 signatures. This needs ~0.15% extra, and the model shows ~1.4%.
2. 38 shifts with no exclusion and degree-8 signatures. This needs ~0.45% extra (the M₃₉/M₃₈ gap), and the model shows ~1.4%.

**Caveat:** the plain M_k model ignores the restriction, Harman and Type III losses of the real criterion, which also depend on the weight.
Making either route a theorem means re-optimizing the multi-component spline trial with 22 signatures and recertifying every numerical premise.
The 180 paper's certification is much larger than this repo's scripts.

## Max gamified vs as intended
- **As intended:** no new bound. Best leads are the two 176 routes above.
- **Max gamified:** the site's Lean statement (`bigospeedrun/verifier` `challenges/prime-gaps/Statement.lean`) is tight, and the tuples are optimal.
  The only game is that the board lists unchecked Claimed entries. Posting 176 from the model alone would be an unsupported claim, so it isn't made here.

## Files
- `narrowest_admissible.c`: exhaustive H(k). It reproduces H(10)=32, H(20)=80 and H(50)=246, and gives H(36..41) = 162, 168, 176, 182, 186, 188.
- `one_pair_exclusion_exact.c k D G`: exact test for a k-tuple whose only pair more than G apart is {0, D}.
- `pair_exclusion_tuples.c`: fewest pairs more than G apart (an upper bound on the minimum; the "no single-pair 178 tuple" claim was proved by the exact variant).
- `mk_p1p2.py`, `mk_signatures.py`: exact M_k lower bounds.
- `earlier-findings.md`: earlier notes on the 182 entry (margin 6.5 × 10⁻⁵, five-idea attempt).
