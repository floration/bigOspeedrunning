# Binary polynomial multiplication over F2: slack in the 1/1302 claim

Source read: arpcs/finite-field-polynomial-multiplication, papers/03-best-binary/versions/0.2.1
(main.tex Lemma "Finite all-input unit", Lemma "Finite uniform column body", end of proof of Theorem 1; COST_LEDGER.txt).

## How the exponent is produced
1. A fixed finite native program (built from E8 root lines) has productive rank profile
   T = {8:18910, 22:240, 36:240} and paid profile P = {1:27445, 2:10400, 3:2200, 4:4340, 5:7760, 6:8120, 7:765}.
2. The only quantitative input is the strict moment inequality  sum_r P_r r^s0 < sum_k T_k k^s0.
   The paper uses s0 = 1 - 1/1300.
3. The recursion gives movement cost O(V (u+1)^t) for any rational t > s0 (via z, d, t = z + d^3).
4. Final bound: O(n L^g polylog L) with g = 1/(2 - t); polylog absorbed by any exponent above g.
   The paper takes u0 = 1300/1301 so g < 1/(2-u0) = 1301/1302, i.e. kappa = 1/1302.

So kappa -> (1 - s*)/(2 - s*), where s* is the root of the moment inequality.

## The slack
- s* = 0.99922966972..., i.e. 1 - 1/1298.1445. The paper's 1 - 1/1300 is not tight.
- Even with s0 = 1 - 1/1300 kept, choosing u0 closer to s0 gives kappa up to just under 1/1301 (paper rounds to 1/1302).
- Limit with the same finite unit: kappa -> 1/1299.1445.

## Proposed parameter change (kappa = 1/1300)
- s0 = 1 - 2/2597 (= 1 - 1/1298.5 > s*). Moment margin target - paid = +0.0328 (100-digit check, check_moment.py);
  paper's margin at 1 - 1/1300 is +0.171 (matches their certificate's numerator gap after the 36^s0 factor).
- u0 = 1 - 1/1299, z = (s0+u0)/2, d = 1 - z. u0 - z = 1/6747006, d^3 = 4.56e-10 < u0 - z, so t = z + d^3 < u0.
- g = 1/(2-t) < 1/(2-u0) = 1299/1300. Bound: O(n log^{1299/1300} n), kappa = 1/1300.
Edits needed: main.tex lines 184, 477-481; appendices/movement.tex line 31; finite-unit.tex line 207 (h = log(36/r)*2/2597)
and rerun checks/probes/finite_certificate.cpp with the new s0 (it is hard-coded there).

## Final push (kappa = 2/2599 = 1/1299.5)
- s0 = 1 - 5/6491 (= 1 - 1/1298.2, just above s* = 1 - 1/1298.1445). Interval lower bound of target - paid: +0.00513
  (check_moment_interval.py: correctly rounded 60-digit Decimal ln/exp with ulp slack on every step).
- u0 = 1 - 2/2597. u0 - z = 8.90e-8 > d^3 = 4.57e-10, so t = z + d^3 < u0.
- g < 1/(2-u0) = 2597/2599. Bound: O(n log^{2597/2599} n), kappa = 2/2599 = 1/1299.5.
- s0 = 1 - 10/12981 fails (margin -0.0041), so ~1/1299.14 is the hard ceiling of this finite unit.
- Same edit locations as above; finite-unit.tex h becomes log(36/r)*5/6491.

## Caveats
- This only inherits the paper's proof. That proof is AI-assisted, unreviewed, and "Claimed" on the board; if it is wrong, so is this.
- I did not rerun the C++ probes (Windows-guarded); the moment check here is high-precision decimal, not directed-rounding rational.
- Real progress beyond ~1/1299 needs a new finite unit with a better T/P profile (combinatorial search), which is hard.
