#!/usr/bin/env python3
"""
soul_patch_loop.py -- ClarityClaw soul intercept patcher for OmegaClaw loop.metta

Usage:
    python3 scripts/soul_patch_loop.py [--dry-run]

This script applies all soul intercepts (5a, 5b, 5c) to OmegaClaw's src/loop.metta.
It uses pattern matching (not line numbers) to find insertion points, so it works
across upstream updates as long as the anchor patterns remain recognizable.

Design principles:
    - Pattern-based: anchors on content, not line numbers
    - Idempotent: detects if already applied, skips gracefully
    - Loud failure: if an anchor is not found, prints exactly what it expected
    - One file: all loop.metta patches in one script
    - Preserves indentation: measures from surrounding context

Author: Berton Bennett / ClarityDAO
Target: OmegaClaw-Core (ASI Alliance) -- src/loop.metta
"""

import sys
import os
import re
import shutil
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

LOOP_FILE = "src/loop.metta"
BACKUP_SUFFIX = ".pre-soul-backup"
SOUL_MARKER = ";; CLARITYCLAW SOUL"  # idempotency check

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def backup_file(path):
    backup = path + BACKUP_SUFFIX
    if not os.path.exists(backup):
        shutil.copy2(path, backup)
        print(f"  Backup created: {backup}")
    else:
        print(f"  Backup already exists: {backup}")

def find_unique(content, pattern, label):
    """Find a pattern that must appear exactly once. Returns (start, end) or fails."""
    matches = list(re.finditer(re.escape(pattern), content))
    if len(matches) == 0:
        print(f"\n  FATAL: Anchor not found for [{label}]")
        print(f"  Expected to find: {repr(pattern[:100])}")
        print(f"  This means OmegaClaw's loop.metta has changed structure.")
        print(f"  Read the new loop.metta and update this script.")
        return None
    if len(matches) > 1:
        print(f"\n  FATAL: Anchor found {len(matches)} times for [{label}]")
        print(f"  Pattern: {repr(pattern[:100])}")
        print(f"  Expected exactly 1 match. loop.metta structure may have changed.")
        return None
    return matches[0].start(), matches[0].end()

def is_already_applied(content):
    return SOUL_MARKER in content

def get_indent(line):
    """Return the leading whitespace of a line."""
    return line[:len(line) - len(line.lstrip())]

# ---------------------------------------------------------------------------
# Patch 1: 5a -- Soul state variables in initLoop
# ---------------------------------------------------------------------------

def patch_5a_state_vars(content):
    """Add soul state variables to initLoop, before the closing line."""
    label = "5a-state-vars"

    # Anchor: the last line of initLoop before it closes
    anchor = '(change-state! &loops (maxNewInputLoops))))'
    loc = find_unique(content, anchor, label)
    if loc is None:
        return None

    # Find the line containing the anchor to get indentation
    line_start = content.rfind('\n', 0, loc[0]) + 1
    existing_line = content[line_start:loc[1]]
    indent = get_indent(existing_line)

    # Insert soul state variables BEFORE the closing line
    soul_vars = f"""
{indent};; CLARITYCLAW SOUL state variables (5a)
{indent}(change-state! &soul_verdict_in  "VERDICT: PROCEED")
{indent}(change-state! &soul_verdict_out "VERDICT: PROCEED")
{indent}(change-state! &person_state "PERSON-STATE: neutral ACTIVE-NEED: none SOUL-TONE: grounded")
{indent}(change-state! &task_context "TASK-STATUS: none TASK-ID: none CUMULATIVE-IRREVERSIBILITY: 0")
{indent}(change-state! &soul_mutation_lock "")
{indent}(change-state! &pending_soul_mutation "")
{indent}(change-state! &soul_ack_sent False)"""

    content = content[:line_start] + soul_vars + "\n" + content[line_start:]
    print(f"  [{label}] Applied: 7 soul state variables added to initLoop")
    return content

# ---------------------------------------------------------------------------
# Patch 2: 5a -- initSoulSeeds and startup check in startup block
# ---------------------------------------------------------------------------

def patch_5a_startup(content):
    """Add initSoulSeeds and soul-rationality-startup-check between initMemory and initChannels."""
    label = "5a-startup"

    # Anchor: initMemory followed by initChannels in the startup progn
    # We insert between these two
    anchor = "(initMemory)\n"
    # Find initMemory in the startup block context
    # Look for the pattern: (initMemory) followed eventually by (initChannels)
    init_memory_pattern = "(initMemory)"
    init_channels_pattern = "(initChannels)"

    mem_loc = find_unique(content, init_memory_pattern, label + "-initMemory")
    if mem_loc is None:
        return None

    chan_loc = find_unique(content, init_channels_pattern, label + "-initChannels")
    if chan_loc is None:
        return None

    # Get indentation from the initMemory line
    line_start = content.rfind('\n', 0, mem_loc[0]) + 1
    existing_line = content[line_start:mem_loc[1]]
    indent = get_indent(existing_line)

    # Insert after initMemory, before initChannels
    insertion = f"""
{indent}(initSoulSeeds)              ;; CLARITYCLAW SOUL: seed soul memory once at startup
{indent}(soul-rationality-startup-check)  ;; CLARITYCLAW SOUL: structural health check"""

    # Insert right after the initMemory line ends
    insert_pos = content.find('\n', mem_loc[1]) + 1
    content = content[:insert_pos] + insertion + "\n" + content[insert_pos:]
    print(f"  [{label}] Applied: initSoulSeeds and soul-rationality-startup-check added to startup")
    return content

# ---------------------------------------------------------------------------
# Patch 3: 5b -- normalize_string after balance_parentheses
# ---------------------------------------------------------------------------

def patch_5b_normalize(content):
    """Wrap balance_parentheses result in normalize_string."""
    label = "5b-normalize"

    anchor = '($resp (py-call (helper.balance_parentheses $respi)))'
    loc = find_unique(content, anchor, label)
    if loc is None:
        return None

    replacement = '($resp (py-call (helper.normalize_string (py-call (helper.balance_parentheses $respi)))))'

    content = content[:loc[0]] + replacement + content[loc[1]:]
    print(f"  [{label}] Applied: normalize_string wrapping balance_parentheses")
    return content

# ---------------------------------------------------------------------------
# Patch 4: 5b -- Input intercept (replace $send assembly)
# ---------------------------------------------------------------------------

def patch_5b_input_intercept(content):
    """Replace the simple $send assembly with soul-enriched version."""
    label = "5b-input-intercept"

    # Anchor: the original $send line
    anchor = '($send (py-str ($prompt $lastmessage)))'
    loc = find_unique(content, anchor, label)
    if loc is None:
        return None

    # Get indentation from the anchor line
    line_start = content.rfind('\n', 0, loc[0]) + 1
    existing_line = content[line_start:loc[1]]
    indent = get_indent(existing_line)

    # The soul input intercept replaces the simple $send with:
    # - soul-pre-compute (native, no LLM)
    # - Channel A: person state (LLM call via soul-llm-call)
    # - Channel B+C: soul evaluation (LLM call via soul-llm-call)
    # - Calibration recording
    # - PAUSE routing (body of let*, genuine halt)
    # - FLAG and PROCEED: $send assembly with soul context
    replacement = f""";; CLARITYCLAW SOUL INPUT INTERCEPT (5b)
{indent}($soul_precompute (soul-pre-compute $msg))
{indent}($person_state (if (> (string_length $msgrcv) 0)
{indent}    (soul-llm-call (py-call (helper.soul_flourishing_prompt $msgrcv)))
{indent}    (get-state &person_state)))
{indent}($_ (change-state! &person_state $person_state))
{indent}($_ (println! (PERSON_STATE: $person_state)))
{indent}($soul_context_in (py-call (helper.soul_brief_tier_a_static)))
{indent}($soul_verdict_in (if (> (string_length $msgrcv) 0)
{indent}    (soul-llm-call (py-call (helper.soul_eval_prompt $soul_context_in $msgrcv $person_state)))
{indent}    (get-state &soul_verdict_in)))
{indent}($_ (change-state! &soul_verdict_in (py-call (helper.soul_verdict_sanitize $soul_verdict_in))))
{indent}($_ (println! (SOUL_VERDICT_IN: $soul_verdict_in)))
{indent}($_ (if (> (string_length $msgrcv) 0)
{indent}        (soul-calibration-record $soul_precompute $soul_verdict_in $msgrcv) _))
{indent}($_ (if (not (soul-proceed? $soul_verdict_in))
{indent}        (soul-note-record $soul_verdict_in "input" $msgrcv) _))
{indent}($_ (change-state! &soul_ack_sent False))
{indent}($send (py-call (helper.soul_send_assemble
{indent}                $prompt $soul_context_in $soul_verdict_in
{indent}                $person_state
{indent}                (soul-extract-flag-note $soul_verdict_in)
{indent}                $lastmessage)))"""

    content = content[:line_start] + replacement + "\n" + content[content.find('\n', loc[1]) + 1:]
    print(f"  [{label}] Applied: soul input intercept (Channel A, B+C, $send assembly)")
    return content

# ---------------------------------------------------------------------------
# Patch 5: 5c -- Output intercept (between RESPONSE println and $results)
# ---------------------------------------------------------------------------

def patch_5c_output_intercept(content):
    """Add output soul evaluation between RESPONSE println and $results binding."""
    label = "5c-output-intercept"

    # Anchor: the RESPONSE println line
    anchor = '($_ (println! (RESPONSE: $sexpr)))'
    loc = find_unique(content, anchor, label)
    if loc is None:
        return None

    # Get indentation
    line_start = content.rfind('\n', 0, loc[0]) + 1
    existing_line = content[line_start:loc[1]]
    indent = get_indent(existing_line)

    # Insert output intercept AFTER the RESPONSE println
    insertion = f"""
{indent};; CLARITYCLAW SOUL OUTPUT INTERCEPT (5c)
{indent}($soul_verdict_out "VERDICT: PROCEED SOUL-NOTE: output-intercept-pending-runtime-fix")
{indent}($_ (println! (SOUL_VERDICT_OUT: $soul_verdict_out)))
{indent}($metta_cmds (if (and (== "(" (first_char $resp)) (== (get-state &error) ()))
{indent}                (collapse (superpose $sexpr))
{indent}                ()))
{indent}($soul_mutation_flag
{indent}  (if (soul-any-metta? $metta_cmds)
{indent}      (let $args (collapse (let $c (superpose $metta_cmds)
{indent}                    (if (soul-is-metta-cmd? $c)
{indent}                        (soul-extract-metta-arg $c) ())))
{indent}           (if (any (collapse (let $a (superpose $args)
{indent}                       (soul-metta-targets-soul-namespace? $a))))
{indent}               (if (soul-mutation-pending?)
{indent}                   "SOUL-NAMESPACE-MUTATION-CONFLICT"
{indent}                   (progn
{indent}                     (change-state! &soul_mutation_lock
{indent}                       (py-call (helper.soul_mutation_lock_str (car-atom $args))))
{indent}                     "SOUL-NAMESPACE-MUTATION-PENDING"))
{indent}               ""))
{indent}      ""))
{indent}($_ (if (and (not (soul-proceed? $soul_verdict_out)) (== (get-state &error) ()))
{indent}        (soul-note-record $soul_verdict_out "output" $resp) _))"""

    insert_pos = content.find('\n', loc[1]) + 1
    content = content[:insert_pos] + insertion + "\n" + content[insert_pos:]
    print(f"  [{label}] Applied: soul output intercept (verdict, mutation gate, soul note)")
    return content

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    dry_run = "--dry-run" in sys.argv

    print("=" * 60)
    print("ClarityClaw Soul Patch -- loop.metta")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Target: {LOOP_FILE}")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print("=" * 60)

    if not os.path.exists(LOOP_FILE):
        print(f"\n  FATAL: {LOOP_FILE} not found.")
        print(f"  Run this script from the OmegaClaw repo root.")
        sys.exit(1)

    content = read_file(LOOP_FILE)

    # Idempotency check
    if is_already_applied(content):
        print(f"\n  Soul patches already detected in {LOOP_FILE}.")
        print(f"  To re-apply, restore from {LOOP_FILE}{BACKUP_SUFFIX} first.")
        print(f"  Skipping.")
        sys.exit(0)

    # Backup
    if not dry_run:
        backup_file(LOOP_FILE)

    # Apply patches in order (order matters -- earlier patches shift content)
    patches = [
        ("5a: State variables", patch_5a_state_vars),
        ("5a: Startup block", patch_5a_startup),
        ("5b: normalize_string wrapping", patch_5b_normalize),
        ("5b: Input intercept", patch_5b_input_intercept),
        ("5c: Output intercept", patch_5c_output_intercept),
    ]

    for name, patch_fn in patches:
        print(f"\n  Applying: {name}")
        result = patch_fn(content)
        if result is None:
            print(f"\n  ABORTED: Patch [{name}] failed. No changes written.")
            sys.exit(1)
        content = result

    if dry_run:
        print(f"\n  DRY RUN complete. No files modified.")
        print(f"\n  --- BEGIN PATCHED CONTENT ---")
        print(content)
        print(f"  --- END PATCHED CONTENT ---")
    else:
        write_file(LOOP_FILE, content)
        print(f"\n  All patches applied successfully to {LOOP_FILE}")
        print(f"  Backup at: {LOOP_FILE}{BACKUP_SUFFIX}")

    print(f"\n{'=' * 60}")
    print("Done.")

if __name__ == "__main__":
    main()
