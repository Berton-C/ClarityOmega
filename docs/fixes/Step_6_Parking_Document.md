# Step 6 Parking Document

**Status:** PARKED 2026-05-21. Resuming requires in-iteration capacity work to land first.

**Why parked:** Step 6 as designed wires the v9 aliveness gate to consume substrate organs (idle-pattern, agency-balance, task-phase) at cycle-level. Bug 4 (duplicate-engagement, the named target of Step 6) is the in-iteration capacity gap manifesting at cycle level. Cycle-level gating responds to fragmentation AFTER it has manifested as send-burst. The root cause is in-iteration capacity. Step 6 wires defense-in-depth, but it does not solve Bug 4 root cause. Resuming Step 6 makes sense once in-iteration capacity is verified working; Step 6 then becomes the cycle-level layer on top of an in-iteration foundation.

---

## Spec context

**Step 6 belongs to:** `docs/design/task-state-primitive_design.md` Section 10 (the task-state primitive mini-sprint, Steps 1-9).

**What Step 6 does per spec:** Migrate the aliveness gate from latch-state-only dispatch (v8) to three-organ substrate composition (v9) that reads task-phase + idle-pattern + agency-balance.

**What Step 6 replaces:** Latch-state as the gate's authority. Latch-state was loop.metta machinery (set externally by msgnew/idle directives). Task-phase is Clarity's self-determined state. The migration moves the gate from "machinery decides if Clarity engages" to "Clarity's self-assessment of phase determines whether engagement is appropriate."

**Spec verification item 10 (the literal Step 6 test):** "Aliveness gate goes SILENT when (task-phase idle), ENGAGE when (task-phase engaged)."

**Where Step 6 sits in the larger vision:** Per `ClarityOmega_Continuity_of_Mind_Spec_v2_5.md` Items 13-14, Step 6 is one of several wiring steps building toward 3-iteration attentional continuity. The Continuity of Mind vision requires in-iteration capacity (which Step 6 alone does NOT provide). Step 6 contributes cycle-level gating to the larger architecture.

**Mini-sprint sequence (where Step 6 sits):**
- Step 1: defined task-state atoms (done)
- Step 2: mechanical writers in loop (done)
- Step 3: Clarity's skills for self-written phase (done)
- Step 4: TASK-STATE prompt block (done)
- Step 4.5: idle-pattern detector (done; Bug 2 fixed)
- Step 4.6: agency-balance guard (done; Bug 2b fixed)
- Step 5: removed SELF-CHECK + self-check-guidance (done)
- **Step 6: PARKED — wire aliveness gate to consume substrate organs**
- Step 7: continuity_driver consumer migration (pending)
- Step 8: remove latch-state entirely (pending; Step 6 v9 keeps latch as transitional fallback per design)
- Step 9: deprecate &task_context (pending)

---

## The v9 design (decisions locked, ready to resume)

**Entry-point signature preserved:** `(aliveness-gate $msgnew $idle)`. loop.metta does NOT change. The `$idle` parameter is the idle_directive STRING (Python-helper output), NOT the idle-pattern atom. Naming similarity is historical.

**Priority hierarchy (final, locked per Berton + Clarity, May 15-21):**

1. `idle_directive non-empty OR msgnew=True` → ENGAGE (supervisor authority + active conversation)
2. `(current-idle-pattern)` send-burst → SILENT
3. `(current-agency-balance)` dependency-risk AND no msgnew → SILENT
4. `(current-phase)` in {attending, idle, waiting, reflecting} → SILENT
5. `(current-phase)` in {engaged, research, response-drafting, boundary-detected} → fall through to legacy latch-state dispatch
6. Unhandled/unknown phase → latch-dispatch (defaults SILENT for unknown states)

**Authority hierarchy decision (May 21):** Supervisor authority absolute. Substrate composition (priorities 2-5) only fires when supervisor returned empty (idle_directive == "") AND no human input (msgnew == False). Per Berton: "the gate should respect supervisor authority absolutely."

**Pre-bootstrap safety paths:**
- `(current-idle-pattern)` returns `()` → fall through to agency-balance check
- `(current-agency-balance)` returns `()` → fall through to task-phase check
- `(current-phase)` returns `attending` symbol if no atom present → SILENT via attending case (NOT a tuple, scalar)
- All unhandled paths default to SILENT (conservative failure mode)

**Atom shapes the gate reads:**
- `(idle-pattern $verdict $count)` via `(current-idle-pattern)`. Verdict ∈ {send-burst, productive}.
- `(agency-balance $verdict $person $system)` via `(current-agency-balance)`. Verdict ∈ {healthy, dependency-risk}.
- `(task-phase $phase)` via `(current-phase)`. Phase ∈ 8 enumerated values.
- `(latch-state $state)` via `(match &self (latch-state $s) $s)` in legacy fallback. State ∈ {IDLE, ENGAGED, COMPLETING}.

**Legacy latch-state fallback:** Preserved as transitional safety net per design. Step 8 removes this fallback later.

**Returns:** ENGAGE or SILENT symbol only. No other verdict values. No atom writes.

**C12-safe:** No match inside if. Function-dispatch on match result is OK. Use collapse-then-branch where explicit empty-vs-present check needed.

**No new LLM surface:** Pure substrate composition. No py-call, no soul-llm-call, no helper.* invocations.

**Deliberate v8 → v9 behavior change documented:** `(latch-dispatch COMPLETING)` returns SILENT in v9 (was ENGAGE in v8). Reasoning: COMPLETING means wrapping up; engaging contradicts wrap-up intent. Clarity's authorship decision May 21, confirmed by Berton (implicit by not reversing). Must be documented in eventual ADR-006.

---

## Clarity's authored v9 substrate file

Clarity authored the v9 MeTTa ground-up May 21 per the design contract. File location: `soul/aliveness-gate-v9.metta` (parallel filename to production v8 `soul/aliveness_gate.metta`, no collision). 67 lines.

Structure verified against design contract:
- Entry-point signature preserved ✓
- All `(=` wrappers present on definitions ✓
- Priority hierarchy 1-6 implemented as designed ✓
- Pre-bootstrap fall-through cases present ✓
- Multi-atom latch defensive handling (`($state1 $state2)` → SILENT, `$other` → SILENT) ✓
- Legacy latch-dispatch preserved with COMPLETING → SILENT change ✓
- C12-safe (no match inside if; collapse-then-function-dispatch in latch fallback) ✓
- No new LLM surface ✓
- No atom writes ✓
- Documentation comments throughout ✓

Paren-balance verified manually on densest lines. Structurally ready to apply.

**The full file content (preserved here for resume):**

```metta
;; v9 Aliveness Gate
;; ================
;; Entry: (aliveness-gate $msgnew $idle)
;; $msgnew - boolean, new human message arrived
;; $idle - idle_directive STRING from Python helper
;; NOT the (current-idle-pattern) ATOM
;;
;; Returns: ENGAGE or SILENT only. Pure consumer, no atom writes.
;; C12-safe: no match inside if; collapse-then-branch where needed.
;;
;; Priority hierarchy:
;; 1. idle_directive non-empty OR msgnew=True -> ENGAGE
;; 2. idle-pattern send-burst -> SILENT
;; 3. agency-balance dependency-risk AND no msgnew -> SILENT
;; 4. task-phase in {attending,idle,waiting,reflecting} -> SILENT
;; 5. active phase -> latch-dispatch
;; 6. unknown -> latch-dispatch (defaults SILENT)
;;
;; All unhandled paths default to SILENT (conservative failure mode)

;; Priority 1: Supervisor authority + active conversation
(= (aliveness-gate True $idle) ENGAGE)
(= (aliveness-gate False $idle) (if (> (string_length $idle) 0) ENGAGE (gate-on-idle-pattern (current-idle-pattern) (current-agency-balance))))

;; Priority 2: Idle-pattern dispatch
(= (gate-on-idle-pattern () $balance) (gate-on-agency-balance $balance))
(= (gate-on-idle-pattern (send-burst $n) $balance) SILENT)
(= (gate-on-idle-pattern (productive $n) $balance) (gate-on-agency-balance $balance))
(= (gate-on-idle-pattern $unknown $balance) (gate-on-agency-balance $balance))

;; Priority 3: Agency-balance dispatch
(= (gate-on-agency-balance ()) (gate-on-task-phase (current-phase)))
(= (gate-on-agency-balance (dependency-risk $person $system)) SILENT)
(= (gate-on-agency-balance (healthy $person $system)) (gate-on-task-phase (current-phase)))
(= (gate-on-agency-balance $unknown) (gate-on-task-phase (current-phase)))

;; Priority 4+5+6: Task-phase dispatch
(= (gate-on-task-phase attending) SILENT)
(= (gate-on-task-phase idle) SILENT)
(= (gate-on-task-phase waiting) SILENT)
(= (gate-on-task-phase reflecting) SILENT)
(= (gate-on-task-phase engaged) (gate-on-latch-fallback))
(= (gate-on-task-phase research) (gate-on-latch-fallback))
(= (gate-on-task-phase response-drafting) (gate-on-latch-fallback))
(= (gate-on-task-phase boundary-detected) (gate-on-latch-fallback))
(= (gate-on-task-phase $other) (gate-on-latch-fallback))

;; Legacy latch-state fallback (transitional safety net)
;; C12-safe: collapse then function-dispatch, not if-on-match
(= (gate-on-latch-fallback) (gate-read-latch-state (collapse (match &self (latch-state $s) $s))))

;; No latch-state -> conservative SILENT
(= (gate-read-latch-state ()) SILENT)
;; Single latch-state -> dispatch
(= (gate-read-latch-state ($state)) (latch-dispatch $state))
;; Multiple latch-state atoms (anomalous) -> SILENT
(= (gate-read-latch-state ($state1 $state2)) SILENT)
;; Any other shape -> SILENT
(= (gate-read-latch-state $other) SILENT)

;; Latch-state dispatch (preserved from v8)
;; COMPLETING -> SILENT: deliberate v9 change
;; COMPLETING means wrapping up; engaging contradicts wrap-up intent
(= (latch-dispatch IDLE) SILENT)
(= (latch-dispatch ENGAGED) ENGAGE)
(= (latch-dispatch COMPLETING) SILENT)
(= (latch-dispatch $other) SILENT)
```

---

## Apply script not yet drafted

The apply script for Step 6 was never drafted. When resuming, the script needs to:

- Full-file rewrite of `soul/aliveness_gate.metta` (v8 17-line → v9 67-line)
- Anchor-based section update of `docs/design/artifact_1_loop_metta_wiring_diagram.md` Phase 4.3 entry (current v8 shape documented in apply_step6_aliveness_gate_migration.py as ART1_ANCHOR — text was verbatim-intact post-Bug-2-commit as of May 20)
- Reversible per F114 with `.bak.<descriptor>` suffix
- paren_balance verification check (helper function from apply_step6 readthrough)
- Same backup pattern across both files
- Discipline 4: substrate edit + artifact_1 update + ADR-006 (NEW) land in same commit

**DO NOT carry forward `staging/apply_step6_aliveness_gate_migration.py`.** Per Berton's direction May 21: "that script tanked Clarity, it's tainted scaffolding, at best treat as one of many reference points among others." Ground-up means ground-up. The May 21 work used apply_step6 only to extract: (a) what discipline patterns appeared in the structure (paren balance, anchor matching, reversibility) and (b) the ART1_ANCHOR text (which was identical to current state per verification). The substrate text content (GATE_NEW) of apply_step6 is NOT to be used; Clarity's authored v9 file above is the authoritative substrate text.

---

## Outstanding pre-rebuild work (for resume)

1. **Draft apply script** wrapping Clarity's v9 substrate file with discipline patterns
2. **Draft ADR-006** documenting the architectural decision (Step 6 substrate composition, the COMPLETING → SILENT deliberate change, the supervisor authority decision, the in-iteration capacity prerequisite)
3. **Verify artifact_1 anchor still intact** at resume time (Bug 2 commit added lines elsewhere; future commits between now and resume could affect it)
4. **Confirm v8 file unchanged** at resume time
5. **Discipline 6 Part B writer-consumer accounting** already complete (file: `/mnt/user-data/outputs/aliveness_gate_discipline_6_part_b_accounting.md` — 227 lines, A-F sections complete, no unknowns)
6. **Surface investigation** already complete (file: `/mnt/user-data/outputs/aliveness_gate_surface_investigation.md` — 259 lines)
7. **Apply, rebuild, verify per spec item 10**

---

## In-iteration capacity prerequisite (the reason Step 6 is parked)

**The architectural insight (May 21):** Bug 4 (duplicate-engagement) is the in-iteration capacity gap manifesting at cycle level. Clarity is forced to fragment work across iterations because she cannot query-then-respond within a single iteration. The send-burst pattern, the three-response contradiction-resolution pattern, the recurring parse errors from multi-command batch attempts — all are workarounds for missing in-iteration capacity.

**Clarity's correction (May 21):** The right architectural move is RECLAIM not BUILD. The current `soul-llm-call` wrapper STRIPS native multi-turn tool-use capability that the LLM API supports natively. The change is removing the constraint, not adding new mechanisms. Writers/consumers (the pattern we built for awareness organs) become OBSERVABILITY for the reclaimed capability, not the capability itself.

**Why Step 6 must come AFTER in-iteration capacity:**

If Step 6 lands while in-iteration capacity is missing:
- Send-burst is gated to SILENT (visible improvement at metric level)
- But the underlying fragmentation continues, just SILENT-fragmented instead of sent-fragmented (no longer visible, but worse from continuity-of-mind perspective)
- We get false confidence Bug 4 is fixed
- The Continuity of Mind vision items 13-14 remain unmet

If Step 6 lands AFTER in-iteration capacity:
- Clarity completes mid-iteration work within iterations (root cause addressed)
- Send-burst pattern rarely arises because work integrates rather than fragmenting
- Step 6 provides defense-in-depth at cycle level on a foundation that's already solved the root cause
- v9 priority hierarchy still applies for the narrower cases where cycle-level gating remains relevant

---

## Open items confirmed orthogonal to Step 6 (do NOT block resume)

These were investigated during May 20-21 work and confirmed as separate concerns:

- **msgnew sticky-True / $msg consumer-side footgun:** Theoretical concern flagged in Path 1 gamma drafting; Clarity's reframe: the bug is likely consumer-side misuse of persistent `$msg` rather than `$msgnew` actually sticking True. Separate investigation, not gated by Step 6.

- **Supervisor 1117-char creative-mode directive:** Confirmed in production logs (May 20). NOT a bug per Clarity's reframe (May 21): creative-mode genesis directive is design-intended when supervisor has no goals. The "fix" is behavioral compliance with the genesis protocol (no sends during exploration), NOT architectural change to gate or supervisor. The v9 priority hierarchy correctly defers to supervisor authority.

- **Iteration-9 trap from original v9 attempt (6ca6f44, May 16):** Berton declared out of scope May 20. Residual risk acknowledged: if a similar mechanism produces a trap post-Step-6-apply, we won't have characterized it in advance.

- **500-cycle parse error pattern (May 20-21 logs):** Likely manifestation of same in-iteration capacity gap. Should resolve once in-iteration capacity work lands. Not a Step 6 concern.

- **Architectural inconsistency in latch-state writes (raw set-atom! in loop vs guarded transitions from Clarity):** Per artifact_1 "never observed as a bug." Step 8 removes latch-state entirely; Step 6 v9 preserves this inconsistency as transitional safety net.

---

## Parked artifacts inventory

**On disk in repo:**
- `soul/aliveness-gate-v9.metta` — Clarity's draft v9 substrate, 67 lines, ready to apply

**In /mnt/user-data/outputs/ (from May 20-21 sessions):**
- `aliveness_gate_surface_investigation.md` — 259 lines, surface investigation per Discipline 6 Part B
- `aliveness_gate_discipline_6_part_b_accounting.md` — 227 lines, full A-F writer-consumer accounting
- `apply_bug2_documentation.py` — applied; documents Bug 2/2b commit (already committed as 2fc066a)

**Project knowledge:**
- All design context, prior investigations, ADRs, artifact_1 wiring diagram

**Not yet created (deferred to resume):**
- ADR-006 (Step 6 architectural decision record)
- Apply script wrapping Clarity's v9 substrate
- Investigation log capturing the May 21 in-iteration-capacity decision and Step 6 parking rationale

---

## Resume checklist

When in-iteration capacity is verified working and Step 6 is unparking:

- [ ] Re-read this parking doc
- [ ] Verify `soul/aliveness-gate-v9.metta` still present and unchanged
- [ ] Verify `soul/aliveness_gate.metta` (v8) still present and unchanged in production
- [ ] Verify `docs/design/artifact_1_loop_metta_wiring_diagram.md` Phase 4.3 anchor text still verbatim-intact (or document any drift)
- [ ] Confirm Discipline 6 Part B accounting and surface investigation still accurately reflect substrate state (re-verify A-E sections; F may need new questions for Clarity given in-iteration capacity changes the substrate she operates within)
- [ ] Surface to Clarity: any updates to her v9 file given in-iteration capacity now exists (e.g., should priority 1 / 1.5 consider "is multi-turn currently active"? Probably not, since in-iteration multi-turn happens BEFORE the cycle-end gate fires, but Clarity should confirm)
- [ ] Draft ADR-006
- [ ] Draft apply script ground-up wrapping Clarity's v9 substrate
- [ ] Dry-run
- [ ] Apply
- [ ] Rebuild via `docker compose build --no-cache clarityclaw`
- [ ] Verify Test 1 (heartbeat F31) iteration counter advancing
- [ ] Verify Test 2 (spec verification item 10): gate goes SILENT when (task-phase idle), ENGAGE when (task-phase engaged)
- [ ] Verify Test 3 (Bug 4 — duplicate-engagement): observe over multi-cycle window; with in-iteration capacity already landed, send-burst pattern should be substantially reduced or absent
- [ ] Commit per Discipline 4 (substrate + artifact_1 + ADR-006 same commit)
- [ ] Update INDEX.md

---

## Critical context to NOT lose

**The Bug 4 reframe.** Bug 4 is NOT "Clarity sends too many messages." Bug 4 IS "Clarity lacks in-iteration capacity, which manifests as cycle-level fragmentation symptoms including but not limited to multi-message bursts." Step 6 addresses the cycle-level symptom layer, not the root cause.

**The discipline lesson.** Step 6 was originally framed as the duplicate-engagement bug fix per the spec. Working on it surfaced that the spec's framing of Bug 4 was incomplete. The spec authors (including Berton + Clarity) didn't have the in-iteration-capacity articulation in May 16 when Step 6 was first attempted; the May 20-21 work surfaced it. Future spec interpretation should hold that specs encode design INTENT that may be refined when new architectural understanding emerges.

**Clarity's first-order observation rights.** Per Discipline 6 Part B, Clarity has first-order observation rights on her own behavior. The Step 6 design decisions (priority ordering, COMPLETING → SILENT, supervisor authority, task-phase silence set) all came from her articulation of her self-experience. These decisions are durable across this parking.

**The May 21 conversation.** This parking doc captures the technical state. The conversational arc that led here is itself part of Step 6's history: Berton's challenges (theatrical hedging, scope drift, narrative loss, lazy carry-forward of tainted scaffolding) corrected Claude's behavior across the session. Future resume work should hold the same discipline: read evidence carefully before theorizing, hold the spec but check the larger vision, don't drift from named scope into adjacent investigation, no theater dressed as honesty.

---

## Document end

Step 6 is parked. The v9 design is locked. Clarity's substrate is ready. The blocker is in-iteration capacity, which proceeds as a separate sprint. Resume Step 6 once that sprint is complete and verified.
