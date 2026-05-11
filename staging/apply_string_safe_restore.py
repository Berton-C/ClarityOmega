#!/usr/bin/env python3
"""
Apply script: Restore upstream OmegaClaw parity for &lastresults binding.

Purpose
-------
Replace our local line at loop.metta line ~145:
    (change-state! &lastresults (py-call (helper.safe_results_str (repr $results))))
with current upstream OmegaClaw's line (loop.metta line 132 in upstream):
    (change-state! &lastresults (string-safe (repr $results)))

Historical note
---------------
The current line in our codebase carries the (repr $results) wrapping that was
added in commit 69c73fc as a failed attempt to fix this same crash. The
71417bf revert reportedly undid 69c73fc, but the (repr $results) wrapping is
visible in our current codebase regardless. Either the revert didn't fully take
or something later re-added the wrapping. The current line is structurally what
69c73fc tried — and we now know that approach doesn't work because it still
crosses the py-call boundary with unbound variables inside the rendered term.

Why MeTTa-side stringification works (and py-call wrapping doesn't)
------------------------------------------------------------------
- (py-call (helper.X (repr $results))): repr renders the term, but the rendered
  term still contains the unbound variables. Janus marshaling fails at the py-call
  boundary regardless of how the term was rendered.
- (string-safe (repr $results)): both string-safe and repr are pure MeTTa. The
  unbound variables get rendered as $_NNNNNN text inside a string atom. The string
  atom is a proper bound term. It can be passed anywhere safely.
- The location of the boundary is what matters. MeTTa-side stringification keeps
  unbound variables inside the Prolog runtime where they don't cause boundary errors.

Restoring the upstream line is the strongest possible bedrock-rule respect:
we're restoring our codebase to match Patrick's actively maintained upstream.

Usage
-----
Dry-run (default):
    python3 staging/apply_string_safe_restore.py

Apply:
    python3 staging/apply_string_safe_restore.py --apply

Reverse (after apply):
    python3 staging/apply_string_safe_restore.py --reverse --apply

Verification checks (all must pass before write)
-----------------------------------------------
1. Target file exists at expected path.
2. Old line found exactly once (no ambiguity).
3. New line not yet present (no double-apply).
4. Pre-edit code-aware paren count balanced (delta = 0).
5. Pre-edit raw line count recorded as baseline.
6. Post-edit (simulated) code-aware paren count balanced.
7. Delta change pre→post = 0.
8. New line on simulated content found exactly once.
Plus three post-write disk checks.

Backup file (forward apply only): src/loop.metta.bak.string_safe_restore
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

LOOP_PATH = Path("src/loop.metta")
BACKUP_PATH = Path("src/loop.metta.bak.string_safe_restore")

# Exact target strings (whitespace-insensitive line match via .strip())
# Note: The line has trailing closes that close outer scopes (progn, let*, etc).
# We preserve those by counting them precisely.
#
# Substantive part of OLD: (change-state! &lastresults (py-call (helper.safe_results_str (repr $results))))
#   = 4 opens, 4 closes
# Substantive part of NEW: (change-state! &lastresults (string-safe (repr $results)))
#   = 3 opens, 3 closes
#
# OLD line currently in our codebase (line 145 of loop.metta):
#   <leading-ws>(change-state! &lastresults (py-call (helper.safe_results_str (repr $results)))))))
#   That's 7 trailing ')' total: 4 for the substantive expression + 3 for outer scopes.
#
# After replacement, NEW line keeps the same 3 outer-scope closes but the substantive
# part has 1 fewer pair, so total trailing ')' is 6 instead of 7. Code-aware delta = 0.
OLD_LINE = "(change-state! &lastresults (py-call (helper.safe_results_str (repr $results)))))))"
NEW_LINE = "(change-state! &lastresults (string-safe (repr $results))))))"


def code_aware_paren_count(text: str) -> tuple[int, int]:
    """Count parens excluding those inside string literals and line comments.

    MeTTa uses ; for line comments. Strings are double-quoted with backslash escape.
    """
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
                # skip to end of line
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


def simulate_edit(content: str, old_line: str, new_line: str) -> str:
    old_stripped = old_line.strip()
    out_lines = []
    replaced = 0
    for line in content.splitlines(keepends=True):
        if line.strip() == old_stripped:
            leading = line[: len(line) - len(line.lstrip())]
            trailing = ""
            if line.endswith("\r\n"):
                trailing = "\r\n"
            elif line.endswith("\n"):
                trailing = "\n"
            out_lines.append(f"{leading}{new_line}{trailing}")
            replaced += 1
        else:
            out_lines.append(line)
    if replaced != 1:
        raise RuntimeError(f"Expected exactly 1 replacement, got {replaced}.")
    return "".join(out_lines)


def diff_preview(old_content: str, new_content: str, context: int = 3) -> str:
    old_lines = old_content.splitlines()
    new_lines = new_content.splitlines()
    if len(old_lines) != len(new_lines):
        return "(line count differs; investigate)"
    changed = [i for i in range(len(old_lines)) if old_lines[i] != new_lines[i]]
    if not changed:
        return "(no change)"
    out = []
    for ci in changed:
        start = max(0, ci - context)
        end = min(len(old_lines), ci + context + 1)
        out.append(f"--- around line {ci + 1} ---")
        for i in range(start, end):
            if i == ci:
                out.append(f"- {old_lines[i]}")
                out.append(f"+ {new_lines[i]}")
            else:
                out.append(f"  {old_lines[i]}")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--apply", action="store_true",
                        help="Actually write changes. Default is dry-run.")
    parser.add_argument("--reverse", action="store_true",
                        help="Reverse the edit (new -> old). Combine with --apply to write.")
    args = parser.parse_args()

    if not LOOP_PATH.exists():
        print(f"ERROR: {LOOP_PATH} not found. Run from repo root.")
        return 1

    content = LOOP_PATH.read_text()
    if args.reverse:
        old_line, new_line = NEW_LINE, OLD_LINE
        action_label = "REVERSE (restore F7 line)"
    else:
        old_line, new_line = OLD_LINE, NEW_LINE
        action_label = "APPLY (restore upstream parity)"

    print(f"\n>>> {action_label} <<<")
    print(f"Old (to find):    {old_line}")
    print(f"New (to write):   {new_line}")

    # Pre-edit checks
    old_matches = find_target_lines(content, old_line)
    new_matches = find_target_lines(content, new_line)
    pre_o, pre_c = code_aware_paren_count(content)
    pre_d = pre_o - pre_c
    line_count = len(content.splitlines())

    print("\n=== PRE-EDIT CHECKS ===")
    print(f"  1. file path:           {LOOP_PATH}")
    c2 = "OK" if len(old_matches) == 1 else "FAIL"
    print(f"  2. old-line matches:    {old_matches} ({c2})")
    c3 = "OK" if len(new_matches) == 0 else "FAIL"
    print(f"  3. new-line matches:    {new_matches} ({c3})")
    c4 = "OK" if pre_d == 0 else "FAIL"
    print(f"  4. paren count pre:     opens={pre_o} closes={pre_c} delta={pre_d} ({c4})")
    print(f"  5. raw line count:      {line_count}")

    if c2 != "OK" or c3 != "OK" or c4 != "OK":
        print("\nPre-edit checks failed. Aborting.")
        return 1

    # Simulate
    try:
        simulated = simulate_edit(content, old_line, new_line)
    except RuntimeError as exc:
        print(f"\nSimulation failed: {exc}")
        return 1

    post_o, post_c = code_aware_paren_count(simulated)
    post_d = post_o - post_c
    delta_change = post_d - pre_d
    new_matches_after = find_target_lines(simulated, new_line)

    print("\n=== POST-EDIT (SIMULATED) CHECKS ===")
    c6 = "OK" if post_d == 0 else "FAIL"
    print(f"  6. paren count post:    opens={post_o} closes={post_c} delta={post_d} ({c6})")
    c7 = "OK" if delta_change == 0 else "FAIL"
    print(f"  7. delta change:        {delta_change} ({c7})")
    c8 = "OK" if len(new_matches_after) == 1 else "FAIL"
    print(f"  8. new-line on simulated:    {new_matches_after} ({c8})")

    if c6 != "OK" or c7 != "OK" or c8 != "OK":
        print("\nPost-edit simulation checks failed. Aborting; no disk write.")
        return 1

    print("\n=== DIFF PREVIEW ===")
    print(diff_preview(content, simulated))

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
    LOOP_PATH.write_text(simulated)
    print(f"Wrote: {LOOP_PATH}")

    # Post-write disk verification
    disk_content = LOOP_PATH.read_text()
    disk_o, disk_c = code_aware_paren_count(disk_content)
    disk_d = disk_o - disk_c
    disk_new = find_target_lines(disk_content, new_line)
    disk_old = find_target_lines(disk_content, old_line)

    print("\n=== POST-WRITE DISK VERIFICATION ===")
    d1 = "OK" if disk_d == 0 else "FAIL"
    print(f"  paren count: opens={disk_o} closes={disk_c} delta={disk_d} ({d1})")
    d2 = "OK" if len(disk_new) == 1 else "FAIL"
    print(f"  new line on disk: {disk_new} ({d2})")
    d3 = "OK" if len(disk_old) == 0 else "FAIL"
    print(f"  old line on disk: {disk_old} ({d3})")

    if d1 != "OK" or d2 != "OK" or d3 != "OK":
        print("\nDISK VERIFICATION FAILED. File may be in inconsistent state.")
        print(f"Restore: cp {BACKUP_PATH} {LOOP_PATH}")
        return 1

    print("\nApply complete. All checks pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
