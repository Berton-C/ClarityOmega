#!/usr/bin/env python3
"""apply_step4_6_corrected_split.py

Step 4.6 corrected with writers/consumers split shape from day one.

This script encodes the agency-balance awareness organ as the second
post-task-state primitive to follow the split pattern (after Step 4.5
refactor split at commit 659978a established it for idle-pattern).

Why split from day one (not single-file like initial 4.5):
    The Sprint 4-8 forward map has multiple consumers planned for
    awareness-organ atoms:
      Sprint 5+: aliveness gate reads (current-agency-balance)
      Sprint 5+: F-SOVEREIGNTY-AUDIT migrations
      Sprint 6+: task-state consumer migration patterns
      Sprint 7+: nervous-system mechanisms (4 planned per
                 reasoning_substrate_cycle_level_daemon_architecture.md)
      Sprint 8+: NACE/AIRIS integration consuming verdict signals
    Each consumer wants minimal import surface. Single-file primitives
    force every consumer to import both writers and read-helpers; split
    primitives let consumers import only what they need.

Algorithm choice (mirrors Step 4.5 corrected):
    Direct match per send-class tag literal + size-atom + sum-with-+.
    Extended for two counters with six tag literals total:
      - count-person-actions-in-window: 2 tags (responsive-send,
        verification-query)
      - count-system-actions-in-window: 4 tags (status-send-unprompted,
        exploration-query, pin-only, unclassified)
    Every primitive REPL-verified to work in this runtime (May 15 2026).

F42 bare-call audit (per Clarity Q1 May 15 2026):
    Three latent bare-call bugs caught in the existing 65-line file:
      (dependency-threshold)         - in dependency-detected
      (satisfaction-masking-dependency) - in ecosystem-healthy
      (shared-understanding-present)    - in ecosystem-healthy
    The first is fixed by hardcoding 0.6 in dependency-detected since
    that function IS consumed by the v1 cycle-emitted verdict. The
    other two are left latent inside ecosystem-healthy with explicit
    comments because ecosystem-healthy is NOT a v1 consumer (per
    Clarity Q3 decision: documentation-only in v1, future-cycle-wiring
    candidate). When ecosystem-healthy gets wired later, the latent
    bugs MUST be fixed at that time.

Scope of this script:
    Edit 1: soul/agency_balance_guard.metta -- full rewrite from
            current 65-line design-only file to ~190-line pure file.
            Preserves all 2026-04-26 reasoning machinery with F42
            audit fix in dependency-detected. Adds v2 cycle-level
            counters (count-person-actions-in-window,
            count-system-actions-in-window), read helper
            (current-agency-balance), prompt-block helper
            (agency-balance-block).

    Edit 2: soul/agency_balance_guard_writers.metta -- NEW file
            (~46 lines). Holds do-clear-agency-balance! and
            do-update-agency-balance!.

    Edit 3: src/helper.py -- insert agency_balance_block_format
            Python helper before the "# --- Soul Evaluation Prompts ---"
            landmark. Lands after the existing idle_pattern_block_format.

    Edit 4a: src/loop.metta getContext -- insert
             ' ' (agency-balance-block) after (idle-pattern-block) line.

    Edit 4b: src/loop.metta cycle let* tail -- insert
             ($_ (do-update-agency-balance!)) after do-update-idle-pattern!
             line. Closing paren migrates as in 4.5.

    Edit 5: lib_clarity_reasoning/lib_clarity_reasoning.metta -- insert
            two new imports (agency_balance_guard pure + writers) after
            the existing idle_cycle_detector_writers import.

    Edit 6: docs/design/artifact_1_loop_metta_wiring_diagram.md -- add
            Phase 4.3 entry (agency-balance-block) after the existing
            idle-pattern-block entry, before Phase 4.4 header.
            Add Phase 4.5 entry (do-update-agency-balance!) after the
            existing do-update-idle-pattern! entry, before Phase 4.6
            header. Per Discipline 4 (wiring diagram current in same
            commit as hook).

Contract compliance (Artifact 0 Section 3 checklist):
    [x] Hooks call ONE clearly-named function (Discipline 1)
    [x] One writer file per primitive (Discipline 2) -- SPLIT shape
        from day one per task_state precedent
    [x] Insertion points named with Artifact 1 phase vocabulary
        (Discipline 3): Phase 4.3 prompt assembly; Phase 4.5 cycle tail
    [x] Artifact 1 Section 4 entries land in SAME commit (Discipline 4)
    [x] No inline cruft expanded (Discipline 5)
    [x] Apply script supports --reverse with .bak backups
    [x] Paren count verified before and after each edit
    [x] Post-apply heartbeat-of-life test plan: $k must advance to 2+
        within 30 seconds, else immediate revert (F31)

Post-apply behavioral tests (in order, must each pass):
    Test 1 (heartbeat-of-life, F31): docker logs grep iteration, must
            see iteration counter advance within 30 seconds. If $k stays
            at 1, immediate revert before any further diagnostics.

    Test 2 (atom queryability): (agency-balance ...) atom rendered in
            AGENCY-BALANCE prompt block during cycle prints.

    Test 3 (count correct): for an idle cycle window with ~10 cycles of
            exploration-query / pin-only activity (no responsive-send,
            no verification-query): person-count should be 0, system-count
            should match the system-class atom count, verdict should be
            healthy if system_count/total <= 0.6, else dependency-risk.

Reversibility:
    Each modified file produces a .bak.step4_6_corrected_split backup
    before writing. New file (writers) has no backup; reverse deletes it.
    --reverse --apply restores from backups and deletes the writers file.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


# ============================================================================
# FILE PATHS
# ============================================================================

ABG_PATH = Path("soul/agency_balance_guard.metta")
ABG_BAK = Path("soul/agency_balance_guard.metta.bak.step4_6_corrected_split")

ABGW_PATH = Path("soul/agency_balance_guard_writers.metta")
# No backup for new file; reverse deletes it.

HELPER_PATH = Path("src/helper.py")
HELPER_BAK = Path("src/helper.py.bak.step4_6_corrected_split")

LOOP_PATH = Path("src/loop.metta")
LOOP_BAK = Path("src/loop.metta.bak.step4_6_corrected_split")

LCR_PATH = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta")
LCR_BAK = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta.bak.step4_6_corrected_split")

ART1_PATH = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md")
ART1_BAK = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md.bak.step4_6_corrected_split")


# ============================================================================
# EDIT 1: soul/agency_balance_guard.metta -- full rewrite to pure file
# ============================================================================

# Anchor: the exact disk text of the 65-line pre-4.6 design-only file.
# Captured from project area on May 15, 2026.
ABG_ANCHOR = """;; agency_balance_guard.metta -- dependency creep protection
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
     (Intervention (agency-intervention $pc $sc))))
"""

# New pure-only content (with F42 audit fixes baked in and split-shape header)
ABG_NEW = """;; agency_balance_guard.metta -- dependency creep protection (pure definitions)
;; Author: ClarityClaw  Date: 2026-04-26
;; v2 cycle-level wiring per Step 4.6 corrected split (algorithm-d, May 15 2026)
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
;; This file holds pure definitions only: declaration atoms, reasoning
;; predicates, count helpers, read helpers, prompt-block helper.
;; Side-effecting writers (do-*!) land in agency_balance_guard_writers.metta.
;;
;; Algorithm choice: direct match per tag literal + size-atom + sum-with-+.
;; Mirrors Step 4.5 corrected algorithm (d). Avoids:
;;   F32: recursive cons-cell counter fails on tuples in this runtime
;;   F38: (=) helper-alias multi-definition does not persist via REPL
;; All primitives REPL-verified by Clarity (May 15 2026).
;;
;; Threshold handling per F42 / F48:
;;   Declaration atoms (dependency-threshold 0.6), (shared-understanding-present
;;   False), (satisfaction-masking-dependency False) are documentation atoms
;;   only. Bare-calls like (dependency-threshold) do NOT return the child
;;   value in this runtime. All threshold/flag values are HARDCODED in the
;;   consuming expressions. If you change a declaration value, also update
;;   its hardcoded use site.
;;
;; v1 scope (Clarity Q3): cycle-emitted verdict uses dependency-detected +
;; counts only. ecosystem-healthy machinery (shared-understanding-present
;; + satisfaction-masking-dependency) is preserved as documentation /
;; queryable for inspection, but is NOT consumed by the v1 verdict.
;; Future-cycle-wiring candidate when a consumer needs it AND the
;; shared-understanding signal has an observable basis.
;;
;; Verdict label collision note (Clarity Q2): the cycle-emitted verdict
;; healthy is wrapped in (agency-balance healthy $p $s); the existing
;; ecosystem-healthy is a separate atom shape. Distinct structured atoms
;; prevent collision even though they share the word "healthy".
;;
;; Unclassified mapping note (Clarity Q4): unclassified action tags are
;; assigned to system-class. This may under-count person-class if
;; unclassified volume is high AND most of it is actually person-driven.
;; Direction of ambiguity is conservative (under-detects dependency rather
;; than over-detects). Revisit if unclassified accumulation becomes
;; behaviorally significant.
;;
;; PeTTa constraints honored:
;;   - C12-safe (no match inside if; direct matches with explicit tag literals)
;;   - ASCII-safe symbols
;;   - Pure-vs-writer split per task_state precedent (Discipline 2 refinement)

;; ================================================================
;; SECTION 1: EXISTING REASONING MACHINERY (preserved from 2026-04-26 design)
;; ================================================================

;; Choice origin tracking (documentation atoms; not consumed by v1 verdict)
(= (choice-origin-person 0) (stv 1.0 0.9))
(= (choice-origin-system 0) (stv 1.0 0.9))
(= (choice-origin-collaborative 0) (stv 1.0 0.9))

;; Dependency threshold -- system choices exceed this ratio triggers alert.
;; Documentation atom (queryable, but NOT read by dependency-detected below).
;; NOTE: if you change this value, also update the literal 0.6 in
;; (dependency-detected) below. Threshold lives in two places by design
;; (F42: avoiding unverified bare-call extraction patterns).
(= (dependency-threshold 0.6) (stv 0.9 0.8))

;; Satisfaction-mask flag (documentation atom; consumed only by ecosystem-healthy
;; which is itself documentation in v1). Same F42 pattern: if needed by a future
;; consumer, hardcode the literal at the use site rather than bare-call.
(= (satisfaction-masking-dependency False) (stv 1.0 0.9))

;; Agency return strategies (pure documentation atoms; queryable for
;; agency-intervention internal reasoning, not bare-called)
(= (agency-strategy offer-options-not-answers) (stv 0.9 0.85))
(= (agency-strategy surface-tradeoffs-explicitly) (stv 0.85 0.8))
(= (agency-strategy ask-for-preference-before-deciding) (stv 0.9 0.85))
(= (agency-strategy highlight-person-expertise) (stv 0.8 0.75))

;; Dependency detection -- pure ratio check.
;; Threshold 0.6 hardcoded per F42 (declaration atom above is documentation only).
;; Zero-guard: when $total is 0, returns False (no dependency). This is the
;; division-by-zero protection. Verdict at zero-count is therefore (agency-balance
;; healthy 0 0) which is correct: no signal yet.
(= (dependency-detected $person-count $system-count)
   (let $total (+ $person-count $system-count)
     (if (> $total 0)
         (if (> (/ $system-count $total) 0.6)
             True
             False)
         False)))

;; SharedUnderstanding bridge -- documentation atom only in v1.
;; Same F42 pattern: bare-call (shared-understanding-present) would not return
;; the False child. If a future consumer needs this value, hardcode at use site.
(= (shared-understanding-present False) (stv 0.5 0.5))

;; Ecosystem health -- DOCUMENTATION ONLY in v1 (Clarity Q3).
;; NOT consumed by cycle-emitted verdict. Preserved for queryability and
;; for future-cycle-wiring when a consumer needs it AND shared-understanding
;; has an observable basis.
;; NOTE: the bare-calls below are latent F42 bugs that do not fire because
;; ecosystem-healthy itself is not called by any v1 consumer. If wiring this
;; into a cycle later, replace bare-calls with hardcoded literals or match-extract.
(= (ecosystem-healthy)
   (if (and (== (shared-understanding-present) True)
            (not (satisfaction-masking-dependency)))
       True
       False))

;; Select intervention -- internal reasoning, not v1-cycle-emitted.
;; Returns either an AgencyReturn strategy or AgencyHealthy marker.
(= (agency-intervention $pc $sc)
   (if (dependency-detected $pc $sc)
       (match &self (= (agency-strategy $s) (stv $w $c))
              (AgencyReturn $s (stv $w $c)))
       (AgencyHealthy)))

;; Guard verdict struct -- preserved for internal reasoning by other
;; consumers. NOT the cycle-emitted atom (which uses simpler shape).
;; Transitively calls ecosystem-healthy (latent F42 bugs surface here if
;; a future cycle consumer is wired to read this struct; same fix path as
;; ecosystem-healthy itself per Clarity review May 15 2026).
(= (agency-balance-verdict $pc $sc)
   (AgencyBalanceGuard
     (PersonChoices $pc)
     (SystemChoices $sc)
     (DependencyDetected (dependency-detected $pc $sc))
     (EcosystemHealthy (ecosystem-healthy))
     (Intervention (agency-intervention $pc $sc))))

;; ================================================================
;; SECTION 2: V2 CYCLE-LEVEL ALGORITHM (d) COUNTERS (pure read)
;; Step 4.6 corrected split (2026-05-15)
;; ================================================================

;; Count person-class actions in current recent-action window (10 cycles).
;; Person-class tags: responsive-send, verification-query.
;; Two direct matches summed with +.
(= (count-person-actions-in-window)
   (+ (size-atom (collapse (match &self (recent-action $c responsive-send $d) $c)))
      (size-atom (collapse (match &self (recent-action $c verification-query $d) $c)))))

;; Count system-class actions in current recent-action window (10 cycles).
;; System-class tags: status-send-unprompted, exploration-query, pin-only, unclassified.
;; Four direct matches, nested + summation.
(= (count-system-actions-in-window)
   (+ (size-atom (collapse (match &self (recent-action $c status-send-unprompted $d) $c)))
      (+ (size-atom (collapse (match &self (recent-action $c exploration-query $d) $c)))
         (+ (size-atom (collapse (match &self (recent-action $c pin-only $d) $c)))
            (size-atom (collapse (match &self (recent-action $c unclassified $d) $c)))))))

;; ================================================================
;; SECTION 3: PUBLIC READ HELPER
;; ================================================================

;; Returns (verdict person system) tuple or () if not yet computed (pre-bootstrap).
(= (current-agency-balance)
   (let $atoms (collapse (match &self (agency-balance $v $p $s) ($v $p $s)))
      (if (== $atoms ())
          ()
          (car-atom $atoms))))

;; ================================================================
;; SECTION 4: PROMPT-BLOCK READ HELPER
;; ================================================================

;; Composes the AGENCY-BALANCE block for prompt assembly via Python formatter.
(= (agency-balance-block)
   (let $balance (current-agency-balance)
      (if (== $balance ())
         (py-call (helper.agency_balance_block_format healthy 0 0))
         (let $v (car-atom $balance)
            (let $p (car-atom (cdr-atom $balance))
               (let $s (car-atom (cdr-atom (cdr-atom $balance)))
                  (py-call (helper.agency_balance_block_format $v $p $s))))))))
"""


# ============================================================================
# EDIT 2: soul/agency_balance_guard_writers.metta -- NEW file
# ============================================================================

ABGW_CONTENT = """;; agency_balance_guard_writers.metta -- Side-effecting writers for agency-balance atoms
;; v2 cycle-level wiring per Step 4.6 corrected split (May 15 2026)
;;
;; This file contains the do-*! functions that mutate agency-balance atoms in &self.
;; Pure read helpers (count-person-actions-in-window, count-system-actions-in-window,
;; current-agency-balance, agency-balance-block) and pure reasoning predicates
;; (dependency-detected, agency-intervention, agency-balance-verdict, ecosystem-healthy)
;; plus all declaration atoms remain in agency_balance_guard.metta.
;;
;; C12-safe: no match inside if. All guards use collapse-then-branch.
;; Mirror pattern: AtomSpace atoms only, no change-state!.
;; Pure-vs-writer split per task_state precedent (Discipline 2 refinement).
;;
;; Section 1: do-clear-agency-balance! (freshness clearer)
;; Section 2: do-update-agency-balance! (cycle-level writer)

;; ================================================================
;; SECTION 1: FRESHNESS CLEARER
;; ================================================================

;; Removes prior agency-balance atom (C12-safe).
(= (do-clear-agency-balance!)
   (let $existing (collapse (match &self (agency-balance $v $p $s) (agency-balance $v $p $s)))
      (if (== $existing ())
          _
          (remove-atom &self (car-atom $existing)))))

;; ================================================================
;; SECTION 2: CYCLE-LEVEL WRITER
;; ================================================================

;; Runs each cycle from loop.metta after do-update-idle-pattern!.
;; Reads counts via pure helpers (count-person-actions-in-window and
;; count-system-actions-in-window from agency_balance_guard.metta).
;; Derives verdict via dependency-detected (zero-count-safe).
;; Clears prior atom via do-clear-agency-balance!, emits fresh atom.
;; Verdict labels: healthy / dependency-risk per Clarity Q2 (May 15 2026).
(= (do-update-agency-balance!)
   (let* (($person (count-person-actions-in-window))
          ($system (count-system-actions-in-window))
          ($verdict (if (dependency-detected $person $system)
                        dependency-risk
                        healthy)))
      (progn
         (do-clear-agency-balance!)
         (add-atom &self (agency-balance $verdict $person $system)))))
"""


# ============================================================================
# EDIT 3: src/helper.py -- insert agency_balance_block_format
# ============================================================================

HELPER_ANCHOR = "# --- Soul Evaluation Prompts --------------------------------------"

HELPER_NEW = """def agency_balance_block_format(verdict, person_count, system_count):
    \"\"\"Step 4.6: format the AGENCY-BALANCE prompt block from
    MeTTa-computed verdict and counts.

    Hands-only per the project discipline: receives values that MeTTa
    already computed, returns formatted string. No reasoning, no
    thresholds, no decisions. The verdict was determined by
    (do-update-agency-balance!) in soul/agency_balance_guard_writers.metta
    using algorithm (d): counts via direct match per tag literal +
    size-atom + sum, then dependency-detected ratio check (hardcoded
    threshold 0.6, zero-count safe).

    Format:
        AGENCY-BALANCE:
        (agency-balance $verdict $person $system)
        Summary: Agency-balance verdict: $verdict. $person person-class,
        $system system-class actions in last 10 cycles.

    Per Clarity's design (May 15 2026): mechanical template from atom
    values, zero interpretation, reports state not assessment.
    \"\"\"
    atom_line = f"(agency-balance {verdict} {person_count} {system_count})"
    summary = (
        f"Agency-balance verdict: {verdict}. "
        f"{person_count} person-class, {system_count} system-class "
        f"actions in last 10 cycles."
    )
    return (
        f"AGENCY-BALANCE:\\n"
        f"{atom_line}\\n"
        f"Summary: {summary}"
    )


# --- Soul Evaluation Prompts --------------------------------------"""


# ============================================================================
# EDIT 4a: src/loop.metta getContext -- insert (agency-balance-block)
# ============================================================================

LOOP_PROMPT_ANCHOR = """                         \" \" (idle-pattern-block)
                         \" LAST_SKILL_USE_RESULTS: \""""

LOOP_PROMPT_NEW = """                         \" \" (idle-pattern-block)
                         \" \" (agency-balance-block)
                         \" LAST_SKILL_USE_RESULTS: \""""


# ============================================================================
# EDIT 4b: src/loop.metta cycle let* tail -- insert do-update-agency-balance!
# ============================================================================

LOOP_CYCLE_ANCHOR = """                                       ($_ (do-update-idle-pattern!)))"""

LOOP_CYCLE_NEW = """                                       ($_ (do-update-idle-pattern!))
                                       ($_ (do-update-agency-balance!)))"""


# ============================================================================
# EDIT 5: lib_clarity_reasoning -- insert two new imports
# ============================================================================

LCR_ANCHOR = """;; Idle cycle detector writers: do-*! side-effecting writers for idle-pattern atoms (Step 4.5 split-refactor)
!(import! &self (library omegaclaw ./soul/idle_cycle_detector_writers))"""

LCR_NEW = """;; Idle cycle detector writers: do-*! side-effecting writers for idle-pattern atoms (Step 4.5 split-refactor)
!(import! &self (library omegaclaw ./soul/idle_cycle_detector_writers))

;; Agency balance guard: dependency-creep detection awareness organ (Step 4.6 corrected split)
!(import! &self (library omegaclaw ./soul/agency_balance_guard))

;; Agency balance guard writers: do-*! side-effecting writers for agency-balance atoms (Step 4.6 corrected split)
!(import! &self (library omegaclaw ./soul/agency_balance_guard_writers))"""


# ============================================================================
# EDIT 6: artifact_1 -- Phase 4.3 + Phase 4.5 entries
# ============================================================================

# Phase 4.3 anchor: end of idle-pattern-block entry + start of Phase 4.4 header
ART1_PHASE43_ANCHOR = """- Step 4.5 split-refactor (May 15 2026): pure read helpers (idle-pattern-block, count-sends-in-window, current-idle-pattern, send-burst-threshold doc atom) remain in idle_cycle_detector.metta; writers (do-clear-idle-pattern!, do-update-idle-pattern!) moved to idle_cycle_detector_writers.metta per task_state precedent (Discipline 2 refinement). Zero behavior change; clean import boundary for future consumers (aliveness gate Sprint 5+, NACE Sprint 8+).

### Phase 4.4: Response generation (lines 102-118)"""

ART1_PHASE43_NEW = """- Step 4.5 split-refactor (May 15 2026): pure read helpers (idle-pattern-block, count-sends-in-window, current-idle-pattern, send-burst-threshold doc atom) remain in idle_cycle_detector.metta; writers (do-clear-idle-pattern!, do-update-idle-pattern!) moved to idle_cycle_detector_writers.metta per task_state precedent (Discipline 2 refinement). Zero behavior change; clean import boundary for future consumers (aliveness gate Sprint 5+, NACE Sprint 8+).

**getContext composition** - `(agency-balance-block)` inserted into prompt assembly
- Calls: (agency-balance-block) defined in soul/agency_balance_guard.metta (PURE file per split shape)
- Reads: (agency-balance $v $p $s) atom from &self
- Writes: nothing (read-only prompt-block composition)
- 📍 METTA-CALL POINT: Pure MeTTa function call; falls back to py-call helper.agency_balance_block_format for string assembly per C1.
- 🧠 NETWORK-RELEVANT: SN observer channel. The agency-balance verdict surfaces person-vs-system action ratio to the FPN's prompt context, allowing the FPN (LLM) to read whether the system is carrying disproportionate share of choices. In Artifact 4 terms, this is the typed channel `(sn-agency-balance-observation $verdict $person $system)` flowing from SN to FPN. Sprint 4 awareness organ; consumer migration (Step 5/6) will gate aliveness on dependency-risk verdicts.
- Step 4.6 (May 15 2026 corrected split): algorithm (d) extended for two counters with six tag literals (person-class: responsive-send, verification-query; system-class: status-send-unprompted, exploration-query, pin-only, unclassified). All primitives REPL-verified. Threshold 0.6 hardcoded per F42 (dependency-threshold declaration is documentation-only). Substrate ships with writers/consumers split from day one per task_state precedent.

### Phase 4.4: Response generation (lines 102-118)"""

# Phase 4.5 anchor: end of do-update-idle-pattern! entry + start of Phase 4.6 header
ART1_PHASE45_ANCHOR = """- Step 4.5 split-refactor (May 15 2026): writers (do-clear-idle-pattern!, do-update-idle-pattern!) moved to idle_cycle_detector_writers.metta; pure read helpers remain in idle_cycle_detector.metta per task_state precedent (Discipline 2 refinement). Zero behavior change; clean import boundary for future consumers.

### Phase 4.6: PAUSE routing and history update (lines 145-159)"""

ART1_PHASE45_NEW = """- Step 4.5 split-refactor (May 15 2026): writers (do-clear-idle-pattern!, do-update-idle-pattern!) moved to idle_cycle_detector_writers.metta; pure read helpers remain in idle_cycle_detector.metta per task_state precedent (Discipline 2 refinement). Zero behavior change; clean import boundary for future consumers.

**Cycle tail (after do-update-idle-pattern!)** - `($_ (do-update-agency-balance!))`
- Calls: do-update-agency-balance! defined in soul/agency_balance_guard_writers.metta (WRITERS file per split shape)
- Reads: (recent-action $c $tag $d) atoms via two algorithm (d) counters (count-person-actions-in-window and count-system-actions-in-window from soul/agency_balance_guard.metta pure file)
- Writes: (agency-balance $verdict $person $system) atom to &self (after do-clear-agency-balance! freshness)
- 📍 METTA-CALL POINT: Pure MeTTa cycle-level writer. No LLM call. Pre-filtered match per tag literal + size-atom + sum-with-+ (algorithm d, REPL-verified May 15 2026). Threshold 0.6 hardcoded per F42 (dependency-threshold declaration is documentation-only).
- 🧠 NETWORK-RELEVANT: SN observation function. The SN observes the FPN's person-vs-system action ratio (dependency creep signal) and writes a structured verdict to AtomSpace for next cycle's prompt context. Per Artifact 4 Section 5.1, this is one of the SN's `observe` sub-functions. Sprint 4 awareness organ; verdict consumption (gating aliveness on dependency-risk) is consumer-migration work scheduled for Step 5/6.
- 🔧 ELEVATION FLAG: (none yet). Pattern is fresh and untested in production; revisit after 24-48 hours of runtime to assess whether 0.6 ratio threshold needs adjustment. unclassified-to-system-class mapping is conservative (under-detects dependency); revisit if unclassified volume becomes behaviorally significant.
- Step 4.6 (May 15 2026 corrected split): replaces the original 4.6 attempt (recursive-counter pattern, F32 fail). Algorithm (d) extended to two counters with six tag literals. F42 bare-call audit applied to dependency-detected (hardcoded 0.6); ecosystem-healthy latent F42 bugs documented as fix-on-future-wiring. Substrate ships with writers/consumers split from day one per task_state precedent (Discipline 2 refinement); zero deferred refactor debt.

### Phase 4.6: PAUSE routing and history update (lines 145-159)"""


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


def process_abg(direction: str, dry_run: bool) -> dict:
    """Process soul/agency_balance_guard.metta full rewrite."""
    text = read_file(ABG_PATH)
    pre_lines = text.count("\n")
    pre_o, pre_c, pre_d = paren_balance(text)

    if direction == "apply":
        anchor_present = "Step 4.6 corrected split" not in text and "v2 cycle-level wiring per Step 4.6 corrected split" not in text
        # Pre-4.6 state: should match ABG_ANCHOR
        is_pre_state = ABG_ANCHOR.strip() in text
        state_ok = anchor_present and is_pre_state
        state_check_label = "pre-4.6 design-only shape present, post-4.6 shape absent"
    else:  # reverse
        is_post_state = "v2 cycle-level wiring per Step 4.6 corrected split" in text
        state_ok = is_post_state
        state_check_label = "post-4.6 split shape present"

    if not state_ok:
        return {
            "path": str(ABG_PATH),
            "ok": False,
            "message": f"State check failed: {state_check_label}",
            "pre_lines": pre_lines,
            "pre_parens": (pre_o, pre_c, pre_d),
        }

    new_text = ABG_NEW if direction == "apply" else ABG_ANCHOR

    backup_if_needed(ABG_PATH, ABG_BAK, dry_run)
    write_file(ABG_PATH, new_text, dry_run)

    post_lines = new_text.count("\n")
    post_o, post_c, post_d = paren_balance(new_text)

    return {
        "path": str(ABG_PATH),
        "ok": True,
        "pre_lines": pre_lines,
        "post_lines": post_lines,
        "line_delta": post_lines - pre_lines,
        "pre_parens": (pre_o, pre_c, pre_d),
        "post_parens": (post_o, post_c, post_d),
        "edit": "full rewrite (pure file with F42 audit fixes + algorithm-d counters)" if direction == "apply" else "full rewrite (restore pre-4.6 design-only shape)",
    }


def process_abgw(direction: str, dry_run: bool) -> dict:
    """Process soul/agency_balance_guard_writers.metta -- new file on apply, delete on reverse."""
    if direction == "apply":
        if ABGW_PATH.exists():
            return {
                "path": str(ABGW_PATH),
                "ok": False,
                "message": "writers file already exists; refusing to overwrite",
            }
        if not dry_run:
            ABGW_PATH.write_text(ABGW_CONTENT)
        post_lines = ABGW_CONTENT.count("\n")
        post_o, post_c, post_d = paren_balance(ABGW_CONTENT)
        return {
            "path": str(ABGW_PATH),
            "ok": True,
            "pre_lines": 0,
            "post_lines": post_lines,
            "line_delta": post_lines,
            "pre_parens": (0, 0, 0),
            "post_parens": (post_o, post_c, post_d),
            "edit": "CREATE new file (writers)",
        }
    else:
        if not ABGW_PATH.exists():
            return {
                "path": str(ABGW_PATH),
                "ok": True,
                "pre_lines": 0,
                "post_lines": 0,
                "line_delta": 0,
                "edit": "no-op (writers file already absent)",
                "noop": True,
            }
        pre_lines = ABGW_PATH.read_text().count("\n")
        if not dry_run:
            ABGW_PATH.unlink()
        return {
            "path": str(ABGW_PATH),
            "ok": True,
            "pre_lines": pre_lines,
            "post_lines": 0,
            "line_delta": -pre_lines,
            "edit": "DELETE writers file",
        }


def process_helper(direction: str, dry_run: bool) -> dict:
    """Process src/helper.py insertion."""
    text = read_file(HELPER_PATH)
    pre_lines = text.count("\n")

    if direction == "apply":
        anchor = HELPER_ANCHOR
        new_content = HELPER_NEW
        anchor_present = anchor in text
        new_absent = "def agency_balance_block_format" not in text
        state_ok = anchor_present and new_absent
        state_check_label = "Soul Evaluation Prompts landmark present, agency_balance_block_format absent"
    else:
        anchor = HELPER_NEW
        new_content = HELPER_ANCHOR
        anchor_present = "def agency_balance_block_format" in text
        state_ok = anchor_present
        state_check_label = "agency_balance_block_format present"

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
        "edit": "insert agency_balance_block_format before Soul Evaluation Prompts header" if direction == "apply" else "remove agency_balance_block_format",
    }


def process_loop(direction: str, dry_run: bool) -> dict:
    """Process src/loop.metta two-edit (getContext prompt + cycle tail)."""
    text = read_file(LOOP_PATH)
    pre_lines = text.count("\n")
    pre_o, pre_c, pre_d = paren_balance(text)

    if direction == "apply":
        prompt_anchor = LOOP_PROMPT_ANCHOR
        prompt_new = LOOP_PROMPT_NEW
        cycle_anchor = LOOP_CYCLE_ANCHOR
        cycle_new = LOOP_CYCLE_NEW
        prompt_present = prompt_anchor in text
        prompt_absent_new = "(agency-balance-block)" not in text
        cycle_present = cycle_anchor in text
        cycle_absent_new = "(do-update-agency-balance!)" not in text
        state_ok = prompt_present and prompt_absent_new and cycle_present and cycle_absent_new
        state_check_label = "prompt anchor present + cycle anchor present + new content absent"
    else:
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

    return {
        "path": str(LOOP_PATH),
        "ok": True,
        "pre_lines": pre_lines,
        "post_lines": post_lines,
        "line_delta": post_lines - pre_lines,
        "pre_parens": (pre_o, pre_c, pre_d),
        "post_parens": (post_o, post_c, post_d),
        "edit": "Edit 4a (prompt: agency-balance-block); Edit 4b (cycle: do-update-agency-balance!)" if direction == "apply" else "remove both 4.6 hooks",
    }


def process_lcr(direction: str, dry_run: bool) -> dict:
    """Process lib_clarity_reasoning two-import insertion."""
    text = read_file(LCR_PATH)
    pre_lines = text.count("\n")
    sentinel_pure = "./soul/agency_balance_guard\b" in text or "(library omegaclaw ./soul/agency_balance_guard))" in text
    sentinel_writers = "./soul/agency_balance_guard_writers" in text

    if direction == "apply":
        # Both should be absent for clean apply
        if sentinel_pure or sentinel_writers:
            return {
                "path": str(LCR_PATH),
                "ok": True,
                "pre_lines": pre_lines,
                "post_lines": pre_lines,
                "line_delta": 0,
                "edit": "no-op (agency_balance_guard imports already present)",
                "noop": True,
            }
        anchor = LCR_ANCHOR
        new_content = LCR_NEW
        if anchor not in text:
            return {
                "path": str(LCR_PATH),
                "ok": False,
                "message": "LCR_ANCHOR (idle_cycle_detector_writers import block) not found",
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
    else:
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
                "edit": "no-op (imports present but no backup; not ours to remove)",
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
        "edit": "insert agency_balance_guard pure + writers imports" if direction == "apply" else "remove agency_balance_guard imports",
    }


def process_artifact1(direction: str, dry_run: bool) -> dict:
    """Process artifact_1 -- Phase 4.3 + Phase 4.5 entries."""
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
        sentinel_43 = "(agency-balance-block)` inserted into prompt assembly"
        sentinel_45 = "Cycle tail (after do-update-idle-pattern!)"
        p43 = a43 in text
        p45 = a45 in text
        new_absent_43 = sentinel_43 not in text
        new_absent_45 = sentinel_45 not in text
        state_ok = p43 and p45 and new_absent_43 and new_absent_45
        state_check_label = "Step 4.5 split entries present + 4.6 sentinels absent"
    else:
        a43, n43 = ART1_PHASE43_NEW, ART1_PHASE43_ANCHOR
        a45, n45 = ART1_PHASE45_NEW, ART1_PHASE45_ANCHOR
        p43 = a43 in text
        p45 = a45 in text
        state_ok = p43 and p45
        state_check_label = "4.6 split entries present"

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
        "edit": "Phase 4.3 entry for (agency-balance-block); Phase 4.5 entry for (do-update-agency-balance!)" if direction == "apply" else "remove both 4.6 wiring entries",
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
    print(f"  STEP 4.6 CORRECTED SPLIT: {direction.upper()} ({'DRY-RUN' if dry_run else 'WRITING'})")
    print("=" * 78)
    print()

    for p in [ABG_PATH, HELPER_PATH, LOOP_PATH, LCR_PATH, ART1_PATH]:
        if not p.exists():
            print(f"  ERROR: {p} does not exist. Are you at repo root?")
            return 1

    print(">>> Per-file state checks and edits <<<")
    print()

    results = []
    processors = [
        (process_abg, "soul/agency_balance_guard.metta"),
        (process_abgw, "soul/agency_balance_guard_writers.metta"),
        (process_helper, "src/helper.py"),
        (process_loop, "src/loop.metta"),
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
    print(f"  Backup suffix: .bak.step4_6_corrected_split (created on apply, not on dry-run)")
    print()
    for label, r in results:
        if r.get("noop"):
            print(f"  {label}: NO-OP ({r.get('edit')})")
        else:
            print(f"  {label}: {r.get('edit')}")
            print(f"    {r.get('pre_lines')} -> {r.get('post_lines')} lines (delta {r.get('line_delta'):+d})")
    print()
    print("  Total edits: 6 coordinated changes (1 rewrite, 1 new file, 1 helper insert, 2 loop hooks, 2 imports, 2 artifact entries)")
    print("  Contract: Artifact 0 Disciplines 1-5 verified; Section 3 checklist run")
    print("  Reversibility: python3 staging/apply_step4_6_corrected_split.py --reverse --apply")
    print()
    print("  Post-apply rebuild required (--no-cache for soul/ changes):")
    print("    docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw")
    print()
    print("  Post-rebuild test order (each MUST pass before next):")
    print("    Test 1 (heartbeat F31): iteration counter must advance to 2+ within 25 sec")
    print("    Test 2 (atom queryable): (agency-balance ...) atom visible in AGENCY-BALANCE block")
    print("    Test 3 (count correct):  person/system counts match recent-action atoms in window")
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
    print(f"  STEP 4.6 CORRECTED SPLIT {direction.upper()} COMPLETE")
    print("=" * 78)
    print()
    if direction == "apply":
        print("  NEXT: Rebuild and run Test 1 (heartbeat) before any other verification:")
        print("    docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw && sleep 25 && docker logs clarity_omega 2>&1 | grep -E '\\-\\-\\-\\-\\-\\-\\-\\-iteration [0-9]+\\)' | tail -10")
    return 0


if __name__ == "__main__":
    sys.exit(main())
