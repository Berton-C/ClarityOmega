# Inverse Audit: Runtime Capability Beyond the Master Doc

**Status:** Read-only analysis. The inverse of the compliance pass. The compliance pass asked "for each doc function, is the runtime compliant." This asks the opposite: "for each live-runtime element, does the master doc account for it, and if not, must it be preserved?"
**Why:** Restoration restores toward the doc. If the runtime gained capability after the doc was written, blind restoration could delete it. This audit inventories every divergence where the runtime does MORE than or DIFFERENT from the doc, so no restoration step silently removes a real capability (reverse-regression).
**Classification:** PRESERVE (sanctioned progression, restoration must not touch it) or DECIDE (Berton determines keep-or-drop). Walked loop.metta lines 1-171 top to bottom.

---

## PRESERVE: runtime capability the doc does not describe, that is clearly progression

These are post-doc additions that are coherent, wired, and serving a purpose. Restoration must not remove or break them. Several are whole subsystems from later sprints.

### P-1. Task-state primitive (lines 36, 42, 75, 102, 114)
`do-bootstrap-task-state!`, `task-state-block`, `do-set-last-activity!`, `do-set-cycles-since-input!`, `current-cycles-since-input`. A whole scalar task-state subsystem (cycles-since-input, last-activity, task-phase) not in the master doc. This is the Sprint 4 task-state primitive. PRESERVE entirely.

### P-2. Idle-pattern + agency-balance awareness organs (lines 43, 44, 137, 138)
`idle-pattern-block`, `agency-balance-block`, `do-update-idle-pattern!`, `do-update-agency-balance!`. Two awareness subsystems writing idle-pattern and agency-balance atoms. Not in the doc. PRESERVE.

### P-3. Recent-action populator + the full DIAG block (lines 41, 136, 139-147, 162)
`your-last-action-block`, `populate-recent-action`, and DIAG-CYCLE-START through DIAG-CYCLE-END (nine diagnostic prints), plus RECENT-ACTION-ATOMS. A recent-action tracking subsystem with extensive diagnostics. Not in the doc. PRESERVE (the diagnostics are how behavior is observed; removing them blinds the loop).

### P-4. corner_gap Layer 5 (the apply-corner-gate line, prior session)
`apply-corner-gate` and the gate-aware results swap. Confirmed wired and loaded in a prior session. Not in the doc (post-doc). PRESERVE. (Already flagged; restated here for completeness.)

### P-5. soul-llm-call dispatcher (lines 79, 85, 150)
Provider-routing abstraction the doc predates (doc uses useGPT directly). Berton confirmed: sanctioned progression. PRESERVE everywhere.

### P-6. Idle-directive / genesis subsystem (lines 96-100, 105)
`$atomspace_goals/_gaps/_fuel` collapse-matches, `soul_idle_goal_prompt_v2`, the wakeupInterval-gated idle directive, latch ENGAGED/IDLE transitions on directive presence. A substantial idle/genesis subsystem. Not in the doc's input sequence. PRESERVE (this is the autonomous-cycle behavior; it is load-bearing for idle operation).

### P-7. aliveness-gate (line 106) and the SILENT path (lines 108, 113, 115)
The aliveness gate and the SILENT-cycle suppression (no send, no LLM call on SILENT). The doc's Section 8 four-channels does not include this mechanical idle-suppression gate. PRESERVE (it is the token-economy / idle-silence mechanism; it is mechanical per P5, correctly so).

### P-8. soul_verdict_sanitize (line 87) and soul_service_learning (line 93)
`helper.soul_verdict_sanitize` (cleans the verdict string post-LLM) and `helper.soul_service_learning`. Not in the doc. Sanitize is plumbing (hands); service-learning is a calibration-adjacent helper. PRESERVE as plumbing, but see D-3 (service-learning may warrant a faculty look later, not now).

### P-9. soul_user_context_save + extract_username (line 94)
`helper.soul_user_context_save` and `extract_username`. Per-user context persistence. Not in the doc. PRESERVE (user-context memory, additive capability).

### P-10. Upstream history-on-autonomous-output (line 161)
The `(or $msgnew (not (== $sexpr ())))` history record, explicitly annotated as an upstream patham9/mettaclaw merge (autonomous reasoning recorded as world knowledge). PRESERVE (upstream alignment, and it is the writeback the Extension E work later refines, not removes).

---

## DECIDE: divergences where Berton must choose

These are not clearly progression. Each is a place the runtime differs from the doc in a way that could be intentional or could be drift, and restoration's treatment depends on Berton's call.

### D-1. The enriched-prompt / getSoulBrief path (lines 103-104)
`$soul_brief (swrite (getSoulBrief))` then `$enriched_prompt (string_concat $soul_brief $prompt)`, and `soul_send_assemble` receives `$enriched_prompt`. The doc's send assembly does not describe a separate `getSoulBrief` + enriched-prompt concat. This may be the runtime's way of prepending the soul brief to the agent prompt (a real function) or a drifted duplicate of the brief that the verdict already uses. DECIDE: is `getSoulBrief` + enriched-prompt a kept mechanism, or does it fold into the restored `soul-brief-symbolic` path? Interacts with the input-brief decision (reinstate soul-brief-symbolic). Worth a focused look before Repair-on-input-brief.

### D-2. soul_send_assemble itself (lines 108-112)
The doc (Section 14 $send assembly) and the survey both noted send-assembly strips the verdict to a token and excludes the soul brief. This is the surface-3 concern (Extension B, soul-authored voice). It is NOT restoration scope (the doc's PROCEED path is LLM-composed too). DECIDE only insofar as: restoration leaves it as-is, Extension B changes it later. Flagged so it is not mistaken for a restoration target. No restoration action.

### D-3. soul_service_learning (line 93) faculty
Listed PRESERVE as plumbing (P-8), but if it makes a judgment (what to learn from the verdict) rather than just recording, it is an ADR-008 reclamation candidate for Extension H, not restoration. DECIDE later (Extension H scope), not now. No restoration action.

### D-4. The engaged_idle_count inline logic (line 101)
The nested-if counter (reset on msgnew or idle-directive, else increment). This is the inline cruft artifact_0 Discipline 1 flags (logic in the loop that should be a hook). Not a doc divergence per se, but a known elevation-flag. DECIDE: leave as-is during restoration (it works), elevate to a hook during a later cleanup. No restoration action; noted so it is not "fixed" mid-restoration and mistaken for a repair.

---

## The reverse-regression guard, applied to the five (six) repairs

For each restoration repair, does it risk deleting any PRESERVE item above?

- **Repair 1 (output intercept):** touches lines 126-133. PRESERVE items nearby: corner_gap (P-4, line 134, below the edit) and the mutation flag (now restored to native). The corrected Repair 1 must leave line 134 untouched (the regenerated script already does). No PRESERVE item deleted. SAFE once corrected.
- **Repair 2 (Channel D note):** touches helper soul_voice_prompt only. No PRESERVE item nearby. SAFE.
- **Repair 3 (PAUSE router):** re-enables soul-pause?, touches the line 148 gate. The PAUSE branch (150-157) is preserved as-is (it already composes Channel D + halts). No PRESERVE item deleted. SAFE (gated).
- **Repair 4 (Mode 2):** wires the existing soul_utils Mode 2 functions. Must not disturb P-1 (task-state primitive) which is a DIFFERENT subsystem (scalar task-state vs Mode 2 agentic). DECIDE-adjacent: confirm Mode 2 wiring and the task-state primitive (P-1) coexist without collision, since both touch task/cycle concepts. FLAG for care.
- **Repair 5 (D-lite + soul_ack_sent):** adds state var + wires composer at input FLAG-distress. No PRESERVE item deleted. SAFE.
- **Input-brief reinstatement (soul-brief-symbolic):** touches line 83, and interacts with D-1 (getSoulBrief/enriched-prompt). MUST resolve D-1 first, because reinstating soul-brief-symbolic at line 83 while getSoulBrief still runs at 103 could create two brief paths. FLAG: resolve D-1 before the input-brief change.

---

## Headline for Berton

The runtime has substantial capability the master doc does not describe: the entire task-state primitive, two awareness organs (idle-pattern, agency-balance), the recent-action + diagnostics subsystem, corner_gap, the idle/genesis subsystem, the aliveness SILENT path, user-context persistence, and the soul-llm-call dispatcher. **All of it is PRESERVE.** These are real post-doc gains, and blind restoration toward the doc would have endangered them. This audit is the keep-list.

Two of the six repair targets now carry a FLAG for collision risk with preserved capability: Repair 4 (Mode 2 vs the task-state primitive P-1) and the input-brief reinstatement (vs the getSoulBrief/enriched-prompt path D-1). Neither is a blocker; both are "resolve this adjacency before editing."

Four DECIDE items, none requiring action during restoration: D-1 (getSoulBrief path, resolve before input-brief change), D-2 (send assembly, Extension B not restoration), D-3 (service-learning faculty, Extension H not restoration), D-4 (engaged_idle_count inline, later cleanup not restoration).

**Confidence after this audit:** the reverse-regression risk is now inventoried, not luck-dependent. The PRESERVE list is the explicit guard. With Repair 4 and input-brief flagged for adjacency resolution, the restoration can proceed without silently deleting post-doc capability.
