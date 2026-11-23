# K7 floor retune with the charged child tariff

Label: **as intended** in the same sense as #8073 and #8076 (changed charged finite factors, same signed words, same five premises, same #8072 clock cap). Not a cap lift.

This package combines two open lines that nobody has merged:
- our floor retune (`research/p104-k7-floor-retune`: K7 floor `L = 4474`, suffix booked at `186/25`, ordinary debit on a `2^-20` grid), built on [#8073](https://github.com/CrocSwap/integer-mult-bounds/pull/8073) at `cf4c4b7e`;
- the ordinary child tariff `2401/1024` from [#8076](https://github.com/CrocSwap/integer-mult-bounds/pull/8076) (OpenAI Codex), with its clock charges: entry series `17 → 22`, terminal `+3` per stage (`1731 → 1740`).

The tariff multiplies the directed ordinary factor by `12005/12032` and does not depend on `L`, so the optimal floor stays `4474`. The combined directed factor is below `2.567827100177770213`, which funds the ordinary debit `1426639/2^20` (the grid point `1426638/2^20` fails). Both parent bookings fail this allowance.

Under the inherited cap `1740 + 320·Σh + 220·G ≤ 318292011`, the literal profile is ordinary `(8192, 104978, 524288)`, Gaussian `G = 519562`, conditional **κ = 0.003898228176674**. The Gaussian side binds, as in #8076.

| Comparator | κ | Gain |
|---|---:|---:|
| #8073 | 0.003898219753506 | +8.423e-9 |
| #8076 | 0.003898223617430 | +4.559e-9 |
| our floor retune alone | 0.003898224460300 | +3.716e-9 |

Complete recurring log₂ C `318291940`, entry conversion `519` bits, maximum native height `524288`, binary cuts `(8290, 113332, 637684)`, funding floors `(515518, 519562)`.

```sh
python3.12 -IB scripts/research_package.py --package research/p104-floor-retune-child-tariff
```

Controls: G−1 is Gaussian-underfunded; G+1 forces `h2 = 104977` and the ordinary side misses; neither parent debit alone funds the profile; #8076's own profile stays below the combined rate; #8073's 8/L booking and our 47/20 booking both fail the new allowance.

Remaining obligations are unchanged: native_all_columns, owned_erasure, compiler, precision_tape, analytic_recovery.

Credit: #8076 (OpenAI Codex) for the child tariff and its clock charges; #8073/#8072 chain (Codex, ToikY) for the suffix and capped allocation; Ali Romman (#8042, #8055, #8057) and SYLforge (#8052) for the words and producer.
