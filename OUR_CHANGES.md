# APSP: c = 1807/90 retune, exponent 2.99556071322466

This builds on the Lean Verified APSP proof chain: Li Xuanji's proof, refined by fringewidth (c = 20, 2.9955607647814) and Joshua Wharton (see MODIFICATIONS.md). The base commit is in BASE_COMMIT.txt. The only change is the tensor-depth multiplier, from c = 20 to the fractional c = 1807/90, with θ and σ re-derived to match. `final-1807-90.patch` is the full diff against the base.

- `Race.bound` as in Submission.lean, see manifest.json (≈ 2.99556071322466).
- Checked on 2026-11-21 with the verifier's Lean `verify.py` on q's PC: pass (`VERIFY_RESULT.txt`).
- `verification.c20-original-fringewidth.*` are the ORIGINAL receipts from fringewidth's c = 20 run, kept for provenance. They are not receipts for this build.
- The base repo's `.github/workflows` was left out of this branch.

Credit: the proof is the upstream authors' work. This is a parameter retune (ported/refiled per the site's terms).
