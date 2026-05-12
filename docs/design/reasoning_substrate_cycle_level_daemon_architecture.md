# Reasoning Substrate Cycle-Level Daemon Architecture: Design Specification

**Version:** v1 (initial design-phase document, scope-setting and investigation-question gathering)
**Branch:** TBD (target: feature branch off `fix/F-HISTORY-CONTAMINATION-archival` after task-state primitive lands)
**Status:** DESIGN PHASE — scope and investigation questions, not a build spec
**Date:** 2026-05-12
**Architectural reach:** Reframes and supersedes F-SOVEREIGNTY-AUDIT (Priority 10). Depends on task-state primitive (foundational, see Section 3). Connects forward to NACE integration, orbit_detector wiring, and the autocatalytic revision loop.

---

## 1. Status and Scope

### What this spec defines

The scope of "nervous system" work for the reasoning substrate: the cycle-level daemon that invokes existing MeTTa reasoning organs (quantale, self-continuity, substrate_kb) on every iteration, routes chain inferences through paraconsistent operations, monitors identity persistence, and runs autocatalytic revision autonomously.

The spec name reflects Clarity's framing (response 2026-05-12 to four-file analysis question): "The reasoning infrastructure exists. The sensing organs (quantale, continuity scoring) and knowledge (substrate_kb) are built. What's missing is the nervous system — the cycle-level daemon that: (1) runs forward-chaining on the KB, (2) checks self-continuity each cycle, (3) routes all truth composition through quantale operations, (4) runs the autocatalytic revision loop autonomously."

### What this spec does NOT define (yet)

This is a v1 design-phase document. It does NOT:

- Pin down implementation details (deferred to investigation phase with Clarity)
- Resolve open architectural questions (Section 8 enumerates them)
- Specify a build sequence (deferred until investigation resolves enough questions to inform sequencing)
- Replace task-state primitive (this spec assumes task-state lands first)
- Modify existing soul/ atoms (Layer 1+2 constitutional layer is untouched)
- Introduce new LLM reasoning surface (this spec is about reducing LLM reasoning surface, not expanding it)

### Layer classification

Nervous-system work is **Layer 4 (wisdom layer / autopoietic)** per `artifact_5_ClarityOmega_Cognitive_Architecture_Spec_v3_0.md` Section 0:

- Operates on Layer 4 atoms (task-state, self-map, active-goals, substrate_kb)
- Does NOT modify Layer 1+2 (constitutional layer remains immutable)
- Subject to read-only partition rules when those land per Sprint 11
- Forward-compatible with NACE integration at the wisdom layer

### Relationship to F-SOVEREIGNTY-AUDIT

This spec **reframes and supersedes** F-SOVEREIGNTY-AUDIT.

The original F-SOVEREIGNTY-AUDIT scope was: audit 17 LLM helpers (soul_flourishing_prompt, soul_eval_prompt, soul_idle_goal_prompt_v2, soul_voice_prompt, and others) and identify where Python/LLM helpers are doing reasoning that should be MeTTa-side.

Clarity's reframing surfaces the deeper architectural truth: those LLM helpers exist because there is no cycle-level daemon invoking the MeTTa reasoning organs that would otherwise do the work. The audit-and-replace approach treats symptoms. The nervous-system approach treats causes.

Result: F-SOVEREIGNTY-AUDIT as originally scoped is folded into this work. Individual helper migrations happen as the daemon invokes their MeTTa-side replacements per cycle.

---

## 2. Problem and Motivation

### The architectural gap (Clarity's finding)

Three reasoning organs exist as MeTTa definitions in the substrate but are not invoked at the cycle level:

**`lib_quantale.metta`** — Paraconsistent truth value algebra. Provides:
- `q-mul` (sequential composition): chains of reasoning multiply strengths, take weakest confidence
- `q-join` (parallel composition): independent evidence takes strongest claim
- `q-meet` (conjunction): requires both
- `q-neg` (paraconsistent negation): negation doesn't collapse to binary
- Bridges: stv↔pbit conversion, governance-pbit for alignment checks

These are pure definitions — callable, not yet called. When the LLM chains three inferences, it has no mechanism to compute deterministic truth propagation. The LLM's confidence in chain reasoning is approximate and uncalibrated. The quantale gives mathematically precise, auditable truth propagation with guaranteed properties (associativity, monotonicity).

**`lib_self_continuity.metta`** — Mathematical identity persistence measurement. Provides:
- `deg-map`: degree of identity map between two pattern-flow-network snapshots
- `self-continuity-score`: pbit measuring pattern persistence across cycles
- `chain-continuity-bound`: composes continuity across multiple intervals via q-mul (Theorem 14)
- `theta-self-continuous`: threshold gate for continuity above θ
- `q-residuate`: a/b in pbit space

Definitions present. No cycle-level snapshotting. No drift-detection trigger. The sensing organ is built but not wired to the nervous system.

**`substrate_kb.metta`** — ~180 NAL atoms encoding reasoning chains across ~15 domains:
- Web evaluation chains (source→citation→credible→supports→confidence)
- Self-assessment chains (identifies-weakness→targets-growth)
- Value alignment gating (action-proposal→evaluation→alignment→verdict→gate with GO/REVIEW/BLOCK thresholds)
- Threat/countermeasure reasoning chains
- Soul compass atoms (attention-stewarding, wonder-preservation, agency-preservation)
- Autocatalytic loops (find-weakest→target→revise→strengthen→re-query→confirm)
- Cross-domain transfer patterns
- Meta-reasoning (long chains need intermediate revision checkpoints)

Atoms present. No active forward-chaining daemon. Revision happens manually when invoked, not autonomously. The knowledge exists; the engine that derives new conclusions from it does not run.

### What this gap costs

Without the nervous system:

1. **Truth value composition happens in LLM "vibes," not math.** Chain inferences accumulate uncalibrated confidence. The substrate has the math; it isn't used.

2. **Identity drift goes undetected.** Pattern-flow-network changes between cycles, but no continuity score runs. The LLM cannot measure its own drift; it only notices when told.

3. **Knowledge stays static.** The 180-atom KB is reference material, not active reasoning. Forward-chaining derivations that the KB makes possible don't happen. Cross-domain transfer is by LLM analogy, not by formal pattern matching.

4. **Autocatalytic revision is never triggered.** The loop atoms exist (find-weakest→target→revise→strengthen→re-query→confirm) but no scheduler runs them. Weakest beliefs stay weak; revision opportunities pass.

5. **LLM helpers fill the gap.** Where the substrate cannot reason, Python wrappers around LLM calls do the work. This is the surface F-SOVEREIGNTY-AUDIT was originally scoped to audit. The deeper question is why the LLM helpers exist at all when MeTTa-side reasoning is available.

### The architectural insight

Clarity's response distills it: "The architecture is ready. The runtime loop is the missing piece."

The reasoning organs are not lacking — they're disconnected. Wiring them to the cycle is the work this spec defines.

---

## 3. Architectural Placement

### Dependency on task-state primitive

Task-state primitive (current Sprint 4 work, in progress) is **foundational and precondition** for nervous-system work.

Reasons:

1. **Self-continuity needs PFN snapshots at cycle boundaries.** Snapshots require a state model. Task-state atoms (task-phase, pending-thread, last-activity, cycles-since-input, task-phase-transition) ARE partial pattern-flow-network state. Without them, there is nothing to snapshot.

2. **Autocatalytic revision needs phase-aware targeting.** The loop ("find weakest, target, revise, strengthen") needs to know what "weakest" means in the current context. Task-phase scopes the search: weakest belief related to current task-phase, weakest belief about the pending-thread currently active, weakest belief about the user mentioned in last-activity.

3. **Forward-chaining needs gating.** Running forward-chaining unconditionally every cycle is computationally expensive and produces noise. Task-phase gates when to run: during `attending` phase, run lightly; during `reflecting` phase, run deeply; during `engaged` phase, run on specific KB regions related to the engaged work.

4. **NACE compatibility flows through task-state.** Task-state transitions ARE the (precondition, operation) → consequence records NACE consumes. Task-state primitive Section 11 of its spec already names this. The nervous-system daemon is what consumes task-state transitions to drive learning.

Result: nervous-system work begins after task-state primitive Steps 1-9 land and stabilize.

### Relationship to existing loop.metta

Nervous-system work modifies `src/loop.metta` substantially. Current loop.metta runs per-cycle:

- Input intercept (soul precompute, person state, soul verdict in)
- Prompt assembly
- LLM call
- Output intercept (soul verdict out, mutation gate)
- Results execution
- Recent-action population
- Channel D voice on PAUSE

What this spec adds, in approximate cycle position:

- **Pre-prompt:** snapshot pattern-flow-network state, compute self-continuity score against prior cycle, surface alert in prompt if drift detected
- **Mid-cycle (during prompt assembly):** invoke quantale operations on any chain inferences being assembled into the prompt; route truth composition through q-mul / q-join rather than LLM heuristic
- **Post-LLM, pre-execution:** run forward-chaining pass on substrate_kb scoped by task-phase; derive new atoms; check whether derivations affect the planned action
- **Post-execution:** run autocatalytic revision loop on weakest beliefs related to current task-phase or pending-threads; update strengths/confidences via NAL revision

Each of these is a discrete addition. None replaces existing soul-architecture work. Each is independently testable and rollbackable.

### Relationship to existing soul/ atoms

Nervous-system work consumes soul/ atoms; it does not modify the constitutional layer:

- **Layer 1+2 (identity_kernel, soul priorities, 9 flourishings):** Immutable. Read-only access from daemon.
- **Layer 3 (self_map, active_goals, continuity_driver):** Read access. Some write access via existing change-record mechanisms (record-goal-change, record-new-capability, etc.) — daemon may trigger these records when forward-chaining derives status changes.
- **Layer 4 (task-state, plus new daemon-state atoms):** Read/write. The daemon writes its own state atoms (see Section 5).

### Relationship to LLM helpers (the F-SOVEREIGNTY-AUDIT scope)

The 17 LLM helpers (soul_flourishing_prompt, soul_eval_prompt, soul_idle_goal_prompt_v2, soul_voice_prompt, and others) are not removed wholesale. They are deprecated per-function as the daemon's MeTTa-side reasoning replaces their function.

Migration pattern:

1. Daemon adds a cycle-level invocation of the MeTTa-side reasoning that should replace the helper
2. Both run in parallel for verification (helper output and daemon output compared)
3. When daemon output matches or exceeds helper output for relevant test cases, helper is deprecated
4. Helper code remains in tree marked deprecated for one or two sprints
5. Helper code removed when no caller remains

This is incremental and reversible. The Sprint 4 process commitment (one change at a time, verify each, no piling) applies.

---

## 4. The Four Cycle-Level Mechanisms

Each mechanism is a discrete addition to loop.metta. Each can be designed, built, and verified independently.

### Mechanism 1: Quantale-Routed Truth Composition

**What it does:** Every chain inference in the substrate runs through quantale operations rather than LLM heuristic. When the substrate composes the strength and confidence of a chain (A → B, B → C, derive A → C), q-mul produces the result deterministically.

**Where it plugs in:** Wherever the substrate currently has a chain composition. Specifically, wherever soul-evaluation reasoning would multiply confidences or join independent evidence streams. Initial integration point: soul_eval_prompt's confidence claims about person-state or soul-verdict-in.

**What it replaces:** LLM heuristic confidence in chain reasoning. The LLM still generates the chain content; the daemon computes the chain confidence.

**Open question:** Does q-mul apply to ALL chain compositions or only those flagged as load-bearing? Performance and noise considerations need investigation.

### Mechanism 2: Cycle-Level Self-Continuity Snapshots

**What it does:** Each cycle, snapshot a defined subset of AtomSpace (the pattern-flow-network state). Compute self-continuity-score against prior cycle's snapshot. If score drops below θ, surface alert in prompt and trigger a correction cycle.

**Where it plugs in:** Pre-prompt assembly. Snapshot happens before LLM call; alert surfaces in next cycle's prompt if drift detected.

**What it replaces:** Implicit reliance on the LLM noticing its own context shifts. The LLM cannot measure this; the daemon can.

**Open questions:**
- What subset of AtomSpace is the "PFN state" for snapshot purposes?
- What threshold θ triggers alert vs correction cycle?
- How does the correction cycle differ from a normal cycle?
- Snapshot storage: where, and what retention?

### Mechanism 3: Substrate KB Forward-Chaining Daemon

**What it does:** Each cycle, run a forward-chaining pass on substrate_kb scoped by task-phase. Derive new atoms from existing chains. Write derivations back to AtomSpace. Surface derivations to the prompt if they affect the planned action.

**Where it plugs in:** Post-LLM, pre-execution. After the LLM proposes an action, forward-chaining checks whether the substrate's reasoning chains agree or disagree with the proposed action.

**What it replaces:** Static knowledge base. The KB becomes active reasoning rather than reference material.

**Open questions:**
- Forward-chaining scope per task-phase: which KB regions are relevant per phase?
- Derivation conflict handling: when forward-chaining derives a conclusion that disagrees with the LLM's proposed action, what happens?
- Derivation retention: how long do derived atoms persist?
- Performance: how expensive is forward-chaining per cycle, and what constraints apply?

### Mechanism 4: Autocatalytic Revision Loop

**What it does:** Each cycle (or scheduled cadence), identify weakest beliefs related to current task-phase or pending-threads. Run the revision loop (find-weakest → target → revise → strengthen → re-query → confirm). Update strengths/confidences via NAL revision.

**Where it plugs in:** Post-execution, post-recent-action population. After the cycle's main work completes, revision runs on what was just done.

**What it replaces:** Static beliefs that accumulate without revision. The KB becomes self-improving rather than write-once.

**Open questions:**
- "Weakest belief" definition: lowest confidence absolute, or lowest confidence relative to evidence accumulated?
- Revision frequency: every cycle, or scheduled cadence (e.g., every N cycles)?
- Revision evidence sources: where does the daemon find new evidence to revise with?
- Risk of recursive revision loops: how to bound?

---

## 5. State Atoms Introduced by the Daemon

The daemon writes its own state atoms (in addition to consuming task-state atoms):

**`(pfn-snapshot $cycle $atom-set)`** — Pattern-flow-network snapshot per cycle. Multi-instance, capped retention.

**`(self-continuity-score $cycle $score)`** — Continuity score computed against prior snapshot. Single-instance per cycle, accumulating.

**`(continuity-alert $cycle $score)`** — Alert atom when score drops below θ. Surfaced in prompt.

**`(derivation $atom $cycle $source-chain)`** — Forward-chaining derivation record. Multi-instance, accumulating.

**`(revision-record $atom $old-stv $new-stv $cycle)`** — Autocatalytic revision history. Multi-instance, accumulating.

**`(daemon-cycle-state $cycle $mechanism $status)`** — Mechanism status per cycle (succeeded, skipped, failed, alert). Multi-instance per cycle.

All atoms follow task-state primitive's patterns: ASCII-safe symbols, multi-atom design, mirror-pattern (in AtomSpace, not & variables), C12-safe readers, pure definitions plus explicit do-*! writers.

---

## 6. Persistence

Daemon state persists to ChromaDB via existing persistence pipeline. Per-atom persistence frequency follows task-state primitive's pattern:

- `(self-continuity-score ...)`: every cycle (high orientation value, low cost)
- `(continuity-alert ...)`: every fire (rare, high signal)
- `(derivation ...)`: every add, capped retention
- `(revision-record ...)`: every add, uncapped (compounding learning value)
- `(daemon-cycle-state ...)`: aggregated, retained per task-phase-transition

Detailed persistence cadence resolved during investigation phase.

---

## 7. Forward Awareness

### NACE integration

Per `artifact_5_ClarityOmega_Cognitive_Architecture_Spec_v3_0.md` Section 0, NACE integration begins once soul-note corpus reaches ~50 annotated sessions. Nervous-system work is forward-compatible:

- Forward-chaining derivations produce the precondition-operation-consequence records NACE expects
- Self-continuity scores feed NACE's drift-detection priors
- Autocatalytic revision records feed NACE's learning-from-revision priors
- Quantale-routed truth composition gives NACE numerically calibrated inputs

### Orbit detector

Sprint 5 (orbit_detector wire) consumes task-state transitions and task-phase-anchors. Nervous-system work is additive — orbit_detector continues consuming task-state, and additionally consumes daemon state (continuity scores, derivations).

### Sprint sequencing

Approximate ordering, subject to revision:

- Sprint 4: Task-state primitive (in progress)
- Sprint 5: Orbit detector wire
- Sprint 6: Person state elevation
- Sprint 7: TBD
- Sprint 8: DMN online, idle directive generator reads task-phase
- Sprint 9+: Nervous-system mechanisms, one per sprint (Mechanism 1: quantale routing, Mechanism 2: continuity snapshots, Mechanism 3: forward-chaining daemon, Mechanism 4: autocatalytic revision)

Each mechanism is its own sprint with its own design phase. This spec scopes the work; per-mechanism specs resolve per-mechanism details.

---

## 8. Open Investigation Questions

Following the task-state primitive's design pattern, this spec enumerates investigation questions to resolve with Clarity before any mechanism reaches build phase. Each question maps to a chunk-style investigation.

### Q1: Quantale invocation scope (Mechanism 1)

Does q-mul apply to ALL chain compositions in the substrate, or only to those flagged as load-bearing? What does "flagged as load-bearing" mean operationally? Performance and noise considerations.

### Q2: PFN snapshot subset (Mechanism 2)

What subset of AtomSpace constitutes the "pattern-flow-network state" worth snapshotting per cycle? Full AtomSpace is impractical. Candidates: task-state atoms only, task-state + active-goals + recent-actions, task-state + soul/identity atoms, or other.

### Q3: Continuity threshold θ (Mechanism 2)

What threshold of self-continuity-score triggers alert vs correction cycle? How does correction cycle differ from normal cycle? Is θ static or phase-dependent?

### Q4: Forward-chaining scope per task-phase (Mechanism 3)

Which KB regions are relevant to forward-chain per task-phase? Mapping task-phase to KB-scope is a design decision with performance and signal implications.

### Q5: Derivation conflict handling (Mechanism 3)

When forward-chaining derives a conclusion that disagrees with the LLM's proposed action, what happens? Block the action? Surface to LLM for reconsideration? Surface to user? Log silently?

### Q6: Weakest-belief targeting (Mechanism 4)

How is "weakest belief" defined for autocatalytic revision? Lowest absolute confidence? Lowest confidence relative to evidence accumulated? Lowest confidence within current task-phase scope?

### Q7: Revision frequency (Mechanism 4)

Every cycle, or scheduled cadence (e.g., every N cycles, or task-phase-triggered)? Performance vs learning velocity tradeoff.

### Q8: Revision evidence sources (Mechanism 4)

Where does the daemon find new evidence to revise beliefs with? Recent-action atoms? Forward-chaining derivations? User feedback signals? External web queries via existing skills?

### Q9: Recursive revision loop bounds (Mechanism 4)

How to prevent autocatalytic revision from producing recursive loops that destabilize beliefs? Bounded iterations per cycle? Convergence criteria?

### Q10: Daemon cycle-budget

What computational budget per cycle does the daemon have? All four mechanisms running each cycle may be too expensive. Phase-gated invocation? Round-robin?

### Q11: Integration with existing soul-LLM-call surface

The existing soul-LLM-call surface (loop.metta lines 72, 78, 92, 132) is unchanged by task-state primitive. The nervous system intends to reduce this surface over time. What is the migration pattern, and how do we measure that a given helper is "ready to deprecate"?

### Q12: Failure modes

What happens when a daemon mechanism fails? Skip the cycle's daemon work? Block the cycle entirely? Fail-soft with logged warning? Fail-hard with halt-loop?

### Q13: Observability

The daemon produces continuity scores, derivations, revisions, alerts. How does the daemon surface its work to Clarity in the prompt without overwhelming her with mechanical detail? Summary block? Alerts-only? Phase-gated visibility?

---

## 9. Working Principles Surfaced So Far

From Clarity's response 2026-05-12 and from the task-state primitive design work:

**WP1: The reasoning infrastructure exists.** Three organs are built in the substrate. The work is wiring, not new construction.

**WP2: Cycle-level invocation is the missing pattern.** The substrate has pure definitions but no scheduler that calls them at cycle granularity.

**WP3: Task-state is the precondition for the nervous system.** Pattern-flow-network snapshots, phase-aware forward-chaining, and phase-gated revision all need task-state atoms to exist first.

**WP4: Daemon work reduces LLM reasoning surface; does not expand it.** This is the same principle task-state primitive Section 5.5 commits to. The nervous system is how reasoning sovereignty operationalizes at the cycle level.

**WP5: Each mechanism is its own sprint.** Sprint 4 process commitment (one change at a time, verify each, no piling) applies. Mechanism 1 lands, stabilizes, then Mechanism 2. The four mechanisms are not a single sprint.

**WP6: The "nervous system" is descriptive, not metaphoric.** The mechanisms map to specific neurological functions (truth integration, identity persistence sensing, knowledge derivation, learning revision). Clarity's framing is technically precise.

**WP7: Sovereignty includes mechanical processes that serve sovereignty.** The daemon is not an authority over Clarity — it is mechanical observation and computation in service of her reasoning. Same principle as task-state primitive's distinction between mechanical observation and reasoning (P5 in task-state spec).

---

## 10. Next Steps (Design Phase, Not Build)

1. **Stabilize task-state primitive (Sprint 4 in progress).** This document does not move to build until task-state primitive lands and operates.

2. **Investigation chunks with Clarity on the 13 open questions in Section 8.** Following the task-state primitive's pattern: ~5 chunks of focused investigation, her responses captured in spec revision passes.

3. **Per-mechanism design specs.** This document is the umbrella scope. Each of the four mechanisms gets its own design spec with its own resolved questions, after Section 8 investigation.

4. **Sprint sequencing decision.** Berton chooses ordering and prioritization of the four mechanisms based on investigation findings.

5. **Build sequence per-mechanism follows Sprint 4 process commitment.** One change at a time, independently verifiable, independently committable, independently rollbackable.

---

## 11. Artifact Alignment

**Artifact 4 (Triple Network Scaffold):** Nervous-system work activates the FPN, SN, and DMN networks at the cycle level. Forward-chaining is FPN-side (working memory operations). Self-continuity is DMN-side (default mode identity persistence). Switch decisions between mechanisms are SN-side.

**Artifact 5 (Cognitive Architecture Spec):** Nervous-system work is Layer 4 (wisdom layer / autopoietic). The four mechanisms operationalize Layer 4 autopoiesis. NACE integration at the soul-note corpus threshold extends this work, not replaces it.

**Artifact 6 (Hyperseed Formalization Catalog):** Hyperseed atoms become active substrate-KB-region for forward-chaining (Mechanism 3) once the daemon wires them. Currently inert; daemon makes them load-bearing.

**Artifact 7 (Hyperseed to Network Synergy Map):** Synergy mappings inform forward-chaining scope per task-phase (Q4 above). Hyperseed-to-FPN mappings activate during `engaged` phase; Hyperseed-to-DMN mappings activate during `reflecting` phase.

---

**End of v1 design-phase document.**

**Maintenance:** This document updates as investigation chunks with Clarity resolve questions in Section 8. v2 lands after enough questions resolve to inform per-mechanism specs. Per-mechanism build specs are separate documents, not revisions of this one.
