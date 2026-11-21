# Round 2: five ideas + gamified vs as-intended (binary polynomial multiplication over F2)

## Headline
Re-optimising the paper's finite unit (choice of balanced trees on the 15 orthogonal E8 frames) gives a new
rectangle partition: 3738 rectangles instead of 3782, verified exact cover of all 7560 directed orthogonal contacts.
New profiles: T={8:18690,22:240,36:240}, P={1:27325,2:9880,3:2320,4:4880,5:6560,6:8600,7:765}
(rank-mass surplus still exactly 120, as the paper's invariant requires).
Moment root s* = 1 - 1/1282.873, so kappa ceiling 1/1283.873 (was 1/1299.14 with the paper's frozen trees).

| version | s0 | u0 | kappa | bound |
|---|---|---|---|---|
| paper (board) | 1-1/1300 | 1300/1301 | 1/1302 | n log^{1301/1302} n |
| as intended, paper's unit | 1-2/2597 | 1-1/1299 | 1/1300 | clean rounding of the paper's own slack |
| as intended, new unit | 1-2/2567 | 1-1/1284 | **1/1285** | n log^{1284/1285} n, margin +0.0586 |
| max gamified, new unit | 1-10/12829 | 1-100/128295 | **20/25679 = 1/1283.95** | margin +0.0025 |
| gamified ceiling | -> s* | -> s* | -> 1/1283.87 | not attainable exactly |

Margins are interval lower bounds (final_check.py, correctly-rounded 60-digit Decimal ln/exp with ulp slack).

## Five ideas
1. Novel (WORKED): optimise trees against the true moment objective, over all 315 balanced trees per frame
   (paper: 21 "linear flags", 2-pass coordinate descent, entropy score). Coordinate descent + random restarts; best of 5 runs 1/1283.87.
   More restarts / annealing would likely shave a bit more.
2. Crazy (DEAD): feed the improved movement exponent g back into the unit as a bootstrap loop. g=1/(2-t) > t always
   (g-t=(1-t)^2/(2-t)), so iterating moves the wrong way.
3. Borrowed, generating functions (DEAD): tensor powers of the unit. The moment difference factors as (f_T-f_P)(f_T+f_P),
   so the root is unchanged. (Leech lattice instead of E8 noted, not attempted: needs a new full construction.)
4. Reverse (MAP): the rank-mass surplus is only 120 out of ~163k, so the root is very sensitive. Removing 100 paid
   rank-1 calls would give 1/708; ~36 fewer rank-1 calls -> 1/1000; ~1431 -> 1/100. Rank-1 calls are mostly rectangle
   side jumps, so fewer/larger rectangles is the lever (that is what idea 1 exploits).
5. Breaking (OPEN): the partial-bank trick is only applied at stages 4-5. Extending it to stage 3 would give ~1/1272
   (old trees), but T1..T3 do not commute with any bank projector in the given word, so it needs a new five-stage
   transvection word. Not proved. Making owned queries free would give 1/326 but breaks the cost model (invalid).

## Caveats
- Everything inherits the unreviewed, AI-assisted v0.2.1 proof. I assume (from reading Lemma 1 and Appendix A) that only the
  rectangle dimensions enter the side invoice and that the main paths/owned centres/five-stage word are tree-independent.
- The new trees include non-"linear-flag" trees; the paper's Appendix A uses linear flags. I believe any balanced tree of
  frame subsets works (only nested sub-projectors are needed), but that is my reading, not checked by the author.
- Reproduce: python3 verify.py best_unit_profile.json rects.json geom.json ; python3 final_check.py best_unit_profile.json "2/2567:1/1284:intended"
