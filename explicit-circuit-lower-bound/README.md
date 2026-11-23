# Explicit circuit lower bound (B2): no new bound

Board: https://bigospeedrun.com/other/explicit-circuit-lower-bound. The current record is 4n − O(log n) (Mishra–Santhanam, ECCC TR26-260 rev. 1, Claimed).

- **As intended:** no improvement. A reweighting LP over the paper's cases shows c ≤ g1 + g4 = 4 (`analysis.md`, `scripts/`).
- **Max gamified:** no legal gain. The board fixes the B2 basis and single-output functions, and only the o(n) term can be tuned.
- `3sat-17-7-preprint-review.md` reviews Yianni–Allahyar's (17/7)n bound for a 3-SAT encoding. It appears correct for that encoding, but 17/7 < 4, so it does not beat the board. Its embedding cannot carry an affine disperser, so 3-SAT does not inherit 4n this way.

Nothing here is independently reviewed.
