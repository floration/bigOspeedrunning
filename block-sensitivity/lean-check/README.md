# Local check of the exact-limit block-sensitivity solution

`Solution.lean` is a copy of `../Sol_reach_exact_log_5591_10121928.lean`.
The two `Theorems/` files are trimmed stubs. Each keeps the exact statement of
a platform theorem that is already Proved, but the proof is `sorry` and the
heavy imports are removed. This check only confirms that the new wrapper
type-checks against those statements. prove2.me supplies the real proofs.

Steps (needs elan):
    cd lean-check
    # if lake rejects the short rev, replace it with the full Mathlib commit for 0df444a
    lake update            # fetches Mathlib at 0df444a
    lake exe cache get     # downloads prebuilt Mathlib .olean files
    lake build Solution

Expected: "declaration uses 'sorry'" warnings in the two stubs only. The
`#print axioms solution` line should list sorryAx only through the stubs, and
there should be no errors in Solution.lean.
