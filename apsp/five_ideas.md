# APSP: five ideas (2026-11-21)

Every number below comes from the balanced exponent of the Lean-verified batched proof: α = max(3 − 2Γσ, 2 + (2B − ½)σ, 3 − (1 − 2q)σ). The scripts are ideas.py and rev.py in the scratchpad, and their logic is restated here.

1. **Novel (finer rational c):** c = 1807/90 gives a limit of 2.995560713224602. That is 4.2e-11 better than c = 502/25 (2.995560713266682). It is the same Lean patch with new numbers, so it is cheap once the 502/25 build passes.
2. **Crazy (drop the c > 10 condition):** No gain. The optimum is c ≈ 20.08, so that condition never binds. Pruned encodings (A_pruned) are worse than B, because they add ½cH(1/c).
3. **Borrowed (fast matrix multiplication for the counting oracle):** Count the residues as polynomials in Z[x]/(x^p − 1) and multiply the blocks together. The cost is n^{1+ω(1,σ,1)}·n^{o(1)}, and since ω(1,σ,1) = 2 for σ below about 0.32, that is n^3. No gain.
4. **Reverse (work back from the bottleneck):** All three costs are balanced, and the encoding base 3 in N₀ = 3^{L−m} is the lever. With base 2.9 the exponent would be 2.99542; with base 2.5 it would be 2.99466. A smaller-alphabet encoding lemma is therefore the most valuable new lemma for this method. None exists yet.
5. **Breaking (modulus p much smaller than block size s):** In the current method the modulus has to be about as large as the block, because of a union bound over the s third vertices in each filter round. If p ≈ s^{1/2} worked, the exponent would be about 2.956 (with c and θ re-optimized, c at the c > 10 boundary). That would need a new filtering lemma, and I haven't found one. It's hypothetical.

## Max gamified vs as intended

| Track | Max gamified | As intended |
|---|---|---|
| Claimed | **2.99294791870930934671834**: the same construction, with parameters pushed to 24 digits (R = 10^40, exact checker passes, files in claimed-witness-maxgamed/). That is 9.07e-14 below the record and about 2e-24 above the construction's limit. | No real improvement. 2.9929479187094 stands; anything below it is digit-shaving. |
| Lean Verified | About **2.99556071322463**, from c = 1807/90 plus margins shrunk from 1e-12 to 1e-14. The proof is not written; it would be a retune of the 502/25 patch. | **2.9955607132692** (c = 502/25), which is the real structural change: making the tensor depth fractional, worth 5.2e-8. The build is running. Further digits only shave about 4e-11. |
