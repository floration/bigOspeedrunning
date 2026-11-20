# Heilbronn triangle: smaller packing for Blinov's degree-five scheme

**Claim (conditional, same scope as Blinov PR #13):** η = 2/(249k+5) with k = 317,831, i.e.

    η = 1/39,569,962 ≈ 2.5272·10^-8

That beats Blinov's 1/50,893,237 ≈ 1.9649·10^-8 by 28.6% and the board-reported Qiuyu Chen value 2/100,866,719 ≈ 1.9828·10^-8 by 27.5%.

## What was changed
In Blinov's "reserved tag words" checkpoint (github.com/littleBro/heilbronn-triangle-bounds, PR #13, commit e29a291) the only property used of the packing is:

* a set S ⊂ [0, ∞) of 2,921 integers with no nontrivial solution to x + y = 2z (3-AP-free),
* exactly five elements below 10 (the label tags; argument needs tag span 10 and k ≥ 20),
* k = 2·max(S) + 1, with norm positions u (rows 1, 2) and k − 1 − 2u (row 3).

Lean's `reserved_packing` uses only this midpoint property (via `zero_energy_midpoint`). Blinov uses binary-ternary words, max 204,390, so k = 408,781.

New set: the 2,921 smallest elements of

    S = A1 + 37·A2 + 1369·C
    A1 = {0,2,3,5,9,19,26,27,30,31}  (3-AP-free in Z/37)
    A2 = {0,1,3,7,17,24,25,28,29,35} (3-AP-free in Z/37)
    C  = {0,1,3,4,9,10,12,13,28,29,31,35,36,38,51,65,78,80,81,85,87,88,103,104,106,107,112,113,115,116}
         (30 elements in [0,117), 3-AP-free; found by tabu search, beats the binary-ternary set's max 118)

Proof of 3-AP-freeness: if s1+s2 = 2s3, reduce mod 37. A1 is 3-AP-free mod 37, so the A1 parts are equal. Cancel them and reduce mod 37 again, so the A2 parts are equal too. Then c1+c2 = 2c3 in the integers, and C is 3-AP-free (checked directly), so the C parts are equal. Tags are {0,2,3,5,9}, and the next element is 19. max(S) = 158,915, so k = 317,831.

## Files
* `packing_2921.txt` has the set.
* `verify_packing.py` checks all 2916² row pairs, the tag exclusions, and computes k and η.
* `check_construction.py` checks the mod-37 conditions and rebuilds S.

## Search limits (final push)
* A tabu search of cyclic groups Z/W for W in 38–174, 201–254 and 331–362 found no 3-AP-free set denser than Z/37 with 10 elements (|A| > W^0.6378). Exhaustive search covered W ≤ 66.
* A tabu search found no 30-element 3-AP-free set in [0,116).

## Caveats
* The claim is conditional exactly as Blinov's is. It assumes the manuscript's geometric estimates and the written transfer, and it holds for all sufficiently large n. The only new input is the packing.
* The Lean `ReservedPacking` proof would need re-instantiating. Its `interval_family` and `zero_energy_midpoint` are specific to ternary words. The mod-37 argument is a finite `decide` over 10³ triples per block plus a decide over the 30-element top set.
* Qiuyu Chen's paper was not read (no URL found). Its formula is different, so this packing may combine with it.
