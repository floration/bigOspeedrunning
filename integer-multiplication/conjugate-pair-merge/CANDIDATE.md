# Candidate: five chart-3 relay shortcuts on the Gaussian (rational) word (2026-11-23 ~05:50 UTC)

**Status: exact map verified over Q with my own code. Not yet replayed with CrocSwap's verifier, and the Gaussian transport trial has not been re-certified.**

## What changed
Base: #8027's final rational word, 5,674 transfers (rebuilt from WORD + BIDIRECTIONAL + QUOTIENT + HELPER-SPLITS + BANK-FACTORS; SHA-256 matches `38d2b3a2…`).
Each shortcut replaces two chart-3-only transfers, X: a→b and Y: b→c (nested a ⊂ b ⊂ c, Y reads X), with one direct transfer D: a→c. D takes X's form, Y's readers at c are dropped, and 3–4 outputs at c read D (coefficients ±1/2, ±1).
| X | Y | charts a→b→c | grades | new label |
|---|---|---|---|---|
| 95398 | 99468 | 412→798→922 | 2+3 → 5 | first new |
| 97628 | 100531 | 614→795→917 | 2+2 → 4 | +1 |
| 95050 | 101275 | 392→1037→918 | 3+2 → 5 | +2 |
| 95056 | 95425 | 411→1038→921 | 3+2 → 5 | +3 |
| 96741 | 96743 | 365→1028→529 | 3+2 → 5 | +4 |
This leaves the X-side map exact, but the chart-3 (helper) block becomes E33 ≠ I. E33 is invertible: it changes 281 columns and touches 511 rows. I re-encoded the chart-3 inputs with E33⁻¹, This touches only chart-3 local forms and no transfers or inputs. The net diff against the base is 44 changed rows (15 at chart 3) plus the 5 new moves, and total form terms fall from 323,573 to 322,917. initial, final and frames are identical to the base.

## Checks (exact, Fractions)
- The full forward map of the new word equals the base word's map on all 1,291 outputs (`exact2.py`: EXACT MAP EQUAL: True).
- 5,669 transfers. Every new move joins strictly nested charts, and donors sit at the right charts by construction.
- Endpoints are unchanged, so the productive (target) histogram is unchanged.
- Literal peak is still 57 bits.
- Word file: `w5669_shortcut5.json.gz`, sha256 ed3bea7186f962f3a8a8ae389cecce3d1ef48a7a832cf9af6c9048a6b5919b35.

## Value
- Paid histogram (48 calls): grade 2 38016→37728, grade 3 23040→22848, grade 4 10848→10896, grade 5 15072→15264. Everything else is unchanged (`hist5669.json`). The linear sum is unchanged, so the gain is from concavity only.
- **Raw Gaussian root: 0.00389848144655 → 0.00390146621942 (+2.985e-6).** `census.py` reproduces the published histogram and root on the base word.
- What κ gains depends on the ordinary side. Under today's caps (heights ≤ 524288, clock 318,292,011) the Gaussian side stops binding. Assuming the trial keeps today's raw-to-trial loss (1.49e-8), the best allocation is G ≈ 39,000 and h ≈ (24576, 418980, 524288), giving **κ ≈ 0.0038982624, about +3.2e-8 over #8082**. The checker's finer search (chk4.py) gives 0.0038982732, or 0.0038982794 with #8076's tariff, and confirms the 5r ≤ 4k transport tail passes. With 20-bit heights (combine-and-lift) the ceiling is higher.

## Still needed before it counts
1. Re-certify the Gaussian trial (`unpowered_price.certify`, moment + 5r ≤ 4k transport, two types 5:451) on the new histogram.
2. Turn the word into a #8027-format delta and re-run the rational application: scalar compiler, ordinary work and depth bound. Chart-3 re-encoding adds ordinary work at chart 3.
3. Re-run the #8057 → #8073 → #8082 allocation chain and the official replay.
