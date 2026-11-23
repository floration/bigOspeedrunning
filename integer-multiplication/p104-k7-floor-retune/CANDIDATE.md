# Candidate: re-optimise the K7 ordinary floor for the new 8/L suffix charge (2026-11-23)

Base: CrocSwap/integer-mult-bounds open PR #8073 (Codex, `research/p104-weighted-k7-suffix`, head cf4c4b7e), κ = 0.003898219753506.
Status: **math only, computed with my own scripts (`floor.py`, `alloc.py`). #8073's own verifier has NOT been re-run on it yet.**

## The idea
The ordinary finite factor in #8073 is

F(L, s) = (47/20)(256/255)(4097/4096)(1028/1024) · (1024·134·L)^c · (1 + s/L + δ) / ((1 − 10/L)(1 − δ)^3),  c = 4391986206293/2^50,

and the ordinary debit is any D with F < 2^D. #8067 chose the floor L = 18960 when the suffix charge was s = 64. That is the optimum for s = 64, since L* ≈ (s + 10)/c = 18,970. #8073 cut the suffix to s = 8 (its directed bound is 10Σk/(tΨ) < 7.4396, which does not depend on L) but kept L = 18960. For s ≈ 8 the optimum floor is L ≈ 4,500.

| s | L | log2 F · 8192 | debit D |
|---|---|---|---|
| 8 (#8073) | 18960 | 11203.87 | 11204/8192 |
| 8 | 4616 | 11173.61 | 11174/8192 |
| 15/2 | 4488 | 11172.32 | **11173/8192** (0.68-tick reserve) |

The floor checks in #8073's `check_ordinary_floor.py` (even, L > 48, L^t > 1024, (1 − 10/L)Ψ > 1, the 77-power delay bound) all hold at L = 4488.

## Reallocation under the same clock cap 318292011
I used the same model #8073 uses: a three-stage ordinary recurrence with 1e-21 booking ticks, Gaussian rate 17145637307/2^42 − (64939/2^19)/G, stop 5e-18, and clock 1731 + 320Σh + 220G ≤ 318292011.

- My script reproduces #8073: (8192, 117168, 524288; G = 501831), sup 0.0038982197535060614 (they install .003898219753506).
- New, D = 11173/8192: (8192, 110635, 524288; G = 511334), clock 318292011, sup 0.003898224339933345, so install **κ = 0.003898224339933**.
- The gain over #8073 is **+4.586e-9**, about the same size as #8073's own step (+5.47e-9).
- With s = 8 instead (L = 4616, D = 11174/8192): κ = 0.003898224196015 (+4.44e-9).
- I also checked 2- and 4-stage allocations. Both are worse, and 3 stages stays optimal.

This counts as as-intended in the same sense as #8073: it is a changed charged finite factor under the same signed words and the same cap. It is not a cap lift.

## For reference (gamed): lifting the clock cap
Gaussian binds at the height cap, so the debit change doesn't matter there. With G = h3 = 524288 the result is κ ≈ 0.0038982303256; with 20-bit heights (2^20 − 1) it is ≈ 0.0038983484.

## What's needed to make it a package
Fork #8073's `prepare.py`/checks with LOWER 18960→4488, suffix 8→15/2, D 11204→11173, the new profile and κ, and then regenerate the hard-coded regression constants (fixture counts, reserves, cuts, seam ceilings) by running the replay.
