#!/usr/bin/env python3
"""
Apply script: corner_gap Layer 5 wiring. ONE coordinated change, all or none.

Wires the validated corner_gap pipeline (already placed at soul/corner_gap/) into
the live loop, registers its imports, and documents the hooks in artifact_1 v1.3
per the Discipline 4 maintenance contract.

This is a single wire integration (not a multi-commit sequence), matching the
established apply_task_state_step2_wiring.py pattern.

Files touched
-------------
1. lib_clarity_reasoning/lib_clarity_reasoning.metta : 5 imports (deps order)
2. src/loop.metta                                    : 4 hook edits
3. docs/design/artifact_1_loop_metta_wiring_diagram.md: Layer 5 subsection

Pre-condition: the 5 validated files exist at soul/corner_gap/. This script does
NOT create them; it wires what is on disk. The graded pair (coupling_quantale_merge,
cycle_continuity_probe[_writers]) is intentionally NOT imported (off-path until
graded activates).

The corner_gap imports (dependency order: pure before writer, detector before gate)
-----------------------------------------------------------------------------------
  state_delta_writer            (pure: classify-state-delta, latest-state-delta-verdict)
  state_delta_writer_writers    (do-clear-state-delta!, populate-state-delta)
  coupling_integrity_detector   (pure: coupling-verdict, corner-confirmed, ...)
  coupling_integrity_detector_writers (populate-coupling-verdict, do-clear-coupling-status!)
  corner_gate                   (apply-corner-gate, gate-aware-results, Layer 3+4)

The four loop.metta hooks (hook-only; Patrick's structure preserved)
--------------------------------------------------------------------
Edit A  RESET (after line 102, in the $msgnew branch):
        ($_ (if $msgnew (do-clear-coupling-status!) _))
        Clears the corner streak on new human input so the gate never fires on a
        response-in-flight cycle (surface map requirement: reset precedes gate).

Edit B  GATE + FEEDBACK (at execution, line 134):
        Insert before:  ($sexpr_gated (apply-corner-gate $sexpr))
        Change in 134:  (superpose $sexpr)  ->  (superpose $sexpr_gated)
        Insert after:   ($results_final (gate-aware-results $results))
        apply-corner-gate is passthrough ($sexpr unchanged) except on a confirmed
        corner, where it returns () to force silence. gate-aware-results swaps the
        empty execution result for the feedback string so &lastresults carries it.
        metta_cmds (128-130) stays on $sexpr (mutation gate must see unfiltered list).

Edit C  CYCLE-TAIL DETECTORS (after line 136 populate-recent-action):
        ($results_nonempty (> (size-atom (collapse (superpose $sexpr_gated))) 0))
        ($results_novel (if (== (py-call (helper.safe_results_str (repr $results))) (get-state &lastresults)) False True))
        ($_ (populate-state-delta $msgnew $results_nonempty $results_novel $k))
        ($_ (populate-coupling-verdict $k))
        Ordering load-bearing: recent-action (136) -> state-delta -> coupling-verdict.

Edit D  FEEDBACK WRITE (line 165): change (repr $results) -> (repr $results_final)
        so the gated cycle's feedback (not the empty result) rides into the next
        prompt's LAST_SKILL_USE_RESULTS via the existing &lastresults pipe.

REVIEW-AND-VERIFY ITEM (Edit C booleans), flagged honestly
----------------------------------------------------------
$results_nonempty and $results_novel are DERIVED from the state_delta_writer
contract (msgnew OR (results non-empty AND results differ from prior &lastresults)),
not transcribed from the harness (which used literal booleans). They are:
  - nonempty: post-gate command list had > 0 commands (size-atom of the superposed
    $sexpr_gated). A cornered or silent cycle yields 0 -> none, as intended.
  - novel: this cycle's rendered results string differs from the prior &lastresults
    (still last cycle's value at the tail, per the contract comment).
These two lines are the dry-run review gate and a post-apply container REPL probe
target. Recommend Clarity confirms them before trusting (substrate observation logic).

Net change
----------
- lib_clarity_reasoning.metta: +9 lines (blank + 3 comment + 5 import); paren delta 0
- loop.metta: +7 lines (1 reset + 2 gate/feedback bindings + 4 cycle-tail); paren delta 0
- artifact_1: + Layer 5 subsection (markdown, no paren check)

Usage
-----
Dry-run (default):  python3 staging/apply_corner_gap_layer5_wiring.py
Apply:              python3 staging/apply_corner_gap_layer5_wiring.py --apply
Reverse (after):    python3 staging/apply_corner_gap_layer5_wiring.py --reverse --apply

Backups (forward apply only):
  lib_clarity_reasoning/lib_clarity_reasoning.metta.bak.corner_gap_l5
  src/loop.metta.bak.corner_gap_l5
  docs/design/artifact_1_loop_metta_wiring_diagram.md.bak.corner_gap_l5
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# ============================================================================
# FILE PATHS
# ============================================================================

LIB_CR_PATH = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta")
LIB_CR_BAK = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta.bak.corner_gap_l5")

LOOP_PATH = Path("src/loop.metta")
LOOP_BAK = Path("src/loop.metta.bak.corner_gap_l5")

ARTIFACT1_PATH = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md")
ARTIFACT1_BAK = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md.bak.corner_gap_l5")

CORNER_GAP_DIR = Path("soul/corner_gap")
REQUIRED_CORNER_GAP_FILES = [
    "state_delta_writer.metta",
    "state_delta_writer_writers.metta",
    "coupling_integrity_detector.metta",
    "coupling_integrity_detector_writers.metta",
    "corner_gate.metta",
]

# Indent for loop.metta let* binding lines (39 spaces, matched to live loop)
IND = " " * 39

# ============================================================================
# EDIT 1: lib_clarity_reasoning imports (dependency order)
# ============================================================================

LIB_CR_ANCHOR = "!(import! &self (library omegaclaw ./soul/cycle_classifier))"

LIB_CR_NEW_BLOCK = (
    LIB_CR_ANCHOR + "\n"
    "\n"
    ";; Corner-gap pipeline (Layer 5 wiring): forward-outcome + coupling-integrity corner\n"
    ";; detection, force-silence gate, feedback shaping. Pure-before-writer (Discipline 2),\n"
    ";; detector-before-gate dependency order.\n"
    "!(import! &self (library omegaclaw ./soul/corner_gap/state_delta_writer))\n"
    "!(import! &self (library omegaclaw ./soul/corner_gap/state_delta_writer_writers))\n"
    "!(import! &self (library omegaclaw ./soul/corner_gap/coupling_integrity_detector))\n"
    "!(import! &self (library omegaclaw ./soul/corner_gap/coupling_integrity_detector_writers))\n"
    "!(import! &self (library omegaclaw ./soul/corner_gap/corner_gate))"
)

# ============================================================================
# EDIT A: loop.metta RESET hook (after line 102)
# ============================================================================

LOOP_ANCHOR_RESET = IND + "($_ (if $msgnew (do-set-cycles-since-input! 0) (do-set-cycles-since-input! (+ 1 (current-cycles-since-input)))))"
LOOP_NEW_RESET = (
    LOOP_ANCHOR_RESET + "\n"
    + IND + "($_ (if $msgnew (do-clear-coupling-status!) _))"
)

# ============================================================================
# EDIT B: loop.metta GATE + FEEDBACK (line 134)
# ============================================================================

LOOP_ANCHOR_EXEC = IND + "($results (RESULTS: (collapse (let $s (superpose $sexpr) (COMMAND_RETURN: ($s (HandleError SINGLE_COMMAND_FORMAT_ERROR_NOTHING_WAS_DONE_PLEASE_FIX_AND_RETRY $s (catch (let $R (collapse (eval $s)) (py-call (helper.normalize_string $R)))))))))))"
LOOP_EXEC_GATED = LOOP_ANCHOR_EXEC.replace("(superpose $sexpr)", "(superpose $sexpr_gated)")
LOOP_NEW_EXEC = (
    IND + "($sexpr_gated (apply-corner-gate $sexpr))" + "\n"
    + LOOP_EXEC_GATED + "\n"
    + IND + "($results_final (gate-aware-results $results))"
)

# ============================================================================
# EDIT C: loop.metta CYCLE-TAIL detectors (after line 136)
# ============================================================================

LOOP_ANCHOR_TAIL = IND + "($_ (populate-recent-action $sexpr $msgnew $k))"
LOOP_NEW_TAIL = (
    LOOP_ANCHOR_TAIL + "\n"
    + IND + "($results_nonempty (> (size-atom (collapse (superpose $sexpr_gated))) 0))" + "\n"
    + IND + "($results_novel (if (== (py-call (helper.safe_results_str (repr $results))) (get-state &lastresults)) False True))" + "\n"
    + IND + "($_ (populate-state-delta $msgnew $results_nonempty $results_novel $k))" + "\n"
    + IND + "($_ (populate-coupling-verdict $k))"
)

# ============================================================================
# EDIT D: loop.metta FEEDBACK WRITE (line 165)
# ============================================================================

LOOP_ANCHOR_LASTRES = " " * 49 + "(change-state! &lastresults (py-call (helper.safe_results_str (repr $results)))))))"
LOOP_NEW_LASTRES = LOOP_ANCHOR_LASTRES.replace("(repr $results)", "(repr $results_final)")

# ============================================================================
# EDIT 6: artifact_1 Layer 5 subsection
# ============================================================================

ARTIFACT1_ANCHOR = "## Section 5: The aliveness latch state machine"

ARTIFACT1_NEW_SUBSECTION = (
    "### Layer 5 wiring additions (corner_gap pipeline)\n"
    "\n"
    "The corner_gap pipeline (soul/corner_gap/) detects a corner (the action-\n"
    "intention-outcome chain severed WHILE emitting), forces silence on a confirmed\n"
    "corner, and feeds the reason back through the existing results channel. Five\n"
    "files imported in dependency order (pure before writer, detector before gate):\n"
    "state_delta_writer(+writers), coupling_integrity_detector(+writers), corner_gate.\n"
    "\n"
    "**Reset hook** (live line 103, after the cycles-since-input hook at 102, in the\n"
    "$msgnew branch). Calls `(do-clear-coupling-status!)` when $msgnew. New human\n"
    "input means the context changed, so the consecutive-corner streak is cleared\n"
    "before the gate runs; the gate therefore never fires on a response-in-flight\n"
    "cycle. Per corner_gate_surface_map.md the reset must precede the gate.\n"
    "\n"
    "**Gate + feedback** (at execution, live line 135 onward). Binds\n"
    "`($sexpr_gated (apply-corner-gate $sexpr))` before execution; the execution\n"
    "`(superpose $sexpr)` becomes `(superpose $sexpr_gated)`. apply-corner-gate is\n"
    "passthrough except on a confirmed corner, where it returns `()` (force silence).\n"
    "Then `($results_final (gate-aware-results $results))` swaps the empty execution\n"
    "result for the feedback string on a gated cycle. The metta_cmds extraction\n"
    "(output intercept, lines 128-131) stays on $sexpr so the mutation gate still\n"
    "sees the unfiltered command list.\n"
    "\n"
    "**Cycle-tail detectors** (after populate-recent-action, live line 136).\n"
    "`populate-state-delta` writes this cycle's forward-outcome verdict, then\n"
    "`populate-coupling-verdict` writes the coupling verdict (order load-bearing:\n"
    "the coupling detector reads the state-delta verdict). The two loop-side\n"
    "booleans feeding state-delta are derived from the writer contract: nonempty is\n"
    "`(> (size-atom (collapse (superpose $sexpr_gated))) 0)`; novel compares this\n"
    "cycle's rendered results against the prior &lastresults (still last cycle's\n"
    "value at the tail). Both are SN cycle-posture observations; they write\n"
    "structured verdicts for the gate to consult on subsequent cycles.\n"
    "\n"
    "**Feedback write** (live line 165). `&lastresults` is written from\n"
    "`$results_final` instead of `$results`, so a gated cycle's feedback rides the\n"
    "existing pipe into the next prompt's LAST_SKILL_USE_RESULTS (read at line 45).\n"
    "No Python change; Layer 4 feedback reuses the established channel.\n"
    "\n"
    "---\n"
    "\n"
)
ARTIFACT1_NEW_AT_ANCHOR = ARTIFACT1_NEW_SUBSECTION + ARTIFACT1_ANCHOR


# ============================================================================
# HELPERS (paren counter + substring finders, per task-state precedent)
# ============================================================================

def code_aware_paren_count(text: str) -> tuple[int, int]:
    """Count parens excluding those inside string literals and line comments."""
    opens = 0
    closes = 0
    in_string = False
    escape = False
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
            elif ch == ";":
                while i < n and text[i] != "\n":
                    i += 1
                continue
            elif ch == "(":
                opens += 1
            elif ch == ")":
                closes += 1
        i += 1
    return opens, closes


def count_sub(text: str, target: str) -> int:
    count = 0
    start = 0
    while True:
        idx = text.find(target, start)
        if idx == -1:
            break
        count += 1
        start = idx + 1
    return count


# ============================================================================
# SIMULATION
# ============================================================================

def simulate_lib_forward(content: str) -> str:
    if count_sub(content, LIB_CR_ANCHOR) != 1:
        raise RuntimeError("lib forward: cycle_classifier import anchor not found exactly once.")
    if count_sub(content, "corner_gap/state_delta_writer") != 0:
        raise RuntimeError("lib forward: corner_gap imports already present.")
    return content.replace(LIB_CR_ANCHOR, LIB_CR_NEW_BLOCK, 1)


def simulate_lib_reverse(content: str) -> str:
    if count_sub(content, LIB_CR_NEW_BLOCK) != 1:
        raise RuntimeError("lib reverse: corner_gap import block not found exactly once.")
    return content.replace(LIB_CR_NEW_BLOCK, LIB_CR_ANCHOR, 1)


def simulate_loop_forward(content: str) -> str:
    for label, anchor in [
        ("RESET", LOOP_ANCHOR_RESET),
        ("EXEC", LOOP_ANCHOR_EXEC),
        ("TAIL", LOOP_ANCHOR_TAIL),
        ("LASTRES", LOOP_ANCHOR_LASTRES),
    ]:
        if count_sub(content, anchor) != 1:
            raise RuntimeError(f"loop forward: anchor {label} not found exactly once.")
    for token in ["$sexpr_gated", "do-clear-coupling-status!", "populate-state-delta",
                  "populate-coupling-verdict", "$results_final"]:
        if token in content:
            raise RuntimeError(f"loop forward: new token '{token}' already present.")
    content = content.replace(LOOP_ANCHOR_RESET, LOOP_NEW_RESET, 1)
    content = content.replace(LOOP_ANCHOR_EXEC, LOOP_NEW_EXEC, 1)
    content = content.replace(LOOP_ANCHOR_TAIL, LOOP_NEW_TAIL, 1)
    content = content.replace(LOOP_ANCHOR_LASTRES, LOOP_NEW_LASTRES, 1)
    return content


def simulate_loop_reverse(content: str) -> str:
    for label, new in [
        ("LASTRES", LOOP_NEW_LASTRES),
        ("TAIL", LOOP_NEW_TAIL),
        ("EXEC", LOOP_NEW_EXEC),
        ("RESET", LOOP_NEW_RESET),
    ]:
        if count_sub(content, new) != 1:
            raise RuntimeError(f"loop reverse: new state {label} not found exactly once.")
    content = content.replace(LOOP_NEW_LASTRES, LOOP_ANCHOR_LASTRES, 1)
    content = content.replace(LOOP_NEW_TAIL, LOOP_ANCHOR_TAIL, 1)
    content = content.replace(LOOP_NEW_EXEC, LOOP_ANCHOR_EXEC, 1)
    content = content.replace(LOOP_NEW_RESET, LOOP_ANCHOR_RESET, 1)
    return content


def simulate_artifact1_forward(content: str) -> str:
    if count_sub(content, ARTIFACT1_ANCHOR) != 1:
        raise RuntimeError("artifact1 forward: Section 5 anchor not found exactly once.")
    if "Layer 5 wiring additions (corner_gap" in content:
        raise RuntimeError("artifact1 forward: Layer 5 subsection already present.")
    return content.replace(ARTIFACT1_ANCHOR, ARTIFACT1_NEW_AT_ANCHOR, 1)


def simulate_artifact1_reverse(content: str) -> str:
    if count_sub(content, ARTIFACT1_NEW_AT_ANCHOR) != 1:
        raise RuntimeError("artifact1 reverse: Layer 5 subsection block not found exactly once.")
    return content.replace(ARTIFACT1_NEW_AT_ANCHOR, ARTIFACT1_ANCHOR, 1)


# ============================================================================
# STATE CHECKS
# ============================================================================

def lib_forward_ok(c: str) -> bool:
    return count_sub(c, LIB_CR_ANCHOR) == 1 and count_sub(c, "corner_gap/corner_gate") == 0


def lib_reverse_ok(c: str) -> bool:
    return count_sub(c, LIB_CR_NEW_BLOCK) == 1


def loop_forward_ok(c: str) -> bool:
    anchors = all(count_sub(c, a) == 1 for a in
                  [LOOP_ANCHOR_RESET, LOOP_ANCHOR_EXEC, LOOP_ANCHOR_TAIL, LOOP_ANCHOR_LASTRES])
    new_absent = all(t not in c for t in
                     ["$sexpr_gated", "do-clear-coupling-status!", "populate-state-delta",
                      "populate-coupling-verdict", "$results_final"])
    return anchors and new_absent


def loop_reverse_ok(c: str) -> bool:
    return all(count_sub(c, n) == 1 for n in
               [LOOP_NEW_RESET, LOOP_NEW_EXEC, LOOP_NEW_TAIL, LOOP_NEW_LASTRES])


def artifact1_forward_ok(c: str) -> bool:
    return count_sub(c, ARTIFACT1_ANCHOR) == 1 and "Layer 5 wiring additions (corner_gap" not in c


def artifact1_reverse_ok(c: str) -> bool:
    return count_sub(c, ARTIFACT1_NEW_AT_ANCHOR) == 1


# ============================================================================
# DIFF PREVIEW
# ============================================================================

def diff_preview(old: str, new: str, label: str, context: int = 2) -> str:
    o = old.splitlines()
    n = new.splitlines()
    start = None
    for i in range(min(len(o), len(n))):
        if o[i] != n[i]:
            start = i
            break
    if start is None and len(o) == len(n):
        return f"--- {label}: NO CHANGE"
    if start is None:
        start = min(len(o), len(n))
    end_o, end_n = len(o), len(n)
    for j in range(1, min(len(o), len(n)) + 1):
        if o[-j] != n[-j]:
            end_o = len(o) - j + 1
            end_n = len(n) - j + 1
            break
    lo = max(0, start - context)
    out = [f"--- {label} (first changed region) ---"]
    for i in range(lo, start):
        out.append(f"  {o[i]}")
    for i in range(start, end_o):
        out.append(f"- {o[i]}")
    for i in range(start, end_n):
        out.append(f"+ {n[i]}")
    return "\n".join(out)


# ============================================================================
# PROCESS
# ============================================================================

def process_file(path, bak, sim_fwd, sim_rev, label, check_parens,
                 fwd_ok, rev_ok, args):
    orig = path.read_text()
    sim = sim_rev(orig) if args.reverse else sim_fwd(orig)

    delta = sim.count("\n") - orig.count("\n")
    print(f"\n[{label}] line delta: {delta:+d}")

    if check_parens:
        o1, c1 = code_aware_paren_count(orig)
        o2, c2 = code_aware_paren_count(sim)
        print(f"[{label}] paren delta orig={o1 - c1} sim={o2 - c2} (both must be 0)")
        if (o2 - c2) != 0:
            print(f"[{label}] FAIL: simulated paren delta != 0")
            return False, orig, sim

    post_ok = fwd_ok(sim) if args.reverse else rev_ok(sim)
    print(f"[{label}] post-sim state check: {'OK' if post_ok else 'FAIL'}")
    return post_ok, orig, sim


def main() -> int:
    p = argparse.ArgumentParser(description="corner_gap Layer 5 wiring (one coordinated change)")
    p.add_argument("--apply", action="store_true", help="write changes (default dry-run)")
    p.add_argument("--reverse", action="store_true", help="reverse edits; combine with --apply")
    args = p.parse_args()

    direction = "REVERSE" if args.reverse else "APPLY"
    print(f"\n========== CORNER_GAP LAYER 5 WIRING: {direction} ==========")

    # Pre-condition: target files and the 5 corner_gap files present
    for path, lbl in [(LIB_CR_PATH, "lib_clarity_reasoning"), (LOOP_PATH, "loop.metta"),
                      (ARTIFACT1_PATH, "artifact_1")]:
        if not path.exists():
            print(f"MISSING target: {path}")
            return 1
    missing = [f for f in REQUIRED_CORNER_GAP_FILES if not (CORNER_GAP_DIR / f).exists()]
    if missing:
        print(f"MISSING corner_gap files in {CORNER_GAP_DIR}: {missing}")
        print("Place the validated files first; this script wires, it does not create them.")
        return 1
    print(f"Pre-condition OK: 5 corner_gap files present in {CORNER_GAP_DIR}")

    try:
        ok_lib, lib_o, lib_s = process_file(LIB_CR_PATH, LIB_CR_BAK,
                                            simulate_lib_forward, simulate_lib_reverse,
                                            "lib_clarity_reasoning.metta", True,
                                            lib_forward_ok, lib_reverse_ok, args)
        if not ok_lib:
            return 1
        ok_loop, loop_o, loop_s = process_file(LOOP_PATH, LOOP_BAK,
                                               simulate_loop_forward, simulate_loop_reverse,
                                               "loop.metta", True,
                                               loop_forward_ok, loop_reverse_ok, args)
        if not ok_loop:
            return 1
        ok_art, art_o, art_s = process_file(ARTIFACT1_PATH, ARTIFACT1_BAK,
                                            simulate_artifact1_forward, simulate_artifact1_reverse,
                                            "artifact_1.md", False,
                                            artifact1_forward_ok, artifact1_reverse_ok, args)
        if not ok_art:
            return 1
    except RuntimeError as e:
        print(f"\nSIMULATION ERROR: {e}")
        print("No files written. Fix the anchor/state issue and re-run.")
        return 1

    print("\n========== DIFF PREVIEWS ==========")
    print(diff_preview(lib_o, lib_s, "lib_clarity_reasoning.metta"))
    print()
    print(diff_preview(loop_o, loop_s, "loop.metta"))
    print()
    print(diff_preview(art_o, art_s, "artifact_1.md"))

    if not args.apply:
        print("\n========== DRY-RUN COMPLETE ==========")
        print("All checks pass. Re-run with --apply to write.")
        print("REVIEW: the two Edit C booleans ($results_nonempty, $results_novel) are derived,")
        print("not harness-transcribed. Confirm them (and ideally Clarity confirms) before trust.")
        return 0

    if not args.reverse:
        for path, bak in [(LIB_CR_PATH, LIB_CR_BAK), (LOOP_PATH, LOOP_BAK), (ARTIFACT1_PATH, ARTIFACT1_BAK)]:
            if bak.exists():
                print(f"WARNING: backup {bak} exists; overwriting.")
            bak.write_text(path.read_text())
            print(f"Backup written: {bak}")

    print("\n========== WRITING ==========")
    LIB_CR_PATH.write_text(lib_s); print(f"Wrote: {LIB_CR_PATH}")
    LOOP_PATH.write_text(loop_s); print(f"Wrote: {LOOP_PATH}")
    ARTIFACT1_PATH.write_text(art_s); print(f"Wrote: {ARTIFACT1_PATH}")

    print("\n========== DISK VERIFICATION ==========")
    lib_d = LIB_CR_PATH.read_text()
    loop_d = LOOP_PATH.read_text()
    art_d = ARTIFACT1_PATH.read_text()
    v_lib = (lib_forward_ok if args.reverse else lib_reverse_ok)(lib_d)
    v_loop = (loop_forward_ok if args.reverse else loop_reverse_ok)(loop_d)
    v_art = (artifact1_forward_ok if args.reverse else artifact1_reverse_ok)(art_d)
    for lbl, d, vok in [("lib", lib_d, v_lib), ("loop", loop_d, v_loop)]:
        o, c = code_aware_paren_count(d)
        print(f"  {lbl}: paren delta={o - c} state={'OK' if vok else 'FAIL'}")
    print(f"  artifact_1: state={'OK' if v_art else 'FAIL'}")
    lib_pok = (lambda d: code_aware_paren_count(d)[0] == code_aware_paren_count(d)[1])(lib_d)
    loop_pok = (lambda d: code_aware_paren_count(d)[0] == code_aware_paren_count(d)[1])(loop_d)

    if not (v_lib and v_loop and v_art and lib_pok and loop_pok):
        print("\nDISK VERIFICATION FAILED. Restore from .bak:")
        print(f"  cp {LIB_CR_BAK} {LIB_CR_PATH}")
        print(f"  cp {LOOP_BAK} {LOOP_PATH}")
        print(f"  cp {ARTIFACT1_BAK} {ARTIFACT1_PATH}")
        return 1

    print("\n========== CORNER_GAP LAYER 5 WIRING COMPLETE ==========")
    if not args.reverse:
        print("Next: stage the 5 corner_gap files + the 3 wired files, rebuild, verify.")
        print("  docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw && sleep 15 && docker logs clarity_omega 2>&1 | tail -100")
        print("Then a seeded-corner REPL probe: confirm a confirmed corner yields (RESULTS: feedback)")
        print("through the live line-134 let/collapse, and normal cycles are unchanged.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
