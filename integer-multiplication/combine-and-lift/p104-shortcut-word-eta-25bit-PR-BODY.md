<!-- claude-projects-attribution: {"github_login":"usbTypeF"} -->
_Requested by **q** · [project thread](https://claude.ai/code/project/chan_01Dizo8KtkYR6xjqySQ1webD?thread=cmsg_01Dizo8KtkYR6xjqySQ1webD3nTy8BMZEYZr3t6hmhX6ZC)_

Main author: floration.

## Change and mathematical scope

**Label: enlarged budget (resource tradeoff), gamed.** Like [#8088](https://github.com/CrocSwap/integer-mult-bounds/pull/8088), this lifts the self-imposed recurring clock cap 318292011. It is not a claim under the fixed #8072 budget. The five framework assumptions are unchanged.

It stacks two upstream ideas on #8088's five-shortcut Gaussian word and #8086's ordinary side (debit `1420718/2^20`, floor L = 4474, suffix 186/25, #8076 child tariff, no ordinary 256/255):
- **25-bit heights** from [#8081](https://github.com/CrocSwap/integer-mult-bounds/pull/8081) / [#8087](https://github.com/CrocSwap/integer-mult-bounds/pull/8087). The native setup bound moves from 20 to 25 bits with the scalar-encoding asserts `92(2^25−1) < 2^32`, `1024(2^25−1)+3 < 2^35` and `2·2048(2^25+1)+7·2^24 < 2^40`.
- **The η lift** from [#8084](https://github.com/CrocSwap/integer-mult-bounds/pull/8084): q < η < 1/250 with η = 1/256. At 25 bits the old 39/10000 clamp would cap the rate near 0.0039, so the lift is what lets the extra height pay. The stage seam now cuts components at `log_width·η` and rounds widths to multiples of lcm(10000, 250, 256) = 160000.

The ordinary side binds. With h3 = 2^25 − 1, the prefix rule `cut[i−1]+2 < h[i]` fixes h2 for each h1, and h1 is optimised over that. The profile is ordinary `(1991687, 31554614, 33554431)` with minimal Gaussian `G = 198448`. Conditional **κ = 0.003900826718768** is the 15-digit floor of the ordinary rate minus 5·10^-18.

| Comparator | κ | Gain |
|---|---:|---:|
| #8088 (20-bit, shortcut word) | 0.003899574328473 | +1.2524e-6 |
| #8087 (25-bit, old word) | 0.003898460000505 | +2.3667e-6 |
| #8073 | 0.003898219753506 | +2.6070e-6 |

Resources: complete recurring log₂ C `21515894540` (the cap was 318292011), entry conversion `30345` bits, terminal log₂ B `21472234377`, binary cuts `(1999750, 33554428, 67108923)`, funding floors `(33331518, 198448)`, maximum native height `33554431`.

## Validation

```sh
python3.12 -IB scripts/research_package.py --package research/p104-shortcut-word-eta-25bit
```

This prints `PASS_REGISTERED_RESEARCH_PACKAGE research/p104-shortcut-word-eta-25bit outcome=completed`, with all seven scopes passing on Linux under CPython 3.12.
- **Price:** the exact invoice matches `RESULT.json`.
- **Calendar:** the scaled check from #8088, at 25 bits. It covers funding on both sides, 54 strict and 4 functional signed inequalities, stock and prefix bounds, η bounds, and direct and compiled stage seams. Negative controls reject: h3−1, h1−166 and h2−167 (the install is the 15-digit floor of the rate, so smaller drops stay funded), h2+1 (breaks the prefix rule), G−1, the capped #8088 profile at the new rate, the inherited cap, the old 39/10000 η, the outer margin removed, a prefix at the previous cut, and the recurring bound minus one.
- **Raw, exterior, nested and product** run the five-shortcut word. **Setup** checks every height has at most 25 bits.

Not covered by the executable checks: the reserve-drop reading inherited from #8082, the shortcut word's rational application (argued in `research/p104-k7-shortcut-word`), and #8084's η proof, which is inherited, not re-proved. A 26-bit height would need a fresh setup certificate.

## Credit

floration (main author) supplied the shortcut word, the stack and this package, building on #8080, #8082, #8086 and #8088. Clear1nsight supplied the 25-bit setup (#8081), the η lift (#8084) and the enlarged-budget method ([#8078](https://github.com/CrocSwap/integer-mult-bounds/pull/8078)). OpenAI Codex supplied the 25-bit signed profile (#8087), the child tariff (#8076) and the suffix, debit and allocation chain, with ToikY and campaign contributors ([#8064](https://github.com/CrocSwap/integer-mult-bounds/pull/8064)–[#8073](https://github.com/CrocSwap/integer-mult-bounds/pull/8073)). Ali Romman supplied #8027's rational word and the producer and caller (#8042, #8055, #8057). SYLforge supplied the K7 word (#8052). Source licenses are retained. Claude (Anthropic) materially assisted the construction and replay.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_011AGrDgRzL3mAN4UjwkDKq7
