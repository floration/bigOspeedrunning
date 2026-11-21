# Contingency tables: repair coefficient 80,000·d^17 → 20,000·d^17

`IdealQuarterRefinement.lean` keeps the chains, scales (U = 5d^3, L = 3d), proposal and exact Poincaré coefficients of the upstream `Math115.PhysicalRepairRefinement` development. Only the final scalar estimate changes. The upstream envelope used U(U+1)/2 ≤ 3U²/4 and (U+1)² ≤ 9U²/4. At U ≥ 6655 both have leading constants 1/2 and 1, which gives refinedConstant ≤ d³U⁴/4 instead of d³U⁴. The coefficient falls from 80000·d¹⁷ to 20000·d¹⁷, and the unit branch from 40000·d¹⁷ to 10000·d¹⁷.

`chk.py` checks the arithmetic. The Lean file has to be built against the upstream Math115 development, and the proof is the upstream authors' work apart from this final estimate. Status: Claimed. The 20,000·d^17 proof (`IdealQuarterRefinement.lean`) compiles against EcoDataLab/contingency-tables @ d851f00 (built 2026-11-21).

## Retuned scales: 12,062·d^17 (`IdealTunedScales.lean`, `chk2.py`)
This retunes the ideal-only threshold to U = ⌊141d³/32⌋, keeping L = 3d. That's the smallest threshold of this form that the existing padding-count budget 47(gL)e ≤ 32(U+1) allows. Combined with the quarter envelope above, the inverse-gap allowance becomes (141⁴/32³)·d¹⁷ < 12,063·d¹⁷, and the unit branch gets half of that. Scope: this proves the actual-chain Poincaré bound and the padding count at the new scales. The later completion-program and sampler modules are instantiated only at U = 5d³ and aren't re-proved here. Build of `IdealTunedScales.lean` pending; if it fails, the claimed value falls back to 20,000·d¹⁷.
