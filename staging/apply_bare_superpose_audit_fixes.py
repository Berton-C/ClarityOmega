#!/usr/bin/env python3
"""
Apply script: bare-superpose audit fixes (defect-class closure).

Purpose
-------
The corner-gate v3 stability investigation proved the durable fact: any
superpose iteration inside a let* must be collapse-wrapped unless downstream
multiplication is intended (N members means N open Prolog choice points that
escape to the caller; see substrate crash knowledge append 2026-07-29).
A repo-wide audit found two remaining sites carrying the pre-2026-06-04
shape. This script closes the class.

Audit result (2026-07-29)
-------------------------
- FIX  soul/corner_gap/cycle_continuity_probe_writers.metta
       do-update-corner-graded! window prune: bare superpose over the
       collapsed $to-remove list. Caller currently dormant (loop calls
       populate-coupling-verdict, not this writer), but the file is on
       disk in bind-mounted soul/ and the defect is latent. The certified
       fixed shape already exists in this same file (do-clear-cycle-pfn!,
       2026-06-04 fix comment block).
- FIX  soul/agency_balance_guard_writers.metta
       do-clear-agency-balance!: empty-guarded, but the non-empty branch
       superposes the collapsed $existing list bare. Live path (called
       every cycle via do-update-agency-balance!). Latent severity: the
       singleton normally has one member, but any duplication multiplies.
- CLEAN soul/idle_cycle_detector_writers.metta
       do-clear-idle-pattern! removes via car-atom with an empty guard;
       no superpose anywhere in the file. Audited clean, no edit.

The two edits
-------------
Edit 1: cycle_continuity_probe_writers.metta, $_prune binding of
  do-update-corner-graded! replaced with the guard-empty + collapse-wrap
  shape (identical to the populator fix in commit 4ef1116). Line delta +1.

Edit 2: agency_balance_guard_writers.metta, whole do-clear-agency-balance!
  function replaced: non-empty branch collapse-wrapped, one solution.
  Line delta -1.

Net change
----------
- cycle_continuity_probe_writers.metta: +1 line; paren delta 0
- agency_balance_guard_writers.metta:   -1 line; paren delta 0

Usage
-----
Dry-run (default):
    python3 staging/apply_bare_superpose_audit_fixes.py
Apply:
    python3 staging/apply_bare_superpose_audit_fixes.py --apply
Reverse (after apply):
    python3 staging/apply_bare_superpose_audit_fixes.py --reverse --apply

Pre-conditions
--------------
- Corner-gate v3 stability fixes applied (commit 4ef1116 lineage)
- Container restartable at convenience (soul/ is bind-mounted; changes
  take effect on next restart; no urgency, both defects latent)

Backup files (forward apply only)
---------------------------------
- soul/corner_gap/cycle_continuity_probe_writers.metta.bak.superpose_audit
- soul/agency_balance_guard_writers.metta.bak.superpose_audit
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# ============================================================================
# FILE PATHS
# ============================================================================

GRADED_PATH = Path("soul/corner_gap/cycle_continuity_probe_writers.metta")
GRADED_BAK = Path("soul/corner_gap/cycle_continuity_probe_writers.metta.bak.superpose_audit")

AGENCY_PATH = Path("soul/agency_balance_guard_writers.metta")
AGENCY_BAK = Path("soul/agency_balance_guard_writers.metta.bak.superpose_audit")

# ============================================================================
# EDIT 1: graded window prune (cycle_continuity_probe_writers.metta)
# ============================================================================

GRADED_OLD = (
    "          ($_prune       (let $old (superpose $to-remove)\n"
    "                                   (if (== $old ())\n"
    "                                       ()\n"
    "                                       (remove-atom &self $old))))"
)
GRADED_NEW = (
    "          ($_prune       (if (== $to-remove ())\n"
    "                                   ()\n"
    "                                   (let $_drained (collapse (let $old (superpose $to-remove)\n"
    "                                                                 (if (== $old ()) () (remove-atom &self $old))))\n"
    "                                      ())))"
)

# ============================================================================
# EDIT 2: agency clearer (agency_balance_guard_writers.metta)
# ============================================================================

AGENCY_OLD = (
    "(= (do-clear-agency-balance!)\n"
    "   (let $existing (collapse (match &self (agency-balance $v $p $s) (agency-balance $v $p $s)))\n"
    "      (if (== $existing ())\n"
    "          _\n"
    "          (let $old (superpose $existing)\n"
    "                    (if (== $old ())\n"
    "                        ()\n"
    "                        (remove-atom &self $old))))))"
)
AGENCY_NEW = (
    "(= (do-clear-agency-balance!)\n"
    "   (let $existing (collapse (match &self (agency-balance $v $p $s) (agency-balance $v $p $s)))\n"
    "      (if (== $existing ())\n"
    "          _\n"
    "          (let $_drained (collapse (let $old (superpose $existing)\n"
    "                                        (if (== $old ()) () (remove-atom &self $old))))\n"
    "             _))))"
)

# ============================================================================
# HELPERS (per apply_task_state_step2_wiring.py template)
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

def simulate_graded_forward(content: str) -> str:
    if find_target_substring_count(content, GRADED_OLD) != 1:
        raise RuntimeError("graded forward: $_prune block not found exactly once (byte drift?).")
    return content.replace(GRADED_OLD, GRADED_NEW, 1)


def simulate_graded_reverse(content: str) -> str:
    if find_target_substring_count(content, GRADED_NEW) != 1:
        raise RuntimeError("graded reverse: collapse-wrapped block not found exactly once.")
    return content.replace(GRADED_NEW, GRADED_OLD, 1)


def simulate_agency_forward(content: str) -> str:
    if find_target_substring_count(content, AGENCY_OLD) != 1:
        raise RuntimeError("agency forward: clearer function not found exactly once (byte drift?).")
    return content.replace(AGENCY_OLD, AGENCY_NEW, 1)


def simulate_agency_reverse(content: str) -> str:
    if find_target_substring_count(content, AGENCY_NEW) != 1:
        raise RuntimeError("agency reverse: collapse-wrapped clearer not found exactly once.")
    return content.replace(AGENCY_NEW, AGENCY_OLD, 1)


# ============================================================================
# STATE CHECK PREDICATES
# ============================================================================

def graded_forward_state_ok(content: str) -> tuple[bool, str]:
    a = find_target_substring_count(content, GRADED_OLD) == 1
    n = find_target_substring_count(content, GRADED_NEW) == 0
    ok = a and n
    return ok, f"old prune present={a}, new absent={n} -> {'OK' if ok else 'FAIL'}"


def graded_reverse_state_ok(content: str) -> tuple[bool, str]:
    n = find_target_substring_count(content, GRADED_NEW) == 1
    return n, f"collapse-wrapped prune present={n} -> {'OK' if n else 'FAIL'}"


def agency_forward_state_ok(content: str) -> tuple[bool, str]:
    a = find_target_substring_count(content, AGENCY_OLD) == 1
    n = find_target_substring_count(content, AGENCY_NEW) == 0
    ok = a and n
    return ok, f"old clearer present={a}, new absent={n} -> {'OK' if ok else 'FAIL'}"


def agency_reverse_state_ok(content: str) -> tuple[bool, str]:
    n = find_target_substring_count(content, AGENCY_NEW) == 1
    return n, f"collapse-wrapped clearer present={n} -> {'OK' if n else 'FAIL'}"


# ============================================================================
# DIFF PREVIEW
# ============================================================================

def diff_preview_first_change(old: str, new: str, label: str, context: int = 3) -> str:
    old_lines = old.splitlines()
    new_lines = new.splitlines()
    differ_start = None
    for i in range(min(len(old_lines), len(new_lines))):
        if old_lines[i] != new_lines[i]:
            differ_start = i
            break
    if differ_start is None:
        if len(old_lines) == len(new_lines):
            return f"--- {label}: NO CHANGES DETECTED ---"
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

def check_file_exists(path: Path, label: str) -> bool:
    if not path.exists():
        print(f"ERROR: {label} not found at {path}. Run from repo root.")
        return False
    return True


def process_file(path, bak_path, simulate_fn, simulate_reverse_fn,
                 expected_line_delta_forward, args, label, check_parens,
                 forward_state_check_fn, reverse_state_check_fn):
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
    if args.reverse:
        state_ok, state_msg = reverse_state_check_fn(content)
    else:
        state_ok, state_msg = forward_state_check_fn(content)
    print(f"  State check: {state_msg}")
    if not state_ok:
        print(f"  STATE CHECK FAILED for {label}. Aborting.")
        return False, content, ""
    try:
        simulated = simulate_reverse_fn(content) if args.reverse else simulate_fn(content)
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


def verify_disk(path, args, label, forward_check_fn, reverse_check_fn, check_parens):
    disk = path.read_text()
    if check_parens:
        o, c = code_aware_paren_count(disk)
        d = o - c
        ok_p = d == 0
        print(f"  {label} disk paren: opens={o} closes={c} delta={d} ({'OK' if ok_p else 'FAIL'})")
        if not ok_p:
            return False
    if args.reverse:
        ok, msg = forward_check_fn(disk)
    else:
        ok, msg = reverse_check_fn(disk)
    print(f"  {label} disk state: {msg}")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bare-superpose audit fixes: graded window prune + agency clearer"
    )
    parser.add_argument("--apply", action="store_true",
                        help="Actually write changes. Default is dry-run.")
    parser.add_argument("--reverse", action="store_true",
                        help="Reverse the edits. Combine with --apply to write.")
    args = parser.parse_args()

    direction = "REVERSE" if args.reverse else "APPLY"
    print(f"\n========== SUPERPOSE AUDIT FIXES: {direction} ==========")

    if not all([
        check_file_exists(GRADED_PATH, "cycle_continuity_probe_writers.metta"),
        check_file_exists(AGENCY_PATH, "agency_balance_guard_writers.metta"),
    ]):
        return 1

    ok_g, g_orig, g_sim = process_file(
        GRADED_PATH, GRADED_BAK,
        simulate_graded_forward, simulate_graded_reverse,
        expected_line_delta_forward=1,
        args=args, label="cycle_continuity_probe_writers.metta",
        check_parens=True,
        forward_state_check_fn=graded_forward_state_ok,
        reverse_state_check_fn=graded_reverse_state_ok,
    )
    if not ok_g:
        return 1

    ok_a, a_orig, a_sim = process_file(
        AGENCY_PATH, AGENCY_BAK,
        simulate_agency_forward, simulate_agency_reverse,
        expected_line_delta_forward=-1,
        args=args, label="agency_balance_guard_writers.metta",
        check_parens=True,
        forward_state_check_fn=agency_forward_state_ok,
        reverse_state_check_fn=agency_reverse_state_ok,
    )
    if not ok_a:
        return 1

    print("\n========== DIFF PREVIEWS ==========")
    print(diff_preview_first_change(g_orig, g_sim, "cycle_continuity_probe_writers.metta", context=2))
    print()
    print(diff_preview_first_change(a_orig, a_sim, "agency_balance_guard_writers.metta", context=2))

    if not args.apply:
        print("\n========== DRY-RUN COMPLETE ==========")
        print("All checks pass. Re-run with --apply to write.")
        return 0

    if not args.reverse:
        for path, bak in [(GRADED_PATH, GRADED_BAK), (AGENCY_PATH, AGENCY_BAK)]:
            if bak.exists():
                print(f"WARNING: backup {bak} exists; overwriting.")
            bak.write_text(path.read_text())
            print(f"Backup written: {bak}")

    print("\n========== WRITING ==========")
    GRADED_PATH.write_text(g_sim)
    print(f"Wrote: {GRADED_PATH}")
    AGENCY_PATH.write_text(a_sim)
    print(f"Wrote: {AGENCY_PATH}")

    print("\n========== DISK VERIFICATION ==========")
    v1 = verify_disk(GRADED_PATH, args, "cycle_continuity_probe_writers.metta",
                     graded_forward_state_ok, graded_reverse_state_ok, check_parens=True)
    v2 = verify_disk(AGENCY_PATH, args, "agency_balance_guard_writers.metta",
                     agency_forward_state_ok, agency_reverse_state_ok, check_parens=True)

    if not (v1 and v2):
        print("\nDISK VERIFICATION FAILED. File(s) may be in inconsistent state.")
        if not args.reverse:
            print("Restore:")
            print(f"  cp {GRADED_BAK} {GRADED_PATH}")
            print(f"  cp {AGENCY_BAK} {AGENCY_PATH}")
        return 1

    print("\n========== SUPERPOSE AUDIT FIXES COMPLETE ==========")
    print("Both edits applied. All checks pass. Defect class closed.")
    if not args.reverse:
        print("\nDeploy at convenience (soul/ is bind-mounted; effective on next restart):")
        print("  docker compose restart clarityclaw")
    return 0


if __name__ == "__main__":
    sys.exit(main())
