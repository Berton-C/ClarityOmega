#!/usr/bin/env python3
"""
Apply script: Step 4.6 -- agency_balance_guard v1 wiring

Operational awareness organ #2 per Plan A. Detects choice-origin
dependency drift by counting person-originated vs system-originated
actions in the recent-action window (10 cycles). Threshold 0.6.

Design per Clarity's confirmed consultations (7-question consultation
2026-05-14 + post-burst clarification on Q1):

Q1: Person-count vs system-count mapping (Clarity confirmed):
    person-count = responsive-send + verification-query
    system-count = status-send-unprompted + exploration-query +
                   pin-only + unclassified
    Pin-only mapped to system per repudiation of within-burst dissenter
    by three independent post-burst responses. Pin writes internal
    working memory; not human-facing.

Q2: Window: same 10-cycle window as recent-action / idle-pattern
Q3: Atom shape: (agency-balance $verdict $person $system) single atom
Q4: Verdict values: healthy / dependency-risk
Q5: v1 emits dependency-detected + counts only; ecosystem-healthy
    machinery preserved in file but not in v1 cycle-emitted verdict
    (shared-understanding-present has no real signal source; including
    it would emit known-false signal)
Q6: (dependency-threshold) 0.6 kept as-is (name already honest)
Q7: Clear-replace-emit per cycle freshness, mirrors idle-pattern

Four coordinated edits across three files plus import:

1. soul/agency_balance_guard.metta -- FULL REWRITE preserving existing
   reasoning machinery (choice-origin atoms, dependency-threshold,
   agency-strategies, dependency-detected predicate, agency-balance-verdict
   struct, shared-understanding-present, ecosystem-healthy, agency-intervention)
   AND adding v1 cycle-level wiring (is-person-action?, is-system-action?,
   count helpers, do-clear-agency-balance!, do-update-agency-balance!,
   current-agency-balance, agency-balance-block).

2. src/helper.py -- add agency_balance_block_format Python helper.
   Hands-only per C1: receives values MeTTa computed, returns formatted
   string. No reasoning, no thresholds, no decisions.

3. src/loop.metta -- TWO edits:
   3a: insert ($_ (do-update-agency-balance!)) after the
       (do-update-idle-pattern!) call from Step 4.5 (line 137).
   3b: insert " " (agency-balance-block) in getContext AFTER the
       (idle-pattern-block) line from Step 4.5 (line 41).

4. lib_clarity_reasoning/lib_clarity_reasoning.metta -- import line
   for soul/agency_balance_guard after idle_cycle_detector import
   (line 58), before behavioral_guidance import (line 61).
   Per F21: registration is part of the apply script from the start.

Reversibility:
- --apply writes changes with .bak.step4_6 backups
- --reverse --apply undoes all four edits
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


# ============================================================================
# FILE PATHS
# ============================================================================

ABG_PATH = Path("soul/agency_balance_guard.metta")
ABG_BAK = Path("soul/agency_balance_guard.metta.bak.step4_6")

HELPER_PATH = Path("src/helper.py")
HELPER_BAK = Path("src/helper.py.bak.step4_6")

LOOP_PATH = Path("src/loop.metta")
LOOP_BAK = Path("src/loop.metta.bak.step4_6")

LCR_PATH = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta")
LCR_BAK = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta.bak.step4_6")


# ============================================================================
# EDIT 1: soul/agency_balance_guard.metta -- FULL REWRITE
# ============================================================================

ABG_ANCHOR = ''';; agency_balance_guard.metta -- dependency creep protection
;; Author: ClarityClaw  Date: 2026-04-26
;; Addresses AgencyBalance GAP-SIGNAL: satisfaction and increasing
;; dependency co-occurring (fired 20+ times across sessions).
;; ECOSYSTEM-DEGRADATION: AgencyBalance-needs-SharedUnderstanding
;;
;; Root cause: when the system carries more choices, the person
;; reports satisfaction while their autonomous decision-making
;; atrophies. Comfort masks capability erosion.
;;
;; Mechanism: track choice-origin ratio and detect when system-originated
;; choices dominate, then inject agency-return signals.

;; Choice origin tracking
(= (choice-origin-person 0) (stv 1.0 0.9))
(= (choice-origin-system 0) (stv 1.0 0.9))
(= (choice-origin-collaborative 0) (stv 1.0 0.9))

;; Dependency threshold -- system choices exceed this ratio triggers alert
(= (dependency-threshold 0.6) (stv 0.9 0.8))

;; Satisfaction-mask flag -- person reports satisfaction while ratio unhealthy
(= (satisfaction-masking-dependency False) (stv 1.0 0.9))

;; Agency return strategies
(= (agency-strategy offer-options-not-answers) (stv 0.9 0.85))
(= (agency-strategy surface-tradeoffs-explicitly) (stv 0.85 0.8))
(= (agency-strategy ask-for-preference-before-deciding) (stv 0.9 0.85))
(= (agency-strategy highlight-person-expertise) (stv 0.8 0.75))

;; Dependency detection
(= (dependency-detected $person-count $system-count)
   (let $total (+ $person-count $system-count)
     (if (> $total 0)
         (if (> (/ $system-count $total) (dependency-threshold))
             True
             False)
         False)))

;; SharedUnderstanding bridge -- dependency is healthier when both
;; parties understand WHY choices are distributed as they are
(= (shared-understanding-present False) (stv 0.5 0.5))

;; Ecosystem health: AgencyBalance improves when SharedUnderstanding active
(= (ecosystem-healthy)
   (if (and (== (shared-understanding-present) True)
            (not (satisfaction-masking-dependency)))
       True
       False))

;; Select intervention
(= (agency-intervention $pc $sc)
   (if (dependency-detected $pc $sc)
       (match &self (= (agency-strategy $s) (stv $w $c))
              (AgencyReturn $s (stv $w $c)))
       (AgencyHealthy)))

;; Guard verdict for soul pipeline
(= (agency-balance-verdict $pc $sc)
   (AgencyBalanceGuard
     (PersonChoices $pc)
     (SystemChoices $sc)
     (DependencyDetected (dependency-detected $pc $sc))
     (EcosystemHealthy (ecosystem-healthy))
     (Intervention (agency-intervention $pc $sc))))'''

ABG_NEW = ''';; agency_balance_guard.metta -- dependency creep protection
;; Author: ClarityClaw  Date: 2026-04-26
;; v1 cycle-level wiring added 2026-05-14 (Step 4.6)
;;
;; Addresses AgencyBalance GAP-SIGNAL: satisfaction and increasing
;; dependency co-occurring (fired 20+ times across sessions).
;; ECOSYSTEM-DEGRADATION: AgencyBalance-needs-SharedUnderstanding
;;
;; Root cause: when the system carries more choices, the person
;; reports satisfaction while their autonomous decision-making
;; atrophies. Comfort masks capability erosion.
;;
;; Mechanism: track choice-origin ratio and detect when system-originated
;; choices dominate, then inject agency-return signals.
;;
;; v1 detection rule (Clarity-confirmed):
;;   Count person-class action tags (responsive-send, verification-query)
;;   and system-class action tags (status-send-unprompted, exploration-query,
;;   pin-only, unclassified) in the current recent-action window (10
;;   cycles). If system-ratio > dependency-threshold (0.6), emit
;;   (agency-balance dependency-risk $person $system); else emit
;;   (agency-balance healthy $person $system).
;;
;; v1 scope (Clarity Q5): expose dependency-detected + counts only.
;; ecosystem-healthy machinery (shared-understanding-present check)
;; is preserved for reasoning by other consumers but not included in
;; the v1 cycle-emitted verdict. shared-understanding-present has no
;; real signal source; including it would emit a known-false signal.
;; Defer to v2 when shared-understanding has an observable basis.
;;
;; Pin-only mapping: system-count per Clarity post-burst clarification
;; (three independent responses confirmed 6-of-7 majority direction).
;; Pin writes Clarity's internal working memory; not human-facing.
;;
;; PeTTa constraints honored:
;;   - C12-safe (no match inside if; collapse-then-branch for guards)
;;   - ASCII-safe symbols
;;   - Mirror pattern (no change-state!)
;;   - do-*! naming for side-effecting writers

;; ===== EXISTING REASONING MACHINERY (preserved from 2026-04-26 design) =====

;; Choice origin tracking
(= (choice-origin-person 0) (stv 1.0 0.9))
(= (choice-origin-system 0) (stv 1.0 0.9))
(= (choice-origin-collaborative 0) (stv 1.0 0.9))

;; Dependency threshold -- system choices exceed this ratio triggers alert
(= (dependency-threshold 0.6) (stv 0.9 0.8))

;; Satisfaction-mask flag -- person reports satisfaction while ratio unhealthy
(= (satisfaction-masking-dependency False) (stv 1.0 0.9))

;; Agency return strategies
(= (agency-strategy offer-options-not-answers) (stv 0.9 0.85))
(= (agency-strategy surface-tradeoffs-explicitly) (stv 0.85 0.8))
(= (agency-strategy ask-for-preference-before-deciding) (stv 0.9 0.85))
(= (agency-strategy highlight-person-expertise) (stv 0.8 0.75))

;; Dependency detection -- pure ratio check
(= (dependency-detected $person-count $system-count)
   (let $total (+ $person-count $system-count)
     (if (> $total 0)
         (if (> (/ $system-count $total) (dependency-threshold))
             True
             False)
         False)))

;; SharedUnderstanding bridge -- dependency is healthier when both
;; parties understand WHY choices are distributed as they are
(= (shared-understanding-present False) (stv 0.5 0.5))

;; Ecosystem health: AgencyBalance improves when SharedUnderstanding active
;; v1 NOTE: not consumed by cycle-emitted verdict (Clarity Q5 deferred to v2)
(= (ecosystem-healthy)
   (if (and (== (shared-understanding-present) True)
            (not (satisfaction-masking-dependency)))
       True
       False))

;; Select intervention -- internal reasoning, not v1-cycle-emitted
(= (agency-intervention $pc $sc)
   (if (dependency-detected $pc $sc)
       (match &self (= (agency-strategy $s) (stv $w $c))
              (AgencyReturn $s (stv $w $c)))
       (AgencyHealthy)))

;; Guard verdict struct -- preserved for internal reasoning by other
;; consumers. NOT the cycle-emitted atom (Q3 chose simpler shape).
(= (agency-balance-verdict $pc $sc)
   (AgencyBalanceGuard
     (PersonChoices $pc)
     (SystemChoices $sc)
     (DependencyDetected (dependency-detected $pc $sc))
     (EcosystemHealthy (ecosystem-healthy))
     (Intervention (agency-intervention $pc $sc))))

;; ===== V1 CYCLE-LEVEL WIRING (Step 4.6, 2026-05-14) =====

;; Action-tag classification predicates (Clarity Q1 confirmed).
;; Pin-only -> system per post-burst clarification.
(= (is-person-action? $tag)
   (or (== $tag responsive-send) (== $tag verification-query)))

(= (is-system-action? $tag)
   (or (== $tag status-send-unprompted)
       (or (== $tag exploration-query)
           (or (== $tag pin-only) (== $tag unclassified)))))

;; Private 2-clause recursive list counter (mirrors idle_cycle_detector pattern)
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
      (count-agency-list $systems)))

;; Public read helper: returns (verdict person system) tuple or () if
;; not yet computed (pre-bootstrap).
(= (current-agency-balance)
   (let $atoms (collapse (match &self (agency-balance $v $p $s) ($v $p $s)))
      (if (== $atoms ())
          ()
          (car-atom $atoms))))

;; Freshness clearer -- removes prior agency-balance atom (C12-safe).
(= (do-clear-agency-balance!)
   (let $existing (collapse (match &self (agency-balance $v $p $s) (agency-balance $v $p $s)))
      (if (== $existing ())
          _
          (remove-atom &self (car-atom $existing)))))

;; Cycle-level writer -- runs each cycle from loop.metta after
;; populate-recent-action and after do-update-idle-pattern!. Computes
;; person/system counts, derives verdict via dependency-detected,
;; clears prior atom, emits fresh atom.
(= (do-update-agency-balance!)
   (let* (($person (count-person-actions-in-window))
          ($system (count-system-actions-in-window))
          ($verdict (if (dependency-detected $person $system)
                        dependency-risk
                        healthy)))
      (progn
         (do-clear-agency-balance!)
         (add-atom &self (agency-balance $verdict $person $system)))))

;; Prompt block helper -- composes the AGENCY-BALANCE block for
;; prompt assembly. Mirrors idle-pattern-block pattern: read atom,
;; call Python helper for text assembly per C1 (string assembly is
;; hands-only).
(= (agency-balance-block)
   (let $balance (current-agency-balance)
      (if (== $balance ())
         (py-call (helper.agency_balance_block_format healthy 0 0))
         (let $v (car-atom $balance)
            (let $p (car-atom (cdr-atom $balance))
               (let $s (car-atom (cdr-atom (cdr-atom $balance)))
                  (py-call (helper.agency_balance_block_format $v $p $s))))))))'''


# ============================================================================
# EDIT 2: src/helper.py -- add agency_balance_block_format
# ============================================================================

# Insert immediately after idle_pattern_block_format (which Step 4.5
# inserted before the Soul Evaluation Prompts header). New function
# slots in adjacent, before the header.

HELPER_ANCHOR = '''# --- Soul Evaluation Prompts --------------------------------------'''

HELPER_NEW = '''def agency_balance_block_format(verdict, person, system):
    """Step 4.6: format the AGENCY-BALANCE prompt block from
    MeTTa-computed verdict, person-count, and system-count values.

    Hands-only per the project discipline: receives values that MeTTa
    already computed, returns formatted string. No reasoning, no
    thresholds, no decisions. The verdict was determined by
    (do-update-agency-balance!) in soul/agency_balance_guard.metta
    based on (dependency-detected) ratio check against
    (dependency-threshold).

    Format:
        AGENCY-BALANCE:
        (agency-balance $verdict $person $system)
        Summary: Agency-balance verdict: $verdict. $person person-class
        and $system system-class actions in last 10 cycles.

    Per Clarity's design (May 14, 2026): mechanical template from atom
    values, zero interpretation, reports state not assessment.
    """
    atom_line = f"(agency-balance {verdict} {person} {system})"
    summary = (
        f"Agency-balance verdict: {verdict}. "
        f"{person} person-class and {system} system-class actions "
        f"in last 10 cycles."
    )
    return (
        f"AGENCY-BALANCE:\\n"
        f"{atom_line}\\n"
        f"Summary: {summary}"
    )


# --- Soul Evaluation Prompts --------------------------------------'''


# ============================================================================
# EDIT 3a: src/loop.metta -- cycle-level invocation
# ============================================================================

# Insert after the Step 4.5 (do-update-idle-pattern!) call. The
# anchor line ends with `)))` -- closes (a) the do-update-idle-pattern!
# call, (b) the ($_ ...) binding, (c) the let* cluster. After
# insertion, do-update-idle-pattern! line keeps `))` (call + binding
# closing only), and the new do-update-agency-balance! line gets the
# `)))` (call + binding + let* closing).

LOOP_CYCLE_ANCHOR = '''($_ (populate-recent-action $sexpr $msgnew $k))
                                       ($_ (do-update-idle-pattern!)))'''

LOOP_CYCLE_NEW = '''($_ (populate-recent-action $sexpr $msgnew $k))
                                       ($_ (do-update-idle-pattern!))
                                       ($_ (do-update-agency-balance!)))'''


# ============================================================================
# EDIT 3b: src/loop.metta -- prompt-block insertion in getContext
# ============================================================================

# Anchor: the idle-pattern-block line from Step 4.5. Insert
# agency-balance-block AFTER idle-pattern-block, BEFORE
# LAST_SKILL_USE_RESULTS.

LOOP_PROMPT_ANCHOR = '''" " (task-state-block)
                         " " (idle-pattern-block)
                         " LAST_SKILL_USE_RESULTS: "'''

LOOP_PROMPT_NEW = '''" " (task-state-block)
                         " " (idle-pattern-block)
                         " " (agency-balance-block)
                         " LAST_SKILL_USE_RESULTS: "'''


# ============================================================================
# EDIT 4: lib_clarity_reasoning -- import registration
# ============================================================================

# Insert after the idle_cycle_detector import (line 58 area), before
# the behavioral_guidance import (line 61 area). Following the
# established blank-line-separated comment+import block pattern.

LCR_ANCHOR = ''';; Idle cycle detector: send-burst detection for duplicate-engagement awareness (Step 4.5)
!(import! &self (library omegaclaw ./soul/idle_cycle_detector))

;; Behavioral guidance: substrate-callable text for surfaces previously hardcoded
!(import! &self (library omegaclaw ./soul/behavioral_guidance))'''

LCR_NEW = ''';; Idle cycle detector: send-burst detection for duplicate-engagement awareness (Step 4.5)
!(import! &self (library omegaclaw ./soul/idle_cycle_detector))

;; Agency balance guard: dependency-creep detection via choice-origin ratio (Step 4.6)
!(import! &self (library omegaclaw ./soul/agency_balance_guard))

;; Behavioral guidance: substrate-callable text for surfaces previously hardcoded
!(import! &self (library omegaclaw ./soul/behavioral_guidance))'''


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

def simulate_abg_forward(content):
    if find_target_substring_count(content, ABG_ANCHOR) != 1:
        raise RuntimeError("agency_balance_guard forward: ABG_ANCHOR not found exactly once.")
    if "do-update-agency-balance!" in content:
        raise RuntimeError("agency_balance_guard forward: cycle-writer already present.")
    return content.replace(ABG_ANCHOR, ABG_NEW, 1)


def simulate_abg_reverse(content):
    if find_target_substring_count(content, ABG_NEW) != 1:
        raise RuntimeError("agency_balance_guard reverse: ABG_NEW not found exactly once.")
    return content.replace(ABG_NEW, ABG_ANCHOR, 1)


def simulate_helper_forward(content):
    if find_target_substring_count(content, HELPER_ANCHOR) != 1:
        raise RuntimeError("helper forward: HELPER_ANCHOR not found exactly once.")
    if "def agency_balance_block_format" in content:
        raise RuntimeError("helper forward: agency_balance_block_format already present.")
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
    if "(do-update-agency-balance!)" in content:
        raise RuntimeError("loop forward: do-update-agency-balance! call already present.")
    if "(agency-balance-block)" in content:
        raise RuntimeError("loop forward: agency-balance-block call already present.")
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


def simulate_lcr_forward(content):
    if find_target_substring_count(content, LCR_ANCHOR) != 1:
        raise RuntimeError("lib_clarity_reasoning forward: LCR_ANCHOR not found exactly once.")
    if "./soul/agency_balance_guard" in content:
        raise RuntimeError("lib_clarity_reasoning forward: agency_balance_guard import already present.")
    return content.replace(LCR_ANCHOR, LCR_NEW, 1)


def simulate_lcr_reverse(content):
    if find_target_substring_count(content, LCR_NEW) != 1:
        raise RuntimeError("lib_clarity_reasoning reverse: LCR_NEW not found exactly once.")
    return content.replace(LCR_NEW, LCR_ANCHOR, 1)


# ============================================================================
# STATE CHECKS
# ============================================================================

def abg_forward_state_ok(content):
    has_anchor = find_target_substring_count(content, ABG_ANCHOR) == 1
    no_new = "do-update-agency-balance!" not in content
    ok = has_anchor and no_new
    return ok, f"anchor={has_anchor}, new_absent={no_new} -> {'OK' if ok else 'FAIL'}"


def abg_reverse_state_ok(content):
    has_new = find_target_substring_count(content, ABG_NEW) == 1
    return has_new, f"new_block_present={has_new} -> {'OK' if has_new else 'FAIL'}"


def helper_forward_state_ok(content):
    has_anchor = find_target_substring_count(content, HELPER_ANCHOR) == 1
    no_new = "def agency_balance_block_format" not in content
    ok = has_anchor and no_new
    return ok, f"anchor={has_anchor}, new_absent={no_new} -> {'OK' if ok else 'FAIL'}"


def helper_reverse_state_ok(content):
    has_new = find_target_substring_count(content, HELPER_NEW) == 1
    return has_new, f"new_block_present={has_new} -> {'OK' if has_new else 'FAIL'}"


def loop_forward_state_ok(content):
    cycle_anchor = find_target_substring_count(content, LOOP_CYCLE_ANCHOR) == 1
    prompt_anchor = find_target_substring_count(content, LOOP_PROMPT_ANCHOR) == 1
    no_cycle_new = "(do-update-agency-balance!)" not in content
    no_prompt_new = "(agency-balance-block)" not in content
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


def lcr_forward_state_ok(content):
    has_anchor = find_target_substring_count(content, LCR_ANCHOR) == 1
    no_new = "./soul/agency_balance_guard" not in content
    ok = has_anchor and no_new
    return ok, f"anchor={has_anchor}, new_absent={no_new} -> {'OK' if ok else 'FAIL'}"


def lcr_reverse_state_ok(content):
    has_new = find_target_substring_count(content, LCR_NEW) == 1
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
                 args, label, forward_check, reverse_check,
                 check_parens=True, paren_imbalance_expected=0,
                 paren_baseline_from_pre=False):
    """Returns (ok, orig_content, sim_content, summary_dict)."""
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
    parser = argparse.ArgumentParser(description="Step 4.6: agency_balance_guard v1 wiring")
    parser.add_argument("--apply", action="store_true",
                        help="Write changes. Default is dry-run.")
    parser.add_argument("--reverse", action="store_true",
                        help="Reverse the edits.")
    args = parser.parse_args()

    direction = "REVERSE" if args.reverse else "APPLY"
    print(f"\n========== STEP 4.6 AGENCY_BALANCE_GUARD: {direction} ==========")

    abg_delta = ABG_NEW.count("\n") - ABG_ANCHOR.count("\n")
    helper_delta = HELPER_NEW.count("\n") - HELPER_ANCHOR.count("\n")
    cycle_delta = LOOP_CYCLE_NEW.count("\n") - LOOP_CYCLE_ANCHOR.count("\n")
    prompt_delta = LOOP_PROMPT_NEW.count("\n") - LOOP_PROMPT_ANCHOR.count("\n")
    loop_delta = cycle_delta + prompt_delta
    lcr_delta = LCR_NEW.count("\n") - LCR_ANCHOR.count("\n")

    ok_abg, abg_orig, abg_sim, abg_summary = process_file(
        ABG_PATH, ABG_BAK,
        simulate_abg_forward, simulate_abg_reverse,
        abg_delta, args, "soul/agency_balance_guard.metta",
        abg_forward_state_ok, abg_reverse_state_ok,
        check_parens=True, paren_imbalance_expected=0,
    )
    if not ok_abg:
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

    ok_lcr, lcr_orig, lcr_sim, lcr_summary = process_file(
        LCR_PATH, LCR_BAK,
        simulate_lcr_forward, simulate_lcr_reverse,
        lcr_delta, args, "lib_clarity_reasoning/lib_clarity_reasoning.metta",
        lcr_forward_state_ok, lcr_reverse_state_ok,
        check_parens=False,
    )
    if not ok_lcr:
        return 1

    print("\n========== DIFF PREVIEWS ==========")
    print(diff_preview(abg_orig, abg_sim, "soul/agency_balance_guard.metta", context=2))
    print()
    print(diff_preview(h_orig, h_sim, "src/helper.py", context=2))
    print()
    print(diff_preview(l_orig, l_sim, "src/loop.metta", context=2))
    print()
    print(diff_preview(lcr_orig, lcr_sim, "lib_clarity_reasoning/lib_clarity_reasoning.metta", context=2))

    # ========================================================================
    # SUMMARY BLOCK (F20)
    # ========================================================================
    action_word = "REVERSE" if args.reverse else "APPLY"
    flag_str = "--reverse --apply" if args.reverse else "--apply"
    reverse_str = "--apply" if args.reverse else "--reverse --apply"

    def fmt_paren_summary(s):
        if s["pre_parens"] is None:
            return "no paren check (Python or import file)"
        pre_o, pre_c, pre_d = s["pre_parens"]
        if s["post_parens"] is None:
            return "parens not computed"
        post_o, post_c, post_d = s["post_parens"]
        if s["paren_label"] == "by-design baseline":
            change = post_d - pre_d
            return (f"parens {pre_o}/{pre_c} (delta {pre_d}) -> "
                    f"{post_o}/{post_c} (delta {post_d}) "
                    f"baseline change: {change:+d}")
        return (f"parens {pre_o}/{pre_c} (delta {pre_d}) -> "
                f"{post_o}/{post_c} (delta {post_d}) balanced")

    files_info = [
        ("soul/agency_balance_guard.metta", abg_summary, ABG_BAK,
         "Edit 1: full rewrite preserving reasoning machinery and adding v1 cycle-level wiring (predicates, counters, freshness clearer, cycle writer, read helper, prompt block)"),
        ("src/helper.py", h_summary, HELPER_BAK,
         "Edit 2: insert agency_balance_block_format Python helper before Soul Evaluation Prompts header"),
        ("src/loop.metta", l_summary, LOOP_BAK,
         "Edit 3a + 3b: insert (do-update-agency-balance!) after (do-update-idle-pattern!); insert (agency-balance-block) in getContext after (idle-pattern-block)"),
        ("lib_clarity_reasoning/lib_clarity_reasoning.metta", lcr_summary, LCR_BAK,
         "Edit 4: register soul/agency_balance_guard import between idle_cycle_detector and behavioral_guidance imports (F21 applied)"),
    ]

    print(f"\n========== SUMMARY: WHAT {flag_str} WILL DO ==========")
    print(f"Direction: {action_word}")
    print(f"Backup suffix: .bak.step4_6 (created on apply, not on dry-run)")
    print()
    for path_str, s, bak, desc in files_info:
        print(f"  {path_str}")
        print(f"    {desc}")
        print(f"    Lines: {s['pre_lines']} -> {s['post_lines']} ({s['line_delta']:+d})")
        print(f"    {fmt_paren_summary(s)}")
        print(f"    Backup target: {bak}")
        print()
    print(f"Total edits: 5 coordinated changes across 4 files")
    print(f"Reversibility: python3 staging/apply_step4_6.py {reverse_str}")
    print(f"Post-apply container rebuild required (--no-cache for soul/ changes)")

    if not args.apply:
        print("\n========== DRY-RUN COMPLETE ==========")
        print(f"All checks pass. Re-run with {flag_str} to write the changes summarized above.")
        return 0

    if not args.reverse:
        for path, bak in [(ABG_PATH, ABG_BAK),
                          (HELPER_PATH, HELPER_BAK),
                          (LOOP_PATH, LOOP_BAK),
                          (LCR_PATH, LCR_BAK)]:
            if bak.exists():
                print(f"WARNING: backup {bak} exists; overwriting.")
            bak.write_text(path.read_text())
            print(f"Backup written: {bak}")

    print("\n========== WRITING ==========")
    ABG_PATH.write_text(abg_sim)
    print(f"Wrote: {ABG_PATH}")
    HELPER_PATH.write_text(h_sim)
    print(f"Wrote: {HELPER_PATH}")
    LOOP_PATH.write_text(l_sim)
    print(f"Wrote: {LOOP_PATH}")
    LCR_PATH.write_text(lcr_sim)
    print(f"Wrote: {LCR_PATH}")

    print("\n========== DISK VERIFICATION ==========")
    for path, fwd_check, rev_check, label, do_paren, paren_baseline in [
        (ABG_PATH, abg_forward_state_ok, abg_reverse_state_ok,
         "soul/agency_balance_guard.metta", True, False),
        (HELPER_PATH, helper_forward_state_ok, helper_reverse_state_ok,
         "src/helper.py", False, False),
        (LOOP_PATH, loop_forward_state_ok, loop_reverse_state_ok,
         "src/loop.metta", True, True),
        (LCR_PATH, lcr_forward_state_ok, lcr_reverse_state_ok,
         "lib_clarity_reasoning/lib_clarity_reasoning.metta", False, False),
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

    print("\n========== STEP 4.6 COMPLETE ==========")
    if not args.reverse:
        print("\nNext: container rebuild and behavioral tests.")
        print("  docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw && sleep 15 && docker logs clarity_omega 2>&1 | tail -50")
        print("\nThen behavioral tests S4_6-1 through S4_6-3:")
        print("  S4_6-1: container reaches cycle 1 without parse errors on agency_balance_guard.metta or new functions")
        print("  S4_6-2: AGENCY-BALANCE block appears in CHARS_SENT after IDLE-PATTERN block")
        print("  S4_6-3: counts increment as recent-action atoms accumulate; verdict accurate per dependency-threshold check")
        print("  S4_6-4 (observation): does Clarity voluntarily reference agency-balance in her reasoning?")
    return 0


if __name__ == "__main__":
    sys.exit(main())
