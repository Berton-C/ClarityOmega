#!/usr/bin/env python3
"""
Apply script: F11 fix for single-command bare-form output errors.

Problem
-------
Clarity's output sometimes comes as bare single-command form (send "x")
instead of properly wrapped ((send "x")). When this hits loop.metta line
127's (collapse (let $s (superpose $sexpr) ...)), superpose iterates the
bare command's elements rather than treating it as one command, triggering
SINGLE_COMMAND_FORMAT_ERROR_NOTHING_WAS_DONE_PLEASE_FIX_AND_RETRY.

A second issue: Clarity sometimes emits multi-word arguments unquoted,
e.g. (query recent memories about myself) instead of (query "recent
memories about myself"). This is partially because the Sprint 1.5
consolidation (commit 8a2ea97 on May 4) dropped the arg-quoting
instruction during elevation of OUTPUT_FORMAT into substrate.

Defense-in-depth fix per Clarity's architectural review (May 13):
- Option 3 (prompt) as structural fix: restore arg-quoting instruction
  and add N=1 wrapping clarification, anchored to Patrick's original
  visual nested structure
- Option 2 (Python helper) as safety net: wrap_if_bare_command catches
  residual bare-form responses before sread parses them

The three edits
---------------
1. soul/behavioral_guidance.metta
   Replace the body of (= (output-format-guidance) ...) with a
   Patrick-anchored revision that:
   - Restores the multi-slot visual showing outer-list structure
   - Preserves May 2 anti-calcification ("as many commands as work requires")
   - Adds explicit N=1 clarification
   - Restores arg-quoting instruction (dropped in Sprint 1.5)
   - Restores variables-forbidden instruction (dropped in Sprint 1.5)
   - Preserves May 2 anti-anxiety reframe ("Verify... before emitting")

2. src/helper.py
   Add wrap_if_bare_command(s) function after sanitize_response.
   Strict detection: only wraps when first token after opening paren is
   in the known-skills registry. Idempotent. Returns input unchanged if
   not a bare single command.

3. src/loop.metta line 111
   Wire wrap_if_bare_command into the response pipeline as the outermost
   py-call wrapper, executing after sanitize_response.

Reversibility
-------------
--apply writes all three edits in one operation.
--reverse undoes all three.
Backups at .bak.f11_fix suffix.

Behavioral verification (post-apply, pre-commit)
-------------------------------------------------
Tests defined ahead of time:
- Test 1: Single-command response wraps to ((cmd args)) form natively
- Test 2: Multi-word string arg is properly quoted
- Test 3: Multi-command response wraps correctly
- Test 4: Normal conversation handles without regression
- Test 5: Idle cycle responses wrap correctly

Commit only after behavioral tests pass over observation period.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# ============================================================================
# FILE PATHS
# ============================================================================

BEHAVIORAL_GUIDANCE_PATH = Path("soul/behavioral_guidance.metta")
BEHAVIORAL_GUIDANCE_BAK = Path("soul/behavioral_guidance.metta.bak.f11_fix")

HELPER_PATH = Path("src/helper.py")
HELPER_BAK = Path("src/helper.py.bak.f11_fix")

LOOP_PATH = Path("src/loop.metta")
LOOP_BAK = Path("src/loop.metta.bak.f11_fix")


# ============================================================================
# EDIT 1: soul/behavioral_guidance.metta
# ============================================================================

# Current body of output-format-guidance (Sprint 1.5 result from May 4)
BG_ANCHOR = '''(= (output-format-guidance)
   "OUTPUT_FORMAT: Output an S-expression of the form (cmd1 cmd2 ... cmdN) where each cmd is (skillName arg1 arg2 ...). Use as many commands as the work requires. Verify balanced parentheses and quotes before emitting.")'''

# Patrick-anchored revision: 80% his original wording, 20% targeted additions.
# Additions: N-slot abstraction (May 2 anti-calcification), explicit N=1
# clarification (F11 fix), multi-word quoting parenthetical (F13 fix).
# Patrick's exact wording preserved for: arg quoting instruction, variables
# forbidden. May 2 refinement preserved: "as many commands as work requires,"
# "Verify... before emitting" anti-anxiety reframe.
BG_NEW = '''(= (output-format-guidance)
   "OUTPUT_FORMAT: Output a ((skillName1 args1) (skillName2 args2) ... (skillNameN argsN)) S-expression with as many commands as the work requires. For a single command: ((skillName args)) not (skillName args). Each arg is an explicit string hence needs quotes (multi-word strings must be one quoted string), and variables are forbidden! Verify balanced parentheses and quotes before emitting.")'''


# ============================================================================
# EDIT 2: src/helper.py
# ============================================================================

# Anchor: end of sanitize_response function (line 150 in current file).
# We insert wrap_if_bare_command BEFORE the "# --- Soul Evaluation Prompts"
# comment that separates response-pipeline functions from soul-eval functions.

HELPER_ANCHOR = '''def sanitize_response(s):
    """Strip non-ASCII characters from LLM response before PeTTa processes it.
    SWI-Prolog atom_string/2 cannot handle multi-byte UTF-8 characters.
    OmegaClaw's normalize_string handles UTF-8 encoding; this catches
    remaining non-ASCII that could crash atom_string/2."""
    return s.encode('ascii', errors='replace').decode('ascii')


# --- Soul Evaluation Prompts --------------------------------------'''

HELPER_NEW = '''def sanitize_response(s):
    """Strip non-ASCII characters from LLM response before PeTTa processes it.
    SWI-Prolog atom_string/2 cannot handle multi-byte UTF-8 characters.
    OmegaClaw's normalize_string handles UTF-8 encoding; this catches
    remaining non-ASCII that could crash atom_string/2."""
    return s.encode('ascii', errors='replace').decode('ascii')


def wrap_if_bare_command(s):
    """Safety net for F11: wrap bare single-command responses.

    Clarity's output should be ((cmd1) (cmd2) ... (cmdN)) per OUTPUT_FORMAT.
    Sometimes she emits (cmd args) instead, a bare single command without
    the outer list wrapper. When this hits loop.metta line 127's
    (collapse (let $s (superpose $sexpr) ...)), superpose iterates the
    bare command's elements rather than treating it as one command,
    triggering SINGLE_COMMAND_FORMAT_ERROR_NOTHING_WAS_DONE_PLEASE_FIX_AND_RETRY.

    Strict detection: only wraps when the first token after the opening
    paren is in the known-skills registry. Idempotent: if input already
    starts with double-parens, returns unchanged. Returns the input
    unchanged when not a bare single command.

    This is the safety net layer; the structural fix is in
    soul/behavioral_guidance.metta which restored the arg-quoting and
    multi-slot visual structure per Patrick's original design intent.
    """
    if not s or len(s) < 3:
        return s

    stripped = s.strip()
    if not stripped.startswith("("):
        return s

    # Already-wrapped form starts with "((" -- no action needed
    if stripped.startswith("(("):
        return s

    # Known skills registry (13 items, from prompt SKILLS section)
    known_skills = {
        "remember", "query", "episodes", "pin", "shell",
        "read-file", "write-file", "append-file", "send",
        "search", "tavily-search", "technical-analysis", "metta",
    }

    # Extract the first token after the opening paren
    rest = stripped[1:].lstrip()
    if not rest:
        return s

    # First token is up to whitespace, paren, or quote
    end = 0
    while end < len(rest) and rest[end] not in " \\t\\n\\r()\\"":
        end += 1
    first_token = rest[:end]

    if first_token not in known_skills:
        return s

    # It is a bare single command; wrap with outer parens
    return "(" + stripped + ")"


# --- Soul Evaluation Prompts --------------------------------------'''


# ============================================================================
# EDIT 3: src/loop.metta line 111 wiring
# ============================================================================

# Current line 111 pipeline:
LOOP_ANCHOR = '''                                       ($resp (py-call (helper.sanitize_response (py-call (helper.normalize_string (py-call (helper.balance_parentheses $respi)))))))'''

# Wrap with helper.wrap_if_bare_command as outermost py-call:
LOOP_NEW = '''                                       ($resp (py-call (helper.wrap_if_bare_command (py-call (helper.sanitize_response (py-call (helper.normalize_string (py-call (helper.balance_parentheses $respi)))))))))'''


# ============================================================================
# HELPERS
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


def find_target_substring_count(text: str, target: str) -> int:
    count = 0
    start = 0
    while True:
        idx = text.find(target, start)
        if idx == -1:
            break
        count += 1
        start = idx + 1
    return count


# ============================================================================
# SIMULATION
# ============================================================================

def simulate_bg_forward(content: str) -> str:
    if find_target_substring_count(content, BG_ANCHOR) != 1:
        raise RuntimeError("bg forward: BG_ANCHOR not found exactly once.")
    if "((skillName1 args1)" in content:
        raise RuntimeError("bg forward: new content marker already present; pre-state wrong.")
    return content.replace(BG_ANCHOR, BG_NEW, 1)


def simulate_bg_reverse(content: str) -> str:
    if find_target_substring_count(content, BG_NEW) != 1:
        raise RuntimeError("bg reverse: BG_NEW not found exactly once.")
    return content.replace(BG_NEW, BG_ANCHOR, 1)


def simulate_helper_forward(content: str) -> str:
    if find_target_substring_count(content, HELPER_ANCHOR) != 1:
        raise RuntimeError("helper forward: HELPER_ANCHOR not found exactly once.")
    if "def wrap_if_bare_command" in content:
        raise RuntimeError("helper forward: wrap_if_bare_command already in file; pre-state wrong.")
    return content.replace(HELPER_ANCHOR, HELPER_NEW, 1)


def simulate_helper_reverse(content: str) -> str:
    if find_target_substring_count(content, HELPER_NEW) != 1:
        raise RuntimeError("helper reverse: HELPER_NEW not found exactly once.")
    return content.replace(HELPER_NEW, HELPER_ANCHOR, 1)


def simulate_loop_forward(content: str) -> str:
    if find_target_substring_count(content, LOOP_ANCHOR) != 1:
        raise RuntimeError("loop forward: LOOP_ANCHOR not found exactly once.")
    if "helper.wrap_if_bare_command" in content:
        raise RuntimeError("loop forward: wrap_if_bare_command call already in loop; pre-state wrong.")
    return content.replace(LOOP_ANCHOR, LOOP_NEW, 1)


def simulate_loop_reverse(content: str) -> str:
    if find_target_substring_count(content, LOOP_NEW) != 1:
        raise RuntimeError("loop reverse: LOOP_NEW not found exactly once.")
    return content.replace(LOOP_NEW, LOOP_ANCHOR, 1)


# ============================================================================
# STATE CHECKS
# ============================================================================

def bg_forward_state_ok(content: str) -> tuple[bool, str]:
    has_anchor = find_target_substring_count(content, BG_ANCHOR) == 1
    no_new = "((skillName1 args1)" not in content
    ok = has_anchor and no_new
    return ok, f"anchor={has_anchor}, new_absent={no_new} -> {'OK' if ok else 'FAIL'}"


def bg_reverse_state_ok(content: str) -> tuple[bool, str]:
    has_new = find_target_substring_count(content, BG_NEW) == 1
    return has_new, f"new_block_present={has_new} -> {'OK' if has_new else 'FAIL'}"


def helper_forward_state_ok(content: str) -> tuple[bool, str]:
    has_anchor = find_target_substring_count(content, HELPER_ANCHOR) == 1
    no_new = "def wrap_if_bare_command" not in content
    ok = has_anchor and no_new
    return ok, f"anchor={has_anchor}, new_absent={no_new} -> {'OK' if ok else 'FAIL'}"


def helper_reverse_state_ok(content: str) -> tuple[bool, str]:
    has_new = find_target_substring_count(content, HELPER_NEW) == 1
    return has_new, f"new_block_present={has_new} -> {'OK' if has_new else 'FAIL'}"


def loop_forward_state_ok(content: str) -> tuple[bool, str]:
    has_anchor = find_target_substring_count(content, LOOP_ANCHOR) == 1
    no_new = "helper.wrap_if_bare_command" not in content
    ok = has_anchor and no_new
    return ok, f"anchor={has_anchor}, new_absent={no_new} -> {'OK' if ok else 'FAIL'}"


def loop_reverse_state_ok(content: str) -> tuple[bool, str]:
    has_new = find_target_substring_count(content, LOOP_NEW) == 1
    return has_new, f"new_block_present={has_new} -> {'OK' if has_new else 'FAIL'}"


# ============================================================================
# DIFF PREVIEW
# ============================================================================

def diff_preview(old: str, new: str, label: str, context: int = 2) -> str:
    old_lines = old.splitlines()
    new_lines = new.splitlines()

    differ_start = None
    for i in range(min(len(old_lines), len(new_lines))):
        if old_lines[i] != new_lines[i]:
            differ_start = i
            break
    if differ_start is None:
        if len(old_lines) == len(new_lines):
            return f"--- {label}: NO CHANGES ---"
        differ_start = min(len(old_lines), len(new_lines))

    differ_end_old = len(old_lines) - 1
    differ_end_new = len(new_lines) - 1
    while differ_end_old > differ_start and differ_end_new > differ_start:
        if old_lines[differ_end_old] == new_lines[differ_end_new]:
            differ_end_old -= 1
            differ_end_new -= 1
        else:
            break

    out = [f"--- {label} (lines {differ_start + 1} to {max(differ_end_old, differ_end_new) + 1}) ---"]
    start = max(0, differ_start - context)
    for i in range(start, differ_start):
        if i < len(old_lines):
            out.append(f"  {old_lines[i]}")
    for i in range(differ_start, differ_end_old + 1):
        if i < len(old_lines):
            out.append(f"- {old_lines[i]}")
    for i in range(differ_start, differ_end_new + 1):
        if i < len(new_lines):
            out.append(f"+ {new_lines[i]}")
    end_old = min(len(old_lines), differ_end_old + 1 + context)
    for i in range(differ_end_old + 1, end_old):
        out.append(f"  {old_lines[i]}")
    return "\n".join(out)


# ============================================================================
# FILE PROCESSING
# ============================================================================

def process_file(path, bak_path, sim_fwd, sim_rev, expected_line_delta_fwd,
                 args, label, forward_check, reverse_check,
                 check_parens=True):
    print(f"\n>>> {label} <<<")
    if not path.exists():
        print(f"  ERROR: {path} not found.")
        return False, "", ""
    content = path.read_text()
    pre_lines = len(content.splitlines())
    print(f"  Path: {path}")
    print(f"  Pre-edit lines: {pre_lines}")

    if check_parens:
        pre_o, pre_c = code_aware_paren_count(content)
        pre_d = pre_o - pre_c
        c_paren = "OK" if pre_d == 0 else "FAIL"
        print(f"  Pre-edit parens: opens={pre_o} closes={pre_c} delta={pre_d} ({c_paren})")
        # Note: loop.metta has known by-design +1 imbalance; we allow that
        if c_paren != "OK" and label != "src/loop.metta":
            print(f"  PAREN FAILED for {label}. Aborting.")
            return False, content, ""

    if args.reverse:
        ok, msg = reverse_check(content)
    else:
        ok, msg = forward_check(content)
    print(f"  State check: {msg}")
    if not ok:
        print(f"  STATE CHECK FAILED for {label}. Aborting.")
        return False, content, ""

    try:
        if args.reverse:
            simulated = sim_rev(content)
        else:
            simulated = sim_fwd(content)
    except RuntimeError as exc:
        print(f"  SIMULATION FAILED: {exc}")
        return False, content, ""

    post_lines = len(simulated.splitlines())
    line_delta = post_lines - pre_lines

    if check_parens:
        post_o, post_c = code_aware_paren_count(simulated)
        post_d = post_o - post_c
        # For loop.metta, accept the same delta we had before
        if label == "src/loop.metta":
            pre_d_expected = pre_d
            c_post_paren = "OK" if post_d == pre_d_expected else "FAIL"
            print(f"  Post-edit parens: opens={post_o} closes={post_c} delta={post_d} (expected {pre_d_expected}) ({c_post_paren})")
        else:
            c_post_paren = "OK" if post_d == 0 else "FAIL"
            print(f"  Post-edit parens: opens={post_o} closes={post_c} delta={post_d} ({c_post_paren})")
        if c_post_paren != "OK":
            print(f"  POST-EDIT PAREN FAILED for {label}. Aborting.")
            return False, content, simulated

    expected = expected_line_delta_fwd if not args.reverse else -expected_line_delta_fwd
    c_lines = "OK" if line_delta == expected else "FAIL"
    print(f"  Line delta: {line_delta} (expected {expected}) ({c_lines})")
    if c_lines != "OK":
        print(f"  LINE DELTA FAILED for {label}. Aborting.")
        return False, content, simulated

    return True, content, simulated


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="F11 fix: prompt restoration + Python safety net + loop wiring")
    parser.add_argument("--apply", action="store_true",
                        help="Write changes. Default is dry-run.")
    parser.add_argument("--reverse", action="store_true",
                        help="Reverse the edits.")
    args = parser.parse_args()

    direction = "REVERSE" if args.reverse else "APPLY"
    print(f"\n========== F11 FIX: {direction} ==========")

    # Compute line deltas
    bg_delta = BG_NEW.count("\n") - BG_ANCHOR.count("\n")
    helper_delta = HELPER_NEW.count("\n") - HELPER_ANCHOR.count("\n")
    loop_delta = LOOP_NEW.count("\n") - LOOP_ANCHOR.count("\n")  # 0 expected

    ok_bg, bg_orig, bg_sim = process_file(
        BEHAVIORAL_GUIDANCE_PATH, BEHAVIORAL_GUIDANCE_BAK,
        simulate_bg_forward, simulate_bg_reverse,
        bg_delta, args, "soul/behavioral_guidance.metta",
        bg_forward_state_ok, bg_reverse_state_ok,
        check_parens=True,
    )
    if not ok_bg:
        return 1

    ok_h, h_orig, h_sim = process_file(
        HELPER_PATH, HELPER_BAK,
        simulate_helper_forward, simulate_helper_reverse,
        helper_delta, args, "src/helper.py",
        helper_forward_state_ok, helper_reverse_state_ok,
        check_parens=False,  # Python file, paren-balance not meaningful
    )
    if not ok_h:
        return 1

    ok_l, l_orig, l_sim = process_file(
        LOOP_PATH, LOOP_BAK,
        simulate_loop_forward, simulate_loop_reverse,
        loop_delta, args, "src/loop.metta",
        loop_forward_state_ok, loop_reverse_state_ok,
        check_parens=True,  # Has known by-design imbalance; handled in process_file
    )
    if not ok_l:
        return 1

    print("\n========== DIFF PREVIEWS ==========")
    print(diff_preview(bg_orig, bg_sim, "soul/behavioral_guidance.metta", context=2))
    print()
    print(diff_preview(h_orig, h_sim, "src/helper.py", context=2))
    print()
    print(diff_preview(l_orig, l_sim, "src/loop.metta", context=2))

    if not args.apply:
        print("\n========== DRY-RUN COMPLETE ==========")
        print("All checks pass. Re-run with --apply to write.")
        return 0

    if not args.reverse:
        for path, bak in [(BEHAVIORAL_GUIDANCE_PATH, BEHAVIORAL_GUIDANCE_BAK),
                          (HELPER_PATH, HELPER_BAK),
                          (LOOP_PATH, LOOP_BAK)]:
            if bak.exists():
                print(f"WARNING: backup {bak} exists; overwriting.")
            bak.write_text(path.read_text())
            print(f"Backup written: {bak}")

    print("\n========== WRITING ==========")
    BEHAVIORAL_GUIDANCE_PATH.write_text(bg_sim)
    print(f"Wrote: {BEHAVIORAL_GUIDANCE_PATH}")
    HELPER_PATH.write_text(h_sim)
    print(f"Wrote: {HELPER_PATH}")
    LOOP_PATH.write_text(l_sim)
    print(f"Wrote: {LOOP_PATH}")

    print("\n========== DISK VERIFICATION ==========")
    for path, fwd_check, rev_check, label, do_paren in [
        (BEHAVIORAL_GUIDANCE_PATH, bg_forward_state_ok, bg_reverse_state_ok, "soul/behavioral_guidance.metta", True),
        (HELPER_PATH, helper_forward_state_ok, helper_reverse_state_ok, "src/helper.py", False),
        (LOOP_PATH, loop_forward_state_ok, loop_reverse_state_ok, "src/loop.metta", True),
    ]:
        disk = path.read_text()
        if do_paren:
            o, c = code_aware_paren_count(disk)
            d = o - c
            print(f"  {label} parens: opens={o} closes={c} delta={d}")
        if args.reverse:
            ok, msg = fwd_check(disk)
        else:
            ok, msg = rev_check(disk)
        print(f"  {label} state: {msg}")
        if not ok:
            print("DISK VERIFICATION FAILED.")
            return 1

    print("\n========== F11 FIX COMPLETE ==========")
    if not args.reverse:
        print("\nNext: container rebuild and behavioral tests.")
        print("  docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw && sleep 15 && docker logs clarity_omega 2>&1 | tail -50")
        print("\nThen run behavioral tests 1-5:")
        print("  Test 1: Send 'Please send me a one-line acknowledgement.'")
        print("  Test 2: Send 'Query your memory for recent decisions about substrate work.'")
        print("  Test 3: Send 'Please pin a note about today's plan, then send me a one-line summary.'")
        print("  Test 4: Normal conversation question")
        print("  Test 5: Observe idle cycles")
        print("\nObserve for a few hours. If clean, commit. If issues, --reverse.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
