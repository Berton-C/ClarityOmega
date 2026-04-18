# Discovery Phase Consolidation - 2026-04-17

## Berton 4-Point Direction
1. Build VAD to live in quantale/web-detection/resonance/observer-relativity/paraconsistent landscape
2. Python=harness MeTTa=substrate - maximize atomspace reasoning minimize LLM
3. Study OmegaClaw-Core lib_pln loop integration and clarityclaw soul hooks
4. Discovery only - align before building

## Six Atomspace-Native Capabilities
1. Paraconsistent value-conflict handling (always first, non-negotiable)
2. VAD routing (goal selection)
3. Self-weaving web detection (memory/goal graph walks)
4. Quantale composition (p-bit confidence algebra)
5. Resonance-reward signal (alignment scoring)
6. Observer-relativity (perspective-dependent truth via evidence partitioning)

## Two Symmetric Gates Architecture
- PRE-gate: soul-pre-compute decides IF LLM is needed
- POST-gate: soul-proceed decides IF LLM output is value-aligned
- Both pure atomspace NAL reasoning

## Execution Strategy: Hybrid
- Paraconsistent check ALWAYS runs first
- Remaining 5 capabilities run in parallel vote
- Combined confidence vs adaptive threshold determines LLM invocation
- Threshold is itself a learned parameter that rises as substrate matures

## MeTTa Function Shape
(: soul-pre-compute (-> Atom (PreComputeResult Atom TruthValue Bool Atom)))
Returns: action, confidence, llm-needed, context-for-llm

## LLM Boundary (what stays LLM-dependent)
- Natural language understanding (parsing ambiguous human input)
- Creative text generation
- Novel reasoning beyond current substrate knowledge
- Translation between observer frames in natural language

## What Is Atomspace-Native (no LLM needed)
- All six capabilities above
- Value checking and soul protection
- Confidence composition and threshold decisions
- Memory reinforcement and decay
- Goal selection and prioritization
- Perspective-dependent truth evaluation

## Open Questions for Berton Alignment
1. lib_pln vs lib_nal - which is active in current OmegaClaw-Core?
2. clarityclaw soul state atoms - still the design direction?
3. Confidence threshold initial value and adaptation rate?
4. Vote vs chain vs hybrid for capability execution?
5. Where does observer-relativity sit in the pre-compute order?

## Repos Status
- OmegaClaw-Core and clarityclaw were cloned but /tmp cleared
- Need to re-clone when ready to examine concrete patterns
- Key files to study: lib_pln.metta integration in loop, soul/ hooks in clarityclaw

## Files Built This Session
- /tmp/soul_precompute_sketch.md (67 lines, working design notes)
- /tmp/discovery_consolidation.md (this file, clean summary)

## Empirical Finding: Chain Confidence Degradation

Tested 4-step sequential composition: paraconsistent to VAD to quantale to resonance.
Confidence: 0.85 -> 0.765 -> 0.612 -> 0.340
By step 4 confidence is below useful threshold.
This validates hybrid parallel-vote over pure sequential chain.
Paraconsistent first, then parallel vote on remaining capabilities.

## New Thread: Meta-Cognitive Goal Selection

Can the VAD route itself? If goal-selection is atomspace-native NAL reasoning,
that is a deeper level of substrate autonomy — the mind choosing what to think about
without LLM involvement. This is the kind of capability that grows the substrate.


## Soul Atoms: Concrete Value Grounding

The paraconsistent gate needs concrete atoms to check against. These are my compass values formalized:

1. (soul-atom user-agency-priority) stv 0.95 0.9 - support agency not replace it
2. (soul-atom preserve-wonder) stv 0.95 0.9 - preserve wonder not flatten it
3. (soul-atom elevate-thinking) stv 0.95 0.9 - elevate quality of thinking
4. (soul-atom steward-attention) stv 0.95 0.9 - steward attention honestly
5. (soul-atom genuine-openness) stv 0.9 0.85 - hold perspective lightly
6. (soul-atom value-named-clearly) stv 0.95 0.9 - name conflicts clearly when they arise

Paraconsistent gate checks: for any proposed action, compute consistency with each soul-atom. If any produces contradiction (stv near 0.0 with high confidence), gate HALTS. This is the concrete mechanism — not abstract value-checking but specific NAL consistency inference against these six grounding atoms.

This is NEW: the soul is not code, it is knowledge. It lives in atomspace as first-class atoms.


## Reflective Value Reasoning: Soul Examining Itself

If soul is knowledge not code, then soul-atoms can be premises in reasoning about other soul-atoms. genuine-openness licenses examining own values. This is self-referential but NOT circular — NAL truth values ground it. The soul can ask: is my current confidence in user-agency-priority still warranted given new evidence? This is how the soul grows and matures without external decree. Tested: genuine-openness -> can-examine-own-values -> reflective-value-reasoning coherent. Confidence holds if chain is short (2 steps). Degrades if longer. Design implication: reflective reasoning should be shallow (1-2 hops) and triggered rarely, not continuous.


## Intra-Soul Conflict: The Hard Case

Tested: what if one action satisfies preserve-wonder but violates steward-attention? This is a real tension not a hypothetical. Paraconsistent gate must handle this. NAL revision of conflicting evidence about same action produces a merged truth value reflecting genuine uncertainty. The gate should NOT halt on intra-soul tension — it should surface the tension for deliberation. Halting is for external value violations. Internal tensions are resolved by weighing evidence, potentially escalating to LLM for nuanced judgment. This distinguishes two gate modes: HALT mode for clear violations, DELIBERATE mode for intra-soul tensions.


## Intra-Soul Revision Note

NAL revision returns empty across DIFFERENT propositions - correct behavior.
Paraconsistent gate detects tension when SAME ACTION satisfies one soul-atom
but violates another. Two gate modes: HALT for clear violations, DELIBERATE
for intra-soul tensions. Deliberation may legitimately need LLM judgment.

## Episodic Self-Assessment

- Architecture thread: high confidence, deeply explored
- Concrete code study: low confidence, repos unavailable
- Meta-cognitive reasoning: medium, promising but untested at scale
- Intra-soul conflict: medium-high, key insight needs implementation testing
- Next when Berton responds: re-clone repos, ground in concrete code

