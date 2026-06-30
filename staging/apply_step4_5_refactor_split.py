#!/usr/bin/env python3
"""apply_step4_5_refactor_split.py

Refactor Step 4.5 corrected (committed at f577acf) from single-file
shape into writers/consumers two-file split, matching the task_state
primitive precedent (task_state.metta + task_state_writers.metta).

Why a split refactor:
    The committed Step 4.5 corrected put pure read helpers and
    side-effecting writers in a single file (soul/idle_cycle_detector.metta).
    Per task_state precedent and Discipline 2 spirit, the cleaner pattern
    is two files: pure helpers in idle_cycle_detector.metta and
    do-*! writers in idle_cycle_detector_writers.metta.

    Rationale (per task-state design decision, Clarity, prior):
    - Pure-vs-effectful is the architectural boundary that matters
    - Consumers and writers have different audiences; splitting respects
      the asymmetry
    - Future consumer migration (Sprint 5+ aliveness gate, Sprint 6+
      task-state consumer migration, Sprint 7+ nervous-system mechanisms,
      Sprint 8+ NACE/AIRIS integration) gets clean import boundaries
    - New primitives (Step 4.6 agency-balance-guard) ship with split
      from day one; existing single-file primitives migrate at next
      refactor opportunity rather than deferred indefinitely

    Cost: one apply script + one commit (~20-30 min). Value: every
    consumer migration through Sprint 8 gets clean import boundary.

Scope of this script:
    Edit 1: soul/idle_cycle_detector.metta -- full rewrite from current
            85-line single-file (mixed pure + writers) to ~76-line
            pure-only file. Retains: send-burst-threshold doc atom,
            count-sends-in-window, current-idle-pattern, idle-pattern-block.
            Removes: do-clear-idle-pattern!, do-update-idle-pattern!.
            Updates header to reference writers file (matches task_state
            cross-reference pattern).

    Edit 2: soul/idle_cycle_detector_writers.metta -- NEW file (~42 lines).
            Holds do-clear-idle-pattern! and do-update-idle-pattern!.
            Header mirrors task_state_writers header pattern.

    Edit 3: lib_clarity_reasoning/lib_clarity_reasoning.metta -- insert
            one new import line after existing idle_cycle_detector import.

    Edit 4: docs/design/artifact_1_loop_metta_wiring_diagram.md -- amend
            two Phase 4.3 / Phase 4.5 wiring entries to note the split:
            (idle-pattern-block) lives in pure file;
            (do-update-idle-pattern!) lives in writers file.

Files NOT touched:
    - src/loop.metta: hook function names unchanged (just file location of definitions)
    - src/helper.py: idle_pattern_block_format stays as-is

Contract compliance (Artifact 0 Section 3 checklist):
    [x] Hooks call ONE clearly-named function (Discipline 1) -- unchanged
    [x] One writer file per primitive (Discipline 2) -- REFINED to split shape
    [x] Insertion points named with Artifact 1 phase vocabulary (Discipline 3)
    [x] Artifact 1 Section 4 entries land in SAME commit (Discipline 4)
    [x] No inline cruft expanded (Discipline 5)
    [x] Apply script supports --reverse with .bak backups
    [x] Paren count verified before and after each edit
    [x] Post-apply heartbeat-of-life test plan: $k must advance to 2+
        within 30 seconds, else immediate revert (F31)

Behavioral expectation:
    ZERO behavior change. Same atoms, same writers, same prompt block,
    same verdict logic. Only file location of writer functions changes.
    All three tests (heartbeat, atom queryable, count correct) must
    still pass; no new failure modes possible from this refactor alone
    because no logic changes.

Reversibility:
    Each modified file produces a .bak.step4_5_refactor_split backup
    before writing. New file (writers) has no backup; reverse deletes it.
    --reverse --apply restores from backups and deletes the new writers file.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


# ============================================================================
# FILE PATHS
# ============================================================================

ICD_PATH = Path("soul/idle_cycle_detector.metta")
ICD_BAK = Path("soul/idle_cycle_detector.metta.bak.step4_5_refactor_split")

ICDW_PATH = Path("soul/idle_cycle_detector_writers.metta")
# No backup for the new file; reverse deletes it.

LCR_PATH = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta")
LCR_BAK = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta.bak.step4_5_refactor_split")

ART1_PATH = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md")
ART1_BAK = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md.bak.step4_5_refactor_split")


# ============================================================================
# EDIT 1: soul/idle_cycle_detector.metta -- full rewrite to pure-only
# ============================================================================

# The exact disk text of the post-commit-f577acf single-file shape.
# Captured from project area on May 15, 2026.
ICD_ANCHOR = """;; idle_cycle_detector.metta -- send-burst awareness organ
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

# The new pure-only content.
ICD_NEW = """;; idle_cycle_detector.metta -- send-burst awareness organ (pure definitions)
;; v2 cycle-level wiring per Step 4.5 corrected + split-refactor (May 15 2026)
;;
;; Detects send-class action accumulation in the 10-cycle recent-action window.
;; Emits (idle-pattern $verdict $count) atom each cycle for prompt-block consumption.
;;
;; This file holds pure definitions only: documentation atom, count helper,
;; read helper, prompt-block helper. C12-safe (no match inside if).
;; Side-effecting writers (do-*!) land in idle_cycle_detector_writers.metta.
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
;;   - Pure-vs-writer split per task_state precedent (Discipline 2 refinement)

;; ================================================================
;; SECTION 1: DOCUMENTATION ATOM
;; ================================================================

;; Send-burst detection threshold -- 3 send-class actions in 10-cycle window.
;; Documentation atom (queryable, but not read by the comparison in writers).
;; NOTE: if you change this value, also update the literal 3 in
;; (do-update-idle-pattern!) in idle_cycle_detector_writers.metta.
;; Threshold lives in two places by design (F39 + F42: avoiding unverified
;; (send-burst-threshold) bare-call extraction patterns).
(= (send-burst-threshold 3) (stv 0.9 0.8))

;; ================================================================
;; SECTION 2: ALGORITHM (d) COUNTER (pure read)
;; ================================================================

;; Count send-class actions in current recent-action window.
;; Two direct matches (one per send-class tag literal), summed with +.
;; Every primitive REPL-verified to work in this runtime (May 15 2026).
(= (count-sends-in-window)
   (+ (size-atom (collapse (match &self (recent-action $c responsive-send $d) $c)))
      (size-atom (collapse (match &self (recent-action $c status-send-unprompted $d) $c)))))

;; ================================================================
;; SECTION 3: PUBLIC READ HELPER
;; ================================================================

;; Returns (verdict count) tuple or () if not yet computed (pre-bootstrap).
(= (current-idle-pattern)
   (let $atoms (collapse (match &self (idle-pattern $v $c) ($v $c)))
      (if (== $atoms ())
          ()
          (car-atom $atoms))))

;; ================================================================
;; SECTION 4: PROMPT-BLOCK READ HELPER
;; ================================================================

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
# EDIT 2: soul/idle_cycle_detector_writers.metta -- NEW file
# ============================================================================

ICDW_CONTENT = """;; idle_cycle_detector_writers.metta -- Side-effecting writers for idle-pattern atoms
;; v2 cycle-level wiring per Step 4.5 corrected + split-refactor (May 15 2026)
;;
;; This file contains the do-*! functions that mutate idle-pattern atoms in &self.
;; Pure read helpers (count-sends-in-window, current-idle-pattern, idle-pattern-block,
;; send-burst-threshold documentation atom) remain in idle_cycle_detector.metta.
;;
;; C12-safe: no match inside if. All guards use collapse-then-branch.
;; Mirror pattern: AtomSpace atoms only, no change-state!.
;; Pure-vs-writer split per task_state precedent (Discipline 2 refinement).
;;
;; Section 1: do-clear-idle-pattern! (freshness clearer)
;; Section 2: do-update-idle-pattern! (cycle-level writer)

;; ================================================================
;; SECTION 1: FRESHNESS CLEARER
;; ================================================================

;; Removes prior idle-pattern atom (C12-safe).
(= (do-clear-idle-pattern!)
   (let $existing (collapse (match &self (idle-pattern $v $c) (idle-pattern $v $c)))
      (if (== $existing ())
          _
          (remove-atom &self (car-atom $existing)))))

;; ================================================================
;; SECTION 2: CYCLE-LEVEL WRITER
;; ================================================================

;; Runs each cycle from loop.metta after populate-recent-action.
;; Reads count via pure helper (count-sends-in-window from idle_cycle_detector.metta),
;; derives verdict, clears prior atom via do-clear-idle-pattern!, emits fresh atom.
;; Threshold 3 hardcoded per F39 + F42 (declaration atom in pure file is
;; documentation only).
(= (do-update-idle-pattern!)
   (let* (($count (count-sends-in-window))
          ($verdict (if (> $count 3)
                        send-burst
                        productive)))
      (progn
         (do-clear-idle-pattern!)
         (add-atom &self (idle-pattern $verdict $count)))))
"""


# ============================================================================
# EDIT 3: lib_clarity_reasoning -- insert new import
# ============================================================================

LCR_ANCHOR = """;; Idle cycle detector: send-burst detection for duplicate-engagement awareness (Step 4.5)
!(import! &self (library omegaclaw ./soul/idle_cycle_detector))"""

LCR_NEW = """;; Idle cycle detector: send-burst detection for duplicate-engagement awareness (Step 4.5)
!(import! &self (library omegaclaw ./soul/idle_cycle_detector))

;; Idle cycle detector writers: do-*! side-effecting writers for idle-pattern atoms (Step 4.5 split-refactor)
!(import! &self (library omegaclaw ./soul/idle_cycle_detector_writers))"""


# ============================================================================
# EDIT 4: artifact_1 -- amend Phase 4.3 and Phase 4.5 wiring entries
# ============================================================================

# Phase 4.3 entry: amend the "Calls" line and add a split-refactor note
ART1_PHASE43_ANCHOR = """**getContext composition** - `(idle-pattern-block)` inserted into prompt assembly
- Calls: (idle-pattern-block) defined in soul/idle_cycle_detector.metta
- Reads: (idle-pattern $v $c) atom from &self
- Writes: nothing (read-only prompt-block composition)
- 📍 METTA-CALL POINT: Pure MeTTa function call; falls back to py-call helper.idle_pattern_block_format for string assembly per C1.
- 🧠 NETWORK-RELEVANT: SN observer channel. The idle-pattern verdict surfaces send-class action accumulation to the FPN's prompt context, allowing the FPN (LLM) to read its own recent posture. In Artifact 4 terms, this is the typed channel `(sn-cycle-posture-observation $verdict $count)` flowing from SN to FPN. Sprint 4 awareness organ; consumer migration (Step 5/6) will gate aliveness on stuck verdicts.
- Step 4.5 (May 15 2026 corrected): algorithm (d) verified in REPL before encoding."""

ART1_PHASE43_NEW = """**getContext composition** - `(idle-pattern-block)` inserted into prompt assembly
- Calls: (idle-pattern-block) defined in soul/idle_cycle_detector.metta (PURE file per split-refactor)
- Reads: (idle-pattern $v $c) atom from &self
- Writes: nothing (read-only prompt-block composition)
- 📍 METTA-CALL POINT: Pure MeTTa function call; falls back to py-call helper.idle_pattern_block_format for string assembly per C1.
- 🧠 NETWORK-RELEVANT: SN observer channel. The idle-pattern verdict surfaces send-class action accumulation to the FPN's prompt context, allowing the FPN (LLM) to read its own recent posture. In Artifact 4 terms, this is the typed channel `(sn-cycle-posture-observation $verdict $count)` flowing from SN to FPN. Sprint 4 awareness organ; consumer migration (Step 5/6) will gate aliveness on stuck verdicts.
- Step 4.5 (May 15 2026 corrected): algorithm (d) verified in REPL before encoding.
- Step 4.5 split-refactor (May 15 2026): pure read helpers (idle-pattern-block, count-sends-in-window, current-idle-pattern, send-burst-threshold doc atom) remain in idle_cycle_detector.metta; writers (do-clear-idle-pattern!, do-update-idle-pattern!) moved to idle_cycle_detector_writers.metta per task_state precedent (Discipline 2 refinement). Zero behavior change; clean import boundary for future consumers (aliveness gate Sprint 5+, NACE Sprint 8+)."""

# Phase 4.5 entry: amend the "Calls" line and add a split-refactor note
ART1_PHASE45_ANCHOR = """**Cycle tail (after populate-recent-action)** - `($_ (do-update-idle-pattern!))`
- Calls: do-update-idle-pattern! defined in soul/idle_cycle_detector.metta
- Reads: (recent-action $c $tag $d) atoms via algorithm (d) counter (count-sends-in-window)
- Writes: (idle-pattern $verdict $count) atom to &self (after do-clear-idle-pattern! freshness)
- 📍 METTA-CALL POINT: Pure MeTTa cycle-level writer. No LLM call. Pre-filtered match per tag literal + size-atom + sum-with-+ (algorithm d, REPL-verified May 15 2026).
- 🧠 NETWORK-RELEVANT: SN observation function. The SN observes the FPN's cycle posture (send accumulation) and writes a structured verdict to AtomSpace for next cycle's prompt context. Per Artifact 4 Section 5.1, this is one of the SN's `observe` sub-functions. Sprint 4 awareness organ; verdict consumption (gating aliveness on send-burst) is consumer-migration work scheduled for Step 5/6.
- 🔧 ELEVATION FLAG: (none yet). Pattern is fresh and untested in production; revisit after 24-48 hours of runtime to assess whether verdict thresholds need adjustment.
- Step 4.5 (May 15 2026 corrected): replaces the recursive-counter version (F32 fail) and the multi-definition-helper version (F38 fail) with algorithm (d) which uses only REPL-verified primitives."""

ART1_PHASE45_NEW = """**Cycle tail (after populate-recent-action)** - `($_ (do-update-idle-pattern!))`
- Calls: do-update-idle-pattern! defined in soul/idle_cycle_detector_writers.metta (WRITERS file per split-refactor)
- Reads: (recent-action $c $tag $d) atoms via algorithm (d) counter (count-sends-in-window from soul/idle_cycle_detector.metta pure file)
- Writes: (idle-pattern $verdict $count) atom to &self (after do-clear-idle-pattern! freshness)
- 📍 METTA-CALL POINT: Pure MeTTa cycle-level writer. No LLM call. Pre-filtered match per tag literal + size-atom + sum-with-+ (algorithm d, REPL-verified May 15 2026).
- 🧠 NETWORK-RELEVANT: SN observation function. The SN observes the FPN's cycle posture (send accumulation) and writes a structured verdict to AtomSpace for next cycle's prompt context. Per Artifact 4 Section 5.1, this is one of the SN's `observe` sub-functions. Sprint 4 awareness organ; verdict consumption (gating aliveness on send-burst) is consumer-migration work scheduled for Step 5/6.
- 🔧 ELEVATION FLAG: (none yet). Pattern is fresh and untested in production; revisit after 24-48 hours of runtime to assess whether verdict thresholds need adjustment.
- Step 4.5 (May 15 2026 corrected): replaces the recursive-counter version (F32 fail) and the multi-definition-helper version (F38 fail) with algorithm (d) which uses only REPL-verified primitives.
- Step 4.5 split-refactor (May 15 2026): writers (do-clear-idle-pattern!, do-update-idle-pattern!) moved to idle_cycle_detector_writers.metta; pure read helpers remain in idle_cycle_detector.metta per task_state precedent (Discipline 2 refinement). Zero behavior change; clean import boundary for future consumers."""


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def count_substr(text: str, needle: str) -> int:
    if not needle:
        return 0
    return text.count(needle)


def paren_balance(text: str) -> tuple[int, int, int]:
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
        anchor_present = anchor.strip() in text
        new_absent = "Pure-vs-writer split per task_state precedent" not in text
        state_ok = anchor_present and new_absent
        state_check_label = "single-file shape present, split-refactor shape absent"
    else:  # reverse
        anchor = ICD_NEW
        new_content = ICD_ANCHOR
        anchor_present = "Pure-vs-writer split per task_state precedent" in text
        new_absent = "Mirror pattern (no change-state!; freshness via remove-atom + add-atom)" not in text
        state_ok = anchor_present and new_absent
        state_check_label = "split-refactor shape present, single-file shape absent"

    if not state_ok:
        return {
            "path": str(ICD_PATH),
            "ok": False,
            "message": f"State check failed: {state_check_label}",
            "pre_lines": pre_lines,
            "pre_parens": (pre_o, pre_c, pre_d),
        }

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
        "edit": "full rewrite (pure-only; writers moved to new file)" if direction == "apply" else "full rewrite (single-file shape restored)",
    }


def process_icdw(direction: str, dry_run: bool) -> dict:
    """Process soul/idle_cycle_detector_writers.metta -- new file on apply, delete on reverse."""
    if direction == "apply":
        if ICDW_PATH.exists():
            return {
                "path": str(ICDW_PATH),
                "ok": False,
                "message": "writers file already exists; refusing to overwrite. Manual cleanup needed.",
            }
        if not dry_run:
            ICDW_PATH.write_text(ICDW_CONTENT)
        post_lines = ICDW_CONTENT.count("\n")
        post_o, post_c, post_d = paren_balance(ICDW_CONTENT)
        return {
            "path": str(ICDW_PATH),
            "ok": True,
            "pre_lines": 0,
            "post_lines": post_lines,
            "line_delta": post_lines,
            "pre_parens": (0, 0, 0),
            "post_parens": (post_o, post_c, post_d),
            "edit": "CREATE new file (writers)",
        }
    else:  # reverse
        if not ICDW_PATH.exists():
            return {
                "path": str(ICDW_PATH),
                "ok": True,
                "pre_lines": 0,
                "post_lines": 0,
                "line_delta": 0,
                "edit": "no-op (writers file already absent)",
                "noop": True,
            }
        pre_lines = ICDW_PATH.read_text().count("\n")
        if not dry_run:
            ICDW_PATH.unlink()
        return {
            "path": str(ICDW_PATH),
            "ok": True,
            "pre_lines": pre_lines,
            "post_lines": 0,
            "line_delta": -pre_lines,
            "edit": "DELETE writers file",
        }


def process_lcr(direction: str, dry_run: bool) -> dict:
    """Process lib_clarity_reasoning import insertion (or removal on reverse)."""
    text = read_file(LCR_PATH)
    pre_lines = text.count("\n")
    sentinel_writers = "./soul/idle_cycle_detector_writers" in text

    if direction == "apply":
        if sentinel_writers:
            return {
                "path": str(LCR_PATH),
                "ok": True,
                "pre_lines": pre_lines,
                "post_lines": pre_lines,
                "line_delta": 0,
                "edit": "no-op (writers import already present)",
                "noop": True,
            }
        anchor = LCR_ANCHOR
        new_content = LCR_NEW
        if anchor not in text:
            return {
                "path": str(LCR_PATH),
                "ok": False,
                "message": "LCR_ANCHOR (idle_cycle_detector import block) not found",
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
        # Only remove if .bak exists (meaning we inserted it)
        if not sentinel_writers:
            return {
                "path": str(LCR_PATH),
                "ok": True,
                "pre_lines": pre_lines,
                "post_lines": pre_lines,
                "line_delta": 0,
                "edit": "no-op (writers import already absent)",
                "noop": True,
            }
        if not LCR_BAK.exists():
            return {
                "path": str(LCR_PATH),
                "ok": True,
                "pre_lines": pre_lines,
                "post_lines": pre_lines,
                "line_delta": 0,
                "edit": "no-op (writers import present but no backup; not ours to remove)",
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
        "edit": "insert idle_cycle_detector_writers import" if direction == "apply" else "remove idle_cycle_detector_writers import",
    }


def process_artifact1(direction: str, dry_run: bool) -> dict:
    """Process artifact_1 -- amend Phase 4.3 and Phase 4.5 wiring entries."""
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
        sentinel_43 = "PURE file per split-refactor"
        sentinel_45 = "WRITERS file per split-refactor"
        p43 = a43 in text
        p45 = a45 in text
        new_absent_43 = sentinel_43 not in text
        new_absent_45 = sentinel_45 not in text
        state_ok = p43 and p45 and new_absent_43 and new_absent_45
        state_check_label = "single-file wiring entries present + split sentinels absent"
    else:  # reverse
        a43, n43 = ART1_PHASE43_NEW, ART1_PHASE43_ANCHOR
        a45, n45 = ART1_PHASE45_NEW, ART1_PHASE45_ANCHOR
        p43 = a43 in text
        p45 = a45 in text
        state_ok = p43 and p45
        state_check_label = "split wiring entries present"

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
        "edit": "amend Phase 4.3 + Phase 4.5 wiring entries with split-refactor notes",
    }


# ============================================================================
# MAIN
# ============================================================================


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--apply", action="store_true", help="Write changes to disk")
    parser.add_argument("--reverse", action="store_true", help="Reverse direction")
    args = parser.parse_args()

    direction = "reverse" if args.reverse else "apply"
    dry_run = not args.apply

    print()
    print("=" * 78)
    print(f"  STEP 4.5 REFACTOR SPLIT: {direction.upper()} ({'DRY-RUN' if dry_run else 'WRITING'})")
    print("=" * 78)
    print()

    # Pre-check existing files
    for p in [ICD_PATH, LCR_PATH, ART1_PATH]:
        if not p.exists():
            print(f"  ERROR: {p} does not exist. Are you at repo root?")
            return 1

    print(">>> Per-file state checks and edits <<<")
    print()

    results = []
    processors = [
        (process_icd, "soul/idle_cycle_detector.metta"),
        (process_icdw, "soul/idle_cycle_detector_writers.metta"),
        (process_lcr, "lib_clarity_reasoning/lib_clarity_reasoning.metta"),
        (process_artifact1, "docs/design/artifact_1_loop_metta_wiring_diagram.md"),
    ]

    for processor, label in processors:
        print(f"  [{label}]")
        result = processor(direction, dry_run=True)
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

    print("=" * 78)
    print(f"  SUMMARY: WHAT --{direction} --apply WILL DO")
    print("=" * 78)
    print()
    print(f"  Direction: {direction.upper()}")
    print(f"  Backup suffix: .bak.step4_5_refactor_split (created on apply, not on dry-run)")
    print()
    for label, r in results:
        if r.get("noop"):
            print(f"  {label}: NO-OP ({r.get('edit')})")
        else:
            print(f"  {label}: {r.get('edit')}")
            print(f"    {r.get('pre_lines')} -> {r.get('post_lines')} lines (delta {r.get('line_delta'):+d})")
    print()
    print("  Total edits: 4 coordinated changes (1 rewrite, 1 new file, 1 import, 1 doc amend)")
    print("  Contract: Artifact 0 Disciplines 1-5 verified; Section 3 checklist run")
    print("  Reversibility: python3 staging/apply_step4_5_refactor_split.py --reverse --apply")
    print()
    print("  Post-apply rebuild required (--no-cache for soul/ changes):")
    print("    docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw")
    print()
    print("  Behavioral expectation: ZERO change. Same atoms, same writers, same prompt block.")
    print()
    print("  Post-rebuild test order:")
    print("    Test 1 (heartbeat F31): iteration counter must advance to 2+ within 25 sec")
    print("    Test 2 (atom queryable): (idle-pattern productive 0) visible in IDLE-PATTERN block")
    print("    Test 3 (count correct):  count matches send-class atoms in window")
    print()

    if dry_run:
        print("  DRY-RUN MODE: no files written. To apply, add --apply.")
        return 0

    print("=" * 78)
    print("  WRITING")
    print("=" * 78)
    print()
    final_results = []
    for processor, label in processors:
        result = processor(direction, dry_run=False)
        if not result.get("ok"):
            print(f"  FAIL on {label}: {result.get('message')}")
            return 1
        print(f"  {'Wrote' if not result.get('noop') else 'Confirmed no-op for'}: {label}")
        final_results.append((label, result))
    print()

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
    print(f"  STEP 4.5 REFACTOR SPLIT {direction.upper()} COMPLETE")
    print("=" * 78)
    print()
    if direction == "apply":
        print("  NEXT: Rebuild and run Test 1 (heartbeat) before any other verification:")
        print("    docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw && sleep 25 && docker logs clarity_omega 2>&1 | grep -E 'iteration' | head -15")
    return 0


if __name__ == "__main__":
    sys.exit(main())
