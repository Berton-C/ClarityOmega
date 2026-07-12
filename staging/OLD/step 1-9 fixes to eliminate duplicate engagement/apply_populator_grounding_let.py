#!/usr/bin/env python3
"""
Apply script: F1.1 — let-binding shape that forces (repr ...) to evaluate
before the populator's add-atom call.

Purpose
-------
F1 (commit 7b1b684) wrapped $description with (repr $description) at the
populator's add-atom call. Genesis re-enable test (commit e6f1a20) confirmed
this did NOT prevent the crash: add-atom stores its argument unreduced, so
the (repr $description) literal compound was stored as-is, with unbound
variables intact one level deeper.

F1.1 fixes this by introducing a let* binding that forces repr to evaluate
before add-atom is called. The bound variable $rendered receives the
evaluated string; add-atom stores that string, not a literal call form.

The change
----------
Insert one new let* binding line after the existing $description binding,
and unwrap line 45's (repr $description) back to a plain $rendered reference.

From (current F1 state):
    (let* (($action-type  (classify-cycle-action-type $sexpr $msgnew))
           ($description  (classify-cycle-description $sexpr))
           ($_diag (if ...))
           ($_assert      (add-atom &self (recent-action $cycle-id $action-type (repr $description))))
           ...

To (F1.1 state):
    (let* (($action-type  (classify-cycle-action-type $sexpr $msgnew))
           ($description  (classify-cycle-description $sexpr))
           ($rendered     (repr $description))
           ($_diag (if ...))
           ($_assert      (add-atom &self (recent-action $cycle-id $action-type $rendered)))
           ...

Net change
----------
- 1 line added (new $rendered binding)
- 1 line modified (line 45, (repr $description) -> $rendered)
- Paren delta: 0 (new line +2 opens / +2 closes; modified line -1 open / -1 close
  for the removed (repr ...) wrap; net +1 open / +1 close)

Mechanism (verified at all layers prior to drafting this script)
----------------------------------------------------------------
- let* evaluates bindings in order
- $rendered binds to the result of evaluating (repr $description)
- repr is a Prolog-backed predicate (/PeTTa/src/metta.pl:29)
- repr evaluation produces a ground string atom
- add-atom receives the bound $rendered, sees the string, stores it
- match retrieval returns the string; no re-parse

Verification gap that F1 missed
-------------------------------
F1 placed (repr $description) inside add-atom's argument. add-atom is a
substrate predicate that does NOT evaluate its argument before storing
(verified empirically by genesis re-enable test cycle 1, where the stored
atom contained a literal (repr (metta (match ...))) compound with unbound
variable $_537060 inside).

Usage
-----
Dry-run (default):
    python3 staging/apply_populator_grounding_let.py

Apply:
    python3 staging/apply_populator_grounding_let.py --apply

Reverse (after apply, returns to F1 state):
    python3 staging/apply_populator_grounding_let.py --reverse --apply

Pre-conditions
--------------
This script EXPECTS F1 to be applied (line 45 has (repr $description) wrap).
If applied against the pre-F1 state, the OLD_LINE45 check will fail.

Backup file (forward apply only): soul/recent_action_populator.metta.bak.f1_1_letbinding
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

POPULATOR_PATH = Path("soul/recent_action_populator.metta")
BACKUP_PATH = Path("soul/recent_action_populator.metta.bak.f1_1_letbinding")

# Edit 1: Insert new $rendered binding line AFTER the $description binding.
# We target the $description line, replace it with itself + a new line.
DESC_LINE = "          ($description  (classify-cycle-description $sexpr))"
RENDERED_LINE = "          ($rendered     (repr $description))"

# Forward direction:
#   $description line -> $description line + $rendered line
# Reverse direction:
#   $description line + $rendered line -> $description line
EDIT1_OLD_FORWARD = DESC_LINE + "\n"
EDIT1_NEW_FORWARD = DESC_LINE + "\n" + RENDERED_LINE + "\n"

# Edit 2: Unwrap line 45 from (repr $description) to plain $rendered.
OLD_LINE45_F1 = "($_assert      (add-atom &self (recent-action $cycle-id $action-type (repr $description))))"
NEW_LINE45_F1_1 = "($_assert      (add-atom &self (recent-action $cycle-id $action-type $rendered)))"


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
    """Count occurrences of a multi-line block exactly."""
    count = 0
    start = 0
    while True:
        idx = text.find(target, start)
        if idx == -1:
            break
        count += 1
        start = idx + 1
    return count


def simulate_forward(content: str) -> str:
    """Apply F1 -> F1.1 transformation."""
    # Edit 1: insert $rendered binding line after $description
    block_count = find_target_substring_count(content, EDIT1_OLD_FORWARD)
    if block_count != 1:
        raise RuntimeError(
            f"Edit 1 forward: expected exactly 1 occurrence of $description line, found {block_count}."
        )
    content = content.replace(EDIT1_OLD_FORWARD, EDIT1_NEW_FORWARD, 1)

    # Edit 2: unwrap line 45
    line45_matches = find_target_lines(content, OLD_LINE45_F1)
    if len(line45_matches) != 1:
        raise RuntimeError(
            f"Edit 2 forward: expected exactly 1 line matching F1 form on line 45, found {line45_matches}."
        )
    out_lines = []
    replaced = 0
    for line in content.splitlines(keepends=True):
        if line.strip() == OLD_LINE45_F1.strip():
            leading = line[: len(line) - len(line.lstrip())]
            trailing = ""
            if line.endswith("\r\n"):
                trailing = "\r\n"
            elif line.endswith("\n"):
                trailing = "\n"
            out_lines.append(f"{leading}{NEW_LINE45_F1_1}{trailing}")
            replaced += 1
        else:
            out_lines.append(line)
    if replaced != 1:
        raise RuntimeError(f"Edit 2 forward: line replace count = {replaced}.")
    return "".join(out_lines)


def simulate_reverse(content: str) -> str:
    """Apply F1.1 -> F1 transformation."""
    # Edit 1 reverse: remove $rendered binding line
    edit1_old_reverse = DESC_LINE + "\n" + RENDERED_LINE + "\n"
    edit1_new_reverse = DESC_LINE + "\n"
    block_count = find_target_substring_count(content, edit1_old_reverse)
    if block_count != 1:
        raise RuntimeError(
            f"Edit 1 reverse: expected exactly 1 occurrence of $description+$rendered block, found {block_count}."
        )
    content = content.replace(edit1_old_reverse, edit1_new_reverse, 1)

    # Edit 2 reverse: re-wrap line 45 with (repr ...)
    line_matches = find_target_lines(content, NEW_LINE45_F1_1)
    if len(line_matches) != 1:
        raise RuntimeError(
            f"Edit 2 reverse: expected exactly 1 line matching F1.1 form, found {line_matches}."
        )
    out_lines = []
    replaced = 0
    for line in content.splitlines(keepends=True):
        if line.strip() == NEW_LINE45_F1_1.strip():
            leading = line[: len(line) - len(line.lstrip())]
            trailing = ""
            if line.endswith("\r\n"):
                trailing = "\r\n"
            elif line.endswith("\n"):
                trailing = "\n"
            out_lines.append(f"{leading}{OLD_LINE45_F1}{trailing}")
            replaced += 1
        else:
            out_lines.append(line)
    if replaced != 1:
        raise RuntimeError(f"Edit 2 reverse: line replace count = {replaced}.")
    return "".join(out_lines)


def diff_preview(old_content: str, new_content: str, context: int = 3) -> str:
    old_lines = old_content.splitlines()
    new_lines = new_content.splitlines()

    # Find the range where they differ
    differ_start = None
    differ_end_old = None
    differ_end_new = None

    # Walk both forward to find first divergence
    min_len = min(len(old_lines), len(new_lines))
    for i in range(min_len):
        if old_lines[i] != new_lines[i]:
            differ_start = i
            break
    if differ_start is None:
        if len(old_lines) == len(new_lines):
            return "(no change)"
        differ_start = min_len

    # Walk both backward to find last divergence
    old_back = len(old_lines) - 1
    new_back = len(new_lines) - 1
    while old_back > differ_start and new_back > differ_start and old_lines[old_back] == new_lines[new_back]:
        old_back -= 1
        new_back -= 1
    differ_end_old = old_back
    differ_end_new = new_back

    out = ["--- diff preview ---"]
    start = max(0, differ_start - context)
    # show context before
    for i in range(start, differ_start):
        out.append(f"  {old_lines[i]}")
    # show old block
    for i in range(differ_start, differ_end_old + 1):
        out.append(f"- {old_lines[i]}")
    # show new block
    for i in range(differ_start, differ_end_new + 1):
        out.append(f"+ {new_lines[i]}")
    # show context after
    end_old = min(len(old_lines), differ_end_old + 1 + context)
    for i in range(differ_end_old + 1, end_old):
        out.append(f"  {old_lines[i]}")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="F1.1 let-binding apply script")
    parser.add_argument("--apply", action="store_true",
                        help="Actually write changes. Default is dry-run.")
    parser.add_argument("--reverse", action="store_true",
                        help="Reverse the edit (F1.1 -> F1). Combine with --apply to write.")
    args = parser.parse_args()

    if not POPULATOR_PATH.exists():
        print(f"ERROR: {POPULATOR_PATH} not found. Run from repo root.")
        return 1

    content = POPULATOR_PATH.read_text()
    direction = "REVERSE (F1.1 -> F1)" if args.reverse else "APPLY (F1 -> F1.1)"
    print(f"\n>>> {direction} <<<")

    pre_o, pre_c = code_aware_paren_count(content)
    pre_d = pre_o - pre_c
    pre_lines = len(content.splitlines())

    # Pre-edit checks
    print("\n=== PRE-EDIT CHECKS ===")
    print(f"  1. file path:           {POPULATOR_PATH}")
    c_pre_paren = "OK" if pre_d == 0 else "FAIL"
    print(f"  2. paren count pre:     opens={pre_o} closes={pre_c} delta={pre_d} ({c_pre_paren})")
    print(f"  3. line count pre:      {pre_lines}")

    if args.reverse:
        # Verify F1.1 state present
        new45 = find_target_lines(content, NEW_LINE45_F1_1)
        rendered = find_target_lines(content, RENDERED_LINE)
        c_state = "OK" if (len(new45) == 1 and len(rendered) == 1) else "FAIL"
        print(f"  4. F1.1 state present:  line45={new45} rendered={rendered} ({c_state})")
        if c_state != "OK":
            print("\nReverse pre-check failed. Aborting.")
            return 1
    else:
        # Verify F1 state present (line 45 has (repr ...) wrap)
        old45 = find_target_lines(content, OLD_LINE45_F1)
        rendered = find_target_lines(content, RENDERED_LINE)
        c_state = "OK" if (len(old45) == 1 and len(rendered) == 0) else "FAIL"
        print(f"  4. F1 state present:    line45_F1={old45} rendered_already={rendered} ({c_state})")
        if c_state != "OK":
            print("\nForward pre-check failed. Expected F1 state (line 45 has (repr ...) wrap, no $rendered binding).")
            return 1

    if c_pre_paren != "OK":
        print("\nParen count failed pre-edit. Aborting.")
        return 1

    # Simulate
    try:
        if args.reverse:
            simulated = simulate_reverse(content)
            expected_line_delta = -1
        else:
            simulated = simulate_forward(content)
            expected_line_delta = 1
    except RuntimeError as exc:
        print(f"\nSimulation failed: {exc}")
        return 1

    post_o, post_c = code_aware_paren_count(simulated)
    post_d = post_o - post_c
    post_lines = len(simulated.splitlines())
    line_delta = post_lines - pre_lines

    print("\n=== POST-EDIT (SIMULATED) CHECKS ===")
    c5 = "OK" if post_d == 0 else "FAIL"
    print(f"  5. paren count post:    opens={post_o} closes={post_c} delta={post_d} ({c5})")
    c6 = "OK" if (post_d - pre_d) == 0 else "FAIL"
    print(f"  6. paren delta change:  {post_d - pre_d} ({c6})")
    c7 = "OK" if line_delta == expected_line_delta else "FAIL"
    print(f"  7. line delta:          {line_delta} (expected {expected_line_delta}) ({c7})")

    if args.reverse:
        # After reverse, we should be back at F1 state
        old45_after = find_target_lines(simulated, OLD_LINE45_F1)
        rendered_after = find_target_lines(simulated, RENDERED_LINE)
        c8 = "OK" if (len(old45_after) == 1 and len(rendered_after) == 0) else "FAIL"
        print(f"  8. simulated state F1:  line45_F1={old45_after} rendered={rendered_after} ({c8})")
    else:
        # After forward, we should be at F1.1 state
        new45_after = find_target_lines(simulated, NEW_LINE45_F1_1)
        rendered_after = find_target_lines(simulated, RENDERED_LINE)
        c8 = "OK" if (len(new45_after) == 1 and len(rendered_after) == 1) else "FAIL"
        print(f"  8. simulated state F1.1: line45_F1.1={new45_after} rendered={rendered_after} ({c8})")

    if c5 != "OK" or c6 != "OK" or c7 != "OK" or c8 != "OK":
        print("\nPost-edit simulation checks failed. Aborting; no disk write.")
        return 1

    print("\n" + diff_preview(content, simulated))

    if not args.apply:
        print("\nDry-run complete. All checks pass. Re-run with --apply to write.")
        return 0

    # Backup (only on forward apply)
    if not args.reverse:
        if BACKUP_PATH.exists():
            print(f"\nWARNING: backup {BACKUP_PATH} exists; overwriting.")
        BACKUP_PATH.write_text(content)
        print(f"\nBackup written: {BACKUP_PATH}")

    # Write
    POPULATOR_PATH.write_text(simulated)
    print(f"Wrote: {POPULATOR_PATH}")

    # Post-write verification
    disk = POPULATOR_PATH.read_text()
    disk_o, disk_c = code_aware_paren_count(disk)
    disk_d = disk_o - disk_c
    print("\n=== POST-WRITE DISK VERIFICATION ===")
    d1 = "OK" if disk_d == 0 else "FAIL"
    print(f"  paren count: opens={disk_o} closes={disk_c} delta={disk_d} ({d1})")
    if args.reverse:
        d_old45 = find_target_lines(disk, OLD_LINE45_F1)
        d_rendered = find_target_lines(disk, RENDERED_LINE)
        d2 = "OK" if (len(d_old45) == 1 and len(d_rendered) == 0) else "FAIL"
        print(f"  F1 state on disk: line45_F1={d_old45} rendered={d_rendered} ({d2})")
    else:
        d_new45 = find_target_lines(disk, NEW_LINE45_F1_1)
        d_rendered = find_target_lines(disk, RENDERED_LINE)
        d2 = "OK" if (len(d_new45) == 1 and len(d_rendered) == 1) else "FAIL"
        print(f"  F1.1 state on disk: line45_F1.1={d_new45} rendered={d_rendered} ({d2})")

    if d1 != "OK" or d2 != "OK":
        print("\nDISK VERIFICATION FAILED. File may be in inconsistent state.")
        if not args.reverse:
            print(f"Restore: cp {BACKUP_PATH} {POPULATOR_PATH}")
        return 1

    print("\nApply complete. All checks pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
