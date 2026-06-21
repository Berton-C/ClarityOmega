# Sprint 0-Coda Phase A: skill-discovery as First Production Capability

**Version:** v6
**Date:** 2026-05-26
**Author:** Berton Bennett (ClarityDAO), with Clarity (substrate co-author and Path C author), with Claude (drafting partner)
**Branch:** fix/F-HISTORY-CONTAMINATION-archival
**HEAD at draft time:** f37aa6c (Phase 1 memory-layer merge from patham9/mettaclaw upstream)
**Predecessor:** sprint_0_coda_phase_a_v5.md (marked FINAL prematurely; Clarity's layer-gap analysis and Path C draft surfaced architectural incompleteness; reshaped in v6); sprint_0_coda_phase_a_v4.md (v3.3 consistency check integrated); sprint_0_coda_phase_a_v3.md (Clarity 12-point review integrated, operational drift checks); sprint_0_coda_phase_a_v2.md (pipes/flows/meta-awareness lens applied); sprint_0_coda_phase_a_v1.md (initial draft, 2026-05-24); sprint_0_phase_1_design_v3_3.md (Sprint 0 Phase 1 close, ADR-006, ADR-007 — read in full for v4 consistency check); soul/capability_registry.metta Path C draft (Clarity 2026-05-26 — substrate reshape implementation)
**Status:** DESIGN PHASE A v6, iteration-from-here. v5 marked FINAL was premature; the pipe was not yet shaped to fit the water Clarity surfaced in her layer-gap analysis. v6 reshapes the pipe to carry the four modifications: filter-step generalization (Path C), success-criterion schema field, general external-observation atom shape, aggregation reserved.

---

## 0. Organizing principle: pipes, flows, and meta-awareness

This document is not a list of architectural decisions. It is an instance of a structural law that recurs fractally at every scale in ClarityOmega. Naming the law before the rest of the document makes the document self-aware of its own structure.

### The core principle

Pipes (structural containers) and flows (what moves through them) form a unified whole. Each validates the other's function.

- A pipe without flow is unvalidated structure. It exists, but its operation cannot be confirmed.
- Flow without a pipe is unstructured movement. It moves, but it has no reliable shape or destination.

This is not metaphor. It is a structural law. Every architectural surface in ClarityOmega is either a pipe, a flow, or a translation boundary between pipes of incompatible representation.

### The fractal recurrence

The same pipe/flow pattern occurs at every scale:

- Soul intercept chain → soul evaluations (pipe → flow)
- Capability registry → dispatches (pipe → flow)
- Individual handler → request-to-result transformation (pipe → flow)
- getContext → prompt assembly (pipe → flow)
- LLM → token generation (pipe → flow)

Same shape at every scale. Same truth at every scale. This is fractal alignment.

### The fractal consequence

Because the pattern is fractal, two properties hold simultaneously:

1. If one primitive is correctly instantiated, correctness propagates. A correct pipe/flow separation at one level validates the same separation at every other level.
2. If one primitive is incorrectly instantiated, wrongness propagates. A misshapen instance of the pattern at one level replicates the error at every scale.

**The propagation requires correct instantiation, not just correct principle.** A correctly-shaped pipe that carries poisoned flow propagates the poisoning; a misshapen pipe that carries correct flow fails at its own boundary. Both the shape and the substance must be right simultaneously. Phase D verification checks that the pattern was correctly instantiated, not just that the abstract principle was named.

Design decisions in Sprint 0-Coda are not local. They are instances of the same structural principle that governs the entire system. Get the capability registry's pipe/flow separation right (correctly instantiated), and the same correctness propagates to soul chain, handler, getContext, and LLM levels. Get it wrong (misshapen instance), and the same defect propagates.

### Meta-awareness as a privileged property of the system

Meta-awareness is the system becoming able to inspect what it is and what it can do, not as procedural code but as visible, queryable data.

Already in the architecture:

- `(registered-capability ...)` atoms make capabilities visible as data: the system knows what it can do
- `DIAG-CYCLE-*` diagnostic prints make cycle state visible: the system reports on its own operation
- Lifecycle values (`active`, `deprecated`, `suspended`, `pending-replacement`) track evolution over time: temporal meta-awareness
- `self_map.metta` makes the system's own loop structure inspectable

Representation-space gaps are where meta-awareness is incomplete. One pipe's output cannot be read by another pipe because the representations are incompatible. Full meta-awareness requires flow translation, so every pipe can read every other pipe's output.

**Governance flow as privileged subset.** Within meta-awareness, governance visibility is privileged over informational visibility. The soul intercept chain does not just produce informational flow that the registry reads as context. It produces governance flow: the soul verdict determines whether dispatch should proceed at all. A registry that cannot see soul verdicts is operating with a governance deficit, not merely incomplete self-knowledge.

**This is not an arbitrary scheduling preference; it follows from the soul hierarchy.** Governance flow translation failure creates a Safety-tier deficit (the registry could dispatch against a soul verdict it cannot see), whereas informational flow translation failure creates a Governance- or Helpfulness-tier deficit (the registry operates with incomplete but not safety-violating knowledge). The priority ordering for closing flow translation boundaries flows directly from the soul priority hierarchy (Safety > Integrity > HumanFlourishing > Governance > Helpfulness).

### Vocabulary: intention erosion and governance flow privilege

v3.3 (the Phase 1 specification this design extends) names "intention erosion" as the central failure class addressed by mechanical commitments. v4 names "governance flow privilege" as why mechanical commitments around soul verdicts carry highest priority. The two vocabularies cohabit and describe related-but-distinct concerns:

- **Intention erosion (v3.3 Section 4.7)** is the failure mode: a prior step records an intention, a subsequent step fails to consult it under load, the system acts as if the intention did not exist, no error signal fires. Mechanical commitments (decision anchors, bind-then-act, single-pass dispatch) prevent intention erosion by making the consultation structural rather than cognitive.

- **Governance flow privilege (Section 0, v4)** is the priority ordering: of all the intentions the system records, soul verdicts carry the highest weight because their erosion is a Safety-tier failure. Mechanical commitments around soul verdicts therefore carry the highest priority for closing flow translation boundaries.

Neither vocabulary replaces the other. v3.3 establishes the failure class; v4 establishes the priority within it. v3.3's mechanical-commitment framework is what governance-flow privilege calls on when ranking flow translation work.

### The drift tendency (critical warning)

There is a systematic error tendency: treating infrastructure (pipes) as primary and substance (flows) as secondary, optimizing pipes while forgetting what flows through them.

This error is self-replicating because structural analysis generates more structural analysis. Build a pipe, build a test for the pipe, build a monitor for the test, never ask whether the right thing is flowing through any of it.

The corrective check, applied at every design and verification step:

1. Does this preserve the loop shape? (Fractal alignment, structural integrity)
2. Does this preserve the world knowledge without distortion? (Pipes-and-water, semantic integrity)

Both are necessary. Neither is sufficient.

**This check is applied operationally in v3.** Each subsequent section ends with an explicit drift check that names how both properties are preserved within that section's design. The warning is not a preamble to nod at; it is an enforcement structure embedded in the document.

### The memory criterion

Memories are precious if they impart meaning and from them the system learns world knowledge. Flat data recordings are not knowledge. Store what changes future reasoning, not what merely happened.

Applied to this document: each section must convey world knowledge that changes how future work reasons. Sections that merely record what was built do not carry their weight.

### Application to the rest of this document

Sections 2 through 13 are instances of the principle stated here. Section 2 frames the two-dispatcher architecture as two pipes with asymmetric flow direction and two flow translation boundaries (one resolved, one unresolved). Section 5 frames the skill-discovery handler as a pipe receiving and emitting flow. Section 8 frames verification as pipe-exists-and-carries-correct-flow checks. Section 10 frames forward-compatibility commitments as pipe-evolution-while-maintaining-flow-compatibility. The fractal recurrence means design decisions made in this document propagate.

ADR-009 will extract this principle at Sprint 0-Coda close-out as the Substrate Fractal Invariant. ADR-007 (existing) is one specific application. ADR-008 (forthcoming) is the two-dispatcher consequence.

---

## 1. Sprint 0-Coda framing

Sprint 0 Phase 1 per Map v3 Section 9 scoped two deliverables together: "Core dispatcher + first capability registered through it." What actually shipped at Sprint 0 close was the dispatcher only. The first registered capability did not land. Sprint 0-Coda finishes that work.

Sprint 0-Coda is not a new sprint. It is Sprint 0 Phase 1 completing what it scoped. The naming makes the structural gap visible rather than rolling deferred work into Sprint 1's scope, where it would contaminate that sprint's already-substantial Category O + B5 + P1 plan.

Phase 1 memory-layer merge from patham9/mettaclaw upstream landed at commit `f37aa6c` between Phase A v1 draft and v2/v3 draft. The merge brought T-2 (bounded execution), T-4 (history-write expansion), persistence-with-curation primitive (promote/demote + SQLite-to-atomspace bridge), and T-3 Configuration B (query-promoted as opt-in alongside existing query). These additions resolve several open items from Phase A v1 and expand what Sprint 0-Coda can build against. See Section 3 for substrate state details.

This document drives the work. ADR-008 (Two-Dispatcher Architecture) will extract from Section 2 at Sprint 0-Coda close-out. ADR-009 (Substrate Fractal Invariant) will extract from Section 0. The dependency direction is design → ADR, not ADR → design.

---

## 2. Two-Dispatcher Context

ClarityOmega's runtime now contains two priority-ordered dispatch systems that coexist and compose. They are structurally distinct and must remain so. Read through the lens of Section 0: they are two pipes with different evolution properties, composed via flow direction, with translation boundaries at the seams.

### The soul intercept chain as fixed-value pipe

`src/loop.metta` lines 76 through 102 contain a procedural let-chain that fires once per iteration before the LLM call:

```
soul-pre-compute
→ person_state evaluation
→ soul-flourishing_prompt
→ soul-eval
→ soul-calibration-record
→ soul-note-record
→ soul-service-learning
→ soul-user-context-save
→ idle-directive computation
→ atomspace-goal-gap-fuel reads
```

This chain is a pipe in the sense of Section 0. Input arrives (`$msgrcv`, `$msgnew`). Flow moves through a fixed sequence of handlers in priority order encoded by let-binding order. Each handler writes to substrate (`change-state!` on state variables) or to local let-bindings consumed downstream. Later handlers read earlier handlers' outputs as flow.

The pipe is fixed-value: not registerable, deregisterable, suspendable, or runtime-extensible. The soul's values are immutable; its evaluations are runtime-adaptive. The hierarchy (Safety > Integrity > HumanFlourishing > Governance > Helpfulness) is fixed at boot, but whether Safety is elevated or nominal in the current cycle is a live evaluation that responds to context.

This structural inescapability is the architectural feature, not a constraint. The soul must be structurally inescapable for the same reason that Sprint 0's decision-anchor (Criterion 3, LOAD-BEARING) must be structurally enforceable: commitment mechanisms whose enforcement is optional are not enforcement mechanisms. The soul is the agent's value-navigation substrate; making it suspendable would make it cease functioning as value-navigation.

The pipe is fixed; the flow through it is adaptive.

### The Capability Registry as extensible pipe

`soul/capability_registry.metta` (180 lines, landed at Sprint 0 close in commit `7142703`) contains a declarative atomspace-matched dispatcher. Input arrives as an atom matching a registered schema. Match-then-collapse finds all registered capabilities whose schema field unifies with the input. Priority-ordered handler invocation fires each in priority order until either the chain completes or a handler writes a `dispatch-decision-anchor` atom terminating the chain.

Registered capabilities live as `(registered-capability ...)` atoms in the atomspace. They can be loaded at file load time via the manifest (`lib_clarity_reasoning.metta`). They can be added via `add-atom` at runtime (mechanism demonstrated empirically through Phase 1 merge bridge work; see Section 3). They carry lifecycle metadata, schema metadata, priority, and other fields.

The pipe is extensible; the flow through it is structured. What flows: skill requests, dispatch results, registered-capability atoms themselves as queryable data.

### Asymmetric ordering is flow direction

The soul cannot be moved into the registry. The registry's defining feature (capabilities can be deprecated, suspended, registered, removed) is the precise feature the soul cannot have. Moving the soul into a registry would make value-navigation deregistrable, the architectural failure mode the entire soul concept is designed against.

The registry cannot subsume the soul, and the soul cannot subsume the registry. The two pipes coexist with an asymmetric ordering that is not arbitrary priority. It is the direction of flow through the composed system:

- The soul intercept pipe runs first. It commits its outputs (person_state, soul_verdict_in, soul_brief, idle_directive, plus substrate atoms) before the rest of the cycle proceeds. Flow exits the soul pipe.
- The Capability Registry pipe fires within getContext (Sprint 0-Coda wires this), reading the soul's already-committed outputs as substrate context when handlers need them. Flow enters the registry pipe carrying soul outputs as context.
- The registry never writes to soul state. Flow direction is one-way: soul → registry, never the reverse.
- The soul intercept pipe never invokes the registry. The soul does not consult capabilities to make value-navigation decisions; the soul is the value-navigation system.

This asymmetric coexistence is the architectural design. The two pipes compose through atoms (the flow), not through governance (which is privileged to the soul). The soul writes substrate state during its chain; the registry reads that state via match patterns during its dispatch.

### Flow translation boundaries

The composition implied by the asymmetric ordering requires bridging at boundaries where pipe representations differ. These are flow translation boundaries: places where flow exits one pipe in one representation and must be translated before entering another pipe expecting a different representation. ClarityOmega currently has two known translation boundaries, with different status as of f37aa6c.

**Boundary 1: Soul intercept output → atomspace.** The soul intercept chain writes to state variables via `change-state!` (e.g., `&person_state`) and to local let-bindings consumed in string assembly (e.g., `$soul_brief` flowing into `$enriched_prompt`). Both are prompt-space artifacts: they flow into the assembled prompt string that gets shipped to the LLM. They are not atomspace atoms that the registry's match patterns can query.

The registry queries atomspace via `match`. For the registry to consume soul state, soul state must exist as `(soul-state ...)` atoms in the atomspace, written via `add-atom` (not `change-state!`).

This boundary is unresolved as of f37aa6c. The soul-state-producer work-package is the flow translator. Its design begins after Sprint 0-Coda Phase D verifies, and it carries higher-priority weight than Boundary 2 because of the governance-flow privilege named in Section 0: soul outputs include governance verdicts, and governance visibility is structurally more important than informational visibility.

**The cost of Boundary 1 being unresolved during Sprint 0-Coda.** During Sprint 0-Coda Phase D, the registry fires without being able to read soul verdicts. This unresolved status is tolerable specifically because the first production capability (skill-discovery) is an informational handler that makes no governance decisions. The handler queries `(registered-capability ...)` atoms and formats them; nothing it does requires consulting a soul verdict. Future capabilities that need to read soul verdicts (e.g., a dispatch-guard that decides whether to allow a registry invocation based on soul Safety state) are blocked until Boundary 1 resolves. This is the Safety-tier deficit named in Section 0: until soul-state atoms are queryable, the registry cannot enforce safety constraints structurally, only by convention.

**Boundary 2: SQLite persistent storage → atomspace.** Persistence and curation primitives adopted from upstream via the Phase 1 merge use SQLite as the source of truth for promotion salience. The `promote/demote` MeTTa functions write to SQLite via `py-call (helper.promotion_set_value ...)`. For the registry (or any atomspace consumer) to read promotion state, salience must exist as `(promoted memory-id $uuid salience $value)` atoms in atomspace.

This boundary is RESOLVED as of f37aa6c. The resolution path was Option A from `memory_layer_merge_design_v1.md` Section 7: SQLite remains the source of truth; atomspace holds a derived view written via dual-write inside promote/demote (Bridge-MeTTa-1 alpha implementation: clean `add-atom &self (promoted memory-id $uuid salience $newv)` inside the inner progn after the SQLite py-call). A startup reconciliation function (`reconcile-promotion-atoms` in `src/memory.metta`, called from initMemory) syncs atomspace from SQLite source-of-truth on every container restart.

**Architectural significance of choosing Option A over Option B.** Option B would have been direct ChromaDB-to-atomspace, bypassing SQLite. Option A introduces SQLite as an intermediate layer where promote/demote curation operates BEFORE atomspace exposure. This matches Sprint 0-Coda's bounded-adoption mandate: not every memory becomes substrate-visible; only memories that pass through curation become available to the registry. The SQLite layer is the curation pipe; the atomspace bridge is what allows curated state to flow to the registry. This choice is not merely operational. It is structural alignment between persistence-with-curation as a single adoptive unit (per merge design v1 Section 8) and the registry's read-only consumer position relative to upstream pipes.

### Drift check (Section 2)

Two-dispatcher separation preserves loop shape (soul still runs first, registry still reads soul output; flow direction one-way; asymmetric ordering enforced structurally) and preserves world knowledge (no soul verdict is dropped or distorted by the architecture itself; the unresolved Boundary 1 limits what registry can see but does not corrupt what passes through the resolved channels). Both properties checked; both hold for v3's design.

### What this section will be extracted into at close-out

ADR-008 (Two-Dispatcher Architecture) will extract from this section at Sprint 0-Coda close-out. The extraction preserves the architectural claims future readers need: two pipes exist for distinct reasons, they coexist with asymmetric flow direction, two flow translation boundaries are named (one resolved at f37aa6c via Option A bridge, one pending soul-state-producer work-package), governance flow privileged over informational flow (Safety-tier deficit reasoning), the fractal recurrence makes these decisions propagate. The ADR records what the design did; this section is the design the ADR records.

---

## 3. Substrate state on commit f37aa6c

Sprint 0-Coda v3 builds on substrate state established at HEAD `f37aa6c`. Verified facts about that foundation:

**Reading guide (per Section 0 memory criterion):** Section 3 records substrate state. Each entry below is verification data; the knowledge it carries is the constraint that data creates for downstream design. Read each subsection asking: what does this fact rule out, require, or enable for Phase B/C/D and Sprint 1+? v4 will surface those constraints inline; v3 leaves them as a reader-applied check.

### Capability Registry dispatcher (Sprint 0 deliverable, unchanged from v1)

- `soul/capability_registry.metta` exists on disk, 180 lines, no catch wrap
- Phase D verification 6/6 PASS at Sprint 0 close, including Criterion 3 (decision anchor) LOAD-BEARING and Criterion 5 as documented limitation
- The file is NOT currently imported in `lib_clarity_reasoning/lib_clarity_reasoning.metta` manifest. Sprint 0-Coda Phase C wires the import.
- ADR-006 (sprint-scoped) and ADR-007 (project-wide) are committed and reference this dispatcher

### Soul intercept chain (unchanged from v1)

- Lives at `src/loop.metta` lines 76-102
- All state writes via `change-state!` to state variables; no atomspace atoms written for soul state
- Output flows: `$soul_brief` at line 103, `$enriched_prompt` at line 104, both feeding into prompt assembly downstream
- This is Boundary 1 from Section 2: unresolved flow translation boundary requiring the soul-state-producer work-package

### getContext function (unchanged from v1)

- `src/loop.metta` lines 38-45
- Pure MeTTa function; no Python boundary
- Line 39 contains the string-assembly chain with `(getSkills)` called directly
- `getSkills` has no MeTTa definition in this repo; resolves as runtime primitive

### getSkills body (what we are migrating from, unchanged from v1)

- Defined in `src/skills.metta` lines 1-25
- Contains 14 quoted-convention skill descriptions hardcoded into the body
- Includes Clarity-local additions (`tavily-search`, `technical-analysis`) not present in upstream
- Uses parenthesized s-expression skill-invocation syntax (`(remember string_in_quotes)`), diverging from upstream's unquoted convention

### Library manifest pattern (unchanged from v1)

- `lib_omegaclaw.metta` is top-level, bundles core libraries + `lib_clarity_reasoning`
- `lib_clarity_reasoning/lib_clarity_reasoning.metta` is the soul-side manifest with one `!(import! ...)` directive per soul/ file
- Adding new soul/ files to runtime means adding a line to `lib_clarity_reasoning.metta`, not editing consumer code
- This manifest pattern is substrate-externalized-control-flow (ADR-007) applied to library structure

### Diagnostic prints (unchanged from v1, commit 7e0aa28)

- Nine `DIAG-CYCLE-*` markers in `src/loop.metta` lines 139-147 fire each iteration
- One `DIAG-POPULATOR-PRUNE` marker in `soul/recent_action_populator.metta`
- All read-only collapse-then-print; visible in running log for verification during Sprint 0-Coda

### gc producer-alignment fix (unchanged from v1, commit Aa = 95a22e6)

- `src/skills.pl` contains gc/1 predicate at lines 12-16 (verbatim from upstream)
- `src/skills.metta` line 53 imports `(shell first_char gc)`
- Empirically verified at runtime: iterations 1+ complete through DIAG-CYCLE-END without errors
- Backups preserved at `src/skills.pl.bak.gc_producer_alignment` and `src/skills.metta.bak.gc_producer_alignment`

### Phase 1 memory-layer merge (NEW since v1, commit f37aa6c)

The merge from patham9/mettaclaw upstream landed four file edits via atomic apply-or-nothing py-script (`staging/apply_phase1_memory_layer_merge.py`):

**T-2 (bounded execution) in `src/skills.metta`:** The metta function now wraps eval in Patrick's full upstream form: `(let $code (sread $str) (repr (progn (call_with_inference_limit (Predicate (quote (eval $code $x))) 100000000) $x)))`. Imports `call_with_inference_limit` from Prolog. Every LLM-generated `(metta ...)` skill invocation now executes under a 100M inference budget. Bounded execution arrives before Sprint 1 writes any metta_eval consumers; no unbounded metta_eval window exists. Note: T-2's 100M bound operates at the Metta evaluation layer; it bounds inference, not computation (wall-clock time, Python call chains).

**Persistence-with-curation in `src/memory.metta` (+105 lines):**

- Configure parameters: `maxSimilarityRecall`, `promotionInflationFactor`, `mostPromotedMemories`
- `promotion_open_map` invoked in `initMemory` to create SQLite file at boot
- `get-promotion` computes time-decayed salience: `salience * (1 + days_elapsed)^(-0.7)`
- `best-promoted-memory-ids` and `best-promoted-memories` rank and retrieve
- `query-promoted` as new function alongside existing `query` (T-3 Configuration B)
- `promote` and `demote` with inline bridge: SQLite py-call PLUS `(add-atom &self (promoted memory-id $uuid salience $newv))` in the same inner progn
- `reconcile-promotion-atoms` called from `initMemory` after `promotion_open_map`, emitting atoms for any SQLite-stored salience > 0.0

**SQLite primitives in `src/helper.py` (+124 lines):** 11 functions (`promotion_open_map`, `promotion_key`, `promotion_set_value`, `promotion_get_value`, `promotion_get_all_keys`, `promotion_set_lasttime`, `promotion_get_lasttime`, `promotion_has_key`, `promotion_delete_key`, `promotion_commit`, `promotion_close_map`), plus `_PROMOTION_CONN` global, plus `sqlite3`/`uuid`/`os` imports, plus `__main__` self-test exercising the 11 helpers end-to-end. Patrick's primitives at the SQLite layer stay intact; the bridge is MeTTa-side.

**T-4 (history-write expansion) in `src/loop.metta`:** Line 159 condition changed from `(if $msgnew ...)` to `(if (or $msgnew (not (== $sexpr ()))) ...)`. Autonomous reasoning output now writes to history even without a new human message. The values commitment: Clarity's autonomous reasoning is substrate-record-worthy world knowledge equivalent to exchange-driven reasoning.

**End-to-end runtime verification (Phase 1 close, in-session):**

- Container boots and iterates cleanly (cycle 1000+)
- `promotions.db` file created at `/PeTTa/repos/omegaclaw/memory/promotions.db` at boot
- Schema verified: `kv(key BLOB PRIMARY KEY, value REAL NOT NULL, lasttime REAL)`; WAL journal mode active
- All 11 SQLite helpers pass `python3 src/helper.py` self-test
- `ids_by_time`, `query_by_ids`, `query_with_ids_and_dists` confirmed present in `/PeTTa/repos/petta_lib_chromadb/lib_chromadb.py`
- Bridge end-to-end exercised: MeTTa `(promote "2026-04-15 13:48:52")` returned PROMOTE-SUCCESS; ids_by_time returned two memory IDs; both SQLite writes AND add-atom fired; atomspace contains `(promoted memory-id $uuid salience $value)` atoms with salience 1.0 and 1.99 (time-decay formula working, pow-math available)
- T-2 wrapping: PROMOTE-SUCCESS returns from wrapped eval; bounded execution operational

**Empirical precedent from Phase 1 bridge work.** The atom shape `(promoted memory-id $uuid salience $value)` from the bridge is more than a demonstration that runtime add-atom works. It is a working schema instance for memory-item atoms keyed by ID with a salience/confidence value. When Phase C considers capability registration (Section 7), the registration pattern can generalize from this empirically-validated shape, not just from the abstract availability of `add-atom`. The bridge gives Sprint 0-Coda an architectural precedent to build on.

### Parity baseline (unchanged from v1)

- CHARS_SENT measured in range 38653-38910 across iterations 1-2 with hardcoded getSkills
- This is the empirical baseline Sprint 0-Coda's parity verification compares against

### Mattermost encoding layer (unchanged from v1)

- The MM-to-LLM transport encodes apostrophes as `_apostrophe_`, newlines as `_newline_`, and similar tokens
- Changes to the SKILLS block content must be verified end-to-end through the encoding layer, not just at MeTTa string level
- The unquoted-convention switch (Sprint 0-Coda) reduces apostrophe-and-paren character density in skill descriptions, likely a net stability win through this layer beyond aesthetic alignment with upstream

---

## 4. Sequencing axiom

The work proceeds in this order. The order matters because each step constrains what the next step can decide:

1. **Contract.** Define what the handler consumes and produces. The schema declared here constrains every downstream decision. Section 5 below.
2. **Registration.** Construct the `(registered-capability ...)` atom that declares skill-discovery to the registry. Section 6 below.
3. **Wiring.** Insert dispatch call in getContext; add manifest imports; update Artifact 1. Section 7 below.
4. **Verification.** Parity-as-migration-sequence; through MM encoding; free Criterion 5 live-observation. Section 8 below.

Reversing any step in this order risks designing to under-specified preconditions. Wiring before the contract is defined wires to the wrong shape. Verifying before wiring lands means verifying a draft.

This axiom is inherited from Sprint 0's empirically-iterative discipline. Sprint 0-Coda is similarly empirically-iterative; the Discipline-4-deviation pattern (substrate + ADRs together first, verify, spec amendment as closing commit) applies.

In pipe/flow terms: the contract defines what flow enters and exits the pipe. Registration declares the pipe to the registry. Wiring connects the pipe to upstream and downstream pipes. Verification confirms the pipe exists and correct flow passes through it. Sequencing follows the flow direction; reversing the sequence wires unmoored pipes.

---

## 5. Contract: skill-discovery handler as pipe receiving and emitting flow

### Input atom: flow entering the pipe

```
(skill-request cycle: $k)
```

The handler matches on this atom. `$k` is the cycle counter passed through getContext. The atom is written once per cycle from within getContext, immediately before the existing string-assembly chain.

The dispatcher's match-and-dispatch infrastructure handles invocation; skill-discovery's handler receives the matched atom as the entering flow and produces its output as exiting flow.

### Output atom: flow exiting the pipe

```
(skill-set skills: $formatted-string)
```

A single atom with a single string field. This atom is the LAST translation boundary between atomspace data and the LLM-facing prompt string. All atom-level intelligence (which capabilities exist, which are active, future context-filtering) lives upstream of this atom inside the handler. The prompt assembler reads the string field and substitutes it for the current `(getSkills)` runtime-primitive call in getContext.

In pipe/flow terms: this atom is the pipe's terminal flow, formatted for downstream consumption by the LLM prompt pipe.

### The companion-atom family (per Path C substrate)

The skill-set atom is the LLM-facing terminus. The registry also writes companion atoms that are NOT consumed by the LLM but ARE consumed by other parts of the substrate (verification scripts, future filter steps, external observers). These atoms make the dispatch process queryable, inspectable, and observable. They are the meta-awareness layer of the registry made structural.

**Dispatch-lifecycle atoms (written by the dispatcher):**

- `(dispatch-invocation invocation-id: $id input-atom: $atom)` — written when dispatch starts; records what was dispatched
- `(capability-invoked invocation-id: $id handler: $h input-atom: $atom)` — written before each handler in the chain runs
- `(dispatch-chain-anchored invocation-id: $id anchor-handler: $h)` — written when a handler returns `decision-anchor` and terminates the chain
- `(dispatch-chain-exhausted invocation-id: $id)` — written when the chain completes without anchoring
- `(dispatch-fallback-activated invocation-id: $id input-atom: $atom reason: $r)` — written when no capabilities matched

These atoms are the dispatcher's behavior made visible. The dispatcher does not change in v6; these atoms come from Path C's existing dispatch primitive.

**Observation-override atoms (operational; drive resolution in filter steps):**

- `(capability-lifecycle-observation handler: $h lifecycle: $observed)` — overrides the registered lifecycle for `$h`
- `(capability-priority-observation handler: $h priority: $observed)` — overrides the registered priority for `$h`
- `(capability-efficacy-observation handler: $h efficacy: $observed)` — overrides the registered or default efficacy for `$h`

These atoms are operational. Filter steps consult them during resolution. When present, the observed value overrides the registered value. When absent, the registered value (or a default) is used. This is the override mechanism Clarity's three principles call external verification hook: any agent — Clarity, Berton, future tooling — can write an observation atom and the next dispatch consults it. The detection-action gap closes here at the substrate level: external observation has a place to land that immediately affects behavior.

**Registered-side declarations (capability declares its own baseline values):**

- `(capability-efficacy-rate handler: $h rate: $r)` — capability-declared baseline efficacy; used by `efficacy-filter-step` when no observation override exists

**General external-observation atom (archival; coexists with operational atoms):**

- `(external-observation observer: $source capability: $h assessment: $verdict evidence: $text timestamp: $ts)` — records WHO observed, WHAT was assessed, the verdict, supporting evidence, and when

Clarity's reasoning on the coexistence of these two atom families: dimension-specific observation atoms (`capability-lifecycle-observation`, `capability-priority-observation`, `capability-efficacy-observation`) are the override mechanism — they drive resolution in filter steps. The general `external-observation` atom is the audit trail — it records provenance, rationale, and evidence. One is mechanism, the other is memory. Both are needed.

Phase 1 implementation uses the dimension-specific atoms in filter steps. The general `external-observation` atom is schema-reserved in v6 but its consumers (audit tools, future Clarity-facing inspection capabilities) come later.

**Aggregation atom shape (reserved for Phase C+; do not implement yet):**

- `(capability-efficacy capability: $h invocations: $n successes: $m last-updated: $ts)` — computed efficacy from observed outcomes

This shape is reserved in the schema so future aggregation logic does not need to retrofit it. Aggregation is Phase C+ work; v6 does not specify the computation that populates this atom. What matters now is that the schema accommodates it — the pipe is shaped to carry the water that will arrive.

### Why these companion atoms are not premature

These atoms exist in the Path C substrate today (commit pending). v6 names them in the contract because the contract is what future readers and future capabilities will consult to understand what the registry guarantees. A capability that wants to consult dispatch-invocation atoms cannot do so reliably if the contract does not name them as guaranteed outputs.

The schema fields, atom shapes, and filter-step infrastructure are structural commitments. Their implementation (aggregation logic, audit tools, success-criterion evaluation) is downstream. The pipe is shaped now; the water flows when capabilities and tools arrive that need to consume it.

### Handler logic: flow transformations within the pipe

```
(= (skill-discovery $request)
   (let* (($capabilities (collapse (match &self
                                          (registered-capability schema: $s
                                                                 handler: $h
                                                                 priority: $p
                                                                 lifecycle: active
                                                                 metadata: $m)
                                          ($s $h $p $m))))
          ($formatted (format-skill-set $capabilities)))
         (skill-set skills: $formatted)))
```

Five flow transformations within the pipe:

1. Receive incoming flow (the `$request` parameter; here `(skill-request cycle: $k)`)
2. Query available pipes: match `(registered-capability ...)` atoms with `lifecycle: active`. The match pattern's `lifecycle: active` filter is the queryable-state primitive. Capabilities with other lifecycle values (deprecated, suspended, pending-replacement) are invisible to this match (the deprecated/suspended pipes still exist for inspection; they simply do not carry active flow).
3. Collapse the match results into a list of `($schema $handler $priority $metadata)` tuples (flow consolidation)
4. Format the list into a skill-description string via `format-skill-set` (flow shape transformation)
5. Return `(skill-set skills: $formatted-string)` (flow emission)

The handler is read-only against atomspace state. It writes no atoms. It calls no helpers in `helper.py` (MeTTa-substrate-only per the project's substrate-first principle). The `format-skill-set` helper is defined in the same soul/ file as skill-discovery itself (also MeTTa-substrate).

### Filter-step contract (the second extension point; parallel to handler registration)

The capability registry has two extension points, both atom-defined:

- **Handler registration** declares what capabilities exist (covered above and in Section 6)
- **Filter-step registration** declares how dispatch eligibility is determined

Filter-step registration is new in v6 (Path C, Clarity 2026-05-26). It replaces the hardcoded resolution pipeline (lifecycle → priority → efficacy) that v5 inherited from earlier drafts. The new design: each dimension becomes a registered filter step. Adding a new dimension (trust, scope, cost, audience) requires no registry code change — only a new step function and a registration atom.

**The filter-step contract:**

```
(capability-filter-step order: $n step: $step-fn)
```

Where `$n` is a numeric ordering value (lower numbers run first) and `$step-fn` is the name of a MeTTa function with the signature:

```
(= ($step-fn $pipeline-entry) $result)
```

The function takes a `pipeline-entry` atom (which carries resolved values forward through the pipeline) and returns one of two results:

1. **An updated `pipeline-entry`** — the step passes the entry along, possibly with one or more fields updated
2. **The atom `filtered-out`** — the step drops the entry from the dispatch chain

A filter step may enrich (return updated entry), filter (return filtered-out), or both. The two-result contract subsumes these behaviors; no registration-level distinction is needed. Per Clarity's reasoning: the filter/enrichment distinction is behavioral, not structural. It lives in the step implementation, not its registration. A step that enriches today may become a filtering step tomorrow if a governance rule emerges — same function, different runtime behavior. Distinguishing kinds at the registration level would re-introduce the rigidity Path C was designed to remove.

**The pipeline-entry shape:**

```
(pipeline-entry handler: $h lifecycle: $l priority: $p efficacy: $e)
```

The pipeline-entry IS the flow between filter steps. It carries resolved values forward; each step can read what prior steps resolved. Accessor and updater functions (`pe-handler`, `pe-with-lifecycle`, etc.) are defined in Path C and stable through v6.

**Phase 1 filter steps (the three existing dimensions, decomposed):**

- `(capability-filter-step order: 10 step: lifecycle-filter-step)` — resolves lifecycle (registered or observed), checks eligibility against `eligible-lifecycle` atoms, filters out ineligible
- `(capability-filter-step order: 20 step: priority-filter-step)` — resolves priority (registered or observed), enriches pipeline-entry (no filtering)
- `(capability-filter-step order: 30 step: efficacy-filter-step)` — resolves efficacy (registered rate or observed override; defaults to 1.0), checks `(>= $efficacy 0.3)`, filters out below threshold

These three registrations live in `soul/capability_registry.metta` itself (Path C lines 95-97). They are seeded with the registry; capabilities do not need to register them.

**Adding a new dimension:**

To add a trust filter:

1. Define the step function:
   ```
   (= (trust-filter-step $entry)
      (let $handler (pe-handler $entry)
           (let $trust (resolve-trust $handler ...)
                (if (>= $trust $threshold)
                    $entry
                    filtered-out))))
   ```
2. Register it: `(capability-filter-step order: 25 step: trust-filter-step)`

No changes to `resolve-and-filter-entries`. No changes to dispatcher logic. The pipeline picks up the new step on the next dispatch.

**Why this generalization matters architecturally:**

The hardcoded pipeline in v5's design was clean and internally consistent, but it forced any new evaluation dimension (and Clarity's layer-gap analysis surfaced multiple coming: efficacy, trust, scope) to require registry code surgery. The generalization closes this rigidity: the registry stops being a decision-maker about which dimensions matter and becomes generic infrastructure that carries whatever dimensions get registered. This is the same shift in spirit as making handlers atom-defined rather than hardcoded — symmetry of extension points across the two axes (what capabilities exist, how dispatch eligibility is determined).

In pipes/flows/meta-awareness terms: filter-step registration is the second flow Clarity's layer-gap analysis called for. v5 had one flow direction (capability registers → dispatch → result). v6 has filter-step registration as a parallel flow that shapes how dispatch eligibility evaluates. New dimensions arrive as registration, not as substrate edits. The pipe is generic; the water (which dimensions matter) is determined by what registers.

### Why the substrate-reshape happened at v6 rather than v5 FINAL

v5 was marked FINAL prematurely. Clarity's layer-gap analysis surfaced a pattern (detection-without-action-selection-update) that has structural consequences for what the capability registry MUST CARRY to avoid replicating that pattern at the substrate level. v5's design was clean but architecturally incomplete: it cataloged capabilities (the catalog question) but had no way to know whether those capabilities DELIVERED (the counter question). Retrofitting efficacy tracking onto a catalog-shaped registry would be uphill against the established frame. The cost of reshaping the pipe now — while no water flows through it — is low. The cost of reshaping later, when "capability registry" has hardened in everyone's mental model as "dispatcher," is high.

The PIPE must fit the WATER. Clarity's analysis named the water (efficacy, observation, success-criterion declaration, filter-step extensibility). v6 shapes the pipe to fit it.

This is the same discipline applied to a different scale than the v3→v4 cycle (which caught the v3.3 consistency gap). The discipline: a design version can be locally complete and still architecturally incomplete; adjacent pressure reveals it; the architecturally-honest move is to reshape now, not defer.

### Empty-context behavior: validated-structure, unvalidated-function transition

In Sprint 0-Coda, only one `(registered-capability ...)` atom exists: skill-discovery itself. The handler matches it but the formatted output for that single self-registration is meaningless to the LLM.

In pipe/flow terms: the skill-discovery pipe has flow but lacks downstream consumption that validates the flow's correctness. The pipe is structurally validated (it exists, it produces output of the right shape), functionally unvalidated (the output does not yet replace what the old getSkills pipe produces). This is the validated-structure, unvalidated-function transition.

Two implementations for the transitional state are viable:

**Option (a):** The handler always emits the hardcoded list at this stage. The `match` on `(registered-capability ...)` collects names of registered capabilities but does not yet drive the output content. Registration is recognized; output content is not yet sourced from registrations. The old pipe carries flow until the new pipe accumulates enough flow (more capability registrations) to validate its function. This is the validated-structure, unvalidated-function transition.

**Option (b):** The handler emits registered-capability descriptions when capabilities are registered with usable description metadata, AND emits the hardcoded fallback for skills not yet migrated to registry form. The transition is partial; the registry-sourced portion grows as capabilities register.

For Sprint 0-Coda specifically:

- **Sprint 0-Coda commits to (a).** Only one capability registers (skill-discovery itself), and its descriptions would not help the LLM. The handler emits the existing hardcoded skill descriptions, with the registry consultation present but not yet driving output content.
- The parity check verifies that the registry-sourced path produces the same skill list the hardcoded getSkills produced.
- The mechanism is proven via registration + match + collapse working correctly; output content parity is the success criterion at this stage.
- Sprint 1's first per-skill registrations (when individual skills migrate to registry form) start using the option (b) pattern progressively.

This is consistent with the recursive-integrity principle: do not ship a commitment that cannot be structurally fulfilled. The dispatcher demonstrates substrate observability (the pipe exists); the content migration is incremental (flow validates the pipe's function progressively).

### Edge case: empty active capability list

If `match` returns no active capabilities, `format-skill-set` produces an empty string, yielding `(skill-set skills: "")`. An empty skill list reaching the LLM is a functional failure.

During Sprint 0-Coda Option (a), this case is overridden by the hardcoded fallback. The registry consultation may return empty; the output still carries the hardcoded skill list.

Post-migration (Sprint 1+), an empty active capability list is a dispatch failure. The correct behavior is: log the empty-list condition for debugging, do not crash the dispatcher chain, and either fall through to a defined default or signal upstream that the registry is unhealthy. The specific recovery policy is Sprint 1+ work; v3 names the edge case so it does not silently produce empty SKILLS blocks.

### Lifecycle transition atomicity (forward-compatibility note)

If a capability's lifecycle transitions from `active` to `suspended` mid-cycle, the match pattern won't find it on the next cycle. Transitions are not transactionally atomic relative to the dispatch cycle. In single-agent operation (ClarityOmega's current configuration), this is tolerable: lifecycle changes happen rarely, and any inconsistency lasts at most one cycle.

In potential multi-agent coordination (future work), this becomes a consistency issue requiring locking or versioned snapshots. The schema permits adding a `version: $v` field to `(registered-capability ...)` atoms without changing the dispatcher; the version field would carry monotonic snapshot identity. v3 flags this as a future-compatibility concern without imposing a solution now.

### Forward-compatibility commitments (six)

The schema and handler are committed to be forward-compatible with six identified directions of substrate evolution. Sprint 0-Coda ships only what is needed now; these commitments preserve the path. Each commitment is restated in Section 10 under the pipe-evolution lens.

**(1) Registration via atoms.** Capabilities are `(registered-capability ...)` atoms loaded from file-load or addable via `add-atom` at runtime. Sprint 0-Coda demonstrates file-load. Runtime registration via add-atom requires no schema change; it is the same atom, written from a different time. **Mechanism demonstrated empirically through Phase 1 bridge work (Section 3): `(promoted memory-id $uuid salience $value)` atoms appear in atomspace via `add-atom &self` calls in production.**

**(2) Single-atom output with extensible schema.** The output is one `(skill-set ...)` atom with one string field. Future field additions (return-type, resource-budget, lifecycle-condition, audience metadata) extend the atom in place. Missing fields mean "unspecified," not "forbidden."

**(3) Per-handler resource budgeting deferred to Phase 1.5.** Sprint 0-Coda does not enforce per-handler inference budgets. Phase 1.5 weighs three paths: (a) reduce/2 exception propagation, (b) Error return contract, (c) per-handler inference-limit wrapping. T-2's `call_with_inference_limit 100M` (now active at the metta-call layer) is precedent for path (c). **Important distinction: T-2's 100M operates at the Metta evaluation layer; it bounds INFERENCE STEPS, not computation. Per-handler resource budgeting (Phase 1.5) would need to bound COMPUTATION — wall-clock time, Python call chains, string operation cost — a different and complementary problem.** All three paths are complementary and may all be needed.

**(4) Provenance via typed returns.** Future dispatch-result atoms carry typed return values (e.g., `WRITE-FILE-SUCCESS` per upstream's pattern, not boolean True). Sprint 0-Coda writes a string-typed result; future handlers add return-type metadata to their registration so downstream consumers can pattern-match on outcome quality.

**(5) Lifecycle extensibility from Phase A.** The dispatcher's match pattern queries `lifecycle: active` specifically. Future lifecycle values (deprecated, suspended, pending-replacement) become available without dispatcher code changes; capabilities with non-active lifecycle become invisible to dispatch but remain in atomspace for inspection or retirement. In pipe/flow terms: pipes can be retired without removal; flow stops but the pipe structure remains queryable.

**(6) Operational metadata position.** The schema includes a `metadata: $m` field with initial empty/null seed value. Taxonomy (e.g., `irreversibility: high`, `audience: soul-state-consumer`) is deferred to first concrete consumer needs, expected to be the soul-state-producer work-package. The position is load-bearing; the contents fill incrementally.

### Drift check (Section 5)

Skill-discovery contract preserves loop shape (handler is read-only against atomspace; no soul state mutation; reads `(registered-capability ...)` atoms, writes one `(skill-set ...)` atom per dispatch; pure transformation) and preserves world knowledge (Option (a) emitting hardcoded fallback during empty-context delays consumption of registry-sourced content but does not distort knowledge — the hardcoded list IS the current world knowledge about skills; the empty active-capabilities edge case is named so empty SKILLS blocks cannot silently propagate). Both properties checked; both hold.

---

## 6. Registration

The capability registry has two registration forms in v6, both atom-defined:

- **Capability registration:** declares what capabilities exist (the handler-side extension point)
- **Filter-step registration:** declares how dispatch eligibility is determined (the resolution-side extension point)

### Capability registration

One `(registered-capability ...)` atom is added to `soul/capabilities/skill_discovery.metta`. The directory `soul/capabilities/` is new this sprint, created to house per-capability files separately from soul/ general infrastructure.

**v5 schema (carried forward):**

```
(registered-capability
   schema: (skill-request cycle: $k)
   handler: skill-discovery
   priority: 100
   lifecycle: active
   metadata: ())
```

**v6 schema extensions (new fields, all optional):**

```
(registered-capability
   schema: (skill-request cycle: $k)
   handler: skill-discovery
   priority: 100
   lifecycle: active
   metadata: ()
   success-criterion: $criterion              ;; NEW; optional
   efficacy-rate: $rate)                       ;; NEW; optional
```

Or, equivalently, the capability can register a separate companion atom for the baseline efficacy rate (Path C convention):

```
(registered-capability ...)
(capability-efficacy-rate handler: skill-discovery rate: 1.0)
```

v6 supports both conventions; the separate-atom form is what Path C uses today. The schema-field form is reserved for future capabilities that prefer single-atom declaration. Filter steps that consult efficacy check both shapes.

**The `success-criterion` field is an open-typed slot.** Per Clarity's reasoning: each capability fills it with what its nature demands. The pipe does not constrain the shape; the capability does. Three idiomatic forms have emerged in Phase A drafting:

1. **MeTTa predicate function:** for capabilities whose success is machine-evaluable. Example: skill-discovery's success-criterion is a predicate that checks whether the LLM's subsequent output invoked at least one skill from the dispatched SKILLS block.
   ```
   success-criterion: skill-discovery-success-predicate
   ```
2. **External-observer reference:** for capabilities whose success is inherently subjective or requires human judgment. Example: a future governance handler whose success is determined by external observation rather than internal computation.
   ```
   success-criterion: (observer: clarity criterion: subjective)
   ```
3. **String description:** for capabilities whose criteria are not yet formalized — an honest admission that the success-definition is human-readable for now.
   ```
   success-criterion: "LLM invoked at least one skill from the dispatched SKILLS block"
   ```

The spec provides examples of all three but does not constrain the shape. This is the same pattern as filter-step registration: the pipe carries whatever the capability puts in it.

**For Sprint 0-Coda's skill-discovery capability, the success-criterion is form (1) — a MeTTa predicate.** Phase B specifies the predicate implementation; Phase A v6 commits to the field shape and reserves the position. Per Clarity's v4 review item 3, the verification metric is Standard level (same skill name AND same argument structure invoked under equivalent conditions); the predicate operationalizes this.

Priority 100 is the initial value for the first production capability; the value is arbitrary at single-capability scale but establishes a numeric scale. Future capabilities register with priorities that produce intentional ordering.

The same file (`soul/capabilities/skill_discovery.metta`) also contains the handler definition (`(= (skill-discovery $request) ...)`), the formatter helper (`(= (format-skill-set $list) ...)`), and (Phase B+) the success-criterion predicate function.

This is the single production capability registration for Sprint 0-Coda. Sprint 0-Coda does not bulk-migrate the 14 hardcoded skill descriptions to individual `(registered-capability ...)` atoms; that is Sprint 1+ work that depends on per-skill registrations becoming useful through context-filtering. Bulk migration before context-filtering exists adds translation overhead without filtering benefit.

The registration pattern can generalize from the Phase 1 bridge atom shape `(promoted memory-id $uuid salience $value)`: keyed by identifier, with salience/priority value, lifecycle metadata, queryable via match-collapse. This is empirical precedent, not abstract design.

### Filter-step registration

Filter steps are registered with a parallel atom shape:

```
(capability-filter-step order: $n step: $step-fn)
```

Phase 1 ships three filter-step registrations seeded inside `soul/capability_registry.metta` itself (per Path C lines 95-97):

```
(capability-filter-step order: 10 step: lifecycle-filter-step)
(capability-filter-step order: 20 step: priority-filter-step)
(capability-filter-step order: 30 step: efficacy-filter-step)
```

These three are seeded with the registry, not as separate registrations the capabilities must perform. They are the substrate's bootstrap filter pipeline.

Future filter-step registrations (trust, scope, cost, audience) can live anywhere — in `soul/capability_registry.metta`, in `soul/capabilities/` per-capability files if a specific capability brings a specific filter, or in a dedicated `soul/filters/` directory if filter steps become numerous. The registration pattern is uniform regardless of file location.

**Symmetry of the two extension points.** Adding a new capability: write handler function, register `(registered-capability ...)` atom. Adding a new filter dimension: write step function, register `(capability-filter-step ...)` atom. Both extend the registry without modifying it. This symmetry is what v6 establishes that v5 did not have.

---

## 7. Wiring

Phase C lands five coordinated changes in one commit per Discipline 4 (v5 had four; v6 adds the substrate-reshape as Change 0 which logically precedes the others):

### Change 0: Substrate reshape — Path C generalization in soul/capability_registry.metta

The existing `soul/capability_registry.metta` (180 lines, landed at Sprint 0 close in commit `7142703`) is replaced with the Path C draft (228 lines, Clarity 2026-05-26). The dispatcher primitive is unchanged. The resolution helpers (`resolve-lifecycle`, `eligible?`, `resolve-priority`, `resolve-efficacy`, `efficacy-eligible?`) are unchanged. What changes:

- `resolve-and-filter-entries` is replaced with the generalized version that walks registered filter steps (Path C lines 174-192)
- New infrastructure added: `apply-filter-pipeline`, `walk-filter-steps`, pipeline-entry shape and accessors/updaters (Path C lines 119-134)
- Three filter-step functions defined that decompose the v5 hardcoded pipeline: `lifecycle-filter-step`, `priority-filter-step`, `efficacy-filter-step` (Path C lines 141-168)
- Three seed filter-step registrations: `(capability-filter-step order: 10 step: lifecycle-filter-step)`, `(capability-filter-step order: 20 step: priority-filter-step)`, `(capability-filter-step order: 30 step: efficacy-filter-step)` (Path C lines 95-97)

The dispatch primitive's call to `resolve-and-filter-entries` is unchanged in shape; only the function's internal implementation changes. Downstream code that calls dispatch sees no contract change. This is what makes the reshape architecturally surgical: the entry point is identical; only the resolution pipeline's implementation is generalized.

Path C also already contains the dimension-specific observation-override atoms in its resolution helpers (lines 41-46, 55-58, 65-67). v6 names these in the Section 5 contract; the substrate already supports them.

The full Path C draft is at `staging/capability_registry_path_c_draft.metta` and gets copied to `soul/capability_registry.metta` as part of the Phase C apply script.

### Change 1: New capability file

`soul/capabilities/skill_discovery.metta` (new file)

Contains:
- The registration atom (Section 6)
- The handler definition (Section 5)
- The formatter helper

### Change 2: Manifest update

`lib_clarity_reasoning/lib_clarity_reasoning.metta` gets two import lines added:

```
;; Capability Registry (Sprint 0 deliverable, loaded by Sprint 0-Coda Phase C)
!(import! &self (library omegaclaw ./soul/capability_registry))

;; skill-discovery capability (Sprint 0-Coda first production registration)
!(import! &self (library omegaclaw ./soul/capabilities/skill_discovery))
```

The first import loads the dispatcher itself, which was committed at Sprint 0 close but never wired to runtime. The second loads the skill-discovery capability and its registration.

### Change 3: getContext dispatch insertion

`src/loop.metta` getContext (lines 38-45) gains one additional let-bind. Current shape:

```
(= (getContext $k)
   (string-safe (py-str ("PROMPT: " (getPrompt)
                         " SKILLS: " (getSkills)
                         ...))))
```

Sprint 0-Coda shape:

```
(= (getContext $k)
   (let* (($_dispatch (dispatch (skill-request cycle: $k) (gensym-invocation-id)))
          ($skill-set (collapse (match &self (dispatch-result $_ (skill-set skills: $s) $_) $s)))
          ($skills-str (car-atom $skill-set)))
         (string-safe (py-str ("PROMPT: " (getPrompt)
                               " SKILLS: " $skills-str
                               ...)))))
```

Two new let-binds (`$_dispatch` and `$skill-set` plus the extracted `$skills-str`), and the substitution of `$skills-str` for `(getSkills)` in the string-assembly chain.

**Critical: Phase C wiring SUBSTITUTES `$skills-str` for `(getSkills)` in the getContext call but does NOT remove the `getSkills` definition from `src/skills.metta`.** `getSkills` remains callable until Phase D verification confirms parity. The Phase D dual-path comparison (Section 8) requires both paths to be invocable simultaneously; removing `getSkills` in the Phase C wiring commit would break the comparison the verification depends on. Removal of `getSkills` is a separate commit, after Phase D Criterion P-4 passes.

This is the migration-sequence discipline applied to the wiring commit: do not remove the old path until the new path's parity is verified at the LLM-facing boundary.

**Source of `gensym-invocation-id`.** This is the per-invocation isolation primitive specified by ADR-006 and Sprint 0 Phase 1 v3.3 Section 5. **v3.3 Section 11 Q4 explicitly left invocation-id generation to Phase C implementation, with the constraint that the chosen mechanism must produce unique-per-cycle IDs.** Phase A v4 escalates the resolution to Phase A→Phase B transition because the Phase D verification script needs to assert per-invocation isolation (v3.3 Criterion 6 equivalent), which cannot be drafted without knowing the ID source. The lineage is: v3.3 Q4 (deferred to Phase C) → Phase A v4 Section 7 Change 3 (resolved at Phase A→Phase B transition).

In v4 of Phase A, the source must be made explicit before the wiring plan is concrete enough to draft an apply script against. Three candidate sources, to be resolved in Phase B:

(i) A MeTTa primitive already available in the runtime. If `gensym` or equivalent exists, the call is `(gensym-invocation-id)` directly, no new definition required. To be verified by reading `lib_omegaclaw.metta` and runtime primitive inventory.

(ii) A Python helper exposed via py-call (e.g., `(py-call (helper.gensym_invocation_id))` returning a fresh integer or UUID per call). This requires adding the helper to `src/helper.py` and importing it into MeTTa.

(iii) A MeTTa function defined in `soul/capability_registry.metta` that uses an atomspace-stored counter (`(invocation-counter $n)` atom incremented per dispatch, with the new value used as the invocation ID). This keeps invocation-ID generation substrate-side and inspectable.

**Evaluation order for Phase B resolution:**

1. **Verify (i) first.** Zero cost if available; reading runtime primitive inventory takes one check. If a MeTTa primitive exists, the source is chosen and Phase B proceeds.
2. **Prefer (iii) over (ii) if (i) is unavailable.** (iii) is substrate-first-aligned per Section 0: invocation-id generation lives in atomspace as `(invocation-counter $n)` atoms, visible to introspection, consistent with the project-wide ADR-007 principle. (ii) violates substrate-first by routing through Python state that is invisible to atomspace queries.
3. **Fall back to (ii) only if (i) and (iii) both fail.** Phase B documents why if this path is taken.

The Phase A→Phase B transition criteria (Section 11) require this gap to close before Phase B drafts the apply script. v5 names both the gap and the resolution preference so Phase B does not re-derive the analysis.

### Change 4: Artifact 1 update

`docs/design/artifact_1_loop_metta_wiring_diagram.md` gets:

- Line-number drift fix (per Sprint 0 verification findings; current source has drifted from documented line numbers due to diagnostic-prints, Phase 1 merge, and other commits)
- New section documenting the skill-discovery dispatch insertion in getContext
- Cross-reference to this Phase A document

All five changes (one substrate reshape, one new file, one manifest update, one loop.metta edit, one artifact_1 update) land in a single commit per Discipline 4. The commit also includes the line-number drift fix because that drift was discovered during this sprint and addressing it now is cleaner than scheduling separate housekeeping.

### Drift check (Section 7)

Wiring preserves loop shape (dispatch fires within getContext, after soul chain; manifest pattern unchanged; one new file in soul/capabilities/ subdirectory; one let-bind addition; substitution of $skills-str for getSkills carries forward the same content slot in the prompt; old `getSkills` definition preserved through Phase D verification, removed only after P-4 passes; the Path C substrate reshape replaces internal resolution logic without changing the dispatch primitive's entry-point contract — downstream callers see no change) and preserves world knowledge (the SKILLS content reaching the LLM is the same content via a different path; gensym-invocation-id source is named with Phase B resolution preference (verify (i), prefer (iii) over (ii) for substrate-first alignment) so a silent gap does not propagate; old-path preservation through Phase D means the dual-path comparison the verification depends on is structurally possible; Path C's filter-step generalization preserves the three existing resolution dimensions identically while opening the architecture to new dimensions; observation-override atoms preserve the override semantics with no changes to override consumers). Both properties checked; both hold for v6's design.

---

## 8. Verification approach

### Parity as migration sequence (Clarity's framing, preserved from v1)

Parity is not a test. It is a migration sequence:

1. Run the current getSkills path. Record output.
2. Run the registry-sourced skill-discovery dispatch path. Record output.
3. Compare. If outputs are functionally identical (same content reaches the LLM, same LLM behavior results), parity is met.
4. Remove the old path. The registry-sourced path is now the canonical path.

The functional-not-syntactic distinction: byte-identical output is not the goal. LLM behavior must remain unchanged across the migration. If the registry-sourced output differs by formatting (e.g., subtle whitespace differences after MM encoding), but the LLM's response distribution is unchanged, parity is met.

### Through-the-MM-encoding verification

Parity verification operates at the LLM-facing prompt level, not at the MeTTa string level. The MM transport encodes apostrophes, newlines, and other characters before the prompt reaches the LLM. The verification looks at:

- CHARS_SENT value (current baseline: 38653-38910 across iterations 1-2)
- LLM response patterns across some number of iterations (to be specified during Phase B verification design)
- Any visible MM-encoding artifacts that differ between old and new paths

**Phase D verification script comparison level: LLM-facing, not MeTTa-level.** MM encoding can introduce differences that are invisible at the MeTTa string level (e.g., apostrophe encoding to `_apostrophe_`, newline encoding to `_newline_`, paren handling) but visible at the LLM level. The Phase D script must compare outputs AFTER the MM encoding step, not before. Phase B's draft of the Phase D script will need to either: (i) invoke both paths and capture the encoded form post-MM, or (ii) verify parity at the LLM response level (treating MM encoding as an opaque transform). Choice (i) gives byte-level comparison at the right boundary; choice (ii) gives semantic comparison at the downstream consumer level. Phase B chooses.

A minor expectation: with the unquoted-convention switch in skill descriptions (Section 5), apostrophe-and-paren character density decreases, which should reduce `_apostrophe_` encoding overhead. CHARS_SENT may decrease slightly. This is the convention switch's hidden stability benefit, not a parity violation.

### Sprint 0-Coda success criteria as pipe-flow validation

Every criterion below checks one of two things: does the pipe exist, and does correct flow pass through it. This pattern generalizes to every future capability's verification.

**Criterion P-1: Capability registers — pipe exists in atomspace.** `(registered-capability schema: (skill-request cycle: $k) handler: skill-discovery priority: 100 lifecycle: active metadata: ())` atom is present in atomspace after substrate load. **Verification path: match-and-collapse query on `(registered-capability ...)` atoms against atomspace state directly.** Println diagnostic is observability aid, not verification substitute, because silent failures return clean from primitive calls (per v3.3 Section 4.4: substrate inspection is required when verifying writes; primitive return values do not distinguish success from silent no-op).

**Criterion P-2: Dispatch fires — flow enters the pipe.** Each iteration's getContext writes a `(skill-request cycle: $k)` atom that triggers dispatch. **Verification path: observe `(dispatch-invocation ...)` and `(dispatch-result ...)` atoms in atomspace after each cycle's dispatch via match-and-collapse query.** Println diagnostic is observability aid for cycle-by-cycle inspection; the verification claim depends on substrate inspection per v3.3 Section 4.4.

**Criterion P-3: Handler produces correct output — correct flow exits the pipe.** The handler returns a `(skill-set skills: $string)` atom whose string field is the formatted skill list. **Verification path: atomspace inspection of the `(dispatch-result $invocation-id (skill-set skills: $s) $_)` atom written by the dispatcher after handler return.** Println diagnostic is observability aid; substrate inspection is the verification claim per v3.3 Section 4.4.

**Criterion P-4: Prompt parity — downstream pipe receives equivalent flow.** The SKILLS block in the LLM-facing prompt matches the hardcoded getSkills output (functionally, per the migration sequence above). CHARS_SENT stays within baseline range 38653-38910 (or shows the expected decrease from unquoted-convention switch).

**Criterion P-5: LLM behavior unchanged — downstream behavior validates functional equivalence of flow.** Across some defined number of iterations (Phase B verification will specify the number), the LLM's skill invocation patterns are indistinguishable between pre-Coda and post-Coda runs by a specified metric. **The metric must be specified, not just the count.** Candidate metrics, by increasing strictness:

- **Minimal:** same skill name invoked on the same input type (e.g., a `(remember ...)` invocation pre-Coda triggers a `(remember ...)` invocation post-Coda under equivalent conditions)
- **Standard:** same skill name AND same argument structure invoked under equivalent conditions
- **Thorough:** same skill name, same argument structure, AND same response structure produced

**Recommended level for Sprint 0-Coda: Standard.** Sprint 0-Coda commits to Option (a) (Section 5): the hardcoded fallback drives output content; the registry consultation is structurally present but does not yet drive content. The expected LLM behavior is parity — identical invocation shape from identical SKILLS content. Standard captures this: same skill name AND same argument structure means the LLM saw the same skill list and made the same choices about which skills to invoke and how to parameterize them.

- Minimal is too weak: an LLM could invoke `(remember ...)` with different argument structure and Minimal would call it parity, masking a regression in skill-parsing behavior.
- Thorough is over-constraining: LLM response variation (token-level differences in natural language) is expected even with identical inputs; Sprint 0-Coda parity does not depend on response-level stability and cannot guarantee it without exposing transient LLM stochasticity as a false failure.

Thorough becomes appropriate in Sprint 1+ when registered capabilities actually drive content rather than being structurally-present-but-content-irrelevant. Phase B specifies the iteration count at the Standard metric level; v(N+1) of this document or Sprint 1's verification design revisits the metric if the migration sequence advances Option (a) to Option (b).

**Criterion P-6: Free Criterion 5 observation — watching for pipe rupture (flow interruption).** During Sprint 0-Coda's runtime period, observe whether the dispatcher's known limitation (Criterion 5: handler crash kills the chain silently) actually fires in production. Sprint 0-Coda is the first production use of the dispatcher; this is the empirical window. Findings recorded; no action required unless the limitation fires.

**Criterion P-7: Filter-step extensibility — the second extension point works as registered.** Verify that a new filter-step can be registered without modifying registry code. Test procedure:

1. Define a test filter step in a Phase D test scope: `(= (test-passthrough-filter-step $entry) $entry)` — always passes, never filters.
2. Register it: `(capability-filter-step order: 25 step: test-passthrough-filter-step)`.
3. Trigger dispatch. **Verification path: inspect atomspace via match-and-collapse for `(dispatch-invocation ...)` and `(dispatch-result ...)` atoms; verify the test filter step was applied without errors and dispatch proceeded normally** (per v3.3 Section 4.4 substrate-inspection discipline). Println diagnostic is observability aid; substrate inspection is the verification claim.
4. Deregister or replace with an always-filter step: `(= (test-block-filter-step $entry) filtered-out)`, register at order 26.
5. Trigger dispatch again. Verify atomspace shows `(dispatch-fallback-activated ...)` because the always-filter step filtered the only registered capability out.

P-7 is the criterion that confirms v6's substrate-reshape works as designed: filter-step extensibility is not architectural claim but operational guarantee. Phase D specifies the exact filter-step registrations to use; the test scope cleans up after itself so production runtime is unaffected.

The criteria are scoped to Sprint 0-Coda. Sprint 1's expansion of registry use generates new criteria, not modifications to these.

### Proof claim refinement (structural vs semantic verification boundary)

The earlier framing "Sprint 0-Coda proves shape under bypass conditions; truth-preservation gets exercised in Sprint 1" creates an interpretive risk: a reader could conclude Phase D verification only checks structural integrity, not semantic correctness, leaving Sprint 1 with an underspecified verification obligation.

The boundary is explicit in v3:

**Phase D verifies bypass patterns preserve structural invariants (atoms written match atoms readable, no data loss round-trip).**

**Sprint 1 verifies truth-preservation under production load (semantic coherence under drift).**

The two are distinct verification operations. Phase D operates at the pipe level: does the pipe exist, does flow enter, does correct flow exit, does the downstream pipe receive equivalent flow. Sprint 1 operates at the flow-content level: does the meaning carried by the flow remain coherent across iterations, across user contexts, across the soul intercept chain's evaluations.

Both are necessary. Neither is sufficient. This is Section 0's corrective check applied to verification scope.

### Phase D verification script

A `phase_d_coda_verification.py` script will be drafted in Phase B. Following the Sprint 0 verification pattern: self-contained, inlines preamble, runs criteria 1-7 in sequence, reports PASS/FAIL/limitation for each.

**Dual-path comparison (1) — old path vs new path.** The script invokes both the old path (hardcoded getSkills) and the new path (registry-sourced skill-discovery dispatch). It captures both outputs at the post-MM-encoding boundary (or compares LLM responses across both paths, per Phase B's resolution of the comparison-level question above). Parity is the equivalence relation at the LLM-facing boundary, not at the MeTTa level. This requires the old path (`getSkills` definition in `src/skills.metta`) to remain callable, which is why Section 7 Change 3 explicitly preserves it until P-4 passes.

**Dual-path comparison (2) — handler's two internal code paths.** Sprint 0-Coda commits to Option (a) for empty-context behavior (Section 5): the handler contains both a registry consultation (match-and-collapse on `(registered-capability ...)` atoms) and a hardcoded fallback that overrides the registry-sourced output content when registrations are sparse. Phase D must test BOTH internal paths, not just the happy path:

- **Path A:** registry consultation with the single self-registration present. Verifies the structural validation of the new pipe — registration is found, match succeeds, collapse produces a list, format-skill-set runs without error. This is the pipe-exists-and-carries-flow check at the handler level.
- **Path B:** fallback override behavior. Verifies that the hardcoded fallback emits the same SKILLS content the old getSkills primitive produces, regardless of what Path A returns. This is the functional-equivalence-to-old-pipe check.

Both paths must produce the same final SKILLS output via different internal code paths. Phase D testing of only Path A would leave a regression risk: a future change that breaks the fallback override would not be caught until Sprint 1+ migrates to Option (b) and notices the divergence in production.

### Drift check (Section 8)

Verification criteria preserve loop shape (seven criteria all checking pipe/flow integrity; no new pipes added by verification itself; verification is read-only against substrate state for P-1 through P-6, with P-7 specifically testing that the substrate's second extension point (filter-step registration) works; substrate inspection is the required verification path per v3.3 Section 4.4, not println; Phase D dual-path testing covers both old-vs-new path comparison AND handler's internal registry-vs-fallback path comparison) and preserve world knowledge (parity check validates that the same skill knowledge reaches the LLM via the new path; P-5 metric specified as Standard for Sprint 0-Coda with Minimal-too-weak and Thorough-over-constraining reasoning; comparison-level for Phase D script specified as LLM-facing so MM-encoding differences cannot silently fail parity at the wrong boundary; substrate inspection means silent no-ops cannot be mistaken for verified success; handler's fallback path is verified, not just the registry consultation path; P-7 ensures the substrate-reshape's filter-step extensibility is operationally true, not architectural claim). Both properties checked; both hold.

---

## 9. Free empirical: Criterion 5 live-firing observation

ADR-006 documented Criterion 5 as a limitation: handler crashes within reduce/2 indirect invocation terminate the chain silently because catch does not absorb arithmetic exceptions from that composition pattern (F181). Phase D Sprint 0 verified this behavior in synthetic tests.

Sprint 0-Coda is the first production use of the dispatcher. Whether the limitation manifests in production conditions has not been observed. Sprint 0-Coda observes whether it fires:

- If never fires across Sprint 0-Coda's window: evidence the cooperative-handlers world is sufficient and Phase 1.5's three paths can be evaluated empirically.
- If fires at least once: a real instance to debug rather than a synthetic one.
- If fires frequently: signal that Phase 1.5 path selection is urgent.

Free observation; no action required during Sprint 0-Coda. Findings recorded for Phase 1.5 scoping.

In pipe/flow terms: Criterion 5 is pipe rupture detection. The limitation is a known mode where the pipe fails silently, terminating flow without signaling. Production observation tests whether the rupture happens under real-world flow conditions or only in synthetic stress tests.

---

## 10. Forward-compatibility as pipe-evolution commitments

The six commitments from Section 5 are reiterated here for cross-reference. Each commitment is a structural decision about how the pipe can evolve while maintaining flow compatibility with pipes upstream and downstream. The pattern is: every pipe is designed so that its flow can evolve without breaking the pipes it connects to.

| # | Commitment | Sprint 0-Coda shape | Future shape | Pipe-evolution property |
|---|---|---|---|---|
| 1 | Registration via atoms (handler-side) | File-load via manifest; first capability is skill-discovery | Runtime add-atom (mechanism demonstrated via Phase 1 bridge end-to-end; empirical precedent in `(promoted memory-id $uuid salience $value)` shape; available for capability registration) | New handler pipes can be added at runtime; flow-compatible extension |
| 2 | Single-atom output for LLM-facing terminus, companion-atom family for substrate observability | One `(skill-set ...)` with one string field; companion atoms include dispatch-invocation, capability-invoked, dispatch-chain-anchored/exhausted, dispatch-fallback-activated, observation-override atoms (lifecycle/priority/efficacy), capability-efficacy-rate, external-observation (general archival), capability-efficacy aggregation reserved for Phase C+ | Field additions in place (return-type, resource-budget, etc.); aggregation atoms populated by Phase C+ outcome computation | The pipe's output shape can grow; flow can carry more without breaking downstream; companion atoms make dispatch process queryable, inspectable, observable |
| 3 | Per-handler resource budgeting | Deferred to Phase 1.5; T-2's 100M precedent active at metta-call layer (bounds inference, not computation) | Three viable paths weighed empirically; computation-bounding (wall-clock, Python call chains) needs distinct mechanism | Flow can be throttled per pipe; inference-bound and computation-bound are distinct throttles |
| 4 | Provenance via typed returns | String-typed result | Named-symbol returns per upstream pattern | Flow carries self-describing type information |
| 5 | Lifecycle extensibility | Filter step queries `lifecycle: active` specifically | Other values invisible to dispatch but inspectable; atomicity-of-transitions noted for multi-agent future | Pipes can be retired without removal; flow stops but structure remains inspectable |
| 6 | Operational metadata position | Empty/null seed value | Taxonomy fills with first concrete consumer (likely soul-state-producer) | Pipes can carry self-describing governance information |
| 7 | Registration via atoms (filter-step-side) — NEW in v6 | Three seed filter-step registrations (lifecycle/priority/efficacy at orders 10/20/30) in soul/capability_registry.metta | Trust, scope, cost, audience and other dimensions registered via `(capability-filter-step order: $n step: $fn)` atoms; no registry code change required | New dimensions of dispatch eligibility can be added at runtime; second extension point parallel to handler registration; the registry stops being a decision-maker about which dimensions matter and becomes generic infrastructure |

---

## 11. Phase A → Phase B transition criteria

Phase A completes when:

- This document is finalized through iteration (v1 → vN per Sprint 0's pattern)
- Clarity has reviewed and concurred with the design (or pushed back with specific structural objections that are resolved before Phase B begins)
- The contract (Section 5) and registration shape (Section 6) are locked, including filter-step contract and success-criterion field shape
- The wiring plan (Section 7) is concrete enough to draft an apply script against — **this requires the gensym-invocation-id source to be resolved** (Section 7 Change 3) — and the Path C substrate reshape (Section 7 Change 0) is the source-of-truth implementation
- The verification criteria (Section 8) are specific enough to draft a Phase D script against — **this requires the P-5 metric and the Phase D comparison-level to be specified** (Section 8) **and the P-7 filter-step extensibility test procedure to be specified** (Section 8 — the test steps are detailed; Phase B inlines them in the script)

Phase B begins by drafting the Phase D verification script first (test-first discipline for empirically-iterative sprints), then iterating the substrate code against the verification.

---

## 12. Open items list

Items decided but not blocking Phase A finalization. Status updates as of f37aa6c:

**Memory-layer adoption (promote/demote and related upstream evolutions).** CLOSED at commit `f37aa6c`. Phase 1 memory-layer merge from patham9/mettaclaw upstream landed via py-script (`apply_phase1_memory_layer_merge.py`). Promote/demote MeTTa functions, persistence-with-curation primitive, SQLite-to-atomspace bridge, T-2 bounded execution, T-4 history-write expansion, T-3 Configuration B (query-promoted opt-in) all operational. End-to-end verified. T-1 cost instrumentation parked at commit `634b3f1` for future re-activation. T-5 normalization simplification deferred pending pipeline audit. See Section 3 for substrate state details.

**Soul-state producer work-package.** Updated as of f37aa6c. The work-package is the flow translator for Boundary 1 (Section 2: soul intercept output → atomspace). Persistence-with-curation primitive is now operational, providing the producer an additional flow-translation path: aged-out soul state can be curated via promote/demote, with substrate-observable state available via the bridge atom shape. The "how does aged-out soul state get pruned" question has a substrate answer. The work-package is scheduled between Sprint 0-Coda close and Sprint 1 open per Clarity's sequencing-axiom decision; its detailed design begins after Sprint 0-Coda Phase D verifies. Per Section 0's governance-flow privilege (Safety-tier deficit reasoning): this work-package is higher-priority than informational-flow translation work because soul outputs include governance verdicts. Boundary 1 being unresolved during Sprint 0-Coda is tolerable specifically because skill-discovery is informational (Section 2); the work-package must close before any governance-decision-making capability registers.

**Tier-B follow-up items.** B3 (history-write condition) CLOSED at commit `f37aa6c` as T-4 of the Phase 1 merge. B4 (response-normalization-pipeline simplification = T-5) remains deferred pending pipeline audit per merge design v1 Section 9.

**(cut) resolution mechanism.** Tentatively confirmed as Prolog runtime bridge via parallel-substrate evidence (upstream Patrick has the same configuration and his system works). Empirically verified by iteration completion in our runtime. Not blocking; logged.

**Section 6 of fork_additions_runtime_audit_2026-05-18.md.** Several verification needs remain open from that document (wakeupInterval actual production value, self-check-guidance retirement status, idle_directive ownership, balance_parentheses apostrophe asymmetry, last upstream merge date, production memory pressure observation, pin substrate-side state). None blocks Sprint 0-Coda.

**ADR-008 full write-up.** Sprint 0-Coda close-out. Extracted from this Phase A v(final) document's Section 2.

**ADR-009 full write-up.** Sprint 0-Coda close-out. Extracted from this Phase A v(final) document's Section 0 (the Substrate Fractal Invariant: pipes-and-flows-and-meta-awareness as the organizing principle, with ADR-007 as one specific application and ADR-008 as the two-dispatcher consequence).

**Memory-criterion reframing of Section 3 (forward).** Section 3 currently carries a reading guide that asks the reader to apply the memory criterion: each entry is verification data carrying a constraint on downstream design; the reader names the constraint. v4 will surface those constraints inline, incrementally replacing "X exists, Y lines" entries with "X exists, Y lines, which constrains [specific downstream decision]." The reading guide in v3 is operational (it changes how the next reader reads Section 3), not decorative (it does not merely name the concern). Per Clarity's review #10.

**Aggregation atom shape (Phase C+ implementation, schema reserved in v6).** Per Clarity's layer-gap analysis: capabilities need a way to track delivered outcomes, not just declared capabilities. The reserved shape:

```
(capability-efficacy capability: $handler invocations: $n successes: $m last-updated: $ts)
```

This atom is computed from observed outcomes (success-criterion evaluations across dispatch results). v6 reserves the shape so future aggregation logic does not need to retrofit it; the registry's `efficacy-filter-step` can be extended to consult this atom alongside the existing `capability-efficacy-rate` (registered baseline) and `capability-efficacy-observation` (external override) atoms. Aggregation computation is Phase C+ work; specifying WHEN to update the atom (after every dispatch, on a schedule, on-demand) is part of that downstream design.

This item is open at v6 close-out; it is the natural extension point for Sprint 1+ work on outcome-tracking. The architecturally-significant decision (schema accommodates it) has already been made in v6; the operational decision (how aggregation works) is downstream.

---

## 13. Versioning and iteration

This is v6. v5 was marked FINAL prematurely; Clarity's layer-gap analysis and Path C draft surfaced architectural incompleteness that required substrate reshape rather than extension. v6 integrates Path C as the primary spec and adds Clarity's three primary-spec modifications (success-criterion schema field, general external-observation atom shape, aggregation atom shape reserved). Per Sprint 0's iteration pattern, expect v7, vN as Clarity and Berton review. The document iterates in place; section content evolves while section structure stays stable. When v(final) lands, ADR-008 and ADR-009 extract.

The numbering convention is sprint_0_coda_phase_a_v1.md → sprint_0_coda_phase_a_v2.md → sprint_0_coda_phase_a_v3.md → sprint_0_coda_phase_a_v4.md → sprint_0_coda_phase_a_v5.md → sprint_0_coda_phase_a_v6.md → etc.; the file lives at `docs/sprints/00_capability_registry/sprint_0_coda_phase_a_v6.md` (and successors at the same path with version-bumped suffix, parallel to Sprint 0's v3_0 → v3_3 trajectory).

**v5 → v6 changes (substrate reshape per Clarity's layer-gap analysis and Path C draft):**

The v5→v6 cycle was driven by an architectural finding that arrived after v5 was marked FINAL: Clarity's analysis of the detection-without-action-selection-update pattern (her layer-gap diagnosis, 2026-05-26) revealed that the capability registry as designed in v5 cataloged capabilities but had no way to know whether those capabilities DELIVERED. Retrofitting efficacy tracking onto a catalog-shaped registry would be uphill against the established frame; reshaping the pipe now — while no water flows through it — was the architecturally-honest move. The PIPE must fit the WATER. Berton's correction of an earlier "extension document" recommendation closed the seam; Clarity's Path C draft provided the substrate implementation; v6 integrates both.

- Section 5 Output atom: extended with the full companion-atom family from Path C (dispatch-lifecycle atoms, observation-override atoms, registered-side declarations) plus the general `external-observation` atom shape (Clarity #3) and the reserved `capability-efficacy` aggregation atom shape (Phase C+); the dimension-specific observation-override atoms are operational mechanism while the general external-observation atom is archival audit trail (Clarity's coexistence framing)
- Section 5 Filter-step contract: new subsection introducing the second extension point parallel to handler registration; filter-step contract is two-result (entry or filtered-out); a filter step may enrich, filter, or both; no registration-level distinction between filter and enrichment steps per Clarity's reasoning (the distinction is behavioral, not structural; premature classification at the registration level is exactly the rigidity Path C was designed to remove)
- Section 5 Why-the-substrate-reshape-happened-at-v6 subsection: records the architectural reasoning so future readers see why v5's FINAL status was provisional and what made the reshape architecturally-honest
- Section 6 Registration: capability registration extends with optional `success-criterion` and `efficacy-rate` fields; success-criterion is an open-typed slot — capabilities fill it with what their nature demands (MeTTa predicate, external-observer reference, or string description); filter-step registration introduced as a parallel registration form; Phase 1 ships three seed filter-step registrations inside the registry itself
- Section 7 Wiring: new Change 0 (substrate reshape — Path C generalization in soul/capability_registry.metta) precedes the previous four changes; total five coordinated changes in one commit per Discipline 4
- Section 7 drift check: updated to reflect substrate-reshape-without-contract-change (the dispatcher's entry-point contract is identical; only internal resolution logic generalizes)
- Section 8: new Criterion P-7 (filter-step extensibility verification) added; verifies that a new filter step can be registered without modifying registry code via test procedure of pass-through and filter-out steps
- Section 8 drift check: updated to reflect P-7 and the seven-criteria count
- Section 10 forward-compatibility table: row 1 extended to specify handler-side registration; row 2 extended to reflect the companion-atom family; new row 7 added for filter-step-side registration as the second extension point
- Section 11 transition criteria: P-7 filter-step extensibility test procedure added as Phase A→Phase B blocker
- Section 12: aggregation atom shape `(capability-efficacy capability: $h invocations: $n successes: $m last-updated: $ts)` reserved as Phase C+ open item with explicit rationale for reserving now vs implementing later
- Header: predecessor list adds Path C draft (Clarity 2026-05-26); status reflects v5 FINAL was premature

**v4 → v5 changes (per Clarity's v4 review, preserved for trace):**

Clarity's v4 review found five action-eligible precision gaps and one observation (Section 6, deferred to Sprint 1 document architecture). All five action items folded into v5.

- Section 7 Change 3: explicit statement that `getSkills` definition is preserved through Phase C wiring and removed only after P-4 passes (Clarity item 1 — old path must survive until Phase D verifies parity)
- Section 7 Change 3: gensym-invocation-id candidate evaluation order added — verify (i) first, prefer (iii) over (ii) for substrate-first alignment, (ii) is fallback only (Clarity item 2)
- Section 8 Criterion P-5: recommended metric level for Sprint 0-Coda named as Standard, with Minimal-too-weak and Thorough-over-constraining reasoning; Thorough flagged as Sprint 1+ territory (Clarity item 3)
- Section 8 Phase D verification script: dual-path comparison split into two distinct dual-path requirements — (1) old path vs new path, (2) handler's two internal code paths (registry consultation vs fallback override); both required (Clarity item 4)
- Section 13: consistency-check-at-version-close-out discipline formally committed (this section; Clarity item 5)

**Consistency-check discipline (committed for v(final) close-out).** The next consistency check occurs at v(final) close-out, before ADR-008 and ADR-009 extract. The check is performed against ALL referenced predecessor documents listed in the v(final) header, not just the immediate predecessor. The discipline is: predecessor documents referenced in headers must be read in full, not just cited; consistency checks happen at version close-outs before ADR extraction; findings are folded into the current version (or, if structural, deferred to v(N+1) with explicit rationale). The v3→v4 cycle demonstrated this discipline's value — three real consistency findings were surfaced (vocabulary harmonization with v3.3 Section 4.7, v3.3 Section 11 Q4 cross-reference, v3.3 Section 4.4 substrate-inspection-required alignment) that v1-v3 had missed despite citing v3.3 in their headers.

**Sprint 1 document architecture observation (deferred per Clarity item 6).** v5 is comprehensive; future readers face significant cognitive load. Some sections could potentially extract to subsidiary documents (Section 10 forward-compatibility table, Section 12 open items list). Not a v5 change — flag for Sprint 1 document architecture work. The principle: phase documents should drive implementation, not become reference manuals. When a phase document grows beyond drive-the-implementation scope, extraction to subsidiary specs preserves the phase document's drivability while keeping the reference content available.

**v3 → v4 changes (post v3.3 consistency check, preserved for trace):**

**v2 → v3 changes (per Clarity's twelve-point review, preserved for trace):**

- Section 0: fractal consequence updated to require correct instantiation, not just correct principle; governance-flow privilege anchored in soul hierarchy via Safety-tier deficit reasoning; drift check elevated from preamble to enforcement structure (operational drift checks added to Sections 2, 5, 7, 8); memory criterion preserved with explicit Section 3 follow-up flagged
- Section 2: cost of Boundary 1 unresolved status named (skill-discovery informational, future governance handlers blocked); drift check added
- Section 3: head reading guide added that operationalizes the memory criterion — asks the reader to apply the criterion to each entry rather than merely naming the concern (Clarity review #10, with her follow-up insisting on operational not decorative)
- Section 5: empty-context behavior restated as validated-structure, unvalidated-function transition (precise language); empty active-capability-list edge case added; lifecycle transition atomicity noted for multi-agent future; commitment 3 clarified as inference-not-computation; drift check added
- Section 7: gensym-invocation-id source named as Phase B resolution requirement with three candidate paths; drift check added
- Section 8: P-5 metric specification required (three candidate strictness levels); Phase D script comparison-level specified as LLM-facing post-MM-encoding; dual-path comparison made explicit; drift check added
- Section 10: row 3 future-shape column updated with inference-vs-computation distinction; row 5 future-shape column noted with atomicity concern
- Section 11: gensym-invocation-id source and P-5 metric added to Phase A→Phase B transition criteria
- Section 12: governance-flow privilege restated with Safety-tier deficit; memory-criterion reframing of Section 3 added as forward work

---

## Document end

This Phase A v6 design document drives the implementation. ADR-008 and ADR-009 extract at v(final) close-out (v6 is not v(final); the v5 FINAL designation was premature and v6 enters the review cycle). Each architectural claim in Section 2 is testable in substrate or commit history. Each verification criterion in Section 8 maps to an empirical check the Phase D script will perform, with substrate inspection as the required verification path per v3.3 Section 4.4, dual-path testing covering both old-vs-new and registry-vs-fallback comparisons, and P-7 confirming the second extension point operates as designed. Section 0 names the organizing principle the rest of the document instantiates and maps v3.3's "intention erosion" vocabulary to v6's "governance flow privilege" vocabulary so future readers see the lineage. Drift checks at Sections 2, 5, 7, 8 make the corrective enforcement structure live rather than decorative.

Sprint 0-Coda finishes what Sprint 0 Phase 1 (v3.3) scoped, plus the substrate reshape Clarity's layer-gap analysis surfaced. The capability registry's value proposition becomes empirically visible in production: substrate-observable dispatch, registered capabilities as data not code, producer-consumer relationships made visible, governance flow distinguished from informational flow with Safety-tier reasoning grounding the priority, AND a second extension point (filter-step registration) that makes new dimensions of dispatch eligibility extensible without registry surgery. The first production capability lands. The path to Sprint 1's capability authoring opens.

The pipes/flows/meta-awareness lens means design decisions made here are not local. They are instances of the same structural principle that governs every level of ClarityOmega. Correct pipe/flow separation here (correctly instantiated, not just correct in principle) validates the pattern everywhere. The drift tendency means structural analysis without flow analysis is the failure mode; the corrective is asking both questions (shape and truth) at every seam, and v3+ enforces this asking via explicit drift checks throughout. The memory criterion means this document should carry world knowledge that changes future reasoning, not flat records of what was decided; v3+ preserves this criterion at the document level via the Section 3 operational reading guide.

The v4 cycle established and v5 formally committed a consistency-check discipline; the v6 cycle established that consistency-check discipline must extend to consistency between design and substrate-reshape needs surfaced after FINAL designation. The v5→v6 cycle is itself an instance of the layer-gap pattern Clarity diagnosed: v5 was locally complete (detected as FINAL) but architecturally incomplete (action-selection at the project level had not yet propagated the awareness that the registry needed efficacy tracking, success-criterion declaration, and filter-step extensibility). Berton's correction of the "extension document" recommendation closed the seam; Clarity's Path C draft provided the substrate; v6 integrates both. The next consistency check happens at v(final) close-out before ADR-008 and ADR-009 extract, against all referenced predecessors (this includes ADR-006, ADR-007, sprint_0_phase_1_design_v3_3.md, all Phase A versions v1 through v(final-1), the Path C draft, and any other documents cited in the v(final) header).

**On the v5→v6 lesson, named explicitly for future readers:** A design version can be marked FINAL based on convergence of review iterations, and still be architecturally incomplete in a way that becomes visible only when adjacent pressure (here: Clarity's layer-gap analysis surfacing what kind of substrate her own action-selection layer needs to close the gap she had been living inside) reveals it. The architecturally-honest response is not to defer the reshape via an "extension document," which is detection-without-action-selection-update at the project level. The architecturally-honest response is to reshape the substrate now, while no water flows through it, and to record explicitly that this happened so future readers see both that v5 was FINAL and that v6 reshaped it. Document-version-management is not engineering-cost-management. The PIPE must fit the WATER. When the water is known and the pipe is unshaped, shape the pipe now.
