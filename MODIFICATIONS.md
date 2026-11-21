# Modifications to the verified APSP baseline

Joshua Wharton · QFEX · joshua@qfex.com

The source baseline is the complete `fringewidth-apsp-299556085` submission at `bigospeedrun/verifier` commit `319252b348e254a4257cdc69805fd6eec3f5cd94`. Original license and copyright notices remain in the files. This refinement changes 17 of its 401 Lean source files.

The query cutoff changes from `56569/500000` to `5656907/50000000`; the block exponent changes from `336175/10000000` to `3361758/100000000`. The tensor depth multiplier remains 20. The code constants, time bounds, and word bounds are changed together. Six real logarithm enclosures and new entropy estimates justify the tighter exponent. The final exact challenge theorem improves `2.99556085` to `2.995560766`.

No instruction semantics, input constraints, output conditions, graph definition, or runtime definition is changed. The source of `Submission/EndStatement.lean` is byte-for-byte unchanged.

## Modified Lean files

- `Submission/ThreeSumApsp/Batch/Final.lean`
- `Submission/ThreeSumApsp/Batch/Numbers.lean`
- `Submission/ThreeSumApsp/Batch/OBound.lean`
- `Submission/ThreeSumApsp/Batch/ONeedPoly.lean`
- `Submission/ThreeSumApsp/Batch/OParams.lean`
- `Submission/ThreeSumApsp/Batch/OProg.lean`
- `Submission/ThreeSumApsp/Batch/ORunParams.lean`
- `Submission/ThreeSumApsp/Batch/OSetup.lean`
- `Submission/ThreeSumApsp/Filter2/Asymp.lean`
- `Submission/ThreeSumApsp/Filter2/Chain.lean`
- `Submission/ThreeSumApsp/Filter2/Defs.lean`
- `Submission/ThreeSumApsp/Filter2/Final.lean`
- `Submission/ThreeSumApsp/Filter2/HostMain.lean`
- `Submission/ThreeSumApsp/Filter2/HostMath.lean`
- `Submission/ThreeSumApsp/Filter2/HostTime.lean`
- `Submission/ThreeSumApsp/Filter2/HostTop.lean`
- `Submission.lean`

## Supporting files

`manifest.json` records the new rational bound. The toolchain, Lake files, `verify.py`, documentation, and `provenance.json` make the full proof independently reproducible. `provenance.json` records the original and modified SHA-256 hashes for each changed Lean file. It is provenance metadata, not a premise of any theorem.

The complete program, compiler, and inherited proof remain attributed to Li Xuanji, Hrishik Sai Bojnal, Anthropic, and the original paper authors, as detailed in the README. The new parameter refinement and proof modifications are attributed to Joshua Wharton, QFEX. AI assistance was used in preparing and reviewing these changes.

## Second refinement: 2.995560766 to 2.9955607647814

Hrishik Sai Bojnal (fringewidth), with Claude Opus 5.5, 2026.

The base is the tree above (source commit `32c6858cf43efd48bf9c8a3541274e7a655ca2ad`). The query cutoff changes to `θ = 155816/1377219` and the block exponent to `σ = 136966/4074237`. These rationals approximate the exact balance point of the box, query, and encoding exponents at `c = 20`. The certified bounds become `Γ > 0.0660254968003`, `q < 0.4339745031995`, and `19 ln 3 / ln 4 < 15.057143756851`. The `p ≤ s n^ε` slack drops from `1e-11` to `1e-13`, the host margin `η` drops from `1e-10` to `1e-13`, and the chain of exponents becomes `2.9955607647791` (absorption premise), `2.9955607647811` (oracle, before the constant), `2.9955607647812` (oracle), `2.9955607647813` (host), and `2.9955607647814` (final). The same Lean files change as in the first refinement.

## Third refinement: 2.9955607647814 to 2.9955607132692 (fractional tensor depth)

usbTypeF, with Claude, 2026. All credits above are retained.

The base is fringewidth/apsp-bound commit `f1f7486411b8a59c351b2fbe75ee680f82ce0579`. At the integer depth `c = 20` the balanced limit of `max(3 - 2Γσ, 2 + (2B - 1/2)σ, 3 - (1 - 2q)σ)`, with `B = (c - 1) ln 3 / ln 4`, is about `2.99556076477889`, which the second refinement had used up. The lemmas of the paper's Section 4.4 already take a real depth `c > 10` (`levelsOf c m = ⌈c m⌉`, `tail_div_M_le`, `K_le_exp`, `Corollary31.rho_lt`), and the program `procs31 G` already contains `Proc.levels31 = ceilMulBody G.a G.b`. This refinement sets `c = 502/25`, where the limit is about `2.99556071326668`:

* `c = 502/25`, `θ = 225677/1996332`, `σ = 152980/4570079`.
* The oracle computes `L = ⌈502 m / 25⌉` with the call `.call Proc.levels31 [v Mm] Ll` (the parameters `G20` become `a = 502`, `b = 25`), and `oL s p = (502 m + 24) / 25`, so `20 m ≤ L ≤ 21 m`.
* The certified bounds become `Γ > 0.0663089654688`, `q < 0.4336910345308`, and `(477/25) ln 3 / ln 4 < 15.12054225688` (with `κ < 2.9` and `1/(1 - ρ_c) = 53/28 < 1.9`). All logarithms are new 40-term atanh enclosures in `Batch/Numbers.lean`.
* `N₀ = 3^{L - m} ≤ e² D^B`, because `25 (L - m) ≤ 477 m + 24`; the boxes, `4^L` and polynomial-need bounds use `L ≤ 21 m` (constants 36288, 80, `Y = (16Q)^42`, `polyBound 3360 840`).
* The chain of exponents becomes `2.9955607132669` (absorption premise), `2.9955607132689` (oracle, before the constant), `2.9955607132690` (oracle), `2.9955607132691` (host), and `2.9955607132692` (final; `manifest.json` and `Race.bound` use the reduced fraction `7488901783173/2500000000000`). With the `1e-13` slack, the box, encoding and query exponents are about `2.995560713266793`, `2.995560713266038` and `2.995560713266716`.

Changed files: `Batch/Numbers.lean`, `Batch/OParams.lean`, `Batch/OProg.lean`, `Batch/ORunParams.lean`, `Batch/OSetup.lean`, `Batch/ONeedPoly.lean`, `Batch/OBound.lean`, `Batch/Final.lean`, the `Filter2` files that carry `σ` or the exponent, `Submission.lean`, `manifest.json`, `verify.py` (the prior bound) and this note. `EndStatement.lean` is unchanged.
