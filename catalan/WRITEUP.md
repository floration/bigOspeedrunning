# Catalan's constant (irrationality measure)

**Our value:** μ(G) ≤ 269.7816584 (gamed). As intended: 269.78167
**Listed record:** 270 (S. Litsey)
**Status:** Claimed.

## What changed
Every margin in Litsey's terminal theorem is pushed to the limit Lean can still certify. The as-intended version keeps ordinary margins.

## How to check it
Both Lean patches build clean against slitsey/catalan-irrationality-measure @ 3797a70c on Lean v4.35.0-rc2, using only the standard axioms. The verifier pins v4.34.1, so this is Claimed, not Lean Verified.

## Credit
S. Litsey, for the whole proof. This folder builds directly on their work. Full repository: https://github.com/floration/bigOspeedrunning
