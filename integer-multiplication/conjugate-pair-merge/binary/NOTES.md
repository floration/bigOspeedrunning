# Relay bypass ported to the binary K7 word (strong-bit-k7.json.gz, #8052): no candidates

- `parse.py` turns the register program (INIT/ADD/MOVE/SWAP/CLEAR) into a GF(2) scalar DAG. It reproduces 2,796 moves, and the per-call grades are {1:1341, 2:1254, 3:55, 4:35, 5:36, 6:74, 7:1}.
- 519 outputs are identity and 111 are pair maps. CLEARs are dirty: all 3,426 clear nonzero values, so they add no zero constraint.
- The free-encoding block is frame 0 (dim 0), which holds 516 inputs, the same role as chart 3 in the Gaussian word.
- 405 transfers carry only frame-0 data. **No frame-0-only transfer reads another one** (0 relay pairs), so the Gaussian bypass has nothing to act on. Every frame-0 courier makes one hop and is then mixed with X-data.
- Transposed version: 498 transfers influence only frame-1 outputs, and again 0 such transfers are adjacent.
- Conclusion: the binary word is a one-hop courier network, and this family is empty by construction. Binary gains need the routing gap (63 per call), as covered by the split/merge threads.
