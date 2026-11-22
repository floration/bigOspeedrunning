# 3SUM: exponent 1.920279408184921

**What changed:** only the proof's last safety margin. `tighten-target.patch` (9 files, 16 lines) moves `Race.bound` from 384055881637/200000000000 (1.920279408185) to 1920279408184921/10^15 (1.920279408184921), a gain of about 8e-14. There is no new algorithm.

**Upstream:** https://github.com/Wang-jiong-han/3sum-weighted-cache @ e1ae71db2231f172c6541820e2ce0a54aa14fc64, the current Lean Verified leader.

**Build** (q's PC, 2026-11-22): all 1568 modules built. The audit shows only propext, Classical.choice and Quot.sound. The repo's README, SUBMISSION.md and SOURCE_MANIFEST hashes still describe the old exponent, so `scripts/check_release.py` may fail on them. Lean verification is not affected.

**Credit:** the mathematics is entirely Jionghan Wang's (Wang-jiong-han). It builds on proof-factory/3sum-bound (c0ldzy17, JoshuaWharton, HrishikSaiBojnal) and on Alman and Vassilevska Williams. Their LICENSE, NOTICE and provenance files are kept in the full tree.
