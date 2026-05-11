#!/usr/bin/env python3
"""
Disable Genesis Encounter directive insertion in build_directive() in
soul/idle_goal_prompt.py to allow container to boot past the $results
unbound-variable crash.

This is a TEMPORARY WORKAROUND. Reverse with --reverse.

Discipline: targets exactly one block in one file. Verifies only the
targeted block changed. AST parse on existing file (sanity baseline)
and on result file (confirms valid Python). No restructuring, no
refactoring, no other changes.

Usage:
    python3 apply_genesis_disable.py              # dry-run (disable)
    python3 apply_genesis_disable.py --apply      # apply (disable)
    python3 apply_genesis_disable.py --reverse    # dry-run (re-enable)
    python3 apply_genesis_disable.py --reverse --apply  # apply (re-enable)
"""

import sys
import os
import shutil
import difflib
import ast
from datetime import datetime

TARGET_FILE = 'soul/idle_goal_prompt.py'

DISABLE_OLD = '''    if mode == 'creative':
        sections.append(genesis)'''

DISABLE_NEW = '''    if mode == 'creative':
        # === TEMP WORKAROUND: GENESIS_DISABLED_2026-05-06 ===
        # Genesis Encounter directive disabled to allow container to boot
        # past $results unbound-variable crash. Reverse with:
        #   python3 apply_genesis_disable.py --reverse --apply
        # See Sprint 4 doc, GLM Switch section, $results crash entry.
        # sections.append(genesis)
        pass
        # === END TEMP WORKAROUND ==='''


def color(text, code):
    return f"\033[{code}m{text}\033[0m"

def red(t): return color(t, '31')
def green(t): return color(t, '32')
def yellow(t): return color(t, '33')
def blue(t): return color(t, '34')
def bold(t): return color(t, '1')


def show_diff(path, old_content, new_content):
    diff = difflib.unified_diff(
        old_content.splitlines(keepends=True),
        new_content.splitlines(keepends=True),
        fromfile=f'a/{path}',
        tofile=f'b/{path}',
        n=4,
    )
    for line in diff:
        s = line.rstrip()
        if line.startswith('+++') or line.startswith('---'):
            print(bold(s))
        elif line.startswith('+'):
            print(green(s))
        elif line.startswith('-'):
            print(red(s))
        elif line.startswith('@@'):
            print(blue(s))
        else:
            print(s)


def verify_only_targeted_block_changed(old_content, new_content, old_block, new_block):
    """Confirm the only difference between old and new is the targeted
    block being replaced. Anything else differing is a structural change
    we did not intend.
    """
    # Compute what the file would look like if ONLY the targeted block
    # changed
    expected_new = old_content.replace(old_block, new_block, 1)
    if expected_new == new_content:
        return True, None
    # Find first divergence
    for i, (a, b) in enumerate(zip(expected_new, new_content)):
        if a != b:
            return False, f"unexpected divergence at byte {i}"
    if len(expected_new) != len(new_content):
        return False, f"length mismatch: expected {len(expected_new)}, got {len(new_content)}"
    return False, "unknown divergence"


def main():
    apply_changes = '--apply' in sys.argv
    reverse = '--reverse' in sys.argv

    if reverse:
        old_text = DISABLE_NEW
        new_text = DISABLE_OLD
        action = "REVERSE: Re-enable Genesis Encounter"
        backup_label = "pre-genesis-reenable"
    else:
        old_text = DISABLE_OLD
        new_text = DISABLE_NEW
        action = "DISABLE: Comment out Genesis Encounter directive"
        backup_label = "pre-genesis-disable"

    print(bold("=" * 70))
    print(bold(action))
    print(bold("=" * 70))
    print(f"Mode:              {'APPLY' if apply_changes else 'DRY-RUN'}")
    print(f"Direction:         {'REVERSE' if reverse else 'FORWARD'}")
    print(f"Target file:       {TARGET_FILE}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Timestamp:         {datetime.now().isoformat()}")
    print()

    # Phase 1: pre-conditions
    print(bold("PHASE 1: Pre-conditions"))
    print("-" * 70)
    if not os.path.exists(TARGET_FILE):
        print(red(f"  FAIL: {TARGET_FILE} not found"))
        return 1
    print(green(f"  OK:   {TARGET_FILE} exists"))

    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        current = f.read()

    # Sanity: existing file is valid Python before we touch it
    try:
        ast.parse(current)
        print(green(f"  OK:   {TARGET_FILE} parses as valid Python (baseline)"))
    except SyntaxError as e:
        print(red(f"  FAIL: {TARGET_FILE} does not parse: {e}"))
        return 1

    if old_text not in current:
        print(red(f"  FAIL: expected source text not found"))
        if reverse:
            print(red(f"        is the file currently in disabled state?"))
        else:
            print(red(f"        is the file already disabled?"))
        return 1
    print(green(f"  OK:   expected source text found"))

    if new_text in current:
        print(yellow(f"  WARN: target text already present, file is already in desired state"))
        return 0
    print(green(f"  OK:   target text not yet present"))

    # Verify the source block appears exactly once (so .replace() with count=1
    # operates unambiguously)
    occurrences = current.count(old_text)
    if occurrences != 1:
        print(red(f"  FAIL: source text appears {occurrences} times, expected exactly 1"))
        return 1
    print(green(f"  OK:   source text appears exactly once"))

    print()
    print(green(bold("Phase 1 complete.")))
    print()

    # Phase 2: compute change
    print(bold("PHASE 2: Compute change"))
    print("-" * 70)
    proposed = current.replace(old_text, new_text, 1)

    # Sanity: proposed file is valid Python
    try:
        ast.parse(proposed)
        print(green(f"  OK:   proposed file parses as valid Python"))
    except SyntaxError as e:
        print(red(f"  FAIL: proposed file does not parse: {e}"))
        return 1

    # Confirm only the targeted block changed
    only_targeted, err = verify_only_targeted_block_changed(current, proposed, old_text, new_text)
    if not only_targeted:
        print(red(f"  FAIL: changes outside targeted block: {err}"))
        return 1
    print(green(f"  OK:   only the targeted block differs between old and proposed"))

    # Confirm line count delta is exactly what we expect
    old_lines = current.splitlines()
    new_lines = proposed.splitlines()
    expected_delta = len(new_text.splitlines()) - len(old_text.splitlines())
    actual_delta = len(new_lines) - len(old_lines)
    if actual_delta != expected_delta:
        print(red(f"  FAIL: line count delta mismatch: expected {expected_delta}, got {actual_delta}"))
        return 1
    print(green(f"  OK:   line count delta is {actual_delta:+d} as expected"))

    print()
    print(bold("Diff to be applied:"))
    print("-" * 70)
    show_diff(TARGET_FILE, current, proposed)
    print()

    # Phase 3: apply or stop
    if not apply_changes:
        print(bold("=" * 70))
        print(yellow(bold("DRY-RUN COMPLETE. No files modified.")))
        if reverse:
            print("To apply: python3 apply_genesis_disable.py --reverse --apply")
        else:
            print("To apply: python3 apply_genesis_disable.py --apply")
        print(bold("=" * 70))
        return 0

    print(bold("PHASE 3: Apply"))
    print("-" * 70)

    backup_suffix = f".{backup_label}-{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
    backup_path = TARGET_FILE + backup_suffix

    try:
        shutil.copy2(TARGET_FILE, backup_path)
        print(green(f"  Backed up: {TARGET_FILE} -> {backup_path}"))

        with open(TARGET_FILE, 'w', encoding='utf-8') as f:
            f.write(proposed)
        print(green(f"  Wrote:     {TARGET_FILE}"))

        # Phase 4: post-conditions
        print()
        print(bold("PHASE 4: Post-conditions"))
        print("-" * 70)
        all_ok = True

        with open(TARGET_FILE, 'r', encoding='utf-8') as f:
            on_disk = f.read()

        if on_disk != proposed:
            print(red(f"  FAIL: written file does not match proposed content"))
            all_ok = False
        else:
            print(green(f"  OK:   written file matches proposed content exactly"))

        try:
            ast.parse(on_disk)
            print(green(f"  OK:   written file parses as valid Python"))
        except SyntaxError as e:
            print(red(f"  FAIL: written file does not parse: {e}"))
            all_ok = False

        if old_text in on_disk:
            print(red(f"  FAIL: old text still present"))
            all_ok = False
        else:
            print(green(f"  OK:   old text removed"))

        if new_text not in on_disk:
            print(red(f"  FAIL: new text not present"))
            all_ok = False
        else:
            print(green(f"  OK:   new text present"))

        if not all_ok:
            print()
            print(red(bold("POST-CONDITION FAILURE. ROLLING BACK.")))
            shutil.copy2(backup_path, TARGET_FILE)
            print(yellow(f"  Restored: {TARGET_FILE}"))
            return 2

        print()
        print(green(bold("Phase 4 complete.")))
        print()
        print(bold("=" * 70))
        if reverse:
            print(green(bold("GENESIS ENCOUNTER RE-ENABLED")))
        else:
            print(green(bold("GENESIS ENCOUNTER DISABLED (TEMP WORKAROUND)")))
        print(bold("=" * 70))
        print()
        print(f"Backup: {backup_path}")
        print()
        print("To roll back manually:")
        print(f"  cp {backup_path} {TARGET_FILE}")
        print()
        if reverse:
            print(bold("To disable again:"))
            print("  python3 apply_genesis_disable.py --apply")
        else:
            print(bold("To re-enable:"))
            print("  python3 apply_genesis_disable.py --reverse --apply")
        print()
        print(bold("Next:"))
        print("  docker compose build --no-cache clarityclaw && docker compose up -d")
        print("  docker logs -f clarity_omega")
        print()
        return 0

    except Exception as e:
        print(red(f"\nERROR: {e}"))
        try:
            shutil.copy2(backup_path, TARGET_FILE)
            print(yellow(f"  Restored: {TARGET_FILE}"))
        except Exception as rerr:
            print(red(f"  ROLLBACK FAILED: {rerr}"))
        return 3


if __name__ == '__main__':
    sys.exit(main())