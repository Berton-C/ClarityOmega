#!/usr/bin/env python3
"""
Apply script: Step 2 of task-state primitive. Wires loop.metta hooks
plus lib_clarity_reasoning import plus artifact_1 phase entries.

Purpose
-------
Step 1 (commit 2a69a80) landed soul/task_state.metta with atom shapes and
read helpers. Step 2 wires the substrate into the cycle: bootstrap call in
initLoop, plus three per-cycle mechanical writers.

Clarity's substrate work for Step 2 has already landed on disk (uncommitted):
- soul/task_state.metta edited (bare atoms removed)
- soul/task_state_writers.metta created (do-bootstrap-task-state!,
  do-set-cycles-since-input!, do-set-last-activity!)

This script does the wiring around her substrate:
- lib_clarity_reasoning/lib_clarity_reasoning.metta: one new import line
- src/loop.metta: four hook insertions (1 bootstrap + 3 per-cycle)
- docs/design/artifact_1_loop_metta_wiring_diagram.md: phase entries for
  the four new hooks (Discipline 4 maintenance contract per artifact 0)

The six edits land as one coordinated change. All or none.

The six edits
-------------
Edit 1: lib_clarity_reasoning import for task_state_writers
  Anchor: existing import line for soul/task_state
  Insertion: 3 lines (blank + comment + import) after the anchor

Edit 2: loop.metta initLoop bootstrap call
  Anchor: closing line of initLoop progn block (the &loops line)
  Insertion: 1 line, hook call before the closing paren of progn

Edit 3: loop.metta post-msgnew last-activity hook (Phase 4.0)
  Anchor: existing &last_human_time write line
  Insertion: 1 line after, hook conditional on $msgnew

Edit 4: loop.metta cycles-since-input hook (Phase 4.2)
  Anchor: existing &engaged_idle_count write line
  Insertion: 1 line after, hook with reset-on-msgnew else increment

Edit 5: loop.metta post-send last-activity hook (Phase 4.4)
  Anchor: existing CHARS_SENT/SILENT_CYCLE println line
  Insertion: 1 line after, hook conditional on non-SILENT aliveness

Edit 6: artifact_1 phase entry updates
  Anchor: end of Phase 4.0 section (line 4.0 boundary)
  Insertion: 4 paragraphs documenting the new hooks per Discipline 4

Hook semantics (resolved with Clarity)
--------------------------------------
- cycles-since-input: reset on $msgnew only, increment otherwise (Option A
  per Clarity's design decision; preserves pure input-staleness semantics)
- last-activity: written at two events per cycle: post-msgnew with
  (get_time), post-send with (get_time)
- bootstrap: conditional add-atom for each scalar; safe in face of
  future persistence restoration

Net change
----------
- lib_clarity_reasoning.metta: +3 lines (blank + comment + import)
- loop.metta: +4 lines (one per hook)
- artifact_1: ~12-16 lines (4 paragraphs of phase documentation)
- Paren delta for both .metta files: 0 (each hook is a balanced expression)

Mechanism
---------
- do-bootstrap-task-state! runs once in initLoop; idempotent in face of
  future persistence restoration
- do-set-last-activity! runs twice per cycle (post-msgnew and post-send)
  with (get_time); reads current via current-last-activity, set-atom!
  replaces with timestamp
- do-set-cycles-since-input! runs once per cycle in the loops>0 branch;
  reads current via current-cycles-since-input, set-atom! replaces with
  either 0 (reset) or (+ 1 current) (increment)

Usage
-----
Dry-run (default):
    python3 staging/apply_task_state_step2_wiring.py

Apply:
    python3 staging/apply_task_state_step2_wiring.py --apply

Reverse (after apply):
    python3 staging/apply_task_state_step2_wiring.py --reverse --apply

Pre-conditions
--------------
- Clarity's substrate work landed: soul/task_state.metta edited and
  soul/task_state_writers.metta present
- Step 1 commit at HEAD or in lineage (atoms loaded at startup currently)
- Container can be rebuilt after apply

Backup files (forward apply only):
- lib_clarity_reasoning/lib_clarity_reasoning.metta.bak.step2_wiring
- src/loop.metta.bak.step2_wiring
- docs/design/artifact_1_loop_metta_wiring_diagram.md.bak.step2_wiring
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# ============================================================================
# FILE PATHS
# ============================================================================

LIB_CR_PATH = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta")
LIB_CR_BAK = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta.bak.step2_wiring")

LOOP_PATH = Path("src/loop.metta")
LOOP_BAK = Path("src/loop.metta.bak.step2_wiring")

ARTIFACT1_PATH = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md")
ARTIFACT1_BAK = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md.bak.step2_wiring")

# ============================================================================
# EDIT 1: lib_clarity_reasoning import for task_state_writers
# ============================================================================

# Anchor: the task_state import line we added in Step 1
LIB_CR_ANCHOR = "!(import! &self (library omegaclaw ./soul/task_state))"

# New block: blank line + comment + import
LIB_CR_NEW_BLOCK = (
    LIB_CR_ANCHOR + "\n"
    "\n"
    ";; Task-state writers: side-effecting do-*! functions for task-state atoms\n"
    "!(import! &self (library omegaclaw ./soul/task_state_writers))\n"
)

LIB_CR_OLD_BLOCK = LIB_CR_ANCHOR + "\n"

# ============================================================================
# EDIT 2: loop.metta initLoop bootstrap hook
# ============================================================================

# Anchor: the &loops init line, last line of initLoop progn before closing
# We insert a new hook line before the closing parens of initLoop's progn
LOOP_ANCHOR_INITLOOP = "          (change-state! &loops (maxNewInputLoops))))"
LOOP_NEW_INITLOOP = (
    "          (change-state! &loops (maxNewInputLoops))\n"
    "          ;; Task-state primitive: conditional bootstrap of scalar atoms\n"
    "          (do-bootstrap-task-state!)))"
)

# ============================================================================
# EDIT 3: loop.metta last-activity post-msgnew hook (Phase 4.0)
# ============================================================================

# Anchor: existing &last_human_time write at line 68
LOOP_ANCHOR_LAST_HUMAN = "                                       ($_ (if $msgnew (change-state! &last_human_time (get_time)) _))"
LOOP_NEW_LAST_HUMAN = (
    LOOP_ANCHOR_LAST_HUMAN + "\n"
    "                                       ($_ (if $msgnew (do-set-last-activity! (get_time)) _))"
)

# ============================================================================
# EDIT 4: loop.metta cycles-since-input hook (Phase 4.2)
# ============================================================================

# Anchor: existing &engaged_idle_count write at line 94
LOOP_ANCHOR_ENGAGED_IDLE = "                                       ($_ (if $msgnew (change-state! &engaged_idle_count 0) (if (> (string_length $idle_directive) 0) (change-state! &engaged_idle_count 0) (change-state! &engaged_idle_count (+ 1 (get-state &engaged_idle_count))))))"
LOOP_NEW_ENGAGED_IDLE = (
    LOOP_ANCHOR_ENGAGED_IDLE + "\n"
    "                                       ($_ (if $msgnew (do-set-cycles-since-input! 0) (do-set-cycles-since-input! (+ 1 (current-cycles-since-input)))))"
)

# ============================================================================
# EDIT 5: loop.metta last-activity post-send hook (Phase 4.4)
# ============================================================================

# Anchor: existing CHARS_SENT/SILENT_CYCLE println at line 107
LOOP_ANCHOR_CHARS_SENT = "                                       ($_ (if (not (== $aliveness SILENT)) (println! (CHARS_SENT: (string_length $send) $send)) (println! (SILENT_CYCLE))))"
LOOP_NEW_CHARS_SENT = (
    LOOP_ANCHOR_CHARS_SENT + "\n"
    "                                       ($_ (if (not (== $aliveness SILENT)) (do-set-last-activity! (get_time)) _))"
)

# ============================================================================
# EDIT 6: artifact_1 phase entries
# ============================================================================

# Anchor: end of Section 4 (just before "## Section 5" header)
# We append a new subsection documenting the four Step 2 hooks
ARTIFACT1_ANCHOR = "## Section 5: The aliveness latch state machine"

ARTIFACT1_NEW_SUBSECTION = (
    "### Step 2 wiring additions (task-state primitive)\n"
    "\n"
    "**initLoop bootstrap hook** (added after the &loops init line in initLoop).\n"
    "Calls `(do-bootstrap-task-state!)` defined in `soul/task_state_writers.metta`.\n"
    "Idempotent conditional add-atom for the three scalar task-state atoms\n"
    "(task-phase, cycles-since-input, last-activity) when absent from &self.\n"
    "Safe in face of future persistence restoration (guard prevents dual-atom\n"
    "ambiguity).\n"
    "\n"
    "**Phase 4.0 last-activity hook** (added after the existing `&last_human_time`\n"
    "write at line 68). Calls `(do-set-last-activity! (get_time))` when $msgnew\n"
    "is true. Mirrors the existing `&last_human_time` semantics into AtomSpace via\n"
    "the task-state primitive. Existing `&last_human_time` write remains in place\n"
    "per Sprint 4 process commitment (writers mirror, not subsume, until consumers\n"
    "migrate in Steps 5-9).\n"
    "\n"
    "**Phase 4.2 cycles-since-input hook** (added after the existing\n"
    "`&engaged_idle_count` write at line 94). Calls\n"
    "`(do-set-cycles-since-input! 0)` when $msgnew is true, otherwise\n"
    "`(do-set-cycles-since-input! (+ 1 (current-cycles-since-input)))`.\n"
    "Reset semantics differ from `&engaged_idle_count` by design (Clarity's\n"
    "decision May 13, 2026): cycles-since-input resets ONLY on $msgnew, preserving\n"
    "the pure input-staleness contract encoded in the atom name. Consumers needing\n"
    "engagement-reset semantics will compose cycles-since-input with last-activity\n"
    "rather than direct-swap when `&engaged_idle_count` retires in Step 5+.\n"
    "\n"
    "**Phase 4.4 last-activity post-send hook** (added after the CHARS_SENT/\n"
    "SILENT_CYCLE println at line 107). Calls `(do-set-last-activity! (get_time))`\n"
    "when aliveness is not SILENT. Records send-event activity into AtomSpace.\n"
    "Spec Section 4 defines last-activity as 'most recent activity (human message\n"
    "OR Clarity-emitted send)'. Both event types are captured per cycle.\n"
    "\n"
    "🔧 ELEVATION FLAG (Step 5+): When self-check-guidance migrates from reading\n"
    "`&engaged_idle_count` (line 97) to reading task-state primitives, the consumer\n"
    "composes `(current-cycles-since-input)` AND `(current-last-activity)` to express\n"
    "its actual semantic need. Per Clarity's architectural call, the composition is\n"
    "more honest than overloading a single counter with two semantic meanings.\n"
    "\n"
    "---\n"
    "\n"
)

ARTIFACT1_OLD_AT_ANCHOR = ARTIFACT1_ANCHOR
ARTIFACT1_NEW_AT_ANCHOR = ARTIFACT1_NEW_SUBSECTION + ARTIFACT1_ANCHOR


# ============================================================================
# HELPERS (reused from apply_populator_grounding_let.py)
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


def find_target_lines(text: str, target: str) -> list[int]:
    target_stripped = target.strip()
    matches = []
    for idx, line in enumerate(text.splitlines(), start=1):
        if line.strip() == target_stripped:
            matches.append(idx)
    return matches


def find_target_substring_count(text: str, target: str) -> int:
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

def simulate_lib_cr_forward(content: str) -> str:
    """Insert task_state_writers import after task_state import."""
    count = find_target_substring_count(content, LIB_CR_OLD_BLOCK)
    if count != 1:
        raise RuntimeError(
            f"lib_cr forward: expected 1 occurrence of task_state import line, found {count}."
        )
    return content.replace(LIB_CR_OLD_BLOCK, LIB_CR_NEW_BLOCK, 1)


def simulate_lib_cr_reverse(content: str) -> str:
    """Remove task_state_writers import block."""
    count = find_target_substring_count(content, LIB_CR_NEW_BLOCK)
    if count != 1:
        raise RuntimeError(
            f"lib_cr reverse: expected 1 occurrence of new import block, found {count}."
        )
    return content.replace(LIB_CR_NEW_BLOCK, LIB_CR_OLD_BLOCK, 1)


def simulate_loop_forward(content: str) -> str:
    """Apply all 4 loop.metta hook insertions."""
    # Edit 2: initLoop bootstrap
    if find_target_substring_count(content, LOOP_ANCHOR_INITLOOP) != 1:
        raise RuntimeError(
            f"loop edit 2: anchor LOOP_ANCHOR_INITLOOP not found exactly once."
        )
    content = content.replace(LOOP_ANCHOR_INITLOOP, LOOP_NEW_INITLOOP, 1)

    # Edit 3: post-msgnew last-activity
    if find_target_substring_count(content, LOOP_ANCHOR_LAST_HUMAN) != 1:
        raise RuntimeError(
            f"loop edit 3: anchor LOOP_ANCHOR_LAST_HUMAN not found exactly once."
        )
    content = content.replace(LOOP_ANCHOR_LAST_HUMAN, LOOP_NEW_LAST_HUMAN, 1)

    # Edit 4: cycles-since-input
    if find_target_substring_count(content, LOOP_ANCHOR_ENGAGED_IDLE) != 1:
        raise RuntimeError(
            f"loop edit 4: anchor LOOP_ANCHOR_ENGAGED_IDLE not found exactly once."
        )
    content = content.replace(LOOP_ANCHOR_ENGAGED_IDLE, LOOP_NEW_ENGAGED_IDLE, 1)

    # Edit 5: post-send last-activity
    if find_target_substring_count(content, LOOP_ANCHOR_CHARS_SENT) != 1:
        raise RuntimeError(
            f"loop edit 5: anchor LOOP_ANCHOR_CHARS_SENT not found exactly once."
        )
    content = content.replace(LOOP_ANCHOR_CHARS_SENT, LOOP_NEW_CHARS_SENT, 1)

    return content


def simulate_loop_reverse(content: str) -> str:
    """Remove all 4 loop.metta hook insertions."""
    # Reverse order: 5, 4, 3, 2
    if find_target_substring_count(content, LOOP_NEW_CHARS_SENT) != 1:
        raise RuntimeError(
            f"loop reverse 5: new state LOOP_NEW_CHARS_SENT not found exactly once."
        )
    content = content.replace(LOOP_NEW_CHARS_SENT, LOOP_ANCHOR_CHARS_SENT, 1)

    if find_target_substring_count(content, LOOP_NEW_ENGAGED_IDLE) != 1:
        raise RuntimeError(
            f"loop reverse 4: new state LOOP_NEW_ENGAGED_IDLE not found exactly once."
        )
    content = content.replace(LOOP_NEW_ENGAGED_IDLE, LOOP_ANCHOR_ENGAGED_IDLE, 1)

    if find_target_substring_count(content, LOOP_NEW_LAST_HUMAN) != 1:
        raise RuntimeError(
            f"loop reverse 3: new state LOOP_NEW_LAST_HUMAN not found exactly once."
        )
    content = content.replace(LOOP_NEW_LAST_HUMAN, LOOP_ANCHOR_LAST_HUMAN, 1)

    if find_target_substring_count(content, LOOP_NEW_INITLOOP) != 1:
        raise RuntimeError(
            f"loop reverse 2: new state LOOP_NEW_INITLOOP not found exactly once."
        )
    content = content.replace(LOOP_NEW_INITLOOP, LOOP_ANCHOR_INITLOOP, 1)

    return content


def simulate_artifact1_forward(content: str) -> str:
    """Insert Step 2 wiring subsection before Section 5 header."""
    count = find_target_substring_count(content, ARTIFACT1_OLD_AT_ANCHOR)
    if count != 1:
        raise RuntimeError(
            f"artifact1 forward: expected 1 occurrence of Section 5 anchor, found {count}."
        )
    return content.replace(ARTIFACT1_OLD_AT_ANCHOR, ARTIFACT1_NEW_AT_ANCHOR, 1)


def simulate_artifact1_reverse(content: str) -> str:
    """Remove Step 2 wiring subsection."""
    count = find_target_substring_count(content, ARTIFACT1_NEW_AT_ANCHOR)
    if count != 1:
        raise RuntimeError(
            f"artifact1 reverse: expected 1 occurrence of new subsection block, found {count}."
        )
    return content.replace(ARTIFACT1_NEW_AT_ANCHOR, ARTIFACT1_OLD_AT_ANCHOR, 1)


# ============================================================================
# DIFF PREVIEW
# ============================================================================

def diff_preview_first_change(old: str, new: str, label: str, context: int = 3) -> str:
    """Show first changed region with context lines."""
    old_lines = old.splitlines()
    new_lines = new.splitlines()

    # Find first differing line
    differ_start = None
    for i in range(min(len(old_lines), len(new_lines))):
        if old_lines[i] != new_lines[i]:
            differ_start = i
            break
    if differ_start is None:
        if len(old_lines) == len(new_lines):
            return f"--- {label}: NO CHANGES DETECTED ---"
        differ_start = min(len(old_lines), len(new_lines))

    # Find end of differing region (simple approach: tail-match)
    differ_end_old = len(old_lines) - 1
    differ_end_new = len(new_lines) - 1
    while differ_end_old > differ_start and differ_end_new > differ_start:
        if old_lines[differ_end_old] == new_lines[differ_end_new]:
            differ_end_old -= 1
            differ_end_new -= 1
        else:
            break

    out = [f"--- {label} (lines {differ_start + 1} to {max(differ_end_old, differ_end_new) + 1}) ---"]
    start = max(0, differ_start - context)
    for i in range(start, differ_start):
        if i < len(old_lines):
            out.append(f"  {old_lines[i]}")
    for i in range(differ_start, differ_end_old + 1):
        if i < len(old_lines):
            out.append(f"- {old_lines[i]}")
    for i in range(differ_start, differ_end_new + 1):
        if i < len(new_lines):
            out.append(f"+ {new_lines[i]}")
    end_old = min(len(old_lines), differ_end_old + 1 + context)
    for i in range(differ_end_old + 1, end_old):
        out.append(f"  {old_lines[i]}")
    return "\n".join(out)


# ============================================================================
# MAIN
# ============================================================================

def check_file_exists(path: Path, label: str) -> bool:
    if not path.exists():
        print(f"ERROR: {label} not found at {path}. Run from repo root.")
        return False
    return True


def process_file(
    path: Path,
    bak_path: Path,
    simulate_fn,
    simulate_reverse_fn,
    expected_line_delta_forward: int,
    args,
    label: str,
    check_parens: bool,
    forward_state_check_fn,
    reverse_state_check_fn,
) -> tuple[bool, str, str]:
    """
    Process a single file: read, run pre-checks, simulate, run post-checks.
    Returns (success, original_content, simulated_content).
    """
    print(f"\n>>> {label} <<<")

    content = path.read_text()
    pre_lines = len(content.splitlines())
    pre_o, pre_c = code_aware_paren_count(content)
    pre_d = pre_o - pre_c

    print(f"  Path: {path}")
    print(f"  Pre-edit line count: {pre_lines}")
    if check_parens:
        c_paren = "OK" if pre_d == 0 else "FAIL"
        print(f"  Pre-edit paren count: opens={pre_o} closes={pre_c} delta={pre_d} ({c_paren})")
        if c_paren != "OK":
            print(f"  PAREN COUNT FAILED for {label}. Aborting.")
            return False, content, ""

    # State check
    if args.reverse:
        state_ok, state_msg = reverse_state_check_fn(content)
    else:
        state_ok, state_msg = forward_state_check_fn(content)
    print(f"  State check: {state_msg}")
    if not state_ok:
        print(f"  STATE CHECK FAILED for {label}. Aborting.")
        return False, content, ""

    # Simulate
    try:
        if args.reverse:
            simulated = simulate_reverse_fn(content)
        else:
            simulated = simulate_fn(content)
    except RuntimeError as exc:
        print(f"  SIMULATION FAILED: {exc}")
        return False, content, ""

    post_lines = len(simulated.splitlines())
    line_delta = post_lines - pre_lines

    if check_parens:
        post_o, post_c = code_aware_paren_count(simulated)
        post_d = post_o - post_c
        c_paren_post = "OK" if post_d == 0 else "FAIL"
        print(f"  Post-edit paren count: opens={post_o} closes={post_c} delta={post_d} ({c_paren_post})")
        if c_paren_post != "OK":
            print(f"  POST-EDIT PAREN COUNT FAILED for {label}. Aborting.")
            return False, content, simulated

    expected_delta = expected_line_delta_forward if not args.reverse else -expected_line_delta_forward
    c_lines = "OK" if line_delta == expected_delta else "FAIL"
    print(f"  Line delta: {line_delta} (expected {expected_delta}) ({c_lines})")
    if c_lines != "OK":
        print(f"  LINE DELTA FAILED for {label}. Aborting.")
        return False, content, simulated

    return True, content, simulated


# State check predicates per file

def lib_cr_forward_state_ok(content: str) -> tuple[bool, str]:
    # Should have task_state import but NOT yet have task_state_writers import
    has_anchor = find_target_substring_count(content, LIB_CR_ANCHOR + "\n") == 1
    has_new = "task_state_writers" in content
    ok = has_anchor and not has_new
    msg = f"anchor present={has_anchor}, writers import absent={not has_new} -> {'OK' if ok else 'FAIL'}"
    return ok, msg


def lib_cr_reverse_state_ok(content: str) -> tuple[bool, str]:
    # Should have the new block present
    has_new_block = find_target_substring_count(content, LIB_CR_NEW_BLOCK) == 1
    msg = f"new block present={has_new_block} -> {'OK' if has_new_block else 'FAIL'}"
    return has_new_block, msg


def loop_forward_state_ok(content: str) -> tuple[bool, str]:
    # All 4 anchors present, no new hooks
    a1 = find_target_substring_count(content, LOOP_ANCHOR_INITLOOP) == 1
    a2 = find_target_substring_count(content, LOOP_ANCHOR_LAST_HUMAN) == 1
    a3 = find_target_substring_count(content, LOOP_ANCHOR_ENGAGED_IDLE) == 1
    a4 = find_target_substring_count(content, LOOP_ANCHOR_CHARS_SENT) == 1
    n1 = "do-bootstrap-task-state!" not in content
    n2 = "do-set-last-activity!" not in content
    n3 = "do-set-cycles-since-input!" not in content
    ok = a1 and a2 and a3 and a4 and n1 and n2 and n3
    msg = f"anchors=({a1},{a2},{a3},{a4}) new_absent=({n1},{n2},{n3}) -> {'OK' if ok else 'FAIL'}"
    return ok, msg


def loop_reverse_state_ok(content: str) -> tuple[bool, str]:
    # All 4 new states present
    n1 = find_target_substring_count(content, LOOP_NEW_INITLOOP) == 1
    n2 = find_target_substring_count(content, LOOP_NEW_LAST_HUMAN) == 1
    n3 = find_target_substring_count(content, LOOP_NEW_ENGAGED_IDLE) == 1
    n4 = find_target_substring_count(content, LOOP_NEW_CHARS_SENT) == 1
    ok = n1 and n2 and n3 and n4
    msg = f"new_states=({n1},{n2},{n3},{n4}) -> {'OK' if ok else 'FAIL'}"
    return ok, msg


def artifact1_forward_state_ok(content: str) -> tuple[bool, str]:
    has_anchor = find_target_substring_count(content, ARTIFACT1_ANCHOR) == 1
    has_new = "Step 2 wiring additions" in content
    ok = has_anchor and not has_new
    msg = f"anchor present={has_anchor}, subsection absent={not has_new} -> {'OK' if ok else 'FAIL'}"
    return ok, msg


def artifact1_reverse_state_ok(content: str) -> tuple[bool, str]:
    has_new_block = find_target_substring_count(content, ARTIFACT1_NEW_AT_ANCHOR) == 1
    msg = f"new block present={has_new_block} -> {'OK' if has_new_block else 'FAIL'}"
    return has_new_block, msg


# Disk verification after write

def verify_disk(path: Path, args, label: str, forward_check_fn, reverse_check_fn, check_parens: bool) -> bool:
    disk = path.read_text()
    if check_parens:
        o, c = code_aware_paren_count(disk)
        d = o - c
        ok_p = d == 0
        print(f"  {label} disk paren: opens={o} closes={c} delta={d} ({'OK' if ok_p else 'FAIL'})")
        if not ok_p:
            return False
    if args.reverse:
        ok, msg = forward_check_fn(disk)  # After reverse, should be in forward-anchor state
    else:
        ok, msg = reverse_check_fn(disk)  # After forward, should be in reverse-anchor state
    print(f"  {label} disk state: {msg}")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Step 2 wiring: task-state primitive hooks in loop.metta + import + artifact_1"
    )
    parser.add_argument("--apply", action="store_true",
                        help="Actually write changes. Default is dry-run.")
    parser.add_argument("--reverse", action="store_true",
                        help="Reverse the edits. Combine with --apply to write.")
    args = parser.parse_args()

    direction = "REVERSE" if args.reverse else "APPLY"
    print(f"\n========== STEP 2 WIRING: {direction} ==========")

    # File existence
    if not all([
        check_file_exists(LIB_CR_PATH, "lib_clarity_reasoning"),
        check_file_exists(LOOP_PATH, "loop.metta"),
        check_file_exists(ARTIFACT1_PATH, "artifact_1"),
    ]):
        return 1

    # Process each file: simulate, check, accumulate results
    ok_lib, lib_orig, lib_sim = process_file(
        LIB_CR_PATH, LIB_CR_BAK,
        simulate_lib_cr_forward, simulate_lib_cr_reverse,
        expected_line_delta_forward=3,
        args=args, label="lib_clarity_reasoning.metta",
        check_parens=True,
        forward_state_check_fn=lib_cr_forward_state_ok,
        reverse_state_check_fn=lib_cr_reverse_state_ok,
    )
    if not ok_lib:
        return 1

    ok_loop, loop_orig, loop_sim = process_file(
        LOOP_PATH, LOOP_BAK,
        simulate_loop_forward, simulate_loop_reverse,
        expected_line_delta_forward=5,  # 4 hooks + 1 for the initLoop comment line
        args=args, label="loop.metta",
        check_parens=True,
        forward_state_check_fn=loop_forward_state_ok,
        reverse_state_check_fn=loop_reverse_state_ok,
    )
    if not ok_loop:
        return 1

    # artifact_1 expected line delta: count lines in ARTIFACT1_NEW_SUBSECTION
    artifact1_delta = ARTIFACT1_NEW_SUBSECTION.count("\n")
    ok_art, art_orig, art_sim = process_file(
        ARTIFACT1_PATH, ARTIFACT1_BAK,
        simulate_artifact1_forward, simulate_artifact1_reverse,
        expected_line_delta_forward=artifact1_delta,
        args=args, label="artifact_1.md",
        check_parens=False,  # markdown, no paren count
        forward_state_check_fn=artifact1_forward_state_ok,
        reverse_state_check_fn=artifact1_reverse_state_ok,
    )
    if not ok_art:
        return 1

    print("\n========== DIFF PREVIEWS ==========")
    print(diff_preview_first_change(lib_orig, lib_sim, "lib_clarity_reasoning.metta", context=2))
    print()
    print(diff_preview_first_change(loop_orig, loop_sim, "loop.metta (first changed region)", context=2))
    print()
    print(diff_preview_first_change(art_orig, art_sim, "artifact_1.md", context=1))

    if not args.apply:
        print("\n========== DRY-RUN COMPLETE ==========")
        print("All checks pass. Re-run with --apply to write.")
        return 0

    # Forward: backup before writing
    if not args.reverse:
        for path, bak in [(LIB_CR_PATH, LIB_CR_BAK), (LOOP_PATH, LOOP_BAK), (ARTIFACT1_PATH, ARTIFACT1_BAK)]:
            if bak.exists():
                print(f"WARNING: backup {bak} exists; overwriting.")
            bak.write_text(path.read_text())
            print(f"Backup written: {bak}")

    # Write all files
    print("\n========== WRITING ==========")
    LIB_CR_PATH.write_text(lib_sim)
    print(f"Wrote: {LIB_CR_PATH}")
    LOOP_PATH.write_text(loop_sim)
    print(f"Wrote: {LOOP_PATH}")
    ARTIFACT1_PATH.write_text(art_sim)
    print(f"Wrote: {ARTIFACT1_PATH}")

    # Post-write disk verification
    print("\n========== DISK VERIFICATION ==========")
    v1 = verify_disk(LIB_CR_PATH, args, "lib_clarity_reasoning.metta",
                     lib_cr_forward_state_ok, lib_cr_reverse_state_ok, check_parens=True)
    v2 = verify_disk(LOOP_PATH, args, "loop.metta",
                     loop_forward_state_ok, loop_reverse_state_ok, check_parens=True)
    v3 = verify_disk(ARTIFACT1_PATH, args, "artifact_1.md",
                     artifact1_forward_state_ok, artifact1_reverse_state_ok, check_parens=False)

    if not (v1 and v2 and v3):
        print("\nDISK VERIFICATION FAILED. File(s) may be in inconsistent state.")
        if not args.reverse:
            print("Restore:")
            print(f"  cp {LIB_CR_BAK} {LIB_CR_PATH}")
            print(f"  cp {LOOP_BAK} {LOOP_PATH}")
            print(f"  cp {ARTIFACT1_BAK} {ARTIFACT1_PATH}")
        return 1

    print("\n========== STEP 2 WIRING COMPLETE ==========")
    print("All 6 edits applied. All checks pass.")
    if not args.reverse:
        print("\nNext: container rebuild and verify atoms update per cycle.")
        print("  docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw && sleep 15 && docker logs clarity_omega 2>&1 | tail -80")
    return 0


if __name__ == "__main__":
    sys.exit(main())
