#!/usr/bin/env python3
"""
apply_collapse_eval_fix.py

Surgical edit to src/loop.metta line 127:
  (eval $s)  ->  (collapse (eval $s))

This materializes the inner nondet stream from (eval $s) into a tuple
before the let binds $R, preventing nondet sub-streams from splintering
the COMMAND_RETURN tuple construction.

Diagnosis confirmed via:
- Patrick Hammer (PeTTa creator): match returns nondet stream, not list
- MeTTa_Type.txt: superpose (-> Expression %Undefined%), collapse (-> Atom Atom)
- Clarity (substrate-resident agent): traced bug to two nondet sources
  stacked at line 127, with outer collapse only materializing the
  superpose level not the eval level
- Crash signature: janus:py_call/3: Arguments are not sufficiently instantiated

Discipline:
- Single occurrence target (verified: '(eval $s)' appears exactly once in loop.metta)
- Read full file, verify exactly one match, perform substitution, verify exactly one change
- Byte-level proof of targeted modification
- Backup file written before any change
- --reverse mode reverts the change cleanly
- --dry-run shows what would change without writing

Usage:
  python3 apply_collapse_eval_fix.py                 # dry run by default
  python3 apply_collapse_eval_fix.py --apply         # actually apply
  python3 apply_collapse_eval_fix.py --reverse --apply  # revert
"""

import argparse
import os
import sys
from pathlib import Path


TARGET_FILE = "src/loop.metta"
BACKUP_SUFFIX = ".bak.collapse_eval_fix"

# The exact substring we expect to find. Single occurrence in line 127.
OLD_PATTERN = "(catch (let $R (eval $s) (py-call (helper.normalize_string $R))))"
NEW_PATTERN = "(catch (let $R (collapse (eval $s)) (py-call (helper.normalize_string $R))))"

# For --reverse mode, swap them
def get_patterns(reverse: bool):
    if reverse:
        return NEW_PATTERN, OLD_PATTERN
    return OLD_PATTERN, NEW_PATTERN


def find_loop_metta() -> Path:
    """Locate src/loop.metta, walking up from cwd if needed."""
    cwd = Path.cwd()
    candidates = [
        cwd / TARGET_FILE,
        cwd / "loop.metta",
    ]
    # Walk up to find a project root containing src/loop.metta
    for parent in [cwd, *cwd.parents]:
        candidate = parent / TARGET_FILE
        if candidate.exists():
            return candidate
    for c in candidates:
        if c.exists():
            return c
    raise FileNotFoundError(
        f"Could not locate {TARGET_FILE}. Run this script from the clarityclaw-omega directory."
    )


def verify_uniqueness(content: str, pattern: str) -> int:
    """Count occurrences of pattern. Should be exactly 1."""
    count = content.count(pattern)
    return count


def apply_change(path: Path, dry_run: bool, reverse: bool) -> bool:
    """Apply or dry-run the change. Returns True on success, False otherwise."""
    old_pattern, new_pattern = get_patterns(reverse)

    direction = "REVERSE" if reverse else "FORWARD"
    print(f"=== apply_collapse_eval_fix.py [{direction}{'  DRY-RUN' if dry_run else ''}] ===")
    print(f"Target file: {path}")

    if not path.exists():
        print(f"ERROR: file does not exist: {path}", file=sys.stderr)
        return False

    original_bytes = path.read_bytes()
    try:
        content = original_bytes.decode("utf-8")
    except UnicodeDecodeError as e:
        print(f"ERROR: could not decode file as UTF-8: {e}", file=sys.stderr)
        return False

    print(f"File size: {len(original_bytes)} bytes")

    # Look for the OLD pattern (the one we want to replace)
    old_count = verify_uniqueness(content, old_pattern)
    new_count = verify_uniqueness(content, new_pattern)

    print(f"Looking for OLD pattern: {old_pattern!r}")
    print(f"  occurrences: {old_count}")
    print(f"Looking for NEW pattern: {new_pattern!r}")
    print(f"  occurrences: {new_count}")

    # Sanity checks
    if old_count == 0:
        if new_count > 0:
            print(
                f"\nNOTE: OLD pattern not found, but NEW pattern is already present "
                f"({new_count} occurrence(s)).",
                file=sys.stderr,
            )
            print("The fix appears to already be applied (or in --reverse mode, already reverted).", file=sys.stderr)
        else:
            print(
                f"\nERROR: neither OLD nor NEW pattern found in file. "
                f"File may have diverged from expected state.",
                file=sys.stderr,
            )
        return False

    if old_count > 1:
        print(
            f"\nERROR: OLD pattern found {old_count} times. Expected exactly 1. "
            f"Aborting to avoid unintended changes.",
            file=sys.stderr,
        )
        return False

    if new_count > 0:
        print(
            f"\nERROR: NEW pattern already present {new_count} time(s) before edit. "
            f"This is unexpected. Aborting.",
            file=sys.stderr,
        )
        return False

    # Perform the substitution
    new_content = content.replace(old_pattern, new_pattern, 1)

    # Verify exactly one change occurred
    after_old_count = new_content.count(old_pattern)
    after_new_count = new_content.count(new_pattern)

    if after_old_count != 0:
        print(
            f"\nERROR: post-substitution OLD pattern still present {after_old_count} time(s). "
            f"Aborting before write.",
            file=sys.stderr,
        )
        return False

    if after_new_count != 1:
        print(
            f"\nERROR: post-substitution NEW pattern present {after_new_count} time(s), expected 1. "
            f"Aborting before write.",
            file=sys.stderr,
        )
        return False

    # Byte-level diff verification
    new_bytes = new_content.encode("utf-8")
    delta = len(new_bytes) - len(original_bytes)
    expected_delta = len(new_pattern.encode("utf-8")) - len(old_pattern.encode("utf-8"))

    if delta != expected_delta:
        print(
            f"\nERROR: byte delta mismatch. expected {expected_delta}, got {delta}. "
            f"Aborting.",
            file=sys.stderr,
        )
        return False

    print(f"\nVerification:")
    print(f"  Original size: {len(original_bytes)} bytes")
    print(f"  New size:      {len(new_bytes)} bytes")
    print(f"  Delta:         {delta:+d} bytes (expected {expected_delta:+d})")
    print(f"  Substitutions: 1 (verified)")

    if dry_run:
        print("\n[DRY-RUN] No changes written. Use --apply to commit.")
        return True

    # Write backup
    backup_path = path.with_suffix(path.suffix + BACKUP_SUFFIX)
    backup_path.write_bytes(original_bytes)
    print(f"\nBackup written: {backup_path}")

    # Write the new content
    path.write_bytes(new_bytes)
    print(f"Modified file: {path}")

    # Re-read and verify
    rewritten = path.read_bytes()
    if rewritten != new_bytes:
        print(
            f"\nERROR: post-write verification failed. File on disk does not match "
            f"intended content. Restoring from backup.",
            file=sys.stderr,
        )
        path.write_bytes(original_bytes)
        return False

    print("Post-write verification: OK")
    print(f"\nDone. To revert, run:")
    print(f"  python3 {Path(__file__).name} --reverse --apply")

    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Surgical edit to src/loop.metta line 127: wrap (eval $s) in collapse",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually write the change. Default is dry-run.",
    )
    parser.add_argument(
        "--reverse",
        action="store_true",
        help="Revert the change instead of applying it.",
    )
    args = parser.parse_args()

    dry_run = not args.apply

    try:
        path = find_loop_metta()
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    success = apply_change(path, dry_run=dry_run, reverse=args.reverse)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
