#!/usr/bin/env python3
"""apply_idle_directive_once_per_window_path1_gamma.py

Path 1 (gamma) fix for idle_directive 50-iteration burst.

Background:
    Step 6 aliveness gate work (May 16 2026) revealed that idle_directive
    fires on every iteration of the 50-iteration wake-burst (configure
    maxWakeLoops 50, line 12 of loop.metta), not once per 600-second
    wakeupInterval as the original design intent.

    Root cause: line 98 guard
        (if (and (not $msgnew)
                 (> (get_time) (+ (get-state &last_human_time) (wakeupInterval))))
            (py-call helper.soul_idle_goal_prompt_v2 ...)
            "")
    once the wakeupInterval threshold is crossed past &last_human_time,
    the guard evaluates True on every iteration of the wake-burst,
    causing idle_directive to fire 50 times.

    Fix (Path 1 / gamma per Clarity's analysis): introduce a parallel
    state variable &last_idle_fire_time that captures the timestamp of
    the most recent idle_directive fire. Extend the guard with a second
    conjunct requiring &last_idle_fire_time + wakeupInterval to also be
    in the past. Update &last_idle_fire_time to (get_time) whenever
    idle_directive fires.

    Result: idle_directive fires at most once per 600-second window
    regardless of wake-burst iteration count. The Step 6 substrate-
    composition gate becomes reachable on iterations 2-50 of the burst.

    Clarity rejected option beta (mutating &last_human_time) explicitly:
    "Mutating &last_human_time to contain synthetic timestamps destroys
    its semantic contract... Do not touch &last_human_time for this."

    Clarity rejected option alpha (wake-burst iteration count tracking)
    explicitly: tying the fix to maxWakeLoops makes it brittle against
    config changes. Time-window gating mirrors the existing
    &nextWakeAt / wakeupInterval idiom.

Important note on drafting context:
    This script was drafted AFTER Berton stopped the container due to a
    NEW issue surfacing during testing: msgnew flag appears to stick
    True across iterations, causing the same human message to be
    processed repeatedly (7+ replays of "Are you stuck?" in history.metta
    with the same read-file response). This human-side duplicate-
    engagement bug is DISTINCT from the idle-side bug this script fixes.

    Before applying this script:
    1. Investigate the human-side issue (Option II in the conversation)
    2. Verify nothing learned during investigation revises Path 1 design
    3. THEN apply this script

    The anchor points are safely outside the human-side hotspot:
    - line 30 area (bootstrap) is not where msgnew handling lives
    - line 98 area (idle guard) is downstream of msgnew handling
    - line 73 (the &last_human_time mutation tied to msgnew) is NOT
      touched by this script

Five coordinated edits:

    Edit 1: src/loop.metta - bootstrap initialization
        After line 30 (&last_human_time 0), insert
        (change-state! &last_idle_fire_time 0)

    Edit 2: src/loop.metta - guard + state mutation (combined)
        Modify line 98 guard to add second conjunct.
        Insert new line 99 ($_ ...) that sets &last_idle_fire_time
        to (get_time) when $idle_directive is non-empty.
        Line 99 (latch transition) becomes line 100.

    Edit 3: docs/design/artifact_1_loop_metta_wiring_diagram.md
        Insert new state variable table row for &last_idle_fire_time
        after &last_human_time row.

    Edit 4: docs/design/artifact_1_loop_metta_wiring_diagram.md
        Add new line documentation paragraph after Line 68 paragraph
        documenting the new state mutation.

    Edit 5: docs/design/artifact_1_loop_metta_wiring_diagram.md
        Update Line 92 (idle directive) Reads list to include
        &last_idle_fire_time alongside &last_human_time.

Contract compliance:
    - Discipline 1 (single function calls): N/A, all changes use existing
      change-state! and if/and primitives
    - Discipline 2 (one writer file): N/A, no new soul/ files
    - Discipline 3 (predictable structural location): bootstrap area
      adjacent to &last_human_time bootstrap; guard area is exact line
      that needs modification
    - Discipline 4 (wiring diagram stays current): three artifact_1
      edits cover this
    - Discipline 5 (migration retires inline logic): N/A, no inline
      logic added; new variable mirrors existing pattern
    - Discipline 6 Part A (pure-vs-writer split): N/A, no new primitive
    - Discipline 6 Part B (writer/consumer enumeration):
      Writers: line 30 (bootstrap to 0), new line after 98 (set to
        get_time when idle fires)
      Consumers: line 98 (extended guard conjunct)
      Intermediate transformations: none
      Configuration constants: wakeupInterval (reused, no new config)
      Other consumers downstream: same as idle_directive (lines 99,
        100, 107, 110, all unchanged behavior on iterations 2-50 of
        burst because idle_directive returns empty)

Reversibility:
    .bak.idle_directive_once_per_window_path1_gamma backups created
    before writing. --reverse --apply restores.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


# ============================================================================
# FILE PATHS
# ============================================================================

LOOP_PATH = Path("src/loop.metta")
LOOP_BAK = Path("src/loop.metta.bak.idle_directive_once_per_window_path1_gamma")

ART1_PATH = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md")
ART1_BAK = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md.bak.idle_directive_once_per_window_path1_gamma")


# ============================================================================
# EDIT 1: loop.metta bootstrap initialization
# ============================================================================

LOOP_ANCHOR_BOOTSTRAP = """          (change-state! &last_human_time 0)
          (change-state! &engaged_idle_count 0)"""

LOOP_NEW_BOOTSTRAP = """          (change-state! &last_human_time 0)
          (change-state! &last_idle_fire_time 0)
          (change-state! &engaged_idle_count 0)"""


# ============================================================================
# EDIT 2: loop.metta guard + state mutation (combined, spans lines 98-99)
# ============================================================================

LOOP_ANCHOR_GUARD = """                                       ($idle_directive (if (and (not $msgnew) (> (get_time) (+ (get-state &last_human_time) (wakeupInterval)))) (py-call (helper.soul_idle_goal_prompt_v2 (py-call (helper.extract_username $msg)) "" $atomspace_goals $atomspace_gaps $atomspace_fuel)) ""))
                                       ($_ (if (not (== $idle_directive "")) (set-atom! &self (latch-state ENGAGED) (latch-state IDLE)) _))"""

LOOP_NEW_GUARD = """                                       ($idle_directive (if (and (not $msgnew) (and (> (get_time) (+ (get-state &last_human_time) (wakeupInterval))) (> (get_time) (+ (get-state &last_idle_fire_time) (wakeupInterval))))) (py-call (helper.soul_idle_goal_prompt_v2 (py-call (helper.extract_username $msg)) "" $atomspace_goals $atomspace_gaps $atomspace_fuel)) ""))
                                       ($_ (if (not (== $idle_directive "")) (change-state! &last_idle_fire_time (get_time)) _))
                                       ($_ (if (not (== $idle_directive "")) (set-atom! &self (latch-state ENGAGED) (latch-state IDLE)) _))"""


# ============================================================================
# EDIT 3: artifact_1 state variable table row insertion
# ============================================================================

ART1_ANCHOR_TABLE = """| `&last_human_time` | `0` | Timestamp of last human message, used for idle threshold | Line 92 (computes idle) | Line 68 |
| `&engaged_idle_count` | `0` | Counter for engaged-idle iterations, drives self-check | Line 94, line 97 | Line 94 |"""

ART1_NEW_TABLE = """| `&last_human_time` | `0` | Timestamp of last human message, used for idle threshold | Line 92 (computes idle) | Line 68 |
| `&last_idle_fire_time` | `0` | Timestamp of last idle_directive fire, used to gate once-per-window idle (Path 1 gamma, May 16 2026) | Line 92 (computes idle) | Line 92 (set on fire) |
| `&engaged_idle_count` | `0` | Counter for engaged-idle iterations, drives self-check | Line 94, line 97 | Line 94 |"""


# ============================================================================
# EDIT 4: artifact_1 line documentation paragraph
# ============================================================================

ART1_ANCHOR_LINE_DOC = """**Line 68** - `(if $msgnew (change-state! &last_human_time (get_time)) _)` - Records timestamp of last human contact, used for idle threshold detection.

### Phase 4.1: Soul input intercept (lines 69-87)"""

ART1_NEW_LINE_DOC = """**Line 68** - `(if $msgnew (change-state! &last_human_time (get_time)) _)` - Records timestamp of last human contact, used for idle threshold detection.

**Line 92.5 (Path 1 gamma)** - `(if (not (== $idle_directive "")) (change-state! &last_idle_fire_time (get_time)) _)` - Records timestamp of last idle_directive fire. Inserted between the guard (line 92) and the latch transition (line 93) so that the wake-burst's subsequent iterations see the guard's second conjunct evaluate False and return empty idle_directive. Implements once-per-window scheduled wakeup semantics. The V2 latch-pattern proposal in soul/aliveness_gate_v2_proposal.metta is the eventual architectural direction for both human-response and idle-response gating (Step 8 territory); &last_idle_fire_time is the time-window-idiom interim correct fix for this architecture.

### Phase 4.1: Soul input intercept (lines 69-87)"""


# ============================================================================
# EDIT 5: artifact_1 Line 92 Reads list update
# ============================================================================

ART1_ANCHOR_READS = """**Line 92** - Idle directive generation
- Reads: $msgnew, &last_human_time, $atomspace_goals/gaps/fuel
- Writes: $idle_directive"""

ART1_NEW_READS = """**Line 92** - Idle directive generation
- Reads: $msgnew, &last_human_time, &last_idle_fire_time (Path 1 gamma), $atomspace_goals/gaps/fuel
- Writes: $idle_directive, &last_idle_fire_time (Path 1 gamma, set when directive non-empty)"""


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def count_substr(text: str, needle: str) -> int:
    if not needle:
        return 0
    return text.count(needle)


def read_file(path: Path) -> str:
    return path.read_text()


def write_file(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        return
    path.write_text(content)


def backup_if_needed(path: Path, bak_path: Path, dry_run: bool) -> None:
    if dry_run:
        return
    if not bak_path.exists():
        bak_path.write_bytes(path.read_bytes())


# ============================================================================
# EDIT PROCESSORS
# ============================================================================


def process_loop_metta(direction: str, dry_run: bool) -> dict:
    """Two sequential replacements in src/loop.metta:
       1. Bootstrap initialization (after line 30)
       2. Guard conjunct + new state mutation (combined, spans 98-99)
    """
    text = read_file(LOOP_PATH)
    pre_lines = text.count("\n")

    if direction == "apply":
        anchors = [
            (LOOP_ANCHOR_BOOTSTRAP, LOOP_NEW_BOOTSTRAP, "Bootstrap initialization"),
            (LOOP_ANCHOR_GUARD, LOOP_NEW_GUARD, "Guard conjunct + new state mutation"),
        ]
        sentinels_to_be_absent = ["&last_idle_fire_time"]
        state_check_label = "pre-Path-1 markers absent"
    else:
        anchors = [
            (LOOP_NEW_BOOTSTRAP, LOOP_ANCHOR_BOOTSTRAP, "Bootstrap initialization"),
            (LOOP_NEW_GUARD, LOOP_ANCHOR_GUARD, "Guard conjunct + new state mutation"),
        ]
        sentinels_to_be_absent = []
        state_check_label = "post-Path-1 markers present"

    for anchor, new, label in anchors:
        if anchor not in text:
            return {
                "path": str(LOOP_PATH),
                "ok": False,
                "message": f"Anchor not found for {label}: state check failed ({state_check_label})",
                "pre_lines": pre_lines,
            }
        count = count_substr(text, anchor)
        if count != 1:
            return {
                "path": str(LOOP_PATH),
                "ok": False,
                "message": f"Anchor for {label} count = {count}, expected 1",
                "pre_lines": pre_lines,
            }

    if direction == "apply":
        for sentinel in sentinels_to_be_absent:
            if sentinel in text:
                return {
                    "path": str(LOOP_PATH),
                    "ok": False,
                    "message": f"Sentinel for already-applied state present: {sentinel}",
                    "pre_lines": pre_lines,
                }

    new_text = text
    for anchor, new, label in anchors:
        new_text = new_text.replace(anchor, new, 1)

    backup_if_needed(LOOP_PATH, LOOP_BAK, dry_run)
    write_file(LOOP_PATH, new_text, dry_run)

    post_lines = new_text.count("\n")
    edit_label = (
        "insert bootstrap + extend guard + add state mutation"
        if direction == "apply"
        else "remove bootstrap + restore guard + remove state mutation"
    )
    return {
        "path": str(LOOP_PATH),
        "ok": True,
        "pre_lines": pre_lines,
        "post_lines": post_lines,
        "line_delta": post_lines - pre_lines,
        "edit": edit_label,
    }


def process_artifact1(direction: str, dry_run: bool) -> dict:
    """Three sequential replacements in artifact_1_loop_metta_wiring_diagram.md:
       1. State variable table row insertion
       2. Line documentation paragraph addition
       3. Line 92 Reads/Writes list update
    """
    text = read_file(ART1_PATH)
    pre_lines = text.count("\n")

    if direction == "apply":
        anchors = [
            (ART1_ANCHOR_TABLE, ART1_NEW_TABLE, "State variable table row"),
            (ART1_ANCHOR_LINE_DOC, ART1_NEW_LINE_DOC, "Line documentation paragraph"),
            (ART1_ANCHOR_READS, ART1_NEW_READS, "Line 92 Reads/Writes update"),
        ]
        sentinels_to_be_absent = ["&last_idle_fire_time"]
        state_check_label = "pre-Path-1 markers absent"
    else:
        anchors = [
            (ART1_NEW_TABLE, ART1_ANCHOR_TABLE, "State variable table row"),
            (ART1_NEW_LINE_DOC, ART1_ANCHOR_LINE_DOC, "Line documentation paragraph"),
            (ART1_NEW_READS, ART1_ANCHOR_READS, "Line 92 Reads/Writes update"),
        ]
        sentinels_to_be_absent = []
        state_check_label = "post-Path-1 markers present"

    for anchor, new, label in anchors:
        if anchor not in text:
            return {
                "path": str(ART1_PATH),
                "ok": False,
                "message": f"Anchor not found for {label}: state check failed ({state_check_label})",
                "pre_lines": pre_lines,
            }
        count = count_substr(text, anchor)
        if count != 1:
            return {
                "path": str(ART1_PATH),
                "ok": False,
                "message": f"Anchor for {label} count = {count}, expected 1",
                "pre_lines": pre_lines,
            }

    if direction == "apply":
        for sentinel in sentinels_to_be_absent:
            if sentinel in text:
                return {
                    "path": str(ART1_PATH),
                    "ok": False,
                    "message": f"Sentinel for already-applied state present: {sentinel}",
                    "pre_lines": pre_lines,
                }

    new_text = text
    for anchor, new, label in anchors:
        new_text = new_text.replace(anchor, new, 1)

    backup_if_needed(ART1_PATH, ART1_BAK, dry_run)
    write_file(ART1_PATH, new_text, dry_run)

    post_lines = new_text.count("\n")
    edit_label = (
        "insert table row + add line doc + update Line 92 Reads"
        if direction == "apply"
        else "remove table row + remove line doc + restore Line 92 Reads"
    )
    return {
        "path": str(ART1_PATH),
        "ok": True,
        "pre_lines": pre_lines,
        "post_lines": post_lines,
        "line_delta": post_lines - pre_lines,
        "edit": edit_label,
    }


# ============================================================================
# MAIN
# ============================================================================


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--apply", action="store_true", help="Write changes to disk")
    parser.add_argument("--reverse", action="store_true", help="Reverse direction")
    args = parser.parse_args()

    direction = "reverse" if args.reverse else "apply"
    dry_run = not args.apply

    print()
    print("=" * 78)
    print(f"  IDLE DIRECTIVE ONCE-PER-WINDOW PATH 1 (GAMMA): {direction.upper()} ({'DRY-RUN' if dry_run else 'WRITING'})")
    print("=" * 78)
    print()

    for p in [LOOP_PATH, ART1_PATH]:
        if not p.exists():
            print(f"  ERROR: {p} does not exist. Are you at repo root?")
            return 1

    print(">>> Per-file state checks and edits <<<")
    print()

    results = []
    processors = [
        (process_loop_metta, "src/loop.metta"),
        (process_artifact1, "docs/design/artifact_1_loop_metta_wiring_diagram.md"),
    ]

    for processor, label in processors:
        print(f"  [{label}]")
        result = processor(direction, dry_run=True)
        if not result.get("ok"):
            print(f"    FAIL: {result.get('message')}")
            print()
            print("  Halting -- no changes written.")
            return 1
        pre_l = result.get("pre_lines")
        post_l = result.get("post_lines")
        delta_l = result.get("line_delta")
        print(f"    Lines: {pre_l} -> {post_l} (delta {delta_l:+d})")
        print(f"    Edit: {result.get('edit')}")
        results.append((label, result))
        print()

    print("=" * 78)
    print(f"  SUMMARY: WHAT --{direction} --apply WILL DO")
    print("=" * 78)
    print()
    print(f"  Direction: {direction.upper()}")
    print(f"  Backup suffix: .bak.idle_directive_once_per_window_path1_gamma")
    print()
    for label, r in results:
        print(f"  {label}: {r.get('edit')}")
        print(f"    {r.get('pre_lines')} -> {r.get('post_lines')} lines (delta {r.get('line_delta'):+d})")
    print()
    print("  Total edits: 2 files")
    print("    - src/loop.metta: 2 edits (bootstrap + combined guard/state-mutation)")
    print("    - docs/design/artifact_1_loop_metta_wiring_diagram.md: 3 edits (table + line doc + Reads)")
    print("  Contract: substrate edit + wiring diagram update, Discipline 4 satisfied")
    print("  Reversibility: python3 staging/apply_idle_directive_once_per_window_path1_gamma.py --reverse --apply")
    print()
    print("  Rebuild required after apply:")
    print("    docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw")
    print()
    print("  Behavioral verification after rebuild:")
    print("    Observe idle_directive fires AT MOST ONCE per 600-second window.")
    print("    Substrate-composition path in aliveness_gate becomes reachable on")
    print("    iterations 2-50 of the wake-burst.")
    print()

    if dry_run:
        print("  DRY-RUN MODE: no files written. To apply, add --apply.")
        return 0

    print("=" * 78)
    print("  WRITING")
    print("=" * 78)
    print()
    final_results = []
    for processor, label in processors:
        result = processor(direction, dry_run=False)
        if not result.get("ok"):
            print(f"  FAIL on {label}: {result.get('message')}")
            return 1
        print(f"  Wrote: {label}")
        final_results.append((label, result))
    print()

    print("=" * 78)
    print("  DISK VERIFICATION")
    print("=" * 78)
    print()
    for label, r in final_results:
        print(f"  {label}: {r.get('post_lines')} lines, edit applied")
    print()
    print("=" * 78)
    print(f"  IDLE DIRECTIVE PATH 1 (GAMMA) {direction.upper()} COMPLETE")
    print("=" * 78)
    print()
    if direction == "apply":
        print("  NEXT: rebuild + observe behavioral verification, then stage + commit.")
        print("        docker compose build --no-cache clarityclaw")
        print("        docker compose up -d clarityclaw")
    return 0


if __name__ == "__main__":
    sys.exit(main())
