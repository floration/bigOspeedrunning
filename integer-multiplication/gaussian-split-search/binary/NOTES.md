# Helper splits and bidirectional merges on the BINARY word: none exist (2026-11-23)

All code is our own (`*.py` here). It reads `strong-bit-k7.json.gz` (git show refs/pull/8052/head:research/p104-k7-retimed-binary/)
and #8027's `strong-bit.json.gz` (extracted as data from #8052's predecessor-8030.tar.gz) and runs no package code.
**No candidate word. Binary raw root unchanged at 0.003900867368050 (K7).**

## 1. Checker (`bchk.py`)
GF(2) replay of INIT/ADD/MOVE/SWAP/CLEAR with locality (ADD fields and MOVE source in the named frame), strict nesting of
every MOVE (frame spans of B taken mod 2, as research-tools/gf2.py does; frames contain -1 entries), outputs at their final
frames, map = (x,y)->(x,y+x) on 111 pairs + identity on 519, histograms and Decimal root.
36-call totals = 36 x native + fixed caller {paid 1,7,14..56: 444 each; targets 8,15..64: 444 each, 127: 222}.

| word | moves | paid/call | targets/call | n_paid | n_tg | raw root |
|---|---|---|---|---|---|---|
| #8027 | 2803 | {1:1348,2:1247,3:55,4:42,5:29,6:81,7:1} | {4:17,8:391} | 104,904 | 18,906 | 0.0038901152865945 (published ...594/595) |
| K7 #8052 | 2796 | {1:1341,2:1254,3:55,4:35,5:36,6:74,7:1} | {4:24,8:384} | 104,652 | 18,906 | 0.0039008673680502 (= 4391986206293/2^50 bound) |

Linear sums match the K7 ledger (paid 284,592, targets 286,098). Backward-pass adjoints reproduce every input column.

## 2. Helper split (`bscan.py`, `brelax.py`, `bprice.py`)
Helpers = the 408 non-main public fields; classes by (start, final): K7 has 12 classes (0->1: 384 helpers; ten small 0->dim4
classes; 506->1, 508->1). No main field shares a class chart pair (x's start in their own frames, y's end in their own frames).
For each class G and each frame c strictly between, W_c = span(inputs at c + values arriving at c) restricted to G-support,
U_c = span(output adjoints of transfers leaving c) restricted to G-support, timing ignored (over-count).
- **(class, chart) pairs with both W_c and U_c nonzero: 0** (K7 and #8027). So no pairing even needs testing.
  Big class: W nonzero at 261 charts, U at 102, disjoint sets.
- Relaxed version (s on any inputs starting at a, h on any outputs ending at z): 20 pairs with both, pairing 0 in all 20.
- Cross-chart (W at c1, U at c2 != c1): 610 nonzero pairings on K7 (579 on #8027) - unlike the complex word, where
  all were orthogonal. Bringing them together costs at least one extra MOVE (-9.4e-5 for rank 1) against +2.0e-6 for a split.
- Price on the 36-call K7 histogram (exact): 8->4+4 +2.0204e-6, 3+5 +1.9285e-6, 2+6 +1.6398e-6, 1+7 +1.0996e-6,
  4->2+2 +1.0127e-6, 1+3 +8.22e-7.

## 3. Bidirectional merge (`bbidir.py`, `bbidir2.py`, `bmerge.py`, `bfix.py`, `bclose.py`)
#8027 coordinates with "chart 3" -> chart 0 (dim 0, holds 516 inputs); X = 114 inputs elsewhere; GF(2) M^-1 = M.
- K7: 405 transfers have u_X=0, **every one also has z_X=0**; 1,643 have z_X=0. So there is **no (u,0)/(0,z) pattern
  pair on any link** (0 links; #8027 same). 113 links carry a u_X=0 transfer and another z_X=0 one (grade 1: 111, grade 4: 2).
- Generalised: all 669 same-link pairs (K7; 683 #8027). Merge error b1 u2^T + b2 u1^T: both terms absorbable by a chart-0
  re-encoding in 168 pairs, exactly one in 223, none in 278. For the 223, the term to cancel has u in **no** off-link
  resident span. For the 168, det(I + z1u2^T + z2u1^T) = 0 over GF(2) in all 168 (block not invertible).
- Exact: every acyclic same-link merge w = s1+s2 (573 K7, 588 #8027; 96/95 have s2 depending on d1) **drops the map's
  rank by exactly 1** (exact virtual replay). A single closure edit (add a resident combination into leaving rows at
  any chart) can restore rank only at a chart where some resident form u has u.k = 1 and some leaving adjoint has
  ell.b = 1 (k, ell = right/left kernel of the merged map). **0 of 573 (0 of 588) merges have such a chart.** The lost
  dimension is visible only at chart 0 (or only among residents that no ell-row leaves): pure one-hop couriers.
  Chart-0 closures specifically: the only leaving rows with ell.b = 1 were the merged transfer itself, which fails exactly.

## Why it's dead
In the binary word each courier from chart 0 is the sole carrier of its information, and the two spaces a split needs
never coexist at a chart. Both conditions are invariant under local recoefficienting, so only a non-local re-synthesis
(SAT/network-coding threads) could create one.
