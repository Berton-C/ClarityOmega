# Corner-Gate v3, Step 0 Findings Package

**Date:** 2026-07-09
**Status:** COMPLETE, read-only. All eight exit criteria (design doc v0.3 Section 5.5) resolved. Amendments below await Berton's ratification. Writer code remains gated until ratified.
**Sources, all hash-certified against the live tree this session:** engine 693089e6...2851, src/loop.metta 1afe674e...b4c5, state_delta_writer.metta 2c661680...17a1 (plus state_delta_writer_writers.metta and coupling_quantale_merge.metta project copies for the ordering note and threshold constants).

---

## (a) Exact signatures, quoted verbatim from the engine

**Edges and chain (lines 770-782):**
```
(: q-intention-action (-> Atom Atom pbit qalignment))
(= (q-intention-action $intention $action $q) (mk-qalignment $intention $action $q))

(: q-action-outcome (-> Atom Atom pbit qalignment))
(= (q-action-outcome $action $outcome $q) (mk-qalignment $action $outcome $q))

(: q-coherence-chain (-> qalignment qalignment qalignment))
(= (q-coherence-chain (mk-qalignment $intention $action (mk-pbit $s1 $c1))
                      (mk-qalignment $action2 $outcome (mk-pbit $s2 $c2)))
   (mk-qalignment $intention $outcome (mk-pbit (* $s1 $s2) (min $c1 $c2))))
```
Chain output pbit: strength multiplies, confidence takes min. pbit shape everywhere: (mk-pbit $s $c), two scalars.

**Hysteresis (4856-4859), single symbol argument:**
```
(= (q-threshold-hysteresis-status? below-lower-band) stable-low)
(= (q-threshold-hysteresis-status? within-band) hold-previous-state)
(= (q-threshold-hysteresis-status? above-upper-band) stable-high)
(= (q-threshold-hysteresis-status? rapid-boundary-flip) blocked-oscillation-risk)
```

**Residual gap (4861-4863), three symbols in, SYMBOL out, not a scalar:**
```
(= (q-residual-threshold-gap? current-support target-threshold residual-available) additional-evidence-needed)
(= (q-residual-threshold-gap? current-support target-threshold residual-absent) cannot-estimate-gap)
(= (q-residual-threshold-gap? target-met target-threshold residual-available) no-additional-evidence-needed)
```
CORRECTION to v0.3: the record's $residual field and the rendered "residual <n>" field are symbolic, not numeric. Amendment in (e).

**Trajectory (5699-5708), five symbols per cycle, then three verdicts:**
```
(= (q-tfs2-polarity-trajectory? $protection $contactability $suspicion $polarity $cycle-ord) -> per-cycle verdict)
  verdicts: defensive-start | metabolizing-transition | metabolized-protection |
            stuck-recurrence-warning | defensive-fixation-risk
(= (q-tfs2-trace-verdict? same-start $verdict-cycle2 $verdict-cycle3) ->
  metabolization-candidate | blocked-defensive-fixation | blocked-repetition-without-metabolization)
```

**q-next-epistemic-move:** symbol-to-symbol map, large domain (state symbol in, move symbol out); also a pbit-form arity at engine line 1693. v3 consumes the symbol form.

**Step 0 discovery, offered for inclusion (DECIDE, new D9):** the engine defines, adjacent to the chain (lines 790-797):
```
(= (q-procedural-honesty (mk-pbit $done-s $verified-c))
   (if (>= $verified-c 0.7) claim-completion name-action-not-verification))
```
This is the computable form of the exact pathology in Clarity's 40-cycle loop (claiming completion without verification). Cost of consuming it: one field. Recommendation: include; the line gains an honesty field only when it reduces name-action-not-verification.

## (b) Accord-summary lossless test: RESOLVED, with one shape consequence

Finding: neither the trajectory functions nor hysteresis consumes accord fields at all. q-tfs2-polarity-trajectory? takes five TFS-2 polarity state symbols; q-tfs2-trace-verdict? takes the three per-cycle trajectory verdicts; hysteresis takes one band-position symbol. Accord statuses feed the cascade direction and the rendered line only. Therefore the compact $accord-summary is lossless for every planned engine call, and the split-field alternative is not required by the engine. The compact field stands.

The real shape consequence the test surfaced: the record must store the PER-CYCLE POLARITY-TRAJECTORY VERDICT, because cycle 3's q-tfs2-trace-verdict? consumes cycles 1 through 3's verdicts. New field $polarity-verdict, amendment in (e).

## (c) Dominant-surface priority: implementable deterministically

The markup-3 order (failed-query > runtime-output > tool-result/capability-result > source-read > user-words > task-state > cycle-trace > none) compiles to a single pure C12-safe cascade function consulted by the one record writer. No conflict found: every 2.1 surface appears exactly once in the order. One order, one function, one writer.

## (d) Cycle ordinal source: RESOLVED, verified in certified loop.metta

The loop's iteration binding $k is the ordinal, already passed to every tail populate hook: populate-recent-action $sexpr $msgnew $k, populate-state-delta ... $k, populate-coupling-verdict $k, populate-corner-window! $metta_cmds $k. v3's writer hook takes $k identically. $ord equals $k.

## (e) Record field packing: FIXED, pending ratification

Amended shape (changes from v0.3: $polarity-verdict added per (b); $residual split into $support scalar plus $residual-gap symbol per (a); $context split into three flat fields for NACE precondition matchability):

```
(coupling-cycle-record $ord $contact-count $dominant-surface $command-sig
                       $chain-state $polarity-verdict $accord-summary
                       $support $residual-gap $next-move
                       $ctx-phase $ctx-msgnew $ctx-soul
                       $producer $depends-on $ts)
```
16 flat fields, all scalars or symbols, all ground via let* before add-atom. $support is the chain pbit strength scalar (band-derivation lineage); $residual-gap is the symbolic gap output. Context alternative if 16 is too wide: one packed $context symbol (equality-matchable only, loses per-component NACE matching). Recommendation: the 16-field split. DECIDE.

Band-position derivation (feeds hysteresis): the adapter maps $support to the band symbol via two threshold constants. The engine defines no numeric thresholds (verified: only a threshold-policy symbol exists). Existing v2 precedent, quoted from coupling_quantale_merge.metta line 86: (corner-threshold-pbit) is (mk-pbit 0.6 0.5), 0.6 matching agency_balance_guard's dependency-threshold, marked TUNING TARGET there. Recommendation (DECIDE, new D10): lower-band 0.4, upper-band 0.6 (upper aligned to the existing 0.6 precedent, symmetric 0.2 band width), adapter-side constants in the pure file, named tuning targets. rapid-boundary-flip derivation: band position differing from BOTH prior window records' positions in opposite directions; derivable from the window, no new atoms.

## (f) As-built state-delta shape: CONFIRMED

(state-delta $cycle-id $verdict), verdict in {forward, none}, SINGLETON by clear-then-write (car-atom-of-stack trap documented in the file). Known risk quoted from source: time-varying command returns can read forward spuriously (novelty compare), named TUNING TARGET. v3 consumes it read-only via latest-state-delta-verdict.

## (g) Discipline 6B surveys: RESULTS channel and 166 site, from certified loop.metta

**Writers into the chain:** $sexpr_verdict (soul-gated batch) enters at line 166: ($sexpr_gated (apply-corner-gate-v2 $sexpr_verdict $msgnew)). $results executes $sexpr_gated with COMMAND_RETURN wrapping and error handling. Line 168: ($results_final (gate-aware-results $results)), the v2 echo filter and the injection point where the legibility line will ride.

**Consumers downstream (the load-bearing seam):** $results_novel at 174 compares repr $results (NOT $results_final) against &lastresults; line 222 updates &lastresults FROM $results_final; line 54 renders &lastresults into her next prompt as LAST_SKILL_USE_RESULTS. Consequence for cutover: whatever gate-aware-results is rebodied to append, the line enters her prompt via &lastresults, and the novelty compare stays on raw $results, so the appended line CANNOT poison the state-delta forward/none classification. That separation is exactly what v3 needs and it already exists.

**Cycle-tail hook order (load-bearing, quoted ordering):** populate-recent-action, then populate-state-delta (must follow it, per the writer file's own note), then populate-coupling-verdict, then populate-corner-window!, then idle/agency updates, then diagnostics. v3's do-record-coupling-cycle! hook takes the populate-corner-window! position, after populate-coupling-verdict, exactly as designed.

**Cutover mechanics (confirms D4 plan):** three surgical swaps at proven sites: the $sexpr_gated binding rebodies to pass-through (name and arity kept, the proven v2-monolith rebody pattern), gate-aware-results rebodies from echo filter to line appender (name and arity kept), populate-corner-window! hook line replaced by the v3 writer hook. Retirement then deletes the dead definitions and the corner_window import.

**Configuration levers:** wakeupInterval, maxFeedback (truncates LAST_SKILL_USE_RESULTS via last_chars; the line must fit comfortably inside maxFeedback, checked at Step 3), maxNewInputLoops. No other constants touch the seam.

## (h) D7 per-leg derivation table, for markup

All derivations mechanical, from Contract 1/2 records. aligned/misaligned per leg:

**Task-accord (intention, action, outcome):** intention aligned when this cycle's command class is consistent with the prior record's $next-move category (TRACE; window-filling cycles feed the accord as not-computed). Action aligned when the batch executed without format error (MECH, ERROR_FEEDBACK absent). Outcome aligned when state-delta reads forward (MECH).

**Contact-accord (contact, audit, navigation):** contact aligned when a qualifying contact-event exists this cycle (MECH, per the ratified 2.1 rule). Audit aligned when the chain-state computed and persisted this cycle (TRACE). Navigation aligned when evaluated at N+1: command signature changed following the computed next-move, or next-move was preserve-course and signature appropriately held (TRACE).

**TFS-2 polarity state inputs (feed q-tfs2-polarity-trajectory?):**
protection-flat-low-warrant: same failing signature at consecutive-fail-count 2 or more AND state-delta none. protection-softens-warrant-rises: signature changed after error visibility (corrective-probe) AND forward delta. contactability-flat: contact-count 0, or cycle-trace-only contact. contactability-rises: contact-count increased versus prior record. suspicion-rises: consecutive-fail-count increased. suspicion-decays: fail-count reset to 0. polarity-blocks: state-delta none AND repetition present. polarity-supports: forward delta present. $cycle-ord: position within the 3-window (cycle-1/2/3).

Her 40-cycle loop replays through this table as: protection-flat-low-warrant, contactability-flat, suspicion-rises, polarity-blocks, reducing stuck-recurrence-warning at window position 2 and defensive-fixation-risk at 3, trace verdict blocked-repetition-without-metabolization. The moment ERROR_FEEDBACK became visible and her signature changed: metabolizing-transition. The table reproduces the lived case.

---

## Ratification items (all DECIDE, nothing coded)

1. Record shape at 16 fields per (e), or packed-context alternative.
2. $residual correction: symbolic $residual-gap plus $support scalar (engine fact, not optional; the choice is field naming).
3. New D9: consume q-procedural-honesty (recommended: yes, one field, reduces only on the named pathology).
4. New D10: band threshold constants 0.4/0.6 adapter-side, named tuning targets (0.6 anchored to the existing precedent).
5. The (h) derivation table as the v1 basis.
6. Cutover mechanics per (g): three rebody/replace swaps at the proven sites.

On ratification of these six, Step 0 closes, the design doc amends to v0.4, and writer code (Sequence step 1, the pure file) is unblocked.

Document end.
