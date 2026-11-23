# Heilbronn triangle problem

**By:** floration. Builds on the upstream work credited below.

**Our value:** η = 1/30,650,782 ≈ 3.2626e-8
**Listed record:** ≈1.96e-8 (Ivan Blinov)
**Status:** Claimed.

## What changed
Uses Blinov's PR #13 reserved-tag scheme with the manuscript's tag span of 10, and drops the i_a = j_a choice, which the manuscript doesn't need. That lets a denser tricolored sum-free family of 2,916 pairs replace the 3-AP-free set.

## How to check it
Running verify_tricolored.py packing_L10.txt reports 0 violations.

## Credit
**Main author: floration.** Builds on: Ivan Blinov, for the scheme and the manuscript. This folder builds directly on their work. Full repository: https://github.com/floration/bigOspeedrunning
