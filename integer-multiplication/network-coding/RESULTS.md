# Network/index coding delivery trick (idea #75) — negative result

By floration. Builds on the integer-multiplication words of the CrocSwap contributors: the binary K7 word (strong-bit-k7) and the #8027 complex/Gaussian word with its BANK-FACTORS rebuild.

**Goal:** find one paid delivery (MOVE) that can be removed or made cheaper because a combined value can serve several consumers, with targets unchanged. If one existed, κ would rise above our best of 0.003898224460300.

**Outcome:** there is no such deletion on either word, so κ is unchanged.

## Tests
| Test | Word | Result |
|---|---|---|
| Unused dimensions per chart (`excess.py`, `bexcess.py`) | binary K7 | 0 charts with unused dimensions |
| Unused dimensions per chart | complex #8027 | 14 charts have 1 unused dimension. The senders share no side information (`side.py`, `kern.py`). |
| Broadcast hub, gauge (`gauge.py`) | complex, chart 599 | fails because y·z = 0 |
| Re-source a delivery from a lower-grade nested chart (`bres2.py`) | binary K7 | 1,224 hits with time ignored, 0 time-correct |
| Re-source a delivery from a lower-grade nested chart (`cres_fast.py`, then `cres_time.py`) | complex final word (5,674 moves) | 2,654 hits with time ignored, 0 time-correct (the source value isn't available at the source chart before the delivery's first use) |

The binary gain lever (`alloc_cb.py`, +5.87e-9) does nothing here because κ is bound by the Gaussian side at G = 2^19.

Both words are therefore tight against one-hop network coding. A gain would need a multi-hop or time-reordered schedule, which is a separate search.
