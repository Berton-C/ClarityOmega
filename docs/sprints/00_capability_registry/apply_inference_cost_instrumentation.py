#!/usr/bin/env python3
"""
apply_inference_cost_instrumentation.py

Adds metta-measured function alongside existing metta in src/skills.metta,
bootstraps the &metta-call-counter state variable in src/loop.metta initLoop,
and documents the new state variable in artifact_1_loop_metta_wiring_diagram.md.

Two purposes:

(1) Empirical evaluation of T-1 from the memory-layer merge design
    (upstream's call_with_inference_limit 100000000 budget). The test
    establishes Clarity's actual reasoning depth distribution so the
    budget decision is empirical, not theoretical.

(2) New cognitive surface for Clarity. Inference-cost-per-cognitive-act
    becomes substrate-observable, allowing future query and self-reasoning
    about resource constraints. Aligns with the architectural endpoint
    where reasoning is substrate-visible at every layer.

Coexistence pattern: original metta stays untouched; metta-measured is
a strict wrapper of the same eval logic. Same-input-same-result
verification required before considering replacement.

Session-only atom shape (no &persistent), pruned at container restart.

Three coordinated edits (atomic via apply-or-nothing pattern):

    Edit 1: src/skills.metta
        Insert metta-measured function definition immediately after
        the existing metta function definition.

    Edit 2: src/loop.metta
        Insert (change-state! &metta-call-counter 0) inside initLoop,
        after (change-state! &loops (maxNewInputLoops)) and before the
        task-state bootstrap comment line.

    Edit 3: docs/design/artifact_1_loop_metta_wiring_diagram.md
        Insert state variable table row for &metta-call-counter
        immediately after the &loops row.

Convention notes:
    - State variables in this codebase are bootstrapped via
      change-state! inside initLoop. The !(bind! ... (new-state 0))
      pattern is NOT used in this codebase. Consistency-over-cleverness
      per Clarity's review.
    - Multi-file coordinated edits via single apply script is the
      established pattern (precedent: apply_idle_directive_once_per_window_path1_gamma.py
      with five coordinated edits; apply_task_state_step2_wiring.py with
      multiple edits).
    - Wiring diagram update is Discipline 4 (wiring diagram stays
      current) per established work-stream pattern.

Usage
-----
Dry-run (default):
    python3 staging/apply_inference_cost_instrumentation.py

Apply:
    python3 staging/apply_inference_cost_instrumentation.py --apply

Reverse (after apply, returns to pre-instrumentation state):
    python3 staging/apply_inference_cost_instrumentation.py --reverse --apply

Pre-conditions
--------------
Expects:
    - src/skills.metta with the original metta function definition
      at the known 3-line form.
    - src/loop.metta with the &loops bootstrap line and task-state
      bootstrap comment in initLoop.
    - artifact_1_loop_metta_wiring_diagram.md with the &loops state
      variable row.

If any anchor is missing or matches more than once, the script halts
without writing.

Backup files (forward apply only):
    src/skills.metta.bak.inference_cost_instrumentation
    src/loop.metta.bak.inference_cost_instrumentation
    docs/design/artifact_1_loop_metta_wiring_diagram.md.bak.inference_cost_instrumentation
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


# ============================================================================
# PATHS
# ============================================================================

SKILLS_METTA_PATH = Path("src/skills.metta")
SKILLS_METTA_BAK = Path("src/skills.metta.bak.inference_cost_instrumentation")

LOOP_METTA_PATH = Path("src/loop.metta")
LOOP_METTA_BAK = Path("src/loop.metta.bak.inference_cost_instrumentation")

WIRING_DIAGRAM_PATH = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md")
WIRING_DIAGRAM_BAK = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md.bak.inference_cost_instrumentation")


# ============================================================================
# EDIT 1: src/skills.metta -- add metta-measured definition
# ============================================================================
#
# Anchor: existing metta function definition (3-line form).
# Insert metta-measured definition immediately after it.

SKILLS_OLD = """(= (metta $str)
   (let $code (sread $str)
        (eval $code)))"""

# metta-measured wraps the same eval logic with inference bookending via
# statistics(inferences, X) through translatePredicate.
#
# Atom shape recorded:
#   (metta-call-stats call-id: $id cycle: $k delta: $delta
#                     call-type: $head sexpr: $str)
#
# Call-id from &metta-call-counter (incremented per measured call).
# Cycle passed by caller. Call-type extracted via car-atom on the parsed
# code. Sexpr stored as the original string for outlier identification.
#
# Session-only (no &persistent), pruned at container restart.

SKILLS_NEW_INSERT = """

(= (metta-measured $str $k)
   (let* (($code (sread $str))
          ($head (car-atom $code))
          ($_inc (change-state! &metta-call-counter
                                (+ 1 (get-state &metta-call-counter))))
          ($id (get-state &metta-call-counter))
          ($x1 (progn (translatePredicate (statistics inferences $X1)) $X1))
          ($result (eval $code))
          ($x2 (progn (translatePredicate (statistics inferences $X2)) $X2))
          ($delta (- $x2 $x1))
          ($_atom (add-atom &self
                            (metta-call-stats call-id: $id
                                              cycle: $k
                                              delta: $delta
                                              call-type: $head
                                              sexpr: $str))))
        $result))"""

SKILLS_NEW = SKILLS_OLD + SKILLS_NEW_INSERT


# ============================================================================
# EDIT 2: src/loop.metta -- bootstrap &metta-call-counter in initLoop
# ============================================================================
#
# Anchor: the existing &loops bootstrap line and the task-state comment
# that follows. Insert &metta-call-counter bootstrap between them.

LOOP_OLD = """          (change-state! &loops (maxNewInputLoops))
          ;; Task-state primitive: conditional bootstrap of scalar atoms"""

LOOP_NEW = """          (change-state! &loops (maxNewInputLoops))
          ;; Substrate instrumentation: per-call inference-cost counter
          (change-state! &metta-call-counter 0)
          ;; Task-state primitive: conditional bootstrap of scalar atoms"""


# ============================================================================
# EDIT 3: docs/design/artifact_1_loop_metta_wiring_diagram.md
# -- state variable table row
# ============================================================================
#
# Anchor: the existing &loops row in the state variable table.
# Insert &metta-call-counter row immediately after it.

WIRING_OLD = "| `&loops` | `(maxNewInputLoops)` | Iteration counter for run cycle. **Currently hardcoded; target architecture per spec_v3.0 Section 0 reads `(switch-iteration-budget ...)` from SWITCH-HUB substrate.** | Line 54, line 62 | Line 54, line 62, line 154 |"

WIRING_NEW = WIRING_OLD + "\n| `&metta-call-counter` | `0` | Monotonic counter for measured metta calls. Used by `metta-measured` (src/skills.metta) to generate unique call-id values on each invocation. Session-only; no persistence; pruned at container restart. | `metta-measured` body | `metta-measured` body (per call) |"


# ============================================================================
# FILE I/O HELPERS
# ============================================================================


def read_file(path: Path) -> str:
    with path.open("r", encoding="utf-8") as f:
        return f.read()


def write_file(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        return
    with path.open("w", encoding="utf-8") as f:
        f.write(content)


def backup_if_needed(src_path: Path, bak_path: Path, dry_run: bool) -> None:
    if dry_run:
        return
    if bak_path.exists():
        return
    bak_path.write_text(src_path.read_text(encoding="utf-8"), encoding="utf-8")


def count_substr(text: str, needle: str) -> int:
    return text.count(needle)


# ============================================================================
# DIFF PREVIEW
# ============================================================================


def diff_preview(old_content: str, new_content: str, context: int = 3) -> str:
    old_lines = old_content.splitlines()
    new_lines = new_content.splitlines()

    differ_start = None
    min_len = min(len(old_lines), len(new_lines))
    for i in range(min_len):
        if old_lines[i] != new_lines[i]:
            differ_start = i
            break
    if differ_start is None:
        if len(old_lines) == len(new_lines):
            return "(no change)"
        differ_start = min_len

    old_back = len(old_lines) - 1
    new_back = len(new_lines) - 1
    while (old_back > differ_start and new_back > differ_start
           and old_lines[old_back] == new_lines[new_back]):
        old_back -= 1
        new_back -= 1
    differ_end_old = old_back
    differ_end_new = new_back

    out = ["--- diff preview ---"]
    start = max(0, differ_start - context)
    for i in range(start, differ_start):
        out.append(f"  {old_lines[i]}")
    for i in range(differ_start, differ_end_old + 1):
        out.append(f"- {old_lines[i]}")
    for i in range(differ_start, differ_end_new + 1):
        out.append(f"+ {new_lines[i]}")
    end_old = min(len(old_lines), differ_end_old + 1 + context)
    for i in range(differ_end_old + 1, end_old):
        out.append(f"  {old_lines[i]}")
    return "\n".join(out)


# ============================================================================
# PER-FILE PROCESSORS
# ============================================================================


def process_skills_metta(direction: str, dry_run: bool) -> dict:
    """Edit 1: insert metta-measured function in src/skills.metta."""

    text = read_file(SKILLS_METTA_PATH)
    pre_lines = text.count("\n")

    if direction == "apply":
        anchor = SKILLS_OLD
        new_block = SKILLS_NEW
        anchor_present = anchor in text
        sentinel_absent = "metta-measured" not in text
        state_ok = anchor_present and sentinel_absent
        state_check_label = "metta definition present, metta-measured absent"
    else:
        anchor = SKILLS_NEW
        new_block = SKILLS_OLD
        anchor_present = anchor in text
        state_ok = anchor_present
        state_check_label = "metta-measured present"

    if not state_ok:
        return {
            "path": str(SKILLS_METTA_PATH),
            "ok": False,
            "message": f"State check failed: {state_check_label}",
            "pre_lines": pre_lines,
        }

    count = count_substr(text, anchor)
    if count != 1:
        return {
            "path": str(SKILLS_METTA_PATH),
            "ok": False,
            "message": f"Anchor match count = {count}, expected 1",
            "pre_lines": pre_lines,
        }

    new_text = text.replace(anchor, new_block, 1)

    if direction == "apply":
        backup_if_needed(SKILLS_METTA_PATH, SKILLS_METTA_BAK, dry_run)

    write_file(SKILLS_METTA_PATH, new_text, dry_run)

    post_lines = new_text.count("\n")

    return {
        "path": str(SKILLS_METTA_PATH),
        "ok": True,
        "pre_lines": pre_lines,
        "post_lines": post_lines,
        "line_delta": post_lines - pre_lines,
        "edit": ("insert metta-measured function"
                 if direction == "apply"
                 else "remove metta-measured function"),
        "diff": diff_preview(text, new_text),
    }


def process_loop_metta(direction: str, dry_run: bool) -> dict:
    """Edit 2: bootstrap &metta-call-counter in initLoop."""

    text = read_file(LOOP_METTA_PATH)
    pre_lines = text.count("\n")

    if direction == "apply":
        anchor = LOOP_OLD
        new_block = LOOP_NEW
        anchor_present = anchor in text
        sentinel_absent = "&metta-call-counter" not in text
        state_ok = anchor_present and sentinel_absent
        state_check_label = "&loops bootstrap present, &metta-call-counter absent"
    else:
        anchor = LOOP_NEW
        new_block = LOOP_OLD
        anchor_present = anchor in text
        state_ok = anchor_present
        state_check_label = "&metta-call-counter bootstrap present"

    if not state_ok:
        return {
            "path": str(LOOP_METTA_PATH),
            "ok": False,
            "message": f"State check failed: {state_check_label}",
            "pre_lines": pre_lines,
        }

    count = count_substr(text, anchor)
    if count != 1:
        return {
            "path": str(LOOP_METTA_PATH),
            "ok": False,
            "message": f"Anchor match count = {count}, expected 1",
            "pre_lines": pre_lines,
        }

    new_text = text.replace(anchor, new_block, 1)

    if direction == "apply":
        backup_if_needed(LOOP_METTA_PATH, LOOP_METTA_BAK, dry_run)

    write_file(LOOP_METTA_PATH, new_text, dry_run)

    post_lines = new_text.count("\n")

    return {
        "path": str(LOOP_METTA_PATH),
        "ok": True,
        "pre_lines": pre_lines,
        "post_lines": post_lines,
        "line_delta": post_lines - pre_lines,
        "edit": ("bootstrap &metta-call-counter in initLoop"
                 if direction == "apply"
                 else "remove &metta-call-counter bootstrap from initLoop"),
        "diff": diff_preview(text, new_text),
    }


def process_wiring_diagram(direction: str, dry_run: bool) -> dict:
    """Edit 3: add &metta-call-counter row to state variable table."""

    text = read_file(WIRING_DIAGRAM_PATH)
    pre_lines = text.count("\n")

    if direction == "apply":
        anchor = WIRING_OLD
        new_block = WIRING_NEW
        anchor_present = anchor in text
        sentinel_absent = "&metta-call-counter" not in text
        state_ok = anchor_present and sentinel_absent
        state_check_label = "&loops row present, &metta-call-counter row absent"
    else:
        anchor = WIRING_NEW
        new_block = WIRING_OLD
        anchor_present = anchor in text
        state_ok = anchor_present
        state_check_label = "&metta-call-counter row present"

    if not state_ok:
        return {
            "path": str(WIRING_DIAGRAM_PATH),
            "ok": False,
            "message": f"State check failed: {state_check_label}",
            "pre_lines": pre_lines,
        }

    count = count_substr(text, anchor)
    if count != 1:
        return {
            "path": str(WIRING_DIAGRAM_PATH),
            "ok": False,
            "message": f"Anchor match count = {count}, expected 1",
            "pre_lines": pre_lines,
        }

    new_text = text.replace(anchor, new_block, 1)

    if direction == "apply":
        backup_if_needed(WIRING_DIAGRAM_PATH, WIRING_DIAGRAM_BAK, dry_run)

    write_file(WIRING_DIAGRAM_PATH, new_text, dry_run)

    post_lines = new_text.count("\n")

    return {
        "path": str(WIRING_DIAGRAM_PATH),
        "ok": True,
        "pre_lines": pre_lines,
        "post_lines": post_lines,
        "line_delta": post_lines - pre_lines,
        "edit": ("insert &metta-call-counter wiring diagram row"
                 if direction == "apply"
                 else "remove &metta-call-counter wiring diagram row"),
        "diff": diff_preview(text, new_text),
    }


# ============================================================================
# MAIN
# ============================================================================


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inference-cost instrumentation apply script (three coordinated edits)"
    )
    parser.add_argument("--apply", action="store_true",
                        help="Write changes to disk")
    parser.add_argument("--reverse", action="store_true",
                        help="Reverse direction (remove instrumentation)")
    args = parser.parse_args()

    direction = "reverse" if args.reverse else "apply"
    dry_run = not args.apply

    print()
    print("=" * 78)
    label = "INFERENCE-COST INSTRUMENTATION (three coordinated edits)"
    mode = "DRY-RUN" if dry_run else "WRITING"
    print(f"  {label}: {direction.upper()} ({mode})")
    print("=" * 78)
    print()

    for p in [SKILLS_METTA_PATH, LOOP_METTA_PATH, WIRING_DIAGRAM_PATH]:
        if not p.exists():
            print(f"  ERROR: {p} does not exist. Are you at repo root?")
            return 1

    print(">>> Per-file state checks <<<")
    print()

    processors = [
        (process_skills_metta, str(SKILLS_METTA_PATH)),
        (process_loop_metta, str(LOOP_METTA_PATH)),
        (process_wiring_diagram, str(WIRING_DIAGRAM_PATH)),
    ]

    dry_results = []
    for processor, label in processors:
        print(f"  [{label}]")
        result = processor(direction, dry_run=True)
        if not result.get("ok"):
            print(f"    FAIL: {result.get('message')}")
            print()
            print("  Halting: state check failed. No changes written.")
            return 1
        print(f"    OK: pre_lines={result['pre_lines']}, "
              f"post_lines={result['post_lines']}, "
              f"line_delta={result['line_delta']:+d}")
        print(f"    Edit: {result['edit']}")
        print()
        print(result["diff"])
        print()
        dry_results.append(result)

    if dry_run:
        print(">>> DRY-RUN complete. No files modified. <<<")
        print()
        print("  To apply:")
        print(f"    python3 staging/apply_inference_cost_instrumentation.py --apply")
        print()
        if direction == "apply":
            print("  Post-apply verification (run in container, after rebuild):")
            print()
            print("    1. Strict-wrapper identity test:")
            print('       In MeTTa REPL, compare:')
            print('         (metta "(+ 1 1)")')
            print('         (metta-measured "(+ 1 1)" 0)')
            print('       Both should return 2.')
            print()
            print("    2. Counter monotonicity:")
            print("       Successive metta-measured calls should produce")
            print("       monotonically increasing call-id values.")
            print()
            print("    3. Atom shape inspection:")
            print('       !(match &self (metta-call-stats $field) $field)')
            print('       Atoms should have shape:')
            print('         (metta-call-stats call-id: ...')
            print('                           cycle: ...')
            print('                           delta: ...')
            print('                           call-type: ...')
            print('                           sexpr: ...)')
            print()
            print("    4. State variable bootstrap:")
            print("       Confirm &metta-call-counter is bound at startup")
            print("       (i.e., first call returns call-id 1, not error).")
            print()
            print("  Container rebuild required for changes to take effect:")
            print()
            print("    docker compose build --no-cache clarityclaw && \\")
            print("    docker compose up -d clarityclaw")
        return 0

    # Apply mode -- write all three for real.
    # Atomicity note: dry-run pass above verified all three would succeed.
    # If any fails on actual write, we leave already-written files in place
    # with backups available for manual reverse.
    print(">>> Writing changes <<<")
    print()

    for processor, label in processors:
        print(f"  [{label}]")
        result = processor(direction, dry_run=False)
        if not result.get("ok"):
            print(f"    FAIL on apply: {result.get('message')}")
            print()
            print("  WARNING: Earlier writes in this run already completed.")
            print("  Use --reverse --apply to undo what was written.")
            return 1
        print(f"    WROTE: {label}")
        if direction == "apply":
            bak_map = {
                str(SKILLS_METTA_PATH): SKILLS_METTA_BAK,
                str(LOOP_METTA_PATH): LOOP_METTA_BAK,
                str(WIRING_DIAGRAM_PATH): WIRING_DIAGRAM_BAK,
            }
            print(f"    BACKUP: {bak_map[label]}")

    print()
    print(">>> All three edits written. <<<")
    print()
    print("  Next steps:")
    print()
    print("  1. Container rebuild:")
    print("       docker compose build --no-cache clarityclaw && \\")
    print("       docker compose up -d clarityclaw")
    print()
    if direction == "apply":
        print("  2. Run strict-wrapper verification in MeTTa REPL (see above).")
        print()
        print("  3. If verification passes, operate for measurement window.")
        print("     Suggested minimum: 100 iterations covering a mix of")
        print("     human-exchange, autonomous-reasoning, and idle-cycle")
        print("     activity.")
        print()
        print("  4. Query and analyze metta-call-stats atoms:")
        print('       !(match &self (metta-call-stats $field) $field)')
        print()
        print("  5. Use distribution analysis to inform T-1 budget decision")
        print("     in memory_layer_merge_design_v2.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
