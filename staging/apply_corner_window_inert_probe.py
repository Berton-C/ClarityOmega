#!/usr/bin/env python3
"""
Diagnostic toggle: make populate-corner-window! inert (differential pinpoint).

THIS IS A PROBE, NOT A FIX. One variable: the only CHANGED call in the proven
death bracket (loop tail lines 175-179; counts 2026-07-07: prune fires 5/5,
DIAG-CYCLE-START fires 0/5) is the 177 hook populate-corner-window!. Its two
writers are probe-proven total in isolation (R/S batteries); the one element
never run in a faithful context is the driver's condition
(corner-confirmed-core) reducing in the full live boot space over the real
(flooded, id-1) atom state.

Forward: the driver body becomes (), leaving the function defined (arity and
name unchanged, loop hook untouched, no rebuild: file is bind-mounted).
Reverse: restores the real driver.

READING THE EXPERIMENT (pre-registered):
- Loop ADVANCES past iteration 1 with the driver inert -> failure convicted
  inside the corner-confirmed-core live reduction; fix targets that chain.
- Loop STILL stuck at iteration 1 -> hook exonerated; suspects become the four
  pre-existing writers under the flooded id-1 atom state.

Usage
-----
Dry-run:  python3 staging/apply_corner_window_inert_probe.py
Apply:    python3 staging/apply_corner_window_inert_probe.py --apply
Reverse:  python3 staging/apply_corner_window_inert_probe.py --reverse --apply
Backup (forward): soul/corner_gap/corner_window_writers.metta.bak.inert_probe
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

WW = Path("soul/corner_gap/corner_window_writers.metta")
BAK = Path("soul/corner_gap/corner_window_writers.metta.bak.inert_probe")

OLD = (
    "(= (populate-corner-window! $cmds $cycle-id)\n"
    "   (if (== (corner-confirmed-core) True)\n"
    "       (do-record-corner-window! $cmds $cycle-id)\n"
    "       (do-clear-corner-window!)))"
)
NEW = (
    ";; INERT-PROBE 2026-07-07: driver disabled for differential pinpoint of the\n"
    ";; cycle-tail failure. Real body preserved in the apply script; --reverse restores.\n"
    "(= (populate-corner-window! $cmds $cycle-id)\n"
    "   ())"
)
MARKER = "INERT-PROBE 2026-07-07"


def parens(text: str) -> tuple[int, int]:
    o = c = 0
    in_s = esc = False
    i = 0
    while i < len(text):
        ch = text[i]
        if in_s:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_s = False
        else:
            if ch == '"':
                in_s = True
            elif ch == ";":
                while i < len(text) and text[i] != "\n":
                    i += 1
                continue
            elif ch == "(":
                o += 1
            elif ch == ")":
                c += 1
        i += 1
    return o, c


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--apply", action="store_true")
    p.add_argument("--reverse", action="store_true")
    a = p.parse_args()
    if not WW.exists():
        print(f"ERROR: {WW} not found. Run from repo root.")
        return 1
    content = WW.read_text()
    src, dst = (NEW, OLD) if a.reverse else (OLD, NEW)
    direction = "REVERSE (inert -> real driver)" if a.reverse else "APPLY (real driver -> inert)"
    print(f"\n>>> INERT PROBE: {direction} <<<")
    n = content.count(src)
    print(f"  anchor count: {n} (expect 1); marker {'present' if MARKER in content else 'absent'}")
    if n != 1 or ((MARKER in content) and not a.reverse):
        print("  Pre-check failed. Aborting; nothing written. Paste the file to re-ground.")
        return 1
    sim = content.replace(src, dst, 1)
    po, pc = parens(sim)
    delta = len(sim.splitlines()) - len(content.splitlines())
    exp = 0
    print(f"  paren post: {po}/{pc} ({'OK' if po == pc else 'FAIL'}); "
          f"line delta {delta:+d} (expected {exp:+d}) ({'OK' if delta == exp else 'FAIL'})")
    if po != pc or delta != exp:
        print("  Aborting; nothing written.")
        return 1
    print("  diff: driver body -> ()" if not a.reverse else "  diff: () -> real driver body")
    if not a.apply:
        print("Dry-run complete. All checks pass. Re-run with --apply to write.")
        return 0
    if not a.reverse:
        BAK.write_text(content)
        print(f"Backup written: {BAK}")
    WW.write_text(sim)
    disk = WW.read_text()
    ok = (MARKER in disk) != a.reverse and parens(disk)[0] == parens(disk)[1]
    print(f"Wrote: {WW}; end state {'OK' if ok else 'FAIL'}")
    if not ok:
        print(f"Restore: cp {BAK} {WW}")
        return 1
    print("Next: docker compose restart clarityclaw, wait ~3 min, then count banners.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
