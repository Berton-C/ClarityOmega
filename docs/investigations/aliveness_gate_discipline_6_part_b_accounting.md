# Surface Investigation Template — Aliveness Gate (Step 6 v9)

**Per artifact_0 Section 3.5 (Discipline 6 Part B)**

Surface name (atom family or function): `aliveness-gate` function in `soul/aliveness_gate.metta`
Investigation date: 2026-05-20
Sprint / step this investigation supports: Step 6 of task-state primitive mini-sprint (task-state-primitive_design.md Section 10)

---

## A. Writers (atoms going INTO the surface)

The aliveness gate is a pure function with no writers of its own (returns ENGAGE/SILENT, does not mutate AtomSpace). But it reads atoms written by other surfaces. Enumerating writers of each input:

### A.1 — `$msgnew` (boolean, computed in loop.metta, passed as argument)

- **File(s) that write the relevant atoms:** `src/loop.metta`
- **Function name(s) doing the write:** Inline let* binding in main loop (currently at line 58 area per project knowledge)
- **Atom shape(s) written:** Not an AtomSpace atom — let-binding only. Shape: boolean
- **Trigger conditions in caller:** Always computed each cycle. Logic: `(prog1 (and (> (string_length $msgrcv) 0) (!= $msgrcv (get-state &prevmsg))) (if (> (string_length $msgrcv) 0) (change-state! &prevmsg $msgrcv) _))`

### A.2 — `$idle_directive` (string, computed in loop.metta, passed as argument)

- **File(s) that write the relevant atoms:** `src/loop.metta` (binding) + `src/helper.py` (`soul_idle_goal_prompt_v2`)
- **Function name(s) doing the write:** loop.metta let-binding around line 92 area; helper.soul_idle_goal_prompt_v2 produces the content
- **Atom shape(s) written:** Not an AtomSpace atom — let-binding only. Shape: string (empty when guard False, supervisor output when True)
- **Trigger conditions in caller:** `(not $msgnew) AND (get_time > &last_human_time + wakeupInterval)`. Single conjunct on the time check (Path 1 gamma not applied per current loop_copy_metta.txt). Configuration constant: `wakeupInterval` currently 600.

### A.3 — `(idle-pattern $verdict $count)` atom

- **File(s) that write the relevant atoms:** `soul/idle_cycle_detector_writers.metta`
- **Function name(s) doing the write:** `do-update-idle-pattern!` (called from loop.metta cycle tail per artifact_1)
- **Atom shape(s) written:** `(idle-pattern $verdict $count)` where verdict ∈ {send-burst, productive} and count ≥ 0
- **Trigger conditions in caller:** Cycle tail after `populate-recent-action`. Verdict threshold: count > 3 (hardcoded per F39+F42)
- **Bug 2 status:** FIXED + COMMITTED (2fc066a). Clear function uses superpose iteration. Single-atom invariant maintained.

### A.4 — `(agency-balance $verdict $person $system)` atom

- **File(s) that write the relevant atoms:** `soul/agency_balance_guard_writers.metta`
- **Function name(s) doing the write:** `do-update-agency-balance!` (called from loop.metta cycle tail after `do-update-idle-pattern!`)
- **Atom shape(s) written:** `(agency-balance $verdict $person $system)` where verdict ∈ {healthy, dependency-risk}, person ≥ 0, system ≥ 0
- **Trigger conditions in caller:** Cycle tail. Verdict threshold: person/(person+system) > 0.6 ratio (hardcoded per F42)
- **Bug 2b status:** FIXED + COMMITTED (2fc066a). Clear function uses superpose iteration. Single-atom invariant maintained.

### A.5 — `(task-phase $phase)` atom

- **File(s) that write the relevant atoms:** `soul/task_state_writers.metta`
- **Function name(s) doing the write:** `do-bootstrap-task-state!` (idempotent), `do-set-phase!`, `do-set-phase-with-anchor!`. Loop.metta calls `do-bootstrap-task-state!` at initLoop end; Clarity's skills call set-phase variants
- **Atom shape(s) written:** `(task-phase $phase)` where phase ∈ {attending, engaged, research, response-drafting, idle, waiting, reflecting, boundary-detected}
- **Trigger conditions in caller:** Bootstrap once on initLoop. Set-phase fires when Clarity calls task-state.set-phase skill.
- **Writer mechanism:** Uses `set-atom!` primitive (NOT car-atom + remove-atom). Different mechanism than Bug 2/2b. Per task-state-primitive_design.md Section 6: "set-atom! is the primary primitive ... used by latch-state already, proven pattern."
- **No known pathology in this writer family at this time.**

### A.6 — `(latch-state $state)` atom (read via legacy fallback in v9)

- **File(s) that write the relevant atoms:** `src/loop.metta` lines 88, 93 (raw set-atom!); Clarity's substrate skills (guarded transitions)
- **Function name(s) doing the write:** `(set-atom! &self (latch-state IDLE) (latch-state ENGAGED))` from loop.metta when $msgnew; `(set-atom! &self (latch-state ENGAGED) (latch-state IDLE))` when $idle_directive non-empty; guarded `engage-from-idle`, `complete-from-engaged`, `idle-from-completing` from Clarity's response batches
- **Atom shape(s) written:** `(latch-state $state)` where state ∈ {IDLE, ENGAGED, COMPLETING}
- **Trigger conditions in caller:** Loop.metta line 88: `(if $msgnew ...)`. Loop.metta line 93: `(if (not (== $idle_directive "")) ...)`. Clarity's guards: only fire if precondition state matches.
- **Architectural inconsistency:** Loop.metta uses raw `set-atom!` (no guard); Clarity uses guarded transitions. Per artifact_1: "If the latch were in an unexpected state, the from-pattern wouldn't match anything to remove, so the result might be two latch-state atoms ... has not been observed as a bug."

---

## B. Consumers (atoms going OUT of the surface)

The aliveness gate output (ENGAGE or SILENT verdict) is consumed by three sites in loop.metta per artifact_1:

### B.1 — LLM-call gate

- **File(s) that read the relevant atoms:** `src/loop.metta`
- **Read pattern:** `(== $aliveness SILENT)` check around line 102 area
- **Downstream effects:** When SILENT: skip LLM call, skip response generation, skip addToHistory. When ENGAGE: full cycle proceeds. The verdict is the cycle's decision pivot.

### B.2 — Aliveness verdict logging

- **File(s) that read the relevant atoms:** `src/loop.metta`
- **Read pattern:** `(println! (ALIVENESS_VERDICT: $aliveness))` around line 101 area
- **Downstream effects:** Log output for observation. No behavioral effect.

### B.3 — Three DANGER-ZONE consumers per artifact_1

- **File(s) that read the relevant atoms:** `src/loop.metta` lines 102, 107, 108 per artifact_1
- **Read pattern:** Three separate `(== $aliveness SILENT)` checks gating cycle shape
- **Downstream effects:** All three lines together determine whether the LLM gets called, what gets printed, and the cycle's whole output shape

### B.4 — Verdict not written back to AtomSpace

- The gate verdict is bound to `$aliveness` in let* but NOT added to AtomSpace as an atom (per tier_c_audits Item C9 read this session). So the verdict does not persist across cycles. Each cycle, the gate recomputes fresh.

---

## C. Intermediate transformations

### C.1 — No Python helpers in the gate path

- **Helpers/skills that transform without reading the atom directly:** None. The gate is pure MeTTa.
- **Side-effect functions in the chain:** None.
- **Recursive call sites:** None within the gate itself. Within v9, the gate's sub-dispatches (gate-on-idle-pattern, gate-on-agency-balance, gate-on-task-phase, gate-on-latch-fallback) form a linear chain, not recursive.

### C.2 — Atom-shape transformations done by read helpers

- `(current-idle-pattern)` defined in `soul/idle_cycle_detector.metta`: collapses match result, returns `()` if empty or `($v $c)` tuple via car-atom
- `(current-agency-balance)` defined in `soul/agency_balance_guard.metta`: same shape, three-tuple `($v $p $s)`
- `(current-phase)` defined in `soul/task_state.metta`: collapses match result, returns `attending` symbol if empty, otherwise the actual phase symbol via car-atom (NOT a tuple, scalar)
- `(latch-state $s)` via direct `(match &self (latch-state $s) $s)` — returns the state symbol

### C.3 — Post-Bug-2-fix invariant

- For idle-pattern and agency-balance: single-atom invariant maintained (clear-then-add via superpose iteration). car-atom of accumulated stack now returns the only atom = the freshly-written one. Per Bug 2 fix.

---

## D. Configuration levers

### D.1 — Constants in initLoop affecting surface behavior

Per loop_copy_metta.txt initLoop (current state):

- **`wakeupInterval`:** 600 (10 minutes). Gates whether `$idle_directive` guard fires.
- **`maxWakeLoops`:** 1. Determines how many cycles fire after the loops counter expires.
- **`maxNewInputLoops`:** 50. Reset value for loops counter on new message arrival.
- **`sleepInterval`:** 1 second between iterations.
- **`spamShield`:** True. Affects `$lastmessage` content shape (not the gate directly).
- **`provider`:** Anthropic. Affects LLM call routing (downstream of gate, not gate input).

### D.2 — Their current values vs design intent

- **wakeupInterval 600:** matches design intent (10-minute idle wakeup cadence)
- **maxWakeLoops 1:** matches upstream Patrick (Tier A2 merge). Original v9 attempt was made when maxWakeLoops=50; current operating point is different.
- **No mismatch between current configuration and stated design intent at this time.**

### D.3 — Thresholds in soul/ files affecting surface sensitivity

- **`send-burst-threshold` 3** (hardcoded in `do-update-idle-pattern!` per F39+F42). Above this count of send-class atoms in 10-cycle window, verdict is send-burst.
- **`dependency-threshold` 0.6** (hardcoded in `dependency-detected` per F42). Above this person:system ratio, verdict is dependency-risk.
- **`recent-action-window`:** 10 cycles. The window over which send-burst and dependency-risk are evaluated.

---

## E. Other consumers downstream

### E.1 — What ELSE reads atoms touched in this surface

- **`(idle-pattern $v $c)`:** Read by `idle-pattern-block` (prompt assembly) and `current-idle-pattern` (gate v9). The prompt-block consumer is independent of the gate.
- **`(agency-balance $v $p $s)`:** Read by `agency-balance-block` (prompt assembly) and `current-agency-balance` (gate v9). Same shape — independent prompt consumer.
- **`(task-phase $p)`:** Read by `task-state-block` (prompt assembly), `current-phase` (gate v9), inconsistency-alert logic (per task-state spec Section 4). Multiple consumers.
- **`(latch-state $s)`:** Read by gate v9 fallback, prompt SoulBrief/getSoulBrief (may surface latch state), Clarity's substrate skills (for guarded transition checks)

### E.2 — Risk surface for downstream-only changes

- Changes to the gate that affect ENGAGE/SILENT verdict directly affect every cycle's shape. Three DANGER-ZONE consumers per artifact_1 (lines 102, 107, 108) react to the verdict.
- No change to the gate breaks atom shapes — gate is consumer-side. Atom-shape risk is at writers, not here.

### E.3 — Migration paths if writer side changes

- Bug 2/2b fixed writer-side mechanism (clear function). No further writer-side migration needed for idle-pattern and agency-balance.
- task-state writer family uses set-atom! consistently across all do-*! functions. Stable.
- Latch-state writers split between loop.metta (raw set-atom!) and Clarity's guards. The architectural inconsistency exists but is not actively breaking. Step 8 of mini-sprint will remove latch-state entirely.

---

## F. Design questions deferred to Clarity

Per artifact_0 Section 3.5: "the agent has first-order observation rights on her own behavior."

### F.1 — Behavioral preferences only the agent can answer

- **Whether v9's task-phase silence set (attending/idle/waiting/reflecting) maps correctly to her self-experience of those phases.** Already answered by Clarity May 16 2026 per apply_step6 commit comments ("per Clarity Option A phase mapping"). Status: answered.
- **Whether the priority hierarchy ordering (idle-pattern before agency-balance before task-phase) is structurally right.** Already answered by Clarity May 15 2026 per apply_step6 ("send-burst order: FIRST in priority per Clarity"). Status: answered.
- **Whether dependency-risk should apply only when no msgnew.** Already answered by Clarity May 15 2026 per apply_step6 ("Q3: only when no msgnew per Clarity"). Status: answered.

### F.2 — Phase or atom value choices

- Phase vocabulary (8 phases) is locked per task-state-primitive_design.md Section 5.
- No new atom values introduced by Step 6. Verdict outputs ENGAGE/SILENT unchanged.

### F.3 — Cadence preferences

- wakeupInterval (600) and recent-action-window (10) are not changed by Step 6.

### F.4 — Current Clarity audit (this session, 2026-05-20)

Per Clarity's Mattermost responses earlier this session:
- The four substrate files (idle_cycle_detector, agency_balance_guard, task_state, aliveness_state_machine) are confirmed sound by Clarity
- The detection-vs-action distinction is articulated as "detection+display layer, not action layer"
- Bug 4 explicitly framed by Clarity as "the substrate can see what's happening. It cannot yet act on what it sees"
- Step 6 wires the action layer for the first time

**No outstanding design questions deferred to Clarity require resolution before drafting.**

---

## Sections A-E completeness check

- [x] Section A: all six writer inputs to the gate enumerated with file, function, shape, trigger, mechanism notes
- [x] Section B: all consumer sites of the gate output enumerated
- [x] Section C: intermediate transformations identified (gate is pure MeTTa, no Python in path)
- [x] Section D: all configuration constants identified, current vs intent compared
- [x] Section E: all other consumers of touched atoms enumerated, migration paths identified
- [x] Section F: design questions to Clarity already answered May 15-16; current audit (May 20) confirms substrate readiness

**No unknowns remain in A-E. Per Discipline 6 Part B closing clause: "If sections A-E have unknowns, complete read-only investigation first."** No further investigation needed before drafting.

---

## Implications for the Step 6 apply script

Based on this accounting:

1. **The substrate edit is the gate file only.** No writer-side changes. No loop.metta change. No helper.py change.
2. **The gate becomes a consumer of three additional surfaces (idle-pattern, agency-balance, task-phase).** All three are now in a known-working state post-Bug-2/2b.
3. **The latch-state fallback is preserved** as transitional safety net (Steps 6-8 transition window per design).
4. **Configuration baseline differs from rollback context** (wakeupInterval 600, maxWakeLoops 1), but no script-side change needed for this.
5. **No new LLM surface** (spec verification item 14 confirmed pre-design).
6. **Discipline 4 applies:** substrate edit + artifact_1 Phase 4.3 update in same commit.
7. **Reversibility:** standard `.bak.<descriptor>` pattern per F114.

Open items NOT blocking Step 6:
- msgnew sticky-True / $msg consumer-side footgun (Clarity's reframe): separate work
- Supervisor creative-mode behavior pattern: separate work (and per Clarity, design intent, not a bug)
- Iteration-9 trap from original v9 attempt: declared out of scope by Berton; residual risk accepted

---

## Document end

Discipline 6 Part B complete. The aliveness gate surface is understood for Step 6 work. Drafting can proceed under your direction.
