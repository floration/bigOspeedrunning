# Combined retune at the largest 20-bit Gaussian height (enlarged budget)

Label: **gamed** (resource tradeoff). It lifts the self-imposed recurring clock cap 318292011 that #8068–#8076 optimise under. κ is an asymptotic exponent and does not see the constant C, and every finite-loss lemma it uses holds for all heights ≥ 1024 / 8192. The same kind of step is already open upstream as [#8078](https://github.com/CrocSwap/integer-mult-bounds/pull/8078) (Clear1nsight, κ 0.00389834 on #8072). By the repo's hill-climbing rule it is "more digits of the same root".

Base: `research/p104-floor-retune-child-tariff` (κ 0.003898228176674). Change: the Gaussian height is set to the largest value the inherited source setup census allows, `G = 2^20 − 1 = 1048575` (every height must fit 20 bits; a 21-bit height needs a fresh setup certificate). The ordinary heights are the smallest that fund the Gaussian rate: `(8192, 36373, 572500)`.

- Conditional **κ = 0.003898348448843** (the 15-digit floor of `17145637307/2^42 − (64939/2^19)/1048575 − 5·10^-18`).
- +8.449e-9 over #8078 (0.00389834), +1.287e-7 over #8073, +1.203e-7 over the capped combined package.
- Complete recurring log₂ C `428149040` (was 318291940), entry conversion `747` bits, log₂ B `197460937`, binary cuts `(8290, 44727, 617291)`, maximum native height `1048575`, funding floors `(540133, 1048575)`.

```sh
python3.12 -IB scripts/research_package.py --package research/p104-height-lift-20bit
```

Controls (all rejected): `h2−1`, `h3−1`, `G−1`, the capped combined profile at the new rate, the inherited cap 318292011, the outer ordinary margin removed, a prefix height at the previous cut, and the recurring bound minus one. A Cauchy relaxation (as in #8078) shows no smaller ordinary height sum funds the target.

Beyond 20 bits (not built, needs a new setup census): 21 bits gives about 0.0038984075, 24 bits 0.0038984592, and the limit is the Gaussian trial 0.0038984666.
