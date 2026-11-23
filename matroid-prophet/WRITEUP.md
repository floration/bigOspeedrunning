# One-sample matroid prophet

**By:** floration. Builds on the upstream work credited below.

**Our value:** C = 5.168434e-10 (gamed). As intended: 5.116809e-10
**Listed record:** ≈5.1149e-10 (darkhipo)
**Status:** Claimed.

## What changed
Re-tunes the algorithm's free numbers: mask rates, a phase grid of L = 2^24, and a decoupled max-branch coin. The as-intended value leaves the algorithm unchanged and tunes only the analysis.

## How to check it
certify_final_tau.py is an exact-rational checker. Its output is saved next to it.

## Credit
**Main author: floration.** Builds on: darkhipo, for the algorithm and the original certificate. This folder builds directly on their work. Full repository: https://github.com/floration/bigOspeedrunning
