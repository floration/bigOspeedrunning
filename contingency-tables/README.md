# Contingency tables: repair coefficient 80,000·d^17 → 20,000·d^17

`IdealQuarterRefinement.lean` keeps the chains, scales (U = 5d^3, L = 3d), proposal and exact Poincaré coefficients of the upstream `Math115.PhysicalRepairRefinement` development. Only the final scalar estimate changes. The upstream envelope used U(U+1)/2 ≤ 3U²/4 and (U+1)² ≤ 9U²/4. At U ≥ 6655 both have leading constants 1/2 and 1, which gives refinedConstant ≤ d³U⁴/4 instead of d³U⁴. The coefficient falls from 80000·d¹⁷ to 20000·d¹⁷, and the unit branch from 40000·d¹⁷ to 10000·d¹⁷.

`chk.py` checks the arithmetic. The Lean file has to be built against the upstream Math115 development, and the proof is the upstream authors' work apart from this final estimate. Status: Claimed, not built here.
