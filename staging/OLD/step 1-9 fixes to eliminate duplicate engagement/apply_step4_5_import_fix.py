#!/usr/bin/env python3
"""
Apply script: Step 4.5 import fix -- register idle_cycle_detector.metta
in lib_clarity_reasoning.metta.

Discovered post-Step-4.5 apply: the substrate file was written correctly
to soul/idle_cycle_detector.metta, but lib_clarity_reasoning.metta did
NOT have an import line for it. Result: the file's functions were never
loaded into the MeTTa runtime, so (idle-pattern-block) and
(do-update-idle-pattern!) silently no-op'd. CHARS_SENT rendered
['idle-pattern-block'] as a literal symbol-list instead of evaluating
to the formatted block text.

This single-file patch adds the import line. Substrate file unchanged;
only the registration was missing.

Going forward (F21): future apply scripts that add new soul/*.metta
files must include the import-registration as part of the script.

The edit:
  Insert two lines (comment + import directive) after the task_state_writers
  import at line 55, before the behavioral_guidance import at line 58.

Reversibility:
  --apply writes the change with .bak.step4_5_import_fix backup
  --reverse --apply removes the import lines

Behavioral verification after apply + rebuild:
  - Container reaches first cycle without parse errors
  - IDLE-PATTERN block renders correctly (not as ['idle-pattern-block'])
  - First-cycle bootstrap: (idle-pattern productive 0)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


# ============================================================================
# FILE PATHS
# ============================================================================

LCR_PATH = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta")
LCR_BAK = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta.bak.step4_5_import_fix")


# ============================================================================
# EDIT: insert idle_cycle_detector import after task_state_writers import
# ============================================================================

LCR_ANCHOR = ''';; Task-state writers: side-effecting do-*! functions for task-state atoms
!(import! &self (library omegaclaw ./soul/task_state_writers))'''

LCR_NEW = ''';; Task-state writers: side-effecting do-*! functions for task-state atoms
!(import! &self (library omegaclaw ./soul/task_state_writers))

;; Idle cycle detector: send-burst detection for duplicate-engagement awareness (Step 4.5)
!(import! &self (library omegaclaw ./soul/idle_cycle_detector))'''


# ============================================================================
# HELPERS (subset of standard pattern, no paren check needed for this file)
# ============================================================================

def find_target_substring_count(text, target):
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

def simulate_forward(content):
    if find_target_substring_count(content, LCR_ANCHOR) != 1:
        raise RuntimeError("forward: LCR_ANCHOR not found exactly once.")
    if "./soul/idle_cycle_detector" in content:
        raise RuntimeError("forward: idle_cycle_detector import already present.")
    return content.replace(LCR_ANCHOR, LCR_NEW, 1)


def simulate_reverse(content):
    if find_target_substring_count(content, LCR_NEW) != 1:
        raise RuntimeError("reverse: LCR_NEW not found exactly once.")
    return content.replace(LCR_NEW, LCR_ANCHOR, 1)


# ============================================================================
# STATE CHECKS
# ============================================================================

def forward_state_ok(content):
    has_anchor = find_target_substring_count(content, LCR_ANCHOR) == 1
    no_new = "./soul/idle_cycle_detector" not in content
    ok = has_anchor and no_new
    msg = f"anchor={has_anchor}, new_absent={no_new} -> {'OK' if ok else 'FAIL'}"
    return ok, msg


def reverse_state_ok(content):
    has_new = find_target_substring_count(content, LCR_NEW) == 1
    msg = f"new_block_present={has_new} -> {'OK' if has_new else 'FAIL'}"
    return has_new, msg


# ============================================================================
# DIFF PREVIEW
# ============================================================================

def diff_preview(old, new, label, context=2):
    old_lines = old.splitlines()
    new_lines = new.splitlines()
    differ_start = None
    for i in range(min(len(old_lines), len(new_lines))):
        if old_lines[i] != new_lines[i]:
            differ_start = i
            break
    if differ_start is None:
        if len(old_lines) == len(new_lines):
            return f"--- {label}: NO CHANGES ---"
        differ_start = min(len(old_lines), len(new_lines))
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

def main():
    parser = argparse.ArgumentParser(description="Step 4.5 import fix: register idle_cycle_detector")
    parser.add_argument("--apply", action="store_true",
                        help="Write changes. Default is dry-run.")
    parser.add_argument("--reverse", action="store_true",
                        help="Reverse the edit.")
    args = parser.parse_args()

    direction = "REVERSE" if args.reverse else "APPLY"
    print(f"\n========== STEP 4.5 IMPORT FIX: {direction} ==========")

    if not LCR_PATH.exists():
        print(f"  ERROR: {LCR_PATH} not found.")
        return 1

    content = LCR_PATH.read_text()
    pre_lines = len(content.splitlines())
    print(f"\n>>> {LCR_PATH} <<<")
    print(f"  Pre-edit lines: {pre_lines}")

    if args.reverse:
        ok, msg = reverse_state_ok(content)
    else:
        ok, msg = forward_state_ok(content)
    print(f"  State check: {msg}")
    if not ok:
        print(f"  STATE CHECK FAILED. Aborting.")
        return 1

    try:
        if args.reverse:
            simulated = simulate_reverse(content)
        else:
            simulated = simulate_forward(content)
    except RuntimeError as exc:
        print(f"  SIMULATION FAILED: {exc}")
        return 1

    post_lines = len(simulated.splitlines())
    line_delta = post_lines - pre_lines
    expected = 3 if not args.reverse else -3  # 3 new lines: blank line + comment + import
    c_lines = "OK" if line_delta == expected else "FAIL"
    print(f"  Line delta: {line_delta} (expected {expected}) ({c_lines})")
    if c_lines != "OK":
        print(f"  LINE DELTA FAILED. Aborting.")
        return 1

    print("\n========== DIFF PREVIEW ==========")
    print(diff_preview(content, simulated, str(LCR_PATH), context=2))

    flag_str = "--reverse --apply" if args.reverse else "--apply"
    reverse_str = "--apply" if args.reverse else "--reverse --apply"
    action_word = "REVERSE" if args.reverse else "APPLY"

    print(f"\n========== SUMMARY: WHAT {flag_str} WILL DO ==========")
    print(f"Direction: {action_word}")
    print(f"Backup suffix: .bak.step4_5_import_fix (created on apply)")
    print()
    print(f"  {LCR_PATH}")
    print(f"    Edit: Insert import line for soul/idle_cycle_detector after task_state_writers import")
    print(f"    Lines: {pre_lines} -> {post_lines} ({line_delta:+d})")
    print(f"    Backup target: {LCR_BAK}")
    print()
    print(f"Total edits: 1 (single-file import registration)")
    print(f"Reversibility: python3 staging/apply_step4_5_import_fix.py {reverse_str}")
    print(f"Post-apply container rebuild required (--no-cache for soul/ changes)")

    if not args.apply:
        print("\n========== DRY-RUN COMPLETE ==========")
        print(f"All checks pass. Re-run with {flag_str} to write the change summarized above.")
        return 0

    # Apply mode
    if not args.reverse:
        if LCR_BAK.exists():
            print(f"WARNING: backup {LCR_BAK} exists; overwriting.")
        LCR_BAK.write_text(content)
        print(f"Backup written: {LCR_BAK}")

    print("\n========== WRITING ==========")
    LCR_PATH.write_text(simulated)
    print(f"Wrote: {LCR_PATH}")

    print("\n========== DISK VERIFICATION ==========")
    disk = LCR_PATH.read_text()
    if args.reverse:
        ok, msg = forward_state_ok(disk)
    else:
        ok, msg = reverse_state_ok(disk)
    print(f"  {LCR_PATH} state: {msg}")
    if not ok:
        print("DISK VERIFICATION FAILED.")
        return 1

    print("\n========== STEP 4.5 IMPORT FIX COMPLETE ==========")
    if not args.reverse:
        print("\nNext: container rebuild and verify IDLE-PATTERN block renders correctly.")
        print("  docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw && sleep 15 && docker logs clarity_omega 2>&1 | tail -50")
        print("\nLook for IDLE-PATTERN block in CHARS_SENT showing:")
        print("  (idle-pattern productive 0)")
        print("  Summary: Idle-pattern verdict: productive. 0 send-class actions in last 10 cycles.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
