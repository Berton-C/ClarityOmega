#!/usr/bin/env python3
"""apply_a2_maxwakeloops_alignment.py

Tier A2 of upstream merge: adopt Patrick's maxWakeLoops value (50 -> 1).

Source of merge content: OmegaClaw upstream snapshot 2026-05-18.
Adoption rationale: per fork_additions_runtime_audit_2026-05-18.md Tier A2.
Patrick's value of 1 produces 2-iteration wake bursts (+ 1 1) instead of
51-iteration wake bursts (+ 1 50). This substantially reduces idle-cycle
volume between human messages, which removes the structural condition where
echo-pathology had the most surface area to manifest.

Edit scope:
    Edit 1: src/loop.metta line 12
        - Change (configure maxWakeLoops 50) ;20  to  (configure maxWakeLoops 1)
        - Preserves the (= (maxWakeLoops) (empty)) declaration at line 2 (unchanged)
        - Affects only the configure-time value, not the declaration

    Edit 2: docs/design/artifact_1_loop_metta_wiring_diagram.md
        - Update Phase 4.6 wake check entry to note A2 alignment
        - Document the value change and its operational effect

Pre-apply state checks (per artifact 0 Section 3 hook insertion checklist):
    - src/loop.metta line 12 contains the maxWakeLoops 50 configure call anchor
    - artifact_1 contains the Phase 4.6 wake check entry

Companion to A1 (applied 2026-05-18, commit 0872ec1):
    A1 replaced the lastmessage content surface. A2 reduces the wake-iteration
    count where that surface had been firing. Together they address echo
    pathology at both content (A1) and frequency (A2) levels.
"""

import argparse
import sys
from pathlib import Path

# ==============================================================================
# File paths and backup suffix
# ==============================================================================

LOOP_PATH = Path("src/loop.metta")
LOOP_BAK = Path("src/loop.metta.bak.a2_maxwakeloops_alignment")

ART1_PATH = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md")
ART1_BAK = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md.bak.a2_maxwakeloops_alignment")

BAK_SUFFIX = ".bak.a2_maxwakeloops_alignment"

# ==============================================================================
# Loop.metta anchor and replacement
# ==============================================================================

# Anchor: line 12 in initLoop body
# Note: line includes the inline ";20" comment which is from our fork's
# annotation history. Patrick's upstream has no such comment. The replacement
# preserves no comment, matching Patrick's clean upstream form.

LOOP_MAXWAKE_ANCHOR_APPLY = "          (configure maxWakeLoops 50)\n"
LOOP_MAXWAKE_NEW_APPLY = "          (configure maxWakeLoops 1)\n"

# Reverse: restore the original 50 value.
LOOP_MAXWAKE_ANCHOR_REVERSE = "          (configure maxWakeLoops 1)\n"
LOOP_MAXWAKE_NEW_REVERSE = "          (configure maxWakeLoops 50)\n"


# ==============================================================================
# Artifact_1 update
# ==============================================================================

# Phase 4.6 wake check entry around lines 158-159 of artifact_1 references
# maxWakeLoops in the wake-check description. Update to document A2 alignment.

ART1_WAKECHECK_ANCHOR_APPLY = """**Lines 158-159** - Wake check
- If outside the message-driven window AND past nextWakeAt, extends loops by maxWakeLoops + 1"""

ART1_WAKECHECK_NEW_APPLY = """**Lines 158-159** - Wake check
- If outside the message-driven window AND past nextWakeAt, extends loops by maxWakeLoops + 1
- maxWakeLoops aligned to upstream value of 1 via Tier A2 merge (2026-05-19): wake-refill produces 2-iteration bursts instead of 51-iteration bursts
- Rationale: per `fork_additions_runtime_audit_2026-05-18.md` Tier A2, reducing wake-iteration volume reduces the surface area where echo pathology has historically manifested. Companion to A1 spamShield (content-level fix); A2 is frequency-level fix.
- Operational effect: idle periods between human messages produce shorter bursts of cycles. Clarity has more time between bursts to observe quietly. No change to message-driven behavior."""

ART1_WAKECHECK_ANCHOR_REVERSE = ART1_WAKECHECK_NEW_APPLY
ART1_WAKECHECK_NEW_REVERSE = ART1_WAKECHECK_ANCHOR_APPLY


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
        anchor = LOOP_MAXWAKE_ANCHOR_APPLY
        new = LOOP_MAXWAKE_NEW_APPLY
    else:
        anchor = LOOP_MAXWAKE_ANCHOR_REVERSE
        new = LOOP_MAXWAKE_NEW_REVERSE

    if anchor not in text:
        raise RuntimeError(f"maxWakeLoops anchor not found in {LOOP_PATH}.\nExpected to find:\n{anchor!r}\nLikely cause: disk content does not match expected pre-{direction} state.")

    if text.count(anchor) != 1:
        raise RuntimeError(f"maxWakeLoops anchor appears {text.count(anchor)} times in {LOOP_PATH}, expected exactly 1.")

    text = text.replace(anchor, new, 1)
    new_lines = text.count("\n")
    new_opens, new_closes = count_parens(text)

    line_delta = new_lines - original_lines
    paren_baseline_delta = (orig_opens - orig_closes) - (new_opens - new_closes)

    print(f"  [{LOOP_PATH}]")
    print(f"    Lines: {original_lines} -> {new_lines} (delta {line_delta:+d})")
    print(f"    Parens: opens {orig_opens}->{new_opens}, closes {orig_closes}->{new_closes}, baseline delta {paren_baseline_delta:+d}->0")
    if direction == "apply":
        print(f"    Edit: change maxWakeLoops 50 -> 1 (align to Patrick upstream)")
    else:
        print(f"    Edit: restore maxWakeLoops 1 -> 50 (pre-A2 value)")

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
        anchor = ART1_WAKECHECK_ANCHOR_APPLY
        new = ART1_WAKECHECK_NEW_APPLY
    else:
        anchor = ART1_WAKECHECK_ANCHOR_REVERSE
        new = ART1_WAKECHECK_NEW_REVERSE

    if anchor not in text:
        raise RuntimeError(f"Artifact_1 Phase 4.6 wake check anchor not found in {ART1_PATH}.\nExpected to find:\n{anchor!r}\nLikely cause: disk content does not match expected pre-{direction} state.")

    if text.count(anchor) != 1:
        raise RuntimeError(f"Artifact_1 wake check anchor appears {text.count(anchor)} times, expected exactly 1.")

    text = text.replace(anchor, new, 1)
    new_lines = text.count("\n")
    line_delta = new_lines - original_lines

    print(f"  [{ART1_PATH}]")
    print(f"    Lines: {original_lines} -> {new_lines} (delta {line_delta:+d})")
    if direction == "apply":
        print(f"    Edit: expand Phase 4.6 wake check entry with A2 alignment documentation")
    else:
        print(f"    Edit: restore Phase 4.6 wake check entry to pre-A2 form")

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
    print(f"  A2 MAXWAKELOOPS ALIGNMENT: {direction.upper()} ({'DRY-RUN' if dry_run else 'WRITING'})")
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

    print("=" * 78)
    print(f"  SUMMARY: WHAT --{direction} --apply WILL DO" if not dry_run else f"  SUMMARY: WHAT --{direction} --apply WOULD DO")
    print("=" * 78)
    print()
    print(f"  Direction: {direction.upper()}")
    print(f"  Backup suffix: {BAK_SUFFIX}")
    print()
    if direction == "apply":
        print(f"  src/loop.metta: change line 12 maxWakeLoops 50 -> 1")
        print(f"  docs/design/artifact_1_loop_metta_wiring_diagram.md: expand Phase 4.6 wake check entry")
    else:
        print(f"  src/loop.metta: restore line 12 maxWakeLoops 1 -> 50")
        print(f"  docs/design/artifact_1_loop_metta_wiring_diagram.md: restore Phase 4.6 wake check entry")
    print()
    print(f"  Contract: Artifact 0 Discipline 4 (wiring diagram in same commit)")
    print(f"  Reversibility: python3 staging/apply_a2_maxwakeloops_alignment.py --reverse --apply")
    print()
    print(f"  Post-apply rebuild required (--no-cache for loop.metta change):")
    print(f"    docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw")
    print()
    print(f"  Post-rebuild test order:")
    print(f"    Test 1 (heartbeat): iteration counter advances cleanly, single execution per cycle")
    print(f"    Test 2 (wake burst length): observe cycles between idle periods.")
    print(f"            Expected: ~2-iteration bursts during wake refills instead of ~51-iteration bursts.")
    print(f"            Indicator: idle gaps between bursts feel shorter overall but each burst is shorter too.")
    print(f"    Test 3 (normal msgnew=true cycle): send test MM message, observe response cycle and subsequent idle.")
    print(f"            Should match A1 baseline: clean response, no multi-fire, lastmessage replacement on idle.")
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
        # Not introduced by A2 if delta is 0
        baseline_delta = loop_opens - loop_closes
        print(f"  NOTE: paren delta in loop.metta is {baseline_delta:+d}")
        print(f"        Per A1 finding 2026-05-18, pre-existing +2 imbalance exists from")
        print(f"        OUTPUT_FORMAT string literal content. A2 edit changes only a numeric")
        print(f"        value (50 -> 1) and adds no parens, so this should remain at +2.")
        print(f"        Verify against backup: diff src/loop.metta.bak.a2_maxwakeloops_alignment src/loop.metta")
        print()

    print("=" * 78)
    print(f"  A2 MAXWAKELOOPS ALIGNMENT {direction.upper()} COMPLETE")
    print("=" * 78)
    print()


if __name__ == "__main__":
    main()
