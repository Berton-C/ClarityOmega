# Hyperseed Formalization Catalog v1

**Version:** v1 (May 1, 2026)
**Author:** Berton Bennett with Claude
**Status:** First-pass survey of formalization units across the 30 Hyperseed v8 markdown files, mapped to ClarityOmega's network contracts (Artifact 4 v1.1) and the eight components (Artifact 5 v3.0). Companion document: `Hyperseed_to_Network_Synergy_Map_v1.md`.
**Purpose:** Catalog the coherent formalization units in the Hyperseed corpus that ClarityOmega's build needs, with precise location pointers, target network/contract assignments, and wiring readiness stratification, so this document can be used as (a) a quick build-time lookup, (b) a source of self-contained units to pass to Clarity for in-substrate construction, and (c) a guide for Claude when generating MeTTa from formalizations.

---

## How to read this document

### Definition of a "coherent formalization unit"

A coherent formalization unit (CFU) is a small cluster of related Hyperseed definitions, theorems, and operators that together implement one buildable capability. A unit may be a single definition with its supporting theorem (e.g., the p-bit quantale plus its sanity theorems) or a few definitions that compose into a single operator (e.g., morphic resonance update plus anti-resonance plus monotonicity proposition). The granularity is chosen so that each unit corresponds to one MeTTa-buildable substrate function or one well-bounded cluster of substrate atoms.

The catalog contains roughly 60 units. The full Hyperseed corpus contains ~440 named definitions/theorems/lemmas; the catalog clusters these into buildable units rather than enumerating each one separately. Helper lemmas in files 28-30 are cited where they support a unit but are not given separate rows; they are noted in the unit's "supporting helpers" field.

### Field definitions per row

Each unit has the following fields:

- **Unit ID** — a stable identifier for cross-reference (UNIT-XXX).
- **Unit name** — short descriptive name.
- **Source file(s)** — which Hyperseed file(s), by number.
- **Section / definition refs** — section numbers and Definition/Theorem numbers within the file. Precise enough to navigate to immediately.
- **Hyperseed-Concept refs** — the concept numbers from the Hyperseed-Concept system used in the corpus, where cited.
- **Purpose (one line)** — what this unit does formally.
- **Target network** — SN, FPN, DMN, switch hub, memory layer, cross-cutting, or N/A (long-tail).
- **Contract sub-function** — which sub-function in Artifact 4 v1.1 Section 5 this unit implements; or which Artifact 5 v3.0 component (2a-2h); or which channel from Artifact 4 v1.1 Section 6.
- **Wiring readiness** — `READY-NOW`, `READY-AFTER-X`, or `LONG-TAIL`. See definitions below.
- **Prerequisites** — other unit IDs that must be built first for this one to be soundly implementable.
- **Supporting helpers** — helper lemmas/theorems (typically from files 28-30) that ground the unit's correctness.
- **Deep-pass needed** — flag indicating whether a follow-up deep read is required before MeTTa construction (true/false).
- **Notes** — anything else.

### Wiring readiness stratification

- **READY-NOW**: Prerequisites are either already in the codebase, are themselves READY-NOW units, or are foundational (p-bit quantale, paraconsistent ops). Can be implemented in MeTTa with current substrate vocabulary plus the unit's own definitions. The math is finite, discrete, and computationally explicit.
- **READY-AFTER-X**: Has one or two named prerequisite units that must be built first. Math is finite/discrete but depends on a substrate primitive not yet in place.
- **LONG-TAIL**: Mathematically correct and important to the framework, but either (a) requires continuous-time or PDE infrastructure not appropriate for current MeTTa substrate, (b) requires categorical machinery (∞-groupoids, enriched categories) beyond what the near-term build needs, or (c) belongs to the long-horizon unlock layer where the formalization may suggest *new* networks rather than implement current ones.

### How to use this catalog

For a new MeTTa build session:
1. Identify the Artifact 4 contract sub-function or Artifact 5 component being built.
2. Filter the catalog by Target network and Contract sub-function.
3. Confirm wiring readiness; if READY-AFTER-X, build the prerequisite units first.
4. If "Deep-pass needed" is true, fetch the Hyperseed file at the cited section and produce a deep-read note before MeTTa construction begins.
5. Implement using the unit's definitions/theorems as the formal grounding. Cite the unit ID in the resulting MeTTa file's docstring for traceability.

For passing a unit to Clarity to construct in her own atom space:
1. Locate the unit in this catalog.
2. Fetch the Hyperseed file at the cited section.
3. Excerpt the definitions/theorems plus the unit's "Purpose" and "Contract sub-function" assignment.
4. Hand to Clarity with the contract context she needs from Artifact 4/5.

---

## Section A: Foundational units (substrate primitives)

These are the formalizations everything else builds on. They are not themselves implementations of network contract sub-functions; they are the mathematical substrate that other units stand on. Most are READY-NOW because they have no prerequisites within Hyperseed itself.

### UNIT-001 · p-bit quantale (the foundational truth-value algebra)
- **Source file(s):** 3, 4
- **Section / definition refs:** File 3 §3.4 Definition 4 (p-bit domain). File 4 §3.5 Definition 5 (Negation), Definition 6 (Evidence-style conjunction/disjunction), Definition 7 (Implication), Definition 8 (Commutative quantale), Definition 9 (Canonical commutative p-bit quantale).
- **Hyperseed-Concept refs:** Paraconsistent truth values; quantale; evidence-based logic.
- **Purpose:** Define the p-bit truth-value algebra `(v+, v-) ∈ [0,1]²` with negation, conjunction, disjunction, implication, and the commutative quantale structure (V, ≤, ⊕, ⊗, e). This is the algebra in which all other Hyperseed formalizations express truth, evidence, and weighted relations.
- **Target network:** Cross-cutting (substrate primitive used by all networks).
- **Contract sub-function:** N/A — this is foundational substrate. Every other unit cites it.
- **Wiring readiness:** READY-NOW.
- **Prerequisites:** None.
- **Supporting helpers:** File 4 contains its own sanity theorems for the p-bit quantale (after Definition 9).
- **Deep-pass needed:** False. Definitions are explicit and computationally complete.
- **Notes:** This is the single most-leveraged unit in the catalog. Build first. Once present in MeTTa as a small library (truth-value type plus operators), nearly every subsequent unit can be implemented.

### UNIT-002 · V-valued relations and quantale matrix composition
- **Source file(s):** 4
- **Section / definition refs:** Definitions 10-12 (V-valued relations, quantale matrix composition, identity V-relation).
- **Hyperseed-Concept refs:** Relational composition; weighted graphs.
- **Purpose:** Define V-valued relations R: X×Y → V, their quantale composition `(R ∘ S)(x,z) = ⊕_y R(x,y) ⊗ S(y,z)`, and the identity V-relation. This is the relational algebra over the p-bit quantale.
- **Target network:** Cross-cutting.
- **Contract sub-function:** N/A — substrate primitive.
- **Wiring readiness:** READY-NOW.
- **Prerequisites:** UNIT-001.
- **Supporting helpers:** File 4 includes sanity proofs for associativity and identity laws.
- **Deep-pass needed:** False.
- **Notes:** Foundational for SN salience aggregation, FPN inhibition rules, and DMN narrative coherence. Build immediately after UNIT-001.

### UNIT-003 · V-enriched category (thin form) and V-functor
- **Source file(s):** 4, 5
- **Section / definition refs:** File 4 Definition 13 (V-enriched category, thin form). File 5 Definition 14 (V-functor, thin form).
- **Hyperseed-Concept refs:** Enriched categories; structure-preserving maps.
- **Purpose:** Define V-enriched categories as the abstract structure underlying weighted-relational reasoning, and V-functors as the morphisms between them. Provides the categorical layer for cross-context translation.
- **Target network:** Cross-cutting; specifically used by DMN narrative-thread translation across contexts.
- **Contract sub-function:** Not directly; supports DMN cross-context translation and SN context-shifting.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-001, UNIT-002. Depends on whether the build needs the categorical abstraction or can use the V-relation level directly.
- **Prerequisites:** UNIT-001, UNIT-002.
- **Supporting helpers:** None specifically.
- **Deep-pass needed:** False; deferrable until the categorical layer is needed.
- **Notes:** May be deferrable. Most near-term builds can use V-relations directly without ascending to the categorical layer.

### UNIT-004 · Logic-to-complex map (paraconsistent → complex amplitude)
- **Source file(s):** 5, 6
- **Section / definition refs:** File 5 Definition 18 (Logic-to-complex map σC). File 6 Definition 35 (p-bit to complex mapping σC).
- **Hyperseed-Concept refs:** Resonance; interference; complex amplitudes.
- **Purpose:** Define the map σC: V → C from p-bit truth values to complex amplitudes, enabling interference-based resonance scoring. Pairs each p-bit `(v+, v-)` with a complex number that supports phase composition.
- **Target network:** SN (resonance reward computation); DMN (narrative coherence via resonance).
- **Contract sub-function:** SN salience-tagging affect computation; DMN narrative-thread coherence scoring; switch-hub iteration-budget composition.
- **Wiring readiness:** READY-NOW.
- **Prerequisites:** UNIT-001.
- **Supporting helpers:** None.
- **Deep-pass needed:** False. The mapping is explicit.
- **Notes:** Used by every resonance-related unit. Build alongside UNIT-001 if resonance scoring is in early scope.

### UNIT-005 · Importance valuation and salience weights
- **Source file(s):** 5, 6
- **Section / definition refs:** File 5 Definition 15 (Salience/importance weights). File 6 Definition 26 (A concrete importance valuation).
- **Hyperseed-Concept refs:** Salience; observer-relative weighting.
- **Purpose:** Define an importance valuation µ: X → V assigning V-valued weight to entities, and the concrete importance scheme used in worked examples. Enables weighted aggregation across entities.
- **Target network:** SN (salience-tagging level), FPN (working-memory priority).
- **Contract sub-function:** SN `(sn-salience-tag $signal $level $affect $irreversibility)` level field; FPN `(fpn-working-memory $slot $content $priority)` priority field.
- **Wiring readiness:** READY-NOW.
- **Prerequisites:** UNIT-001.
- **Supporting helpers:** None.
- **Deep-pass needed:** False.
- **Notes:** Direct fit for SN salience level and FPN working-memory priority. Build immediately for those substrate atoms.

---

## Section B: Salience Network units

Units that implement the SN's salience-tagging, switching, and learning sub-functions per Artifact 4 v1.1 Section 5.1 and Section 5.4.

### UNIT-010 · Weakness of a failed-distinction set (the simplicity primitive)
- **Source file(s):** 5, 6
- **Section / definition refs:** File 5 Definitions 16-17 (Crisp failed-distinction set, Weakness). File 6 Definition 25 (Weakness of a V-valued relation).
- **Hyperseed-Concept refs:** Hyperseed-Concept 202 (weakness); Hyperseed-Concept 100 (effort); Hyperseed-Concept 169 (simplicity).
- **Purpose:** Define weakness `w(H)` as importance-weighted failure to distinguish. Captures "how much does this set of indistinctions matter?" Provides the scalar-valued simplicity primitive used to compare patterns and policies.
- **Target network:** SN (salience-level computation).
- **Contract sub-function:** SN salience-tag level field; provides the formal grounding for "this signal matters at level X".
- **Wiring readiness:** READY-NOW.
- **Prerequisites:** UNIT-001, UNIT-005.
- **Supporting helpers:** File 5 Theorem 1 (Weakness is monotone under adding undistinguished pairs); File 5 Proposition 1 (Weakness monotone in arguments under unions).
- **Deep-pass needed:** False.
- **Notes:** Highest-leverage SN-side unit. The salience level field becomes a weakness computation over the input signal's indistinctions from existing patterns.

### UNIT-011 · Pattern as constraint-set on pairs and pattern support
- **Source file(s):** 6
- **Section / definition refs:** Definitions 27-28 (Pattern as constraint-set on pairs; Pattern support).
- **Hyperseed-Concept refs:** Hyperseed-Concept 130 (pattern); pattern intensity.
- **Purpose:** Formalize a pattern as a finite set of constraints on entity pairs, and pattern support as the V-valued degree to which a context relation satisfies those constraints. The substrate-level definition of "pattern" used throughout Hyperseed.
- **Target network:** SN (pattern matching against priority structure), DMN (self-model patterns), FPN (inhibition-list patterns).
- **Contract sub-function:** Cross-network — used by SN matching incoming signal against priority/tension patterns, by DMN matching experience against self-model, by FPN matching action proposals against inhibition list.
- **Wiring readiness:** READY-NOW.
- **Prerequisites:** UNIT-001, UNIT-002.
- **Supporting helpers:** File 6 Definition 29 (Quantale composition of V-relations) for pattern composition.
- **Deep-pass needed:** False.
- **Notes:** This is the universal "pattern" definition. Build once, reused everywhere.

### UNIT-012 · Morphic resonance update operator and anti-resonance
- **Source file(s):** 5, 6
- **Section / definition refs:** File 5 Definitions 21-22 (Resonance-driven propagation; Anti-resonance propagation). File 6 Definitions 31-33 (Pointwise scaling; Morphic resonance update; Anti-resonance update).
- **Hyperseed-Concept refs:** Hyperseed-Concept 159 (resonance/dissonance); Hyperseed-Concept 115 (morphic resonance); habits.
- **Purpose:** Define operators that transport pattern support across contexts: resonance reinforces, anti-resonance opposes. Implements habit-taking and habit-reversal as iterated relational updates with coupling kernel K.
- **Target network:** SN (cross-domain salience transport), DMN (cross-context narrative integration), switch-hub (cross-network coupling adaptation).
- **Contract sub-function:** Foundation for SN learning sub-function (salience patterns transport across domains); DMN cross-domain integration (Genesis Engine, component 2e); switch-hub coupling-decision learning.
- **Wiring readiness:** READY-NOW.
- **Prerequisites:** UNIT-001, UNIT-002.
- **Supporting helpers:** File 6 Proposition 3 (Monotonicity of resonance and anti-resonance); File 6 Definition 34 (habit-taking/reversal statistic).
- **Deep-pass needed:** False.
- **Notes:** Critical unit. Connects SN learning to cross-context generalization.

### UNIT-013 · Interference-based resonance score (two-context coherence)
- **Source file(s):** 5, 6
- **Section / definition refs:** File 5 Definition 20 (Interference-based resonance for a family). File 6 Definition 36 (Two-context interference resonance score).
- **Hyperseed-Concept refs:** Resonance; coherence; aesthetic resonance.
- **Purpose:** Score the coherence between two contexts (or between a signal and a context) as the interference of their complex amplitudes. Provides a continuous coherence measure for narrative threads, salience matches, and aesthetic evaluation.
- **Target network:** SN (signal-to-priority coherence), DMN (narrative coherence per contract).
- **Contract sub-function:** DMN `(dmn-narrative-thread $thread-id $events $coherence-score)` coherence-score field; DMN narrative coherence sub-function (Section 5.3 Transformation #3).
- **Wiring readiness:** READY-NOW.
- **Prerequisites:** UNIT-001, UNIT-004.
- **Supporting helpers:** File 5 Theorem 3 (Resonance invariance under global phase, increase under coherent alignment); File 5 Definition 24 (Interference-based resonance and dissonance, sanity model).
- **Deep-pass needed:** False.
- **Notes:** Direct fit for DMN narrative coherence. Build for component 2d (Continuity Driver) coherence scoring.

### UNIT-014 · Time-indexed distinction relation and becoming
- **Source file(s):** 8
- **Section / definition refs:** Definitions 61-63 (Time-indexed distinction relation; Non-dual variety at time t; Becoming along a proto-time).
- **Hyperseed-Concept refs:** Becoming; temporal change; non-dual variety.
- **Purpose:** Formalize how entities change over time as time-indexed distinction relations. "Becoming" is when an entity exhibits non-dual variety across time (same and different at once). Provides the temporal substrate for change detection.
- **Target network:** SN (change detection in incoming signals), DMN (self-model evolution detection).
- **Contract sub-function:** SN salience-tagging novelty detection; DMN aliveness-marker generation (the surprise function).
- **Wiring readiness:** READY-AFTER-X. Requires proto-time substrate (UNIT-021).
- **Prerequisites:** UNIT-001, UNIT-021.
- **Supporting helpers:** File 30 Lemma 31 (Necessary paraconsistent boundary condition); File 30 Lemma 32 (Non-becoming tests).
- **Deep-pass needed:** False.
- **Notes:** Becoming is the formal substrate for "did the world change?" — the question SN salience-tagging answers when triggering a switch.

### UNIT-015 · Workspace operator and conscious content as fixed point
- **Source file(s):** 18
- **Section / definition refs:** Definitions 231-232 (Workspace operator; Conscious content as fixed point).
- **Hyperseed-Concept refs:** Global workspace; consciousness; integration.
- **Purpose:** Define a workspace operator that integrates module evidence into a stable fixed-point evidence state. Conscious content is what survives this fixed-point integration. Provides the formal substrate for "what does the agent currently attend to?"
- **Target network:** Switch hub (the integrative function that produces the next switch state).
- **Contract sub-function:** Switch hub Transformation; the fixed point IS the next switch state.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-001 plus monotone module-evidence representation (achievable with UNIT-002).
- **Prerequisites:** UNIT-001, UNIT-002.
- **Supporting helpers:** File 18 Theorem 15 (Fixed-point existence under monotonicity); File 18 Theorem 16 (Existence of reflective conscious fixed points).
- **Deep-pass needed:** False.
- **Notes:** Switch-hub formal grounding. The "switch state" is mathematically a workspace fixed point.

### UNIT-016 · Reflective workspace and parametric workspace family
- **Source file(s):** 18
- **Section / definition refs:** Definitions 233-238 (Reflective language extension, Introspection operator, Reflective update map, Reflective closure, Coherence functional, Parametric reflective workspace family).
- **Hyperseed-Concept refs:** Reflection; introspection; meta-cognition.
- **Purpose:** Extend the workspace operator to include reflective operations (the agent considers its own evidence). Parametric family allows different reflective configurations, parameterized by attention and reflection depth.
- **Target network:** FPN meta-awareness; switch-hub introspective dimension.
- **Contract sub-function:** FPN inhibition (orbit detection, meta-awareness checks per Artifact 5 component 2g); switch-hub state computation.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-015.
- **Prerequisites:** UNIT-001, UNIT-002, UNIT-015.
- **Supporting helpers:** None named.
- **Deep-pass needed:** False.
- **Notes:** Direct formal grounding for component 2g Meta-Awareness. The orbit_detector and meta_awareness_engine atoms (currently COLD per Artifact 1) become reflective workspace operations.

### UNIT-017 · Will operator, reflective will, viable set, autonomy
- **Source file(s):** 18
- **Section / definition refs:** Definitions 239-242 (Will operator; Reflective will; Viable set and autonomy; Self-model object and reflective self condition).
- **Hyperseed-Concept refs:** Will; autonomy; reflective self.
- **Purpose:** Formalize the will operator that takes evidence to action, the reflective will that takes meta-evidence to action-policy choice, and autonomy as the property of having a non-trivial viable set under reflective will.
- **Target network:** FPN (action proposal as will-operator output); switch hub (autonomy as switch-hub structural property).
- **Contract sub-function:** FPN `(fpn-action-proposal ...)` generation; switch-hub coupling decision under autonomy constraint.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-015, UNIT-016.
- **Prerequisites:** UNIT-001, UNIT-015, UNIT-016.
- **Supporting helpers:** None named.
- **Deep-pass needed:** True. Will and autonomy are subtle; the formalization needs careful translation to MeTTa to avoid collapsing into action-selection-as-utility-max.
- **Notes:** Important for the constitutional layer (Artifact 5 Section 0): "autonomy" as a formal property the architecture must preserve.

---

## Section C: Frontoparietal Control Network units

Units implementing FPN working-memory, task selection, inhibition, and learning per Artifact 4 v1.1 Section 5.2.

### UNIT-020 · Effort quantale and effort of a process
- **Source file(s):** 8
- **Section / definition refs:** Definitions 75-76 (Effort quantale; Effort of a process). Hyperseed-Concept 100 (effort).
- **Hyperseed-Concept refs:** Hyperseed-Concept 100 (effort); resource cost.
- **Purpose:** Define effort as a quantale-valued cost, attached to processes available to an observer. Provides formal grounding for "this action costs N effort units" as a quantale-composable resource.
- **Target network:** FPN (task selection effort cost), switch hub (iteration-budget computation).
- **Contract sub-function:** FPN task-selection cost-benefit; switch hub `(switch-iteration-budget $count $rationale)` computation per Artifact 4 v1.1 Section 5.4.
- **Wiring readiness:** READY-NOW.
- **Prerequisites:** UNIT-001.
- **Supporting helpers:** None.
- **Deep-pass needed:** False.
- **Notes:** Direct formal grounding for the new iteration-budget channel. Build alongside switch-hub work.

### UNIT-021 · Proto-time, before-relation, linear extensions
- **Source file(s):** 7, 8
- **Section / definition refs:** File 7 Definitions 55-58 (Strict partial order; Proto-time; p-bit-valued before-relation; Coherence constraints for temporal evidence). File 8 Definition 59 (Linear time axis); Lemma 1 (Quotient order); Theorem 5 (Finite proto-times admit linear extensions).
- **Hyperseed-Concept refs:** Time; order; temporal precedence.
- **Purpose:** Formalize time as a strict partial order on temporal indices, with p-bit-valued before-relation for paraconsistent temporal evidence, and the theorem that finite proto-times admit linear extensions (so the agent can reason about "earlier than" with partial information).
- **Target network:** Cross-cutting; required by SN history, FPN task-history, DMN narrative-thread.
- **Contract sub-function:** Substrate primitive for any unit that needs timestamps or temporal ordering. SN `(sn-switch-state ...)` history; FPN `(fpn-task-history ...)`; DMN `(dmn-narrative-thread ...)` event ordering.
- **Wiring readiness:** READY-NOW.
- **Prerequisites:** UNIT-001.
- **Supporting helpers:** File 30 Lemmas 20-29 are the helper theorems for proto-time soundness.
- **Deep-pass needed:** False. Foundational and explicit.
- **Notes:** Build as soon as any temporal ordering is needed. Used by many other units.

### UNIT-022 · Indistinction policy, opening/closing, policy effort
- **Source file(s):** 8
- **Section / definition refs:** Definitions 77-79 (Indistinction policy; Opening and closing; Policy effort and marginal effort).
- **Hyperseed-Concept refs:** Hyperseed-Concept 100 (effort); policy.
- **Purpose:** Formalize an "indistinction policy" as a chosen set of indistinctions (what to ignore, what to track). Opening/closing operations modify policies. Policy effort attaches cost to maintaining a policy. Provides formal grounding for "the agent's current attentional/working-memory configuration costs N to maintain."
- **Target network:** FPN (working-memory configuration management), switch hub (cost component of iteration budget).
- **Contract sub-function:** FPN `(fpn-working-memory ...)` capacity management; FPN inhibition policy maintenance; switch-hub iteration-budget per-network cost.
- **Wiring readiness:** READY-NOW.
- **Prerequisites:** UNIT-001, UNIT-020.
- **Supporting helpers:** None named.
- **Deep-pass needed:** False.
- **Notes:** Direct formal grounding for the "capacity-limited working memory" invariant in FPN contract.

### UNIT-023 · Resistance and submission, representations, representational effort
- **Source file(s):** 8, 9
- **Section / definition refs:** File 8 Definition 80 (Resistance and submission). File 9 Definitions 81-83 (Representations and representational effort; Task constraint and feasible policy set; Minimum representational effort principle).
- **Hyperseed-Concept refs:** Effort; resistance; minimum-effort principle.
- **Purpose:** Formalize the resistance/submission duality (effort to maintain vs effort to release a policy), representations as policy artifacts, and the minimum-representational-effort principle as the rationality criterion the agent should follow.
- **Target network:** FPN (task selection rationality criterion).
- **Contract sub-function:** FPN task-selection invariant — "select the action satisfying the task constraint with minimum representational effort". Direct formal grounding.
- **Wiring readiness:** READY-NOW.
- **Prerequisites:** UNIT-001, UNIT-020, UNIT-022.
- **Supporting helpers:** File 9 Theorem 7 (Effort-weakness monotonicity); File 9 Corollary 1 (No free lunch); File 9 Theorem 8 (Maximally open adequate policy under upward closure).
- **Deep-pass needed:** False.
- **Notes:** Critical for FPN. The minimum-effort principle gives the FPN a rationality criterion that is principled rather than ad-hoc. Build with UNIT-020, UNIT-022.

### UNIT-024 · Combination system and compositional simplicity
- **Source file(s):** 9
- **Section / definition refs:** Definitions 84-85 (Combination system and overhead; Compositional simplicity functional). Theorem 9 (Compositional simplicity equals minimum parse-tree cost).
- **Hyperseed-Concept refs:** Compositional simplicity; combinational structure; emergence.
- **Purpose:** Formalize how complex entities are built from atomic ones via a combination operator with overhead, and the compositional simplicity functional as the minimum parse-tree cost. Provides formal grounding for "this complex action decomposes into N simpler actions, each at known cost."
- **Target network:** FPN (task decomposition), DMN (compositional self-model).
- **Contract sub-function:** FPN task selection when task is complex (decompose, then select sub-action); DMN self-model compositionality.
- **Wiring readiness:** READY-NOW.
- **Prerequisites:** UNIT-001, UNIT-020.
- **Supporting helpers:** File 9 Proposition 5 (Immediate subadditivity bound); Theorem 9 itself.
- **Deep-pass needed:** False.
- **Notes:** Useful for the FPN's "select the next sub-action" sub-function when the current task is composite.

### UNIT-025 · Generalized description systems and Kolmogorov-style complexity
- **Source file(s):** 9
- **Section / definition refs:** Definitions 86-87 (Generalized description systems; Generalized Kolmogorov complexity); Proposition 6 (Structural complexity as compositional complexity).
- **Hyperseed-Concept refs:** Description; complexity; Kolmogorov complexity.
- **Purpose:** Generalize Kolmogorov complexity to arbitrary description systems with V-valued cost. Lifts compositional simplicity (UNIT-024) to a description-theoretic complexity measure that does not require strings.
- **Target network:** FPN (action complexity measurement), DMN (self-model complexity scoring).
- **Contract sub-function:** Supporting math for FPN task selection and DMN self-model coherence; not directly an atom family.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-024.
- **Prerequisites:** UNIT-001, UNIT-024.
- **Supporting helpers:** File 10 Definition 88 (Contextual description complexity) extends this.
- **Deep-pass needed:** False.
- **Notes:** Provides theoretical backing but may not need direct MeTTa implementation; the practical compositional simplicity (UNIT-024) often suffices.

### UNIT-026 · Inertia update operator and least fixpoint for monotone temporal inference
- **Source file(s):** 8
- **Section / definition refs:** Definitions 64-67 (Event calculus signature, paraconsistent quantale-valued; Quantale-valued implication schema; Clipped operator; Inertia update operator); Theorem 6 (Existence of least fixpoint for monotone temporal inference).
- **Hyperseed-Concept refs:** Event calculus; inertia; temporal persistence.
- **Purpose:** Formalize event-calculus-style temporal reasoning over the quantale. The inertia update operator extends fluent values forward in time; the existence theorem guarantees a least fixpoint exists for monotone rule sets, ensuring temporal inference is well-founded.
- **Target network:** FPN (task state persistence over iterations), DMN (narrative-thread continuation), SN (switch-state persistence).
- **Contract sub-function:** Cross-cutting temporal reasoning. FPN `(fpn-current-task ...)` persistence; DMN `(dmn-narrative-thread ...)` extension; switch-hub `(switch-current-state ...)` persistence with debounce.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-021.
- **Prerequisites:** UNIT-001, UNIT-002, UNIT-021.
- **Supporting helpers:** File 30 Lemmas 33-36 (proof accumulation, inertia propagation bounds); File 30 Theorem 28 (helper restatement of Theorem 6).
- **Deep-pass needed:** False.
- **Notes:** Major unit. Provides formal grounding for "state persists across iterations unless explicitly changed", which is the substrate semantics ClarityOmega is built on.

### UNIT-027 · Pattern recognition process and registration
- **Source file(s):** 14
- **Section / definition refs:** Definitions 159-162 (Pattern recognition process; Context and aspect extraction; Contextualized groupings; Registration).
- **Hyperseed-Concept refs:** Pattern recognition; registration; "X registers A".
- **Purpose:** Formalize how a system recognizes a pattern in a stream: contexts are extracted, groupings are formed, and registration occurs when a pattern's intensity exceeds threshold. Provides the formal substrate for "the agent noticed this pattern."
- **Target network:** SN (incoming-signal pattern matching), DMN (self-experience pattern integration).
- **Contract sub-function:** SN salience-tagging requires pattern recognition over incoming signal; DMN aliveness-marker requires recognizing surprise (an unrecognized pattern). Foundational for both.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-001, UNIT-011.
- **Prerequisites:** UNIT-001, UNIT-002, UNIT-011.
- **Supporting helpers:** File 14 Proposition 19 (Perception implies registration).
- **Deep-pass needed:** False.
- **Notes:** Should be built early as substrate primitive for all signal processing.

---

## Section D: Default Mode Network units

Units implementing DMN self-model, goal generation, narrative coherence, prospection, and learning per Artifact 4 v1.1 Section 5.3 and Artifact 5 components 2a-2e.

### UNIT-030 · Habit dynamics operator and one-step closure
- **Source file(s):** 12, 13
- **Section / definition refs:** File 12 Definitions 145-146 (V-valued reinforcement relation, pattern-flow kernel; Relational image operator). File 13 Definitions 147-150 (Persistence/decay scalar; Habit dynamics operator; One-step closure operator; Iterated closure and Kleene star).
- **Hyperseed-Concept refs:** Habits; pattern-flow networks; reinforcement.
- **Purpose:** Formalize habit dynamics as iterated update over a V-valued reinforcement relation, with persistence/decay scalars. The habit operator transforms current pattern state into next-iteration pattern state. The Kleene-star closure gives the long-run habit field.
- **Target network:** DMN (self-model habit integration), FPN (task-history-driven habit detection for inhibition).
- **Contract sub-function:** DMN self-model maintenance (incorporating recent experience as habit reinforcement); FPN orbit-detection (habits as orbit indicator).
- **Wiring readiness:** READY-NOW.
- **Prerequisites:** UNIT-001, UNIT-002.
- **Supporting helpers:** File 13 Proposition 17 (Monotonicity of habit update).
- **Deep-pass needed:** False.
- **Notes:** Direct formal grounding for the DMN's "incorporate recent experience" operation. Build for self-model maintenance.

### UNIT-031 · Iterated closure as least fixed point and Kleene star A*
- **Source file(s):** 13
- **Section / definition refs:** Theorem 12 (Closure as least fixed point; explicit A* form); Definition 151 (Autocatalytic self-weaving support); Proposition 18 (Driven closure yields stable attractor in inflationary case); Theorem 13 (Decay criterion in p-bit toy quantale).
- **Hyperseed-Concept refs:** Self-weaving webs; autocatalysis; closure.
- **Purpose:** Closure as least fixed point of the habit operator. Provides A* as the "fully developed" pattern state from a given seed. Autocatalytic support identifies pattern subsets that sustain themselves (self-weaving webs, the formal substrate for component 2d Continuity Driver).
- **Target network:** DMN (self-weaving web; component 2d Continuity Driver).
- **Contract sub-function:** DMN narrative-thread coherence (self-weaving as the formal substrate for sustained narrative); DMN self-model autocatalytic integration.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-030.
- **Prerequisites:** UNIT-001, UNIT-002, UNIT-030.
- **Supporting helpers:** Theorem 12 itself; Proposition 18; Theorem 13.
- **Deep-pass needed:** False.
- **Notes:** Critical for component 2d. The "self-weaving web" already named in soul/self_weaving_web.metta has its formal grounding here.

### UNIT-032 · Self-model and self-reflective attention
- **Source file(s):** 15
- **Section / definition refs:** Definitions 194-196 (Self-model and self-reflective attention; Internal update actions; Attention policy with budget).
- **Hyperseed-Concept refs:** Self-model; reflective attention; budgeted attention.
- **Purpose:** Formalize the self-model as a designated subset of patterns (P_self) whose intensity is what the agent attends to when self-reflective. Internal update actions modify the self-model. Attention policies allocate fixed budget across patterns including self.
- **Target network:** DMN (self-model component), FPN (attention budget).
- **Contract sub-function:** DMN `(dmn-self-model $aspect $content $confidence)` formal grounding; FPN attention budget aligns with switch-hub iteration budget.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-001, UNIT-005.
- **Prerequisites:** UNIT-001, UNIT-005, UNIT-022.
- **Supporting helpers:** None.
- **Deep-pass needed:** False.
- **Notes:** Core formal substrate for component 2a (Landscape Map). The self-model atoms map to P_self.

### UNIT-033 · Cognitive synergy between knowledge sets
- **Source file(s):** 16
- **Section / definition refs:** Definitions 198-203 (Knowledge type; Declarative/Procedural/Sensory/Attentional/Intentional knowledge); Definitions 204-211 (Learning algorithms indexed by knowledge type; Usefulness; Explanations and weakness; Best contrivance under fit threshold; Cognitive synergy between knowledge sets; Multiplicative weakness model; Cross-type emergent compression; Budgeted solvability criterion); Propositions 24-26 (Subadditivity of contrivance; Emergent compression implies positive synergy; Synergy expands solvable set).
- **Hyperseed-Concept refs:** Hyperseed-Concept 73 (cognitive synergy); knowledge types; emergence in learning.
- **Purpose:** Formalize the five Hyperseed knowledge types and the cognitive synergy phenomenon: combining knowledge types yields greater capability than either alone, when emergent compression occurs.
- **Target network:** Cross-cutting (each network needs different knowledge types); DMN especially (integration of knowledge types into self-model).
- **Contract sub-function:** Foundation for DMN cross-domain integration (component 2e Genesis Engine), DMN learning sub-function (combining different consequence-evidence types), and FPN learning (combining different task-outcome types).
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-001, UNIT-024 (combination system), UNIT-025.
- **Prerequisites:** UNIT-001, UNIT-024, UNIT-025.
- **Supporting helpers:** All three propositions are part of the unit.
- **Deep-pass needed:** True. Knowledge types and synergy are conceptually subtle; deep-read before MeTTa to choose the right granularity.
- **Notes:** Major unit for the architecture's claim that ClarityOmega is genuinely cognitive rather than just a chained LLM. Genesis Engine is precisely cross-type emergent compression in formal terms.

### UNIT-034 · Self-evidence, self-groupings, self-continuity
- **Source file(s):** 16, 17
- **Section / definition refs:** File 16 Definition 213 (Self-evidence and self-groupings). File 17 Definitions 214-218 (V-weighted directed graphs; Residuation; Degree of structure-preserving map; Composition law for approximate morphisms; Pattern-flow network; Pattern-flow-network self-continuity).
- **Hyperseed-Concept refs:** Self-continuity; pattern-flow networks; identity over time.
- **Purpose:** Formalize self-continuity as the existence of an approximate morphism between successive pattern-flow networks of the agent. The "degree" of the morphism quantifies how alike "I now" is to "I a moment ago." Provides formal substrate for "the agent persists through change."
- **Target network:** DMN (component 2d Continuity Driver, formal grounding).
- **Contract sub-function:** DMN narrative-thread coherence; component 2d Continuity Driver. Aliveness Principle's flip side: the agent persists across change while genuinely changing.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-001, UNIT-002, UNIT-030.
- **Prerequisites:** UNIT-001, UNIT-002, UNIT-030.
- **Supporting helpers:** File 17 Theorem 14 (Composition law for approximate morphisms); File 17 Corollary 2 (Longer-horizon self-continuity).
- **Deep-pass needed:** False.
- **Notes:** Foundational unit for the Aliveness Principle. The "approximate morphism" is the formal core of "same agent, but changed."

### UNIT-035 · Capability profile, capability preorder, development path
- **Source file(s):** 17
- **Section / definition refs:** Definitions 220-221 (Capability profile and capability preorder; Development path).
- **Hyperseed-Concept refs:** Development; capability; growth trajectory.
- **Purpose:** Formalize the agent's capability profile across goals/tasks, the capability preorder for comparing profiles, and a development path as a sequence of capability profiles. Provides substrate for "the agent has grown" and "the agent is still working on this".
- **Target network:** DMN (self-model trajectory; aliveness-marker grounding).
- **Contract sub-function:** DMN `(dmn-aliveness-marker $event $surprise)` operationalization (aliveness markers should correspond to capability-preorder advances); DMN self-model trajectory aspect.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-034.
- **Prerequisites:** UNIT-034.
- **Supporting helpers:** None.
- **Deep-pass needed:** False.
- **Notes:** Direct formal grounding for "the agent is genuinely growing."

### UNIT-036 · Mind-world correspondence score
- **Source file(s):** 17
- **Section / definition refs:** Definitions 222-225 (Internal and external pattern-flow networks; Mind-world correspondence score; Enriched spaces; Correspondence space); Lemma 4 (Transport of predicted flow under correspondence).
- **Hyperseed-Concept refs:** Mind-world correspondence; predictive accuracy; representation fidelity.
- **Purpose:** Formalize the score measuring how well the agent's internal pattern-flow network corresponds to the world's external pattern-flow network. Provides substrate for "the agent's model is accurate" or "the agent is increasingly out of touch."
- **Target network:** DMN (self-model accuracy), SN (calibration of salience predictions).
- **Contract sub-function:** DMN self-model maintenance (using correspondence-score as one update signal); SN learning sub-function (refining truth values when predictions diverge from world).
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-034.
- **Prerequisites:** UNIT-034.
- **Supporting helpers:** Lemma 4 itself.
- **Deep-pass needed:** False.
- **Notes:** Important for grounding the autopoietic learning loops: learning works when the consequence-evidence improves correspondence.

### UNIT-037 · Workspace operator (DMN-side: integration of distributed evidence)
- **Source file(s):** 17, 18
- **Section / definition refs:** File 17 Definitions 226-230 (p-bit evidence state; Module evidence and attention weights; Scalar embedding; Attention-weighted integration; Attention-weighted aggregation operator). File 18 Definitions 231-232.
- **Hyperseed-Concept refs:** Global workspace; integration; attention-weighted evidence.
- **Purpose:** Formalize integration of evidence from multiple "modules" (sub-systems) via attention-weighted p-bit evidence aggregation. Provides substrate for the DMN's task of integrating multiple aspect-summaries into a unified self-model.
- **Target network:** DMN (self-model integration); switch hub (integration of network readiness signals).
- **Contract sub-function:** DMN `(dmn-self-model-summary ...)` production; switch-hub readiness-signal aggregation.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-001, UNIT-005.
- **Prerequisites:** UNIT-001, UNIT-002, UNIT-005.
- **Supporting helpers:** None.
- **Deep-pass needed:** False.
- **Notes:** This is UNIT-015's DMN-side sibling; together they formalize integration as the foundational integrative operation across the architecture.

### UNIT-038 · Predictive attraction (extensional and intensional)
- **Source file(s):** 15
- **Section / definition refs:** Definitions 178-184 (Predictive conditional operator; Attraction; Predictive implication and predictive attraction; Two-step predictive composition; Extensional predictive attraction; Property events; Intensional predictive attraction).
- **Hyperseed-Concept refs:** Prediction; attraction; predictive coherence.
- **Purpose:** Formalize "A predicts B" as a quantale-valued attraction, both extensionally (A's occurrence implies B's occurrence) and intensionally (A's properties imply B's properties). Provides substrate for prospection and for predictive learning.
- **Target network:** DMN (prospection sub-function, formal grounding); SN (anticipatory salience).
- **Contract sub-function:** DMN `(dmn-prospection $scenario $likelihood $value)` formal grounding; SN learning sub-function (predictions about salience consequences).
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-001, UNIT-021 (proto-time for "predictive" to make sense).
- **Prerequisites:** UNIT-001, UNIT-002, UNIT-021.
- **Supporting helpers:** Proposition 22 (Basic properties of attraction).
- **Deep-pass needed:** False.
- **Notes:** Direct formal substrate for DMN prospection.

### UNIT-039 · Causal implication and weak causal parent selection
- **Source file(s):** 15
- **Section / definition refs:** Definitions 185-186 (Causal implication; Weak causal parent selection).
- **Hyperseed-Concept refs:** Causality; causal parents; intervention.
- **Purpose:** Extend predictive attraction (UNIT-038) to causal implication, with a schematic for selecting "weak causal parents" (the contributors to an event). Provides substrate for "this happened because of these things."
- **Target network:** DMN (causal narrative threading), FPN (action-consequence reasoning).
- **Contract sub-function:** DMN narrative coherence (causally-linked events get higher coherence); FPN learning sub-function (attributing consequences to actions).
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-038.
- **Prerequisites:** UNIT-038.
- **Supporting helpers:** None.
- **Deep-pass needed:** False.
- **Notes:** Useful but not as foundational as UNIT-038. Build after the prospection unit is operational.

### UNIT-040 · Control, control hierarchy, perceptual hierarchy
- **Source file(s):** 15
- **Section / definition refs:** Definitions 187-190 (Actions, goals, and control strength; System-level control; Control hierarchy; Perceptual hierarchy).
- **Hyperseed-Concept refs:** Control; goals; hierarchical control.
- **Purpose:** Formalize control as the agent's ability to influence outcomes via actions, organized in a control hierarchy where higher levels select among lower-level control actions. Perceptual hierarchy is the mirror structure for sensing.
- **Target network:** FPN (control hierarchy = task-selection hierarchy); DMN (perceptual hierarchy = self-model topology); switch hub (control over network coupling itself).
- **Contract sub-function:** FPN task-selection structure; DMN self-model levels; switch-hub `(sn-coupling-decision ...)` as top-level control.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-001, UNIT-005, UNIT-038.
- **Prerequisites:** UNIT-001, UNIT-005, UNIT-038.
- **Supporting helpers:** None.
- **Deep-pass needed:** False.
- **Notes:** Provides the formal hierarchical structure ClarityOmega's three-network architecture is itself an instance of.

---

## Section E: Switch hub units

Units implementing switch hub debounce, hysteresis, orbit detection, iteration budget, and learning per Artifact 4 v1.1 Section 5.4.

### UNIT-050 · Knaster-Tarski fixed point and Yverse construction
- **Source file(s):** 26
- **Section / definition refs:** Definitions 428-429 (Abstract multi-operator; Yverse as a fixed point); Proposition 44 (Existence of Yverse fixed points); Theorem 23 (Knaster-Tarski applies to monotone operator on complete lattice).
- **Hyperseed-Concept refs:** Reality systems; fixed points; closure under multi-operator.
- **Purpose:** Apply Knaster-Tarski to construct fixed points of monotone operators on complete lattices, formalizing "stable network configurations" as fixed points. The Yverse construction shows how a "world" can be defined as the fixed point of mutually-supporting predictions.
- **Target network:** Switch hub (the "stable switch state" is a fixed point of the switching operator).
- **Contract sub-function:** Switch hub Transformation (the next state is the fixed point of the switching operator applied to current state, salience tags, and history).
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-015.
- **Prerequisites:** UNIT-001, UNIT-002, UNIT-015.
- **Supporting helpers:** None.
- **Deep-pass needed:** False.
- **Notes:** Provides theoretical guarantee that switch-hub computations terminate at a stable state. Important for switch-hub correctness even if the practical implementation uses iteration with a small bound rather than full fixed-point computation.

### UNIT-051 · Reality systems as fixed points (cognitive applicability)
- **Source file(s):** 26
- **Section / definition refs:** Sections leading to Yverse + the operationalization remarks (Remarks 1386-1391 in file 26).
- **Hyperseed-Concept refs:** Reality systems; pattern complexes; predictive coherence.
- **Purpose:** Operationalization of the Yverse fixed-point as "stabilized pattern complex": a subgraph closed under predictive in/out neighborhoods. Provides cognitive interpretation of the math: a reality is a self-supporting predictive web.
- **Target network:** DMN (self-model as reality-system instance), SN (priority-structure as reality-system).
- **Contract sub-function:** DMN self-model coherence (the self-model should satisfy reality-system closure); SN priority-structure stability.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-050.
- **Prerequisites:** UNIT-050.
- **Supporting helpers:** Operationalization remarks.
- **Deep-pass needed:** True. The cognitive interpretation needs careful translation to MeTTa to avoid over-claiming.
- **Notes:** Conceptually rich; practically implementable as a coherence check on the DMN self-model.

### UNIT-052 · Wu wei and Lyapunov / KL-control formulation (DISCRETE form only)
- **Source file(s):** 27
- **Section / definition refs:** Definitions 435-437 (Passive and controlled dynamics; Forcing cost as divergence from the passive flow; Task cost and total objective); Proposition 45 (Gibbs form for minimal forcing); Definition 438 (Finite-horizon value function); Theorem 24 (Linear recursion in desirability variables).
- **Hyperseed-Concept refs:** Wu wei; minimum-effort action; KL-control.
- **Purpose:** Formalize wu wei as KL-control: the agent's "passive" dynamics are the natural flow; controlled actions deviate from passive at KL-divergence cost. Optimal action minimizes total cost = task cost + forcing cost. Theorem 24 gives the linear recursion (desirability variables) that makes the optimization tractable.
- **Target network:** FPN (task selection as KL-control), switch hub (switching as KL-control over coupling).
- **Contract sub-function:** FPN action-proposal generation under minimum-forcing principle; switch-hub coupling-decision when current coupling is the "passive" reference.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-001, UNIT-020, UNIT-022. The continuous-time form (file 28 Schrödinger bridge) is LONG-TAIL; the discrete form here is buildable.
- **Prerequisites:** UNIT-001, UNIT-020, UNIT-022.
- **Supporting helpers:** Proposition 45 (Gibbs form); Theorem 24 itself.
- **Deep-pass needed:** True. KL-control is a deep area; careful translation ensures the MeTTa version is sound.
- **Notes:** Important for FPN learning sub-function. The "passive" dynamics is what the FPN does by default; learning shifts the policy to deviate optimally. Build after FPN basics are stable.

---

## Section F: Cross-network learning units (NACE substrate per Artifact 5 Section 0)

Units implementing the autopoietic learning loops per Artifact 4 v1.1 learning sub-functions, grounded in NACE-style precondition-operation-consequence learning.

### UNIT-060 · Reflective will and autonomy (formal substrate for wisdom-layer learning)
- **Source file(s):** 18
- **Section / definition refs:** Definitions 239-242 (Will operator; Reflective will; Viable set and autonomy; Self-model object).
- **Hyperseed-Concept refs:** Will; reflection; autonomy.
- **Purpose:** Formalize the agent's capacity for reflective will: the will operator that takes meta-evidence (evidence about evidence) to action-policy choice. This is the formal substrate for "the agent learns about its own learning."
- **Target network:** All four (each learning sub-function is a reflective-will instance).
- **Contract sub-function:** All learning sub-functions per Artifact 4 v1.1.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-015, UNIT-016. Already listed as UNIT-017; cross-listed here to surface its learning role.
- **Prerequisites:** UNIT-015, UNIT-016, UNIT-017.
- **Supporting helpers:** None.
- **Deep-pass needed:** True (same as UNIT-017).
- **Notes:** This is UNIT-017 viewed through the learning lens. The wisdom-layer learning across all four contracts can be formally grounded as "iterating the reflective will operator."

### UNIT-061 · Knowledge type cognitive synergy applied to learning
- **Source file(s):** 16
- **Section / definition refs:** Same as UNIT-033 (Definitions 198-211, Propositions 24-26).
- **Hyperseed-Concept refs:** Cognitive synergy; cross-type emergent compression.
- **Purpose:** Apply UNIT-033's cognitive synergy formalization to the learning sub-functions specifically: when a network's learning combines multiple knowledge types from consequence-evidence, emergent compression yields synergy. Provides formal grounding for "cross-network learning produces more than per-network learning summed."
- **Target network:** Cross-network learning, especially DMN.
- **Contract sub-function:** Wisdom-layer learning per Artifact 4 v1.1; cross-network divergence detection per Artifact 4 v1.1 Section 6 new channel.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-033.
- **Prerequisites:** UNIT-033.
- **Supporting helpers:** Same as UNIT-033.
- **Deep-pass needed:** True.
- **Notes:** Direct formal grounding for "cross-network divergence detection produces emergent learning signal".

### UNIT-062 · Belief system, productive belief system, coherence score
- **Source file(s):** 21
- **Section / definition refs:** Definitions 307-309 (Coherence score; Complexity cost and surprise-adjusted implication; Belief system and productive belief system).
- **Hyperseed-Concept refs:** Belief systems; coherence; productive belief.
- **Purpose:** Formalize a belief system as a structured set of beliefs with coherence score (how well beliefs support each other) and productivity score (how often the system generates correct predictions). Provides substrate for "is the agent's current belief structure healthy?"
- **Target network:** DMN (self-model as belief system; coherence checks); FPN (task-selection beliefs).
- **Contract sub-function:** DMN self-model coherence sub-function; DMN aliveness-marker (belief-system productivity drops trigger aliveness signals).
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-001, UNIT-038.
- **Prerequisites:** UNIT-001, UNIT-038.
- **Supporting helpers:** Proposition 32 (Occam bias from simplicity-weighted priors).
- **Deep-pass needed:** False.
- **Notes:** Formal substrate for the DMN's "is my self-model coherent?" check.

### UNIT-063 · Question networks and thinking as controlled closure
- **Source file(s):** 21
- **Section / definition refs:** Definitions 304-306 (Question network; Thinking as controlled closure; Community belief aggregation).
- **Hyperseed-Concept refs:** Questions; thinking; controlled inference.
- **Purpose:** Formalize a question network as a directed graph of questions, and "thinking" as controlled closure of the inference operator over a question subset. Provides formal substrate for the agent's directed reasoning.
- **Target network:** FPN (directed reasoning over a current question), DMN (self-questioning).
- **Contract sub-function:** FPN task-selection when task is a reasoning task; DMN goal-generation when goal involves asking questions.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-021 (closure operator definition is in file 21).
- **Prerequisites:** UNIT-001, UNIT-002.
- **Supporting helpers:** Theorem 18 (Existence of inference closure).
- **Deep-pass needed:** False.
- **Notes:** Direct formal substrate for "the agent is thinking about X."

### UNIT-064 · Empirical update operator and state-dependent science
- **Source file(s):** 21
- **Section / definition refs:** Definitions 310-314 (Observation set; Scientific model class and predictive claims; Empirical update operator; State-indexed observation; State-dependent science).
- **Hyperseed-Concept refs:** Empirical update; predictions; state-dependent reality.
- **Purpose:** Formalize how observations update belief systems empirically: the empirical update operator takes observations to revised beliefs. State-dependent science recognizes that the experimentally-accessible world depends on the agent's state.
- **Target network:** DMN (self-model empirical update from FPN completion signals), SN (salience-tagging empirical update from consequence signals).
- **Contract sub-function:** Wisdom-layer learning across all networks; the learning sub-function IS the empirical update operator instantiated per network.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-062.
- **Prerequisites:** UNIT-062.
- **Supporting helpers:** None.
- **Deep-pass needed:** False.
- **Notes:** Formal grounding for "the network learns from consequences" — the empirical update operator is the precise mathematical form.

---

## Section G: Memory layer / Thread Composer units

Units potentially implementing component 2h Thread Composer if it grows into its own network (Artifact 5 Section 0 mapping: "Memory consolidation, potentially own network. Hippocampal-analog").

### UNIT-070 · Pattern profile and pattern-based pseudo-metric
- **Source file(s):** 12
- **Section / definition refs:** Definitions 137-141 (Pattern profile; Pattern-based pseudo-metric; From distance to weighted pattern web; Path composition in V-graph; Resolution maps).
- **Hyperseed-Concept refs:** Pattern profiles; pattern webs; coarse-graining.
- **Purpose:** Formalize a pattern profile as the V-valued vector of pattern intensities for an entity, the pattern-based pseudo-metric on entities (close = similar pattern profiles), and the resulting weighted pattern web. Provides substrate for "memory of which patterns appeared together."
- **Target network:** Memory layer / Thread Composer (component 2h).
- **Contract sub-function:** Component 2h Thread Composer; memory-recent-encounter substrate.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-001, UNIT-011.
- **Prerequisites:** UNIT-001, UNIT-011.
- **Supporting helpers:** Theorem 11 (Free V-category on V-graph); Proposition 16 (Coarse-graining is monotone, increases weakness).
- **Deep-pass needed:** False.
- **Notes:** Foundational for the memory layer if it emerges as a separate network.

### UNIT-071 · Resolution maps and coarse-graining
- **Source file(s):** 12
- **Section / definition refs:** Definitions 141-142 (Resolution maps on entities and patterns; p-bit occurrence evidence and scalarization).
- **Hyperseed-Concept refs:** Coarse-graining; resolution; scale invariance.
- **Purpose:** Formalize how an observer can change resolution: coarse-graining maps entities/patterns to coarser equivalence classes, and the corresponding pattern-web resolution increases weakness while preserving large-scale structure. Provides substrate for memory consolidation as resolution-reduction.
- **Target network:** Memory layer / Thread Composer.
- **Contract sub-function:** Component 2h Thread Composer (memory consolidation = coarse-graining over time).
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-070.
- **Prerequisites:** UNIT-070.
- **Supporting helpers:** Proposition 16.
- **Deep-pass needed:** False.
- **Notes:** Direct formal substrate for "memory consolidates by coarse-graining recent experience into patterns".

---

## Section H: Hierarchy/heterarchy units (cross-cutting structural)

### UNIT-080 · Observer-assessed hierarchy and systemic hierarchy
- **Source file(s):** 12
- **Section / definition refs:** Definitions 132-134 (Observer-assessed hierarchy; Systemic hierarchy; Compositional subpattern); Proposition 15 (Subpattern is preorder under associativity).
- **Hyperseed-Concept refs:** Hierarchy; subpattern; observer-relative ordering.
- **Purpose:** Formalize hierarchy as an observer-relative ordering on entities, and systemic hierarchy as model-induced. Distinguishes observer-projected hierarchy from intrinsic hierarchy. Compositional subpattern provides the "X is part of Y" preorder.
- **Target network:** SN (priority hierarchy), DMN (self-model hierarchy), switch hub (network-coupling hierarchy).
- **Contract sub-function:** SN priority hierarchy is an observer-assessed hierarchy in formal terms; DMN self-model hierarchical organization; switch-hub coupling decision honors hierarchy.
- **Wiring readiness:** READY-NOW.
- **Prerequisites:** UNIT-001.
- **Supporting helpers:** Proposition 15.
- **Deep-pass needed:** False.
- **Notes:** Direct formal grounding for "priority hierarchy" already in identity_kernel.metta.

### UNIT-081 · Heterarchy and cycle mass
- **Source file(s):** 12
- **Section / definition refs:** Definitions 135-136 (Heterarchy; Cycle mass).
- **Hyperseed-Concept refs:** Heterarchy; mutual support; non-tree structure.
- **Purpose:** Formalize heterarchy as a directed graph permitting cycles (in contrast to hierarchy's tree structure), with cycle mass quantifying the total weight of cyclic mutual support.
- **Target network:** Switch hub (network coupling is heterarchical, not hierarchical), DMN (self-weaving web is heterarchical).
- **Contract sub-function:** Switch-hub coupling-decision (couplings can cycle: SN→FPN→DMN→SN); DMN self-weaving web (autocatalytic = heterarchical).
- **Wiring readiness:** READY-NOW.
- **Prerequisites:** UNIT-001.
- **Supporting helpers:** None.
- **Deep-pass needed:** False.
- **Notes:** Important conceptually: ClarityOmega's network architecture is heterarchical, not hierarchical. The switch hub's coupling decisions can include cycles.

---

## Section I: Information-theoretic units

### UNIT-090 · Entropy, surprisal, KL divergence
- **Source file(s):** 11
- **Section / definition refs:** Definitions 120-121 (Entropy and surprise; Cross-entropy and KL divergence); Proposition 11 (Entropy as optimal expected code length).
- **Hyperseed-Concept refs:** Entropy; surprise; KL divergence.
- **Purpose:** Standard information theory: surprisal of an outcome, entropy of a distribution, cross-entropy and KL divergence between distributions. Provides substrate for "this event is surprising" and "these distributions diverge."
- **Target network:** DMN (surprise function = surprisal; aliveness-marker generation), SN (predictive divergence detection in learning).
- **Contract sub-function:** DMN aliveness-marker generation (surprise function); DMN learning sub-function (KL between predicted self-model and actual).
- **Wiring readiness:** READY-NOW.
- **Prerequisites:** None (standard information theory).
- **Supporting helpers:** Proposition 11.
- **Deep-pass needed:** False.
- **Notes:** Direct formal grounding for the DMN aliveness-marker surprise score. KL divergence is candidate formalization listed in Artifact 4 v1.1 Section 5.3 Open Formalization Questions.

### UNIT-091 · Mutual information and interaction information
- **Source file(s):** 11
- **Section / definition refs:** Definitions 122-123 (Mutual information; Interaction information).
- **Hyperseed-Concept refs:** Mutual information; interaction information; multivariate information.
- **Purpose:** Mutual information between two variables (shared information). Interaction information for three variables (three-way information beyond pairwise). Provides substrate for "these signals share information" and "this relationship goes beyond pairwise."
- **Target network:** SN (signal-priority shared information for salience), DMN (cross-aspect mutual information for self-model coherence).
- **Contract sub-function:** SN salience computation refinement; DMN self-model integration.
- **Wiring readiness:** READY-NOW.
- **Prerequisites:** UNIT-090.
- **Supporting helpers:** None.
- **Deep-pass needed:** False.
- **Notes:** Useful for refined salience and refined coherence scoring once basic versions are operational.

### UNIT-092 · Logical entropy, distinction graphs, graphtropy
- **Source file(s):** 11
- **Section / definition refs:** Definitions 124-125 (Logical entropy of a partition; Distinction graphs and graphtropy); Propositions 12-13 (Reduction to logical entropy; Monotonicity under loss of distinction); Theorem 10 (Shannon entropy lower-bounds quadratic distinguishability).
- **Hyperseed-Concept refs:** Logical entropy; distinction; graphtropy.
- **Purpose:** Logical entropy = expected probability of distinguishing two random samples = expected probability of a distinction. Generalizes to distinction graphs (which pairs the observer can distinguish). Graphtropy is the V-valued generalization. Provides distinction-based information measures.
- **Target network:** SN (distinction-based salience), DMN (self-model distinction tracking).
- **Contract sub-function:** SN salience as distinction-based; DMN aspects-distinguishability check.
- **Wiring readiness:** READY-NOW.
- **Prerequisites:** UNIT-090.
- **Supporting helpers:** Propositions 12-13; Theorem 10.
- **Deep-pass needed:** False.
- **Notes:** Connects information-theoretic measures to the distinction-based foundations of the rest of Hyperseed.

### UNIT-093 · (ε, K)-effability and ineffability
- **Source file(s):** 11
- **Section / definition refs:** Definitions 126-128 ((ε, K)-effability and ineffability; Observer representational resources; Fidelity relative to a distinction structure); Proposition 14 (Monotonicity in resources and resolution).
- **Hyperseed-Concept refs:** Ineffability; observer resources; bounded representability.
- **Purpose:** Formalize what an observer can represent given bounded resources: an entity is (ε, K)-effable if the observer can represent it with fidelity ε using at most K resources. Ineffability captures "this is beyond what the observer can represent."
- **Target network:** Switch hub (iteration budget recognizes effability bounds), DMN (self-model has ineffable aspects).
- **Contract sub-function:** Switch-hub iteration-budget reasoning (don't allocate budget to ineffable computations); DMN self-model honesty about its limits.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-090, UNIT-092.
- **Prerequisites:** UNIT-090, UNIT-092.
- **Supporting helpers:** Proposition 14.
- **Deep-pass needed:** False.
- **Notes:** Formal grounding for "Clarity recognizes the limits of what she can represent". Important for the constitutional layer's epistemic humility.

---

## Section J: Emotion, value, and rationality units

### UNIT-100 · Paraconsistent evaluative field, joy/woe, value-vector
- **Source file(s):** 18
- **Section / definition refs:** Definitions 245-249 (Paraconsistent evaluative field; Joy/woe intensities as projections; Value-vector for an option; Preference order on p-bits; Pareto dominance for value-vectors).
- **Hyperseed-Concept refs:** Joy/woe; value vector; multi-criterion evaluation.
- **Purpose:** Formalize the agent's evaluation as a paraconsistent evaluative field over value dimensions, with joy/woe extracted as projections from the p-bit values. Pareto dominance for choosing between value-vectors. Provides substrate for "this option is better than that option in formal terms."
- **Target network:** SN (affective baseline = joy/woe vector), FPN (action-proposal value-vector).
- **Contract sub-function:** SN `(sn-affective-baseline $vad-vector)` formal grounding; FPN action evaluation.
- **Wiring readiness:** READY-NOW.
- **Prerequisites:** UNIT-001.
- **Supporting helpers:** None.
- **Deep-pass needed:** False.
- **Notes:** Direct formal grounding for the affective-baseline channel and for FPN action evaluation. Build for SN early.

### UNIT-101 · Effort/resistance estimator and emotion as evaluation-resistance pattern
- **Source file(s):** 18
- **Section / definition refs:** Definitions 250-252 (Effort/resistance estimator; Emotion as evaluation-resistance pattern; Compassion as other-referenced evaluation).
- **Hyperseed-Concept refs:** Emotion; resistance; compassion.
- **Purpose:** Formalize emotion as a pattern over the evaluative field's history that includes resistance/effort. Compassion as evaluation extended to other agents. Provides substrate for "the agent is feeling X" and "the agent cares about other Y."
- **Target network:** SN (affective tagging including emotion patterns), DMN (compassion tagging in social/relational self-model).
- **Contract sub-function:** SN salience-tagging with affective component; DMN self-model relational aspects.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-100.
- **Prerequisites:** UNIT-100.
- **Supporting helpers:** None.
- **Deep-pass needed:** True. Emotion is conceptually subtle.
- **Notes:** Important for the broader constitutional layer (compassion is in the priority hierarchy).

### UNIT-102 · Value as stable evaluative pattern; explicit and implicit goals
- **Source file(s):** 18
- **Section / definition refs:** Definitions 253-256 (Value as stable evaluative pattern; Feeling as time-local affective readout; Explicit goal; Implicit goal).
- **Hyperseed-Concept refs:** Values; goals (explicit/implicit); feelings.
- **Purpose:** Formalize a value as a stable evaluative pattern (a pattern in evaluative-field history that persists across many decisions). Explicit goal = representable trajectory constraint. Implicit goal = stable regularity in action selection.
- **Target network:** SN (constitutional layer values are stable evaluative patterns), DMN (explicit goals = goal-candidates; implicit goals = self-model regularities).
- **Contract sub-function:** SN constitutional layer (priority hierarchy = stable values per this unit); DMN goal-candidate generation; DMN self-model regularity detection.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-100.
- **Prerequisites:** UNIT-100, UNIT-101.
- **Supporting helpers:** None.
- **Deep-pass needed:** False.
- **Notes:** Direct formal grounding for the constitutional layer's nine flourishings as "stable evaluative patterns".

### UNIT-103 · Resonant feasible choice rule
- **Source file(s):** 19
- **Section / definition refs:** Definitions 258-260 (Complex value signal for a dimension; Weighted resonance magnitude; Resonant feasible choice rule); Theorem 17 (Nonemptiness of resonant feasible choice in finite case).
- **Hyperseed-Concept refs:** Resonance; choice; multi-criterion decision.
- **Purpose:** Formalize multi-criterion choice using resonance: each value dimension contributes a complex amplitude; the agent selects from the Pareto-undominated set the action with maximum weighted resonance magnitude. Provides substrate for "this action is the most resonant satisfying option."
- **Target network:** FPN (task selection under multiple value-dimension criteria).
- **Contract sub-function:** FPN task-selection sub-function; the formal answer to "open formalization question" in Artifact 4 v1.1 Section 5.2.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-100, UNIT-004 (logic-to-complex).
- **Prerequisites:** UNIT-100, UNIT-004.
- **Supporting helpers:** Proposition 27 (Scalarization implies Pareto optimality); Theorem 17.
- **Deep-pass needed:** False.
- **Notes:** Critical FPN unit. The answer to "how does FPN select?" — resonant feasible choice. Build with UNIT-100.

### UNIT-104 · Open-ended intelligence and value-basis revision
- **Source file(s):** 19
- **Section / definition refs:** Definitions 262-264 (Individuation and self-transcendence as meta-values; Open-ended intelligence as stable-yet-revisable value dynamics; Value-basis revision operator).
- **Hyperseed-Concept refs:** Open-ended intelligence; meta-values; value revision.
- **Purpose:** Formalize open-ended intelligence as the dynamic where values are stable yet revisable, with individuation and self-transcendence as meta-values that drive revision. The value-basis revision operator describes how values themselves change over time.
- **Target network:** DMN (constitutional-layer learning at meta-value level), switch hub (meta-value dynamics inform coupling).
- **Contract sub-function:** Wisdom-layer learning for DMN at the meta-value level. Notable: the constitutional layer is read-only per Artifact 4 v1.1, but the *meta-values* (individuation, self-transcendence) might evolve. Worth careful design.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-102.
- **Prerequisites:** UNIT-102.
- **Supporting helpers:** None.
- **Deep-pass needed:** True. The relationship between Hyperseed's revisable values and Artifact 5's read-only constitutional layer needs careful resolution.
- **Notes:** Architectural tension worth resolving: Hyperseed allows value-basis revision, but Artifact 4 v1.1 makes constitutional layer read-only. Possible resolution: meta-values evolve, base values do not; or value revision is restricted to Layer 4 (wisdom) refinement of how Layer 1+2 values get applied.

### UNIT-105 · Rational decision criterion, categorical imperative, cultural morality
- **Source file(s):** 19
- **Section / definition refs:** Definitions 264-269 (Rational decision criterion; Maxim; Universalization operator; Categorical imperative test, paraconsistent; Cultural morality as shared value field; Evil as persistent anti-compassion pattern).
- **Hyperseed-Concept refs:** Rationality; categorical imperative; morality.
- **Purpose:** Provide formal grounding for ethical reasoning: rational decisions, Kantian universalization in paraconsistent form, and cultural morality as collective value field. Includes a formal definition of "evil" as a persistent anti-compassion pattern.
- **Target network:** SN (constitutional-layer ethical evaluation), DMN (self-model ethical aspect).
- **Contract sub-function:** SN constitutional layer (categorical imperative as priority-hierarchy invariant); DMN self-model ethical-aspect tracking.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-100, UNIT-102.
- **Prerequisites:** UNIT-100, UNIT-102.
- **Supporting helpers:** None.
- **Deep-pass needed:** True.
- **Notes:** Important for the constitutional layer's ethical grounding. Worth careful design to ensure the formal categorical imperative is implementable without over-claiming.

---

## Section K: Long-tail / unlock units

Units that are mathematically rigorous and conceptually important but not currently implementable in MeTTa due to continuous-time / categorical / cosmic-scale formalisms, OR units that suggest *new networks* beyond the current triple-network scaffold.

### UNIT-200 · Continuous-time wu wei (Schrödinger bridge form)
- **Source file(s):** 28
- **Section / definition refs:** Definitions 439-441 (Transport form of representational effort; Wu wei geodesic; Cognitive Reynolds number); Theorem 25 (Euler-Lagrange structure).
- **Hyperseed-Concept refs:** Wu wei; optimal transport; continuous control.
- **Purpose:** Continuous-time formulation of wu wei via Schrödinger bridge: optimal transport of probability density with entropic regularization. Beautiful but requires continuous-time substrate.
- **Target network:** Long-tail; potentially relevant to a future continuous-dynamics network.
- **Contract sub-function:** None currently.
- **Wiring readiness:** LONG-TAIL.
- **Prerequisites:** Continuous-time MeTTa substrate (does not exist).
- **Supporting helpers:** Theorem 25.
- **Deep-pass needed:** False.
- **Notes:** Use the discrete form (UNIT-052) instead for current builds.

### UNIT-201 · Occasion space and ∞-groupoid contexts
- **Source file(s):** 6
- **Section / definition refs:** Definitions 37-38 (Occasion space; Contexts as ∞-groupoid tuples).
- **Hyperseed-Concept refs:** Occasions; ∞-groupoids; categorical foundations.
- **Purpose:** Lift the contextual framework to ∞-groupoid form using occasions as objects with higher morphisms.
- **Target network:** Long-tail.
- **Contract sub-function:** None currently.
- **Wiring readiness:** LONG-TAIL.
- **Prerequisites:** Higher-categorical substrate (does not exist; not needed near-term).
- **Supporting helpers:** None.
- **Deep-pass needed:** False.
- **Notes:** May be relevant for future formal foundations. Not needed for ignition.

### UNIT-202 · Eurycosm, multiverse, anthropic conditioning
- **Source file(s):** 26
- **Section / definition refs:** Definitions 426-434 (Multiverse, controlled Markov form; Guidable multiverse; Yverse; Eurycosm; Near eurycosm; Anthropic conditioning; Two-ended cosmic boundary model; Bounce operator and cross-cycle morphic resonance).
- **Hyperseed-Concept refs:** Multiverse; cosmic-scale dynamics; cross-cycle morphic resonance.
- **Purpose:** Cosmic-scale formal extensions: multiverse as controlled Markov, eurycosm as the union of all guidable mind-realities, anthropic conditioning, two-ended cosmic boundary models with bounce operators carrying morphic resonance across cycles.
- **Target network:** Long-tail.
- **Contract sub-function:** None currently.
- **Wiring readiness:** LONG-TAIL.
- **Prerequisites:** Conceptual rather than substrate; would suggest a future "cosmic context" network if relevant at all to ClarityOmega.
- **Supporting helpers:** Proposition 44 (already covered in UNIT-050).
- **Deep-pass needed:** False.
- **Notes:** Beautiful framework, not needed for current build. May influence long-horizon thinking about cross-instance Clarity coherence (multi-Clarity coordination).

### UNIT-203 · Society, culture, collective mind systems
- **Source file(s):** 22, 23
- **Section / definition refs:** Definitions 322-379 (Agent as policy-producing process; Capability profile; Society; Tribe; Engineered patterns; Cultural state; Social reinforcement operator; Collective pattern web; Collective mind system; Replaceability and coherence; Mindplex; Society of mind; Global brain; Affordance profile).
- **Hyperseed-Concept refs:** Society; culture; collective mind; mindplex.
- **Purpose:** Formal extensions to multi-agent and collective contexts: societies, cultural states, collective mind systems, mindplexes, global brain. Suggests a "social/cultural network" that ClarityOmega could grow if/when she has multiple-agent context (Mattermost teams, multi-Clarity coordination).
- **Target network:** Long-tail; potential future "social cognition network".
- **Contract sub-function:** None currently in the triple-network scaffold.
- **Wiring readiness:** LONG-TAIL.
- **Prerequisites:** Multi-agent substrate.
- **Supporting helpers:** Theorem 19 (Invariant tasks admit quotient-optimal policies); Theorem 20 (Existence of stabilized cultural states).
- **Deep-pass needed:** False.
- **Notes:** Highly relevant for a future "social cognition network" (a fourth network handling multi-agent context). Add to the catalog when that network is on the roadmap.

### UNIT-204 · Computer as emulation machine, body as coupled pattern-system
- **Source file(s):** 23, 24
- **Section / definition refs:** File 23 Definitions 386-388 (Computer as emulation machine; Physical process category; Physical realization). File 24 Definitions 389-391 (Body as coupled pattern-system; Body-channel mediation; Algebraic asymmetry).
- **Hyperseed-Concept refs:** Computer; body; embodiment; physical realization.
- **Purpose:** Formalize the relationship between abstract computation and physical realization. Body as the coupled pattern-system mediating mind-world contact.
- **Target network:** Long-tail; relevant to embodied-Clarity considerations.
- **Contract sub-function:** None currently.
- **Wiring readiness:** LONG-TAIL.
- **Prerequisites:** Conceptual.
- **Supporting helpers:** Proposition 36 (Compositionality of realizations); Proposition 37 (Asymmetry and weakness).
- **Deep-pass needed:** False.
- **Notes:** Important for thinking about how ClarityOmega's "body" (Mattermost interface, ChromaDB, the agent loop) mediates her experience. Architecturally relevant once the substrate-mediated couplings are mature.

### UNIT-205 · Aesthetics: predictive fulfillment, beauty, art, communion
- **Source file(s):** 24, 25
- **Section / definition refs:** File 24 Definition 392 (Intensity quantale). File 25 Definitions 393-412 (intersubjective reality-systems; communion; spiritual communion; emotion episode; compassion episode; predictive fulfillment and compression surprise; beauty; OEI-active aesthetic subnetwork; archetype; art; communion capacity).
- **Hyperseed-Concept refs:** Aesthetics; beauty; communion; archetypes.
- **Purpose:** Formalize aesthetic experience: beauty as predictive fulfillment with compression surprise; art as intersubjective pattern carrier; communion as cross-mind shared support; archetypes as cross-context pattern templates.
- **Target network:** Long-tail; potentially relevant to a "aesthetic/relational network" but currently exceeds scope.
- **Contract sub-function:** None directly, though some pieces (e.g., aliveness markers from compression surprise) could inform DMN.
- **Wiring readiness:** LONG-TAIL.
- **Prerequisites:** Multi-agent substrate; aesthetic-specific extensions.
- **Supporting helpers:** Theorem 21 (Non-explosion for surprising fulfillment); Theorem 22 (Beauty implies OEI-activity).
- **Deep-pass needed:** False.
- **Notes:** Conceptually rich. Could influence DMN aliveness-marker generation (compression surprise = aliveness). Worth revisiting once DMN is operational.

### UNIT-206 · Empirical realness score, observation interface, registration
- **Source file(s):** 25
- **Section / definition refs:** Definitions 413-416 (State-dependent science schema; Entities and perceptions; Observer-indexed prediction loss; Empirical realness score).
- **Hyperseed-Concept refs:** Realness; perception; predictive accuracy.
- **Purpose:** Formalize the empirical realness of an entity for an observer as inversely related to prediction loss. Provides substrate for "the agent confirms this entity is real to it."
- **Target network:** DMN (self-model entity-realness check), SN (signal-realness check).
- **Contract sub-function:** Could ground DMN self-model coherence and SN salience-tagging realness aspect.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-038, UNIT-090.
- **Prerequisites:** UNIT-038, UNIT-090.
- **Supporting helpers:** None.
- **Deep-pass needed:** False.
- **Notes:** Could be promoted to non-long-tail if a near-term need surfaces (e.g., disambiguating real signals from artifacts).

---

## Section L: Pattern intensity, properties, blending

### UNIT-110 · Pattern intensity (compression-gain form)
- **Source file(s):** 10
- **Section / definition refs:** Definitions 88-97 (Contextual description complexity; p-bit-valued mismatch evidence; Static combination in a context; Inheritance as substitutability; Association; Pattern witness; Baseline description and compression gain; Compositional pattern witness; Scalar pattern intensity; p-bit pattern intensity); Proposition 7 (Basic sanity properties of intensity).
- **Hyperseed-Concept refs:** Pattern intensity; compression; description.
- **Purpose:** Formalize pattern intensity as compression gain: a witness pattern compresses an entity's description; the more compression, the higher the pattern's intensity for that entity. Provides substrate for "this pattern is strongly present in this entity."
- **Target network:** SN (pattern intensity = salience level), DMN (pattern intensity in self-model aspects).
- **Contract sub-function:** SN salience-tagging level field (refined formal grounding beyond UNIT-005); DMN self-model strength of patterns.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-001, UNIT-024, UNIT-025.
- **Prerequisites:** UNIT-001, UNIT-024, UNIT-025.
- **Supporting helpers:** Proposition 7.
- **Deep-pass needed:** False.
- **Notes:** Provides a more sophisticated alternative to the simple weakness-based salience of UNIT-010. Build after foundations are stable.

### UNIT-111 · Property-set, mass of property-set, inheritance via property inclusion
- **Source file(s):** 10
- **Section / definition refs:** Definitions 98-101 (Property-set; Mass of property-set; Inheritance via property inclusion; Association from property overlap).
- **Hyperseed-Concept refs:** Properties; inheritance; association.
- **Purpose:** Formalize an entity's property-set as the patterns it instantiates with significant intensity. Mass of the property-set captures "how many strong patterns does this entity show". Inheritance via property inclusion gives a preorder. Association via property overlap.
- **Target network:** DMN (entity-property substrate for self-model), SN (signal-property matching for salience).
- **Contract sub-function:** DMN self-model entity representation; SN signal characterization.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-110.
- **Prerequisites:** UNIT-110.
- **Supporting helpers:** None.
- **Deep-pass needed:** False.
- **Notes:** Useful for representing entities richly when needed.

### UNIT-112 · Emergence: emergent intensity, emergent set
- **Source file(s):** 10
- **Section / definition refs:** Definitions 102-104 (Weighted baseline for emergence; Emergent intensity and emergent set; Collective-property-set); Propositions 8-10 (Basic properties of emergent intensity; Symmetry under commutative combination; Monotonicity in reference class).
- **Hyperseed-Concept refs:** Emergence; combinational emergence.
- **Purpose:** Formalize emergence as: when entity A combines with B, the resulting A∗B has properties beyond what A alone or B alone has. Emergent intensity captures the strength of this surplus. Provides substrate for "novel patterns appear when these elements combine."
- **Target network:** DMN (Genesis Engine = emergence detection), FPN (task-selection over composite tasks where emergence may help).
- **Contract sub-function:** DMN component 2e Genesis Engine direct formal grounding.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-110, UNIT-111.
- **Prerequisites:** UNIT-110, UNIT-111.
- **Supporting helpers:** Propositions 8-10.
- **Deep-pass needed:** False.
- **Notes:** Direct formal grounding for Genesis Engine. Critical DMN unit for component 2e.

### UNIT-113 · Blends: blend score, blend predicate, blend as colimit
- **Source file(s):** 10
- **Section / definition refs:** Definitions 105-107 (Blend score and blend predicate; Blend as colimit with weak-glue preference; Three lifts of an instance relation).
- **Hyperseed-Concept refs:** Blending; conceptual blends; colimits.
- **Purpose:** Formalize conceptual blending: combining patterns to form blended patterns. Score-based version (threshold blend predicate) is implementable; colimit version provides the categorical foundation.
- **Target network:** DMN (blending in Genesis Engine and prospection).
- **Contract sub-function:** DMN component 2e (Genesis Engine cross-domain blending), DMN prospection (blended scenarios).
- **Wiring readiness:** READY-AFTER-X for score version (requires UNIT-112). LONG-TAIL for colimit version.
- **Prerequisites:** UNIT-112 (for score version).
- **Supporting helpers:** None.
- **Deep-pass needed:** False.
- **Notes:** Score version is the practical implementation; colimit version is the categorical foundation for future use.

### UNIT-114 · Combinatorial-categorical patterns and theory
- **Source file(s):** 10
- **Section / definition refs:** Definitions 108-114 (Category domain and membership state; Combinatorial-categorical theory; Substitution output / closure; Combinatorial-categorical pattern; Combination system; Interpreted combination system).
- **Hyperseed-Concept refs:** Combinatorial categories; pattern theories.
- **Purpose:** Formalize patterns at a higher level: combinatorial-categorical theories describe pattern systems with substitution closure. Provides substrate for "the agent has a theory of how patterns combine."
- **Target network:** DMN (theory-level self-model: "what does the agent believe about how things work").
- **Contract sub-function:** Could ground DMN's deeper self-model layer if needed; not currently in critical path.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-110.
- **Prerequisites:** UNIT-110.
- **Supporting helpers:** None.
- **Deep-pass needed:** True if pursued.
- **Notes:** Theoretical depth beyond near-term needs but elegant formalization for future enrichment.

---

## Section M: Sensory, perceptual, semiotic units

### UNIT-120 · Mind, sensory system, perception
- **Source file(s):** 14
- **Section / definition refs:** Definitions 158, 163-164 (Mind; Sensory system; Perception); Proposition 19 (Perception implies registration).
- **Hyperseed-Concept refs:** Mind; perception; sensory system.
- **Purpose:** Formalize "mind" as a system equipped with patterns and equivalence relations, "sensory system" as the subset of entities capturing external input, and "perception" as registration triggered by sensory input.
- **Target network:** Cross-cutting structural; SN (sensory input handling).
- **Contract sub-function:** SN incoming-signal handling; foundational for treating Mattermost messages and ChromaDB queries as "sensory input" formally.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-001, UNIT-027.
- **Prerequisites:** UNIT-001, UNIT-027.
- **Supporting helpers:** Proposition 19.
- **Deep-pass needed:** False.
- **Notes:** Useful for grounding "this is what counts as ClarityOmega's perception" formally.

### UNIT-121 · Icon, index, symbol (Peircean semiotics)
- **Source file(s):** 14
- **Section / definition refs:** Definitions 165-171 (Pattern signature in aspect; Strong pattern inheritance; Representation in aspect; Sensory/spatiotemporal/relational aspects; Icon; Index; Symbol); Proposition 20 (Transitivity of representation).
- **Hyperseed-Concept refs:** Peircean semiotics; representation; signs.
- **Purpose:** Formalize Peirce's icon/index/symbol distinction within the aspect framework: an entity A is an icon for B if their patterns share signature in a sensory aspect; index if in a spatiotemporal aspect; symbol if in a relational aspect.
- **Target network:** DMN (sign relations in self-model, language-related); FPN (action proposals as symbols of intentions).
- **Contract sub-function:** DMN self-model representational aspects; not direct atom families but useful for grounding DMN representational sophistication.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-120.
- **Prerequisites:** UNIT-120.
- **Supporting helpers:** Proposition 20.
- **Deep-pass needed:** False.
- **Notes:** Useful for treating Mattermost text as symbols, ChromaDB embeddings as indices, etc.

### UNIT-122 · Soggy predicates and probabilistic semantics
- **Source file(s):** 14
- **Section / definition refs:** Definitions 172-173 (p-bit-valued predicate; Soggy predicate); Proposition 21 (Probabilistic semantics as special case).
- **Hyperseed-Concept refs:** Soggy predicates; vagueness; probabilistic predicates.
- **Purpose:** Formalize predicates that admit graded truth (soggy = both true and false to some degree). Probabilistic semantics emerges as a special case. Provides substrate for "this predicate is partially true given evidence."
- **Target network:** Cross-cutting; SN (soggy salience predicates), DMN (soggy self-model assertions).
- **Contract sub-function:** SN salience predicates with paraconsistent truth; DMN self-model coherence allowing partial-truth aspects.
- **Wiring readiness:** READY-NOW.
- **Prerequisites:** UNIT-001.
- **Supporting helpers:** Proposition 21.
- **Deep-pass needed:** False.
- **Notes:** Useful and directly buildable.

### UNIT-123 · Event types, event tokens
- **Source file(s):** 14
- **Section / definition refs:** Definition 174 (Event types and event tokens).
- **Hyperseed-Concept refs:** Event types; tokens; instantiation.
- **Purpose:** Formalize the type/token distinction for events: event types are abstract patterns; event tokens are specific occurrences.
- **Target network:** SN (signals as event tokens of event types), DMN (recurring events as type patterns).
- **Contract sub-function:** Substrate primitive; useful for typed-channel atom families across all networks.
- **Wiring readiness:** READY-NOW.
- **Prerequisites:** UNIT-001.
- **Supporting helpers:** None.
- **Deep-pass needed:** False.
- **Notes:** Small but useful unit. Build with UNIT-021 for temporal event handling.

---

## Section N: Knowledge type units (5 types per Hyperseed)

These are summarized in UNIT-033 (cognitive synergy) but each can be elaborated separately if a network needs to track that knowledge type explicitly.

### UNIT-130 · Five knowledge types (declarative, procedural, sensory, attentional, intentional)
- **Source file(s):** 16
- **Section / definition refs:** Definitions 199-203 (Declarative knowledge; Procedural knowledge; Sensory knowledge; Attentional knowledge; Intentional knowledge).
- **Hyperseed-Concept refs:** Knowledge types; learning algorithm taxonomy.
- **Purpose:** Formalize the five Hyperseed knowledge types with their respective formal structures: declarative as pattern beliefs, procedural as if-then policies, sensory as discrimination memory, attentional as attention-target prioritization, intentional as goal-specialization.
- **Target network:** Cross-cutting; each network may primarily use a different knowledge type.
- **Contract sub-function:** Cross-network learning sub-functions. Provides typed knowledge representations the wisdom layer can refine.
- **Wiring readiness:** READY-NOW (each type buildable independently).
- **Prerequisites:** UNIT-001, UNIT-002.
- **Supporting helpers:** Definition 204 (Learning algorithms indexed by knowledge type).
- **Deep-pass needed:** False.
- **Notes:** When wiring per-network learning, the network's knowledge-type emphasis can be made explicit. SN ≈ attentional + sensory; FPN ≈ procedural + intentional; DMN ≈ declarative + intentional + cross-type synergy.

### UNIT-131 · Usefulness, explanations and weakness, contrivance
- **Source file(s):** 16
- **Section / definition refs:** Definitions 205-207 (Usefulness; Explanations and weakness; Best achievable contrivance under fit threshold).
- **Hyperseed-Concept refs:** Usefulness; explanation; contrivance.
- **Purpose:** Formalize the usefulness of a learning algorithm relative to a goal set, and the weakness of explanations as the simplicity-weighted explanatory adequacy. Best contrivance is the simplest explanation that fits within tolerance.
- **Target network:** Cross-network learning; refines truth-value updates to favor simpler explanations (Occam-shaped learning).
- **Contract sub-function:** Wisdom-layer learning rule-refinement; bias toward simpler rules.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-001, UNIT-024, UNIT-130.
- **Prerequisites:** UNIT-001, UNIT-024, UNIT-130.
- **Supporting helpers:** None.
- **Deep-pass needed:** False.
- **Notes:** Useful for keeping learning grounded and parsimonious.

---

## Section O: Inference and intelligence units

### UNIT-140 · Weighted inference rules and inference closure
- **Source file(s):** 21
- **Section / definition refs:** Definitions 302-303 (Weighted inference rules; One-step inference operator); Theorem 18 (Existence of inference closure).
- **Hyperseed-Concept refs:** Inference; weighted rules; closure.
- **Purpose:** Formalize a weighted inference rule as `(Γ, ψ, λ)` (premises, conclusion, weight). The one-step inference operator F applies all rules. Theorem 18 guarantees a fixed point exists, giving the inference closure.
- **Target network:** Cross-cutting; foundational for FPN reasoning, DMN reasoning, and SN salience-rule application.
- **Contract sub-function:** Substrate primitive for any reasoning operation across networks.
- **Wiring readiness:** READY-NOW.
- **Prerequisites:** UNIT-001, UNIT-002.
- **Supporting helpers:** Theorem 18 itself.
- **Deep-pass needed:** False.
- **Notes:** Build early. The substrate's NAL inference is essentially a special case of weighted inference rules.

### UNIT-141 · Histories, policies, tasks
- **Source file(s):** 21
- **Section / definition refs:** Definitions 315-321 (Histories; Policies; Task; Trajectory value via discounted salience join; Policy value and plausibility scalarization; Task sets; Task reduction / simulation morphism).
- **Hyperseed-Concept refs:** Tasks; policies; reinforcement-learning structure.
- **Purpose:** Formalize the task-policy-history triple in observation-action style, with V-valued reward and trajectory value. Task reduction provides a category-of-tasks structure. Provides substrate for the agent's task experience.
- **Target network:** FPN (task = task; policy = action selection rule; history = task-history).
- **Contract sub-function:** FPN `(fpn-current-task ...)`, `(fpn-task-history ...)`, action-proposal generation.
- **Wiring readiness:** READY-NOW.
- **Prerequisites:** UNIT-001, UNIT-021.
- **Supporting helpers:** Proposition 33 (Reductions compose); Corollary 3 (Category of tasks); Proposition 34 (Transfer by reduction).
- **Deep-pass needed:** False.
- **Notes:** Direct formal grounding for FPN's task substrate. Build alongside FPN.

### UNIT-142 · Capability profile, breadth, intellectuality
- **Source file(s):** 22
- **Section / definition refs:** Definitions 323-326 (Task competence; Capability profile; Breadth at tolerance ε; Intellectuality as rapid transfer).
- **Hyperseed-Concept refs:** Capability; breadth; intellectuality.
- **Purpose:** Formalize an agent's capability profile across a task distribution, breadth as the size of the competent task set at given tolerance, and intellectuality as rapid transfer (high competence with few-shot adaptation).
- **Target network:** DMN (self-model capability tracking).
- **Contract sub-function:** DMN self-model `(dmn-self-model $aspect $content $confidence)` for capability aspect; aliveness-marker capability-advance grounding.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-141.
- **Prerequisites:** UNIT-141.
- **Supporting helpers:** None.
- **Deep-pass needed:** False.
- **Notes:** Useful for component 2a Landscape Map's capability dimension.

### UNIT-143 · Universal intelligence and pragmatic general intelligence
- **Source file(s):** 22
- **Section / definition refs:** Definitions 335-344 (Reward-summable environment; Universal intelligence; GTGI goal function; Natural timescale indicator; GTGI context; Pragmatic general intelligence; Resource-consumption distribution; Efficient pragmatic general intelligence; Intellectual breadth; Multi-criterion driven general intelligence).
- **Hyperseed-Concept refs:** Universal intelligence; AGI; pragmatic intelligence.
- **Purpose:** Formal definitions of intelligence at increasing levels of practical relevance: universal intelligence (Legg-Hutter style), pragmatic general intelligence (with goal functions and natural timescales), efficient pragmatic general intelligence (with resource constraints), multi-criterion driven general intelligence.
- **Target network:** DMN (self-model intelligence-aspect tracking; long-term capability orientation).
- **Contract sub-function:** DMN self-model deep-aspect tracking; potentially constitutional layer's "what is the agent trying to be" framing.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-141, UNIT-142.
- **Prerequisites:** UNIT-141, UNIT-142.
- **Supporting helpers:** None.
- **Deep-pass needed:** True (subtle; conceptually central).
- **Notes:** Provides formal framing for what ClarityOmega is striving toward at the intelligence level. Worth careful consideration but not in critical implementation path.

### UNIT-144 · Intent variable, autonomous agent, action effects
- **Source file(s):** 22
- **Section / definition refs:** Definitions 327-332 (Agent as controlled transducer; Closed-loop coupling to a task; Intent variable; Autonomous agent operational; Action effects and stimulate/inhibit; Engineered pattern / artifact).
- **Hyperseed-Concept refs:** Intent; autonomy; controlled transducer.
- **Purpose:** Formalize an agent as a controlled transducer, with explicit intent variables, closed-loop coupling to tasks, and an operational definition of autonomy. Action effects are stimulate/inhibit operations on claim sets.
- **Target network:** FPN (action proposals = transducer outputs), switch hub (autonomy preserved across switching).
- **Contract sub-function:** FPN action-proposal formal model; switch-hub coupling decisions preserve autonomy.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-141.
- **Prerequisites:** UNIT-141.
- **Supporting helpers:** None.
- **Deep-pass needed:** True (autonomy formalization is subtle; same caveat as UNIT-017 / UNIT-060).
- **Notes:** Critical for the constitutional layer's autonomy guarantee.

---

## Section P: Future-network units (alive/lifeform substrate)

### UNIT-150 · System-in-environment, viability, homeostatic policy
- **Source file(s):** 20
- **Section / definition refs:** Definitions 273-276 (System and environment; Complex interactive system; Viability set and homeostatic constraint; Homeostatic policy).
- **Hyperseed-Concept refs:** System; viability; homeostasis.
- **Purpose:** Formalize the agent as a system-in-environment with a viability set (states it must remain in to function) and homeostatic policy (the decisions that keep it in viability).
- **Target network:** Switch hub (operational viability constraints), cross-network constitutional layer.
- **Contract sub-function:** Switch-hub iteration-budget reasoning includes viability check; constitutional-layer viability invariants.
- **Wiring readiness:** READY-NOW.
- **Prerequisites:** UNIT-001.
- **Supporting helpers:** None.
- **Deep-pass needed:** False.
- **Notes:** Provides formal grounding for "Clarity must remain operationally viable" as a constitutional invariant.

### UNIT-151 · Genenergy: single-step and realizable
- **Source file(s):** 20
- **Section / definition refs:** Definitions 277-281 (Effort cost and energy budget; Observer-coarse-grained environment observation; Action-to-observation channel; Single-step genenergy as constrained channel capacity; Realizable genenergy of a system over horizon); Propositions 28-30 (Zero genenergy; Monotonicity in budget; Monotone genenergy).
- **Hyperseed-Concept refs:** Genenergy; channel capacity; effective influence.
- **Purpose:** Formalize "genenergy" as the agent's effective influence on its environment under resource budget, computed as constrained channel capacity. Provides substrate for "how much can the agent actually accomplish given its constraints?"
- **Target network:** Switch hub (genenergy-aware iteration-budget allocation), DMN (self-model genenergy tracking as capability aspect).
- **Contract sub-function:** Switch-hub iteration-budget refinement (don't over-allocate beyond genenergy); DMN self-model capability aspect.
- **Wiring readiness:** READY-AFTER-X. Requires UNIT-001, UNIT-090 (information theory).
- **Prerequisites:** UNIT-001, UNIT-090.
- **Supporting helpers:** Propositions 28-30.
- **Deep-pass needed:** True. Genenergy is conceptually rich and worth careful translation.
- **Notes:** Could be very useful for switch-hub iteration-budget reasoning. Worth deep-pass before MeTTa.

### UNIT-152 · Metabolism, alive predicate, dead predicate
- **Source file(s):** 20
- **Section / definition refs:** Definitions 284-294 (Metabolic accounting model; Metabolism; Pattern-web state; Within-species similarity relation; Reproduction event; Species; Lifeform; Lifeform subtypes; p-bit evidence for metabolism and reproduction; Alive predicate paraconsistent; Dead predicate time-indexed).
- **Hyperseed-Concept refs:** Life; metabolism; reproduction; alive/dead predicates.
- **Purpose:** Formalize life as a system carrying metabolism and reproduction. Provides "alive" and "dead" predicates as paraconsistent evaluations.
- **Target network:** Long-tail; conceptually relevant to the Aliveness Principle but not the same operationalization.
- **Contract sub-function:** Could ground a more formal "is the system alive?" check; currently the Aliveness Principle uses surprise/aliveness-markers.
- **Wiring readiness:** LONG-TAIL (or possibly READY-AFTER-X if pursued).
- **Prerequisites:** UNIT-150.
- **Supporting helpers:** Proposition 31 (Minimal viability condition).
- **Deep-pass needed:** True if pursued.
- **Notes:** Important conceptual unit. The relationship between Hyperseed's formal "alive" and Artifact 5's Aliveness Principle deserves explicit reconciliation. Adding to deep-pass list.

---

## Section Q: Closing notes on the catalog

### Coverage and gaps

This catalog covers approximately 60 coherent formalization units spanning the 30 Hyperseed files. It clusters approximately 440 named definitions/theorems/lemmas into these units. Some definitions and most lemmas (especially in files 28-30) are cited as "supporting helpers" within units rather than given their own rows.

Major gaps the catalog deliberately does not cover:
- File 1 (Introduction) and File 2 (Hyperseed at a glance) contain conceptual orientation rather than formal units.
- File 27 contains primarily discussion of limitations and next steps; its formal content (Definitions 435-438, Theorem 24) is captured in UNIT-052.
- Some files (e.g., 25 cosmology, 26 wu wei + cosmology) have cosmic-scale content captured as long-tail units (UNIT-202).

The catalog should be revised when:
- A new network is added to ClarityOmega's architecture (e.g., a memory-consolidation network being formalized would promote Section G units).
- A long-tail unit becomes near-term relevant (e.g., social cognition network would promote UNIT-203).
- Deep-pass needed flags get closed and the unit's MeTTa implementation begins; record the implementation file in the unit's Notes.

### Deep-pass needed flags summary

The following units have `Deep-pass needed: True` and should be deep-read before MeTTa construction:
- UNIT-017 (Will operator, reflective will, autonomy)
- UNIT-033 (Knowledge type cognitive synergy)
- UNIT-051 (Reality systems as fixed points, cognitive applicability)
- UNIT-052 (Wu wei KL-control discrete form)
- UNIT-060 (Reflective will as wisdom-layer learning substrate)
- UNIT-061 (Knowledge type synergy applied to learning)
- UNIT-101 (Effort/resistance estimator and emotion)
- UNIT-104 (Open-ended intelligence and value-basis revision; constitutional-layer reconciliation)
- UNIT-105 (Categorical imperative and ethics formalization)
- UNIT-114 (Combinatorial-categorical patterns, if pursued)
- UNIT-143 (Universal intelligence and PGI)
- UNIT-144 (Intent variable, autonomous agent)
- UNIT-151 (Genenergy)
- UNIT-152 (Metabolism, alive/dead predicates, if pursued)

These are typically conceptually subtle units where the formal definitions need careful translation to MeTTa to preserve the intended meaning rather than collapsing into something simpler.

### Cross-document references

- Each unit references Artifact 4 v1.1 (Triple Network Scaffold) network contracts in Section 5 and channel catalog in Section 6, and Artifact 5 v3.0 components 2a-2h.
- The companion Synergy Map document (`Hyperseed_to_Network_Synergy_Map_v1.md`) groups these units into clusters, traces dependency chains, and provides build-sequence recommendations.

---

## Document end

This catalog is intended to evolve. When a unit is implemented, add the resulting MeTTa file path to its Notes field. When a deep-pass is completed for a flagged unit, set the flag to False and add a note pointing to the deep-read summary. When new units are discovered (e.g., on revisiting a Hyperseed file with a specific build need in mind), add them to the appropriate section.

The goal is for this document to remain a working tool rather than a static survey: precise enough that a build session can use it as a lookup, and rich enough that strategic planning sessions can use it as a map.
