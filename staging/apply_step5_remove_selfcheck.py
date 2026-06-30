#!/usr/bin/env python3
"""apply_step5_remove_selfcheck.py

Step 5 of the task-state primitive mini-sprint: remove SELF-CHECK block
from prompt assembly + retire self-check-guidance caller.

Per spec (task-state-primitive_design.md Section 10):
    "Step 5: Remove SELF-CHECK block from prompt assembly + migrate
     self-check-guidance trigger. TASK-STATE block now carries the
     orientation work."

Per Section 13 verification criteria:
    Item 7: SELF-CHECK three-question block is gone from the prompt
    Item 8: self-check-guidance after 3 idle cycles is gone (replaced
            by task-phase-driven gating)
    Item 12: CHARS_SENT reduction from removed text-eval surfaces
            (expected 1-3KB drop per cycle when guidance fires)
    Item 14: No new LLM helper functions or soul-llm-call invocations

Decision: α (Berton confirmed). The &engaged_idle_count counter wiring
in loop.metta line 96 stays in place; its sole reader is being removed
but the counter write stays. Deferred to Step 8/9 cleanup. Keeps the
Step 5 commit small and focused on the SELF-CHECK retirement only.

Scope of this script (3 file edits):

    Edit 1: src/loop.metta
            Remove line 104: ($self_check (self-check-guidance ...))
            Remove line 105: ($final_prompt (string_concat ...))
            Change line 110 consumer: $final_prompt -> $enriched_prompt
            Net delta: -2 lines (159 -> 157)

    Edit 2: soul/behavioral_guidance.metta
            Update the self-check-guidance function header comment to
            note Step 5 retired the caller. Function definition stays
            intact -- queryable atom preserved per α scope, but with
            documentation that no consumer remains in v1.
            Net delta: small comment addition

    Edit 3: docs/design/artifact_1_loop_metta_wiring_diagram.md
            Replace stale Phase 4.3 entries documenting lines 97-98
            (the pre-Sprint-1.5 Python self_check + final_prompt wiring)
            with current Phase 4.4 entries documenting:
              - Sprint 1.5 elevation that already happened (b079df6)
              - Step 5 removal of the prompt surface entirely
            Line numbers shift after Step 5 (line 100 aliveness moves
            to line 98 in the new shape).
            Net delta: roughly -10 to +5 lines (cleaner entries)

Contract compliance (Artifact 0 Section 3 checklist):
    [x] Hooks call ONE clearly-named function: N/A (this is REMOVAL, not addition)
    [x] One writer file per primitive: N/A (no new substrate)
    [x] Insertion points named with Artifact 1 phase vocabulary: Phase 4.3 (prompt assembly)
    [x] Artifact 1 wiring diagram updated SAME commit (Discipline 4)
    [x] No inline cruft expanded: this RETIRES inline logic per Discipline 5
    [x] Apply script supports --reverse with .bak backups
    [x] Paren count verified before and after each edit
    [x] Post-apply heartbeat-of-life test plan: $k must advance to 2+
        within 30 seconds, else immediate revert (F31)

Post-apply behavioral tests:
    Test 1 (heartbeat-of-life F31): docker logs grep iteration, must
            see iteration counter advance within 30 seconds.

    Test 2 (SELF-CHECK absent): the string "SELF-CHECK:" must NOT
            appear in subsequent CHARS_SENT log lines. Search:
              docker logs clarity_omega 2>&1 | grep -c "SELF-CHECK:"
            Expected delta: previously fired on count >= 5; now never.

    Test 3 (CHARS_SENT delta): subtle reduction (~100-200 chars per
            cycle) on cycles where self-check would have fired previously.
            Hard to measure precisely until the next idle window builds
            up to count >= 5; safer to consider this PASSED if Test 2
            confirms the surface is absent.

Reversibility:
    Each modified file produces a .bak.step5_remove_selfcheck backup
    before writing. --reverse --apply restores from backups.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


# ============================================================================
# FILE PATHS
# ============================================================================

LOOP_PATH = Path("src/loop.metta")
LOOP_BAK = Path("src/loop.metta.bak.step5_remove_selfcheck")

BG_PATH = Path("soul/behavioral_guidance.metta")
BG_BAK = Path("soul/behavioral_guidance.metta.bak.step5_remove_selfcheck")

ART1_PATH = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md")
ART1_BAK = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md.bak.step5_remove_selfcheck")


# ============================================================================
# EDIT 1: src/loop.metta -- remove self_check + final_prompt, redirect consumer
# ============================================================================

# Three-line block being removed + the line-110 consumer redirect.
# Anchor captures: $enriched_prompt binding, $self_check binding, $final_prompt
# binding, the println for idle directive (which separates the two regions).
LOOP_ANCHOR = """                                       ($enriched_prompt (string_concat $soul_brief $prompt))
                                       ($self_check (self-check-guidance (get-state &engaged_idle_count)))
                                       ($final_prompt (string_concat $self_check $enriched_prompt))
                                       ($_ (println! (IDLE_DIRECTIVE_RAW: $idle_directive)))"""

LOOP_NEW = """                                       ($enriched_prompt (string_concat $soul_brief $prompt))
                                       ($_ (println! (IDLE_DIRECTIVE_RAW: $idle_directive)))"""

# Consumer redirect: soul_send_assemble previously received $final_prompt,
# now receives $enriched_prompt directly.
LOOP_CONSUMER_ANCHOR = """                                       ($send (if (== $aliveness SILENT) "" (py-call (helper.soul_send_assemble
                                                       $final_prompt $soul_context_in $soul_verdict_in"""

LOOP_CONSUMER_NEW = """                                       ($send (if (== $aliveness SILENT) "" (py-call (helper.soul_send_assemble
                                                       $enriched_prompt $soul_context_in $soul_verdict_in"""


# ============================================================================
# EDIT 2: soul/behavioral_guidance.metta -- header note retiring caller
# ============================================================================

# Anchor the existing function header comment block.
BG_ANCHOR = """;; self-check-guidance: reflective self-check that fires after engaged-idle
;; iterations exceed threshold. Returns empty string when threshold not reached.
;; Refinements from Clarity (May 2): three reflective questions instead of
;; binary work-or-idle framing; "or change direction" addition catches the
;; orbit pattern (where engagement feels active but is circling without advancing).
;; Threshold of 5 (raised from 3) gives multi-step work room to breathe.
(= (self-check-guidance $count)"""

BG_NEW = """;; self-check-guidance: reflective self-check that fires after engaged-idle
;; iterations exceed threshold. Returns empty string when threshold not reached.
;; Refinements from Clarity (May 2): three reflective questions instead of
;; binary work-or-idle framing; "or change direction" addition catches the
;; orbit pattern (where engagement feels active but is circling without advancing).
;; Threshold of 5 (raised from 3) gives multi-step work room to breathe.
;;
;; STEP 5 (May 15 2026): caller in loop.metta retired. The SELF-CHECK
;; prompt surface is no longer assembled into the LLM prompt; TASK-STATE
;; block (Step 4), IDLE-PATTERN block (Step 4.5), and AGENCY-BALANCE block
;; (Step 4.6) now carry the orientation work via observable cycle-level
;; primitives rather than via a counter threshold + reflective questions.
;; The function definition stays intact for queryability and for potential
;; future task-phase-driven gating; the &engaged_idle_count counter is
;; still written by loop.metta but has no readers in v1 (α scope decision,
;; deferred removal to Step 8/9).
(= (self-check-guidance $count)"""


# ============================================================================
# EDIT 3: docs/design/artifact_1_loop_metta_wiring_diagram.md
# ============================================================================

# The current stale entries documenting Line 97 (Python self_check) and Line 98
# (final_prompt). Line numbers are pre-line-drift; we replace with current+post-Step-5
# entries documenting both the Sprint 1.5 elevation that already happened AND the
# Step 5 retirement.
ART1_ANCHOR = """**Line 97** - `($self_check (py-call (helper.soul_self_check_prompt (get-state &engaged_idle_count))))`
- Reads: &engaged_idle_count
- Writes: $self_check (the prompt addition)
- Calls: helper.soul_self_check_prompt (returns empty if count < 3, else the binary work-or-idle prompt)
- 🧠 NETWORK-RELEVANT: FPN inhibition function. Self-check is the FPN's reflective halt - asking "should I keep going or should I stop?" In the brain, the FPN's anterior cingulate component does exactly this kind of effort-vs-stop monitoring. Currently the threshold and message are Python; the brain-side function predicts this should be MeTTa with substrate-derived effort-trap and orbit detection.
- 🔧 ELEVATION FLAG (high impact for premature completion): The threshold of 3 fires too early and pushes binary completion choice. Two options: (a) raise threshold to 5-7 with softer message, (b) move the entire self-check into a MeTTa atom in soul/. Option (a) is 10 minutes for immediate operational improvement. Option (b) is 1 hour for architectural cleanliness. Recommendation: (a) now, (b) later.
- 💡 INSERTION POINT: The self-check could include additional context (e.g., last action summary, recent verdict trend) by passing more arguments to the helper. But cleaner still: make this a MeTTa function that queries needed state directly.

**Line 98** - `($final_prompt (string_concat $self_check $enriched_prompt))` - Final assembled prompt for LLM."""

ART1_NEW = """**SELF-CHECK retirement history (lines retired through Sprint 1.5 + Step 5)**

The SELF-CHECK prompt surface evolved through two phases and was retired in Step 5.

- **Phase 1 (original wiring, pre-Sprint-1.5):** Line 97 called `(py-call (helper.soul_self_check_prompt (get-state &engaged_idle_count)))`. Threshold and message both lived in Python; threshold was 3; message was a binary work-or-idle prompt.

- **Phase 2 (Sprint 1.5 elevation, commit b079df6, May 3 2026):** Caller migrated from Python to MeTTa-native `(self-check-guidance (get-state &engaged_idle_count))` defined in `soul/behavioral_guidance.metta`. Threshold raised to 5 per Clarity's May 2 refinement; message reshaped to three reflective questions instead of binary framing. Caller still lived in loop.metta, reading `&engaged_idle_count`, concatenated into `$final_prompt` consumed by `soul_send_assemble`.

- **Phase 3 (Step 5 retirement, May 15 2026):** The SELF-CHECK prompt surface removed entirely from prompt assembly per task-state-primitive_design.md Section 10. The `$self_check` and `$final_prompt` bindings deleted; `soul_send_assemble` now consumes `$enriched_prompt` directly. The `self-check-guidance` function stays defined in `soul/behavioral_guidance.metta` as a queryable atom but has no production caller. TASK-STATE block (Step 4), IDLE-PATTERN block (Step 4.5), and AGENCY-BALANCE block (Step 4.6) now carry the orientation work via observable cycle-level primitives rather than via a counter threshold + reflective questions.

- 🧠 NETWORK-RELEVANT: FPN inhibition function retired in favor of substrate-derived observation organs. Per the task-state-primitive_design.md spec, the awareness organs accumulate observable signals each cycle; aliveness gate consumption of those signals is scheduled for Step 6 (the duplicate-engagement bug fix moment).

- 🔧 ELEVATION FLAG (resolved): both options from the prior flag are now superseded. Option (a) threshold raise landed in Sprint 1.5 (b079df6). Option (b) the architectural cleanliness move landed across Sprint 4 (Steps 4-4.6) and Step 5. The SELF-CHECK surface itself is gone; the substrate question of "should I keep going" is now answered by task-phase + idle-pattern + agency-balance composition, observable each cycle, available for any consumer (Step 6 will be the first such consumer in the aliveness gate)."""


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


def process_loop(direction: str, dry_run: bool) -> dict:
    """Process src/loop.metta two-edit (block removal + consumer redirect)."""
    text = read_file(LOOP_PATH)
    pre_lines = text.count("\n")
    pre_o, pre_c, pre_d = paren_balance(text)

    if direction == "apply":
        block_anchor = LOOP_ANCHOR
        block_new = LOOP_NEW
        consumer_anchor = LOOP_CONSUMER_ANCHOR
        consumer_new = LOOP_CONSUMER_NEW
        block_present = block_anchor in text
        consumer_present = consumer_anchor in text
        new_absent_block = "$self_check" not in text or "$final_prompt" not in text
        state_ok = block_present and consumer_present and (not new_absent_block)
        state_check_label = "self_check + final_prompt block present, soul_send_assemble using final_prompt present"
    else:
        block_anchor = LOOP_NEW
        block_new = LOOP_ANCHOR
        consumer_anchor = LOOP_CONSUMER_NEW
        consumer_new = LOOP_CONSUMER_ANCHOR
        block_present = block_anchor in text
        consumer_present = consumer_anchor in text
        state_ok = block_present and consumer_present
        state_check_label = "post-Step-5 shape present"

    if not state_ok:
        return {
            "path": str(LOOP_PATH),
            "ok": False,
            "message": f"State check failed: {state_check_label}",
            "pre_lines": pre_lines,
            "pre_parens": (pre_o, pre_c, pre_d),
        }

    bc = count_substr(text, block_anchor)
    cc = count_substr(text, consumer_anchor)
    if bc != 1 or cc != 1:
        return {
            "path": str(LOOP_PATH),
            "ok": False,
            "message": f"Anchor counts: block={bc} consumer={cc} (both expected 1)",
            "pre_lines": pre_lines,
            "pre_parens": (pre_o, pre_c, pre_d),
        }

    new_text = text.replace(block_anchor, block_new, 1)
    new_text = new_text.replace(consumer_anchor, consumer_new, 1)

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
        "edit": "remove self_check + final_prompt bindings; redirect soul_send_assemble to enriched_prompt" if direction == "apply" else "restore self_check + final_prompt bindings; redirect soul_send_assemble back to final_prompt",
    }


def process_bg(direction: str, dry_run: bool) -> dict:
    """Process soul/behavioral_guidance.metta header comment addition."""
    text = read_file(BG_PATH)
    pre_lines = text.count("\n")

    if direction == "apply":
        anchor = BG_ANCHOR
        new_content = BG_NEW
        anchor_present = anchor in text
        new_absent = "STEP 5 (May 15 2026): caller in loop.metta retired" not in text
        state_ok = anchor_present and new_absent
        state_check_label = "pre-Step-5 header present, Step 5 marker absent"
    else:
        anchor = BG_NEW
        new_content = BG_ANCHOR
        anchor_present = "STEP 5 (May 15 2026): caller in loop.metta retired" in text
        state_ok = anchor_present
        state_check_label = "Step 5 marker present"

    if not state_ok:
        return {
            "path": str(BG_PATH),
            "ok": False,
            "message": f"State check failed: {state_check_label}",
            "pre_lines": pre_lines,
        }

    count = count_substr(text, anchor)
    if count != 1:
        return {
            "path": str(BG_PATH),
            "ok": False,
            "message": f"Anchor match count = {count}, expected 1",
            "pre_lines": pre_lines,
        }

    new_text = text.replace(anchor, new_content, 1)

    backup_if_needed(BG_PATH, BG_BAK, dry_run)
    write_file(BG_PATH, new_text, dry_run)

    post_lines = new_text.count("\n")
    return {
        "path": str(BG_PATH),
        "ok": True,
        "pre_lines": pre_lines,
        "post_lines": post_lines,
        "line_delta": post_lines - pre_lines,
        "edit": "add Step 5 caller-retirement note above self-check-guidance" if direction == "apply" else "remove Step 5 caller-retirement note",
    }


def process_artifact1(direction: str, dry_run: bool) -> dict:
    """Replace stale Line 97/98 entries with current+post-Step-5 entries."""
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
        sentinel_absent = "SELF-CHECK retirement history" not in text
        state_ok = anchor_present and sentinel_absent
        state_check_label = "stale Line 97/98 entries present, Step 5 retirement entry absent"
    else:
        anchor = ART1_NEW
        new_content = ART1_ANCHOR
        anchor_present = anchor in text
        state_ok = anchor_present
        state_check_label = "Step 5 retirement entry present"

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
        "edit": "replace stale Line 97/98 entries with SELF-CHECK retirement history" if direction == "apply" else "restore stale Line 97/98 entries",
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
    print(f"  STEP 5 REMOVE SELFCHECK: {direction.upper()} ({'DRY-RUN' if dry_run else 'WRITING'})")
    print("=" * 78)
    print()

    for p in [LOOP_PATH, BG_PATH, ART1_PATH]:
        if not p.exists():
            print(f"  ERROR: {p} does not exist. Are you at repo root?")
            return 1

    print(">>> Per-file state checks and edits <<<")
    print()

    results = []
    processors = [
        (process_loop, "src/loop.metta"),
        (process_bg, "soul/behavioral_guidance.metta"),
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
    print(f"  Backup suffix: .bak.step5_remove_selfcheck")
    print()
    for label, r in results:
        print(f"  {label}: {r.get('edit')}")
        print(f"    {r.get('pre_lines')} -> {r.get('post_lines')} lines (delta {r.get('line_delta'):+d})")
    print()
    print("  Total edits: 3 coordinated changes")
    print("  Contract: Artifact 0 Discipline 5 retirement; Section 3 checklist run")
    print("  Reversibility: python3 staging/apply_step5_remove_selfcheck.py --reverse --apply")
    print()
    print("  Post-apply rebuild required (--no-cache for soul/ changes):")
    print("    docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw")
    print()
    print("  Post-rebuild test order:")
    print("    Test 1 (heartbeat F31): iteration counter must advance to 2+ within 25 sec")
    print("    Test 2 (SELF-CHECK absent): grep -c 'SELF-CHECK:' should return 0")
    print("    Test 3 (CHARS_SENT delta): subtle reduction; consider PASSED if Test 2 passes")
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
    print(f"  STEP 5 REMOVE SELFCHECK {direction.upper()} COMPLETE")
    print("=" * 78)
    print()
    if direction == "apply":
        print("  NEXT: Rebuild and run Test 1 (heartbeat) before any other verification:")
        print("    docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw && sleep 25 && docker logs clarity_omega 2>&1 | grep -E '\\-\\-\\-\\-\\-\\-\\-\\-iteration [0-9]+\\)' | tail -10")
    return 0


if __name__ == "__main__":
    sys.exit(main())
