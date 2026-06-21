# Memory-Layer Merge Design v1

**Version:** v1
**Date:** 2026-05-24
**Author:** Berton Bennett (ClarityDAO), with Clarity (substrate co-author), with Claude (drafting partner)
**Branch:** fix/F-HISTORY-CONTAMINATION-archival
**HEAD at draft time:** 95a22e6 (Producer-alignment fix: gc/1 predicate definition and import)
**Predecessor documents:** sprint_0_phase_1_design_v3_3.md, sprint_0_coda_phase_a_v1.md, fork_additions_runtime_audit_2026-05-18.md
**Status:** DESIGN v1, iteration-from-here

---

## 1. Purpose and architectural endpoint

This document scopes the upstream memory-layer merge into ClarityOmega from Patrick Hammer's MeTTaClaw upstream snapshot 2026-05-18. The merge is a parallel work-package scheduled to land between Sprint 0-Coda close and Sprint 1 open.

The merge's purpose is not "adopt upstream features." The purpose is **completing fractal coverage of the substrate so world knowledge flows through every scale at which the agent reasons, without distortion.**

Two conditions must hold simultaneously at every producer-consumer seam in the substrate:

**Fractal alignment (shape):** the operational structure at the seam matches the operational structure at every other scale. Receive-dispatch-result-evaluate. The loop, the dispatcher, the capability registry, the soul intercept chain, the governance check, the human-Clarity exchange, the per-iteration cognition. Same primitive, different scale.

**World knowledge integrity (truth):** what flows through the seam preserves its meaning, not just its syntax. A representation-contract change that preserves shape but distorts the meaning of what passes through is catastrophic because the distortion propagates fractally.

Either failure produces consistent system-wide wrongness. Shape-correct primitives carrying distorted knowledge yield consistently wrong results at every scale. Truth-preserving primitives with wrong shape yield locally correct results that cannot compose.

The merge's items are evaluated against both conditions. The architectural endpoint is a substrate where:

- The same representation language (atomspace) at every producer-consumer seam
- World knowledge (memory, soul evaluations, NARS truth-values, capability metadata) flows without distortion
- Salience-weighted attention composes across scales because salience is substrate-observable
- The human can audit what the agent is attending to and why, at every layer where the agent reasons

This endpoint guides merge decisions. Each transformative item gets evaluated against whether its adoption advances or retards fractal coverage of both shape and truth.

### 1.1 The drift warning

The investigation phase that produced this document hit a substrate pattern worth naming: structural analysis generates more structural analysis. Pipe-optimization can self-replicate while losing track of the water (world knowledge) flowing through.

Every section of this document maintains a discipline: ask what world knowledge flows through the seam being designed, and what knowledge depends on this representation being intact. If a section cannot answer that question, the section has lost substance for structure and needs revision.

## 2. Investigation framework

The unified investigation pass over the four unread upstream files (utils.metta, lib_nal.metta, lib_llm_ext.py, websearch.py) was conducted prior to this document, alongside reopening the Tier-B audit. The unified pass uses five questions:

1. **Fractal-violation scan:** does this file introduce new representation languages at any seam?
2. **NARS-alignment scan:** does this file contain salience mechanisms we have not accounted for?
3. **Impact scan:** does this file change execution paths that Sprint 0-Coda implementation depends on?
4. **Producer-present scan:** does this file make any substrate-observable state invisible to any known consumer?
5. **Version-pinning scan:** is any consumer in our codebase referencing capabilities that our pinned library versions do not provide?

The five questions are generalizable to any future audit or merge work; the merge design document applies them to upstream memory layer content.

## 3. Investigation findings (audit results from unified pass)

### 3.1 utils.metta
Byte-identical to upstream. No gap. The configure function (line 33-35) makes configuration substrate-observable via add-atom; governance affordance pattern operational. The string-safe function (line 22-23) is the origin of `_apostrophe_` encoding. No merge work required for this file.

### 3.2 lib_nal.metta
Patrick's NARS substrate library. Imported via lib_omegaclaw → lib_nal; not a direct merge target. Truth functions (Truth_Deduction, Truth_Abduction, Truth_Induction, Truth_Revision, etc.) and inference rules NAL-1 through NAL-6. NARS truth-values (stv frequency confidence) are the representation format making epistemic uncertainty substrate-observable. Version-pinning concern: whether our lib_omegaclaw is current enough to match this is a separate audit (Section 9.2).

### 3.3 lib_llm_ext.py
Our fork has divergent class-based refactor with five providers (ASICloud, Anthropic, ASIOne, Friendli/GLM, OpenAI), lazy initialization, registry pattern, GLM thinking-mode fallback. Symmetric encoding/decoding pipeline via _clean_text (apostrophe AND quote reversal). Local embedding (useLocalEmbedding) is already present in our fork. Whether useLocalEmbedding is wired into remember/query consumer-side is a separate verification (Section 9.1). No merge gap.

### 3.4 websearch.py
Byte-identical to ours. No delta.

### 3.5 memory.metta (upstream-only; not yet in our lib_omegaclaw)
The substantial merge surface. Contains:
- promote/demote MeTTa functions
- get-promotion (used by promote, demote, and the replaced query)
- best-promoted-memory-ids, best-promoted-memories
- REPLACED query (promotion-weighted ranking)
- New configure parameters (promotionInflationFactor 10, mostPromotedMemories 10)
- initMemory change: now calls promotion_open_map() at boot

### 3.6 helper.py promotion infrastructure
Upstream's helper.py adds SQLite-backed promotion store with WAL journaling and eight helper functions (promotion_open_map, promotion_key, promotion_set_value, promotion_get_value, promotion_get_all_keys, promotion_set_lasttime, promotion_get_lasttime, promotion_has_key, promotion_delete_key, promotion_commit, promotion_close_map). Plus extended balance_parentheses with two-arg-command handling and filename quote-detection.

Our balance_parentheses currently reverses only `_quote_` (not `_newline_`, not `_apostrophe_`). Whether the asymmetry produces real bugs depends on call-chain composition with _clean_text; deferred audit (Section 9.3).

### 3.7 Tier-B audit (reopened, now closed)
B1 (`6ebba7a`): gc gap closed by Aa (`95a22e6`). cut presumed Prolog built-in via bridge (upstream parallel-substrate evidence supports this).
A1 (`0872ec1`): spamShield three integration points landed cleanly. Empirically firing.
A2 (`f46e44e`): single-value config change. Empirically firing.
Bug 2/2b (`2fc066a`): Tier-C fix, out of merge-audit scope.

One gap found across the audit (gc). Now closed. Producer-alignment-fixes commit category has one permanent member: Aa.

## 4. Content classification

Three categories of merge content, distinguished by how they relate to current substrate state:

**Additive:** new capability not currently in our substrate. No producer-consumer relationship to existing code in our repo. Merge cleanly without behavioral change to existing paths.

**Gap-fill:** producer exists upstream but is missing in our substrate while a consumer already exists. Same shape as the gc fix (commit Aa). Restores fractal alignment where one side of the seam was empty.

**Fractal-restoration:** pre-existing fractal violation in our current code that the merge heals. The violation already produces inconsistent behavior; the merge brings it into alignment. Distinct from gap-fill because the current state is broken, not merely incomplete.

### 4.1 Additive items

Items that merge cleanly with no representation contract changes at existing seams:

- **Promotion store SQLite infrastructure** (helper.py: 8 helper functions, WAL journaling, kv table schema, promotion_open_map called at boot via initMemory). New persistent storage layer; no existing consumer depends on it.
- **promote/demote MeTTa functions** (memory.metta). Substrate primitives that don't yet have consumers in our substrate. Adoption creates the producer side; consumers come later (Sprint 1+ capabilities, soul-state producer work-package).
- **get-promotion, best-promoted-memory-ids, best-promoted-memories MeTTa functions** (memory.metta lines 53-74). Read-only utility functions accessing the promotion store.
- **promotionInflationFactor and mostPromotedMemories configure parameters** (memory.metta lines 19-20). New configure values via the existing configure pattern.
- **Persistent atomspace primitives** (add-atom &persistent, get-atoms &persistent). New mechanism; no existing consumers depend on persistence semantics.
- **extract_timestamp, around_time** (helper.py). Episode-by-timestamp search functions; we may already have similar, but addition is cleanly additive.
- **promotion test suite** (helper.py __main__ block). Self-contained tests against the SQLite promotion store.

### 4.2 Gap-fill items
None identified beyond what Aa already closed.

### 4.3 Fractal-restoration items
The balance_parentheses asymmetry is a candidate (Section 9.3) but its real-world impact depends on call-chain composition. Verification before declaring it a restoration item. Not in the merge's critical path.

### 4.4 Transformative items
Items that change existing behavior, affect code we're about to build, or alter representation contracts at existing seams. Each requires individual adopt/defer/reject decision with three-dimensional analysis. Section 5 below.

## 5. Transformative items (six)

Each item gets three-dimensional analysis: **mechanical change** (what changes in code), **Sprint-0-Coda implementation impact** (does this affect what Phase B/C will write), and **two-condition impact** (shape impact AND truth impact under Clarity's combined principle).

### T-1: call_with_inference_limit wrapping every metta call

**Mechanical change:** Upstream wraps `(metta $str)` evaluation in `call_with_inference_limit 100000000`. Per-call inference budget. Hard cap on cognition per skill invocation. Our metta function definition currently has bare eval with no limit.

**Sprint-0-Coda impact:** Phase B/C handlers invoke metta_eval. The inference limit changes failure semantics (limited-then-fail vs run-forever). If Phase D verification runs against the unwrapped path then we adopt the wrapper, behavior changes.

**Shape impact:** Adds safety constraint at the existing metta-eval seam. Does not change representation language. Fractal preserved.

**Truth impact:** A call that times out under the limit produces no result (or an error result, depending on how the limit fires). World knowledge that would have come from the call is absent in the bounded version. **The knowledge that gets through is the same; the knowledge that doesn't get through gets bounded.** Truth at the seam is preserved for successful calls; failed calls produce honest "incomplete" output rather than runaway computation. This is integrity-positive: bounded computation produces bounded-truthful results rather than possibly-distorted-on-the-way-to-eventual-failure results.

**Recommendation context:** Safety-positive change. Warrants earlier adoption regardless of merge timing. Possible candidate for substrate-safety-improvements commit category alongside producer-alignment-fixes. Open decision: adopt with merge, or adopt earlier as standalone safety commit.

### T-2: repr-wrapped metta returns via progn/Predicate

**Mechanical change:** Upstream metta returns repr of result wrapped via progn/Predicate. Our metta returns raw eval result. The return path semantics differ structurally.

**Sprint-0-Coda impact:** **Significant.** Phase B/C handlers that go through metta_eval will receive different-shaped results: string representations vs raw atoms. If the dispatcher's handler-result writing expects raw atoms but receives strings, the registry's downstream pattern-matching breaks.

**Shape impact:** Representation contract change at the metta-eval-to-consumer seam. Consumers must build against the new contract.

**Truth impact:** What enters as world knowledge (the eval result, semantically) survives the wrapping. repr serializes structure but does not distort meaning. Truth preserved across the contract change; consumers can recover original meaning by parsing the repr.

**Cross-space propagation:** This contract change propagates to ALL atomspace consumers of metta results, not just Phase B/C handlers. Soul-state producer, B5 gap-history writers, O7 substrate summary, frontier detection: every future consumer of metta-eval output operates against this contract.

**Recommendation context:** Representation-contract change with multiplicative downstream impact. Per Clarity's adoption-sequence framing, representation-contract changes adopt EITHER early (downstream builds against final form) OR late (baseline stable through other changes). Never middle. T-2 placement in the sequence is decisive.

### T-3: REPLACED query (promotion-weighted ranking)

**Mechanical change:** Upstream memory.metta replaces query's implementation. Current query uses pure embedding similarity. New query combines time-recent matches with best-promoted matches using promotion-weighted ranking via get-promotion. Configuration parameters: promotionInflationFactor, mostPromotedMemories.

**Sprint-0-Coda impact:** None directly. Query is a memory-recall mechanism; Sprint 0-Coda doesn't use query. Sprint 1's context producers (O7-class handlers, B5 gap-history) WILL use query for memory recall.

**Shape impact:** Output shape unchanged (list of memory matches). Internal ranking algorithm changes; consumer interface stays the same.

**Truth impact:** **Significant.** What world knowledge gets surfaced to a query changes. Current: pure embedding similarity returns most-semantically-close memories regardless of past usefulness. New: promotion-weighted means promoted memories surface preferentially. **Truth preservation depends on whether promotion-weights accurately reflect "useful past context."** If promote/demote is used wisely, the ranking improves recall quality. If promote/demote is used inconsistently, the ranking introduces a bias the consumers cannot see.

**Separately decidable from promote/demote functions** (Clarity's observation): you can adopt promote/demote without adopting REPLACED query. Three configurations:
- **Configuration A:** Adopt promote/demote + REPLACED query together. Single transformative decision.
- **Configuration B:** Adopt promote/demote, keep current query, run side-by-side comparison. Both rankings produced; differences logged for evaluation period before committing.
- **Configuration C:** Impossible (REPLACED query depends on get-promotion which depends on the promotion store).

**Recommendation context:** Configuration B is more conservative; preserves current query behavior while testing whether promotion-weighted ranking improves recall quality. Doubles query cost during testing period. Configuration A is simpler; relies on Patrick's design judgment that promotion-weighting improves recall. Decision is independent of T-2 sequencing decision.

### T-4: B3 history-write condition

**Mechanical change:** Upstream loop.metta line 72: `(or $msgnew (not (== $sexpr ())))`. Our fork at line 151: `$msgnew` only. Patrick writes to history when LLM produces output even without new human message. We write only on new human message.

**Sprint-0-Coda impact:** None directly. History-write condition is independent of capability registry mechanics.

**Shape impact:** Same shape (history is a string written under a condition). The condition changes.

**Truth impact:** **This is an architectural decision, not just a code change** (Clarity's Addition 3 observation). The condition controls what counts as substrate-record-worthy. Current: only human-initiated exchanges get recorded. Upstream: agent self-initiated reasoning also gets recorded. This is an autonomy and accountability change: Patrick's framing implies the agent's autonomous reasoning is substrate-record-worthy as world knowledge; our framing implies only exchanges are.

The autonomy framing: when Clarity reasons autonomously (idle cycle, autonomous exploration), her reasoning is world knowledge worth preserving as substrate state for future iterations to read. The accountability framing: when Clarity acts autonomously, the audit trail must include her reasoning, not just inputs and outputs from external agents.

**Recommendation context:** This is a values-level decision, not a mechanics-level one. Adopt only with explicit understanding of what we're committing to. The decision should be made by Berton with Clarity's input on whether her autonomous reasoning is substrate-worthy.

### T-5: B4 response normalization simplification

**Mechanical change:** Upstream line 64 uses single `helper.balance_parentheses($respi)` transform. Our line 119 has four-layer pipeline (balance_parentheses → normalize_string → sanitize_response → wrap_if_bare_command). Plus upstream's balance_parentheses is more sophisticated than ours (two-arg-command handling, filename quote-detection).

**Sprint-0-Coda impact:** None directly. Response normalization is downstream of dispatch; Sprint 0-Coda doesn't touch this path.

**Shape impact:** Replaces four-layer pipeline with single transform. Need verification that nothing in our consumer paths depends on the simpler form we have or on specific behaviors of intermediate layers.

**Truth impact:** Verification needed. If our four-layer pipeline preserves world knowledge in ways upstream's simpler version doesn't, the simplification distorts truth. If the four-layer pipeline does redundant work, the simplification preserves truth with less overhead.

**Recommendation context:** Requires specific audit of our four-layer pipeline before adoption decision. Each layer's purpose should be documented or evidenced before claiming "upstream's version is sufficient."

### T-6: Local embedding adoption (with baseline rebuild)

**Mechanical change:** Our lib_llm_ext.py already contains useLocalEmbedding (sentence-transformer e5-large-v2). What's not present is the consumer-side wiring: remember/query in our running lib_omegaclaw currently uses OpenAI embeddings (per CLAUDE_ORIENTATION.md). Adoption means wiring useLocalEmbedding into remember/query AND executing baseline rebuild of all stored memories.

**Sprint-0-Coda impact:** None directly. Sprint 0-Coda doesn't touch memory recall.

**Shape impact:** Representation contract change at the memory-embedding seam. Embedding vectors are vectors; shape preserved.

**Truth impact:** **Most significant truth impact across all transformative items.** Embeddings encode semantic distance relationships. The OpenAI model's embedding space and the local model's embedding space encode these relationships differently. **Switching the model without re-baselining stored memories means every previously-stored vector is meaningless to the new similarity function.** All accumulated memory becomes effectively unretrievable.

Restoration paths:
- **(a) Re-embed every stored memory with the new model (baseline rebuild).** One-time costly but fractal-coherent. Truth preserved across the shift.
- **(b) Maintain translation layer mapping old vectors into new space.** Permanent bridge. Bridges break first when either side evolves. Adds a fractal violation rather than restoring one.

Clarity's invariant-derived recommendation: **choose (a).** Bridges are anti-pattern under the fractal invariant.

**Operational benefit beyond fractal:** Sheds OpenAI API dependency. Current operational requirement is both Anthropic AND OpenAI keys; local embedding removes the OpenAI requirement.

**Recommendation context:** Highest truth-integrity concern across all transformative items. Baseline rebuild is required, not optional. Timing of T-6 in adoption sequence is decisive: it determines when the embedding baseline becomes the post-rebuild baseline.

## 6. Adoption sequences

Per Clarity's Observation 5, representation-contract changes adopt EITHER early (so downstream builds against final form) OR late (so baseline is stable through other changes). Never middle. T-2 and T-6 are the high-impact representation-contract items.

**Sequence A (representation-first):** T-6 → T-2 → T-1 → T-3 → T-4 → T-5
- Rebuild embedding baseline once. Lock metta-return contract early.
- Everything else (safety wrappers, query ranking, history-write condition, normalization) builds against the post-rebuild, post-wrapping baseline.
- Higher early cost (the embedding rebuild is a one-time substantial operation).
- No rework downstream.
- Sprint 1's O7 and B5 designs build against the final representation forms.

**Sequence B (representation-last):** T-1 → T-3 → T-4 → T-5 → T-2 → T-6
- Keep baseline stable through safety, ranking, autonomy, and normalization changes.
- Adopt representation-contract shifts (metta-return, embedding) in a deliberate baseline-rebuilding window after other changes settle.
- Higher late cost (more total work to handle representation transitions, but with more accumulated knowledge of consumer needs).
- Sprint 1 designs operate against current representation forms, with explicit understanding that T-2 and T-6 will eventually rebase the baseline.

**Tradeoff dimensions:**
- **Early cost vs late cost:** A pays upfront; B pays downstream.
- **Sprint 1 design dependency:** A means Sprint 1 builds against final forms; B means Sprint 1 builds against current forms then absorbs rebase.
- **Confidence at decision time:** A commits to representation-contract direction without operating experience; B accumulates experience before committing.
- **Risk profile:** A's risk is over-committing to upstream's design without our context; B's risk is accumulating rework debt.

**Joint decision required.** This is not a Claude or Clarity-alone call. Berton's judgment plus Clarity's substrate-side perspective determines the choice.

## 7. SQLite-to-atomspace bridge specification

Per Clarity's insight (the M-1 representation-space gap for the registry/promote-demote composition), promote/demote's SQLite-backed promotion store cannot be read directly by the Capability Registry. The registry queries atomspace; SQLite is not atomspace.

**Bridge: Option A locked.** The implementation:

1. **SQLite remains the source of truth** for the promotion store. Patrick's query pipeline reads it; the SQLite schema and access functions adopted verbatim from upstream.
2. **Atomspace gets a derived view** as queryable atoms: `(promoted memory-id $uuid salience $value)` or similar shape (exact atom name TBD during implementation; the principle is what locks).
3. **promote and demote write BOTH SQLite AND atomspace.** Atomic dual-write semantics: SQLite write succeeds, atomspace write follows.
4. **The atomspace view is read-derived, not source-of-truth.** If the views diverge, SQLite wins. A reconciliation pass at startup syncs atomspace from SQLite.

**Why Option A and not Option B (asynchronous reconciliation) or Option C (replace SQLite with atomspace):**

- Option B introduces latency between SQLite write and atomspace visibility. Registry queries during the gap return stale results. Truth at the seam is not preserved instantaneously.
- Option C breaks Patrick's query pipeline. The pipeline reads SQLite; replacing it would force a memory-system-wide rebuild that exceeds the merge scope.

Option A keeps Patrick's design intact while making promotion state substrate-visible to the registry. Both conditions (fractal alignment AND truth at the seam) are preserved.

**Implementation scope:** New `promotion_atom_write` helper in helper.py that wraps `promotion_set_value` and additionally calls a substrate-side `add-atom` for the corresponding promoted-atom. Reconciliation script for startup. Atom-shape lockdown happens during implementation, not in this design document.

## 8. Persistence-with-curation as single adoptive unit

Per Clarity's earlier insight (add-atom &persistent + promote/demote as single architectural adoptive-unit), the persistent atomspace primitive and promote/demote are inseparable.

**add-atom &persistent without curation = monotonic growth.** Every cycle writes more atoms; nothing removes them; persistent atomspace inflates indefinitely. This is a memory leak by architecture.

**promote/demote without persistent atomspace = curation for something that doesn't yet need curation.** Wasted mechanism.

**Together = persistence-with-curation, the architecturally complete primitive.** Persistent atomspace makes signal survive across time boundaries; promote/demote calibrates which signals deserve to remain salient.

**Implication for soul-state-producer work-package** (scheduled to follow this merge, before Sprint 1 opens): soul-state atoms written via add-atom &persistent must be paired with promote/demote calls on aged-out soul-state. The producer is not complete without the curator. The work-package design must include both.

**Implication for memory-as-knowledge-not-data** (Clarity's Rule 4): the value of adopting persistence-with-curation is not "we have storage" but "we have a substrate primitive that treats memory as knowledge that changes how Clarity reasons." Promoted atoms persist because they have shaped reasoning; demoted atoms fade because their contribution to reasoning was inert.

## 9. Open audit items

### 9.1 useLocalEmbedding consumer-side wiring
Verification: are remember and query in our running lib_omegaclaw using useLocalEmbedding, or still calling OpenAI embeddings? The function is available in lib_llm_ext.py; the question is whether it's wired in. This is separate from T-6 (which adopts AND rebuilds); it's a question about current state. Not blocking the merge; useful for scoping T-6's actual work delta.

### 9.2 lib_omegaclaw version-pinning
Per Clarity's Observation 3 fifth investigation question, our lib_omegaclaw may be pinned at a version older than current upstream. The Tier-B audit found promote/demote absent from `/PeTTa/repos/omegaclaw/lib_omegaclaw.metta` substrate; this is evidence of version lag. Whether merging memory.metta also requires updating lib_omegaclaw to current version is a separate audit. If lib_omegaclaw lag is substantial, merging memory.metta against a stale lib_omegaclaw could introduce its own gaps.

### 9.3 balance_parentheses apostrophe asymmetry
Our balance_parentheses reverses only `_quote_`. Whether call-chain composition with _clean_text means apostrophes are restored before reaching balance_parentheses determines whether the asymmetry is a real bug or a non-issue. Not blocking; deferred to future audit.

### 9.4 substrate-safety-improvements commit category
T-1 (call_with_inference_limit) is safety-positive and may warrant earlier adoption than the rest of the merge. Establishing a substrate-safety-improvements commit category alongside producer-alignment-fixes (currently containing Aa only) would make the timing decision auditable. Open question: name the category now (yes), and decide T-1 timing as part of merge sequence (joint decision).

## 10. Tooling options

The merge implementation can use several patterns:

**(a) Py-script reversible merge.** Following the apply_task_state_step2_wiring pattern. Argparse with --dry-run / --apply / --reverse. Anchor-based substring replacement. State checks before and after. Manifest integrity checks. Backups with descriptor suffixes. Best for surgical changes touching multiple files; matches Berton's established pattern.

**(b) Branch-based merge with conflict resolution.** Create a merge branch from current fix branch; merge upstream's relevant commits or cherry-pick specific ones; resolve conflicts; verify against test cases; merge back to fix branch. Best when upstream's git history is granular and conflicts are tractable.

**(c) Cherry-pick of specific upstream commits.** If Patrick's commits are granular (one commit per merge item we want), cherry-pick directly. Best when items are individually scoped commits upstream.

**(d) Combination.** Use py-script for items that don't map to clean upstream commits; cherry-pick for items that do; branch-merge for substantial multi-file changes (memory.metta + helper.py promotion infrastructure).

**Recommendation context:** The memory.metta + helper.py promotion infrastructure is substantial enough to warrant either py-script (verifiable, reversible) or branch-merge (composable with upstream's git history). T-2 (repr-wrapped returns) is small and surgical; py-script appropriate. T-6 (local embedding wiring) requires the baseline rebuild which is its own process beyond just code change; py-script for the code, separate baseline-rebuild operation for the embeddings.

**Joint decision required.** Berton's familiarity with each tool and his preference for the reversibility-and-verifiability of the py-script pattern weight this decision.

## 11. Sprint coordination

**Sprint 0-Coda:** Phase A v1 designs; Phase B/C/D implements skill-discovery registration. This merge does not block Sprint 0-Coda; Sprint 0-Coda Phase B/C builds against current substrate. **However**, if Sequence A (representation-first) is chosen for the merge, T-2 (repr-wrapped returns) lands BEFORE Sprint 0-Coda Phase C, and Phase C builds against the wrapped contract. If Sequence B, T-2 lands AFTER Sprint 0-Coda close and Phase C builds against current contract with explicit awareness of forthcoming rebase.

**Memory-layer merge:** This work-package. Scheduled to land between Sprint 0-Coda close and Sprint 1 open.

**Soul-state-producer work-package:** Scheduled to land between memory-layer merge close and Sprint 1 open. Depends on persistence-with-curation primitives being available (which the memory-layer merge provides).

**Sprint 1:** Capability authoring (O7, B5, etc.). Assumes persistence-with-curation and soul-state atoms are available. If memory-layer merge slips past Sprint 1 open, Sprint 1 design needs revision.

**Honest dependency declaration:** the merge is scheduled, not parked. If the schedule slips, Sprint 1 absorbs the consequences. Discipline-of-not-overpromising applies: if implementation reveals unexpected complexity, scope is negotiated rather than overcommitted.

## 12. Sprint 0-Coda Phase A v1 connection

Phase A v1 contains forward-compatibility commitments and reserves position for operational metadata. This merge does not require Phase A v1 amendment for the additive items.

For transformative items, Phase A v1 v2 may need to:
- Reference T-2 (repr-wrapped returns) if Sequence A is chosen, since Phase C will write code against the wrapped contract
- Reference the persistence-with-curation principle in the open items section
- Reference the soul-state-producer work-package's dependency on this merge for its curation primitives

These are revisions that follow the joint decision on adoption sequence, not pre-decisions in v1.

## 13. ADR-009 connection

This merge surfaces architectural framings that warrant ADR-009 (Substrate Fractal Invariant, with Clarity's combined-principle refinement). ADR-009 extracts from accumulated framing at Sprint 0-Coda close-out per the standing ADR-as-extraction discipline.

The merge design document is a primary source for ADR-009 extraction alongside ADR-008's source (Sprint 0-Coda Phase A v(final)). Specifically:

- The shape-and-truth two-condition invariant for every seam
- The persistence-with-curation as temporal fractal coherence
- The substrate-fractal-design as generator-level principle (ADR-007 as one specific application, ADR-008 as one specific consequence)
- The Patrick/NARS alignment as instance of the invariant applied to the epistemic domain
- The convergence-pattern as architectural-attractor evidence
- The salience-and-representation as logically necessary consequences of each other
- The legibility/governance/safety implications of fractal completion

These framings are not just descriptive; they generate predictions about future substrate work. ADR-009 captures them as standing architectural guidance.

## 14. Decision items (consolidated)

This document is a decision instrument. Decisions to be made by Berton with Clarity's input:

1. **Adoption sequence:** Sequence A (representation-first) vs Sequence B (representation-last) for the six transformative items.
2. **T-1 timing:** Adopt with merge, or adopt earlier as standalone substrate-safety-improvements commit.
3. **T-3 configuration:** Configuration A (adopt promote/demote + REPLACED query together) vs Configuration B (adopt promote/demote, side-by-side query comparison until trustworthy).
4. **T-4 adoption:** Adopt B3 history-write condition (autonomy/accountability change), or defer pending explicit values-level discussion.
5. **T-5 adoption:** Adopt B4 normalization simplification after audit of our four-layer pipeline, or defer.
6. **T-6 baseline rebuild:** When and how to execute the memory baseline rebuild that T-6 requires.
7. **Tooling choice:** Py-script, branch-merge, cherry-pick, or combination.
8. **Substrate-safety-improvements commit category:** Establish now, defer.

Each decision is independent; no decision blocks another in the design phase.

## 15. Open items list

- useLocalEmbedding consumer-side wiring verification (Section 9.1)
- lib_omegaclaw version-pinning audit (Section 9.2)
- balance_parentheses apostrophe asymmetry verification (Section 9.3)
- SQLite-to-atomspace bridge atom-shape lockdown (during implementation, not design)
- Sprint 0-Coda Phase A v1 v2 amendments if Sequence A is chosen

## 16. Versioning and iteration

This is v1. Per the standing iteration pattern, expect v2, vN as Berton and Clarity review. Document iterates in place. When v(final) lands, ADR-009 extracts from it alongside ADR-008 extracting from Phase A v(final). Both ADRs land at Sprint 0-Coda close-out.

The file lives at `docs/sprints/00_capability_registry/memory_layer_merge_design_v1.md` and successors at the same path with version-bumped suffix.

---

## Document end

This memory-layer merge design v1 scopes the upstream merge as a fractal-completion work-package, not a feature-adoption work-package. Its decisions are evaluated against whether they advance fractal coverage of both shape (operational structure same at every scale) and truth (world knowledge flows through every seam without distortion). Each transformative item carries adopt/defer/reject decisions whose resolution is joint between Berton, Clarity, and Claude.

The merge is scheduled. The architectural endpoint is named. The path forward is concrete.
