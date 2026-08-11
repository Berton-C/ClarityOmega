#!/usr/bin/env python3
"""
Apply script: death-window trace sentinels (five edits, five files, all-or-none).

THIS IS A DIAGNOSTIC, NOT A FIX. No commit until the culprit is named; fully
reversible; no behavior change (each edit adds exactly one println! binding).

Why
---
The cycle conjunction provably dies between the populator's PRUNE diag and
DIAG-CYCLE-START (line 180) every cycle (counts 2026-07-07: PRUNE 5/5, d1 0/5,
AB-PERSON 0). Every function body in that window is now TOTAL BY VERBATIM READ
(populator interior, state-delta writer, coupling writer plus its June-4 bugfix
record, idle writer per the Bug-2 record, agency counters). Text-total yet
live-failing means the failure is a live-reduction fact; the window contains
ZERO prints, so localization needs sentinels, not more reading.

The five edits (one println! binding each, +1 line per file)
------------------------------------------------------------
1. recent_action_populator.metta: ($_exit (println! (TRACE-172-EXIT))) as the
   final let* binding (proves the populator COMPLETES).
2. state_delta_writer_writers.metta: ($_entry (println! (TRACE-175-ENTRY)))
   first binding of populate-state-delta.
3. coupling_integrity_detector_writers.metta: ($_entry (println!
   (TRACE-176-ENTRY))) first binding of populate-coupling-verdict.
4. idle_cycle_detector_writers.metta: ($_entry (println! (TRACE-178-ENTRY)))
   first binding of do-update-idle-pattern!.
5. agency_balance_guard_writers.metta: ($_entry (println! (TRACE-179-ENTRY)))
   first binding of do-update-agency-balance! (fires BEFORE the counter
   bindings, unlike the existing AB-PERSON print which fires after).

Reading the result (pre-registered)
-----------------------------------
After restart, the LAST sentinel firing names the failure:
- no TRACE-172-EXIT: death inside the populator's post-PRUNE live reduction.
- 172-EXIT but no 175-ENTRY: death in loop lines 173-174 (the two bindings).
- 175 but no 176: inside populate-state-delta (classify-state-delta chain).
- 176 but no 178: inside populate-coupling-verdict (coupling-verdict chain).
- 178 but no 179: inside do-update-idle-pattern!.
- 179 but no DIAG-WRITER-AB-PERSON: inside the agency counters' live reduction.
- all five plus AB prints, and d1 still absent: the contradiction escalates to
  the loop text between 179 and 180, which the June-21 diff already cleared,
  forcing a re-read of the d1 line itself.

Anchors are verbatim from live reads this session (populator sed, state-delta
sed, coupling body from project knowledge, idle/agency writer bodies from the
copies with fail-loud counts). Any anchor mismatch aborts writing NOTHING;
paste the named file to re-ground.

Usage
-----
Dry-run:  python3 staging/apply_death_window_trace_sentinels.py
Apply:    python3 staging/apply_death_window_trace_sentinels.py --apply
Reverse:  python3 staging/apply_death_window_trace_sentinels.py --reverse --apply
Backups (forward): <file>.bak.trace_sentinels
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

MARKER = "TRACE-17"

E1_PATH = Path("soul/recent_action_populator.metta")
E1_OLD = (
    "          ($_prune       (let $old (superpose $to-remove)\n"
    "                                   (if (== $old ())\n"
    "                                       ()\n"
    "                                       (remove-atom &self $old)))))\n"
    "         ()))"
)
E1_NEW = (
    "          ($_prune       (let $old (superpose $to-remove)\n"
    "                                   (if (== $old ())\n"
    "                                       ()\n"
    "                                       (remove-atom &self $old))))\n"
    "          ($_exit        (println! (TRACE-172-EXIT))))\n"
    "         ()))"
)

E2_PATH = Path("soul/corner_gap/state_delta_writer_writers.metta")
E2_OLD = (
    "(= (populate-state-delta $msgnew $results-nonempty $results-novel $cycle-id)\n"
    "   (let* (($verdict (classify-state-delta $msgnew $results-nonempty $results-novel))"
)
E2_NEW = (
    "(= (populate-state-delta $msgnew $results-nonempty $results-novel $cycle-id)\n"
    "   (let* (($_entry (println! (TRACE-175-ENTRY)))\n"
    "          ($verdict (classify-state-delta $msgnew $results-nonempty $results-novel))"
)

E3_PATH = Path("soul/corner_gap/coupling_integrity_detector_writers.metta")
E3_OLD = (
    "(= (populate-coupling-verdict $cycle-id)\n"
    "   (let* (($verdict (coupling-verdict))"
)
E3_NEW = (
    "(= (populate-coupling-verdict $cycle-id)\n"
    "   (let* (($_entry (println! (TRACE-176-ENTRY)))\n"
    "          ($verdict (coupling-verdict))"
)

E4_PATH = Path("soul/idle_cycle_detector_writers.metta")
E4_OLD = (
    "(= (do-update-idle-pattern!)\n"
    "   (let* (($count (count-sends-in-window))"
)
E4_NEW = (
    "(= (do-update-idle-pattern!)\n"
    "   (let* (($_entry (println! (TRACE-178-ENTRY)))\n"
    "          ($count (count-sends-in-window))"
)

E5_PATH = Path("soul/agency_balance_guard_writers.metta")
E5_OLD = (
    "(= (do-update-agency-balance!)\n"
    "   (let* (($person (count-person-actions-in-window))"
)
E5_NEW = (
    "(= (do-update-agency-balance!)\n"
    "   (let* (($_entry (println! (TRACE-179-ENTRY)))\n"
    "          ($person (count-person-actions-in-window))"
)

EDITS = [
    ("populator exit", E1_PATH, E1_OLD, E1_NEW, 1),
    ("state-delta entry", E2_PATH, E2_OLD, E2_NEW, 1),
    ("coupling entry", E3_PATH, E3_OLD, E3_NEW, 1),
    ("idle entry", E4_PATH, E4_OLD, E4_NEW, 1),
    ("agency entry", E5_PATH, E5_OLD, E5_NEW, 1),
]


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Death-window trace sentinels")
    parser.add_argument("--apply", action="store_true",
                        help="Actually write changes. Default is dry-run.")
    parser.add_argument("--reverse", action="store_true",
                        help="Remove the sentinels. Combine with --apply to write.")
    args = parser.parse_args()

    direction = "REVERSE (sentinels out)" if args.reverse else "APPLY (sentinels in)"
    print(f"\n>>> DEATH-WINDOW TRACE SENTINELS: {direction} <<<")

    plan = []
    print("\n=== PRE-EDIT CHECKS ===")
    for label, path, old, new, delta in EDITS:
        if not path.exists():
            print(f"ERROR: {path} not found. Run from repo root.")
            return 1
        content = path.read_text()
        src, dst = (new, old) if args.reverse else (old, new)
        c = count_block(content, src)
        po, pc = code_aware_paren_count(content)
        print(f"  {label} ({path.name}): anchor count {c} (expect 1); "
              f"paren {po}/{pc} ({'OK' if po == pc else 'FAIL'})")
        if c != 1 or po != pc:
            print(f"  ABORT: anchor or paren failure in {path}. Nothing written. "
                  f"Paste the file to re-ground.")
            return 1
        plan.append((label, path, content, content.replace(src, dst, 1), delta))

    print("\n=== SIMULATION ===")
    for label, path, orig, sim, delta in plan:
        po, pc = code_aware_paren_count(sim)
        d = len(sim.splitlines()) - len(orig.splitlines())
        exp = -delta if args.reverse else delta
        ok = po == pc and d == exp
        print(f"  {label}: paren post {po}/{pc}; line delta {d:+d} "
              f"(expected {exp:+d}) ({'OK' if ok else 'FAIL'})")
        if not ok:
            print("  ABORT: nothing written.")
            return 1

    print("\n=== DIFF PREVIEWS ===")
    for label, path, orig, sim, _ in plan:
        old_l = orig.splitlines()
        new_l = sim.splitlines()
        i = 0
        while i < min(len(old_l), len(new_l)) and old_l[i] == new_l[i]:
            i += 1
        print(f"--- {label} ({path.name}) at line {i + 1} ---")
        for k in range(max(0, i - 1), min(len(new_l), i + 3)):
            tag = "+" if k >= i and (k >= len(old_l) or old_l[k] != new_l[k]) else " "
            print(f"{tag} {new_l[k]}")
        print()

    if not args.apply:
        print("=== DRY-RUN COMPLETE ===")
        print("All checks pass. Re-run with --apply to write.")
        return 0

    for label, path, orig, sim, _ in plan:
        if not args.reverse:
            bak = Path(str(path) + ".bak.trace_sentinels")
            bak.write_text(orig)
            print(f"Backup written: {bak}")
        path.write_text(sim)
        print(f"Wrote: {path}")

    print("\n=== POST-WRITE DISK VERIFICATION ===")
    all_ok = True
    for label, path, _, _, _ in plan:
        disk = path.read_text()
        po, pc = code_aware_paren_count(disk)
        m_ok = (MARKER in disk) != args.reverse
        ok = po == pc and m_ok
        print(f"  {label}: paren {'OK' if po == pc else 'FAIL'}; sentinel "
              f"{'present' if MARKER in disk else 'absent'} ({'OK' if ok else 'FAIL'})")
        all_ok = all_ok and ok
    if not all_ok:
        print("VERIFICATION FAILED. Restore from the .bak.trace_sentinels files.")
        return 1
    print("\nDone. Next: docker compose restart clarityclaw, wait ~3 min, then:")
    print("  docker logs clarity_omega --since 3m 2>&1 | grep -F 'TRACE-17' | tail -12")
    print("  docker logs clarity_omega --since 3m 2>&1 | grep -F 'DIAG-WRITER-AB-PERSON' | grep -v println | tail -3")
    return 0


if __name__ == "__main__":
    sys.exit(main())
