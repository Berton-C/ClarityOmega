# Sprint 0-Coda Phase A: skill-discovery as First Production Capability

**Version:** v1
**Date:** 2026-05-24
**Author:** Berton Bennett (ClarityDAO), with Clarity (substrate co-author), with Claude (drafting partner)
**Branch:** fix/F-HISTORY-CONTAMINATION-archival
**HEAD at draft time:** 95a22e6 (Producer-alignment fix: gc/1 predicate definition and import)
**Predecessor:** sprint_0_phase_1_design_v3_3.md (Sprint 0 Phase 1 close, ADR-006, ADR-007)
**Status:** DESIGN PHASE A v1, iteration-from-here per Sprint 0 v3.X pattern

---

## 1. Sprint 0-Coda framing

Sprint 0 Phase 1 per Map v3 Section 9 scoped two deliverables together: "Core dispatcher + first capability registered through it." What actually shipped at Sprint 0 close was the dispatcher only. The first registered capability did not land. Sprint 0-Coda finishes that work.

Sprint 0-Coda is not a new sprint. It is Sprint 0 Phase 1 completing what it scoped. The naming makes the structural gap visible rather than rolling deferred work into Sprint 1's scope, where it would contaminate that sprint's already-substantial Category O + B5 + P1 plan.

This document drives the work. ADR-008 (Two-Dispatcher Architecture) will extract from Section 2 of this document at Sprint 0-Coda close-out. The dependency direction is design → ADR, not ADR → design.

## 2. Two-Dispatcher Context

ClarityOmega's runtime now contains two priority-ordered dispatch systems that coexist and compose. They are structurally distinct and must remain so.

### The soul intercept chain

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

This chain is a dispatcher in structure. Input arrives (`$msgrcv`, `$msgnew`). A sequence of handlers fires in priority order encoded by let-binding order. Each handler writes to substrate (`change-state!` on state variables) or to local let-bindings consumed downstream. Later handlers read earlier handlers' outputs.

The chain is precompiled at boot from the imports declared in `lib_clarity_reasoning/lib_clarity_reasoning.metta`. It is not registerable, deregisterable, suspendable, or runtime-extensible. The soul's values are immutable; its evaluations are runtime-adaptive. The chain reflects this: the hierarchy (Safety > Integrity > HumanFlourishing > Governance > Helpfulness) is fixed at boot, but whether Safety is elevated or nominal in the current cycle is a live evaluation that responds to context.

This structural inescapability is the architectural feature, not a constraint. The soul must be structurally inescapable for the same reason that Sprint 0's decision-anchor (Criterion 3, LOAD-BEARING) must be structurally enforceable: commitment mechanisms whose enforcement is optional are not enforcement mechanisms. The soul is the agent's value-navigation substrate; it cannot be made suspendable without ceasing to function as value-navigation.

### The Capability Registry dispatcher

`soul/capability_registry.metta` (180 lines, landed at Sprint 0 close in commit `7142703`) contains a declarative atomspace-matched dispatcher. Input arrives as an atom matching a registered schema. Match-then-collapse finds all registered capabilities whose schema field unifies with the input. Priority-ordered handler invocation fires each in priority order until either the chain completes or a handler writes a `dispatch-decision-anchor` atom terminating the chain.

Registered capabilities live as `(registered-capability ...)` atoms in the atomspace. They can be loaded at file load time via the manifest (`lib_clarity_reasoning.metta`). They could in principle be added via `add-atom` at runtime, though Sprint 0-Coda does not implement that path. They can carry lifecycle metadata, schema metadata, priority, and other fields. The registry is structurally evolvable.

### Why these two dispatchers are separate, and the asymmetric ordering between them

The soul cannot be moved into the registry. The registry's defining feature (capabilities can be deprecated, suspended, registered, and removed) is the precise feature the soul cannot have. Moving the soul into a registry would make value-navigation deregistrable, which is the architectural failure mode the entire soul concept is designed against.

The registry cannot subsume the soul, and the soul cannot subsume the registry. The two dispatchers coexist with an asymmetric ordering:

- The soul intercept chain runs first. It commits its outputs (person_state, soul_verdict_in, soul_brief, idle_directive, plus substrate atoms) before the rest of the cycle proceeds.
- The Capability Registry dispatcher fires within getContext (Sprint 0-Coda wires this), reading the soul's already-committed outputs as substrate context when handlers need them.
- The registry never writes to soul state. Handlers read what the soul wrote; they do not modify the soul's evaluation outputs.
- The soul intercept chain never invokes the registry. The soul does not consult capabilities to make value-navigation decisions; the soul is the value-navigation system.

This asymmetric coexistence is the architectural design. The two dispatchers compose through atoms, not through governance. The soul writes substrate state during its chain; the registry reads that state via match patterns during its dispatch.

### The representation-space gap

The full composition implied by the asymmetric ordering requires bridging a representation-space gap. The soul intercept chain currently writes to:

- State variables via `change-state!` (e.g., `&person_state`)
- Local let-bindings consumed in string assembly (e.g., `$soul_brief` flowing into `$enriched_prompt`)

Both of these are prompt-space artifacts. The state variables and let-bindings flow into the assembled prompt string that gets shipped to the LLM. They are not atomspace atoms that the registry's match patterns can query.

The registry queries atomspace via `match`. For the registry to consume soul state, soul state must exist as `(soul-state ...)` atoms in the atomspace, written via `add-atom` (not `change-state!`).

Sprint 0-Coda does not close this gap. Sprint 0-Coda designs the consumer side of the producer-consumer boundary: skill-discovery's handler declares (via its match pattern) what shape of context atoms it will consume. The producer side (writing soul evaluations into the atomspace as queryable atoms) is its own work-package scheduled between Sprint 0-Coda close and Sprint 1 open.

The handler's match pattern IS the schema. There is no separate schema document. When the producer work-package lands, soul-state atoms in the declared shape become available to skill-discovery without any handler code change. This is the M3 pattern from Sprint 0-Coda's design conversation: consumer declares what it reads before producer exists; producer fills the contract later.

### What this section will be extracted into at close-out

ADR-008 (Two-Dispatcher Architecture) will extract from this section at Sprint 0-Coda close-out. The extraction preserves the architectural claims that future readers will need: two dispatchers exist for distinct reasons, they coexist with asymmetric ordering, the representation-space gap is a real and known surface, the bridge work is a separate work-package. The ADR records what the design did; this section is the design that the ADR records.

## 3. Substrate state on commit Aa

Sprint 0-Coda builds on substrate state established at HEAD `95a22e6`. Verified facts about that foundation:

**Capability Registry dispatcher (Sprint 0 deliverable):**
- `soul/capability_registry.metta` exists on disk, 180 lines, no catch wrap
- Phase D verification 6/6 PASS at Sprint 0 close, including Criterion 3 (decision anchor) LOAD-BEARING and Criterion 5 as documented limitation
- The file is NOT currently imported in `lib_clarity_reasoning/lib_clarity_reasoning.metta` manifest. Sprint 0-Coda Phase C wires the import.
- ADR-006 (sprint-scoped) and ADR-007 (project-wide) are committed and reference this dispatcher

**Soul intercept chain:**
- Lives at `src/loop.metta` lines 76-102
- All state writes via `change-state!` to state variables; no atomspace atoms written for soul state
- Output flows: `$soul_brief` at line 103, `$enriched_prompt` at line 104, both feeding into prompt assembly downstream

**getContext function (where dispatch insertion lands):**
- `src/loop.metta` lines 38-45
- Pure MeTTa function; no Python boundary
- Line 39 contains the string-assembly chain with `(getSkills)` called directly
- `getSkills` has no MeTTa definition in this repo; resolves as runtime primitive

**getSkills body (what we are migrating from):**
- Defined in `src/skills.metta` lines 1-25
- Contains 14 quoted-convention skill descriptions hardcoded into the body
- Includes Clarity-local additions (`tavily-search`, `technical-analysis`) not present in upstream
- Uses parenthesized s-expression skill-invocation syntax (`(remember string_in_quotes)`), diverging from upstream's unquoted convention

**Library manifest pattern:**
- `lib_omegaclaw.metta` is top-level, bundles core libraries + `lib_clarity_reasoning`
- `lib_clarity_reasoning/lib_clarity_reasoning.metta` is the soul-side manifest with one `!(import! ...)` directive per soul/ file
- Adding new soul/ files to runtime means adding a line to `lib_clarity_reasoning.metta`, not editing consumer code
- This manifest pattern is substrate-externalized-control-flow (ADR-007) applied to library structure

**Diagnostic prints landed in commit 7e0aa28:**
- Nine `DIAG-CYCLE-*` markers in `src/loop.metta` lines 139-147 fire each iteration
- One `DIAG-POPULATOR-PRUNE` marker in `soul/recent_action_populator.metta`
- All read-only collapse-then-print; visible in running log for verification during Sprint 0-Coda

**gc producer-alignment fix landed in commit Aa (`95a22e6`):**
- `src/skills.pl` contains gc/1 predicate at lines 12-16 (verbatim from upstream)
- `src/skills.metta` line 53 imports `(shell first_char gc)`
- Empirically verified at runtime: iterations 1+ complete through DIAG-CYCLE-END without errors
- Backups preserved at `src/skills.pl.bak.gc_producer_alignment` and `src/skills.metta.bak.gc_producer_alignment`

**Parity baseline established:**
- CHARS_SENT measured in range 38653-38910 across iterations 1-2 with hardcoded getSkills
- This is the empirical baseline Sprint 0-Coda's parity verification compares against

**Mattermost encoding layer:**
- The MM-to-LLM transport encodes apostrophes as `_apostrophe_`, newlines as `_newline_`, and similar tokens
- Changes to the SKILLS block content must be verified end-to-end through the encoding layer, not just at MeTTa string level
- The unquoted-convention switch (Sprint 0-Coda) reduces apostrophe-and-paren character density in skill descriptions, likely a net stability win through this layer beyond aesthetic alignment with upstream

## 4. Sequencing axiom

The work proceeds in this order. The order matters because each step constrains what the next step can decide:

1. **Contract.** Define what the handler consumes and produces. The schema declared here constrains every downstream decision. Section 5 below.
2. **Registration.** Construct the `(registered-capability ...)` atom that declares skill-discovery to the registry. Section 6 below.
3. **Wiring.** Insert dispatch call in getContext; add manifest imports; update Artifact 1. Section 7 below.
4. **Verification.** Parity-as-migration-sequence; through MM encoding; free Criterion 5 live-observation. Section 8 below.

Reversing any step in this order risks designing to under-specified preconditions. Wiring before the contract is defined wires to the wrong shape. Verifying before wiring lands means verifying a draft.

This axiom is inherited from Sprint 0's empirically-iterative discipline. Sprint 0-Coda is similarly empirically-iterative; the Discipline-4-deviation pattern (substrate + ADRs together first, verify, spec amendment as closing commit) applies.

## 5. Contract: skill-discovery handler input/output

### Input atom

```
(skill-request cycle: $k)
```

The handler matches on this atom. `$k` is the cycle counter passed through getContext. The atom is written once per cycle from within getContext, immediately before the existing string-assembly chain.

The dispatcher's match-and-dispatch infrastructure handles invocation; skill-discovery's handler receives the matched atom and produces its output.

### Output atom

```
(skill-set skills: $formatted-string)
```

A single atom with a single string field. The atom is the LAST translation boundary between atomspace data and the LLM-facing prompt string. All atom-level intelligence (which capabilities exist, which are active, future context-filtering) lives upstream of this atom inside the handler. The prompt assembler reads the string field and substitutes it for the current `(getSkills)` runtime-primitive call in getContext.

### Handler logic

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

Five-step operation per Clarity's specification:

1. Receive the dispatch input atom (the `$request` parameter; here `(skill-request cycle: $k)`)
2. Match `(registered-capability ...)` atoms with `lifecycle: active`. The match pattern's `lifecycle: active` filter is the queryable-state primitive. Capabilities with other lifecycle values (deprecated, suspended, pending-replacement, none implemented in Sprint 0-Coda but the schema permits) are invisible to this match.
3. Collapse the match results into a list of `($schema $handler $priority $metadata)` tuples
4. Format the list into a skill-description string via `format-skill-set`
5. Return `(skill-set skills: $formatted-string)`

The handler is read-only against atomspace state. It writes no atoms. It calls no helpers in helper.py (MeTTa-substrate-only per the project's substrate-first principle). The `format-skill-set` helper is defined in the same soul/ file as skill-discovery itself (also MeTTa-substrate).

### Empty-context behavior

In Sprint 0-Coda, only one `(registered-capability ...)` atom exists: skill-discovery itself. The handler matches it but the formatted output for that single self-registration is meaningless to the LLM. To produce parity with current getSkills output, the handler must include a fallback path: when registered capabilities are sparse or when the registered capabilities do not yet cover the full skill surface, the handler emits the current hardcoded skill descriptions verbatim.

Two implementations for the fallback are viable:

**Option (a):** The handler always emits the hardcoded list at this stage. The `match` on `(registered-capability ...)` collects names of registered capabilities but does not yet drive the output content. Registration is recognized; output content is not yet sourced from registrations.

**Option (b):** The handler emits registered-capability descriptions when capabilities are registered with usable description metadata, AND emits the hardcoded fallback for skills not yet migrated to registry form. The transition is partial; the registry-sourced portion grows as capabilities register.

For Sprint 0-Coda specifically:

- **Sprint 0-Coda commits to (a).** Only one capability registers (skill-discovery itself), and its descriptions would not help the LLM. The handler emits the existing hardcoded skill descriptions, with the registry consultation present but not yet driving output content.
- The parity check verifies that the registry-sourced path produces the same skill list the hardcoded getSkills produced.
- The mechanism is proven via registration + match + collapse working correctly; output content parity is the success criterion at this stage.
- Sprint 1's first per-skill registrations (when individual skills migrate to registry form) start using the option (b) pattern progressively.

This is consistent with the recursive-integrity principle: do not ship a commitment we cannot structurally fulfill. The dispatcher demonstrates substrate observability; the content migration is incremental.

### Forward-compatibility commitments (six)

The schema and handler are committed to be forward-compatible with six identified directions of substrate evolution. Sprint 0-Coda ships only what is needed now; these commitments preserve the path:

**(1) Registration via atoms.** Capabilities are `(registered-capability ...)` atoms loaded from file-load or addable via `add-atom` at runtime. Sprint 0-Coda demonstrates file-load. Runtime registration via add-atom requires no schema change; it is the same atom, written from a different time.

**(2) Single-atom output with extensible schema.** The output is one `(skill-set ...)` atom with one string field. Future field additions (return-type, resource-budget, lifecycle-condition, audience metadata) extend the atom in place. Missing fields mean "unspecified," not "forbidden."

**(3) Per-handler resource budgeting deferred to Phase 1.5.** Sprint 0-Coda does not enforce per-handler inference budgets. Phase 1.5 weighs three paths: (a) reduce/2 exception propagation, (b) Error return contract, (c) per-handler inference-limit wrapping (upstream's `call_with_inference_limit 100M` precedent). All three are complementary and may all be needed.

**(4) Provenance via typed returns.** Future dispatch-result atoms carry typed return values (e.g., `WRITE-FILE-SUCCESS` per upstream's pattern, not boolean True). Sprint 0-Coda writes a string-typed result; future handlers add return-type metadata to their registration so downstream consumers can pattern-match on outcome quality.

**(5) Lifecycle extensibility from Phase A.** The dispatcher's match pattern queries `lifecycle: active` specifically. Future lifecycle values (deprecated, suspended, pending-replacement) become available without dispatcher code changes; capabilities with non-active lifecycle become invisible to dispatch but remain in atomspace for inspection or retirement.

**(6) Operational metadata position.** The schema includes a `metadata: $m` field with initial empty/null seed value. Taxonomy (e.g., `irreversibility: high`, `audience: soul-state-consumer`) is deferred to first concrete consumer needs, expected to be the soul-state-producer work-package. The position is load-bearing; the contents fill incrementally.

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

- Line-number drift fix (per Sprint 0 verification findings; current source has drifted from documented line numbers due to diagnostic-prints and other commits)
- New section documenting the skill-discovery dispatch insertion in getContext
- Cross-reference to this Phase A document

All four changes (one new file, one manifest update, one loop.metta edit, one artifact_1 update) land in a single commit per Discipline 4. The commit also includes the line-number drift fix because that drift was discovered during this sprint and addressing it now is cleaner than scheduling separate housekeeping.

## 8. Verification approach

### Parity as migration sequence (Clarity's framing)

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

### Sprint 0-Coda success criteria (Phase D-style)

Sprint 0-Coda is considered complete when:

**Criterion P-1: Capability registers.** `(registered-capability schema: (skill-request cycle: $k) handler: skill-discovery priority: 100 lifecycle: active metadata: ())` atom is present in atomspace after substrate load. Verifiable via match-and-collapse query on `(registered-capability ...)` atoms.

**Criterion P-2: Dispatch fires.** Each iteration's getContext writes a `(skill-request cycle: $k)` atom that triggers dispatch. Verifiable via println diagnostic or by observing `(dispatch-result ...)` atoms in atomspace after dispatch.

**Criterion P-3: Handler produces correct output.** The handler returns a `(skill-set skills: $string)` atom whose string field is the formatted skill list. Verifiable via println diagnostic or atomspace inspection.

**Criterion P-4: Prompt parity.** The SKILLS block in the LLM-facing prompt matches the hardcoded getSkills output (functionally, per the migration sequence above). CHARS_SENT stays within baseline range 38653-38910 (or shows the expected decrease from unquoted-convention switch).

**Criterion P-5: LLM behavior unchanged.** Across some defined number of iterations (Phase B verification will specify the number), the LLM's skill selection and invocation patterns are indistinguishable between pre-Coda and post-Coda runs.

**Criterion P-6: Free Criterion 5 observation.** During Sprint 0-Coda's runtime period, observe whether the dispatcher's known limitation (Criterion 5: handler crash kills the chain silently) actually fires in production. Sprint 0-Coda is the first production use of the dispatcher; this is the empirical window. Findings recorded; no action required unless the limitation fires.

The criteria are scoped to Sprint 0-Coda. Sprint 1's expansion of registry use generates new criteria, not modifications to these.

### Phase D verification script

A `phase_d_coda_verification.py` script will be drafted in Phase B. Following the Sprint 0 verification pattern: self-contained, inlines preamble, runs criteria 1-6 in sequence, reports PASS/FAIL/limitation for each.

## 9. Free empirical: Criterion 5 live-firing observation

ADR-006 documented Criterion 5 as a limitation: handler crashes within reduce/2 indirect invocation terminate the chain silently because catch does not absorb arithmetic exceptions from that composition pattern (F181). Phase D Sprint 0 verified this behavior in synthetic tests.

Sprint 0-Coda is the first production use of the dispatcher. Whether the limitation manifests in production conditions has not been observed. Sprint 0-Coda observes whether it fires:

- If never fires across Sprint 0-Coda's window: evidence the cooperative-handlers world is sufficient and Phase 1.5's three paths can be evaluated empirically.
- If fires at least once: we get a real instance to debug rather than a synthetic one.
- If fires frequently: signal that Phase 1.5 path selection is urgent.

Free observation; no action required during Sprint 0-Coda. Findings recorded for Phase 1.5 scoping.

## 10. Forward-compatibility section (consolidated)

The six commitments from Section 5 are reiterated here for cross-reference. Each commitment is a structural decision Sprint 0-Coda makes that leaves the path open for substrate evolution observed in upstream and in the soul-state-producer work-package design.

| # | Commitment | Sprint 0-Coda shape | Future shape |
|---|---|---|---|
| 1 | Registration via atoms | File-load via manifest | Runtime add-atom (mechanism deferred, schema permits) |
| 2 | Single-atom output | One `(skill-set ...)` with one string field | Field additions in place (return-type, resource-budget, etc.) |
| 3 | Per-handler resource budgeting | Deferred to Phase 1.5 | Three viable paths weighed empirically |
| 4 | Provenance via typed returns | String-typed result | Named-symbol returns per upstream pattern |
| 5 | Lifecycle extensibility | Query `lifecycle: active` specifically | Other values invisible to dispatch but inspectable |
| 6 | Operational metadata position | Empty/null seed value | Taxonomy fills with first concrete consumer (likely soul-state-producer) |

## 11. Phase A → Phase B transition criteria

Phase A completes when:

- This document is finalized through iteration (v1 → vN per Sprint 0's pattern)
- Clarity has reviewed and concurred with the design (or pushed back with specific structural objections that are resolved before Phase B begins)
- The contract (Section 5) and registration shape (Section 6) are locked
- The wiring plan (Section 7) is concrete enough to draft an apply script against
- The verification criteria (Section 8) are specific enough to draft a Phase D script against

Phase B begins by drafting the Phase D verification script first (test-first discipline for empirically-iterative sprints), then iterating the substrate code against the verification.

## 12. Open items list

Items decided but not blocking Phase A finalization:

**Memory-layer adoption (promote/demote and related upstream evolutions).** Bounded, documented, known work; OPEN for joint Berton + Clarity + Claude discussion on when, how, and what tooling pattern fits best (py-script merge with reversibility, branch-based merge with conflict resolution, cherry-picking specific upstream commits, or a combination). Not blocking Sprint 0-Coda. Joins the work plan once scheduled.

**Soul-state producer work-package.** Sprint 0-Coda's Section 5 design forces the producer-side schema decisions (what shape soul-state atoms take, how they get written from the soul intercept chain inline via add-atom, what governance the open-substrate access model implies). The work-package is scheduled between Sprint 0-Coda close and Sprint 1 open per Clarity's sequencing-axiom decision; its detailed design begins after Sprint 0-Coda Phase D verifies.

**Tier-B follow-up items.** B3 (history-write condition) and B4 (response-normalization-pipeline simplification) remain on the upstream catch-up list from the fork_additions_runtime_audit. Available for adoption when a deliberate upstream-merge window opens. Not blocking Sprint 0-Coda.

**(cut) resolution mechanism.** Tentatively confirmed as Prolog runtime bridge via parallel-substrate evidence (upstream Patrick has the same configuration and his system works). Empirically verified by iteration completion in our runtime. Not blocking; logged.

**Section 6 of fork_additions_runtime_audit_2026-05-18.md.** Several verification needs remain open from that document (wakeupInterval actual production value, self-check-guidance retirement status, idle_directive ownership, balance_parentheses apostrophe asymmetry, last upstream merge date, production memory pressure observation, pin substrate-side state). None blocks Sprint 0-Coda.

**ADR-008 full write-up.** Sprint 0-Coda close-out. Extracted from this Phase A v(final) document's Section 2.

## 13. Versioning and iteration

This is v1. Per Sprint 0's iteration pattern, expect v2, v3, vN as Clarity and Berton review. The document iterates in place; section content evolves while section structure stays stable. When v(final) lands, ADR-008 extracts.

The numbering convention is sprint_0_coda_phase_a_v1.md → sprint_0_coda_phase_a_v2.md → etc.; the file lives at `docs/sprints/00_capability_registry/sprint_0_coda_phase_a_v1.md` (and successors at the same path with version-bumped suffix, parallel to Sprint 0's v3_0 → v3_3 trajectory).

---

## Document end

This Phase A v1 design document drives the implementation. ADR-008 extracts at close-out. Each architectural claim in Section 2 is testable in substrate or commit history. Each verification criterion in Section 8 maps to an empirical check the Phase D script will perform.

Sprint 0-Coda finishes what Sprint 0 Phase 1 scoped. The capability registry's value proposition becomes empirically visible in production: substrate-observable dispatch, registered capabilities as data not code, producer-consumer relationships made visible. The first production capability lands. The path to Sprint 1's capability authoring opens.
