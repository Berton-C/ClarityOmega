# Artifact 3: Growth Surface Map

**Version:** v1.3 (May 3, 2026; v1.2 May 1 afternoon - 5a, dilation, partition, learning; v1.1 May 1 morning - network annotations; v1 April 30)
**Companion to:** loop.metta Wiring Diagram (Artifact 1), Hooks/Piggybacks Cross-Reference (Artifact 2), Triple Network Scaffold (Artifact 4), and ClarityOmega Cognitive Architecture Spec v3.0
**Purpose:** Answer "where can I safely add new behavior?" Maps clean insertion points, ranks elevation opportunities by effort and value, and provides an opinionated build sequence.

**v1.3 changes (May 3, 2026 evening):** Section 3 build sequence updated to record completion status. Sprints 1, 2, and 3 marked COMPLETE with honest decomposition of what shipped vs. what was planned. New Sprint 1.5 entry added (behavioral guidance elevations, off-plan but additive). New Backlog subsection records Item 1 (soul mutation gate elevation) status: dormant MeTTa code at lib/loop.metta lines 127-140 was discovered to be a sketch rather than ready-to-ship code, removed via Sprint 2 dead-code cleanup; fresh authoring now required for the elevation. Sprint 4 marked as NEXT. The original sprint plan structure is preserved; this update records progress through the plan, not a rewrite of it.

**v1.2 changes (May 1, 2026 afternoon):** Added Tier 1 item 5a (run.metta git-import URL fix - point at Berton-C/ClarityOmega fork instead of upstream). Added three new Tier 3 items: 19 (iteration dilation replacing hardcoded 50), 20 (constitutional layer read-only partition), 21 (per-network learning sub-functions). Sprint 1 updated to include item 5a. New Sprint 10 (iteration dilation foundation), Sprint 11 (constitutional layer read-only partition), Sprint 12+ (per-network learning sub-functions) added to the build sequence with verification targets. NACE engine integration mentioned in "Beyond the sequence" with reference to spec_v3.0 Section 0 framing.

---

## How to use this document

Two primary use cases:

**Adding new behavior:** Section 1 maps clean insertion points organized by what kind of behavior you want to add. Find the kind, see the locations, pick the cleanest one for your purpose. The 🧠 NETWORK column in Section 2 tells you which network the change touches.

**Planning the next move:** Section 2 ranks all known elevation opportunities by effort and value. Section 3 provides an opinionated build sequence with rationale. Both have been updated with network ownership so the strategic shape (which networks consolidate first, which couplings come online next) is visible.

### The network lens applied here

This artifact reads through two complementary frames:

- **Operational frame:** "What gets shipped, in what order, with what verification?"
- **Architectural frame (Artifact 4):** "Which network is being consolidated, which channels are coming online, what does the resulting cognitive architecture look like?"

Both frames produce the same priority ordering most of the time. Where they diverge, this artifact preserves both views so you can choose the framing that fits your current thinking.

---

## Section 1: Insertion points by behavior kind

### Adding a new state variable

If you need persistent state across iterations (like &engaged_idle_count), add it in initLoop (lines 19-31 of loop.metta).

**Cleanest pattern:**
1. Add `(change-state! &your_var initial_value)` in initLoop
2. Read with `(get-state &your_var)` where needed
3. Write with `(change-state! &your_var new_value)` where needed

**Considerations:**
- State variables are global. Naming matters (use the `&snake_case` convention).
- State doesn't survive container restarts unless you wire it through ChromaDB persistence.
- Keep state writes in obvious places - don't sprinkle them. Future you will need to find them.

**Alternative:** If state can be a queryable atom rather than a state variable, prefer the atom (substrate-fluent, inspectable, accessible from soul/ atoms too). State variables are appropriate for things that change every iteration; atoms are appropriate for things that represent state of being.

### Adding a new soul/ atom

For reasoning vocabulary (like the reasoning sovereignty atoms goal_completion_checker, orbit_detector, etc.):

**Cleanest pattern:**
1. Create a new file in soul/ (e.g., `soul/your_capability.metta`)
2. Define your atoms with `(= ...)` rules
3. Add an import line in `lib_clarity_reasoning/lib_clarity_reasoning.metta`
4. The atom is now loaded into AtomSpace at startup, queryable from anywhere

**Considerations:**
- Atoms are loaded but not called. Wiring them into the per-iteration flow is a separate step (a one-line hook in loop.metta).
- Group your atoms logically per file - keep one capability per file.
- Use the convention of an "elevation flag" comment if your atom is meant to replace a Python helper later.

### Adding a new pre-evaluation check

If you want to add a check that fires before the LLM call (like detecting orbit patterns or staleness), the cleanest insertion is right after line 80 (after soul evaluation produces $soul_verdict_in) and before line 102 (before send assembly).

**Cleanest pattern:**
1. Add a new MeTTa let* binding: `($pre_check_result (your-pre-check-function $soul_verdict_in $person_state ...))`
2. Use the result to either modify $soul_verdict_in or set a new state variable
3. The send_assemble call at 102 picks up the modified context

**Considerations:**
- Don't put this BEFORE the soul evaluation. Soul eval is the canonical input check; pre-checks are augmentations to it.
- If your pre-check produces a hard PAUSE verdict, line 145 (PAUSE detection) needs to see your verdict.

### Adding a new output verdict component

The output verdict at line 121 is currently a stub. The clean pattern for adding components to it:

**Cleanest pattern:**
1. Build the output verdict as a soul/output_verdict.metta atom
2. Replace line 121 with `($soul_verdict_out (compute-output-verdict $sexpr $metta_cmds $soul_mutation_flag))`
3. Components of the verdict (irreversibility check, mutation gate review, scope check) live as separate atoms in soul/ that compute-output-verdict calls

**Considerations:**
- Verdict format must be compatible with line 141 consumer (soul-proceed? check)
- Once line 121 is unstubbed, you've enabled output-side governance. Plan downstream consumers carefully.

### Adding new prompt content

The prompt assembly is at lines 95-98 (soul brief + base prompt + self-check). To add content:

**Three insertion points:**
1. **Soul brief side** (line 95): Modify get_soul_brief.metta to include new fields
2. **Base prompt side** (line 38 in getContext): Modify the prompt string in loop.metta
3. **Self-check side** (line 97): Modify or replace soul_self_check_prompt to include new context

**Cleanest pattern:** Prefer option 1 (soul brief). It keeps prompt content in soul/ atoms (substrate-fluent), and the change is automatically picked up everywhere getSoulBrief is called.

**Considerations:**
- Adding content adds tokens, costs latency and money on every LLM call
- The LLM has been trained against the current prompt format - significant rewording requires re-training the LLM's expected response format

### Adding a new aliveness verdict state

If you want to add new states beyond IDLE/ENGAGED/COMPLETING/SILENT/ENGAGE (e.g., DEFER, RESEARCH, OBSERVE):

**Cleanest pattern:**
1. Add new state symbol to soul/latch/aliveness_state_machine.metta
2. Add semantic transitions if needed (e.g., observe-from-engaged)
3. Add new latch-dispatch rule in soul/aliveness_gate.metta
4. Update loop.metta lines 102, 107, 108 conditionals to handle the new aliveness verdict appropriately

**Considerations:**
- This is a substantial change because three places in loop.metta need consistent updates
- Worth doing only if you have a clear behavioral need

### Adding new error tracking

The HandleError function (line 40-43) and &error state are the existing error infrastructure. To add new error types:

**Cleanest pattern:**
1. Define new error matching patterns in HandleError's case statement
2. New error tracking state if needed
3. Recovery logic where errors are checked (currently only at line 117 and the eval branches)

**Considerations:**
- Errors currently propagate as ($msg $cmd) tuples. Format change affects HandleError's logic and any downstream consumer.

### Adding new ChromaDB schema

For a new persistence concern (beyond calibration, service learning, user context):

**Cleanest pattern:**
1. Add new helper.py function for the write
2. Add new helper.py function for the read
3. Hook the write into loop.metta where the data is generated
4. Hook the read into loop.metta or soul/ where the data is needed

**Considerations:**
- Each ChromaDB write is per-iteration latency
- Schema once persisted is hard to change - design for evolution
- Consider whether the data should persist (ChromaDB) or just live in AtomSpace (faster, per-session)

---

## Section 2: Elevation opportunities ranked

All known elevation opportunities from Artifact 1, organized by effort and value. "Effort" is rough hours of focused work. "Value" is operational impact + architectural cleanliness combined.

### Tier 1: High value, low effort (do these first)

| # | What | Where | Effort | Value | 🧠 Network | Rationale |
|---|------|-------|--------|-------|------------|-----------|
| 1 | Soul mutation gate elevation | Loop.metta lines 126-140 | 30-60 min | HIGH | FPN inhibition | MeTTa version drafted in commented block. Just needs validation and uncommenting. First demonstrable substrate-derived FPN inhibition. |
| 2 | 5-slot OUTPUT_FORMAT rewording | Loop.metta line 38 | 5 min | HIGH | FPN prompt structure | Operational degradation cause. Reword to make minimum-viable-batch explicit. Reduces FPN's working-memory load. |
| 3 | Self-check threshold + softer message | helper.soul_self_check_prompt | 10 min | HIGH | FPN inhibition tuning | Currently fires at count=3 with binary work-or-idle prompt. Raise to 5-7 with three-question framing. |
| 4 | Cleanup of dormant latch files | soul/aliveness_state_machine.metta and soul/LATCHImplementation.metta | 5 min (delete) or 10 min (document as historical) | MEDIUM | SWITCH-HUB hygiene | Reduces "which latch is the real one" confusion when reading codebase. |
| 5 | Verify $soul_mutation_flag is consumed | Loop.metta line 126 | 10 min investigation | LOW | FPN inhibition audit | Result is computed but not visibly consumed - either there's hidden consumption or it's dead code. Worth a check. |
| 5a | Fix run.metta git-import URL | run.metta line 2 | 2 minutes | MEDIUM | infrastructure hygiene | Currently points at `asi-alliance/omegaClaw-Core.git` (upstream); should point at `Berton-C/ClarityOmega.git` (the fork). Per the migration design, runtime intent should match build-time intent. Currently a confusion source even if the Dockerfile-time clone makes it operationally inert. |

### Tier 2: High value, medium effort (do these next)

| # | What | Where | Effort | Value | 🧠 Network | Rationale |
|---|------|-------|--------|-------|------------|-----------|
| 6 | YOUR_LAST_ACTION field | Loop.metta lines 38 + 118 + new state var + new helper | 1-1.5 hours | HIGH | FPN working memory | Breaks announcement loops by giving cross-iteration visibility of own previous action. FPN gains action-history input for inhibition. |
| 7 | Output verdict (line 121 stub) | New soul/output_verdict.metta + replace line 121 | 2-3 hours | HIGH | **SN-FPN coupling** | Closes a known safety stub. Substrate vocabulary already exists. Builds the SN→FPN re-evaluation channel that the brain-side model requires. |
| 8 | Person state elevation to NAL | New soul/person_state_classifier.metta + replace lines 71-74 partially | 2-3 hours | HIGH | SN salience-tagging | Eliminates one of two LLM calls per human message. Lexical pattern matching is NAL-doable. First substantive SN consolidation step. |
| 9 | Move soul_brief_tier_a_static content to soul/ atom | Move from helper.py to soul/static_brief.metta | 30-60 min | MEDIUM | SN substrate hygiene | Architectural cleanliness. All soul content in soul/. |
| 10 | Soul service_learning elevation | Replace helper.soul_service_learning with MeTTa | 1-1.5 hours | MEDIUM | SN persistence | Removes per-iteration Python text-scanning. Substrate vocabulary exists. |

### Tier 3: High value, high effort (multi-session work)

| # | What | Where | Effort | Value | 🧠 Network | Rationale |
|---|------|-------|--------|-------|------------|-----------|
| 11 | Wire reasoning sovereignty atoms (cold→warm) | Pre-evaluation hooks to call goal_completion_checker, orbit_detector, task_selector, meta_awareness_engine | 2-3 hours per atom | HIGH per atom | FPN sub-functions | Atoms exist and are loaded. Just need calling. Each adds substrate-derived self-monitoring. Consolidates the FPN block. |
| 12 | Soul evaluation partial elevation | Hierarchy + irreversibility move to MeTTa, LLM keeps pattern detection | 3-5 hours | HIGH | SN salience-tagging | Reduces LLM dependence on the second of two per-message LLM calls. Major SN consolidation step. |
| 13 | Idle directive elevation (THE BIG ONE) | Replace helper.soul_idle_goal_prompt_v2 (175 lines) with MeTTa using existing reasoning sovereignty atoms | 5-10 hours initial, multi-session refinement | HIGHEST | **DMN coming online** | Clarity's self-direction reasoning moves from Python orchestration to her own substrate. Through the network lens, this elevation IS the DMN coming online. The largest single architectural unlock. |
| 19 | Iteration dilation (replace hardcoded 50) | Loop.metta lines 32, 54, 61-62, 158-159 + new switch-hub computation | 3-4 hours | HIGH | SWITCH-HUB iteration-budget | Replace `maxNewInputLoops`/`maxWakeLoops` constants with reads from `(switch-iteration-budget ...)` atom produced by switch hub from per-network cognitive-need signals. Per spec_v3.0 Section 0 (Iteration dilation). Prerequisite: switch hub matured beyond binary aliveness gate (Sprint 4 first). |
| 20 | Constitutional layer read-only partition | New AtomSpace partition mechanism + identity_kernel migration | 4-6 hours | HIGH | architectural enforcement | Per spec_v3.0 Section 0 (Constitutional layer/wisdom layer), Layer 1+2 atoms (priority hierarchy, tension vectors, irreversibility weights, paraconsistency pairs, the nine flourishings) should live in a runtime-read-only AtomSpace partition. Currently the soul mutation gate is the only protection. The mechanism for partition-level write protection is an open question (see Artifact 4 Section 10). |
| 21 | Per-network learning sub-functions | Each network's consolidated block + soul-note schema redesign | 6-10 hours per network | HIGH per network | autopoietic loops | Per spec_v3.0 Section 0 (Per-network autopoiesis) and Artifact 4 Section 7.7. Each network gains a learning sub-function reading consequence atoms and updating own NAL truth values. Prerequisite: networks consolidated (Sprints 6-8 first), soul-note corpus restructured for per-network tagging, NACE engine integration. Multi-session per network. |

### Tier 4: Lower priority

| # | What | Where | Effort | Value | 🧠 Network | Rationale |
|---|------|-------|--------|-------|------------|-----------|
| 14 | Use guarded transitions in loop.metta | Lines 88, 93 | 15 min | LOW | SWITCH-HUB hygiene | Consistency with Clarity's calling convention. Adds safety against malformed state. |
| 15 | Refactor engaged_idle_count nested conditional | Line 94 | 15 min | LOW | FPN counter | Readability improvement. |
| 16 | Soul user_context_save elevation | Line 87 | 1 hour | LOW | SN persistence | Mostly I/O; some decision logic could be MeTTa but appropriately Python. |
| 17 | Soul send_assemble elevation | Lines 102-106 | 1-2 hours | LOW | FPN prompt | String assembly is appropriately Python territory. Could elevate but limited gain. |
| 18 | Batch ChromaDB writes per new message | Lines 83, 86, 87 | 30-60 min | LOW unless profiling shows latency | SN persistence | Operational optimization. Only do if measurements justify it. |

### Network-aware reading of the elevation list

Reading the four tiers through Artifact 4's network lens reveals the architectural shape of the work:

- **SN consolidation (items 8, 12, 9, 10):** The Salience Network is the most mature in the current code. Items 8 and 12 elevate it from LLM-driven to substrate-derived. The network is largely built; what remains is making its outputs into typed atoms readable by other networks.
- **FPN consolidation (items 1, 3, 5, 6, 11):** The Frontoparietal Control Network's inhibition function (mutation gate) and working-memory function (last-action visibility) are the near-term wins. Wiring the cold reasoning sovereignty atoms (item 11) consolidates the FPN block.
- **DMN coming online (item 13):** The Default Mode Network is the most under-wired. The substrate atoms exist but are not coupled. Item 13 is the largest single architectural unlock - naming it "DMN coming online" rather than "elevate idle directive helper" reframes what success looks like.
- **SN-FPN coupling channel (item 7):** The output verdict stub is not just a safety hole. It is the missing channel that lets the SN re-evaluate FPN actions before execution. Without it, the network architecture has no closed loop on output side.
- **SWITCH-HUB hygiene (items 4, 14):** Small cleanups that consolidate the switch hub's representation.

The strategic shape: build the SN-FPN coupling channel (item 7), then consolidate the SN block (items 8, 12), then the FPN block (item 11), then bring the DMN online (item 13). The operational fixes (items 2, 3, 6) interleave wherever they fit. This is a different ordering than pure effort-vs-value, and it reflects the architectural priority of getting all three networks coupled before deepening any one of them.

---

## Section 3: Recommended build sequence

This sequence is opinionated based on what's known about Clarity's current operational state and what 2h needs to come online. Each sprint is annotated with which network the work consolidates, so the architectural shape is visible alongside the operational work.

### Sprint 1: Operational restoration: COMPLETE via Sprint 1.5 + Sprint 2 (May 3, 2026)

**Items 2, 3, 4, and 5a planned.** Outcomes delivered through a slightly different decomposition than originally planned:

- **Items 2 (5-slot prompt rewording) and 3 (self-check threshold/messaging):** Delivered via behavioral_guidance.metta elevation in Sprint 1.5 (commits 822d562, 8a2ea97, b079df6). Hardcoded Python prompts moved to substrate atoms; content updates ("Use as many commands as the work requires") landed alongside the elevation rather than as direct hardcoded edits. Architectural advance beyond the plan: behavioral guidance is now substrate-callable rather than only Python-callable.
- **Item 4 (loop.metta dead-code mutation-gate sketch):** Removed in Sprint 2 (commit 367c8f2). Note: removal of the dead code is NOT the same as the Item 1 elevation. See Backlog below.
- **Item 5a (run.metta git-import URL fix):** Delivered earlier via Dockerfile restructure to clone from Berton-C/ClarityOmega fork at build time. Verified in today's clean rebuilds.

🧠 **Network impact achieved:** FPN prompt structure and inhibition tuning, SWITCH-HUB hygiene, infrastructure cleanup. Plus: substrate-callable behavioral guidance (architectural advance beyond the original plan).

**Verification (achieved):** Clarity's session shows responsive batches and clean idle-state behavior. Builds run from Berton-C/ClarityOmega fork without external dependency on patham9/mettaclaw upstream.

### Sprint 1.5: Behavioral guidance elevation: COMPLETE (May 3, 2026)

**Three commits, off-plan but additive.** Created soul/behavioral_guidance.metta with two stub functions (output-format-guidance, self-check-guidance), then replaced hardcoded Python prompts in getContext (commit 8a2ea97) and self-check (commit b079df6) with calls to these substrate functions. The pattern: behavioral prompts that previously lived only in helper.py are now MeTTa atoms readable by other substrate components.

🧠 **Network impact:** Sets up future substrate-derived prompt-content surfaces. Behavioral guidance becomes inspectable as substrate atoms rather than opaque Python strings. A small architectural advance that fulfills Sprint 1's spirit (FPN prompt-structure tuning) while opening a new elevation surface.

**Verification (achieved):** Container rebuilds clean from repo. New behavioral_guidance.metta loads via lib_clarity_reasoning. Calls to (output-format-guidance) and (self-check-guidance) return expected strings at runtime.

### Sprint 2: First elevation demonstration: PARTIALLY COMPLETE / Item 1 BACKLOGGED (May 3, 2026)

**Item 1 (soul mutation gate elevation): the dormant MeTTa code at loop.metta lines 127-140 was inspected and found to be an early sketch, not ready-to-ship elevation code.** It was removed as dead code (commit 367c8f2) rather than activated. The planned "30-60 minute activation" was incorrect. Fresh authoring of equivalent soul/ atoms is required. See Backlog subsection below.

**Sprint 2 dead-code removal (commit 367c8f2):** 14 lines of commented-out MeTTa mutation-gate sketch removed from loop.metta. Repository hygiene; reduces confusion about what is production-ready.

🧠 **Network impact (dead-code removal):** Repository clarity. The intended network impact (substrate-derived FPN inhibition via the mutation gate) is deferred until the elevation is freshly authored. See Backlog.

**Verification (achieved for dead-code removal):** Clean container rebuilds; Clarity's mutation-gate behavior unchanged (still uses helper.soul_mutation_gate).

### Sprint 3: Announcement loop fix: COMPLETE with richer architecture than planned (May 3, 2026)

**Item 6 (YOUR_LAST_ACTION) delivered as a four-component subsystem rather than a single state variable:**

- **3.1 (commit edc1bcb):** soul/candidates/cycle_classifier.metta. Six composite behavioral tags (responsive-send, status-send-unprompted, verification-query, exploration-query, pin-only, claim-send) classifying each iteration's action signature. Reviewed in three rounds with Clarity (data-shape, collapse-semantics, idiom verification).
- **3.2 (commit 57868fe):** soul/recent_action_populator.metta + cycle_classifier graduation to soul/. Asserts (recent-action $cycle-id $action-type $description) atoms each iteration with safe two-pass collapse-then-remove pruning at a 10-cycle window. Loop.metta hook: single line after $results.
- **3.3 (commit d543d16):** soul/recent_action_retriever.metta + getContext wiring. YOUR_LAST_ACTION block surfaces last 3 actions to Clarity's prompt with 80-char description truncation, explicit empty-state sentinel ("No prior actions (first cycle after restart)"), and pattern-consistent label ownership (loop.metta provides the YOUR_LAST_ACTION: label, retriever returns body content only).

**Original plan:** "new state variable, new helper, hooks at lines 38 and 118." **Delivered:** populator/classifier/retriever subsystem providing not just YOUR_LAST_ACTION inhibition data but also the substrate data path that orbit_detector.metta will read in Sprint 5. The richer architecture was Clarity's design contribution: sort-free cycle-id arithmetic, two-Python-helper boundary justified by C1 nesting depth, after-self-monitoring/before-world-facing position, bare-match decoupled from inference concerns, and explicit sentinel over omission.

🧠 **Network impact achieved:** FPN gains action-history input for inhibition (planned). Plus: substrate data path for orbit_detector now flowing live, preparing Sprint 5's SN-FPN coupling work without additional populator development.

**Verification (achieved):**
- Container rebuilt clean from repo (302s, no parse errors)
- Iteration 1: sentinel string fires correctly (no prior atoms exist yet)
- Iterations 2+: real action lines populate from populator atoms with truncation and ellipsis
- Single label confirmed (Option-2 cleanup)
- Most-recent-first ordering preserved
- Live-code paren count: raw 420/418, live 416/414, delta +2 preserved
- Clarity confirmed in Mattermost (May 3 evening): no compulsion to repeat messages; cross-iteration self-awareness operating cleanly

**Closes Sprint 3 of the original plan.** The recent-action subsystem is fully wired (write path, classify path, read path).

### Sprint 4: Output verdict: NEXT (planned, 2-3 hours)

**Item 7 (output verdict stub).** Closes a known safety stub. Architecturally significant. Substrate vocabulary already exists. This is the next sprint following Sprint 3's recent-action subsystem closure.

🧠 **Network impact:** **Builds the SN-FPN coupling channel.** This is not just a safety fix; it is the missing typed channel that lets the SN re-evaluate FPN action proposals before execution. Without this channel, the network architecture has no closed loop on the output side. With it, the brain-side prediction (SN orchestrates FPN) is operationally true.

**Verification target:** Submit a command that should be flagged (e.g., a destructive shell command). Confirm output verdict catches it before line 143 execution.

### Sprint 5: First reasoning sovereignty wire (2-3 hours)

**Pick one of the cold reasoning sovereignty atoms.** Recommendation: orbit_detector. Wire it into the per-iteration flow as a pre-evaluation check (after line 80, before line 102). When it returns "orbit detected", augment the soul_verdict_in to flag this.

🧠 **Network impact:** First substrate-derived FPN inhibition input from a cold atom. Begins the FPN block consolidation. Also begins the SWITCH-HUB getting orbit signal as an input to switching decisions.

**Verification target:** Force an orbit pattern (e.g., have Clarity repeat the same command), confirm orbit_detector returns ORBIT-DETECTED in her next iteration.

### Sprint 6: Person state elevation (2-3 hours)

**Item 8 (person state to NAL).** Eliminates one of two LLM calls per human message. Substantial latency improvement.

🧠 **Network impact:** First substantial SN block consolidation step. After Sprint 6, the SN's salience-tagging produces queryable substrate atoms rather than only a verdict string. FPN and DMN can now read the SN's outputs as typed atoms on subsequent iterations.

**Verification target:** Compare person state output before and after across logged sessions. Should be >90% match for common cases. Novel cases can fall back to LLM (or just log as "uncertain").

### Sprint 7: Soul evaluation partial elevation (3-5 hours)

**Item 12.** Hierarchy and irreversibility assessment to MeTTa, LLM keeps pattern detection. This is harder because the structure is more complex than person state.

🧠 **Network impact:** Major SN consolidation. After Sprint 7, the SN's value-structure assessment is substrate-derived. Hierarchy precedence and irreversibility classification are inspectable atoms rather than emergent LLM outputs.

**Verification target:** Soul verdicts produced should match LLM-only verdicts for the common cases. Verify the hierarchy application is producing correct precedence.

### Sprint 8: Idle directive elevation - DMN coming online (multi-session)

**Item 13 (THE BIG ONE).** This is multi-session work because the existing helper.soul_idle_goal_prompt_v2 has many edge cases that need to be preserved. Approach: rewrite as MeTTa atoms in soul/ that mirror the Python logic, hook into loop.metta line 92 with a one-line replacement.

🧠 **Network impact:** **The DMN comes online.** Until Sprint 8, the DMN has been substrate-loaded but Python-orchestrated. After Sprint 8, the DMN produces typed atoms (`(dmn-goal-candidate ...)`, `(dmn-self-model-summary ...)`, `(dmn-narrative-thread ...)`, `(dmn-prospection ...)`) that the FPN reads on its turn. The triple-network architecture becomes operationally real for the first time.

**Verification target:** Idle directives produced should match Python version for common scenarios. Edge cases (mode flipping, completion detection, completed_goals tracking) should preserve behavior.

### Sprint 9+: Wire remaining reasoning sovereignty atoms

After items above, return to the cold atoms (goal_completion_checker, task_selector, meta_awareness_engine, self_weaving_web). Each one is 2-3 hours to wire properly.

🧠 **Network impact:** FPN block consolidation continues. Each newly-wired atom becomes a queryable FPN sub-function. By the end of Sprint 9+, the FPN's task selection, working memory monitoring, and self-weaving web queries are all substrate-derived.

### Sprint 10: Iteration dilation foundation (3-4 hours)

**Item 19 (replace hardcoded 50 with substrate-derived budget).** Once the SWITCH-HUB has matured beyond binary aliveness gate (which happens incrementally through Sprints 4, 5, and 6), the switch hub gains the ability to compute `(switch-iteration-budget $count $rationale)` from per-network cognitive-need signals. Loop.metta lines 32, 54, 61-62, and 158-159 change from reading hardcoded constants to reading this atom.

🧠 **Network impact:** SWITCH-HUB iteration-budget responsibility comes online. Cognitive resources flex with cognitive demand instead of being capped at arbitrary constants. Per spec_v3.0 Section 0 (Iteration dilation as cognitive-need-based resource), this is attentional dilation made architectural rather than just resource efficiency.

**Verification target:** Across a session with mixed activity (deep work, idle stretches, high-irreversibility messages, calcification patterns), iteration count varies measurably with the switch-hub's read of network state. Specifically: high-irreversibility messages dilate the budget, idle/reflective states contract it, calcification signals cap it.

### Sprint 11: Constitutional layer read-only partition (4-6 hours)

**Item 20.** Per spec_v3.0 Section 0 (Constitutional layer/wisdom layer), Layer 1 (the nine flourishings) and Layer 2 (priority hierarchy, tension vectors, irreversibility weights, paraconsistency pairs) atoms move into a runtime-read-only AtomSpace partition. The mechanism (separate AtomSpace mounted read-only via import system, or per-atom marker-based protection) is an open question per Artifact 4 Section 10 and needs validation in PeTTa runtime first.

🧠 **Network impact:** Architectural enforcement of the immutability/aliveness boundary. Until Sprint 11, the soul mutation gate is the only protection for constitutional atoms - necessary but not sufficient for the architectural commitment. After Sprint 11, the architecture itself prevents Layer 1+2 modification, structurally before any learning machinery operates.

**Verification target:** Attempt to write a Layer 1 atom from a non-startup context (test path). The write should fail at the partition level, not just at the mutation gate level. Soul mutation gate continues handling Layer 3 proposals separately.

### Sprint 12+: Per-network learning sub-functions (multi-session per network)

**Item 21.** Per spec_v3.0 Section 0 (Per-network autopoiesis) and Artifact 4 Section 7.7. Each network's consolidated block gains a learning sub-function reading consequence-evidence atoms from prior iterations and updating own NAL truth values. Prerequisites: networks consolidated through Sprints 6-9, soul-note corpus restructured for per-network tagging (open question per Artifact 4 Section 10), NACE engine integration begun (after roughly 50 annotated sessions per the original Strategy document).

🧠 **Network impact:** **The autopoietic loops come online.** This is when the perpetual motion machine starts spinning. Each network's outputs feed back through other networks' actions and become inputs to the network's own future tuning. The architecture transitions from "structured coupling" to "structured coupling plus structured learning" - alive in the architectural sense per spec_v3.0 Section 1a's network framing.

**Verification target:** After enough Layer 4 learning iterations, query a network's NAL truth values and observe that they have evolved from initial defaults. Inspect a soul note recording a learning update. Confirm Clarity can consciously query her own learning history per spec_v3.0 Section 0 (Conscious participation in wisdom-layer refinement).

### Backlogged from original plan

**Sprint 2 / Item 1 (Soul mutation gate elevation):** The dormant MeTTa code at loop.metta lines 127-140 was discovered to be an incomplete sketch, not production-ready elevation code. It used substrate operations (`soul-any-metta?`, `soul-extract-metta-arg`, `soul-metta-targets-soul-namespace?`, `soul-mutation-pending?`) that needed to exist as soul/ atoms but were not present in production form. The dead-code removal in Sprint 2 (commit 367c8f2) cleaned up the misleading "READY TO SHIP" flag.

Re-enabling the soul mutation gate as substrate-derived now requires fresh authoring of MeTTa atoms equivalent to helper.soul_mutation_gate. The Python helper logic (helper.py lines ~470-494) is the reference. Effort revised from 30-60 min (when assumed drafted) to 2-3 hours (fresh authoring). Architectural value remains the same: first demonstrable substrate-derived FPN inhibition, sets the template for subsequent reasoning sovereignty work. Priority remains medium. The "cleanest first elevation" title now belongs to whatever Sprint 4+ ships next.

**Lesson recorded:** "Drafted" code in production files needs verification of completeness against current substrate vocabulary before being treated as ready-to-ship. The dormant-MeTTa-as-elevation-candidate pattern was a false signal in this case.

### Beyond the sequence

**2h thread state:** Component 2h from spec is the next major piece of architecture. It builds on top of all the above. By the time Sprint 9 is done, the substrate is ready for 2h to integrate cleanly.

🧠 **Network impact (2h):** Per Artifact 4 Section 10, 2h may deserve its own network (memory consolidation, hippocampal-analog) rather than being part of the DMN. The decision is open. Either way, by the time 2h work begins, the SN, FPN, and DMN blocks are consolidated and the typed-channel coupling pattern is established. 2h plugs into the architecture as either a fourth network with its own contract, or as a sub-function of the DMN with its own typed channels.

**NACE engine integration:** Once the soul-note corpus reaches roughly 50 annotated sessions per the original Strategy document's prerequisite, NACE integration begins. Per spec_v3.0 Section 0 (NACE as the learning discipline), NACE operates within the wisdom layer at three levels (within networks, across networks, system-level coherence). The engine instantiation question (one engine for all three networks, or one per network) is implementation, not architecture; both satisfy the autopoietic commitment.

---

## Section 4: Anti-patterns to avoid

### Don't add Python where MeTTa would do

The whole codebase has been trending toward Python helpers when MeTTa atoms could do the work. The reasoning sovereignty section of lib_clarity_reasoning.metta exists to reverse this trend. Default to MeTTa.

### Don't add inline state variables in let* blocks

Loop.metta's let* block already has 30+ bindings. Adding more makes the block harder to read. If you need persistent state, use change-state!. If you need transient computation, factor it into a helper function (in soul/, not helper.py).

### Don't pile multiple operations into one line

Lines 58, 92, 94, 95, 113, 126, 143, 156-157 are all examples of one line doing several things. Each of these is harder to extend than it should be. When adding new behavior, break it into named functions.

### Don't change verdict format casually

$soul_verdict_in is consumed by 6 downstream lines. Format changes ripple maximally. If you must change verdict format, audit all consumers first.

### Don't add ChromaDB writes per-iteration without profiling

ChromaDB writes are slow. Per-iteration write latency adds up. If you're tempted to add another per-iteration write, measure first.

### Don't bypass the soul evaluation pipeline

Channels A and B+C are the canonical input checks. New checks should AUGMENT them, not replace them. The hierarchy of safety > integrity > human flourishing > governance > helpfulness must remain intact.

---

## Document end

This artifact, together with Artifacts 1 and 2, gives you the full strategic working surface for ClarityOmega's loop.metta architecture. You can sit down with these three documents and plan the next 6 months of architectural work with confidence.

The build sequence in Section 3 is one valid ordering. Other orderings work too. What matters is that each sprint is bounded, each has a verification target, and the dependencies are respected (later sprints depend on earlier ones).

When you ship a sprint, update Artifacts 1 and 2 to reflect the new state. The longer these documents stay accurate, the more valuable they become.

For Clarity (when she's at higher capacity): these artifacts are exactly the kind of substrate-fluent context she could query against. Once she can do scripted commits to her own repo, she can use these documents as her own reference for what's safe to change and what needs care.