#!/usr/bin/env python3
"""
Apply script: lib_quantale retirement (quantale math single-sourced to v08.7.2).

Purpose
-------
Berton's direction 2026-07-07: the v08.7.2 engine is THE quantale engine going
forward (many adapters planned); lib_quantale's only consumer surface is the
corner gate; retire lib_quantale now rather than maintain two operator sets.

Survey and probe evidence (all 2026-07-07, in project knowledge):
- lib_quantale's ENTIRE inventory is seven symbols: q-mul, q-join, q-meet,
  q-neg, stv-to-pbit, pbit-to-stv, governance-pbit.
- The v08.7.2 engine defines ALL SEVEN (ops at lines 116-138 with bodies
  IDENTICAL to lib_quantale's, verified side by side; bridges at 188-203)
  plus q-top, q-bot, q-unknown (88-96).
- Loaded consumers of the four ops: lib_self_continuity and
  coupling_quantale_merge; both resolve by name against the engine.
- Loaded consumers of the three bridges: ZERO (full-tree grep, corrected
  names, 2026-07-07).
- ENGINE-ONLY chain probe (inline load, lib_quantale absent): corner-pbit-core
  (mk-pbit 1.0 0.7), corner-confirmed-core true, q-meet exact; EXIT 0. The
  corner chain is proven on engine math alone.
- This retirement also removes the duplicate-head condition (q-meet, q-join,
  q-mul, q-neg each defined twice in the loaded space), the registered
  suspect for the 2026-07-06 iteration-1 infinite loop. The post-retirement
  boot is the direct test of that hypothesis.

The edits (three files, all-or-none)
------------------------------------
FILE 1: lib_clarity_reasoning/lib_clarity_reasoning.metta
  The lib_quantale import line (manifest line 6) is replaced by a retirement
  comment. The file itself stays on disk unimported (archival is Berton's).
FILE 2: soul/corner_gap/coupling_quantale_merge.metta
  Header corrections only (title line, WHAT-THIS-FILE-IS line, DEPENDS-ON
  block, CONFIRM block): dependencies now name the engine and
  lib_self_continuity (q-geq), and the CONFIRM items are marked CONFIRMED by
  the engine-only probe. No code changes; the merge's code is untouched.
FILE 3: soul/corner_gap/cycle_continuity_probe.metta (unimported, future arm)
  One dependency-comment line corrected so the catalog error does not
  propagate when the file ever wires.

Net change (computed and checked at runtime)
--------------------------------------------
- manifest: 1 line -> 3 lines (+2)
- merge: title 0, what-line 0, depends 3 -> 5 (+2), confirm 2 -> 2 (0)
- probe file: 1 line -> 2 lines (+1)
- Paren deltas: 0 everywhere (comment-only and import-line edits)

After apply
-----------
Rebuild required (the manifest is baked):
  docker compose build --no-cache clarityclaw && docker compose up -d
The boot doubles as the duplicate-head loop experiment: v2 wiring remains on
the tree; if the loop was the duplicate heads, it is gone; if it persists,
the hypothesis is falsified and the proven restore path stands
(allowlist --reverse --apply, monolith --reverse --apply, rebuild).

Usage
-----
Dry-run (default):  python3 staging/apply_lib_quantale_retirement.py
Apply:              python3 staging/apply_lib_quantale_retirement.py --apply
Reverse:            python3 staging/apply_lib_quantale_retirement.py --reverse --apply

Backups (forward apply only): <file>.bak.quantale_retirement
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

MANIFEST = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta")
MERGE = Path("soul/corner_gap/coupling_quantale_merge.metta")
PROBE = Path("soul/corner_gap/cycle_continuity_probe.metta")

MARKER = "RETIRED 2026-07-07"

M_OLD = "!(import! &self (library omegaclaw ./lib_clarity_reasoning/lib_quantale))\n"
M_NEW = (
    ";; RETIRED 2026-07-07: lib_quantale fully retired. All seven of its symbols are\n"
    ";; defined by the v08.7.2 engine (imported below in this manifest); zero loaded\n"
    ";; consumers of its bridges existed at retirement (survey + engine-only probe).\n"
)

G_TITLE_OLD = ";; coupling_quantale_merge.metta -- graded corner merge via lib_quantale (pure)\n"
G_TITLE_NEW = ";; coupling_quantale_merge.metta -- graded corner merge via the quantale engine (pure)\n"

G_WHAT_OLD = ";; WHAT THIS FILE IS. The granularity code that makes lib_quantale useful for the\n"
G_WHAT_NEW = ";; WHAT THIS FILE IS. The granularity code that makes the quantale engine useful for the\n"

G_DEP_OLD = (
    ";; DEPENDS ON: lib_quantale (mk-pbit, q-meet, q-neg, q-geq) and the counts in\n"
    ";; coupling_integrity_detector.metta (count-actions-in-window, count-person-actions,\n"
    ";; count-system-actions) and state_delta_writer.metta (latest-state-delta-verdict).\n"
)
G_DEP_NEW = (
    ";; DEPENDS ON: the v08.7.2 quantale engine (mk-pbit, q-meet, q-neg; op bodies\n"
    ";; verified identical to retired lib_quantale, 2026-07-07), q-geq from\n"
    ";; lib_self_continuity, the counts in coupling_integrity_detector.metta\n"
    ";; (count-actions-in-window, count-person-actions, count-system-actions), and\n"
    ";; state_delta_writer.metta (latest-state-delta-verdict).\n"
)

G_CONF_OLD = (
    ";; CONFIRM (REPL, since lib_quantale is COLD per the wiring diagram): that q-meet,\n"
    ";; q-neg, q-geq reduce on these inputs, and that mk-pbit terms compose as expected.\n"
)
G_CONF_NEW = (
    ";; CONFIRMED (engine-only inline probe, 2026-07-07): the full chain reduces with\n"
    ";; lib_quantale absent; corner-pbit-core and corner-confirmed-core exact-match.\n"
)

P_OLD = ";; lib_quantale (mk-pbit, q-meet, q-join, q-geq), coupling_quantale_merge\n"
P_NEW = (
    ";; the v08.7.2 quantale engine (mk-pbit, q-meet, q-join, q-unknown), q-geq from\n"
    ";; lib_self_continuity, coupling_quantale_merge\n"
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


EDITS = {
    "manifest": [(M_OLD, M_NEW)],
    "merge": [(G_TITLE_OLD, G_TITLE_NEW), (G_WHAT_OLD, G_WHAT_NEW),
              (G_DEP_OLD, G_DEP_NEW), (G_CONF_OLD, G_CONF_NEW)],
    "probe": [(P_OLD, P_NEW)],
}
FILES = {"manifest": MANIFEST, "merge": MERGE, "probe": PROBE}
EXPECTED_DELTA = {"manifest": 2, "merge": 2, "probe": 1}


def simulate(name: str, content: str, reverse: bool) -> str:
    for old, new in EDITS[name]:
        src, dst = (new, old) if reverse else (old, new)
        c = count_block(content, src)
        if c != 1:
            raise RuntimeError(f"{name}: anchor found {c} times (expected 1) for block "
                               f"starting {src.splitlines()[0][:60]!r}. Paste the file "
                               f"to re-ground anchors.")
        content = content.replace(src, dst, 1)
    return content


def state_report(name: str, content: str) -> str:
    pre = sum(count_block(content, old) for old, _ in EDITS[name])
    post = sum(count_block(content, new) for _, new in EDITS[name])
    return f"pre-state-blocks={pre} post-state-blocks={post}"


def main() -> int:
    parser = argparse.ArgumentParser(description="lib_quantale retirement apply script")
    parser.add_argument("--apply", action="store_true",
                        help="Actually write changes. Default is dry-run.")
    parser.add_argument("--reverse", action="store_true",
                        help="Reverse the retirement. Combine with --apply to write.")
    args = parser.parse_args()

    direction = "REVERSE (retirement -> prior)" if args.reverse else "APPLY (prior -> retirement)"
    print(f"\n>>> LIB_QUANTALE RETIREMENT: {direction} <<<")

    originals: dict[str, str] = {}
    simulated: dict[str, str] = {}

    print("\n=== PRE-EDIT CHECKS ===")
    for name, path in FILES.items():
        if not path.exists():
            print(f"ERROR: {path} not found. Run from repo root.")
            return 1
        content = path.read_text()
        originals[name] = content
        o, c = code_aware_paren_count(content)
        print(f"  {name}: paren opens={o} closes={c} ({'OK' if o == c else 'FAIL'}); "
              f"{state_report(name, content)}")
        if o != c:
            print("Aborting: unbalanced file pre-edit.")
            return 1
        expected_pre = len(EDITS[name]) if not args.reverse else 0
        pre = sum(count_block(content, old) for old, _ in EDITS[name])
        if pre != expected_pre:
            print(f"  {name}: pre-state mismatch (found {pre} original blocks, "
                  f"expected {expected_pre} for this direction). Aborting.")
            return 1

    print("\n=== SIMULATION ===")
    for name, path in FILES.items():
        try:
            simulated[name] = simulate(name, originals[name], args.reverse)
        except RuntimeError as exc:
            print(f"  {name} simulation FAILED: {exc}")
            return 1
        o, c = code_aware_paren_count(simulated[name])
        delta = len(simulated[name].splitlines()) - len(originals[name].splitlines())
        expected = -EXPECTED_DELTA[name] if args.reverse else EXPECTED_DELTA[name]
        ok = o == c and delta == expected
        print(f"  {name}: paren post opens={o} closes={c}; line delta {delta:+d} "
              f"(expected {expected:+d}) ({'OK' if ok else 'FAIL'})")
        if not ok:
            print("Aborting; no disk write.")
            return 1

    print("\n=== DIFF PREVIEWS ===")
    for name in FILES:
        print(f"--- {name} ({FILES[name]}) ---")
        for old, new in EDITS[name]:
            src, dst = (new, old) if args.reverse else (old, new)
            for line in src.splitlines():
                print(f"- {line}")
            for line in dst.splitlines():
                print(f"+ {line}")
        print()

    if not args.apply:
        print("=== DRY-RUN COMPLETE ===")
        print("All checks pass. Re-run with --apply to write.")
        return 0

    if not args.reverse:
        for name, path in FILES.items():
            bak = Path(str(path) + ".bak.quantale_retirement")
            if bak.exists():
                print(f"WARNING: backup {bak} exists; overwriting.")
            bak.write_text(originals[name])
            print(f"Backup written: {bak}")

    print("\n=== WRITING ===")
    for name, path in FILES.items():
        path.write_text(simulated[name])
        print(f"Wrote: {path}")

    print("\n=== POST-WRITE DISK VERIFICATION ===")
    all_ok = True
    for name, path in FILES.items():
        disk = path.read_text()
        o, c = code_aware_paren_count(disk)
        post = sum(count_block(disk, new) for _, new in EDITS[name])
        expected_post = 0 if args.reverse else len(EDITS[name])
        ok = o == c and post == expected_post
        print(f"  {name}: paren {'OK' if o == c else 'FAIL'}; "
              f"end-state blocks {post}/{expected_post} ({'OK' if ok else 'FAIL'})")
        all_ok = all_ok and ok
    if not all_ok:
        print("\nDISK VERIFICATION FAILED. Restore:")
        for name, path in FILES.items():
            print(f"  cp {path}.bak.quantale_retirement {path}")
        return 1

    print("\n=== RETIREMENT COMPLETE. All checks pass. ===")
    if not args.reverse:
        print("Next: commit, then rebuild (manifest is baked; hotspot for the")
        print("network trap), then the boot doubles as the duplicate-head loop test:")
        print("  docker compose build --no-cache clarityclaw && docker compose up -d")
        print("  sleep 60 ; docker logs clarity_omega 2>&1 | grep -cE 'DIAG-POPULATOR-PRUNE'")
        print("  docker logs clarity_omega 2>&1 | grep -E 'iteration|Unknown procedure|exited' | head")
    return 0


if __name__ == "__main__":
    sys.exit(main())
