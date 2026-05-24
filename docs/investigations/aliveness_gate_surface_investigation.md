# Surface Investigation: Aliveness Gate (v9 re-integration)

**Per:** `docs/design/artifact_0_loop_extension_contract.md` Section 3.5 (Surface Investigation Template), Discipline 6 Part B
**Investigation date:** 2026-05-20
**Sprint / step this investigation supports:** v9 aliveness gate re-integration (post-Bug 2/2b fix)
**Investigators:** Berton (project lead), Clarity (substrate co-designer), Claude (investigation assistant)
**Scope:** What is in front of us now. Current substrate state, current spec, gap between them. No historical excavation of the rolled-back v9.

---

## Surface name

**Aliveness gate** (the function `(aliveness-gate $msgnew $idle)` in `soul/aliveness_gate.metta`)

Currently at v8 (12 lines, binary latch-state dispatch). Called from `src/loop.metta` line 100 (per artifact_1) as `(aliveness-gate $msgnew $idle_directive)`. Returns ENGAGE or SILENT. The verdict drives whether the LLM call fires that cycle (loop.metta DANGER ZONE lines 102, 107, 108).

---

## A. Writers (atoms going INTO the surface the gate reads)

The v9 spec design reads six things: `$msgnew`, `$idle` (the idle_directive string), `(current-idle-pattern)`, `(current-agency-balance)`, `(current-phase)`, and `(latch-state)` via fallback. Each has writers, configuration, and behavior worth surveying.

### A.1 — `$msgnew` (boolean, passed to gate at call site)

- **Producer:** `loop.metta` let* chain. Computed as `(prog1 (and (> (string_length $msgrcv) 0) (!= $msgrcv (get-state &prevmsg))))` per `loop_copy_metta.txt`.
- **Trigger:** Non-empty receive buffer AND different from `&prevmsg`. True only on actual new human messages.
- **Bug risk identified:** Earlier investigation (apply_idle_directive_once_per_window_path1_gamma.py drafting context) noted "msgnew flag appears to stick True across iterations, causing the same human message to be processed repeatedly." Status unclear — not in this turn's verified data. **Open question, not blocking but worth verifying in observation.**
- **Atom-shape (when read by gate):** Just a boolean. Not an AtomSpace atom.

### A.2 — `$idle_directive` (string, passed to gate as `$idle`)

- **Producer:** `loop.metta` line 92 area: `(if (and (not $msgnew) (> (get_time) (+ (get-state &last_human_time) (wakeupInterval)))) (py-call (helper.soul_idle_goal_prompt_v2 ...)) "")`.
- **Configuration constants this writer reads:** `wakeupInterval` (current value: 600 per loop_copy_metta.txt initLoop), `&last_human_time` (set on `$msgnew` per artifact_1 Line 68).
- **Trigger:** `(not $msgnew) AND (get_time > &last_human_time + 600)`. Single conjunct on the time check. No `&last_idle_fire_time` guard (Path 1 gamma drafted but NOT applied per current loop_copy_metta.txt).
- **Atom-shape (when read by gate):** String. Empty `""` when guard False; non-empty supervisor-generated directive when True.
- **Known behavior pattern:** The 6ca6f44 commit message says "supervisor returns a 953-char directive even when selected_goal=None, so step-1 ENGAGE wins every cycle before substrate composition can fire." So the helper produces non-empty output even when there's no real goal. This is the "supervisor-side bug" referenced in the rollback rationale.
- **Behavior with maxWakeLoops=1 (current):** wake-burst is one cycle, not 50. So even if the supervisor returns non-empty every wake, that's only one cycle's worth of forced-ENGAGE per wakeupInterval window (10 minutes) — assuming nothing else triggers another wake. Important distinction from the rolled-back design assumption.

### A.3 — `(current-idle-pattern)` atom

- **Returns:** `($verdict $count)` tuple (e.g., `(productive 0)`, `(send-burst 5)`), or `()` if no atom in AtomSpace yet.
- **Definition:** `soul/idle_cycle_detector.metta` Section 3 (pure read helper): `(let $atoms (collapse (match &self (idle-pattern $v $c) ($v $c))) (if (== $atoms ()) () (car-atom $atoms)))`
- **Atom shape in AtomSpace:** `(idle-pattern $verdict $count)`. Verdict values: `send-burst`, `productive`. Threshold for verdict: `count > 3` per `do-update-idle-pattern!` in writers file.
- **Writer:** `do-update-idle-pattern!` in `soul/idle_cycle_detector_writers.metta`, called from loop.metta cycle tail (per artifact_1 wiring diagram).
- **Bug 2 status:** FIXED + VERIFIED + COMMITTED (commit 2fc066a). Pre-fix: car-atom returned cycle-1 bootstrap; post-fix: returns live current verdict.
- **Verified behavior post-fix:** Cycles 1-9 hold count=1, atom transitions productive→send-burst correctly as send activity accumulates. End-to-end verified in cycles 34-35 (heterogeneous transition).
- **Pre-bootstrap behavior:** Returns `()`. The v9 gate handles this via `(gate-on-idle-pattern ())` fall-through case.

### A.4 — `(current-agency-balance)` atom

- **Returns:** `($verdict $person $system)` tuple (e.g., `(healthy 2 1)`, `(dependency-risk 0 5)`), or `()` if no atom in AtomSpace.
- **Definition:** `soul/agency_balance_guard.metta` Section 3 (pure read helper). Same shape pattern as current-idle-pattern.
- **Atom shape in AtomSpace:** `(agency-balance $verdict $person $system)`. Verdict values: `healthy`, `dependency-risk`. Threshold: 0.6 ratio (hardcoded in `dependency-detected` per F42 per agency_balance_guard_copy_metta.txt).
- **Writer:** `do-update-agency-balance!` in `soul/agency_balance_guard_writers.metta`, called from loop.metta cycle tail after `do-update-idle-pattern!` (per artifact_1).
- **Bug 2b status:** FIXED + VERIFIED + COMMITTED (commit 2fc066a). Same structural mechanism as Bug 2.
- **Pre-bootstrap behavior:** Returns `()`. The v9 gate handles this via `(gate-on-agency-balance ())` fall-through case.
- **Person-class tags counted:** `responsive-send`, `verification-query`.
- **System-class tags counted:** `status-send-unprompted`, `exploration-query`, `pin-only`, `unclassified`.
- **Note (unclassified):** `unclassified` is assigned to system-class per agency_balance_guard_copy_metta.txt design comment. Conservative direction: under-detects dependency rather than over-detects.

### A.5 — `(current-phase)` atom

- **Returns:** `$phase` symbol (one of `attending`, `engaged`, `research`, `response-drafting`, `idle`, `waiting`, `reflecting`, `boundary-detected`). Defaults to `attending` if no atom present.
- **Definition:** `soul/task_state.metta` Section 3 (per task_state_copy_metta.txt): `(let $result (collapse (match &self (task-phase $p) $p)) (if (== $result ()) attending (car-atom $result)))`
- **Atom shape in AtomSpace:** `(task-phase $phase)` (scalar, exactly one atom at a time).
- **Writers (from task_state_writers_copy_metta.txt):**
  - `do-bootstrap-task-state!` — idempotent guard on startup. If `(task-phase $p)` absent, adds `(task-phase attending)`. Called from loop.metta initLoop end.
  - `do-set-phase! $new-phase` — uses **`set-atom!`** primitive (NOT car-atom + remove-atom). Reads `current-phase`. If same: no-op. Else: `set-atom!` replace + add transition record. Called from Clarity's skills.
  - `do-set-phase-with-anchor! $new-phase $value $reason` — same as do-set-phase! plus conditional anchor record.
- **Writer mechanism reliability:** Uses `set-atom!` primitive. **Different mechanism than Bug 2 / 2b.** Per task-state-primitive_design.md Section 6: "set-atom! is the primary primitive ... used by latch-state already, proven pattern." No known pathology in this writer family at this time.
- **Note on `set-atom!` behavior under bootstrap-failure:** If `do-bootstrap-task-state!` didn't run, the from-pattern in `set-atom!` would not match. Per artifact_1 latch flow notes, `set-atom!` then "would still fire from set-atom! perspective but the from-pattern wouldn't match anything to remove, so the result might be two atoms or just an added atom." Discussed for latch transitions; same risk theoretical for task-phase. Not observed in production per artifact_1.
- **Pre-bootstrap behavior of `(current-phase)`:** Returns `attending` (the default symbol) — not `()`. **This matters for v9 gate dispatch:** the gate's `(gate-on-task-phase attending)` case fires with SILENT, so pre-bootstrap defaults to SILENT via the attending case rather than via a fall-through.

### A.6 — `(latch-state)` atom (via legacy fallback in v9 gate)

- **Returns:** `IDLE`, `ENGAGED`, or `COMPLETING` symbol via `(match &self (latch-state $s) $s)`.
- **Atom shape:** `(latch-state $state)` — single-arg predicate atom.
- **Definition file:** `soul/latch/aliveness_state_machine.metta` (the `latch/` subdirectory version is ACTIVE per artifact_1; two other versions dormant).
- **Initial state:** `(latch-state IDLE)` added at file import time.
- **Writers from loop.metta (raw set-atom!):**
  - Line 88 (per artifact_1): `(set-atom! &self (latch-state IDLE) (latch-state ENGAGED))` when `$msgnew` is True.
  - Line 93 (per artifact_1): `(set-atom! &self (latch-state ENGAGED) (latch-state IDLE))` when `$idle_directive` is non-empty.
- **Writers from Clarity's substrate skills (guarded):**
  - `(engage-from-idle)` — IDLE → ENGAGED, only fires if currently IDLE.
  - `(complete-from-engaged)` — ENGAGED → COMPLETING, only fires if currently ENGAGED.
  - `(idle-from-completing)` — COMPLETING → IDLE, only fires if currently COMPLETING.
- **Architectural inconsistency flagged in artifact_1:** Loop.metta uses raw `set-atom!` transitions; Clarity uses guarded transitions. If latch is in an unexpected state when loop.metta line 88 or 93 fires, the from-pattern won't match, potentially leaving two latch-state atoms in AtomSpace. "This has not been observed as a bug. But it is a potential inconsistency to be aware of when modifying the latch flow."
- **Important for v9 design:** The v9 gate's latch-fallback (Section 6 of the v9 source) reads `(latch-state $s)` and dispatches IDLE→SILENT, ENGAGED→ENGAGE, COMPLETING→ENGAGE, $other→SILENT. **The behavior depends on whether the latch state is what we think it is at gate-call time.**

---

## B. Consumers of the gate's output verdict

The gate's verdict is bound to `$aliveness` in loop.metta. Three downstream consumers:

### B.1 — LLM-call gating (`(== $aliveness SILENT)`)

- **Location (per artifact_1):** Lines 102, 107, 108 — the artifact_1 wiring diagram labels these "⚠️ DANGER ZONE" since they determine whether the LLM gets called, what gets printed, and the cycle's whole shape.
- **Behavior on SILENT:** LLM call skipped, response not generated, addToHistory NOT called for that cycle.
- **Behavior on ENGAGE:** Normal LLM call fires, response generated, history updated.

### B.2 — Aliveness verdict logging

- **Location:** `loop.metta` line 101 area (per artifact_1): `(println! (ALIVENESS_VERDICT: $aliveness))`. Confirmed in current loop_copy_metta.txt.

### B.3 — Verdict not written back to AtomSpace

- The gate verdict is bound to `$aliveness` in let* but NOT added to AtomSpace as an atom (per tier_c_audits_2026-05-18.md Item C9). So the verdict does not persist across cycles. Each cycle, the gate recomputes fresh.

---

## C. Intermediate transformations

The gate's logic chain in v9 (per apply_step6_aliveness_gate_migration.py source):

```
aliveness-gate $msgnew $idle
  │
  ├─ string_length($idle) > 0? ─yes─> ENGAGE
  │
  └─ aliveness-gate-default $msgnew
        │
        ├─ True ─> ENGAGE                                  [Priority 1: msgnew]
        │
        └─ False ─> gate-on-idle-pattern (current-idle-pattern)
              │
              ├─ () ─> gate-on-agency-balance (current-agency-balance)   [pre-bootstrap]
              │
              └─ ($v $c) ─> if $v == send-burst then SILENT              [Priority 2]
                            else gate-on-agency-balance (current-agency-balance)
                              │
                              ├─ () ─> gate-on-task-phase (current-phase)   [pre-bootstrap]
                              │
                              └─ ($v $p $s) ─> if $v == dependency-risk then SILENT  [Priority 3]
                                              else gate-on-task-phase (current-phase)
                                                │
                                                ├─ attending ─> SILENT       [Priority 4]
                                                ├─ idle ─> SILENT            [Priority 4]
                                                ├─ waiting ─> SILENT         [Priority 4]
                                                ├─ reflecting ─> SILENT      [Priority 4]
                                                │
                                                ├─ engaged ─> gate-on-latch-fallback     [Priority 5]
                                                ├─ research ─> gate-on-latch-fallback
                                                ├─ response-drafting ─> gate-on-latch-fallback
                                                ├─ boundary-detected ─> gate-on-latch-fallback
                                                │
                                                └─ $other ─> gate-on-latch-fallback     [Priority 6]
                                                              │
                                                              ├─ IDLE ─> SILENT
                                                              ├─ ENGAGED ─> ENGAGE
                                                              ├─ COMPLETING ─> ENGAGE
                                                              └─ $other ─> SILENT
```

No Python helpers in the gate path. All decision logic in MeTTa. Same property v8 had ("one of the cleanest reasoning-sovereignty wins" per artifact_1).

---

## D. Configuration constants affecting behavior

Per loop_copy_metta.txt initLoop and substrate files:

| Constant | Value | Affects |
| --- | --- | --- |
| `wakeupInterval` | 600 (10 minutes) | Idle directive guard (line 92). When > this many seconds since `&last_human_time`, guard True. |
| `maxWakeLoops` | 1 | After loops counter hits 0, this is how many more wake cycles fire. Currently 1, not 50. |
| `maxNewInputLoops` | 50 | Resets loops counter to this on new message arrival. |
| `sleepInterval` | 1 | Seconds between iterations. |
| `spamShield` | True | Adds "DO NOT RE-SEND OR SPAM!" suffix to `$lastmessage` when `!$msgnew`. |
| `send-burst-threshold` | 3 (hardcoded in writer per F39+F42) | Above this count of send-class atoms in 10-cycle window, idle-pattern verdict is send-burst. |
| `dependency-threshold` | 0.6 (hardcoded in writer per F42) | Above this person:system ratio, agency-balance verdict is dependency-risk. |
| `recent-action window` | 10 cycles (per artifact_1) | The window over which send-burst and dependency-risk are evaluated. |

**Configuration consequence to note:** The v9 design was rolled back when `wakeupInterval=1` (per tier_c_audits "Verification need #1"). Current wakeupInterval=600. This is a different operating point than the rollback context.

---

## E. Behavioral expectations under current configuration

Given current state (Bug 2/2b fixed, v8 gate active, wakeupInterval=600, maxWakeLoops=1), and given Berton's note that the "rolled-back v9 forced Clarity into a loop she could not iterate past the 9th iteration" is NOT being investigated further:

### E.1 — What v8 currently does (per current production source)

The v8 gate:
1. If `$idle_directive` non-empty → ENGAGE.
2. Else if `$msgnew` is True → ENGAGE.
3. Else dispatch on `(latch-state)`: IDLE → SILENT, ENGAGED → ENGAGE, COMPLETING → ENGAGE, other → SILENT.

The v8 gate does NOT read idle-pattern, agency-balance, or task-phase. Bug 2/2b's fix to those organs gives Clarity live data in her **prompt**, but the **gate** ignores them entirely. The prompt-vs-gate distinction is the key fact:

- Prompt blocks (`idle-pattern-block`, `agency-balance-block`, `task-state-block`) ARE in `getContext` per loop_copy_metta.txt. Clarity SEES the verdicts each cycle.
- Gate (`aliveness-gate`) does NOT consume those verdicts in v8. The gate engages based on idle_directive/msgnew/latch only.

**Consequence today:** When Clarity hits send-burst (today's spam pattern), her prompt shows `(idle-pattern send-burst 7)`. She self-diagnoses "If v9 gate were wired, I would be SILENT right now" (her words this morning). But the gate continues to engage. This is Bug 4: detection-without-consumer.

### E.2 — What v9 would do (per apply_step6 source)

Same priority-1 entry (idle_directive OR msgnew → ENGAGE). Then substrate composition: send-burst → SILENT, dependency-risk → SILENT, attending/idle/waiting/reflecting → SILENT. Engaged/research/response-drafting/boundary-detected fall through to latch dispatch. Unknown phase → latch dispatch.

### E.3 — Spec-vs-current gap (the actual gap)

| Element | Spec (v9 per artifact_1) | Current (v8) | Gap |
| --- | --- | --- | --- |
| Priority 1: idle_directive OR msgnew → ENGAGE | YES | YES | None |
| Priority 2: send-burst → SILENT | YES | NO | Bug 4 (consumer not wired) |
| Priority 3: dependency-risk + !msgnew → SILENT | YES | NO | Bug 4 (consumer not wired) |
| Priority 4: attending/idle/waiting/reflecting → SILENT | YES | NO | Consumer not wired |
| Priority 5: engaged/research/response-drafting/boundary-detected → latch fallback | YES | (latch is what v8 dispatches on directly, no phase guard) | Wiring difference |
| Priority 6: unknown phase → latch fallback | YES | (no phase read) | Wiring difference |

Functions that need to be defined for v9 (per the apply_step6 source):
- `aliveness-gate-default $msgnew` — wraps the default branch with msgnew check
- `gate-on-idle-pattern $pattern` — handles `()` pre-bootstrap and `($v $c)` tuple cases
- `gate-on-agency-balance $balance` — handles `()` pre-bootstrap and `($v $p $s)` tuple cases
- `gate-on-task-phase $phase` — handles each phase symbol + `$other` wildcard
- `gate-on-latch-fallback` — wraps the v8 latch-dispatch

The original 6ca6f44 commit had ALL of this working structurally at commit time ("Test 1 heartbeat F31 PASSED"). The iteration-9 trap that emerged later was NOT captured in the commit message itself.

### E.4 — Other behavioral notes that surfaced during this survey

These are facts noted in passing during reads; they're not gate logic, but they touch substrate the gate depends on:

- **msgnew sticky-True risk (open):** The Path 1 gamma drafting context flagged "msgnew flag appears to stick True across iterations, causing the same human message to be processed repeatedly." Not verified in this turn. Could affect the v9 priority-1 ENGAGE path's behavior.
- **idle_directive 953-char even when selected_goal=None (open):** Per 6ca6f44 commit message, the supervisor helper returns text content when it should return empty. This is a **helper-side bug, not a gate-side bug.** The v9 gate is structurally correct; the priority-1 ENGAGE path short-circuits when idle_directive is non-empty regardless of whether the directive content is meaningful.
- **Architectural inconsistency raw-vs-guarded latch transitions:** Loop.metta uses raw `set-atom!` for IDLE→ENGAGED and ENGAGED→IDLE; Clarity uses guarded `engage-from-idle`/`complete-from-engaged`/`idle-from-completing`. The v9 latch-fallback path reads whatever state results from those mixed-pattern writes.
- **maxWakeLoops=1 vs maxWakeLoops=50:** The rolled-back v9 was operating with wakeupInterval=1 (per tier_c audit speculation). Current configuration has wakeupInterval=600 and maxWakeLoops=1. The wake-burst that motivated Path 1 gamma is currently a single cycle, not 50. Path 1 gamma was drafted but NOT applied.

---

## What this template does NOT decide

This template does not decide:
- Whether to land v9 as-designed in 6ca6f44 source verbatim
- Whether to modify any priority hierarchy
- Whether to investigate the iteration-9 trap further (per Berton: no, not a rabbit hole)
- Whether to land Path 1 gamma first, or v9 first, or neither
- Whether to fix the supervisor-side "953-char even when selected_goal=None" bug first, after, or alongside
- Whether to address the msgnew sticky-True risk before v9 work

These are scope and sequencing decisions for Berton after reading the template.

---

## What this template DOES establish

- **Bug 4 is real and characterized:** detection-without-consumer pathology. The substrate observation organs work (Bug 2/2b fix verified). The gate doesn't read them. Clarity sees verdicts but the gate ignores them.
- **The v9 design (6ca6f44 source) exists in full and is recoverable:** the apply_step6_aliveness_gate_migration.py script contains the complete v9 substrate, dry-runnable, reversible.
- **task-state writers use a different mechanism than Bug 2/2b:** `set-atom!` rather than `car-atom + remove-atom`. No known pathology in this family at this time.
- **Pre-bootstrap safety in v9 is explicit per source:** `(current-idle-pattern) → ()`, `(current-agency-balance) → ()`, `(current-phase) → attending`. v9 handles all three cases via dedicated fall-through dispatch rules.
- **The gate signature `(aliveness-gate $msgnew $idle)` is preserved across v8 and v9:** No loop.metta change required for the gate substitution itself.
- **Configuration baseline differs from rollback context:** wakeupInterval=600 (not 1), maxWakeLoops=1 (not 50). Different operating point.
- **Open behavioral risks beyond the gate exist:** msgnew sticky-True, idle_directive 953-char-when-no-goal, raw-vs-guarded latch transitions. These are not gate bugs but they touch the gate's input surface.

---

## Document end

This survey is the pre-design audit Discipline 6 Part B requires. Next-step decisions (scope of v9 wiring, sequencing of fixes, what to verify empirically before drafting) are Berton's, informed by this evidence.
