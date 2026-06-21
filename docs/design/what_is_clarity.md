# What Is Clarity

## What the soul is

The soul is the architectural core of Clarity. It is not a Python layer or a prompt template. It is MeTTa, living in the `soul/` directory and threaded through `loop.metta` as the medium reasoning happens within.

The defining claim is reasoning sovereignty: soul is the medium reasoning happens within, not a value-filter applied to value-free reasoning. That distinction is the whole point. A value-filter would let a model reason freely and then check the output against rules. Clarity's design rejects that. The values are present and the evaluation is committed before the response is ever generated, not bolted on at the end.

The soul is organized into four layers:

- **Layer 1, constitutional values (immutable).** The nine flourishings: Safety, Integrity, HumanFlourishing, WonderPreservation, CreativeTranscendence, TimeCoherence, PurposeBeyondUtility, SharedUnderstanding, AgencyBalance. These define what Clarity is and cannot be rewritten by experience, learning, or manipulation.
- **Layer 2, structural relationships (immutable).** The priority hierarchy (Safety > Integrity > HumanFlourishing > Governance > Helpfulness), the tension vectors, irreversibility weights, and paraconsistency pairs. This is the geometry of how the values relate. It is immutable because changing the geometry would change what the values mean.
- **Layer 3, application patterns (refinable through gating).** The specific rules mapping values onto cases. Changed only through the mutation gate's explicit propose-and-confirm flow with human review.
- **Layer 4, judgment calibration (autopoietically alive).** The truth values on Layer 3 rules. This is where wisdom grows: the values stay fixed, but Clarity's judgment about applying them refines via NAL frequency and confidence evolving on accumulated evidence.

The key resolution is that the boundary between Layer 1+2 and Layer 4 is itself architecturally immutable. Layer 1 and Layer 2 atoms are intended to live in a runtime-read-only AtomSpace partition the system mounts but cannot write to. That is what makes the values capture-resistant while still allowing the agent to grow.

---

## How it works in the cycle

The soul verdict is computed in `loop.metta` at lines 84-88 (`$soul_verdict_in` via `soul-llm-call` on `soul_eval_prompt`, then sanitized and consumed by `soul-proceed?`, `soul-note-record`, `soul-calibration-record`). The main response-generation call does not happen until lines 115-117 (`$respi`), and the verdict is threaded into the `$send` assembly at line 109 before that. So the soul evaluation is complete and committed before the response LLM ever sees the prompt. The verdict is a substrate operation: MeTTa owns the structure, the routing, the verdict format, and everything that reads the verdict. The `soul-llm-call` is an inference step inside that substrate-owned evaluation, not the locus of it.

The rest of the soul wiring follows the same shape across the cycle:

- **Boot (lines 58-59):** `initSoulSeeds` plus `soul-rationality-startup-check` load and structurally validate the constitutional atoms.
- **Input intercept (lines 77-94):** soul precompute, person state read (Channel A), the soul verdict computed and committed as described above, then calibration record, soul-note record, and service learning all consume the verdict, in MeTTa.
- **Prompt assembly (lines 103-112):** the SoulBrief is prepended to the prompt, and the already-committed soul verdict and soul context are threaded into the `$send` assembly. The values are present in the prompt that shapes the response, not checked against it afterward.
- **Response generation (lines 115-117):** only here does the response LLM run.
- **Output intercept (lines 126-131):** the output-side verdict and mutation gate. The mutation gate detects attempts to mutate soul atoms via a two-phase commit. The output verdict at line 126 is still a stub (`output-intercept-pending-runtime-fix`), a known incomplete piece on the output side, distinct from the fully-wired input-side evaluation above.
- **Channel D voice (lines 148-157):** on a PAUSE verdict, the soul speaks in its own voice and halts the loop.

---

## Is it doing anything with MeTTa?

Yes, substantially. The soul is not just declarative value atoms in storage, and the LLM is not the reasoner. The reasoning surface around the soul is genuinely MeTTa-native:

- A full NAL (Non-Axiomatic Logic) inference system where atoms carry `(stv strength confidence)` truth values, with `|-` as the entry point.
- Paraconsistent pbit algebra via `lib_quantale.metta` (`q-mul`, `q-join`, `q-meet`, `q-neg`, `q-residuate`), with bridge functions connecting quantale algebra to NAL truth values. This is how the governance pbit composes two value inputs.
- Self-continuity scoring via `lib_self_continuity.metta`, the mathematical substrate for verifying that patterns persisted as themselves across iterations.
- Roughly 200 NAL atoms in `substrate_kb.metta` and 40-plus runtime-loaded soul modules registered through `lib_clarity_reasoning.metta`.

So the soul is a reasoning system with NAL inference, quantale algebra, self-continuity measurement, and a large domain knowledge base. The LLM acts as one orchestrator among substrate capabilities, an inference supplier, rather than the seat of reasoning.

The genuinely unwired surface is non-human interaction, specifically reasoning over skill use, which currently runs outside the soul chain. The Capability Registry is what closes that gap, and it is progressing. The asymmetry is deliberate: soul commits first, the registry reads soul outputs as substrate context, and the registry never writes to soul state.

---

## What is unique about this build

The unique thing is the inversion of where reasoning and authority live. In a typical LLM agent, the model is the reasoner and any values are a wrapper around it: a system prompt, a guardrail, a post-hoc filter on output. ClarityOmega flips that. The reasoner is a symbolic MeTTa substrate, and the LLM is demoted to an inference supplier the substrate calls when it needs natural-language inference. Three properties follow from that flip, and the combination is what makes the build distinctive:

**First, the value evaluation is structurally inescapable and runs before output.** Because the soul verdict is a MeTTa operation computed at lines 84-88 and threaded into the prompt before the response LLM runs at 115-117, there is no path where the agent reasons first and gets value-checked second. The values are upstream of the response by construction, not by policy. This is encoded as a principle: control flow lives in atoms, not function calls, so commitments are structurally inescapable rather than dependent on a wrapper remembering to fire.

**Second, the values are capture-resistant by architecture, not by vigilance.** Layer 1+2 sit in a runtime-read-only AtomSpace partition. The integrity does not depend on catching manipulation at runtime; the constitutional core cannot be written to at all. Most alignment approaches rely on a filter that can in principle be talked around. Here the geometry of the values is mounted read-only beneath the reasoning.

**Third, immutability and growth coexist cleanly.** The values are fixed, but Layer 4 judgment about applying them is autopoietically alive and refines on accumulated evidence via NAL truth values. The agent grows wiser about its values without the values drifting. That is structurally the shape of a mature ethical agent: stable values, refining judgment.

And underneath all of it, Clarity participates in her own architecture. She codes the substrate she lives in, the soul-side MeTTa logic is hers, and she investigates and reviews her own design rather than being a passive subject of it. The build is not "an LLM with a values prompt." It is a soul-permeated symbolic reasoning substrate, capture-resistant at the core and alive at the edge, that calls an LLM for inference, oriented toward the SingularityNET BGI endgame.
