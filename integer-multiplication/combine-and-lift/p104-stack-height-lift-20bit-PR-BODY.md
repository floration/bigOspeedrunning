<!-- claude-projects-attribution: {"github_login":"usbTypeF"} -->
_Requested by **q** · [project thread](https://claude.ai/code/project/chan_01Dizo8KtkYR6xjqySQ1webD?thread=cmsg_01Dizo8KtkYR6xjqySQ1webD3nTy8BMZEYZr3t6hmhX6ZC)_

## Change and mathematical scope

**Label: enlarged-budget (resource tradeoff).** This lifts the self-imposed recurring clock cap 318292011 that #8068–#8082 optimise under, in the same way as [#8078](https://github.com/CrocSwap/integer-mult-bounds/pull/8078) (Clear1nsight). It is not a claim under the fixed #8072 budget. The signed words, the five framework assumptions and every finite-loss lemma (stated for H ≥ 1024 Gaussian and H ≥ 8192 ordinary) are unchanged. Every height fits the 20 bits the inherited source setup census admits.

The package stacks four open lines on #8073 (head `cf4c4b7ea`):
- the K7 floor retune L = 4474 with the (186/25)/L suffix ([#8080](https://github.com/CrocSwap/integer-mult-bounds/pull/8080));
- the ordinary child tariff 2401/1024 with its clock charges (entry series 17 → 22, terminal +3 per stage) ([#8076](https://github.com/CrocSwap/integer-mult-bounds/pull/8076));
- the ordinary 256/255 reserve drop and the Gaussian booking 1039017/2^23 ([#8082](https://github.com/CrocSwap/integer-mult-bounds/pull/8082));
- the enlarged budget, set to the largest 20-bit Gaussian height G = 2^20 − 1 = 1048575 (as in #8078, which used G = 978582 on #8072).

The directed ordinary factor `(2401/1024)(4097/4096)(1028/1024)(1024·134·L)^c(1+s/L+δ)/((1−10/L)(1−δ)^3) < 2.557796525567700799` funds the ordinary debit `1420718/2^20` (the grid point below fails). The minimal funded ordinary heights are `(8192, 36093, 570250)`. The Gaussian rate binds, and the result is conditional **κ = 0.003898348449639**, the 15-digit floor of `17145637307/2^42 − (1039017/2^23)/1048575 − 5·10^-18`.

| Comparator | κ | Gain |
|---|---:|---:|
| #8078 (enlarged budget on #8072) | 0.00389834 | +8.450e-9 |
| #8082 (fixed #8072 cap) | 0.003898230327195 | +1.181e-7 |
| #8073 | 0.003898219753506 | +1.287e-7 |

Resources: complete recurring log₂ C `427339440` (cap was 318292011), entry conversion `746` bits, terminal log₂ B `196651337`, binary cuts `(8290, 44447, 614761)`, funding floors `(537891, 1048575)`, maximum native height `1048575`.

Remaining obligations are unchanged: native_all_columns, owned_erasure, compiler, precision_tape and analytic_recovery.

## Validation

```sh
python3.12 -IB scripts/research_package.py --package research/p104-stack-height-lift-20bit
```

This prints `PASS_REGISTERED_RESEARCH_PACKAGE research/p104-stack-height-lift-20bit outcome=completed`. All seven scopes (price, calendar, raw, exterior, nested, product, setup) pass on Linux with CPython 3.12.

- **Price:** the exact invoice matches `RESULT.json`, and `upper^(2^20) < 2^1420718` holds exactly. Every parent ordinary booking (#8073, #8076, #8080, #8082, and the tariff stack with 256/255) fails the stacked allowance.
- **Calendar:** in place of the capped-allocation check, a scaled check after #8078's `check_scaled.py`. It checks funding on both sides, the 54 strict and 4 functional signed inequalities, the stock and prefix bounds, the direct and compiled stage seams at the new cuts, and a Cauchy relaxation showing no smaller ordinary height sum funds the target. It rejects these negative controls: `h2−1`, `h3−1`, `G−1`, the capped #8082 profile at the new rate, the inherited cap 318292011, the outer ordinary margin removed, a prefix height at the previous cut, and the recurring bound minus one.
- Raw, exterior, nested, product and setup are re-run at the new profile. The setup census checks that all entry and terminal heights have at most 20 bits.

The executable checks don't cover the reserve-drop step inherited from #8082, which is a reading of #8042's written proof. Please review it there. A 21-bit or larger height would need a fresh setup certificate. It is not claimed here.

## Credit

Clear1nsight ([#8078](https://github.com/CrocSwap/integer-mult-bounds/pull/8078)) supplied the enlarged-budget method and scaled check. OpenAI Codex ([#8076](https://github.com/CrocSwap/integer-mult-bounds/pull/8076), and with ToikY/Campaign contributors [#8064](https://github.com/CrocSwap/integer-mult-bounds/pull/8064)–[#8073](https://github.com/CrocSwap/integer-mult-bounds/pull/8073)) supplied the child tariff, the suffix envelope, the debits and the capped allocation. The predecessor packages [#8080](https://github.com/CrocSwap/integer-mult-bounds/pull/8080) and [#8082](https://github.com/CrocSwap/integer-mult-bounds/pull/8082) are floration's. Ali Romman supplied the words and producer ([#8042](https://github.com/CrocSwap/integer-mult-bounds/pull/8042), [#8055](https://github.com/CrocSwap/integer-mult-bounds/pull/8055), [#8057](https://github.com/CrocSwap/integer-mult-bounds/pull/8057)), and SYLforge supplied the K7 word ([#8052](https://github.com/CrocSwap/integer-mult-bounds/pull/8052)). Source licenses are retained. Claude (Anthropic) materially assisted the construction and replay.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_011AGrDgRzL3mAN4UjwkDKq7
