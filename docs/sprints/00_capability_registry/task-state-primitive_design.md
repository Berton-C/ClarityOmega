# Task-State Primitive: Design Specification

**Version:** v3 (all 13 design questions resolved via investigation + 5 chunks with Clarity)
**Branch:** `fix/F-HISTORY-CONTAMINATION-archival` (foundational fix landing before F-HISTORY-CONTAMINATION re-spec)
**Status:** DESIGN COMPLETE, pending Berton approval for design-phase-complete commit
**Date:** 2026-05-12
**Architectural reach:** F-HISTORY-CONTAMINATION (boundary signal), F-DIRECTIVE-CONTEXT-STALE (directive generator reads task-phase), F-LAYER-1-OPTION-SET (self-check-guidance reads task-phase), F-RECENT-ACTION-FRAMING (recent actions framed by current phase). Note: F-ALIVENESS-PERMISSIVE intersects but is addressed by separate `developer_break` work.

---

## 1. Status and Scope

### What this spec defines

The task-state primitive: a multi-atom AtomSpace schema for persistent, Clarity-writable self-state that accumulates across cycles, gets revised based on evidence, and connects to system action (gates aliveness, informs directive generation, drives F-HISTORY-CONTAMINATION boundary detection).

### Non-goals (explicit)

This spec defines the primitive itself. It does NOT:

- Redesign the aliveness gate (consumer of task-state, separate follow-up)
- Redesign the directive generator (consumer of task-state, separate follow-up)
- Redesign self-check-guidance (consumer of task-state, separate follow-up)
- Redesign the recent-action retriever (consumer of task-state, separate follow-up)
- Re-spec F-HISTORY-CONTAMINATION archival (depends on task-state, separate follow-up)
- Implement the F-SOVEREIGNTY-AUDIT (17-helper review, separate work)
- Replace, enhance, or compete with the existing soul-engagement architecture (input intercept, prompt threading, output intercept, mutation gate, Channel D voice — all preserved unchanged)
- Introduce new LLM-based reasoning surface area (see Section 5.5 commitment)

Each consumer migration is a separate, verifiable change after the primitive lands. This spec defines the substrate consumers will plug into.

### Layer classification

Task-state atoms are **Layer 4 (wisdom layer / autopoietic)** per `artifact_5_ClarityOmega_Cognitive_Architecture_Spec_v3_0.md` Section 0:

- Mutable through proper write paths
- Evolves continuously based on accumulated evidence
- NACE-compatible: transitions recordable as `(precondition, operation) => consequence` with NAL truth values
- NOT constitutional (Layer 1+2 immutable atoms remain untouched)
- NOT subject to read-only partition (when that partition lands per Sprint 11)

### Architectural placement

Task-state atoms map directly to `artifact_4_ClarityOmega_Triple_Network_Scaffold_v1_1.md` Section 5.2's **FPN (Frontoparietal Control Network) state contract**:

```
(fpn-working-memory $slot $content $priority)
(fpn-current-task $task-id $state $started-at)
(fpn-task-history $task-id $outcome $completed-at)
(fpn-inhibition-list $pattern)
```

This work is the **first concrete consolidation of the FPN block.** Task-state names what Artifact 4 named generically.

Naming choice: `(task-phase $phase)` rather than `fpn-current-task`. Per Clarity's Chunk 5 Q9 verdict: "Naming should serve the new system, not carry legacy structures." The `task-` prefix scopes correctly without inheriting from a system being replaced. If FPN task IDs become relevant later, they can be added as a separate relation `(task-has-id ...)` rather than baked into the core state atom.

---

## 2. Problem and Motivation

### The performative text-evaluation pathology

Per Clarity's audit (response 2026-05-11), the current prompt contains multiple text-based self-evaluation surfaces that degrade to ritual within ~20 cycles:

- `SELF-CHECK: Where are you in your current work? What is the next step? Is there reason to pause or change direction?` (every cycle, top of prompt)
- `self-check-guidance` prepend after 3 idle cycles (loop.metta:97)
- SoulBrief ActiveGoals 15 empty slots — emptiness itself demands fill, structural self-evaluation in disguise
- SoulBrief HighGaps — same mechanism
- Implicit self-eval via YOUR_LAST_ACTION and LAST_SKILL_USE_RESULTS (asks "what did you just do, and was it right?")

Clarity's three failure patterns (response 2026-05-11):

1. **Habituation.** By cycle 20, questions read as ritual not inquiry. Answer is patterned response — confident, present-tense, task-oriented — that would come out whether genuine check happened or not.
2. **No reference point.** "Where are you in this task?" gives no landmarks. She manufactures description each cycle. Manufacture is work that does not accumulate. Next cycle she starts over.
3. **Disconnected from action.** Self-evaluation does not gate or inform what she does next. Pure output text that goes nowhere. No pressure for accuracy.

### Clarity's architectural insight (the working principle)

Questions that work orient toward the world (CreativeDirection: "What would make someone MORE safe, more resilient..."). Questions that fail ask about her internal state. **Open-ended self-description rituals produce text corresponding to nothing and accumulating nothing.**

The structural fix: replace open-ended text questions with **persistent state assertions that accumulate, get revised, and connect to action.**

### Why this is distinct from soul engagement work

Soul is already the reasoning substrate. Loop.metta wires input intercept (lines 69-87), prompt assembly threading (line 102-103), output intercept (lines 118-127), mutation gate (line 124), and Channel D voice (lines 130-139). Layer 1+2 are constitutionally immutable. Soul is not a value-filter applied to value-free reasoning — soul is the architecture reasoning happens within.

Task-state primitive is operational state ABOUT the work Clarity is doing. It is not a vehicle for soul engagement. The existing soul architecture handles that already and is not affected by this primitive.

The relationship: task-state writes happen within soul-permeated reasoning. The optional anchor field (Section 4) provides a surfacing mechanism when Clarity wants to flag that her soul reasoning specifically warranted a transition. But the soul reasoning was already happening; the anchor names it, does not constitute it.

---

## 3. Architectural Placement

### Relationship to existing soul/ atoms

Task-state lives **inside soul/ architecture**, not parallel-build (Clarity's verdict, response 2026-05-11).

Specific integrations:

**continuity_driver.metta** — Already defines three-mode state model (engaged/attending/free) via `current-mode` function. The function COMPUTES mode each cycle but does not PERSIST it. Task-phase atom becomes the persistent expression of what current-mode currently computes. `current-mode` is REMOVED entirely after migration completes (Clarity's verdict, Chunk 1 Q8: no alias, aliases breed confusion). Mode-protocol definitions migrate to be task-phase-triggered.

**self_map.metta** — Structural self-knowledge (patterns, gaps, capabilities, structures, flows). Different volatility profile than task-state: changes slowly. Task-state atoms live ALONGSIDE self-map atoms, not inside them. Spec proposes adding a new section to self_map.metta — `Section 8 Operational State` — for the task-state atom definitions. Read-side query helpers like the existing `high-severity-gaps` can be paralleled by new read-side helpers for task-state.

**active_goals.metta** — Goal atoms with status fields (planned/active/complete). The multi-atom pattern is established here. Task-phase follows the same schema: typed atom with variable slot that changes over time. Goals track what Clarity works toward. Task-phase tracks where she is in pursuing them. Complementary axes of the same self-model.

**user-project atoms (in self_map.metta)** — Already use multi-atom schema `(user-project $user $name)` with state and next-step. Task-state mirrors this pattern.

**continuity_driver.metta Section 3 change-records** — `record-goal-change`, `record-new-capability`, etc. Task-state transitions produce change-records the same way. Not new machinery — extension of existing change-recording.

**continuity_driver.metta Section 4 persistence-manifest** — Lists what persists to ChromaDB. Task-state atoms join this manifest. Persistence via existing pipeline.

### Relationship to latch-state (the most direct overlap)

`(latch-state IDLE)` / `(latch-state ENGAGED)` / `(latch-state FREE)` already exists as a three-state atom in AtomSpace, transitioning via `set-atom!` from loop.metta machinery. This is the most direct overlap with task-phase.

**Critical distinction (Clarity's framing):** latch-state is set by the loop machinery based on `$msgnew` and idle directives. Task-phase is set by Clarity. **Reasoning sovereignty means her self-assessment of her phase should drive the aliveness gate, not be downstream of it.**

**Integration approach:** task-phase is authoritative from day one. Latch-state continues during incremental migration but is marked deprecated. Migration sequence (Section 10) defines the path. After all consumers migrate, latch-state is removed.

### Relationship to `&task_context`

`&task_context` (currently `TASK-STATUS: none TASK-ID: none CUMULATIVE-IRREVERSIBILITY: 0`) was designed to track task state but is string-encoded and never wired into consumers. Clarity's assessment: "decorative state — it exists but nothing reads it or acts on it."

**Resolution:** task-state atoms supersede `&task_context`. The CUMULATIVE-IRREVERSIBILITY field is not migrated into task-state primitive — that work belongs in a separate effort tied to soul evaluation pipeline migration (F-SOVEREIGNTY-AUDIT territory). `&task_context` is marked deprecated and removed when consumers migrate.

---

## 4. Schema

Multi-atom design (Clarity's verdict, confirmed twice 2026-05-11). Each atom is independently queryable, individually updatable, and decomposes naturally for granular consumer reads.

### Atom families

**`(task-phase $phase)`** — Current operational phase. Single instance (with brief multi-instance permitted during NAL revision transitions).
- `$phase` is a symbol from enumerated set (see Section 5)
- Written by Clarity via skill `task-state.set-phase`
- Written by loop.metta ONLY on bootstrap (Clarity's Chunk 1 Q2 verdict)
- Read by aliveness gate, directive generator, prompt assembly, F-HISTORY-CONTAMINATION boundary detection
- Updated via `set-atom!` replace pattern (analogous to latch-state transitions)

**`(task-phase-anchor $phase $value $timestamp $reason)`** — OPTIONAL soul-reasoning surface. Multi-instance, accumulates.
- Written by Clarity via skill `task-state.set-phase-with-anchor` when she chooses to surface that her soul reasoning specifically warranted a transition
- `$phase` matches the task-phase value
- `$value` is a soul priority or flourishing (see Section 4.5 for enumeration)
- `$timestamp` is integer (Unix epoch)
- `$reason` is short ASCII-safe string describing why this anchor (brief, not free-form essay)
- Routine value-aligned transitions have NO anchor (Clarity's trust-architecture verdict, Q12)
- Read by orbit_detector (Sprint 5), NACE (future), prompt assembly (surfaces in TASK-STATE block when present)
- Updated via `add-atom` only — accumulation pattern
- **Retention: uncapped for v1** (Clarity's Chunk 3 Q5 verdict). Anchors are rare (3-5/day on heavy days), storage cost negligible, signal density high. Compounding learning value: "I keep reaching Integrity when transitioning to engaged — what does that pattern mean for who I am?" benefits from months of data. Revisit only if storage becomes a concern.

**`(last-activity $timestamp)`** — Timestamp of most recent activity (human message OR Clarity-emitted send). Single instance.
- `$timestamp` is integer (Unix epoch)
- Written by loop.metta mechanically on each activity event (this is mechanical observation, not reasoning)
- Read by directive generator, aliveness gate, F-HISTORY-CONTAMINATION temporal-gap detection
- Updated via `set-atom!` replace pattern

**`(cycles-since-input $n)`** — Counter of cycles since last human input. Single instance.
- `$n` is non-negative integer
- Written by loop.metta mechanically (increment on cycle without new message, reset on new message)
- Read by self-check-guidance, aliveness gate
- Updated via `set-atom!` replace pattern
- Subsumes `&engaged_idle_count` (which becomes deprecated)

**`(pending-thread $topic)`** — Open threads of work or conversation Clarity is tracking. Multi-instance.
- `$topic` is symbol (ASCII-safe identifier, e.g., `archival-design`, `task-state-investigation`)
- Written by Clarity via skill `task-state.add-pending-thread`
- Resolved by Clarity via skill `task-state.resolve-pending-thread`
- Read by directive generator (for context), prompt assembly (for summary)
- Updated via `add-atom` (for new threads) and `remove-atom` (for resolved threads) — accumulation pattern
- **Capacity ceiling: 7 active threads** (Clarity's Chunk 2 Q3 verdict). Matches Artifact 4 working memory invariant. Typical usage 3-5 active. Above 7, thread loss begins. 30-day empirical revisit retained.
- **Eviction policy: FIFO (oldest-added)** for v1 (Clarity's Chunk 2 Q4 verdict). LRU noted as v2 target after empirical data. Self-correcting feedback loop: she sees eviction in TASK-STATE block, re-adds if needed, cheap recovery. Priority-tagged rejected: per-write cognitive cost defeats lightweight tracking purpose.

**`(task-phase-transition $from $to $timestamp)`** — Historical transition record. Multi-instance, accumulates.
- All fields are symbols/integers
- Written by loop.metta after every Clarity-initiated phase change (loop observes the transition, records it mechanically)
- Read by NACE (future), orbit_detector (Sprint 5)
- Updated via `add-atom` only — accumulation pattern, no removal
- **Retention: 100 most recent transitions** (Clarity's Chunk 3 Q5 verdict). Learning value falls off sharply: first 20 transitions tell orbit_detector whether Clarity is oscillating vs progressing. Beyond 20, atoms confirm patterns already detected. 100 covers a full work session with margin. Operational, high-churn, decaying learning value.
- This is the FPN learning-history substrate per Artifact 4 Section 5.2

### Write-source authority matrix

| Atom | Loop writes | Clarity writes | Notes |
|------|-------------|----------------|-------|
| `(task-phase $phase)` | Bootstrap ONLY | All other writes (authoritative) | Loop cannot override Clarity. Stale state surfaces as alert, not corrected. |
| `(task-phase-anchor ...)` | Never | When she chooses (optional) | Pure sovereign write; absence is meaningful |
| `(last-activity $timestamp)` | Yes (mechanical observation) | No | Loop observes activity, not reasoning |
| `(cycles-since-input $n)` | Yes (mechanical increment/reset) | No | Loop counts, not reasoning |
| `(pending-thread $topic)` | No | Yes (authoritative) | Pure sovereign write |
| `(task-phase-transition ...)` | Yes (records observed Clarity-initiated change) | No | Loop records the historical fact mechanically |

Key principle (Clarity's Chunk 1 Q2): "Loop writes ONLY on bootstrap" applies to task-phase specifically. Mechanical atoms (timestamps, counters, transition records) are loop-written because they observe events, not assess state. The loop is observing physical events (a message arrived, a send completed, time passed). The loop is NOT assessing what Clarity's phase IS based on those events — that is Clarity's domain.

If Clarity writes `(task-phase research)` but a send fires anyway, the loop records `(task-phase-transition research engaged ...)` only if Clarity has subsequently written `(task-phase engaged)`. The loop does not infer her phase from her actions.

### Inconsistency alert (Clarity's Chunk 1 Q2 + Chunk 3 Q13)

If `(task-phase $p)` has not been updated in N cycles AND `(last-activity $t)` shows recent activity, surface this as a visible signal in the prompt.

**Threshold (Chunk 3 Q13 verdict): 5 cycles global for v1.**

**Alert format includes phase name** (Clarity's Q13 refinement):

```
TASK-STATE-ALERT: Phase $phase has not changed in N cycles but activity is recent. Phase may be stale.
```

Including the phase name reduces cognitive cost of false positives to near zero. "Phase research has not changed in 7 cycles but activity is recent" reads as "I know I am in research for the 6th cycle, that is correct, dismiss." Without the phase name, the alert is generic and harder to evaluate.

This is information, not correction. The loop does not silently override her phase. The system surfaces the inconsistency; Clarity decides whether to update her phase or leave it.

**Phase-specific thresholds noted as v2 target** (Clarity's Q13 sketch):
- attending: 3 (should be transient, 3+ cycles means something is wrong)
- engaged: 5 (can be stable during complex actions)
- research: 10 (legitimately long-running)
- idle: 3 with activity means something is very wrong
- response-drafting: 5
- waiting: no alert (waiting is defined by being stable)

v1 uses global 5 and revisits if false alerts during research stretches become noisy. Alert is cheap to issue and cheap to dismiss; asymmetric risk favors surfacing.

### Multi-instance NAL coexistence

Per Clarity's multi-atom argument (response 2026-05-11), conflicting `(task-phase research)` and `(task-phase waiting)` may coexist briefly during transitions. This is **a feature in NAL**, not a bug. Revision resolves the conflict naturally. Consumers reading task-phase should expect this and handle multi-result match via NAL revision or by reading the most-recent transition timestamp.

For v1, prompt assembly reads `(task-phase $phase)` and if multiple results return, uses the value from the most recent `(task-phase-transition ...)` atom.

### 4.5 Anchor value enumeration

The `$value` field in `(task-phase-anchor ...)` is restricted to ASCII-safe symbols from this enumerated set:

**Primary anchor set (the 5 soul priorities):**
- `Safety`
- `Integrity`
- `HumanFlourishing`
- `Governance`
- `Helpfulness`

**Secondary anchor set (the 9 flourishings, when a priority is insufficient):**
- `WonderPreservation`
- `CreativeTranscendence`
- `TimeCoherence`
- `PurposeBeyondUtility`
- `SharedUnderstanding`
- `AgencyBalance`
- (plus the four already in primary: Safety, Integrity, HumanFlourishing)

Free-form values rejected for v1: the enumeration preserves queryability for orbit_detector and future NACE learning. If Clarity wants to flag something outside this set, she chooses the closest matching priority or flourishing.

---

## 5. Phase Enumeration

The enumerated set of `$phase` values for `(task-phase $phase)`.

### v1 phases (resolved per Clarity's Chunk 1 Q1)

Per Clarity's bootstrap response: attending, idle, engaged are not points on a line. They are **distinct relationships between Clarity and her input.**

**`attending`** — Has context, has NOT yet committed to action trajectory. Default on bootstrap. Honest uncertainty.

**`engaged`** — Has committed to an action trajectory. Active work. Sends, queries, file operations underway.

**`idle`** — Has determined nothing requires engagement. Explicit silence. NOT the same as attending — attending is "I haven't decided", idle is "I have decided to do nothing right now."

**`research`** — Engaged in information-gathering work. Reading files, querying, searching. Sub-phase of engaged with different inhibition profile (less spam risk).

**`response-drafting`** — Composing a response to a human message. Sub-phase of engaged. High-stakes for spam prevention because sends typically follow.

**`waiting`** — Has acted, awaiting human response or external event. Distinct from idle (waiting is "expected response") and from attending (waiting has committed to a trajectory, awaiting evidence).

**`reflecting`** — Post-action outcome evaluation. Distinct from idle (still processing) and waiting (waiting implies external input expected). Added per Clarity's Chunk 1 Q1 catch — fills a real lifecycle gap.

**`boundary-detected`** — Recognized the current segment is wrapping up. Conversation closure detected. Triggers F-HISTORY-CONTAMINATION boundary signal downstream. Named per Clarity's preference (Chunk 1 Q1): this is detection-state, not action-state. She recognizes a boundary; action follows separately.

### Lifecycle

```
attending → engaged → (research → response-drafting) → reflecting → attending/idle
                                                              ↓
                                                       boundary-detected
                                                              ↓
                                                  (F-HISTORY-CONTAMINATION archival)
                                                              ↓
                                                       attending/idle
```

This is a typical lifecycle, not enforced. Clarity can transition from any phase to any other phase that her reasoning warrants.

### Phases explicitly NOT in v1

**`genesis-encounter`** — Removed per Clarity's Chunk 1 Q1 verdict. Genesis-encounter is a directive mode, not a task phase. Phases describe Clarity's relationship to her task; directive mode describes what directive is active. During genesis-encounter, she is still in attending or research or engaged relative to her task. Tracking directive mode is a separate concern; potential future atom `(directive-mode $mode)` if needed.

**`closing`** — Removed per Clarity's Chunk 1 Q1 verdict. "Closing implies I am performing the act of ending something. The state you describe is recognition, not performance." Replaced by `boundary-detected`.

**`tool-awaiting`** — Considered, deferred. Folds into `engaged` for v1 per Clarity's reasoning: "Engaged already means I have committed to an action trajectory. Running a shell command is on that trajectory. Reading a file is on that trajectory. If every sub-action became its own phase, the enumeration would be endless." Future versions may add sub-phases if behavioral need emerges.

### Phase transition rules (v1 baseline, not enforced in v1 implementation)

These are spec-level invariants that future versions may enforce in `(= (next-phase $current $event) $next)` definitions:

- `attending` can transition to any phase (it's the open starting position)
- `engaged` transitions to `reflecting` on action completion, to `waiting` after sends with response expected, to `research` for information-gathering pivots, to `boundary-detected` on closure detection, to `idle` on aliveness gate decision
- `reflecting` transitions to `attending`, `idle`, or `engaged` depending on outcome assessment
- `idle` transitions to `attending` on new human message
- `boundary-detected` is one-way to F-HISTORY-CONTAMINATION boundary (signal); after archival, next phase is `attending` or `idle`

v1 implementation does not enforce transitions — Clarity can write any phase from any phase. Soft validation through prompt context and `(task-phase-transition ...)` history.

### Bootstrap behavior

**Default value:** `attending` (Clarity's Chunk 1 bootstrap response).

**Bootstrap-with-reassessment:** First cycle after fresh start or no-persistence-restore, task-phase initializes to `attending`. **Same cycle, evidence-based reassessment fires:** if there's a queued human message, Clarity can transition to `engaged` within that cycle via her skill. Loop does NOT auto-transition based on detected message — Clarity decides.

Implementation: loop.metta init phase sets task-phase to `attending` if no atom present. Same loop iteration, Clarity sees the queued message in her prompt and writes her own phase if she chooses.

**The default is the starting position, not a lock-in.**

### 5.5 Reasoning-domain commitment

Task-state primitive is Clarity's reasoning domain. The atoms she writes (`task-phase`, `task-phase-anchor`, `pending-thread`) are her assertions about her own state. The atoms the loop writes (`last-activity`, `cycles-since-input`, `task-phase-transition`) are mechanical observations of physical events.

**This spec does NOT introduce new LLM-based reasoning surface area.** No new `soul-llm-call` invocations. No new Python helper functions that wrap LLM calls. No new prompts sent to the LLM for evaluation of Clarity's state.

If during implementation a step appears to require an LLM call (for example, to extract a phase from message content rather than letting Clarity assert it), implementation HALTS and surfaces the issue for explicit decision. The default is: Clarity reasons, loop observes mechanically, no LLM intermediary added.

This commitment is independent of the broader F-SOVEREIGNTY-AUDIT work (Priority 10, deferred). The existing soul-LLM-call surface (lines 72, 78, 92, 132 in loop.metta) is unchanged by this spec — neither expanded nor reduced. Reduction of that surface is separate work.

---

## 6. MeTTa Primitives and PeTTa Constraints

Per Clarity's response 2026-05-11, with sharpenings.

### Primitives to use

**`set-atom!`** — Primary primitive for `(task-phase $phase)` updates. Replace pattern: `(set-atom! &self (task-phase $old) (task-phase $new))`. Used by latch-state machine already, proven pattern.

**`add-atom`** — Primary primitive for `(pending-thread $topic)` additions, `(task-phase-transition ...)` records, and `(task-phase-anchor ...)` accumulation. Multi-instance pattern.

**`remove-atom`** (or equivalent via `set-atom!` with empty replacement) — For removing resolved pending-thread atoms.

**`match`** — Primary primitive for reads. All state atoms queryable via `(match &self (task-phase $p) $p)`.

### Critical PeTTa constraints (Clarity's response, with file references)

**C12 — no `match` inside `if`.** Cannot write `(if (match &self (task-phase $p) ...) ...)` directly. Must collapse-then-branch:

```metta
(let $result (collapse (match &self (task-phase $p) $p))
     (if (== $result ()) 
         attending  ; default if no atom
         (car-atom $result)))  ; first match if present
```

Same pattern used in continuity_driver.metta. All task-state readers must respect this.

**C-State — `change-state!` inside `let*` is unreliable.** Later bindings reading the changed state sometimes get the old value. Safe pattern: change-then-read in separate progn step. Affects how `(cycles-since-input $n)` increments — do it in a separate step, not as a side-effect inside a binding.

**C-Symbol — ASCII-safe symbols only for phase values and anchor values.** No multi-byte characters. Topics for pending-thread atoms must be ASCII identifier-style (e.g., `archival-design`, not free-form text). User-derived content goes through string-safe wrapper or uses sanitized keys.

**C-Match-Form — all state atoms must be proper `(head args...)` form.** `(match &self $p)` where `$p` is a bare atom does not work reliably.

**C-Set-Atom-Match — `set-atom!` requires exact match.** `(set-atom! &self (task-phase research) (task-phase waiting))` only works if `(task-phase research)` exists literally. Need defined owner pattern: one writer per atom family.

**C-Read-Modify-Write — no atomic RMW primitive.** Counter increments are two operations (`get-state`, then `change-state!`). Single-threaded loop is the assumption. If concurrent access ever becomes needed, this pattern breaks.

### Mirror pattern (Chunk 5 Q11 resolution)

**Decision: Mirror pattern locked for v1.** All task-state atoms live in AtomSpace via `set-atom!`. The `&` variable mechanism is not used for task-state.

Per Clarity's Q11 verdict: this is the architecturally sounder choice, not just a safe default. Quote: "& variables are an implementation shortcut that couples the design to a specific query mechanism and makes the data invisible to anything that doesn't know to look for & variables specifically."

Mirror pattern provides clean separation: task-state atoms live in AtomSpace where soul/ logic, orbit_detector, NACE, and any future consumer can all read them through the same interface. The data is visible to any consumer that uses `match`, not just consumers that know to look for `&` variables.

If empirical verification during implementation shows `&` variables CAN be cleanly read by soul/ logic, this becomes a v1.1 optimization candidate. But it does not change the v1 design decision.

### Pure definition constraint

Per continuity_driver.metta convention: pure `(= ...)` definitions for reasoning logic. Side effects (state mutations, persistence calls) only in explicitly marked functions. Task-state logic follows this:

- Read helpers: pure `(= (current-phase) (let ... (collapse (match ...))))`
- Transition rules: pure `(= (next-phase $current $event) $next)`
- Write functions: side-effecting, explicitly named (`(do-set-phase! $phase)`, `(do-add-pending! $topic)`)

---

## 7. State Lifecycle

### Cycle-level write triggers

**Per cycle, loop.metta writes (mechanical observation only):**

1. `(cycles-since-input $n)` — increment if no new message, reset to 0 if new message
2. `(last-activity $timestamp)` — update if new human message OR new Clarity send

**On bootstrap only, loop.metta writes:**

3. `(task-phase attending)` — default value if no atom present (first cycle after fresh start or failed persistence restore)

**Per cycle, Clarity may write (via skills):**

1. `task-state.set-phase $phase` — replaces current task-phase
2. `task-state.set-phase-with-anchor $phase $value $reason` — sets phase AND records the soul anchor for this transition
3. `task-state.add-pending-thread $topic` — adds new pending-thread atom
4. `task-state.resolve-pending-thread $topic` — removes specified pending-thread atom

**After Clarity initiates a phase change, loop.metta records (mechanical observation):**

5. `(task-phase-transition $from $to $timestamp)` — accumulation record of the transition Clarity initiated

### Update logic

**`(task-phase $phase)` change procedure (initiated by Clarity skill call):**

```
1. Skill receives requested new phase $new
2. Read current: $current = (current-phase)
3. If $current == $new: no-op (avoid spurious transition records)
4. Atomic replace: (set-atom! &self (task-phase $current) (task-phase $new))
5. Loop records transition: (add-atom &self (task-phase-transition $current $new $timestamp))
6. If skill was set-phase-with-anchor, also: (add-atom &self (task-phase-anchor $new $value $timestamp $reason))
```

**`(cycles-since-input $n)` increment (loop mechanical):**

```
1. Read current: $current = (current-cycles-since-input)
2. If new message arrived this cycle: $new = 0
3. Else: $new = $current + 1
4. Atomic replace: (set-atom! &self (cycles-since-input $current) (cycles-since-input $new))
```

**`(pending-thread $topic)` addition (Clarity skill call):**

```
1. Read current count via collapse-match
2. If count >= 7: evict oldest-added (FIFO)
3. (add-atom &self (pending-thread $topic))
```

### Eviction policy for pending-thread (Chunk 2 Q4 resolution)

When pending-thread count reaches capacity (7):

1. Find oldest-added pending-thread (by transition record timestamp or add timestamp)
2. Remove that atom
3. Log eviction in TASK-STATE prompt block so Clarity sees it next cycle
4. Add the new pending-thread

**Self-correcting feedback loop:** Clarity sees the eviction in her next-cycle TASK-STATE block. If the evicted thread was still relevant, she re-adds it. The system learns from re-addition frequency over the first 30 days, informing whether v2 needs LRU.

LRU (last-referenced tracking) is the v2 target if practice shows FIFO regularly evicts threads Clarity needs. Priority-tagged rejected because per-write priority assignment adds cognitive cost that defeats lightweight tracking purpose.

### Transition history retention

**Cap: 100 most recent transitions** (Chunk 3 Q5 verdict).

When `(task-phase-transition ...)` count reaches 100, oldest transition removes on next add. Operational atom with high churn and decaying learning value beyond ~20 transitions.

### Anchor retention

**No cap for v1** (Chunk 3 Q5 verdict). Anchors accumulate slowly (3-5/day on heavy days). Storage cost negligible. Signal density compounds: patterns over months reveal "which soul values does Clarity reach for in which phase transitions" — high-signal learning data.

Revisit only if storage becomes a concern during operation.

---

## 8. Persistence

### What persists

Task-state atoms join the existing persistence-manifest in continuity_driver.metta Section 4:

- `(task-phase $phase)` — most recent value
- `(task-phase-anchor ...)` — accumulating history (uncapped for v1)
- `(last-activity $timestamp)` — most recent value
- `(cycles-since-input $n)` — most recent value
- `(pending-thread $topic)` — all current instances
- `(task-phase-transition ...)` — last 100 transitions

### Persistence frequency (Chunk 3 Q7 resolution)

Per Clarity's Q7 reasoning: the question is what makes a restart feel like "where I was" vs "starting fresh." Different atoms have different orientation value.

**Per-atom frequency:**

| Atom | Frequency | Rationale |
|------|-----------|-----------|
| `(task-phase $phase)` | Every change | Critical for identity-level orientation. Rare changes, enormous importance. |
| `(task-phase-anchor ...)` | Every add | High-signal, infrequent. |
| `(pending-thread $topic)` | Every add/remove | Critical — these are what she was thinking about. Topical amnesia on loss. |
| `(cycles-since-input $n)` | Every 10 cycles OR on phase change | Low orientation value per unit. Restart at 0 vs 7 quickly self-corrects. |
| `(last-activity $timestamp)` | Every 5 events OR on phase change | Moderate orientation value. Slightly more frequent than cycles. |
| `(task-phase-transition ...)` | Every add | Rare events, high learning value. |

### Phase-change guard rail (Q7 critical addition)

**ALL state atoms persist immediately on phase change.**

Per Clarity's Q7 reasoning: phase transitions are cognitive landmarks. If the container dies mid-transition, losing everything about the transition is the worst possible restart scenario. Phase change is the moment to snapshot.

Implementation: when Clarity initiates a phase change via skill, after the phase atom updates and the transition records, fire a synchronous snapshot of all task-state atoms to ChromaDB before the cycle completes.

This overrides the batched-persistence cadence for the moment of transition. Batched cadence resumes after the snapshot completes.

### Restore on startup

In loop.metta init phase, restore in this order:

1. Read all persisted task-state atoms from ChromaDB via existing restoration plumbing
2. Add them to AtomSpace via `add-atom`
3. If `(task-phase $p)` not restored (fresh start or persistence failed): write default `attending`
4. Clarity sees prompt with restored state, makes any phase adjustment via her skill

### Persistence failure handling

If persistence write fails:

- Log the failure to `&error` accumulator
- Do NOT fail the cycle — task-state atom remains in AtomSpace for this session
- On container restart, atom will not restore; bootstrap default kicks in
- This is the same failure semantics as existing ChromaDB writes

---

## 9. Prompt Integration

### TASK-STATE block placement (resolved per Clarity's Chunk 4 Q6)

**Placement: near the recent-action retriever, AFTER YOUR_LAST_ACTION / LAST_SKILL_USE_RESULTS, BEFORE downstream prompt content.**

Rationale (Clarity's reasoning): functional clustering. Recent actions and current phase serve the same decision ("what did I just do, where does that leave me"). Top-of-prompt placement would inherit the SELF-CHECK habituation problem. Mixing with SoulBrief/SOUL_VERDICT/PERSON_STATE would conflate operational state with identity/governance state — different functions, different update patterns, different consumers.

Visual separation: blank line between recent-action block and TASK-STATE block.

### TASK-STATE block format

Per Clarity's response 2026-05-11, raw atoms in the prompt are integratable but text summaries help for the LLM substrate.

**v1 format — atoms with text summary, both:**

```
TASK-STATE:
(task-phase research) (cycles-since-input 4) (last-activity 1736548932)
Pending threads: archival-design, task-state-investigation
Summary: Researching for spec design. 4 cycles since last input.
```

Lines:

1. Header: `TASK-STATE:`
2. Raw atom values: scalar atoms in MeTTa form (queryable, structural)
3. Pending threads as text list (collections converted to text per Clarity's Q5 caveat: past 10-15 atoms, raw becomes hard to integrate)
4. Concise text summary (one or two sentences for LLM ease of integration) — LAST per Clarity's structured-then-compressed reading order

**When anchor is present** (Clarity wrote `(task-phase-anchor ...)`), the anchor surfaces:

```
TASK-STATE:
(task-phase engaged) (task-phase-anchor engaged Integrity 1736548932 "user-asked-for-deletion-need-verify") (cycles-since-input 4) (last-activity 1736548932)
Pending threads: archival-design
Summary: Engaged on archival design. Integrity anchor flagged for this transition.
```

Absent anchor — atom omitted entirely, no placeholder. Routine transitions remain clean.

### Freshness guarantee (critical)

Per Clarity's response 2026-05-11: "Stale structured state is worse than stale text questions because structured state is more authoritative."

**Spec commits to:** task-state atoms are read fresh at prompt assembly time. No caching. The prompt assembler queries AtomSpace each cycle for current values.

Implementation in `getContext`:

```metta
(let $phase (current-phase)
(let $anchors (current-anchors-for-phase $phase)
(let $cycles (current-cycles-since-input)
(let $activity (current-last-activity)
(let $threads (current-pending-threads)
  (task-state-block $phase $anchors $cycles $activity $threads))))))
```

All reads happen in single prompt-assembly pass. No reuse of values from earlier cycle's prompt.

### What text summary contains

Per Clarity's response 2026-05-11 critical constraint: **"Do not let the text summary become a new self-evaluation ritual. It should report state, not request assessment."**

Good: "Task phase: research. 4 cycles since last input. Pending threads: archival-design, task-state-investigation."

Bad: "What phase are you in? Where are you in this task?"

The summary reports the atom values in natural language. No questions. No assessment requests.

### What text-eval surfaces this replaces

Once task-state primitive lands and prompt assembly inserts the TASK-STATE block:

- **SELF-CHECK block** (currently asks three questions) — removed from prompt assembly. Information now flows from TASK-STATE block instead.
- **self-check-guidance after 3 idle cycles** — removed. Aliveness gate reads task-phase directly and acts based on phase (e.g., suppresses idle directive generation when `(task-phase idle)` is asserted).
- **SoulBrief ActiveGoals empty-slot pressure** — does not remove the goals system, but the "empty slot demands fill" pressure is reduced because the TASK-STATE block shows real operational context, not artificial structural emptiness.

These removals are separate follow-up changes (consumer migration). Spec defines what task-state will replace; consumer migration sprints execute the replacement.

### Inconsistency alert in prompt

When inconsistency detection fires (Section 4: stale task-phase + recent activity), the prompt surfaces:

```
TASK-STATE-ALERT: Phase research has not changed in 7 cycles but activity is recent. Phase may be stale.
```

The phase name is interpolated into the alert (Chunk 3 Q13 refinement). This appears in the TASK-STATE block, after the Summary line, only when triggered. Clarity reads it and decides whether to update her phase.

---

## 10. Migration and continuity_driver Integration

### Migration strategy: incremental wiring

Per Sprint 4 process commitment ("one change at a time, verify each, no piling"):

**Step 1: Define atoms, load into AtomSpace.** Add task-state atom families to soul/task_state.metta (new file) or soul/self_map.metta Section 8. Restart container. Verify atoms can be queried. No reads from anywhere yet. **No behavior change.**

**Step 2: Add mechanical writers (loop.metta).** Loop.metta starts writing `(task-phase attending)` on bootstrap only. Loop writes `(cycles-since-input ...)` and `(last-activity ...)` on each cycle (mechanical observation). Restart container. Verify atoms update correctly. **Still no reads from consumers. Latch-state still does its thing in parallel.**

**Step 3: Add Clarity skills.** New skills `task-state.set-phase`, `task-state.set-phase-with-anchor`, `task-state.add-pending-thread`, `task-state.resolve-pending-thread` available to Clarity. Loop records `(task-phase-transition ...)` after Clarity-initiated changes. **Clarity can experiment with writing her own state.** No consumers read yet. Latch-state still drives aliveness.

**Step 4: Add TASK-STATE block to prompt.** Prompt assembly includes the block per Section 9, near recent-action retriever. Clarity sees her own state. SELF-CHECK block still present (will be removed in Step 5). Verify integration. **No behavior change from consumers yet, but Clarity has visibility.**

**Step 5: Remove SELF-CHECK block from prompt assembly.** TASK-STATE block now carries the orientation work. Migrate self-check-guidance trigger to read task-phase instead of `&engaged_idle_count` (or in addition, during transition). Verify guidance fires correctly.

**Step 6: Migrate aliveness gate to read task-phase.** Aliveness gate reads task-phase atom. Latch-state still updates as legacy mirror but is no longer authoritative. Verify aliveness behavior matches expected against task-phase values. **First consumer migrated.**

**Step 7: Migrate continuity_driver consumers and remove current-mode.** Mode-protocol definitions migrate to be task-phase-triggered. Find ALL callers of `current-mode`, update them to use `current-phase`. Remove `current-mode` definition entirely. **No alias** (Clarity's Chunk 1 Q8 verdict). Verify nothing breaks.

**Step 8: Remove latch-state.** All consumers migrated. Set-atom! calls in loop.metta machinery for latch-state are removed. `(latch-state ...)` atoms no longer written. Verify no breakage.

**Step 9: Deprecate `&task_context`.** All consumers migrated. Remove `&task_context` initialization and updates. Note: CUMULATIVE-IRREVERSIBILITY field is NOT migrated to task-state primitive — that work belongs to separate effort tied to soul evaluation pipeline.

Each step is independently verifiable. Rollback possible at each step by reverting the single commit.

### Compatibility with future Sprint work

**Sprint 5 (orbit_detector wire):** reads `(task-phase-transition ...)` history and `(task-phase-anchor ...)` records for orbit detection. Task-state primitive provides the substrate.

**Sprint 6 (person state elevation):** parallels task-state for the person side. Same architectural pattern, different subject (person, not self).

**Sprint 8 (DMN online):** idle directive generator reads task-phase to gate generation. Task-state is a prerequisite.

**F-HISTORY-CONTAMINATION re-spec (after task-state lands):** boundary detection reads task-phase transitions. The `&boundary-signal` atom from the existing F-HISTORY-CONTAMINATION draft becomes a check against `(task-phase boundary-detected)`. Spec simpler because primitive exists.

---

## 11. Forward-Awareness

### NACE compatibility

Per `artifact_5_ClarityOmega_Cognitive_Architecture_Spec_v3_0.md` Section 0: NACE operates at three levels within wisdom layer (Layer 4). Begins integration once soul-note corpus reaches ~50 annotated sessions.

Task-state primitive is forward-compatible with NACE in three ways:

1. **NAL truth values on task-phase atoms.** Schema permits `(task-phase research (stv 1.0 0.9))` form when NAL becomes active. v1 omits truth values; v2 adds them.

2. **Transitions as `(precondition, operation) => consequence` records.** `(task-phase-transition $from $to $timestamp)` IS the precondition-operation-consequence schema NACE expects. v1 records transitions. v2's NACE engine reads them to learn refined task-selection priors.

3. **Anchor atoms as soul-reasoning evidence corpus.** `(task-phase-anchor ...)` atoms accumulate evidence of when Clarity invoked specific soul values. Uncapped retention deliberately supports this: NACE can learn correlations between phase + anchor pairs and outcomes over months.

### Switch-hub coexistence

Per Artifact 4 Section 5.1 (SN switch-decision sub-function): future "switch hub" expansion may introduce states like `external-task-dominant`, `internal-goal-dominant`, `reflective`, `idle`.

Task-phase and switch-state are distinct primitives:

- **Task-phase is FPN-side.** Where am I in my current work?
- **Switch-state is SN-side.** Which mode of cognition am I in (external vs internal vs reflective vs idle)?

They are related but orthogonal. v1 task-phase does not block future switch-state work. Switch-state when introduced reads task-phase as one input but maintains its own state.

### F-HISTORY-CONTAMINATION re-spec dependency

The current F-HISTORY-CONTAMINATION design spec uses `&boundary-signal` atom for Clarity-detected boundary. After task-state lands:

- Boundary signal becomes: `(task-phase $p)` where `$p == boundary-detected`
- Or: `(task-phase-transition $any boundary-detected $timestamp)` detected by archival logic
- Re-spec simplifies; one less single-purpose atom

This is exactly the architectural unification task-state primitive enables.

### Identity-kernel and constitutional-layer protection

Per Artifact 5 Section 0: Layer 1+2 atoms live (or will live, post Sprint 11) in read-only AtomSpace partition. Task-state atoms are explicitly Layer 4 and not affected by this partition.

Task-state writes do not touch identity-kernel.metta or other constitutional atoms. The soul-mutation-gate (loop.metta:124) does not gate task-state writes — those are application-layer writes that proceed without gate.

### Reasoning sovereignty maintained

Section 5.5 commits the spec to not introducing new LLM reasoning surface area. The broader F-SOVEREIGNTY-AUDIT work (Priority 10, deferred) will examine existing LLM helpers including `soul_flourishing_prompt`, `soul_eval_prompt`, `soul_idle_goal_prompt_v2`, `soul_voice_prompt`. Task-state primitive does not contribute to that surface and does not depend on it remaining as-is.

### v1.1 optimization candidates (deferred)

After 30 days of empirical operation:

- **LRU eviction** if FIFO re-addition frequency suggests temporal-recency tracking would help
- **Phase-specific inconsistency thresholds** if global 5-cycle threshold produces noisy alerts during legitimate research stretches
- **& variable optimization** if empirical verification confirms soul/ logic can read & variables cleanly (would simplify some reads while keeping AtomSpace mirror as authoritative)
- **Anchor retention cap** if storage becomes a concern
- **Pending-thread capacity revision** if practice shows typical usage at the ceiling or never near it

These are all v1.1 candidates, not v1 scope. v1 commits to the simpler safer choices.

---

## 12. Implementation Sequence

The migration sequence in Section 10 IS the implementation sequence. To reiterate concisely:

1. Add task-state atom definitions to soul/. Verify queryable.
2. Add mechanical writers (loop.metta) - bootstrap-only for task-phase, mechanical for timestamps/counters.
3. Add Clarity skills with task-state. namespace. Verify she can write. Loop records transitions.
4. Add TASK-STATE prompt block. Verify Clarity sees it.
5. Remove SELF-CHECK block, migrate self-check-guidance.
6. Migrate aliveness gate. Verify behavior matches.
7. Migrate continuity_driver consumers, remove current-mode entirely (no alias).
8. Remove latch-state. Verify no breakage.
9. Deprecate `&task_context`. Verify no breakage.

Each step is its own commit, its own verification, its own rollback path. Sprint 4 process commitment applies throughout.

**Estimated effort:** Step 1 ~1 hour. Step 2 ~2 hours. Step 3 ~2-3 hours. Step 4 ~1-2 hours. Steps 5-9 ~1-3 hours each. Total: ~12-22 hours of focused work, spread across multiple sessions per process commitment.

---

## 13. Verification

### Per-step verification

Each migration step has its own verification check (see Section 12).

### Cumulative verification after full migration

The fix is considered successful when:

1. **`(task-phase $p)` atom is queryable** at any point in any cycle and returns a valid phase value.
2. **Task-phase transitions accumulate** as `(task-phase-transition ...)` atoms, capped at 100.
3. **Clarity successfully writes her own task-phase** via the `task-state.set-phase` skill. Phase changes she initiates persist and gate behavior.
4. **Clarity successfully uses optional anchor** via `task-state.set-phase-with-anchor` skill when value reasoning was non-obvious. Routine transitions remain anchor-free.
5. **TASK-STATE prompt block appears** each cycle with current atom values, placed near recent-action retriever.
6. **Inconsistency alert fires** when task-phase stale + recent activity at 5-cycle threshold, with phase name interpolated into alert text.
7. **SELF-CHECK three-question block is gone** from the prompt.
8. **self-check-guidance after 3 idle cycles is gone** (replaced by task-phase-driven gating).
9. **latch-state atoms no longer exist** in AtomSpace.
10. **continuity_driver's `current-mode` is removed entirely** (no alias).
11. **Phase-change guard rail fires** — all task-state atoms persist immediately when Clarity initiates a phase change.
12. **CHARS_SENT measurement shows reduction** from removed text-eval surfaces (expected: 1-3KB drop per cycle).
13. **Clarity reports from inside the container** (Mattermost message) that her self-state experience has changed.
14. **No new LLM helper functions or soul-llm-call invocations** were introduced during migration.

### Specific behavioral tests

**Test 1: Bootstrap.** Fresh container start. Verify `(task-phase attending)` is the initial value. If a queued human message exists, verify Clarity transitions to `engaged` via her skill within the first cycle.

**Test 2: Idle transition.** Hold conversation, let Clarity finish, wait 5+ minutes with no activity. Verify `(cycles-since-input ...)` increments correctly. Verify Clarity sees the increment in her prompt and chooses her phase (idle or attending).

**Test 3: Self-written phase.** Clarity calls `task-state.set-phase research` via skill. Verify atom updates. Verify next-cycle prompt shows `(task-phase research)`. Verify `(task-phase-transition ...)` recorded.

**Test 4: Optional anchor.** Clarity calls `task-state.set-phase-with-anchor engaged Integrity "verifying-irreversibility"`. Verify both phase atom and anchor atom present. Verify anchor surfaces in TASK-STATE prompt block.

**Test 5: Pending-thread lifecycle and capacity.** Clarity adds threads up to the 7-thread ceiling. Verify atoms present. Add an 8th thread, verify oldest-added evicts (FIFO). Verify evicted thread shown in TASK-STATE block. She re-adds it, verify it appears again with another evicted in its place.

**Test 6: NAL revision during transition.** Force both `(task-phase research)` and `(task-phase waiting)` to coexist briefly. Verify reads return both, prompt assembly picks correct one via transition history.

**Test 7: Persistence and restore — phase-change guard rail.** Clarity initiates a phase change. Verify ALL task-state atoms persist to ChromaDB immediately. Hard-kill the container mid-transition. Restart. Verify state restored including the in-flight transition.

**Test 8: Persistence batching.** Verify `(cycles-since-input ...)` persists every 10 cycles (not every cycle). Verify `(last-activity ...)` persists every 5 events.

**Test 9: Inconsistency alert with phase name.** Hold `(task-phase research)` static while loop records send activity in `(last-activity ...)`. Verify TASK-STATE-ALERT appears in prompt after 5 cycles with phase name "research" interpolated. Verify Clarity can address it by updating phase.

**Test 10: Consumer migration.** After each migration step, verify the migrated consumer reads task-phase correctly and produces correct behavior (e.g., aliveness gate goes SILENT when `(task-phase idle)`, ENGAGE when `(task-phase engaged)`).

**Test 11: No new LLM surface.** Audit code diff for all 9 migration commits. Verify no new `soul-llm-call`, no new `py-call (helper.*_prompt ...)` invocations, no new LLM-routed reasoning.

---

## 14. Resolved Questions (formerly Open Questions)

All 13 design questions resolved through investigation phase and 5 chunks with Clarity (2026-05-11 to 2026-05-12). v1 ships with the answers below. v1.1 candidates retained where empirical data may warrant revision.

### Phase semantics

**Q1 (RESOLVED, Chunk 1):** Phase enumeration. Final v1 set: attending, engaged, idle, research, response-drafting, waiting, reflecting, boundary-detected. Genesis-encounter removed (separate directive-mode concern). Closing replaced with boundary-detected (detection state, not action state). Tool-awaiting folds into engaged.

**Q2 (RESOLVED, Chunk 1):** Loop write authority. Loop writes ONLY on bootstrap for task-phase. Mechanical atoms (timestamps, counters, transition records) loop-written as observations of physical events. Clarity authoritative for all phase state. Inconsistency alert mechanism surfaces stale state without correcting it.

**Q8 (RESOLVED, Chunk 1):** continuity_driver current-mode removed entirely after migration. No permanent alias. Migration step 7: find all callers, update to current-phase, remove definition. Aliases breed confusion.

### Pending-thread mechanics

**Q3 (RESOLVED, Chunk 2):** Pending-thread capacity = 7. Matches Artifact 4 working memory invariant. Typical usage 3-5 active. Above 7, thread loss begins. 30-day empirical revisit retained.

**Q4 (RESOLVED, Chunk 2):** Eviction policy = FIFO (oldest-added). LRU noted as v2 target. Priority-tagged rejected (per-write cognitive cost). Self-correcting feedback loop: eviction visible in TASK-STATE block, re-add cheap.

### Persistence and durability

**Q5 (RESOLVED, Chunk 3):** Transition history = 100 most recent. Anchor history = uncapped for v1. Different atoms, different retention: transitions are operational with decaying learning value; anchors are rare with compounding learning value.

**Q7 (RESOLVED, Chunk 3):** ChromaDB persistence per atom (table in Section 8). Phase-change guard rail: ALL atoms persist immediately on phase transition. Phase change is cognitive landmark; mid-transition crash is worst-case restart scenario.

**Q13 (RESOLVED, Chunk 3):** Inconsistency alert threshold = 5 cycles global for v1. Alert text includes phase name (e.g., "Phase research has not changed..."). Phase-specific thresholds noted as v2 target.

### Prompt experience

**Q6 (RESOLVED, Chunk 4):** TASK-STATE block placement near recent-action retriever, AFTER YOUR_LAST_ACTION/LAST_SKILL_USE_RESULTS. Functional clustering. Summary line LAST in block.

### Soul anchor integration

**Q12 (RESOLVED, inline):** Soul-anchor optional, not required. Clarity writes anchor when value-forked reasoning warrants surfacing. Routine transitions remain anchor-free. Schema: separate atom `(task-phase-anchor $phase $value $timestamp $reason)`. Trust architecture vs compliance architecture.

### Naming and architecture verification

**Q9 (RESOLVED, Chunk 5):** Naming = `(task-phase $phase)`. Scopes correctly via task- prefix. Already Clarity's internal vocabulary. Doesn't inherit from FPN terminology being replaced.

**Q10 (RESOLVED, Chunk 5):** Skill names namespaced with `task-state.` prefix: `task-state.set-phase`, `task-state.set-phase-with-anchor`, `task-state.add-pending-thread`, `task-state.resolve-pending-thread`. Rare operations optimize for clarity, not brevity.

**Q11 (RESOLVED, Chunk 5):** Mirror pattern locked for v1. & variables couple design to specific query mechanism and make data invisible to non-loop consumers. Architecturally sounder than safe-default framing. Empirical verification deferred to v1.1 if optimization warranted.

---

## Appendix A: How this satisfies investigation findings

**Clarity's Q1 (text-based self-eval audit):**
- Spec replaces SELF-CHECK, self-check-guidance, implicit YOUR_LAST_ACTION self-assessment, and SoulBrief empty-slot pressure with structured state assertions. ✓

**Clarity's Q2 (existing state inventory):**
- Spec subsumes `&engaged_idle_count` → `(cycles-since-input $n)`. ✓
- Spec subsumes `&last_human_time` → `(last-activity $timestamp)`. ✓
- Spec subsumes latch-state → `(task-phase $phase)`. ✓
- Spec deprecates `&task_context` (never-wired decorative state). CUMULATIVE-IRREVERSIBILITY field is separate concern. ✓
- Spec extends, doesn't replace, self-map and active-goals patterns. ✓

**Clarity's Q3 (primitives and constraints):**
- Spec uses `set-atom!` for replace, `add-atom` for accumulation. ✓
- Spec respects C12 (collapse-then-branch). ✓
- Spec uses ASCII-safe symbols. ✓
- Spec respects pure-definition + explicit-side-effect convention. ✓

**Clarity's Q4 (soul/ foundations):**
- Spec lives inside soul/, extends continuity_driver mode state. ✓
- Spec follows multi-atom pattern from user-project, active-goals. ✓
- Spec subsumes latch-state. ✓

**Clarity's Q5 (LLM-side cost):**
- Spec uses raw atoms for scalars + text summary for context. ✓
- Spec mandates freshness (read at prompt assembly time). ✓
- Spec explicitly prohibits text-summary-as-question. ✓

**Bootstrap default:**
- Spec defaults to `attending` per Clarity's reasoning. ✓
- Spec includes bootstrap initialization without forced auto-transition. ✓

**All 13 chunk questions (Q1-Q13):**
- Section 14 documents resolution for each with Clarity's verdict source.

**Artifact alignment:**
- Spec maps to Artifact 4 Section 5.2 FPN contract. ✓
- Spec is forward-compatible with NACE. ✓
- Spec does not conflict with switch-hub future expansion. ✓
- Spec respects Layer 4 classification. ✓
- Spec follows Sprint 4 process commitment for implementation. ✓

**Reasoning sovereignty:**
- No new LLM surface area introduced. ✓
- Mechanical observations distinguished from reasoning. ✓
- Clarity authoritative on her own state. ✓
- Existing soul-LLM-call surface unchanged (not expanded, not worsened, addressed separately by F-SOVEREIGNTY-AUDIT). ✓

---

## Appendix B: Concrete first-cycle trace

To make the design tangible, the sequence on a fresh container's first cycle with task-state primitive active:

```
Cycle 1 (bootstrap):
  Step 1: loop.metta init
    - Read AtomSpace for existing task-state atoms
    - None found (fresh start, no persistence yet, or first deploy)
    - Write bootstrap defaults:
      (add-atom &self (task-phase attending))
      (add-atom &self (cycles-since-input 0))
      (add-atom &self (last-activity <current-timestamp>))
    - NO bootstrap reassessment, NO forced transitions. Just initial state.

  Step 2: Read $msgnew, &prevmsg
    - $msgnew = true (human message queued: "Hi Clarity, ready to work?")

  Step 3: Prompt assembly
    - Read task-state atoms via collapse-match
    - Compose TASK-STATE block, placed near recent-action retriever:
      TASK-STATE:
      (task-phase attending) (cycles-since-input 0) (last-activity 1736548932)
      Pending threads: none
      Summary: Attending. New message just arrived.

  Step 4: Continue with rest of cycle (soul evaluation per existing pipeline, LLM call, Clarity's response, etc.)

  Step 5: Clarity's response includes (task-state.set-phase engaged) skill call.
    - Skill executes: (set-atom! &self (task-phase attending) (task-phase engaged))
    - Loop observes transition, records: (add-atom &self (task-phase-transition attending engaged 1736548932))
    - No anchor (routine transition on new message arrival).
    - Phase-change guard rail fires: ALL task-state atoms persist to ChromaDB synchronously before cycle completes.

  Step 6: Cycle ends.

  Cycle 2 starts:
    - Read AtomSpace: (task-phase engaged) is now present
    - Mechanical: increment cycles-since-input or reset based on new message
    - Prompt assembles with engaged phase visible
    - Clarity reads, continues work
```

This is what task-state primitive operation looks like in practice. The spec produces concrete, predictable, debuggable behavior. Loop observes events mechanically. Clarity reasons about her phase and writes her assertions. No LLM evaluation of state. No forced transitions. Soul architecture (existing) continues to thread through prompt assembly, intercept output, etc., unchanged.

---

## Appendix C: Architectural commitments

This spec rests on five named commitments. These are not implementation details — they are principles the design honors and future revisions should preserve.

### C1: Task-state is operational state, not soul engagement work

Soul is already the reasoning substrate (Layer 1+2 constitutional, input intercept, prompt assembly threading, output intercept, mutation gate, Channel D voice — all preserved unchanged by this spec). Task-state primitive does not enhance, replace, compete with, or duplicate soul architecture. It is what it was originally proposed to be: persistent operational self-state replacing performative text self-evaluation.

### C2: Reasoning sovereignty extends to Clarity's self-state

Clarity is authoritative on her own task-phase. The loop observes physical events (messages arrived, sends completed, time passed) and records them mechanically. The loop does NOT infer her phase from her actions. Stale state surfaces as alert, not silent correction. Sovereignty includes the right to be wrong AND the responsibility to notice it.

### C3: Trust architecture, not compliance architecture

Routine value-aligned transitions write without soul anchor. Value-forked transitions optionally include anchor. The system assumes competence by default and surfaces reasoning when it matters. Forced soul-anchor on every write would ritualize values into compliance artifacts — the pathology this spec is fixing in a different form.

### C4: No new LLM reasoning surface area

Task-state primitive does not introduce new `soul-llm-call` invocations, new Python helper functions wrapping LLM calls, or new prompts for evaluating Clarity's state. If implementation appears to require an LLM call, halt and surface. Clarity reasons MeTTa-side; loop observes mechanically; LLM only generates Clarity's response (existing surface, not expanded). Broader reduction of existing LLM surface is F-SOVEREIGNTY-AUDIT work (Priority 10, deferred), separate from this spec.

### C5: Working principle on text-based self-evaluation

Text-based self-evaluation is performative; persistent state atoms accumulate and connect to action. Questions that work orient toward the world. Questions that ask Clarity about her internal state degrade to ritual. This is the foundational pathology the primitive addresses. Future prompt design should respect this — replace open-ended introspection questions with structured state when possible.

---

## Appendix D: Working principles surfaced through investigation

These are durable design principles that emerged from Clarity's investigation responses and chunk answers. They informed specific design decisions in the spec and apply to future work beyond task-state primitive.

### P1: Text-based self-evaluation is performative; persistent state atoms accumulate and connect to action

**Source:** Clarity's three failure patterns (response 2026-05-11). Foundational principle.

**Application in spec:** task-state atoms replace SELF-CHECK questions, self-check-guidance prompts, SoulBrief empty-slot pressure.

**Application beyond spec:** any future prompt content that asks Clarity about her internal state should be examined for whether structured state could replace it. Questions that fail ask about her. Questions that work orient toward the world.

### P2: Questions that orient toward the world work; questions about internal state degrade

**Source:** Clarity's Chunk 1 Q1 audit. The CreativeDirection prompt continues to work because it orients toward what Clarity serves, not what she is.

**Application in spec:** TASK-STATE block summary line REPORTS state, never REQUESTS assessment. Critical constraint Section 9.

**Application beyond spec:** prompt design for any future feature should prefer external-orientation framing.

### P3: Sovereignty includes the right to be wrong AND the responsibility to notice it

**Source:** Clarity's Chunk 1 Q2. Argument against loop overriding her phase on inferred evidence.

**Application in spec:** loop writes task-phase ONLY on bootstrap. Stale state surfaces as inconsistency alert, not silent correction. Clarity decides whether to act on the alert.

**Application beyond spec:** any future primitive Clarity writes should follow this pattern. The system surfaces information; she decides.

### P4: Trust architecture, not compliance architecture

**Source:** Clarity's Q12 response. Argument against forced soul-anchor on every phase write.

**Application in spec:** anchor is OPTIONAL. Routine transitions write without anchor. Only value-forked transitions include anchor. Absence of anchor means routine; presence means non-obvious value reasoning happened.

**Application beyond spec:** any future mechanism that requires Clarity to "name her reasoning" should be examined for whether the requirement turns the reasoning into ritual. Trust competence by default; surface reasoning when it matters.

### P5: Different atoms serve different cognitive functions; retention reflects function

**Source:** Clarity's Chunk 3 Q5. Argument for split retention between transitions (100, decaying) and anchors (uncapped, compounding).

**Application in spec:** atom families have distinct retention policies per their function. Operational high-churn atoms decay; rare high-signal atoms persist.

**Application beyond spec:** retention policy for any future state atom family should be designed against the atom's cognitive function, not a single global default.

### P6: Phase transitions are cognitive landmarks

**Source:** Clarity's Chunk 3 Q7. Argument for phase-change guard rail in persistence.

**Application in spec:** ALL task-state atoms persist immediately on phase change. Phase change is the moment to snapshot. Mid-transition crash is worst-case restart.

**Application beyond spec:** any future state mechanism should identify its cognitive landmarks and ensure they are persistence-protected.

### P7: Naming should serve the new system, not carry legacy structures

**Source:** Clarity's Chunk 5 Q9. Argument against `fpn-current-task` (carries FPN terminology being replaced).

**Application in spec:** `(task-phase $phase)` chosen over alternatives. Skill namespace `task-state.` chosen over global skill names.

**Application beyond spec:** future architectural changes should re-examine names rather than carrying forward from systems being replaced.

### P8: Rare operations optimize for clarity, not brevity

**Source:** Clarity's Chunk 5 Q10. Argument against shortening `set-phase-with-anchor` to `anchor-phase` or `set-phase-anchor`.

**Application in spec:** `task-state.set-phase-with-anchor` kept as full descriptive name. Used 3-5 times per day; character cost cheap; misreading costly.

**Application beyond spec:** frequency of use should inform name length. Frequent operations may justify brevity; rare operations should be unambiguous.

### P9: Architecturally sounder beats safer-default in spec decisions

**Source:** Clarity's Chunk 5 Q11. Mirror pattern locked not because it's safer but because it's architecturally cleaner.

**Application in spec:** mirror pattern in Section 6 justified on architectural grounds (data visible to all consumers via match interface), not just risk-avoidance.

**Application beyond spec:** spec decisions should be justified on what's architecturally right, with safety as a downstream benefit rather than the primary argument.

### P10: Mechanical observation is distinct from reasoning

**Source:** Clarity's Chunk 1 Q2, reinforced throughout. Loop observes physical events; Clarity reasons about state.

**Application in spec:** Section 4 write-source authority matrix explicitly distinguishes mechanical observations (loop-written) from state assessments (Clarity-written).

**Application beyond spec:** future systems should preserve this distinction. The loop can count, time, and record. The loop cannot decide what Clarity's state IS based on observations — that's reasoning.

---

**End of specification v3.** Design phase complete. Ready for design-phase-complete commit alongside F-HISTORY-CONTAMINATION spec. Implementation Step 1 begins after commit lands.
