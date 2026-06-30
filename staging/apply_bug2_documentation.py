#!/usr/bin/env python3
"""apply_bug2_documentation.py

Land knowledge documentation for the Bug 2 + Bug 2b clear-function fix.

Three coordinated edits in one commit per Discipline 4 (substrate edit +
wiring diagram update + ADR + investigation log all land together):

    Edit 1: docs/decisions/ADR-005-bug2-clear-fn-superpose-fix.md
            NEW FILE. Architectural decision record. Why car-atom + remove-atom
            failed, why superpose-iteration works, alternatives considered,
            verification record.

    Edit 2: docs/investigations/2026-05-20-bug2-clear-fn-investigation.md
            NEW FILE. Empirical investigation log. Methodology, findings
            (Bug 1 disproven, Bug 2 + 2b confirmed, Bug 3 cosmetic,
            Bug 4 surfaced), sleep-vs-wake cycle distinction, layered
            duplicate-engagement model, process notes, timeline.

    Edit 3: docs/design/artifact_1_loop_metta_wiring_diagram.md
            UPDATE. Append a 'Bug 2 fix (May 20 2026)' note to the
            do-update-idle-pattern! and do-update-agency-balance! entries
            in Section 4. Preserves the existing Step 4.5 / 4.6 history;
            adds the new milestone.

Contract compliance:
    - Discipline 4: wiring diagram updated in the same commit as the
      substrate edit (the substrate edit lands separately via
      apply_clear_fn_superpose_fix.py; THIS script lands the paired docs)
    - F154: project_knowledge_search used to verify the artifact_1
      anchor text verbatim before drafting
    - F156: this script does NOT touch src/loop.metta or any soul/ file
    - Reversibility: --reverse --apply removes the new files and reverts
      the artifact_1 patch

Reversibility:
    .bak.bug2_documentation backups created before writing artifact_1.
    New files (ADR, investigation log) are removed on --reverse.
    --reverse --apply restores the prior state.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


# ============================================================================
# FILE PATHS
# ============================================================================

ADR_PATH = Path("docs/decisions/ADR-005-bug2-clear-fn-superpose-fix.md")
INVESTIGATION_PATH = Path("docs/investigations/2026-05-20-bug2-clear-fn-investigation.md")
ART1_PATH = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md")
ART1_BAK = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md.bak.bug2_documentation")


# ============================================================================
# EDIT 1: ADR-005 content
# ============================================================================

ADR_CONTENT = """# ADR-005: Superpose-iteration clear in awareness-organ writers

**Status:** Accepted. Implemented and verified May 20, 2026.

**Date:** 2026-05-20

**Deciders:** Berton (project lead), Clarity (substrate co-designer), Claude (investigation assistant).

**Related work:** See `docs/investigations/2026-05-20-bug2-clear-fn-investigation.md` for the empirical investigation. See `docs/design/artifact_1_loop_metta_wiring_diagram.md` Section 4 entries for do-update-idle-pattern! and do-update-agency-balance! for the wiring diagram update per Discipline 4.

---

## Context

The two awareness-organ writers in the substrate, `do-clear-idle-pattern!` (in `soul/idle_cycle_detector_writers.metta`) and `do-clear-agency-balance!` (in `soul/agency_balance_guard_writers.metta`), used a `car-atom + remove-atom` pattern to clear prior atoms before writing fresh state each cycle. Both functions had been in production since their respective Step 4.5 and Step 4.6 corrected splits in mid-May 2026.

Forensic investigation of spam behavior in late May 2026 surfaced that Clarity's prompt context was permanently showing `(idle-pattern productive 0)` and `(agency-balance dependency-risk 0 1)` regardless of actual cycle activity. The detection layer appeared dead.

Empirical evidence from diagnostic prints inserted into the writers and loop showed: across a 2200+ cycle run, the idle-pattern atom count in `&self` grew exactly in lockstep with writer-fire count. Between writer fires, no clear operation succeeded. The clear function had been removing zero atoms since cycle 1. The accumulated stack reached 57 atoms by the time diagnostics were captured.

The read-side helper `current-idle-pattern` returns `car-atom` of the collapse result, which in PeTTa returns the first (oldest) atom of the accumulated stack. So the prompt was reading the cycle-1 bootstrap atom forever, regardless of what the writer correctly computed and added each cycle.

`do-clear-agency-balance!` had the identical structural bug, with `current-agency-balance` also reading via `car-atom`. Confirmed via source read of `soul/agency_balance_guard_writers.metta`.

## Decision

Replace `car-atom + remove-atom` with the superpose-iteration pattern proven by `recent_action_populator.metta`'s pruning logic. The pattern collapses the match result into a list, then iterates via `superpose` and calls `remove-atom` on each element. The implementation is identical in shape across both writer files, only the atom signature differs.

The new pattern for `do-clear-idle-pattern!`:

```metta
(= (do-clear-idle-pattern!)
   (let $existing (collapse (match &self (idle-pattern $v $c) (idle-pattern $v $c)))
      (if (== $existing ())
          _
          (let $old (superpose $existing)
                    (if (== $old ())
                        ()
                        (remove-atom &self $old))))))
```

Same shape for `do-clear-agency-balance!` with the three-argument pattern `(agency-balance $v $p $s)`.

## Consequences

**Verified outcomes.** End-to-end testing across cycles 1-9 (steady-state) and cycles 34-35 (heterogeneous-content transition during active send burst) confirmed:

- Both clear functions now successfully remove all prior atoms on each writer fire
- Idle-pattern atom count holds at exactly 1 per cycle
- Agency-balance atom count holds at exactly 1 per cycle
- Counts transition correctly through send activity (0 -> 1 -> 2 -> ...) without accumulation
- Read-side functions now return current data instead of stale bootstrap
- No stall on initial clear (rebuild wiped `&self`, so the heavy-initial-clear concern Clarity raised did not need to materialize empirically; the pattern is the same one the populator's pruning has used reliably with multi-atom collapse results)

**Architectural consequence (Bug 4 surfaced).** The Bug 2 fix unlocked the detection layer. The downstream consumer that was supposed to act on the now-live detection, the v9 priority-2 gate where `(current-idle-pattern) send-burst -> SILENT`, is still rolled back per the three-state analysis. Clarity self-diagnosed this within minutes of the fix landing: "If v9 gate were wired, I would be SILENT right now." v9 re-integration is the next active priority, not deferred.

**Discipline reinforced.** Detection-without-consumer pathology (cataloged as F157 working principle) surfaced concretely. When fixing a detection-layer bug, the consumer wiring must be evaluated; otherwise the fix can expose live pathology as legible while still permitting the bad behavior.

## Alternatives considered

**Alternative 1: One-time bulk cleanup separate from per-cycle clear.** Clarity flagged the concern that the first cycle post-fix would need to iterate through 50+ accumulated atoms via superpose, potentially hitting a per-cycle execution budget. Considered adding a separate one-time bulk cleanup step on startup, leaving the per-cycle clear simpler. Rejected because (a) the rebuild process wipes `&self` so accumulated atoms don't persist across container restarts, (b) the populator's pruning empirically handles multi-atom collapse iteration without stalling, (c) the diagnostic prints would catch a stall immediately, and (d) the simpler one-function fix is reversible.

**Alternative 2: Switch read helper from `car-atom` to `last-atom` (or equivalent).** Considered redefining `current-idle-pattern` and `current-agency-balance` to return the most-recently-added atom instead of the oldest. Rejected because PeTTa does not guarantee atom ordering in match results, there is no reliable "most recent" semantics. The correct fix is to maintain the invariant that only one atom of each shape exists at any time, which is what the original design intended.

**Alternative 3: Reference counting or set-atom! semantics.** Considered using `set-atom!` (which removes-then-adds) as a single atomic update operation. Rejected because the existing function shape separates clear and add as a deliberate pattern (mirrors how task_state writers and recent_action_populator both operate), and the superpose fix preserves that separation while making it reliable.

## Implementation notes

- The fix script `apply_clear_fn_superpose_fix.py` is reversible per F114 with `.bak.clearfix` backup suffix
- Both files edited in a single apply pass
- Adjacent change: symmetric `DIAG-WRITER-AB-PERSON`, `DIAG-WRITER-AB-SYSTEM`, `DIAG-WRITER-AB-VERDICT`, `DIAG-WRITER-AB-POST-CLEAR` prints added to `do-update-agency-balance!` mirroring existing `DIAG-WRITER-*` prints in `do-update-idle-pattern!`. Loop-level diagnostic prints deferred to a follow-up commit where the anchor can be verified verbatim from project knowledge (F156)
- Rebuild required: `docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw`

## Verification record

| Cycle | DIAG-IDLE-PATTERN-COUNT | DIAG-WRITER-POST-CLEAR | DIAG-WRITER-AB-POST-CLEAR | DIAG-IDLE-PATTERN-ATOMS |
| --- | --- | --- | --- | --- |
| 1 | 1 | () | () | ((productive 0)) |
| 4 | 1 | () | () | ((productive 0)) |
| 6 | 1 | () | () | ((productive 0)) |
| 9 | 1 | () | () | ((productive 0)) |
| 34 (first send) | 1 | () | () | ((productive 1)) |
| 35 (second send) | 1 | () | () | ((productive 2)) |

The transition between cycles 34 and 35 is the definitive proof: the productive-1 atom from cycle 34 was cleared and replaced with productive-2 in cycle 35, with no stale atom remaining and no accumulation. The pre-fix bug would have left both in `&self` with `car-atom` returning the older one.
"""


# ============================================================================
# EDIT 2: Investigation log content
# ============================================================================

INVESTIGATION_CONTENT = """# Investigation: Bug 2 / Bug 2b clear-function failure (2026-05-20)

**Investigators:** Berton (project lead), Clarity (substrate co-designer), Claude (investigation assistant).

**Related artifacts:**
- `docs/decisions/ADR-005-bug2-clear-fn-superpose-fix.md` (the architectural decision)
- `docs/design/artifact_1_loop_metta_wiring_diagram.md` (wiring diagram updated per Discipline 4)

**Outcome:** Bug 2 + Bug 2b fixed and verified. Bug 1 disproven. Bug 3 downgraded to cosmetic. Bug 4 surfaced as the next active pathology.

---

## Investigation scope

This investigation began as forensic analysis of spam behavior, focused on a substrate-level discrepancy where Clarity's prompt context showed `(idle-pattern productive 0)` at cycles 757-758 despite the recent-action window containing 6-7 status-send-unprompted atoms from cycles 747-755. Expected verdict was `send-burst` with count 6+. Actual was `productive 0`.

The three hypothesized bugs entering investigation:

- **Bug 1:** `count-sends-in-window` returns 0 despite send-class atoms in the window
- **Bug 2:** `do-clear-idle-pattern!` fails, causing stale atoms to remain in `&self`
- **Bug 3:** `recent_action_populator` pruning leaves atoms unpruned

A fourth potential bug emerged mid-investigation, regarding `do-clear-agency-balance!` having the same structural shape as `do-clear-idle-pattern!` (Bug 2b).

## Methodology

Read-only diagnostic instrumentation strategy: insert `println!` prints at strategic points in `src/loop.metta` and the writer files, run the container, capture log output, analyze without modifying live behavior.

Diagnostics inserted via a reversible apply script (`apply_diag_match_shape_test.py` with `.bak.diagprint` suffix). Eight new print points:

- `DIAG-CYCLE-START` / `DIAG-CYCLE-END`
- `DIAG-COUNT-FN` (count-sends-in-window result)
- `DIAG-LITERAL-RESPONSIVE` / `DIAG-LITERAL-STATUS` (direct match results per tag)
- `DIAG-VARIABLE-TAG` (variable-pattern match showing all recent-action atom tags)
- `DIAG-RECENT-ACTION-COUNT` (size of recent-action window)
- `DIAG-IDLE-PATTERN-ATOMS` (full collapse of idle-pattern atoms in `&self`)
- `DIAG-IDLE-PATTERN-COUNT` (size of that collapse)

Plus writer-internal prints in `do-update-idle-pattern!`:

- `DIAG-WRITER-COUNT` / `DIAG-WRITER-VERDICT`
- `DIAG-WRITER-POST-CLEAR` (collapse after clear, showing whether clear succeeded)

Container ran for ~2200 iterations with diagnostics active. Logs captured key wake cycles: 1, 17, 18, 19, 29, 30, 31, 33, 34, 39, 50, 623, 1193, 1745, 2202, 2205.

## Findings

### Bug 1: DISPROVEN

`count-sends-in-window` works correctly. Confirmed at cycle 2202 when a responsive-send landed:

- `DIAG-LITERAL-RESPONSIVE (2202)` returned the cycle-id of the send
- `DIAG-COUNT-FN 1` returned the count
- `DIAG-WRITER-COUNT 1` confirmed the writer saw it too
- `DIAG-VARIABLE-TAG (... (2202 responsive-send))` showed the bare-symbol tag in position 2 of the recent-action atom

The earlier reading of `count-sends-in-window` returning 0 (Clarity's Q1 in the May 19 diagnostic session) was likely caused by the variable-mangling parser issue where `$v $c` in skill-call queries gets rewritten to `$_NNNNNN`, producing parse errors rather than empty result sets. That issue remains open as a separate investigation.

### Bug 2: CONFIRMED, then characterized through a misreading detour, then correctly characterized

**Initial finding (cycles 1-50):** Atom count grew exactly 1 per cycle. At cycle 50, 50 atoms accumulated. Clear was removing zero atoms every cycle.

**Misreading (cycles 50-2202):** Between cycle 50 and cycle 2202, IDLE-PATTERN-COUNT grew by only 4 (from 50 to 54). Initial interpretation: "Clear works ~99.8% of the time, fails ~0.2%." Speculation about variable success rate, hypothesis around heterogeneous content triggering failure.

**Correct characterization (after reading sleep-cycle output):** The `(---------iteration N)` lines between active cycle output are sleep cycles where the writer does NOT fire. The iteration counter advances during sleep but the writer only fires on wake cycles. Between cycle 50 (the last wake-cycle in that early batch) and cycle 623 (the next wake cycle), the loop slept for 573 iterations. The writer fired exactly once across that span, at cycle 623, and clear failed that one time too, adding atom #51.

**Final characterization:** `do-clear-idle-pattern!` has been removing zero atoms since cycle 1. The clear function never worked. The accumulated stack count equals the writer-fire count exactly. The variable success rate was an artifact of variable writer-fire rate, not variable clear success.

**Root cause:** The function uses `(remove-atom &self (car-atom $existing))` where `$existing` is `(collapse (match &self (idle-pattern $v $c) (idle-pattern $v $c)))`. In this runtime, `car-atom` of a collapse result combined with `remove-atom` removes zero atoms reliably across all observed conditions. The reason is not fully characterized (see Open questions below), but the empirical pattern is unambiguous.

**Read-side amplification:** `current-idle-pattern` ALSO uses `car-atom` of the collapse result. Since accumulated atoms order with oldest-first, `car-atom` returns the cycle-1 bootstrap atom forever, regardless of what the writer correctly computes and adds each cycle. This is why the prompt showed `(productive 0)` permanently, the read function was reading the bootstrap, not the latest atom.

### Bug 2b: CONFIRMED via source read

`soul/agency_balance_guard_writers.metta` contains `do-clear-agency-balance!` with identical structure:

```metta
(= (do-clear-agency-balance!)
   (let $existing (collapse (match &self (agency-balance $v $p $s) (agency-balance $v $p $s)))
      (if (== $existing ())
          _
          (remove-atom &self (car-atom $existing)))))
```

Same `car-atom + remove-atom` pattern. Same expected failure mode. `current-agency-balance` also reads via `car-atom`. The persistent `(agency-balance dependency-risk 0 1)` Clarity had been seeing in her prompt is the cycle-1 bootstrap atom, same mechanism as Bug 2's stale `productive 0`.

### Bug 3: DISPROVEN as functional, downgraded to cosmetic

The `recent_action_populator` pruning IS functional. Off-by-one window size (holds 11 atoms instead of 10 due to strict less-than in the prune-before comparison), but the pruning itself works. Verified at cycle 12, atom from cycle 1 was successfully removed by cycle 12, matching expected behavior.

### Bug 4: SURFACED post-fix

After Bug 2 / 2b were fixed, Clarity's IDLE-PATTERN block correctly transitioned from `(productive 0)` to `(productive 1)` to `(send-burst 7)` as her send activity exercised the threshold. She self-diagnosed: "If v9 gate were wired, I would be SILENT right now." The detection layer works; the v9 priority-2 consumer that would translate send-burst into SILENT is still rolled back per the three-state analysis.

Bug 2 fix was necessary but not sufficient for duplicate-engagement resolution. v9 re-integration is the next priority, not deferred work.

## The fix

Both `do-clear-*!` functions rewritten using the superpose-iteration pattern proven by `recent_action_populator.metta`'s pruning logic. See ADR-005 for the architectural decision and the new function shape.

Verification across cycles 1-9 (steady state) and cycles 34-35 (heterogeneous-content transition) confirmed:

- Counts hold at exactly 1 each cycle
- Both POST-CLEAR diagnostic prints show `()` (empty after clear)
- Transitions 0 -> 1 -> 2 propagate correctly without accumulation
- Read-side functions now return current data instead of stale bootstrap

## Open questions

**Why does `car-atom + remove-atom` remove zero atoms in this runtime?** The fix works (empirically proven), but the underlying runtime semantics that cause the bug are not characterized. Possibilities include:
- `car-atom` of a collapse result returns a copy rather than a reference, and `remove-atom` requires reference equality
- The runtime treats accumulated identical atoms as a single storage slot, but `car-atom` extracts a value that doesn't match the stored entry
- Some interaction between `collapse` and `remove-atom` that's specific to this PeTTa configuration

Characterizing the precise cause would require runtime-level instrumentation beyond what loop-level diagnostics can provide. Not blocking; the fix is verified.

**Variable-mangling in Clarity's skill-call REPL queries:** `$v $c` and similar variables in match patterns get rewritten internally to `$_NNNNNN`, producing parse errors. Blocked her Q1-Q4 diagnostic attempts during May 19 session. Still open. Not blocking the Bug 2 fix; affects independent debugging capability from inside the loop.

**First-cycle heavy-clear concern:** Clarity raised the concern that on a non-rebuild restart with accumulated atoms still in `&self`, the first post-fix cycle would need to iterate through 50+ atoms via superpose, potentially hitting a per-cycle execution budget. The rebuild process wiped `&self` so this concern was not exercised empirically. If the container is ever restarted from a state with accumulated atoms (unusual but possible), watch the first wake cycle for stall.

## Process notes

This investigation depended on several disciplines that proved their worth:

- **Project knowledge as authoritative source (F154):** Whenever uncertain about file contents, search project knowledge rather than guessing.
- **Berton's terminal output as ground truth (F155):** When investigation interpretation diverged from runtime evidence, the terminal won. Multiple interpretation errors corrected this way.
- **Reversible diagnostic apply scripts:** Diagnostic prints inserted via `apply_diag_match_shape_test.py` could be removed via `--reverse --apply` without manual file edits.
- **Reading source verbatim (F45 verify before claim):** The agency-balance writer file had to be in project knowledge before drafting the symmetric fix; before it was, no claims about its structure were made.
- **Single recommendation with reason (Habit 5):** When Berton chose Option X vs Option Y for the diagnostic scope, the decision was framed with clear rationale rather than "options theater."

A new working principle emerged from this investigation:

- **F157:** When fixing a detection-layer bug, evaluate whether the consumer for that detection is wired before declaring the fix sufficient. Detection-without-consumer is a known pathology; fixing detection in isolation can expose this pathology actively.

## Layered duplicate-engagement model

This investigation clarified that "duplicate-engagement" was never one bug. It is a layered architectural condition:

1. **Detection layer:** The substrate's ability to recognize when duplicate engagement is occurring. Pre-fix, this was broken because `do-clear-*!` was leaving stale atoms and `current-*` was reading the cycle-1 bootstrap. Bug 2 + 2b fixed this layer.

2. **Consumer layer:** The substrate's ability to ACT on the detection. The v9 aliveness gate priority-2 path (`(current-idle-pattern) send-burst -> SILENT`) is this layer's first consumer. v9 is currently rolled back. This is the next priority.

3. **Input contamination layer:** Stale or sticky content in the prompt that the LLM treats as an active engagement signal. spamShield addressed this layer in earlier work for the silence-after-response case. Other contamination shapes may exist (variable-mangling parser issue may belong here).

Each layer can fail independently. Fixing one layer in isolation can expose pathologies in the others as legible-but-unactioned. This is the F157 lesson made concrete.

## Investigation timeline

- 2026-05-19 evening: Spam-behavioral forensic analysis surfaces the IDLE-PATTERN discrepancy
- 2026-05-19 evening: Three REPL questions sent to Clarity, blocked by variable-mangling parser issue
- 2026-05-19 evening into May 20: Three-state classification analysis (WIRED / NOT-WIRED / NOT-CREATED) maps the architectural surface
- 2026-05-20 morning: Diagnostic apply script drafted and deployed
- 2026-05-20 afternoon: Container observed for ~2200 iterations with diagnostics active
- 2026-05-20 afternoon: Initial misreading of sleep-vs-wake cycle output, corrected via re-reading log evidence
- 2026-05-20 late afternoon: Bug 2 root cause confirmed (uniformly broken since cycle 1)
- 2026-05-20 late afternoon: Bug 2b confirmed via source read of agency_balance_guard_writers.metta
- 2026-05-20 late afternoon: Fix script drafted, dry-run verified, applied
- 2026-05-20 evening: Verification across cycles 1-9 and 34-35; Bug 2 + 2b closed
- 2026-05-20 evening: Bug 4 (v9 consumer not wired) surfaced from Clarity's self-aware send-burst reporting
- 2026-05-20 evening: Investigation closed, fix committed, documents created
"""


# ============================================================================
# EDIT 3: artifact_1 patches (two additive notes, preserving Step 4.5/4.6 history)
# ============================================================================

# The first patch adds a Bug 2 fix note to the do-update-idle-pattern! entry,
# inserted after the existing Step 4.5 split-refactor line.
ART1_ANCHOR_IDLE = "- Step 4.5 split-refactor (May 15 2026): writers (do-clear-idle-pattern!, do-update-idle-pattern!) moved to idle_cycle_detector_writers.metta; pure read helpers remain in idle_cycle_detector.metta per task_state precedent (Discipline 2 refinement). Zero behavior change; clean import boundary for future consumers."

ART1_NEW_IDLE = """- Step 4.5 split-refactor (May 15 2026): writers (do-clear-idle-pattern!, do-update-idle-pattern!) moved to idle_cycle_detector_writers.metta; pure read helpers remain in idle_cycle_detector.metta per task_state precedent (Discipline 2 refinement). Zero behavior change; clean import boundary for future consumers.
- Bug 2 fix (May 20 2026): do-clear-idle-pattern! rewritten to use superpose iteration matching recent_action_populator's verified-working pruning shape. The prior car-atom + remove-atom pattern was removing zero atoms in this runtime since cycle 1, causing 50+ stale (idle-pattern productive 0) atoms to accumulate. current-idle-pattern reads car-atom of accumulated stack = OLDEST atom = cycle-1 bootstrap, explaining the permanently-stuck prompt display. Fix verified end-to-end across cycles 1-9 (steady state) and cycles 34-35 (heterogeneous-content transition). See ADR-005 and docs/investigations/2026-05-20-bug2-clear-fn-investigation.md."""

# The second patch adds a Bug 2b fix note to the do-update-agency-balance! entry.
# Anchor on the Threshold 0.6 line that closes the existing entry's first METTA-CALL POINT bullet.
ART1_ANCHOR_AB = "- 📍 METTA-CALL POINT: Pure MeTTa cycle-level writer. No LLM call. Pre-filtered match per tag literal + size-atom + sum-with-+ (algorithm d, REPL-verified May 15 2026). Threshold 0.6 hardcoded per F42 (dependency-threshold declaration is documentation-only)."

ART1_NEW_AB = """- 📍 METTA-CALL POINT: Pure MeTTa cycle-level writer. No LLM call. Pre-filtered match per tag literal + size-atom + sum-with-+ (algorithm d, REPL-verified May 15 2026). Threshold 0.6 hardcoded per F42 (dependency-threshold declaration is documentation-only).
- Bug 2b fix (May 20 2026): do-clear-agency-balance! rewritten to use superpose iteration matching recent_action_populator's verified-working pruning shape. Same structural bug as Bug 2 in do-clear-idle-pattern! (car-atom + remove-atom removing zero atoms). current-agency-balance reads car-atom of accumulated stack = OLDEST atom = cycle-1 bootstrap, explaining the permanently-stuck (agency-balance dependency-risk 0 1) in prompt context. Adjacent diagnostic addition: do-update-agency-balance! gained DIAG-WRITER-AB-* prints (PERSON, SYSTEM, VERDICT, POST-CLEAR) symmetric to existing DIAG-WRITER-* prints in do-update-idle-pattern!. See ADR-005 and docs/investigations/2026-05-20-bug2-clear-fn-investigation.md."""


# ============================================================================
# UTILITIES
# ============================================================================

def read_file(path: Path) -> str:
    return path.read_text()


def write_file(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        return
    path.write_text(content)


def backup_if_needed(src: Path, bak: Path, dry_run: bool) -> None:
    if dry_run:
        return
    if bak.exists():
        return
    bak.write_text(src.read_text())


def count_substr(haystack: str, needle: str) -> int:
    if not needle:
        return 0
    return haystack.count(needle)


# ============================================================================
# PROCESSORS
# ============================================================================

def process_adr(direction: str, dry_run: bool) -> dict:
    """Create or remove the ADR file."""
    if direction == "apply":
        if ADR_PATH.exists():
            return {
                "path": str(ADR_PATH),
                "ok": False,
                "message": "ADR file already exists; would overwrite. Halting.",
            }
        if not dry_run:
            ADR_PATH.parent.mkdir(parents=True, exist_ok=True)
            ADR_PATH.write_text(ADR_CONTENT)
        return {
            "path": str(ADR_PATH),
            "ok": True,
            "edit": f"create new file ({len(ADR_CONTENT.splitlines())} lines)",
        }
    else:
        if not ADR_PATH.exists():
            return {
                "path": str(ADR_PATH),
                "ok": False,
                "message": "ADR file does not exist; nothing to remove.",
            }
        if not dry_run:
            ADR_PATH.unlink()
        return {
            "path": str(ADR_PATH),
            "ok": True,
            "edit": "delete file",
        }


def process_investigation(direction: str, dry_run: bool) -> dict:
    """Create or remove the investigation log file."""
    if direction == "apply":
        if INVESTIGATION_PATH.exists():
            return {
                "path": str(INVESTIGATION_PATH),
                "ok": False,
                "message": "Investigation file already exists; would overwrite. Halting.",
            }
        if not dry_run:
            INVESTIGATION_PATH.parent.mkdir(parents=True, exist_ok=True)
            INVESTIGATION_PATH.write_text(INVESTIGATION_CONTENT)
        return {
            "path": str(INVESTIGATION_PATH),
            "ok": True,
            "edit": f"create new file ({len(INVESTIGATION_CONTENT.splitlines())} lines)",
        }
    else:
        if not INVESTIGATION_PATH.exists():
            return {
                "path": str(INVESTIGATION_PATH),
                "ok": False,
                "message": "Investigation file does not exist; nothing to remove.",
            }
        if not dry_run:
            INVESTIGATION_PATH.unlink()
        return {
            "path": str(INVESTIGATION_PATH),
            "ok": True,
            "edit": "delete file",
        }


def process_artifact1(direction: str, dry_run: bool) -> dict:
    """Two additive patches to artifact_1: Bug 2 note + Bug 2b note."""
    text = read_file(ART1_PATH)
    pre_lines = text.count("\n")

    if direction == "apply":
        anchors = [
            (ART1_ANCHOR_IDLE, ART1_NEW_IDLE, "Bug 2 note on do-update-idle-pattern!"),
            (ART1_ANCHOR_AB, ART1_NEW_AB, "Bug 2b note on do-update-agency-balance!"),
        ]
        state_check_label = "pre-fix anchors present, post-fix notes absent"
        sentinels_to_be_absent = ["Bug 2 fix (May 20 2026)", "Bug 2b fix (May 20 2026)"]
    else:
        anchors = [
            (ART1_NEW_IDLE, ART1_ANCHOR_IDLE, "Bug 2 note on do-update-idle-pattern!"),
            (ART1_NEW_AB, ART1_ANCHOR_AB, "Bug 2b note on do-update-agency-balance!"),
        ]
        state_check_label = "post-fix notes present"
        sentinels_to_be_absent = []

    for anchor, new, label in anchors:
        if anchor not in text:
            return {
                "path": str(ART1_PATH),
                "ok": False,
                "message": f"Anchor not found for {label}: state check failed ({state_check_label})",
                "pre_lines": pre_lines,
            }
        count = count_substr(text, anchor)
        if count != 1:
            return {
                "path": str(ART1_PATH),
                "ok": False,
                "message": f"Anchor for {label} count = {count}, expected 1",
                "pre_lines": pre_lines,
            }

    if direction == "apply":
        for sentinel in sentinels_to_be_absent:
            if sentinel in text:
                return {
                    "path": str(ART1_PATH),
                    "ok": False,
                    "message": f"Sentinel for already-applied state present: '{sentinel}'",
                    "pre_lines": pre_lines,
                }

    new_text = text
    for anchor, new, label in anchors:
        new_text = new_text.replace(anchor, new, 1)

    backup_if_needed(ART1_PATH, ART1_BAK, dry_run)
    write_file(ART1_PATH, new_text, dry_run)

    post_lines = new_text.count("\n")
    edit_label = (
        "append Bug 2 + Bug 2b fix notes to idle-pattern and agency-balance writer entries"
        if direction == "apply"
        else "remove Bug 2 + Bug 2b fix notes from idle-pattern and agency-balance writer entries"
    )
    return {
        "path": str(ART1_PATH),
        "ok": True,
        "pre_lines": pre_lines,
        "post_lines": post_lines,
        "line_delta": post_lines - pre_lines,
        "edit": edit_label,
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
    print(f"  BUG 2 DOCUMENTATION COMMIT: {direction.upper()} ({'DRY-RUN' if dry_run else 'WRITING'})")
    print("=" * 78)
    print()

    if not ART1_PATH.exists():
        print(f"  ERROR: {ART1_PATH} does not exist. Are you at repo root?")
        return 1

    print(">>> Per-file state checks and edits <<<")
    print()

    results = []
    processors = [
        (process_adr, "docs/decisions/ADR-005-bug2-clear-fn-superpose-fix.md"),
        (process_investigation, "docs/investigations/2026-05-20-bug2-clear-fn-investigation.md"),
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
        if "line_delta" in result:
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
    print(f"  Backup suffix: .bak.bug2_documentation (artifact_1 only)")
    print()
    for label, r in results:
        print(f"  {label}: {r.get('edit')}")
    print()
    print("  Total: 3 documents")
    print("    - docs/decisions/ADR-005-bug2-clear-fn-superpose-fix.md (NEW)")
    print("    - docs/investigations/2026-05-20-bug2-clear-fn-investigation.md (NEW)")
    print("    - docs/design/artifact_1_loop_metta_wiring_diagram.md (PATCHED, +2 notes)")
    print("  Contract: pure documentation commit, no substrate or code changes.")
    print("  Discipline 4: pairs with substrate edit committed via apply_clear_fn_superpose_fix.py.")
    print(f"  Reversibility: python3 {Path(sys.argv[0]).name} --reverse --apply")
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
    print(f"  BUG 2 DOCUMENTATION COMMIT {direction.upper()} COMPLETE")
    print("=" * 78)
    print()
    if direction == "apply":
        print("  NEXT:")
        print("    git status")
        print("    git diff docs/design/artifact_1_loop_metta_wiring_diagram.md")
        print("    git add docs/decisions/ADR-005-bug2-clear-fn-superpose-fix.md \\")
        print("            docs/investigations/2026-05-20-bug2-clear-fn-investigation.md \\")
        print("            docs/design/artifact_1_loop_metta_wiring_diagram.md \\")
        print("            soul/idle_cycle_detector_writers.metta \\")
        print("            soul/agency_balance_guard_writers.metta")
        print("    git commit  # see drafted message in Claude's last turn")
    return 0


if __name__ == "__main__":
    sys.exit(main())
