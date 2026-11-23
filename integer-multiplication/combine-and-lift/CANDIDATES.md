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

## Update (06:20 UTC): lifted five-shortcut word
`p104-shortcut-word-lift-20bit`, κ **0.003899574328473** (gamed, enlarged budget). It is +1.226e-6 over #8086. The ordinary side binds at the 20-bit ceiling with heights (62186, 986008, 1048575) and G = 66037. The official runner passes all 7 scopes.

## Update (07:05 UTC): 25-bit + η = 1/256 on the shortcut word
New upstream record #8087 (0.003898460000505, 25-bit, old word) is below our #8088. Stacking #8081/#8087's 25-bit setup and #8084's η = 1/256 (q < η < 1/250) on the #8088 package:
- `p104-shortcut-word-eta-25bit`, κ **0.003900826718768** (gamed). Heights (1991687, 31554614, 33554431), G = 198448, log2 C 21515894540. +1.2524e-6 over #8088, +2.3667e-6 over #8087. Official runner: all 7 scopes pass.
- `p104-shortcut-word-eta-25bit-4stage` (checker's 4-stage idea): κ **0.003900826966095**, heights (125432, 1988432, 31439868, 33554431), G = 198527, log2 C 21518289843. +2.47e-10 over the 3-stage. Official runner: all 7 scopes pass. Checker verified both (minimal G, locally optimal heights; a 5th stage is worth <~1e-12).
Note: build_25.py holds placeholders; the final values were edited in place in the packages.

## Update (08:35 UTC): 27-bit heights, 5 ordinary stages
`p104-shortcut-word-eta-27bit-5stage`, κ **0.003900857267786** (gamed). +3.03e-8 over #8090. Heights (31808, 502922, 7951907, 125730703, 134217727), G = 208653, log2 C 85945126846. Setup lemma extension: SETUP-27BIT.md. Official runner: all 7 scopes pass (calendar ~264 s).
The ceiling for this line is the binary trial c_B = 0.003900867368; 28 bits gives 0.003900862317916 but its calendar takes ~522 s against the runner's 600 s cap, so it was not proposed. Builder: build_bits.py <bits> <stages> then finish_bits.sh <name>.
