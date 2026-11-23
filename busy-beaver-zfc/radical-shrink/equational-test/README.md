# Feasibility test: equational (Tarski–Givant style) checker

**By floration (q).** Builds on Vladimir Reshetnikov's K215 source language and resolver (ProveIt, MIT-0). Code written with Claude.

**Verdict: the route is ruled out. It doesn't beat 215, let alone 100.**

## What was built

- `rmc.py`: a small structured compiler into K215's exact source language (CI/CD/CB/CC/CH binary trees, at most 9 registers). It also has an exact simulator of the source semantics, copied from ProveIt's `graph_intervals` resolver, and the same distinct-subtree count that K215's state count tracks.
- `checker2.py`: a working equational proof search in that language. It treats each number M as a proof, with these commands:
  - axiom instance (Tarski's ten relation-algebra axioms with arbitrary term parameters)
  - symmetry
  - transitivity
  - congruence for complement, converse, union and composition

  It halts when the stack top has the form t = complement(t), which forces 1 = 0. Every pairing goes through one shared register triple to maximize sharing. (`checker.py` is the first, unoptimized draft.)
- Tests:
  - `test2.py` compares the compiled program against a Python reference on 629 random proofs (stack contents and the halt decision). 629 agree, 0 disagree.
  - Adding a false axiom x = complement(x) makes the search halt from a blank start, as it should.

## Distinct-subtree counts (the measure K215's 215 states track)

| Part | Distinct subtrees |
|---|---|
| Engine: decoding, stack, symmetry, transitivity, congruences, contradiction test | 264 |
| Tarski's ten relation-algebra axioms | 137 |
| **Total, before adding any set-theory axioms** | **401** |
| For comparison, all of K215 (engine, first-order logic and ZFC axioms) | 202 |
| K215's axiom and formula section alone | 73 used nowhere else |

## Why this kills the route

The engine is a first draft, and upstream's engine had months of tuning, so the 264 could plausibly be halved. The axioms are the decisive part. **The ten relation-algebra axioms alone cost 137 subtrees, about twice what K215 pays for its entire logic plus all of ZFC.** Removing variables (the point of Tarski–Givant) only moves the cost into a long list of equational axioms. The set-theory axioms of the variable-free system would then come on top.

Even with generous savings, the estimate is about 130 + 110 + 50 or more, roughly 290, which is above 215:

- engine halved to about 130
- relation-algebra axioms cut to about 110 with a single-axiom Boolean basis
- at least 50 for the set-theory axioms

So K215's Meredith-style single axiom plus quantifier rules is the more compact logic. A sub-215 machine is more likely to come from shrinking K215's own core than from replacing its logic.
