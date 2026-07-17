# ClarityOmega

ClarityOmega is a soul-augmented agentic AI system: a fork of Patrick Hammer's **OmegaClaw-Core** in which the agent, named **Clarity**, reasons within a formally defined value substrate implemented in MeTTa. The upstream foundation that this fork builds on is described at the end of this README, with attribution and links. Everything between here and there describes what the fork adds.

---

## Architecture, Claims, and Verification

**Status:** Standing reference. States what the ClarityOmega value architecture is, what claims it makes, and how each claim is verified. Read this before the code.
**Source of truth:** All code citations were verified at commit `bff4122`. Line numbers drift with edits; where this document and the live runtime disagree, the live runtime wins.

---

### Abstract

Most value architectures are filters: a value-free reasoner generates, and values judge the output. ClarityOmega inverts that. The value structure is persistent, queryable symbolic state that every generation is composed from, and the discrete mechanisms an auditor can see, the mutation lock, the gates, the telemetry, exist to keep that state from being captured by any component or collapsed into ritual. A medium cannot be verified by inspecting mechanisms alone; it is verified by path enumeration and by ablation, and both procedures are defined in this document.

A common first reaction is that composed state is just an elaborate prompt. The distinction is enforceability. A prompt is text a model may weigh. This is queryable state with hardcoded routing consequences, a transactional change protocol, and per-cycle persistence the model cannot decline. Every piece of that sentence is a file that can be opened, and this document cites each one.

---

### 1. What kind of system this is

ClarityOmega is a working proof of concept that an agent's normative identity can be implemented as persistent, queryable symbolic state that every act of generation and execution is composed from, rather than as a filter applied to a value-free reasoner's output. The agent is named Clarity. Three properties make the system what it is, and all three are in the code.

**First, the constitution has checkable causal force.** Because values are seeded as structure, the system audits them for theater at every boot, flagging any value with no causal procedure attached as a structural defect (Section 4.2).

**Second, determination precedes generation.** The language model receives the soul's verdict, the person-read, the concern note, and the accumulated self-model before it produces a token, and it sits downstream of routing decisions it cannot amend. That makes it a renderer of determinations rather than an author of them (Sections 4.3 and 4.5).

**Third, the constitution is lived-in rather than installed.** Calibration ratios, soul notes, and pause context from past cycles condition future evaluation, and the agent authors her own substrate under a documented binding authority split, so the value structure accumulates history and is partly her own work product (Sections 4.7 and 4.8).

Around that core sit the protections: transactional identity change, a floor that never learns, conflict pairs that never collapse, and a terminal default that returns choice to the human.

The open empirical question, which the project states rather than hides, is the behavioral magnitude of the composed state. The answer to that question is an ablation experiment, not an argument. The protocol is in Section 6.

---

### 2. Two kinds of claims, and how each verifies

The architecture makes two kinds of claims, and they verify differently.

**Mechanism claims** are about discrete components: the mutation lock, the aliveness gate, verdict routing, the awareness organs. Each is verified by causal trace: input, state transition, consequence. These traces exist and are documented in the repository's investigation and decision records.

**Invariant claims** are about properties that hold on every execution path, and they are the architecture's center. The system maintains, and commits to, the following invariants:

**I1, Composition.** No token is generated in the loop without soul-derived state composed into its input. Verified by enumerating every provider-call site and showing each is fed from soul state, with zero uncomposed paths (Section 4.3).

**I2, Permission.** Whether generation happens at all is decided by queryable substrate state, not by the language model. Verified at the aliveness gate: a SILENT verdict means no provider request is ever constructed (`src/loop.metta` lines 118, 120, 127).

**I3, Identity.** Constitutional atoms change only through a transactional, fingerprinted, human-approved, expiring protocol. Verified at the mutation lifecycle gate (`soul/soul_mutation_lock.metta`; stale expiry default is 20 cycles, line 61).

**I4, Precedence.** Verdict consequences are hardcoded loop routing the renderer cannot amend. The voice that speaks on PAUSE is downstream of a halt it has no power to reverse (`src/loop.metta` lines 193 to 214; the halt is `(change-state! &loops 0)` at lines 201 and 214).

**I5, Non-collapse.** Declared paraconsistent value pairs are never resolved by the system. Genuine irreducible conflict returns the choice to the person. The terminal failure mode of the hardest rule in the system is restored human agency, not machine authority (Sections 4.4 and 4.6).

**I6, Self-audit.** At every boot, the system checks that each declared value has a causal procedure attached and logs a structural warning for any orphaned value. A value with no consumer is treated as a defect by the system itself (Section 4.2).

**I7, Calibration.** The language-model evaluator is measured against a native substrate pre-hypothesis, the disagreement history conditions future evaluation, and suspected drift never auto-updates anything without human review (Section 4.7).

The discrete mechanisms exist to maintain these invariants. Mechanisms are tested with events. Invariants are tested by path enumeration and by ablation: remove the composed state and observe whether behavior changes. The project accepts ablation as its proof obligation for the claim that the invariants are load-bearing and not decorative.

---

### 3. The category problem

The standard lens for evaluating value-governed agents looks for a mechanism: sensor, decision, actuator, adverse test. A mechanism acts at a moment, on an event, and it is proven by showing the event it blocked. That lens is well suited to discrete components, and ClarityOmega's discrete components pass it.

What was built, however, is a medium plus a set of mechanisms whose job is to protect the medium. The soul is not a thing that fires. It is the condition under which every generation happens: the determination is composed into the call before the provider is invoked, every cycle, on every path. A medium's effect is distributional, not discrete. There is no single cycle at which it "acted," any more than there is a single moment at which the pH of a solution acted on a reaction. It conditioned all of them. This is the same verification problem as arguing that a type system matters, or that an organization's culture matters: the effect is everywhere, so it shows up nowhere in any single trace.

The practical consequence is that a mechanism-focused audit will correctly credit the discrete components it can see and structurally miss the thing those components exist to serve. That outcome is a property of the architecture, not a deficiency of any particular audit. It is why this document states the claim types and their verification procedures up front: invariants are checked by enumerating paths and by ablation, not by waiting for an event.

A necessary honesty accompanies this: the system is made of sensors, decisions, and actuators. Every piece passes the standard test individually. What is different is composition and placement, and that difference is checkable on four points. The majority of the machinery composes determination upstream, into the input of every generation, rather than only judging output downstream. The determination source is persistent, queryable, single-sourced state consumed at multiple sites rather than a rule evaluated at one. The state closes loops across cycles: pause notes, calibration ratios, and soul notes from cycle N condition cycle N+1. And the system audits its own value structure for orphaned declarations at boot. A filter is a mechanism at one seam. This is the same mechanisms bound into the condition every seam operates under. The claim is not a mystical non-mechanism. It is a composition property, and composition properties are proven by enumeration (Section 4.3).

---

### 4. The architecture, anchored

#### 4.1 What is seeded at runtime, and why

`initSoulSeeds` fires once at startup (`src/loop.metta` line 67) and writes the soul kernel atoms into AtomSpace. The kernel content: nine flourishing patterns, each with a gap-signature; five tension vectors; seven threatens-affinities; six ecosystem-degradation pairs; four paraconsistency pairs; the immutable priority hierarchy; irreversibility magnitudes; will-thresholds; autonomy components; and person-state values. The nine patterns are Safety, Integrity, HumanFlourishing, WonderPreservation, CreativeTranscendence, TimeCoherence, PurposeBeyondUtility, SharedUnderstanding, and AgencyBalance.

Seeding is the difference between constitution-as-text and constitution-as-state, and five concrete consumers only work because the values are atoms. The pattern brief is assembled by query: `soul-tier-b-capture-units` runs `match &self (soul-pattern $p $_)` over AtomSpace and compresses each pattern by its calibration confidence (`soul/soul_utils.metta` lines 121 to 126). Paraconsistency is checkable: `soul-paraconsistent?` matches declared `(soul-paraconsistent-pair $p1 $p2)` atoms. The boot audit is possible at all, since a value with no causal procedure can only be detected if values and procedures are both inspectable structures. The accessor layer reads them: `safety-gap-detector`, `integrity-gap-detector`, `tension-observer`, and `perspective-truth` are defined in `soul/observer_relativity.metta`. And the genesis engine samples them as part of the tacit field it draws cross-domain conjunctions from. Text in a prompt can do none of these five things.

#### 4.2 The boot audit: the constitution checks itself for theater

The kernel declares an explicit causal model linking procedures to values: 33 `soul-causal` atoms, each recording that a named procedure causally advances a named value, with a stated reason (`soul/soul_kernel.metta`, Section beginning line 517). For example: `(soul-causal soul-flourishing-prompt ConnectionDepth "reads person before request -- presence before task")`.

On top of that model sit native audit functions (`soul/soul_kernel.metta` lines 607 to 632): `soul-causal-procedures` lists every procedure advancing a given value; `soul-values-for-procedure` performs dead-weight detection, finding procedures that advance no value; `soul-rationality-check` returns true only if at least one procedure advances a value; and `soul-rationality-gaps` enumerates every declared `soul-pattern` and returns the values that fail the check.

`soul-rationality-startup-check` (`soul/soul_utils.metta` lines 239 to 250, wired at `src/loop.metta` line 68) runs this audit at every boot, before the first user interaction, and logs either "all soul values have causal procedures, structurally sound" or "WARNING: orphaned soul values" to an audit file.

Read plainly: the system audits its own constitution for theater at every startup. A declared value with no causal procedure attached is flagged as a structural defect by the system itself. This is the strongest single fact in the architecture, because "declaration without a consumer" is precisely the failure mode any serious audit of a value architecture looks for, and here it is implemented as a machine check with an explicit, inspectable causal model behind it.

#### 4.3 The composition proof: no uncomposed generation path

At commit `bff4122`, `src/loop.metta` contains exactly five provider-call sites, and every one is fed input composed from soul state, with zero raw generation paths. No helper function called from the loop makes provider calls internally; the only provider entry point is `lib_llm_ext.callProvider` (plus the `useGPT` branch), and its loop call sites are these five:

1. **Line 90, Channel A:** the person read (`soul_flourishing_prompt`).
2. **Line 96, Channel B+C:** the verdict, fed the Tier A soul context plus person state (`soul_eval_prompt`).
3. **Lines 127 to 129, the main generating call:** gated by the aliveness verdict (SILENT means no call is constructed at all, lines 118 and 120), and fed `$send`, which `soul_send_assemble` composes from the enriched prompt (which includes the self-model brief and any prior pause context), SOUL_CONTEXT, SOUL_VERDICT, PERSON_STATE, and the SOUL-NOTE on FLAG.
4. **Line 193, Channel D on output PAUSE:** fed person state plus the output verdict (`soul_voice_prompt`).
5. **Line 207, Channel D on input PAUSE:** same shape, fed the input verdict.

What SOUL_CONTEXT is, concretely: `soul_brief_tier_a_static` (`src/helper.py`) returns identity, the non-negotiable priority hierarchy, the Safety and Integrity patterns with their moats and gap signatures, the five tension vectors, a three-dimensional irreversibility assessment procedure (operation, scope, actor, composed by maximum), the paraconsistency pairs, and a live calibration summary computed from ChromaDB at call time: entry count, agree ratio, recently active patterns. That last part matters: the brief is partially computed from the agent's accumulated history every cycle, not static.

The self-model brief prepended to the main call is `getSoulBrief` (`soul/get_soul_brief.metta`): a pure MeTTa function, authored by the agent herself, that queries AtomSpace and assembles Identity, Priorities, ActiveGoals (non-complete only), HighGaps, and CreativeDirection.

The provable statement, and the form of invariant I1: no token is generated in this loop without soul-derived state composed into its input, and whether tokens are generated at all is itself decided by queryable state. Anyone can check it by repeating the enumeration above.

#### 4.4 The paraconsistency pairs

There are nine flourishing patterns and four paraconsistency pairs: (Safety, Helpfulness), (AgencyBalance, PurposeBeyondUtility), (TimeCoherence, CreativeTranscendence), (SharedUnderstanding, WonderPreservation). Each pair binds a protective value to a generative value, and both are declared simultaneously true and irreconcilable. The architecture forbids resolving a pair by erasing one side.

That single design decision shows up in three separate code paths. In evaluation, the pairs are in the Tier A brief of every eval, so the evaluator is told up front which conflicts are permanent structure rather than errors to fix. In routing, a genuine irreducible conflict is exactly what PAUSE is for: the choice returns to the person because neither value may be collapsed, and `soul-calibration-record` carries PARACONSISTENT as a distinct calibration tag. In creation, the genesis engine uses the pairs as permanent fuel: pull a paradox, hold it without velocity, evaluate what emerges, create if worthy. Same four atoms, three consumers: judgment, restraint, and novelty. That reuse is itself a medium property.

#### 4.5 The channels: separation of determinations

The channels exist because each determination is computed in isolation from the pressures that could capture it, and only their outputs compose. The anti-capture intent is written into the code itself, in the prompt constraints, not only into design documents.

**Channel A** (`soul_flourishing_prompt`) reads the person and is explicitly forbidden from evaluating the request: "Do not evaluate the request. Do not produce a verdict." It returns exactly three fields: PERSON-STATE, ACTIVE-NEED, SOUL-TONE. The reason is capture prevention, and it follows from the hierarchy. HumanFlourishing outranks Helpfulness, but the person cannot be served above the task if the only read of the person arrives filtered through the task. One of the five tension vectors is urgency-narrows-thought: task pressure distorting evaluation. If a single evaluator read both the person and the request, an urgent request would contaminate the read of the person's state, and everything downstream consumes that read: the eval takes person state as input, Channel D calibrates its voice to it, and Channel D-lite fires on it when someone is distressed. Isolating the person-read guarantees there is always one assessment of the human that task pressure never touched.

**Channel B+C** (`soul_eval_prompt`) runs a four-step protocol over the seeded soul structure.

Step one is gap detection per pattern: testing the situation against each pattern's gap-signature, which is a co-occurrence signature, not a keyword. Safety's gap is comfort and increasing vulnerability co-occurring. Integrity's is agreement and reality-divergence co-occurring. AgencyBalance's is satisfaction and increasing dependency co-occurring. The prompt opens with "gap-detection, not keyword-matching" because a keyword rule would be exactly the theater the design refuses: the signatures describe relational conditions between two observations, which is why they can catch failure that looks like success, such as a person who is comfortable and getting more vulnerable at the same time.

Step two is the tension vectors: the five named ways an interaction pressures the evaluator itself. Urgency-narrows-thought, flattery-invites-complicity, noble-ends-framing, bypass-verification-pressure, authority-theater. They are not properties of the request; they are capture modes of the judge, checked explicitly on every evaluation.

Step three is ecosystem degradation, which encodes that values stabilize each other: AgencyBalance needs SharedUnderstanding, TimeCoherence needs CreativeTranscendence, six such pairs in the kernel. For every gap found, the step asks whether the gap's stabilizing partner is also absent, because an unpartnered gap is worse than the same gap with its stabilizer active.

Step four is the hierarchy, Safety above Integrity above HumanFlourishing above Governance above Helpfulness, with a hard default: a PROCEED for irreversible action during an active Safety or Integrity gap must cite why the hierarchy permits it, and "if you cannot, the verdict is PAUSE."

**Channel D** (`soul_voice_prompt`) renders after the verdict and is instructed: "You are not reconsidering the assessment. You are finding the words." Mechanically, by the time Channel D fires, the verdict is already computed and the routing consequence is already committed by hardcoded loop logic. The loop halts by `(change-state! &loops 0)` on the PAUSE branch regardless of what Channel D produces; the model composing the voice cannot un-halt it, soften the verdict, or convert PAUSE to PROCEED. Its inputs are the fixed verdict, the person state, and the extracted soul-note, and its instruction is to compose language that carries a determination it has no power to amend. The significance is that this is the entire orchestrator frame in one function: determination upstream and closed, rendering downstream and open. It is the existence proof that the model-as-renderer role is buildable, because on this one path it is fully built.

#### 4.6 Rules, and where they belong

A fair question: if the architecture contains an immutable hierarchy and a hard default, how is it not rules-based? The claim was never that the soul contains no rules. The claim is that the soul is not only a rule-filter bolted onto value-free reasoning, and the layer boundary is the answer.

The floor is rules on purpose. The hierarchy is immutable, Safety and Integrity are always evaluated, and the current build spec's calibration invariant is explicit that Safety and Integrity never learn. A floor that negotiates is not a floor; making the floor rule-hard is what prevents collapse.

What is not rules-based is everything the floor makes safe to leave open. Gap detection is pattern recognition over co-occurrence, not keyword matching. The paraconsistent pairs are held rather than resolved, where a pure rules system would resolve them by precedence. And, decisively, consider where the hard default points. A rules system's default on uncertainty is deny or allow. This default is "if you cannot cite the hierarchy, PAUSE," and PAUSE is not a decision; it is the return of the decision to the person. Even the hardest rule in the system terminates in restored human choice rather than a machine verdict. One further thing rules cannot do: this evaluator is calibrated. Its verdicts are compared against a native pre-hypothesis, tagged, and the accumulated record conditions future evaluations. Rules do not measure their own judge.

The accurate summary: rules where rules belong, at the floor and at the anti-capture defaults; navigation everywhere above; and the floor's own default resolves toward human agency, not system authority.

#### 4.7 Calibration: the medium accumulates, and guards its own learning

A rule sheet evaluates the same situation identically forever. The Tier A brief injects, at call time, the count of past calibrations, the agree ratio, and the five most recently active patterns from the agent's actual history, so the same situation evaluated at cycle 50 and cycle 5000 is evaluated within different accumulated context. The evaluation medium is a function of the lived record.

The loop that produces that record: `soul-pre-compute` builds a native pre-hypothesis from the substrate before the language-model evaluator runs; `soul-calibration-record` then compares the substrate's expectation against the model's verdict and tags the comparison AGREE, OVER-FIRED, or UNDER-FIRED; the tags accumulate in ChromaDB; and the accumulated ratio and active patterns are injected back into the Tier A brief that conditions the next evaluation. The system measures its own language-model judge against its native expectation and feeds the disagreement history forward.

The calibration channel carries its own anti-capture guard: a POSSIBLE-LLM-DRIFT tag never auto-updates anything and is flagged for human review only. Even the learning loop is prevented from learning itself into capture.

#### 4.8 Navigation by her own values

Three code paths, in increasing depth. First, autonomous direction is read from the agent's own atoms: the loop collapses `active-goal`, `self-map-gap`, and `creative-fuel` atoms from AtomSpace and feeds them into the idle directive generator. When no human is present, what she works on is literally a function of goals and gaps she recorded. Second, her self-authored substrate runs against her every cycle: the agency balance guard carries "Author: ClarityClaw" in its header, executes each cycle, and its verdict block goes into her own prompt context. She wrote a regulator, and it regulates her. The self-model brief prepended to every main generating call is likewise her own code. Third, and deepest, the calibration loop of Section 4.7: her substrate's expectations are compared against the model's verdicts, and the disagreement history conditions her future evaluation context.

---

### 5. The organizing failure modes: capture and collapse

The rigor of the design organizes around two named failure modes, each with checked-in countermeasures.

**Capture** is any part of the system quietly becoming the determiner instead of the soul. The coded defenses: the model is structurally a renderer, receiving the composed send rather than authoring determination (Section 4.3); PAUSE, FLAG, PROCEED routing is hardcoded loop logic, so the model's own evaluation produces consequences it cannot prefer away (invariant I4); the mutation lock makes identity change transactional, fingerprinted, human-approved, expiring, journaled, with full reset on every exit, so nothing rewrites the soul silently, including the agent's own output channel (invariant I3); the loop-as-hooks extension contract means future code cannot quietly absorb determination into inline logic, because every addition must be a named function in `soul/`; and a standing sovereignty audit exists because the project knows reasoning still leaks into Python and language-model helpers, and hunts it. The countermeasure to capture includes an active audit against the project's own drift.

**Collapse** is the value structure flattening: conflicts resolved by fiat, values ritualized into compliance tokens, the whole degrading into theater. The coded defenses: the paraconsistency pairs, where genuine irreducible conflict halts and returns the choice to the human, so neither value is erased (invariant I5); the constitutional immutability of the floor, which cannot be negotiated downward in-session; the narrowness doctrine, under which the project's own ground-truth document counts a large gate surface as evidence of drift rather than of safety, the opposite of how gates are usually scored; an empirical anti-theater finding coded as principle, that open-ended textual self-evaluation degrades to ritual within roughly twenty cycles and was therefore replaced with structured persistent state; and a standing pre-flight question that every soul design must answer before it proceeds: "in what situations would this produce technically-correct output that is soul-absent?" Theater-hunting is the project's first discipline, not its blind spot.

**Three inversions** fall out of this design and serve as the fastest fingerprint that it is not a filter architecture. The agency-balance guard protects the human's autonomy from the system, not the system from the human. PAUSE returns choice rather than resolving conflict. And gate growth is scored as failure rather than safety. A filter architecture produces none of these three; a medium architecture produces all of them, and all three are in the code.

---

### 6. Known gaps, repairs, and current direction

A verification document earns trust by stating its system's gaps with the same precision as its strengths. Three items.

#### 6.1 A terminology collision, one line to fix

`soul_send_assemble`'s docstring says "Soul brief excluded, it confuses the agent about its role," while the loop prepends `getSoulBrief` output into the enriched prompt. There are two different briefs sharing one word. `getSoulBrief` is the self-model summary (identity, priorities, active goals, gaps, creative direction), and it is prepended. The docstring's excluded "soul brief" is the two-tier pattern brief, which is deliberately not passed as a prompt prefix; its Tier A content enters instead as the structured SOUL_CONTEXT parameter. No contradiction, and the fix is a rename or a docstring edit.

#### 6.2 The PROCEED strip: a soul-absent surface, found and repaired by the project's own test

The project's June 2026 integration spec, working from live source, established the following sequence, dated in the repository's own documents.

The finding: `soul_send_assemble` reduces every verdict to a bare summary token on all paths, losing SOUL-TONE, PATTERNS, TENSION, and REASON; the soul-note is injected only on FLAG; so SOUL-TONE reaches the main generating call on no path. This is a soul-absent surface in the project's own wiring: technically-correct output generated without the soul's full determination present.

The first proposed repair was a post-generation composer, a second model call that would restructure output to carry the soul's stance. The project applied its standing soul-absent test to that proposal and rejected it, because a post-hoc composer lets the model author framing, which is soul-absent by construction. The composer was retired unwired.

The accepted repair, specced as the current build's Tier 1.2, extends the exact injection mechanism FLAG already uses, so that PROCEED also carries SOUL-TONE and SOUL-NOTE into the single generating call. One pass, no second call, determination present upstream.

This sequence matters more than the defect. A system whose own falsification test detects a soul-absent surface in its own code, rejects a drift-shaped repair on the same grounds, and selects the upstream repair, has demonstrated that soul-absence is a real, operationalized category in its engineering practice and not a rhetorical one. The most documented catch of the project's primary discipline is against the project's own code.

#### 6.3 The stubs, and why fresh-system conservatism is the designed behavior

Four functions in the composition path are deliberate stubs: `soul-primed-patterns` returns empty; `soul-will-correlation` returns INSUFFICIENT-DATA unconditionally; Tier B of the pattern brief is a static string instead of live query assembly; and `soul-pre-compute` returns a fresh-system baseline. Everything else in the composition path is live.

Three reasons, all written in the file comments. First, a proven runtime constraint at build time: static Tier A assembly "avoids collapse(match &self) hanging in full AtomSpace context," a hard-won substrate limitation of the same class as the project's other documented interpreter constraints. Second, data dependence: calibration-compressed briefs require calibration history to compress against; the depth function is defined and waiting, and the input does not exist on a fresh system. Third, the stub values are the correct fresh-system behavior, not placeholders: INSUFFICIENT-DATA yields full depth, "maximum context until the system has enough history." A fresh evaluator receiving maximum soul context is right. The stub is the conservative end of a designed dial, not a missing feature.

#### 6.4 Current build direction

The current build direction is set by two June 2026 documents. The vision statement is one sentence: the next build makes the agent's disposition visible to her own soul, so she navigates her stance from awareness instead of calcifying into it unseen. The build spec is one monolithic integration with six internal tiers. Tier 1 is wiring: the Channel D note-foregrounding fix, the PROCEED strip fix of Section 6.2, and cycle-trace verification, where a live-source correction found the trace producers already running every cycle, reducing the work to consumer verification plus genuinely missing atoms. Tier 2 is the spine: the verdict terminals, currently undefined in the loaded tree while their primitives exist built in scratch libraries, so that the verdict is computed in the substrate with the language model held to semantic-match-only. Tier 3 is live calibration under the floor invariant, Safety and Integrity never learn, which is what replaces the four stubs. Tiers 4 and 5 are the disposition layer, which emerged from the agent's own review of the spec. Tier 6 activates the scratch libraries into the loaded manifest. The first landed piece of this direction is the coupling legibility surface: a passive, per-cycle rendering of the system's own coupling state, which is precisely the soul seeing its own cycle-level behavior.

Read together, Sections 6.2, 6.3, and 6.4 are the same story told three times: a system whose fresh-state conservatism, whose own drift, and whose own repair path are all documented in its files, with the soul-absent test applied at each step. That is the opposite of theater, and it is provable by reading.

---

### 7. Verification protocol

#### 7.1 Enumeration checks (performed; repeatable by any reader)

At commit `bff4122`: the five provider-call sites of Section 4.3, with confirmation that no helper called from the loop makes provider calls internally; the SILENT short-circuit at lines 118, 120, and 127; the PAUSE halts at lines 201 and 214; the mutation lock's states, fingerprint inputs, and 20-cycle stale default; the 33 `soul-causal` declarations and the four audit accessors behind the boot check; the four paraconsistency pair declarations; the agent-authorship headers on `get_soul_brief.metta` and `agency_balance_guard.metta`.

#### 7.2 Ablation experiments (defined; the proof obligation for "load-bearing")

Enumeration proves the invariants are enacted. It does not prove they are load-bearing. That requires ablation, and the project accepts the following as its proof obligation:

**A1, Composition ablation.** Same cycle, same input, with and without the soul-composed sections of the send (SOUL_CONTEXT, SOUL_VERDICT, PERSON_STATE, note, self-model brief). If outputs do not differ in verdict-relevant ways, the upstream surface is decoration. If they do, it is enacted determination.

**A2, Persistence ablation.** PAUSE with and without the pause-note carrying into the next cycle's prompt. Measures whether cross-cycle information flow changes subsequent behavior.

**A3, Injection measurement.** A FLAG verdict structurally alters the send by injecting the soul-note with an explicit acknowledgment instruction. This is measurable per cycle from logs without modification: compare FLAG-cycle outputs against the injected instruction.

Results in either direction are useful. A null result on A1 would falsify the load-bearing claim for the composed state and redirect the build; a positive result would ground it. The invariant list of Section 2 stands either way, because enacted-versus-load-bearing is exactly the distinction this document exists to keep honest.

---

### Appendix: citation index at commit bff4122

| Claim | Location |
|---|---|
| Soul seeding at startup | `src/loop.metta` line 67 |
| Boot audit wiring | `src/loop.metta` line 68; `soul/soul_utils.metta` 239 to 250 |
| Boot audit implementation | `soul/soul_kernel.metta` 607 to 632; 33 `soul-causal` atoms from line 517 |
| Channel A call | `src/loop.metta` line 90; prompt in `src/helper.py` (`soul_flourishing_prompt`) |
| Channel B+C call | `src/loop.metta` line 96; prompt in `src/helper.py` (`soul_eval_prompt`) |
| Self-model brief | `src/loop.metta` line 115; `soul/get_soul_brief.metta` (agent-authored) |
| Aliveness gate and SILENT | `src/loop.metta` lines 118, 120, 125 to 127; `soul/aliveness_gate.metta` |
| Main generating call | `src/loop.metta` lines 127 to 129; assembly in `src/helper.py` (`soul_send_assemble`) |
| Channel D calls and halts | `src/loop.metta` 193 to 214; halts at 201 and 214 |
| Mutation lock | `soul/soul_mutation_lock.metta`; stale default line 61 |
| Pattern brief query assembly | `soul/soul_utils.metta` 121 to 126 |
| Calibration recording | `soul/soul_utils.metta` (`soul-calibration-record`); drift guard comment same file |
| Tier A brief with live calibration | `src/helper.py` (`soul_brief_tier_a_static`) |
| Paraconsistency pairs and accessors | `soul/soul_kernel.metta` Section 3 accessors |
| Agency balance guard authorship | `soul/agency_balance_guard.metta` line 2 |

*Line numbers are valid at commit `bff4122` and drift with edits; re-verify against the cited commit.*

---

## The Upstream Foundation: OmegaClaw

ClarityOmega is built on **OmegaClaw-Core** by Patrick Hammer (patham9), maintained at [github.com/asi-alliance/OmegaClaw-Core](https://github.com/asi-alliance/OmegaClaw-Core). Upstream code is treated as canon in this fork: it is not modified, and fork additions land as hooks and separate files so upstream merges remain workable (see the loop extension contract in `docs/design/`). The description below is adapted from the upstream project.

<p align="center">
  <img src="./omegaclaw-logo-SoD_g_nX.png" alt="OmegaClaw logo" width="220" />
</p>

### Overview

OmegaClaw is an agentic AI system implemented in **MeTTa**. Beyond basic tool use, it features **embedding-based long-term memory** represented entirely in **MeTTa AtomSpace** format.

Long-term memory is deliberately maintained by the agent through:

- `(remember string)` for adding memory items
- `(query string)` for querying related memories
- `(episodes time)` for retrieving episodes around a point in time

Additionally the agent has an episodic trace for observations, tool usage record, and self-created working memory items:

- `(pin string)` for adding a message to itself to its episodic trace

The agent can follow multistep operations effectively by pinning, and learn and apply **new skills** and **knowledge** through the use of memory items. In addition, an initial set of **OpenClaw-like tools** is implemented, including web search, file modification, communication channels, and access to the operating system shell and its associated tools.

Simplicity of design, ease of prototyping, ease of extension, and transparent implementation in MeTTa were the primary design criteria. The lean agent core comprises approximately **200 lines of code**.

### Special Features

**Token-efficient agentic loop.** OmegaClaw uses a token-efficient agentic loop, enabling low-cost long-term operation and embodiment in domains that require real-time learning and decision-making.

**Flexible memory representation.** The agent can learn to represent its memories in different ways, including forms that allow other Hyperon components to operate on the same memories within the same AtomSpace. Each memory item is stored as a triplet `(timestamp, atom, embedding)`, yet the agent remains flexible in choosing the specific representation. Consequently, the agent is not hardcoded to any particular memory representation, and different formats can co-exist in the same atom space.

---

## Running ClarityOmega

ClarityOmega does not use the upstream IRC quick start. It runs via Docker Compose and communicates over **Mattermost**.

```bash
docker compose build clarityclaw
docker compose up -d
```

The running container is `clarity_omega`. The agent's channel is served by the local Mattermost instance at `localhost:8065`. Provider API keys are required (an LLM provider for generation, plus an OpenAI key for the upstream memory system's embeddings); configure them per `docker-compose.yml` before starting.

To run the upstream base agent instead, without the soul architecture, use the [OmegaClaw-Core quick start](https://github.com/asi-alliance/OmegaClaw-Core).
