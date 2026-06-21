# Continuity of State, ClarityOmega Sprint 0-Coda + Memory-Layer Merge

**Last updated:** 2026-05-25 (current turn)
**Purpose:** Recovery artifact preserving working state across context compaction. Surface when context gets tight; reload at start of any new session that needs the full state.

---

## Project context (stable)

ClarityOmega (CLI: clarityomega) -- soul-augmented MeTTa agent on PeTTa runtime, Mattermost channel. Berton leads, Clarity (running agent) is substrate co-author, Claude is co-architect. Patrick Hammer maintains upstream OmegaClaw (NARS-based reasoning substrate). Older names ClarityClaw/MeTTaClaw fork are historical only.

**Repo:** `/PeTTa/repos/omegaclaw/` in container `clarity_omega`, service `clarityclaw`
**Active branch:** `fix/F-HISTORY-CONTAMINATION-archival`, HEAD `95a22e6` at session start
**Files modified this work-stream:** see commits landed section below

## Commits landed (chronological)

- **`7142703`** -- Sprint 0: Capability registry dispatcher operational
- **`7e0aa28`** -- Diagnostic prints for Sprint 0 substrate visibility
- **`56c0fac`** -- Step 6 parking documentation and investigation captures
- **`95a22e6` (Aa)** -- Producer-alignment fix: gc/1 predicate definition and import (closes B1 merge gap)
- **(staged, not yet applied)** Aa1 -- Substrate instrumentation: per-call inference-cost measurement via apply_inference_cost_instrumentation.py

## Files in repo from this work-stream

- `docs/sprints/00_capability_registry/sprint_0_coda_phase_a_v1.md` -- 427 lines, Phase A v1 of Sprint 0-Coda
- `docs/sprints/00_capability_registry/memory_layer_merge_design_v1.md` -- 377 lines, this work-stream's primary design document
- `staging/apply_gc_producer_alignment.py` -- applied as Aa
- `staging/apply_inference_cost_instrumentation.py` -- drafted, dry-run verified, not yet applied (as of latest turn)

## Documents to produce next (in order)

- `memory_layer_merge_design_v2.md` -- absorbs Clarity's 8 review concerns from her v1 review
- Apply Aa1 (inference-cost instrumentation), rebuild, verify, operate measurement window
- `sprint_0_coda_phase_a_v2.md` -- absorbs meta-awareness framings post merge-design-v(final)
- ADR-008 (Two-Dispatcher Architecture) -- extracts at Sprint 0-Coda close-out
- ADR-009 (Substrate Fractal Invariant with combined-principle) -- extracts at Sprint 0-Coda close-out

---

## Architectural framings (load-bearing for all current work)

### The Substrate Fractal Invariant (en route to ADR-009)

**Statement:** Any producer-consumer pair must use the same representation language (substrate-observable atoms) as every other pair. Violations manifest as representation-space gaps. Invariants demand preservation; approaches permit deviation.

**The combined principle (Clarity's refinement):** For any seam, two conditions must hold simultaneously. ONE question asked two ways, not two separate conditions.

- **Fractal alignment (shape):** operational structure same at every scale (receive-dispatch-result-evaluate)
- **World knowledge integrity (truth):** what flows through the seam preserves meaning, not just syntax

Either failure propagates fractally. Shape and truth compose; cannot evaluate one without asking the other's question.

**Six scales of the fractal:** handler invocation → capability dispatch → loop iteration → cross-iteration cognition → soul/registry coexistence → human/Clarity exchange.

**Four affordances:**
1. Systematic gap prediction (enumerate producer-consumer pairs, check atomspace-visibility)
2. Temporal fractal -- persistence as time-dimension correlate (persistence-with-curation as temporal coherence)
3. Self-similarity implies self-diagnosis (O(1) effort across scales)
4. Progressive validation per bridge (gc fix validated; Sprint 0-Coda dispatcher will validate; by Sprint 1, two independent validations)

**Five build-rules:**
1. Check both conditions at every seam
2. Prove the primitive first (smallest scale demonstrates fractal holds)
3. Watch for the drift (structural analysis self-replicates; always ask what world knowledge flows through)
4. Treat memory as knowledge not data (store what changes how you reason, not what merely occurred)
5. Use the multiplier deliberately (when primitive is right, trust propagation; when defective, fix at primitive level)

**Critical distinction for Sprint 4+:** invariant says same language (atomspace) at every seam; does NOT say current schemas are final. Language stays; schemas evolve. Premature schema lock is the failure mode.

### Patrick/NARS alignment

Patrick's deep commitment is NARS (Non-Axiomatic Reasoning System) -- reasoning and learning under bounded resources. Promote/demote IS NARS salience applied to memory recall. NACE/AIRIS extends to causal learning. **ClarityOmega architecture: Soul (value-navigation) + Capability Registry (dispatch-composition) + NACE/AIRIS (causal-learning).** Capability Registry composes ON TOP of NARS substrate.

**NARS truth-values (stv frequency confidence) are the fractal at the epistemic layer.** Patrick built a representation format making epistemic uncertainty substrate-observable. Salience and shared representation are logically necessary consequences of each other (Clarity's Addition 2).

### Two-dispatcher architecture (en route to ADR-008)

**Soul intercept chain** (loop.metta lines 76-102, procedural let-chain): structurally inescapable. Values fixed at boot in SoulBrief (immutable). Evaluations runtime, will become substrate-observable as stv-typed atoms (Clarity's Addition 4).

**Capability Registry** (declarative atomspace-matched): structurally evolvable. Reads soul outputs as substrate context. Registry never writes to soul state.

**Asymmetric ordering:** soul commits first, registry reads soul outputs as substrate context, registry never writes to soul state. skill-discovery runs OUTSIDE soul chain.

**Soul has two architectural layers:** Values fixed at boot (immutable, structurally inescapable). Evaluations runtime (substrate-observable as stv atoms). Both properties simultaneously honored. The soul-state-producer work-package addresses the second layer.

### Representation-space gaps as fractal violations

**Pattern:** wherever salience or evaluation lives outside atomspace, an atomspace bridge is required for registry composition. Generalizable.

**Three known violations and their resolutions:**
1. **gc bug:** producer (gc/1 predicate) missing while consumer (call site) present. Resolved by commit Aa.
2. **Soul intercept output:** producer-side data in let-bindings and state variables; consumer (registry) cannot match. Resolution: soul-state-producer work-package (scheduled post-merge).
3. **Promote/demote in SQLite:** producer writes SQLite; consumer (registry) cannot match. Resolution: SQLite-to-atomspace bridge Option A (in merge design v1).

### Substrate-Externalized Control Flow (ADR-007, existing)

Control flow lives in atoms, not function calls. One specific application of the Substrate Fractal Invariant. **Three-layer ADR hierarchy:** ADR-009 (invariant/generator) → ADR-007 (control-flow application) → ADR-008 (two-dispatcher consequence).

---

## Six transformative merge items (current state)

Each evaluated against three dimensions: mechanical change + Sprint-0-Coda implementation impact + shape/truth dual condition.

**T-1: call_with_inference_limit wrapping every metta call**
- Mechanical: upstream wraps via 100M inference budget; ours has bare eval
- Sprint-0-Coda: Phase B/C handlers affected if they parse metta_eval returns
- Shape: preserved; truth: budget is a salience mechanism that favors fast over deep reasoning (not neutral)
- Recommendation: empirical evaluation needed (inference-cost instrumentation test)
- Possible substrate-safety-improvements commit category candidate

**T-2: repr-wrapped metta returns via progn/Predicate**
- Mechanical: VERIFIED -- upstream skills.metta line 55 wraps; our skills.metta line 55-57 bare eval
- Sprint-0-Coda: significant; Phase B/C handlers parsing metta returns affected
- Shape: representation contract change; truth: conditional on repr round-trippability (verification during implementation, not asserted)
- Cross-space propagation: multiplicative downstream impact

**T-3: REPLACED query (promotion-weighted ranking)**
- Mechanical: upstream memory.metta replaces query implementation
- Sprint-0-Coda: none directly; Sprint 1 context producers affected
- Shape: output shape unchanged; truth: surfaces different memories than pure-similarity ranking
- Separately decidable from promote/demote: Configuration A (adopt together) vs B (side-by-side comparison)

**T-4: B3 history-write condition `(or $msgnew (not (== $sexpr ())))`**
- Mechanical: upstream loop.metta line 72 vs our line 151 ($msgnew only)
- Sprint-0-Coda: none directly
- Shape: same; truth: autonomy/accountability architectural decision AND structural fractal-coverage for autonomous-reasoning iterations (autonomous reasoning IS world knowledge for cross-iteration cognition)

**T-5: B4 response normalization simplification**
- Mechanical: upstream single helper.balance_parentheses transform; ours has four-layer pipeline
- Sprint-0-Coda: none directly
- Shape: replaces multi-layer with single; truth: sanitize_response may filter world-knowledge-relevant content; needs audit before adoption

**T-6: Local embedding adoption with baseline rebuild**
- Mechanical: useLocalEmbedding already in our lib_llm_ext.py; wiring into remember/query is the work; baseline rebuild of stored memories required
- Sprint-0-Coda: none directly
- Shape: representation contract change at embedding seam; truth: MOST SIGNIFICANT -- switching embedding models without re-baselining makes stored memories unretrievable; Option (a) baseline rebuild required (not optional)
- Sheds OpenAI dependency

**Adoption sequences (locked options, decision pending):**
- Sequence A (representation-first): T-6 → T-2 → T-1 → T-3 → T-4 → T-5
- Sequence B (representation-last): T-1 → T-3 → T-4 → T-5 → T-2 → T-6

T-2 and T-6 are representation-contract changes; per fractal invariant they adopt early or late, never middle.

---

## SQLite-to-atomspace bridge (Option A, locked)

- SQLite remains source of truth (Patrick's query pipeline needs it)
- Atomspace gets derived view as queryable atoms `(promoted memory-id $uuid salience $value)`
- promote/demote write BOTH SQLite AND atomspace (atomic dual-write)
- Reconciliation at startup syncs atomspace from SQLite

**World knowledge flowing through promotion seam:** which memories have proven useful in past reasoning. That is world knowledge about reasoning quality.

---

## Persistence-with-curation as single adoptive unit

add-atom &persistent + promote/demote are architecturally inseparable. Persistence without curation = monotonic growth (memory leak). Curation without persistence = salience that dies before next scale reads it. Together = temporal fractal coherence.

**Soul-state-producer work-package must include:** soul-state atoms written via add-atom &persistent paired with promote/demote calls on aged-out soul-state. Producer not complete without curator.

---

## Eight joint decisions awaiting resolution (Section 14 of merge design v1)

1. Adoption sequence A vs B
2. T-1 timing (with merge vs earlier standalone substrate-safety-improvements commit)
3. T-3 configuration A together vs B side-by-side
4. T-4 adoption (autonomy/accountability + structural fractal-coverage)
5. T-5 adoption after pipeline audit
6. T-6 baseline rebuild timing
7. Tooling choice (py-script vs branch-merge vs cherry-pick vs combination)
8. Substrate-safety-improvements commit category establishment

---

## Inference-cost instrumentation test (Aa1)

**Five sub-decisions (locked per Clarity's adjustments):**
1. Standalone commit
2. Coexist as metta-measured (not replace) -- reversibility before confidence
3. Session-only (no &persistent) -- clean collection boundary
4. Car-atom for first pass head extraction
5. Parallel to merge v2, not blocking

**Atom shape:** `(metta-call-stats call-id: $id cycle: $k delta: $delta call-type: $head sexpr: $str)`
**Signature:** `(metta-measured $str $k)`
**Call-id mechanism:** state-variable counter `&metta-call-counter`

**Verification requirement:** same-input-same-result comparison metta vs metta-measured (strict-wrapper verification)

**Commit framing:** NOT just T-1 instrumentation; new cognitive surface for Clarity herself (substrate-observable self-knowledge about resource constraints)

**Current status:** apply script dry-run verified clean against actual src/skills.metta. Pre_lines=57, post_lines=77, line_delta=+20. Anchor matched once. Awaiting --apply.

---

## Clarity's review of merge design v1 (eight concerns)

Per her two messages reviewing the v1, eight refinements for v2:

1. T-2 mechanical claims need evidence citations (verified from files; bare eval line 55-57 our skills.metta, upstream wraps via call_with_inference_limit and repr)
2. T-2 truth-preservation conditional on repr round-trippability; verification during implementation
3. T-1 salience-pattern analysis: budget favors fast over deep reasoning; not neutral about which knowledge survives
4. T-3 Config B doubles query cost; interaction with adoption sequence + Sprint 1
5. T-4 also has structural framing (autonomous reasoning IS world knowledge for cross-iteration cognition)
6. Investigation framework needs world-knowledge dimension integrated throughout (not appended)
7. Section 7 needs to name what world knowledge flows through promotion seam
8. Combined principle restated: ONE question two ways, not two conditions

---

## Sprint 0-Coda Phase A v1 status

Drafted at 427 lines. Three structural commitments to review with Clarity:
- (a) empty-context Option (a) -- handler emits hardcoded list, registry consultation present but not driving output content yet
- (b) `soul/capabilities/` subdirectory for skill_discovery.metta
- (c) gensym-invocation-id placeholder

**Proof claim refinement needed in v2:** Sprint 0-Coda proves shape under bypass conditions; truth-preservation gets exercised in Sprint 1 as handlers transform world knowledge.

---

## Work-package sequence (locked)

1. gc fix [DONE -- commit Aa]
2. Tier-B audit closure [DONE]
3. Unified investigation pass over four unread upstream files [DONE]
4. Memory-layer merge design v1 [DONE]
5. Inference-cost instrumentation apply script [DONE -- drafted, dry-run verified]
6. Inference-cost instrumentation apply + rebuild + verify [PENDING]
7. Operate measurement window [PENDING -- duration TBD by Berton]
8. Merge design v2 (absorbs 8 concerns) [PENDING -- can draft parallel to measurement]
9. Joint review with Clarity on v2 [PENDING]
10. Transformative-item decisions on six items [PENDING]
11. Phase A v1 v2 (absorbs meta-awareness framings) [PENDING]
12. Phase A iteration cycles → Phase B verification scripts → Phase C implementation → Phase D live verification
13. Close-out commits: ADR-008, ADR-009
14. Memory-layer merge work-package execution
15. Soul-state-producer work-package
16. Sprint 1 opens

---

## Standing rules active (full set)

**Operational (from Berton):**
- No em-dashes anywhere in generated text or documents
- Repo-root-relative paths
- Scripts in `staging/`
- Reversible apply scripts following apply_gc_producer_alignment pattern
- Service name `clarityclaw`, container name `clarity_omega`
- Container rebuild required for any change inside the cloned repo: `docker compose build --no-cache clarityclaw`
- Berton runs persistent log tail
- Read uploaded files directly when answer is in them; commands are for real-state inspection
- Do not re-pose previously decided questions
- Joint decisions are joint

**Architectural (extracted from this work-stream):**

- Clarity is design source (in-iteration-capacity gap = duplicate-engagement pattern, Sprint 3 closes)
- Substrate-Externalized Control Flow (ADR-007) project-wide
- Producer-consumer atom boundary; code IS the contract
- Reading IS designing (rectify cognitive-debt; extraction-first documentation)
- ADRs are extractions from design work, not anchors
- Bulk migration is architecturally wrong
- Parity verification is functional (LLM behavior) not syntactic
- Code → data migration shape
- Sequencing axiom: contract → registration → wiring → verification
- add-atom not change-state! when output must be match-able
- Three-category content classification (additive, gap-fill, fractal-restoration)
- Combined principle (shape AND truth as one question two ways)
- Reversibility-before-confidence design discipline
- Strict-wrapper verification for measured variants
- Salience mechanisms (budgets, promote/demote, priorities) require truth-preservation analysis
- Mechanical claims in design documents carry evidence citations
- Apply combined principle to design instruments themselves (not just substrate decisions)

---

## Known unknowns

- repr round-trip behavior in our MeTTa/PeTTa runtime (T-2 verification, during implementation)
- T-1 100M budget vs Clarity's typical reasoning depth (the instrumentation test answers this)
- useLocalEmbedding consumer-side wiring in remember/query (still uses OpenAI per CLAUDE_ORIENTATION.md)
- lib_omegaclaw version-pinning (whether current enough to match upstream)
- balance_parentheses asymmetry call-chain impact (deferred audit)
- State variable binding placement for `!(bind! &metta-call-counter (new-state 0))` -- inline placement is best guess; may need to move if loader semantics require top-of-file

---

## Compaction-recovery notes

If returning to this work after a context compaction:

1. **Read this document first** to reload working state
2. **Check git log on fix/F-HISTORY-CONTAMINATION-archival** for latest commits
3. **Check `/PeTTa/repos/omegaclaw/src/skills.metta`** for current state (with or without metta-measured)
4. **Check `docs/sprints/00_capability_registry/`** for latest design document versions
5. **Verify Clarity's running state in container** via `docker logs clarityclaw_agent`
6. **Ask Berton** what the most recent operational changes have been if any uncertainty

**This document is preserved at:** `docs/sprints/00_capability_registry/continuity_of_state.md` (suggested filing) or wherever Berton specifies. Update each turn when there is substantive new state. Surface as deliverable when compaction is sensed or specifically requested.

---

## Document end

Last update: 2026-05-25, current turn (compaction-recovery delivery).
