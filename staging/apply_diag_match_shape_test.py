#!/usr/bin/env python3
"""
Apply script: maximal-surface diagnostic prints for Bug 1, Bug 2, Bug 3.

Anchors below are pulled VERBATIM from the actual deployed files
(via project_knowledge_search), not from assumptions about whitespace.

Modifies three files:
  src/loop.metta
  soul/idle_cycle_detector_writers.metta
  soul/recent_action_populator.metta

Backup suffix: .bak.diagprint

Usage
-----
Dry-run (default):
    python3 staging/apply_diag_match_shape_test.py
Apply:
    python3 staging/apply_diag_match_shape_test.py --apply
Reverse:
    python3 staging/apply_diag_match_shape_test.py --reverse --apply

Output prints (every cycle, all prefixed with DIAG- for greppability):

From populator (after $to-remove computed, before pruning fires):
  (DIAG-POPULATOR-PRUNE cycle-id N prune-before M to-remove (...))

From idle-pattern writer (inside do-update-idle-pattern!):
  (DIAG-WRITER-COUNT N)              -- what count-sends-in-window returned
  (DIAG-WRITER-VERDICT V)            -- verdict derived
  (DIAG-WRITER-POST-CLEAR (...))     -- atoms remaining after clear

From loop tail (after do-update-agency-balance!):
  (DIAG-CYCLE-START $k)
  (DIAG-COUNT-FN N)                   -- count-sends-in-window from loop context
  (DIAG-LITERAL-RESPONSIVE (...))     -- literal-tag match for responsive-send
  (DIAG-LITERAL-STATUS (...))         -- literal-tag match for status-send-unprompted
  (DIAG-VARIABLE-TAG (...))           -- variable-tag baseline match
  (DIAG-RECENT-ACTION-COUNT N)        -- total recent-action atoms (Bug 3 indicator)
  (DIAG-IDLE-PATTERN-ATOMS (...))     -- all idle-pattern atoms
  (DIAG-IDLE-PATTERN-COUNT N)         -- count of idle-pattern atoms (Bug 2 indicator)
  (DIAG-CYCLE-END $k)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# ============================================================================
# FILE PATHS
# ============================================================================

LOOP_PATH = Path("src/loop.metta")
WRITERS_PATH = Path("soul/idle_cycle_detector_writers.metta")
POPULATOR_PATH = Path("soul/recent_action_populator.metta")

LOOP_BAK = Path("src/loop.metta.bak.diagprint")
WRITERS_BAK = Path("soul/idle_cycle_detector_writers.metta.bak.diagprint")
POPULATOR_BAK = Path("soul/recent_action_populator.metta.bak.diagprint")

# ============================================================================
# ANCHORS - verbatim from the deployed files (via project_knowledge_search)
# ============================================================================

# ----- POPULATOR -----
# Anchor: the $_prune binding, which is the last let* binding.
# We insert a DIAG print binding immediately before it so we see what
# pruning is about to attempt.
POPULATOR_ANCHOR = """          ($_prune       (let $old (superpose $to-remove)
                                   (if (== $old ())
                                       ()
                                       (remove-atom &self $old)))))"""

POPULATOR_NEW = """          ($_diag_prune  (println! (DIAG-POPULATOR-PRUNE cycle-id $cycle-id prune-before $prune-before to-remove $to-remove)))
          ($_prune       (let $old (superpose $to-remove)
                                   (if (== $old ())
                                       ()
                                       (remove-atom &self $old)))))"""

# ----- WRITERS (idle_cycle_detector_writers.metta) -----
# Anchor: the entire do-update-idle-pattern! definition.
WRITERS_ANCHOR = """(= (do-update-idle-pattern!)
   (let* (($count (count-sends-in-window))
          ($verdict (if (> $count 3)
                        send-burst
                        productive)))
      (progn
         (do-clear-idle-pattern!)
         (add-atom &self (idle-pattern $verdict $count)))))"""

WRITERS_NEW = """(= (do-update-idle-pattern!)
   (let* (($count (count-sends-in-window))
          ($_diag_count (println! (DIAG-WRITER-COUNT $count)))
          ($verdict (if (> $count 3)
                        send-burst
                        productive))
          ($_diag_verdict (println! (DIAG-WRITER-VERDICT $verdict))))
      (progn
         (do-clear-idle-pattern!)
         (println! (DIAG-WRITER-POST-CLEAR (collapse (match &self (idle-pattern $v $c) ($v $c)))))
         (add-atom &self (idle-pattern $verdict $count)))))"""

# ----- LOOP -----
# Anchor: the three tail bindings + the closing paren that ends the outer let*.
# Verbatim from loop_copy_metta.txt around line 137-139.
LOOP_ANCHOR = """                                       ($_ (populate-recent-action $sexpr $msgnew $k))
                                       ($_ (do-update-idle-pattern!))
                                       ($_ (do-update-agency-balance!)))"""

LOOP_NEW = """                                       ($_ (populate-recent-action $sexpr $msgnew $k))
                                       ($_ (do-update-idle-pattern!))
                                       ($_ (do-update-agency-balance!))
                                       ($_d1 (println! (DIAG-CYCLE-START $k)))
                                       ($_d2 (println! (DIAG-COUNT-FN (count-sends-in-window))))
                                       ($_d3 (println! (DIAG-LITERAL-RESPONSIVE (collapse (match &self (recent-action $c responsive-send $d) $c)))))
                                       ($_d4 (println! (DIAG-LITERAL-STATUS (collapse (match &self (recent-action $c status-send-unprompted $d) $c)))))
                                       ($_d5 (println! (DIAG-VARIABLE-TAG (collapse (match &self (recent-action $c $t $d) ($c $t))))))
                                       ($_d6 (println! (DIAG-RECENT-ACTION-COUNT (size-atom (collapse (match &self (recent-action $c $t $d) $c))))))
                                       ($_d7 (println! (DIAG-IDLE-PATTERN-ATOMS (collapse (match &self (idle-pattern $v $c) ($v $c))))))
                                       ($_d8 (println! (DIAG-IDLE-PATTERN-COUNT (size-atom (collapse (match &self (idle-pattern $v $c) (idle-pattern $v $c)))))))
                                       ($_d9 (println! (DIAG-CYCLE-END $k))))"""

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

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


def find_substring_count(text: str, target: str) -> int:
    count = 0
    start = 0
    while True:
        idx = text.find(target, start)
        if idx == -1:
            break
        count += 1
        start = idx + 1
    return count


def diff_preview(old: str, new: str, label: str, context: int = 3) -> str:
    old_lines = old.splitlines()
    new_lines = new.splitlines()
    out = [f"--- diff preview: {label} ---"]
    if old_lines == new_lines:
        out.append("(no change)")
        return "\n".join(out)

    min_len = min(len(old_lines), len(new_lines))
    differ_start = None
    for i in range(min_len):
        if old_lines[i] != new_lines[i]:
            differ_start = i
            break
    if differ_start is None:
        differ_start = min_len

    old_back = len(old_lines) - 1
    new_back = len(new_lines) - 1
    while old_back > differ_start and new_back > differ_start and old_lines[old_back] == new_lines[new_back]:
        old_back -= 1
        new_back -= 1

    start = max(0, differ_start - context)
    for i in range(start, differ_start):
        out.append(f"  {old_lines[i]}")
    for i in range(differ_start, old_back + 1):
        out.append(f"- {old_lines[i]}")
    for i in range(differ_start, new_back + 1):
        out.append(f"+ {new_lines[i]}")
    end_old = min(len(old_lines), old_back + 1 + context)
    for i in range(old_back + 1, end_old):
        out.append(f"  {old_lines[i]}")
    return "\n".join(out)


def transform(content: str, anchor: str, replacement: str, label: str) -> str:
    """Replace anchor with replacement. Verify exactly one match."""
    count = find_substring_count(content, anchor)
    if count != 1:
        raise RuntimeError(
            f"{label}: expected exactly 1 occurrence of anchor, found {count}.\n"
            f"  This usually means the deployed file differs from the anchor.\n"
            f"  Anchor (first 100 chars): {anchor[:100]!r}"
        )
    return content.replace(anchor, replacement, 1)


# ============================================================================
# PER-FILE EDIT FUNCTIONS
# ============================================================================

def edit_populator(content: str, reverse: bool) -> str:
    if reverse:
        return transform(content, POPULATOR_NEW, POPULATOR_ANCHOR, "populator")
    else:
        return transform(content, POPULATOR_ANCHOR, POPULATOR_NEW, "populator")


def edit_writers(content: str, reverse: bool) -> str:
    if reverse:
        return transform(content, WRITERS_NEW, WRITERS_ANCHOR, "writers")
    else:
        return transform(content, WRITERS_ANCHOR, WRITERS_NEW, "writers")


def edit_loop(content: str, reverse: bool) -> str:
    if reverse:
        return transform(content, LOOP_NEW, LOOP_ANCHOR, "loop")
    else:
        return transform(content, LOOP_ANCHOR, LOOP_NEW, "loop")


# ============================================================================
# MAIN
# ============================================================================

def process_file(path: Path, bak: Path, edit_fn, reverse: bool, apply: bool, label: str) -> bool:
    print(f"\n{'='*60}")
    print(f"FILE: {label} ({path})")
    print(f"{'='*60}")

    if not path.exists():
        print(f"  ERROR: file not found")
        return False

    content = path.read_text()
    pre_o, pre_c = code_aware_paren_count(content)
    pre_d = pre_o - pre_c
    pre_lines = len(content.splitlines())
    print(f"  pre:  opens={pre_o} closes={pre_c} delta={pre_d} lines={pre_lines}")

    if pre_d != 0:
        print(f"  ERROR: pre-edit paren delta non-zero. Aborting.")
        return False

    try:
        new_content = edit_fn(content, reverse)
    except RuntimeError as exc:
        print(f"  ERROR: {exc}")
        return False

    post_o, post_c = code_aware_paren_count(new_content)
    post_d = post_o - post_c
    post_lines = len(new_content.splitlines())
    print(f"  post: opens={post_o} closes={post_c} delta={post_d} lines={post_lines}")

    if post_d != 0:
        print(f"  ERROR: post-edit paren delta non-zero. Aborting.")
        return False

    print(diff_preview(content, new_content, label))

    if not apply:
        return True

    if not reverse:
        if bak.exists():
            print(f"  WARNING: backup {bak} exists; overwriting.")
        bak.write_text(content)
        print(f"  Backup: {bak}")

    path.write_text(new_content)
    print(f"  Wrote:  {path}")

    disk = path.read_text()
    disk_o, disk_c = code_aware_paren_count(disk)
    if disk_o != post_o or disk_c != post_c:
        print(f"  ERROR: disk verification failed (parens differ).")
        return False
    print(f"  Verified on disk.")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Maximal-surface diagnostic apply script")
    parser.add_argument("--apply", action="store_true",
                        help="Actually write changes. Default is dry-run.")
    parser.add_argument("--reverse", action="store_true",
                        help="Reverse the edits. Combine with --apply to write.")
    args = parser.parse_args()

    direction = "REVERSE (remove diagnostics)" if args.reverse else "APPLY (add diagnostics)"
    print(f">>> {direction} <<<")

    ok1 = process_file(POPULATOR_PATH, POPULATOR_BAK, edit_populator, args.reverse, args.apply, "POPULATOR")
    ok2 = process_file(WRITERS_PATH, WRITERS_BAK, edit_writers, args.reverse, args.apply, "WRITERS")
    ok3 = process_file(LOOP_PATH, LOOP_BAK, edit_loop, args.reverse, args.apply, "LOOP")

    print(f"\n{'='*60}")
    if ok1 and ok2 and ok3:
        if args.apply:
            print("All edits applied successfully.")
        else:
            print("Dry-run complete. All checks pass. Re-run with --apply to write.")
        return 0
    else:
        print("ONE OR MORE EDITS FAILED.")
        if args.apply:
            print("Files may be in inconsistent state. Restore from backups:")
            print(f"  cp {POPULATOR_BAK} {POPULATOR_PATH}")
            print(f"  cp {WRITERS_BAK} {WRITERS_PATH}")
            print(f"  cp {LOOP_BAK} {LOOP_PATH}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
