# Tight finite losses for the mixed-cutoff P104 BIT supplier

The full application replay gives **conditional κ ≥ 0.00387992804606**. This gains **0.00000000001050** over #7830 (0.00387992803556), **0.00000000002005** over #7835 and **0.00000000002100** over #7831. The admitted ordinary BIT saving is **0.003879928046143**, which is 0.000000000000011 below the unchanged signed binary crossing [0.003879928046154, 0.003879928046155].

The binary word, rational word, 480-factor mixed cutoff schedule (bases 10 and 11), productive floor 16, strict moment trial 0.003879928046148 and its separation surplus are all unchanged from #7830. Only the two finite exponent losses change.

| Schedule | Uniform loss e | Delayed-cover loss d | log₂ N | q criterion | Admitted BIT | Conditional κ |
| --- | ---: | ---: | ---: | --- | ---: | ---: |
| #7830 | 2.5·10⁻¹² | 8·10⁻¹² | 1,285,200,000,000,000 | q > 2⁴⁵N⁵ | 0.003879928035646 | 0.00387992803556 |
| This package | 10⁻¹⁵ | 2·10⁻¹⁵ | 3,954,000,000,000,000,000 | q > 2⁶⁰N⁵ | 0.003879928046143 | **0.00387992804606** |

## Why each change is admissible

**Uniform loss.** The uniform carrier needs (H+1)^64 < 2^{eH} with the same θ = 13/15, log power 64 and ambient 134^480. #7830 already checks this exactly at e = 10⁻¹⁵ and H = 10¹⁵·3954 as its "uniform sensitivity at a separately priced loss". The preceding grid point fails there too. This package uses that carrier as the actual one. The θ and ambient inequalities do not depend on H.

**Delayed-cover loss.** The retained bridge (`research/p104-shared-native-helper-splits/retained/compiler/bit-audit/retained/DELAYED-COVER-BRIDGE.md` §7) says to choose q large enough that the fallback surcharge fits the slack. It states that a sufficiently large prime avoiding the frozen catalogue exists because the precompiled program is finite. The surcharge is at most 64N⁵/q. With q > 2⁶⁰N⁵ it is at most 64/2⁶⁰ ≈ 5.6·10⁻¹⁷, which is below d/4 = 5·10⁻¹⁶. The check N^d = 2^{Hd} ≥ 1 + d/2 holds with Hd = 7908. A larger q only enlarges the fixed finite constants (|GL_N(F_q)|, q^{N²(w−1)}). The bridge and the stock argument absorb those constants at a fresh eventual threshold, as they already do for the enormous N.

**Stock stages.** The same five ρ = 1/250 stages from the seed 0.00385248 converge to covered = C − e − d = 0.003879928046145. The fifth stage admits 0.003879928046143 and rejects ORDINARY + 2·10⁻¹⁵.

## Reproduce

The package lives at `research/p104-tight-losses`. Use CPython 3.12, the same pinned public inputs as #7830, and a fresh output directory each time.

~~~sh
python3.12 -IB verify.py --work inputs --out replay --fetch
cmp BIT.json replay/BIT.json && cmp AUDIT.json replay/AUDIT.json && cmp RESULT.json replay/RESULT.json
python3.12 -IB review/independent.py --work inputs --out independent-replay --producer replay
~~~

Both commands passed on 2026-11-20. The first printed `PASS_COMPLETE_CONDITIONAL_APPLICATION 0.00387992804606` after the full native, scalar, ordinary and 54 strict + 4 functional outer checks. The second printed `PASS_INDEPENDENT_MIXED_CUTOFF_CONDITIONAL_APPLICATION 0.00387992804606`.

The changes to #7830's scripts are listed in `tight-losses.diff`:
- the loss constants and carrier;
- the q exponent;
- generic (not hard-coded) stage and overclaim checks;
- the headline gain strings;
- the reviewer's producer pins;
- the reviewer's control "uniform-loss substitution fails at q > 2⁴⁵N⁵", which is specific to the old q and was dropped.

## Scope and what remains

This is still conditional on the five premises: native_all_columns, owned_erasure, compiler, precision_tape and analytic_recovery. It squeezes out essentially all remaining finite slack on the fixed BIT profile, since it sits only 1.1·10⁻¹⁴ below the raw crossing. Further gains need a stronger signed binary profile, together with a matching rational profile.

## Credit

This package adapts #7830 (Clear1nsight, with OpenAI Codex), the #7831 cutoff rebalance (Dugongue) and the #7835 grade-14 successor (Rohan Arun). Their words, callers and verifiers are reused unchanged apart from the parameters above. The retained NOTICE and LICENSE (Apache-2.0) apply.
