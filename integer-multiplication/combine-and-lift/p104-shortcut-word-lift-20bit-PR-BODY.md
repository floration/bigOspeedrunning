<!-- claude-projects-attribution: {"github_login":"usbTypeF"} -->
_Requested by **q** · [project thread](https://claude.ai/code/project/chan_01Dizo8KtkYR6xjqySQ1webD?thread=cmsg_01Dizo8KtkYR6xjqySQ1webD3nTy8BMZEYZr3t6hmhX6ZC)_

Main author: floration.

## Change and mathematical scope

**Label: enlarged budget (resource tradeoff).** This PR lifts the self-imposed recurring clock cap 318292011, as [#8078](https://github.com/CrocSwap/integer-mult-bounds/pull/8078) and [#8086](https://github.com/CrocSwap/integer-mult-bounds/pull/8086) do. It is not a claim under the fixed #8072 budget. Every height fits the 20 bits that the inherited source setup census admits. The five framework assumptions are unchanged.

The package stacks these on #8073 (head `cf4c4b7ea`):
- **A new Gaussian word.** Five exact chart-3 relay shortcuts on #8027's rational word. Each replaces X: a→b and Y: b→c (nested charts, Y reads X) with one direct D: a→c, and re-encodes the chart-3 inputs. That gives 5,669 transfers, and the full forward map over Q equals the base map on all 1,291 outputs. Endpoints, charts and targets are unchanged. Paid grades shift 2,3 → 4,5 at a fixed linear sum. The raw Gaussian root rises from 0.00389848144655 to 0.00390146621942. The re-certified two-type trial is `17158764376/2^42`, and the Gaussian debit is `1039776/2^23`. The word is `w5669_shortcut5.json.gz` (sha256 `6ef741c3…`, graph digest `ed3bea71…`), installed through a pinned `strong_complex.py` patch.
- **The ordinary side from #8086.** It combines the floor retune L = 4474 with the (186/25)/L suffix ([#8080](https://github.com/CrocSwap/integer-mult-bounds/pull/8080)), the #8076 child tariff 2401/1024 and its clock charges, and no ordinary 256/255 ([#8082](https://github.com/CrocSwap/integer-mult-bounds/pull/8082)). The ordinary debit is `1420718/2^20`.

With the new word the Gaussian side no longer binds, and the ordinary side binds at its 20-bit ceiling. The prefix rule `cut[i−1]+2 < h[i]` (activation.binary_entries) with h3 = 2^20 − 1 fixes h2 for each h1, and h1 is optimised over that. The profile is ordinary `(62186, 986008, 1048575)` with minimal Gaussian `G = 66037`. Conditional **κ = 0.003899574328473** is the 15-digit floor of the ordinary rate minus 5·10^-18.

| Comparator | κ | Gain |
|---|---:|---:|
| #8086 (enlarged budget, old word) | 0.003898348449639 | +1.2259e-6 |
| #8078 (enlarged budget on #8072) | 0.00389834 | +1.2343e-6 |
| #8073 | 0.003898219753506 | +1.3546e-6 |

Resources: complete recurring log₂ C `685495960` (the cap was 318292011), entry conversion `973` bits, terminal log₂ B `670966217`, binary cuts `(62500, 1048572, 2097211)`, funding floors `(1047843, 66037)`, maximum native height `1048575`.

## Validation

```sh
python3.12 -IB scripts/research_package.py --package research/p104-shortcut-word-lift-20bit
```

This prints `PASS_REGISTERED_RESEARCH_PACKAGE research/p104-shortcut-word-lift-20bit outcome=completed`, with all seven scopes passing on Linux under CPython 3.12.
- **Price:** the exact invoice matches `RESULT.json`, and `upper^(2^20) < 2^1420718`. Every parent ordinary booking fails the allowance. The new word's directed Gaussian factor is below `2^(1039776/2^23)`, and the next lower tick fails.
- **Calendar:** a scaled check after #8078's `check_scaled.py`. It covers funding on both sides, 54 strict and 4 functional signed inequalities, stock and prefix bounds, and direct and compiled stage seams. It also checks that h2 is the largest the prefix rule allows and that neighbouring h1 choices are lower. Negative controls reject: h2−1, h3−1, G−1, the capped profile at the new rate, the inherited cap, the outer margin removed, a prefix at the previous cut, and the recurring bound minus one.
- **Raw, exterior, nested and product** run the actual five-shortcut word: typed raw paid counts 282336 / 281328, transport 105216 / 563662. **Setup** checks that every height has at most 20 bits.

Not covered by the executable checks:
- The reserve-drop reading inherited from #8082.
- The shortcut word's rational application (scalar compiler, chart-3 ordinary work and depth). That is argued in the companion capped package `research/p104-k7-shortcut-word`.

A 21-bit or larger height would need a fresh setup certificate. This PR does not claim one.

## Credit

floration (main author) supplied the shortcut word, its exact-map checks and this package, building on #8080, #8082 and #8086. Ali Romman supplied #8027's rational word and edits, and the producer and caller ([#8042](https://github.com/CrocSwap/integer-mult-bounds/pull/8042), [#8055](https://github.com/CrocSwap/integer-mult-bounds/pull/8055), [#8057](https://github.com/CrocSwap/integer-mult-bounds/pull/8057)). SYLforge supplied the K7 word ([#8052](https://github.com/CrocSwap/integer-mult-bounds/pull/8052)). OpenAI Codex supplied the child tariff ([#8076](https://github.com/CrocSwap/integer-mult-bounds/pull/8076)) and the suffix, debit and allocation chain, with ToikY and campaign contributors ([#8064](https://github.com/CrocSwap/integer-mult-bounds/pull/8064)–[#8073](https://github.com/CrocSwap/integer-mult-bounds/pull/8073)). Clear1nsight supplied the enlarged-budget method and scaled check ([#8078](https://github.com/CrocSwap/integer-mult-bounds/pull/8078)). Source licenses are retained. Claude (Anthropic) materially assisted the construction and replay.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_011AGrDgRzL3mAN4UjwkDKq7
