/-
Copyright (c) 2026 Anthropic, PBC. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
SPDX-License-Identifier: Apache-2.0

APSP in time O(n^2.99556071322466) on the word-RAM of `EndStatement`.

This is the proof of Li Xuanji (GitHub: ldct), bigospeedrun/verifier pull request #6, commit
a6e77d9a122e9e3137afbf2e1ac310b2032447f4, which extends the Lean development of anthropics/formal-math
(3sum-apsp, commit e1a4e6508154ea59f030480661590a9fe3018011, by Anthropic, after the paper of Josh Alman
and Virginia Vassilevska Williams, arXiv:2610.06783) with deterministic prime-by-prime filtering,
two-digit residue lifting and batched tensor slots. This refinement follows the sharper numerical certificate by Hrishik Sai Bojnal (fringewidth),
which proved exponent 2.99556085. It changes the executable rational parameters to c = 20,
θ = 155816/1377219 and σ = 136966 / 4074237, tightens the proved logarithm enclosures, and adjusts
all concrete word/time bounds and asymptotic absorptions to prove exponent 2.9955607647814.

Parameter and numerical refinement by Joshua Wharton, QFEX <joshua@qfex.com>, 2026.
Re-balanced parameters θ = 155816/1377219, σ = 136966/4074237 and tightened absorption margins
(exponent 2.995560766 -> 2.9955607647814) by Hrishik Sai Bojnal (fringewidth), with Claude Opus 5.5, 2026.
Fractional tensor depth c = 502/25 (L = ⌈c m⌉, computed by the existing ceilMul procedure 72), with
θ = 225677/1996332 and σ = 152980/4570079 (exponent 2.9955607647814 -> 2.9955607132692), by usbTypeF,
with Claude, 2026; see MODIFICATIONS.md.
Retune to c = 1807/90, θ = 290417/2568962, σ = 576969/17234159 with absorption margins tightened
100x (exponent 2.9955607132692 -> 2.99556071322466), by usbTypeF, with Claude, 2026; see MODIFICATIONS.md.
All inherited credits, license notices, algorithms, and canonical EndStatement definitions
are retained. The proof targets the complete fixed-width word-RAM EndStatement, not only a
numerical feasibility ledger.
-/
import Submission.EndStatement
import Submission.ThreeSumApsp.Batch.Final

theorem Race.bound : EndStatement.APSP.SolvedInTime ((149778035661233 : Rat) / 50000000000000) := by
  have h : ((149778035661233 : Rat) / 50000000000000) = (2.99556071322466 : ℚ) := by norm_num
  rw [h]
  exact apsp_299556071322466
