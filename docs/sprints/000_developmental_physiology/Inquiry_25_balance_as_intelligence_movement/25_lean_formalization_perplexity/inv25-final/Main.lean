import Core
import Models
import Verification

/-!
# Main.lean — thin entrypoint (25j required package layout)

This executable's only job is to sanity-check, at ordinary Lean
elaboration time (i.e. every time `lake build` runs), that the finite
witnesses central to the Investigation 25 verdict are genuinely
inhabited/provable — not merely that the files parse. It is a redundant,
belt-and-suspenders check on top of `Verification.lean`'s `#print axioms`
audit (which is the actual evidence of record); this file adds nothing
new to the mathematical content of the package.
-/

open Inv25

def main : IO Unit := do
  -- M1: base signature admits at least one lawful, non-degenerate reading.
  let _ : Nonempty (Adm25Witness M1.sig M1.doctrine M1.Movement.skilled) := ⟨M1.skilledAdm⟩
  -- M2: post-contact retry that preserves the trace is admissible.
  let _ : Nonempty (Adm25Witness M2.sig2 M2.doctrine2 M2.Movement.retryTraceVisible) :=
    ⟨M2.retryTraceVisibleAdm⟩
  -- M3: the full bridge diagram (all material + decorative relations present)
  -- is admissible, and so is the independent LB-sourced local movement.
  let _ : Nonempty (Adm25Witness M3.sig3 M3.doctrine3 M3.Movement.bridgeMove) := ⟨M3.bridgeMoveAdm⟩
  let _ : Nonempty (Adm25Witness M3.sig3 M3.doctrine3 M3.Movement.localMoveB) := ⟨M3.localMoveBAdm⟩
  -- Correction B/C sanity check: `skilled` has a genuine (non-vacuous) redesigned
  -- `HarmonicAlign` witness under the new Adm25/ReadApp/material-extension signature.
  let _ : Nonempty (HarmonicAlign M1.sig M1.doctrine M1.Movement.skilled) :=
    ⟨M1.m1_skilled_harmonic_align_holds⟩
  -- Correction A sanity check: `tStuck` crosses the typed threshold (Stuck), while
  -- `tLow` remains a genuine SNSLike-but-not-Stuck countermodel (no converse holds).
  let _ : Nonempty (Stuck M1.sig M1.Trajectory.tStuck) := ⟨M1.T_adv15_tStuck.1⟩
  let _ : Nonempty (SNSLike M1.sig M1.Trajectory.tLow) := ⟨M1.T_adv15_tLow.1⟩
  IO.println "Investigation 25 — Lean 4 formalization (final faithfulness patch): \
    Core + M1 + M2 + M3 loaded; T01-T25 + N01-N07 theorem inventory type-checked; \
    central Adm25Witness / HarmonicAlign / Stuck instances confirmed inhabited. \
    See Verification.lean / 25_final_build_and_axiom_report.md for the \
    #print axioms / sorryAx audit."
