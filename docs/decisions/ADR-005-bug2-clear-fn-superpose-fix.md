# ADR-005: Superpose-iteration clear in awareness-organ writers

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
