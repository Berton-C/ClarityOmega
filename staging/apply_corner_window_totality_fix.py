#!/usr/bin/env python3
"""
Apply script: corner-window writer totality fix (the stuck-iteration repair).

Purpose
-------
PROVEN mechanism (2026-07-07): do-clear-corner-window! runs (superpose $olds)
without guarding the empty case. Superpose over an empty tuple yields ZERO
solutions, the writer FAILS (Prolog false, not error), the populate-corner-window!
binding in the loop's let* fails, and the cycle BACKTRACKS: the loop re-enters
the k=1 activation and re-runs full cycles forever (observed: 1 process start,
17 iteration-1 banners, 0 iteration-2 banners; every cycle's log dying between
the prune diag and the history prints, exactly where the hook sits).
Reproduced in isolation: R1_EMPTY_CLEAR (CLEAR_RAN 0).

The codebase already documented this exact defect and its fix in
soul/corner_gap/state_delta_writer_writers.metta (the do-clear-idle-pattern!
verified idiom): guard (== $list ()) on the COLLAPSED list BEFORE superpose,
and collapse-wrap the iteration so the writer returns exactly one solution
and cannot multiply the following bindings. This script brings BOTH writers
in corner_window_writers.metta to that idiom:

- do-clear-corner-window!: empty guard + collapse-wrapped drain.
  Fix probe: R3 (V2_RAN 1) empty, R4 (V2_RAN 1) nonempty, R5 remaining 0.
- do-record-corner-window!: same latent class, two ways: an empty batch
  during a confirmed corner would zero-solution-fail identically, and a
  multi-command batch would yield one solution PER COMMAND and fork the
  cycle tail. Empty guard + collapse-wrap. Fix probe S1/S2/S3 (run before
  this script applies).

Runtime notes
-------------
soul/ is bind-mounted (docker-compose.yml line 41), so the fix reaches the
container at `docker compose restart clarityclaw` with NO rebuild. The restart
also clears the id-1 atom pollution from the stuck cycles (recent-action and
friends are in-memory only).

Net change (computed and checked at runtime)
--------------------------------------------
- Edit 1 (clear): 6 lines -> 9 lines (+3, including the 2-line fix comment)
- Edit 2 (record): 6 lines -> 9 lines (+3, including the 2-line fix comment)
- Expected line delta forward: +6 (reverse: -6)
- Paren delta: 0 (checked by code-aware count)

Usage
-----
Dry-run (default):  python3 staging/apply_corner_window_totality_fix.py
Apply:              python3 staging/apply_corner_window_totality_fix.py --apply
Reverse:            python3 staging/apply_corner_window_totality_fix.py --reverse --apply

Backup (forward apply only): soul/corner_gap/corner_window_writers.metta.bak.totality_fix
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

WW_PATH = Path("soul/corner_gap/corner_window_writers.metta")
BACKUP_PATH = Path("soul/corner_gap/corner_window_writers.metta.bak.totality_fix")

MARKER = "TOTALITY-FIX 2026-07-07"

E1_OLD = (
    "(= (do-clear-corner-window!)\n"
    "   (let $olds (collapse (match &self (corner-window-cmd $c $r) (corner-window-cmd $c $r)))\n"
    "        (let $o (superpose $olds)\n"
    "             (if (== $o ())\n"
    "                 ()\n"
    "                 (remove-atom &self $o)))))"
)
E1_NEW = (
    ";; TOTALITY-FIX 2026-07-07: guard empty BEFORE superpose; collapse-wrap the drain\n"
    ";; (state_delta / do-clear-idle-pattern! verified idiom; repro R1=0, fix R3/R4/R5).\n"
    "(= (do-clear-corner-window!)\n"
    "   (let $olds (collapse (match &self (corner-window-cmd $c $r) (corner-window-cmd $c $r)))\n"
    "        (if (== $olds ())\n"
    "            ()\n"
    "            (let $_drained (collapse (let $o (superpose $olds)\n"
    "                                          (remove-atom &self $o)))\n"
    "                 ()))))"
)

E2_OLD = (
    "(= (do-record-corner-window! $cmds $cycle-id)\n"
    "   (let $c (superpose $cmds)\n"
    "        (if (== $c ())\n"
    "            ()\n"
    "            (let $r (repr $c)\n"
    "                 (add-atom &self (corner-window-cmd $cycle-id $r))))))"
)
E2_NEW = (
    ";; TOTALITY-FIX 2026-07-07: empty-batch guard + collapse-wrap so the writer\n"
    ";; returns exactly one solution and cannot fork the cycle tail (probe S1/S2/S3).\n"
    "(= (do-record-corner-window! $cmds $cycle-id)\n"
    "   (if (== $cmds ())\n"
    "       ()\n"
    "       (let $_recorded (collapse (let $c (superpose $cmds)\n"
    "                                      (let $r (repr $c)\n"
    "                                           (add-atom &self (corner-window-cmd $cycle-id $r)))))\n"
    "            ())))"
)


def code_aware_paren_count(text: str) -> tuple[int, int]:
    opens = closes = 0
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
    pairs = [(E1_OLD, E1_NEW, "Edit 1 (clear)"), (E2_OLD, E2_NEW, "Edit 2 (record)")]
    for old, new, label in pairs:
        src, dst = (new, old) if reverse else (old, new)
        c = count_block(content, src)
        if c != 1:
            raise RuntimeError(f"{label}: anchor found {c} times (expected 1). "
                               f"Paste the file to re-ground anchors.")
        content = content.replace(src, dst, 1)
    return content


def state_report(content: str) -> str:
    return (f"old-clear={count_block(content, E1_OLD)} "
            f"old-record={count_block(content, E2_OLD)} "
            f"fixed-clear={count_block(content, E1_NEW)} "
            f"fixed-record={count_block(content, E2_NEW)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Corner-window writer totality fix")
    parser.add_argument("--apply", action="store_true",
                        help="Actually write changes. Default is dry-run.")
    parser.add_argument("--reverse", action="store_true",
                        help="Reverse the fix. Combine with --apply to write.")
    args = parser.parse_args()

    if not WW_PATH.exists():
        print(f"ERROR: {WW_PATH} not found. Run from repo root.")
        return 1

    content = WW_PATH.read_text()
    direction = "REVERSE (fixed -> prior)" if args.reverse else "APPLY (prior -> fixed)"
    print(f"\n>>> CORNER-WINDOW WRITER TOTALITY FIX: {direction} <<<")

    pre_o, pre_c = code_aware_paren_count(content)
    pre_lines = len(content.splitlines())
    print("\n=== PRE-EDIT CHECKS ===")
    print(f"  paren pre: opens={pre_o} closes={pre_c} ({'OK' if pre_o == pre_c else 'FAIL'})")
    print(f"  lines pre: {pre_lines}")
    print(f"  state: {state_report(content)}")
    if pre_o != pre_c:
        print("Aborting: unbalanced file pre-edit.")
        return 1

    try:
        simulated = simulate(content, args.reverse)
        expected_delta = -6 if args.reverse else 6
    except RuntimeError as exc:
        print(f"\nSimulation failed: {exc}")
        return 1

    post_o, post_c = code_aware_paren_count(simulated)
    delta = len(simulated.splitlines()) - pre_lines
    print("\n=== POST-EDIT (SIMULATED) CHECKS ===")
    print(f"  paren post: opens={post_o} closes={post_c} ({'OK' if post_o == post_c else 'FAIL'})")
    print(f"  line delta: {delta:+d} (expected {expected_delta:+d}) "
          f"({'OK' if delta == expected_delta else 'FAIL'})")
    print(f"  simulated end state: {state_report(simulated)}")
    if post_o != post_c or delta != expected_delta:
        print("Aborting; no disk write.")
        return 1

    print("\n=== DIFF PREVIEW ===")
    pairs = [(E1_OLD, E1_NEW), (E2_OLD, E2_NEW)]
    for old, new in pairs:
        src, dst = (new, old) if args.reverse else (old, new)
        for line in src.splitlines():
            print(f"- {line}")
        for line in dst.splitlines():
            print(f"+ {line}")
        print()

    if not args.apply:
        print("Dry-run complete. All checks pass. Re-run with --apply to write.")
        return 0

    if not args.reverse:
        if BACKUP_PATH.exists():
            print(f"WARNING: backup {BACKUP_PATH} exists; overwriting.")
        BACKUP_PATH.write_text(content)
        print(f"Backup written: {BACKUP_PATH}")
    WW_PATH.write_text(simulated)
    disk = WW_PATH.read_text()
    d_o, d_c = code_aware_paren_count(disk)
    ok = d_o == d_c and ((MARKER in disk) != args.reverse)
    print(f"Wrote: {WW_PATH}")
    print("\n=== POST-WRITE DISK VERIFICATION ===")
    print(f"  paren: opens={d_o} closes={d_c} ({'OK' if d_o == d_c else 'FAIL'})")
    print(f"  end state: {state_report(disk)} ({'OK' if ok else 'FAIL'})")
    if not ok:
        print(f"DISK VERIFICATION FAILED. Restore: cp {BACKUP_PATH} {WW_PATH}")
        return 1
    print("\nApply complete. All checks pass.")
    print("Next: docker compose restart clarityclaw (bind-mounted; no rebuild),")
    print("then verify the banner advances past iteration 1.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
