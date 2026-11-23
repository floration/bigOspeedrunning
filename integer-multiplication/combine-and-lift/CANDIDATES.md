# Combine upstream lines and lift cap: results (2026-11-23)

Both packages pass CrocSwap's official runner (`python3.12 -IB scripts/research_package.py --package research/<name>`, all 7 scopes, `outcome=completed`) on a local commit over #8073 head cf4c4b7e. Logs: `*-official-replay.log`.

| Package | Label | κ | vs best open PR |
|---|---|---:|---|
| p104-floor-retune-child-tariff | as intended (finite-factor, under the #8072 cap) | 0.003898228176674 | +4.559e-9 over #8076 (0.003898223617430) |
| p104-height-lift-20bit | gamed (cap lifted to log2 C 428149040; 20-bit heights) | 0.003898348448843 | +8.449e-9 over #8078 (0.00389834) |

Idea #96 (merge #8056's unequal packets into the #8057/#8073 line): not built. #8056 works on the single-type supplier; on the weighted two-type line all transport levers together are capped at <=1.5e-8 (research.md section 9.2), and the packet change only shaves split mass, worth far less. This thread merged the line that mattered instead: #8076's child tariff.

Scripts: combo.py (model), lift.py (gamed allocation), build_combo.py / build_lift.py (package builders; final placeholder values were filled from the regenerate mode).

## Update (05:40 UTC): full stack with #8082's reserve drop
- As intended (under the cap): the stack gives exactly #8082's κ 0.003898230327195. The Gaussian side binds at G = 2^19, the top of #8073's stated domain, so the tariff only frees clock (minimal h2 falls 101729 → 89635). No new package.
- Gamed: `p104-stack-height-lift-20bit`, κ **0.003898348449639** (+8.450e-9 over #8078, +7.96e-13 over p104-height-lift-20bit). Official runner: all 7 scopes pass.
