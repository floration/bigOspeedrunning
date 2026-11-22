# 3SUM: exponent 1.920279408184921

`tighten-target.patch` changes the target of the current Lean Verified 3SUM proof's `Race.bound` from 384055881637/200000000000 (1.920279408185) to 1920279408184921/10^15 (1.920279408184921), together with the matching certified-optimality and budget files. The gain is about 7.9e-14: the same weighted-cache construction with its last digits tightened.

Build (q's PC, 2026-11-22): all 1568 modules pass, and the axiom audit shows only propext, Classical.choice and Quot.sound. The full tree is on the PC (BIGO\3sum-tighten). Credit: the construction and proof are the upstream authors' work.
