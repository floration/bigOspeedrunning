# Haldane gap: γ_L > 0.151707 via a sharper tail invariant

**Result (conditional on the same premises as amachino v1.7):** for the periodic spin-one Heisenberg chain at J = 1, the ground state is unique and

    γ_L > 151707/1000000 = 0.151707   for every integer L ≥ 24

(in particular for every even L ≥ 2304, the board's domain). This improves the listed 0.1515 (amachino/haldane-gap-refinement v1.7, commit `15909bdc`).

The certificate is a change to the tail argument of `verify_quarter_refinement.py` only. Thermal tables, filters, polynomial certificates, the seed, the ten recurrence rows, the short lengths and the finite intervals are all unchanged upstream inputs and code. The negative control `TARGET=151708/1000000` fails at the tail exponential comparison.

## Files

- `verify_quarter_refinement.py`: drop-in replacement for the upstream file at `15909bdc`.
- `tail18.patch`: unified diff against the upstream file (about 30 changed lines).
- `quarter_refinement_0151707.json`: the output receipt (384 named exact checks).

## Reproduce

```sh
git clone https://github.com/amachino/haldane-gap-refinement && cd haldane-gap-refinement
git checkout 15909bdc15e947795b6fba946008dd8530bb3477
patch verify_quarter_refinement.py < tail18.patch        # or copy the file over
python3 verify_quarter_refinement.py                     # PASS: 384 exact checks (about 25 s)
TARGET=151708/1000000 python3 verify_quarter_refinement.py   # negative control: fails
```

The `TARGET` environment variable defaults to 151707/1000000. `make integrity` will report the changed hash of this one file. The other `make check` certificates are untouched.

## Why the old tail lost rate

v1.7 ends the recurrence at row 9 (n₀ = 21504, b₀ = 12544) with defects p (spatial) and q (thermal), then switches to the v1.3 invariant p^{3/2} ≤ w, q ≤ w, w₊ = 6w². That invariant freezes the rate at −log(6w₀)/b₀ ≈ 0.15162. The coupled update itself behaves like q₊ ≈ 2q². Upstream rows confirm it: −(log q_k + log 2)/b_k = 0.1517074 at rows 8 and 9 alike. So the factor 6, which comes from √27 in propagating p^{3/2}, wastes log 3 / 12544 ≈ 0.0000876 of rate. Adding recurrence rows only recovers this slowly; 11 rows certify just 0.15165.

## The sharpened tail lemma

Fix σ = 73/100, λ = 10⁻⁷, W = 10⁻⁸⁰⁰, C = 2 + 10⁻³⁰⁰, B = 3/2 + 10⁻⁷⁰. At an even reference length n and inverse temperature b, consider the invariant

    p ≤ λ w^σ,   q ≤ w,   0 < w ≤ W,

where p bounds 1 − S(n,b) and q bounds 1 − T(2n,b).

**Propagation.** Use Lemma (Rounded update) with p₊ := λ(Cw²)^σ and q₊ := Cw². This needs f(a) ≤ p₊ and f(1 − (1−q)²(1−p₊)) ≤ q₊, with f(x) = x²/(2(1−x)²) increasing.
- a = 1 − (1−p)²(1−q) ≤ 2p + q ≤ w^σ(2λ + w^{1−σ}) =: z. Then f(z) = w^{2σ}(2λ + w^{1−σ})²/(2(1−z)²). Every w-dependent factor increases with w, because 1−σ > 0. So f(a) ≤ λC^σ w^{2σ} follows from the exact check (2λ + W^{1−σ})² ≤ 2(1 − 2λW^σ − W)² · λ · (8/5), together with 8/5 ≤ C^σ (checked as (8/5)¹⁰⁰ ≤ C⁷³).
- 1 − (1−q)²(1−p₊) ≤ 2q + p₊ ≤ w(2 + λC^σ w^{2σ−1}) =: z′, where 2σ − 1 > 0. Using C^σ ≤ 3, f(z′) ≤ Cw² follows from (2 + 3λW^{2σ−1})² ≤ 2(1 − 2W − 3λW^{2σ})² C.
- Since Cw² ≤ CW·w ≤ w ≤ W, the invariant holds again at (2n, 2b) with w₊ = Cw².

**Purity on [3n/2, 3n].** Follow the v1.3 proof (paper §"An asymmetric invariant for the infinite tail") verbatim with the new bounds. With R_b(L) ≤ d(p)^{3/2}, R_{2b}(L) ≤ d(a)^{3/2}, d(z) ≤ z for z ≤ 1/3, and leading contribution ≥ g^{L/(2n)} ≥ g^{3/2} ≥ 1 − (3/2)(q + p₊) (L ≤ 3n, Bernoulli):

    T(L,b) ≥ 1 − (3/2)(q + p₊) − a^{3/2} − 2p^{3/2} ≥ 1 − B w.

Dividing by w, the coefficient is at most 3/2 + (9/2)λW^{2σ−1} + (2λ + W^{1−σ})W^{3σ/2−1} + 2λW^{3σ/2−1} ≤ B. This uses 3σ/2 − 1 > 0, x^{3/2} ≤ x for x ≤ 1, and λ ≤ 1. Odd L are covered exactly as in v1.3 (signed trace).

**Gap extraction.** Put w_k = C⁻¹(Cw₀)^{2^k}, n_k = n₀2^k, b_k = b₀2^k. The intervals [3n_k/2, 3n_k] cover every L ≥ 3n₀/2 = 32256. On each,

    e^{−b_k γ_L} ≤ B w_k/(1 − B w_k) ≤ (B/(C(1 − B w₀))) (Cw₀)^{2^k} ≤ (Cw₀)^{2^k} < E^{−2^k},

with E ≥ e^{b₀δ} the upstream rational Taylor bound. The exact checks are E·C·w₀ < 1 and B ≤ C(1 − Bw₀). Hence γ_L > δ = 0.151707.

**Seed.** w₀ = q from row 9 exactly. The check p¹⁰⁰ ≤ λ¹⁰⁰ w₀⁷³ is done in exact rational arithmetic, with no rounding. Upstream gives p ≈ 10^{−610.9} and q ≈ 10^{−826.8}, so p ≈ q^{0.7389}. Any σ < 0.7388 with σ > 2/3 works; σ = 0.73 leaves room for λ = 10⁻⁷.

All fractional powers of W are exact powers of ten, and the checker verifies the exponent bookkeeping (for example (10⁻⁵⁸⁴)¹⁰⁰ = W⁷³).

## Ceiling of this route

With the tail now essentially lossless (C → 2), the certified rate equals the recurrence's own limit, about 0.1517075. Extra rows add nothing. Rescanning the seed (m ∈ 20..34, t ∈ 7/4..9/4, n = 42) gave no seed better than upstream's (26, 2, 42), which the 117 moment polynomials are tuned for. Going further needs new inputs, such as a colder thermal table or higher moments with regenerated polynomial certificates. That is substantial work, and the retracted beta=13 attempt (BigO-Hunter/haldane-gap-beta13) shows the risk.

## Status

Unreviewed and conditional on the same OpenAI premises and finite inputs as v1.7. There is no Lean proof, so it would be listed as Claimed. The tail lemma above was written in this thread and has not been independently reviewed.

## Two versions of the claim

| Version | Claim | How |
|---|---|---|
| As intended | γ_L > 0.151707 for all L ≥ 24 | Default `TARGET`; a round 6-digit constant from the new tail lemma |
| Max gamified | γ_L > 0.151707452 for all L ≥ 24 | `TARGET=151707452/1000000000` passes, and ...453 fails. Receipt: `quarter_refinement_0151707452_gamified.json` |

Both are the same exact certificate; the gamified one only squeezes the last digits up to the recurrence limit −log(2q₉)/b₉ ≈ 0.1517074527. Restricting to the board domain (even L ≥ 2304) gains nothing, because the tail, not the short lengths, binds.

## Five-ideas sweep (2026-11-21, diagnostics are non-rigorous)

The certified rate is set almost entirely by the 84-site seed: −log(2q)/b is 0.1616 at the seed and settles to 0.15171 after two rows. Halving the seed's thermal defect q would give about 0.173 (diagnostic).

1. **Novel: re-seed partway up.** At row 1 or 2, take the minimum of the propagated bounds and a fresh finite-data seed. Best case +0.0000006 (m = 22 or 26 at row 1). Row 2 fails dominance. Not worth it; it would also need a new 168-site trial.
2. **Crazy: other reference lengths and temperatures.** The seed n ranged over 32–60, t over 7/4–5/2, and m over 20–38. n = 42, t = 2, m = 26 stays optimal (n = 44 gives 0.1512, n = 40 gives 0.1504, n = 60 gives 0.130).
3. **Borrowed: Christoffel / Gauss–Radau optimality** (orthogonal polynomials). Solving U⁴ v(U)ᵀ H⁻¹ v(U) = 1 for the moment Hankel matrix H reproduces the upstream caps (A 1.000798, B .43165, E .69930, V .71706). The quartic filters are already optimal for moments up to 12, so there is no slack there.
4. **Reverse: from target to inputs.** With every check disabled, the A-sector top-eigenvalue cap drives everything. A cap of 1.0006 instead of 1.0008 would give about 0.172, and 1.0004 about 0.18 (unverified diagnostics). The other three sector supports matter far less.
5. **Breaking: moments past order 12.** This breaks the assumption that thermal traces stop at L = 12. The upstream C++ engine takes 1.0 s, 5.9 s and 50 s for L = 9, 10 and 11 on 4 CPUs (about 8.5× per length). That puts L = 13 at about 1 h per twist (about 4 h for all four twists) and L = 14 at about 8.5 h per twist (about 34 h). A tighter A cap needs even moments (14, 16). It would also need regenerating the 8 filters and 117 polynomial certificates at higher degree, and checking 256-bit overflow in the engine. This is the only route found that could move the bound materially, but it is a multi-day project.
