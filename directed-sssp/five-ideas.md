# Directed SSSP: five ideas (2026-11-21)

Current Lean Verified (LV) rows: C-HD n log^{11/12} n at m ≤ n log^{3/4} n; Dijkstra n log² n at
m ≤ n log n; our built rows (DijkstraRowB/C) n log^{1+b} n at n log^b n (b ≤ 2) and n^a log n at n^a.

## 1. Novel: density-adaptive d-ary heap (d ≈ m/n)
Dijkstra with a d-ary heap costs O(m log_d n + n d log_d n).
- At m = n log n, d = log n: n log² n / log log n → tuple (1, 2, -1), strictly below LV (1, 2, 0).
- At m = n^a (1 < a < 2), d = n^(a-1): O(m/(a-1) + n^a/(a-1)) = O(n^a), so linear.
Status: not built. It needs darkhipo's 4k-line binary-heap proof generalised to d children. Medium effort.

## 2. Crazy: look for a loophole in the cost model
I checked Frontier/CostModel.lean. Every statement and test costs 1. Allocation of k cells costs k+1.
Words must stay below cap = (n+m+2)^(e+1) (`fit`), and reals only support +, compare and load.
Expression sizes are program constants. No free computation, word packing or reading of cap.
Status: dead end, no loophole.

## 3. Borrowed (graph theory): Frederickson degree reduction, then C-HD
Split vertices into a constant-degree graph with n' = O(m), m' = O(m), then run C-HD.
Tchd(O(m), O(m)) = O(m log^{2/3} n), which is the STOC'25 shape.
Status: valid, but strictly worse than idea 5. Dropped.

## 4. Reverse: start from the target T = D (linear time)
Fibonacci heaps reach T = D only for D ≥ n log n. Which rows can reach linear time without them?
Answer: every polynomial density n^a with 1 < a < 2, via idea 1's d-ary heap.
That improves the built n^a log n rows to n^a.
Status: same build as idea 1.

## 5. Breaking: pad the graph with isolated vertices so C-HD's own theorem applies
The C-HD Lean theorem bounds the cost on EVERY graph with m ≤ n·F(n), F(n) = ⌊⌊log₂ n⌋^{3/4}⌋,
by Tchd(n, m) = n + m + m log(m/(n+1)+2) + m^{1/3} (n log(n+2))^{2/3}.
Add k isolated vertices, with n' = n + ⌊m / F(n)⌋ + 1. Then m ≤ n'·F(n'), so the C-HD branch runs.
Distances to the original n vertices are unchanged.
For m ≤ n·log^b n with b ≥ 3/4 (and m ≤ n², so log n' = O(log n)):
- n' = O(n log^{b-3/4} n)
- m log(m/n'+2) = O(m log log n), which is lower order
- m^{1/3}(n' log n')^{2/3} = O((n log^b)^{1/3} · (n log^{b+1/4})^{2/3}) = O(n log^{b+1/6} n)

So T = O(n log^{b+1/6} n), i.e. O(m log^{1/6} n). At b = 3/4 this equals C-HD's 11/12, a continuity check.

| density D | LV today | padding (on paper) |
|---|---|---|
| n log^{7/8} n | n log^{15/8} n (ours) | n log^{25/24} n |
| n log n | n log² n | **n log^{7/6} n** |
| n log² n | n log³ n (ours) | n log^{13/6} n |
| n^a, 1<a<2 | n^a log n (ours) | n^a log^{1/6} n (d-ary gives n^a) |

### Lean plan, splicing via Dispatch.BodySpec / InitLike (CHD/Dispatch.lean, CHD/L6/Body.lean)
`body_spec` gives C-HD's body from ANY state that `Agree`s with `init0 e ps G' s` outside the
scratch registers [px, pa, py, pr, pq]. `initState` depends on n only through register "n" and
`cap`, and the input arrays src/dst/w are the same for G'. So the wrapper is:
`compute F(n) in scratch regs; wset "n" (n + m / pr + 1); chdBody core; copy reach/dist back to length n`.
The pieces needed:
1. A cap-monotonicity lemma for `exec`/`evalW`: a run that succeeds under cap c also succeeds with
   the same result under any c' ≥ c. `fit` is the only use of cap. The wrapper needs wordExp ≥ 321,
   because (n'+m+2)^161 ≤ (n+m+2)^322.
2. The padded graph G' (Fin.castLE on src/dst) and the lemma G'.dist s v = G.dist s v for v < n.
3. An O(n) output copy so that wlen "reach" = vlen "dist" = n.
4. Arithmetic: Tchd(n', m) ≤ C·n·log^{b+1/6} n, using floors and log log x ≤ 6 (log x)^{1/6}.
5. A dispatch on m ≤ n² to keep the polynomial fallback (Bellman–Ford above that).
Estimate: roughly 1.5k–3k lines. Nothing in it is research. It is plumbing on top of a proven theorem.
