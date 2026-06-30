#!/usr/bin/env python3
"""apply_clear_fn_superpose_fix.py

Fix Bug 2 + Bug 2b: do-clear-idle-pattern! and do-clear-agency-balance! have
been removing zero atoms since cycle 1 because the (remove-atom &self
(car-atom $existing)) pattern is unreliable in this runtime.

Replace with the superpose-iteration pattern proven by recent_action_populator's
pruning logic. While we're in agency_balance_guard_writers.metta, also add
symmetric DIAG-WRITER-* prints to do-update-agency-balance! so we can see
agency-balance internals the same way we see idle-pattern internals.

Reversibility:
    --apply   : forward edit
    --reverse : restore original
    (no flag) : dry-run, no writes
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


# ============================================================================
# FILE PATHS
# ============================================================================

IDLE_PATH = Path("soul/idle_cycle_detector_writers.metta")
IDLE_BAK = Path("soul/idle_cycle_detector_writers.metta.bak.clearfix")

AB_PATH = Path("soul/agency_balance_guard_writers.metta")
AB_BAK = Path("soul/agency_balance_guard_writers.metta.bak.clearfix")


# ============================================================================
# EDIT 1: do-clear-idle-pattern! superpose-iteration fix
# soul/idle_cycle_detector_writers.metta
# ============================================================================

IDLE_CLEAR_ANCHOR = """;; Removes prior idle-pattern atom (C12-safe).
(= (do-clear-idle-pattern!)
   (let $existing (collapse (match &self (idle-pattern $v $c) (idle-pattern $v $c)))
      (if (== $existing ())
          _
          (remove-atom &self (car-atom $existing)))))"""

IDLE_CLEAR_NEW = """;; Removes ALL prior idle-pattern atoms (C12-safe).
;; Bug-2 fix (May 20 2026): car-atom + remove-atom pattern was removing zero
;; atoms in this runtime, causing 50+ stale (idle-pattern productive 0) atoms
;; to accumulate from cycle 1 onward. current-idle-pattern reads via car-atom
;; which returns the OLDEST atom (bootstrap), explaining stale prompt data.
;; Fix mirrors recent_action_populator's verified-working pruning shape.
(= (do-clear-idle-pattern!)
   (let $existing (collapse (match &self (idle-pattern $v $c) (idle-pattern $v $c)))
      (if (== $existing ())
          _
          (let $old (superpose $existing)
                    (if (== $old ())
                        ()
                        (remove-atom &self $old))))))"""


# ============================================================================
# EDIT 2: do-clear-agency-balance! superpose-iteration fix
# soul/agency_balance_guard_writers.metta
# ============================================================================

AB_CLEAR_ANCHOR = """;; Removes prior agency-balance atom (C12-safe).
(= (do-clear-agency-balance!)
   (let $existing (collapse (match &self (agency-balance $v $p $s) (agency-balance $v $p $s)))
      (if (== $existing ())
          _
          (remove-atom &self (car-atom $existing)))))"""

AB_CLEAR_NEW = """;; Removes ALL prior agency-balance atoms (C12-safe).
;; Bug-2b fix (May 20 2026): same car-atom + remove-atom pathology as
;; do-clear-idle-pattern!. current-agency-balance reads via car-atom
;; returning the OLDEST atom (bootstrap), explaining stale (dependency-risk 0 1)
;; in prompt context. Fix mirrors populator's verified-working pruning shape.
(= (do-clear-agency-balance!)
   (let $existing (collapse (match &self (agency-balance $v $p $s) (agency-balance $v $p $s)))
      (if (== $existing ())
          _
          (let $old (superpose $existing)
                    (if (== $old ())
                        ()
                        (remove-atom &self $old))))))"""


# ============================================================================
# EDIT 3: do-update-agency-balance! gets DIAG-WRITER-* prints
# soul/agency_balance_guard_writers.metta
# Symmetric to existing prints in do-update-idle-pattern!.
# ============================================================================

AB_UPDATE_ANCHOR = """(= (do-update-agency-balance!)
   (let* (($person (count-person-actions-in-window))
          ($system (count-system-actions-in-window))
          ($verdict (if (dependency-detected $person $system)
                        dependency-risk
                        healthy)))
      (progn
         (do-clear-agency-balance!)
         (add-atom &self (agency-balance $verdict $person $system)))))"""

AB_UPDATE_NEW = """(= (do-update-agency-balance!)
   (let* (($person (count-person-actions-in-window))
          ($system (count-system-actions-in-window))
          ($verdict (if (dependency-detected $person $system)
                        dependency-risk
                        healthy)))
      (progn
         (println! (DIAG-WRITER-AB-PERSON $person))
         (println! (DIAG-WRITER-AB-SYSTEM $system))
         (println! (DIAG-WRITER-AB-VERDICT $verdict))
         (do-clear-agency-balance!)
         (println! (DIAG-WRITER-AB-POST-CLEAR (collapse (match &self (agency-balance $v $p $s) ($v $p $s)))))
         (add-atom &self (agency-balance $verdict $person $system)))))"""


# ============================================================================
# UTILITIES
# ============================================================================

def read_file(path: Path) -> str:
    return path.read_text()


def write_file(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        return
    path.write_text(content)


def backup_if_needed(src: Path, bak: Path, dry_run: bool) -> None:
    if dry_run:
        return
    if bak.exists():
        return
    bak.write_text(src.read_text())


def count_substr(haystack: str, needle: str) -> int:
    if not needle:
        return 0
    return haystack.count(needle)


# ============================================================================
# PROCESSORS
# ============================================================================

def process_idle(direction: str, dry_run: bool) -> dict:
    """One replacement in soul/idle_cycle_detector_writers.metta:
       do-clear-idle-pattern! superpose-iteration fix."""
    text = read_file(IDLE_PATH)
    pre_lines = text.count("\n")

    if direction == "apply":
        anchor, new = IDLE_CLEAR_ANCHOR, IDLE_CLEAR_NEW
        state_check_label = "pre-fix car-atom pattern present"
    else:
        anchor, new = IDLE_CLEAR_NEW, IDLE_CLEAR_ANCHOR
        state_check_label = "post-fix superpose pattern present"

    if anchor not in text:
        return {
            "path": str(IDLE_PATH),
            "ok": False,
            "message": f"Anchor not found: state check failed ({state_check_label})",
            "pre_lines": pre_lines,
        }
    count = count_substr(text, anchor)
    if count != 1:
        return {
            "path": str(IDLE_PATH),
            "ok": False,
            "message": f"Anchor match count = {count}, expected 1",
            "pre_lines": pre_lines,
        }

    new_text = text.replace(anchor, new, 1)

    backup_if_needed(IDLE_PATH, IDLE_BAK, dry_run)
    write_file(IDLE_PATH, new_text, dry_run)

    post_lines = new_text.count("\n")
    return {
        "path": str(IDLE_PATH),
        "ok": True,
        "pre_lines": pre_lines,
        "post_lines": post_lines,
        "line_delta": post_lines - pre_lines,
        "edit": "rewrite do-clear-idle-pattern! using superpose iteration" if direction == "apply" else "restore car-atom pattern in do-clear-idle-pattern!",
    }


def process_ab(direction: str, dry_run: bool) -> dict:
    """Two replacements in soul/agency_balance_guard_writers.metta:
       1. do-clear-agency-balance! superpose-iteration fix
       2. do-update-agency-balance! gains DIAG-WRITER-AB-* prints (symmetric to
          existing DIAG-WRITER-* prints inside do-update-idle-pattern!)."""
    text = read_file(AB_PATH)
    pre_lines = text.count("\n")

    if direction == "apply":
        anchors = [
            (AB_CLEAR_ANCHOR, AB_CLEAR_NEW, "do-clear-agency-balance! superpose fix"),
            (AB_UPDATE_ANCHOR, AB_UPDATE_NEW, "do-update-agency-balance! DIAG-WRITER prints"),
        ]
        state_check_label = "pre-fix car-atom pattern present + diagnostic prints absent"
    else:
        anchors = [
            (AB_CLEAR_NEW, AB_CLEAR_ANCHOR, "do-clear-agency-balance! superpose fix"),
            (AB_UPDATE_NEW, AB_UPDATE_ANCHOR, "do-update-agency-balance! DIAG-WRITER prints"),
        ]
        state_check_label = "post-fix superpose pattern present + diagnostic prints present"

    for anchor, new, label in anchors:
        if anchor not in text:
            return {
                "path": str(AB_PATH),
                "ok": False,
                "message": f"Anchor not found for {label}: state check failed ({state_check_label})",
                "pre_lines": pre_lines,
            }
        count = count_substr(text, anchor)
        if count != 1:
            return {
                "path": str(AB_PATH),
                "ok": False,
                "message": f"Anchor for {label} count = {count}, expected 1",
                "pre_lines": pre_lines,
            }

    new_text = text
    for anchor, new, label in anchors:
        new_text = new_text.replace(anchor, new, 1)

    backup_if_needed(AB_PATH, AB_BAK, dry_run)
    write_file(AB_PATH, new_text, dry_run)

    post_lines = new_text.count("\n")
    edit_label = (
        "rewrite do-clear-agency-balance! using superpose iteration + add DIAG-WRITER-AB-* prints to do-update-agency-balance!"
        if direction == "apply"
        else "restore car-atom pattern in do-clear-agency-balance! + remove DIAG-WRITER-AB-* prints from do-update-agency-balance!"
    )
    return {
        "path": str(AB_PATH),
        "ok": True,
        "pre_lines": pre_lines,
        "post_lines": post_lines,
        "line_delta": post_lines - pre_lines,
        "edit": edit_label,
    }


# ============================================================================
# MAIN
# ============================================================================


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--apply", action="store_true", help="Write changes to disk")
    parser.add_argument("--reverse", action="store_true", help="Reverse direction")
    args = parser.parse_args()

    direction = "reverse" if args.reverse else "apply"
    dry_run = not args.apply

    print()
    print("=" * 78)
    print(f"  CLEAR-FN SUPERPOSE FIX: {direction.upper()} ({'DRY-RUN' if dry_run else 'WRITING'})")
    print("=" * 78)
    print()

    for p in [IDLE_PATH, AB_PATH]:
        if not p.exists():
            print(f"  ERROR: {p} does not exist. Are you at repo root?")
            return 1

    print(">>> Per-file state checks and edits <<<")
    print()

    results = []
    processors = [
        (process_idle, "soul/idle_cycle_detector_writers.metta"),
        (process_ab, "soul/agency_balance_guard_writers.metta"),
    ]

    for processor, label in processors:
        print(f"  [{label}]")
        result = processor(direction, dry_run=True)
        if not result.get("ok"):
            print(f"    FAIL: {result.get('message')}")
            print()
            print("  Halting -- no changes written.")
            return 1
        pre_l = result.get("pre_lines")
        post_l = result.get("post_lines")
        delta_l = result.get("line_delta")
        print(f"    Lines: {pre_l} -> {post_l} (delta {delta_l:+d})")
        print(f"    Edit: {result.get('edit')}")
        results.append((label, result))
        print()

    print("=" * 78)
    print(f"  SUMMARY: WHAT --{direction} --apply WILL DO")
    print("=" * 78)
    print()
    print(f"  Direction: {direction.upper()}")
    print(f"  Backup suffix: .bak.clearfix")
    print()
    for label, r in results:
        print(f"  {label}: {r.get('edit')}")
        print(f"    {r.get('pre_lines')} -> {r.get('post_lines')} lines (delta {r.get('line_delta'):+d})")
    print()
    print("  Total edits: 2 files")
    print("    - soul/idle_cycle_detector_writers.metta: 1 edit (do-clear-idle-pattern!)")
    print("    - soul/agency_balance_guard_writers.metta: 2 edits (do-clear + DIAG-WRITER-AB-* prints)")
    print("  Contract: substrate fix (Bug 2 + Bug 2b) + symmetric diagnostic surface for agency-balance.")
    print("  Existing loop-level diagnostic prints (DIAG-IDLE-PATTERN-ATOMS etc.) remain in place.")
    print(f"  Reversibility: python3 {Path(sys.argv[0]).name} --reverse --apply")
    print()
    print("  Rebuild required after apply:")
    print("    docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw")
    print()
    print("  Behavioral verification after rebuild:")
    print("    Cycle 1 post-fix: DIAG-IDLE-PATTERN-COUNT should drop from 57 to 1.")
    print("    Cycle 1 post-fix: DIAG-WRITER-AB-POST-CLEAR should show ().")
    print("    Watch first cycle for any stall on heavy initial clear (~57 atoms via superpose).")
    print("    If first cycle stalls: writer fails to complete, count stays high one cycle.")
    print("    Steady-state: both counts should equal 1 every wake cycle.")
    print()

    if dry_run:
        print("  DRY-RUN MODE: no files written. To apply, add --apply.")
        return 0

    print("=" * 78)
    print("  WRITING")
    print("=" * 78)
    print()
    final_results = []
    for processor, label in processors:
        result = processor(direction, dry_run=False)
        if not result.get("ok"):
            print(f"  FAIL on {label}: {result.get('message')}")
            return 1
        print(f"  Wrote: {label}")
        final_results.append((label, result))
    print()

    print("=" * 78)
    print("  DISK VERIFICATION")
    print("=" * 78)
    print()
    for label, r in final_results:
        print(f"  {label}: {r.get('post_lines')} lines, edit applied")
    print()
    print("=" * 78)
    print(f"  CLEAR-FN SUPERPOSE FIX {direction.upper()} COMPLETE")
    print("=" * 78)
    print()
    if direction == "apply":
        print("  NEXT:")
        print("    docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw")
        print("    docker logs -f clarity_omega 2>&1 | grep -E 'DIAG-(IDLE-PATTERN-COUNT|WRITER-AB|CYCLE)'")
        print("    Watch first wake cycle: DIAG-IDLE-PATTERN-COUNT should drop to 1.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
