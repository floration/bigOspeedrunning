# Average sensitivity (max gamified): AS(f) ≤ (353514424368353/110766156451452)·d·√n

- **C** = 353514424368353/110766156451452 ≈ 3.19153824321146142352. That is 1.34e-21 above the proof's floor 8/√(2π), and as close as Mathlib's `Real.pi_gt_d20` can certify.
- **Upstream:** https://github.com/darkhipo/average-sensitivity-lean, base 78fe0e6. Only the rational constant and its π certificate changed (same four text replacements as the 476765550/149384251 entry).
- **Build** (user's PC, 2026-11-21, local commit 9d3e5fa on branch sharpen-353514424368353-110766156451452): `lake build` printed "Build completed successfully (3432 jobs)". `lake env lean Submission.lean` and `lake env lean AxiomAudit.lean` both exited 0. There were no errors and no `sorry`.
- **Axioms:** `Race.bound` and `AverageSensitivity.AS_bound_353514424368353_110766156451452` depend on [propext, Classical.choice, Quot.sound].
- **Submission.lean sha256:** 2f9e373b65a258525fd1b50d27982a2a801b2b250a0ebec6b59c356de20d3dac (matches the PC build).
- This is decimal-tuning only. The honest value of this method is 8/√(2π).
