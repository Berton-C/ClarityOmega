#!/usr/bin/env python3
"""apply_a1_spamshield_mechanism.py

Tier A1 of upstream merge: adopt Patrick's spamShield mechanism cohesively
(config declaration + initLoop setting + lastmessage conditional).

Source of merge content: OmegaClaw upstream snapshot 2026-05-18 lines 9, 14, 56.
Adoption rationale: per fork_additions_runtime_audit_2026-05-18.md Tier A1,
this is the architectural answer Patrick built for echo-when-msgnew-is-false.
Our fork currently emits HUMAN-LAST-MSG with persistent stale msg + MESSAGE-IS-NEW
flag every cycle, which the LLM does not honor under prompt-surface pressure.
Patrick's mechanism replaces stale-message content with anti-spam directive
or empty string when msgnew is false.

Cohesive scope (per audit, should not be split):
    Edit 1: src/loop.metta
        - Insert (= (spamShield) (empty)) after existing wakeupInterval declaration
        - Insert (configure spamShield True) after sleepInterval configure
        - Replace lastmessage construction at lines 69-70 with Patrick's conditional

    Edit 2: docs/design/artifact_1_loop_metta_wiring_diagram.md
        - Update Phase 4.0 entry to document the new lastmessage shape and
          spamShield config dependency

Pre-apply state checks (per artifact 0 Section 3 hook insertion checklist):
    - src/loop.metta line 8 contains the wakeupInterval declaration anchor
    - src/loop.metta line 13 contains the sleepInterval configure anchor
    - src/loop.metta lines 69-70 contain the existing two-line lastmessage
    - artifact_1 contains the existing Phase 4.0 lastmessage entry

Compatibility verified:
    helper.soul_send_assemble appends $lastmessage as " " + str(lastmessage)
    with no prefix parsing. Safe with all three Patrick lastmessage outputs:
    (HUMAN-MSG: $msg), " DO NOT RE-SEND OR SPAM!", or "".

src/helper.py: UNCHANGED. soul_send_assemble already accepts $lastmessage
    as opaque string and concatenates it. No Python changes required.
"""

import argparse
import sys
from pathlib import Path

# ==============================================================================
# File paths and backup suffix
# ==============================================================================

LOOP_PATH = Path("src/loop.metta")
LOOP_BAK = Path("src/loop.metta.bak.a1_spamshield_mechanism")

ART1_PATH = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md")
ART1_BAK = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md.bak.a1_spamshield_mechanism")

BAK_SUFFIX = ".bak.a1_spamshield_mechanism"

# ==============================================================================
# Loop.metta anchors and replacements
# ==============================================================================

# Anchor 1: top-level config declaration block
# Insert (= (spamShield) (empty)) after the wakeupInterval declaration.

LOOP_CONFIG_DECL_ANCHOR_APPLY = "(= (wakeupInterval) (empty))\n"
LOOP_CONFIG_DECL_NEW_APPLY = "(= (wakeupInterval) (empty))\n(= (spamShield) (empty))\n"

# Reverse: remove the spamShield declaration line.
LOOP_CONFIG_DECL_ANCHOR_REVERSE = "(= (wakeupInterval) (empty))\n(= (spamShield) (empty))\n"
LOOP_CONFIG_DECL_NEW_REVERSE = "(= (wakeupInterval) (empty))\n"


# Anchor 2: initLoop configure calls
# Insert (configure spamShield True) after sleepInterval configure.
# Match the surrounding indentation (10 spaces per existing lines).

LOOP_INITLOOP_ANCHOR_APPLY = "          (configure sleepInterval 1) ;10\n"
LOOP_INITLOOP_NEW_APPLY = "          (configure sleepInterval 1) ;10\n          (configure spamShield True)\n"

# Reverse: remove the configure spamShield line.
LOOP_INITLOOP_ANCHOR_REVERSE = "          (configure sleepInterval 1) ;10\n          (configure spamShield True)\n"
LOOP_INITLOOP_NEW_REVERSE = "          (configure sleepInterval 1) ;10\n"


# Anchor 3: $lastmessage construction
# Replace existing two-line HUMAN-LAST-MSG with Patrick's single-line conditional.

LOOP_LASTMSG_ANCHOR_APPLY = """                                (let* (($lastmessage (HUMAN-LAST-MSG: $msg
                                                      MESSAGE-IS-NEW: $msgnew))"""

LOOP_LASTMSG_NEW_APPLY = """                                (let* (($lastmessage (if $msgnew (HUMAN-MSG: $msg) (if (spamShield) " DO NOT RE-SEND OR SPAM!" "")))"""

# Reverse: restore the two-line HUMAN-LAST-MSG construction.
LOOP_LASTMSG_ANCHOR_REVERSE = LOOP_LASTMSG_NEW_APPLY
LOOP_LASTMSG_NEW_REVERSE = LOOP_LASTMSG_ANCHOR_APPLY


# ==============================================================================
# Artifact_1 update
# ==============================================================================

# The existing artifact_1 Phase 4.0 entry around line 64-65 documents
# $lastmessage formatting with HUMAN-LAST-MSG prefix. Update to document
# the new conditional shape and spamShield config dependency.

ART1_LASTMSG_ANCHOR_APPLY = """**Lines 64-65** - `$lastmessage` formatted with HUMAN-LAST-MSG: prefix for downstream prompt assembly."""

ART1_LASTMSG_NEW_APPLY = """**Lines 64-65** - `$lastmessage` conditional construction (Patrick-evolution adopted via Tier A1 merge, 2026-05-18):
- When `$msgnew` is True: emits `(HUMAN-MSG: $msg)` for downstream prompt assembly
- When `$msgnew` is False AND `(spamShield)` is True (default): emits `" DO NOT RE-SEND OR SPAM!"` directive
- When `$msgnew` is False AND `(spamShield)` is False: emits empty string `""`
- Reads: `$msgnew`, `$msg`, `(spamShield)` config atom
- Writes: `$lastmessage` (local binding)
- Downstream consumers: line 72 println, line 113 soul_send_assemble (as 6th argument)
- 🧠 NETWORK-RELEVANT: SN signal modulation. Patrick's mechanism prevents the SN from re-presenting stale human-message content to downstream networks (FPN reading the prompt) when no new input has arrived. Removes the structural temptation for FPN to re-engage with already-handled content.
- Rationale: per `fork_additions_runtime_audit_2026-05-18.md` Tier A1, adopted to address echo-when-msgnew-is-false pathology. Our prior MESSAGE-IS-NEW flag approach was not honored by the LLM under prompt-surface pressure; Patrick's content-replacement approach is structurally stronger.
- spamShield config declared at line 9 (top-level), configured to True in initLoop (line 14 post-A1)."""

ART1_LASTMSG_ANCHOR_REVERSE = ART1_LASTMSG_NEW_APPLY
ART1_LASTMSG_NEW_REVERSE = ART1_LASTMSG_ANCHOR_APPLY


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
# Process loop.metta (3 coordinated edits)
# ==============================================================================

def process_loop(direction: str, dry_run: bool) -> dict:
    text = read_file(LOOP_PATH)
    original_text = text
    original_lines = text.count("\n")
    orig_opens, orig_closes = count_parens(text)

    if direction == "apply":
        anchor_1 = LOOP_CONFIG_DECL_ANCHOR_APPLY
        new_1 = LOOP_CONFIG_DECL_NEW_APPLY
        anchor_2 = LOOP_INITLOOP_ANCHOR_APPLY
        new_2 = LOOP_INITLOOP_NEW_APPLY
        anchor_3 = LOOP_LASTMSG_ANCHOR_APPLY
        new_3 = LOOP_LASTMSG_NEW_APPLY
    else:
        anchor_1 = LOOP_CONFIG_DECL_ANCHOR_REVERSE
        new_1 = LOOP_CONFIG_DECL_NEW_REVERSE
        anchor_2 = LOOP_INITLOOP_ANCHOR_REVERSE
        new_2 = LOOP_INITLOOP_NEW_REVERSE
        anchor_3 = LOOP_LASTMSG_ANCHOR_REVERSE
        new_3 = LOOP_LASTMSG_NEW_REVERSE

    # Pre-flight state checks
    if anchor_1 not in text:
        raise RuntimeError(f"Anchor 1 (config declaration) not found in {LOOP_PATH}.\nExpected to find:\n{anchor_1!r}\nLikely cause: disk content does not match expected pre-{direction} state.")
    if anchor_2 not in text:
        raise RuntimeError(f"Anchor 2 (initLoop configure) not found in {LOOP_PATH}.\nExpected to find:\n{anchor_2!r}\nLikely cause: disk content does not match expected pre-{direction} state.")
    if anchor_3 not in text:
        raise RuntimeError(f"Anchor 3 (lastmessage construction) not found in {LOOP_PATH}.\nExpected to find:\n{anchor_3!r}\nLikely cause: disk content does not match expected pre-{direction} state.")

    # Verify anchors are unique (no ambiguity)
    if text.count(anchor_1) != 1:
        raise RuntimeError(f"Anchor 1 appears {text.count(anchor_1)} times in {LOOP_PATH}, expected exactly 1.")
    if text.count(anchor_2) != 1:
        raise RuntimeError(f"Anchor 2 appears {text.count(anchor_2)} times in {LOOP_PATH}, expected exactly 1.")
    if text.count(anchor_3) != 1:
        raise RuntimeError(f"Anchor 3 appears {text.count(anchor_3)} times in {LOOP_PATH}, expected exactly 1.")

    # Apply edits in order
    text = text.replace(anchor_1, new_1, 1)
    text = text.replace(anchor_2, new_2, 1)
    text = text.replace(anchor_3, new_3, 1)

    new_lines = text.count("\n")
    new_opens, new_closes = count_parens(text)

    line_delta = new_lines - original_lines
    opens_delta = new_opens - orig_opens
    closes_delta = new_closes - orig_closes
    paren_baseline_delta = (orig_opens - orig_closes) - (new_opens - new_closes)

    print(f"  [{LOOP_PATH}]")
    print(f"    Lines: {original_lines} -> {new_lines} (delta {line_delta:+d})")
    print(f"    Parens: opens {orig_opens}->{new_opens}, closes {orig_closes}->{new_closes}, baseline delta {paren_baseline_delta:+d}->0")
    if direction == "apply":
        print(f"    Edits: (1) add spamShield config decl, (2) add configure spamShield True, (3) replace lastmessage with Patrick conditional")
    else:
        print(f"    Edits: (1) remove spamShield config decl, (2) remove configure spamShield True, (3) restore HUMAN-LAST-MSG two-line lastmessage")

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
        anchor = ART1_LASTMSG_ANCHOR_APPLY
        new = ART1_LASTMSG_NEW_APPLY
    else:
        anchor = ART1_LASTMSG_ANCHOR_REVERSE
        new = ART1_LASTMSG_NEW_REVERSE

    if anchor not in text:
        raise RuntimeError(f"Artifact_1 Phase 4.0 lastmessage anchor not found in {ART1_PATH}.\nExpected to find:\n{anchor!r}\nLikely cause: disk content does not match expected pre-{direction} state.")

    if text.count(anchor) != 1:
        raise RuntimeError(f"Artifact_1 anchor appears {text.count(anchor)} times, expected exactly 1.")

    text = text.replace(anchor, new, 1)
    new_lines = text.count("\n")
    line_delta = new_lines - original_lines

    print(f"  [{ART1_PATH}]")
    print(f"    Lines: {original_lines} -> {new_lines} (delta {line_delta:+d})")
    if direction == "apply":
        print(f"    Edit: expand Phase 4.0 lastmessage entry with Patrick-evolution documentation")
    else:
        print(f"    Edit: restore Phase 4.0 lastmessage entry to single-line summary")

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
    print(f"  A1 SPAMSHIELD MECHANISM: {direction.upper()} ({'DRY-RUN' if dry_run else 'WRITING'})")
    print("=" * 78)
    print()
    print(">>> Per-file state checks and edits <<<")
    print()

    processors = [
        ("loop.metta", process_loop),
        ("artifact_1", process_artifact1),
    ]

    # Dry-run first pass to verify all state checks pass before any writes
    results = []
    try:
        for name, processor in processors:
            result = processor(direction, dry_run=True)
            results.append((name, result))
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
    print(f"  SUMMARY: WHAT --{direction} --apply WILL DO")
    print("=" * 78)
    print()
    print(f"  Direction: {direction.upper()}")
    print(f"  Backup suffix: {BAK_SUFFIX}")
    print()
    if direction == "apply":
        print(f"  src/loop.metta: 3 coordinated edits")
        print(f"    (1) Insert (= (spamShield) (empty)) after wakeupInterval declaration")
        print(f"    (2) Insert (configure spamShield True) after sleepInterval configure")
        print(f"    (3) Replace 2-line HUMAN-LAST-MSG with Patrick's conditional lastmessage")
        print(f"  docs/design/artifact_1_loop_metta_wiring_diagram.md: expand Phase 4.0 lastmessage entry")
    else:
        print(f"  src/loop.metta: 3 coordinated reversals")
        print(f"    (1) Remove (= (spamShield) (empty)) declaration")
        print(f"    (2) Remove (configure spamShield True) initLoop call")
        print(f"    (3) Restore 2-line HUMAN-LAST-MSG lastmessage construction")
        print(f"  docs/design/artifact_1_loop_metta_wiring_diagram.md: restore single-line Phase 4.0 entry")
    print()
    print(f"  Contract: Artifact 0 Discipline 4 (wiring diagram in same commit)")
    print(f"  Reversibility: python3 staging/apply_a1_spamshield_mechanism.py --reverse --apply")
    print()
    print(f"  Post-apply rebuild required (--no-cache for loop.metta change):")
    print(f"    docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw")
    print()
    print(f"  Post-rebuild test order:")
    print(f"    Test 1 (heartbeat): iteration counter advances cleanly, single execution per cycle")
    print(f"    Test 2 (spamShield active): on msgnew=false cycles, log shows lastmessage")
    print(f"            replaced with anti-spam directive, NOT persistent HUMAN-LAST-MSG content")
    print(f"    Test 3 (msgnew=true normal): on Berton sending MM message, lastmessage")
    print(f"            shows HUMAN-MSG: <content> cleanly, LLM responds")
    print(f"    Test 4 (echo reduction): observe whether stale-message echo pattern reduces over")
    print(f"            multi-cycle idle window post-response")
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
        print(f"  WARNING: paren mismatch in loop.metta ({loop_opens} opens, {loop_closes} closes)")
        print()

    print("=" * 78)
    print(f"  A1 SPAMSHIELD MECHANISM {direction.upper()} COMPLETE")
    print("=" * 78)
    print()


if __name__ == "__main__":
    main()
