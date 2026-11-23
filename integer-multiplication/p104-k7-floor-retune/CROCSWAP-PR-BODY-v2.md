## Change and mathematical scope

This is a parameter construction on top of #8073: one changed charged finite factor and a re-funded literal profile, with the same signed words and the same five framework assumptions. It is a κ improvement under the #8072 clock cap, not a scalar saving: conditional **κ = 0.003898224460300**. That is `2353397/500000000000000` (+4.707e-9) above #8073's installed 0.003898219753506, and above #8073's exact fixed-booking ceiling `523210198560303585338978849681/134217728000000000000000000000000`.

The ordinary K7 floor `L` was fixed at 18960 in #8067. That is the minimiser of `c·log L + (s+10)/L`, and so of the complete ordinary factor, for the old 64/L suffix allowance (`L* ≈ (s+10)/c ≈ 18970`). #8073 proved the suffix `10Σk/(tΨ) < 7.43958 < 8`, but kept `L = 18960`. Ψ depends only on the 24 directed edge cells, so that bound does not depend on `L`. This package books the suffix at `186/25`, moves the floor to the new optimum `L = 4474`, and books the ordinary debit on a 2^-20 grid. The directed complete factor
`(47/20)(256/255)(4097/4096)(1028/1024)(1024·134·L)^c(1+s/L+δ)/((1−10/L)(1−δ)^3) < 2.573602304817903473`
supports `D = 1430037/2^20`, where #8073 used `11204/8192 = 1434112/2^20`. Under the unchanged cap `1731+320Σb+220G ≤ 318292011`, the funded profile is ordinary `(8192,110461,524288)` with Gaussian `G = 511587`. The complete recurring log₂ C is 318291991, the entry conversion uses 518 bits, and the maximum native height stays 524288.

Remaining obligations are unchanged from #8073: native_all_columns, owned_erasure, compiler, precision_tape and analytic_recovery.

## Task and overlap

Base: #8073 head `cf4c4b7ea`. The package is `research/p104-k7-floor-retune` (a copy of #8073's package plus the changes above), and it reuses `peer8057.tar.gz` at #8057 `cbe847a9`. Task card: `scalar-to-moment`, scope **refined**: one retuned all-size K7 floor with the (186/25)/L suffix charge, and one literal capped profile. Nearest overlap is #8067 (floor 18960), #8072 (capped allocation) and #8073 (8/L suffix). The added value is that the floor is re-optimised for the sharper suffix, which neither PR did.

## Validation

```sh
python3.12 -IB scripts/research_package.py --package research/p104-k7-floor-retune
```

This prints `PASS_REGISTERED_RESEARCH_PACKAGE research/p104-k7-floor-retune outcome=completed`. All seven scopes (price, calendar, raw, exterior, nested, product, setup) pass on Linux with CPython 3.12.

- **Price:** the exact invoice matches `RESULT.json`, and `upper^(2^20) < 2^1430037` holds exactly. Independent 192-bit directed roots give a reserve above 7.58e-7.
- **Debit controls:** the finer grid point `1430036/2^20` fails, and #8073's own (18960, 8/L) booking fails the new allowance, while still passing its old reserve 2.776e-5.
- **Calendar:** all five ordinary recipes open with `level_floor = 4474` through `Recipe.open`. The all-size floor hypotheses hold: `L^t ≈ 4331 > 1024`, `(1−10/L)Ψ > 1`, the 77-power delay bound holds, and the first columns are (4466, 4468). The fringe ceiling is 7.439580927 < 186/25. A full two-port fixture on the occupied K7 grade (49,64) gives 76380 opens, 456 returned paid prefixes and 38003660528 paid singletons.
- **Allocation:** #8072's and #8073's exact family ceilings are re-derived. Both adjacent Gaussian heights fail: G−1 keeps the same ranks and is underfunded on the Gaussian side, and G+1 forces b₂=110460 and overfunds the ordinary side. The new profile also fails under #8073's debit. Two- and four-stage allocations under the same cap are lower. These are finite checks; the integer-optimum argument is #8073's tangent-slope argument, applied unchanged.
- The raw, exterior, nested, product and setup scopes are unchanged checks, re-run at the new floor and profile.

## Credit

**Main author: floration.** This is a collaboration that builds on the upstream work credited below.

This builds directly on #8073 (Campaign contributor, with OpenAI Codex), and through it on:
- Ali Romman's #8042 suffix argument, #8057 signed producer and caller, and #8055 setup proof;
- SYLforge's #8052 K7 word;
- #8059, #8063 and #8064 (Gaussian factor and band), #8066 and #8067 (ordinary price and K7 floor), and #8068 to #8072 (allocation method and bookings).

Source licenses and notices are retained. floration found and built the floor retune, the pricing changes and the replay, with substantial assistance from Claude (Anthropic). An independent Claude session rechecked the debit and allocation in its own exact-rational code.

## Open next questions

The ordinary debit now sits near the directed optimum of this factor, so the Gaussian finite factor and the clock cap bind the allocation. A larger step needs a charged change to the Gaussian word itself: a legal rewrite that removes paid mass at fixed target ranks, with the full signed invoice and a literal witness.
