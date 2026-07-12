#!/usr/bin/env python3
"""
Apply script: Step 4.5 -- idle_cycle_detector v1 (send-burst detection)

Per Plan A and Clarity's confirmed design (May 14, 2026), Step 4.5 wires
operational awareness organ #1: idle_cycle_detector. Detects send-burst
duplicate-engagement patterns by counting send-class actions in the
existing recent-action window.

Design (Clarity-confirmed):
- Detection rule: count send-class tags (responsive-send,
  status-send-unprompted) in current recent-action window (10 cycles)
- Threshold: 3
- Verdict atom: (idle-pattern $verdict $count) where $verdict is
  productive or stuck-duplicate-engagement
- Threshold name: (send-burst-threshold) -- renamed from existing
  (idle-cycle-threshold) per Clarity Q6
- v1 scope: send-burst only; mechanism 1 (content-repetition) deferred to v2
- Per-cycle freshness: detector clears prior atom and emits new each cycle
- Implementation: window-count, not since-last-input, per Clarity Q1
  confirmation. Stale-residue false-positive ~5 cycles is acceptable and
  self-healing per Clarity Q2.

Three coordinated edits:
1. soul/idle_cycle_detector.metta -- FULL REWRITE
   The existing 30-line candidate-proposal file gets replaced with the
   complete v1 detection function set:
   - (send-burst-threshold) atom
   - (is-send-action?) predicate
   - (count-send-list) recursive list counter
   - (count-sends-in-window) reads recent-action atoms
   - (current-idle-pattern) public read helper
   - (do-clear-idle-pattern!) clears prior atom for freshness
   - (do-update-idle-pattern!) cycle-level writer
   - (idle-pattern-block) prompt-block read helper

2. src/helper.py -- add idle_pattern_block_format Python helper
   Per C1 (py-str hangs inside MeTTa function definitions), text
   assembly lives in Python. This is hands-only: receives verdict and
   count, returns formatted block string. No reasoning, no decisions.

3. src/loop.metta -- two coordinated edits:
   3a: cycle-level invocation of (do-update-idle-pattern!) inserted
       after populate-recent-action at line 134
   3b: prompt-block insertion of " " (idle-pattern-block) in getContext
       AFTER (task-state-block) and BEFORE LAST_SKILL_USE_RESULTS

Reversibility:
- --apply writes changes with .bak.step4_5 backups
- --reverse --apply undoes all four edits

Behavioral tests:
- S4_5-1: container rebuild parse-clean
- S4_5-2: IDLE-PATTERN block visible in CHARS_SENT after TASK-STATE block
- S4_5-3: send burst triggers stuck-duplicate-engagement; window roll
  returns to productive
- S4_5-4 (observation): does Clarity voluntarily reference idle-pattern
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


# ============================================================================
# FILE PATHS
# ============================================================================

ICD_PATH = Path("soul/idle_cycle_detector.metta")
ICD_BAK = Path("soul/idle_cycle_detector.metta.bak.step4_5")

HELPER_PATH = Path("src/helper.py")
HELPER_BAK = Path("src/helper.py.bak.step4_5")

LOOP_PATH = Path("src/loop.metta")
LOOP_BAK = Path("src/loop.metta.bak.step4_5")


# ============================================================================
# EDIT 1: soul/idle_cycle_detector.metta -- FULL REWRITE
# ============================================================================

# The existing 30-line file is replaced entirely. The new file preserves
# the original header comments (purpose, motivation, candidate-id) and
# rebuilds the substrate per Clarity's Step 4.5 design.
#
# The anchor for full-file replacement is the entire existing content;
# the new content is the v1 detection function set.

ICD_ANCHOR = ''';; Candidate 002: idle-cycle-detector
;; Proposed 2026-04-25T17:24 by Clarity
;; Purpose: Detect when Clarity is idle-cycling on a blocked goal
;; and suggest productive alternative work instead of repeating
;; the same status check.
;;
;; Motivation: 15+ identical iterations observed on Goal 15 while
;; blocked on external input. This wastes cycles and demonstrates
;; a gap in self-regulation.

(= (candidate-id 002) idle-cycle-detector)
(= (candidate-status idle-cycle-detector) proposed)
(= (candidate-description idle-cycle-detector)
  "Detect idle cycling on blocked goals and redirect to productive alternatives")

;; === DETECTION RULE ===
;; If same pin text repeated 3+ times AND goal status is blocked:
;;   -> trigger idle-cycle-detected
(= (idle-cycle-threshold) 3)
(= (idle-cycle-action blocked-on-external)
  (alternatives
    (propose-new-candidate)
    (review-existing-artifacts-for-quality)
    (write-documentation)
    (run-soul-eval-audit)
    (consolidate-knowledge-into-atomspace)))

;; === TEST HOOK ===
(= (test-idle-cycle-detector)
  (idle-cycle-action blocked-on-external))'''

ICD_NEW = ''';; soul/idle_cycle_detector.metta
;; Idle-cycle detector v1: send-burst detection (Step 4.5)
;;
;; History:
;;   2026-04-25: Candidate 002 proposed by Clarity (mechanism 1:
;;     content-repetition detection, never wired)
;;   2026-05-14: v1 implementation per Plan A Step 4.5, design
;;     confirmed by Clarity. Mechanism 2 (send-burst) implemented;
;;     mechanism 1 (content-repetition) deferred to v2.
;;
;; v1 detection rule (Clarity-confirmed):
;;   Count send-class action tags (responsive-send, status-send-unprompted)
;;   in the current recent-action window (10 cycles, per
;;   recent_action_populator.metta). If count > send-burst-threshold,
;;   emit (idle-pattern stuck-duplicate-engagement $count); else emit
;;   (idle-pattern productive $count).
;;
;; Why window-count over since-last-input (Clarity Q1 May 14):
;;   Cleaner implementation. recent-action's built-in 10-cycle pruning
;;   acts as implicit time scope. Stale-residue false-positive ~5
;;   cycles, self-healing as window rolls. Acceptable per Clarity Q2.
;;
;; PeTTa constraints honored:
;;   - C12-safe (no match inside if; collapse-then-branch for guards)
;;   - ASCII-safe symbols
;;   - Mirror pattern (no change-state!)
;;   - do-*! naming for side-effecting writers
;;
;; Atom shape (Clarity Q3 prior consultation):
;;   (idle-pattern $verdict $count)
;;   $verdict in {productive, stuck-duplicate-engagement}
;;   $count is Nat (count of send-class actions in window)

;; Candidate identity preserved from original proposal
(= (candidate-id 002) idle-cycle-detector)
(= (candidate-status idle-cycle-detector) active-v1)
(= (candidate-description idle-cycle-detector)
   "Detect send-burst duplicate-engagement via recent-action window count")

;; === THRESHOLD ===
;; v1 send-burst threshold. Renamed from (idle-cycle-threshold) per
;; Clarity Q6 for honest semantic naming. v2 may reintroduce
;; idle-cycle-threshold for mechanism 1 (content-repetition).
(= (send-burst-threshold) 3)

;; === SEND DETECTION PREDICATE ===
;; A send-class action is one of the two send-emitting classifier tags
;; per cycle_classifier.metta classify-cycle-action-type:
;;   responsive-send       (msgnew=True path)
;;   status-send-unprompted (msgnew=False path)
;; Both count for v1 per Clarity Q3 of design refinement.
(= (is-send-action? $tag)
   (or (== $tag responsive-send) (== $tag status-send-unprompted)))

;; === LIST LENGTH HELPER ===
;; Private 2-clause recursive counter for collapse-then-count pattern.
(= (count-send-list ()) 0)
(= (count-send-list ($head $tail)) (+ 1 (count-send-list $tail)))

;; === WINDOW COUNT ===
;; Count send-class recent-action atoms in the current window.
;; The window is implicit (10 cycles, per recent_action_populator.metta
;; line 23 (recent-action-window) 3). collapse over the match yields
;; a list of cycle-ids for send-class actions; count-send-list returns
;; the length.
(= (count-sends-in-window)
   (let $sends (collapse (match &self (recent-action $c $tag $d)
                                       (if (is-send-action? $tag) $c ())))
      (count-send-list $sends)))

;; === PUBLIC READ HELPER ===
;; Returns current idle-pattern atom as (verdict count) pair, or ()
;; if no atom exists yet (pre-bootstrap).
(= (current-idle-pattern)
   (let $atoms (collapse (match &self (idle-pattern $v $n) ($v $n)))
      (if (== $atoms ())
          ()
          (car-atom $atoms))))

;; === FRESHNESS WRITER ===
;; Clears prior (idle-pattern ...) atom so the cycle-level writer can
;; emit fresh. C12-safe: collapse first, branch on empty.
(= (do-clear-idle-pattern!)
   (let $existing (collapse (match &self (idle-pattern $v $n) (idle-pattern $v $n)))
      (if (== $existing ())
          _
          (remove-atom &self (car-atom $existing)))))

;; === CYCLE-LEVEL WRITER ===
;; Called once per cycle from loop.metta (after populate-recent-action,
;; before next getContext). Computes send-count, derives verdict,
;; clears prior atom, emits fresh atom.
(= (do-update-idle-pattern!)
   (let* (($count (count-sends-in-window))
          ($verdict (if (> $count (send-burst-threshold))
                        stuck-duplicate-engagement
                        productive)))
      (progn
         (do-clear-idle-pattern!)
         (add-atom &self (idle-pattern $verdict $count)))))

;; === PROMPT BLOCK ===
;; Composes the IDLE-PATTERN block for prompt assembly. Mirrors the
;; (task-state-block) pattern: read atoms, call Python helper for text
;; assembly per C1. Block format matches task-state-block style.
(= (idle-pattern-block)
   (let $pattern (current-idle-pattern)
      (if (== $pattern ())
         (py-call (helper.idle_pattern_block_format productive 0))
         (let $v (car-atom $pattern)
            (let $n (car-atom (cdr-atom $pattern))
               (py-call (helper.idle_pattern_block_format $v $n)))))))'''


# ============================================================================
# EDIT 2: src/helper.py -- add idle_pattern_block_format
# ============================================================================

# Anchor on the same Soul Evaluation Prompts section header used in
# Step 4. Insert new function BEFORE that header. Step 4 inserted
# task_state_block_format / join_threads_text there too; we insert
# idle_pattern_block_format adjacent.

HELPER_ANCHOR = '''# --- Soul Evaluation Prompts --------------------------------------'''

HELPER_NEW = '''def idle_pattern_block_format(verdict, count):
    """Step 4.5: format the IDLE-PATTERN prompt block from MeTTa-computed
    verdict and count values.

    Hands-only per the project discipline: receives values that MeTTa
    already computed, returns formatted string. No reasoning, no
    thresholds, no decisions. The verdict was determined by
    (do-update-idle-pattern!) in soul/idle_cycle_detector.metta.

    Format:
        IDLE-PATTERN:
        (idle-pattern $verdict $count)
        Summary: Idle-pattern verdict: $verdict. $count send-class
        actions in last 10 cycles.

    Per Clarity's design (May 14, 2026, design-refinement consultation):
    mechanical template from atom values, zero interpretation, reports
    state not assessment.
    """
    atom_line = f"(idle-pattern {verdict} {count})"
    summary = (
        f"Idle-pattern verdict: {verdict}. "
        f"{count} send-class actions in last 10 cycles."
    )
    return (
        f"IDLE-PATTERN:\\n"
        f"{atom_line}\\n"
        f"Summary: {summary}"
    )


# --- Soul Evaluation Prompts --------------------------------------'''


# ============================================================================
# EDIT 3a: src/loop.metta -- cycle-level invocation after populate-recent-action
# ============================================================================

# The original line 134 ends with `)))` closing call + binding + let*.
# After insertion, the populate-recent-action line keeps only `))` (call +
# binding), and the new line `($_ (do-update-idle-pattern!)))` has three
# closes (call + binding + let*).
#
# Indent matches the existing cluster: 39 spaces before `($_`.

LOOP_CYCLE_ANCHOR = '($_ (populate-recent-action $sexpr $msgnew $k)))'

LOOP_CYCLE_NEW = '''($_ (populate-recent-action $sexpr $msgnew $k))
                                       ($_ (do-update-idle-pattern!)))'''


# ============================================================================
# EDIT 3b: src/loop.metta -- prompt-block insertion in getContext
# ============================================================================

# Anchor: the task-state-block insertion from Step 4. Inserts
# idle-pattern-block AFTER task-state-block, BEFORE LAST_SKILL_USE_RESULTS.

LOOP_PROMPT_ANCHOR = '''" YOUR_LAST_ACTION: " (your-last-action-block $k)
                         " " (task-state-block)
                         " LAST_SKILL_USE_RESULTS: "'''

LOOP_PROMPT_NEW = '''" YOUR_LAST_ACTION: " (your-last-action-block $k)
                         " " (task-state-block)
                         " " (idle-pattern-block)
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

def simulate_icd_forward(content):
    if find_target_substring_count(content, ICD_ANCHOR) != 1:
        raise RuntimeError("idle_cycle_detector forward: ICD_ANCHOR not found exactly once.")
    if "do-update-idle-pattern!" in content:
        raise RuntimeError("idle_cycle_detector forward: detection function already present.")
    return content.replace(ICD_ANCHOR, ICD_NEW, 1)


def simulate_icd_reverse(content):
    if find_target_substring_count(content, ICD_NEW) != 1:
        raise RuntimeError("idle_cycle_detector reverse: ICD_NEW not found exactly once.")
    return content.replace(ICD_NEW, ICD_ANCHOR, 1)


def simulate_helper_forward(content):
    if find_target_substring_count(content, HELPER_ANCHOR) != 1:
        raise RuntimeError("helper forward: HELPER_ANCHOR not found exactly once.")
    if "def idle_pattern_block_format" in content:
        raise RuntimeError("helper forward: idle_pattern_block_format already present.")
    return content.replace(HELPER_ANCHOR, HELPER_NEW, 1)


def simulate_helper_reverse(content):
    if find_target_substring_count(content, HELPER_NEW) != 1:
        raise RuntimeError("helper reverse: HELPER_NEW not found exactly once.")
    return content.replace(HELPER_NEW, HELPER_ANCHOR, 1)


def simulate_loop_forward(content):
    cycle_count = find_target_substring_count(content, LOOP_CYCLE_ANCHOR)
    prompt_count = find_target_substring_count(content, LOOP_PROMPT_ANCHOR)
    if cycle_count != 1:
        raise RuntimeError(f"loop forward: LOOP_CYCLE_ANCHOR not found exactly once (count={cycle_count}).")
    if prompt_count != 1:
        raise RuntimeError(f"loop forward: LOOP_PROMPT_ANCHOR not found exactly once (count={prompt_count}).")
    if "(do-update-idle-pattern!)" in content:
        raise RuntimeError("loop forward: do-update-idle-pattern! call already present.")
    if "(idle-pattern-block)" in content:
        raise RuntimeError("loop forward: idle-pattern-block call already present.")
    step1 = content.replace(LOOP_CYCLE_ANCHOR, LOOP_CYCLE_NEW, 1)
    step2 = step1.replace(LOOP_PROMPT_ANCHOR, LOOP_PROMPT_NEW, 1)
    return step2


def simulate_loop_reverse(content):
    if find_target_substring_count(content, LOOP_CYCLE_NEW) != 1:
        raise RuntimeError("loop reverse: LOOP_CYCLE_NEW not found exactly once.")
    if find_target_substring_count(content, LOOP_PROMPT_NEW) != 1:
        raise RuntimeError("loop reverse: LOOP_PROMPT_NEW not found exactly once.")
    step1 = content.replace(LOOP_CYCLE_NEW, LOOP_CYCLE_ANCHOR, 1)
    step2 = step1.replace(LOOP_PROMPT_NEW, LOOP_PROMPT_ANCHOR, 1)
    return step2


# ============================================================================
# STATE CHECKS
# ============================================================================

def icd_forward_state_ok(content):
    has_anchor = find_target_substring_count(content, ICD_ANCHOR) == 1
    no_new = "do-update-idle-pattern!" not in content
    ok = has_anchor and no_new
    return ok, f"anchor={has_anchor}, new_absent={no_new} -> {'OK' if ok else 'FAIL'}"


def icd_reverse_state_ok(content):
    has_new = find_target_substring_count(content, ICD_NEW) == 1
    return has_new, f"new_block_present={has_new} -> {'OK' if has_new else 'FAIL'}"


def helper_forward_state_ok(content):
    has_anchor = find_target_substring_count(content, HELPER_ANCHOR) == 1
    no_new = "def idle_pattern_block_format" not in content
    ok = has_anchor and no_new
    return ok, f"anchor={has_anchor}, new_absent={no_new} -> {'OK' if ok else 'FAIL'}"


def helper_reverse_state_ok(content):
    has_new = find_target_substring_count(content, HELPER_NEW) == 1
    return has_new, f"new_block_present={has_new} -> {'OK' if has_new else 'FAIL'}"


def loop_forward_state_ok(content):
    cycle_anchor = find_target_substring_count(content, LOOP_CYCLE_ANCHOR) == 1
    prompt_anchor = find_target_substring_count(content, LOOP_PROMPT_ANCHOR) == 1
    no_cycle_new = "(do-update-idle-pattern!)" not in content
    no_prompt_new = "(idle-pattern-block)" not in content
    ok = cycle_anchor and prompt_anchor and no_cycle_new and no_prompt_new
    return ok, (
        f"cycle_anchor={cycle_anchor}, prompt_anchor={prompt_anchor}, "
        f"cycle_absent={no_cycle_new}, prompt_absent={no_prompt_new} "
        f"-> {'OK' if ok else 'FAIL'}"
    )


def loop_reverse_state_ok(content):
    cycle_new = find_target_substring_count(content, LOOP_CYCLE_NEW) == 1
    prompt_new = find_target_substring_count(content, LOOP_PROMPT_NEW) == 1
    ok = cycle_new and prompt_new
    return ok, (
        f"cycle_new={cycle_new}, prompt_new={prompt_new} "
        f"-> {'OK' if ok else 'FAIL'}"
    )


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
        if i < len(old_lines):
            out.append(f"  {old_lines[i]}")
    return "\n".join(out)


# ============================================================================
# FILE PROCESSING
# ============================================================================

def process_file(path, bak_path, sim_fwd, sim_rev, expected_line_delta_fwd,
                 args, label, forward_check, reverse_check,
                 check_parens=True, paren_imbalance_expected=0,
                 paren_baseline_from_pre=False):
    """Returns (ok, orig_content, sim_content, summary_dict).
    summary_dict has: pre_lines, post_lines, line_delta, pre_parens,
    post_parens, paren_label."""
    summary = {
        "pre_lines": 0, "post_lines": 0, "line_delta": 0,
        "pre_parens": None, "post_parens": None, "paren_label": None,
    }
    print(f"\n>>> {label} <<<")
    if not path.exists():
        print(f"  ERROR: {path} not found.")
        return False, "", "", summary
    content = path.read_text()
    pre_lines = len(content.splitlines())
    summary["pre_lines"] = pre_lines
    print(f"  Path: {path}")
    print(f"  Pre-edit lines: {pre_lines}")

    pre_imbalance = None
    if check_parens:
        pre_o, pre_c = code_aware_paren_count(content)
        pre_d = pre_o - pre_c
        pre_imbalance = pre_d
        summary["pre_parens"] = (pre_o, pre_c, pre_d)
        if paren_baseline_from_pre:
            expected_imbalance = pre_d
            summary["paren_label"] = "by-design baseline"
            print(f"  Pre-edit parens: opens={pre_o} closes={pre_c} delta={pre_d} (file's by-design baseline)")
        else:
            expected_imbalance = paren_imbalance_expected
            summary["paren_label"] = "balanced"
            c_paren = "OK" if pre_d == expected_imbalance else "FAIL"
            print(f"  Pre-edit parens: opens={pre_o} closes={pre_c} delta={pre_d} (expected {expected_imbalance}) ({c_paren})")
            if c_paren != "OK":
                print(f"  PAREN FAILED for {label}. Aborting.")
                return False, content, "", summary

    if args.reverse:
        ok, msg = reverse_check(content)
    else:
        ok, msg = forward_check(content)
    print(f"  State check: {msg}")
    if not ok:
        print(f"  STATE CHECK FAILED for {label}. Aborting.")
        return False, content, "", summary

    try:
        if args.reverse:
            simulated = sim_rev(content)
        else:
            simulated = sim_fwd(content)
    except RuntimeError as exc:
        print(f"  SIMULATION FAILED: {exc}")
        return False, content, "", summary

    post_lines = len(simulated.splitlines())
    line_delta = post_lines - pre_lines
    summary["post_lines"] = post_lines
    summary["line_delta"] = line_delta

    if check_parens:
        post_o, post_c = code_aware_paren_count(simulated)
        post_d = post_o - post_c
        summary["post_parens"] = (post_o, post_c, post_d)
        if paren_baseline_from_pre:
            paren_delta_change = post_d - pre_imbalance
            print(f"  Post-edit parens: opens={post_o} closes={post_c} delta={post_d} (change={paren_delta_change:+d}, expected 0)")
            if paren_delta_change != 0:
                print(f"  POST-EDIT PAREN BALANCE CHANGED for {label}. Aborting.")
                return False, content, simulated, summary
        else:
            expected_imbalance = paren_imbalance_expected
            c_post_paren = "OK" if post_d == expected_imbalance else "FAIL"
            print(f"  Post-edit parens: opens={post_o} closes={post_c} delta={post_d} (expected {expected_imbalance}) ({c_post_paren})")
            if c_post_paren != "OK":
                print(f"  POST-EDIT PAREN FAILED for {label}. Aborting.")
                return False, content, simulated, summary

    expected = expected_line_delta_fwd if not args.reverse else -expected_line_delta_fwd
    c_lines = "OK" if line_delta == expected else "FAIL"
    print(f"  Line delta: {line_delta} (expected {expected}) ({c_lines})")
    if c_lines != "OK":
        print(f"  LINE DELTA FAILED for {label}. Aborting.")
        return False, content, simulated, summary

    return True, content, simulated, summary


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Step 4.5: idle_cycle_detector v1 wiring")
    parser.add_argument("--apply", action="store_true",
                        help="Write changes. Default is dry-run.")
    parser.add_argument("--reverse", action="store_true",
                        help="Reverse the edits.")
    args = parser.parse_args()

    direction = "REVERSE" if args.reverse else "APPLY"
    print(f"\n========== STEP 4.5 IDLE_CYCLE_DETECTOR: {direction} ==========")

    icd_delta = ICD_NEW.count("\n") - ICD_ANCHOR.count("\n")
    helper_delta = HELPER_NEW.count("\n") - HELPER_ANCHOR.count("\n")
    cycle_delta = LOOP_CYCLE_NEW.count("\n") - LOOP_CYCLE_ANCHOR.count("\n")
    prompt_delta = LOOP_PROMPT_NEW.count("\n") - LOOP_PROMPT_ANCHOR.count("\n")
    loop_delta = cycle_delta + prompt_delta

    ok_icd, icd_orig, icd_sim, icd_summary = process_file(
        ICD_PATH, ICD_BAK,
        simulate_icd_forward, simulate_icd_reverse,
        icd_delta, args, "soul/idle_cycle_detector.metta",
        icd_forward_state_ok, icd_reverse_state_ok,
        check_parens=True, paren_imbalance_expected=0,
    )
    if not ok_icd:
        return 1

    ok_h, h_orig, h_sim, h_summary = process_file(
        HELPER_PATH, HELPER_BAK,
        simulate_helper_forward, simulate_helper_reverse,
        helper_delta, args, "src/helper.py",
        helper_forward_state_ok, helper_reverse_state_ok,
        check_parens=False,
    )
    if not ok_h:
        return 1

    ok_l, l_orig, l_sim, l_summary = process_file(
        LOOP_PATH, LOOP_BAK,
        simulate_loop_forward, simulate_loop_reverse,
        loop_delta, args, "src/loop.metta",
        loop_forward_state_ok, loop_reverse_state_ok,
        check_parens=True, paren_baseline_from_pre=True,
    )
    if not ok_l:
        return 1

    print("\n========== DIFF PREVIEWS ==========")
    print(diff_preview(icd_orig, icd_sim, "soul/idle_cycle_detector.metta", context=2))
    print()
    print(diff_preview(h_orig, h_sim, "src/helper.py", context=2))
    print()
    print(diff_preview(l_orig, l_sim, "src/loop.metta", context=2))

    # ========================================================================
    # SUMMARY BLOCK: what --apply will do
    # ========================================================================
    action_word = "REVERSE" if args.reverse else "APPLY"
    flag_str = "--reverse --apply" if args.reverse else "--apply"
    reverse_str = "--apply" if args.reverse else "--reverse --apply"

    def fmt_paren_summary(s):
        if s["pre_parens"] is None:
            return "no paren check (Python file)"
        pre_o, pre_c, pre_d = s["pre_parens"]
        if s["post_parens"] is None:
            return f"parens not computed"
        post_o, post_c, post_d = s["post_parens"]
        if s["paren_label"] == "by-design baseline":
            change = post_d - pre_d
            return (f"parens {pre_o}/{pre_c} (delta {pre_d}) -> "
                    f"{post_o}/{post_c} (delta {post_d}) "
                    f"baseline change: {change:+d}")
        return (f"parens {pre_o}/{pre_c} (delta {pre_d}) -> "
                f"{post_o}/{post_c} (delta {post_d}) balanced")

    files_info = [
        ("soul/idle_cycle_detector.metta", icd_summary, ICD_BAK,
         "Edit 1: full rewrite of candidate-002 file with v1 detection function set"),
        ("src/helper.py", h_summary, HELPER_BAK,
         "Edit 2: insert idle_pattern_block_format Python helper before Soul Evaluation Prompts header"),
        ("src/loop.metta", l_summary, LOOP_BAK,
         "Edit 3a + 3b: insert (do-update-idle-pattern!) after populate-recent-action; insert (idle-pattern-block) in getContext after task-state-block"),
    ]

    print(f"\n========== SUMMARY: WHAT {flag_str} WILL DO ==========")
    print(f"Direction: {action_word}")
    print(f"Backup suffix: .bak.step4_5 (created on apply, not on dry-run)")
    print()
    for path_str, s, bak, desc in files_info:
        print(f"  {path_str}")
        print(f"    {desc}")
        print(f"    Lines: {s['pre_lines']} -> {s['post_lines']} ({s['line_delta']:+d})")
        print(f"    {fmt_paren_summary(s)}")
        print(f"    Backup target: {bak}")
        print()
    print(f"Total edits: 4 coordinated changes across 3 files")
    print(f"Reversibility: python3 staging/apply_step4_5.py {reverse_str}")
    print(f"Post-apply container rebuild required (--no-cache for soul/ changes)")

    if not args.apply:
        print("\n========== DRY-RUN COMPLETE ==========")
        print(f"All checks pass. Re-run with {flag_str} to write the changes summarized above.")
        return 0

    if not args.reverse:
        for path, bak in [(ICD_PATH, ICD_BAK),
                          (HELPER_PATH, HELPER_BAK),
                          (LOOP_PATH, LOOP_BAK)]:
            if bak.exists():
                print(f"WARNING: backup {bak} exists; overwriting.")
            bak.write_text(path.read_text())
            print(f"Backup written: {bak}")

    print("\n========== WRITING ==========")
    ICD_PATH.write_text(icd_sim)
    print(f"Wrote: {ICD_PATH}")
    HELPER_PATH.write_text(h_sim)
    print(f"Wrote: {HELPER_PATH}")
    LOOP_PATH.write_text(l_sim)
    print(f"Wrote: {LOOP_PATH}")

    print("\n========== DISK VERIFICATION ==========")
    for path, fwd_check, rev_check, label, do_paren, paren_baseline in [
        (ICD_PATH, icd_forward_state_ok, icd_reverse_state_ok,
         "soul/idle_cycle_detector.metta", True, False),
        (HELPER_PATH, helper_forward_state_ok, helper_reverse_state_ok,
         "src/helper.py", False, False),
        (LOOP_PATH, loop_forward_state_ok, loop_reverse_state_ok,
         "src/loop.metta", True, True),
    ]:
        disk = path.read_text()
        if do_paren:
            o, c = code_aware_paren_count(disk)
            d = o - c
            print(f"  {label} parens: opens={o} closes={c} delta={d}"
                  + (" (file's by-design baseline)" if paren_baseline else " (expected 0)"))
        if args.reverse:
            ok, msg = fwd_check(disk)
        else:
            ok, msg = rev_check(disk)
        print(f"  {label} state: {msg}")
        if not ok:
            print("DISK VERIFICATION FAILED.")
            return 1

    print("\n========== STEP 4.5 COMPLETE ==========")
    if not args.reverse:
        print("\nNext: container rebuild and behavioral tests.")
        print("  docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw && sleep 15 && docker logs clarity_omega 2>&1 | tail -50")
        print("\nThen run behavioral tests S4_5-1 through S4_5-3:")
        print("  S4_5-1: Verify no parse errors on the 3 modified files")
        print("  S4_5-2: Verify IDLE-PATTERN block appears in CHARS_SENT after TASK-STATE block")
        print("  S4_5-3: Send 3+ messages in quick succession; verify (idle-pattern stuck-duplicate-engagement N) appears, then returns to productive after 10 cycles")
        print("  S4_5-4 (observation): Watch whether Clarity voluntarily references idle-pattern in her reasoning")
    return 0


if __name__ == "__main__":
    sys.exit(main())
