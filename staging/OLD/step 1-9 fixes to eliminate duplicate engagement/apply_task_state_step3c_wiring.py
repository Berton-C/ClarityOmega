#!/usr/bin/env python3
"""
Apply script: Step 3c of task-state primitive. Adds validation helper,
two skills (do-set-phase-with-anchor!, do-add-pending-thread!), and
pending-thread eviction infrastructure.

Purpose
-------
Steps 3a and 3b landed Clarity's substrate work for the atom shape change
(pending-thread with timestamp) and the two simplest skills (do-set-phase!,
do-resolve-pending-thread!). Step 3c completes the four-skill set with
the two harder skills plus their supporting helpers.

Clarity exercised architectural sovereignty on:
- 3a atom shape (Option A: timestamp in atom)
- Skill patterns (do-*! naming, C12-safe collapse-then-branch)
- Helper placement (count-pending-threads + count-pending-list in
  task_state.metta as public read helpers; find-min-ts and
  oldest-pending-thread in task_state_writers.metta as eviction internals)
- Naming: count-pending-list (not generic count-list) per her collision-
  risk flag

3c implementation is pure code transcription of pre-vetted patterns.
This script does that work atomically.

The two edits
-------------
Edit 1: task_state.metta
  Add count-pending-list (private list-counter helper) and
  count-pending-threads (public read) as new functions in Section 3,
  after current-pending-threads (current line 109).

Edit 2: task_state_writers.metta
  Add to Section 3, after do-resolve-pending-thread!:
  - is-valid-anchor-value? (validation helper)
  - do-set-phase-with-anchor! (skill)
  - find-min-ts (recursive min-finder, 2 clauses)
  - oldest-pending-thread (wraps find-min-ts with collapse-match)
  - do-add-pending-thread! (skill, uses count and oldest helpers)

Net change
----------
- task_state.metta: +12 lines (count-pending-list 2 clauses + count-pending-threads)
- task_state_writers.metta: +40 lines (validation + 2 skills + 2 eviction helpers)
- Paren delta for both files: 0 (each function is balanced)

Mechanism
---------
- is-valid-anchor-value? uses nested-if comparison chain for 11 valid values
- count-pending-list is a 2-clause recursive function (base case + recursive case)
- find-min-ts is similarly 2-clause recursive
- do-set-phase-with-anchor! mirrors do-set-phase! plus conditional anchor add
- do-add-pending-thread! adds atom, checks count, evicts oldest if > 7

Usage
-----
Dry-run (default):
    python3 staging/apply_task_state_step3c_wiring.py

Apply:
    python3 staging/apply_task_state_step3c_wiring.py --apply

Reverse (after apply):
    python3 staging/apply_task_state_step3c_wiring.py --reverse --apply

Pre-conditions
--------------
- Steps 3a and 3b landed; current task_state_writers.metta has the
  five functions in Sections 1, 2, 3 (the canonical post-cleanup state)
- Step 2 commit at HEAD or in lineage
- Container can be rebuilt after apply

Backup files (forward apply only):
- soul/task_state.metta.bak.step3c_wiring
- soul/task_state_writers.metta.bak.step3c_wiring
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# ============================================================================
# FILE PATHS
# ============================================================================

TASK_STATE_PATH = Path("soul/task_state.metta")
TASK_STATE_BAK = Path("soul/task_state.metta.bak.step3c_wiring")

WRITERS_PATH = Path("soul/task_state_writers.metta")
WRITERS_BAK = Path("soul/task_state_writers.metta.bak.step3c_wiring")

# ============================================================================
# EDIT 1: task_state.metta - add count-pending-list and count-pending-threads
# ============================================================================

# Anchor: the closing line of current-pending-threads (last line of file
# before the percent sign that's actually the bash %% prompt indicator)
# We anchor on the full multi-line current-pending-threads block.

TS_ANCHOR = """;; Current pending threads. Returns all pending-thread topics,
;; projecting just $topic from the ($topic $timestamp) shape.
;; Collection reader -- no if-branch needed because empty IS
;; the correct answer, not a fallback.
(= (current-pending-threads)
   (match &self (pending-thread $topic $timestamp) $topic))"""

TS_NEW_BLOCK = TS_ANCHOR + """

;; Count helper: recursive length of a list. Private helper used by
;; count-pending-threads. Renamed from count-list to avoid potential
;; collision in PeTTa module scope (per Clarity's review).
(= (count-pending-list ()) 0)
(= (count-pending-list ($head $tail)) (+ 1 (count-pending-list $tail)))

;; Current pending thread count. Returns Nat count of pending-thread
;; atoms in &self. Public read helper; consumers can use without
;; depending on task_state_writers.metta.
(= (count-pending-threads)
   (let $all (collapse (match &self (pending-thread $topic $ts) ($topic $ts)))
      (count-pending-list $all)))"""

# ============================================================================
# EDIT 2: task_state_writers.metta - add validation, 2 skills, 2 eviction helpers
# ============================================================================

# Anchor: do-resolve-pending-thread! is the last existing function in Section 3
# We anchor on its full block and add new content after.

WR_ANCHOR = """;; (do-resolve-pending-thread! $topic)
;;   Finds (pending-thread $topic $timestamp) via collapse-match.
;;   If absent, silent no-op. If found, remove-atom with exact pattern.
(= (do-resolve-pending-thread! $topic)
   (let $ts (collapse (match &self (pending-thread $topic $t) $t))
      (if (== $ts ())
          _
          (remove-atom &self (pending-thread $topic $ts)))))"""

WR_NEW_BLOCK = WR_ANCHOR + """

;; (is-valid-anchor-value? $v)
;;   Returns True if $v is in the valid anchor set (Section 4.5 of spec),
;;   False otherwise. Primary: Safety, Integrity, HumanFlourishing,
;;   Governance, Helpfulness. Secondary: WonderPreservation,
;;   CreativeTranscendence, TimeCoherence, PurposeBeyondUtility,
;;   SharedUnderstanding, AgencyBalance.
(= (is-valid-anchor-value? $v)
   (if (== $v Safety) True
   (if (== $v Integrity) True
   (if (== $v HumanFlourishing) True
   (if (== $v Governance) True
   (if (== $v Helpfulness) True
   (if (== $v WonderPreservation) True
   (if (== $v CreativeTranscendence) True
   (if (== $v TimeCoherence) True
   (if (== $v PurposeBeyondUtility) True
   (if (== $v SharedUnderstanding) True
   (if (== $v AgencyBalance) True
       False))))))))))))

;; (do-set-phase-with-anchor! $new-phase $value $reason)
;;   Same shape as do-set-phase! plus conditional anchor record.
;;   If $current == $new-phase: no-op.
;;   Else: replace phase, add transition, conditionally add anchor.
;;   $value must be in valid anchor set; if invalid, anchor skipped
;;   but phase transition proceeds. v1 baseline silent-skip behavior.
(= (do-set-phase-with-anchor! $new-phase $value $reason)
   (let $current (current-phase)
      (if (== $current $new-phase)
          _
          (progn
             (set-atom! &self (task-phase $current) (task-phase $new-phase))
             (add-atom &self (task-phase-transition $current $new-phase (get_time)))
             (if (is-valid-anchor-value? $value)
                 (add-atom &self (task-phase-anchor $new-phase $value (get_time) $reason))
                 _)))))

;; (find-min-ts $best $rest) - eviction internal
;;   Recursive min-finder over ($topic $timestamp) pairs. $best is the
;;   current best pair; $rest is the remaining list to scan.
;;   Returns the pair with minimum $timestamp.
(= (find-min-ts $best ()) $best)
(= (find-min-ts ($best-topic $best-ts) (($t $ts) $rest))
   (if (< $ts $best-ts)
       (find-min-ts ($t $ts) $rest)
       (find-min-ts ($best-topic $best-ts) $rest)))

;; (oldest-pending-thread) - eviction internal
;;   Wraps find-min-ts with collapse-match. Returns ($topic $timestamp)
;;   of pending-thread atom with smallest timestamp, or () if no pending
;;   threads exist.
(= (oldest-pending-thread)
   (let $all (collapse (match &self (pending-thread $t $ts) ($t $ts)))
      (if (== $all ())
          ()
          (find-min-ts (car-atom $all) (cdr-atom $all)))))

;; (do-add-pending-thread! $topic)
;;   Adds (pending-thread $topic (get_time)) to &self. After adding,
;;   checks count via count-pending-threads. If > 7, evicts oldest
;;   (FIFO) via oldest-pending-thread + remove-atom. If <= 7, no-op.
(= (do-add-pending-thread! $topic)
   (let $now (get_time)
      (progn
         (add-atom &self (pending-thread $topic $now))
         (if (> (count-pending-threads) 7)
             (let $oldest (oldest-pending-thread)
                (if (== $oldest ())
                    _
                    (let $old-topic (car-atom $oldest)
                       (let $old-ts (car-atom (cdr-atom $oldest))
                          (remove-atom &self
                             (pending-thread $old-topic $old-ts))))))
             _))))"""


# ============================================================================
# HELPERS (reused from prior apply scripts)
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


def find_target_lines(text: str, target: str) -> list[int]:
    target_stripped = target.strip()
    matches = []
    for idx, line in enumerate(text.splitlines(), start=1):
        if line.strip() == target_stripped:
            matches.append(idx)
    return matches


# ============================================================================
# SIMULATION
# ============================================================================

def simulate_ts_forward(content: str) -> str:
    if find_target_substring_count(content, TS_ANCHOR) != 1:
        raise RuntimeError("ts forward: TS_ANCHOR not found exactly once.")
    if "count-pending-list" in content:
        raise RuntimeError("ts forward: count-pending-list already in file; pre-state wrong.")
    if "count-pending-threads" in content:
        raise RuntimeError("ts forward: count-pending-threads already in file; pre-state wrong.")
    return content.replace(TS_ANCHOR, TS_NEW_BLOCK, 1)


def simulate_ts_reverse(content: str) -> str:
    if find_target_substring_count(content, TS_NEW_BLOCK) != 1:
        raise RuntimeError("ts reverse: TS_NEW_BLOCK not found exactly once.")
    return content.replace(TS_NEW_BLOCK, TS_ANCHOR, 1)


def simulate_wr_forward(content: str) -> str:
    if find_target_substring_count(content, WR_ANCHOR) != 1:
        raise RuntimeError("wr forward: WR_ANCHOR not found exactly once.")
    if "is-valid-anchor-value?" in content:
        raise RuntimeError("wr forward: is-valid-anchor-value? already in file; pre-state wrong.")
    if "do-set-phase-with-anchor!" in content:
        raise RuntimeError("wr forward: do-set-phase-with-anchor! already in file; pre-state wrong.")
    if "do-add-pending-thread!" in content:
        raise RuntimeError("wr forward: do-add-pending-thread! already in file; pre-state wrong.")
    return content.replace(WR_ANCHOR, WR_NEW_BLOCK, 1)


def simulate_wr_reverse(content: str) -> str:
    if find_target_substring_count(content, WR_NEW_BLOCK) != 1:
        raise RuntimeError("wr reverse: WR_NEW_BLOCK not found exactly once.")
    return content.replace(WR_NEW_BLOCK, WR_ANCHOR, 1)


# ============================================================================
# DIFF PREVIEW
# ============================================================================

def diff_preview(old: str, new: str, label: str, context: int = 2) -> str:
    """Show first changed region with context."""
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
# STATE CHECKS
# ============================================================================

def ts_forward_state_ok(content: str) -> tuple[bool, str]:
    has_anchor = find_target_substring_count(content, TS_ANCHOR) == 1
    no_new = "count-pending-list" not in content and "count-pending-threads" not in content
    ok = has_anchor and no_new
    msg = f"anchor={has_anchor}, new_absent={no_new} -> {'OK' if ok else 'FAIL'}"
    return ok, msg


def ts_reverse_state_ok(content: str) -> tuple[bool, str]:
    has_new = find_target_substring_count(content, TS_NEW_BLOCK) == 1
    msg = f"new_block_present={has_new} -> {'OK' if has_new else 'FAIL'}"
    return has_new, msg


def wr_forward_state_ok(content: str) -> tuple[bool, str]:
    has_anchor = find_target_substring_count(content, WR_ANCHOR) == 1
    no_validation = "is-valid-anchor-value?" not in content
    no_anchor_skill = "do-set-phase-with-anchor!" not in content
    no_pending_skill = "do-add-pending-thread!" not in content
    ok = has_anchor and no_validation and no_anchor_skill and no_pending_skill
    msg = f"anchor={has_anchor}, new_absent=({no_validation},{no_anchor_skill},{no_pending_skill}) -> {'OK' if ok else 'FAIL'}"
    return ok, msg


def wr_reverse_state_ok(content: str) -> tuple[bool, str]:
    has_new = find_target_substring_count(content, WR_NEW_BLOCK) == 1
    msg = f"new_block_present={has_new} -> {'OK' if has_new else 'FAIL'}"
    return has_new, msg


# ============================================================================
# FILE PROCESSING
# ============================================================================

def process_file(path, bak_path, sim_fwd, sim_rev, expected_line_delta_fwd,
                 args, label, forward_check, reverse_check):
    print(f"\n>>> {label} <<<")
    if not path.exists():
        print(f"  ERROR: {path} not found.")
        return False, "", ""
    content = path.read_text()
    pre_lines = len(content.splitlines())
    pre_o, pre_c = code_aware_paren_count(content)
    pre_d = pre_o - pre_c
    print(f"  Path: {path}")
    print(f"  Pre-edit lines: {pre_lines}")
    c_paren = "OK" if pre_d == 0 else "FAIL"
    print(f"  Pre-edit parens: opens={pre_o} closes={pre_c} delta={pre_d} ({c_paren})")
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
    post_o, post_c = code_aware_paren_count(simulated)
    post_d = post_o - post_c
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
    parser = argparse.ArgumentParser(description="Step 3c wiring: validation + 2 skills + 2 helpers")
    parser.add_argument("--apply", action="store_true",
                        help="Write changes. Default is dry-run.")
    parser.add_argument("--reverse", action="store_true",
                        help="Reverse the edits.")
    args = parser.parse_args()

    direction = "REVERSE" if args.reverse else "APPLY"
    print(f"\n========== STEP 3c WIRING: {direction} ==========")

    # Compute line deltas from the new blocks
    ts_delta = TS_NEW_BLOCK.count("\n") - TS_ANCHOR.count("\n")
    wr_delta = WR_NEW_BLOCK.count("\n") - WR_ANCHOR.count("\n")

    ok_ts, ts_orig, ts_sim = process_file(
        TASK_STATE_PATH, TASK_STATE_BAK,
        simulate_ts_forward, simulate_ts_reverse,
        ts_delta, args, "task_state.metta",
        ts_forward_state_ok, ts_reverse_state_ok,
    )
    if not ok_ts:
        return 1

    ok_wr, wr_orig, wr_sim = process_file(
        WRITERS_PATH, WRITERS_BAK,
        simulate_wr_forward, simulate_wr_reverse,
        wr_delta, args, "task_state_writers.metta",
        wr_forward_state_ok, wr_reverse_state_ok,
    )
    if not ok_wr:
        return 1

    print("\n========== DIFF PREVIEWS ==========")
    print(diff_preview(ts_orig, ts_sim, "task_state.metta", context=2))
    print()
    print(diff_preview(wr_orig, wr_sim, "task_state_writers.metta", context=2))

    if not args.apply:
        print("\n========== DRY-RUN COMPLETE ==========")
        print("All checks pass. Re-run with --apply to write.")
        return 0

    if not args.reverse:
        for path, bak in [(TASK_STATE_PATH, TASK_STATE_BAK),
                          (WRITERS_PATH, WRITERS_BAK)]:
            if bak.exists():
                print(f"WARNING: backup {bak} exists; overwriting.")
            bak.write_text(path.read_text())
            print(f"Backup written: {bak}")

    print("\n========== WRITING ==========")
    TASK_STATE_PATH.write_text(ts_sim)
    print(f"Wrote: {TASK_STATE_PATH}")
    WRITERS_PATH.write_text(wr_sim)
    print(f"Wrote: {WRITERS_PATH}")

    # Disk verification
    print("\n========== DISK VERIFICATION ==========")
    for path, fwd_check, rev_check, label in [
        (TASK_STATE_PATH, ts_forward_state_ok, ts_reverse_state_ok, "task_state.metta"),
        (WRITERS_PATH, wr_forward_state_ok, wr_reverse_state_ok, "task_state_writers.metta"),
    ]:
        disk = path.read_text()
        o, c = code_aware_paren_count(disk)
        d = o - c
        ok_p = d == 0
        print(f"  {label} parens: opens={o} closes={c} delta={d} ({'OK' if ok_p else 'FAIL'})")
        if args.reverse:
            ok, msg = fwd_check(disk)
        else:
            ok, msg = rev_check(disk)
        print(f"  {label} state: {msg}")
        if not ok_p or not ok:
            print("DISK VERIFICATION FAILED.")
            if not args.reverse:
                print(f"Restore: cp {TASK_STATE_BAK} {TASK_STATE_PATH} && cp {WRITERS_BAK} {WRITERS_PATH}")
            return 1

    print("\n========== STEP 3c WIRING COMPLETE ==========")
    if not args.reverse:
        print("\nNext: container rebuild and verify the new skills are callable.")
        print("  docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw && sleep 15 && docker logs clarity_omega 2>&1 | tail -50")
    return 0


if __name__ == "__main__":
    sys.exit(main())
