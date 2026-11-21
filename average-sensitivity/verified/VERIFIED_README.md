# Average sensitivity: AS(f) ≤ (476765550/149384251)·d·√n

- **Bound:** C = 476765550/149384251 ≈ 3.191538243211461, for every degree-≤d polynomial threshold function on {-1,1}^n (sign(0)=1), 1 ≤ d, 1 ≤ n.
- **Previous best (Lean Verified):** 90295/28292 ≈ 3.1915382440 (bigospeedrun/verifier#93). Improvement ≈ 8.15e-10.
- **Upstream:** https://github.com/darkhipo/average-sensitivity-lean, base commit 78fe0e65b6915143f3a8055f2444b8ec44b806b2.
- **Change:** only the final rational constant and its π certificate. The text replacements in AverageSensitivity/WallisAssembly.lean, AverageSensitivity/WallisMAD.lean, AverageSensitivity.lean, AxiomAudit.lean and Submission.lean:
  - `90295_28292` → `476765550_149384251`, `90295/28292` → `476765550/149384251`
  - `8153187025/800437264` → `227305389666802500/22315654446831001` (the constant squared)
  - `25613992448/8153187025` → `178525235574648008/56826347416700625` (the required π threshold, 32·q²/p²)
- **Certificate:** 64·149384251²·10²⁰ < 2·314159265358979323846·476765550², discharged with Mathlib's `Real.pi_gt_d20`. The constant is a continued-fraction convergent of 8/√(2π), 4.2e-18 above this proof method's floor.
- **Build (user's Windows PC, 2026-11-20):** Lean v4.33.1, Mathlib 0df444a. `lake exe cache get`, then `lake build` printed "Build completed successfully (3432 jobs)". `lake env lean Submission.lean` and `lake env lean AxiomAudit.lean` both exited 0. There were no errors and no `sorry`, only pre-existing linter warnings.
- **Axioms:** `Race.bound` and `AverageSensitivity.AS_bound_476765550_149384251` depend on [propext, Classical.choice, Quot.sound].
- **Submission.lean sha256:** 4999d8fe7b843bcccd9d158480aeb8905877186d4c16c170ce3eb763cdb8b770. This matches the file built on the PC (local commit 229bba9, branch sharpen-476765550-149384251).
- Doc comments still quote the old decimals ("3.191538244…"). They are cosmetic and were left as built.
