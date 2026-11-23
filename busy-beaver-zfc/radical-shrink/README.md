# Busy Beaver ZFC: can a radical idea get far below 215 states?

**By floration (q).** Builds on Vladimir Reshetnikov's K215 machine and source (ProveIt repo, `Computability/BusyBeaver/Research/ZFC/candidate-k215`, MIT-0), which builds in turn on Andrew James Wade's compiler and the earlier work of Jeff Ketchersid, Johannes Riebel, Stefan O'Rear, and Adam Yedidia and Scott Aaronson. Analysis prepared with Claude.

**Status: analysis only. No new machine and no new record.** The board record is still K215 (215 states).

## Short answer

Nothing proven rules out a sub-100-state machine. But this study measures why no tuning or compiler trick on today's construction can get there. Under 100 needs a **new ZFC-strength refutation search whose whole description is roughly 35 to 50% shorter than today's**. That is a research program, not a search.

## What K215 actually is (measured)

K215 compiles a 9-register counter-machine program, written as a binary tree with 4,751 leaves. Identical subtrees are shared, so the tree is really a DAG with **202 distinct subtrees**. The Turing machine spends about one state per distinct subtree: 202 subtrees give 215 states. So **state count tracks the number of distinct subtrees of the source program**.

Measured with `tools/symmetry_floor.py` on `sites215.json`:

| Count of distinct subtrees | Nodes |
|---|---|
| Exact (what K215 pays for) | 202 |
| Treating subtrees that differ only by register renaming as the same | 146 |
| Ignoring control-depth arguments | 199 |
| Both | 142 |
| Tree **shape only** (every leaf identical) | **131** |

The shape-only count is a floor for this program under the one-state-per-node compilation. Even a perfect compiler that could pass every leaf's opcode and register as a parameter for free would still pay for 131 shapes, plus engine states. **So keeping this source program and improving the compiler can't reach 100.** Breaking that would need many contextual folds (one state serving several roles told apart by the tape). Upstream has managed only a few of these, each with a lot of proof work.

Where the subtrees go (`tools/subtree_census.py`). The large selector subtree at path `1101001001110101` (4,174 of the 4,751 leaves, which carries the axiom and formula construction) reaches 152 subtrees, and 73 of them are used nowhere else. The other ~130 are shared arithmetic, pairing, stack and dispatch. **Even deleting the axiom part entirely would leave about 130 nodes.** A shorter axiom list helps, but on its own it can't get below about 130.

## Information budget

From `tools/info_budget.py`. These are counting bounds, not proofs about any particular encoding.

- A 100-state, 2-symbol machine can be named in about **1,214 bits** (taking out state relabeling).
- The K215 source DAG alone takes about **1,655 bits** to name.
- The 215-state table has room for about 2,841 bits. So about 40% of K215's capacity goes to the engine and routing, not the program.

Any machine under 100 states, of any design (compiled, interpreter plus program on tape, or something stranger), must fit the whole searcher, data and engine, into about 1,200 bits. Today the program alone is about 1,650 bits. **Under 100 therefore needs a ZFC-strength consistency search that is genuinely about 2x shorter than today's.**

## The radical routes, ranked

| Route | Verdict | Why |
|---|---|---|
| 1. Same source, smarter compiler or allocator | **Can't reach 100** | Shape floor is 131 (measured above). Upstream already does this. |
| 2. Universal TM plus program written on tape (Rogozhin/Neary–Woods style, Korec register machines, Fractran) | **Worse** | The program bits still have to come from states. At about 1,650 bits that needs about 130+ writer states before any interpreter. Tag-system encodings of counter machines blow up further. |
| 3. Shorter or stronger axiom system (Tarski–Grothendieck "Tarski axiom", finitely axiomatized NBG/MK, Ackermann-style single reflection schema) | **Plausible gain, perhaps 215 to ~160–180. Not 100 on its own.** | The axiom-only part is about 73 nodes. NBG is equiconsistent with ZFC (provable in PA). TG is stronger (inaccessibles), which the board accepts only as a qualified row. |
| 4. New logic core: variable-free equational set theory (Tarski–Givant 1987), single-rule condensed detachment over combinators, or a pure-type-system checker | **The only route with a real shot at under 100. Unproven and believed only.** | It replaces quantifiers, substitution and schemas with one rule (replace equals by equals) and finitely many equations. Nobody has measured its size as a counter program. |
| 5. Diophantine equation for Con(ZFC) | **Much worse** | A polynomial for Con(ZFC) is obtained by arithmetizing a proof checker, so it inherits the checker's size and adds an enumeration of tuples plus big-integer evaluation (our assessment; no size was measured). |
| 6. Friedman-style finite combinatorics (Con(SRP)-equivalent statements) | **Historically worse** | Yedidia–Aaronson's Friedman-based machine had 7,910 states. Direct proof search (O'Rear, 748) beat it immediately, and the checker isn't simpler. |
| 7. Collatz or Antihydra-style tiny machine whose halting is *proved* equivalent to Con(ZFC) | **No known mechanism** | Small "cryptid" machines encode open problems, but nobody knows how to tie one to Con(ZFC). Any proof of the equivalence would itself have to encode proof checking. This is the only path to around 20 states, and it needs a new mathematical idea. |

## What is proven versus believed

- **Proven here (by computation, reproducible):** the subtree counts (202 / 146 / 131), the census, and the counting bounds above.
- **Model-dependent:** "131 is a floor" holds for compilers that spend one state per distinct source shape. Contextual folds can beat it locally. No upper limit on how much is proven.
- **Believed, not proven:** that route 4 can come in about 2x shorter; that under 100 is reachable at all; independence thresholds around 10–20 states (Aaronson's guess).

## Concrete next step if we pursue it

Write route 4's core (a Tarski–Givant-style equational ZF checker: term pairing, congruence, transitivity and about 20 fixed axiom equations) in K215's source language. Then measure its distinct subtrees with `tools/subtree_census.py`. That single number decides the route.

- **Kill test:** if the core alone exceeds about 120 subtrees, route 4 can't beat 100.
- **Promising:** under about 80 subtrees would justify the full compile, then the runtime proof and the equiconsistency proof. That is weeks of work, not hours.

## Reproduce

```
python3 tools/symmetry_floor.py sites215.json
python3 tools/subtree_census.py sites215.json 0 1101001001110101
python3 tools/info_budget.py
```

`sites215.json` comes from the ProveIt repo path given above (MIT-0).
