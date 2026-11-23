# Conjugate-pair merge on the Gaussian word: scan results (2026-11-23)

Result: **no candidate.** No rewrite of this kind beats κ = 0.003898224460300, so nothing went to the checker.

## The literal idea doesn't apply
The "Gaussian" word used by #8027/#8057/#8073 (`research/p104-live-relative-gain/WORD.json.gz` plus its deltas) has rational coefficients (1/2, 1/3, ...), and its charts are GF(2) subspaces of a 9-bit space. There are no complex z / z̄ pairs, so conjugation has nothing to merge.
The closest real version is #8027's forward/adjoint sharing (BIDIRECTIONAL.md). There, a transfer that matters only forward, written (u,0), shares a link with one that matters only backward, written (0,z). The chart-3 helper encoding is free, so chart-3 data may be re-encoded.

## What #8027's 21 merges actually were
- 31 retired transfers and 11 new ones, all new ones going straight to chart 127.
- Retired grade sum 66 = added grade sum 66. So they are relay-chain shortcuts that change no linear sums, and the gain comes only from concavity, about +1e-6 raw each. None of them is a deletion.

## New exact scans (mod p = 2147483629)
Words rebuilt with my own code. The 5,680 and 5,676 words match #8027's SHA-256 pins.
| Scan | 5,700 | 5,680 | 5,676 |
|---|---:|---:|---:|
| Adjoint-dead transfers | 0 | 0 | 0 |
| Charts with adjoint (transpose) dependencies | 0 | 0 | 0 |
| Relaxed deletions (u has no X part, z in span at its source chart) passing the X-side test | 323 | 319 | 316 |
| ...that keep the chart-3 block invertible | – | – | **0 of 316** |
| Joint pair deletions with both cross terms nonzero | – | – | 70 screened, 6 tested exactly, all lose rank 2 |
| Chart-3 relay chains into chart 127 left to shortcut | – | – | 0 (only 10 chart-3-only transfers reach 127, all direct) |

Reading: every chart-3-only transfer is the only carrier of some helper information. Folding it into other transfers keeps the X outputs right but loses one dimension of chart-3 information. So a single relaxed deletion can't work, and the pairs tested also fail. #8027's shortcut family looks used up at chart 127.

## Still open (not attempted)
1,201 relay pairs of chart-3-only transfers elsewhere in the 5,676 word, i.e. shortcuts that don't end at 127. Each would be worth roughly +1e-6 on the raw Gaussian root, if one can be made to work. Testing them needs #8027's per-chart re-solve (K U_in = U_out, Kᵀ Z_out = Z_in) for each proposed structure. Even a working one would then need the #8027 rational application and the #8057 → #8073 → p104-k7-floor-retune chain rebuilt and replayed.

## Files
uz.py (forward u and adjoint z vectors), scan.py, dual.py, relaxed.py, relaxed2.py, pairs.py, applyS.py (exact delete-and-check), chains.py, rebuild.py (applies the delta format).
