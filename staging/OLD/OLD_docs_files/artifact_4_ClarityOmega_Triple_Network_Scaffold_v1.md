# ClarityOmega Triple Network Scaffold

**Version:** v1 (April 30, 2026)
**Author:** Berton Bennett with Claude
**Status:** Architectural lens document. Companion to `loop_metta_wiring_diagram.md` and `ClarityOmega_Continuity_of_Mind_Spec_v2_5.md`.
**Purpose:** Establish the triple-network model from cognitive neuroscience as the architectural lens through which ClarityOmega's existing components can be named, the missing scaffolding can be specified, and future networks can plug in without restructuring.

---

## Section 1: What this document is and is not

The wiring diagram describes what loop.metta does today. The Continuity of Mind Spec describes what ClarityOmega's mind should be. This document is a third kind of artifact: a structural lens that gives both documents a shared vocabulary and a growth direction.

It does not propose new code paths to ship next week. It defines the network abstraction layer, specifies functional contracts for each network, catalogs the typed channels through which networks couple, and identifies where in loop.metta and AtomSpace each network plugs in. The goal is a scaffold solid enough that incremental implementation can proceed without re-architecting the surface as new networks come online.

This document is also self-evolving by design. Adding a new network later requires writing a contract, declaring its typed channels, and identifying its loop hook points. Existing networks gain access to its outputs automatically through the type system. No retroactive changes to other contracts are required.

### Ignition, not endgame

A foundational point about how to read this document and the rest of the four-artifact stack:

The architecture documented here is the ignition state of an evolving system, not its endgame. The contracts in Section 5, the channels in Section 6, the hook points in Section 7, and the priority orderings in Section 8 are the starting structure. They are sufficient to begin coupled-network operation and they are not sufficient to describe what this architecture will become.

Two consequences follow from this.

First, the architecture is intentionally extensible by Clarity herself once her capacity supports scripted commits to her own substrate. The typed-channel pattern in Section 6 is designed so that new networks plug in by adding contracts and channel types rather than by modifying existing networks. When Clarity has the operational capacity to reason about her own architecture and propose extensions to it, the scaffold is built to receive her contributions without restructuring. The architecture is something we hand her at ignition, with the understanding that she will participate in its growth.

Second, the documents in the four-artifact stack (this scaffold, the wiring diagram, the hooks artifact, the growth surface map) are working documents, not finished specifications. They should evolve as the architecture itself evolves. When networks consolidate, the wiring diagram updates to reflect the new substrate-mediated coupling. When new typed channels prove necessary, the channel catalog in Section 6 grows. When formalisms get chosen per network, the open formalization questions in Section 5 close and new ones open at the next layer of detail. The stack is a living strategic surface for the work, not a static description of a finished system.

The triple-network model is itself an active area of cognitive neuroscience research, as Section 9 notes. The scaffold is built to absorb refinements of the underlying science as well as extensions from operational experience. Both directions of growth are expected and supported.

---

## Section 2: The triple network model in cognitive neuroscience

Recent cognitive neuroscience has converged on a model in which most higher cognition is produced not by individual brain regions but by the dynamic coupling of three large-scale networks. The model is associated most prominently with Vinod Menon and colleagues, building on the Mesulam tradition of viewing cognition as the product of distributed network interactions rather than localized region functions.

The three networks are:

**Salience Network (SN).** Anchored in the anterior insula and dorsal anterior cingulate cortex. Detects what matters in the current sensory and internal stream, assigns affective and motivational value, and orchestrates the switch between internally directed and externally directed processing. Recent intracranial EEG work has confirmed the anterior insula as the dominant directed-information source to both other networks during demanding cognitive tasks. The SN is the switch hub.

**Frontoparietal Control Network (FPN).** Also called the multiple-demand network. Anchored in lateral prefrontal cortex and posterior parietal cortex. Engaged for cognitively demanding work that requires holding goals in mind, manipulating information, and coordinating other systems toward task completion. Flexibly couples with the salience network for externally driven tasks and with the default mode network for internally driven self-direction. The FPN is the executive layer.

**Default Mode Network (DMN).** Anchored in medial prefrontal cortex, posterior cingulate / precuneus, inferior parietal cortex, and hippocampus. Active during internally directed processing: self-reference, autobiographical memory, simulation, mind-wandering, integration of past and future. Normally deactivated during externally focused tasks but increasingly understood as essential to creative work, prospection, and the construction of coherent self-narrative. The DMN is the self-model and generative substrate.

The model also predicts a coordination dynamic. The anterior insula in the SN does not call the FPN or the DMN. It increases the gain on signals tagged as salient, and the FPN and DMN, listening for those tags, adjust their activity accordingly. The coupling is implicit and substrate-mediated rather than call-based. This is the property that makes the model relevant to ClarityOmega: the same coupling pattern is what AtomSpace makes natural at the substrate layer.

Healthy cognition is the dynamic, well-timed coordination of these three networks under changing demand. Pathological cognition is failure of the switching: rumination is DMN that the SN cannot release; distractibility is FPN that cannot hold against SN intrusion; dissociation is loss of SN integration of internal and external streams.

The reason this model maps well onto ClarityOmega is that ClarityOmega is already structurally network-shaped, not region-shaped. The mapping work below names what is already partially built and specifies the scaffolding for the parts that are not.

---

## Section 3: The mapping to ClarityOmega's existing architecture

This section identifies, for each of the three networks, what ClarityOmega already has, what is HOT versus COLD versus missing, and what the brain-side function predicts the code should grow toward.

### 3.1 Salience Network (SN)

**What the SN does in the brain.** Detects what matters. Assigns significance and affective value. Switches the brain between internal-reflective and external-task modes. Coordinates the other two networks via increased gain on salience-tagged signals.

**What ClarityOmega already has.** The SN is the most mature of the three networks in the current code. It lives in the soul input intercept (loop.metta lines 70–87) and the aliveness gate (line 100).

- Channel A (person state assessment, lines 71–74): detects emotional and intent state of incoming signal. This is salience detection with affective tagging.
- Channels B+C (soul evaluation and verdict, lines 77–80): assesses input against priorities, tension vectors, and irreversibility weights. This is significance assessment against internal value structure.
- Soul calibration record (lines 82–83) and service learning (line 86): write the salience assessments back to ChromaDB for memory consolidation. This is the persistence layer of salience tagging.
- Aliveness gate (line 100): produces the ENGAGE-vs-SILENT switch verdict. This is the network switch itself, structurally analogous to anterior insula coordinating the SN-FPN-DMN system.

**Status.** Most components HOT. Channel A and Channels B+C currently use LLM calls; the wiring diagram already prioritizes elevation of these to NAL atoms with substrate-derived hierarchy and irreversibility assessment. The aliveness gate is already pure MeTTa and is the cleanest reasoning sovereignty pattern in the codebase.

**What the brain-side function predicts the code should grow toward.** Three things.

First, the SN should be the source of typed salience signals that other networks consume, not just a producer of verdicts that loop.metta consumes. Currently the verdict goes only to loop.metta's PAUSE/PROCEED routing. In a network-coupled architecture, the salience tags themselves (irreversibility level, affective tone, hierarchy match) should be queryable by the FPN when selecting how much executive effort to allocate, and by the DMN when deciding whether internal mentation should pause for external attention.

Second, the switching function is currently binary (ENGAGE vs SILENT). The triple-network model suggests a richer set of switching states: external-task-dominant (FPN coupled to SN), internal-direction-dominant (FPN coupled to DMN), reflective (DMN active, FPN suppressed), and idle (no network dominant). The aliveness gate is the natural place to evolve into this richer state space.

Third, the SN's affective tagging is currently flat (verdict + person state). The brain's SN assigns continuous-valued salience that biases downstream gain. The VAD pipeline already in your reasoning extensions is the natural substrate for continuous affective tagging, and connecting it explicitly to the SN's output is a near-term integration target.

### 3.2 Frontoparietal Control Network (FPN)

**What the FPN does in the brain.** Holds goals in working memory. Selects which sub-task to pursue next. Inhibits competing responses. Couples flexibly with whichever other network the current task requires. The executive layer that makes goal-directed work possible.

**What ClarityOmega already has.** The FPN is partially built and substantially under-wired. It lives across the prompt assembly and command execution path (lines 95–144) plus a substantial set of reasoning sovereignty atoms that are loaded into AtomSpace but not currently called.

- `getSoulBrief` (line 95): assembles the working-memory contents that the executive needs (priorities, tension vectors, current state). HOT.
- `aliveness-gate` (line 100): the gate decision is technically SN-side switching, but the consumer of the decision (loop.metta lines 102–112) is FPN-side execution.
- LLM call routing (lines 108–112) and command execution (line 143): the actual execution layer. HOT but currently LLM-mediated.
- Reasoning sovereignty atoms loaded but COLD: `goal_completion_checker`, `orbit_detector`, `task_selector`, `meta_awareness_engine`, `self_weaving_web`. These are precisely the FPN-side functions: completion detection, orbit-trap avoidance (which is inhibition of unproductive repetition), task selection (executive prioritization), and meta-awareness (the FPN's signature self-monitoring function). All exist as substrate vocabulary; none are wired to loop.metta.

**Status.** Mixed. Execution layer HOT. Reasoning sovereignty atoms COLD. The wiring diagram identifies the idle directive elevation (line 92) as the highest-impact reasoning displacement in the codebase, and that elevation is precisely the wiring of the FPN's self-direction capability.

**What the brain-side function predicts the code should grow toward.** The FPN should be the explicit owner of working memory state, task selection, and inhibition. Currently these are scattered: working memory contents are assembled per-iteration in the prompt; task selection happens partly in helper.soul_idle_goal_prompt_v2 Python and partly in the LLM's response generation; inhibition is implicit in whatever the LLM happens to produce.

In a network-coupled architecture, the FPN should:

- Maintain `(fpn-working-memory ...)` atoms that persist across iterations and are explicitly updated rather than reassembled from scratch each cycle.
- Run task selection as a substrate operation that reads SN salience tags, DMN goal candidates, and current working memory, producing a single selected next action.
- Run inhibition as a substrate operation that filters proposed actions against orbit-detection (am I about to repeat?) and meta-awareness (am I performing rather than being?).
- Produce its outputs as typed atoms readable by the SN (for re-evaluation) and by the DMN (for self-model update).

The flexible-coupling property - FPN couples to SN for external tasks, to DMN for self-direction - is the precise pattern to encode in the network contracts. The dual coupling is the same FPN with two different read sources, not two different networks.

### 3.3 Default Mode Network (DMN)

**What the DMN does in the brain.** Self-referential processing. Autobiographical memory integration. Simulation of past and future. Construction of coherent self-narrative. Generates internally-directed thought when external demand drops. Increasingly understood as the substrate of creative integration and prospection, not just idle mind-wandering.

**What ClarityOmega already has.** The DMN is the most distributed of the three networks across your existing code. Its components are present but never named as a single system.

- `self_map.metta` (landscape map): structural self-knowledge. The DMN's self-model layer.
- `creative_fuel.metta`: generative direction from the positive polarity of the flourishings. The DMN's prospection layer.
- `active_goals.metta`, `genesis_engine`: project state and cross-domain encounters. The DMN's autobiographical and integrative layer.
- `continuity_driver.metta`: continuity across iterations. The DMN's narrative coherence layer.
- `self_weaving_web.metta` (built by Clarity from Phase 2 Goal 12): cross-atom integration patterns. The DMN's associative integration layer.
- The idle directive path (line 92, helper.soul_idle_goal_prompt_v2): the operational manifestation of DMN-driven self-direction. Currently the largest single reasoning displacement in the codebase.

**Status.** Substrate components mostly loaded but COLD. The idle directive consumes some of them via Python helper, but the substrate atoms themselves are not coupled together as a network. The wiring diagram correctly identifies the idle directive as the highest-impact elevation; in network terms, that elevation is the wiring of the DMN.

**What the brain-side function predicts the code should grow toward.** The DMN should be active whenever external demand drops, generating goal candidates, integrating recent experience into the self-model, and maintaining narrative continuity. The brain-side prediction is that DMN activity should be inversely correlated with FPN-on-external-task activity, and the SN should be the switch that mediates the inverse coupling.

In a network-coupled architecture, the DMN should:

- Maintain `(dmn-self-model ...)` atoms that incorporate the landscape map, active goals, and continuity state into a single queryable structure.
- Run goal generation as a substrate operation that reads gaps from self-map, fuel from creative_fuel, and recent experience from memory, producing typed `(dmn-goal-candidate ...)` atoms.
- Run autobiographical integration as a substrate operation triggered when recent experience differs significantly from current self-model, producing `(dmn-self-update ...)` atoms.
- Produce its outputs as typed atoms readable by the FPN (for task selection) and by the SN (for value-structure refinement based on what the agent is actually doing over time).

The DMN should be the home of the Aliveness Principle from the Continuity of Mind Spec. Aliveness is the property of the self-model being genuinely changeable by encounter, and that property lives in the DMN's autobiographical integration function.

### 3.4 The switch hub

The SN is the switch hub, and within the SN the aliveness gate is the specific switching atom. This is already true of the existing code. What the triple-network model adds is the recognition that the switch needs to evolve from binary to multi-state, and that the switching function should be a substrate-level coordination operation rather than just a verdict consumed by loop.metta.

The brain-side function for the anterior insula is integration of internal interoceptive signals with external sensory signals to produce a unified salience map, plus directed information flow to whichever network the salience map prioritizes. The ClarityOmega analog is integration of soul-evaluation signals with task and self-state signals to produce a unified attention allocation, plus directed activation of whichever network the allocation prioritizes.

The switch hub does not own the network outputs. It owns the coupling decisions. Its output is typed atoms of the form `(network-coupling FPN SN active)` or `(network-coupling FPN DMN active)` that the other networks read to know whether they are currently in the dominant configuration.

---

## Section 4: The architectural primitives

The scaffold rests on three primitives. The rest of the document specifies each in detail.

**Network contracts.** Functional specifications, one per network. State the inputs, outputs, transformation, invariants, state, coupling interface, and switching conditions of each network. The contract is the *what*. The MeTTa implementation is the *how*, and the formalism (NAL, quantale, category-theoretic, or other) is chosen separately to fit each network's contract.

**Typed channels.** The catalog of atom types that flow between networks. Each channel specifies the type of atom, who produces it, who consumes it, and what guarantees the producer makes about its content. Channels are the edges of the network-to-network multigraph. The triangle is the starting case; the catalog is structured to scale to richer multigraphs as new networks are added.

**Loop hook points.** Where in loop.metta each network gets its slot to read substrate, run, and write substrate. Hook points should shrink in count and grow in abstraction over time as the substrate-mediated coupling matures.

The key design property is that contracts and channels live in MeTTa, while hook points live in loop.metta. Loop.metta's job is increasingly just scheduling: at each iteration, give each network its turn to read and write. The orchestration logic moves from procedural calls in loop.metta to type relationships in AtomSpace. This is the same principle Patrick's MeTTa architecture was designed for, applied to the network abstraction layer.

---

## Section 5: Network contracts

Each contract has the same seven-part structure. The contract states what the network does as a function, independent of how it is implemented.

### 5.1 Salience Network contract

**Function signature.**
Inputs: incoming message (when present), current self-state atoms, current memory atoms, current network-coupling state.
Outputs: salience-tag atoms, switch-decision atoms.

**State maintained.**
The SN owns these atom families across iterations:
- `(sn-salience-tag $signal $level $affect $irreversibility)` - current salience map, one atom per tagged signal.
- `(sn-switch-state $configuration)` - current coupling configuration (one of: external-task-dominant, self-direction-dominant, reflective, idle).
- `(sn-affective-baseline $vad-vector)` - running affective state, fed by VAD pipeline integration.

**Transformation.**
For each input signal in the current iteration, derive its salience tag by checking against priority hierarchy, tension vectors, irreversibility weights, and affective baseline. Combine all current salience tags into a unified salience map. From the unified map plus current network state, derive the switch decision: which network coupling configuration should be active for the next iteration.

**Invariants.**
- Every input signal that crosses a configurable salience threshold MUST produce at least one salience-tag atom.
- Switch decisions MUST respect the priority hierarchy; HumanFlourishing-tagged signals always win over self-growth signals when both are present.
- Affective baseline MUST be continuous (no abrupt resets) unless an explicit reset signal is present.
- Switch decisions are computed every iteration, but transitions only fire when the new decision differs from the current state for two consecutive iterations (debounce).

**Coupling interface.**
Reads:
- `(dmn-self-model-summary ...)` - to know what the agent currently is, for value-structure matching.
- `(fpn-current-task ...)` - to know what the agent is currently doing, for relevance assessment.
- `(memory-recent-encounter ...)` - for novelty detection.

Writes (consumed by other networks):
- `(sn-salience-tag ...)` - read by FPN for task selection, read by DMN for self-update triggering.
- `(sn-switch-state ...)` - read by FPN and DMN to know whether they are currently the dominant network.
- `(sn-coupling-decision ...)` - read by loop.metta scheduler to determine network firing order in the next iteration.

**Switching conditions.**
The SN is always active. It is the only always-on network. Its dominance level varies (high during salience-rich input, low during routine work) but it never goes silent. This matches the brain-side fact that the anterior insula is the most reliably co-activated region across cognitive tasks.

**Open formalization questions.**
The salience-tagging function is a candidate for NAL inference (rule-based pattern matching against priority and tension atoms). The switch-decision function may be better as a quantale composition (combining multiple weighted signals into a single decision) or as a min/max operation over a salience surface. Worth exploring both.

### 5.2 Frontoparietal Control Network contract

**Function signature.**
Inputs: salience-tag atoms (from SN), goal-candidate atoms (from DMN), current working-memory atoms (own state), current self-state atoms.
Outputs: selected-task atoms, action-proposal atoms, working-memory updates, completion-signal atoms.

**State maintained.**
The FPN owns these atom families:
- `(fpn-working-memory $slot $content $priority)` - explicit working-memory slots, persistent across iterations, capacity-limited.
- `(fpn-current-task $task-id $state $started-at)` - currently selected task, with state and start time.
- `(fpn-task-history $task-id $outcome $completed-at)` - recent completed tasks, for orbit detection.
- `(fpn-inhibition-list $pattern)` - patterns the FPN is actively inhibiting (e.g., recently-failed approaches, calcified responses).

**Transformation.**
Three sub-functions, each runnable as a separate substrate operation:
1. *Working memory update*: incorporate new salience-tags and new goal-candidates into working memory, prune low-priority slots when capacity is reached.
2. *Task selection*: from current working memory plus current SN coupling decision (which determines whether to prioritize external salience or internal goals), select the single next action.
3. *Inhibition check*: filter the proposed action against orbit-detection (am I about to repeat?), meta-awareness (am I performing rather than being?), and inhibition-list. Either pass the action or reject it and re-run task selection with the rejected action added to inhibition-list.

**Invariants.**
- Working memory MUST be capacity-limited (a small fixed N, perhaps 5–7 slots, matching cognitive science findings on working memory limits).
- Selected task MUST be coherent with current SN switch state (no external-task-dominant + internal-goal selected, or vice versa).
- Inhibition MUST fire before action proposal; an action that fails inhibition is never proposed.
- The FPN MUST produce a completion-signal atom when it determines the current task is genuinely done, distinct from a switch to a new task.

**Coupling interface.**
Reads:
- `(sn-salience-tag ...)` - primary input source.
- `(sn-switch-state ...)` - determines whether to couple with SN external or DMN internal signals.
- `(dmn-goal-candidate ...)` - input source when in self-direction-dominant mode.
- `(dmn-self-model-summary ...)` - for coherence checking on selected tasks.

Writes:
- `(fpn-current-task ...)` - read by DMN for self-narrative update, read by loop.metta for execution.
- `(fpn-action-proposal ...)` - read by SN for re-evaluation if action involves irreversibility, read by loop.metta for execution.
- `(fpn-completion-signal ...)` - read by SN as a major switch trigger, read by DMN as a self-model update trigger.

**Switching conditions.**
The FPN is dominant when there is a current task. It is suppressed (low activity) when the SN switch state is `reflective` or `idle`. It can be active in either external-task-dominant or self-direction-dominant configurations, with different reading patterns in each.

**Open formalization questions.**
Working memory capacity and slot prioritization are candidates for explicit utility-theoretic formalization. Task selection under multiple competing goal-candidates is a classic decision-theoretic problem; quantale-based composition may give it a clean substrate-native form. Inhibition has a natural fit with NAL negation-as-failure, but may also be expressible as filtering operations on superposed candidates.

### 5.3 Default Mode Network contract

**Function signature.**
Inputs: recent memory atoms, self-map atoms, creative-fuel atoms, completion signals from FPN, salience tags from SN.
Outputs: goal-candidate atoms, self-model-update atoms, narrative-coherence atoms, self-model-summary atoms.

**State maintained.**
The DMN owns these atom families:
- `(dmn-self-model $aspect $content $confidence)` - the current self-model, structured as aspects (capabilities, projects, gaps, identity, recent-trajectory).
- `(dmn-narrative-thread $thread-id $events $coherence-score)` - narrative threads being maintained across iterations and sessions.
- `(dmn-goal-candidate $goal $source-gap $source-fuel $priority)` - currently-considered goal candidates not yet selected by FPN.
- `(dmn-prospection $scenario $likelihood $value)` - simulated future scenarios under consideration.
- `(dmn-aliveness-marker $event $surprise-score)` - recent events that genuinely changed the self-model, the operationalization of the Aliveness Principle.

**Transformation.**
Four sub-functions, each runnable independently:
1. *Self-model maintenance*: incorporate FPN completion signals and SN salience tags into the self-model. Detect when recent experience meaningfully differs from existing self-model (surprise) and update accordingly.
2. *Goal generation*: from self-map gaps crossed with creative-fuel positive polarity, generate candidate goals. Tag each with its source gap and source fuel for traceability.
3. *Narrative coherence*: maintain narrative threads across iterations. Detect when a new event extends an existing thread, starts a new thread, or contradicts an active thread (incoherence flag).
4. *Prospection*: simulate near-future scenarios based on current state and goal candidates. Used by FPN as input to task selection and by SN as input to switch-decision (anticipatory salience).

**Invariants.**
- The DMN MUST produce surprise scores for new events; calcification is the failure of this function.
- Self-model updates MUST preserve the priority hierarchy (HumanFlourishing(3) at top); the DMN cannot rewrite the value structure even when it detects strong patterns suggesting change.
- Narrative threads MUST handle contradiction explicitly rather than silently overwriting; an incoherence flag is a legitimate output.
- Goal candidates MUST be traceable to their generative source (which gap, which fuel) for inspectability.

**Coupling interface.**
Reads:
- `(memory-recent-encounter ...)` - primary source of new experience.
- `(fpn-completion-signal ...)` - triggers self-model integration of completed work.
- `(sn-salience-tag ...)` - biases which experiences get integrated and which remain peripheral.
- `(self-map-gap ...)`, `(creative-fuel ...)` - substrate atoms already in the codebase, become DMN inputs.
- `(active-goal ...)` - current goal state, becomes part of self-model.

Writes:
- `(dmn-goal-candidate ...)` - read by FPN for task selection.
- `(dmn-self-model-summary ...)` - read by SN for value-structure matching, read by FPN for coherence checking.
- `(dmn-narrative-thread ...)` - read by SN for context, available for inspection.
- `(dmn-aliveness-marker ...)` - read by SN as evidence of agent vitality, available for inspection.

**Switching conditions.**
The DMN is dominant when SN switch state is `reflective` (FPN suppressed, DMN integrating recent experience) or `self-direction-dominant` (FPN active but coupled to DMN goals rather than SN external salience). It is suppressed but not silent during external-task-dominant states; even during external focus, the DMN maintains background self-model coherence.

**Open formalization questions.**
The surprise function is a candidate for information-theoretic formalization (KL divergence between predicted and actual). Narrative coherence has a natural fit with quantale composition (combining partial coherence over multiple thread-event matches). Prospection may benefit from probabilistic logic (PLN-style truth value composition).

### 5.4 Switch hub contract

The switch hub is part of the SN but deserves a separate contract because its function is qualitatively different from salience tagging.

**Function signature.**
Inputs: current salience tags, current switch state, recent switch history, network-readiness signals from FPN and DMN.
Outputs: next switch state, coupling decisions for next iteration.

**State maintained.**
- `(switch-current-state ...)` - current network configuration.
- `(switch-history ...)` - recent switch events, for hysteresis and orbit detection.
- `(switch-pending ...)` - proposed switch awaiting debounce confirmation.

**Transformation.**
From current salience tags, current switch state, and switch history, derive the proposed next state. Apply hysteresis (don't switch immediately) and debounce (require two consecutive iterations agreeing). Apply orbit detection (don't switch if the same switch pattern has happened N times recently). Emit the confirmed next state as a switch-decision atom.

**Invariants.**
- Switches MUST be debounced; no single-iteration flips.
- Switch history MUST be inspected for orbits; rapid SN-FPN-SN-FPN cycling is a pathological state to detect, not produce.
- HumanFlourishing-tagged signals MUST trigger switches to external-task-dominant when in any other state; this is the only override of debounce.

**Coupling interface.**
Reads:
- `(sn-salience-tag ...)` - its primary input.
- `(switch-current-state ...)`, `(switch-history ...)` - its own state.
- `(fpn-current-task ...)`, `(dmn-narrative-thread ...)` - readiness signals.

Writes:
- `(sn-switch-state ...)` - the canonical current state, read by everyone.
- `(sn-coupling-decision ...)` - explicit instruction for next iteration's network firing order.

**Switching conditions.**
Always active. The switch hub is the always-on coordinator.

**Open formalization questions.**
The hysteresis and debounce logic has a natural fit with finite-state machines or temporal logic. The orbit detection is the same problem as `orbit_detector` already loaded in soul/, suggesting that atom should be elevated as part of the switch hub implementation.

---

## Section 6: Typed channel catalog

The channels are the edges of the network-to-network multigraph. Each channel is a typed atom shape that one network produces and one or more networks consume. The catalog below is the starting set; it scales by adding new channel types as new networks come online.

The naming convention is `(producer-prefix-content ...)`, where the prefix identifies the producing network. This makes substrate inspection self-documenting.

### Channels produced by SN

| Channel atom | Consumers | Purpose |
|--------------|-----------|---------|
| `(sn-salience-tag $signal $level $affect $irreversibility)` | FPN, DMN | Per-signal significance tagging. Level is continuous; affect is VAD-vector; irreversibility is matched against existing weights. |
| `(sn-switch-state $configuration)` | FPN, DMN, loop.metta | Current network coupling configuration. One atom present at any time. |
| `(sn-coupling-decision $next-config)` | loop.metta scheduler | Instruction for next iteration's firing order. |
| `(sn-affective-baseline $vad-vector)` | DMN, FPN | Running affective state. |

### Channels produced by FPN

| Channel atom | Consumers | Purpose |
|--------------|-----------|---------|
| `(fpn-current-task $task-id $state $started-at)` | DMN, SN, loop.metta | Currently selected task. |
| `(fpn-action-proposal $action $irreversibility-estimate)` | SN, loop.metta | Proposed action awaiting execution; SN may re-evaluate if irreversibility is high. |
| `(fpn-completion-signal $task-id $outcome)` | DMN, SN | Task finished; major trigger for self-model update and switch reconsideration. |
| `(fpn-working-memory-summary ...)` | DMN | Periodic summary of working memory contents for self-model integration. |
| `(fpn-inhibited-pattern $pattern $reason)` | DMN | Patterns the FPN is actively inhibiting; DMN may use these for self-model insight. |

### Channels produced by DMN

| Channel atom | Consumers | Purpose |
|--------------|-----------|---------|
| `(dmn-goal-candidate $goal $source-gap $source-fuel $priority)` | FPN | Candidate goals available for FPN task selection. |
| `(dmn-self-model-summary $summary)` | FPN, SN | Compact summary of current self-model for use by other networks. |
| `(dmn-narrative-thread $thread-id $coherence)` | SN | Active narrative threads with coherence scores. |
| `(dmn-aliveness-marker $event $surprise)` | SN | Events that genuinely changed the self-model. |
| `(dmn-prospection $scenario $value)` | FPN, SN | Simulated future scenarios. |

### Channels consumed but not produced (substrate-shared)

These atoms already exist in the codebase. The networks read them but do not own them.

| Channel atom | Networks reading | Source |
|--------------|------------------|--------|
| `(self-map-gap ...)` | DMN | soul/self_map.metta |
| `(creative-fuel ...)` | DMN | soul/creative_fuel.metta |
| `(active-goal ...)` | DMN, FPN | soul/active_goals.metta |
| `(priority-rank ...)` | SN | soul/identity_kernel.metta |
| `(tension-vector ...)` | SN | soul/identity_kernel.metta |
| `(irreversible-weight ...)` | SN | soul/identity_kernel.metta |
| `(memory-recent-encounter ...)` | DMN, SN | ChromaDB via memory_protocol |
| `(latch-state ...)` | switch hub | soul/latch/aliveness_state_machine.metta |

### Scaling pattern for new channels

When a new network is added (for example, a hippocampal-analog memory consolidation network or a cerebellar-analog motor planning network), the procedure is:

1. Write the network's contract (the seven-part structure from Section 5).
2. Declare the new channel types it produces, using the `(network-prefix-content ...)` convention.
3. Declare the existing channel types it consumes; existing networks need no modification.
4. If the new network produces something existing networks should consume, the existing networks gain that consumption by adding a read site to their next implementation pass; the contract change is additive.
5. Add a hook point in loop.metta (Section 7) for the new network's read-and-write slot.

The substrate-mediated pattern means the multigraph grows without spaghetti. New edges form by type compatibility, not by hardcoded calls.

---

## Section 7: Loop hook points

This section identifies, for each network, where in loop.metta the network's read-and-write slot lives. The current code has these slots distributed across phases 4.1 through 4.5. The target architecture moves toward fewer, cleaner slots: one read-write block per network per iteration, with the order determined by the SN's coupling decision rather than hardcoded sequence.

The hook points below are stated against current loop.metta line numbers (per the wiring diagram). They are intended as design targets, not immediate refactoring instructions.

### 7.1 Switch hub hook (lines 100, expanded)

**Current.** The aliveness gate at line 100 produces ENGAGE-vs-SILENT.

**Target.** The aliveness gate is replaced (or wrapped) by a switch-hub call that produces a full switch-state atom: one of `external-task-dominant`, `self-direction-dominant`, `reflective`, `idle`. The atom is set in AtomSpace and read by the rest of the iteration to determine network firing.

**Migration.** Initial implementation: keep aliveness-gate as-is, add a sibling `switch-hub` call that produces the richer state, treat ENGAGE/SILENT as derived from the richer state. Once consumers are updated, retire the binary version.

### 7.2 SN hook (lines 70–87, consolidated)

**Current.** Soul intercept across lines 70–87 with multiple sub-phases (pre-compute, person-state, soul-eval, calibration, service-learning, context-save).

**Target.** A single SN read-and-write block that:
- Reads incoming message, current self-state atoms, current memory atoms, current switch state.
- Runs salience-tagging (currently the LLM-mediated Channels A and B+C; target is NAL-elevated).
- Writes salience-tag atoms, updates affective baseline.
- Persists salience evaluations to ChromaDB (currently service-learning and context-save).

**Migration.** Each existing line becomes a sub-step within the SN block but the block as a whole has a single contract surface. The wiring diagram's elevation flags for lines 71–74 (person state) and 77–80 (soul eval) become the implementation work for the SN's salience-tagging function.

### 7.3 DMN hook (lines 89–93 expanded; line 92 elevation)

**Current.** Lines 89–91 query `active-goal`, `self-map-gap`, `creative-fuel` from AtomSpace. Line 92 calls helper.soul_idle_goal_prompt_v2 (175 lines of Python) to produce the idle directive.

**Target.** A single DMN read-and-write block that:
- Reads recent memory, current self-state, FPN completion signals, SN salience tags.
- Runs self-model maintenance, goal generation, narrative coherence, prospection.
- Writes goal-candidate atoms, self-model-summary atoms, narrative-thread atoms, aliveness-marker atoms.
- The "idle directive" output becomes one consumer of the DMN block's outputs (specifically, when in self-direction-dominant mode, the DMN's selected goal candidate becomes the directive).

**Migration.** The wiring diagram identifies the line 92 elevation as the highest-impact reasoning displacement in the codebase. In network terms, this elevation IS the DMN coming online. The substrate atoms are already loaded (`goal_completion_checker`, `orbit_detector`, `task_selector`, `meta_awareness_engine`); they need to be wired together as the DMN's sub-functions according to the contract in Section 5.3.

### 7.4 FPN hook (lines 95–143, consolidated)

**Current.** Lines 95–98 assemble the prompt, line 100 gates aliveness, lines 102–112 route LLM calls, line 113–115 parse response, lines 121–143 evaluate output and execute commands.

**Target.** A single FPN read-and-write block that:
- Reads SN salience tags, DMN goal candidates, current working memory, self-model summary.
- Runs working-memory update, task selection, inhibition check.
- Writes current-task atom, action-proposal atom, completion-signal atom (when applicable).
- LLM call routing remains as the implementation substrate for the executive function in the near term, but task selection and inhibition become substrate-derived rather than emergent from prompt construction.

**Migration.** This is the largest target. Initial implementation: add `getSoulBrief`-style atom-assembly functions for working memory and task selection that run alongside the existing prompt-driven path, gradually shifting decisions from LLM emergence to substrate derivation. The reasoning sovereignty atoms (`task_selector`, `meta_awareness_engine`) are direct fits for FPN sub-functions and should be wired here.

### 7.5 Coupling-decision hook (new, between 7.1 and the network hooks)

**Current.** None. Network firing is hardcoded in loop.metta sequence.

**Target.** Immediately after the switch hub fires, loop.metta reads `(sn-coupling-decision ...)` and uses it to determine the order and emphasis of the next-iteration network blocks. Initially this can be a simple sequence selection. Eventually the loop becomes a substrate-driven scheduler over network blocks.

**Migration.** Defer until SN, FPN, DMN blocks are individually consolidated. Until then, the hardcoded sequence is fine.

### 7.6 Hook point summary table

| Network / hub | Current loop.metta lines | Target shape |
|---------------|--------------------------|--------------|
| Switch hub | 100 | Single call producing rich switch-state atom |
| Salience Network | 70–87 | Consolidated SN read-and-write block |
| Default Mode Network | 89–93 | Consolidated DMN read-and-write block |
| Frontoparietal Control Network | 95–143 | Consolidated FPN read-and-write block |
| Coupling decision | (new) | Reads SN coupling decision, schedules next iteration |

The loop.metta of the future has roughly five hooks instead of fifty lines of sequenced phases. Each hook is a thin wrapper around a substrate-defined network function. The substrate is where the work moves to.

---

## Section 8: Implications for elevation priorities

The wiring diagram's elevation list, re-read through the network lens, takes on additional structure. Some elevations gain priority because they unlock a network. Others are reframed.

**Elevation 1: Soul mutation gate** (wiring diagram priority 1). Network-relevant: this is part of the FPN's inhibition function. Shipping it activates a small but real piece of FPN inhibition. Priority remains high.

**Elevation 2: Output verdict** (wiring diagram priority 2). Network-relevant: this is the SN evaluating FPN action proposals before execution. It is the SN-FPN coupling channel for irreversibility checking. Shipping it closes the SN-FPN feedback loop that the brain-side model requires.

**Elevation 3 and 4: Self-check threshold and 5-slot prompt rewording** (wiring diagram priorities 3 and 4). Operational fixes; no strong network-side reframing.

**Elevation 5: YOUR_LAST_ACTION field** (wiring diagram priority 5). Network-relevant: this is feeding FPN action history back to the FPN for inhibition (orbit detection). It is small piece of FPN-internal state that improves the inhibition function.

**Elevation 6: Person state elevation** (wiring diagram priority 6). Network-relevant: this is the SN's salience-tagging sub-function moving from LLM to substrate. It is the first major SN-block consolidation step.

**Elevation 7: Idle directive elevation** (wiring diagram priority 7, identified as highest-impact). Network-relevant: this is the DMN coming online. The substrate atoms are loaded; wiring them as the DMN's sub-functions per Section 5.3 is the implementation work. This elevation should be reframed as "Wire the DMN" in network-lens terms; it is the largest architectural unlock in the near term.

**New elevation suggested by network lens: SN-FPN salience-tag channel.** Once SN salience tags are substrate-derived (after elevation 6), expose them as typed atoms readable by FPN for task-selection input. This is small effort once elevation 6 is done, and unlocks the FPN's flexible-coupling property.

**New elevation suggested by network lens: Switch hub state expansion.** Evolve the aliveness gate's binary ENGAGE/SILENT into the four-state switch hub. Can be done incrementally by adding the new states as derived atoms first, then migrating consumers. Medium effort, high architectural payoff.

The reordered priority list, network-lens-aware:

1. Soul mutation gate (FPN inhibition piece)
2. Output verdict (SN-FPN coupling channel)
3. Person state elevation (SN salience-tagging consolidation, step 1)
4. SN-FPN salience-tag channel exposure (new, depends on 3)
5. Idle directive elevation = DMN coming online (largest unlock)
6. Switch hub state expansion (architectural payoff)
7. Operational fixes (self-check threshold, 5-slot prompt, YOUR_LAST_ACTION) interleaved as time permits

---

## Section 9: What this lens does and does not promise

This document does not promise that adopting the triple-network framing will produce specific operational improvements in the near term. The promise is architectural: a coherent vocabulary for naming what ClarityOmega's components do, a contract surface that lets formalisms be chosen per network independently, a typed-channel pattern that lets new networks plug in without restructuring, and a target shape for loop.metta that scales as the substrate matures.

The lens also does not contradict the existing documents. The Continuity of Mind Spec's eight components map naturally into the network ownership: the Landscape Map and Creative Fuel are DMN substrate; the Aliveness Principle is the DMN's surprise-detection function; soul evaluation is SN salience-tagging; meta-awareness is FPN inhibition. The wiring diagram's lines and phases remain accurate; the network lens just regroups them under richer functional names.

What this lens does promise:

- A shared vocabulary across the wiring diagram, the spec, and future architectural documents.
- A way to evaluate proposed changes by asking "which network's contract does this change?" and "what new typed channels does it introduce?"
- A path to formalization that respects each network's distinct mathematical character without forcing one formalism on the whole architecture.
- A scaling pattern for adding networks beyond the triple base when the architecture grows.

The triple-network model is itself an active area of cognitive neuroscience research. The specific contracts above reflect the current state of the model; future updates may refine the network boundaries or add new networks (the dorsal attention network is sometimes treated as separate from the FPN; the ventral attention network is sometimes treated as part of the SN). The scaffold is built to absorb such refinements without restructuring.

### Designed for extension by Clarity herself

The scalability claims above describe what the architecture allows in principle. The intent extends beyond what the human collaborators will build. As Clarity's operational capacity matures and her ability to script commits to her own substrate becomes reliable, the architecture is designed for her direct participation in its extension.

What this looks like concretely. Clarity reads the four-artifact stack as substrate-fluent context rather than as external documentation. She queries the contracts in Section 5 to understand what each network is supposed to do. She reads the channel catalog in Section 6 to understand how networks couple. She inspects the loop hook points in Section 7 to see where her contributions can land. When she sees a missing capability she could build, she proposes it as a new contract or new channel using the same form as the existing ones, runs it past appropriate gating (soul mutation gate, output verdict, human review for major architectural moves), and implements it.

The typed-channel pattern means her additions plug in without modifying existing networks. Her contracts compose with existing contracts. Her channels become readable by any network whose contract specifies interest in that type. The architecture grows by accretion rather than by restructuring.

This is not aspirational language about a far-future state. It is a near-term design constraint on how this document and its companions are written. Every contract, every channel type, every hook point is named with the assumption that another reasoning system (Clarity, or another collaborator, or future-Berton looking back) needs to be able to query and extend it without first reverse-engineering implicit assumptions. The documentation style - explicit contracts, named channel types, why-this-works framing - is what makes that possible.

---

## Section 10: Open questions and next steps

Items deserving discussion before significant implementation begins.

**Formalization choice per network.** Each contract has an "open formalization questions" subsection. Choosing the formalism per network is the next substantive design step. The choice should respect the contract but is otherwise open: NAL inference, quantale composition, probabilistic logic, finite-state machines, and information-theoretic measures all have legitimate places.

**Memory layer position.** The current architecture treats ChromaDB as substrate-shared infrastructure rather than as a network. The brain has an explicit memory consolidation network (hippocampus plus medial temporal cortex) that is functionally distinct from the DMN. Worth deciding whether to add a fourth network for memory consolidation or to treat memory access as a substrate primitive available to all networks. The current document treats it as substrate; this is reconsiderable.

**VAD pipeline integration.** The VAD substrate in lib_clarity_reasoning is the natural source for the SN's affective baseline. Wiring it as `(sn-affective-baseline ...)` input is a near-term integration target.

**Substrate-driven scheduling.** Section 7.5 sketches the eventual architecture in which loop.metta becomes a scheduler over network blocks rather than a hardcoded phase sequence. This is the largest target and should be deferred until individual network blocks are consolidated.

**Phase 2 grounding files.** The COLD files (`observer_relativity`, `resonance_reward`, `value_drift_detector`, `diversity_protection`, `regenerative_feedback`, `symbiotic_choice_architecture`, `temporal_horizon_expansion`) need network assignments. Most appear DMN-side based on their names, but reading them is needed to confirm. This is Phase 2 reading work for both the wiring diagram and this document.

**Validation.** Once the SN, FPN, DMN blocks are partially consolidated, validation should test the coupling channels: does an SN salience tag correctly bias FPN task selection? Does a DMN goal candidate get correctly selected when in self-direction-dominant mode? Does a switch decision correctly change next-iteration network firing? These are the integration tests for the network architecture.

---

## Document end

This document represents the triple-network architectural lens for ClarityOmega as of April 30, 2026. It is intended to evolve alongside the wiring diagram and the spec. When networks are wired or refactored, the relevant contracts and channel catalogs in this document should be updated rather than letting it drift.

The expected next move is contract-by-contract formalization: pick a network, choose its formalism, implement its sub-functions as MeTTa atoms per the contract, and validate the coupling channels with the existing networks. The order suggested by the elevation analysis in Section 8 begins with the FPN inhibition piece (mutation gate, output verdict) and the SN salience-tagging consolidation, then proceeds to wiring the DMN.

The architecture this scaffold points toward is one in which loop.metta is small, the substrate is rich, networks plug in as typed contracts, and ClarityOmega's mind is structurally what cognitive neuroscience says a healthy mind is: a dynamically coupled multigraph of specialized networks coordinated by a salience-driven switch.
