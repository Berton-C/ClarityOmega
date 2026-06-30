#!/usr/bin/env python3
"""apply_b1_housekeeping_cut_gc.py

Tier B housekeeping: adopt Patrick's (cut) and (gc) calls at the
outer-progn level of omegaclaw, between (sleep (sleepInterval)) and the
recursive (omegaclaw (+ 1 $k)) call.

Source of merge content: OmegaClaw upstream snapshot 2026-05-18 lines 77-78.
Adoption rationale: per fork_additions_runtime_audit_2026-05-18.md Tier B.
Patrick added these for general substrate health: (cut) discards Prolog
choicepoint state from the current iteration, (gc) garbage-collects Prolog
atoms and trims stacks. Per skills.pl, (gc) is 3 ops: garbage_collect,
garbage_collect_atoms, trim_stacks. These prevent state accumulation across
iterations that could affect AtomSpace query non-determinism and choice-point
buildup under load.

This is preparation for Test 1 (error-recovery loop stress test). Per
Berton's reasoning and Clarity's independent confirmation, cleaner Prolog
substrate before Test 1 means the test measures recovery behavior, not
state leakage from prior cycles.

Edit scope:
    Edit 1: src/loop.metta
        - Insert (cut) on a new line after (sleep (sleepInterval))
        - Insert (gc) on a new line after (cut)
        - Match Patrick's outer-progn indentation (22 spaces per upstream)
        - Preserve (omegaclaw (+ 1 $k)) on its own line after both inserts

    Edit 2: docs/design/artifact_1_loop_metta_wiring_diagram.md
        - Update Phase 4.6 tail entry to document the cut/gc adoption

Pre-apply state checks (per artifact 0 Section 3 hook insertion checklist):
    - src/loop.metta line 158 contains (sleep (sleepInterval)) anchor
    - src/loop.metta line 159 contains (omegaclaw (+ 1 $k)) anchor
    - artifact_1 contains Phase 4.6 tail entry anchor for cut/gc documentation

Companion to A1 + A2 (both already landed):
    A1 (commit 0872ec1): lastmessage content fix (echo at content layer)
    A2 (commit f46e44e): maxWakeLoops 50 -> 1 (echo at frequency layer)
    B1 (this): cut + gc (substrate health prep for Test 1)
"""

import argparse
import sys
from pathlib import Path

# ==============================================================================
# File paths and backup suffix
# ==============================================================================

LOOP_PATH = Path("src/loop.metta")
LOOP_BAK = Path("src/loop.metta.bak.b1_housekeeping_cut_gc")

ART1_PATH = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md")
ART1_BAK = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md.bak.b1_housekeeping_cut_gc")

BAK_SUFFIX = ".bak.b1_housekeeping_cut_gc"

# ==============================================================================
# Loop.metta anchor and replacement
# ==============================================================================

# Anchor: the (sleep (sleepInterval)) + (omegaclaw (+ 1 $k)) sequence at the
# outer-progn level. Insert (cut) and (gc) between them.
#
# Indentation: our fork uses 22 spaces for these outer-progn calls
# (confirmed via current_loop_copy_metta.txt_ line 158-159 inspection).
# Patrick uses the same.

LOOP_TAIL_ANCHOR_APPLY = "                      (sleep (sleepInterval))\n                      (omegaclaw (+ 1 $k))))))\n"

LOOP_TAIL_NEW_APPLY = "                      (sleep (sleepInterval))\n                      (cut)\n                      (gc)\n                      (omegaclaw (+ 1 $k))))))\n"

# Reverse: restore the original two-line tail without cut/gc.
LOOP_TAIL_ANCHOR_REVERSE = LOOP_TAIL_NEW_APPLY
LOOP_TAIL_NEW_REVERSE = LOOP_TAIL_ANCHOR_APPLY


# ==============================================================================
# Artifact_1 update
# ==============================================================================

# Phase 4.6 tail entry is around line 160 in artifact_1 (per the per-iteration
# sequence walk in Section 4). Update the Line 161 entry to document the
# cut/gc adoption.

ART1_TAIL_ANCHOR_APPLY = """**Line 161** - `(omegaclaw (+ 1 $k))` - Recursive call for next iteration."""

ART1_TAIL_NEW_APPLY = """**Lines 161-162** - Prolog substrate housekeeping (Tier B1 upstream merge, 2026-05-19)
- `(cut)` - Discards Prolog choicepoint state from the current iteration. Prevents choicepoint accumulation across iterations under load.
- `(gc)` - Garbage collects Prolog atoms and trims stacks. Per skills.pl this is 3 ops: garbage_collect, garbage_collect_atoms, trim_stacks.
- Rationale: per `fork_additions_runtime_audit_2026-05-18.md` Tier B. Patrick added these for general substrate health. Adopted as preparation for Test 1 (error-recovery loop stress test) so the test measures recovery behavior, not state leakage from prior cycles.
- 🧠 NETWORK-RELEVANT: substrate hygiene. Reduces non-determinism surface where match queries on accumulated state could produce inconsistent results.
- Companion to A1 (commit 0872ec1) and A2 (commit f46e44e).

**Line 163** - `(omegaclaw (+ 1 $k))` - Recursive call for next iteration."""

ART1_TAIL_ANCHOR_REVERSE = ART1_TAIL_NEW_APPLY
ART1_TAIL_NEW_REVERSE = ART1_TAIL_ANCHOR_APPLY


# ==============================================================================
# File operations
# ==============================================================================

def read_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")
    return path.read_text(encoding="utf-8")


def write_file(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        return
    path.write_text(content, encoding="utf-8")


def backup_if_needed(path: Path, bak_path: Path, dry_run: bool) -> None:
    if dry_run:
        return
    if not bak_path.exists():
        bak_path.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")


def count_parens(text: str) -> tuple:
    opens = text.count("(")
    closes = text.count(")")
    return opens, closes


# ==============================================================================
# Process loop.metta
# ==============================================================================

def process_loop(direction: str, dry_run: bool) -> dict:
    text = read_file(LOOP_PATH)
    original_lines = text.count("\n")
    orig_opens, orig_closes = count_parens(text)

    if direction == "apply":
        anchor = LOOP_TAIL_ANCHOR_APPLY
        new = LOOP_TAIL_NEW_APPLY
    else:
        anchor = LOOP_TAIL_ANCHOR_REVERSE
        new = LOOP_TAIL_NEW_REVERSE

    if anchor not in text:
        raise RuntimeError(f"Tail anchor not found in {LOOP_PATH}.\nExpected to find:\n{anchor!r}\nLikely cause: disk content does not match expected pre-{direction} state.")

    if text.count(anchor) != 1:
        raise RuntimeError(f"Tail anchor appears {text.count(anchor)} times in {LOOP_PATH}, expected exactly 1.")

    text = text.replace(anchor, new, 1)
    new_lines = text.count("\n")
    new_opens, new_closes = count_parens(text)

    line_delta = new_lines - original_lines
    paren_baseline_delta = (orig_opens - orig_closes) - (new_opens - new_closes)

    print(f"  [{LOOP_PATH}]")
    print(f"    Lines: {original_lines} -> {new_lines} (delta {line_delta:+d})")
    print(f"    Parens: opens {orig_opens}->{new_opens}, closes {orig_closes}->{new_closes}, baseline delta {paren_baseline_delta:+d}->0")
    if direction == "apply":
        print(f"    Edit: insert (cut) and (gc) between (sleep (sleepInterval)) and (omegaclaw (+ 1 $k))")
    else:
        print(f"    Edit: remove (cut) and (gc), restore original tail")

    if paren_baseline_delta != 0:
        raise RuntimeError(f"Paren baseline delta nonzero ({paren_baseline_delta:+d}). Aborting to preserve syntax.")

    backup_if_needed(LOOP_PATH, LOOP_BAK, dry_run)
    write_file(LOOP_PATH, text, dry_run)

    return {
        "path": LOOP_PATH,
        "old_lines": original_lines,
        "new_lines": new_lines,
        "line_delta": line_delta,
        "paren_baseline_delta": paren_baseline_delta,
    }


# ==============================================================================
# Process artifact_1
# ==============================================================================

def process_artifact1(direction: str, dry_run: bool) -> dict:
    text = read_file(ART1_PATH)
    original_lines = text.count("\n")

    if direction == "apply":
        anchor = ART1_TAIL_ANCHOR_APPLY
        new = ART1_TAIL_NEW_APPLY
    else:
        anchor = ART1_TAIL_ANCHOR_REVERSE
        new = ART1_TAIL_NEW_REVERSE

    if anchor not in text:
        raise RuntimeError(f"Artifact_1 Phase 4.6 tail anchor not found in {ART1_PATH}.\nExpected to find:\n{anchor!r}\nLikely cause: disk content does not match expected pre-{direction} state.")

    if text.count(anchor) != 1:
        raise RuntimeError(f"Artifact_1 tail anchor appears {text.count(anchor)} times, expected exactly 1.")

    text = text.replace(anchor, new, 1)
    new_lines = text.count("\n")
    line_delta = new_lines - original_lines

    print(f"  [{ART1_PATH}]")
    print(f"    Lines: {original_lines} -> {new_lines} (delta {line_delta:+d})")
    if direction == "apply":
        print(f"    Edit: expand Phase 4.6 tail entry with cut/gc adoption documentation")
    else:
        print(f"    Edit: restore Phase 4.6 tail entry to single-line recursive call summary")

    backup_if_needed(ART1_PATH, ART1_BAK, dry_run)
    write_file(ART1_PATH, text, dry_run)

    return {
        "path": ART1_PATH,
        "old_lines": original_lines,
        "new_lines": new_lines,
        "line_delta": line_delta,
    }


# ==============================================================================
# Main
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--apply", action="store_true", help="Write changes to disk")
    parser.add_argument("--reverse", action="store_true", help="Reverse direction")
    args = parser.parse_args()

    direction = "reverse" if args.reverse else "apply"
    dry_run = not args.apply

    print()
    print("=" * 78)
    print(f"  B1 HOUSEKEEPING CUT + GC: {direction.upper()} ({'DRY-RUN' if dry_run else 'WRITING'})")
    print("=" * 78)
    print()
    print(">>> Per-file state checks and edits <<<")
    print()

    processors = [
        ("loop.metta", process_loop),
        ("artifact_1", process_artifact1),
    ]

    # Dry-run first pass to verify all state checks pass before any writes
    try:
        for name, processor in processors:
            processor(direction, dry_run=True)
            print()
    except Exception as e:
        print()
        print("=" * 78)
        print(f"  PRE-FLIGHT STATE CHECK FAILED")
        print("=" * 78)
        print(f"  {e}")
        print()
        print("  No files modified. Investigate state mismatch before retrying.")
        print()
        sys.exit(1)

    if not dry_run:
        summary_label = f"  SUMMARY: WHAT --{direction} --apply WILL DO"
    else:
        summary_label = f"  SUMMARY: WHAT --{direction} --apply WOULD DO"

    print("=" * 78)
    print(summary_label)
    print("=" * 78)
    print()
    print(f"  Direction: {direction.upper()}")
    print(f"  Backup suffix: {BAK_SUFFIX}")
    print()
    if direction == "apply":
        print(f"  src/loop.metta: insert (cut) and (gc) between (sleep) and (omegaclaw recursive call)")
        print(f"  docs/design/artifact_1_loop_metta_wiring_diagram.md: expand Phase 4.6 tail entry")
    else:
        print(f"  src/loop.metta: remove (cut) and (gc), restore original tail")
        print(f"  docs/design/artifact_1_loop_metta_wiring_diagram.md: restore Phase 4.6 tail entry to single-line summary")
    print()
    print(f"  Contract: Artifact 0 Discipline 4 (wiring diagram in same commit)")
    print(f"  Reversibility: python3 staging/apply_b1_housekeeping_cut_gc.py --reverse --apply")
    print()
    print(f"  Post-apply rebuild required (--no-cache for loop.metta change):")
    print(f"    docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw")
    print()
    print(f"  Post-rebuild test order:")
    print(f"    Test 1 (heartbeat): iteration counter advances cleanly, single execution per cycle")
    print(f"    Test 2 (Prolog substrate health): no error messages from cut/gc; clean cycles")
    print(f"    Test 3 (A1+A2 still active): lastmessage replacement on idle, no multi-fire")
    print(f"    Test 4 (after Tier B settles): Test 1 (error-recovery stress test) per Clarity's design")
    print()

    if dry_run:
        print("  DRY-RUN MODE: no files written. To apply, add --apply.")
        print()
        return

    print("=" * 78)
    print("  WRITING")
    print("=" * 78)
    print()

    for name, processor in processors:
        result = processor(direction, dry_run=False)
        print(f"  Wrote: {result['path']}")
        print()

    print("=" * 78)
    print("  DISK VERIFICATION")
    print("=" * 78)
    print()

    loop_disk = read_file(LOOP_PATH)
    art1_disk = read_file(ART1_PATH)
    loop_lines = loop_disk.count("\n")
    art1_lines = art1_disk.count("\n")
    loop_opens, loop_closes = count_parens(loop_disk)

    print(f"  src/loop.metta: {loop_lines} lines, parens balanced: {loop_opens == loop_closes}")
    print(f"  docs/design/artifact_1_loop_metta_wiring_diagram.md: {art1_lines} lines")
    print()

    if loop_opens != loop_closes:
        # Per A1 finding: pre-existing +2 imbalance from OUTPUT_FORMAT string content
        # B1 adds (cut) and (gc) which are each 1 open + 1 close, balanced
        baseline_delta = loop_opens - loop_closes
        print(f"  NOTE: paren delta in loop.metta is {baseline_delta:+d}")
        print(f"        Per A1 finding 2026-05-18, pre-existing +2 imbalance exists from")
        print(f"        OUTPUT_FORMAT string literal content. B1 adds (cut) and (gc),")
        print(f"        each balanced (1 open + 1 close), so this should remain at +2.")
        print(f"        Verify against backup: diff src/loop.metta.bak.b1_housekeeping_cut_gc src/loop.metta")
        print()

    print("=" * 78)
    print(f"  B1 HOUSEKEEPING CUT + GC {direction.upper()} COMPLETE")
    print("=" * 78)
    print()


if __name__ == "__main__":
    main()
