# Bounded prime gaps (H1 <= 182): difficulty and findings

**Difficulty: hard.** No easy improvement exists.

## Current best
- 182 (Claimed): GPT-6 Astra, prompted by Romyar Sharifi. Proves DHL[39,2] (any admissible 39-tuple has infinitely many translates with 2 primes), then applies a 39-tuple of diameter 182.
  The Lean repo (romyar1/prime-gaps-lean) is conditional: 262 numerical integral inequalities, three Deligne-type finite-field bounds and a Type III local Fourier proposition are premises.
- 186 (Claimed): OpenAI PrimeGaps186, DHL[40,2] with a 40-tuple of diameter 186; Lean with 3 axioms.
- 246 is the best Lean Verified (Polymath8b value, DHL[50,2]).

## What the 182 approach does
Maynard-Tao sieve with a 39-coordinate spline weight (726 coefficients, 393k grid cells), enlarged support,
Harman-sieve and Type III distribution estimates. Positivity of the restored sieve energy is certified by 262
interval-arithmetic integrals (~1h44m on a Mac, custom FLINT build).

## Check: are the tuples optimal? Yes.
Exhaustive search (narrowest_admissible.c, sieving every prime <= k with the endpoints forced in) gives the
narrowest admissible diameters H(k):

| k | 36 | 37 | 38 | 39 | 40 | 41 | 50 |
|---|----|----|----|----|----|----|----|
| H(k) | 162 | 168 | 176 | 182 | 186 | 188 | 246 |

Sanity checks also reproduce H(10)=32, H(20)=80, H(50)=246 (Polymath8b).

So 182 and 186 already use the best possible tuples. No bound in 177..181 is reachable; the next bound
is **176**, which needs DHL[38,2], i.e. a better sieve (M_38 above the threshold under their distribution level).
That needs new analytic input or a ~1% gain in the sieve ratio, then redoing a 38-dimensional certified computation.
The 182 authors dropped from 40 to 39 with heavy new machinery, so slack at k=39 is likely thin.

## Reproduce
    gcc -O3 -march=native -o adm narrowest_admissible.c
    ./adm 39 180   # none
    ./adm 39 182   # FOUND, prints a tuple
    ./adm 38 176   # FOUND

## Second attempt (Nov 20): how much slack does the 39-dimensional sieve have?
The Lean file `formal/PhysicalRestoration182.lean` proves the normalized sieve energy is
> 65213759/10^12 ≈ 6.5e-5 (`physical_restored_energy_margin182`), cut to 3.3e-5 after the sharp-deficit
perturbation (`formal/SharpDeficitMargin182.lean`). So the criterion holds with about 0.003-0.007% to spare.

Dropping from k=39 to k=38 costs roughly a 1/k share of M_k (M_k grows like log k), i.e. ~0.7-1% of the main
term. That is ~100x more than the available slack, so re-optimizing the same trial at k=38 cannot work.
Getting 176 needs a new distribution estimate (a larger level θ / ϖ) or a structurally better sieve, which is
research work rather than a tuning fix.

## Third attempt (Nov 21): five ideas, aiming at 176

Tool: `mk_signatures.py` computes exact (rational) lower bounds for Maynard's M_k with weights
F = Σ c (1−P1)^a · Π P_λj (power sums, signatures with parts ≥ 2). Validated: reproduces Maynard's
M_105 = 4.002069 (`mk_p1p2.py 105 11`). Run: `python3 mk_signatures.py <k> <radial deg> <signature deg>`.

The 182 trial uses 11 angular signatures, all of degree ≤ 6 ([], [2], …, [2,2,2]) × 22 radial splines.
Radial flexibility is saturated (k=38: radial deg 8 → 12 changes M by 0.003%). Angular degree is not:

| k (width) | sig ≤ 6 | sig ≤ 8 |
|---|---|---|
| 39 (182) | 3.58899 | 3.64083 |
| 38 (176) | 3.57273 | 3.62274 |
| 37 (168) | — | 3.60393 |
| 36 (162) | — | 3.58437 |
| 35 (158) | — | 3.56400 |

Reference level = the 182 trial's family at k=39 (3.58899).

1. **Novel (richer angular signatures): promising lead, not a bound.** With degree-8 signatures, k=38 beats the
   reference by 0.94% (needed: >0), and k=37 by 0.42%. k=36 falls 0.13% short (degree 10 might close it).
   Caveat: this is the plain simplex M_k model; the 182 criterion adds enlarged support, a cap and Type III/
   Harman losses that also depend on F. The comparison assumes the gain transfers proportionally.
   Turning it into a bound needs re-optimizing their 3-component spline trial at k=38 with 22 signatures and
   recertifying the integrals (their optimizer is not in the repo; certification took ~1h44m at 11 signatures).
2. **Crazy (exclude only the endpoint pair → 180):** needs the sieve surplus to exceed the probability that the
   two primes are exactly the endpoints, heuristically ~(1/k)² ≈ 7e-4 of the main term, vs the 182 margin of
   6.5e-5. ~10× short with their trial, and it would only give 180. Dropped.
3. **Borrowed (spectral ceiling, Polymath's M_k ≤ k/(k−1)·log k):** k/(k−1)log k < 3.589 for k ≤ 32, so better
   weights alone can never go below k=33 (width 152) at this distribution level. Weights alone: floor ~152.
4. **Reverse (from 176 back to the distribution level):** with the existing family, k=38 needs θ larger by a
   factor 3.58899/3.57273 = 1.0046, i.e. Δϖ ≈ 0.0011 in θ = 1/2 + 2ϖ. With degree-8 signatures it needs nothing.
5. **Breaking (non-symmetric weights for one specific tuple):** no gain possible. The leading-order functional
   is S_k-symmetric with positive kernels, so the top eigenfunction is symmetric (Perron–Frobenius), and the
   main term does not depend on the tuple.

## Max gamified vs as intended
- **As intended:** no new bound. Best lead is the degree-8 signature trial at k=38 (176), possibly k=37 (168).
- **Max gamified:** the Lean statement (`verifier/challenges/prime-gaps/Statement.lean`,
  `∃ᶠ m in atTop, p(m+1) − p(m) ≤ B`) is tight; I found no loophole. The tuple parameters are already optimal.
  The only "game" is that the board ranks unchecked Claimed entries (the #1, 182, is conditional). One could
  post "176, conditional on numerical premises" from the model computation alone, but those premises are not
  certified, so it would be an unsupported claim. I did not make one.
