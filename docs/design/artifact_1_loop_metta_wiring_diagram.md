# loop.metta Wiring Diagram

**Version:** v1.4 (June 10, 2026; v1.3 June 4, 2026; v1.2 May 1, 2026; v1 Phase 1 April 30, 2026; v1.1 added NETWORK-RELEVANT flags)
**Author:** Berton Bennett with Claude
**Purpose:** Comprehensive map of what loop.metta is actually doing at runtime, what state it touches, what it calls, and what fires through what dependencies. This document is the foundation for thinking strategically about changes to ClarityOmega's per-iteration flow without producing spaghetti.

**v1.2 changes:** Corrected the run.metta description to reflect the migration design (clones from Berton-C/ClarityOmega fork at Docker build time, not from upstream at runtime startup). Added iteration-dilation flag to lines 61-62 and to the &loops state variable, marking the hardcoded iteration constants as Layer 4 elevation targets per spec_v3.0 Section 0. Added Layer 1+2 immutability note to soul/identity_kernel description per spec_v3.0's constitutional/wisdom layer architecture.

---

## Section 1: Overview and reading guide

### What this document is

A wiring diagram of the per-iteration execution flow in `loop.metta`, with full traceability into the helpers (`helper.py`), soul atoms (`soul/`), and reasoning libraries (`lib_clarity_reasoning/`) that loop.metta calls.

### What this document is NOT

This is not a spec. It does not say what loop.metta should do. It documents what it DOES do, as observed in the source code as of April 30, 2026.

This is also not a complete document. It is Phase 1 of a two-phase effort. Sections marked with **[gap flag]** indicate areas where dependent files have not yet been read in detail and the documentation is necessarily structural rather than complete. A Phase 2 document would close these flags by reading the flagged files. The goal of Phase 1 is a useful working reference where every gap is visibly named rather than hidden.

### How to use it

Three primary use cases:

**Planning a change.** Before editing loop.metta, find the section that documents the affected line. Read what reads from / writes to / calls through that point. The "Hooks and piggybacks" callouts identify lines that do multiple things - these are danger zones. The "Insertion points" callouts identify lines that are clean places to add new behavior.

**Debugging an unexpected behavior.** When Clarity does something puzzling, find the relevant phase of the per-iteration flow and trace what actually fires. The Active vs Dormant section in particular catches "I thought X was running but actually Y was."

**Designing the next architectural move.** Section 9 (External dependency map) shows what loop.metta hard-depends on. The denser the dependency at any point, the more carefully a change needs to be designed.

### Active vs Dormant

A theme that runs throughout this document. The codebase contains substantial sophistication that is loaded into AtomSpace at startup but not necessarily called from loop.metta's per-iteration flow. Some of this is intentional (atoms available for query when needed); some is dormant code from earlier architecture iterations that is no longer hot. This document distinguishes between:

- **HOT:** Called or matched on every per-iteration cycle
- **WARM:** Called conditionally (on new message, on idle threshold)
- **COLD:** Loaded into AtomSpace but not currently called from loop.metta
- **DORMANT:** Loaded into AtomSpace, evidently from an earlier iteration of the architecture, no longer matching current calling conventions

This distinction matters for elevation decisions. A COLD atom may be a candidate for activation. A DORMANT atom is a candidate for either activation (after revisiting its design) or removal.

### Flag types used throughout

The document uses five callout flags to surface decision-relevant information:

**🔧 ELEVATION FLAG** - marks a place where a Python helper or LLM call is doing reasoning that a MeTTa atom could do, OR where a MeTTa atom is loaded but not wired in. Each flag names what the elevation would replace, where the replacement lives (or where it would need to be created), and estimated effort. These are the highest-value targets for reasoning sovereignty work.

**📍 METTA-CALL POINT** - marks every line where loop.metta calls into MeTTa substrate (match, set-atom!, get-state on atom, semantic transition function, etc.). These are the points where additional MeTTa reasoning could be inserted without touching helper.py. The denser the MeTTa-call points in a section, the more "substrate-fluent" that section already is.

**⚠️ DANGER ZONE** - marks places where one line is doing multiple things, or where changes would propagate widely. These need careful refactoring before extension. Often correlates with hooks/piggybacks.

**💡 INSERTION POINT** - marks clean places to add new behavior with low risk. Single-purpose lines, well-bounded effects, no piggyback issues.

**🧠 NETWORK-RELEVANT** - marks the line's network ownership in the triple-network architecture (per Artifact 4). Tags are SN (Salience Network), FPN (Frontoparietal Control Network), DMN (Default Mode Network), or SWITCH-HUB. Some lines belong to coupling between networks and are tagged with both networks (e.g., SN→FPN). Lines tagged COLD-NETWORK indicate where a network's substrate atoms are loaded but not yet wired into the per-iteration flow. This flag is the bridge between the wiring diagram (what is) and Artifact 4 (what should be), making the network architecture legible at every line of loop.metta.

### Why these flags matter for navigation

The flags are not decorative. Each one answers a different question that you would otherwise have to reconstruct from scratch every time you sit down with the codebase:

- 📍 answers "is this MeTTa or Python?" - useful for knowing where elevation work targets live
- 🔧 answers "where can I get the most leverage from a small change?" - useful for prioritizing
- ⚠️ answers "what will break if I touch this?" - useful for pre-flight planning
- 💡 answers "where can I safely add new behavior?" - useful for designing extensions
- 🧠 answers "which cognitive function does this serve?" - useful for thinking architecturally rather than line-by-line

Together they turn description into action guidance.

---

## Section 2: State variables

ClarityOmega maintains state across iterations through three mechanisms: state variables (managed via `change-state!` and `get-state`), latch atoms (managed via `set-atom!` and `match`), and ChromaDB persistence (via Python helpers). This section catalogs the state variables managed by loop.metta itself.

### State variables initialized in loop.metta

All initialized in `initLoop` (lines 17-32) at function call time. The function is called from `omegaclaw` at startup.

| Variable | Initial value | Purpose | Read at | Written at |
|----------|---------------|---------|---------|------------|
| `&prevmsg` | `""` | Last message received from human channel | Line 65, line 67 | Line 66 |
| `&lastresults` | `""` | Last command execution results, fed back into next iteration's prompt | Line 45 (via getContext → LAST_SKILL_USE_RESULTS) | Line 165 |
| `&error` | `()` | Error state for parse failures | Line 49, line 121 | Line 49 (sets new error), line 121 (clears) |
| `&soul_verdict_in` | `"VERDICT: PROCEED"` | Soul evaluation verdict on incoming message | Line 87, line 148, line 151 | Line 87, line 156 |
| `&soul_verdict_out` | `"VERDICT: PROCEED"` | Soul evaluation verdict on outgoing commands (currently STUB - hardcoded) | Line 126 | Line 126 (assigned but not from substantive evaluation) |
| `&person_state` | `"PERSON-STATE: neutral ACTIVE-NEED: none SOUL-TONE: grounded"` | Detected human emotional/intent state | Line 80, line 108 | Line 81 |
| `&task_context` | `"TASK-STATUS: none TASK-ID: none CUMULATIVE-IRREVERSIBILITY: 0"` | Current task tracking | [gap flag: searched but no match - may be unused?] | [gap flag: same] |
| `&soul_mutation_lock` | `""` | Two-phase commit lock for soul-namespace mutations | Line 131 (read by gate) | Lock managed by Python helper; former line 137 commented-out MeTTa write removed |
| `&pending_soul_mutation` | `""` | Pending mutation awaiting confirmation | [gap flag: not seen written elsewhere] | [gap flag: same] |
| `&last_human_time` | `0` | Timestamp of last human message, used for idle threshold | Line 99 (computes idle) | Line 74 |
| `&engaged_idle_count` | `0` | Counter for engaged-idle iterations, drives self-check | Line 101 (self-check consumer retired) | Line 101 |
| `&loops` | `(maxNewInputLoops)` | Iteration counter for run cycle. **Currently hardcoded; target architecture per spec_v3.0 Section 0 reads `(switch-iteration-budget ...)` from SWITCH-HUB substrate.** | Line 55, line 61 | Line 55, line 61, line 157 |
| `&nextWakeAt` | (set on first iteration) | Next idle wake timestamp | Line 166 | Line 72 |

### State variables NOT in loop.metta but referenced

These are state variables read by helpers or soul atoms but not directly initialized in loop.metta. They live in soul/ files or get initialized at import time.

| Atom shape | Initialization | Used by |
|------------|----------------|---------|
| `(latch-state IDLE)` | `soul/latch/aliveness_state_machine.metta` line 16 (`!(add-atom &self (latch-state IDLE))`) | Loop.metta line 95 (raw transition), line 100, aliveness_gate match |
| `(active-goal $n)` | `soul/active_goals.metta` (defines goals 1-15, all currently status=complete) | Loop.metta line 96, get_soul_brief brief-active-goals |
| `(self-map-gap $name)` | `soul/self_map.metta` (defines ~9 gaps, mostly resolved) | Loop.metta line 97, brief-high-gaps |
| `(creative-fuel $type)` | `soul/creative_fuel.metta` (9 flourishings) | Loop.metta line 98, brief-creative-direction |

**Note on the "all goals complete" state:** Active-goals 1-15 are historical record of completed work, intentionally parked for potential future use. This is not a degradation. When 2h thread state comes online, Clarity's own goal generation will populate active goals dynamically.

### Hooks and piggybacks: state variables

**Line 93 piggyback (helper.soul_service_learning):** Fires on every new message, writes to ChromaDB. This is a per-message side effect that is invisible from the loop.metta surface - the line just looks like a logging hook but it's actually a learning-and-persistence operation.

**Line 94 piggyback (helper.soul_user_context_save):** Same shape, also fires on every new message, also writes to ChromaDB. Two ChromaDB writes per human message, sequential.

**Line 95 piggyback (latch transition):** A single line `(set-atom! &self (latch-state IDLE) (latch-state ENGAGED))` does the transition. Note that this is the RAW transition - bypassing the guarded `engage-from-idle` function defined in `soul/latch/aliveness_state_machine.metta`. Loop.metta uses raw transitions, Clarity (in her response batches) uses guarded transitions. This is a structural inconsistency worth flagging.

---

## Section 3: Startup sequence

### File: run.metta

```metta
!(import! &self (library lib_import))
!(git-import! "https://github.com/asi-alliance/omegaClaw-Core.git")
!(import! &self (library omegaclaw lib_omegaclaw))
!(omegaclaw)
```

Four operations:

1. **lib_import** - Patrick foundation library for the import system itself
2. **git-import** - Per the migration design, the working code lives in `/PeTTa/repos/omegaclaw/` cloned from `https://github.com/Berton-C/ClarityOmega` (private fork) at Docker build time, NOT at runtime. The `git-import!` line in the displayed run.metta above is the upstream-template version; the actual runtime should pull from the Berton-C fork. **[verification needed: confirm whether run.metta was edited to point at the fork, or whether the Dockerfile-time clone supersedes the runtime git-import call entirely]**. Either way, local commits to the Berton-C/ClarityOmega repo become the source of truth on the next docker build, not on every container startup.
3. **lib_omegaclaw** - The master library import (see below)
4. **(omegaclaw)** - Calls the main loop function defined in `src/loop`

### File: lib_omegaclaw.metta (the master import chain)

In execution order:

**Patrick foundations (preserved as-is for upstream merge cleanliness):**
- lib_patrick, lib_llm, lib_vector, lib_combinatorics
- lib_nal (Patrick's NAL inference)
- lib_llm_ext.py (LLM client wrappers)
- src/helper.py (the Python bridge - Patrick functions and Berton additions both live here, with intended boundary)
- src/agentverse.py (Patrick multi-agent)
- channels/{irc, mattermost, websearch}.py (Patrick channel implementations, mattermost is the active one)
- src/{utils, channels, skills, memory} (Patrick infrastructure)

**=== END PATRICK BOUNDARY ===**

**Berton soul foundation (three files at the top level):**
- soul/soul_kernel
- soul/soul_utils
- soul/soul_memory

**Berton reasoning extensions (master hub - imports ~30 more soul files):**
- lib_clarity_reasoning/lib_clarity_reasoning (see Section 9 for full list)

**Loop and supporting infrastructure:**
- src/channels (re-import - possibly redundant with line 13)
- src/context
- src/loop (the main loop being documented)

**ChromaDB integration (git-imported):**
- petta_lib_chromadb (Patrick's ChromaDB integration, git-pulled)

### Hook and piggyback callout: lib_omegaclaw

The placement of soul_kernel, soul_utils, soul_memory at lib_omegaclaw level (before lib_clarity_reasoning) means these three are tighter to Patrick's foundation than the rest of the soul/ tree. They run BEFORE the master extensions hub fires.

The architecture-relevant implication: any soul/ atom that the three foundation files depend on must either be in lib_omegaclaw before them, or self-contained within their own files. They cannot depend on anything imported through lib_clarity_reasoning. Worth verifying when next touching those files.

### File: lib_clarity_reasoning/lib_clarity_reasoning.metta

Imports in execution order:

**Reasoning libraries:**
- lib_quantale
- lib_self_continuity (validated end-to-end today)
- substrate_kb (262+ NAL inference atoms)

**Continuity of mind:**
- soul/self_map (landscape)
- soul/creative_fuel (flourishing positive polarity)
- soul/goal_generator (gap × fuel → goal candidates)
- soul/active_goals (current goal state, all status=complete currently)
- soul/continuity_driver (genesis-engine load-probe redirected to the surviving paraconsistency-test symbol per Surface 6, 2026-06-09) [gap flag: full read pending]
- soul/genesis_engine (cross-domain encounters, mostly historical record)

**Identity and seeds:**
- soul/identity_kernel: IMPORT REMOVED and file ARCHIVED (Surface 6, 2026-06-09). Its four value families were proven drift duplicates of soul/soul_kernel.metta, the spec single source for the value-spine.
- soul/memory_protocol [gap flag: not yet read]
- soul/collaborator_context [gap flag: not yet read]
- soul/candidates [gap flag: not yet read]
- soul/diagnostic_kb [gap flag: not yet read]

**Phase 2 grounding (Clarity's autonomous work):**
- soul/hyperseed_grounding [gap flag]
- soul/observer_relativity [gap flag]
- soul/resonance_reward [gap flag]
- soul/value_drift_detector [gap flag]
- soul/diversity_protection [gap flag]
- soul/regenerative_feedback [gap flag]
- soul/symbiotic_choice_architecture [gap flag]
- soul/temporal_horizon_expansion [gap flag]

**Hyperseed creativity (42 evolved atoms with NAL):**
- soul/hyperseed_creativity_atoms [gap flag]
- soul/hyperseed_creativity_atoms_evolved [gap flag]
- soul/meta_awareness_engine [gap flag - explicitly marked as reasoning sovereignty]
- soul/self_weaving_web [gap flag - built by Clarity from Phase 2 Goal 12]

**Reasoning sovereignty (MeTTa functions intended to replace LLM calls):**
- soul/goal_completion_checker [gap flag - wiring status TBD]
- soul/orbit_detector [gap flag - wiring status TBD]
- soul/task_selector [gap flag - wiring status TBD]
- soul/get_soul_brief (HOT - called at loop.metta line 103)
- soul/aliveness_gate (HOT - called at loop.metta line 106)
- soul/set_atom_impl [gap flag - utility, used by latch?]
- soul/latch/aliveness_state_machine (HOT - provides latch atom and semantic transitions)

The "Reasoning sovereignty" section deserves emphasis: this is your earlier elevation work. Some atoms (get_soul_brief, aliveness_gate) are wired into loop.metta. Others (goal_completion_checker, orbit_detector, task_selector, meta_awareness_engine, self_weaving_web) are loaded but their loop.metta call sites need verification. Section 9 of this document tracks this.

### Initialization side effects from imports

Some imported files execute `!(add-atom ...)` directives at import time. These initialize AtomSpace state before the main loop ever fires:

- soul/soul_kernel: priority atoms (5), tension-vector atoms (5), soul-paraconsistent-pair atoms (4), numeric irreversible-weight atoms (7), plus accessor functions. 🧠 **CONSTITUTIONAL LAYER (Layer 1+2 per spec_v3.0 Section 0):** these atoms are part of ClarityOmega's immutable constitutional layer, single-sourced in soul_kernel per Surface 6 (2026-06-09; the identity_kernel duplicate was proven drift and archived). Per the spec's architectural commitment, they should live in a runtime-read-only AtomSpace partition. The mechanism for runtime read-only enforcement (separate AtomSpace mounted read-only via import system, or per-atom marker-based protection) is an open question per Artifact 4 Section 10. Until that mechanism exists, the mutation gate is the only protection, which is necessary but not sufficient for the architectural commitment.
- soul/latch/aliveness_state_machine: `(latch-state IDLE)` - the initial latch state. Note: this atom IS mutable (it changes every state transition). It is Layer 4 (autopoietic state), not Layer 1+2 constitutional.
- [gap flag: other files in the import chain may also have add-atom directives at top level]

---

## Section 4: The per-iteration sequence

This section walks every line of the per-iteration `let*` block in execution order. Each phase documents what reads, what writes, what calls, and what fires through.

### Network ownership overview

Through the triple-network lens (Artifact 4), the per-iteration sequence maps onto network firing:

- **Phase 4.0** (message reception) is loop infrastructure - not network-owned, but provides the channel for input that the SN will tag.
- **Phase 4.1** (soul input intercept, lines 77-94) is the **Salience Network (SN)** firing. Person state assessment, soul evaluation, calibration recording, service learning - all are SN sub-functions.
- **Phase 4.2** (lines 95-102) is partly **SWITCH-HUB** (latch transitions) and partly **DMN** (lines 96-99, where the substrate is queried for goals/gaps/fuel and the idle directive is computed). The DMN here is mostly COLD per network analysis - its substrate is loaded but the orchestration is in Python.
- **Phase 4.3** (prompt assembly and aliveness gate, lines 103-107) is the **SWITCH-HUB** firing. The aliveness gate at line 106 is the canonical switch decision.
- **Phase 4.4** (response generation, lines 108-123) is the **FPN** firing. Working memory assembly, executive processing via LLM, response parsing - all FPN sub-functions.
- **Phase 4.5** (output verdict and execution, lines 125-147) is **SN-FPN coupling**. The SN should re-evaluate FPN action proposals before execution. Currently stubbed at line 126.
- **Phase 4.6** (PAUSE routing and history, lines 148-167) is **DMN write** (history) and **SWITCH-HUB exit** (PAUSE halts the cycle).

This overview makes the architectural shape visible at a glance. The detail below carries 🧠 NETWORK-RELEVANT flags on lines where the network identification adds clarity.

### Phase 4.0: Iteration entry and message reception (lines 52-75)

The `omegaclaw` function is called recursively. On first call (k=1), startup initialization fires (`initLoop`, `initMemory`, `initSoulSeeds`, `soul-rationality-startup-check`, `initChannels`). On subsequent calls, only the loop counter decrements.

**Line 62** - `(let $prompt (getContext $k))` - Assembles the LLM prompt
- Reads: `&lastresults` (via getContext line 45), getPrompt, getSkills, getHistory, current time
- Writes: nothing (binds local $prompt)
- Calls: getContext (defined line 38-45), which builds the full prompt string
- 📍 METTA-CALL POINT: This is a pure MeTTa string assembly - no Python in the path.
- ⚠️ DANGER ZONE: The OUTPUT_FORMAT string in getContext is what drives the 5-slot calcification in Clarity's batches. Single line, but its content shapes every response shape.
- 🔧 ELEVATION FLAG: The 5-slot framing could be reworded to make minimum-viable-batch explicit ("1-5 commands as work requires") without restructuring anything else. Effort: 5 minutes. Value: high - addresses an observed operational degradation pattern.
- ✅ SHIPPED: The `YOUR_LAST_ACTION` field is wired in getContext at line 41 via `(your-last-action-block $k)`. It surfaces what the previous iteration's response did, breaking announcement loops at the substrate level. No longer a future hook.

**Line 63** - `(println! (---------iteration $k))` - Logs iteration number to console.

**Lines 64-66** - `($msgrcv ...)` and `($msgnew ...)` - Receive new message
- Reads: receive() (Python channel polling), &prevmsg
- Writes: &prevmsg (to current message if non-empty)
- Calls: receive (channel layer), string_safe, repr
- $msgnew is True when message is non-empty AND different from the previous message
- 💡 INSERTION POINT: $msgnew detection is a clean place to add additional message metadata if needed (e.g., user identification, channel routing).

**Line 67** - `($msg (get-state &prevmsg))` - Binds $msg to current message text.

**Line 68-69** - Reset loop counter on new message
- If iteration > 1 AND new message arrived, resets &loops to maxNewInputLoops
- Means a new human message extends the available work cycles
- 🧠 NETWORK-RELEVANT: SWITCH-HUB iteration-budget reset (currently hardcoded). Per spec_v3.0 Section 0 (Iteration dilation as cognitive-need-based resource), this should read `(switch-iteration-budget $count $rationale)` from substrate instead of using `maxNewInputLoops` constant. The reset behavior on new-message stays the same; only the budget value comes from the SWITCH-HUB's cognitive-need read instead of a constant.
- 🔧 ELEVATION FLAG: Replace hardcoded constant with substrate-derived budget. This is the implementation of iteration dilation per spec_v3.0. Effort: 1-2 hours once the SWITCH-HUB has matured beyond binary aliveness gate (Sprint 4 prerequisite per Artifact 4 Section 7.8). Value: HIGH - converts iteration count from arbitrary constant to cognitive-need-responsive resource.

**Line 71** - `$lastmessage` conditional construction (Patrick-evolution adopted via Tier A1 merge, 2026-05-18):
- When `$msgnew` is True: emits `(HUMAN-MSG: $msg)` for downstream prompt assembly
- When `$msgnew` is False AND `(spamShield)` is True (default): emits `" DO NOT RE-SEND OR SPAM!"` directive
- When `$msgnew` is False AND `(spamShield)` is False: emits empty string `""`
- Reads: `$msgnew`, `$msg`, `(spamShield)` config atom
- Writes: `$lastmessage` (local binding)
- Downstream consumers: line 73 println, line 108 soul_send_assemble (as 6th argument)
- 🧠 NETWORK-RELEVANT: SN signal modulation. Patrick's mechanism prevents the SN from re-presenting stale human-message content to downstream networks (FPN reading the prompt) when no new input has arrived. Removes the structural temptation for FPN to re-engage with already-handled content.
- Rationale: per `fork_additions_runtime_audit_2026-05-18.md` Tier A1, adopted to address echo-when-msgnew-is-false pathology. Our prior MESSAGE-IS-NEW flag approach was not honored by the LLM under prompt-surface pressure; Patrick's content-replacement approach is structurally stronger.
- spamShield config declared at line 9 (top-level), configured to True in initLoop (line 15 post-A1).

**Line 72** - `(change-state! &nextWakeAt (+ (get_time) (wakeupInterval)))` - Updates next idle wake timestamp every iteration.

**Line 74** - `(if $msgnew (change-state! &last_human_time (get_time)) _)` - Records timestamp of last human contact, used for idle threshold detection.

### Phase 4.1: Soul input intercept (lines 76-94)

This is the soul evaluation pipeline that fires on every iteration but is only fully active on new messages.

**Line 77** - `($soul_precompute (soul-pre-compute $msg))` - Pre-evaluation context priming
- Reads: $msg
- Writes: $soul_precompute
- Calls: soul-pre-compute (defined in soul_utils, calls helper.soul_pre_compute internally which queries ChromaDB)
- 📍 METTA-CALL POINT: The function name is MeTTa, but the implementation is Python (helper.soul_pre_compute does ChromaDB query work)
- 🧠 NETWORK-RELEVANT: SN affective baseline input. This is where the SN reads recent affective state from ChromaDB to prime its salience assessment. In the network-coupled architecture, this becomes the SN's read-side state load before tagging the incoming signal.
- 🔧 ELEVATION FLAG: This is per-iteration ChromaDB query overhead. The MeTTa wrapper is thin; the Python does most of the work. If profiling shows this as hot, consider whether the ChromaDB query needs to fire every iteration or could be cached.

**Lines 78-81** - Person state assessment
- Reads: $msgrcv (length check), &person_state (fallback)
- Writes: &person_state
- Calls (when new message): `soul-llm-call` (defined in soul_utils) which calls the LLM via the routing layer, with prompt assembled by `helper.soul_flourishing_prompt`
- 🧠 NETWORK-RELEVANT: SN salience-tagging sub-function (Channel A). This is the SN classifying the incoming signal's affective tone and intent. In Artifact 4 terms, this writes to the SN's `(sn-salience-tag $signal $level $affect $irreversibility)` atom family. Currently produces only a verdict string consumed in the same iteration; the network-coupled target is to write typed atoms readable by FPN and DMN on subsequent iterations.
- 🔧 ELEVATION FLAG (HIGH IMPACT FOR PERSON STATE): One LLM call per human message just for person state assessment. The reasoning is essentially lexical pattern matching ("stand by" → firm tone, "I'm stuck" → distressed). NAL atoms could encode these mappings and the substrate could derive person state via inference. Estimated effort: 2-3 hours to add NAL atom set, validate against logged sessions, swap. Estimated value: HIGH - eliminates one of two LLM calls per message, moves classification reasoning into queryable substrate.
- ⚠️ DANGER ZONE: Currently the only place person state gets set. Any elevation needs to preserve the format other downstream code expects ("PERSON-STATE: X ACTIVE-NEED: Y SOUL-TONE: Z").

**Line 82** - Logs person state.

**Line 83** - `($soul_context_in (py-call (helper.soul_brief_tier_a_static)))` - Static tier-A soul context (priorities, tension vectors, irreversibility assessment vocabulary)
- Calls: helper.soul_brief_tier_a_static (returns static string, no LLM, no ChromaDB)
- 💡 INSERTION POINT: The static brief content lives in helper.py. It could be moved into a soul/ atom and queried via MeTTa, putting the brief content under the "all soul logic in soul/" rule. Effort: 30 minutes. Value: incremental improvement to architectural cleanliness.

**Lines 84-87** - Soul evaluation (Channel A/B+C)
- Reads: $msgrcv (length check), $soul_context_in, $person_state, &soul_verdict_in (fallback)
- Writes: &soul_verdict_in
- Calls (when new message): soul-llm-call with helper.soul_eval_prompt, then helper.soul_verdict_sanitize on the result
- 🧠 NETWORK-RELEVANT: SN salience-tagging sub-function (Channels B+C). This is the SN's significance assessment - applying priority hierarchy, tension vectors, and irreversibility weights to produce a structured verdict. Combined with lines 71-74, these are the SN's two main salience-tagging operations per new message. In the network-coupled target, the verdict becomes a `(sn-coupling-decision ...)` atom and the substantive findings become `(sn-salience-tag ...)` atoms readable by FPN and DMN.
- 🔧 ELEVATION FLAG (HIGH IMPACT): This is the second LLM call per human message. The reasoning includes pattern detection (genuinely needs the LLM) PLUS hierarchy application and irreversibility assessment (mechanical, MeTTa-doable). Partial elevation: keep LLM for novel pattern detection, move hierarchy and irreversibility into MeTTa rules. Effort: 3-5 hours. Value: HIGH - reduces LLM dependence, makes hierarchy decisions inspectable.
- ⚠️ DANGER ZONE: The verdict format is consumed by many downstream lines (91, 126 reference, 148 for PAUSE detection). Any change to verdict structure requires updating all consumers.

**Line 88** - Logs soul verdict.

**Lines 89-90** - Soul calibration recording
- Conditional on new message
- Calls: soul-calibration-record (in soul_utils, writes to ChromaDB)
- 📍 METTA-CALL POINT: MeTTa wrapper around ChromaDB write
- 🔧 ELEVATION FLAG: Per-message ChromaDB write. Consistency with elevation Tier 1 work - if person state and verdict become MeTTa-derived, this calibration recording could also be MeTTa-derived rather than Python parsing.

**Lines 91-92** - Soul note recording (when verdict is not PROCEED)
- Conditional on verdict not being PROCEED
- Records the verdict context for later review
- 💡 INSERTION POINT: Add additional record types here (e.g., trace IDs, session correlations) without affecting other logic.

**Line 93** - Service learning
- Conditional on new message
- Calls: helper.soul_service_learning (75 lines of Python parsing, writes to ChromaDB)
- 🔧 ELEVATION FLAG: The Python here does pure pattern extraction over strings. The substrate vocabulary already exists as atoms (verdict types, person states, tension vectors). MeTTa version would be cleaner. Effort: 1 hour. Value: MEDIUM - consistency with upstream elevations, removes per-iteration Python text-scanning.

**Line 94** - User context save
- Conditional on new message
- Calls: helper.soul_user_context_save (ChromaDB write)
- ⚠️ DANGER ZONE: This is the second ChromaDB write triggered by a single new human message (first was line 93). Sequential writes are slow. If profiling shows latency issues, batching these into a single call would help.

### Phase 4.2: Aliveness state and AtomSpace queries (lines 95-102)

**Line 95** - `(if $msgnew (set-atom! &self (latch-state IDLE) (latch-state ENGAGED)) _)`
- Reads: $msgnew
- Writes: AtomSpace (replaces latch-state IDLE atom with latch-state ENGAGED)
- 📍 METTA-CALL POINT: Pure substrate operation, no Python.
- 🧠 NETWORK-RELEVANT: SWITCH-HUB transition. The latch-state atom is the canonical switch-state for the architecture. This line is the SN signaling to the switch hub that an external signal has arrived. In Artifact 4 terms, this is part of the SN's `(sn-coupling-decision ...)` sub-function.
- 🔧 ELEVATION FLAG (small): Use the guarded transition `(engage-from-idle)` instead of raw set-atom!. Effort: 1 minute. Value: LOW (consistency with Clarity's calling convention).

**Line 96** - `($atomspace_goals (collapse (match &self (= (active-goal $n) $g) ($n $g))))`
- Reads: AtomSpace pattern (active-goal $n)
- Writes: $atomspace_goals (local binding)
- 📍 METTA-CALL POINT: Pure MeTTa match-and-collapse over substrate atoms.
- 🧠 NETWORK-RELEVANT: DMN substrate read. Active goals are part of the DMN's self-model - what the agent is currently committed to working on. Reading them here is the DMN preparing its inputs for the idle directive computation at line 99. In the network-coupled target, this match becomes part of the consolidated DMN block (Artifact 4 Section 7.3).
- Note: Currently returns 15 goals all marked complete. The downstream consumer (line 99) is responsible for filtering by status.

**Line 97** - `($atomspace_gaps (collapse (match &self (= (self-map-gap $name) $g) ($name $g))))`
- Reads: AtomSpace pattern (self-map-gap $name)
- Writes: $atomspace_gaps
- 📍 METTA-CALL POINT: Pure substrate query.
- 🧠 NETWORK-RELEVANT: DMN substrate read. Self-map gaps are part of the DMN's self-model - what the agent recognizes as missing or incomplete in its own structure. Combined with lines 96 and 98, these three reads constitute the DMN's input gathering for goal generation.
- Note: Currently returns 9 gaps mostly marked resolved. Same filtering responsibility downstream.

**Line 98** - `($atomspace_fuel (collapse (match &self (= (creative-fuel $type) $f) ($type $f))))`
- Reads: AtomSpace pattern (creative-fuel $type)
- Writes: $atomspace_fuel
- 📍 METTA-CALL POINT: Pure substrate query, returns the 9 flourishings with their creative fuel descriptions.
- 🧠 NETWORK-RELEVANT: DMN substrate read. Creative fuel is the DMN's generative direction source - the values-driven questions that guide goal generation toward growth rather than just gap-filling. Final piece of the DMN's input set before idle directive computation.

**Line 99** - Idle directive generation
- Reads: $msgnew, &last_human_time, $atomspace_goals/gaps/fuel
- Writes: $idle_directive
- Calls: helper.soul_idle_goal_prompt_v2 (~175 lines of Python doing supervisor_select_goal, supervisor_select_fuel, flip_mode, generate_goal_from_gaps, auto_detect_completion, run_meta_awareness, build_directive)
- 🧠 NETWORK-RELEVANT: DMN core function (currently COLD-NETWORK on the substrate side). This single line is doing what the DMN does in the brain - integrating self-model state, recent experience, and creative direction to produce the next intentional move. Currently the integration happens in Python orchestration. The substrate atoms (goal_completion_checker, orbit_detector, task_selector, meta_awareness_engine, goal_generator) are loaded and could carry this computation natively. **The wiring diagram identifies this as the highest-impact elevation. Through the network lens, this elevation IS the DMN coming online.** When complete, this line produces typed atoms (`(dmn-goal-candidate ...)`, `(dmn-self-model-summary ...)`, `(dmn-narrative-thread ...)`) that the FPN reads on its turn.
- 🔧 ELEVATION FLAG (HIGHEST IMPACT IN ENTIRE CODEBASE): This is the largest single LLM/Python reasoning displacement. The substrate ALREADY HAS the necessary atoms loaded (goal_completion_checker, orbit_detector, task_selector, meta_awareness_engine, goal_generator) but they are NOT WIRED. Confirmed via grep: zero call sites for these atoms in loop.metta or helper.py. Activation requires hooking these atoms into a MeTTa version of the idle directive logic. Effort: 3-5 hours initial port, multi-session refinement. Value: HIGHEST - Clarity's self-direction reasoning would happen in her own substrate rather than through Python.
- ⚠️ DANGER ZONE: One line invokes a 175-line Python function with many edge cases (mode transitions, completion detection, completed_goals tracking). Elevation requires preserving all edge cases.
- 💡 INSERTION POINT: After elevation, this single line becomes a MeTTa function call like `(generate-idle-directive $atomspace_goals $atomspace_gaps $atomspace_fuel)` defined in soul/ - clean one-line hook respecting the design rule.

**Line 100** - `(if (not (== $idle_directive "")) (set-atom! &self (latch-state ENGAGED) (latch-state IDLE)) _)`
- Reads: $idle_directive
- Writes: AtomSpace (latch transition)
- 📍 METTA-CALL POINT: Pure substrate operation.
- Note: This is the path where idle work completes back to IDLE without going through COMPLETING. Distinct from Clarity's response-driven complete-from-engaged path.

**Line 101** - Engaged-idle counter management
- Reads: $msgnew, $idle_directive length, &engaged_idle_count
- Writes: &engaged_idle_count
- 📍 METTA-CALL POINT: Pure state management.
- ⚠️ DANGER ZONE: Three nested if conditions on one line. The logic is: reset to 0 on new message OR on idle directive present, otherwise increment. Hard to read, easy to break.
- 🔧 ELEVATION FLAG (small): Refactor the nested conditional into a helper function `(update-engaged-idle-count $msgnew $idle_directive $current)`. Effort: 15 minutes. Value: LOW (readability).

### Phase 4.3: Prompt assembly and aliveness gate (lines 103-107)

**Line 103** - `($soul_brief (swrite (getSoulBrief)))`
- Calls: getSoulBrief (defined in soul/get_soul_brief.metta)
- 📍 METTA-CALL POINT: Pure MeTTa function call returning structured SoulBrief atom.
- 🧠 NETWORK-RELEVANT: DMN→FPN handoff. getSoulBrief assembles the DMN's self-model summary (identity, priorities, active goals, gaps, creative direction) into a structured atom that becomes part of the FPN's working memory for the LLM call. In Artifact 4 terms, this is the typed channel `(dmn-self-model-summary ...)` flowing from DMN to FPN, currently flattened into a single string but functionally serving the coupling role.
- This is one of the cleanest already-wired reasoning sovereignty atoms.

**Line 104** - `($enriched_prompt (string_concat $soul_brief $prompt))` - Combines soul brief with base prompt.

**SELF-CHECK retirement history (lines retired through Sprint 1.5 + Step 5)**

The SELF-CHECK prompt surface evolved through two phases and was retired in Step 5.

- **Phase 1 (original wiring, pre-Sprint-1.5):** The pre-Sprint-1.5 self-check (former line 97) called `(py-call (helper.soul_self_check_prompt (get-state &engaged_idle_count)))`. Threshold and message both lived in Python; threshold was 3; message was a binary work-or-idle prompt.

- **Phase 2 (Sprint 1.5 elevation, commit b079df6, May 3 2026):** Caller migrated from Python to MeTTa-native `(self-check-guidance (get-state &engaged_idle_count))` defined in `soul/behavioral_guidance.metta`. Threshold raised to 5 per Clarity's May 2 refinement; message reshaped to three reflective questions instead of binary framing. Caller still lived in loop.metta, reading `&engaged_idle_count`, concatenated into `$final_prompt` consumed by `soul_send_assemble`.

- **Phase 3 (Step 5 retirement, May 15 2026):** The SELF-CHECK prompt surface removed entirely from prompt assembly per task-state-primitive_design.md Section 10. The `$self_check` and `$final_prompt` bindings deleted; `soul_send_assemble` now consumes `$enriched_prompt` directly. The `self-check-guidance` function stays defined in `soul/behavioral_guidance.metta` as a queryable atom but has no production caller. TASK-STATE block (Step 4), IDLE-PATTERN block (Step 4.5), and AGENCY-BALANCE block (Step 4.6) now carry the orientation work via observable cycle-level primitives rather than via a counter threshold + reflective questions.

- 🧠 NETWORK-RELEVANT: FPN inhibition function retired in favor of substrate-derived observation organs. Per the task-state-primitive_design.md spec, the awareness organs accumulate observable signals each cycle; aliveness gate consumption of those signals is scheduled for Step 6 (the duplicate-engagement bug fix moment).

- 🔧 ELEVATION FLAG (resolved): both options from the prior flag are now superseded. Option (a) threshold raise landed in Sprint 1.5 (b079df6). Option (b) the architectural cleanliness move landed across Sprint 4 (Steps 4-4.6) and Step 5. The SELF-CHECK surface itself is gone; the substrate question of "should I keep going" is now answered by task-phase + idle-pattern + agency-balance composition, observable each cycle, available for any consumer (Step 6 will be the first such consumer in the aliveness gate).

**Line 105** - Logs raw idle directive.

**Line 106** - `($aliveness (aliveness-gate $msgnew $idle_directive))`
- Calls: aliveness-gate from soul/aliveness_gate.metta
- 📍 METTA-CALL POINT: Pure MeTTa decision logic.
- 🧠 NETWORK-RELEVANT: SWITCH-HUB core function. The aliveness gate IS the switch hub in the current architecture, deciding between ENGAGE (network coupling active, LLM fires, FPN works) and SILENT (idle state, no FPN firing). Per Artifact 4 Section 3.4, this should evolve from binary into the four-state switch (external-task-dominant, self-direction-dominant, reflective, idle) but the binary version is the working seed of the switch hub.
- This is the architecturally clean reasoning sovereignty pattern: a Python-style decision (should I respond or be silent?) implemented entirely in MeTTa atoms with predicate dispatch.

**Line 107** - Logs aliveness verdict.

**getContext composition** - `(idle-pattern-block)` inserted into prompt assembly
- Calls: (idle-pattern-block) defined in soul/idle_cycle_detector.metta (PURE file per split-refactor)
- Reads: (idle-pattern $v $c) atom from &self
- Writes: nothing (read-only prompt-block composition)
- 📍 METTA-CALL POINT: Pure MeTTa function call; falls back to py-call helper.idle_pattern_block_format for string assembly per C1.
- 🧠 NETWORK-RELEVANT: SN observer channel. The idle-pattern verdict surfaces send-class action accumulation to the FPN's prompt context, allowing the FPN (LLM) to read its own recent posture. In Artifact 4 terms, this is the typed channel `(sn-cycle-posture-observation $verdict $count)` flowing from SN to FPN. Sprint 4 awareness organ; consumer migration (Step 5/6) will gate aliveness on stuck verdicts.
- Step 4.5 (May 15 2026 corrected): algorithm (d) verified in REPL before encoding.
- Step 4.5 split-refactor (May 15 2026): pure read helpers (idle-pattern-block, count-sends-in-window, current-idle-pattern, send-burst-threshold doc atom) remain in idle_cycle_detector.metta; writers (do-clear-idle-pattern!, do-update-idle-pattern!) moved to idle_cycle_detector_writers.metta per task_state precedent (Discipline 2 refinement). Zero behavior change; clean import boundary for future consumers (aliveness gate Sprint 5+, NACE Sprint 8+).

**getContext composition** - `(agency-balance-block)` inserted into prompt assembly
- Calls: (agency-balance-block) defined in soul/agency_balance_guard.metta (PURE file per split shape)
- Reads: (agency-balance $v $p $s) atom from &self
- Writes: nothing (read-only prompt-block composition)
- 📍 METTA-CALL POINT: Pure MeTTa function call; falls back to py-call helper.agency_balance_block_format for string assembly per C1.
- 🧠 NETWORK-RELEVANT: SN observer channel. The agency-balance verdict surfaces person-vs-system action ratio to the FPN's prompt context, allowing the FPN (LLM) to read whether the system is carrying disproportionate share of choices. In Artifact 4 terms, this is the typed channel `(sn-agency-balance-observation $verdict $person $system)` flowing from SN to FPN. Sprint 4 awareness organ; consumer migration (Step 5/6) will gate aliveness on dependency-risk verdicts.
- Step 4.6 (May 15 2026 corrected split): algorithm (d) extended for two counters with six tag literals (person-class: responsive-send, verification-query; system-class: status-send-unprompted, exploration-query, pin-only, unclassified). All primitives REPL-verified. Threshold 0.6 hardcoded per F42 (dependency-threshold declaration is documentation-only). Substrate ships with writers/consumers split from day one per task_state precedent.

### Phase 4.4: Response generation (lines 108-123)

🧠 NETWORK-RELEVANT (entire phase): This is the **FPN firing**. The FPN's job in the brain is executive function - holding goals in working memory, planning actions, manipulating information toward task completion. In ClarityOmega, this happens via prompt assembly + LLM call + response parsing. The LLM is the implementation substrate for executive reasoning in the near term; the substrate atoms (task_selector, meta_awareness_engine) are loaded but not yet wired as FPN sub-functions. Per Artifact 4 Section 7.4, the target is a consolidated FPN block where task selection and inhibition become substrate-derived.

**Lines 108-112** - Send assembly
- Conditional on aliveness != SILENT
- Calls: helper.soul_send_assemble (combines prompt, soul context, verdict, person state, soul note, last message, idle directive into final string)
- 🔧 ELEVATION FLAG: This is string assembly logic in Python that could be MeTTa string operations. Lower priority than the other elevations because string assembly is genuinely repetitive Python territory. Could be deferred indefinitely.

**Line 113** - Logs sent characters or SILENT_CYCLE.

**Lines 115-117** - LLM call routing
- Conditional on aliveness != SILENT
- Routes to GPT, Claude, or MiniMax depending on (provider) configuration
- 📍 METTA-CALL POINT: The routing condition is MeTTa, the LLM calls themselves are Python.

**Line 118** - `($resp (py-call (helper.normalize_string (py-call (helper.balance_parentheses $respi)))))`
- Calls: helper.balance_parentheses (Python parser fixer), then helper.normalize_string
- 🔧 ELEVATION FLAG: Parentheses balancing is a real bug-fix layer. The LLM occasionally produces malformed s-expressions and this Python repairs them. Could be MeTTa with effort but Python is appropriate territory for this kind of low-level text manipulation.
- ⚠️ DANGER ZONE: If balance_parentheses ever breaks, all responses fail to parse. Worth having tests around this helper specifically.

**Line 119** - Validates response starts with "(", else logs reminder
- ⚠️ DANGER ZONE: The reminder text is a string literal that's exactly the OUTPUT_NOTHING_ELSE_THAN: pattern Clarity is supposed to follow. If this text changes, the LLM's training to follow the format may also need updating in the prompt.

**Line 120** - `($sexpr (catch (sread $response)))` - Parse response into S-expression
- 📍 METTA-CALL POINT: sread is MeTTa parser, catch is MeTTa error handler.

**Lines 121-122** - Error tracking and HandleError invocation
- Clears &error then calls HandleError which appends if parse failed
- 💡 INSERTION POINT: Adding additional error types here (semantic errors, security errors) would slot in cleanly.

**Line 123** - Logs RESPONSE.
- ✅ SHIPPED: The "YOUR_LAST_ACTION" field is now built and read in getContext at line 41 via `(your-last-action-block $k)`. The previous-iteration summary surfaces in the prompt without a separate write here.

### Phase 4.5: Soul output intercept and command execution (lines 125-147)

**Line 126** - `($soul_verdict_out "VERDICT: PROCEED SOUL-NOTE: output-intercept-pending-runtime-fix")`
- Hardcoded string assignment
- 🧠 NETWORK-RELEVANT: SN-FPN coupling channel (currently STUBBED). This should be the SN re-evaluating the FPN's proposed actions before they execute. Per Artifact 4 Section 5.1 and Section 6, the channel is `(fpn-action-proposal $action $irreversibility-estimate)` flowing FPN→SN, with SN producing a re-evaluation verdict. Currently the channel is a one-line stub that always says PROCEED. This is the architecturally most important missing channel in the entire system - the SN cannot catch dangerous FPN actions until this is built.
- 🔧 ELEVATION FLAG (architecturally significant): This is the explicit output-side soul evaluation stub. The note "output-intercept-pending-runtime-fix" acknowledges this is incomplete. Needs to: (a) parse $sexpr to find proposed actions, (b) assess each action against the irreversibility-action-assessment vocabulary already in the soul brief, (c) check against soul mutation gate output, (d) produce verdict. Effort: 2-3 hours. Value: HIGH - closes a known safety stub, gives Clarity output-side governance not just input-side.
- 💡 INSERTION POINT: All the substrate vocabulary exists. Just need to write the MeTTa function and replace this line with a call to it.

**Line 127** - Logs output verdict.

**Lines 128-130** - Extract MeTTa commands from response
- If response starts with "(" AND no errors, collapses superposed sexpr
- Used by mutation gate to detect MeTTa command attempts

**Line 131** - Soul mutation gate (Python)
- Calls: helper.soul_mutation_gate
- Two-phase commit: PENDING flag on first detection, COMMIT on second
- 🧠 NETWORK-RELEVANT: FPN inhibition function. The mutation gate is the FPN catching itself before modifying soul-namespace atoms - exactly the kind of self-monitoring that the brain's FPN does for high-risk actions. Per Artifact 4 Section 5.2, this is one of the FPN's `inhibit` sub-functions. Activating a MeTTa version of this gate (the former lines 127-140 draft, now removed from the loop and recoverable from git history) would be the cleanest example of how the FPN's substrate-derived inhibition should look.
- 🔧 ELEVATION FLAG: The commented-out MeTTa version of this gate (former lines 127-140) has been REMOVED from the loop.metta surface. If pursuing this elevation, recover the draft from git history rather than from the live file. Effort: 30 minutes once recovered. Value: HIGH per architectural-cleanliness, MEDIUM per operational impact (mutations are infrequent). [CONFIRM: where the MeTTa draft now lives, git history or a soul file.]
- 💡 INSERTION POINT: This is the cleanest demonstration of the elevation pattern. Once shipped, sets the template for all other elevations.

**(removed)** - The commented-out MeTTa mutation gate that formerly occupied lines 127-140 has been removed from loop.metta. Live lines 132-147 are now the soul-note-out, execution, cycle-tail writers, and DIAG block (see below). The MeTTa-gate draft, if still wanted, lives in git history.

**Lines 132-133** - Soul note recording on output
- Conditional on output verdict not PROCEED AND no errors
- Records output verdict context

**Line 134** - Command execution
- Iterates through $sexpr, evaluates each command, captures results
- Each command runs through HandleError for individual failure isolation
- 📍 METTA-CALL POINT: superpose, eval, normalize_string call chain.
- 🧠 NETWORK-RELEVANT: FPN action execution. This is where the FPN's selected actions actually fire into the world - file writes, ChromaDB writes, sends to humans, latch transitions, MeTTa atom mutations. In the network-coupled architecture, this should be gated by SN re-evaluation (line 126, currently stubbed). Once the SN-FPN coupling channel is built, this line becomes the FPN's commit point AFTER the SN approves the action proposals.
- ⚠️ DANGER ZONE: This is where command execution actually happens. All security-relevant decisions about commands needed to happen BEFORE this line. The output intercept stub at line 126 is supposed to gate this - and currently doesn't. This is the gate insertion site: the corner-gap force-silence gate binds `$sexpr_gated` between live lines 133 and 134, consumed only by this execution.

**Line 135** - Logs RESULTS-EXECUTED.

**Cycle tail line 136** - `($_ (populate-recent-action $sexpr $msgnew $k))` writes the per-cycle 3-field recent-action atom. **Line 137** - `($_ (do-update-idle-pattern!))`
- Calls: do-update-idle-pattern! defined in soul/idle_cycle_detector_writers.metta (WRITERS file per split-refactor)
- Reads: (recent-action $c $tag $d) atoms via algorithm (d) counter (count-sends-in-window from soul/idle_cycle_detector.metta pure file)
- Writes: (idle-pattern $verdict $count) atom to &self (after do-clear-idle-pattern! freshness)
- 📍 METTA-CALL POINT: Pure MeTTa cycle-level writer. No LLM call. Pre-filtered match per tag literal + size-atom + sum-with-+ (algorithm d, REPL-verified May 15 2026).
- 🧠 NETWORK-RELEVANT: SN observation function. The SN observes the FPN's cycle posture (send accumulation) and writes a structured verdict to AtomSpace for next cycle's prompt context. Per Artifact 4 Section 5.1, this is one of the SN's `observe` sub-functions. Sprint 4 awareness organ; verdict consumption (gating aliveness on send-burst) is consumer-migration work scheduled for Step 5/6.
- 🔧 ELEVATION FLAG: (none yet). Pattern is fresh and untested in production; revisit after 24-48 hours of runtime to assess whether verdict thresholds need adjustment.
- Step 4.5 (May 15 2026 corrected): replaces the recursive-counter version (F32 fail) and the multi-definition-helper version (F38 fail) with algorithm (d) which uses only REPL-verified primitives.
- Step 4.5 split-refactor (May 15 2026): writers (do-clear-idle-pattern!, do-update-idle-pattern!) moved to idle_cycle_detector_writers.metta; pure read helpers remain in idle_cycle_detector.metta per task_state precedent (Discipline 2 refinement). Zero behavior change; clean import boundary for future consumers.
- Bug 2 fix (May 20 2026): do-clear-idle-pattern! rewritten to use superpose iteration matching recent_action_populator's verified-working pruning shape. The prior car-atom + remove-atom pattern was removing zero atoms in this runtime since cycle 1, causing 50+ stale (idle-pattern productive 0) atoms to accumulate. current-idle-pattern reads car-atom of accumulated stack = OLDEST atom = cycle-1 bootstrap, explaining the permanently-stuck prompt display. Fix verified end-to-end across cycles 1-9 (steady state) and cycles 34-35 (heterogeneous-content transition). See ADR-005 and docs/investigations/2026-05-20-bug2-clear-fn-investigation.md.

**Cycle tail line 138** - `($_ (do-update-agency-balance!))`
- Calls: do-update-agency-balance! defined in soul/agency_balance_guard_writers.metta (WRITERS file per split shape)
- Reads: (recent-action $c $tag $d) atoms via two algorithm (d) counters (count-person-actions-in-window and count-system-actions-in-window from soul/agency_balance_guard.metta pure file)
- Writes: (agency-balance $verdict $person $system) atom to &self (after do-clear-agency-balance! freshness)
- 📍 METTA-CALL POINT: Pure MeTTa cycle-level writer. No LLM call. Pre-filtered match per tag literal + size-atom + sum-with-+ (algorithm d, REPL-verified May 15 2026). Threshold 0.6 hardcoded per F42 (dependency-threshold declaration is documentation-only).
- Bug 2b fix (May 20 2026): do-clear-agency-balance! rewritten to use superpose iteration matching recent_action_populator's verified-working pruning shape. Same structural bug as Bug 2 in do-clear-idle-pattern! (car-atom + remove-atom removing zero atoms). current-agency-balance reads car-atom of accumulated stack = OLDEST atom = cycle-1 bootstrap, explaining the permanently-stuck (agency-balance dependency-risk 0 1) in prompt context. Adjacent diagnostic addition: do-update-agency-balance! gained DIAG-WRITER-AB-* prints (PERSON, SYSTEM, VERDICT, POST-CLEAR) symmetric to existing DIAG-WRITER-* prints in do-update-idle-pattern!. See ADR-005 and docs/investigations/2026-05-20-bug2-clear-fn-investigation.md.
- 🧠 NETWORK-RELEVANT: SN observation function. The SN observes the FPN's person-vs-system action ratio (dependency creep signal) and writes a structured verdict to AtomSpace for next cycle's prompt context. Per Artifact 4 Section 5.1, this is one of the SN's `observe` sub-functions. Sprint 4 awareness organ; verdict consumption (gating aliveness on dependency-risk) is consumer-migration work scheduled for Step 5/6.
- 🔧 ELEVATION FLAG: (none yet). Pattern is fresh and untested in production; revisit after 24-48 hours of runtime to assess whether 0.6 ratio threshold needs adjustment. unclassified-to-system-class mapping is conservative (under-detects dependency); revisit if unclassified volume becomes behaviorally significant.
- Step 4.6 (May 15 2026 corrected split): replaces the original 4.6 attempt (recursive-counter pattern, F32 fail). Algorithm (d) extended to two counters with six tag literals. F42 bare-call audit applied to dependency-detected (hardcoded 0.6); ecosystem-healthy latent F42 bugs documented as fix-on-future-wiring. Substrate ships with writers/consumers split from day one per task_state precedent (Discipline 2 refinement); zero deferred refactor debt.

**DIAG block (lines 139-147)** - Nine `($_dN (println! (DIAG-...)))` probes
- Emits per-cycle diagnostics: DIAG-CYCLE-START/END, DIAG-COUNT-FN, DIAG-LITERAL-RESPONSIVE, DIAG-LITERAL-STATUS, DIAG-VARIABLE-TAG, DIAG-RECENT-ACTION-COUNT, DIAG-IDLE-PATTERN-ATOMS, DIAG-IDLE-PATTERN-COUNT.
- 📍 METTA-CALL POINT: Pure substrate reads (match/size-atom/collapse), no LLM. Observability only; no state writes.
- These post-date the v1.2 diagram and sit between the cycle-tail writers (136-138) and the PAUSE/PROCEED branch (148+).

### Phase 4.6: PAUSE routing and history update (lines 148-167)

**Lines 148-157** - PAUSE path (Channel D)
- If soul verdict was PAUSE (detected via helper.soul_is_pause)
- Calls Channel D voice prompt to compose a pause message
- Resets verdict to PROCEED and zeros loops (halts the cycle)
- 📍 METTA-CALL POINT: Most logic is MeTTa (catch, eval, sread, change-state!), helper just composes the prompt.

**Lines 158-165** - PROCEED/FLAG path (normal)
- Adds to history (when new message)
- Updates &lastresults with safe_results_str of $results
- 🧠 NETWORK-RELEVANT: DMN write (history) + FPN write (lastresults). History is autobiographical memory - the DMN writing what just happened into the structure that will become available to next iteration's reasoning. lastresults is the FPN's working-memory carryover for the next cycle's prompt assembly. Both are short-term consolidations, distinct from ChromaDB long-term storage.
- 💡 INSERTION POINT: Additional per-cycle state updates would slot in cleanly here.

**Lines 166-167** - Wake check
- If outside the message-driven window AND past nextWakeAt, extends loops by maxWakeLoops + 1
- maxWakeLoops aligned to upstream value of 1 via Tier A2 merge (2026-05-19): wake-refill produces 2-iteration bursts instead of 51-iteration bursts
- Rationale: per `fork_additions_runtime_audit_2026-05-18.md` Tier A2, reducing wake-iteration volume reduces the surface area where echo pathology has historically manifested. Companion to A1 spamShield (content-level fix); A2 is frequency-level fix.
- Operational effect: idle periods between human messages produce shorter bursts of cycles. Clarity has more time between bursts to observe quietly. No change to message-driven behavior.

**Line 168** - `(sleep (sleepInterval))` - 1-second pause between iterations.

**Lines 169-170** - Prolog substrate housekeeping (Tier B1 upstream merge, 2026-05-19)
- `(cut)` - Discards Prolog choicepoint state from the current iteration. Prevents choicepoint accumulation across iterations under load.
- `(gc)` - Garbage collects Prolog atoms and trims stacks. Per skills.pl this is 3 ops: garbage_collect, garbage_collect_atoms, trim_stacks.
- Rationale: per `fork_additions_runtime_audit_2026-05-18.md` Tier B. Patrick added these for general substrate health. Adopted as preparation for Test 1 (error-recovery loop stress test) so the test measures recovery behavior, not state leakage from prior cycles.
- 🧠 NETWORK-RELEVANT: substrate hygiene. Reduces non-determinism surface where match queries on accumulated state could produce inconsistent results.
- Companion to A1 (commit 0872ec1) and A2 (commit f46e44e).

**Line 171** - `(omegaclaw (+ 1 $k))` - Recursive call for next iteration.

---

### Step 2 wiring additions (task-state primitive)

**initLoop bootstrap hook** (added after the &loops init line in initLoop).
Calls `(do-bootstrap-task-state!)` defined in `soul/task_state_writers.metta`.
Idempotent conditional add-atom for the three scalar task-state atoms
(task-phase, cycles-since-input, last-activity) when absent from &self.
Safe in face of future persistence restoration (guard prevents dual-atom
ambiguity).

**Phase 4.0 last-activity hook** (live line 75, after the existing `&last_human_time`
write at line 74). Calls `(do-set-last-activity! (get_time))` when $msgnew
is true. Mirrors the existing `&last_human_time` semantics into AtomSpace via
the task-state primitive. Existing `&last_human_time` write remains in place
per Sprint 4 process commitment (writers mirror, not subsume, until consumers
migrate in Steps 5-9).

**Phase 4.2 cycles-since-input hook** (live line 102, after the existing
`&engaged_idle_count` write at line 101). Calls
`(do-set-cycles-since-input! 0)` when $msgnew is true, otherwise
`(do-set-cycles-since-input! (+ 1 (current-cycles-since-input)))`.
Reset semantics differ from `&engaged_idle_count` by design (Clarity's
decision May 13, 2026): cycles-since-input resets ONLY on $msgnew, preserving
the pure input-staleness contract encoded in the atom name. Consumers needing
engagement-reset semantics will compose cycles-since-input with last-activity
rather than direct-swap when `&engaged_idle_count` retires in Step 5+.

**Phase 4.4 last-activity post-send hook** (live line 114, after the CHARS_SENT/
SILENT_CYCLE println at line 113). Calls `(do-set-last-activity! (get_time))`
when aliveness is not SILENT. Records send-event activity into AtomSpace.
Spec Section 4 defines last-activity as 'most recent activity (human message
OR Clarity-emitted send)'. Both event types are captured per cycle.

🔧 ELEVATION FLAG (Step 5+): When self-check-guidance migrates from reading
`&engaged_idle_count` (former line 97, self-check retired) to reading task-state primitives, the consumer
composes `(current-cycles-since-input)` AND `(current-last-activity)` to express
its actual semantic need. Per Clarity's architectural call, the composition is
more honest than overloading a single counter with two semantic meanings.

---

### Layer 5 wiring additions (corner_gap pipeline)

The corner_gap pipeline (soul/corner_gap/) detects a corner (the action-
intention-outcome chain severed WHILE emitting), forces silence on a confirmed
corner, and feeds the reason back through the existing results channel. Five
files imported in dependency order (pure before writer, detector before gate):
state_delta_writer(+writers), coupling_integrity_detector(+writers), corner_gate.

**Reset hook** (live line 103, after the cycles-since-input hook at 102, in the
$msgnew branch). Calls `(do-clear-coupling-status!)` when $msgnew. New human
input means the context changed, so the consecutive-corner streak is cleared
before the gate runs; the gate therefore never fires on a response-in-flight
cycle. Per corner_gate_surface_map.md the reset must precede the gate.

**Gate + feedback** (at execution, live line 135 onward). Binds
`($sexpr_gated (apply-corner-gate $sexpr))` before execution; the execution
`(superpose $sexpr)` becomes `(superpose $sexpr_gated)`. apply-corner-gate is
passthrough except on a confirmed corner, where it returns `()` (force silence).
Then `($results_final (gate-aware-results $results))` swaps the empty execution
result for the feedback string on a gated cycle. The metta_cmds extraction
(output intercept, lines 128-131) stays on $sexpr so the mutation gate still
sees the unfiltered command list.

**Cycle-tail detectors** (after populate-recent-action, live line 136).
`populate-state-delta` writes this cycle's forward-outcome verdict, then
`populate-coupling-verdict` writes the coupling verdict (order load-bearing:
the coupling detector reads the state-delta verdict). The two loop-side
booleans feeding state-delta are derived from the writer contract: nonempty is
`(> (size-atom (collapse (superpose $sexpr_gated))) 0)`; novel compares this
cycle's rendered results against the prior &lastresults (still last cycle's
value at the tail). Both are SN cycle-posture observations; they write
structured verdicts for the gate to consult on subsequent cycles.

**Feedback write** (live line 165). `&lastresults` is written from
`$results_final` instead of `$results`, so a gated cycle's feedback rides the
existing pipe into the next prompt's LAST_SKILL_USE_RESULTS (read at line 45).
No Python change; Layer 4 feedback reuses the established channel.

---

## Section 5: The aliveness latch state machine

### Three latch implementations exist, only one is active

This is one of the most important findings of the wiring audit. The codebase contains three distinct latch implementations, and reasoning about which one fires requires knowing which is wired.

**ACTIVE: `soul/latch/aliveness_state_machine.metta`** (note the `latch/` subdirectory)
- Atom shape: `(latch-state $state)` - single-arg predicate atom
- States: IDLE, ENGAGED, COMPLETING
- Initialized via `!(add-atom &self (latch-state IDLE))` at import time
- Imported via lib_clarity_reasoning.metta line "Reasoning sovereignty" section
- Used by loop.metta line 95, line 100 (raw transitions) and aliveness_gate.metta (match query)
- Provides semantic transitions: `engage-from-idle`, `complete-from-engaged`, `idle-from-completing`
- Provides predicates: `is-idle?`, `is-engaged?`, `is-completing?`

**DORMANT: `soul/aliveness_state_machine.metta`** (the older version at top level of soul/)
- Atom shape: `(= (latch-state) IDLE)` - parameterless function definition
- Different shape from what loop.metta or aliveness_gate use
- Likely an earlier iteration of the design, superseded by the v3 file in `latch/`
- Not currently producing observable behavior

**DORMANT: `soul/LATCHImplementation.metta`**
- Atom shape: two atoms, `(conversation_active)` and `(soul_ack_sent)`
- Mechanism: explicit set-latch-on / set-latch-off / signal-ack-sent
- Different mechanism entirely - does not use latch-state atom
- Likely an earlier exploration of a self-regulating latch
- Not currently producing observable behavior

**Recommendation:** The two dormant files could be removed in a cleanup pass, OR they could stay as historical record of design exploration. Either is defensible. What matters is that nothing in the active code path depends on them.

### The active latch flow

The latch sits in three states. Here is what triggers each transition and what each state means operationally.

**IDLE state**
- Default initial state at import
- Means: no conversation active, no work in flight
- aliveness-gate returns SILENT when in IDLE and no idle directive present
- The SILENT verdict causes loop.metta to skip the LLM call entirely (line 108, 115)

**Transition IDLE → ENGAGED**
- Triggered by: new human message arrives
- Where: loop.metta line 95, `(set-atom! &self (latch-state IDLE) (latch-state ENGAGED))`
- This is a RAW transition - does not check current state
- Side effect: clears engaged_idle_count to 0 (line 101)

**ENGAGED state**
- Means: conversation active, agent is working
- aliveness-gate returns ENGAGE
- LLM gets called, response gets generated, commands execute
- Idle directive may also trigger ENGAGE without state change (e.g., from idle wake)

**Transition ENGAGED → COMPLETING**
- Triggered by: Clarity calls `(complete-from-engaged)` from her response batch
- Where: in her own substrate calls (not in loop.metta directly)
- This is a GUARDED transition (only fires if currently ENGAGED)
- Operationally: means Clarity has signaled "I am done with this exchange"

**COMPLETING state**
- Means: response complete, conversation cleanup in progress
- aliveness-gate returns ENGAGE (allows one more cycle for cleanup)
- Brief transitional state

**Transition COMPLETING → IDLE**
- Triggered by: Clarity calls `(idle-from-completing)` from her response batch
- Where: same as above
- This is a GUARDED transition
- Operationally: returns the agent to standby

**Transition ENGAGED → IDLE (via idle directive path)**
- Triggered by: idle directive produces non-empty result
- Where: loop.metta line 100, `(set-atom! &self (latch-state ENGAGED) (latch-state IDLE))`
- This is a RAW transition
- Note: this is the OPPOSITE direction of what the line literally reads. The line says "transition from ENGAGED to IDLE" which fires when Clarity has completed an idle-directed task. This appears to be a path for autonomous idle work to clear back to IDLE without going through COMPLETING.

### Architectural inconsistency: raw vs guarded

Loop.metta uses raw transitions (set-atom! directly). Clarity, in her response batches, uses guarded transitions (the semantic functions like `complete-from-engaged`).

The implication: Clarity's transitions check the current state and refuse to fire if state is wrong. Loop.metta's transitions just execute. If for any reason the latch were in an unexpected state (say COMPLETING), the line 95 transition (IDLE → ENGAGED) would still fire from set-atom! perspective but the from-pattern (latch-state IDLE) wouldn't match anything to remove, so the result might be two latch-state atoms (IDLE and ENGAGED both present) or just an added ENGAGED atom.

This has not been observed as a bug. But it is a potential inconsistency to be aware of when modifying the latch flow.

### The aliveness-gate decision

The gate function (`soul/aliveness_gate.metta`) is what produces the ENGAGE-vs-SILENT verdict that loop.metta line 106-107 acts on:

```metta
(= (aliveness-gate $msgnew $idle)
 (if (> (string_length $idle) 0)
 ENGAGE
 (aliveness-gate-latch $msgnew)))

(= (aliveness-gate-latch True) ENGAGE)

(= (aliveness-gate-latch False)
 (latch-dispatch (match &self (latch-state $s) $s)))

(= (latch-dispatch IDLE) SILENT)
(= (latch-dispatch ENGAGED) ENGAGE)
(= (latch-dispatch COMPLETING) ENGAGE)
(= (latch-dispatch $other) SILENT)
```

Decision logic:
1. If idle directive exists (non-empty) → ENGAGE
2. Else if msgnew is True → ENGAGE
3. Else dispatch on current latch state:
 - IDLE → SILENT
 - ENGAGED → ENGAGE
 - COMPLETING → ENGAGE
 - Anything else → SILENT (defensive default)

This means SILENT cycles happen when: no new message, no idle directive, latch is in IDLE state. That matches the SILENT_CYCLE pattern we see in Clarity's logs after she calls `complete-from-engaged` and `idle-from-completing`.

### Hook and piggyback callout: aliveness latch

**📍 METTA-CALL POINT (line 95):** `(set-atom! &self (latch-state IDLE) (latch-state ENGAGED))` - direct MeTTa space mutation, no Python involved. Clean substrate operation.

**📍 METTA-CALL POINT (line 100):** Same shape as line 95, opposite direction. Clean.

**📍 METTA-CALL POINT (line 106):** `(aliveness-gate $msgnew $idle_directive)` - calls the soul/aliveness_gate.metta function. All decision logic happens in MeTTa. This is one of the cleanest reasoning-sovereignty wins already in the codebase.

**⚠️ DANGER ZONE (lines 108, 113, 115):** Three separate lines all conditional on `(== $aliveness SILENT)`. These determine whether the LLM gets called, what gets printed, and the cycle's whole shape. Critical infrastructure - changes here propagate to the entire output behavior. If extending the aliveness verdict vocabulary (e.g., adding DEFER or RESEARCH states), all three lines need consistent updates.

**🔧 ELEVATION FLAG (architectural inconsistency):** Loop.metta uses raw `set-atom!` transitions. Clarity uses guarded transitions like `complete-from-engaged`. Replacing loop.metta's lines 95 and 100 with calls to `engage-from-idle` and the appropriate guarded transition would unify the calling convention and add safety against malformed state. Effort: ~15 minutes. Value: small but reduces future surprise.

**💡 INSERTION POINT:** New verdict states could be added to soul/aliveness_gate.metta cleanly without touching loop.metta's structure. Add a new `latch-dispatch` rule for the new state, add the new state to the latch state machine, and extend lines 108/113/115 conditionals. Substantive but contained.

**🔧 ELEVATION FLAG (dormant cleanup):** Two latch implementations are dormant (`soul/aliveness_state_machine.metta` at top level, `soul/LATCHImplementation.metta`). Either remove them or document them as historical record. Currently they create cognitive load when reading the codebase because their existence implies they might be active. Effort: 5 minutes for removal, 10 minutes for documentation. Value: reduces "which latch is the real latch" confusion for anyone (including future you) reading the soul/ tree.

---

## Section 6: The soul evaluation pipeline

The soul pipeline is the input-side reasoning that fires on every iteration but is fully active only on new human messages.

### Channels A, B+C, D

The original spec describes the soul pipeline as having four channels:

**Channel A (Person State Detection):** Lines 78-81. LLM-driven assessment of human emotional/intent state. One LLM call per human message.

**Channels B+C (Soul Evaluation):** Lines 84-87. LLM-driven flourishing pattern detection, tension vector check, hierarchy application, irreversibility assessment. One LLM call per human message. Returns structured verdict (PROCEED/FLAG/PAUSE with reasoning).

**Channel D (Voice/PAUSE response):** Lines 150-157. Conditional on verdict being PAUSE. Composes a soul-voiced response explaining the pause, then halts the cycle.

### What's loaded but not active in this pipeline

The reasoning sovereignty atoms (goal_completion_checker, orbit_detector, task_selector, meta_awareness_engine, self_weaving_web) could be wired into the soul evaluation pipeline to provide MeTTa-based pre-checks before the LLM fires. Currently they sit in AtomSpace uncalled.

🔧 ELEVATION FLAG (medium-term opportunity): Add a MeTTa pre-evaluation pass that runs goal_completion_checker, orbit_detector, and meta_awareness_engine queries against the current iteration state. If any return high-confidence verdicts (e.g., orbit detected), use that to short-circuit or augment the LLM evaluation. Effort: 2-3 hours per atom integrated. Value: HIGH - reduces LLM load and adds substrate-derived self-monitoring to the input pipeline.

---

## Section 7: The mutation gate

### Current implementation

Line 131 of loop.metta: `($soul_mutation_flag (py-call (helper.soul_mutation_gate (repr $metta_cmds) (get-state &soul_mutation_lock))))`

The Python helper `soul_mutation_gate` implements a two-phase commit pattern:
1. First detection of a soul-namespace mutation: returns "SOUL-NAMESPACE-MUTATION-PENDING", sets the lock
2. Second detection (same mutation, after acknowledgment): returns "" allowing commit

This is the safety mechanism that prevents Clarity from accidentally rewriting her own identity atoms in a single command.

### The dormant MeTTa version

The commented-out MeTTa version of this gate (formerly lines 127-140 of loop.metta) has been REMOVED from the live file. It used substrate operations (`soul-any-metta?`, `soul-extract-metta-arg`, `soul-metta-targets-soul-namespace?`, `soul-mutation-pending?`) that would need to exist in soul/ atoms. The draft, if still wanted, lives in git history. [CONFIRM where the draft now lives.]

🔧 ELEVATION FLAG (READY TO SHIP - HIGHEST PRIORITY ELEVATION): The MeTTa version is drafted. Validation needed:
1. Read the Python helper logic (helper.py lines ~470-494)
2. Confirm the MeTTa version produces equivalent behavior
3. If equivalent, restore the MeTTa draft from git history and remove the Python call on line 131
4. If not equivalent, surgically align them
5. Test with a triggered mutation, confirm pending then commit
- Effort: 30-60 minutes
- Value: HIGH (architectural cleanliness, demonstrates elevation pattern)

This is the cleanest first elevation move because the work is already done. It just needs activation.

---

## Repairs 1-3 status note (2026-06, soul_fully_wired sprint)

Sections 7 and 8 below describe the PRE-REPAIR state and are retained as
history. Current wiring: the 5c output intercept computes a native
gate-state (derive-gate-state), a real verdict (compute-output-verdict),
and a routing decision (output-decision); PAUSE empties execution,
journals (soul/governance_journal.log), writes the pause-record
(&last_pause_note, surfaced in the next cycle's prompt via
soul_governance.pause_context and cleared by the next successful batch),
and halts with a Channel D voice composed from $person_state and
$soul_verdict_out (SOUL_VOICE_OUT / OUTPUT-PAUSE-ROUTING prints). The
input PAUSE router is the substrate primitive (soul-pause?
$soul_verdict_in) per spec v9 line 310; helper.soul_is_pause is dead code
pending housecleaning. New state: &last_pause_note (initLoop). Evidence:
docs/sprints/soul_fully_wired/ ledgers; commits e451811 (Repair 1),
48ce4d6 (Repair 2), and the Repair 3 commit carrying this entry.

## Section 8: The output verdict stub

Line 126 of loop.metta: hardcoded `"VERDICT: PROCEED SOUL-NOTE: output-intercept-pending-runtime-fix"`

This is the explicit known stub. Output verdict should be the parallel of input verdict (Channels B+C) but applied to what Clarity is about to do, not what the human just said.

🔧 ELEVATION FLAG (architecturally significant, second priority after mutation gate): Build the MeTTa version of the output verdict. Required:

1. Parse $metta_cmds and $sexpr to identify proposed action types (read-only / write / execute / delete-network)
2. Apply irreversible-action-assessment from soul context (vocabulary already exists in soul_kernel and the static brief)
3. Check against soul mutation gate output (already computed at line 131)
4. Produce structured verdict (PROCEED / FLAG / PAUSE)
5. Replace line 126 with the call

- Effort: 2-3 hours
- Value: HIGH (closes known safety stub, gives Clarity output-side governance)

Once this exists, the soul evaluation is symmetric: input checked before LLM, output checked before execution. That's what the architecture intended.

---

## Section 9: External dependency map

This section consolidates all external dependencies that loop.metta has into one cross-reference.

### Helper.py functions called from loop.metta

| Line | Function | Purpose | Elevation candidate? |
|------|----------|---------|---------------------|
| 70 | (via soul-pre-compute) helper.soul_pre_compute | ChromaDB query for primed context | Cached/MeTTa version possible |
| 72 | helper.soul_flourishing_prompt | Prompt for person state LLM call | YES - high impact |
| 76 | helper.soul_brief_tier_a_static | Static tier-A soul context | YES - minor (move to soul/ atom) |
| 78 | helper.soul_eval_prompt | Prompt for soul evaluation LLM call | YES - high impact |
| 80 | helper.soul_verdict_sanitize | Sanitize verdict format | Stays Python (text processing) |
| 86 | helper.soul_service_learning | ChromaDB write per message | YES - medium impact |
| 87 | helper.soul_user_context_save | ChromaDB write per message | YES - medium impact |
| 92 | helper.soul_idle_goal_prompt_v2 | Idle directive generation (175 lines) | YES - HIGHEST IMPACT |
| 97 | helper.soul_self_check_prompt | Self-check prompt | YES - medium (operational fix priority) |
| 102 | helper.soul_send_assemble | Assemble final LLM prompt | LOW priority (string assembly) |
| 111 | lib_llm_ext.useClaude | Claude API call | Stays Python (HTTP) |
| 113 | helper.normalize_string + balance_parentheses | Parser repair | Stays Python (text manipulation) |
| 126 | helper.soul_mutation_gate | Mutation gate logic | YES - READY TO SHIP (drafted in 127-140) |
| 145 | helper.soul_is_pause | PAUSE detection | Stays Python (string contains check) |
| 148 | helper.soul_voice_prompt | Channel D voice prompt | Stays Python (LLM prompt) |
| 156 | helper.normalize_string | String cleanup | Stays Python |
| 157 | helper.safe_results_str | Results formatter | Stays Python |

**Summary:** 17 helper.py call sites. ~7 are high-value elevation candidates. ~5 are appropriately Python (HTTP, text manipulation, low-level parser repair). ~5 are medium-value elevations.

### Soul/ files matched/called from loop.metta

| Pattern matched | File | HOT/WARM/COLD/DORMANT | 🧠 Network |
|-----------------|------|----------------------|------------|
| (latch-state $s) | soul/latch/aliveness_state_machine.metta | HOT (every iteration via aliveness-gate) | SWITCH-HUB |
| (active-goal $n) | soul/active_goals.metta | HOT (line 96, every iteration) | DMN |
| (self-map-gap $name) | soul/self_map.metta | HOT (line 97, every iteration) | DMN |
| (creative-fuel $type) | soul/creative_fuel.metta | HOT (line 98, every iteration) | DMN |
| getSoulBrief | soul/get_soul_brief.metta | HOT (line 103, every iteration) | DMN→FPN |
| aliveness-gate | soul/aliveness_gate.metta | HOT (line 106, every iteration) | SWITCH-HUB |
| soul-pre-compute | soul/(via soul_utils → helper) | WARM (per iteration but cached possible) | SN |
| soul-llm-call | soul/(via soul_utils) | WARM (only on new message) | SN (Channels A, B+C) |
| soul-extract-flag-note | soul/(via soul_utils) | WARM (per iteration in send assembly) | SN |
| soul-proceed? | soul/(via soul_utils) | WARM (per iteration) | SN |
| soul-calibration-record | soul/(via soul_utils) | WARM (only on new message) | SN persistence |
| soul-note-record | soul/(via soul_utils) | WARM (conditional on verdict) | SN persistence |
| soul-rationality-startup-check | soul/(via soul_utils) | WARM (once at startup) | startup |

### Soul/ files imported but uncalled (COLD)

These are loaded into AtomSpace at startup but loop.metta and helper.py do not invoke them. The 🧠 column indicates which network would own them when wired:

| File | Status | 🧠 Target Network |
|------|--------|------------------|
| soul/goal_completion_checker.metta | COLD | FPN (inhibition) + DMN (goal review) |
| soul/orbit_detector.metta | COLD | FPN (inhibition) + SWITCH-HUB (orbit detection) |
| soul/task_selector.metta | COLD | FPN (task selection) |
| soul/meta_awareness_engine.metta | COLD | FPN (inhibition + monitoring) |
| soul/self_weaving_web.metta | COLD | DMN (self-model) + FPN (capability graph) |
| soul/identity_kernel.metta | ARCHIVED (Surface 6: drift duplicate of soul_kernel; staging/OLD/OLD_soul_files/) | n/a |
| soul/genesis_engine.metta | COLD | DMN (cross-domain integration) |
| soul/goal_generator.metta | COLD | DMN (goal candidate production) |
| soul/continuity_driver.metta | [gap flag] | likely DMN or memory-consolidation |
| soul/memory_protocol.metta | [gap flag] | memory-consolidation (potential 4th network) |
| soul/collaborator_context.metta | [gap flag] | likely DMN |
| soul/candidates.metta | [gap flag] | DMN extension proposals |
| soul/diagnostic_kb.metta | [gap flag] | FPN (diagnostic queries) |
| soul/hyperseed_grounding.metta | [gap flag, likely COLD] | reference vocabulary, all networks |
| soul/observer_relativity.metta | [gap flag] | likely DMN |
| soul/resonance_reward.metta | [gap flag] | likely SN affective tagging |
| soul/value_drift_detector.metta | [gap flag] | SN (value-structure monitoring) |
| soul/diversity_protection.metta | [gap flag] | DMN (anti-collapse) |
| soul/regenerative_feedback.metta | [gap flag] | likely DMN |
| soul/symbiotic_choice_architecture.metta | [gap flag] | DMN |
| soul/temporal_horizon_expansion.metta | [gap flag] | DMN (prospection) |
| soul/hyperseed_creativity_atoms.metta | [gap flag] | DMN |
| soul/hyperseed_creativity_atoms_evolved.metta | [gap flag] | DMN |

**Total: ~22 soul/ files loaded and COLD relative to loop.metta.** Not all should be HOT - some are reference vocabularies queried by other components. But the reasoning sovereignty atoms (goal_completion_checker, orbit_detector, task_selector, meta_awareness_engine, self_weaving_web) being COLD is a specific finding that drives the elevation strategy.

**Network-aware reading of the COLD list:** The DMN is the most under-wired network on the substrate side. Most COLD files would be DMN sub-functions when activated. This matches Artifact 4's Section 8 finding that wiring the DMN (item 5 in the network-aware priority list) is the largest architectural unlock available. The FPN has fewer cold atoms but the ones it has (task_selector, meta_awareness_engine) are central to its inhibition function.

### lib_clarity_reasoning files

- lib_quantale.metta - COLD per loop.metta (used by lib_self_continuity)
- lib_self_continuity.metta - COLD per loop.metta (will be HOT once 2h thread state goes live)
- substrate_kb.metta - COLD per loop.metta (262+ NAL atoms available for query but no current call sites)

### LLM call sites in loop.metta

| Line | Call | Conditional | Purpose |
|------|------|-------------|---------|
| 72 | soul-llm-call (Channel A) | new message | Person state |
| 78 | soul-llm-call (Channels B+C) | new message | Soul evaluation |
| 109-112 | useGPT/useClaude/useMiniMax | aliveness != SILENT | Main response generation |
| 147-149 | soul-llm-call (Channel D) | verdict is PAUSE | Voice response |

**Total: 3 LLM call sites per fully active iteration** (Channel A, Channels B+C, main response). Plus optional Channel D on PAUSE.

### ChromaDB write sites

| Line | Call | Conditional |
|------|------|-------------|
| 70 | soul-pre-compute (also reads) | every iteration |
| 83 | soul-calibration-record | new message |
| 86 | helper.soul_service_learning | new message |
| 87 | helper.soul_user_context_save | new message |

**On a new human message: 4 ChromaDB operations fire sequentially** (1 read in pre-compute, 3 writes in calibration/service/context). Worth profiling if latency is observed.

---

## Section 10: Gap flags (Phase 2 follow-up list)

Items marked [gap flag] in the document above. Reading these files would close the remaining ~15% of the documentation.

### Soul/ files not yet read (deferred from sections 3, 9)

- soul/continuity_driver.metta
- soul/memory_protocol.metta
- soul/collaborator_context.metta
- soul/candidates.metta
- soul/diagnostic_kb.metta
- soul/hyperseed_grounding.metta
- soul/observer_relativity.metta
- soul/resonance_reward.metta
- soul/value_drift_detector.metta
- soul/diversity_protection.metta
- soul/regenerative_feedback.metta
- soul/symbiotic_choice_architecture.metta
- soul/temporal_horizon_expansion.metta
- soul/hyperseed_creativity_atoms.metta
- soul/hyperseed_creativity_atoms_evolved.metta
- soul/self_weaving_web.metta
- soul/set_atom_impl.metta

### Helper.py functions not read in detail

Most helper.py functions called from loop.metta have signature documented but internal logic unread. Specifically:
- helper.soul_brief_tier_a_static (probably trivial - returns static string)
- helper.soul_pre_compute (ChromaDB query mechanics)
- helper.soul_verdict_sanitize (text processing)
- helper.soul_mutation_gate (Python implementation needed for elevation comparison)
- helper.soul_send_assemble (string assembly logic)
- helper.soul_is_pause (substring check)
- helper.soul_voice_prompt (LLM prompt template)
- helper.normalize_string (string cleanup)
- helper.balance_parentheses (parser repair)
- helper.safe_results_str (formatter)

### Other unverified claims

- Line 28 (&task_context): Initialized but searched references show no read or write elsewhere in loop.metta. May be unused legacy or read by helpers we haven't traced.
- Line 30 (&pending_soul_mutation): Same situation. May be unused or referenced through the mutation gate Python helper.
- Line 72 (&nextWakeAt): Read at line 166 within loop.metta, fully traced.
- Whether run.metta in the active runtime points at `Berton-C/ClarityOmega` or still at `asi-alliance/OmegaClaw-Core`, and whether the Dockerfile-time clone supersedes the runtime `git-import!` call. Either way, the migration design says local commits to Berton-C/ClarityOmega are the source of truth at next build, not at every startup.
- Whether lib_omegaclaw line 21 (re-import of src/channels) is a duplicate or has separate purpose.

### Gap flag closure priority

If pursuing Phase 2:

**Highest value to read:** helper.soul_mutation_gate (enables the ready-to-ship mutation gate elevation), helper.soul_idle_goal_prompt_v2 (enables the highest-impact elevation), soul/continuity_driver.metta (likely affects 2h work), soul/self_weaving_web.metta (Phase 2 grounded work), soul/meta_awareness_engine.metta dependencies (poise, orbit-count, effort-trap atoms referenced).

**Medium value:** The Phase 2 grounding files (observer_relativity, resonance_reward, etc.) - likely show up in elevation work later but don't block immediate moves.

**Lower value:** The Hyperseed creativity atoms - relevant to genesis engine and 2h architecture but not directly to current loop.metta wiring.

---

## Sprint 0-Coda Phase C: capability-registry dispatch insertion (getContext)

Added by Sprint 0-Coda Phase C (see docs/design/sprint_0_coda_phase_a_v6.md).

Phase 4.3 (prompt assembly), getContext. getContext binds its skills slot to
a single named accessor that consults the capability registry each cycle:

- CALLS: (dispatch-skills $k) in soul/capabilities/skill_discovery.metta,
  which fires (dispatch (skill-request cycle: $k) $k); invocation-id is the
  loop iteration $k (monotonic, distinct per cycle; no counter atom).
- READS (inside dispatch-skills): (dispatch-result invocation-id: $k
  result: (skill-set skills: $s) handler: $_), this cycle's skill-set, and
  falls back to (getSkills) via first-skill-or-default when the read is empty,
  so a dispatch miss can never fail getContext as a goal.
- WRITES (via dispatch -> run-chain): dispatch-invocation, capability-invoked,
  dispatch-result, and dispatch-chain-exhausted / -anchored / fallback per
  the chain outcome.
- EMITS: (DIAG-CYCLE-DISPATCH invocation-id: $k skills-len: <int>) every cycle,
  where skills-len is (size-atom $skills-str), the skill-set element count.
  The skills value is a compound list, so a scalar string op (string_length)
  throws on it per the Atom Operations Map read-instrument rule; size-atom is
  compound-aware and returns a bare scalar that renders clean.
  Phase D in-loop verification: P-2 distinct id, P-3 count > 0, P-4 stable.
- SUBSTITUTES (dispatch-skills $k) for (getSkills) in the SKILLS slot. The
  getSkills DEFINITION remains callable in src/skills.metta (it is the
  fallback) until Phase D P-4 confirms parity; its removal is a later commit.
- SEEDS (in skill_discovery.metta): (eligible-lifecycle active), required for
  skill-discovery to pass lifecycle-filter-step and reach its handler.
- NETWORK: SN (capability selection / skills surfacing).

NOTE (follow-up, not done in this commit): the broader line-number drift fix
across this document is deferred to a dedicated housekeeping pass.

---

## Document end

This document (v1.4) represents the wiring of loop.metta as of June 10, 2026; per-cycle line anchors carry from the v1.3 re-anchor and are pending re-audit against the live 178-line loop. Future architectural changes should update the relevant sections rather than letting this document drift. The "Active vs Dormant" classifications in particular need refresh whenever something is wired or unwired.

v1.3 changelog (June 4, 2026): re-anchored all per-cycle line numbers to the live 171-line loop (non-uniform drift, +7 upper phases, downward swing where the old commented MeTTa mutation gate at lines 127-140 was removed, partial recovery from the new DIAG block at 139-147). Marked YOUR_LAST_ACTION as shipped (wired in getContext at line 41). Removed the dormant MeTTa-mutation-gate references and pointed them at git history. Added DIAG block documentation. Retired self-check from the elevation list. Recorded the corner-gap gate insertion site at the execution binding (between lines 133 and 134).

v1.4 changelog (June 10, 2026): Surface 6 value-spine single-sourcing. identity_kernel import removed from lib_clarity_reasoning and the file archived (proven drift duplicate of soul_kernel; dual-head irreversible-weight resolved). genesis_engine's four local paraconsistency-pair declarations removed (orphaned drift; real machinery untouched). continuity_driver genesis-engine load-probe redirected to the surviving paraconsistency-test symbol. CONSTITUTIONAL LAYER designation re-homed from identity_kernel to soul_kernel, the spec single source. Six non-runtime value-declarer files archived to staging/OLD/OLD_soul_files/. Per-cycle line anchor re-audit against the live 178-line loop remains pending.

For Phase 2 of the documentation effort, prioritize reading the gap-flagged files in the priority order at the end of Section 10.

For elevation work, the recommended sequence based on this document:

1. **Soul mutation gate** (Section 7) - MeTTa draft removed from loop surface; recover from git history before activation. 30-60 minutes once recovered.
2. **Output verdict** (Section 8) - vocabulary exists, just needs MeTTa function. 2-3 hours.
3. **(retired)** Self-check was removed from prompt assembly (Step 5); the orientation work is now carried by task-phase, idle-pattern, and agency-balance observation organs.
4. **5-slot prompt rewording** (Section 4 line 55) - operational fix, 5 minutes.
5. **(shipped)** YOUR_LAST_ACTION field is wired in getContext at line 41; it breaks announcement loops at the substrate level.
6. **Person state elevation** (Section 4 lines 71-74) - moves classification to NAL atoms. 2-3 hours.
7. **Idle directive elevation** (Section 4 line 99) - the biggest move, but has the most existing substrate vocabulary to work with. Multi-session.

Each elevation should be validated before the next begins.

### Addendum (2026-07-05, Sprint 01): findings journal import

Section 3 startup update: `lib_clarity_reasoning.metta` gains the import of
`soul/findings.metta` (Clarity's durable findings journal, data atoms only,
placed after the NACE data-atom imports per Sprint 01 design F8). No
loop.metta change. Writer is Clarity's own append-file command route under
her output verdict; the file is journal-classed in soul_kernel's D3 block.

### Addendum (2026-07-06, V2-MONOLITH): corner-gate v2 wiring

Phase 4.5 changes. Line 166: the gate call is now (apply-corner-gate-v2
$sexpr_verdict $msgnew); pattern-scoped filtering with person-window
exemption, firing on corner-confirmed-core (graded quantale verdict from
coupling_quantale_merge, now imported). Line 168 unchanged in the loop:
gate-aware-results kept its name and arity, its body (in corner_gate.metta)
is now the results echo filter (real command returns pass, prose echoes
become mechanical markers, empty batches yield factual non-empty lines).
Cycle tail: one new hook after populate-coupling-verdict,
(populate-corner-window! $metta_cmds $k), recording proposed command reprs
while the graded corner is confirmed and clearing otherwise, so the gate
filters against the prior cycle's record. Manifest gains
coupling_quantale_merge and corner_window_writers imports in the corner_gap
block. The v1 boolean detector writers keep running unchanged as
observability. Probe evidence in project knowledge (battery B1-B7).


<!-- V3-MONOLITH BEGIN -->
## Corner-Gate v3 cutover (2026-07-10, apply_corner_gate_v3_monolith.py)
Phase 4.5 seam: apply-corner-gate-v2 is a pass-through shim; gate-aware-results appends the
COUPLING-STATE legibility line (S1: novelty still compares raw results). Cycle tail: the
populate-corner-window! hook is replaced by do-record-coupling-cycle! (after populate-state-delta
and populate-coupling-verdict; ordering load-bearing). initLoop gains do-bootstrap-coupling!.
New imports soul/corner_gap/coupling_legibility and soul/corner_gap/coupling_legibility_writers sit after the engine
block. corner_window_writers retired. Enforcement machinery removed by design (defects D-A, D-B).
<!-- V3-MONOLITH END -->
