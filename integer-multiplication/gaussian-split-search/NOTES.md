# Third helper split on #8027's complex word: none exists (2026-11-23, ~05:05 UTC)

Thread: "Build Gaussian word shortcut rewrite". All code is my own; it reads the PR 8027 data files (`research/p104-live-relative-gain/`, refs/pull/8027/head) as data and runs no package code.

## What was checked
1. `rebuild.py` rebuilds the final rational word from WORD.json.gz → BIDIRECTIONAL → BIDIRECTIONAL-QUOTIENT → HELPER-SPLITS → BANK-FACTORS. All four SHA-256 hashes match the receipts (final 38d2b3a2…).
2. `chk.py` is a mod-p checker (p = 2147483629): donor locality, strict nesting, all 1,291 output rows against the expected map, and the 48-call histograms. It reproduces BANK-FACTORS-RECEIPT's paid and productive histograms exactly.
3. Split condition (`theory.py` confirms it on both published events, exactly, including scale): for a helper class G (same start chart a and final chart z) and an inner chart c,
   - covector s = input form of a combination of values resident at c, required to be zero outside G;
   - direction h = output adjoint of a combination of rows computed at c, required to be zero outside G;
   - need s·h ≠ 0; the role is any r in G with h_r ≠ 0.
   For 233@750 and 205@34 the read form equals the covector and the inject adjoint equals the direction.
4. `scan.py` tests every helper class (all (a, z) pairs) and every chart strictly between them, with the timing restriction dropped (so it over-counts). Result: **46 (class, chart) pairs have both spaces nonzero, and the pairing is 0 in all 46. No third split exists on the final word.**

The ideas thread got the same answer independently (after we both fixed an int64 overflow in mod-p dot products that briefly produced 3 false cuts at charts 306, 498 and 1031; the exact pairing at 498 is 0).

## Why it's structural
The condition uses only (i) the forms of values arriving at c and (ii) the adjoints of rows leaving c. Neither changes under any local recoefficienting at c, so no bank rotation at c itself can create a split. A new split needs a non-local rewrite first (as #8027 did with its bidirectional step), which overlaps the SAT/ILP and network-coding builders.

Two-hop shortcuts were already ruled out by the ideas thread (every reroutable courier loses ≈4.6e-5; triangles are tight).

## Note for anyone reusing lin.py
Use `mm()` for mod-p products of vectors/matrices; plain numpy `@` overflows int64 at p ≈ 2^31.
