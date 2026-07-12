#!/usr/bin/env python3
"""
Apply script: Step 4.5/4.6 PREDICATE FIX -- collapse-trap correction

Bug: both soul/idle_cycle_detector.metta (Step 4.5) and
soul/agency_balance_guard.metta (Step 4.6) use the pattern:

    (collapse (match &self (recent-action $c $tag $d)
                            (if (is-X-action? $tag) $c ())))

Per Sprint 3 Knowledge Section 11:
    "the naive forms (if (== (collapse ...) ()) False True) look
    reasonable but have subtle traps. The collapse of () markers
    does not return (). Instead it returns a list of () markers,
    which is non-empty."

The collapse padding with () markers causes count-{send,agency}-list
to count empty markers as real elements. Counts come out wrong; the
in-production agency-balance shows (agency-balance healthy 0 0) even
when recent-action atoms exist.

Fix per the verified-safe pattern from soul/task_state.metta
count-pending-threads (committed Sprint 3, Clarity-reviewed):

    ;; Match without if-filter; project just the discriminating field
    (= (count-X-actions-in-window)
       (let $tags (collapse (match &self (recent-action $c $tag $d) $tag))
          (count-X-tags $tags)))

    ;; Filter in the recursive counter where if returns numbers, not ()
    (= (count-X-tags ()) 0)
    (= (count-X-tags ($head $tail))
       (if (is-X-action? $head)
           (+ 1 (count-X-tags $tail))
           (count-X-tags $tail)))

This mirrors task_state.metta's count-pending-list + count-pending-threads
shape, with predicate filter moved into the recursive counter.

Edits across two files:

1. soul/idle_cycle_detector.metta -- replace count-send-list block
   (lines 55-69 in disk version): old list counter + count-sends-in-window
   become predicate-filtered count-send-tags + count-sends-in-window
   using match-without-filter pattern.

2. soul/agency_balance_guard.metta -- replace count-agency-list block
   (lines 110-125 in disk version): old list counter + two count-*-actions
   become two predicate-filtered counters (count-person-tags,
   count-system-tags) + two updated entry points.

No helper.py, no loop.metta, no lib_clarity_reasoning changes.
Predicates is-send-action?, is-person-action?, is-system-action?
are preserved unchanged -- they were not the bug.

Reversibility:
- --apply writes changes with .bak.step4_5_6_predicate_fix backups
- --reverse --apply restores prior counter shape
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


# ============================================================================
# FILE PATHS
# ============================================================================

ICD_PATH = Path("soul/idle_cycle_detector.metta")
ICD_BAK = Path("soul/idle_cycle_detector.metta.bak.step4_5_6_predicate_fix")

ABG_PATH = Path("soul/agency_balance_guard.metta")
ABG_BAK = Path("soul/agency_balance_guard.metta.bak.step4_5_6_predicate_fix")


# ============================================================================
# EDIT 1: soul/idle_cycle_detector.metta -- predicate-filter pattern
# ============================================================================

ICD_ANCHOR = ''';; === LIST LENGTH HELPER ===
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
      (count-send-list $sends)))'''

ICD_NEW = ''';; === PREDICATE-FILTERED LIST COUNTER ===
;; Private 2-clause recursive counter that applies is-send-action?
;; during recursion. Pattern per task_state.metta count-pending-list
;; (Sprint 3, Clarity-reviewed) plus filter-in-counter idiom.
;;
;; Why this shape (Sprint 3 Section 11):
;;   The naive collapse-with-if-defaulting-to-() pattern pads results
;;   with () markers, producing a non-empty list when nothing matches.
;;   By projecting just $tag in the match and filtering in the counter,
;;   the if-branches return numbers (not ()), avoiding the trap.
(= (count-send-tags ()) 0)
(= (count-send-tags ($head $tail))
   (if (is-send-action? $head)
       (+ 1 (count-send-tags $tail))
       (count-send-tags $tail)))

;; === WINDOW COUNT ===
;; Count send-class recent-action atoms in the current window.
;; The window is implicit (10 cycles, per recent_action_populator.metta).
;; Match projects just $tag for every recent-action; count-send-tags
;; recursively filters by predicate and returns the matching count.
(= (count-sends-in-window)
   (let $tags (collapse (match &self (recent-action $c $tag $d) $tag))
      (count-send-tags $tags)))'''


# ============================================================================
# EDIT 2: soul/agency_balance_guard.metta -- predicate-filter pattern
# ============================================================================

ABG_ANCHOR = ''';; Private 2-clause recursive list counter (mirrors idle_cycle_detector pattern)
(= (count-agency-list ()) 0)
(= (count-agency-list ($head $tail)) (+ 1 (count-agency-list $tail)))

;; Count person-class actions in current recent-action window (10 cycles).
;; Window is implicit (recent_action_populator.metta prunes at 10).
(= (count-person-actions-in-window)
   (let $persons (collapse (match &self (recent-action $c $tag $d)
                                          (if (is-person-action? $tag) $c ())))
      (count-agency-list $persons)))

;; Count system-class actions in current recent-action window (10 cycles).
(= (count-system-actions-in-window)
   (let $systems (collapse (match &self (recent-action $c $tag $d)
                                          (if (is-system-action? $tag) $c ())))
      (count-agency-list $systems)))'''

ABG_NEW = ''';; Private 2-clause recursive predicate-filtered counters.
;; Pattern per task_state.metta count-pending-list (Sprint 3) plus
;; filter-in-counter idiom. Per Sprint 3 Section 11, the naive
;; collapse-with-if-defaulting-to-() pattern pads results with () markers
;; producing non-empty lists; the safe pattern projects just $tag in the
;; match and filters in the recursive counter where if returns numbers.
(= (count-person-tags ()) 0)
(= (count-person-tags ($head $tail))
   (if (is-person-action? $head)
       (+ 1 (count-person-tags $tail))
       (count-person-tags $tail)))

(= (count-system-tags ()) 0)
(= (count-system-tags ($head $tail))
   (if (is-system-action? $head)
       (+ 1 (count-system-tags $tail))
       (count-system-tags $tail)))

;; Count person-class actions in current recent-action window (10 cycles).
;; Window is implicit (recent_action_populator.metta prunes at 10).
;; Match projects just $tag; count-person-tags filters by predicate.
(= (count-person-actions-in-window)
   (let $tags (collapse (match &self (recent-action $c $tag $d) $tag))
      (count-person-tags $tags)))

;; Count system-class actions in current recent-action window (10 cycles).
;; Same shape as count-person-actions-in-window with the system predicate.
(= (count-system-actions-in-window)
   (let $tags (collapse (match &self (recent-action $c $tag $d) $tag))
      (count-system-tags $tags)))'''


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
    if "count-send-tags" in content:
        raise RuntimeError("idle_cycle_detector forward: count-send-tags already present.")
    return content.replace(ICD_ANCHOR, ICD_NEW, 1)


def simulate_icd_reverse(content):
    if find_target_substring_count(content, ICD_NEW) != 1:
        raise RuntimeError("idle_cycle_detector reverse: ICD_NEW not found exactly once.")
    return content.replace(ICD_NEW, ICD_ANCHOR, 1)


def simulate_abg_forward(content):
    if find_target_substring_count(content, ABG_ANCHOR) != 1:
        raise RuntimeError("agency_balance_guard forward: ABG_ANCHOR not found exactly once.")
    if "count-person-tags" in content or "count-system-tags" in content:
        raise RuntimeError("agency_balance_guard forward: predicate-filtered counters already present.")
    return content.replace(ABG_ANCHOR, ABG_NEW, 1)


def simulate_abg_reverse(content):
    if find_target_substring_count(content, ABG_NEW) != 1:
        raise RuntimeError("agency_balance_guard reverse: ABG_NEW not found exactly once.")
    return content.replace(ABG_NEW, ABG_ANCHOR, 1)


# ============================================================================
# STATE CHECKS
# ============================================================================

def icd_forward_state_ok(content):
    has_anchor = find_target_substring_count(content, ICD_ANCHOR) == 1
    no_new = "count-send-tags" not in content
    ok = has_anchor and no_new
    return ok, f"anchor={has_anchor}, new_absent={no_new} -> {'OK' if ok else 'FAIL'}"


def icd_reverse_state_ok(content):
    has_new = find_target_substring_count(content, ICD_NEW) == 1
    return has_new, f"new_block_present={has_new} -> {'OK' if has_new else 'FAIL'}"


def abg_forward_state_ok(content):
    has_anchor = find_target_substring_count(content, ABG_ANCHOR) == 1
    no_new = ("count-person-tags" not in content) and ("count-system-tags" not in content)
    ok = has_anchor and no_new
    return ok, f"anchor={has_anchor}, new_absent={no_new} -> {'OK' if ok else 'FAIL'}"


def abg_reverse_state_ok(content):
    has_new = find_target_substring_count(content, ABG_NEW) == 1
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
        if i < len(old_lines):
            out.append(f"  {old_lines[i]}")
    return "\n".join(out)


# ============================================================================
# FILE PROCESSING
# ============================================================================

def process_file(path, bak_path, sim_fwd, sim_rev, expected_line_delta_fwd,
                 args, label, forward_check, reverse_check):
    """Returns (ok, orig_content, sim_content, summary_dict)."""
    summary = {
        "pre_lines": 0, "post_lines": 0, "line_delta": 0,
        "pre_parens": None, "post_parens": None,
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

    pre_o, pre_c = code_aware_paren_count(content)
    pre_d = pre_o - pre_c
    summary["pre_parens"] = (pre_o, pre_c, pre_d)
    c_paren = "OK" if pre_d == 0 else "FAIL"
    print(f"  Pre-edit parens: opens={pre_o} closes={pre_c} delta={pre_d} ({c_paren})")
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

    post_o, post_c = code_aware_paren_count(simulated)
    post_d = post_o - post_c
    summary["post_parens"] = (post_o, post_c, post_d)
    c_post_paren = "OK" if post_d == 0 else "FAIL"
    print(f"  Post-edit parens: opens={post_o} closes={post_c} delta={post_d} ({c_post_paren})")
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
    parser = argparse.ArgumentParser(description="Step 4.5/4.6 predicate-fix (collapse-trap correction)")
    parser.add_argument("--apply", action="store_true",
                        help="Write changes. Default is dry-run.")
    parser.add_argument("--reverse", action="store_true",
                        help="Reverse the edits.")
    args = parser.parse_args()

    direction = "REVERSE" if args.reverse else "APPLY"
    print(f"\n========== STEP 4.5/4.6 PREDICATE FIX: {direction} ==========")

    icd_delta = ICD_NEW.count("\n") - ICD_ANCHOR.count("\n")
    abg_delta = ABG_NEW.count("\n") - ABG_ANCHOR.count("\n")

    ok_icd, icd_orig, icd_sim, icd_summary = process_file(
        ICD_PATH, ICD_BAK,
        simulate_icd_forward, simulate_icd_reverse,
        icd_delta, args, "soul/idle_cycle_detector.metta",
        icd_forward_state_ok, icd_reverse_state_ok,
    )
    if not ok_icd:
        return 1

    ok_abg, abg_orig, abg_sim, abg_summary = process_file(
        ABG_PATH, ABG_BAK,
        simulate_abg_forward, simulate_abg_reverse,
        abg_delta, args, "soul/agency_balance_guard.metta",
        abg_forward_state_ok, abg_reverse_state_ok,
    )
    if not ok_abg:
        return 1

    print("\n========== DIFF PREVIEWS ==========")
    print(diff_preview(icd_orig, icd_sim, "soul/idle_cycle_detector.metta", context=2))
    print()
    print(diff_preview(abg_orig, abg_sim, "soul/agency_balance_guard.metta", context=2))

    # ========================================================================
    # SUMMARY BLOCK (F20)
    # ========================================================================
    action_word = "REVERSE" if args.reverse else "APPLY"
    flag_str = "--reverse --apply" if args.reverse else "--apply"
    reverse_str = "--apply" if args.reverse else "--reverse --apply"

    def fmt_paren_summary(s):
        if s["pre_parens"] is None:
            return "no paren check"
        pre_o, pre_c, pre_d = s["pre_parens"]
        if s["post_parens"] is None:
            return "parens not computed"
        post_o, post_c, post_d = s["post_parens"]
        return (f"parens {pre_o}/{pre_c} (delta {pre_d}) -> "
                f"{post_o}/{post_c} (delta {post_d}) balanced")

    files_info = [
        ("soul/idle_cycle_detector.metta", icd_summary, ICD_BAK,
         "Edit 1: Replace count-send-list + count-sends-in-window with predicate-filtered count-send-tags pattern (per Sprint 3 Section 11 collapse-trap fix; task_state.metta count-pending-threads idiom)"),
        ("soul/agency_balance_guard.metta", abg_summary, ABG_BAK,
         "Edit 2: Replace count-agency-list + count-person-actions-in-window + count-system-actions-in-window with predicate-filtered count-person-tags + count-system-tags pattern (same Sprint 3 fix)"),
    ]

    print(f"\n========== SUMMARY: WHAT {flag_str} WILL DO ==========")
    print(f"Direction: {action_word}")
    print(f"Backup suffix: .bak.step4_5_6_predicate_fix (created on apply, not on dry-run)")
    print()
    for path_str, s, bak, desc in files_info:
        print(f"  {path_str}")
        print(f"    {desc}")
        print(f"    Lines: {s['pre_lines']} -> {s['post_lines']} ({s['line_delta']:+d})")
        print(f"    {fmt_paren_summary(s)}")
        print(f"    Backup target: {bak}")
        print()
    print(f"Total edits: 2 coordinated changes across 2 files")
    print(f"Reversibility: python3 staging/apply_step4_5_6_predicate_fix.py {reverse_str}")
    print(f"Post-apply container rebuild required (--no-cache for soul/ changes)")

    if not args.apply:
        print("\n========== DRY-RUN COMPLETE ==========")
        print(f"All checks pass. Re-run with {flag_str} to write the changes summarized above.")
        return 0

    if not args.reverse:
        for path, bak in [(ICD_PATH, ICD_BAK), (ABG_PATH, ABG_BAK)]:
            if bak.exists():
                print(f"WARNING: backup {bak} exists; overwriting.")
            bak.write_text(path.read_text())
            print(f"Backup written: {bak}")

    print("\n========== WRITING ==========")
    ICD_PATH.write_text(icd_sim)
    print(f"Wrote: {ICD_PATH}")
    ABG_PATH.write_text(abg_sim)
    print(f"Wrote: {ABG_PATH}")

    print("\n========== DISK VERIFICATION ==========")
    for path, fwd_check, rev_check, label in [
        (ICD_PATH, icd_forward_state_ok, icd_reverse_state_ok,
         "soul/idle_cycle_detector.metta"),
        (ABG_PATH, abg_forward_state_ok, abg_reverse_state_ok,
         "soul/agency_balance_guard.metta"),
    ]:
        disk = path.read_text()
        o, c = code_aware_paren_count(disk)
        d = o - c
        print(f"  {label} parens: opens={o} closes={c} delta={d} (expected 0)")
        if args.reverse:
            ok, msg = fwd_check(disk)
        else:
            ok, msg = rev_check(disk)
        print(f"  {label} state: {msg}")
        if not ok:
            print("DISK VERIFICATION FAILED.")
            return 1

    print("\n========== STEP 4.5/4.6 PREDICATE FIX COMPLETE ==========")
    if not args.reverse:
        print("\nNext: container rebuild and behavioral tests.")
        print("  docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw && sleep 15 && docker logs clarity_omega 2>&1 | tail -50")
        print("\nBehavioral verification targets:")
        print("  - idle-pattern $count > 0 when send-class atoms exist in window")
        print("  - agency-balance $person+$system > 0 when recent-action atoms exist")
        print("  - idle-pattern verdict flips to stuck-duplicate-engagement when count > 3")
        print("  - agency-balance verdict flips to dependency-risk when system/total > 0.6")
        print("  - Consistency: idle-pattern count and agency-balance counts derive from same window")
    return 0


if __name__ == "__main__":
    sys.exit(main())
