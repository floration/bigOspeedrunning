# Gamed Lean build: c = 1807/90 (runs after the 502/25 build passes)

Start from the passing 502/25 tree and change:
- c: 502/25 → 1807/90. In `oL`, use (1807*m + 89)/90; in G20, a = 1807 and b = 90; use levels31 with a = 1807, b = 90. Then c − 1 = 1717/90 and rhoC = 810/1717, so 1/(1−ρ) = 1717/907 < 1.9.
- θ: 225677/1996332 → 290417/2568962. σ: 152980/4570079 → 576969/17234159.
- Γ > 0.066301113347407, q < 0.433698886652977, B = (1717/90)·ln3/ln4 < 15.118781187434585. Numbers.lean is pre-generated here and checked with exact rationals.
- cast_N0_le: 90 j ≤ 1717 m + 89.
- Margins, tightened 100×: in one_add_le_exp/absorb, 10^12 → 10^14 (so 10^24 → 10^28 everywhere). The y-slack 0.0000000000001 → 0.000000000000001.
- Exponent chain: absorb hypothesis 2.995560713224637, absorb output …657, oracle …658, filter …659, final 2.99556071322466 = 149778035661233/50000000000000 (for Race.bound and manifest.json).
- Worst balanced term is 2.9955607132246239 (boxes), with eps = 1e-15, so the margin is 1.3e-14.
