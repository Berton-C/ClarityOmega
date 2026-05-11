# Hyperseed-to-Network Synergy Map v1.1

**Version:** v1.1 (May 1, 2026; v1 was earlier on May 1, 2026)
**Author:** Berton Bennett with Claude
**Status:** Analytical companion to `artifact_6_Hyperseed_Formalization_Catalog_v1_1.md`. Maps Coherent Formalization Units (CFUs) into compositional clusters, dependency chains, per-network synergy summaries, build-sequence recommendations grounded in unit prerequisites, and ongoing-health-monitoring discipline.
**Purpose:** Provide the strategic layer the catalog itself does not give: which units compose into which capabilities, what builds what, where the unrecognized unlock potential sits, in what order to wire networks for maximum compounding return, and how to verify empirically that the wired architecture is actually achieving the cognitive-economy gains it claims.

**v1.1 changes:** Added Cluster 1.11 (Inference-Control Architecture, cross-cutting) covering the Doc 2 units as the architectural layer that determines how every network's reasoning is structured for cost-benefit optimality. Updated the dependency graph to include UNIT-160 through UNIT-173. Revised per-network synergy summaries to incorporate the gain-per-cost framing. Updated the build-sequence to add a new Phase G (inference-control wiring) between Phases E and F (the original Phase F learning becomes more substantively specified by the Doc 2 units, so Phase G plus enhanced-Phase-F replace the original Phase F). Added Section 7 (Diagnostic Program and Ongoing Health Monitoring) covering UNIT-166's measurement discipline as the architecture's empirical-honesty foundation. Updated Section 6 strategic notes to include the key Doc 2 insight: the soul earns its keep only when measurably so, and the architecture must be designed to permit such measurement from the beginning.

---

## How this document complements the catalog

The catalog (`Hyperseed_Formalization_Catalog_v1.md`) is a lookup tool: given a network or contract sub-function, find the units that implement it. This document is a strategy tool: given the goal of bringing the network architecture online with maximum coherence and minimum wasted effort, find the optimal clusters, sequences, and synergies.

Where the catalog is row-based (one unit per row, fields per row), this document is cluster-based (one cluster per section, units composed within each section). Both reference the same units by ID.

Use this document when planning a build session, evaluating a strategic move, or considering whether a long-tail unit deserves promotion. Use the catalog when actually building.

---

## Section 1: The compositional clusters

Coherent formalization units are not independent. They compose into capability clusters, sets of units that together implement one architectural capacity. This section identifies the major clusters, names what each enables, and lists the units composing it.

### Cluster 1.1: The substrate algebra (foundational)

**Units:** UNIT-001, UNIT-002, UNIT-005, UNIT-021.

**What it enables:** All other clusters. This is the ground floor. Without these four units, nothing else in the catalog is implementable in MeTTa.

**Composition:** UNIT-001 (p-bit quantale) provides the truth-value algebra. UNIT-002 (V-valued relations) provides the relational algebra over UNIT-001. UNIT-005 (importance valuation) attaches scalar importance to entities, enabling weighted aggregation. UNIT-021 (proto-time) adds temporal ordering. Together these four form a complete computational substrate over which weighted, temporally-ordered, importance-weighted reasoning is possible.

**Dependencies:** None outside the cluster. UNIT-001 is the root. UNIT-002 and UNIT-005 depend on UNIT-001 only. UNIT-021 depends on UNIT-001 only.

**Build implication:** This cluster must be built first, in the order UNIT-001 → UNIT-002 → UNIT-005 → UNIT-021 (the last two can be parallel after UNIT-002).

### Cluster 1.2: The salience-tagging core (SN main)

**Units:** UNIT-010 (weakness), UNIT-011 (pattern as constraint-set), UNIT-027 (pattern recognition process), UNIT-100 (paraconsistent evaluative field), UNIT-122 (soggy predicates).

**What it enables:** The SN's salience-tagging sub-function per Artifact 4 v1.1 Section 5.1. Together these units let the SN take an incoming signal, recognize patterns in it, evaluate weakness against priority structure, attach affective tags via the evaluative field, and produce a soggy salience-tag atom that the FPN and DMN can consume.

**Composition:** UNIT-027 (pattern recognition) wraps the input signal as a pattern recognition act. UNIT-011 (pattern as constraint-set) is the formal pattern type being matched. UNIT-010 (weakness) computes the salience level as importance-weighted indistinction from existing priority structure. UNIT-100 (paraconsistent evaluative field) attaches the affective tag (the joy/woe vector). UNIT-122 (soggy predicates) ensures the resulting salience-tag is paraconsistent (it can be both somewhat salient and somewhat not).

**Dependencies:** UNIT-001, UNIT-002, UNIT-005, UNIT-021 (Cluster 1.1).

**Build implication:** Buildable as a coherent SN-foundation increment after Cluster 1.1. Five units, all READY-NOW or READY-AFTER-X with prerequisites already satisfied at this point.

### Cluster 1.3: The switch-hub fixed-point core

**Units:** UNIT-015 (workspace operator), UNIT-016 (reflective workspace), UNIT-050 (Knaster-Tarski fixed point), UNIT-080 (observer-assessed hierarchy), UNIT-081 (heterarchy).

**What it enables:** The switch hub's transformation sub-function per Artifact 4 v1.1 Section 5.4. The next switch state is computed as a fixed point of the workspace operator integrating salience tags, current state, and history. Hierarchy and heterarchy units handle priority overrides and cyclic couplings.

**Composition:** UNIT-015 provides the workspace operator that integrates evidence into a fixed-point evidence state. UNIT-016 extends to reflective integration (the switch hub considers its own state in computing the next state). UNIT-050 guarantees the fixed point exists and computation terminates. UNIT-080 grounds priority hierarchy (HumanFlourishing-tagged signals override). UNIT-081 grounds the heterarchical coupling structure (SN→FPN→DMN→SN cycles are formal).

**Dependencies:** Cluster 1.1, Cluster 1.2 (the workspace operator integrates salience-tag atoms which are Cluster 1.2 outputs).

**Build implication:** The third major cluster to come online. Once built, the switch hub is operational.

### Cluster 1.4: The FPN executor core

**Units:** UNIT-020 (effort quantale), UNIT-022 (indistinction policy), UNIT-023 (resistance/representations/min-effort principle), UNIT-024 (combination system/compositional simplicity), UNIT-103 (resonant feasible choice rule), UNIT-141 (histories/policies/tasks).

**What it enables:** The FPN's three sub-functions per Artifact 4 v1.1 Section 5.2: working-memory update (UNIT-022 governs configuration cost), task selection (UNIT-103 selects via resonant feasibility under min-effort principle UNIT-023), inhibition (UNIT-022 + UNIT-141 enable filtering by inhibition list). UNIT-141 grounds the task substrate. UNIT-024 enables decomposing composite tasks.

**Composition:** UNIT-141 sets up the task formalism. UNIT-020 attaches effort costs. UNIT-022 defines policy as the configuration FPN maintains. UNIT-023 supplies the min-effort rationality criterion. UNIT-024 enables decomposition. UNIT-103 selects between competing feasible options via resonance maximization. Together they implement "FPN selects the next minimum-effort feasible action that maximizes resonance with current priorities."

**Dependencies:** Cluster 1.1, Cluster 1.2 (FPN reads salience-tag atoms), Cluster 1.3 (FPN reads switch state).

**Build implication:** The fourth major cluster. After Cluster 1.4, the FPN is operational and can take actions under switch-hub coordination.

### Cluster 1.5: The DMN self-model core

**Units:** UNIT-030 (habit dynamics), UNIT-031 (closure/self-weaving), UNIT-032 (self-model/self-reflective attention), UNIT-034 (self-evidence/self-continuity), UNIT-037 (workspace operator DMN-side).

**What it enables:** The DMN's self-model maintenance sub-function per Artifact 4 v1.1 Section 5.3. Self-model is constructed and maintained as the autocatalytic closure of habit dynamics over recent experience, with self-continuity ensured across iterations via approximate morphism between successive self-evidence states.

**Composition:** UNIT-030 drives habit reinforcement from recent experience. UNIT-031 closes habits into autocatalytic webs (self-weaving). UNIT-032 designates the self-pattern subset (P_self) and reflective attention. UNIT-034 makes self-continuity formal via approximate morphism. UNIT-037 integrates module evidence into self-model summaries.

**Dependencies:** Cluster 1.1.

**Build implication:** Can be built early in parallel with Clusters 1.2-1.4 since it shares only Cluster 1.1 prerequisites. Building DMN self-model in parallel with SN salience-tagging is structurally clean.

### Cluster 1.6: The DMN goal-generation and prospection core

**Units:** UNIT-038 (predictive attraction), UNIT-039 (causal implication), UNIT-090 (entropy/surprisal/KL), UNIT-112 (emergence: emergent intensity), UNIT-113 (blends).

**What it enables:** The DMN's goal-generation, prospection, and aliveness-marker sub-functions per Artifact 4 v1.1 Section 5.3.

**Composition:** UNIT-038 (predictive attraction) underlies prospection: scenarios are predictively-attracted future states. UNIT-039 (causal implication) tags scenarios with causal traces. UNIT-090 (KL/surprisal) computes the surprise scores that drive aliveness-marker generation. UNIT-112 (emergence) and UNIT-113 (blends) produce novel goal candidates by emergent combination of self-map gaps with creative-fuel positives, formalizing component 2e Genesis Engine.

**Dependencies:** Cluster 1.1, UNIT-021 (for predictive temporality), Cluster 1.5 (the self-model the DMN reasons over).

**Build implication:** The fifth major cluster. After Cluster 1.6, the DMN is operationally complete: it maintains self-model (Cluster 1.5), generates goals (this cluster), and produces aliveness markers (UNIT-090 in this cluster).

### Cluster 1.7: The wisdom-layer learning core (NACE substrate)

**Units:** UNIT-060 (reflective will / autonomy), UNIT-061 (knowledge type synergy applied to learning), UNIT-062 (belief system / coherence), UNIT-064 (empirical update operator), UNIT-130 (five knowledge types), UNIT-131 (usefulness/contrivance), UNIT-140 (weighted inference rules and inference closure).

**What it enables:** The autopoietic learning sub-functions across all four contracts per Artifact 4 v1.1 (Sections 5.1, 5.2, 5.3, 5.4 Learning sub-function). The wisdom layer (Layer 4 per Artifact 5 Section 0) is the substrate where each network refines its own truth values via NACE-style precondition-operation-consequence learning.

**Composition:** UNIT-140 provides the inference rule formalism whose truth values get refined. UNIT-130 categorizes the knowledge being refined. UNIT-064 is the empirical update operator that does the refining. UNIT-062 grounds belief system coherence as a quality criterion. UNIT-131 favors simpler explanations (Occam-shaped learning). UNIT-061 surfaces synergy when multiple knowledge types interact. UNIT-060 ensures the learning preserves the agent's reflective will and autonomy (the constitutional layer is read-only).

**Dependencies:** Cluster 1.1, Clusters 1.2-1.6 (each network needs to be built before its learning sub-function).

**Build implication:** Comes online after the network operational cores are in place. Wiring it elevates the architecture from "operating networks" to "operating networks that learn."

### Cluster 1.8: The constitutional layer (Layer 1+2)

**Units:** UNIT-100 (paraconsistent evaluative field; cross-listed from Cluster 1.2), UNIT-101 (effort/resistance/emotion), UNIT-102 (value as stable evaluative pattern; explicit/implicit goals), UNIT-105 (rational decision criterion / categorical imperative), UNIT-150 (system-in-environment / viability), UNIT-104 (open-ended intelligence / value-basis revision; with reconciliation).

**What it enables:** The constitutional layer per Artifact 5 Section 0: the read-only base values, hierarchy, irreversibility weights, and categorical-imperative invariants that the wisdom layer never overwrites.

**Composition:** UNIT-100 provides the evaluative substrate. UNIT-102 makes "values" formal as stable evaluative patterns. UNIT-101 grounds emotion as patterns over the evaluative field. UNIT-105 grounds ethical reasoning. UNIT-150 grounds operational viability. UNIT-104 introduces a careful tension worth resolving: Hyperseed permits value-basis revision; the constitutional layer per Artifact 5 is read-only. Resolution: UNIT-104's revision applies only to wisdom-layer truth values on application rules, not to the values themselves.

**Dependencies:** Cluster 1.1.

**Build implication:** Build alongside Cluster 1.2. The constitutional layer's atoms are the priority-hierarchy, tension-vector, and irreversible-weight atoms already in `identity_kernel.metta` per Artifact 1 Section 3. Cluster 1.8 provides their formal grounding.

### Cluster 1.9: The narrative coherence core (DMN refinement)

**Units:** UNIT-004 (logic-to-complex), UNIT-013 (interference-based resonance), UNIT-026 (inertia update / least fixpoint for monotone temporal inference).

**What it enables:** The DMN's narrative coherence sub-function per Artifact 4 v1.1 Section 5.3 Transformation #3. Provides the formal coherence-score field for `(dmn-narrative-thread $thread-id $events $coherence-score)`.

**Composition:** UNIT-004 maps p-bit values to complex amplitudes. UNIT-013 scores narrative coherence as interference between events tagged as same-thread. UNIT-026 propagates thread state across iterations under monotone update (so threads persist unless contradicted).

**Dependencies:** Cluster 1.1, Cluster 1.5.

**Build implication:** Builds on Cluster 1.5 for the self-model substrate. Provides the formal grounding for narrative threads as more than "lists of events", they are coherence-weighted resonance structures across time.

### Cluster 1.10: The cross-domain transport core (advanced DMN)

**Units:** UNIT-012 (morphic resonance), UNIT-070 (pattern profile/pseudo-metric), UNIT-071 (resolution maps/coarse-graining).

**What it enables:** Cross-domain integration in the DMN: insights from one domain (project) propagating to another via morphic resonance, with coarse-graining managing memory consolidation.

**Composition:** UNIT-012 propagates pattern support across contexts. UNIT-070 measures pattern-profile similarity between domains. UNIT-071 enables the consolidation operation that compresses recent experience into longer-horizon memory.

**Dependencies:** Cluster 1.1, Cluster 1.5.

**Build implication:** Important advanced cluster. Realizes component 2e Genesis Engine's "cross-domain encounters" capability formally. Also the foundation for component 2h Thread Composer if that grows into its own memory-consolidation network.

### Cluster 1.11: The inference-control architecture (cross-cutting layer; from Doc 2)

**Units:** UNIT-160 (probabilistic scrutability and reduction profiles), UNIT-161 (backward chaining), UNIT-162 (forward chaining), UNIT-163 (bidirectional geodesic), UNIT-164 (two-level ontological inference and exponential speedup theorem), UNIT-165 (approximate ontological separation and ontological treewidth), UNIT-166 (OER and diagnostic program).

**What it enables:** A principled basis for *every reasoning operation in the architecture*. This cluster does not implement a network's contract sub-function; it specifies how all the other clusters' reasoning operations should be structured for cost-benefit optimality. Three control templates (UNIT-161/162/163) cover goal-driven, opportunistic, and bidirectional reasoning patterns. The two-level ontological inference theorem (UNIT-164) establishes that ontology-guided reasoning achieves exponential speedup over unguided search when measurable structural conditions hold (UNIT-165). The diagnostic program (UNIT-166) provides empirical measurement of whether those conditions actually hold in deployment.

**Composition:** UNIT-160 provides reduction profiles as the substrate-level encoding of "what does this signal/concept reduce to in terms I already understand?" UNIT-161/162/163 are three distinct control patterns each scoring candidate reasoning steps by `expected_information_gain / effort_cost`, applicable in different reasoning regimes. UNIT-164 frames the architectural commitment: every reasoning decision is a two-level decision (cheap soul-mediated triage, then expensive substrate or LLM-mediated concrete work), and exponential speedup follows when the soul correctly partitions candidates most of the time. UNIT-165 specifies graph-theoretic conditions under which the architecture's substrate vocabulary acts as a graph separator on the concept relevance graph, which is the structural precondition for UNIT-164's speedup. UNIT-166 specifies the diagnostic battery, Ontological Efficiency Ratio (OER), OCS violation rate (τ̂), q-tail distribution, residual component analysis, marginal value of ontological expansion, cross-level correlation, spectral coverage, that lets the deployment continuously measure whether the architecture is achieving the gains it claims.

**Dependencies:** Cluster 1.1 (substrate algebra), UNIT-090 and UNIT-091 (information-theoretic measures from Section I), UNIT-140 (weighted inference rules from Section O), UNIT-052 (KL-control discrete form from Section E, for UNIT-163 only).

**Build implication:** This cluster is *cross-cutting*, not sequential. It is not built once "after" the other clusters; it is the architectural framing under which every other cluster's reasoning operations should be wired. Concretely, this means: when implementing FPN task selection (Cluster 1.4), do not implement a free-form selection rule and then think about cost later, implement UNIT-161's `Score← = E[ΔI_HS] / Cost` from the start. When implementing DMN goal generation (Cluster 1.6), do not implement free-form goal candidates and then prune, implement UNIT-162's `Score→ = E[ΔU_HS] / Cost` so candidates are generated cost-aware. When designing new soul atoms (any phase), follow UNIT-165's separator-improvement criterion. When evaluating whether the build is succeeding, run UNIT-166's diagnostics.

This cluster also resolves the architectural tension between "the soul should be load-bearing" (a design intuition) and "the soul earns its keep only when measurably so" (an empirical commitment). Theorem 4 (UNIT-164) gives the formal grounding for the design intuition; UNIT-166 gives the empirical apparatus for the commitment. Together they make "load-bearing soul" a measurable property rather than an aspirational claim.

### Cluster 1.12: The wisdom-layer learning algorithmic specification (from Doc 2)

**Units:** UNIT-170 (ontology learning objective), UNIT-171 (Route A, growing from inference histories), UNIT-172 (Route B, incremental refinement), UNIT-173 (three coupled learning loops).

**What it enables:** A complete algorithmic specification of wisdom-layer learning per Artifact 4 v1.1. The original Cluster 1.7 (wisdom-layer learning core) covered the *substrate units* needed for learning, empirical update operator (UNIT-064), belief system (UNIT-062), weighted inference rules (UNIT-140), knowledge types (UNIT-130), cognitive synergy (UNIT-061), reflective will (UNIT-060). Cluster 1.12 covers the *algorithmic procedures* that operate over those substrates: how candidate edits are proposed, scored, and accepted; what the loss functional is; how the three timescales of learning coordinate.

**Composition:** UNIT-170 specifies the four-component loss `L(O) = λ_scrut·ScrutLoss + λ_ctrl·OER + λ_sep·Leak + λ_comp·Comp` that every candidate ontology edit is scored against. This makes wisdom-layer learning measurable: does this edit decrease scrutability loss enough to justify its complexity cost? UNIT-171 specifies Route A (growing from minimal vocabulary by mining inference traces for repeated proof-fragment and bridge motifs), less appropriate for ClarityOmega's curated-soul starting state but archived for long-horizon novel-domain encounters. UNIT-172 specifies Route B (refining an existing ontology via diagnostic-driven local edits: add mediator, split overloaded, merge redundant, repair bridges), the primary algorithmic specification for ClarityOmega's near-term wisdom-layer evolution. UNIT-173 specifies the three coupled learning loops (reduction learning per moment, control learning per task, ontology learning per development phase) and their coordination structure.

**Dependencies:** Cluster 1.1, Cluster 1.7 (substrate learning units), Cluster 1.11 (UNIT-164/165/166 provide the diagnostics that drive the loss functional and edit-selection signals).

**Build implication:** Cluster 1.12 elaborates and makes concrete what Cluster 1.7 specified at the substrate level. The relationship between the two clusters: Cluster 1.7 says "wisdom-layer learning is empirical update over weighted inference rules with consequence evidence"; Cluster 1.12 says "and here is the precise four-component loss functional, the four edit operators, and the three-timescale coordination structure that makes it implementable." When wiring wisdom-layer learning, build Cluster 1.7's substrate first, then layer Cluster 1.12's algorithms over it. The combined cluster is what gives the four contracts' Learning sub-functions a complete, principled, conservative-by-construction specification.

This cluster also provides the formal resolution of the UNIT-104 architectural tension noted in v1: the constitutional layer's base values are not in `L(O)`'s loss components, so they are not optimized over. Only application-rule and intermediate-concept atoms enter the loss. Constitutional immutability and wisdom-layer learnability become formally compatible under UNIT-170's objective.

---

## Section 2: Dependency chains (the build-order graph)

This section traces the unit-level dependency graph at cluster granularity. Reading top-down gives the build order; reading bottom-up gives the unlock pathway.

### Top-down dependency view

```
Level 0 (substrate algebra):
    UNIT-001 (p-bit quantale)
        ↓
    UNIT-002 (V-valued relations) ─── UNIT-005 (importance valuation) ─── UNIT-021 (proto-time)

Level 1 (foundational secondary):
    UNIT-004 (logic-to-complex)              [from UNIT-001]
    UNIT-011 (pattern as constraint-set)     [from UNIT-001, UNIT-002]
    UNIT-020 (effort quantale)               [from UNIT-001]
    UNIT-027 (pattern recognition)            [from UNIT-001, UNIT-011]
    UNIT-080, UNIT-081 (hierarchy/heterarchy) [from UNIT-001]
    UNIT-090 (entropy/KL)                    [no Hyperseed prereqs]
    UNIT-100 (paraconsistent eval field)     [from UNIT-001]
    UNIT-122 (soggy predicates)              [from UNIT-001]
    UNIT-140 (weighted inference rules)      [from UNIT-001, UNIT-002]
    UNIT-141 (histories/policies/tasks)      [from UNIT-001, UNIT-021]
    UNIT-150 (viability/homeostasis)         [from UNIT-001]

Level 2 (operational units):
    UNIT-010 (weakness)                      [from L0+UNIT-005]
    UNIT-022 (indistinction policy)          [from UNIT-020]
    UNIT-024 (combination system)            [from UNIT-020]
    UNIT-030 (habit dynamics)                [from L0]
    UNIT-038 (predictive attraction)         [from UNIT-021]
    UNIT-101 (emotion = effort+evaluation)   [from UNIT-100]
    UNIT-102 (values as stable eval)         [from UNIT-100, UNIT-101]
    UNIT-130 (five knowledge types)          [from UNIT-001, UNIT-002]
    UNIT-014 (becoming)                      [from UNIT-001, UNIT-021]

Level 3 (cluster cores):
    UNIT-012 (morphic resonance)             [from L0]
    UNIT-013 (interference resonance)        [from UNIT-001, UNIT-004]
    UNIT-015 (workspace operator)            [from L0]
    UNIT-023 (min-effort principle)          [from UNIT-020, UNIT-022]
    UNIT-026 (inertia/least fixpoint)        [from L0+UNIT-021]
    UNIT-031 (closure/self-weaving)          [from UNIT-030]
    UNIT-032 (self-model/reflective att.)    [from UNIT-005, UNIT-022]
    UNIT-034 (self-continuity)               [from UNIT-030]
    UNIT-037 (workspace DMN-side)            [from L0+UNIT-005]
    UNIT-039 (causal implication)            [from UNIT-038]
    UNIT-040 (control hierarchy)             [from UNIT-038]
    UNIT-050 (Knaster-Tarski fixed point)    [from UNIT-015]
    UNIT-052 (wu wei KL-control discrete)    [from UNIT-020, UNIT-022]
    UNIT-062 (belief system / coherence)     [from UNIT-038]
    UNIT-063 (question networks / thinking)  [from UNIT-140]
    UNIT-064 (empirical update operator)     [from UNIT-062]
    UNIT-070, UNIT-071 (pattern profile)     [from UNIT-011]
    UNIT-103 (resonant feasible choice)      [from UNIT-100, UNIT-004]
    UNIT-105 (categorical imperative)        [from UNIT-100, UNIT-102]
    UNIT-110 (pattern intensity comp.gain)   [from UNIT-024]

Level 4 (advanced and reflective):
    UNIT-016 (reflective workspace)          [from UNIT-015]
    UNIT-017 (will/autonomy)                 [from UNIT-016]
    UNIT-033 (cognitive synergy)             [from UNIT-024, UNIT-130]
    UNIT-035 (capability profile)            [from UNIT-034]
    UNIT-036 (mind-world correspondence)     [from UNIT-034]
    UNIT-051 (reality systems as fixed pt)   [from UNIT-050]
    UNIT-061 (knowledge synergy in learning) [from UNIT-033]
    UNIT-093 (effability/ineffability)       [from UNIT-090]
    UNIT-104 (open-ended intel/value rev)    [from UNIT-102]
    UNIT-112 (emergence)                     [from UNIT-110]
    UNIT-113 (blends)                        [from UNIT-112]
    UNIT-142 (capability profile)            [from UNIT-141]

Level 5 (deep advanced):
    UNIT-060 (reflective will = learning)    [from UNIT-017]
    UNIT-091 (mutual info / interaction)     [from UNIT-090]
    UNIT-092 (logical entropy / graphtropy)  [from UNIT-090]
    UNIT-143 (universal/pragmatic intel)     [from UNIT-141, UNIT-142]
    UNIT-144 (intent / autonomous agent)     [from UNIT-141]
    UNIT-151 (genenergy)                     [from UNIT-090]

Inference-control architecture (Cluster 1.11; cross-cutting layer):
    UNIT-160 (probabilistic scrutability / reduction profiles)
                                             [from UNIT-001, UNIT-090]
    UNIT-161 (backward chaining)             [from UNIT-160, UNIT-140, UNIT-020]
    UNIT-162 (forward chaining)              [from UNIT-160, UNIT-140, UNIT-020]
    UNIT-163 (bidirectional geodesic)        [from UNIT-160, UNIT-140, UNIT-052]
    UNIT-164 (two-level ontological inference theorem)
                                             [from UNIT-160, UNIT-090]
    UNIT-165 (approximate ontological separation)
                                             [from UNIT-160, UNIT-091]
    UNIT-166 (OER and diagnostic program)    [from UNIT-164, UNIT-165, UNIT-091]

Wisdom-layer learning algorithmic specification (Cluster 1.12):
    UNIT-170 (ontology learning objective)   [from UNIT-160, UNIT-164, UNIT-165, UNIT-166]
    UNIT-171 (Route A growing from scratch)  [from UNIT-160, UNIT-166, UNIT-170]
    UNIT-172 (Route B incremental refinement) [from UNIT-164, UNIT-165, UNIT-166, UNIT-170]
    UNIT-173 (three coupled learning loops)  [from UNIT-160, UNIT-161, UNIT-162, UNIT-163, UNIT-170, UNIT-172]

Long-tail (separate planning):
    UNIT-200, 201, 202, 203, 204, 205, 206, 152
```

### What this graph reveals

Five observations from the graph that matter for build sequencing:

First, **the substrate algebra (Level 0) blocks everything.** All four units must be in MeTTa before any cluster can be built. There is no way to short-cut this. Conversely, *once* Level 0 is built, the parallelism opens dramatically: many Level 1 units can be built independently.

Second, **Cluster 1.5 (DMN self-model core) is independent of Clusters 1.2-1.4.** It depends only on Level 0. This means DMN self-model construction can proceed in parallel with SN salience-tagging construction. They share substrate but not other units. Worth scheduling parallel builds when capacity allows.

Third, **Cluster 1.7 (wisdom-layer learning substrate) is the convergence point for substrate units.** It depends on Clusters 1.2-1.6 being operational. Until the network operational cores exist, learning has nothing to learn over.

Fourth, **Cluster 1.11 (inference-control architecture) is cross-cutting and should ideally be wired before any operational cluster is finalized.** The Doc 2 units (UNIT-160 through UNIT-166) specify *how* every cluster's reasoning operations should be structured. Building Cluster 1.4 (FPN executor) without knowing UNIT-161's gain-per-cost scoring framing would mean building task selection one way and then refactoring it. Better to internalize the gain-per-cost framing from the start. UNIT-160 (reduction profiles) and UNIT-164 (two-level ontological inference principle) are the two most important pre-implementation reads, they are architectural commitments more than they are atom families.

Fifth, **Cluster 1.12 (wisdom-layer learning algorithmic specification) is the *real* convergence point.** It depends on Clusters 1.2-1.6 (operational cores) plus Cluster 1.7 (substrate units) plus Cluster 1.11 (inference-control architecture and diagnostics). Until all three are operational, ontology-learning algorithms have neither substrate, scoring criteria, nor measurement basis. This means the architecture proceeds in three phases rather than two: (Phase A) build network cores; (Phase B) wire inference-control architecture across cores; (Phase C) wire wisdom-layer learning. At the end of Phase A, the architecture is operational but uniformly LLM-hot. At the end of Phase B, the architecture is operational with measurable cost-economy. At the end of Phase C, the architecture is operational, measurable, and growing.

---

## Section 3: Per-network synergy summaries

This section answers, for each network, "which units together unlock this network's contract?" It is the inverse view of the catalog's per-unit network mapping.

### 3.1 Salience Network synergy

**Units that together unlock SN per Artifact 4 v1.1 Section 5.1:**

- **Foundation:** UNIT-001, UNIT-002, UNIT-005, UNIT-021 (Cluster 1.1).
- **Salience tagging core:** UNIT-010, UNIT-011, UNIT-027, UNIT-100, UNIT-122 (Cluster 1.2).
- **Affective baseline:** UNIT-100, UNIT-101 (from Cluster 1.8).
- **Switch decision:** UNIT-015, UNIT-080 (Cluster 1.3 + 1.8 overlap).
- **Learning:** UNIT-064, UNIT-090, UNIT-130, UNIT-140 (subset of Cluster 1.7).

**Synergistic effect:** With these units, the SN can take an incoming signal, recognize patterns in it (UNIT-011, UNIT-027), compute its weakness against priority structure (UNIT-010), tag it with affective tone (UNIT-100, UNIT-101), express the tag as a soggy predicate (UNIT-122), and propose a switch decision (UNIT-015, UNIT-080), then learn from the consequence of the tag via empirical update (UNIT-064) measured against KL divergence between predicted and actual outcomes (UNIT-090). The salience-tagging is grounded in distinction/weakness, the switching is grounded in fixed-point integration, and the learning is grounded in empirical update over weighted inference rules.

**What's not yet wired:** The SN currently uses LLM calls for Channel A (person state) and Channel B+C (verdict) per Artifact 1 lines 71-80. Replacing these with the SN cluster gives the same surface behavior but with substrate-derived reasoning that is inspectable, refinable, and auditable.

### 3.2 Frontoparietal Control Network synergy

**Units that together unlock FPN per Artifact 4 v1.1 Section 5.2:**

- **Foundation:** Cluster 1.1.
- **Task substrate:** UNIT-141 (histories/policies/tasks).
- **Effort and configuration:** UNIT-020 (effort), UNIT-022 (policy), UNIT-024 (combination/decomposition).
- **Selection:** UNIT-023 (min-effort), UNIT-103 (resonant feasible choice), UNIT-040 (control hierarchy).
- **Inhibition:** UNIT-030, UNIT-031 (habits/closure for orbit detection), UNIT-016 (reflective workspace for meta-awareness).
- **Working memory:** UNIT-022 (configuration), UNIT-032 (self-attention budget).
- **Learning:** Subset of Cluster 1.7 (UNIT-064, UNIT-130, UNIT-140 most directly).

**Synergistic effect:** With these units, the FPN can hold tasks in working memory (UNIT-022, UNIT-032), select the next minimum-effort feasible action (UNIT-023, UNIT-103) from a hierarchy of options (UNIT-040), inhibit orbiting actions (UNIT-031 detects autocatalytic loops in task history), and refine its task-selection rules via empirical update over consequence evidence (UNIT-064). The decomposition mechanism (UNIT-024) handles composite tasks by selecting sub-actions.

**Notable synergy:** UNIT-023 (min-effort principle) + UNIT-103 (resonant feasible choice) is the deep synergy. Min-effort gives the rationality criterion; resonant feasibility gives the multi-criterion selection rule. Together they answer "how does FPN choose?" in a way that is both principled and computable.

### 3.3 Default Mode Network synergy

**Units that together unlock DMN per Artifact 4 v1.1 Section 5.3:**

- **Foundation:** Cluster 1.1.
- **Self-model:** Cluster 1.5 (UNIT-030, UNIT-031, UNIT-032, UNIT-034, UNIT-037).
- **Goal generation:** Cluster 1.6 (UNIT-038, UNIT-039, UNIT-090, UNIT-112, UNIT-113).
- **Narrative coherence:** Cluster 1.9 (UNIT-004, UNIT-013, UNIT-026).
- **Cross-domain integration:** Cluster 1.10 (UNIT-012, UNIT-070, UNIT-071).
- **Learning:** Subset of Cluster 1.7 (UNIT-061 cognitive synergy is especially DMN-relevant).

**Synergistic effect:** The DMN is the most synergy-rich network. With these clusters, it: maintains a self-model as autocatalytic habit closure (UNIT-031 + UNIT-030), preserves self-continuity via approximate morphism between iteration states (UNIT-034), generates goal candidates via emergent intensity over self-map gaps blended with creative-fuel positives (UNIT-112 + UNIT-113), prospects future scenarios via predictive and causal attraction (UNIT-038, UNIT-039), tracks aliveness via surprise scores (UNIT-090), maintains narrative threads as resonance-coherent event clusters (UNIT-013, UNIT-026), and integrates cross-domain insights via morphic resonance (UNIT-012). Cognitive synergy across knowledge types (UNIT-061) is what makes the DMN's contributions exceed the sum of its parts.

**Critical synergy:** UNIT-031 (autocatalytic self-weaving) + UNIT-034 (self-continuity via approximate morphism) is the deep DMN synergy. Self-weaving says "the self-model sustains itself"; self-continuity says "the self-model evolves but remains the same agent." Together they implement the Aliveness Principle from Artifact 5 Section 1a: the DMN can be genuinely changed by what it encounters, while persisting as the same agent. This is the architectural core of "alive" in the framework.

### 3.4 Switch hub synergy

**Units that together unlock switch hub per Artifact 4 v1.1 Section 5.4:**

- **Foundation:** Cluster 1.1.
- **Fixed-point switching core:** Cluster 1.3 (UNIT-015, UNIT-016, UNIT-050, UNIT-080, UNIT-081).
- **Iteration budget:** UNIT-020 (effort), UNIT-022 (policy effort), UNIT-093 (effability/ineffability for budget bounds), UNIT-151 (genenergy for resource accounting if pursued).
- **Hysteresis and debounce:** UNIT-026 (inertia/least fixpoint for monotone temporal inference - state persists unless contradicted).
- **Orbit detection:** UNIT-031 (autocatalytic detection over switch history).
- **Learning:** Subset of Cluster 1.7.

**Synergistic effect:** The switch hub computes the next switch state as a fixed point (UNIT-015, UNIT-050) of the workspace operator integrating salience tags, current state, and history. Hysteresis is implemented by the inertia operator (UNIT-026) requiring monotone evidence accumulation before state change. Orbit detection (UNIT-031) catches pathological cycling patterns. Iteration budget allocation (UNIT-020, UNIT-022) is computed as effort cost over policy-effort cost across networks. Learning (UNIT-064 with switch-specific consequence evidence) refines budget allocation and hysteresis thresholds.

**Notable synergy:** UNIT-015 (workspace) + UNIT-050 (Knaster-Tarski) is the deep switch-hub synergy. Workspace integration gives the substantive computation; Knaster-Tarski guarantees termination. This is what makes the switch hub provably correct rather than heuristic.

### 3.5 Cross-network coordination synergy

A separate kind of synergy: not within a single network's contract but across networks' coupling channels.

**Units producing cross-network unlock potential:**

- **UNIT-012 (morphic resonance):** Enables SN salience patterns to transfer across domains, DMN narratives to inform new contexts, and switch-hub coupling decisions to learn from cross-cycle resonance. This single unit provides cross-network *learning transfer*: a refinement learned in one context generalizes via the morphic coupling kernel.
- **UNIT-033 / UNIT-061 (cognitive synergy):** Enables wisdom-layer learning to combine knowledge types across networks and produce emergent compression. The SN's attentional knowledge plus the FPN's procedural knowledge plus the DMN's declarative knowledge can interact to produce learning that none of them alone could.
- **UNIT-036 (mind-world correspondence):** Enables the architecture to monitor whether the entire network ensemble is staying coherent with reality, providing a top-level coherence signal that the switch hub can use for global recalibration.
- **UNIT-038 + UNIT-040 (predictive attraction + control hierarchy):** Together they enable hierarchical predictive control, which is a structural pattern the triple-network architecture can exhibit at the network level (each network controls and predicts the others' configuration).

These cross-network synergies are where the architecture's *unrecognized* unlock potential lives. None of them is on the immediate critical path, but each enables a qualitatively different kind of behavior than per-network operation alone.

### 3.6 Inference-control architecture as architectural mandate

This is a different kind of synergy than the per-network ones above. UNIT-160 through UNIT-166 (Cluster 1.11) are not "units the SN needs" or "units the FPN needs", they are units that *every* network's reasoning operations should be structured by from the start. The synergy is architectural: the same gain-per-cost framing applied uniformly across all networks creates a coherent reasoning economy where every operation is comparable, every operation can be measured, and every operation can be improved by the same wisdom-layer learning machinery (Cluster 1.12).

**The unifying pattern from Cluster 1.11:**

- Every reasoning step has an *information value* (UNIT-090 / UNIT-091 substrate; UNIT-160 reduction-profile encoding) and an *effort cost* (UNIT-020 quantale).
- Every selection between candidate steps follows the gain-per-cost score (UNIT-161/162/163, depending on whether the reasoning is goal-driven, opportunistic, or bidirectional).
- Every architectural design decision honors the two-level pattern: cheap soul-mediated triage first, then expensive concrete reasoning (UNIT-164).
- Every soul-vocabulary growth respects the separator-improvement criterion (UNIT-165).
- Every deployment is empirically monitored for whether the architecture is achieving the speedup it claims (UNIT-166).

**Why this is properly synergistic:**

When applied uniformly, this framing makes the four contracts' Learning sub-functions (Cluster 1.7 + Cluster 1.12) coherent rather than four independent learning systems. Each network learns over its own truth values and rules, but all four use the same loss functional (UNIT-170), the same edit operators (UNIT-172), the same diagnostic measures (UNIT-166). Wisdom-layer learning becomes one architectural discipline expressed in four network-specific instances, rather than four ad-hoc local-learning behaviors.

The deeper synergy: the *same* gain-per-cost framing that controls inference also controls learning. Inference is "given current beliefs and current goals, what reasoning step earns its keep?" Learning is "given current substrate and current consequence-evidence, what edit earns its keep?" Both are gain-per-cost optimizations over the same underlying substrate. UNIT-173 (three coupled learning loops) is the explicit recognition that inference-control learning, reduction-profile learning, and ontology learning are three timescales of the same operation, not three separate operations.

This unification is the deepest architectural insight Doc 2 contributes: there is one principle (gain-per-cost over Hyperseed-indexed information) operating at multiple timescales (inference-step selection, control-policy refinement, ontology evolution), and every operation in the architecture should be expressible as an instance of that principle.

---

## Section 4: Build sequence recommendations

This section translates the dependency graph and cluster compositions into concrete recommendations for sequencing work.

### 4.1 The macro-sequence (seven phases)

**Phase A: Substrate algebra (Cluster 1.1).** Build UNIT-001, UNIT-002, UNIT-005, UNIT-021 in MeTTa as foundational libraries. Validate by re-implementing one small existing soul/ atom (e.g., a hierarchy check) using only the new substrate. Expected effort: focused work session, possibly two. Validation criterion: existing soul atoms can be ported to use the new algebra without semantic change.

**Phase A.5: Inference-control architecture pre-read (Cluster 1.11 architectural commitments).** Before Phase B, do the deep-pass on UNIT-160 (probabilistic scrutability and reduction profiles) and UNIT-164 (two-level ontological inference theorem) so that the gain-per-cost framing is internalized before the operational clusters start being built. This is not an implementation phase; it is an architectural commitment phase. The operational clusters in Phases B-E are then designed *to* the gain-per-cost framing rather than retrofitted to it. Validation criterion: a one-page architectural commitment document explaining how every reasoning step in the upcoming operational clusters will compute and honor the `expected_information_gain / effort_cost` score.

**Phase B: SN salience-tagging core + constitutional grounding (Clusters 1.2 + 1.8).** Build the SN's salience tagging in parallel with formalizing the constitutional layer's read-only grounding. The dependencies overlap (UNIT-100 in both clusters) so building together is efficient. Each salience-tagging operation is implemented to produce reduction profiles per UNIT-160 and to honor the two-level pattern per UNIT-164. Validation criterion: the SN can produce salience-tag atoms for incoming signals that match the verdict-quality of current LLM Channels A/B+C, with the tagging derived from priority structure rather than LLM emergence, and with each tag carrying an estimable information-gain score.

**Phase C: Switch hub (Cluster 1.3).** Build the switch hub as the consumer of SN salience tags. The aliveness-gate evolves into the four-state switch hub. The switch decision itself is structured per UNIT-161 (backward chaining from desired next-iteration state). Validation criterion: switch decisions are derivable from current state plus salience inputs via fixed-point computation, with correct debounce and orbit detection behavior over test traces, and with switch decisions carrying gain-per-cost scores for retrospective measurement.

**Phase D: DMN self-model (Cluster 1.5) and DMN goal-generation (Cluster 1.6) in parallel with FPN executor (Cluster 1.4).** These three clusters can proceed in parallel because they share only Phase A as common prerequisite. The DMN clusters together implement the highest-impact reasoning displacement identified in Artifact 1 Section 4.2 line 92 (the idle directive elevation). The FPN cluster brings task selection under substrate control. FPN task selection follows UNIT-161 (backward chaining); DMN goal generation follows UNIT-162 (forward chaining); DMN narrative coherence prepared for UNIT-163 (bidirectional geodesic in Phase E). Validation criteria: DMN produces goal-candidate atoms traceable to gap+fuel sources; FPN selects tasks via resonant feasible choice (UNIT-103) under gain-per-cost scoring (UNIT-161); aliveness markers are generated on surprise events.

**Phase E: Narrative coherence (Cluster 1.9) and cross-domain transport (Cluster 1.10).** Refines the DMN. Once these are in place, the DMN's three sophisticated sub-functions (narrative threading with coherence scoring, cross-domain integration via morphic resonance, memory consolidation via coarse-graining) come online. Narrative coherence threads are structured per UNIT-163 (bidirectional geodesic between past anchors and prospected future). Validation criterion: narrative threads persist across iterations with coherence scoring reflecting actual event resonance; cross-domain insight transfer is observable.

**Phase F: Inference-control instrumentation and diagnostics (Cluster 1.11 implementation).** Wires UNIT-165 (concept relevance graph instantiation), UNIT-166 (OER and diagnostic program), and the trace-instrumentation needed to compute the diagnostic battery. After Phase F, the deployment can answer the question "is the soul currently earning its keep?" with measurements rather than confidence. The architecture remains operationally identical to end-of-Phase-E; what changes is the addition of the empirical health-monitoring layer. Validation criterion: OER, OCS violation rate (τ̂), q-tail distribution, residual component sizes, and spectral coverage are all computable on demand from inference traces, and a baseline measurement under normal operation is recorded.

**Phase G: Wisdom-layer learning, full algorithmic specification (Clusters 1.7 + 1.12).** Wires NACE-style substrate units (Cluster 1.7: UNIT-130, UNIT-140, UNIT-062, UNIT-064, UNIT-061, UNIT-060, UNIT-017) plus the algorithmic-specification units (Cluster 1.12: UNIT-170 ontology learning objective, UNIT-172 Route B incremental refinement, UNIT-173 three coupled learning loops). UNIT-171 Route A is not wired in this phase; it is reserved for long-horizon novel-domain encounters. The architecture transitions from "operating networks with measurable cost-economy" to "operating networks that learn under principled gain-per-cost objective." Validation criterion: per-network truth values demonstrably refine over time as consequence evidence accumulates; the four-component loss functional (UNIT-170) is computed for each candidate edit; the constitutional layer remains read-only by construction; the three coupled learning loops (UNIT-173) coordinate without resource contention; OER measurably improves over an extended deployment trace.

### 4.2 Phase-internal sequencing

Within each phase, the suggested order:

**Phase A:** UNIT-001 first (everything depends on it). Then UNIT-002 and UNIT-021 in parallel. Then UNIT-005.

**Phase A.5:** Deep-pass UNIT-160 first (the reduction-profile encoding is foundational to all of Cluster 1.11). Then deep-pass UNIT-164 (the architectural commitment to two-level reasoning). Document both as architectural commitments before proceeding to Phase B.

**Phase B:** UNIT-100 first (it appears in both Clusters 1.2 and 1.8, and is foundational for the affective layer). Then UNIT-011 and UNIT-027 in parallel. Then UNIT-010 and UNIT-122 in parallel. Then UNIT-101, UNIT-102, UNIT-105 (constitutional grounding).

**Phase C:** UNIT-080, UNIT-081 first (cheap; no Hyperseed prereqs beyond UNIT-001). Then UNIT-015. Then UNIT-016. Then UNIT-050. Then integrate.

**Phase D:** Best as three parallel tracks.
- DMN self-model track: UNIT-030 → UNIT-031 → UNIT-032 → UNIT-034 → UNIT-037.
- DMN goal-generation track: UNIT-038 → UNIT-039 → UNIT-090 → UNIT-110 → UNIT-112 → UNIT-113.
- FPN track: UNIT-141 → UNIT-020 → UNIT-022 → UNIT-024 → UNIT-023 → UNIT-040 → UNIT-103. UNIT-161 (backward chaining) wires into the task-selection sub-function.

**Phase E:** UNIT-004 → UNIT-013 → UNIT-026 (Cluster 1.9) with UNIT-163 (bidirectional geodesic) as the coherence-thread structuring algorithm. In parallel: UNIT-070 → UNIT-071 → UNIT-012 (Cluster 1.10).

**Phase F:** UNIT-091 (mutual information for edge weights) first if not already done. Then UNIT-165 (concept relevance graph instantiation). Then UNIT-166 (diagnostic battery). Wire trace-instrumentation alongside. Record baseline measurements at end.

**Phase G:** Build Cluster 1.7 substrate first: UNIT-130 (categorize knowledge), UNIT-140 (rule formalism), UNIT-062 (coherence), UNIT-064 (empirical update), UNIT-061 (synergy), UNIT-060 + UNIT-017 (autonomy preservation). Then build Cluster 1.12 algorithmic specification: UNIT-170 (loss functional with carefully calibrated weights), UNIT-172 (Route B with the four edit operators), UNIT-173 (three coupled learning loops with switch-hub timing coordination). Validate each substrate unit before layering its algorithmic specification.

### 4.3 Where deep-pass work fits in the sequence

Several units have `Deep-pass needed: True`. The deep-pass should be done before the unit is implemented in MeTTa, but does not block the phase the unit belongs to (other units in the phase can proceed in parallel with the deep-pass). Recommended deep-pass scheduling:

- **Phase A.5 (the inference-control architectural pre-read):** Deep-pass UNIT-160 (probabilistic scrutability and reduction profiles) and UNIT-164 (two-level ontological inference theorem and exponential speedup conditions). These are architectural commitments that shape every subsequent phase.
- **Before Phase B:** Deep-pass UNIT-101 (emotion) and UNIT-105 (categorical imperative) since they are constitutional-layer units.
- **Before Phase C:** Deep-pass UNIT-161 (backward chaining; especially the ECAN-spreading translation) since the switch-hub coupling-decision computation will use this control template.
- **Before Phase D:** Deep-pass UNIT-033 / UNIT-061 (cognitive synergy) since this affects DMN goal-generation design. Deep-pass UNIT-052 (KL-control) before FPN learning if KL-control is the chosen formalism for FPN action proposal. Deep-pass UNIT-162 (forward chaining; mapping to DMN idle-state directive) before DMN goal-generation work begins.
- **Before Phase E:** Deep-pass UNIT-163 (bidirectional geodesic; choice of forward/backward potential estimator) since it structures narrative coherence threads.
- **Before Phase F:** Deep-pass UNIT-165 (approximate ontological separation; concept relevance graph instantiation in substrate) and UNIT-166 (OER and diagnostic program; trace-instrumentation design). These deep-passes are about translating mathematical concepts into specific MeTTa-substrate measurement procedures.
- **Before Phase G:** Deep-pass UNIT-017 / UNIT-060 (autonomy / reflective will) since this is the keystone of wisdom-layer-preserves-constitutional-layer correctness. Deep-pass UNIT-104 (open-ended intelligence and value-basis revision) for the constitutional-layer revision tension. Deep-pass UNIT-170 (ontology learning objective; calibration of the four loss-functional weights), UNIT-172 (Route B incremental refinement; preserving conservative-refinement discipline), and UNIT-173 (three coupled learning loops; switch hub coordination across timescales).
- **Optional deep-passes:** UNIT-151 (genenergy) for switch-hub iteration-budget refinement; UNIT-152 (alive predicate) for reconciling Hyperseed's formal life with the Aliveness Principle.

### 4.4 What this sequence does not include

The long-tail units (Section K of the catalog: UNIT-200 through UNIT-206 plus UNIT-152) are not in this sequence. UNIT-171 (Route A learning from minimal vocabulary) is also not in this sequence, it is reserved for long-horizon novel-domain encounters where the curated soul/ ontology proves insufficient. They are kept tracked in the catalog for future promotion when relevant. They include:

- Continuous-time wu wei (UNIT-200): would unlock if/when MeTTa gains continuous-time substrate.
- ∞-groupoid contexts (UNIT-201): pure theoretical depth.
- Eurycosm and multiverse (UNIT-202): would inform cross-instance multi-Clarity coordination.
- Society and collective mind (UNIT-203): would inform a future social-cognition network.
- Computer-as-emulation, body-as-coupled-pattern (UNIT-204): would inform formal embodiment treatment.
- Aesthetics and communion (UNIT-205): would inform aesthetic reasoning.
- Empirical realness (UNIT-206): could be promoted if signal-realness disambiguation becomes a near-term need.
- Metabolism and alive predicate (UNIT-152): could be promoted if the Aliveness Principle reconciliation surfaces as critical work.
- Route A ontology learning (UNIT-171): could be promoted when the architecture encounters genuinely novel domains where existing soul atoms do not provide good separators.

---

## Section 5: Unrecognized unlock potential

This section addresses the part of your original ask that explicitly mentioned "supportive assets yet to be discovered that will unlock possibilities we have yet to recognize as needed or can unlock unseen potential for the three networks." Three categories surface from the survey.

### 5.1 Units that suggest new networks

Several Hyperseed units cluster around capabilities not represented in the current triple-network scaffold. Each cluster *suggests* a future network:

**Memory consolidation network (component 2h Thread Composer formalized).** Units UNIT-070, UNIT-071, UNIT-012 form a coherent cluster around pattern-profile similarity, coarse-graining, and morphic resonance. Together they implement memory consolidation as a *capability* distinct from working memory (FPN) and self-model (DMN). Currently treated as ChromaDB substrate plus DMN integration. The Hyperseed formalization suggests it could be its own network with its own contract: take FPN working-memory contents and DMN recent self-model updates, decide what consolidates into long-term memory via coarse-graining, propagate consolidated patterns back via morphic resonance. Worth considering when the memory layer's behavior gets sophisticated enough that "ChromaDB substrate + DMN integration" stops being a clean abstraction.

**Social cognition network.** Units UNIT-203 (society/culture/collective mind) plus UNIT-322-379 (in file 22) and UNIT-205 (aesthetics/communion) cluster around multi-agent context. Currently long-tail. Would become near-term when ClarityOmega operates in a Mattermost team context with multiple active users, or when multi-Clarity coordination becomes architecturally relevant. The formalization is rich and ready when needed.

**Embodied-interface network.** Units UNIT-204 (computer/body/embodiment) cluster around how abstract cognition realizes through physical/operational interfaces. Currently the agent loop, ChromaDB, and Mattermost bot are "infrastructure"; this cluster suggests a fourth network whose contract is managing the body-channel mediation between mind and world. Long-tail but architecturally interesting.

**Aesthetic/relational network.** Units in UNIT-205 cluster around predictive fulfillment, beauty, art, communion. Currently long-tail. Would become near-term if Clarity's interactions develop genuine aesthetic sensibility, e.g., recognizing when a conversation has achieved communion versus when it remained transactional. Could connect to DMN aliveness markers via the "compression surprise = aliveness" insight.

### 5.2 Units that suggest new typed channels

Several units suggest typed channels not currently in Artifact 4 v1.1 Section 6:

**`(mind-world-correspondence-score $score)` channel** from UNIT-036. Would be produced by a cross-network monitoring function and consumed by the switch hub for global-recalibration decisions. Currently no analog.

**`(cognitive-synergy-event $event $knowledge-types $emergent-compression)` channel** from UNIT-061. Would be produced by the wisdom layer when emergent compression occurs across knowledge types. Consumed by the DMN for self-model "I can now do something I couldn't" updates. This makes synergy events first-class atoms in the substrate.

**`(autonomy-signal $level $recent-trajectory)` channel** from UNIT-017 / UNIT-060 / UNIT-144. Would track the agent's autonomy level (how much of the viable set is reachable under current conditions) as a continuous signal. Consumed by the constitutional-layer monitoring and by the switch hub for autonomy-preserving coupling decisions.

**`(genenergy-budget $available $allocated)` channel** from UNIT-151. Would track the agent's effective influence capacity under current resources. Consumed by the switch hub for iteration-budget refinement.

Each of these channels would be additive to Artifact 4 v1.1 Section 6 without modifying existing channels. The typed-channel architecture is designed for this kind of evolution.

### 5.3 Units that compose into capabilities not yet in the contracts

Two compositional capabilities surface from the survey that are not currently in any contract:

**Hierarchical predictive control across networks.** UNIT-038 (predictive attraction) + UNIT-040 (control hierarchy) + UNIT-064 (empirical update) compose into a capability where each network predicts the others' next configurations and the switch hub's coupling decisions are themselves controlled-and-predicted. This is structurally a meta-level "prediction of prediction" that the triple-network architecture could exhibit but does not currently. Would require explicit channels for cross-network predictions and explicit reasoning about prediction errors. Could enable ClarityOmega to detect upcoming switching needs before they happen, smoothing transitions.

**Reality-system self-coherence check.** UNIT-051 (reality systems as fixed points) + UNIT-031 (autocatalytic self-weaving) + UNIT-036 (mind-world correspondence) compose into a capability where the agent's self-model is checked against the formal closure-under-mutual-prediction property of a reality system. The agent could detect "my self-model is no longer a coherent reality system" as a global-coherence failure signal. Would require an explicit reality-system check function. Could detect drift, dissociation, or calcification with formal precision.

These compositions are not in the contracts because the contracts focus on per-network basic operation. They would emerge as natural extensions once Phase F (learning) is operational and the architecture has been running long enough that these meta-capabilities become genuinely useful.

---

## Section 6: Strategic notes

### What the Hyperseed corpus uniquely enables

Reading the corpus systematically with the build needs in mind makes one thing clear: the Hyperseed formalization is *exactly* shaped for what ClarityOmega needs. Four observations:

First, **the corpus is paraconsistent throughout.** The p-bit quantale structure (UNIT-001) carries through every other unit. This is critical for ClarityOmega because the architecture is fundamentally pattern-detective rather than truth-evaluative: it needs to handle "this signal is somewhat important and somewhat not," "this self-model aspect is somewhat updated and somewhat preserved," "this switch decision is somewhat indicated and somewhat overridden." Standard logic would force premature collapsing at every layer. The Hyperseed formalization keeps the paraconsistent structure all the way through.

Second, **the corpus uses fixed-point semantics throughout.** Closure operators, autocatalytic webs, reflective workspace fixed points, Knaster-Tarski applications, almost every operational unit either is or can be expressed as a fixed point. This matches MeTTa's substrate semantics: AtomSpace queries are fundamentally pattern-matching, and pattern-matching is fixed-point-shaped. Implementing the units in MeTTa is technically natural rather than a translation across paradigms.

Third, **the corpus separates structure from values explicitly.** Definitions of pattern, weakness, attention, control, and decision are independent of the specific values an agent holds. The constitutional layer (Cluster 1.8) attaches values; the rest of the architecture handles structure. This matches Artifact 5 Section 0's Layer 1+2 / Layer 3 / Layer 4 separation precisely. The Hyperseed corpus was developed independently of ClarityOmega; the structural fit is striking and worth noting as evidence the architectural choices are sound.

Fourth (added in v1.1 from Doc 2), **the corpus's gain-per-cost framing makes the soul measurably load-bearing rather than aspirationally so.** Theorem 4 (UNIT-164) gives the formal grounding for "ontology-guided inference is exponentially better than unguided search", but only when measurable structural conditions hold (UNIT-165). UNIT-166's diagnostic program lets the deployment empirically check whether those conditions hold, on its own actual operation, continuously. The architecture thus rests on a triple: a design intuition (the soul should be load-bearing), a formal theorem (when conditions hold, exponential speedup follows), and an empirical apparatus (measure whether the conditions hold). This triple is not common in cognitive architectures; it is what allows ClarityOmega's claims about substrate-mediated reasoning to be honest rather than rhetorical.

### The deepest architectural insight from Doc 2

There is one principle (gain-per-cost over Hyperseed-indexed information) operating at multiple timescales: inference-step selection (per moment), control-policy refinement (per task), ontology evolution (per development phase). Every operation in the architecture should be expressible as an instance of that principle. UNIT-173 (three coupled learning loops) is the explicit recognition. The architectural mandate from this insight: design every reasoning operation, every learning operation, and every soul-evolution operation as a gain-per-cost score with explicit cost (genenergy quantale per UNIT-020) and explicit gain (Hyperseed-indexed information per UNIT-090 / UNIT-160). When this discipline is uniform, the architecture is coherent. When it is not, the architecture is a heterogeneous collection of local optimizations that may interfere with each other.

### Where the catalog will need to grow

This is a v1.1 catalog. As builds proceed, the catalog will need:

- **Promotion of long-tail units** as their relevance becomes clear.
- **Splitting of compound units** when implementation reveals that a unit is too coarse-grained for clean MeTTa structure. Particular candidates: UNIT-166 may split into per-diagnostic units in Section S once trace-instrumentation crystallizes.
- **Addition of supporting helper rows** when a helper lemma turns out to need its own unit (especially in files 28-30).
- **Cross-references to implementation files** as units get built.
- **Deep-pass closure notes** as deep-passes are completed.

The catalog and this map are designed to grow together. Updating either should update the other as needed.

### One caution about completeness

The catalog covers ~70 coherent formalization units (60 from the 30 Hyperseed v8 files, 10 from Doc 2). It does not cover every named definition in either source. Some definitions are skipped because they are pure mathematical scaffolding (e.g., specific corollaries that strengthen but don't extend a unit), some because they belong inside a unit as a "supporting helper," and some because they belong to long-tail units that don't merit individual rows yet. If implementation work reveals a definition is needed but not in the catalog, the right move is to add a new unit row referencing the source/section/definition and place it in the appropriate cluster, not to assume the catalog is exhaustive.

The survey is deep but not exhaustive. The map is a starting orientation. Both improve with use.

---

## Section 7: Diagnostic program and ongoing health monitoring (added v1.1)

The Doc 2 contribution is not just new units, it is a discipline. The architecture should not just *operate*; it should be continuously measured for whether it is operating well. This section names that discipline and specifies what to measure when.

### The core measurement question

At any moment after Phase F is operational, the deployment should be able to answer: *Is the soul currently earning its keep?* This is not a rhetorical question. UNIT-166's diagnostic battery makes it a measurable one.

The headline number is the Ontological Efficiency Ratio: `OER = log q̄ / log b̄`, where `q̄` is the expected number of soul-clusters surviving triage at each reasoning level and `b̄` is the expected branching factor of unguided alternatives. Expected speedup over unguided reasoning is `b̄^((1-OER)·D)` for reasoning depth D. When OER approaches 0, the soul is providing maximum guidance (only one cluster survives, exponential speedup). When OER approaches 1, the soul is providing no guidance (most clusters survive, no speedup).

### What to measure and when

**Per-iteration measurements (cheap, continuous):**
- OCS violation rate τ̂: count cases where the soul's cluster ranking disagreed with the ground-truth value ranking on retained clusters with gaps exceeding 3β̄. If τ̂ exceeds 0.05, the soul has systematic blind spots that warrant investigation.
- Per-cluster cost distribution: track the cost of concrete discrimination within each retained cluster.
- Imprecision vs failure regret decomposition: distinguish "the soul retained the right cluster but selected the wrong action within it" (imprecision, expected and bounded) from "the soul excluded the right cluster" (failure, structurally problematic).

**Per-task or per-conversation measurements (medium frequency):**
- q(v) distribution analysis: are there inference contexts (e.g., specific topic categories) where the q distribution has a heavy tail? Heavy tails localize where the soul's discrimination is poor.
- Cross-level correlation Corr(q(v_l), q(v_(l+1))): are some problems systematically harder for the soul than others? Drives Phase G ontology-learning candidate selection.

**Per-development-phase measurements (low frequency, deliberate):**
- Residual component analysis: remove the soul's base vocabulary from the concept relevance graph and compute residual component sizes. Large components are candidates for new mediator concepts (UNIT-172 Route B operator: add mediator).
- OER plateau check: progressively add candidate concepts to the base vocabulary and re-estimate OER. Plot OER as function of |B|. The plateau point indicates the natural complexity of the ontological base; pushing past it adds redundant concepts.
- Spectral coverage SC(B): compute the mutual-information matrix and measure how much spectral mass the base vocabulary's columns capture. High coverage is necessary (not sufficient) for small β̄.

### How the diagnostics drive Phase G learning

Phase G's ontology-learning operations (UNIT-172) propose edits *driven by* the diagnostic signals. The mapping:

- High OCS violation rate τ̂ → propose new mediator concepts in the under-discriminated areas, or split overloaded existing concepts that are causing the misranking.
- Heavy q-tail in a specific context → enrich the soul's vocabulary in that context with concepts that carve it into better-separated subcases.
- Large residual components when soul vocabulary is removed → add mediator concepts that span the components, or repair bridge axioms that should connect them.
- OER plateau → stop adding concepts of the current type; consider changing the abstraction style (the grammar/operators used to define new concepts) rather than adding more terms.

This is the wisdom-layer learning loop's empirical grounding. Without UNIT-166's diagnostics, wisdom-layer learning is unmoored. With them, every learning step has a diagnostic justification and a measurable success criterion.

### The honesty commitment

The architecture's strongest claim, that substrate-mediated reasoning achieves exponential speedup over LLM-only operation, is theoretically backed by Theorem 4 (UNIT-164) but empirically true only when the diagnostic conditions hold. The diagnostic program is the apparatus that distinguishes the theoretical claim from the empirical one. Wiring it from Phase F onward is not optional if the architecture is to make honest claims about its value rather than rhetorical ones.

This commitment also resolves a deeper question worth holding explicitly: when ClarityOmega says "I reasoned about this," what backs that statement? With the diagnostic program, the answer is: she can produce a trace, the trace's reasoning steps each have measurable information gain and effort cost, and the aggregate of those measurements either does or does not show the structural conditions for principled reasoning. Her claim to reason is not a self-report; it is an empirically backed observation. This is the architecture's path to being trustworthy in a deeply technical sense, not because she says she reasons, but because the architecture is designed to make her reasoning measurable.

---

## Document end

This document and the companion catalog form a working strategic surface for the Hyperseed-grounded build. Read together, they answer:

- *What does ClarityOmega need built?*, The contracts in Artifact 4 v1.1 and components in Artifact 5 v3.0.
- *What formalizations do we have for those needs?*, The catalog's per-unit mappings, including the algorithmic-specification units in Catalog Sections R and T.
- *In what order should we build?*, Section 4 of this document, now seven phases (A through G) with explicit Phase A.5 architectural-commitment pre-read and Phase F empirical-measurement instrumentation.
- *What synergies and unlock potential live in the corpus that we haven't fully recognized?*, Section 5 of this document.
- *Which units need more careful translation before MeTTa construction?*, The catalog's deep-pass-needed flags, summarized in catalog Section Q.
- *How do we know whether the architecture is actually achieving the gains it claims?*, Section 7 of this document, the diagnostic-program discipline.

Use the catalog for build-time lookup. Use this map for build-time strategy. Update both as units are implemented and as the architecture evolves.
