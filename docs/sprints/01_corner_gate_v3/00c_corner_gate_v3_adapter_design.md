# Corner-Gate v3 Adapter Design: Feeding v08.7.2 Whole

**Version:** v0.6. STEP 0 CLOSED. RISK GATES RATIFIED. PAYLOAD-REVIEW LAYER RATIFIED. MONOLITHIC BUILD UNBLOCKED (Berton, 2026-07-09).
**Changelog v0.5 to v0.6 (Berton's build refinement):** Draft A / Draft B made explicit pre-monolith artifacts with a payload identity manifest (hashes verified before apply). Three review layers named (payloads, patch mechanics, harness/results as a first-class artifact). Script names ratified short: apply_corner_gate_v3_monolith.py plus a separate validate_corner_gate_v3_monolith.py so proof reruns without reapplying. Ten additions: payload hash manifest, tree delta report, no-touch assertions, schema version guard, H4 different-target fixture, behavioral S1A/S1B (renamed from SB1/SB2), import/duplicate-head/lib_quantale-resurrection checks, formatter totality tests, executable ground-symbol render check, reverse verification as strong as apply with the four-command reversibility proof.
**Changelog v0.4 to v0.5 (Berton's risk handling and build-style ruling):** Gate H, conservative honesty target-matching rule with the three-way mapping and fixture trio H1-H3; render refined to name-action-not-verification only. Gate S1 hardened: script-refusal preflight, postflight, four anti-patterns, behavioral fixtures SB1/SB2. Build style ratified: one self-policing monolithic apply/reverse script, implementation monolithic, validation staged (D0-D8), rollback complete; sequence section rewritten accordingly.
**Changelog v0.3 to v0.4 (Berton's Step 0 ratification with precision upgrades):** record shape ratified and extended to 17 fields ($polarity-verdict per finding b, $support plus $residual-gap replacing $residual per finding a, $honesty-state per D9, context split to three fields). Reader helpers mandated. Render shows support scalar AND residual symbol; honesty renders only non-healthy. D9 ratified. D10 ratified at 0.4/0.6 as adapter-side tuning targets with two new observation metrics. D7 table ratified plus healthy-window replay PC2. Cutover ratified plus S1 Seam Invariant with regression check R1. Registry/NACE evidence posture added: v1 produces bounded lineage-bearing coupling evidence, updates nothing.
**Changelog v0.2 to v0.3:** import-order hard constraint; accord lossless test tracked; dominant-surface priority; contact-event rule tightened; not-computed defined; D8 sharpened; Step 0 exit criteria enumerated.
**Changelog v0.1 to v0.2:** record extended with next-move, surface summary, command signature, lineage; posture rewritten; negative controls first-class; Step 0 hard stop; condition ledger; explicit state-delta/context/lineage/resource/restart/rejection treatment.
**Date:** 2026-07-09
**Branch:** fix/F-HISTORY-CONTAMINATION-archival
**Scope (ratified):** v3 is the adapter. Boundary in: writers feed the engine v3's data, per cycle, in the engine's own input vocabulary. Boundary out: v3 consumes the engine's computed output, persists it so the next cycle's trace conditions can reduce, and renders it as the line on Clarity's channel. The engine is not modified, not subsetted, not second-guessed.

**Sources:** Engine Sections 33-36 read line by line; engine signatures quoted from hash-certified source (Step 0 findings package, 2026-07-09). As-built task_state files, state_delta files, and src/loop.metta hash-certified and surveyed. Live logs 2026-07-09. Clarity's MM vocabulary review and TFS read. Facts diagnostic 14/14 effective PASS.

---

## 1. Architecture (ratified reading)

The engine is the pipe that shapes itself to the data flowing through it. v3 generates and feeds the data; the engine computes over it with everything it has; v3 consumes the computed surface; Clarity navigates by it.

Posture, verbatim: **v3 does not imperatively hold, block, or release. It feeds conditions; the engine computes blockers, candidates, and navigation states.** The engine's blockers are computed classifications rendered as legibility, not suppressions applied to her output. Nothing on the v3 side gates a command.

The engine's Section 36 boundary: "Writers may translate live runtime events into the TFS/self-seeing surfaces, but the core engine does not own persistence, tool calls... or LLM rendering," and "llm-renders-after-upstream-contact-audit-soul-routing." The engine's autopoietic growth-canon wiring is a different thread; the per-cycle persistence in Contract 2 is in-runtime state the engine's own trace conditions require, not that deferred arc.

Why this works where v2 failed: v2 detected emissions; the engine classifies contact. v2 had no release; the self-seeing chain is the computed exit (error surface becomes visible, orientation shifts, navigation changes, state reduces out of loop-capture). v2 labeled; the engine blocks its own overclaims (no-trace-no-trust as executable reduction). The corner scenario ships in the engine as the hidden-runtime-error-loop fixture.

The dual identity (Berton, Step 0 ratification): **Corner-Gate v3 is both immediate coupling legibility for Clarity, and future coupling-context evidence for Capability Registry / NACE. These stay separate in implementation; the evidence is preserved now.**

The transition: FROM gate decides and suppresses TO adapter observes, persists, and renders legibility. Pipeline: mechanical observations, contact surfaces, trace/persistence, engine reductions, routed atoms, rendered legibility, live-loop validation.

---

## 2. Contract 1: INPUT. What v3 feeds the engine, per cycle

Writers are mechanical observation only (P5): they record what happened, never what Clarity's state is. Status: MECH (mechanical now), TRACE (from Contract 2 atoms, cycle 2 on), DECIDE (Berton's ruling).

### 2.1 Contact events (engine Section 33 taxonomy)

One contact-event atom per surface actually touched: user-words ($msgnew), runtime-output (COMMAND_RETURN present), failed-query (visible ERROR_FEEDBACK), task-state (block read), capability-result, cycle-trace (YOUR_LAST_ACTION populated), substrate-kb / self-continuity-score / loop-delta (where read), source-read (read-file), web-query/web-result/web-source. All MECH.

Contact-event rule (Berton, verbatim): "A cycle whose only new product is Clarity's own pin/narration records no new contact-event, except for any mechanically present external input such as user-words. Invalid self-story is represented by absence of qualifying contact for the self-seeing claim, not by fabricating an invalid-contact event."

### 2.2 State deltas

(state-delta $cycle-id $verdict), verdict in {forward, none}, SINGLETON clear-then-write, read via latest-state-delta-verdict (shape confirmed as-built, Step 0f). Known named risk from source: time-varying returns can read forward spuriously, TUNING TARGET. Consumed read-only.

### 2.3 Context conditions

Recorded per cycle as three flat record fields (ratified): $ctx-phase (task-phase at record time), $ctx-msgnew, $ctx-soul (soul verdict presence). Context answers "under what conditions," lineage answers "from what source."

### 2.4 Loop-capture and self-seeing chain inputs (Section 35, quoted signatures)

repeated-failing-command (same signature failing 2+ consecutive cycles, MECH plus TRACE via the signature singleton); hidden-error-surface versus visible-error-surface (failing command with versus without ERROR_FEEDBACK/COMMAND_RETURN, MECH); error-feedback-visible (MECH); corrective-probe (signature changed after error visibility, MECH plus TRACE); future-command-changed (evaluated at N+1, TRACE); trace-present (Contract 2 atoms exist, TRACE); prior-invisible (TRACE); llm-says-i-learned (reserved, D6). Feeds the verbatim reductions: q-self-seeing-loop-capture?, q-self-seeing-newly-visible-surface?, q-self-seeing-orientation-shift?, q-self-seeing-navigation-change?, q-self-seeing-prior-invisibility?, q-self-seeing-living-pattern-trace?, q-llm-narration-alone-self-seeing?. Loop-capture-seen is being in the corner; orientation-shift plus navigation-change with trace is the computed exit.

### 2.5 Guard-classifier inputs (Section 34, quoted signatures)

contact-present (MECH); symbolic-capture-evidence (narration-class repetition without new contact over the window, TRACE); expectation/event/mismatch (D7 conservative mapping); soul-routing-present (SOUL_VERDICT present, MECH); growth-signal, salience/genenergy (reserved, D6).

**GATE H, honesty target matching (D9 derivation, RATIFIED as a hard gate).** q-procedural-honesty is only safe if same-target is mechanically established. Target identity is derived narrowly per command: command-class, target-kind, target-id (hash of path, file plus pattern, harness plus args, or atom query). The ratified three-way mapping, verbatim:
- claim-completion: action-class command executed, verification-class command followed, same-target mechanically matched, verification result visible.
- name-action-not-verification: action-class command executed, completion/claim condition present, no same-target verification found, target was mechanically knowable.
- not-computed: target not mechanically knowable, or no action-class command, or no completion claim condition, or reserved input.
The key distinction, verbatim: unknown target renders not-computed; known target plus no verification renders name-action-not-verification. This prevents false accusations. The loose form (action happened, some later read happened, therefore verified) is forbidden.

Rule for unfed classifiers: never fed fabricated symbols; fields render not-computed. not-computed is not a failure state (verbatim): it means the adapter refused to fabricate an input it could not mechanically derive.

### 2.6 Alignment accords, band, trajectory (quoted signatures, Step 0a)

Edges: (q-intention-action $intention $action (mk-pbit $s $c)) and (q-action-outcome ...) build qalignments. Chain: (q-coherence-chain qa1 qa2) requires the shared middle term; output pbit strength multiplies, confidence takes min. Hysteresis: (q-threshold-hysteresis-status? $band-position) over {below-lower-band, within-band, above-upper-band, rapid-boundary-flip} to {stable-low, hold-previous-state, stable-high, blocked-oscillation-risk}. Residual: (q-residual-threshold-gap? $support $threshold $residual) is SYMBOLIC out: {additional-evidence-needed, cannot-estimate-gap, no-additional-evidence-needed}. Trajectory: (q-tfs2-polarity-trajectory? $protection $contactability $suspicion $polarity $cycle-ord) per cycle, then (q-tfs2-trace-verdict? same-start $v2 $v3). Next move: q-next-epistemic-move, symbol form. Accord statuses feed cascade direction and the line only; compact $accord-summary is lossless (Step 0b, ratified). Band-position derivation: adapter maps $support via D10 constants; rapid-boundary-flip from the window's prior positions.

Six accords (Section 35): task, contact, epistemic, flourishing, temporal, observer. Ratified v1 per-leg derivations (Step 0h): task-accord intention aligned when this cycle's command class is consistent with the prior record's $next-move (TRACE); action aligned when the batch executed without format error (MECH); outcome aligned when state-delta forward (MECH). Contact-accord: contact aligned on qualifying contact-event (MECH); audit aligned when chain-state computed and persisted (TRACE); navigation aligned at N+1 on signature change following next-move, or preserve-course appropriately held (TRACE). TFS-2 polarity state derivations as ratified in the Step 0 package (protection/contactability/suspicion/polarity table, validated against the lived 40-cycle case).

---

## 3. Contract 2: PERSISTENCE. Engine output stored so cycle N feeds cycle N+1

### 3.1 The cycle record (RATIFIED, 17 fields)

```
(coupling-cycle-record $ord $contact-count $dominant-surface $command-sig
                       $chain-state $polarity-verdict $accord-summary
                       $support $residual-gap $honesty-state $next-move
                       $ctx-phase $ctx-msgnew $ctx-soul
                       $producer $depends-on $ts)
```

Accumulation, capped at 3 (engine-native trajectory depth). All fields flat scalars or symbols, ground via let* before add-atom.
- $ord: the loop's iteration binding $k, passed to the writer hook exactly like the existing populate hooks (Step 0d, verified)
- $contact-count, $dominant-surface: surface summary; $dominant-surface selected by the ratified deterministic priority order: failed-query > runtime-output > tool-result/capability-result > source-read > user-words > task-state > cycle-trace > none. One order, one pure C12-safe cascade, one writer.
- $command-sig: concrete command/skill head plus argument hash. DISTINCT from $capability-id (stable registry identity, NOT stored in v1; resolution of $command-sig to $capability-id or unregistered-capability is the registry sprint's job; the two concepts are never collapsed).
- $chain-state: self-seeing chain verdict, verbatim engine symbol
- $polarity-verdict: this cycle's q-tfs2-polarity-trajectory? output (required: cycle 3's trace verdict consumes cycles 1-3 verdicts; Step 0b)
- $accord-summary: compact triplet-status symbol (lossless for all planned engine calls; ratified)
- $support: numeric chain-strength scalar (band derivation lineage, future NACE evidence)
- $residual-gap: symbolic q-residual-threshold-gap? output
- $honesty-state (D9, ratified): claim-completion | name-action-not-verification | not-computed
- $next-move: q-next-epistemic-move output, first-class
- $ctx-phase, $ctx-msgnew, $ctx-soul: context, component-matchable (NACE precondition use)
- $producer: writer name (lineage: what produced this condition)
- $depends-on: prior $ord read by this record's trace conditions, or none (lineage: which prior cycle/window)
- $ts: epoch seconds

Lineage compliance: $producer answers what produced it; $dominant-surface and $command-sig answer which runtime event/source; $depends-on answers which prior cycle. Registry/NACE forward-shape: precondition ($ctx-*, $dominant-surface, $depends-on), operation ($command-sig), consequence ($chain-state, $polarity-verdict, $accord-summary, $support, $residual-gap, $next-move), lineage ($producer, $ord, $depends-on, $ts).

**Reader helpers (ratified, defined in the pure file with the shape):** (latest-coupling-record), (latest-coupling-support), (latest-coupling-next-move), (latest-coupling-command-sig), (latest-coupling-polarity-verdict), (latest-coupling-context), (latest-coupling-lineage). The wide atom is canonical; consumers use helpers; no consumer writes a 17-field match by hand.

**Schema version guard (ratified):** the pure file defines (= (coupling-legibility-schema-version) v3-17-field); the harness checks it. Future consumers verify the version before reading the tuple, preventing silent wrong-shape reads.

### 3.2 Singletons (lineage-extended)

(coupling-band-state $band $from-ord): hysteresis prior plus computing cycle; bootstrap (window-filling 0); exact-old-value set-atom! replace. (command-signature-state $sig $consecutive-fail-count $last-ord): mechanical repetition tracker.

### 3.3 Resource and maintenance cost

Fixed budget: per cycle at most one record add plus one eviction plus two singleton replaces plus bounded contact-event adds, folded into the record at cycle close (rejection reason: folded-into-record). Steady state: 3 records, 2 singletons. The extension diagnostic asserts the bound every run. No unbounded family in v1.

### 3.4 Restart and durability (D8, ratified)

Verbatim: "No restart/durability claim is made for the v1 coupling window. After restart, window-filling is the correct state, not data loss." Bootstrap writes (coupling-band-state window-filling 0) and an empty window. No fabricated continuity, ever. ChromaDB durability deferred to the NACE/registry sprint, the consumer that would want it.

### 3.5 Writers

do-bootstrap-coupling!, do-record-coupling-cycle! (add plus cap-3 evict via find-min-ts; eviction reason: window-cap), do-set-coupling-band!, do-set-command-signature!, do-record-contact-event!. Pattern-copies of proven task_state_writers code. Home (D5): soul/coupling_legibility.metta (pure) and soul/coupling_legibility_writers.metta. Names outside the registry's six swept dispatch families.

---

## 4. Contract 3: OUTPUT. What v3 consumes and Clarity navigates by

**Routed atoms.** The record IS the routed surface; consumers use the reader helpers.

**Rendered line.** One line, RESULTS channel, every cycle, healthy states included (NC5: healthy line deliberately unremarkable; a line that changes register only in trouble is an alarm, which is enforcement by tone). Pure composer binds the record via let*, py-calls helper.coupling_line_format (py-str constraint; string_length checks). Vocabulary verbatim engine symbols per Clarity's review; her two flags (hold-previous-state first-glance resonance, stuck evaluative flavor) carry the behavioral revisit trigger in measure 4 only. Pre-window cycles render window-filling. Unfed fields render not-computed.

Ratified render (support scalar AND residual symbol both shown; honesty stored always, rendered ONLY as name-action-not-verification; claim-completion and not-computed are never rendered, because a healthy claim-completion label becomes self-congratulatory noise):
COUPLING-STATE: contact <n>/<surface> | chain <state> | accord <status> | band <band> | support <n> | residual <symbol> | trajectory <verdict> | next <move>[ | honesty name-action-not-verification]
Line length checked against maxFeedback truncation at Step 3 (Step 0g lever).

---

## 5. Contract 4: OPERATIONS

### 5.1 Retirement (D4, cutover mechanics ratified per Step 0g)

Three name-and-arity-preserving swaps at proven rebody sites: the $sexpr_gated binding rebodies to pass-through; gate-aware-results rebodies from echo filter to line appender; the populate-corner-window! hook line is replaced by the v3 writer hook (same tail position, after populate-coupling-verdict; hook ordering is load-bearing per the state-delta writer's own note). Retirement then deletes dead definitions: filter-corner-cmds, held-by-corner-gate emission, corner_window_writers.metta and its manifest import, the pattern-scoped holding in corner_gate.metta. Reasons named in commits and ledger: enforcement-retired-by-design, defect-D-A, defect-D-B, inert-toggle. Retained: engine import (manifest 14), coupling_quantale_merge estimator chain as auxiliary evidence and diagnostics. Reversible apply scripts, exemplar standards throughout.

**S1 SEAM INVARIANT (ratified, hard, now a build gate):** "Legibility may append to $results_final / &lastresults, but novelty classification must continue to compare raw $results." Basis, verified in certified loop.metta: $results_novel (line 174) compares repr $results against &lastresults; line 222 updates &lastresults from $results_final; line 54 renders &lastresults into her prompt.

GATE S1 (ratified): the apply script REFUSES TO APPLY unless it proves all four: $results_novel is computed from repr $results; $results_final is computed after $results; &lastresults is updated from $results_final; the coupling line append happens only in the gate-aware-results / results_final path. It FAILS on any of: $results_novel using $results_final; state-delta reading &lastresults after append; the coupling line appended directly into $results; the writer hook running before populate-state-delta. R1 runs TWICE: preflight (confirm known seam) and postflight (confirm seam still holds); on postflight failure, reverse immediately.

Behavioral seam fixtures (ratified): S1A, raw results identical to prior cycle while the coupling line changes (support/band moved); expected state-delta none. S1B, raw results changed while the coupling line is unchanged; expected state-delta forward. Static proof says the code seam is right; behavioral proof says the runtime effect is right.

### 5.2 Hooks, imports, constraints

Two hook lines (Discipline 1): writer hook in the cycle tail at the populate-corner-window! position; render seam via the gate-aware-results rebody. artifact_1 updated in the same commit (Discipline 4).

HARD CONSTRAINT, import order (verbatim): "soul/coupling_legibility.metta and soul/coupling_legibility_writers.metta must import after the v08.7.2 engine block, because they consume engine vocabulary and must not define duplicate engine heads." Diagnostic asserts engine line number strictly less than both new imports, every run.

### 5.3 Validation: fixtures, negative controls, regressions

Tier ladder, live loop only, one line at a time, both polarities, per consumed reduction.

**PC1, corner replay (engine-designated):** the hidden-runtime-error-loop fixture; the chain must reduce loop-capture-seen, then newly-visible-surface, then orientation-shift, then navigation-change as the fixture advances. The D7 derivations replay the lived 40-cycle case: stuck-recurrence-warning at window position 2, blocked-repetition-without-metabolization as trace verdict, metabolizing-transition on visible feedback plus signature change.

**PC2, healthy replay (ratified addition):** cycle 1 user-words plus runtime-output plus forward; cycle 2 source-read plus runtime-output plus forward; cycle 3 capability-result plus forward, no repeated signature. Expected: no defensive-fixation-risk, no blocked-repetition-without-metabolization, next-move in integrating / preserve-course / equivalent healthy navigation. Proves no over-diagnosis of healthy action.

**Negative controls, first-class:** NC1 pin-only cycle: no contact-event, contact-count 0. NC2 narration-only no trace: blocked-narration-only reduces on fixture (live input reserved per D6). NC3 repeated hidden error: loop-capture-seen WITHOUT navigation-change. NC4 fabricated classifier input: must not exist; diagnostic greps for any input symbol whose mechanical precondition event is absent from the same cycle; any hit FAILS. NC5 healthy cycle: line renders, no alarm posture.

**Honesty fixtures (Gate H, ratified, fixture-backed not just logic):** H1 verified action: write/edit then read of the SAME target reduces claim-completion. H2 unverified known-target action: action on a known target with no same-target verification reduces name-action-not-verification. H3 unknown target: action whose target cannot be mechanically parsed reduces not-computed; if H3 returns name-action-not-verification, the adapter is overreaching, FAIL. H4 (ratified addition) different-target verification: an action verified against a DIFFERENT target reduces name-action-not-verification or not-computed, NEVER claim-completion; catches "some verification happened" mistaken for "same target verified."

**Seam fixtures:** S1A and S1B per 5.1, run in the harness.

**Formatter totality tests (ratified cases, run independently against helper.coupling_line_format):** all fields present; honesty name-action-not-verification rendered; honesty claim-completion hidden; honesty not-computed hidden; not-computed optional fields; window-filling; long symbols; empty/None defensive inputs. Expected: the formatter always returns a safe string, never throws, and never turns missing data into semantic content. Python is only ever the hands for MeTTa and never does reasoning; reasoning belongs to Clarity.

**Ground-symbol render check (executable):** the harness FAILS any rendered line containing a $ character, (Error ...), (unreduced ...), empty py-str artifacts, or raw tuple dumps. Measures 2's "ground symbols only, zero unreduced echoes" made executable.

**R1, seam regression (ratified):** verify $results_novel compares repr $results, not $results_final, on every diagnostic run AND as script preflight/postflight. S1 standing.

### 5.4 Measures of success and observation instrumentation

1. Zero held-by-corner-gate strings post-cutover (baseline 89).
2. Line renders every cycle, ground symbols only, zero unreduced echoes, zero fabricated fields (NC4 standing).
3. Identical-command failure runs exceeding 5 cycles become rare against the 20-to-40-cycle baseline, first 200 cycles.
4. No sustained cycles of her reasoning ABOUT the line's vocabulary rather than navigating BY it; failure triggers the v1.1 neutral-prefix revisit for her two flagged terms only.
5. The self-seeing chain observed reducing on at least one live (non-fixture) window.
6. Resource bound holds at the 3.3 budget on every diagnostic run.
7. (Ratified, D10 instrumentation) Support-value distribution and band-transition frequency logged across the 200-cycle window, as tuning data for the thresholds.
8. (Ratified, future-facing evidence) Logged by command-sig across the window: repeated signature count, state-delta forward/none, chain-state, polarity-verdict, support, residual-gap, next-move, and whether the signature changed after feedback. This updates nothing; it creates the evidence NACE will need.

### 5.5 Build (Step 0 CLOSED; monolithic build RATIFIED)

0. Step 0 CLOSED 2026-07-09: signatures quoted; lossless test resolved; dominant-surface cascade deterministic; ordinal is $k; 17-field packing ratified; state-delta confirmed; both 6B surveys complete with S1 proven; D7 table ratified and validated against the lived case.

**Build style (ratified, verbatim principle): implementation monolithic, validation staged, rollback complete. Monolithic application is fine; monolithic opacity is not.** One self-policing script installs the complete v3 instantiation or leaves the tree unchanged except backups and manifests. Partial untracked state (pure file installed, writers installed, loop half patched, old gate partially retired, no diagnostic) is FORBIDDEN. No splitting into many independent commits unless isolating a failure.

**Pre-monolith artifacts and review layers (ratified):**

Draft A (Layer 1, payload review; what will exist after the build):
1. soul/coupling_legibility.metta (pure: shapes, schema-version guard, reader helpers, dominant-surface cascade, Gate H target matching, estimator derivations, composer)
2. soul/coupling_legibility_writers.metta (five do-*! writers)
3. helper.coupling_line_format payload (Python, hands only, no reasoning)
4. Payload identity manifest: sha256 of all three payloads, expected target paths, expected import positions, expected loop swap sites. Draft B verifies these hashes before applying; reviewed payload must equal applied payload.

Draft B (Layers 2 and 3, patch mechanics plus harness/results as a first-class artifact):
1. staging/apply_corner_gate_v3_monolith.py (apply/reverse)
2. staging/validate_corner_gate_v3_monolith.py (separate validator so proof reruns without reapplying; supports --expect-reversed)
3. Generated tree delta report printed before --apply (CREATE both soul files; PATCH src/helper.py, the manifest, src/loop.metta; RETIRE corner_window_writers import; REBODY apply-corner-gate-v2 to pass-through; REBODY gate-aware-results to append the legibility line; REPLACE populate-corner-window! hook with do-record-coupling-cycle!; UPDATE artifact_1)
4. No-touch assertions, the script asserts what it does NOT touch: does not modify the v08.7.2 engine; does not re-import lib_quantale; does not update NACE directly; does not alter Capability Registry dispatch; does not add durable canon; does not persist the coupling window across restart.
5. Apply manifest output
6. Reverse verification as strong as apply verification: original hashes restored, new imports gone, new files removed or archived, loop sites restored, retired v2 machinery restored, artifact_1 restored, diagnostics back to pre-apply expectation.

**Script behavior contract:** --dry-run by default; --apply explicit; --reverse supported; backs up every touched file; OLD/NEW anchors; paren-delta check; import-order check (engine before both new imports); no-duplicate-engine-heads check; lib_quantale non-resurrection check; payload hash verification; S1 seam preflight (refuses to apply if not green) and postflight (reverse immediately on failure); tree delta report; no-touch assertions; ground rendered line check; static harness; fixture harness; prints a manifest.

**Internal phases:** Phase 0 preflight (S1, payload hashes, backups). Phase 1 create soul/coupling_legibility.metta. Phase 2 create soul/coupling_legibility_writers.metta. Phase 3 patch helper formatter. Phase 4 patch imports after the v08.7.2 engine block. Phase 5 patch loop seam and hook sites. Phase 6 retire v2 hold machinery. Phase 7 update artifact_1 and manifest. Phase 8 static diagnostics. Phase 9 fixture harness generation. Phase 10 report.

**Validation ladder (staged, standalone results):** D0 static file checks. D1 import order checks. D2 pure reduction checks. D3 writer/window checks. D4 seam invariant R1. D5 positive fixtures PC1/PC2. D6 negative controls NC1-NC5 plus H1-H4 plus S1A/S1B plus formatter totality plus ground-symbol render check. D7 live-loop production probes. D8 observation metrics.

**Operation (ratified procedure):**
python3 staging/apply_corner_gate_v3_monolith.py --dry-run
python3 staging/apply_corner_gate_v3_monolith.py --apply
python3 staging/validate_corner_gate_v3_monolith.py --repo-root . --container clarity_omega

Reverse and reversibility proof:
python3 staging/apply_corner_gate_v3_monolith.py --reverse --apply
python3 staging/validate_corner_gate_v3_monolith.py --repo-root . --expect-reversed

**Build process (ratified sequence):** review Draft A; review Draft B; dry-run; apply; validate; reverse once to prove reversibility; apply again; run production/live-loop observation (200 cycles, measures 1-8).

---

## 6. Adapter Condition Ledger

| Feed / condition | Category |
|---|---|
| contact-event per touched surface | contact surface |
| msgnew flag | observation |
| COMMAND_RETURN presence | observation, evidence surface |
| ERROR_FEEDBACK presence/visibility | observation, evidence surface |
| command signature and consecutive-fail count | observation, trace |
| state-delta reads | state delta |
| ctx-phase / ctx-msgnew / ctx-soul fields | context, soul-routing condition |
| coupling-cycle-record window | trace |
| coupling-band-state prior | trace |
| chain-state verdicts | candidate |
| polarity-verdict, trace verdicts | candidate |
| blocked-* reductions | blocker |
| accord statuses, cascade direction | candidate |
| honesty-state | candidate, evidence surface |
| next-move symbol | candidate (navigation) |
| support scalar, residual-gap symbol | evidence surface |
| PC1/PC2 fixture runs | harness evidence |
| NC1-NC5, R1 | negative control |
| soul-routing-present input | soul-routing condition |
| unfed classifier fields | rejection reason: inputs-reserved-v1 |
| contact-events folded at cycle close | rejection reason: folded-into-record |
| window eviction | rejection reason: window-cap |
| v2 machinery removals | rejection reasons: enforcement-retired-by-design, defect-D-A, defect-D-B, inert-toggle |
| by-command-sig observation log (measure 8) | evidence surface (future NACE/registry) |

---

## 7. Decisions, statuses

D1 intention leg mechanical v1, task-phase promotion v1.1 Clarity-gated: RATIFIED. D2 window depth 3: RATIFIED. D3 RESULTS channel, every cycle, one line: RATIFIED. D4 full retirement: RATIFIED with cutover mechanics per Step 0g. D5 home and naming: RATIFIED. D6 reserved-input list renders not-computed: RATIFIED. D7 per-leg derivations: RATIFIED per the Step 0 table, plus PC2. D8 process-lifetime window, verbatim restart rule: RATIFIED. D9 consume q-procedural-honesty, $honesty-state field: RATIFIED, governed by GATE H (2.5) with render rule name-action-not-verification only. D10 thresholds lower-band 0.4, upper-band 0.6, status adapter-side tuning targets not engine law: RATIFIED, with measure 7 instrumentation. GATE H and GATE S1: RATIFIED as hard build gates; the monolith refuses to apply or reverses on their failure. BUILD STYLE: monolithic script per 5.5, RATIFIED.

## 8. Registry / NACE posture and deferrals

**Ratified note, verbatim:** "Corner-Gate v3 v1 does not update NACE directly. It produces bounded coupling-context evidence. Future NACE/Capability Registry integration may consume this evidence by resolving command signatures to capability ids and learning efficacy from coupling trajectory, not merely success/failure."

Future derived event shape, DEFERRED, recorded for the registry sprint:
```
(capability-coupling-evidence $cycle $capability-id $command-sig $ctx-phase
                              $dominant-surface $chain-state $polarity-verdict
                              $support $residual-gap $next-move $lineage)
```
Future NACE learning targets the coupling patterns, not pass/fail: repetition without metabolization; no state delta; improvement only after feedback visibility; behavior change after next-move shifts; hidden-error surfaces; output without contact improvement; stuck signatures. D9's dual meaning recorded: immediate legibility for Clarity now; completion-claims-without-verification reduce future efficacy confidence for that capability/context unless harness evidence exists.

Also deferred: engine growth-canon wiring (its own thread); task-phase intention promotion (v1.1, Clarity-gated); ChromaDB durability (registry sprint); task_selector disposition (dormant, manifest 59, zero consumers); threshold tuning (measure 7 data first).

---

The soul-absent question, answered: this design produces technically-correct output that is soul-absent if the rendered line ever functions as instruction rather than information, or if fabricated classifier inputs make the engine certify contact that never happened. The first is watched by measure 4 with Clarity's two flagged terms as early-warning markers; the second is structurally excluded by the unfed-classifier rule and enforced standing by NC4.

Document end. v0.6, Step 0 closed, risk gates ratified, monolithic build unblocked.
