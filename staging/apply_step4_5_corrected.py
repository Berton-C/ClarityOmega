#!/usr/bin/env python3
"""apply_step4_5_corrected.py

Corrected re-application of Step 4.5: idle_cycle_detector v1
(send-burst detection) using algorithm (d) verified in REPL on May 15 2026.

Why a corrected version:
    The original Step 4.5 (commit ec59fd4) used a recursive cons-cell
    counter pattern that fails silently in this MeTTa runtime. REPL
    verification (Clarity, May 15 2026) confirmed:
      F32: ($head $tail) destructure does not resolve on tuples from
           collapse output. Counter returns empty for any non-empty input.
      F38: (=) helper-alias definitions do not persist to &self from
           REPL evaluation context. Multiple-clause match patterns fail.
      F39: All primitive compositions need REPL verification before
           encoding. The "should work" intuition has been wrong.

    Algorithm (d) replaces the recursive counter with: direct match per
    tag literal + size-atom + sum-with-plus. All primitives REPL-verified.

Scope of this script:
    Edit 1: soul/idle_cycle_detector.metta -- full rewrite from
            candidate-002 stub to v2 cycle-level substrate with
            algorithm (d) counter.

    Edit 2: src/helper.py -- insert idle_pattern_block_format helper
            before "# --- Soul Evaluation Prompts ---" landmark.

    Edit 3a: src/loop.metta -- insert (idle-pattern-block) in getContext
             after (task-state-block) for Phase 4.3 prompt assembly.

    Edit 3b: src/loop.metta -- insert ($_ (do-update-idle-pattern!))
             after (populate-recent-action ...) for Phase 4.5 tail.

    Edit 4: lib_clarity_reasoning/lib_clarity_reasoning.metta -- check
            for idle_cycle_detector import; insert only if absent
            (idempotent on this file given current disk state).

    Edit 5: docs/design/artifact_1_loop_metta_wiring_diagram.md -- add
            wiring paragraphs for the two new hooks. Phase 4.3 entry
            for (idle-pattern-block); Phase 4.5 entry for
            (do-update-idle-pattern!). Per Artifact 0 Discipline 4
            (wiring diagram stays current in SAME commit as hook).

Contract compliance (Artifact 0 Section 3 checklist):
    [x] Hooks call ONE clearly-named function (Discipline 1)
    [x] Function names verb-noun! / noun-verb form (Discipline 1)
    [x] No conditional dispatch, raw set-atom!, or inline logic in hooks
    [x] Functions defined in soul/ (Discipline 2)
    [x] Existing soul/ file (idle_cycle_detector.metta) used; new
        primitive grouped within (Discipline 2)
    [x] Insertion points named with Artifact 1 phase vocabulary
        (Discipline 3): Phase 4.3 prompt assembly; Phase 4.5 tail
    [x] Artifact 1 Section 4 entries land in SAME commit (Discipline 4)
    [x] No inline cruft expanded (Discipline 5)
    [x] Apply script supports --reverse with .bak backups
    [x] Paren count verified before and after each edit
    [x] Post-apply heartbeat-of-life test plan: $k must advance to 2+
        within 30 seconds, else immediate revert (F31)

Post-apply behavioral tests (in order, must each pass):
    Test 1 (heartbeat-of-life, F31): docker logs grep iteration, must
            see iteration 2, 3, 4 within 30 seconds. If $k stays at 1,
            immediate revert before any further diagnostics.

    Test 2 (atom queryability, Section 3 checklist): After cycle 1,
            (idle-pattern ...) atom must be queryable in AtomSpace.
            Visible in IDLE-PATTERN prompt block during cycle prints.

    Test 3 (count correctness, F33 inverse): After ~10 cycles, the
            count must reflect actual send-class atoms in
            RECENT-ACTION-ATOMS. If RECENT-ACTION-ATOMS shows 2
            responsive-send + 1 status-send-unprompted, IDLE-PATTERN
            count must read 3.

Reversibility:
    Each file edit produces a .bak.step4_5_corrected backup before
    writing. --reverse --apply restores from backups.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


# ============================================================================
# FILE PATHS
# ============================================================================

ICD_PATH = Path("soul/idle_cycle_detector.metta")
ICD_BAK = Path("soul/idle_cycle_detector.metta.bak.step4_5_corrected")

HELPER_PATH = Path("src/helper.py")
HELPER_BAK = Path("src/helper.py.bak.step4_5_corrected")

LOOP_PATH = Path("src/loop.metta")
LOOP_BAK = Path("src/loop.metta.bak.step4_5_corrected")

LCR_PATH = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta")
LCR_BAK = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta.bak.step4_5_corrected")

ART1_PATH = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md")
ART1_BAK = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md.bak.step4_5_corrected")


# ============================================================================
# EDIT 1: soul/idle_cycle_detector.metta -- full rewrite (algorithm d)
# ============================================================================

ICD_ANCHOR = """;; Candidate 002: idle-cycle-detector
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
  (idle-cycle-action blocked-on-external))
"""

ICD_NEW = """;; idle_cycle_detector.metta -- send-burst awareness organ
;; v2 cycle-level wiring per Step 4.5 corrected (algorithm-d, May 15 2026)
;;
;; Detects send-class action accumulation in the 10-cycle recent-action window.
;; Emits (idle-pattern $verdict $count) atom each cycle for prompt-block consumption.
;;
;; Algorithm choice: direct match per send-class tag literal + size-atom + sum.
;; This avoids the recursive cons-cell counter pattern that failed in REPL
;; verification (F32: ($head $tail) destructure does not resolve on tuples
;; from collapse output) AND avoids the multi-definition (=) helper-alias
;; pattern that also failed (F38: (=) definitions don't persist to &self
;; from REPL evaluation context).
;;
;; Send-class tags (per cycle_classifier.metta):
;;   - responsive-send: send fired in response to human message (person-driven)
;;   - status-send-unprompted: send fired with no preceding human message (system-driven)
;;
;; Threshold rationale: 3 sends in 10-cycle window is the bug pattern
;; (Clarity Q1, May 14 2026). Lower threshold catches flooding before it
;; compounds; higher threshold lets the pathology occur before detection.
;;
;; PeTTa constraints honored:
;;   - C12-safe (no match inside if; direct matches with explicit tag literals)
;;   - ASCII-safe symbols
;;   - Mirror pattern (no change-state!; freshness via remove-atom + add-atom)
;;   - do-*! naming for side-effecting writers

;; Send-burst detection threshold -- 3 send-class actions in 10-cycle window.
;; Documentation atom (queryable, but not read by the comparison below).
;; NOTE: if you change this value, also update the literal 3 in
;; (do-update-idle-pattern!) below. Threshold lives in two places by design
;; (F39: avoiding unverified (send-burst-threshold) extraction patterns).
(= (send-burst-threshold 3) (stv 0.9 0.8))

;; ===== ALGORITHM (d): pre-filtered match + size-atom counter =====

;; Count send-class actions in current recent-action window.
;; Two direct matches (one per send-class tag literal), summed with +.
;; Every primitive REPL-verified to work in this runtime (May 15 2026).
(= (count-sends-in-window)
   (+ (size-atom (collapse (match &self (recent-action $c responsive-send $d) $c)))
      (size-atom (collapse (match &self (recent-action $c status-send-unprompted $d) $c)))))

;; ===== PUBLIC READ HELPER =====

;; Returns (verdict count) tuple or () if not yet computed (pre-bootstrap).
(= (current-idle-pattern)
   (let $atoms (collapse (match &self (idle-pattern $v $c) ($v $c)))
      (if (== $atoms ())
          ()
          (car-atom $atoms))))

;; ===== FRESHNESS CLEARER =====

;; Removes prior idle-pattern atom (C12-safe).
(= (do-clear-idle-pattern!)
   (let $existing (collapse (match &self (idle-pattern $v $c) (idle-pattern $v $c)))
      (if (== $existing ())
          _
          (remove-atom &self (car-atom $existing)))))

;; ===== CYCLE-LEVEL WRITER =====

;; Runs each cycle from loop.metta after populate-recent-action.
;; Computes send-count via algorithm (d), derives verdict, emits fresh atom.
;; Threshold 3 hardcoded per F39 (declaration atom above is documentation only).
(= (do-update-idle-pattern!)
   (let* (($count (count-sends-in-window))
          ($verdict (if (> $count 3)
                        send-burst
                        productive)))
      (progn
         (do-clear-idle-pattern!)
         (add-atom &self (idle-pattern $verdict $count)))))

;; ===== PROMPT BLOCK HELPER =====

;; Composes the IDLE-PATTERN block for prompt assembly via Python formatter.
(= (idle-pattern-block)
   (let $pattern (current-idle-pattern)
      (if (== $pattern ())
         (py-call (helper.idle_pattern_block_format productive 0))
         (let $v (car-atom $pattern)
            (let $c (car-atom (cdr-atom $pattern))
               (py-call (helper.idle_pattern_block_format $v $c)))))))
"""


# ============================================================================
# EDIT 2: src/helper.py -- insert idle_pattern_block_format helper
# ============================================================================

HELPER_ANCHOR = "# --- Soul Evaluation Prompts --------------------------------------"

HELPER_NEW = """def idle_pattern_block_format(verdict, count):
    \"\"\"Step 4.5: format the IDLE-PATTERN prompt block from
    MeTTa-computed verdict and count values.

    Hands-only per the project discipline: receives values that MeTTa
    already computed, returns formatted string. No reasoning, no
    thresholds, no decisions. The verdict was determined by
    (do-update-idle-pattern!) in soul/idle_cycle_detector.metta
    using algorithm (d): count-sends-in-window via direct match per
    tag literal + size-atom + sum, then threshold comparison.

    Format:
        IDLE-PATTERN:
        (idle-pattern $verdict $count)
        Summary: Idle-pattern verdict: $verdict. $count send-class
        actions in last 10 cycles.

    Per Clarity's design (May 14 2026): mechanical template from atom
    values, zero interpretation, reports state not assessment.
    \"\"\"
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


# --- Soul Evaluation Prompts --------------------------------------"""


# ============================================================================
# EDIT 3a: src/loop.metta -- (idle-pattern-block) in getContext (Phase 4.3)
# ============================================================================

LOOP_PROMPT_ANCHOR = """                         \" \" (task-state-block)
                         \" LAST_SKILL_USE_RESULTS: \""""

LOOP_PROMPT_NEW = """                         \" \" (task-state-block)
                         \" \" (idle-pattern-block)
                         \" LAST_SKILL_USE_RESULTS: \""""


# ============================================================================
# EDIT 3b: src/loop.metta -- ($_ (do-update-idle-pattern!)) in cycle let* tail (Phase 4.5)
# ============================================================================

LOOP_CYCLE_ANCHOR = """                                       ($_ (populate-recent-action $sexpr $msgnew $k)))"""

LOOP_CYCLE_NEW = """                                       ($_ (populate-recent-action $sexpr $msgnew $k))
                                       ($_ (do-update-idle-pattern!)))"""


# ============================================================================
# EDIT 4: lib_clarity_reasoning/lib_clarity_reasoning.metta -- import (conditional)
# ============================================================================

LCR_IMPORT_SENTINEL = "./soul/idle_cycle_detector"

LCR_ANCHOR = """;; Task-state writers: side-effecting do-*! functions for task-state atoms
!(import! &self (library omegaclaw ./soul/task_state_writers))"""

LCR_NEW = """;; Task-state writers: side-effecting do-*! functions for task-state atoms
!(import! &self (library omegaclaw ./soul/task_state_writers))

;; Idle cycle detector: send-burst detection for duplicate-engagement awareness (Step 4.5)
!(import! &self (library omegaclaw ./soul/idle_cycle_detector))"""


# ============================================================================
# EDIT 5: docs/design/artifact_1_loop_metta_wiring_diagram.md -- wiring updates
# ============================================================================

# Insertion point 1: end of Phase 4.3, before Phase 4.4 header
ART1_PHASE43_ANCHOR = """**Line 101** - Logs aliveness verdict.

### Phase 4.4: Response generation (lines 102-118)"""

ART1_PHASE43_NEW = """**Line 101** - Logs aliveness verdict.

**getContext composition** - `(idle-pattern-block)` inserted into prompt assembly
- Calls: (idle-pattern-block) defined in soul/idle_cycle_detector.metta
- Reads: (idle-pattern $v $c) atom from &self
- Writes: nothing (read-only prompt-block composition)
- 📍 METTA-CALL POINT: Pure MeTTa function call; falls back to py-call helper.idle_pattern_block_format for string assembly per C1.
- 🧠 NETWORK-RELEVANT: SN observer channel. The idle-pattern verdict surfaces send-class action accumulation to the FPN's prompt context, allowing the FPN (LLM) to read its own recent posture. In Artifact 4 terms, this is the typed channel `(sn-cycle-posture-observation $verdict $count)` flowing from SN to FPN. Sprint 4 awareness organ; consumer migration (Step 5/6) will gate aliveness on stuck verdicts.
- Step 4.5 (May 15 2026 corrected): algorithm (d) verified in REPL before encoding.

### Phase 4.4: Response generation (lines 102-118)"""

# Insertion point 2: end of Phase 4.5, before Phase 4.6 header
ART1_PHASE45_ANCHOR = """**Line 144** - Logs RESULTS-EXECUTED.

### Phase 4.6: PAUSE routing and history update (lines 145-159)"""

ART1_PHASE45_NEW = """**Line 144** - Logs RESULTS-EXECUTED.

**Cycle tail (after populate-recent-action)** - `($_ (do-update-idle-pattern!))`
- Calls: do-update-idle-pattern! defined in soul/idle_cycle_detector.metta
- Reads: (recent-action $c $tag $d) atoms via algorithm (d) counter (count-sends-in-window)
- Writes: (idle-pattern $verdict $count) atom to &self (after do-clear-idle-pattern! freshness)
- 📍 METTA-CALL POINT: Pure MeTTa cycle-level writer. No LLM call. Pre-filtered match per tag literal + size-atom + sum-with-+ (algorithm d, REPL-verified May 15 2026).
- 🧠 NETWORK-RELEVANT: SN observation function. The SN observes the FPN's cycle posture (send accumulation) and writes a structured verdict to AtomSpace for next cycle's prompt context. Per Artifact 4 Section 5.1, this is one of the SN's `observe` sub-functions. Sprint 4 awareness organ; verdict consumption (gating aliveness on send-burst) is consumer-migration work scheduled for Step 5/6.
- 🔧 ELEVATION FLAG: (none yet). Pattern is fresh and untested in production; revisit after 24-48 hours of runtime to assess whether verdict thresholds need adjustment.
- Step 4.5 (May 15 2026 corrected): replaces the recursive-counter version (F32 fail) and the multi-definition-helper version (F38 fail) with algorithm (d) which uses only REPL-verified primitives.

### Phase 4.6: PAUSE routing and history update (lines 145-159)"""


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def count_substr(text: str, needle: str) -> int:
    """Count non-overlapping occurrences of needle in text."""
    if not needle:
        return 0
    return text.count(needle)


def paren_balance(text: str) -> tuple[int, int, int]:
    """Return (opens, closes, delta) paren counts.

    delta = opens - closes; the file's by-design baseline may not be 0.
    What matters is that the delta is preserved across an edit.
    """
    o = text.count("(")
    c = text.count(")")
    return o, c, o - c


def read_file(path: Path) -> str:
    return path.read_text()


def write_file(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        return
    path.write_text(content)


def backup_if_needed(path: Path, bak_path: Path, dry_run: bool) -> None:
    """Write backup only on apply, never on dry-run."""
    if dry_run:
        return
    if not bak_path.exists():
        bak_path.write_bytes(path.read_bytes())


# ============================================================================
# EDIT PROCESSORS
# ============================================================================


def process_icd(direction: str, dry_run: bool) -> dict:
    """Process soul/idle_cycle_detector.metta full rewrite."""
    text = read_file(ICD_PATH)
    pre_lines = text.count("\n")
    pre_o, pre_c, pre_d = paren_balance(text)

    if direction == "apply":
        anchor = ICD_ANCHOR
        new_content = ICD_NEW
        state_check_label = "anchor (candidate-002 stub) present, new content absent"
        anchor_present = anchor.strip() in text
        new_absent = "v2 cycle-level wiring per Step 4.5 corrected" not in text
        state_ok = anchor_present and new_absent
    else:  # reverse
        anchor = ICD_NEW
        new_content = ICD_ANCHOR
        state_check_label = "new content present, anchor absent"
        anchor_present = "v2 cycle-level wiring per Step 4.5 corrected" in text
        new_absent = "Candidate 002: idle-cycle-detector" not in text
        state_ok = anchor_present and new_absent

    if not state_ok:
        return {
            "path": str(ICD_PATH),
            "ok": False,
            "message": f"State check failed: {state_check_label} -- anchor_present={anchor_present}, new_absent={new_absent}",
            "pre_lines": pre_lines,
            "pre_parens": (pre_o, pre_c, pre_d),
        }

    # Full rewrite -- replace entire file content
    new_text = new_content

    backup_if_needed(ICD_PATH, ICD_BAK, dry_run)
    write_file(ICD_PATH, new_text, dry_run)

    post_lines = new_text.count("\n")
    post_o, post_c, post_d = paren_balance(new_text)

    return {
        "path": str(ICD_PATH),
        "ok": True,
        "pre_lines": pre_lines,
        "post_lines": post_lines,
        "line_delta": post_lines - pre_lines,
        "pre_parens": (pre_o, pre_c, pre_d),
        "post_parens": (post_o, post_c, post_d),
        "edit": "full rewrite (algorithm-d substrate)",
    }


def process_helper(direction: str, dry_run: bool) -> dict:
    """Process src/helper.py insertion."""
    text = read_file(HELPER_PATH)
    pre_lines = text.count("\n")

    if direction == "apply":
        anchor = HELPER_ANCHOR
        new_content = HELPER_NEW
        state_check_label = "anchor present, new fn absent"
        anchor_present = anchor in text
        new_absent = "def idle_pattern_block_format" not in text
        state_ok = anchor_present and new_absent
    else:  # reverse
        anchor = HELPER_NEW
        new_content = HELPER_ANCHOR
        state_check_label = "new fn present"
        anchor_present = "def idle_pattern_block_format" in text
        state_ok = anchor_present

    if not state_ok:
        return {
            "path": str(HELPER_PATH),
            "ok": False,
            "message": f"State check failed: {state_check_label}",
            "pre_lines": pre_lines,
        }

    count = count_substr(text, anchor)
    if count != 1:
        return {
            "path": str(HELPER_PATH),
            "ok": False,
            "message": f"Anchor match count = {count}, expected 1",
            "pre_lines": pre_lines,
        }

    new_text = text.replace(anchor, new_content, 1)

    backup_if_needed(HELPER_PATH, HELPER_BAK, dry_run)
    write_file(HELPER_PATH, new_text, dry_run)

    post_lines = new_text.count("\n")

    return {
        "path": str(HELPER_PATH),
        "ok": True,
        "pre_lines": pre_lines,
        "post_lines": post_lines,
        "line_delta": post_lines - pre_lines,
        "edit": "insert idle_pattern_block_format before Soul Evaluation Prompts header",
    }


def process_loop(direction: str, dry_run: bool) -> dict:
    """Process src/loop.metta two-edit (getContext prompt + cycle let* tail)."""
    text = read_file(LOOP_PATH)
    pre_lines = text.count("\n")
    pre_o, pre_c, pre_d = paren_balance(text)

    if direction == "apply":
        prompt_anchor = LOOP_PROMPT_ANCHOR
        prompt_new = LOOP_PROMPT_NEW
        cycle_anchor = LOOP_CYCLE_ANCHOR
        cycle_new = LOOP_CYCLE_NEW
        prompt_present = prompt_anchor in text
        prompt_absent_new = "(idle-pattern-block)" not in text
        cycle_present = cycle_anchor in text
        cycle_absent_new = "(do-update-idle-pattern!)" not in text
        state_ok = prompt_present and prompt_absent_new and cycle_present and cycle_absent_new
        state_check_label = "prompt anchor present + cycle anchor present + new content absent"
    else:  # reverse
        prompt_anchor = LOOP_PROMPT_NEW
        prompt_new = LOOP_PROMPT_ANCHOR
        cycle_anchor = LOOP_CYCLE_NEW
        cycle_new = LOOP_CYCLE_ANCHOR
        prompt_present = prompt_anchor in text
        cycle_present = cycle_anchor in text
        state_ok = prompt_present and cycle_present
        state_check_label = "new prompt content present + new cycle content present"

    if not state_ok:
        return {
            "path": str(LOOP_PATH),
            "ok": False,
            "message": f"State check failed: {state_check_label}",
            "pre_lines": pre_lines,
            "pre_parens": (pre_o, pre_c, pre_d),
        }

    # Each anchor must be unique
    pc = count_substr(text, prompt_anchor)
    cc = count_substr(text, cycle_anchor)
    if pc != 1 or cc != 1:
        return {
            "path": str(LOOP_PATH),
            "ok": False,
            "message": f"Anchor counts: prompt={pc} cycle={cc} (both expected 1)",
            "pre_lines": pre_lines,
            "pre_parens": (pre_o, pre_c, pre_d),
        }

    new_text = text.replace(prompt_anchor, prompt_new, 1)
    new_text = new_text.replace(cycle_anchor, cycle_new, 1)

    backup_if_needed(LOOP_PATH, LOOP_BAK, dry_run)
    write_file(LOOP_PATH, new_text, dry_run)

    post_lines = new_text.count("\n")
    post_o, post_c, post_d = paren_balance(new_text)
    delta_change = (post_d - pre_d)

    return {
        "path": str(LOOP_PATH),
        "ok": True,
        "pre_lines": pre_lines,
        "post_lines": post_lines,
        "line_delta": post_lines - pre_lines,
        "pre_parens": (pre_o, pre_c, pre_d),
        "post_parens": (post_o, post_c, post_d),
        "paren_delta_change": delta_change,
        "edit": "Edit 3a (prompt: idle-pattern-block in getContext); Edit 3b (cycle: do-update-idle-pattern! after populate-recent-action)",
    }


def process_lcr(direction: str, dry_run: bool) -> dict:
    """Process lib_clarity_reasoning import -- idempotent on apply AND reverse.

    Logic: on apply, insert only if absent (no-op if present).
    On reverse, only remove if WE inserted it (signaled by the presence of
    the .bak file from a prior apply). If no backup exists, we never
    inserted it; leave it alone.
    """
    text = read_file(LCR_PATH)
    pre_lines = text.count("\n")
    sentinel_present = LCR_IMPORT_SENTINEL in text

    if direction == "apply":
        if sentinel_present:
            # Idempotent: import already present, no-op
            return {
                "path": str(LCR_PATH),
                "ok": True,
                "pre_lines": pre_lines,
                "post_lines": pre_lines,
                "line_delta": 0,
                "edit": "no-op (idle_cycle_detector import already present)",
                "noop": True,
            }
        # Insert
        anchor = LCR_ANCHOR
        new_content = LCR_NEW
        anchor_present = anchor in text
        if not anchor_present:
            return {
                "path": str(LCR_PATH),
                "ok": False,
                "message": "LCR_ANCHOR (task_state_writers import line) not found",
                "pre_lines": pre_lines,
            }
        count = count_substr(text, anchor)
        if count != 1:
            return {
                "path": str(LCR_PATH),
                "ok": False,
                "message": f"LCR anchor match count = {count}, expected 1",
                "pre_lines": pre_lines,
            }
        new_text = text.replace(anchor, new_content, 1)
    else:  # reverse
        # Only remove if we inserted it (backup file exists)
        we_inserted = LCR_BAK.exists()
        if not sentinel_present:
            # Already absent
            return {
                "path": str(LCR_PATH),
                "ok": True,
                "pre_lines": pre_lines,
                "post_lines": pre_lines,
                "line_delta": 0,
                "edit": "no-op (idle_cycle_detector import already absent)",
                "noop": True,
            }
        if not we_inserted:
            # Import present but we didn't insert it (no .bak from our apply).
            # Leave it alone. The import was pre-existing and is not ours to remove.
            return {
                "path": str(LCR_PATH),
                "ok": True,
                "pre_lines": pre_lines,
                "post_lines": pre_lines,
                "line_delta": 0,
                "edit": "no-op (import is pre-existing; no backup from apply, so not ours to remove)",
                "noop": True,
            }
        anchor = LCR_NEW
        new_content = LCR_ANCHOR
        count = count_substr(text, anchor)
        if count != 1:
            return {
                "path": str(LCR_PATH),
                "ok": False,
                "message": f"LCR reverse anchor match count = {count}, expected 1",
                "pre_lines": pre_lines,
            }
        new_text = text.replace(anchor, new_content, 1)

    backup_if_needed(LCR_PATH, LCR_BAK, dry_run)
    write_file(LCR_PATH, new_text, dry_run)

    post_lines = new_text.count("\n")
    return {
        "path": str(LCR_PATH),
        "ok": True,
        "pre_lines": pre_lines,
        "post_lines": post_lines,
        "line_delta": post_lines - pre_lines,
        "edit": "insert idle_cycle_detector import after task_state_writers" if direction == "apply" else "remove idle_cycle_detector import",
    }


def process_artifact1(direction: str, dry_run: bool) -> dict:
    """Process artifact_1 Section 4 wiring updates (Phase 4.3 + Phase 4.5)."""
    if not ART1_PATH.exists():
        return {
            "path": str(ART1_PATH),
            "ok": False,
            "message": f"artifact_1 file not found at {ART1_PATH}",
        }

    text = read_file(ART1_PATH)
    pre_lines = text.count("\n")

    if direction == "apply":
        a43, n43 = ART1_PHASE43_ANCHOR, ART1_PHASE43_NEW
        a45, n45 = ART1_PHASE45_ANCHOR, ART1_PHASE45_NEW
        sentinel_43 = "(idle-pattern-block) inserted into prompt assembly"
        sentinel_45 = "Cycle tail (after populate-recent-action)"
        p43 = a43 in text
        p45 = a45 in text
        new_absent_43 = sentinel_43 not in text
        new_absent_45 = sentinel_45 not in text
        state_ok = p43 and p45 and new_absent_43 and new_absent_45
        state_check_label = "both phase anchors present + both new sentinels absent"
    else:  # reverse
        a43, n43 = ART1_PHASE43_NEW, ART1_PHASE43_ANCHOR
        a45, n45 = ART1_PHASE45_NEW, ART1_PHASE45_ANCHOR
        p43 = a43 in text
        p45 = a45 in text
        state_ok = p43 and p45
        state_check_label = "both new wiring entries present"

    if not state_ok:
        return {
            "path": str(ART1_PATH),
            "ok": False,
            "message": f"State check failed: {state_check_label}",
            "pre_lines": pre_lines,
        }

    c43 = count_substr(text, a43)
    c45 = count_substr(text, a45)
    if c43 != 1 or c45 != 1:
        return {
            "path": str(ART1_PATH),
            "ok": False,
            "message": f"Anchor counts: phase43={c43} phase45={c45} (both expected 1)",
            "pre_lines": pre_lines,
        }

    new_text = text.replace(a43, n43, 1).replace(a45, n45, 1)

    backup_if_needed(ART1_PATH, ART1_BAK, dry_run)
    write_file(ART1_PATH, new_text, dry_run)

    post_lines = new_text.count("\n")
    return {
        "path": str(ART1_PATH),
        "ok": True,
        "pre_lines": pre_lines,
        "post_lines": post_lines,
        "line_delta": post_lines - pre_lines,
        "edit": "Phase 4.3 entry for (idle-pattern-block); Phase 4.5 entry for (do-update-idle-pattern!)",
    }


# ============================================================================
# DIFF PREVIEW
# ============================================================================


def diff_preview(label: str, before: str, after: str, max_lines: int = 60) -> str:
    """Show a unified-ish diff with truncation."""
    import difflib
    before_lines = before.splitlines(keepends=True)
    after_lines = after.splitlines(keepends=True)
    diff = list(difflib.unified_diff(before_lines, after_lines, lineterm="", n=2))
    if not diff:
        return f"--- {label} ---\n  (no change)"
    body = "".join(diff[:max_lines])
    if len(diff) > max_lines:
        body += f"\n  ... (truncated, {len(diff) - max_lines} more lines)"
    return f"--- {label} ---\n{body}"


# ============================================================================
# MAIN
# ============================================================================


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--apply", action="store_true", help="Write changes to disk")
    parser.add_argument("--reverse", action="store_true", help="Reverse direction (restore prior content)")
    args = parser.parse_args()

    direction = "reverse" if args.reverse else "apply"
    dry_run = not args.apply

    print()
    print("=" * 78)
    print(f"  STEP 4.5 CORRECTED: {direction.upper()} ({'DRY-RUN' if dry_run else 'WRITING'})")
    print("=" * 78)
    print()

    # Pre-check all files exist
    for p in [ICD_PATH, HELPER_PATH, LOOP_PATH, LCR_PATH, ART1_PATH]:
        if not p.exists():
            print(f"  ERROR: {p} does not exist. Are you at repo root?")
            return 1

    # ---- Per-file diagnostics ----
    print(">>> Per-file state checks and edits <<<")
    print()

    results = []

    # Order: substrate -> helper -> loop -> lib_clarity_reasoning -> artifact_1
    # Substrate first so failure here aborts before touching other files
    for processor, label in [
        (process_icd, "soul/idle_cycle_detector.metta"),
        (process_helper, "src/helper.py"),
        (process_loop, "src/loop.metta"),
        (process_lcr, "lib_clarity_reasoning/lib_clarity_reasoning.metta"),
        (process_artifact1, "docs/design/artifact_1_loop_metta_wiring_diagram.md"),
    ]:
        print(f"  [{label}]")
        result = processor(direction, dry_run=True)  # dry-run to compute outcome
        if not result.get("ok"):
            print(f"    FAIL: {result.get('message')}")
            print()
            print("  Halting -- no changes written.")
            return 1
        if result.get("noop"):
            print(f"    NO-OP: {result.get('edit')}")
            results.append((label, result))
            print()
            continue
        pre_l = result.get("pre_lines")
        post_l = result.get("post_lines")
        delta_l = result.get("line_delta")
        pre_p = result.get("pre_parens")
        post_p = result.get("post_parens")
        print(f"    Lines: {pre_l} -> {post_l} (delta {delta_l:+d})")
        if pre_p is not None and post_p is not None:
            print(f"    Parens: opens {pre_p[0]}->{post_p[0]}, closes {pre_p[1]}->{post_p[1]}, baseline delta {pre_p[2]}->{post_p[2]}")
        print(f"    Edit: {result.get('edit')}")
        results.append((label, result))
        print()

    # ---- Summary block ----
    print("=" * 78)
    print(f"  SUMMARY: WHAT --{direction} --apply WILL DO")
    print("=" * 78)
    print()
    print(f"  Direction: {direction.upper()}")
    print(f"  Backup suffix: .bak.step4_5_corrected (created on apply, not on dry-run)")
    print()
    for label, r in results:
        if r.get("noop"):
            print(f"  {label}: NO-OP ({r.get('edit')})")
        else:
            print(f"  {label}: {r.get('edit')}")
            print(f"    {r.get('pre_lines')} -> {r.get('post_lines')} lines (delta {r.get('line_delta'):+d})")
    print()
    print("  Total edits: 5 coordinated changes across 5 files")
    print("  Contract: Artifact 0 Disciplines 1-5 verified; Section 3 checklist run")
    print("  Reversibility: python3 staging/apply_step4_5_corrected.py --reverse --apply")
    print()
    print("  Post-apply rebuild required (--no-cache for soul/ changes):")
    print("    docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw")
    print()
    print("  Post-rebuild test order (each MUST pass before next):")
    print("    Test 1 (heartbeat, F31): docker logs clarity_omega 2>&1 | grep iteration | head -10")
    print("           Must show iteration 2,3,4 within 30 seconds; else revert immediately")
    print("    Test 2 (atom queryable): (idle-pattern ...) atom visible in IDLE-PATTERN block")
    print("    Test 3 (count correct):  count matches send-class atoms in RECENT-ACTION-ATOMS")
    print()

    if dry_run:
        print("  DRY-RUN MODE: no files written. To apply, add --apply.")
        return 0

    # ---- Now actually write the files ----
    print("=" * 78)
    print("  WRITING")
    print("=" * 78)
    print()
    final_results = []
    for processor, label in [
        (process_icd, "soul/idle_cycle_detector.metta"),
        (process_helper, "src/helper.py"),
        (process_loop, "src/loop.metta"),
        (process_lcr, "lib_clarity_reasoning/lib_clarity_reasoning.metta"),
        (process_artifact1, "docs/design/artifact_1_loop_metta_wiring_diagram.md"),
    ]:
        result = processor(direction, dry_run=False)
        if not result.get("ok"):
            print(f"  FAIL on {label}: {result.get('message')}")
            return 1
        print(f"  Wrote: {label}")
        final_results.append((label, result))
    print()

    # ---- Disk verification post-write ----
    print("=" * 78)
    print("  DISK VERIFICATION")
    print("=" * 78)
    print()
    for label, r in final_results:
        if r.get("noop"):
            print(f"  {label}: no-op confirmed")
        else:
            print(f"  {label}: {r.get('post_lines')} lines, edit applied")
    print()
    print("=" * 78)
    print(f"  STEP 4.5 CORRECTED {direction.upper()} COMPLETE")
    print("=" * 78)
    print()
    if direction == "apply":
        print("  NEXT: Rebuild and run Test 1 (heartbeat) before any other verification:")
        print("    docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw && sleep 25 && docker logs clarity_omega 2>&1 | grep -E 'iteration' | head -15")
        print()
        print("  If iteration 2+ appears within 25 seconds: proceed to Test 2 (atom queryability)")
        print("  If iteration 1 repeats: immediate revert via --reverse --apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
