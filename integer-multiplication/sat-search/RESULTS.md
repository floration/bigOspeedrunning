# Gaussian (complex) word: computer search for cheaper rewrites

By floration. Builds on CrocSwap PR #8027 (rational/complex word), #8073/#8057 (Gaussian supplier) and SYLforge's PR #8052 (K7 move elimination idea for the binary word).

Target: a complex word with exact kappa above our best 0.003898224460300.

## Result: no improvement found (all local rewrite classes give 0)

Word rebuilt from #8027 (`build_final.py`, hash matches APPLICATION.json rational_word; 5,674 moves, 1,291 fields).
Model root reproduces rational_raw = 0.00389848144654994 (dM/dc ~ -1.0137e6).

| Search | Tests | Hits after exact check |
|---|---|---|
| Pure relays (a move that only forwards one value) | all moves | 0 |
| Per-chart forward/backward rank redundancy (`backred.py`) | all charts | 0 |
| Reroute a move to another chart, with cascade deletion (`reroute.py`) | 18,468 | 0 |
| Two-hop bypass a->b->c replaced by a->c (`bypass.py`) | 7,026 triples | 0 |
| Generalized bypass, small target charts (`bypass3.py` + `post3.py`) | 1,069 raw | 0 (all create cycles) |
| Generalized bypass, large target charts incl. chart 127 (`bypass5.py`) | 59,958 donor tests on 2,937 edges | 0 |

Value per change (for reference): 1+1->2 merge +2.56e-7; 2+2 merge +5.1e-7; one grade-1 unit per call +4.7e-5.

## Why
Per route, transfer count = rank(sum u z^T) (forward value x adjoint), and matrix flow is conserved per chart. Every single-move or two-hop rewrite therefore has to move rank between routes; none of the local ones do. Paid linear per call 9,639 vs direct lower bound 9,527 (gap 112), but the gap is forced by main pairs whose start chart is not nested in the final chart.

## Next step (not done)
Window re-synthesis: ILP/SAT over a chart neighbourhood that re-chooses routes jointly (rank moved between routes). Plugging a new word into the Gaussian supplier (#8057 pipeline) is also substantial work.

## Window ILP (CP-SAT), Nov 23 follow-up

Model: split each chart's activity into independent pieces (1,350 pieces, 428 fixed because they hold inputs/outputs; 5,674 moves as edges). Re-choose the chart of every free piece jointly, subject to strict nesting on every move. Objective: exact concave cost sum of g^(1-c), the same as the κ margin. Circuit topology stays fixed, so the map is unchanged by construction. Tools: `cgraph.py`, `win.py`, `rtwin.py` (OR-tools CP-SAT).

| Window | Pieces | Result |
|---|---|---|
| 922 BFS windows of 8 pieces | 8 each | all OPTIMAL, gain 0 |
| Round trips + 1 hop | 119 | OPTIMAL, gain 0 |
| Round trips + 3 hops | 776 | OPTIMAL, gain 0 |
| Whole word | 922 (all free) | OPTIMAL, gain 0 |

So the current chart assignment is **globally optimal** for this circuit.

Level-cut bound (`cut.py`): moves crossing each dimension level are rank-tight except for 8 downward round trips that span levels 1..7. That is 8 down plus 8 extra up per level, 112 units in total, and it is exactly the known gap. These carry the 104 "main" dependencies whose input chart is not nested in the output chart; they are bundled about 13 per chain, which already beats routing each one through chart 3 (2 units each, 208 total).

Remaining lever: change the network code itself (the bundling of the 104 non-nested dependencies), not the routes. That is a new design problem, not a local search.
