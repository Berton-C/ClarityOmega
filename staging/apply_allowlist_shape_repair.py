#!/usr/bin/env python3
"""
Apply script: allowlist shape repair in corner_gate.metta (post-monolith fix).

Purpose
-------
PROVEN mechanism (2026-07-06, minimal reproduction m_repro/m_fix): the monolith's
allowlist clause

    (= (allowed-heads)
       (send metta shell ...))

has a body that is a bare APPLICATION of `send` (a DEFINED skill, arity 1) to
thirteen arguments. In the boot context where skill heads are defined, the
PeTTa transpiler compiles the body as a call, dies on the arity mismatch
(length/2 domain error, found -13; fatal exit 2 standalone), and under the
library import the machinery continues while REGISTERING NOTHING AFTER that
clause in the file. Live signature: head-in-list?, real-return?,
filter-returns, cmd-in-corner-window?, filter-corner-cmds never registered;
first runtime call into filter-returns crashed the cycle (Unknown procedure
filter-returns/2, exit 2, restart loop).

Every pre-wire probe passed because probe contexts had those heads UNDEFINED,
so the same body compiled as data. New durable constraints recorded in the
sprint docs: defined-head data tuples are forbidden; probe environments must
stub the heads the live context defines.

The repair (proven in the killing context: m_fix exit 0, F3 registered)
------------------------------------------------------------------------
Edit 1: the allowed-heads tuple and head-in-list? recursion are REPLACED by
  fifteen allowed-head data atoms (membership-seed pattern; add-atom stores
  its argument unreduced, so defined heads are inert) plus head-allowed?
  (match-count membership, the detector idiom).
Edit 2: real-return? switches its membership call from
  (head-in-list? (car-atom $s) (allowed-heads)) to
  (head-allowed? (car-atom $s)).

Semantics are IDENTICAL to the probe-proven filter behavior (B7, P1-P4):
real command returns pass verbatim, prose echoes become the mechanical
marker, unlisted heads fail toward the marker (information loss, never
poison).

Net change
----------
- Edit 1: 10 lines -> 23 lines (+13)
- Edit 2: 3 lines -> 3 lines (0)
- Expected line delta forward: +13 (reverse: -13)
- Paren delta: 0 (checked by code-aware count)

Runtime notes
-------------
soul/ is bind-mounted: the repair reaches the container at the next
`docker compose up -d` with NO rebuild (the mount overrides the baked copy).

Usage
-----
Dry-run (default):  python3 staging/apply_allowlist_shape_repair.py
Apply:              python3 staging/apply_allowlist_shape_repair.py --apply
Reverse:            python3 staging/apply_allowlist_shape_repair.py --reverse --apply

Backup (forward apply only): soul/corner_gap/corner_gate.metta.bak.allowlist_repair
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

GATE_PATH = Path("soul/corner_gap/corner_gate.metta")
BACKUP_PATH = Path("soul/corner_gap/corner_gate.metta.bak.allowlist_repair")

E1_OLD = (
    "(= (allowed-heads)\n"
    "   (send metta shell read-file write-file append-file query remember\n"
    "    pin promote demote tavily-search technical-analysis agentverse progn))\n"
    "\n"
    "(= (head-in-list? $x $lst)\n"
    "   (if (== $lst ())\n"
    "       False\n"
    "       (let* (($h (car-atom $lst))\n"
    "              ($t (cdr-atom $lst)))\n"
    "             (if (== $h $x) True (head-in-list? $x $t)))))"
)

E1_NEW = (
    ";; ALLOWLIST-REPAIR 2026-07-06: the tuple body applied DEFINED skill heads and\n"
    ";; killed transpiler registration of everything after it (repro: m_repro exit 2,\n"
    ";; length/2 domain error, arity -13). Replaced by data atoms (membership-seed\n"
    ";; pattern; add-atom stores unreduced, defined heads inert) plus match-count\n"
    ";; membership (repro: m_fix exit 0, later functions register).\n"
    "!(add-atom &self (allowed-head send))\n"
    "!(add-atom &self (allowed-head metta))\n"
    "!(add-atom &self (allowed-head shell))\n"
    "!(add-atom &self (allowed-head read-file))\n"
    "!(add-atom &self (allowed-head write-file))\n"
    "!(add-atom &self (allowed-head append-file))\n"
    "!(add-atom &self (allowed-head query))\n"
    "!(add-atom &self (allowed-head remember))\n"
    "!(add-atom &self (allowed-head pin))\n"
    "!(add-atom &self (allowed-head promote))\n"
    "!(add-atom &self (allowed-head demote))\n"
    "!(add-atom &self (allowed-head tavily-search))\n"
    "!(add-atom &self (allowed-head technical-analysis))\n"
    "!(add-atom &self (allowed-head agentverse))\n"
    "!(add-atom &self (allowed-head progn))\n"
    "\n"
    "(= (head-allowed? $h)\n"
    "   (> (size-atom (collapse (match &self (allowed-head $h) $h))) 0))"
)

E2_OLD = (
    "(= (real-return? $el)\n"
    "   (let (COMMAND_RETURN: ($s $r)) $el\n"
    "        (head-in-list? (car-atom $s) (allowed-heads))))"
)

E2_NEW = (
    "(= (real-return? $el)\n"
    "   (let (COMMAND_RETURN: ($s $r)) $el\n"
    "        (head-allowed? (car-atom $s))))"
)

MARKER = "ALLOWLIST-REPAIR 2026-07-06"


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
    if reverse:
        for blk, name in [(E1_NEW, "Edit 1 (repaired allowlist)"),
                          (E2_NEW, "Edit 2 (repaired real-return?)")]:
            if count_block(content, blk) != 1:
                raise RuntimeError(f"Reverse: {name} not found exactly once.")
        content = content.replace(E1_NEW, E1_OLD, 1)
        return content.replace(E2_NEW, E2_OLD, 1)
    for blk, name in [(E1_OLD, "Edit 1 (tuple allowlist)"),
                      (E2_OLD, "Edit 2 (head-in-list? call)")]:
        if count_block(content, blk) != 1:
            raise RuntimeError(f"Forward: {name} anchor not found exactly once. "
                               f"Paste the file so anchors can be re-grounded.")
    if MARKER in content:
        raise RuntimeError("Forward: repair marker already present.")
    content = content.replace(E1_OLD, E1_NEW, 1)
    return content.replace(E2_OLD, E2_NEW, 1)


def state_report(text: str) -> str:
    return (f"tuple-allowlist={count_block(text, E1_OLD)} "
            f"old-real-return={count_block(text, E2_OLD)} "
            f"repaired-allowlist={count_block(text, E1_NEW)} "
            f"repaired-real-return={count_block(text, E2_NEW)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Allowlist shape repair apply script")
    parser.add_argument("--apply", action="store_true",
                        help="Actually write changes. Default is dry-run.")
    parser.add_argument("--reverse", action="store_true",
                        help="Reverse the repair. Combine with --apply to write.")
    args = parser.parse_args()

    if not GATE_PATH.exists():
        print(f"ERROR: {GATE_PATH} not found. Run from repo root.")
        return 1

    content = GATE_PATH.read_text()
    direction = "REVERSE (repair -> monolith shape)" if args.reverse else "APPLY (monolith shape -> repair)"
    print(f"\n>>> ALLOWLIST SHAPE REPAIR: {direction} <<<")

    pre_o, pre_c = code_aware_paren_count(content)
    pre_lines = len(content.splitlines())
    print("\n=== PRE-EDIT CHECKS ===")
    print(f"  paren pre: opens={pre_o} closes={pre_c} delta={pre_o - pre_c} "
          f"({'OK' if pre_o == pre_c else 'FAIL'})")
    print(f"  lines pre: {pre_lines}")
    print(f"  state: {state_report(content)}")
    if pre_o != pre_c:
        print("Aborting: unbalanced file pre-edit.")
        return 1

    try:
        simulated = simulate(content, args.reverse)
        expected_delta = -13 if args.reverse else 13
    except RuntimeError as exc:
        print(f"\nSimulation failed: {exc}")
        return 1

    post_o, post_c = code_aware_paren_count(simulated)
    post_lines = len(simulated.splitlines())
    delta = post_lines - pre_lines
    print("\n=== POST-EDIT (SIMULATED) CHECKS ===")
    print(f"  paren post: opens={post_o} closes={post_c} delta={post_o - post_c} "
          f"({'OK' if post_o == post_c else 'FAIL'})")
    print(f"  line delta: {delta} (expected {expected_delta}) "
          f"({'OK' if delta == expected_delta else 'FAIL'})")
    print(f"  simulated end state: {state_report(simulated)}")
    if post_o != post_c or delta != expected_delta:
        print("Aborting; no disk write.")
        return 1

    print("\n=== DIFF PREVIEW (changed regions) ===")
    if args.reverse:
        print("- (repaired allowlist block, 24 lines)\n+ (tuple allowlist + head-in-list?, 10 lines)")
        print("- (head-allowed? call in real-return?)\n+ (head-in-list? call in real-return?)")
    else:
        print("- (= (allowed-heads) (send metta shell ...tuple...))")
        print("- (= (head-in-list? $x $lst) ...recursion...)")
        print("+ ;; ALLOWLIST-REPAIR comment block")
        print("+ 15x !(add-atom &self (allowed-head <skill>))")
        print("+ (= (head-allowed? $h) (> (size-atom (collapse (match &self (allowed-head $h) $h))) 0))")
        print("- (head-in-list? (car-atom $s) (allowed-heads)) [inside real-return?]")
        print("+ (head-allowed? (car-atom $s)) [inside real-return?]")

    if not args.apply:
        print("\nDry-run complete. All checks pass. Re-run with --apply to write.")
        return 0

    if not args.reverse:
        if BACKUP_PATH.exists():
            print(f"\nWARNING: backup {BACKUP_PATH} exists; overwriting.")
        BACKUP_PATH.write_text(content)
        print(f"\nBackup written: {BACKUP_PATH}")
    GATE_PATH.write_text(simulated)
    disk = GATE_PATH.read_text()
    d_o, d_c = code_aware_paren_count(disk)
    ok = d_o == d_c and ((MARKER in disk) != args.reverse)
    print(f"Wrote: {GATE_PATH}")
    print("\n=== POST-WRITE DISK VERIFICATION ===")
    print(f"  paren: opens={d_o} closes={d_c} ({'OK' if d_o == d_c else 'FAIL'})")
    print(f"  end state: {state_report(disk)} ({'OK' if ok else 'FAIL'})")
    if not ok:
        print(f"DISK VERIFICATION FAILED. Restore: cp {BACKUP_PATH} {GATE_PATH}")
        return 1
    print("\nApply complete. All checks pass.")
    print("Next: pre-restart faithful-context probe, then docker compose up -d")
    return 0


if __name__ == "__main__":
    sys.exit(main())
