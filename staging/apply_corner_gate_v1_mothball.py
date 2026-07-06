#!/usr/bin/env python3
"""
Apply script: interim mothball of corner-gate v1 enforcement.

Purpose
-------
The v1 corner gate is a proven structural latch (Sprint 01_corner_gate_v2
design doc, Sections 2 and 10): once corner-confirmed, it empties every
command batch, which blinds its own forward-outcome arm, so it releases only
on human input. It ate a knowledge write, the D3 survey answers, and a direct
person-response. Corner-gate v2 (pattern-scoped, visibility-first) is designed
and drafted; her code-analysis phase is sustained multi-cycle autonomous work,
which is exactly the class of activity the armed v1 latch suppresses.

This script turns v1 ENFORCEMENT off while detectors keep observing
(commitment 7 of the blessed guiding statement: detection outlives
enforcement). It is interim: the B4 build step of v2 replaces these
definitions entirely.

The change
----------
Two edits in soul/corner_gap/corner_gate.metta.

Edit 1, the gate filter. From:
    (= (apply-corner-gate $sexpr)
       (if (== (corner-confirmed) True)
           ()
           $sexpr))
To:
    ;; MOTHBALLED 2026-07-06 (interim until v2 lands): enforcement off, detectors keep observing.
    ;; Original body: (if (== (corner-confirmed) True) () $sexpr)
    (= (apply-corner-gate $sexpr) $sexpr)

Edit 2, the active flag (drives gate-aware-results feedback substitution). From:
    (= (corner-gate-active)
       (corner-confirmed))
To:
    ;; MOTHBALLED 2026-07-06: original body (corner-confirmed)
    (= (corner-gate-active) False)

Net change
----------
- Edit 1: 4 lines -> 3 lines (delta -1)
- Edit 2: 2 lines -> 2 lines (delta 0)
- Total expected line delta forward: -1 (reverse: +1)
- Paren delta: 0 (all blocks balanced; comment-quoted originals excluded by
  code-aware counting)

Runtime notes
-------------
soul/ is bind-mounted, so the edit reaches the container without a rebuild;
it takes effect at the next container restart (the file is executed at
import). Both replacement bodies are single-head total definitions, no
overlapping heads (P3 fork precedent), C12-safe (no match anywhere).

Usage
-----
Dry-run (default):
    python3 staging/apply_corner_gate_v1_mothball.py

Apply:
    python3 staging/apply_corner_gate_v1_mothball.py --apply

Reverse (mothball -> original v1):
    python3 staging/apply_corner_gate_v1_mothball.py --reverse --apply

Pre-conditions
--------------
Forward EXPECTS the original v1 bodies present exactly once each and no
MOTHBALLED marker. Reverse EXPECTS the mothballed bodies present exactly once
each. Any mismatch aborts with counts printed; no disk write.

Backup file (forward apply only): soul/corner_gap/corner_gate.metta.bak.mothball
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

GATE_PATH = Path("soul/corner_gap/corner_gate.metta")
BACKUP_PATH = Path("soul/corner_gap/corner_gate.metta.bak.mothball")

OLD_GATE = (
    "(= (apply-corner-gate $sexpr)\n"
    "   (if (== (corner-confirmed) True)\n"
    "       ()\n"
    "       $sexpr))"
)
NEW_GATE = (
    ";; MOTHBALLED 2026-07-06 (interim until v2 lands): enforcement off, detectors keep observing.\n"
    ";; Original body: (if (== (corner-confirmed) True) () $sexpr)\n"
    "(= (apply-corner-gate $sexpr) $sexpr)"
)

OLD_ACTIVE = (
    "(= (corner-gate-active)\n"
    "   (corner-confirmed))"
)
NEW_ACTIVE = (
    ";; MOTHBALLED 2026-07-06: original body (corner-confirmed)\n"
    "(= (corner-gate-active) False)"
)

MARKER = "MOTHBALLED 2026-07-06"


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


def count_block(text: str, block: str) -> int:
    count = 0
    start = 0
    while True:
        idx = text.find(block, start)
        if idx == -1:
            break
        count += 1
        start = idx + 1
    return count


def simulate(content: str, reverse: bool) -> str:
    if reverse:
        pairs = [(NEW_GATE, OLD_GATE, "gate"), (NEW_ACTIVE, OLD_ACTIVE, "active")]
    else:
        pairs = [(OLD_GATE, NEW_GATE, "gate"), (OLD_ACTIVE, NEW_ACTIVE, "active")]
    for old, new, name in pairs:
        c = count_block(content, old)
        if c != 1:
            raise RuntimeError(
                f"Edit '{name}': expected exactly 1 occurrence of the "
                f"{'mothballed' if reverse else 'original'} block, found {c}."
            )
        content = content.replace(old, new, 1)
    return content


def diff_preview(old_content: str, new_content: str, context: int = 3) -> str:
    old_lines = old_content.splitlines()
    new_lines = new_content.splitlines()
    out = ["--- diff preview ---"]
    min_len = min(len(old_lines), len(new_lines))
    i = 0
    while i < min_len:
        if old_lines[i] != new_lines[i]:
            # print a hunk: context, then removed/added run until re-sync
            start = max(0, i - context)
            for j in range(start, i):
                out.append(f"  {old_lines[j]}")
            oi, ni = i, i
            while oi < len(old_lines) and old_lines[oi] not in new_lines[ni:ni + 8]:
                out.append(f"- {old_lines[oi]}")
                oi += 1
            while ni < len(new_lines) and (oi >= len(old_lines) or new_lines[ni] != old_lines[oi]):
                out.append(f"+ {new_lines[ni]}")
                ni += 1
            end = min(len(old_lines), oi + context)
            for j in range(oi, end):
                out.append(f"  {old_lines[j]}")
            out.append("  ...")
            # advance both cursors past the hunk
            delta = ni - i
            i = oi
            new_lines = new_lines  # cursors tracked via oi/ni offsets
            min_len = min(len(old_lines), len(new_lines) - (delta - (oi - (i))))
            # simple resync: continue scanning from oi with aligned offset
            new_offset = ni - oi
            # rebuild aligned views for the remainder
            old_rest = old_lines[oi:]
            new_rest = new_lines[oi + new_offset:]
            for k in range(min(len(old_rest), len(new_rest))):
                if old_rest[k] != new_rest[k]:
                    out.append("  (further hunks follow; see file)")
                    return "\n".join(out)
            return "\n".join(out)
        i += 1
    if len(old_lines) != len(new_lines):
        out.append("(tail length differs)")
    else:
        out.append("(no change)")
    return "\n".join(out)


def state_report(text: str) -> dict:
    return {
        "old_gate": count_block(text, OLD_GATE),
        "old_active": count_block(text, OLD_ACTIVE),
        "new_gate": count_block(text, NEW_GATE),
        "new_active": count_block(text, NEW_ACTIVE),
        "marker": count_block(text, MARKER),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Corner-gate v1 interim mothball apply script")
    parser.add_argument("--apply", action="store_true",
                        help="Actually write changes. Default is dry-run.")
    parser.add_argument("--reverse", action="store_true",
                        help="Reverse the edit (mothball -> original v1). Combine with --apply to write.")
    args = parser.parse_args()

    if not GATE_PATH.exists():
        print(f"ERROR: {GATE_PATH} not found. Run from repo root.")
        return 1

    content = GATE_PATH.read_text()
    direction = "REVERSE (mothball -> v1 original)" if args.reverse else "APPLY (v1 original -> mothball)"
    print(f"\n>>> {direction} <<<")

    pre_o, pre_c = code_aware_paren_count(content)
    pre_d = pre_o - pre_c
    pre_lines = len(content.splitlines())
    st = state_report(content)

    print("\n=== PRE-EDIT CHECKS ===")
    print(f"  1. file path:           {GATE_PATH}")
    c_paren = "OK" if pre_d == 0 else "FAIL"
    print(f"  2. paren count pre:     opens={pre_o} closes={pre_c} delta={pre_d} ({c_paren})")
    print(f"  3. line count pre:      {pre_lines}")
    if args.reverse:
        c_state = "OK" if (st["new_gate"] == 1 and st["new_active"] == 1
                           and st["old_gate"] == 0 and st["old_active"] == 0) else "FAIL"
        print(f"  4. mothball state:      {st} ({c_state})")
    else:
        c_state = "OK" if (st["old_gate"] == 1 and st["old_active"] == 1
                           and st["marker"] == 0) else "FAIL"
        print(f"  4. v1-original state:   {st} ({c_state})")
    if c_state != "OK" or c_paren != "OK":
        print("\nPre-check failed. Aborting; no disk write. If the anchor counts "
              "are 0, the live file text differs from the expected block; paste "
              "the file so the anchors can be re-grounded.")
        return 1

    try:
        simulated = simulate(content, args.reverse)
        expected_line_delta = 1 if args.reverse else -1
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
    c6 = "OK" if line_delta == expected_line_delta else "FAIL"
    print(f"  6. line delta:          {line_delta} (expected {expected_line_delta}) ({c6})")
    st_post = state_report(simulated)
    if args.reverse:
        c7 = "OK" if (st_post["old_gate"] == 1 and st_post["old_active"] == 1
                      and st_post["marker"] == 0) else "FAIL"
    else:
        c7 = "OK" if (st_post["new_gate"] == 1 and st_post["new_active"] == 1
                      and st_post["old_gate"] == 0 and st_post["old_active"] == 0) else "FAIL"
    print(f"  7. simulated end state: {st_post} ({c7})")

    if c5 != "OK" or c6 != "OK" or c7 != "OK":
        print("\nPost-edit simulation checks failed. Aborting; no disk write.")
        return 1

    print("\n" + diff_preview(content, simulated))

    if not args.apply:
        print("\nDry-run complete. All checks pass. Re-run with --apply to write.")
        return 0

    if not args.reverse:
        if BACKUP_PATH.exists():
            print(f"\nWARNING: backup {BACKUP_PATH} exists; overwriting.")
        BACKUP_PATH.write_text(content)
        print(f"\nBackup written: {BACKUP_PATH}")

    GATE_PATH.write_text(simulated)
    print(f"Wrote: {GATE_PATH}")

    disk = GATE_PATH.read_text()
    disk_o, disk_c = code_aware_paren_count(disk)
    disk_d = disk_o - disk_c
    st_disk = state_report(disk)
    print("\n=== POST-WRITE DISK VERIFICATION ===")
    d1 = "OK" if disk_d == 0 else "FAIL"
    print(f"  paren count: opens={disk_o} closes={disk_c} delta={disk_d} ({d1})")
    if args.reverse:
        d2 = "OK" if (st_disk["old_gate"] == 1 and st_disk["old_active"] == 1
                      and st_disk["marker"] == 0) else "FAIL"
    else:
        d2 = "OK" if (st_disk["new_gate"] == 1 and st_disk["new_active"] == 1
                      and st_disk["old_gate"] == 0 and st_disk["old_active"] == 0) else "FAIL"
    print(f"  end state on disk: {st_disk} ({d2})")

    if d1 != "OK" or d2 != "OK":
        print("\nDISK VERIFICATION FAILED. File may be in inconsistent state.")
        if not args.reverse:
            print(f"Restore: cp {BACKUP_PATH} {GATE_PATH}")
        return 1

    print("\nApply complete. All checks pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
