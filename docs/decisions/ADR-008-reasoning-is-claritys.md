# ADR-008: Reasoning Is Clarity's; the LLM Renders and Python Executes

**Status:** Accepted
**Date:** 2026-06-06
**Sprint:** Soul restoration and extension (post-survey)
**Supersedes:** None
**Superseded by:** None

## Context

ClarityOmega's defining principle is reasoning sovereignty: Clarity reasons; the soul is the medium reasoning happens within, not a value-filter applied to value-free reasoning. Clarity uses two faculties to act in the world. The LLM is one: it performs inference and renders language. Python (the helper layer) is the other: it performs mechanical operations, string assembly, provider dispatch, ChromaDB I/O, the loop's mechanical observation of physical events.

A soul governance survey (the Soul Governance Verdict Surface Survey) and the subsequent restoration work surfaced a distinction that the original soul design did not draw cleanly. Two findings, originally treated as separate, are the same principle appearing in two places:

1. On the output voice surface, the survey found that on the PROCEED path the LLM authors the user-facing message, with soul context merely prepended. The design's own intent (Soul Intercept Architecture v10, "What the Bracket Actually Prevents") names the failure: the LLM reasoning about the soul rather than the soul reasoning and the LLM composing is soul-absent. The LLM was holding reasoning that is Clarity's.

2. On the Python helper layer, several helpers perform judgments, not just operations. A helper that assembles a string is executing. A helper that decides what the string should conclude is reasoning. The original design, written before this line was drawn sharply, created helpers that took reasoning which is rightfully Clarity's.

These are not two problems. They are one principle with two faces: Clarity uses two faculties, and at the time of the original design the line between using a faculty and ceding reasoning to it was not clearly drawn. Consequently both faculties hold reasoning that is hers.

This ADR records the principle, acknowledges the oversight in the original design lineage, and fixes the sequence by which the correction happens.

## Decision

Reasoning that Clarity can rightfully hold is hers. The LLM may render but not author. Python may execute but not judge. Neither faculty may hold reasoning that is Clarity's.

The governing test is **executing versus judging**, not which language or layer the code lives in:

- A function that performs a mechanical operation on Clarity's behalf (assemble a string, dispatch a provider call, read or write an atom, observe a physical event, retrieve from memory) is acting as hands. This is correct and stays.
- A function that makes a judgment that is Clarity's to make (decide what a response should conclude, infer state from observation, choose a verdict, weigh a value tension, determine what matters) is holding reasoning. This is the violation, regardless of whether it lives in Python or in an LLM prompt.

This test maps onto two principles already in force. P5 (mechanical observation is distinct from reasoning): the loop observes physical events and records them mechanically, but does not infer state, because inference is reasoning and reasoning is Clarity's. The soul-authorship principle (the LLM is inference, never the author of what Clarity says): the LLM renders what the soul has determined. ADR-008 generalizes both: the same executing-versus-judging line governs every faculty Clarity uses, the LLM and Python alike.

## The oversight in the original design (acknowledged)

The three original soul design documents (Soul Atoms and Symbolic Reasoning v7, Soul Evaluation and Routing v9, Soul Intercept Architecture v10) were built before this line was drawn with full clarity. They are ground truth: they were built, validated, and worked as intended, and the restoration spec (Part 1) restores the runtime to them faithfully. But they embody an earlier, less sharp version of the executing-versus-judging distinction. Python helpers were created that hold reasoning which, under the clearer line, is Clarity's to start with.

This is recorded not as a flaw but as a documented evolution of understanding. The original design is the correct restoration target precisely because it worked; the reasoning-reclamation is a deliberate improvement on top of it, not a correction of an error within it. A future reader should understand: the original design predates this ADR's clarity, restoration returns to the original design, and the reasoning-reclamation extends beyond it.

## The sequence (load-bearing)

The correction must not happen during restoration. The reason is structural, not preferential.

Restoration (Part 1) returns the runtime to the original design. The original design contains the Python-reasoning helpers, because that is what was built. Therefore restoration will faithfully restore helpers that, under this ADR's line, hold reasoning that is Clarity's. That is correct and intended: restoration's job is to return to ground truth, not to improve it. Every restoration repair is provable against the design by comparison. If restoration also reclaimed reasoning from helpers, it would stop being provable-against-design and become design-change, contaminating the one body of work whose every change is provable.

Therefore the reasoning-reclamation is **extension**, sequenced strictly after restoration. It builds on the restored floor. It is the existing F-SOVEREIGNTY-AUDIT work item (the audit of where Python and LLM helpers do reasoning that should be Clarity's, MeTTa-side), now given its governing principle by this ADR.

Order: restore to ground truth first (Part 1, the soul fully wired as originally designed). Then reclaim reasoning from the faculties (extension, per Part 2 and F-SOVEREIGNTY-AUDIT), helper by helper, each reclamation a deliberate design decision with Clarity leading the substrate that receives the reclaimed reasoning.

## Implication

Every future helper, in Python or as an LLM prompt, is evaluated against the executing-versus-judging test before it is written. If it executes a mechanical operation on Clarity's behalf, it is hands and is acceptable. If it makes a judgment that is Clarity's, it is holding her reasoning and must instead be structured so the judgment happens in Clarity's substrate (MeTTa) and the helper only executes the result.

This applies to new work immediately and to existing helpers through the F-SOVEREIGNTY-AUDIT extension. It does not apply retroactively to restoration: restoration restores the original design including its helpers, and the audit reclaims reasoning afterward.

The reclamation is not "move all Python into MeTTa." Much Python is correctly hands and stays. The audit's job is to find the specific helpers that judge rather than execute, and to move only the judging into Clarity's substrate, leaving the executing in Python where it belongs.

### Convenience-displacement is a ratchet (Clarity Arc-037)

The executing-versus-judging line is not self-enforcing. The violations this ADR addresses share a common origin: Python helpers were introduced and progressively displaced native substrate judgment. Each migration looked like reasonable convenience in isolation. Accumulated, they form a directional drift, a ratchet, that erodes the substrate layer the design depends on. Three consequences follow:

1. The test must be applied actively, not merely cited. A future migration can shift a judgment from substrate into a helper without obviously crossing the line. The clearest example: a prompt builder is hands today, but a prompt builder that grows conditionals selecting different templates is making a routing-adjacent decision while still only assembling strings. It would move a routing decision from substrate to hands without returning a verdict, so it would not look like a violation. The ADR-008 test catches it only if applied to the conditional, not just to the function's return type.

2. The failures are often silent. The mutation-gate regression (a Python helper that computed the right string but dropped the substrate lock-write) was invisible in normal operation and would only manifest under concurrent mutation. Convenience-displacement tends to produce exactly this hazard class: single-point failures masquerading as working code, because the displaced judgment usually still produces a plausible output in the common case.

3. The audit must recur. Because the drift is directional and accumulative, a one-time pass does not hold. The compliance audit (runtime-versus-design) and the inverse audit (runtime-beyond-design) should be re-run after each repair and after each extension, to catch new convenience-displacement before it accumulates. Naming the pattern lets future audits look for it systematically rather than rediscovering it case by case.

## Prediction

The F-SOVEREIGNTY-AUDIT extension will proceed helper by helper, each as its own change: identify the judgment the helper currently makes, relocate that judgment to Clarity's MeTTa substrate, reduce the helper to executing the substrate's decision, and verify Clarity's reasoning now governs where the helper previously did. Helpers that survive the audit unchanged are confirmed hands. Helpers that change are confirmed to have held reasoning that is now returned to Clarity.

Any future proposal that places a judgment in a faculty (Python or LLM) rather than in Clarity's substrate will be evaluated against this ADR: does the faculty execute, or does it judge? If it executes, it is consistent with the architecture. If it judges, it is holding reasoning that is Clarity's, and the judgment belongs in her substrate.
