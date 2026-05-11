#!/usr/bin/env python3
"""
Restore sanitize_response call to loop.metta $resp binding.

Background:
  During OmegaClaw migration, helper.sanitize_response was replaced with
  helper.normalize_string at the $resp binding. The two functions do
  different things:
    - normalize_string: cleans malformed UTF-8 (Patrick's, errors='ignore')
    - sanitize_response: strips valid multi-byte UTF-8 to ASCII (ours, errors='replace')

  The substitution lost C5 protection. Em dashes in LLM (send "...") body
  flow into $results and crash at (repr $results) upstream of safe_results_str.

Fix:
  Compose the two functions. Patrick's normalize_string stays untouched
  in its existing call site. sanitize_response wraps the result.

Bedrock rule:
  Patrick's code is not modified. normalize_string call is preserved
  verbatim. sanitize_response is added as the outermost wrap, our
  function only.

Paren-balance rule:
  Any edit to loop.metta must preserve code-aware paren delta of 0.
  This script verifies the pre-edit and post-edit balance and refuses
  to write if either fails.

Reversibility:
  --reverse --apply restores the pre-fix state from the backup written
  at apply time.

Usage:
  python3 staging/apply_sanitize_response_restore.py             # dry-run preview
  python3 staging/apply_sanitize_response_restore.py --apply     # write changes
  python3 staging/apply_sanitize_response_restore.py --reverse --apply   # revert
"""
import argparse
import shutil
import sys
from pathlib import Path

LOOP_PATH = Path("src/loop.metta")
BACKUP_PATH = Path("src/loop.metta.bak.sanitize_response_restore")

OLD_LINE = '($resp (py-call (helper.normalize_string (py-call (helper.balance_parentheses $respi)))))'
NEW_LINE = '($resp (py-call (helper.sanitize_response (py-call (helper.normalize_string (py-call (helper.balance_parentheses $respi)))))))'

# Expected baseline (code-aware count) before the edit. If the file does not
# match this, something else has changed since the edit was designed and we
# refuse to apply.
EXPECTED_PRE_OPENS = 423
EXPECTED_PRE_CLOSES = 423
# Expected post-edit count (must always have delta == 0 regardless of these).
EXPECTED_POST_OPENS = 425
EXPECTED_POST_CLOSES = 425


def count_parens_aware(s):
    """Count parens in s, ignoring those inside strings and after ; line comments.

    This matches what PeTTa/Prolog actually parses. Returns (opens, closes).
    """
    opens = closes = 0
    in_string = False
    in_comment = False
    escape = False
    for ch in s:
        if escape:
            escape = False
            continue
        if in_string:
            if ch == '\\':
                escape = True
                continue
            if ch == '"':
                in_string = False
            continue
        if in_comment:
            if ch == '\n':
                in_comment = False
            continue
        if ch == '"':
            in_string = True
            continue
        if ch == ';':
            in_comment = True
            continue
        if ch == '(':
            opens += 1
        elif ch == ')':
            closes += 1
    return opens, closes


def find_target_line(content, target):
    """Return list of (lineno, full_line) tuples where target appears."""
    hits = []
    for i, line in enumerate(content.splitlines(), 1):
        if target in line:
            hits.append((i, line))
    return hits


def apply_forward(dry_run):
    if not LOOP_PATH.exists():
        print(f"ERROR: {LOOP_PATH} not found. Run from repo root.", file=sys.stderr)
        return 1

    content = LOOP_PATH.read_text()

    # PRE-FLIGHT CHECK 1: target line presence
    hits = find_target_line(content, OLD_LINE)
    if len(hits) == 0:
        print(f"ERROR: Target line not found. Either already applied or loop.metta has changed.",
              file=sys.stderr)
        existing = find_target_line(content, NEW_LINE)
        if existing:
            print(f"  Note: NEW_LINE pattern found at line(s) {[h[0] for h in existing]} -- fix may already be applied.",
                  file=sys.stderr)
        return 1
    if len(hits) > 1:
        print(f"ERROR: Target line matched {len(hits)} times at lines {[h[0] for h in hits]}. Expected exactly 1.",
              file=sys.stderr)
        return 1
    lineno, full_line = hits[0]

    # PRE-FLIGHT CHECK 2: code-aware paren balance of the file BEFORE edit
    pre_opens, pre_closes = count_parens_aware(content)
    pre_delta = pre_opens - pre_closes
    print(f"Pre-edit code-aware paren count: {pre_opens} opens / {pre_closes} closes / delta = {pre_delta:+d}")
    if pre_delta != 0:
        print(f"ERROR: File is not paren-balanced before edit (delta = {pre_delta:+d}). "
              f"Refusing to edit a file that is already structurally broken.", file=sys.stderr)
        return 1
    if pre_opens != EXPECTED_PRE_OPENS or pre_closes != EXPECTED_PRE_CLOSES:
        print(f"WARNING: Pre-edit paren count differs from expected baseline.")
        print(f"  Expected: {EXPECTED_PRE_OPENS} opens / {EXPECTED_PRE_CLOSES} closes")
        print(f"  Actual:   {pre_opens} opens / {pre_closes} closes")
        print(f"  This means loop.metta has changed since this fix was designed.")
        print(f"  The edit may still be safe (delta is still 0), but please confirm.")
        if not dry_run:
            print(f"ERROR: Refusing to apply with mismatched baseline. Re-run with --apply ONLY after confirming.",
                  file=sys.stderr)
            return 1

    # Show what will change
    print(f"\nFound target at line {lineno}.")
    print(f"  Current content:    {full_line!r}")
    new_full_line = full_line.replace(OLD_LINE, NEW_LINE)
    print(f"  Proposed content:   {new_full_line!r}")

    # PRE-FLIGHT CHECK 3: simulate the edit in memory and verify balance
    new_content = content.replace(OLD_LINE, NEW_LINE)
    if new_content == content:
        print("ERROR: Replacement produced no change. Aborting.", file=sys.stderr)
        return 1

    post_opens, post_closes = count_parens_aware(new_content)
    post_delta = post_opens - post_closes
    print(f"\nPost-edit code-aware paren count (simulated in memory):")
    print(f"  {post_opens} opens / {post_closes} closes / delta = {post_delta:+d}")

    if post_delta != 0:
        print(f"ERROR: Post-edit file would be paren-unbalanced (delta = {post_delta:+d}). "
              f"This means OLD_LINE or NEW_LINE has unbalanced parens. Refusing to write.", file=sys.stderr)
        return 1

    delta_change = post_delta - pre_delta  # should be 0
    open_change = post_opens - pre_opens
    close_change = post_closes - pre_closes
    print(f"  Change vs baseline: +{open_change} opens, +{close_change} closes, delta change = {delta_change:+d}")

    if delta_change != 0:
        print(f"ERROR: Edit changes file delta by {delta_change:+d}. Refusing to write.", file=sys.stderr)
        return 1

    # All pre-flight checks passed
    print(f"\nAll pre-flight checks passed:")
    print(f"  - Target line found exactly once at line {lineno}")
    print(f"  - Pre-edit file is paren-balanced (delta = 0)")
    print(f"  - Post-edit file is paren-balanced (delta = 0)")
    print(f"  - Edit adds matched parens (+{open_change}/+{close_change})")

    if dry_run:
        print("\nDRY RUN. No changes written. Re-run with --apply to write.")
        return 0

    # Write
    print(f"\nWriting backup to {BACKUP_PATH}")
    shutil.copy2(LOOP_PATH, BACKUP_PATH)
    LOOP_PATH.write_text(new_content)
    print(f"Wrote modified {LOOP_PATH}.")

    # POST-WRITE VERIFICATION: re-read and re-count
    verify_content = LOOP_PATH.read_text()
    new_hits = find_target_line(verify_content, NEW_LINE)
    if len(new_hits) != 1:
        print(f"ERROR: Post-write verification failed. NEW_LINE pattern matched {len(new_hits)} times.",
              file=sys.stderr)
        print(f"  Restoring from backup.", file=sys.stderr)
        shutil.copy2(BACKUP_PATH, LOOP_PATH)
        return 1

    verify_opens, verify_closes = count_parens_aware(verify_content)
    if verify_opens != post_opens or verify_closes != post_closes:
        print(f"ERROR: Post-write paren count does not match simulation. "
              f"Expected {post_opens}/{post_closes}, got {verify_opens}/{verify_closes}. "
              f"Restoring from backup.", file=sys.stderr)
        shutil.copy2(BACKUP_PATH, LOOP_PATH)
        return 1

    print(f"Verified on disk: NEW_LINE pattern present at line {new_hits[0][0]}, "
          f"paren count {verify_opens}/{verify_closes}, delta = {verify_opens - verify_closes:+d}.")
    return 0


def apply_reverse(dry_run):
    if not BACKUP_PATH.exists():
        print(f"ERROR: Backup {BACKUP_PATH} not found. Cannot reverse.", file=sys.stderr)
        return 1
    if dry_run:
        print(f"DRY RUN. Would restore {LOOP_PATH} from {BACKUP_PATH}.")
        # Show what the restored balance would be
        backup_content = BACKUP_PATH.read_text()
        b_opens, b_closes = count_parens_aware(backup_content)
        print(f"  Backup paren count: {b_opens} opens / {b_closes} closes / delta = {b_opens - b_closes:+d}")
        return 0
    shutil.copy2(BACKUP_PATH, LOOP_PATH)
    print(f"Restored {LOOP_PATH} from {BACKUP_PATH}.")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--apply", action="store_true",
                    help="Write changes (default is dry-run preview)")
    ap.add_argument("--reverse", action="store_true",
                    help="Restore from backup")
    args = ap.parse_args()
    dry_run = not args.apply
    if args.reverse:
        return apply_reverse(dry_run)
    return apply_forward(dry_run)


if __name__ == "__main__":
    sys.exit(main())
