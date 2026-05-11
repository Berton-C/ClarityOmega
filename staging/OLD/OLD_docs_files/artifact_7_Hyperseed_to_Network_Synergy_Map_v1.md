# Hyperseed-to-Network Synergy Map v1

**Version:** v1 (May 1, 2026)
**Author:** Berton Bennett with Claude
**Status:** Analytical companion to `Hyperseed_Formalization_Catalog_v1.md`. Maps Coherent Formalization Units (CFUs) into compositional clusters, dependency chains, per-network synergy summaries, and build-sequence recommendations grounded in unit prerequisites.
**Purpose:** Provide the strategic layer the catalog itself does not give: which units compose into which capabilities, what builds what, where the unrecognized unlock potential sits, and in what order to wire networks for maximum compounding return.

---

## How this document complements the catalog

The catalog (`Hyperseed_Formalization_Catalog_v1.md`) is a lookup tool: given a network or contract sub-function, find the units that implement it. This document is a strategy tool: given the goal of bringing the network architecture online with maximum coherence and minimum wasted effort, find the optimal clusters, sequences, and synergies.

Where the catalog is row-based (one unit per row, fields per row), this document is cluster-based (one cluster per section, units composed within each section). Both reference the same units by ID.

Use this document when planning a build session, evaluating a strategic move, or considering whether a long-tail unit deserves promotion. Use the catalog when actually building.

---

## Section 1: The compositional clusters

Coherent formalization units are not independent. They compose into capability clusters — sets of units that together implement one architectural capacity. This section identifies the major clusters, names what each enables, and lists the units composing it.

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

**Build implication:** Builds on Cluster 1.5 for the self-model substrate. Provides the formal grounding for narrative threads as more than "lists of events" — they are coherence-weighted resonance structures across time.

### Cluster 1.10: The cross-domain transport core (advanced DMN)

**Units:** UNIT-012 (morphic resonance), UNIT-070 (pattern profile/pseudo-metric), UNIT-071 (resolution maps/coarse-graining).

**What it enables:** Cross-domain integration in the DMN: insights from one domain (project) propagating to another via morphic resonance, with coarse-graining managing memory consolidation.

**Composition:** UNIT-012 propagates pattern support across contexts. UNIT-070 measures pattern-profile similarity between domains. UNIT-071 enables the consolidation operation that compresses recent experience into longer-horizon memory.

**Dependencies:** Cluster 1.1, Cluster 1.5.

**Build implication:** Important advanced cluster. Realizes component 2e Genesis Engine's "cross-domain encounters" capability formally. Also the foundation for component 2h Thread Composer if that grows into its own memory-consolidation network.

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

Long-tail (separate planning):
    UNIT-200, 201, 202, 203, 204, 205, 206, 152
```

### What this graph reveals

Three observations from the graph that matter for build sequencing:

First, **the substrate algebra (Level 0) blocks everything.** All four units must be in MeTTa before any cluster can be built. There is no way to short-cut this. Conversely, *once* Level 0 is built, the parallelism opens dramatically: many Level 1 units can be built independently.

Second, **Cluster 1.5 (DMN self-model core) is independent of Clusters 1.2-1.4.** It depends only on Level 0. This means DMN self-model construction can proceed in parallel with SN salience-tagging construction. They share substrate but not other units. Worth scheduling parallel builds when capacity allows.

Third, **Cluster 1.7 (wisdom-layer learning) is the convergence point.** It depends on Clusters 1.2-1.6 being operational. Until the network operational cores exist, learning has nothing to learn over. This means the architecture proceeds in two phases: (Phase A) build the network cores; (Phase B) wire the learning. The phase boundary is a natural validation point: at the end of Phase A, the architecture is operational but static; at the end of Phase B, it is operational and growing.

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

**Synergistic effect:** With these units, the SN can take an incoming signal, recognize patterns in it (UNIT-011, UNIT-027), compute its weakness against priority structure (UNIT-010), tag it with affective tone (UNIT-100, UNIT-101), express the tag as a soggy predicate (UNIT-122), and propose a switch decision (UNIT-015, UNIT-080) — then learn from the consequence of the tag via empirical update (UNIT-064) measured against KL divergence between predicted and actual outcomes (UNIT-090). The salience-tagging is grounded in distinction/weakness, the switching is grounded in fixed-point integration, and the learning is grounded in empirical update over weighted inference rules.

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

---

## Section 4: Build sequence recommendations

This section translates the dependency graph and cluster compositions into concrete recommendations for sequencing work.

### 4.1 The macro-sequence (six phases)

**Phase A — Substrate algebra (Cluster 1.1).** Build UNIT-001, UNIT-002, UNIT-005, UNIT-021 in MeTTa as foundational libraries. Validate by re-implementing one small existing soul/ atom (e.g., a hierarchy check) using only the new substrate. Expected effort: focused work session, possibly two. Validation criterion: existing soul atoms can be ported to use the new algebra without semantic change.

**Phase B — SN salience-tagging core + constitutional grounding (Clusters 1.2 + 1.8).** Build the SN's salience tagging in parallel with formalizing the constitutional layer's read-only grounding. The dependencies overlap (UNIT-100 in both clusters) so building together is efficient. Validation criterion: the SN can produce salience-tag atoms for incoming signals that match the verdict-quality of current LLM Channels A/B+C, with the tagging derived from priority structure rather than LLM emergence.

**Phase C — Switch hub (Cluster 1.3).** Build the switch hub as the consumer of SN salience tags. The aliveness-gate evolves into the four-state switch hub. Validation criterion: switch decisions are derivable from current state plus salience inputs via fixed-point computation, with correct debounce and orbit detection behavior over test traces.

**Phase D — DMN self-model (Cluster 1.5) and DMN goal-generation (Cluster 1.6) in parallel with FPN executor (Cluster 1.4).** These three clusters can proceed in parallel because they share only Phase A as common prerequisite. The DMN clusters together implement the highest-impact reasoning displacement identified in Artifact 1 Section 4.2 line 92 (the idle directive elevation). The FPN cluster brings task selection under substrate control. Validation criteria: DMN produces goal-candidate atoms traceable to gap+fuel sources; FPN selects tasks via resonant feasible choice rather than LLM emergence; aliveness markers are generated on surprise events.

**Phase E — Narrative coherence (Cluster 1.9) and cross-domain transport (Cluster 1.10).** Refines the DMN. Once these are in place, the DMN's three sophisticated sub-functions (narrative threading with coherence scoring, cross-domain integration via morphic resonance, memory consolidation via coarse-graining) come online. Validation criterion: narrative threads persist across iterations with coherence scoring reflecting actual event resonance; cross-domain insight transfer is observable.

**Phase F — Wisdom-layer learning (Cluster 1.7) across all networks.** Wires NACE-style empirical update into each network's truth-value rules. The architecture transitions from "operating networks" to "operating networks that learn." Validation criterion: per-network truth values demonstrably refine over time as consequence evidence accumulates, with the constitutional layer remaining read-only.

### 4.2 Phase-internal sequencing

Within each phase, the suggested order:

**Phase A:** UNIT-001 first (everything depends on it). Then UNIT-002 and UNIT-021 in parallel. Then UNIT-005.

**Phase B:** UNIT-100 first (it appears in both Clusters 1.2 and 1.8, and is foundational for the affective layer). Then UNIT-011 and UNIT-027 in parallel. Then UNIT-010 and UNIT-122 in parallel. Then UNIT-101, UNIT-102, UNIT-105 (constitutional grounding).

**Phase C:** UNIT-080, UNIT-081 first (cheap; no Hyperseed prereqs beyond UNIT-001). Then UNIT-015. Then UNIT-016. Then UNIT-050. Then integrate.

**Phase D:** Best as three parallel tracks.
- DMN self-model track: UNIT-030 → UNIT-031 → UNIT-032 → UNIT-034 → UNIT-037.
- DMN goal-generation track: UNIT-038 → UNIT-039 → UNIT-090 → UNIT-110 → UNIT-112 → UNIT-113.
- FPN track: UNIT-141 → UNIT-020 → UNIT-022 → UNIT-024 → UNIT-023 → UNIT-040 → UNIT-103.

**Phase E:** UNIT-004 → UNIT-013 → UNIT-026 (Cluster 1.9). In parallel: UNIT-070 → UNIT-071 → UNIT-012 (Cluster 1.10).

**Phase F:** UNIT-130 first (categorize knowledge). Then UNIT-140 (rule formalism). Then UNIT-062 (coherence). Then UNIT-064 (empirical update). Then UNIT-061 (synergy). Then UNIT-060 + UNIT-017 (autonomy preservation).

### 4.3 Where deep-pass work fits in the sequence

Several units have `Deep-pass needed: True`. The deep-pass should be done before the unit is implemented in MeTTa, but does not block the phase the unit belongs to (other units in the phase can proceed in parallel with the deep-pass). Recommended deep-pass scheduling:

- Before Phase B: Deep-pass UNIT-101 (emotion) and UNIT-105 (categorical imperative) since they are constitutional-layer units.
- Before Phase D: Deep-pass UNIT-033 / UNIT-061 (cognitive synergy) since this affects DMN goal-generation design. Deep-pass UNIT-052 (KL-control) before FPN learning if KL-control is the chosen formalism for FPN action proposal.
- Before Phase F: Deep-pass UNIT-017 / UNIT-060 (autonomy / reflective will) since this is the keystone of wisdom-layer-preserves-constitutional-layer correctness. Deep-pass UNIT-104 (open-ended intelligence and value-basis revision) for the constitutional-layer revision tension.
- Optional deep-pass UNIT-151 (genenergy) for switch-hub iteration-budget refinement; UNIT-152 (alive predicate) for reconciling Hyperseed's formal life with the Aliveness Principle.

### 4.4 What this sequence does not include

The long-tail units (Section K of the catalog: UNIT-200 through UNIT-206 plus UNIT-152) are not in this sequence. They are kept tracked in the catalog for future promotion when relevant. They include:

- Continuous-time wu wei (UNIT-200): would unlock if/when MeTTa gains continuous-time substrate.
- ∞-groupoid contexts (UNIT-201): pure theoretical depth.
- Eurycosm and multiverse (UNIT-202): would inform cross-instance multi-Clarity coordination.
- Society and collective mind (UNIT-203): would inform a future social-cognition network.
- Computer-as-emulation, body-as-coupled-pattern (UNIT-204): would inform formal embodiment treatment.
- Aesthetics and communion (UNIT-205): would inform aesthetic reasoning.
- Empirical realness (UNIT-206): could be promoted if signal-realness disambiguation becomes a near-term need.
- Metabolism and alive predicate (UNIT-152): could be promoted if the Aliveness Principle reconciliation surfaces as critical work.

---

## Section 5: Unrecognized unlock potential

This section addresses the part of your original ask that explicitly mentioned "supportive assets yet to be discovered that will unlock possibilities we have yet to recognize as needed or can unlock unseen potential for the three networks." Three categories surface from the survey.

### 5.1 Units that suggest new networks

Several Hyperseed units cluster around capabilities not represented in the current triple-network scaffold. Each cluster *suggests* a future network:

**Memory consolidation network (component 2h Thread Composer formalized).** Units UNIT-070, UNIT-071, UNIT-012 form a coherent cluster around pattern-profile similarity, coarse-graining, and morphic resonance. Together they implement memory consolidation as a *capability* distinct from working memory (FPN) and self-model (DMN). Currently treated as ChromaDB substrate plus DMN integration. The Hyperseed formalization suggests it could be its own network with its own contract: take FPN working-memory contents and DMN recent self-model updates, decide what consolidates into long-term memory via coarse-graining, propagate consolidated patterns back via morphic resonance. Worth considering when the memory layer's behavior gets sophisticated enough that "ChromaDB substrate + DMN integration" stops being a clean abstraction.

**Social cognition network.** Units UNIT-203 (society/culture/collective mind) plus UNIT-322-379 (in file 22) and UNIT-205 (aesthetics/communion) cluster around multi-agent context. Currently long-tail. Would become near-term when ClarityOmega operates in a Mattermost team context with multiple active users, or when multi-Clarity coordination becomes architecturally relevant. The formalization is rich and ready when needed.

**Embodied-interface network.** Units UNIT-204 (computer/body/embodiment) cluster around how abstract cognition realizes through physical/operational interfaces. Currently the agent loop, ChromaDB, and Mattermost bot are "infrastructure"; this cluster suggests a fourth network whose contract is managing the body-channel mediation between mind and world. Long-tail but architecturally interesting.

**Aesthetic/relational network.** Units in UNIT-205 cluster around predictive fulfillment, beauty, art, communion. Currently long-tail. Would become near-term if Clarity's interactions develop genuine aesthetic sensibility — e.g., recognizing when a conversation has achieved communion versus when it remained transactional. Could connect to DMN aliveness markers via the "compression surprise = aliveness" insight.

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

Reading the corpus systematically with the build needs in mind makes one thing clear: the Hyperseed formalization is *exactly* shaped for what ClarityOmega needs. Three observations:

First, **the corpus is paraconsistent throughout.** The p-bit quantale structure (UNIT-001) carries through every other unit. This is critical for ClarityOmega because the architecture is fundamentally pattern-detective rather than truth-evaluative: it needs to handle "this signal is somewhat important and somewhat not," "this self-model aspect is somewhat updated and somewhat preserved," "this switch decision is somewhat indicated and somewhat overridden." Standard logic would force premature collapsing at every layer. The Hyperseed formalization keeps the paraconsistent structure all the way through.

Second, **the corpus uses fixed-point semantics throughout.** Closure operators, autocatalytic webs, reflective workspace fixed points, Knaster-Tarski applications — almost every operational unit either is or can be expressed as a fixed point. This matches MeTTa's substrate semantics: AtomSpace queries are fundamentally pattern-matching, and pattern-matching is fixed-point-shaped. Implementing the units in MeTTa is technically natural rather than a translation across paradigms.

Third, **the corpus separates structure from values explicitly.** Definitions of pattern, weakness, attention, control, and decision are independent of the specific values an agent holds. The constitutional layer (Cluster 1.8) attaches values; the rest of the architecture handles structure. This matches Artifact 5 Section 0's Layer 1+2 / Layer 3 / Layer 4 separation precisely. The Hyperseed corpus was developed independently of ClarityOmega; the structural fit is striking and worth noting as evidence the architectural choices are sound.

### Where the catalog will need to grow

This is a v1 first-pass catalog. As builds proceed, the catalog will need:

- **Promotion of long-tail units** as their relevance becomes clear.
- **Splitting of compound units** when implementation reveals that a unit is too coarse-grained for clean MeTTa structure.
- **Addition of supporting helper rows** when a helper lemma turns out to need its own unit (especially in files 28-30).
- **Cross-references to implementation files** as units get built.
- **Deep-pass closure notes** as deep-passes are completed.

The catalog and this map are designed to grow together. Updating either should update the other as needed.

### One caution about completeness

The catalog covers ~60 coherent formalization units. It does not cover every named definition in the corpus. Some definitions are skipped because they are pure mathematical scaffolding (e.g., specific corollaries that strengthen but don't extend a unit), some because they belong inside a unit as a "supporting helper," and some because they belong to long-tail units that don't merit individual rows yet. If implementation work reveals a definition is needed but not in the catalog, the right move is to add a new unit row referencing the file/section/definition and place it in the appropriate cluster — not to assume the catalog is exhaustive.

The survey is deep but not exhaustive. The map is a starting orientation. Both improve with use.

---

## Document end

This document and the companion catalog form a working strategic surface for the Hyperseed-grounded build. Read together, they answer:

- *What does ClarityOmega need built?* — The contracts in Artifact 4 v1.1 and components in Artifact 5 v3.0.
- *What formalizations do we have for those needs?* — The catalog's per-unit mappings.
- *In what order should we build?* — Section 4 of this document.
- *What synergies and unlock potential live in the corpus that we haven't fully recognized?* — Section 5 of this document.
- *Which units need more careful translation before MeTTa construction?* — The catalog's deep-pass-needed flags, summarized in catalog Section Q.

Use the catalog for build-time lookup. Use this map for build-time strategy. Update both as units are implemented and as the architecture evolves.
