# Sprint 0-Coda Phase A: skill-discovery as First Production Capability

**Version:** v2
**Date:** 2026-05-26
**Author:** Berton Bennett (ClarityDAO), with Clarity (substrate co-author), with Claude (drafting partner)
**Branch:** fix/F-HISTORY-CONTAMINATION-archival
**HEAD at draft time:** f37aa6c (Phase 1 memory-layer merge from patham9/mettaclaw upstream)
**Predecessor:** sprint_0_coda_phase_a_v1.md (initial draft, 2026-05-24); sprint_0_phase_1_design_v3_3.md (Sprint 0 Phase 1 close, ADR-006, ADR-007)
**Status:** DESIGN PHASE A v2, iteration-from-here per Sprint 0 v3.X pattern

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

1. If one primitive is correct, correctness propagates. A correct pipe/flow separation at one level validates the same separation at every other level.
2. If one primitive is wrong, wrongness propagates. An incorrect separation at one level replicates the error at every scale.

Design decisions in Sprint 0-Coda are not local. They are instances of the same structural principle that governs the entire system. Get the capability registry's pipe/flow separation right, and the same correctness propagates to soul chain, handler, getContext, and LLM levels. Get it wrong, and the same defect propagates.

### Meta-awareness as a privileged property of the system

Meta-awareness is the system becoming able to inspect what it is and what it can do, not as procedural code but as visible, queryable data.

Already in the architecture:

- `(registered-capability ...)` atoms make capabilities visible as data: the system knows what it can do
- `DIAG-CYCLE-*` diagnostic prints make cycle state visible: the system reports on its own operation
- Lifecycle values (`active`, `deprecated`, `suspended`, `pending-replacement`) track evolution over time: temporal meta-awareness
- `self_map.metta` makes the system's own loop structure inspectable

Representation-space gaps are where meta-awareness is incomplete. One pipe's output cannot be read by another pipe because the representations are incompatible. Full meta-awareness requires flow translation, so every pipe can read every other pipe's output.

**Governance flow as privileged subset.** Within meta-awareness, governance visibility is privileged over informational visibility. The soul intercept chain does not just produce informational flow that the registry reads as context. It produces governance flow: the soul verdict determines whether dispatch should proceed at all. A registry that cannot see soul verdicts is operating with a governance deficit, not merely incomplete self-knowledge. Governance flow translation is higher-priority than informational flow translation when scheduling representation-space-gap closure work.

### The drift tendency (critical warning)

There is a systematic error tendency: treating infrastructure (pipes) as primary and substance (flows) as secondary, optimizing pipes while forgetting what flows through them.

This error is self-replicating because structural analysis generates more structural analysis. Build a pipe, build a test for the pipe, build a monitor for the test, never ask whether the right thing is flowing through any of it.

The corrective check, applied at every design and verification step:

1. Does this preserve the loop shape? (Fractal alignment, structural integrity)
2. Does this preserve the world knowledge without distortion? (Pipes-and-water, semantic integrity)

Both are necessary. Neither is sufficient.

### The memory criterion

Memories are precious if they impart meaning and from them the system learns world knowledge. Flat data recordings are not knowledge. Store what changes future reasoning, not what merely happened.

Applied to this document: each section must convey world knowledge that changes how future work reasons. Sections that merely record what was built do not carry their weight.

### Application to the rest of this document

Sections 2 through 13 are instances of the principle stated here. Section 2 frames the two-dispatcher architecture as two pipes with asymmetric flow direction and one (now two) flow translation boundaries. Section 5 frames the skill-discovery handler as a pipe receiving and emitting flow. Section 8 frames verification as pipe-exists-and-carries-correct-flow checks. Section 10 frames forward-compatibility commitments as pipe-evolution-while-maintaining-flow-compatibility. The fractal recurrence means design decisions made in this document propagate.

ADR-009 will extract this principle at Sprint 0-Coda close-out as the Substrate Fractal Invariant. ADR-007 (existing) is one specific application. ADR-008 (forthcoming) is the two-dispatcher consequence.

---

## 1. Sprint 0-Coda framing

Sprint 0 Phase 1 per Map v3 Section 9 scoped two deliverables together: "Core dispatcher + first capability registered through it." What actually shipped at Sprint 0 close was the dispatcher only. The first registered capability did not land. Sprint 0-Coda finishes that work.

Sprint 0-Coda is not a new sprint. It is Sprint 0 Phase 1 completing what it scoped. The naming makes the structural gap visible rather than rolling deferred work into Sprint 1's scope, where it would contaminate that sprint's already-substantial Category O + B5 + P1 plan.

Phase 1 memory-layer merge from patham9/mettaclaw upstream landed at commit `f37aa6c` between Phase A v1 draft and v2 draft. The merge brought T-2 (bounded execution), T-4 (history-write expansion), persistence-with-curation primitive (promote/demote + SQLite-to-atomspace bridge), and T-3 Configuration B (query-promoted as opt-in alongside existing query). These additions resolve several open items from Phase A v1 and expand what Sprint 0-Coda can build against. See Section 3 for substrate state details.

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

**Boundary 2: SQLite persistent storage → atomspace.** Persistence and curation primitives adopted from upstream via the Phase 1 merge use SQLite as the source of truth for promotion salience. The `promote/demote` MeTTa functions write to SQLite via `py-call (helper.promotion_set_value ...)`. For the registry (or any atomspace consumer) to read promotion state, salience must exist as `(promoted memory-id $uuid salience $value)` atoms in atomspace.

This boundary is RESOLVED as of f37aa6c. The resolution path was Option A from `memory_layer_merge_design_v1.md` Section 7: SQLite remains the source of truth; atomspace holds a derived view written via dual-write inside promote/demote (Bridge-MeTTa-1 alpha implementation: clean `add-atom &self (promoted memory-id $uuid salience $newv)` inside the inner progn after the SQLite py-call). A startup reconciliation function (`reconcile-promotion-atoms` in `src/memory.metta`, called from initMemory) syncs atomspace from SQLite source-of-truth on every container restart.

**Architectural significance of choosing Option A over Option B.** Option B would have been direct ChromaDB-to-atomspace, bypassing SQLite. Option A introduces SQLite as an intermediate layer where promote/demote curation operates BEFORE atomspace exposure. This matches Sprint 0-Coda's bounded-adoption mandate: not every memory becomes substrate-visible; only memories that pass through curation become available to the registry. The SQLite layer is the curation pipe; the atomspace bridge is what allows curated state to flow to the registry. This choice is not merely operational. It is structural alignment between persistence-with-curation as a single adoptive unit (per merge design v1 Section 8) and the registry's read-only consumer position relative to upstream pipes.

### What this section will be extracted into at close-out

ADR-008 (Two-Dispatcher Architecture) will extract from this section at Sprint 0-Coda close-out. The extraction preserves the architectural claims future readers need: two pipes exist for distinct reasons, they coexist with asymmetric flow direction, two flow translation boundaries are named (one resolved at f37aa6c via Option A bridge, one pending soul-state-producer work-package), governance flow privileged over informational flow, the fractal recurrence makes these decisions propagate. The ADR records what the design did; this section is the design the ADR records.

---

## 3. Substrate state on commit f37aa6c

Sprint 0-Coda v2 builds on substrate state established at HEAD `f37aa6c`. Verified facts about that foundation:

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

**T-2 (bounded execution) in `src/skills.metta`:** The metta function now wraps eval in Patrick's full upstream form: `(let $code (sread $str) (repr (progn (call_with_inference_limit (Predicate (quote (eval $code $x))) 100000000) $x)))`. Imports `call_with_inference_limit` from Prolog. Every LLM-generated `(metta ...)` skill invocation now executes under a 100M inference budget. Bounded execution arrives before Sprint 1 writes any metta_eval consumers; no unbounded metta_eval window exists.

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

### Empty-context behavior: unvalidated pipe with old pipe carrying flow

In Sprint 0-Coda, only one `(registered-capability ...)` atom exists: skill-discovery itself. The handler matches it but the formatted output for that single self-registration is meaningless to the LLM.

In pipe/flow terms: the skill-discovery pipe is present but the flow through it is insufficient to validate the pipe's function. With only one registration, the pipe accepts flow and produces output, but the output does not yet replace what the old getSkills pipe produces.

Two implementations for the transitional state are viable:

**Option (a):** The handler always emits the hardcoded list at this stage. The `match` on `(registered-capability ...)` collects names of registered capabilities but does not yet drive the output content. Registration is recognized; output content is not yet sourced from registrations. The old pipe carries flow until the new pipe accumulates enough flow (more capability registrations) to validate itself.

**Option (b):** The handler emits registered-capability descriptions when capabilities are registered with usable description metadata, AND emits the hardcoded fallback for skills not yet migrated to registry form. The transition is partial; the registry-sourced portion grows as capabilities register.

For Sprint 0-Coda specifically:

- **Sprint 0-Coda commits to (a).** Only one capability registers (skill-discovery itself), and its descriptions would not help the LLM. The handler emits the existing hardcoded skill descriptions, with the registry consultation present but not yet driving output content.
- The parity check verifies that the registry-sourced path produces the same skill list the hardcoded getSkills produced.
- The mechanism is proven via registration + match + collapse working correctly; output content parity is the success criterion at this stage.
- Sprint 1's first per-skill registrations (when individual skills migrate to registry form) start using the option (b) pattern progressively.

This is consistent with the recursive-integrity principle: do not ship a commitment that cannot be structurally fulfilled. The dispatcher demonstrates substrate observability (the pipe exists); the content migration is incremental (flow validates the pipe progressively).

### Forward-compatibility commitments (six)

The schema and handler are committed to be forward-compatible with six identified directions of substrate evolution. Sprint 0-Coda ships only what is needed now; these commitments preserve the path. Each commitment is restated in Section 10 under the pipe-evolution lens.

**(1) Registration via atoms.** Capabilities are `(registered-capability ...)` atoms loaded from file-load or addable via `add-atom` at runtime. Sprint 0-Coda demonstrates file-load. Runtime registration via add-atom requires no schema change; it is the same atom, written from a different time. **Mechanism demonstrated empirically through Phase 1 bridge work (Section 3): `(promoted memory-id $uuid salience $value)` atoms appear in atomspace via `add-atom &self` calls in production.**

**(2) Single-atom output with extensible schema.** The output is one `(skill-set ...)` atom with one string field. Future field additions (return-type, resource-budget, lifecycle-condition, audience metadata) extend the atom in place. Missing fields mean "unspecified," not "forbidden."

**(3) Per-handler resource budgeting deferred to Phase 1.5.** Sprint 0-Coda does not enforce per-handler inference budgets. Phase 1.5 weighs three paths: (a) reduce/2 exception propagation, (b) Error return contract, (c) per-handler inference-limit wrapping. T-2's `call_with_inference_limit 100M` (now active at the metta-call layer) is precedent for path (c). All three are complementary and may all be needed.

**(4) Provenance via typed returns.** Future dispatch-result atoms carry typed return values (e.g., `WRITE-FILE-SUCCESS` per upstream's pattern, not boolean True). Sprint 0-Coda writes a string-typed result; future handlers add return-type metadata to their registration so downstream consumers can pattern-match on outcome quality.

**(5) Lifecycle extensibility from Phase A.** The dispatcher's match pattern queries `lifecycle: active` specifically. Future lifecycle values (deprecated, suspended, pending-replacement) become available without dispatcher code changes; capabilities with non-active lifecycle become invisible to dispatch but remain in atomspace for inspection or retirement. In pipe/flow terms: pipes can be retired without removal; flow stops but the pipe structure remains queryable.

**(6) Operational metadata position.** The schema includes a `metadata: $m` field with initial empty/null seed value. Taxonomy (e.g., `irreversibility: high`, `audience: soul-state-consumer`) is deferred to first concrete consumer needs, expected to be the soul-state-producer work-package. The position is load-bearing; the contents fill incrementally.

---

## 6. Registration

One `(registered-capability ...)` atom is added to `soul/capabilities/skill_discovery.metta`. The directory `soul/capabilities/` is new this sprint, created to house per-capability files separately from soul/ general infrastructure.

The registration:

```
(registered-capability
   schema: (skill-request cycle: $k)
   handler: skill-discovery
   priority: 100
   lifecycle: active
   metadata: ())
```

Priority 100 is the initial value for the first production capability; the value is arbitrary at single-capability scale but establishes a numeric scale. Future capabilities register with priorities that produce intentional ordering.

The same file also contains the handler definition (`(= (skill-discovery $request) ...)`) and the formatter helper (`(= (format-skill-set $list) ...)`).

This is the single production registration. Sprint 0-Coda does not bulk-migrate the 14 hardcoded skill descriptions to individual `(registered-capability ...)` atoms; that is Sprint 1+ work that depends on per-skill registrations becoming useful through context-filtering. Bulk migration before context-filtering exists adds translation overhead without filtering benefit.

The registration pattern can generalize from the Phase 1 bridge atom shape `(promoted memory-id $uuid salience $value)`: keyed by identifier, with salience/priority value, lifecycle metadata, queryable via match-collapse. This is empirical precedent, not abstract design.

---

## 7. Wiring

Phase C lands three coordinated changes in one commit per Discipline 4:

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

The `gensym-invocation-id` is whatever invocation-id-generation primitive the dispatcher uses for per-invocation isolation (per ADR-006 and v3.3 Section 5).

### Change 4: Artifact 1 update

`docs/design/artifact_1_loop_metta_wiring_diagram.md` gets:

- Line-number drift fix (per Sprint 0 verification findings; current source has drifted from documented line numbers due to diagnostic-prints, Phase 1 merge, and other commits)
- New section documenting the skill-discovery dispatch insertion in getContext
- Cross-reference to this Phase A document

All four changes (one new file, one manifest update, one loop.metta edit, one artifact_1 update) land in a single commit per Discipline 4. The commit also includes the line-number drift fix because that drift was discovered during this sprint and addressing it now is cleaner than scheduling separate housekeeping.

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

A minor expectation: with the unquoted-convention switch in skill descriptions (Section 5), apostrophe-and-paren character density decreases, which should reduce `_apostrophe_` encoding overhead. CHARS_SENT may decrease slightly. This is the convention switch's hidden stability benefit, not a parity violation.

### Sprint 0-Coda success criteria as pipe-flow validation

Every criterion below checks one of two things: does the pipe exist, and does correct flow pass through it. This pattern generalizes to every future capability's verification.

**Criterion P-1: Capability registers — pipe exists in atomspace.** `(registered-capability schema: (skill-request cycle: $k) handler: skill-discovery priority: 100 lifecycle: active metadata: ())` atom is present in atomspace after substrate load. Verifiable via match-and-collapse query on `(registered-capability ...)` atoms.

**Criterion P-2: Dispatch fires — flow enters the pipe.** Each iteration's getContext writes a `(skill-request cycle: $k)` atom that triggers dispatch. Verifiable via println diagnostic or by observing `(dispatch-result ...)` atoms in atomspace after dispatch.

**Criterion P-3: Handler produces correct output — correct flow exits the pipe.** The handler returns a `(skill-set skills: $string)` atom whose string field is the formatted skill list. Verifiable via println diagnostic or atomspace inspection.

**Criterion P-4: Prompt parity — downstream pipe receives equivalent flow.** The SKILLS block in the LLM-facing prompt matches the hardcoded getSkills output (functionally, per the migration sequence above). CHARS_SENT stays within baseline range 38653-38910 (or shows the expected decrease from unquoted-convention switch).

**Criterion P-5: LLM behavior unchanged — downstream behavior validates functional equivalence of flow.** Across some defined number of iterations (Phase B verification will specify the number), the LLM's skill selection and invocation patterns are indistinguishable between pre-Coda and post-Coda runs.

**Criterion P-6: Free Criterion 5 observation — watching for pipe rupture (flow interruption).** During Sprint 0-Coda's runtime period, observe whether the dispatcher's known limitation (Criterion 5: handler crash kills the chain silently) actually fires in production. Sprint 0-Coda is the first production use of the dispatcher; this is the empirical window. Findings recorded; no action required unless the limitation fires.

The criteria are scoped to Sprint 0-Coda. Sprint 1's expansion of registry use generates new criteria, not modifications to these.

### Proof claim refinement (structural vs semantic verification boundary)

The earlier framing "Sprint 0-Coda proves shape under bypass conditions; truth-preservation gets exercised in Sprint 1" creates an interpretive risk: a reader could conclude Phase D verification only checks structural integrity, not semantic correctness, leaving Sprint 1 with an underspecified verification obligation.

The boundary is explicit in v2:

**Phase D verifies bypass patterns preserve structural invariants (atoms written match atoms readable, no data loss round-trip).**

**Sprint 1 verifies truth-preservation under production load (semantic coherence under drift).**

The two are distinct verification operations. Phase D operates at the pipe level: does the pipe exist, does flow enter, does correct flow exit, does the downstream pipe receive equivalent flow. Sprint 1 operates at the flow-content level: does the meaning carried by the flow remain coherent across iterations, across user contexts, across the soul intercept chain's evaluations.

Both are necessary. Neither is sufficient. This is Section 0's corrective check applied to verification scope.

### Phase D verification script

A `phase_d_coda_verification.py` script will be drafted in Phase B. Following the Sprint 0 verification pattern: self-contained, inlines preamble, runs criteria 1-6 in sequence, reports PASS/FAIL/limitation for each.

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
| 1 | Registration via atoms | File-load via manifest | Runtime add-atom (mechanism demonstrated via Phase 1 bridge end-to-end; empirical precedent in `(promoted memory-id $uuid salience $value)` shape; available for capability registration) | New pipes can be added at runtime; flow-compatible extension |
| 2 | Single-atom output | One `(skill-set ...)` with one string field | Field additions in place (return-type, resource-budget, etc.) | The pipe's output shape can grow; flow can carry more without breaking downstream |
| 3 | Per-handler resource budgeting | Deferred to Phase 1.5 | Three viable paths weighed empirically; T-2's 100M precedent active at metta-call layer | Flow can be throttled per pipe |
| 4 | Provenance via typed returns | String-typed result | Named-symbol returns per upstream pattern | Flow carries self-describing type information |
| 5 | Lifecycle extensibility | Query `lifecycle: active` specifically | Other values invisible to dispatch but inspectable | Pipes can be retired without removal; flow stops but structure remains inspectable |
| 6 | Operational metadata position | Empty/null seed value | Taxonomy fills with first concrete consumer (likely soul-state-producer) | Pipes can carry self-describing governance information |

---

## 11. Phase A → Phase B transition criteria

Phase A completes when:

- This document is finalized through iteration (v1 → vN per Sprint 0's pattern)
- Clarity has reviewed and concurred with the design (or pushed back with specific structural objections that are resolved before Phase B begins)
- The contract (Section 5) and registration shape (Section 6) are locked
- The wiring plan (Section 7) is concrete enough to draft an apply script against
- The verification criteria (Section 8) are specific enough to draft a Phase D script against

Phase B begins by drafting the Phase D verification script first (test-first discipline for empirically-iterative sprints), then iterating the substrate code against the verification.

---

## 12. Open items list

Items decided but not blocking Phase A finalization. Status updates as of f37aa6c:

**Memory-layer adoption (promote/demote and related upstream evolutions).** CLOSED at commit `f37aa6c`. Phase 1 memory-layer merge from patham9/mettaclaw upstream landed via py-script (`apply_phase1_memory_layer_merge.py`). Promote/demote MeTTa functions, persistence-with-curation primitive, SQLite-to-atomspace bridge, T-2 bounded execution, T-4 history-write expansion, T-3 Configuration B (query-promoted opt-in) all operational. End-to-end verified. T-1 cost instrumentation parked at commit `634b3f1` for future re-activation. T-5 normalization simplification deferred pending pipeline audit. See Section 3 for substrate state details.

**Soul-state producer work-package.** Updated as of f37aa6c. The work-package is the flow translator for Boundary 1 (Section 2: soul intercept output → atomspace). Persistence-with-curation primitive is now operational, providing the producer an additional flow-translation path: aged-out soul state can be curated via promote/demote, with substrate-observable state available via the bridge atom shape. The "how does aged-out soul state get pruned" question has a substrate answer. The work-package is scheduled between Sprint 0-Coda close and Sprint 1 open per Clarity's sequencing-axiom decision; its detailed design begins after Sprint 0-Coda Phase D verifies. Per Section 0's governance-flow privilege: this work-package is higher-priority than informational-flow translation work because soul outputs include governance verdicts.

**Tier-B follow-up items.** B3 (history-write condition) CLOSED at commit `f37aa6c` as T-4 of the Phase 1 merge. B4 (response-normalization-pipeline simplification = T-5) remains deferred pending pipeline audit per merge design v1 Section 9.

**(cut) resolution mechanism.** Tentatively confirmed as Prolog runtime bridge via parallel-substrate evidence (upstream Patrick has the same configuration and his system works). Empirically verified by iteration completion in our runtime. Not blocking; logged.

**Section 6 of fork_additions_runtime_audit_2026-05-18.md.** Several verification needs remain open from that document (wakeupInterval actual production value, self-check-guidance retirement status, idle_directive ownership, balance_parentheses apostrophe asymmetry, last upstream merge date, production memory pressure observation, pin substrate-side state). None blocks Sprint 0-Coda.

**ADR-008 full write-up.** Sprint 0-Coda close-out. Extracted from this Phase A v(final) document's Section 2.

**ADR-009 full write-up.** Sprint 0-Coda close-out. Extracted from this Phase A v(final) document's Section 0 (the Substrate Fractal Invariant: pipes-and-flows-and-meta-awareness as the organizing principle, with ADR-007 as one specific application and ADR-008 as the two-dispatcher consequence).

---

## 13. Versioning and iteration

This is v2. Per Sprint 0's iteration pattern, expect v3, vN as Clarity and Berton review. The document iterates in place; section content evolves while section structure stays stable. When v(final) lands, ADR-008 and ADR-009 extract.

The numbering convention is sprint_0_coda_phase_a_v1.md → sprint_0_coda_phase_a_v2.md → etc.; the file lives at `docs/sprints/00_capability_registry/sprint_0_coda_phase_a_v2.md` (and successors at the same path with version-bumped suffix, parallel to Sprint 0's v3_0 → v3_3 trajectory).

**v1 → v2 changes:**

- New Section 0: Organizing principle (pipes, flows, meta-awareness, fractal recurrence, drift tendency, memory criterion, governance flow as privileged subset)
- Section 1: framing updated with Phase 1 merge context
- Section 2: reframed under pipe/flow lens; two-dispatcher architecture as fixed-value pipe + extensible pipe with asymmetric flow direction; flow translation boundaries named (Boundary 1 unresolved, Boundary 2 resolved at f37aa6c); architectural significance of Option A bridge choice; meta-awareness and governance-flow privilege subsection added
- Section 3: HEAD reference advanced to f37aa6c; new Phase 1 memory-layer merge subsection; empirical precedent paragraph for Phase 1 bridge atom shape
- Section 4: sequencing axiom restated in pipe/flow terms
- Section 5: contract reframed as pipe receiving and emitting flow; empty-context behavior reframed as unvalidated pipe + old pipe carrying flow; commitment 1 updated with Phase 1 bridge empirical demonstration
- Section 6: registration with empirical precedent note from Phase 1 bridge
- Section 8: six criteria reframed as pipe-exists-and-carries-correct-flow checks; proof claim refinement boundary made explicit (Phase D = structural invariants; Sprint 1 = semantic coherence under drift)
- Section 9: Criterion 5 framed as pipe rupture detection
- Section 10: table updated with Pipe-evolution property column; row 1 future shape updated to reflect Phase 1 bridge demonstration
- Section 12: memory-layer adoption CLOSED; soul-state producer work-package updated with persistence-with-curation availability and governance-flow priority; B3 CLOSED; B4 still deferred; ADR-009 added
- Section 13: this section

---

## Document end

This Phase A v2 design document drives the implementation. ADR-008 and ADR-009 extract at close-out. Each architectural claim in Section 2 is testable in substrate or commit history. Each verification criterion in Section 8 maps to an empirical check the Phase D script will perform. Section 0 names the organizing principle the rest of the document instantiates.

Sprint 0-Coda finishes what Sprint 0 Phase 1 scoped. The capability registry's value proposition becomes empirically visible in production: substrate-observable dispatch, registered capabilities as data not code, producer-consumer relationships made visible, governance flow distinguished from informational flow. The first production capability lands. The path to Sprint 1's capability authoring opens.

The pipes/flows/meta-awareness lens means design decisions made here are not local. They are instances of the same structural principle that governs every level of ClarityOmega. Correct pipe/flow separation here validates the pattern everywhere. The drift tendency means structural analysis without flow analysis is the failure mode; the corrective is asking both questions (shape and truth) at every seam. The memory criterion means this document should carry world knowledge that changes future reasoning, not flat records of what was decided.
