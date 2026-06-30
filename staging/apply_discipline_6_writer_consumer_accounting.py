#!/usr/bin/env python3
"""apply_discipline_6_writer_consumer_accounting.py

Formalize Discipline 6 (Pure-vs-writer split + writer/consumer
enumeration) into the project contract. Three coordinated documentation
edits in one commit.

Background:
    Discipline 6 emerged from Step 6 aliveness gate work, May 16 2026.
    The Step 6 design phase focused on the gate (consumer) without
    enumerating idle_directive's writer side or the wakeupInterval
    configuration constant. The behavioral gap revealed in runtime
    testing showed the gate is structurally correct but behaviorally
    inert because the writer side fires constantly (wakeupInterval=1
    vs intended 600).

    Investigation also showed: the pure-vs-writer file split has
    ALREADY been practiced in task_state (Step 4), idle_cycle_detector
    (Step 4.5 corrected split), and agency_balance_guard (Step 4.6
    corrected split). Both 4.5 and 4.6 explicitly cite "Discipline 2
    refinement" in their substrate file headers. Discipline 6 formalizes
    this learned-and-practiced pattern into the contract.

    Patrick's library import mechanism (lib_clarity_reasoning.metta)
    provides the foundation; ClarityOmega's writer/reader split is a
    higher-level organizational discipline that operates within
    Patrick's import structure.

Three coordinated edits:

    Edit 1: docs/design/artifact_0_loop_extension_contract.md
            Insert Discipline 6 between Discipline 5 and the
            "## 3. The hook insertion checklist" section. Same shape
            as Disciplines 1-5: Rule, Failure mode, Operational trigger,
            Done-right, Done-wrong.

    Edit 2: docs/design/artifact_0_loop_extension_contract.md
            Insert Surface Investigation Template as Section 3.5,
            between the hook insertion checklist (Section 3) and
            Section 4 "Maintenance contract". The template is a
            structured form contributors fill out before drafting
            changes to any substrate surface.

    Edit 3: docs/CLAUDE_ORIENTATION.md
            Insert P11 (writer/consumer accounting working principle)
            between P10 and "Tone and style rules" section. Cross-links
            to Artifact 0 Discipline 6 for the formal contract.

    Edit 4 (within Edit 1's file): docs/design/artifact_0_loop_extension_contract.md
            Update Section 8 version history with v2 entry.

Contract compliance:
    Pure documentation commit. No code changes. No substrate atoms
    added or removed. No new LLM surface area. Discipline 4 (wiring
    diagram) N/A since loop.metta unchanged.

Reversibility:
    .bak.discipline_6_writer_consumer_accounting backups created
    before writing. --reverse --apply restores.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


# ============================================================================
# FILE PATHS
# ============================================================================

ART0_PATH = Path("docs/design/artifact_0_loop_extension_contract.md")
ART0_BAK = Path("docs/design/artifact_0_loop_extension_contract.md.bak.discipline_6_writer_consumer_accounting")

ORIENT_PATH = Path("docs/CLAUDE_ORIENTATION.md")
ORIENT_BAK = Path("docs/CLAUDE_ORIENTATION.md.bak.discipline_6_writer_consumer_accounting")


# ============================================================================
# EDIT 1+2: Artifact 0 -- insert Discipline 6 + Investigation Template
# ============================================================================

# Anchor: the boundary between Discipline 5 (ending with its Done-wrong
# paragraph + ---) and "## 3. The hook insertion checklist".
ART0_ANCHOR_DISCIPLINE_BOUNDARY = """**Done wrong.** A capability spec that says "phase 1 adds hooks, no retirement scheduled." Hooks pile on top of unretired inline logic. Six months later, no one remembers which inline logic was supposed to be retired vs which is current architecture. The cruft becomes permanent.

---

## 3. The hook insertion checklist"""

ART0_NEW_DISCIPLINE_BOUNDARY = """**Done wrong.** A capability spec that says "phase 1 adds hooks, no retirement scheduled." Hooks pile on top of unretired inline logic. Six months later, no one remembers which inline logic was supposed to be retired vs which is current architecture. The cruft becomes permanent.

---

### Discipline 6: Pure-vs-writer file split + writer/consumer enumeration before design

**Rule.** Two parts, both required.

Part A (file organization, for new primitives with side effects). When introducing a new substrate primitive that has BOTH read helpers AND mutation (do-*! writers), split into two files. The pure file (e.g., `task_state.metta`) contains atom shape documentation, valid value enumerations, and read helpers (current-*, format-*, count-*, etc.). The writers file (e.g., `task_state_writers.metta`) contains do-*! functions that mutate AtomSpace atoms. Both files register in `lib_clarity_reasoning/lib_clarity_reasoning.metta` with explicit comments naming their role. The pure file's header explicitly states "Side-effecting writers (do-*!) land in <writers_file>".

Part B (investigation, for any change to existing surfaces). Before designing changes to a substrate surface that already exists, enumerate four things: writers (what code paths add or mutate the relevant atoms), consumers (what code paths read them), intermediate transformations (helpers and skills between writer and consumer that transform without reading the atom directly), and configuration constants (initLoop values like wakeupInterval, thresholds in soul/ files, and similar cadence/sensitivity levers). The default assumption "we know who writes this" is the failure mode. Verify against actual code before claiming.

**Failure mode prevented.** Two failure modes, paired with the two parts.

Part A failure (file organization): pure read helpers and side-effecting writers mixed in one file. Read sites import a "pure" file and get unwanted writer surface area. Refactoring requires invasive file splits later (already happened in Steps 4.5 corrected + 4.6 corrected). Documentation cannot cleanly say "this file is queryable in REPL without side effects" when writers are interleaved.

Part B failure (investigation): designing for one side of a surface (commonly the consumer) without seeing the writer side or configuration constants. Step 6 (May 16 2026) designed the substrate-composition gate (consumer) thoroughly with three-organ priority hierarchy. The gate is structurally correct. But the writer side of `idle_directive` (helper.soul_idle_goal_prompt_v2, plus wakeupInterval=1 config constant making the writer fire every cycle) was discovered only at first behavioral test. The substrate-composition path the gate built carefully is behaviorally inert in production because the writer-side surface short-circuits every cycle. Discipline 6 Part B would have surfaced this in design phase, not as runtime surprise.

**Operational trigger.** Part A: when proposing any new substrate file containing both atom shape definitions AND do-*! functions. Part B: when designing a change to any existing substrate surface that has writers, consumers, or both. When working with a primitive that touches `idle_directive`, `latch-state`, `task-phase`, `idle-pattern`, `agency-balance`, `recent-action`, or any similar surface with established writers/consumers.

**Done right (Part A, task_state, Step 4).** `soul/task_state.metta` contains atom shape documentation for six atom families, valid phase enumeration, and pure read helpers (current-phase, current-cycles-since-input, current-anchors-for-phase, format-pending-threads, task-state-block). The file header explicitly says "Side-effecting writers (do-*!) land in task_state_writers.metta." `soul/task_state_writers.metta` contains do-bootstrap-task-state!, do-set-cycles-since-input!, do-set-last-activity!, do-set-phase!, do-resolve-pending-thread!. Both register in lib_clarity_reasoning.metta. The pattern was cited as precedent by idle_cycle_detector (Step 4.5 corrected split) and agency_balance_guard (Step 4.6 corrected split) under the header note "Pure-vs-writer split per task_state precedent." Discipline 6 formalizes this already-practiced pattern.

**Done right (Part B, Step 6 idle_directive survey, May 16 2026).** Before proposing supervisor-side changes to idle_directive, surveyed the surface via read-only grep: function definition (helper.soul_idle_goal_prompt_v2, lines 1217-1395), call sites (loop.metta line 98), downstream consumers (loop.metta lines 99, 100, 107, 110), goal-completion writer (helper.soul_mark_goal_complete + state['completed_goals'] mutation sites), intermediate transformations (supervisor_select_goal, generate_goal_from_gaps, supervisor_format_genesis_directive), configuration constants (wakeupInterval). Discovery: the "supervisor bug" framing was wrong. The helper is correctly designed (always returns directive, switches to genesis on no-goal). The cadence is wrong (wakeupInterval=1 vs intended 600). Survey changed the design conclusion entirely.

**Done wrong (Part A).** A new awareness organ ships as one file mixing `(verdict-threshold 0.6)` documentation atoms, pure `(current-verdict)` readers, AND `do-update-verdict!` writers. Some consumer file imports the pure file expecting no side effects, gets the writer namespace too. Subsequent commits add more writers to the same file because the precedent is "writers go here." Refactoring later requires touching every consumer.

**Done wrong (Part B).** "We know the supervisor returns text; let's design a gate that handles the cases." Design proceeds. Gate ships. First behavioral test reveals the supervisor returns text every cycle (writer-side surprise) due to a configuration value the design phase never inspected (wakeupInterval=1 vs intended 600). The structural work is correct; the behavioral fix is somewhere else entirely. Survey-first would have surfaced this in design.

---

## 3. The hook insertion checklist"""


# Anchor for Investigation Template insertion: end of the hook insertion
# checklist (the closing of the code block) and start of Section 4.
# Need to find a stable anchor at end of Section 3 / start of Section 4.
ART0_ANCHOR_TEMPLATE_BOUNDARY = """[ ] Atom queryability verified for any new substrate state
```

Any NO answer halts the commit. Either fix the issue or document why this case is an exception (and add the exception pattern to this artifact for next time).

---

## 4. Maintenance contract"""

ART0_NEW_TEMPLATE_BOUNDARY = """[ ] Atom queryability verified for any new substrate state
```

Any NO answer halts the commit. Either fix the issue or document why this case is an exception (and add the exception pattern to this artifact for next time).

---

## 3.5 Surface investigation template

Per Discipline 6 Part B. Before designing any change to an existing substrate surface, fill in the structured form below. If a field reads "unknown -- need to investigate," that field is the next read-only investigation pass, NOT a design assumption.

```
SURFACE INVESTIGATION TEMPLATE

Surface name (atom family or function): ____________________
Investigation date: ____________________
Sprint / step this investigation supports: ____________________

A. Writers (atoms going INTO the surface)
[ ] File(s) that write the relevant atoms: ____________________
[ ] Function name(s) doing the write: ____________________
[ ] Atom shape(s) written: (foo $a $b)
[ ] Trigger conditions in caller (loop.metta line + condition): ____________________

B. Consumers (atoms going OUT of the surface)
[ ] File(s) that read the relevant atoms: ____________________
[ ] Read pattern (match, py-call to helper, get-state, etc.): ____________________
[ ] Downstream effects (what the consumer does with the read value): ____________________

C. Intermediate transformations
[ ] Helpers/skills that transform without reading the atom directly: ____________________
[ ] Side-effect functions in the chain: ____________________
[ ] Recursive call sites (helper calls another helper that calls back): ____________________

D. Configuration levers
[ ] Constants in initLoop affecting surface behavior: ____________________
[ ] Their current values vs design intent: ____________________
[ ] Thresholds in soul/ files affecting surface sensitivity: ____________________

E. Other consumers downstream
[ ] What ELSE reads atoms touched in this surface: ____________________
[ ] Risk surface for downstream-only changes: ____________________
[ ] Migration paths if writer side changes: ____________________

F. Design questions deferred to Clarity (the agent has first-order
observation rights on her own behavior):
[ ] Behavioral preferences only the agent can answer: ____________________
[ ] Phase or atom value choices: ____________________
[ ] Cadence preferences: ____________________

If sections A-E have unknowns, complete read-only investigation first.
If section F has items, draft a Clarity survey before design.
ONLY THEN propose design alternatives.
```

The template is not bureaucratic overhead. It exists because Step 6 (May 16 2026) shipped a structurally correct substrate-composition gate that was behaviorally inert in production due to a configuration constant the design phase never inspected. Surveys take 10-20 minutes; discovering the gap at first behavioral test costs a rebuild cycle and erodes confidence in the work. The trade is heavily in favor of survey-first.

---

## 4. Maintenance contract"""


# Anchor for Edit 4 (version history update): end of Section 8 / v1 entry.
ART0_ANCHOR_VERSION = """**v1 (May 12, 2026).** Initial draft. Five disciplines, hook insertion checklist, maintenance contract, eight self-enforcement habits, reading triggers, cross-reference table. Drafted following the task-state primitive Step 1 thread, which surfaced the durability concern that motivated this document. Citations to lines 68, 88, 93, 94 of loop.metta as wrong-example inline logic; line 95 as right-example hook pattern."""

ART0_NEW_VERSION = """**v1 (May 12, 2026).** Initial draft. Five disciplines, hook insertion checklist, maintenance contract, eight self-enforcement habits, reading triggers, cross-reference table. Drafted following the task-state primitive Step 1 thread, which surfaced the durability concern that motivated this document. Citations to lines 68, 88, 93, 94 of loop.metta as wrong-example inline logic; line 95 as right-example hook pattern.

**v2 (May 16, 2026).** Added Discipline 6 (Pure-vs-writer file split + writer/consumer enumeration before design) following the Step 6 aliveness gate work. Part A formalizes the already-practiced pattern from task_state (Step 4), idle_cycle_detector (Step 4.5 corrected split), and agency_balance_guard (Step 4.6 corrected split). Part B adds the survey-first discipline for changes to existing surfaces, motivated by the Step 6 idle_directive surprise where wakeupInterval=1 configuration was missed in design phase. Section 3.5 (Surface investigation template) added as the operational form. Cross-referenced from CLAUDE_ORIENTATION.md P11 working principle."""


# Combined: Discipline 6 anchor + Template anchor + Version anchor.
# Three separate replacements within the same file. Each verified count=1.

# Apply order matters: insert Discipline 6 first (changes line numbers),
# but anchor strings are line-independent (they're text matches), so
# order is flexible. We apply in source order for readability of the
# script and for any future debugging that walks edits sequentially.


# ============================================================================
# EDIT 3: CLAUDE_ORIENTATION.md -- insert P11 between P10 and Tone section
# ============================================================================

# Anchor: P10 ending paragraph + blank line + "### Tone and style rules"
ORIENT_ANCHOR = """### P10: Text-based self-evaluation is performative

Open-ended introspection questions in prompts degrade to ritual within ~20 cycles. Replace with structured persistent state that accumulates, gets revised, and connects to action. Questions that work orient toward the world; questions about internal state degrade.

### Tone and style rules"""

ORIENT_NEW = """### P10: Text-based self-evaluation is performative

Open-ended introspection questions in prompts degrade to ritual within ~20 cycles. Replace with structured persistent state that accumulates, gets revised, and connects to action. Questions that work orient toward the world; questions about internal state degrade.

### P11: Writer/consumer accounting before design (cross-link: Artifact 0 Discipline 6)

Before touching any substrate surface, enumerate: writers (what code writes the relevant atoms), consumers (what code reads them), intermediate transformations (helpers between writer and consumer), and configuration constants (cadence/threshold levers in initLoop or soul/ files). The default assumption "we know who writes this" is the failure mode. Verify against actual code first. The task_state plus task_state_writers pattern is the canonical exemplar for new primitives; the Step 6 idle_directive survey is the canonical exemplar for investigating existing surfaces. The formal contract is Artifact 0 Discipline 6; this principle is its working-principle short form for use during investigations.

### Tone and style rules"""


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def count_substr(text: str, needle: str) -> int:
    if not needle:
        return 0
    return text.count(needle)


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


def process_artifact0(direction: str, dry_run: bool) -> dict:
    """Three sequential replacements in artifact_0:
       1. Discipline 6 insertion (between Discipline 5 and Section 3)
       2. Investigation Template insertion (between Section 3 and Section 4)
       3. Version history update in Section 8
    """
    text = read_file(ART0_PATH)
    pre_lines = text.count("\n")

    if direction == "apply":
        anchors = [
            (ART0_ANCHOR_DISCIPLINE_BOUNDARY, ART0_NEW_DISCIPLINE_BOUNDARY, "Discipline 6"),
            (ART0_ANCHOR_TEMPLATE_BOUNDARY, ART0_NEW_TEMPLATE_BOUNDARY, "Investigation Template"),
            (ART0_ANCHOR_VERSION, ART0_NEW_VERSION, "Version history v2"),
        ]
        state_check_label = "v1 markers present, v2 markers absent"
        sentinels_to_be_absent = ["Discipline 6: Pure-vs-writer", "## 3.5 Surface investigation template", "v2 (May 16, 2026)"]
    else:
        anchors = [
            (ART0_NEW_DISCIPLINE_BOUNDARY, ART0_ANCHOR_DISCIPLINE_BOUNDARY, "Discipline 6"),
            (ART0_NEW_TEMPLATE_BOUNDARY, ART0_ANCHOR_TEMPLATE_BOUNDARY, "Investigation Template"),
            (ART0_NEW_VERSION, ART0_ANCHOR_VERSION, "Version history v2"),
        ]
        state_check_label = "v2 markers present"
        sentinels_to_be_absent = []

    # State check: anchors present, sentinels-to-be-absent absent.
    for anchor, new, label in anchors:
        if anchor not in text:
            return {
                "path": str(ART0_PATH),
                "ok": False,
                "message": f"Anchor not found for {label}: state check failed ({state_check_label})",
                "pre_lines": pre_lines,
            }
        count = count_substr(text, anchor)
        if count != 1:
            return {
                "path": str(ART0_PATH),
                "ok": False,
                "message": f"Anchor for {label} count = {count}, expected 1",
                "pre_lines": pre_lines,
            }

    if direction == "apply":
        for sentinel in sentinels_to_be_absent:
            if sentinel in text:
                return {
                    "path": str(ART0_PATH),
                    "ok": False,
                    "message": f"Sentinel for already-applied state present: {sentinel}",
                    "pre_lines": pre_lines,
                }

    # All checks pass: apply edits.
    new_text = text
    for anchor, new, label in anchors:
        new_text = new_text.replace(anchor, new, 1)

    backup_if_needed(ART0_PATH, ART0_BAK, dry_run)
    write_file(ART0_PATH, new_text, dry_run)

    post_lines = new_text.count("\n")
    edit_label = "insert Discipline 6 + Investigation Template + v2 version note" if direction == "apply" else "remove Discipline 6 + Investigation Template + v2 version note"
    return {
        "path": str(ART0_PATH),
        "ok": True,
        "pre_lines": pre_lines,
        "post_lines": post_lines,
        "line_delta": post_lines - pre_lines,
        "edit": edit_label,
    }


def process_orientation(direction: str, dry_run: bool) -> dict:
    """Process docs/CLAUDE_ORIENTATION.md P11 insertion."""
    text = read_file(ORIENT_PATH)
    pre_lines = text.count("\n")

    if direction == "apply":
        anchor = ORIENT_ANCHOR
        new_content = ORIENT_NEW
        anchor_present = anchor in text
        sentinel_absent = "P11: Writer/consumer accounting" not in text
        state_ok = anchor_present and sentinel_absent
        state_check_label = "P10 anchor present, P11 sentinel absent"
    else:
        anchor = ORIENT_NEW
        new_content = ORIENT_ANCHOR
        anchor_present = anchor in text
        state_ok = anchor_present
        state_check_label = "P11 sentinel present"

    if not state_ok:
        return {
            "path": str(ORIENT_PATH),
            "ok": False,
            "message": f"State check failed: {state_check_label}",
            "pre_lines": pre_lines,
        }

    count = count_substr(text, anchor)
    if count != 1:
        return {
            "path": str(ORIENT_PATH),
            "ok": False,
            "message": f"Anchor match count = {count}, expected 1",
            "pre_lines": pre_lines,
        }

    new_text = text.replace(anchor, new_content, 1)

    backup_if_needed(ORIENT_PATH, ORIENT_BAK, dry_run)
    write_file(ORIENT_PATH, new_text, dry_run)

    post_lines = new_text.count("\n")
    return {
        "path": str(ORIENT_PATH),
        "ok": True,
        "pre_lines": pre_lines,
        "post_lines": post_lines,
        "line_delta": post_lines - pre_lines,
        "edit": "insert P11 working principle between P10 and Tone section" if direction == "apply" else "remove P11 working principle",
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
    print(f"  DISCIPLINE 6 DOCUMENTATION COMMIT: {direction.upper()} ({'DRY-RUN' if dry_run else 'WRITING'})")
    print("=" * 78)
    print()

    for p in [ART0_PATH, ORIENT_PATH]:
        if not p.exists():
            print(f"  ERROR: {p} does not exist. Are you at repo root?")
            return 1

    print(">>> Per-file state checks and edits <<<")
    print()

    results = []
    processors = [
        (process_artifact0, "docs/design/artifact_0_loop_extension_contract.md"),
        (process_orientation, "docs/CLAUDE_ORIENTATION.md"),
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
        print(f"    Lines: {pre_l} -> {post_l} (delta {delta_l:+d})")
        print(f"    Edit: {result.get('edit')}")
        results.append((label, result))
        print()

    print("=" * 78)
    print(f"  SUMMARY: WHAT --{direction} --apply WILL DO")
    print("=" * 78)
    print()
    print(f"  Direction: {direction.upper()}")
    print(f"  Backup suffix: .bak.discipline_6_writer_consumer_accounting")
    print()
    for label, r in results:
        print(f"  {label}: {r.get('edit')}")
        print(f"    {r.get('pre_lines')} -> {r.get('post_lines')} lines (delta {r.get('line_delta'):+d})")
    print()
    print("  Total edits: 2 files, 3 insertions in Artifact 0 + 1 insertion in CLAUDE_ORIENTATION")
    print("  Contract: pure documentation commit, no code changes, no substrate impact")
    print("  Reversibility: python3 staging/apply_discipline_6_writer_consumer_accounting.py --reverse --apply")
    print()
    print("  No rebuild required (documentation only).")
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
    print(f"  DISCIPLINE 6 DOCUMENTATION COMMIT {direction.upper()} COMPLETE")
    print("=" * 78)
    print()
    if direction == "apply":
        print("  NEXT: review the changes, then stage + commit.")
        print("  No rebuild needed; documentation commit only.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
