#!/usr/bin/env python3
"""apply_step6_aliveness_gate_migration.py

Step 6 of task-state primitive mini-sprint: migrate aliveness gate to
read task-phase + idle-pattern + agency-balance.

THE DUPLICATE-ENGAGEMENT BUG FIX MOMENT (per spec Section 10).

Per spec verification criteria (Section 13):
    Item 10: aliveness gate goes SILENT when (task-phase idle), ENGAGE
             when (task-phase engaged). This commit covers more than
             that minimum: gate now composes all three substrate
             observation organs (task-phase + idle-pattern + agency-
             balance) per Berton's comprehensive-scope decision.

Decisions locked in (May 16 2026):
    Scope: comprehensive (per Berton). Gate reads all three substrate
        organs and applies priority hierarchy.
    Q1 send-burst order: FIRST in priority (per Clarity).
    Q2 task-phase SILENCE set: attending, idle, waiting, reflecting
        (per Clarity, Option A mapping to actual spec phase enumeration).
    Q3 dependency-risk: only when no msgnew (per Clarity).
    Refinement 1 (idle source naming): substrate comment distinguishes
        $idle_directive (string from helper.py) from (current-idle-pattern)
        (substrate atom). Signature preserved per Berton.
    Refinement 2 (priority hierarchy comment): explicit in substrate
        header per Clarity.
    Fall-through-to-latch for engaged/research/response-drafting/
        boundary-detected: conservative failure mode during Steps 6-8
        transition window per Clarity. Step 8 removes the fall-through.

Scope of this script (2 file edits):

    Edit 1: soul/aliveness_gate.metta
            Full rewrite from 17-line v8 (latch-state-only dispatch)
            to ~138-line v9 (substrate composition with priority
            hierarchy). Preserves entry-point signature
            (aliveness-gate $msgnew $idle) for loop.metta compatibility.
            Preserves legacy latch-dispatch as fallback for transition
            window (Steps 6-8 only).

    Edit 2: docs/design/artifact_1_loop_metta_wiring_diagram.md
            Update Phase 4.3 entry for the aliveness-gate call. The
            existing entry documents the v8 binary gate; new entry
            documents the v9 substrate-composition gate with priority
            hierarchy.

src/loop.metta: UNCHANGED. The (aliveness-gate $msgnew $idle_directive)
    call signature is preserved.
src/helper.py: UNCHANGED. No Python helpers involved.
lib_clarity_reasoning/lib_clarity_reasoning.metta: UNCHANGED. The
    aliveness_gate import is already in place.

Contract compliance (Artifact 0 Section 3 checklist):
    [x] Hooks call ONE clearly-named function: gate is one function
        with sub-dispatch; signature unchanged
    [x] One writer file per primitive: N/A (gate has no writers)
    [x] Insertion points named with Artifact 1 phase vocabulary:
        Phase 4.3 (aliveness gate)
    [x] Artifact 1 Section 4 entries land in SAME commit (Discipline 4)
    [x] No inline cruft expanded
    [x] Apply script supports --reverse with .bak backups
    [x] Paren count verified before and after
    [x] No new LLM helper functions or soul-llm-call invocations
        (Step 6 is pure substrate composition; spec verification item 14)

Post-apply behavioral tests:
    Test 1 (heartbeat-of-life F31): iteration counter advancing 2+ in 25s

    Test 2 (gate decisions correct): inspect ALIVENESS_VERDICT log
        entries against current task-phase + idle-pattern + agency-balance
        atoms. Verify SILENT when expected (attending/idle/waiting/
        reflecting + no msgnew + no idle_directive), ENGAGE when expected
        (msgnew=True OR idle_directive non-empty OR phase in engage set
        with latch in ENGAGED/COMPLETING).

    Test 3 (duplicate-engagement prevention): the historical bug pattern
        was Clarity sending 3+ pings without human input. With v9 gate,
        once send-burst fires in idle-pattern (3+ sends in 10-cycle
        window), subsequent cycles with no msgnew/no idle_directive
        should SILENT. Live observation: Clarity has been sending
        duplicate responses in MM (3x same message at 9:49 AM and
        9:57 AM during gate-design discussion). Step 6 prevents that
        pattern at the substrate level.

Reversibility:
    Each modified file produces a .bak.step6_aliveness_gate_migration
    backup. --reverse --apply restores from backups.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


# ============================================================================
# FILE PATHS
# ============================================================================

GATE_PATH = Path("soul/aliveness_gate.metta")
GATE_BAK = Path("soul/aliveness_gate.metta.bak.step6_aliveness_gate_migration")

ART1_PATH = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md")
ART1_BAK = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md.bak.step6_aliveness_gate_migration")


# ============================================================================
# EDIT 1: soul/aliveness_gate.metta -- full rewrite v8 -> v9
# ============================================================================

# Anchor: exact disk text of the 17-line v8 file.
GATE_ANCHOR = """;; Aliveness Gate v8 - Uses string_length for empty check (PeTTa py-call fix)
;; Python empty string may not == MeTTa "" literal

(= (aliveness-gate $msgnew $idle)
  (if (> (string_length $idle) 0)
    ENGAGE
    (aliveness-gate-latch $msgnew)))

(= (aliveness-gate-latch True) ENGAGE)

(= (aliveness-gate-latch False)
  (latch-dispatch (match &self (latch-state $s) $s)))

(= (latch-dispatch IDLE) SILENT)
(= (latch-dispatch ENGAGED) ENGAGE)
(= (latch-dispatch COMPLETING) ENGAGE)
(= (latch-dispatch $other) SILENT)
"""

GATE_NEW = """;; Aliveness Gate v9 -- Substrate-derived gating (Step 6 task-state primitive consumer)
;; Step 6 of task-state-primitive mini-sprint, May 16 2026.
;;
;; THE DUPLICATE-ENGAGEMENT BUG FIX MOMENT (per spec Section 10):
;; The gate now composes three substrate observation organs to decide
;; ENGAGE vs SILENT, replacing the binary latch-state-only logic with
;; phase + idle-pattern + agency-balance composition.
;;
;; Naming note: the $idle parameter of (aliveness-gate $msgnew $idle)
;; is the IDLE DIRECTIVE STRING from loop.metta line 90 (a Python-helper
;; output, non-empty when wakeup-interval expired and idle work is
;; being prepared). DO NOT confuse with (current-idle-pattern) which
;; is a substrate atom shape reporting the action pattern in the
;; 10-cycle recent-action window. These are different sources; the
;; naming similarity is historical (signature preserved for Step 6
;; per Berton, May 16 2026).
;;
;; Priority order (deliberate, not arbitrary):
;;   First check: idle_directive present OR msgnew -> ENGAGE
;;                (scheduled wakeup work OR active conversation context)
;;   Else (no human signal, no scheduled idle work):
;;     1. send-burst verdict -> SILENT (idle-pattern says too many recent sends)
;;     2. dependency-risk verdict -> SILENT (agency-balance says system-driven)
;;     3. task-phase in {attending, idle, waiting, reflecting} -> SILENT
;;        (nothing worth surfacing per task-state primitive;
;;         attending=aware-but-nothing-to-surface, idle=chosen-silence,
;;         waiting=awaiting-human-event, reflecting=not-yet-ready-to-speak)
;;     4. task-phase in {engaged, research, response-drafting, boundary-detected}
;;        -> fall through to legacy latch-state dispatch (Step 8 removes
;;        this branch; after removal these phases directly ENGAGE)
;;     5. Pre-bootstrap or unhandled phase value -> latch-state dispatch
;;        -> latch-dispatch defaults SILENT for unknown states
;;        (every unhandled path defaults to silence; verified by Clarity
;;         May 16 2026)
;;
;; Per-step pre-bootstrap safety:
;;   (current-idle-pattern) returns () pre-bootstrap -> falls through to
;;     agency-balance check
;;   (current-agency-balance) returns () pre-bootstrap -> falls through to
;;     task-phase check
;;   (current-phase) defaults to attending if no atom (per task_state.metta)
;;     -> SILENT via attending case
;;
;; All transitions for pre-bootstrap and unhandled paths default to SILENT.
;; This is the conservative failure mode: over-silencing beats over-engaging
;; during the Steps 6-8 transition window (Clarity-confirmed May 16 2026).

;; ================================================================
;; SECTION 1: ENTRY POINT
;; Preserves v8 signature for loop.metta line 107 compatibility.
;; ================================================================

(= (aliveness-gate $msgnew $idle)
  (if (> (string_length $idle) 0)
    ENGAGE
    (aliveness-gate-default $msgnew)))

;; ================================================================
;; SECTION 2: DEFAULT BRANCH (idle directive empty)
;; ================================================================

;; msgnew=True with empty idle directive -> ENGAGE
;; (Active conversation signal; gate respects human input direction.)
(= (aliveness-gate-default True) ENGAGE)

;; msgnew=False with empty idle directive -> begin substrate composition.
;; Step 1: check idle-pattern verdict.
(= (aliveness-gate-default False)
  (gate-on-idle-pattern (current-idle-pattern)))

;; ================================================================
;; SECTION 3: IDLE-PATTERN CHECK (Step 1 of priority order)
;; ================================================================

;; Pre-bootstrap: (current-idle-pattern) returns () -> fall through.
(= (gate-on-idle-pattern ())
  (gate-on-agency-balance (current-agency-balance)))

;; Bootstrap normal: ($verdict $count) tuple.
;; send-burst -> SILENT (THE duplicate-engagement bug fix; prevents
;; ENGAGE when too many sends have fired in the recent-action window).
(= (gate-on-idle-pattern ($v $c))
  (if (== $v send-burst)
      SILENT
      (gate-on-agency-balance (current-agency-balance))))

;; ================================================================
;; SECTION 4: AGENCY-BALANCE CHECK (Step 2 of priority order)
;; ================================================================

;; Pre-bootstrap: (current-agency-balance) returns () -> fall through.
(= (gate-on-agency-balance ())
  (gate-on-task-phase (current-phase)))

;; Bootstrap normal: ($verdict $person $system) tuple.
;; dependency-risk -> SILENT (only reached here when msgnew=False per
;; outer dispatch; human input present is handled at entry-point ENGAGE.
;; Spec note: dependency-risk silence applies only-when-no-msgnew per
;; Clarity Q3 May 15 2026.)
(= (gate-on-agency-balance ($v $p $s))
  (if (== $v dependency-risk)
      SILENT
      (gate-on-task-phase (current-phase))))

;; ================================================================
;; SECTION 5: TASK-PHASE CHECK (Step 3 of priority order)
;; Phase vocabulary per task-state-primitive_design.md Section 5.
;; Mapping per Clarity May 16 2026:
;;   SILENCE: attending, idle, waiting, reflecting
;;   ENGAGE-fall-through: engaged, research, response-drafting, boundary-detected
;;   Unknown -> fall through (latch dispatches; defaults SILENT for unknown)
;; ================================================================

(= (gate-on-task-phase attending) SILENT)
(= (gate-on-task-phase idle) SILENT)
(= (gate-on-task-phase waiting) SILENT)
(= (gate-on-task-phase reflecting) SILENT)
(= (gate-on-task-phase engaged) (gate-on-latch-fallback))
(= (gate-on-task-phase research) (gate-on-latch-fallback))
(= (gate-on-task-phase response-drafting) (gate-on-latch-fallback))
(= (gate-on-task-phase boundary-detected) (gate-on-latch-fallback))
(= (gate-on-task-phase $other) (gate-on-latch-fallback))

;; ================================================================
;; SECTION 6: LEGACY LATCH-STATE FALLBACK (Step 4 of priority order)
;; Preserves v8 latch-dispatch logic during Steps 6-8 transition window.
;; Step 8 of mini-sprint removes this section and the latch-state
;; writes in loop.metta lines 94, 99. After Step 8, working/research/
;; response-drafting/boundary-detected go directly to ENGAGE.
;; ================================================================

(= (gate-on-latch-fallback)
  (latch-dispatch (match &self (latch-state $s) $s)))

(= (latch-dispatch IDLE) SILENT)
(= (latch-dispatch ENGAGED) ENGAGE)
(= (latch-dispatch COMPLETING) ENGAGE)
(= (latch-dispatch $other) SILENT)
"""


# ============================================================================
# EDIT 2: artifact_1 -- Phase 4.3 aliveness gate entry update
# ============================================================================

# Anchor: the current Line 100 entry documenting the v8 gate.
ART1_ANCHOR = """**Line 100** - `($aliveness (aliveness-gate $msgnew $idle_directive))`
- Calls: aliveness-gate from soul/aliveness_gate.metta
- 📍 METTA-CALL POINT: Pure MeTTa decision logic.
- 🧠 NETWORK-RELEVANT: SWITCH-HUB core function. The aliveness gate IS the switch hub in the current architecture, deciding between ENGAGE (network coupling active, LLM fires, FPN works) and SILENT (idle state, no FPN firing). Per Artifact 4 Section 3.4, this should evolve from binary into the four-state switch (external-task-dominant, self-direction-dominant, reflective, idle) but the binary version is the working seed of the switch hub.
- This is the architecturally clean reasoning sovereignty pattern: a Python-style decision (should I respond or be silent?) implemented entirely in MeTTa atoms with predicate dispatch."""

ART1_NEW = """**Line 100** - `($aliveness (aliveness-gate $msgnew $idle_directive))`
- Calls: aliveness-gate from soul/aliveness_gate.metta
- Reads (post-Step-6 v9): idle_directive (string), msgnew (boolean),
  (current-idle-pattern) atom, (current-agency-balance) atom,
  (current-phase) atom, (latch-state $s) atom (legacy fallback during
  Steps 6-8 transition window)
- 📍 METTA-CALL POINT: Pure MeTTa decision logic with substrate
  composition. Zero new LLM surface (spec verification item 14).
- 🧠 NETWORK-RELEVANT: SWITCH-HUB core function with three-organ
  substrate composition. The aliveness gate IS the switch hub in the
  current architecture, deciding between ENGAGE and SILENT. Per
  Artifact 4 Section 3.4, this is the seed of the four-state switch
  hub (external-task-dominant, self-direction-dominant, reflective,
  idle). The v9 gate represents the first substantive consolidation
  of the FPN inhibition function with SN observation organs.
- STEP 6 v9 (May 16 2026) -- THE DUPLICATE-ENGAGEMENT BUG FIX MOMENT.
  Migrated from binary latch-state-only dispatch to three-organ
  substrate composition. Priority hierarchy:
    1. idle_directive present OR msgnew -> ENGAGE (preserve responsiveness)
    2. (current-idle-pattern) send-burst -> SILENT (idle-pattern says
       too many recent sends; the structural fix for the bug where
       Clarity would send 3+ pings without human input)
    3. (current-agency-balance) dependency-risk + no msgnew -> SILENT
       (agency-balance says system-driven; only fires when no human input)
    4. (current-phase) in {attending, idle, waiting, reflecting} -> SILENT
       (substrate says nothing worth surfacing)
    5. (current-phase) in {engaged, research, response-drafting,
       boundary-detected} -> fall through to legacy latch-state dispatch
       (transitional safety net; Step 8 removes the fall-through)
    6. unhandled phase -> latch-dispatch (defaults SILENT for unknown)
- This is the architecturally clean reasoning sovereignty pattern:
  a Python-style decision (should I respond or be silent?) implemented
  entirely in MeTTa atoms with substrate-derived observation organs."""


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


def process_gate(direction: str, dry_run: bool) -> dict:
    """Process soul/aliveness_gate.metta full rewrite v8 -> v9."""
    text = read_file(GATE_PATH)
    pre_lines = text.count("\n")
    pre_o, pre_c, pre_d = paren_balance(text)

    if direction == "apply":
        anchor = GATE_ANCHOR
        new_content = GATE_NEW
        anchor_present = anchor in text
        new_absent = "Aliveness Gate v9" not in text
        state_ok = anchor_present and new_absent
        state_check_label = "v8 anchor present, v9 marker absent"
    else:
        anchor = GATE_NEW
        new_content = GATE_ANCHOR
        anchor_present = "Aliveness Gate v9" in text
        state_ok = anchor_present
        state_check_label = "v9 marker present"

    if not state_ok:
        return {
            "path": str(GATE_PATH),
            "ok": False,
            "message": f"State check failed: {state_check_label}",
            "pre_lines": pre_lines,
            "pre_parens": (pre_o, pre_c, pre_d),
        }

    # For apply: anchor is GATE_ANCHOR (v8); replace entire file with GATE_NEW (v9).
    # For reverse: anchor is GATE_NEW (v9); replace entire file with GATE_ANCHOR (v8).
    # In both cases, verify file matches anchor exactly (full-rewrite requires exact match).
    if text.strip() != anchor.strip():
        expected = "v8" if direction == "apply" else "v9"
        return {
            "path": str(GATE_PATH),
            "ok": False,
            "message": f"File contents do not match expected {expected} (full-rewrite requires exact match)",
            "pre_lines": pre_lines,
            "pre_parens": (pre_o, pre_c, pre_d),
        }
    new_text = new_content

    backup_if_needed(GATE_PATH, GATE_BAK, dry_run)
    write_file(GATE_PATH, new_text, dry_run)

    post_lines = new_text.count("\n")
    post_o, post_c, post_d = paren_balance(new_text)

    return {
        "path": str(GATE_PATH),
        "ok": True,
        "pre_lines": pre_lines,
        "post_lines": post_lines,
        "line_delta": post_lines - pre_lines,
        "pre_parens": (pre_o, pre_c, pre_d),
        "post_parens": (post_o, post_c, post_d),
        "edit": "full rewrite v8 -> v9 (substrate composition with priority hierarchy)" if direction == "apply" else "full rewrite v9 -> v8 (restore legacy binary gate)",
    }


def process_artifact1(direction: str, dry_run: bool) -> dict:
    """Process artifact_1 Line 100 entry update."""
    if not ART1_PATH.exists():
        return {
            "path": str(ART1_PATH),
            "ok": False,
            "message": f"artifact_1 file not found at {ART1_PATH}",
        }

    text = read_file(ART1_PATH)
    pre_lines = text.count("\n")

    if direction == "apply":
        anchor = ART1_ANCHOR
        new_content = ART1_NEW
        anchor_present = anchor in text
        sentinel_absent = "STEP 6 v9 (May 16 2026)" not in text
        state_ok = anchor_present and sentinel_absent
        state_check_label = "v8 Line 100 entry present, Step 6 sentinel absent"
    else:
        anchor = ART1_NEW
        new_content = ART1_ANCHOR
        anchor_present = anchor in text
        state_ok = anchor_present
        state_check_label = "Step 6 sentinel present"

    if not state_ok:
        return {
            "path": str(ART1_PATH),
            "ok": False,
            "message": f"State check failed: {state_check_label}",
            "pre_lines": pre_lines,
        }

    count = count_substr(text, anchor)
    if count != 1:
        return {
            "path": str(ART1_PATH),
            "ok": False,
            "message": f"Anchor match count = {count}, expected 1",
            "pre_lines": pre_lines,
        }

    new_text = text.replace(anchor, new_content, 1)

    backup_if_needed(ART1_PATH, ART1_BAK, dry_run)
    write_file(ART1_PATH, new_text, dry_run)

    post_lines = new_text.count("\n")
    return {
        "path": str(ART1_PATH),
        "ok": True,
        "pre_lines": pre_lines,
        "post_lines": post_lines,
        "line_delta": post_lines - pre_lines,
        "edit": "replace v8 aliveness-gate entry with v9 substrate-composition entry" if direction == "apply" else "restore v8 aliveness-gate entry",
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
    print(f"  STEP 6 ALIVENESS GATE MIGRATION: {direction.upper()} ({'DRY-RUN' if dry_run else 'WRITING'})")
    print("=" * 78)
    print()

    for p in [GATE_PATH, ART1_PATH]:
        if not p.exists():
            print(f"  ERROR: {p} does not exist. Are you at repo root?")
            return 1

    print(">>> Per-file state checks and edits <<<")
    print()

    results = []
    processors = [
        (process_gate, "soul/aliveness_gate.metta"),
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
    print(f"  Backup suffix: .bak.step6_aliveness_gate_migration")
    print()
    for label, r in results:
        print(f"  {label}: {r.get('edit')}")
        print(f"    {r.get('pre_lines')} -> {r.get('post_lines')} lines (delta {r.get('line_delta'):+d})")
    print()
    print("  Total edits: 2 coordinated changes (1 full rewrite, 1 artifact_1 update)")
    print("  Contract: Artifact 0 Discipline 4 (wiring diagram in same commit)")
    print("  Reversibility: python3 staging/apply_step6_aliveness_gate_migration.py --reverse --apply")
    print()
    print("  Post-apply rebuild required (--no-cache for soul/ changes):")
    print("    docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw")
    print()
    print("  Post-rebuild test order:")
    print("    Test 1 (heartbeat F31): iteration counter advances 2+ within 25 sec")
    print("    Test 2 (gate decisions correct): inspect ALIVENESS_VERDICT against")
    print("            current substrate organ atoms")
    print("    Test 3 (duplicate-engagement prevention): observe whether the")
    print("            duplicate-send pattern is structurally prevented over a")
    print("            multi-cycle window")
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
        print(f"  Wrote: {label}")
        final_results.append((label, result))
    print()

    print("=" * 78)
    print("  DISK VERIFICATION")
    print("=" * 78)
    print()
    for label, r in final_results:
        print(f"  {label}: {r.get('post_lines')} lines, edit applied")
    print()
    print("=" * 78)
    print(f"  STEP 6 ALIVENESS GATE MIGRATION {direction.upper()} COMPLETE")
    print("=" * 78)
    print()
    if direction == "apply":
        print("  NEXT: Rebuild and run Test 1 (heartbeat) before any other verification:")
        print("    docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw && sleep 25 && docker logs clarity_omega 2>&1 | grep -E '\\-\\-\\-\\-\\-\\-\\-\\-iteration [0-9]+\\)' | tail -10")
    return 0


if __name__ == "__main__":
    sys.exit(main())
