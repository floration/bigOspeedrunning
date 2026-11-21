# Contingency tables: as-intended vs. max-gamed

The board metric is the inverse spectral gap of the "ideal auxiliary chain", A·d^p. The record is 80,000·d¹⁷ (EcoDataLab).

| Version | Bound | Lean status | Sampler still valid? | File |
|---|---|---|---|---|
| As intended, nothing changed (scales and sampler as in EcoDataLab) | 20,000·d¹⁷ | Compiled, standard axioms | Yes, the full sampler is unchanged | IdealQuarterRefinement.lean |
| As intended, retuned threshold | 12,062·d¹⁷ | Compiled, standard axioms | The gap bound and padding count are proved; sampler modules are only proved at 5d³ | IdealTunedScales.lean |
| **As intended, best** (sharp log-2 padding budget) | **11,232·d¹⁷** | Compiled, standard axioms | Same as above | IdealLogScales.lean |
| Gamed (constant): unpadding success ≥ 1/K | ≈ 2592/ln⁴K · d¹⁷ (for example, about 700 at K=4) | Not written | Polynomial, but expected retries grow K× | (not written) |
| **Max-gamed** (threshold U=2) | **2048·d⁵** | Compiled, standard axioms | **No.** Unpadding can fail with overwhelming probability | GamedTinyThreshold.lean |

Why the max-gamed version is a true theorem: the upstream and EcoDataLab Poincaré theorem holds for every U ≥ 2, so U=2 is a legitimate instance. What makes the d¹⁷ result meaningful is a separate lemma, the padding count, which needs U ≳ 4.33·d³. The board metric only measures the gap, so it doesn't see the missing lemma.

Limits of the as-intended route: the proved constant equals the large-d limit of this argument, and the exact values peak at about 9,900·d¹⁷ for m, n < 60. Lowering it further needs new mathematics: a better p³ defect factor, a better U⁴ path factor, or removing the factor-2 loss from rounding the proposal rate to a power of 2.
