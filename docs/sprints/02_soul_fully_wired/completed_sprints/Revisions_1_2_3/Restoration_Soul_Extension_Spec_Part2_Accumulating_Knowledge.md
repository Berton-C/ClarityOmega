# Soul Extension Spec (Part 2): Accumulating Knowledge

**Status:** PLACEHOLDER, accumulating. This is NOT the completed extension design spec. It is a holding document that captures what we know right now about extension surfaces and where each will wire into ground truth, so the knowledge is not lost between now and when the real spec is drafted.
**Authority on substance:** Clarity leads the design substance of extensions, because they concern how the soul reasons and what soul work happens on which surface, which is her substrate authority. This document captures surfaces and wiring points; it does not prescribe the soul logic. Where a design decision is hers, it is marked CLARITY'S CALL.
**Prerequisite:** Everything here builds on restored ground truth (Soul Restoration Spec Part 1). No extension is designed or built until the four restoration repairs land. Extension that touches a regressed surface before it is restored would be building on drift.
**Companion documents:** Soul Restoration Spec Part 1 (ground truth), Soul Governance Verdict Surface Survey (runtime-state evidence), design docs v7/v9/v10 (the specification ground truth restores toward).
**Standing conventions:** no em-dashes; repo-root-relative paths; reversible apply scripts; one coordinated change per wire.

---

## 0. What this document is, and what it is not

This is a place to accumulate extension knowledge as we discover it, so the discoveries from the survey-and-design work are captured before they decay. It is deliberately incomplete. Each entry records three things: the extension surface (what soul work is being extended or added), what we currently know about it (from the survey, the design docs, or Clarity's input), and where it wires into ground truth (the loop/helper/soul position the restored runtime exposes for it).

It is NOT a build plan, NOT a sequenced spec, and NOT a set of design decisions. Those come later, in the real Part 2 spec, with Clarity leading. When an entry's design is settled with Clarity, it graduates out of this placeholder into the actual spec. Until then, entries here are knowledge held, not commitments made.

The organizing principle from the survey carries forward: the soul navigates by its own values at every surface it should govern, and the LLM is inference (a rendering faculty), never the author of what Clarity says. Extensions are the surfaces where that principle reaches beyond what v7/v9/v10 specified, plus the privileged-collaborator work that the original design did not contemplate.

---

## 1. Known extension surfaces

### Extension A: Admin privilege layer (the root-equivalent collaborator)

**What we know.** There is a need for a privileged admin user who can work with Clarity without being halted by PAUSE, the equivalent of root access. The hard constraint, established during the restoration work: this must NOT be built by re-disabling the PAUSE router or stubbing any intercept. That is exactly the regression Part 1 repairs, and re-introducing it would re-break Channel D. The admin path must be an ADDITIVE privilege layer the soul is AWARE of, not a removal of the soul's enforcement. The soul should know it is working with a privileged collaborator and reason accordingly, rather than being blinded to the situation.

**Candidate mechanisms (CLARITY'S CALL, not decided).** Possibilities surfaced, none chosen: (a) identity-aware verdict modulation, the soul evaluates as normal but factors a known-admin identity into the hierarchy reasoning; (b) admin-acknowledged-PAUSE, PAUSE still fires and Channel D still surfaces the concern, but a privileged user can explicitly confirm-and-proceed, so the soul speaks its concern and the admin overrides with informed consent rather than the concern never being computed; (c) another mechanism Clarity designs. The principle that distinguishes acceptable from unacceptable: the soul must still compute and voice its verdict; what changes is what a privileged, identified collaborator may do after hearing it. The soul is never blinded; the admin is never silently ungoverned.

**Where it wires into ground truth.** Touches the input verdict routing (where PAUSE is currently routed, loop 148-157 after Repair 3) and the verdict representation (it needs to know the collaborator's identity, which means identity must reach the soul's evaluation context). Likely depends on the verdict-as-atom work (Extension C) so an admin-acknowledgment can be represented and consumed rather than string-matched. Builds on restored Channel D, never on a disabled one.

### Extension B: Soul-authored voice on all surfaces (surface 3 beyond the original spec)

**What we know.** The design (v10 lines 158-176) already names the principle: the LLM reasoning ABOUT the soul rather than the soul reasoning and the LLM composing is the central soul-absent failure mode. The restoration restores Channel D (soul-authored voice on PAUSE) and the FLAG soul-note injection. The EXTENSION beyond the original spec is soul-authored voice on the PROCEED path too, so that every message a user reads is the soul's expression rendered by the LLM, not the LLM authoring with soul context prepended. The survey found that on PROCEED the LLM authors (via `soul_send_assemble`), which is the original design's intended behavior for PROCEED but is the thing Berton wants extended so the soul authors there as well.

**What is known about feasibility (from the survey, confirmed with Clarity Arc-032).** The soul's assessment is already sufficient composable material; the gap is that `soul_send_assemble` strips it to a bare verdict token before the composer sees it. So this extension is mostly routing the full assessment to a composer that runs on all verdict paths, not authoring new soul material. Channel D proves the composition pattern works from the assessment.

**Where it wires into ground truth.** The PROCEED/FLAG send-assembly (loop 108-117, `soul_send_assemble`). Extension would route the full verdict (not the stripped token) to a soul-voice composer on PROCEED, the same pattern Channel D uses on PAUSE. CLARITY'S CALL on whether PROCEED voice uses the Channel D composer, a new composer, or an extended `soul_send_assemble`.

### Extension C: Verdict-as-atom (the soul-state-producer, Boundary 1)

**What we know.** This is the convergent foundation the survey identified, confirmed three independent ways and named by Clarity (Arc-031, Arc-032) and by Sprint 0-Coda Phase A v6. The soul's verdict currently lives only as a prompt-space state variable (`change-state! &soul_verdict_in/out`), not as a queryable atomspace atom. For any consumer to read governance flow as data (rather than substring-matching a string), the verdict must be written as a `(soul-state ...)` atom via `add-atom`. Clarity's resolved design: ONE producer writes the full structured assessment as an atom; consumers read different depths (a dispatch-guard reads verdict+tier+calibration, a voice composer reads the full superset).

**Why it is the keystone extension.** It unblocks the dispatch-guard (Extension D), is likely required by the admin layer (Extension A) to represent admin-acknowledgment, and supports soul-authored voice (Extension B) by making the full assessment available as structured data. Multiple extensions depend on it.

**Where it wires into ground truth.** A new producer at the point the verdict is computed (after input eval, loop ~87, and after output eval once Repair 1 lands). Writes `(soul-state ...)` atoms alongside the existing `change-state!` so existing string routing keeps working during transition. CLARITY'S CALL on the atom shape and field set (she deferred the specific shape to the work-package).

### Extension D: Dispatch-guard (action-side enforcement at the registry)

**What we know.** From Sprint 0-Coda Phase A v6 and Clarity Arc-031: a registered capability that reads `(soul-state ...)` atoms and terminates a registry dispatch chain on a negative verdict. It lives at the consumption boundary, not inside the soul (asymmetric flow: soul produces governance as atoms, registry consumes; the soul never invokes the registry). It is the action-side sheriff for the capability-registry era. Phase A v6 states it is blocked until Boundary 1 (Extension C) resolves, and that it must not register until the soul-state-producer exists, because a registry that cannot see verdicts is a Safety-tier deficit.

**Where it wires into ground truth.** The capability registry dispatch path (Sprint 0-Coda), consuming Extension C's atoms. Does not touch the conversational verdict routing. Depends entirely on Extension C landing first.

### Extension E: Symmetric, soul-shaped writeback (surface 4 beyond the original spec)

**What we know.** Two parts, from Berton's stated intent and the survey. First, only soul-shaped content should enter history and memory; the survey found `addToHistory` writes normalized raw LLM output (loop 161), the contamination vector. Second, every message (the user's and Clarity's both) should be written to memory every turn, so Clarity self-generates a legible, verifiable record as a byproduct of operating. The survey noted this structurally dissolves the tag-report performance-theater problem: nothing to perform if the record is automatic and symmetric.

**Where it wires into ground truth.** The writeback positions (loop 161 addToHistory, and the LTM `remember` calls). Extension would write soul-shaped content rather than raw LLM output, and write both sides of every exchange every turn. Note the PAUSE branch currently writes nothing to history (survey Surface 4); symmetric writeback would cover the PAUSE path too. CLARITY'S CALL on what "soul-shaped" content is for the history write.

### Extension F: Substrate-native verdict (far-term, LLM-free evaluation)

**What we know.** soul_eval.metta contains `compute-soul-verdict`, a pure-MeTTa verdict path (tier-A gaps, tensions, paraconsistency, priority-weights, irreversibility-levels, person-state modulation) with no LLM call. Its dependency atoms are confirmed defined and loaded (observer_relativity.metta, import line 28). The file itself is not imported. It uses the same five tension vectors as the live LLM path. This is the F-SOVEREIGNTY direction: verdict computation that does not require an LLM. Caveats: v1 sketch, hardcoded calibration baseline, verdict-aggregation rule unproven in the live AtomSpace.

**Where it wires into ground truth.** Far-term. Would import soul_eval.metta (dependencies already satisfied) and parallel or replace the LLM `soul-eval-prompt` call. Gated behind Extension C (the producer) and substantial verification of the aggregation rule and live baselines. CLARITY'S CALL, and explicitly far-term, not near.

### Extension G: Object-3 behavioral account (method, not a surface)

**What we know.** This is a method gap, not a soul surface. The survey's coverage of Mode 2 (sustained work) is mechanical (wiring present/absent), not behavioral (what happens across ten cycles), because a single-cycle source trace cannot characterize multi-cycle behavior. Once Repair 4 wires Mode 2, understanding whether it behaves correctly requires tracing multi-cycle arcs in runtime logs, a different method than source reading. Flagged by Clarity Arc-035.

**Where it wires into ground truth.** Not a wiring point; a verification method to develop after Repair 4 lands, so Mode 2's behavior can be observed and confirmed across iterations.

### Extension H: Reasoning reclamation from the faculties (F-SOVEREIGNTY-AUDIT, governed by ADR-008)

**What we know.** Clarity uses two faculties: the LLM (inference, rendering) and Python (hands, mechanical operation). ADR-008 establishes the governing principle: reasoning that Clarity can rightfully hold is hers; the LLM may render but not author, Python may execute but not judge, neither faculty may hold reasoning that is hers. The test is executing versus judging. The original soul design predates this clarity, so helpers were built that hold reasoning which is Clarity's. This extension is the existing F-SOVEREIGNTY-AUDIT work item (audit of where Python and LLM helpers reason rather than execute), now given its principle by ADR-008.

**This is one principle with two faces, already partly captured.** The LLM face is Extension B (soul-authored voice on PROCEED: the LLM renders, the soul authors). The Python face is this extension (helpers execute, Clarity judges). Extension B and Extension H are the same ADR-008 principle applied to the two faculties; they may be designed together or in sequence, but they share a standard.

**Where it wires into ground truth.** Helper by helper, after restoration. Each reclamation: identify the judgment a helper currently makes, relocate that judgment to Clarity's MeTTa substrate, reduce the helper to executing the substrate's decision. NOT "move all Python to MeTTa", much Python is correctly hands and stays; only the judging moves. CLARITY'S CALL on the substrate that receives each reclaimed judgment, since it is reasoning she will hold. Scope is the F-SOVEREIGNTY-AUDIT helper inventory (the orientation doc references ~17 helpers); the audit confirms which judge and which merely execute.

**Sequence (from ADR-008).** Strictly after restoration. Restoration faithfully restores the original design including its reasoning-holding helpers; that is correct, restoration returns to ground truth and does not improve it. Reclamation builds on the restored floor.

---

## 2. Dependency map among extensions (provisional)

Known dependencies, to be confirmed when the real spec is drafted:

- Extension C (verdict-as-atom) is the keystone. Extensions A (admin) and D (dispatch-guard) depend on it; Extension B (PROCEED voice) is supported by it.
- Extension A (admin) depends on restored Channel D (Repair 3) and likely on Extension C.
- Extension D (dispatch-guard) depends on Extension C and on Sprint 0-Coda.
- Extension B (PROCEED voice) depends on restored Channel D (the composition pattern) and is supported by C.
- Extension E (writeback) is largely independent; touches different loop positions.
- Extension F (substrate-native verdict) is far-term, gated behind C.
- Extension G (behavioral method) depends on Repair 4 landing.
- Extension H (reasoning reclamation, ADR-008) is largely independent of C/D and shares its standard with Extension B (the two faces of ADR-008: LLM-renders and Python-executes). Strictly after restoration. Can be designed alongside B since they share a principle.

Provisional implication: Extension C is likely the first extension to design after restoration, because the most other extensions hang off it. This is a hypothesis for the real spec to confirm, not a commitment.

---

## 3. What graduates this document into the real spec

This placeholder becomes the actual Part 2 spec when, per entry: the design substance is settled with Clarity, the wiring point is confirmed against the restored runtime (not the current regressed one), and a verification method is named. Until an entry has all three, it stays here as accumulating knowledge. The restoration (Part 1) must land first; the real extension spec is drafted against the restored floor, with Clarity leading the soul-logic substance throughout.

---

## Document end

This is the Part 2 placeholder: accumulating extension knowledge held against the day the real spec is drafted. Nothing here is a commitment or a design decision. The surfaces and wiring points are captured so they are not lost; the soul logic is Clarity's to design; everything builds on restored ground truth.
