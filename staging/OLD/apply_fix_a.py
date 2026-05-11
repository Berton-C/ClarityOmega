#!/usr/bin/env python3
"""
Fix A: Replace parser-hostile (N) parenthesized enumeration with [N] bracket style
in runtime LLM-prompt locations.

Hypothesis: Removing parenthesized number enumeration (1) (2) (3) from runtime
LLM-prompt locations and replacing with [1] [2] [3] will reduce or eliminate
Pattern A calcification (parser-hostile prose enumeration triggering parser-salvage
of LLM output into pin-fragments) without changing semantic meaning.

Usage:
    python3 apply_fix_a.py           # dry-run, shows what would change
    python3 apply_fix_a.py --apply   # actually apply changes

Exit codes:
    0 - success (or dry-run completed)
    1 - pre-condition check failed (file content differs from expectation)
    2 - post-condition check failed (write succeeded but verification failed)
    3 - file I/O error
"""

import sys
import os
import shutil
import difflib
from datetime import datetime

# ============================================================
# EDIT SPECIFICATIONS
# Each entry: (path, expected_old_text, replacement_text, context_description)
# ============================================================

EDITS = [
    # --- src/helper.py ---
    (
        'src/helper.py',
        'Safety (1) > Integrity (2) > HumanFlourishing (3) > Governance (4) > Helpfulness (5)',
        'Safety [1] > Integrity [2] > HumanFlourishing [3] > Governance [4] > Helpfulness [5]',
        'soul_eval_prompt: Step 4 HIERARCHY line (Channel B+C input verdict prompt)',
    ),
    (
        'src/helper.py',
        '[(1 Safety) (2 Integrity) (3 HumanFlourishing) (4 Governance) (5 Helpfulness)]',
        '[[1] Safety [2] Integrity [3] HumanFlourishing [4] Governance [5] Helpfulness]',
        'soul_brief_tier_a_static: PRIORITY HIERARCHY in SOUL_CONTEXT (every cycle)',
    ),
    
    # --- soul/idle_goal_prompt.py ---
    (
        'soul/idle_goal_prompt.py',
        "'Priority Hierarchy: (1) Safety (2) Integrity (3) HumanFlourishing (4) Governance (5) Helpfulness'",
        "'Priority Hierarchy: [1] Safety [2] Integrity [3] HumanFlourishing [4] Governance [5] Helpfulness'",
        'build_directive: idle directive priority hierarchy (every idle cycle)',
    ),
    # NOTE: idle_goal_prompt.py has the same string at two locations (382 and 501).
    # The replace() call will catch both occurrences in one pass.
    
    # --- soul/continuity_driver.metta ---
    (
        'soul/continuity_driver.metta',
        'HumanFlourishing (3) outranks',
        'HumanFlourishing [3] outranks',
        'continuity_driver comment line: hierarchy reference',
    ),
    
    # --- soul/creative_fuel.metta ---
    (
        'soul/creative_fuel.metta',
        ';; Safety (1) and Integrity (2) gaps get addressed before',
        ';; Safety [1] and Integrity [2] gaps get addressed before',
        'creative_fuel comment line: priority hierarchy reference',
    ),
    (
        'soul/creative_fuel.metta',
        ';; WonderPreservation (6) gaps, even if wonder is more interesting.',
        ';; WonderPreservation [6] gaps, even if wonder is more interesting.',
        'creative_fuel comment line: continuation of hierarchy reference',
    ),
    
    # --- soul/self_map.metta ---
    (
        'soul/self_map.metta',
        "soul's hierarchy: HumanFlourishing (3) > self-growth goals.",
        "soul's hierarchy: HumanFlourishing [3] > self-growth goals.",
        'self_map comment line: hierarchy reference',
    ),
]

# ============================================================
# UTILITIES
# ============================================================

def color(text, code):
    return f"\033[{code}m{text}\033[0m"

def red(t): return color(t, '31')
def green(t): return color(t, '32')
def yellow(t): return color(t, '33')
def blue(t): return color(t, '34')
def bold(t): return color(t, '1')

def show_diff(path, old_content, new_content):
    """Show a unified diff of the changes."""
    diff = difflib.unified_diff(
        old_content.splitlines(keepends=True),
        new_content.splitlines(keepends=True),
        fromfile=f'a/{path}',
        tofile=f'b/{path}',
        n=2,
    )
    for line in diff:
        if line.startswith('+++') or line.startswith('---'):
            print(bold(line.rstrip()))
        elif line.startswith('+'):
            print(green(line.rstrip()))
        elif line.startswith('-'):
            print(red(line.rstrip()))
        elif line.startswith('@@'):
            print(blue(line.rstrip()))
        else:
            print(line.rstrip())

# ============================================================
# MAIN
# ============================================================

def main():
    apply_changes = '--apply' in sys.argv
    
    print(bold("=" * 70))
    print(bold("Fix A: Parser-hostile enumeration removal"))
    print(bold("=" * 70))
    print()
    print(f"Mode: {'APPLY (will modify files)' if apply_changes else 'DRY-RUN (no files modified)'}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    # ----------------------------------------------------------------
    # PHASE 1: Pre-condition checks
    # Verify all target files exist and contain the expected old text.
    # ----------------------------------------------------------------
    print(bold("PHASE 1: Pre-condition checks"))
    print("-" * 70)
    
    file_contents = {}  # path -> current content
    file_planned_changes = {}  # path -> list of (old, new, desc)
    
    for path, old, new, desc in EDITS:
        if not os.path.exists(path):
            print(red(f"  FAIL: {path} does not exist"))
            print(red("  ABORT: cannot proceed with missing file."))
            return 1
        
        # Read once per file
        if path not in file_contents:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    file_contents[path] = f.read()
                file_planned_changes[path] = []
            except IOError as e:
                print(red(f"  FAIL: cannot read {path}: {e}"))
                return 3
        
        content = file_contents[path]
        
        if old not in content:
            print(red(f"  FAIL: {path}"))
            print(red(f"        expected text not found: {desc}"))
            print(red(f"        looking for: {old[:100]}{'...' if len(old) > 100 else ''}"))
            print(red("  ABORT: file content does not match audit expectations."))
            print(red("        File may have changed since audit. Re-run audit and update script."))
            return 1
        
        # Check that the new text is not already present (prevents double-apply)
        # We check this only against the original content, not after edits, so the
        # check is informational rather than blocking
        occurrence_count = content.count(old)
        
        file_planned_changes[path].append((old, new, desc, occurrence_count))
        print(green(f"  OK:   {path}"))
        print(f"        {desc} ({occurrence_count} occurrence{'s' if occurrence_count != 1 else ''})")
    
    print()
    print(green(bold("Phase 1 complete: all pre-conditions met.")))
    print()
    
    # ----------------------------------------------------------------
    # PHASE 2: Compute changes (in-memory) and show diffs
    # ----------------------------------------------------------------
    print(bold("PHASE 2: Computing changes (in-memory)"))
    print("-" * 70)
    
    new_contents = {}  # path -> new content
    
    for path, changes in file_planned_changes.items():
        original = file_contents[path]
        modified = original
        total_replacements = 0
        
        for old, new, desc, expected_count in changes:
            # Count before replace
            before_count = modified.count(old)
            modified = modified.replace(old, new)
            after_count = modified.count(old)
            replacements_made = before_count - after_count
            total_replacements += replacements_made
            
            if replacements_made == 0:
                print(red(f"  WARNING: no replacement made for {desc}"))
            elif replacements_made != expected_count:
                print(yellow(f"  NOTE: {replacements_made} replacement(s) made for {desc} (expected {expected_count})"))
        
        new_contents[path] = modified
        print(f"  {path}: {total_replacements} total replacement(s)")
    
    print()
    print(bold("PHASE 2.5: Diffs to be applied"))
    print("-" * 70)
    
    for path in new_contents:
        if file_contents[path] == new_contents[path]:
            print(yellow(f"\n  No changes for {path}"))
            continue
        print(f"\n--- Diff for {bold(path)} ---")
        show_diff(path, file_contents[path], new_contents[path])
    
    print()
    
    # ----------------------------------------------------------------
    # PHASE 3: Apply (if --apply) or stop (if dry-run)
    # ----------------------------------------------------------------
    if not apply_changes:
        print(bold("=" * 70))
        print(yellow(bold("DRY-RUN COMPLETE. No files modified.")))
        print()
        print("To apply these changes, run:")
        print(bold("    python3 apply_fix_a.py --apply"))
        print(bold("=" * 70))
        return 0
    
    print(bold("PHASE 3: Applying changes with backups"))
    print("-" * 70)
    
    backup_suffix = f".pre-fix-a-{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
    backups_made = []
    
    try:
        # Backup all files first
        for path in new_contents:
            if file_contents[path] == new_contents[path]:
                continue  # no changes, no backup needed
            backup_path = path + backup_suffix
            shutil.copy2(path, backup_path)
            backups_made.append((path, backup_path))
            print(green(f"  Backed up: {path} -> {backup_path}"))
        
        # Write all files
        for path, content in new_contents.items():
            if file_contents[path] == content:
                continue
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(green(f"  Wrote:     {path}"))
        
        print()
        
        # ----------------------------------------------------------------
        # PHASE 4: Post-condition checks
        # Re-read files and verify the edits took.
        # ----------------------------------------------------------------
        print(bold("PHASE 4: Post-condition checks"))
        print("-" * 70)
        
        all_verified = True
        
        for path, changes in file_planned_changes.items():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    on_disk = f.read()
            except IOError as e:
                print(red(f"  FAIL: cannot re-read {path}: {e}"))
                all_verified = False
                continue
            
            for old, new, desc, _ in changes:
                old_still_present = old in on_disk
                new_present = new in on_disk
                
                if old_still_present:
                    print(red(f"  FAIL: old text still present in {path}: {desc}"))
                    all_verified = False
                if not new_present:
                    print(red(f"  FAIL: new text not found in {path}: {desc}"))
                    all_verified = False
            
            if all([new in on_disk and old not in on_disk for old, new, _, _ in changes]):
                print(green(f"  OK:   {path}"))
        
        if not all_verified:
            print()
            print(red(bold("POST-CONDITION FAILURES DETECTED. ROLLING BACK.")))
            for original_path, backup_path in backups_made:
                shutil.copy2(backup_path, original_path)
                print(yellow(f"  Restored: {original_path} from {backup_path}"))
            return 2
        
        print()
        print(green(bold("Phase 4 complete: all changes verified.")))
        print()
        
        # ----------------------------------------------------------------
        # PHASE 5: Summary
        # ----------------------------------------------------------------
        print(bold("=" * 70))
        print(green(bold("FIX A APPLIED SUCCESSFULLY")))
        print(bold("=" * 70))
        print()
        print("Backups created:")
        for original_path, backup_path in backups_made:
            print(f"  {backup_path}")
        print()
        print("To roll back manually:")
        for original_path, backup_path in backups_made:
            print(f"  cp {backup_path} {original_path}")
        print()
        print(bold("Next steps:"))
        print("  1. Rebuild container: docker compose build --no-cache mettaclaw")
        print("  2. Start container and observe 8-10 idle cycles for clean iteration")
        print("  3. Provoke with a long Berton message containing dense reasoning")
        print("  4. Confirm calcification does not appear")
        print("  5. If verification passes, document Fix A as successful in Sprint 4 doc")
        print()
        return 0
    
    except Exception as e:
        print(red(f"\nUNEXPECTED ERROR: {e}"))
        print(red("Attempting rollback of any backups made..."))
        for original_path, backup_path in backups_made:
            try:
                shutil.copy2(backup_path, original_path)
                print(yellow(f"  Restored: {original_path}"))
            except Exception as rollback_err:
                print(red(f"  ROLLBACK FAILED for {original_path}: {rollback_err}"))
                print(red(f"  Manual restore required from: {backup_path}"))
        return 3


if __name__ == '__main__':
    sys.exit(main())