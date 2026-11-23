# Integer multiplication

**By:** floration. Builds on the upstream work credited below.

**Our best value:** conditional κ = 0.003898348449639 (gamed, CrocSwap PR #8086). As intended: 0.003898230327195 (PR #8082).
**Listed record:** 3.890115286e-3 (Chris R, Claimed, Nov 21).
**Status:** Claimed, conditional on the framework's five premises.

## What changed
#8082 drops a reserve in the P104 mixed-cutoff BIT supplier, with the Gaussian height capped at 2^19. #8086 stacks a 20-bit height lift on top, which enlarges the budget. Both are open as pull requests on CrocSwap/integer-mult-bounds, which is this problem's review repo.

## How to check it
Each PR carries its own replay scripts (verify.py plus an independent reviewer). The packages in this folder are earlier steps in the same line.

## Credit
**Main author: floration.** Builds on the CrocSwap integer-mult-bounds contributors, whose P104 framework and #7830 package this builds on. floration opened both PRs.

- https://github.com/CrocSwap/integer-mult-bounds/pull/8082
- https://github.com/CrocSwap/integer-mult-bounds/pull/8086
