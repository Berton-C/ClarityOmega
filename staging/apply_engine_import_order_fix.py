#!/usr/bin/env python3
"""
Apply script: quantale engine import-order fix (ledger C1').

Purpose
-------
PROVEN by the live REPL differential (2026-07-08, Clarity's seven expressions
plus the nested-tree line, ledger 00a sections A2/A3/C1'): the import-path
transpiler compiles applications by what is DEFINED at each file's import
time. q-geq (defined at manifest line 9, before the merge) was compiled as a
CALL in the merge's body; q-meet (defined by the engine at ~line 119, after
the merge at ~92) was compiled as DATA. Result: corner-pbit-core returns an
unreduced q-meet tree, q-geq zero-matches it, corner-confirmed-core FAILS
(zero solutions), and every non-msgnew active cycle dies at loop line 166,
which is the entire stuck-iteration crisis and Clarity's silenced follow-ups.

The fix: the engine import MOVES to the top of the manifest (directly under
the lib_quantale retirement comment, BEFORE lib_self_continuity), so its
operator heads are defined before every consumer file compiles. This also
fixes ledger C2 (lib_self_continuity's own q-mul/q-meet call sites, compiled
post-retirement without the ops in scope). MOVE not copy: a duplicated import
would double-register every engine clause and fork every operator call.

Edits (one file, two blocks, all-or-none)
-----------------------------------------
FILE: lib_clarity_reasoning/lib_clarity_reasoning.metta
Edit 1: engine import inserted after the retirement comment (with the fix
        rationale comment), before the lib_self_continuity import.
Edit 2: engine import removed from the v08.7.2 block (replaced by a note;
        the evolutionary satellite imports remain in place).

Net change (verified at runtime)
--------------------------------
- Edit 1: 4 lines -> 10 lines (+6)
- Edit 2: 4 lines -> 5 lines (+1)
- Expected line delta forward: +7 (reverse: -7)
- Engine-import occurrence count: exactly 1 before, exactly 1 after (both
  directions; checked explicitly, this is the anti-fork invariant).

After apply
-----------
Manifest is baked: commit, then
  docker compose build --no-cache clarityclaw && docker compose up -d
Boot verification per ledger Section E: Clarity reruns
  (metta "(corner-pbit-core)")      -> expect a ground (mk-pbit s c)
  (metta "(corner-confirmed-core)") -> expect true or false, NOT empty
plus the banner advancing on active cycles without Berton posting, and her
follow-up messages arriving unprompted.

Usage
-----
Dry-run:  python3 staging/apply_engine_import_order_fix.py
Apply:    python3 staging/apply_engine_import_order_fix.py --apply
Reverse:  python3 staging/apply_engine_import_order_fix.py --reverse --apply
Backup (forward): lib_clarity_reasoning/lib_clarity_reasoning.metta.bak.import_order
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

MANIFEST = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta")
BACKUP = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta.bak.import_order")

ENGINE_IMPORT = ("!(import! &self (library omegaclaw ./lib_clarity_reasoning/"
                 "lib_quantale_autopoietic_epistemic_dynamics_engine_v08_7_2_"
                 "SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY))")

MARKER = "IMPORT-ORDER FIX 2026-07-08"

E1_OLD = (
    ";; RETIRED 2026-07-07: lib_quantale fully retired. All seven of its symbols are\n"
    ";; defined by the v08.7.2 engine (imported below in this manifest); zero loaded\n"
    ";; consumers of its bridges existed at retirement (survey + engine-only probe).\n"
    "!(import! &self (library omegaclaw ./lib_clarity_reasoning/lib_self_continuity))"
)
E1_NEW = (
    ";; RETIRED 2026-07-07: lib_quantale fully retired. All seven of its symbols are\n"
    ";; defined by the v08.7.2 engine (imported directly below); zero loaded\n"
    ";; consumers of its bridges existed at retirement (survey + engine-only probe).\n"
    ";; IMPORT-ORDER FIX 2026-07-08 (ledger C1'): the engine import MOVED HERE from\n"
    ";; the v08.7.2 block so its operator heads are defined BEFORE every consumer\n"
    ";; file compiles. The import-path transpiler compiles applications by what is\n"
    ";; defined at each file's import time (proven by the live REPL differential:\n"
    ";; q-geq call-compiled, q-meet data-compiled, exprs 2/6/7 of 2026-07-08).\n"
    + ENGINE_IMPORT + "\n"
    "!(import! &self (library omegaclaw ./lib_clarity_reasoning/lib_self_continuity))"
)

E2_OLD = (
    ";; BEGIN v08.7.2 soul-evolutionary quantale import block\n"
    ";; v08.7.2: quantale durable evolutionary governance engine + soul-owned topology\n"
    + ENGINE_IMPORT + "\n"
    "!(import! &self (library omegaclaw ./soul/evolutionary/index))"
)
E2_NEW = (
    ";; BEGIN v08.7.2 soul-evolutionary quantale import block\n"
    ";; v08.7.2: quantale durable evolutionary governance engine + soul-owned topology\n"
    ";; NOTE 2026-07-08: the engine import itself MOVED to the top of this manifest\n"
    ";; (import-order fix, ledger C1'); the evolutionary satellites remain here.\n"
    "!(import! &self (library omegaclaw ./soul/evolutionary/index))"
)


def code_aware_paren_count(text: str) -> tuple[int, int]:
    """Count parens excluding string literals and line comments (exemplar shape)."""
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


def diff_preview_first_change(old: str, new: str, context: int = 3) -> str:
    """First-divergence diff with context lines (exemplar shape)."""
    ol, nl = old.splitlines(), new.splitlines()
    i = 0
    while i < min(len(ol), len(nl)) and ol[i] == nl[i]:
        i += 1
    lines = [f"  first divergence at line {i + 1}:"]
    for k in range(max(0, i - context), min(len(ol), i + context + 4)):
        lines.append(f"  - {ol[k]}" if k >= i else f"    {ol[k]}")
    for k in range(i, min(len(nl), i + context + 4)):
        lines.append(f"  + {nl[k]}")
    return "\n".join(lines)


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Engine import-order fix")
    parser.add_argument("--apply", action="store_true",
                        help="Actually write changes. Default is dry-run.")
    parser.add_argument("--reverse", action="store_true",
                        help="Reverse the fix. Combine with --apply to write.")
    args = parser.parse_args()

    if not MANIFEST.exists():
        print(f"ERROR: {MANIFEST} not found. Run from repo root.")
        return 1

    content = MANIFEST.read_text()
    direction = "REVERSE (top -> v08.7.2 block)" if args.reverse else "APPLY (v08.7.2 block -> top)"
    print(f"\n>>> ENGINE IMPORT-ORDER FIX: {direction} <<<")

    engine_count = count_block(content, ENGINE_IMPORT)
    print("\n=== PRE-EDIT CHECKS ===")
    print(f"  engine-import occurrences: {engine_count} (expect 1)")
    print(f"  lines pre: {len(content.splitlines())}")
    marker_present = MARKER in content
    print(f"  fix marker: {'present' if marker_present else 'absent'} "
          f"(expect {'present' if args.reverse else 'absent'})")
    if engine_count != 1 or marker_present != args.reverse:
        print("ABORT: pre-state mismatch. Nothing written. Paste the manifest head.")
        return 1

    pairs = [(E1_OLD, E1_NEW, "Edit 1 (top-of-manifest insert)"),
             (E2_OLD, E2_NEW, "Edit 2 (v08.7.2 block removal)")]
    sim = content
    for old, new, label in pairs:
        src, dst = (new, old) if args.reverse else (old, new)
        c = count_block(sim, src)
        print(f"  {label}: anchor count {c} (expect 1)")
        if c != 1:
            print(f"ABORT: anchor mismatch for {label}. Nothing written. "
                  f"Paste the manifest to re-ground.")
            return 1
        sim = sim.replace(src, dst, 1)

    pre_o, pre_c = code_aware_paren_count(content)
    post_o, post_c = code_aware_paren_count(sim)
    delta = len(sim.splitlines()) - len(content.splitlines())
    expected = -7 if args.reverse else 7
    post_count = count_block(sim, ENGINE_IMPORT)
    print("\n=== POST-EDIT (SIMULATED) CHECKS ===")
    print(f"  paren pre: opens={pre_o} closes={pre_c} delta={pre_o - pre_c} "
          f"({'OK' if pre_o == pre_c else 'FAIL'})")
    print(f"  paren post: opens={post_o} closes={post_c} delta={post_o - post_c} "
          f"({'OK' if post_o == post_c else 'FAIL'})")
    print(f"  line delta: {delta:+d} (expected {expected:+d}) "
          f"({'OK' if delta == expected else 'FAIL'})")
    print(f"  engine-import occurrences post: {post_count} (expect 1, the anti-fork "
          f"invariant) ({'OK' if post_count == 1 else 'FAIL'})")
    if delta != expected or post_count != 1 or pre_o != pre_c or post_o != post_c:
        print("ABORT: nothing written.")
        return 1

    print("\n=== DIFF PREVIEW (first divergence, with context) ===")
    print(diff_preview_first_change(content, sim))

    if not args.apply:
        print("\nDry-run complete. All checks pass. Re-run with --apply to write.")
        return 0

    if not args.reverse:
        BACKUP.write_text(content)
        print(f"\nBackup written: {BACKUP}")
    MANIFEST.write_text(sim)
    disk = MANIFEST.read_text()
    ok = (count_block(disk, ENGINE_IMPORT) == 1
          and (MARKER in disk) != args.reverse)
    print(f"Wrote: {MANIFEST}")
    print("\n=== POST-WRITE DISK VERIFICATION ===")
    print(f"  engine-import occurrences: {count_block(disk, ENGINE_IMPORT)} (expect 1)")
    print(f"  fix marker: {'present' if MARKER in disk else 'absent'} "
          f"({'OK' if ok else 'FAIL'})")
    if not ok:
        print(f"DISK VERIFICATION FAILED. Restore: cp {BACKUP} {MANIFEST}")
        return 1
    print("\nApply complete. All checks pass.")
    print("Next: commit, then docker compose build --no-cache clarityclaw && docker compose up -d")
    print("Then ledger Section E verification (her expr 6/7 rerun; banner advancing")
    print("on active cycles unprompted; her follow-ups arriving without pushes).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
