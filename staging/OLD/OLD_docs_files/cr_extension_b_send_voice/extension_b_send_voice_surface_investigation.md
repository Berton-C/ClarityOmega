# Surface Investigation: Extension B (soul-authored voice on the PROCEED path)

**Template:** artifact_0 Section 3.5 (Surface Investigation Template), per Discipline 6 Part B.
**Investigation date:** 2026-06-18
**Sprint / step this supports:** Extension B (soul-authored voice on PROCEED). Minimum-viable form, string-based, off-critical-path from the soul-state-producer / Boundary 1.
**Source state:** live `src/loop.metta` and `src/helper.py` at HEAD `38737ac` (Sprint 0-Coda Phase C). Line numbers reconfirmed against the live files, not the stale ~228-line project-knowledge copy.

---

## Surface name

The PROCEED send-composition path. Concretely: the routing of `$soul_verdict_in` into `$send` assembly, the strip performed by `soul_send_assemble`, and the proven composer `soul_voice_prompt`.

---

## A. Writers (assessment going INTO the surface)

- **File / function:** `$soul_verdict_in` is written in the input intercept of `src/loop.metta`, lines 95-98. It is set from `(soul-llm-call (py-call (helper.soul_eval_prompt $soul_context_in $msgrcv $person_state)) (provider))` when `$msgrcv` length > 0 (line 95-96), otherwise carried forward via `(get-state &soul_verdict_in)` (line 97). Line 98 sanitizes it through `helper.soul_verdict_sanitize`.
- **Producing prompt:** `helper.soul_eval_prompt` (helper.py 455-478), Channel B+C. Its return contract (line 474) is the full eight-field assessment: `PATTERNS / PERSON-STATE / TASKS / TENSION / VERDICT / SOUL-TONE / REASON / SOUL-NOTE`.
- **State shape:** `&soul_verdict_in` is a state variable (`change-state!`), holding the eight-field string. `soul_verdict_sanitize` (helper.py 651-658) flattens newlines and strips `*` and `#`, capping at 3000 chars. It does NOT remove fields. So at the send point the full assessment is present as a one-line string.
- **Trigger condition:** input intercept, per cycle, fires the LLM eval only when a message was received (`$msgrcv` length > 0); otherwise the prior cycle's value persists.

## B. Consumers (assessment going OUT of the surface)

- **`soul_send_assemble`** (helper.py 660-683), called at loop.metta line 120-124 with `$soul_verdict_in` (line 121). This is the consumer that discards the assessment: lines 664-672 reduce the verdict to a `verdict_summary` token (PAUSE / FLAG / PROCEED); the assembled `$send` (677-683) carries only that token, `SOUL_CONTEXT`, `PERSON_STATE`, an optional flag-note, and `lastmessage`. PATTERNS, TENSION, SOUL-TONE, REASON, and the PROCEED SOUL-NOTE do not survive. **This is the Uncle_Fester strip.**
- **`soul-extract-flag-note`** (loop.metta line 123) reads `$soul_verdict_in` to pull a flag note, passed to `soul_send_assemble` as the `soul_note` arg. On PROCEED this is typically empty.
- **`soul-pause?`** (loop.metta line 204) reads `$soul_verdict_in` on the input-pause branch.
- **`soul_voice_prompt`** (helper.py 493-509), called at loop.metta line 207 on the input-pause branch with the full `$soul_verdict_in`. This is the proven composer pattern, already consuming the full input verdict in production.

## C. Intermediate transformations

- `soul_verdict_sanitize` (helper.py 651-658): flatten + strip + cap. Field-preserving.
- `soul-extract-flag-note` (loop.metta 123): extracts the flag note for `note_section`.
- `soul_send_assemble` token reduction (helper.py 664-672): the lossy transformation. This is the surface to change.

## D. Configuration levers

- `maxOutputToken`, `reasoningMode`, `provider` (loop.metta line 128) govern the main agent LLM call on the send path. Not the strip, but the same path.
- `soul_voice_prompt` composer budget is 200 tokens (helper.py 494 docstring). Relevant if a PROCEED composer mirrors it.
- No cadence/threshold constant gates the strip. The strip is unconditional in `soul_send_assemble`.

## E. Other consumers downstream

- **The main agent LLM** (loop.metta line 128, `useGPT`) consumes `$send`, the stripped prompt, and authors both the response and any commands. This is the agentic path. Whether a voice composer replaces or augments this is the send-versus-agentic boundary (Question 1).
- **`$soul_verdict_out`** (loop.metta line 149, `compute-output-verdict $metta_cmds $soul_gate_state`) is a SEPARATE downstream verdict, computed AFTER the LLM call at line 128. It is NOT available at the send-composition point. Its consumer is the output-pause Channel D (line 193). It is out of scope for the send-composition surface and belongs to the dispatch-guard / output-governance surface (Track B).
- **MeTTa-first note:** the routing (which path, which verdict reaches the composer) is and stays MeTTa in loop.metta. The composer prompt is the Python-side LLM-call surface only. No control flow moves into Python.

---

## Resolved must-answer (the load-bearing unknown)

**At the send-composition point (loop.metta 120-124), `$soul_verdict_in` is the only verdict carrying the current cycle's full assessment.** `$soul_verdict_out` does not exist there: it is computed at line 149, after the main LLM call at line 128, from the command list that does not yet exist when `$send` is assembled. So the conversational-PROCEED composer can only read `$soul_verdict_in`, and `$soul_verdict_in` carries the full eight fields.

This is corroborated structurally rather than by instinct: `soul_voice_prompt` already composes from `$soul_verdict_in` on the input-pause branch at line 207. The composer is proven against the exact verdict Extension B needs. The apparent counter-evidence (line 193 uses `$soul_verdict_out`) is the output-pause branch, which runs after line 149 where that verdict exists. Different loop position, different live verdict. No contradiction.

---

## F. Design questions deferred to Clarity

Clarity has first-order observation rights on her own voice behavior. Three orthogonal axes:

1. **Send-versus-agentic boundary.** Where is the line between a PROCEED that should be composed in her voice by a Channel-D-style composer and a PROCEED that is agentic execution the composer must not consume? Is the discriminator the command shape (lone `send` vs other commands) or something in the assessment?
2. **Confirm the source.** Confirm the conversational-PROCEED composer reads `$soul_verdict_in`, consistent with line 207.
3. **Binding-force.** How binding are the SOUL-NOTE and the assessment's design conditions on the composition: conditions the output must satisfy, or context the LLM may write around? Uniform across the assessment, or per-field (SOUL-NOTE and REASON binding on content, SOUL-TONE binding on stance, wording free)? Note: binding-force is at greater risk on PROCEED than on PAUSE, because PROCEED conditions are quieter and the agreeable prior smooths quiet conditions more easily. The existing PAUSE composer (helper.py 502, 504) binds tone but hands the verdict over as background ("what ClarityClaw has decided"), so even it is tone-binding, not content-binding.

---

## Disposition

Sections A through E complete; no remaining unknowns blocking design. The must-answer is resolved (`$soul_verdict_in`). Section F is the Clarity scoping survey, which gates composer shape and binding semantics. Build does not begin until F returns.
