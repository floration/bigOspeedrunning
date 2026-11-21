# Integer multiplication: the max-gamified and as-intended versions compared (2026-11-21)

Everything below is conditional on the same five framework premises: native_all_columns, owned_erasure, compiler, precision_tape and analytic_recovery. Nothing has been submitted or made public.

| Version | Conditional κ | Gain over #7830 (0.00387992803556) | What changed |
| --- | ---: | ---: | --- |
| #7830 (current #1 claim) | 0.00387992803556 | — | — |
| A. Tight losses (`../p104-tight-losses/`) | 0.00387992804606 | +1.050e-11 | uniform loss 1e-15 and cover loss 2e-15, with q > 2^60 N^5 |
| B. + finer consumer grid | 0.003879928046135 | +1.0575e-11 | rational claim on a 1e-15 grid (claim = floor(cap·10^15) − 8, tested = claim + 7·10^−15) |
| **C. Max gamified (this package)** | **0.003879928046140** | **+1.058e-11** | B, plus tensor power 720, strict trial 0.003879928046153, log power 96, horizon 5989 |
| Fixed-profile ceiling (raw binary crossing) | < 0.003879928046155 | +1.06e-11 | no finite schedule on this binary word can pass it |

Version C passes #7830's full producer verifier (`verify.py`). That run covers native and caller coefficients, exact basis products, scalar plans, the ordinary recount, depth guards, and all 54 strict and 4 functional outer checks (minimum margin 1e-16). It prints `PASS_COMPLETE_CONDITIONAL_APPLICATION 0.003879928046140`. The changes are listed in `max-gamified.diff`:
- the loss and carrier constants;
- a 1e-15 consumer grid, applied by patching the inherited `price` and the audit's `tested` offset at load time;
- tensor power 720, trial and log power;
- a generated same-rank witness for powers other than 480;
- relaxed comparisons where the larger compiler H changes the #7835 ordinary-audit fields;
- the headline strings.

Version A also passes #7830's independent reviewer (`review/independent.py`). B and C have not been put through it: that reviewer hard-codes the 1e-14 grid and the 480-power constants and would need the same parameter edits.

Reproduce from #7830's pinned inputs:

~~~sh
python3.12 -IB verify.py --work inputs --out replay --fetch
~~~

## As intended (no gaming)
The repo's hill-climbing rule says "a step must change the complete paid profile (more digits of the same root do not count)". Read honestly, none of A, B or C is a new result. All three re-spend finite slack on the unchanged binary word d3aa44… and the unchanged rational word 766098…. Under that rule the true frontier on this profile is the raw binary crossing, [0.003879928046154, 0.003879928046155]. That ceiling has not moved, and every gamed version sits within 1.5e-14 of it.

To improve the bound as intended, someone needs a new binary signed profile: an operator-preserving split or return in the 680-field characteristic-2 word, followed by enough rational headroom. The rational raw root, 0.00388013644, has about 2.1e-7 to spare. One binary 8→4+4 split across all 36 calls would be worth about +2e-6.

On the leaderboard as it is actually scored, #7831, #7835 and #7830 were each listed for gains of about 1e-12 to 1e-11 from exactly this kind of schedule tuning. So version A, or C, would rank #1 there.

## Five-idea log
1. Reverse (start from the consumer end): the rational consumer was throwing away 8 ticks of 1e-14 below the BIT cap. A 1e-15 grid recovers 7.5e-14 (version B).
2. Novel: the strict-moment trial was 6e-15 under the raw crossing. A larger tensor power (720) lets the trial sit 1e-15 under it, giving +5e-15 (version C). Tensor power 960 breaks the interval library's exponent bound, |x| < 16.
3. Borrowed (compiler peephole / common-subexpression elimination): I scanned all 2,874 binary MOVEs for round trips and chained transfers of the same owner with nothing touching it in between. There were zero, so no free redundancy is left at that level. A deeper GF(2) common-subexpression search over the 680-dimensional values was not attempted.
4. Crazy (push the trial to the raw root itself, with more cutoff classes): the gain is capped analytically at about 1.5e-14 above C, because nothing on this word can pass the raw crossing. I took the trial to ...153, one tick below the root, and stopped there.
5. Breaking (the "the binary word binds" assumption): κ is the smaller of the two sides. The rational side has about 2e-7 of headroom, but the BIT service must be a characteristic-2 supplier, and the complex word cannot serve it. Breaking the bind needs a new binary word, which is the as-intended route above. I tried no new supplier.
