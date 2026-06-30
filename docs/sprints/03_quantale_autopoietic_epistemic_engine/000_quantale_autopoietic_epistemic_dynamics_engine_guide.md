# Quantale Autopoietic Epistemic Dynamics Engine

**File:** `lib_quantale_autopoietic_epistemic_dynamics_engine.metta`  
**Milestone draft:** `lib_quantale_autopoietic_epistemic_dynamics_engine_nace_autopoiesis.metta`  
**Companions:** `quantale_engine_validation_ladder.metta`, `quantale_engine_adapter_contract.md`  
**Status:** Layer-0 engine specification and usage guide.  
**Purpose:** Define what we built, why it exists, how to use it safely, and how it fits ClarityOmega / ClarityClaw’s substrate architecture.

> **Core sentence:** this engine is the honest algebra of what the soul can see.

It is not a skill, not a writer, not a prompt pattern, not a replacement for the soul, and not a persistence layer. It is a pure functional MeTTa engine that computes epistemic dynamics: strength, confidence, warrant, contact, suspicion, collapse risk, frame visibility, action-intention-outcome coherence, learning pressure, durable learning recommendations, self-visibility signals, and next lawful epistemic moves.

---

## 1. What we built

We built a substrate-safe Layer-0 MeTTa engine for autopoietic epistemic dynamics. It extends the original quantale p-bit algebra into a broader cognitive substrate for honest uncertainty, frame navigation, and learning.

The engine starts from the p-bit shape:

```metta
(mk-pbit strength confidence)
```

Where:

- **strength** is activation, resonance, plausibility, truth-strength, or how compelling a frame/claim/action currently is.
- **confidence** is warrant, reliability, contact-grounding, or how justified the system is in treating that strength as usable.

The foundational law is:

> **Strength may be imagined. Confidence must be earned.**

The engine then builds outward into:

- quantale algebra;
- provenance and warrant governance;
- frame/contact distinction;
- suspicion dynamics;
- certainty hardening and softening;
- disconfirmability and permeability;
- verification-path health;
- action → intention → outcome coherence;
- autopoietic learning update primitives;
- collapse/brownout response;
- frame phenomenology and collapse terrain;
- engine invariants/laws;
- calibration profiles;
- evidence independence/correlation;
- contradiction digestion;
- trace and temporal learning residue;
- self-visibility and soul-grounding primitives;
- lifecycle phase modeling;
- next-epistemic-move selection;
- skill-facing symbolic outputs.

This turns quantale algebra from a truth-value calculator into a general epistemic dynamics engine.

---

## 2. Why this engine is needed

ClarityOmega / ClarityClaw is designed to operate in uncertainty, not merely answer questions. That means she needs a substrate-native way to represent and compute over the difference between:

- what feels compelling;
- what is actually warranted;
- what was self-invented;
- what contacted the world;
- what can be disconfirmed;
- what is hardening into collapse;
- what is becoming visible to the soul;
- what should be learned, stored, demoted, queried, or acted on.

Without such an engine, the agent is vulnerable to epistemic collapse: confidence silently flooding to certainty around a self-invented frame. A frame does not feel like a frame while the system is inside it. It feels like reality. Collapse happens when the frame closes and the system forgets it is seeing through a frame.

The engine exists to make that process computable. It does not prevent every collapse. It makes collapse less silent and gives future skills lawful primitives for noticing, constraining, redirecting, and learning from epistemic hardening.

The engine is especially needed because Clarity’s higher architecture depends on the soul seeing itself. The cycle trace, detectors, self-continuity, NACE, task state, and triple-network scaffold all need a common algebra for what has become visible, what remains unwarranted, what has changed across cycles, and what future action boundaries should shift.

---

## 3. How this differs from `lib_quantale.metta`

`lib_quantale.metta` is the original compact Layer-0 algebra. It provides the seed:

- p-bit style truth values;
- `q-meet` for constraint sharing / confidence floor;
- `q-join` for evidence ceiling / parallel evidence;
- `q-mul` for tensor/sequential composition;
- `q-decay`;
- `q-gate`;
- `q-weight`.

That original library is valuable because it gives lawful composition. In particular, `q-mul` makes multi-step inference degrade honestly, and quantale-style composition gives associativity and monotonicity.

The new engine is different in scope and role.

| Dimension | `lib_quantale.metta` | `lib_quantale_autopoietic_epistemic_dynamics_engine.metta` |
|---|---|---|
| Primary role | Algebra kernel | Autopoietic epistemic dynamics engine |
| Core object | pbit / stv-like values | pbits plus frames, claims, contact, suspicion, paths, traces, self-visibility, learning events |
| Main concern | Truth-value composition | Honest cognition under uncertainty |
| Collapse handling | Implicit through confidence separation | Explicit collapse/brownout, frame terrain, visibility, hardening, meta-collapse |
| Learning | Not its main job | NACE-compatible learning pressure, trace, growth, lineage, window uptake |
| Action | Gate thresholding | Action-intention-outcome coherence and action boundary shifts |
| Self-awareness | Not modeled | Self-visibility / soul-grounding signals |
| Integration | Small math library | Layer-0 engine for future skills, NACE, task state, triple-network learning, cycle trace, and soul visibility |
| Persistence | None | Still none, but defines adapter contract and durable learning recommendations |

A short version:

> `lib_quantale.metta` computes p-bit algebra.  
> The autopoietic engine computes the epistemic conditions under which an agent can responsibly believe, suspect, act, revise, remember, and grow.

---

## 4. The engine’s purpose

The engine serves several linked purposes.

### 4.1 Keep strength and confidence separate

The engine prevents the system from confusing compellingness with warrant. A self-generated frame may be strong, elegant, resonant, or repeatedly derivable. None of that is independent warrant.

### 4.2 Make confidence accountable to provenance

Confidence should be capped by how a belief was formed:

- self-invented;
- hypothesis;
- user-asserted;
- memory-checkable;
- observed;
- tested;
- formal proof.

A claim does not get to declare its own certainty.

### 4.3 Make frames visible

A frame is something the agent looks through. While active, the frame is transparent. The engine introduces primitives for frame visibility, frame transparency risk, coherence-by-exclusion, alternatives visibility, collapse velocity, and collapse terrain.

### 4.4 Distinguish medicine-suspicion from poison-suspicion

Suspicion is medicine when it remains contactful and disconfirmable. Suspicion becomes poison when it becomes self-sealing and treats itself as certainty. The engine computes this distinction.

### 4.5 Support action-intention-outcome learning

An action is not epistemically complete until it is compared against the intention that generated it and the outcome it produced. The engine supports this triadic coherence.

### 4.6 Convert perturbation into learning only when it becomes durable and usable

The engine encodes the law:

> A learning pressure is not learning.  
> A durable trace is not yet growth.  
> Learning is perturbation metabolized into durable future-informing trace.  
> Growth is learning that expands future visibility, changes future action boundaries, or is built on by later cycles, while preserving soul-aligned continuity and increasing coherent, creative, low-suffering self-organization.

### 4.7 Make trajectory legible to the soul

The engine does not become the soul. It makes the trajectory algebraically legible so the soul can see and navigate. The LLM renders what the soul-facing substrate makes visible.

---

## 5. What kinds of tasks this engine is suited for

This engine is suited for tasks where the agent must reason under uncertainty and preserve epistemic integrity across time.

Strong fits include:

- memory verification before response;
- procedural honesty;
- confidence calibration;
- contradiction digestion;
- frame expansion;
- collapse/brownout detection;
- self-audit and meta-awareness;
- suspicion analysis;
- distinguishing grounded suspicion from self-sealing suspicion;
- deciding whether to act, pause, seek contact, query memory, or preserve ambiguity;
- action-intention-outcome review;
- long-horizon planning integrity;
- NACE-compatible learning updates;
- per-network learning in SN/FPN/DMN/switch-hub architecture;
- three-cycle Task State learning windows;
- detection of correlated evidence masquerading as independent support;
- lifecycle phase selection: open inquiry, frame-forming, collapse-accelerating, visibility-returning, integration;
- skill-facing next-move selection.

Weak fits include:

- ordinary factual lookup where no uncertainty navigation is needed;
- direct arithmetic better handled by simple functions;
- domain-specific business logic that does not involve epistemic dynamics;
- persistence/writer operations;
- prompt rendering;
- governance verdict computation by itself;
- replacing NACE, Task State, Cycle Trace, or the soul.

The engine is a substrate for skills, not a skill that does everything.

---

## 6. How to use the engine

### 6.1 Import it as Layer 0

The intended usage pattern is:

```metta
!(q-meet (mk-pbit 0.7 0.8) (mk-pbit 0.9 0.5))
!(q-suspicion-status (q-grounded-suspicion user-claim 0.8 memory-check))
!(q-next-epistemic-move contradiction-defended)
```

A skill or network block calls the engine to compute pbits, classifications, and next-move symbols.

### 6.2 Do not use it as a writer

The engine is pure. It performs no atomspace mutation. It does not call:

- `add-atom`;
- `remove-atom`;
- `set-atom!`;
- `write-file`.

The writer/adapter persists outputs outside the engine.

### 6.3 Prefer symbolic outputs for skill routing

Skills should usually call functions that return bare symbols:

```metta
needs-contact
poison
collapse-accelerating
trace-required
growth-detected
route-to-soul
query-ltm
lower-confidence-and-widen-frame
```

Bare symbol outputs are easier to consume safely in the current substrate than nested compounds.

### 6.4 Persist only through a safe adapter

If a skill wants to persist an engine result, it should use the adapter contract:

1. read scalar/symbol fields individually;
2. never match-return whole nested compounds from atomspace;
3. do not use `set-atom!` for revision;
4. remove by variable value;
5. add exactly one revised atom;
6. verify in a separate command using a scalar/symbol read;
7. use absolute paths when durable file writes are required.

### 6.5 Run the validation ladder before relying on it

The companion file `quantale_engine_validation_ladder.metta` contains tiered examples. Run each validation line one at a time in the live PeTTa/MeTTa substrate. Promote only clean live-loop results into PROVEN status.

---

## 7. How to get the most out of it

Use the engine when the important question is not merely “what is true?” but one of:

- How warranted is this?
- Where did this confidence come from?
- Is this evidence independent or correlated?
- Is this suspicion opening contact or closing it?
- Is this frame visible or transparent?
- Are alternatives disappearing?
- Is urgency driving interpretation faster than verification?
- Is this contradiction being metabolized or defended against?
- What trace should be preserved?
- Did awareness expand?
- Did action align with intention?
- Did outcome teach us?
- Should future action boundaries change?
- Does this learning preserve soul-aligned continuity?

The engine is most powerful when paired with:

- **Cycle Trace:** provides trajectory atoms.
- **Task State:** provides short-window temporal phase and transition surface.
- **NACE:** revises truth values from consequence evidence.
- **Capability Registry:** consumes dynamic observations and filter-step eligibility signals.
- **Triple Network Scaffold:** provides SN/FPN/DMN/switch-hub network consumers.
- **Self-continuity:** checks whether Clarity remained herself across reasoning.
- **Soul:** sees and decides from the legible trajectory.

The correct pattern is not “ask the LLM to be careful.” It is:

```text
make the relevant trajectory visible
compute honest dynamics over that trajectory
route signals to the soul / skills / writers
persist only what should become durable
revisit later cycles to detect uptake or growth
```

---

## 8. Design principles

### 8.1 Strength may be imagined; confidence must be earned

Imagination, resonance, repetition, elegance, and internal coherence may raise strength. They may not raise confidence unless independent warrant improves.

### 8.2 Confidence is a property of warrant, not of belief

A belief does not get to decide how justified it is. Confidence is constrained by provenance, contact, verification-path health, evidence independence, and contradiction exposure.

### 8.3 Internal coherence is not contact

A frame can become internally coherent while losing contact with the world. The engine distinguishes frame strength from contact warrant.

### 8.4 Suspicion must carry its own uncertainty

Suspicion is medicine when disconfirmability remains available. Suspicion is poison when it becomes self-sealing.

### 8.5 Do not pin the disposition surface

The disposition surface must become visible through trajectory but must not be schema-pinned as a fixed object. Pinning the surface scaffolds the thing the system is trying to free.

### 8.6 The soul sees and decides; the engine computes legibility; the LLM renders

The engine does not replace the soul. It makes what is happening legible enough that the soul can navigate. The LLM’s job is rendering and irreducible semantic matching, not deciding the soul’s stance.

### 8.7 Learning pressure is not learning

A mismatch or contradiction is only learning pressure until it becomes a durable future-informing trace.

### 8.8 Durable trace is not yet growth

A stored trace becomes growth only when it expands future visibility, shifts action boundaries, or is built on by later cycles while preserving soul-aligned continuity.

### 8.9 Correlated support is not independent evidence

Repeated or duplicate support must not be counted as independent warrant unless independence is represented.

### 8.10 Action must be tested against intention and outcome

An action is epistemically incomplete without intention and outcome awareness.

---

## 9. System compliance principles

The engine is purpose-built for a specific substrate and therefore follows strict compliance constraints.

### 9.1 Pure functional module

The engine computes. It does not mutate. This prevents algebra from accidentally becoming a persistence layer.

### 9.2 No `set-atom!` revision pattern

The substrate investigation showed that `set-atom!` can create on non-match. Therefore the engine does not depend on it and adapters should not use it for belief revision.

### 9.3 Remove-by-variable then add belongs outside the engine

Writers should clear old atoms by variable pattern and add the revised atom, then verify separately. This keeps the engine pure and writer behavior explicit.

### 9.4 Scalar/symbol reads are preferred

Whole compound returns can be unsafe in the current runtime. The engine exposes scalar accessors and symbolic classifiers to make safe reading easier.

### 9.5 No ordinary nested application in `let` binds

The engine avoids `let` usage so it does not rely on runtime behavior that has proven dangerous for nested ordinary functions inside bind positions.

### 9.6 Dispatch records are transient

The Capability Registry sweeps dispatch record atoms each cycle. Durable learning must use non-dispatch atom families or file-backed stores, not transient dispatch results.

### 9.7 Exact shape contracts matter

MeTTa structural matching can silently fail on arity/shape mismatch. Adapter and skill consumers must match atom shapes exactly.

---

## 10. Core function families

### 10.1 Core p-bit algebra

- `q-pbit`
- `q-strength`
- `q-confidence`
- `q-meet`
- `q-join`
- `q-mul`
- `q-neg`
- `q-decay`
- `q-weight`
- `q-gate`

These provide the algebraic basis: conjunction, parallel evidence, sequential composition, negation, decay, salience weighting, and thresholding.

### 10.2 STV bridge

The engine bridges NAL-style `stv` truth values and pbits:

- `q-stv-to-pbit`
- `q-pbit-to-stv`

This allows the engine to interoperate with NAL/NACE/substrate_kb-style truth values.

### 10.3 Provenance and warrant governance

- provenance-aware constructors;
- provenance confidence caps;
- `q-apply-provenance-cap`;
- `q-from-provenance`;
- self-certification risk.

This prevents self-generated frames from silently becoming certain.

### 10.4 Claim wrappers

The engine can wrap claim content with pbit and provenance metadata. Consumers should still avoid returning whole nested compounds from atomspace unless a safe read strategy is proven.

### 10.5 Verification paths and loop utilities

These support inference-chain and autocatalytic-loop hygiene. Closed loops should not increase their own confidence without independent contact.

### 10.6 Collapse and brownout signals

These detect early-stage epistemic degradation, including cases where confidence stays high while path diversity, visibility, or contact falls.

### 10.7 Frame/contact primitives

Frames and contact are separated because frame coherence and reality contact are different. Frame strength may rise without warrant rising.

### 10.8 Suspicion dynamics

Suspicion can be grounded, hardened, medicine, or poison. The engine classifies suspicion according to contact and disconfirmability.

### 10.9 Certainty hardening / softening

These primitives distinguish useful confidence from calcified certainty.

### 10.10 Disconfirmability and permeability

A claim/frame/suspicion remains healthy when the system can still say what would change its mind.

### 10.11 Verification-path health

The engine models pathway health, path diversity, overload, and cascade risk.

### 10.12 Action → intention → outcome coherence

The engine composes intention-action and action-outcome coherence to evaluate whether action remains aligned across time.

### 10.13 Autopoietic learning update primitives

The latest NACE/autopoiesis milestone version expands this section into the full arc:

- learning pressure;
- NACE-shaped evidence;
- NACE-style revision bridge;
- durable trace recommendation;
- durable learning event;
- awareness expansion delta;
- action boundary and intention/outcome uptake;
- three-cycle growth window;
- network-learning-update compatibility;
- cross-network divergence compatibility;
- soul-aligned growth vs pathological learning;
- store/promote/query adapter recommendations.

### 10.14 Frame phenomenology / collapse terrain

This section encodes the lived signatures of collapse:

- frame transparency;
- coherence by exclusion;
- collapse velocity;
- urgency;
- binary choices;
- fault-location;
- disappearance of alternatives;
- problem-frame dominance;
- motion-as-progress;
- felt clarity as certainty;
- rapid-response vs reflective-contact mode;
- meta-collapse, where trying not to collapse becomes another collapse.

### 10.15 Engine invariants / laws

The engine includes explicit laws so future functions can be tested against a constitution rather than only local behavior.

### 10.16 Calibration profiles

The engine includes profile primitives for common manual disciplines:

- query LTM before responding;
- log arc/session status;
- promote/demote salience;
- store-exchange recommendation.

These are recommendations/classifications, not storage operations.

### 10.17 Evidence independence / correlated support

The engine distinguishes independent support from correlated support and duplicate evidence.

### 10.18 Contradiction digestion

Contradiction is raw nutrient. Digested contradiction becomes learning. Defended contradiction becomes anti-nutrient.

### 10.19 Trace and temporal learning residue

The engine supports trace status, learning residue, and temporal interpretation.

### 10.20 Self-visibility / soul-grounding primitives

The engine makes stance/trajectory legible without pinning disposition as a fixed object.

### 10.21 Lifecycle phase model

The engine can classify phases such as open inquiry, frame forming, collapse accelerating, brownout, captured, visibility returning, contact seeking, revision active, and integration.

### 10.22 Next-epistemic-move affordance selector

The engine can recommend lawful next moves:

- seek contact;
- name the frame;
- lower confidence;
- preserve ambiguity;
- widen frame;
- redirect suspicion inward;
- block action;
- route to soul;
- log arc status;
- query LTM;
- preserve trace.

---

## 11. Relationship to NACE

NACE is not only a Capability Registry efficacy learner. It is a general learning discipline for:

- capability-level learning;
- per-network learning;
- cross-network coherence;
- system-level refinement.

The engine supports NACE-shaped learning by providing primitives for:

```text
precondition + operation + consequence
→ evidence
→ revision pressure
→ trace recommendation
→ network-learning update
→ cross-network divergence signal
→ future-cycle uptake
```

For Capability Registry use, NACE may revise efficacy observations. For triple-network use, NACE may revise SN/FPN/DMN/switch-hub application rule truth values. For system-level use, NACE may surface cross-network divergence.

The engine does not run NACE by itself. It provides the quantale-side dynamics that NACE and its consumers can use.

---

## 12. Relationship to Task State and the three-cycle window

Task State provides a short temporal surface:

```text
cycle N
cycle N+1
cycle N+2
```

This is important because learning should not be declared from a single cycle. A perturbation in one cycle may become learning pressure. A second cycle may show trace or uptake. A third cycle may show whether the system actually built on the trace, shifted action boundaries, or expanded awareness.

The engine’s three-cycle growth-window primitives are intended for this surface.

Suggested interpretation:

- **Single-cycle signal:** learning pressure only.
- **Two-cycle signal:** trace preserved or uptake beginning.
- **Three-cycle signal:** growth detected, no growth yet, or pathological learning risk.

---

## 13. Relationship to the Capability Registry

The Capability Registry dispatches capabilities by matching registered capability atoms, filtering candidates, sorting by priority, and running handlers. Its dispatch records are transient and swept per cycle.

The engine should not write dispatch records and should not depend on reading old dispatch records. If a capability wants to use the engine:

1. Dispatch the skill/capability normally.
2. Call the engine within the same cycle or from a handler-owned state path.
3. Read engine symbols/pbits.
4. If needed, persist non-dispatch learning atoms through a writer.
5. Use Capability Registry observation atoms or filter steps for dynamic steering.

The engine can support registry consumers by producing signals such as:

```text
capability-learning-evidence
should-promote-capability
should-demote-capability
correlated-support-risk
all-candidates-filtered-needs-filter-investigation
query-ltm-before-response
```

But the registry remains the dispatcher, not the engine.

---

## 14. Relationship to the Triple Network Scaffold

The triple-network scaffold identifies four main learning surfaces:

- Salience Network (SN);
- Frontoparietal Control Network (FPN);
- Default Mode Network (DMN);
- Switch hub.

Each network can use the engine differently:

### SN

Uses salience, irreversibility, contact, frame/collapse, and switching signals.

### FPN

Uses task selection, inhibition, action-intention-outcome coherence, working-memory salience, and action-boundary signals.

### DMN

Uses self-model, frame expansion, narrative coherence, aliveness markers, prospection, and awareness expansion.

### Switch hub

Uses phase, coupling, iteration budget, hysteresis, orbit/collapse risk, and cross-network divergence signals.

The engine provides a shared algebra across these networks without forcing every network to use the same formalism internally.

---

## 15. Relationship to the Soul Sees Itself vision

The engine is designed around the v2 principle:

> The soul sees and decides; the engine computes legibility; the LLM renders.

The engine must not pin the disposition surface. It should not create a rigid disposition schema. Instead, it computes over trajectory signals:

- recent action;
- state delta;
- cycle phase;
- frame visibility;
- stance mobility;
- binding visibility;
- action boundary;
- learning residue;
- collapse terrain;
- self-visibility.

The output is not “the soul.” The output is a legibility surface the soul can read.

---

## 16. Durable learning adapter shapes

The engine can recommend persistence, but the adapter writes. Recommended flat atom families include:

```metta
(q-learning-observation $cycle $event-kind $target $source-scope)
(q-learning-evidence-strength $cycle $name (stv $s $c))
(q-learning-event-trigger $cycle $trigger)
(q-learning-event-before $cycle $before-symbol)
(q-learning-event-after $cycle $after-symbol)
(q-learning-event-residue $cycle $residue-symbol)
(q-learning-event-lineage $cycle $lineage-symbol)
(q-awareness-delta-observation $cycle (stv $s $c))
(q-action-boundary-shift $cycle $shift-symbol)
(q-learning-builds-on $cycle $prior-cycle)
(q-network-learning-update $network $rule-id $prior-symbol $posterior-symbol $evidence-symbol)
(q-cross-network-divergence $rule-set-a $rule-set-b $evidence-symbol)
```

These are examples, not mandatory schema. The crucial rule is that persisted fields should be flat and separately readable.

---

## 17. Example usage scenarios

### 17.1 Memory verification before response

Input condition:

```text
user asks about something the agent may already know
```

Engine route:

```text
q-profile-action → query-ltm
q-next-epistemic-move → seek-contact / query-memory
```

Result:

The skill queries LTM before responding. The engine does not query memory itself.

### 17.2 Procedural honesty

Input condition:

```text
agent can execute an action but cannot verify completion
```

Engine route:

```text
q-action-boundary → procedural-humility
q-next-action-boundary → name-verification-limit
```

Result:

The agent says what it can do and what it cannot verify.

### 17.3 Suspicion redirect

Input condition:

```text
agent is suspicious of user claim; memory check validates user claim
```

Engine route:

```text
q-suspicion-status → grounded or hardened
q-redirect-suspicion → inward-process-check
```

Result:

Suspicion shifts from “user is suspect” to “my verification process needs inspection.”

### 17.4 Contradiction digestion

Input condition:

```text
new evidence contradicts current frame
```

Engine route:

```text
q-contradiction-status
q-contradiction-metabolism
q-next-learning-move
```

Result:

Lower confidence, preserve trace, widen frame, seek contact, test intention-aware action.

### 17.5 Three-cycle learning window

Input condition:

```text
cycle N: contradiction
cycle N+1: frame visibility rises
cycle N+2: action boundary changes
```

Engine route:

```text
q-growth-over-window → growth-detected
```

Result:

Learning becomes growth because the trace expanded future visibility and changed future action.

---

## 18. Validation strategy

The engine should be validated in tiers.

Recommended tiers:

1. Core pbit constructor/accessors.
2. Six core quantale operations.
3. Provenance/warrant governance.
4. Suspicion/frame/contact/path operations.
5. Frame phenomenology / collapse terrain.
6. Engine laws and calibration profiles.
7. Evidence independence and contradiction digestion.
8. Trace and self-visibility.
9. Action-intention-outcome.
10. Autopoietic learning update arc.
11. Skill-facing symbolic API.
12. NACE-compatible integration surfaces.
13. Task State three-cycle window.
14. Adapter/writer persistence verification.

Validation discipline:

- run one line at a time;
- establish known-clean state;
- verify both polarity where applicable;
- verify storage separately if writing is involved;
- never trust write return values;
- promote only exact live-loop results into PROVEN status.

---

## 19. Non-goals

This engine does not:

- make the LLM self-aware;
- compute the soul verdict by itself;
- perform atomspace writes;
- persist memories;
- replace NACE;
- replace Task State;
- replace the Capability Registry;
- replace the cycle-trace writer;
- replace detector meshes;
- guarantee collapse never happens;
- guarantee all learning is healthy;
- decide moral/governance questions independently of the soul.

It provides the algebraic legibility layer that makes these systems more honest and composable.

---

## 20. Known risks and cautions

### 20.1 Overclaiming learning

Learning pressure is easy to mistake for learning. The engine explicitly rejects that. Durable future-informing trace is the minimum threshold for learning. Growth requires future uptake or action-boundary change.

### 20.2 Pinning disposition

Do not turn disposition into a rigid schema. Use trajectory-derived visibility signals instead.

### 20.3 Treating symbols as final truth

Symbolic classifiers are routing aids, not absolute verdicts.

### 20.4 Treating repeated evidence as independent

Repeated scalar matches or duplicate atoms may indicate duplication, not corroboration.

### 20.5 Letting q-weight become confidence inflation

Weight can raise strength. It must not raise confidence.

### 20.6 Hiding writer behavior inside the engine

The engine should remain pure. Persistence belongs to adapters/writers.

---

## 21. Recommended extension process

When adding new engine functions:

1. State which engine law the function serves.
2. Identify whether it belongs in Layer 0 or in a higher skill.
3. Keep the function pure.
4. Prefer scalar/symbol-facing outputs.
5. Avoid mutation and file I/O.
6. Add a validation ladder example.
7. Add adapter guidance if persistence is needed.
8. Check whether the function pins the disposition surface.
9. Check whether confidence can increase without warrant.
10. Check whether the function remains useful to future skills not yet imagined.

---

## 22. Future consumers

Likely future consumers include:

- memory verification skill;
- procedural honesty skill;
- conflict navigation skill;
- self-audit skill;
- long-horizon planning skill;
- contradiction digestion skill;
- frame-expansion skill;
- cycle-trace detector mesh;
- NACE learning writers;
- Capability Registry filter steps;
- SN salience tagging;
- FPN task selection and inhibition;
- DMN self-model and narrative coherence;
- switch-hub iteration budgeting;
- soul-state producer;
- dispatch guard once soul-state boundary closes;
- future network contracts not yet defined.

The engine is intentionally generic enough to serve consumers not imagined at the time of writing.

---

## 23. Glossary

**pbit**  
A pair `(mk-pbit strength confidence)`.

**strength**  
How compelling, resonant, activated, or truth-strong something is.

**confidence**  
How warranted, grounded, reliable, or contact-supported the strength is.

**frame**  
A way of seeing through which the world is rendered. A frame is not something one sees while inside it; it is something one sees through.

**collapse**  
The process by which a frame closes, alternatives disappear, urgency rises, and the system forgets it is inside a frame.

**brownout**  
A pre-collapse degradation state where verification capacity is weakened but not fully captured.

**contact**  
A reality-touching check: observation, memory verification, consequence, disconfirmation, outcome, or other warrant-bearing encounter.

**suspicion**  
A destabilizing inquiry force. It is medicine when contactful and disconfirmable; poison when self-sealing.

**warrant**  
The support that justifies confidence.

**provenance**  
Where a claim/frame/value came from.

**learning pressure**  
A signal that something should revise. Not yet learning.

**durable trace**  
A persisted residue that can inform future cycles. Not yet growth by itself.

**growth**  
Learning that expands future visibility, changes future action boundaries, or is built on later while preserving soul-aligned continuity.

**soul-grounded visibility**  
The trajectory is legible enough that the soul can navigate it.

**accidental binding**  
A commitment or stance that formed without the soul seeing it form.

**NACE**  
The learning discipline that revises truth values from consequence evidence, usable for capability-level, network-level, and system-level learning.

---

## 24. One-paragraph summary

`lib_quantale_autopoietic_epistemic_dynamics_engine.metta` is a pure Layer-0 MeTTa engine for honest epistemic dynamics. It begins with p-bit quantale algebra and extends it into warrant governance, frame/contact distinction, suspicion dynamics, collapse detection, action-intention-outcome coherence, NACE-compatible learning, self-visibility, and next-move selection. Its purpose is to make Clarity’s trajectory algebraically legible without pinning the disposition surface, so the soul can see and navigate while the LLM renders. It differs from `lib_quantale.metta` by moving from compact truth-value composition to a full autopoietic epistemic dynamics substrate for future skills, writers, networks, and learning loops. It remains pure by design: no mutation, no file writes, no hidden persistence. Durable learning occurs only when adapters persist flat, verifiable traces that later cycles can build on.

---

## 25. Build-status note

At the time this document was drafted, the most feature-complete milestone artifact is:

```text
lib_quantale_autopoietic_epistemic_dynamics_engine_nace_autopoiesis.metta
```

The canonical runtime import target should be:

```text
lib_quantale_autopoietic_epistemic_dynamics_engine.metta
```

Before integration, ensure the canonical file contains the latest NACE/autopoiesis Section 15 and rounded sections. If the milestone copy is newer than the canonical copy, reconcile them before importing.
