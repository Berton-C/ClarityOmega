#!/usr/bin/env python3
"""
Apply script: Step 4 -- Add TASK-STATE block to prompt.

Per task-state-primitive_design.md Section 9 and Step 4 implementation order
(line 634): "Prompt assembly includes the block per Section 9, near
recent-action retriever. Clarity sees her own state. No behavior change
from consumers yet, but Clarity has visibility."

This is pure visibility wiring. No consumer migrations, no behavior change
intended. Step 5+ handle consumer migrations.

Design constraints honored:
- Mechanical template from atom values (Clarity confirmed 2026-05-14)
- "Report state, not request assessment" (spec line 592)
- Atoms read fresh at prompt assembly time, no caching (spec line 575)
- Atom-name predicates as reasoning hooks, not vague boolean checks
  (Clarity's principle preserved by structural shape: atoms ARE the predicates)
- Position: between YOUR_LAST_ACTION and LAST_SKILL_USE_RESULTS (spec line 534)

PeTTa constraint C1: py-str hangs inside MeTTa function definitions.
String assembly therefore lives in Python helpers (task_state_block_format,
join_threads_text). MeTTa task-state-block reads atoms via pure read
helpers, passes values to Python for text composition.

Three coordinated edits
-----------------------
1. soul/task_state.metta -- append three pure read functions:
   - current-anchors-for-phase
   - format-pending-threads
   - task-state-block

2. src/helper.py -- insert two text-composition helpers BEFORE the
   "# --- Soul Evaluation Prompts" section header:
   - join_threads_text
   - task_state_block_format

3. src/loop.metta -- insert TASK-STATE line in getContext between
   YOUR_LAST_ACTION and LAST_SKILL_USE_RESULTS.

Reversibility
-------------
--apply writes all three edits with .bak.step4 backups.
--reverse --apply undoes all three.
Plain run is dry-run with state checks.

Behavioral verification (post-apply, pre-commit)
-------------------------------------------------
- S4-1: container rebuild parse-clean
- S4-2: CHARS_SENT contains TASK-STATE block in correct position
- S4-3: atom freshness verified by sending message and watching
  cycles-since-input update in next cycle
- S4-4 (observation only): whether Clarity voluntarily uses task-state
  in her reasoning. Step 5/6 work, not Step 4 pass/fail.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


# ============================================================================
# FILE PATHS
# ============================================================================

TASK_STATE_PATH = Path("soul/task_state.metta")
TASK_STATE_BAK = Path("soul/task_state.metta.bak.step4")

HELPER_PATH = Path("src/helper.py")
HELPER_BAK = Path("src/helper.py.bak.step4")

LOOP_PATH = Path("src/loop.metta")
LOOP_BAK = Path("src/loop.metta.bak.step4")


# ============================================================================
# EDIT 1: soul/task_state.metta -- append three functions
# ============================================================================

# Anchor: the final function in the current file (count-pending-threads body)
# We append after this anchor, before the final closing.
TS_ANCHOR = '''(= (count-pending-threads)
   (let $all (collapse (match &self (pending-thread $topic $ts) ($topic $ts)))
      (count-pending-list $all)))'''

# Append the three new functions after the anchor. Note: the file may or may
# not end with a trailing newline; we handle both cases by checking what's
# already there.
TS_NEW = '''(= (count-pending-threads)
   (let $all (collapse (match &self (pending-thread $topic $ts) ($topic $ts)))
      (count-pending-list $all)))

;; ================================================================
;; SECTION 4: PROMPT-BLOCK READ HELPERS (Step 4)
;; Pure read helpers that compose the TASK-STATE prompt block per
;; spec Section 9. Text assembly happens in Python helpers
;; (helper.task_state_block_format, helper.join_threads_text) per
;; PeTTa constraint C1: py-str hangs inside MeTTa function definitions.
;; ================================================================

;; (current-anchors-for-phase $phase)
;;   Returns all (task-phase-anchor $phase $value $ts $reason) atoms whose
;;   $phase matches. Returns () if no anchor atoms exist for this phase.
;;   Pure collapse-then-branch pattern, C12-safe.
(= (current-anchors-for-phase $phase)
   (collapse (match &self (task-phase-anchor $phase $value $ts $reason)
                          (task-phase-anchor $phase $value $ts $reason))))

;; (format-pending-threads)
;;   Returns comma-separated text of current pending thread topics,
;;   or the literal string "none" if no pending threads exist.
;;   Python helper join_threads_text handles the text composition.
(= (format-pending-threads)
   (let $threads (collapse (current-pending-threads))
      (py-call (helper.join_threads_text $threads))))

;; (task-state-block)
;;   Composes the full TASK-STATE prompt block per spec Section 9.
;;   Format (when no anchor for current phase):
;;     TASK-STATE:
;;     (task-phase $phase) (cycles-since-input $n) (last-activity $t)
;;     Pending threads: $threads_text
;;     Summary: Task phase: $phase. $n cycles since last input. Pending threads: $threads_text.
;;
;;   Format (when anchor present):
;;     TASK-STATE:
;;     (task-phase $phase) (task-phase-anchor ...) (cycles-since-input $n) (last-activity $t)
;;     Pending threads: $threads_text
;;     Summary: Task phase: $phase. $n cycles since last input. Pending threads: $threads_text.
;;
;;   Mechanical template, zero interpretation, reports state not assessment
;;   (spec line 592, Clarity confirmed 2026-05-14).
;;   All atom reads happen fresh at prompt assembly time, no caching.
(= (task-state-block)
   (let* (($phase (current-phase))
          ($anchors (current-anchors-for-phase $phase))
          ($cycles (current-cycles-since-input))
          ($activity (current-last-activity))
          ($threads-text (format-pending-threads)))
      (py-call (helper.task_state_block_format $phase $anchors $cycles $activity $threads-text))))'''


# ============================================================================
# EDIT 2: src/helper.py -- insert two text-composition helpers
# ============================================================================

# Anchor on the Soul Evaluation Prompts section header. This is stable across
# pre-F11 and post-F11 versions of the file. New Step 4 functions land
# immediately before this header.
HELPER_ANCHOR = '''# --- Soul Evaluation Prompts --------------------------------------'''

HELPER_NEW = '''def join_threads_text(threads_list):
    """Step 4: format pending-thread topics as comma-separated text.

    Returns "none" if the list is empty, otherwise a comma-separated
    string of topic names. Used by (format-pending-threads) in
    soul/task_state.metta.

    PeTTa lists arrive as Python list/tuple objects when passed via py-call.
    Each element is a topic atom; we use str() to surface its symbolic form.
    """
    if not threads_list:
        return "none"
    return ", ".join(str(t) for t in threads_list)


def task_state_block_format(phase, anchors, cycles, activity, threads_text):
    """Step 4: compose the full TASK-STATE prompt block.

    Format per task-state-primitive_design.md Section 9:

        TASK-STATE:
        (task-phase $phase) [anchor atoms if present] (cycles-since-input $n) (last-activity $t)
        Pending threads: $threads_text
        Summary: Task phase: $phase. $cycles cycles since last input. Pending threads: $threads_text.

    Anchor atoms (when present for the current phase) appear inline on the
    atoms line between the phase atom and cycles-since-input.

    Per Clarity's design constraint (May 14 confirmed): mechanical template
    from atom values, zero interpretation, reports state not assessment.
    """
    # Anchor atoms inline (empty when no anchors for current phase)
    if anchors:
        anchor_text = " " + " ".join(str(a) for a in anchors)
    else:
        anchor_text = ""

    atoms_line = (
        f"(task-phase {phase}){anchor_text} "
        f"(cycles-since-input {cycles}) (last-activity {activity})"
    )

    summary = (
        f"Task phase: {phase}. {cycles} cycles since last input. "
        f"Pending threads: {threads_text}."
    )

    return (
        f"TASK-STATE:\\n"
        f"{atoms_line}\\n"
        f"Pending threads: {threads_text}\\n"
        f"Summary: {summary}"
    )


# --- Soul Evaluation Prompts --------------------------------------'''


# ============================================================================
# EDIT 3: src/loop.metta -- insert TASK-STATE line in getContext
# ============================================================================

# Anchor on the exact text that includes YOUR_LAST_ACTION line plus the
# transition into LAST_SKILL_USE_RESULTS. This is the insertion seam.
LOOP_ANCHOR = '''" YOUR_LAST_ACTION: " (your-last-action-block $k)
                         " LAST_SKILL_USE_RESULTS: "'''

LOOP_NEW = '''" YOUR_LAST_ACTION: " (your-last-action-block $k)
                         " " (task-state-block)
                         " LAST_SKILL_USE_RESULTS: "'''


# ============================================================================
# HELPERS
# ============================================================================

def code_aware_paren_count(text):
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


def find_target_substring_count(text, target):
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

def simulate_ts_forward(content):
    if find_target_substring_count(content, TS_ANCHOR) != 1:
        raise RuntimeError("task_state forward: TS_ANCHOR not found exactly once.")
    if "(task-state-block)" in content:
        raise RuntimeError("task_state forward: task-state-block already in file; pre-state wrong.")
    return content.replace(TS_ANCHOR, TS_NEW, 1)


def simulate_ts_reverse(content):
    if find_target_substring_count(content, TS_NEW) != 1:
        raise RuntimeError("task_state reverse: TS_NEW not found exactly once.")
    return content.replace(TS_NEW, TS_ANCHOR, 1)


def simulate_helper_forward(content):
    if find_target_substring_count(content, HELPER_ANCHOR) != 1:
        raise RuntimeError("helper forward: HELPER_ANCHOR not found exactly once.")
    if "def task_state_block_format" in content:
        raise RuntimeError("helper forward: task_state_block_format already in file; pre-state wrong.")
    return content.replace(HELPER_ANCHOR, HELPER_NEW, 1)


def simulate_helper_reverse(content):
    if find_target_substring_count(content, HELPER_NEW) != 1:
        raise RuntimeError("helper reverse: HELPER_NEW not found exactly once.")
    return content.replace(HELPER_NEW, HELPER_ANCHOR, 1)


def simulate_loop_forward(content):
    if find_target_substring_count(content, LOOP_ANCHOR) != 1:
        raise RuntimeError("loop forward: LOOP_ANCHOR not found exactly once.")
    if "(task-state-block)" in content:
        raise RuntimeError("loop forward: task-state-block call already in loop; pre-state wrong.")
    return content.replace(LOOP_ANCHOR, LOOP_NEW, 1)


def simulate_loop_reverse(content):
    if find_target_substring_count(content, LOOP_NEW) != 1:
        raise RuntimeError("loop reverse: LOOP_NEW not found exactly once.")
    return content.replace(LOOP_NEW, LOOP_ANCHOR, 1)


# ============================================================================
# STATE CHECKS
# ============================================================================

def ts_forward_state_ok(content):
    has_anchor = find_target_substring_count(content, TS_ANCHOR) == 1
    no_new = "(task-state-block)" not in content
    ok = has_anchor and no_new
    return ok, f"anchor={has_anchor}, new_absent={no_new} -> {'OK' if ok else 'FAIL'}"


def ts_reverse_state_ok(content):
    has_new = find_target_substring_count(content, TS_NEW) == 1
    return has_new, f"new_block_present={has_new} -> {'OK' if has_new else 'FAIL'}"


def helper_forward_state_ok(content):
    has_anchor = find_target_substring_count(content, HELPER_ANCHOR) == 1
    no_new = "def task_state_block_format" not in content
    ok = has_anchor and no_new
    return ok, f"anchor={has_anchor}, new_absent={no_new} -> {'OK' if ok else 'FAIL'}"


def helper_reverse_state_ok(content):
    has_new = find_target_substring_count(content, HELPER_NEW) == 1
    return has_new, f"new_block_present={has_new} -> {'OK' if has_new else 'FAIL'}"


def loop_forward_state_ok(content):
    has_anchor = find_target_substring_count(content, LOOP_ANCHOR) == 1
    no_new = "(task-state-block)" not in content
    ok = has_anchor and no_new
    return ok, f"anchor={has_anchor}, new_absent={no_new} -> {'OK' if ok else 'FAIL'}"


def loop_reverse_state_ok(content):
    has_new = find_target_substring_count(content, LOOP_NEW) == 1
    return has_new, f"new_block_present={has_new} -> {'OK' if has_new else 'FAIL'}"


# ============================================================================
# DIFF PREVIEW
# ============================================================================

def diff_preview(old, new, label, context=2):
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
                 check_parens=True, paren_imbalance_expected=0):
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
        c_paren = "OK" if pre_d == paren_imbalance_expected else "FAIL"
        print(f"  Pre-edit parens: opens={pre_o} closes={pre_c} delta={pre_d} (expected {paren_imbalance_expected}) ({c_paren})")
        if c_paren != "OK":
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
        c_post_paren = "OK" if post_d == paren_imbalance_expected else "FAIL"
        print(f"  Post-edit parens: opens={post_o} closes={post_c} delta={post_d} (expected {paren_imbalance_expected}) ({c_post_paren})")
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
    parser = argparse.ArgumentParser(description="Step 4: TASK-STATE prompt block")
    parser.add_argument("--apply", action="store_true",
                        help="Write changes. Default is dry-run.")
    parser.add_argument("--reverse", action="store_true",
                        help="Reverse the edits.")
    args = parser.parse_args()

    direction = "REVERSE" if args.reverse else "APPLY"
    print(f"\n========== STEP 4 TASK-STATE BLOCK: {direction} ==========")

    # Compute line deltas
    ts_delta = TS_NEW.count("\n") - TS_ANCHOR.count("\n")
    helper_delta = HELPER_NEW.count("\n") - HELPER_ANCHOR.count("\n")
    loop_delta = LOOP_NEW.count("\n") - LOOP_ANCHOR.count("\n")

    ok_ts, ts_orig, ts_sim = process_file(
        TASK_STATE_PATH, TASK_STATE_BAK,
        simulate_ts_forward, simulate_ts_reverse,
        ts_delta, args, "soul/task_state.metta",
        ts_forward_state_ok, ts_reverse_state_ok,
        check_parens=True, paren_imbalance_expected=0,
    )
    if not ok_ts:
        return 1

    ok_h, h_orig, h_sim = process_file(
        HELPER_PATH, HELPER_BAK,
        simulate_helper_forward, simulate_helper_reverse,
        helper_delta, args, "src/helper.py",
        helper_forward_state_ok, helper_reverse_state_ok,
        check_parens=False,  # Python file
    )
    if not ok_h:
        return 1

    # loop.metta has a known by-design paren imbalance (HandleError pattern).
    # We don't hardcode the value; we read pre-state and accept the same delta post-edit.
    print("\n>>> src/loop.metta <<<")
    if not LOOP_PATH.exists():
        print(f"  ERROR: {LOOP_PATH} not found.")
        return 1
    loop_content = LOOP_PATH.read_text()
    loop_pre_lines = len(loop_content.splitlines())
    print(f"  Path: {LOOP_PATH}")
    print(f"  Pre-edit lines: {loop_pre_lines}")

    loop_pre_o, loop_pre_c = code_aware_paren_count(loop_content)
    loop_pre_d = loop_pre_o - loop_pre_c
    print(f"  Pre-edit parens: opens={loop_pre_o} closes={loop_pre_c} delta={loop_pre_d} (file's by-design baseline)")

    if args.reverse:
        ok_l_state, msg_l = loop_reverse_state_ok(loop_content)
    else:
        ok_l_state, msg_l = loop_forward_state_ok(loop_content)
    print(f"  State check: {msg_l}")
    if not ok_l_state:
        print(f"  STATE CHECK FAILED for src/loop.metta. Aborting.")
        return 1

    try:
        if args.reverse:
            loop_sim = simulate_loop_reverse(loop_content)
        else:
            loop_sim = simulate_loop_forward(loop_content)
    except RuntimeError as exc:
        print(f"  SIMULATION FAILED: {exc}")
        return 1

    loop_post_lines = len(loop_sim.splitlines())
    loop_line_delta = loop_post_lines - loop_pre_lines
    loop_expected = loop_delta if not args.reverse else -loop_delta

    loop_post_o, loop_post_c = code_aware_paren_count(loop_sim)
    loop_post_d = loop_post_o - loop_post_c
    paren_delta_change = loop_post_d - loop_pre_d
    print(f"  Post-edit parens: opens={loop_post_o} closes={loop_post_c} delta={loop_post_d} (change={paren_delta_change:+d}, expected 0)")

    if paren_delta_change != 0:
        print(f"  POST-EDIT PAREN BALANCE CHANGED for src/loop.metta. Aborting.")
        return 1

    c_loop_lines = "OK" if loop_line_delta == loop_expected else "FAIL"
    print(f"  Line delta: {loop_line_delta} (expected {loop_expected}) ({c_loop_lines})")
    if c_loop_lines != "OK":
        print(f"  LINE DELTA FAILED for src/loop.metta. Aborting.")
        return 1

    print("\n========== DIFF PREVIEWS ==========")
    print(diff_preview(ts_orig, ts_sim, "soul/task_state.metta", context=2))
    print()
    print(diff_preview(h_orig, h_sim, "src/helper.py", context=2))
    print()
    print(diff_preview(loop_content, loop_sim, "src/loop.metta", context=2))

    if not args.apply:
        print("\n========== DRY-RUN COMPLETE ==========")
        print("All checks pass. Re-run with --apply to write.")
        return 0

    if not args.reverse:
        for path, bak in [(TASK_STATE_PATH, TASK_STATE_BAK),
                          (HELPER_PATH, HELPER_BAK),
                          (LOOP_PATH, LOOP_BAK)]:
            if bak.exists():
                print(f"WARNING: backup {bak} exists; overwriting.")
            bak.write_text(path.read_text())
            print(f"Backup written: {bak}")

    print("\n========== WRITING ==========")
    TASK_STATE_PATH.write_text(ts_sim)
    print(f"Wrote: {TASK_STATE_PATH}")
    HELPER_PATH.write_text(h_sim)
    print(f"Wrote: {HELPER_PATH}")
    LOOP_PATH.write_text(loop_sim)
    print(f"Wrote: {LOOP_PATH}")

    print("\n========== DISK VERIFICATION ==========")
    for path, fwd_check, rev_check, label, do_paren, expected_imbalance in [
        (TASK_STATE_PATH, ts_forward_state_ok, ts_reverse_state_ok, "soul/task_state.metta", True, 0),
        (HELPER_PATH, helper_forward_state_ok, helper_reverse_state_ok, "src/helper.py", False, 0),
        (LOOP_PATH, loop_forward_state_ok, loop_reverse_state_ok, "src/loop.metta", True, loop_pre_d),
    ]:
        disk = path.read_text()
        if do_paren:
            o, c = code_aware_paren_count(disk)
            d = o - c
            print(f"  {label} parens: opens={o} closes={c} delta={d} (expected {expected_imbalance})")
        if args.reverse:
            ok, msg = fwd_check(disk)
        else:
            ok, msg = rev_check(disk)
        print(f"  {label} state: {msg}")
        if not ok:
            print("DISK VERIFICATION FAILED.")
            return 1

    print("\n========== STEP 4 COMPLETE ==========")
    if not args.reverse:
        print("\nNext: container rebuild and behavioral tests.")
        print("  docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw && sleep 15 && docker logs clarity_omega 2>&1 | tail -50")
        print("\nThen run behavioral tests S4-1 through S4-3:")
        print("  S4-1: Verify no parse errors on the 3 modified files")
        print("  S4-2: Send any message; verify TASK-STATE block appears in CHARS_SENT in correct position")
        print("  S4-3: Send a message; verify cycles-since-input resets to 0 in next cycle's TASK-STATE block")
        print("  S4-4 (observation): Watch whether Clarity voluntarily references task-state in her reasoning")
        print("\nObserve for a few hours. If clean, commit. If issues, --reverse --apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
