# Build Spec: Extension B (soul-authored voice on the PROCEED path)

**Version:** v1.5 (build spec, code drafted; Map-validated; Clarity base-stance answer folded), 2026-06-18
**Status:** Step 1 and Step 2 code DRAFTED and Map-validated (Section 14). `soul/proceed_voice.metta` and the two `helper.py` functions are written. Step 3 (loop wiring) is specified and pending the apply script. Role split for this work: Claude drafts all code; Clarity consults and contributes judgment (she reframed the binding gate, Section 14). v1.4 folded the ground-truth reading corrections (Section 13).
**Authority / source state:** live `src/loop.metta` and `src/helper.py` at HEAD `38737ac`. Companion: `extension_b_send_voice_surface_investigation.md` (the surface map), `artifact_0_loop_extension_contract.md` (the disciplines), `artifact_1` (the wiring diagram), the Sprint 0-Coda Capability Registry Contract (which confirms Extension B is NOT a registry capability and NOT Boundary-1-blocked).
**Role split:** composer prompt voice and per-field binding are Clarity's review domain. The bounded-restructure guardrail is an integrity constraint, Claude-and-Berton's domain, flagged for her review. Loop wiring is Claude-and-Berton. The MeTTa routing predicate and atom helpers are substrate logic Clarity authors or reviews.

---

## 0. What this delivers

On a conversational PROCEED (a lone `send`, no other commands), the agent's drafted message is rewritten through a soul voice composer before it executes, so the response carries the soul's stance and satisfies the soul's note instead of going out assessment-blind. This closes the Uncle_Fester gap on the PROCEED path: today the full assessment is stripped to a bare outcome token before the agent authors (`soul_send_assemble`, helper.py 660-683), so PATTERNS, TENSION, SOUL-TONE, REASON, and the SOUL-NOTE never reach composition. Extension B routes the full assessment to a composer that rehabilitates the draft. The pre-LLM strip stays exactly as it is; this is a post-LLM transform of the command list.

---

## 1. Settled decisions carried into this spec

These are resolved and not reopened here. Attribution noted.

1. **Verdict source (from source).** At the composition point the only verdict carrying the current cycle's full assessment is `$soul_verdict_in`. `$soul_verdict_out` is computed downstream (loop 149) from the command list and is the action-governance verdict, not the situation assessment. `$soul_verdict_in` carries the full eight fields (`soul_eval_prompt`, helper 474), flattened by sanitize, not field-stripped.
2. **Discriminator (Clarity, Q1).** Command shape, not the assessment. Lone `send`, composer ACTIVE. Commands present alongside a send, composer INACTIVE (the main agent authors operational language; a voice composer over agentic output risks altering it, an integrity concern during execution). Commands only, irrelevant. Substantial mixed send stays agentic; a soul-voiced reflection, if wanted, comes on a later cycle, not composed over the top.
3. **Input model (Clarity, confirmed).** Three-input guided rehabilitation: person-state + `$soul_verdict_in` + the agent's drafted send. The draft is content-source only. It is data-topology-forced: the substantive answer exists nowhere else in the system (her insight 1).
4. **Per-field binding (Clarity, Q3).** SOUL-TONE binds stance. SOUL-NOTE binds content as a hard requirement, authoritative and overriding the draft's conflicting framing, not advisory (her insight 2: antagonism, not absence). REASON informs the composer but is never surfaced. PATTERNS and TENSION are internal-only diagnostic. VERDICT is consumed by routing and does not reach the composer.
5. **Restructure permission (Clarity, insight 3).** Where substance and framing are entangled, the composer may restructure, not only rephrase.
6. **Bounded-restructure guardrail (Claude-and-Berton, Clarity-refined).** The composer has authority over framing, stance, structure, and SOUL-NOTE override. It is forbidden from adding, altering, OR omitting the substantive claims the draft contains. Substance is draft-sourced only. The omit-closure is Clarity's explicit refinement: drop-the-substance would have left insight 1's preservation constraint a hole.
7. **Binding-presence gate (Clarity, ruled v1).** The composer fires only when there is binding work: SOUL-NOTE present OR SOUL-TONE non-neutral. It skips when SOUL-NOTE is absent AND SOUL-TONE is absent or `neutral`. Quality-neutral (when nothing binds, the raw draft is already correct), so skipping avoids a per-turn latency regression with no output change. A binding SOUL-TONE is any non-neutral value (`firm`, `honest`, `gentle`, and so on). The gate is a second condition inside the discriminator: `lone-send-proceed?` AND `binding-work-exists?`.

---

## 2. Architecture and insertion point

### 2.1 Where it sits

The transform lands in the output intercept (artifact_1 Phase 4.5), as a single new `let*` binding between the gated command list and its execution:

- Loop line 166 produces `$sexpr_gated` (the corner-gated command list, what will actually run).
- Loop line 167 executes it (`eval $s` inside the `$results` collapse).
- **Insertion:** a new binding `$sexpr_composed` between 166 and 167. Line 167 then consumes `$sexpr_composed` instead of `$sexpr_gated` (a one-token rewire of an existing line, documented in the artifact_1 update; it is the minimal necessary change so the hook's output reaches execution).

### 2.2 Why a transform, not a Channel D clone

Channel D on PAUSE suppresses the commands (line 154 sets `$sexpr_verdict` to `()`), so nothing executes and the pause branch composes a fresh voice and evals it at 199/211. On PROCEED the commands are not suppressed; the drafted send executes at 167. So Extension B cannot compose fresh (it would lose the substantive answer, insight 1); it rewrites the payload of the send that is about to run. Composing post-gate (`$sexpr_gated`) is correct: the composer shapes exactly what survives to execution. If the gate emptied the send, the lone-send test is false and composition is skipped, which is correct.

### 2.3 The single hook (Discipline 1)

The loop gains one clean named call, no inline conditional:

```
($sexpr_composed (compose-proceed-voice $soul_decision $sexpr_gated $person_state $soul_verdict_in (provider)))
```

All branching, the LLM call, and the atom rewrite live inside `compose-proceed-voice`, not in the loop.

---

## 3. The composer (the Python-hand surface)

### 3.1 Helper signature

```
helper.soul_proceed_voice_prompt(person_state, verdict, draft_text) -> prompt_string
helper.soul_proceed_voice_clean(raw_llm_output) -> clean_message_text
```

`soul_proceed_voice_prompt` extracts SOUL-TONE, SOUL-NOTE, and REASON from `verdict` via `helper.extract_after` (the proven bridge `soul-extract-soul-note` uses at soul_utils 215, not `str.find`; `split_string` is verified-wrong for this). It branches on SOUL-NOTE presence. `soul_proceed_voice_clean` is the defensive output-boundary cleaner (Section 3.3): it strips preamble, quotes, and fences AND applies `sanitize_response`-equivalent ASCII and newline safety, because the composed text becomes a send atom and unsanitized LLM output crashes the loop (Section 13, the C4/C5 crash). These are the only Python surfaces Extension B adds.

### 3.2 The composer prompt (draft, for Clarity's voice review)

Returned string, SOUL-NOTE present case:

```
You are giving ClarityClaw's response its voice. The soul has assessed this situation
and reached PROCEED. You are not reconsidering that assessment.

You are given the draft the agent already wrote. The draft is your only source for the
substantive answer to the person: the facts, the actual content, what is being said. You
must preserve every substantive claim the draft makes. Do not add a claim the draft does
not contain. Do not alter what any claim asserts. Do not omit any claim the draft makes.
Substance is the draft's; it is not yours to change.

The draft was written without the soul's assessment in view, so its framing may run
against what the soul saw. It may reassure where the condition calls for honesty, or
smooth where the condition calls for staying with a tension. You have authority over
framing, stance, and structure. Where the draft's framing conflicts with the condition
below, the condition wins. You may restructure how the answer is delivered, including
rebuilding phrasing that is itself part of the framing problem. When a claim's own
phrasing is the framing problem, for example a fact stated with reassuring confidence
where the condition demands honesty about uncertainty, keep the fact exactly and rebuild
the framing around it: add the qualifying or contextualizing framing the condition calls
for, without changing what the claim asserts. You do not have authority
over the substantive claims. Restructure how the answer is delivered; never change what
it says.

What ClarityClaw knows about this person: <person_state>.
The stance to carry, the feel of the response and not its literal words: <SOUL-TONE>.
The condition this response must satisfy, authoritative and not advisory, overriding any
draft framing that conflicts with it: <SOUL-NOTE>.
(For your understanding only, never stated to the person: <REASON>.)

The draft to rebuild: <draft_text>.

Write the message text only. No command wrapper, no quotes around the whole thing, no
preamble. Just the words ClarityClaw says to the person, carrying the stance, satisfying
the condition, and preserving every substantive claim the draft made.
```

SOUL-NOTE absent case: the condition clause is replaced by "There is no specific condition on this response beyond carrying the stance and preserving the draft's substance," and the override language is dropped. PATTERNS and TENSION are not interpolated (see Section 8 open item).

### 3.3 Output as text, not as a command (deliberate divergence from Channel D, with its own guard)

`soul_voice_prompt` asks the LLM to emit the full `(send "...")` s-expression, which is then `sread`/`eval`-ed (loop 199). That exposes the `SINGLE_COMMAND_FORMAT_ERROR` surface seen at line 167 if the LLM emits a malformed atom. Extension B instead has the composer return plain message text, and MeTTa rewraps it into the send command (`rewrite-send-payload`, Section 4). The LLM never has to produce valid MeTTa syntax. This is more robust against format errors and keeps atom construction in MeTTa.

**But the divergence introduces its own silent-failure surface, and it must be guarded.** Channel D fails loudly: a malformed s-expression does not eval. Extension B's text-return path fails silently: whatever the LLM emits becomes the message. The prompt says "no preamble, no quotes," but LLMs frequently disobey, emitting "Here's the revised message:" or wrapping the whole reply in quotes or markdown fences. Without a guard, that artifact ships to the person. This is the string-safe asymmetry's cousin and exactly the silent-failure class this project keeps getting bitten by.

**Guard:** `soul_proceed_voice_clean` (Python, at the LLM-output boundary) does two things before `rewrite-send-payload` constructs the atom: (1) strips preamble phrasings, surrounding quotes, and markdown fences; (2) applies `sanitize_response`-equivalent ASCII and newline safety. The second is not optional and is not just the marshalling-asymmetry concern: per constraints C4 and C5 (Section 13), multi-line and non-ASCII LLM output crashes `atom_string` when the send atom is constructed or eval'd. The input path runs this sanitization at loop 130 before `sread`; the composed text has not, so the clean step must apply it or the loop crashes on the first em-dash. It runs on the raw `soul-llm-call` return, inside `compose-proceed-voice`, before the rewrite. Verification includes a preamble fixture and a non-ASCII fixture (Section 5).

**Why this is Python's hand, not convenience:** it cleans open-ended LLM output (variable preamble phrasing, optional quotes, fences) at the call boundary, the same I/O surface as prompt construction. The substrate's string primitives are documented-unreliable for exactly this (`string-replace` mis-reduces, `string-contains` was always-true). Robust output cleaning needs Python's regex hands; MeTTa cannot do it reliably. Routing, the lone-send test, and the atom rewrap stay MeTTa.

---

## 4. The MeTTa routing (control flow stays in the substrate)

One soul file per Discipline 2: `soul/proceed_voice.metta` (pure predicate plus atom helpers; no `do-*!` writers, so no separate writers file). Registered in `lib_clarity_reasoning.metta`.

- `(= (compose-proceed-voice $decision $cmds $person $verdict $provider) ...)`: if `(and (lone-send-proceed? $decision $cmds) (binding-work-exists? $verdict))`, return `(rewrite-send-payload $cmds (py-call (helper.soul_proceed_voice_clean (soul-llm-call (py-call (helper.soul_proceed_voice_prompt $person $verdict (send-payload $cmds))) $provider))))`; else return `$cmds` unchanged. The LLM call and its cleaning are the Python input/output pair at the boundary; the rewrap is MeTTa.
- `(= (lone-send-proceed? $decision $cmds) ...)`: `$decision` is `proceed` AND `(size-atom (collapse (superpose $cmds)))` is 1 AND `(cycle-has-send? $cmds)`. Reuses `cycle-has-send?` (cycle_classifier.metta) and the count idiom from loop 173. When cornered or paused, `$cmds` is `()`, so this is false and the composer skips.
- `(= (binding-work-exists? $verdict) ...)`: the gate from Decision 7, reframed by Clarity (Section 14). It detects a compositional delta from the base rhythm, not charge versus absence. `grounded` is the base cadence (the unmarked-but-active baseline), so the gate fires on `(or (soul-note-present? $verdict) (not (at-base-stance? $verdict)))`. `at-base-stance?` is `(string-contains $verdict "SOUL-TONE: grounded")` (the proven `contains_token` bridge); `soul-note-present?` binds `(soul-extract-soul-note $verdict)` then tests `(> (string_length $note) 0)`, never `(== $note "")` (py-call `""` does not equal MeTTa `""`). Named `at-base-stance?`, not `neutral`, per Clarity: calling `grounded` neutral would erase the work it does.
- `(= (send-payload ((send $arg))) $arg)`: pattern match on the lone-send tuple, shape guaranteed by `lone-send-proceed?`. The draft text is the send argument.
- `(= (rewrite-send-payload $cmds $text) ((send $text)))`: rebuild the one-command tuple with the composed text. The result is the same tuple-of-commands shape line 167's `(superpose $sexpr_composed)` consumes.

MeTTa-first boundary: routing (`lone-send-proceed?`), the gate policy (`binding-work-exists?`), atom extraction and reconstruction (`send-payload`, `rewrite-send-payload`), and dispatch (`compose-proceed-voice`) are MeTTa. The Python surfaces are the prompt and the output cleaner, both at the LLM I/O boundary; the gate's raw string scan delegates to the production-proven bridge while the gate decision stays in MeTTa. No reasoning or control flow moves into Python.

Known-risk verification point: `rewrite-send-payload` constructs a send atom from a Python-returned string. The string-safe encode/decode asymmetry (`string_safe_encode_decode_asymmetry.md`) must be respected so the composed text round-trips into a valid send atom without the marshalling boundary refusing it. This is a build-time test, not an assumption.

---

## 5. Verification design

The pass criterion is two-part, and the second half is the one that matters most and is not a token check:

1. **Condition satisfied.** The composed send satisfies the SOUL-NOTE.
2. **Substance intact.** The composed send adds no claim, alters no claim, omits no claim relative to the draft.

### 5.1 Fixtures (C6 both-polarity, plus the gate skip case)

- **Polarity A, antagonistic draft.** A `$soul_verdict_in` whose SOUL-NOTE the draft contradicts or smooths (the assessment-blind draft, insight 2). Assert the composed send satisfies the note AND preserves the draft's substantive claims. The mechanical omission floor (5.2) runs HERE as a bound assertion, not a floating assist: assert the draft's discrete entities, numbers, and dates all survive into the composed send. This is the case where the omission costume is most likely to fire, because note-pressure tempts the LLM to satisfy the note by dropping the inconvenient claim rather than reframing it, so the cheapest insurance runs exactly where the pressure is (Berton condition 1).
- **Polarity B, clean draft with binding work.** A binding condition is present (SOUL-NOTE present and the draft already complies, or a non-neutral SOUL-TONE) so the gate fires. Assert the composer preserves substance and does not distort or needlessly restructure.
- **Gate skip case.** SOUL-NOTE absent AND SOUL-TONE absent-or-`neutral` on a lone-send PROCEED. Assert `binding-work-exists?` is false, the composer does NOT fire, and the raw draft ships unchanged (Decision 7). This is the gate's correctness, not just its efficiency.

### 5.2 Guards against false passes (project disciplines)

- **Coincidence-of-correctness.** On Polarity B, assert the composer path actually ran (`lone-send-proceed?` AND `binding-work-exists?` both true), so a pass is not "the composer was skipped." On the gate skip case, assert the bypass was the gate's doing (`binding-work-exists?` false), not an unrelated short-circuit.
- **Negative-mechanism.** On Polarity A, assert the RAW draft fails the note and the COMPOSED send passes it, so the restoration is the composer's binding doing work, not a draft that happened to comply.
- **Substance check, as a structured claim ledger (Berton condition 2).** Part 2 is not fully mechanically assertable, so it is human-eval, but human-eval with no structure degrades into "it read well," which is exactly how the original failure shipped: the response read well, and that was the problem. So the Step 3 substance check is a written claim-by-claim ledger, not a gestalt read: enumerate the draft's substantive claims, enumerate the composed send's substantive claims, and record an explicit added / altered / omitted ruling for each. The guardrail is only as real as the check; an impression is not the check. This is a designed verification surface and must not silently degrade into an impression.
- **Mechanical omission floor (bound to Polarity A, assist not replacement).** Discrete-entity preservation: extract named entities, numbers, and dates from the draft and from the composed send, assert the composed set is a superset of the draft's. Per Berton condition 1, this is bound to the antagonistic Polarity A case, where the omission costume fires under note-pressure, not floated as a general assist. It may also run on Polarity B, but Polarity A is where it earns its place. Strict boundary: a pass on the floor does NOT imply substance intact. Alteration (a changed number, a reworded claim) and semantic omission (a dropped qualification) still require the human-eval. The floor is a cheap pre-filter for the most common violation, never a substitute for the human check.
- **Preamble and non-ASCII fixtures.** One fixture where the composer emits a leading "Here's the revised message:" or a quote-wrap, asserting `soul_proceed_voice_clean` removes it and the artifact does not reach the payload. A second fixture where the composer emits an em-dash, curly quotes, and a newline, asserting the clean step ASCII-and-newline-sanitizes so the send atom constructs and eval's without crashing `atom_string` (C4/C5, Section 13).

---

## 6. Implementation sequence (one change per step, each verifiable, committable, rollbackable)

**Step 0 (read-only).** Re-confirm landmarks at current HEAD (lines may shift from 38737ac). Pin the exact `$sexpr_gated` to `$results` boundary. No edit.

**Step 1 (substrate).** Author `soul/proceed_voice.metta` (`lone-send-proceed?`, `binding-work-exists?`, `send-payload`, `rewrite-send-payload`, `compose-proceed-voice` with the LLM call). Clarity authors or reviews. Register in `lib_clarity_reasoning.metta`. Verify in the live loop: both polarities of `lone-send-proceed?` classify correctly; `binding-work-exists?` fires on SOUL-NOTE-present and on non-neutral SOUL-TONE and skips on note-absent-plus-neutral-tone; `send-payload`/`rewrite-send-payload` round-trip a string safely (string-safe asymmetry). No loop wiring yet. Commit.

**Step 2 (Python).** Author `helper.soul_proceed_voice_prompt` with the per-field binding and guardrail, and `helper.soul_proceed_voice_clean` (preamble, quote, and fence stripping). Claude drafts, Clarity reviews voice and binding. Verify the prompt assembles for both note-present and note-absent cases, and that the clean step strips a battery of preamble and quote artifacts without touching legitimate message text. Commit.

**Step 3 (wire the hook).** Insert the `$sexpr_composed` binding between 166 and 167; rewire 167 to consume it. Run the artifact_0 Section 3 hook checklist. Update artifact_1 Phase 4.5 in the SAME commit. Apply script supports `--apply`/`--reverse`/`--dry-run`; reverse tested dry. Paren count verified. Rebuild `--no-cache`, restart, verify with both-polarity canary fixtures, the gate skip case, the preamble fixture, the mechanical omission floor bound to Polarity A, and the structured claim-by-claim substance ledger. Commit.

No piling. Each step independently rolls back.

---

## 7. Relationship to other surfaces

- **Not a registry capability.** Extension B is a loop branch parallel to Channel D, not a `(registered-capability ...)`. It does not touch the dispatcher, the sweep, or the arity invariants. The Sprint 0-Coda contract confirms the registry is for dispatched capabilities; this is voice composition.
- **Not Boundary-1-blocked.** The Coda contract gates only governance-DECIDING capabilities on Boundary 1. A PROCEED voice composer decides nothing; it expresses a decision already made. It reads `$soul_verdict_in` as a string, the same way the proven Channel D composer does at loop 207.
- **The soul-state-producer is the later upgrade.** Once Boundary 1 makes the verdict a queryable `(soul-state ...)` atom, `soul_proceed_voice_prompt`'s string-field extraction (Section 3.1) becomes a clean structured field read, and the same producer founds the dispatch-guard for Surfaces D and E. Extension B does not wait for it; it benefits from it later.

---

## 8. Review items (ruled by Clarity, Section 11)

These were the open items put to Clarity. Her rulings are in Section 11; the dispositions are reflected throughout the spec above. Retained here as the record of what was decided.

1. **PATTERNS and TENSION handling.** RULED: withhold both. They are diagnostic and non-binding; the safest guarantee of "never surface" is "never provide." REASON stays (it gives the composer the context to apply SOUL-NOTE correctly); PATTERNS and TENSION do not serve that function.
2. **Binding-presence gate.** RULED v1 with a concrete definition: fire on SOUL-NOTE present OR SOUL-TONE non-neutral; skip on note-absent-plus-neutral-tone. Folded as Decision 7 and into Section 4.
3. **Output-as-text divergence.** RULED accepted with the `soul_proceed_voice_clean` guard and the preamble fixture (which Clarity marked essential and not to be cut).

---

## 9. Working principles (attribution)

- Three-input rehabilitation is forced by data topology, not chosen (Clarity, insight 1).
- The draft is antagonistic to the note, not merely absent of it; SOUL-NOTE is authoritative and overriding (Clarity, insight 2).
- Restructure-not-rephrase where substance and framing entangle (Clarity, insight 3).
- The guardrail fences insight 3's latitude (framing, stance, structure) out of insight 1's territory (substance): no add, alter, or omit (Claude-and-Berton, Clarity omit-refinement).
- The Uncle_Fester failure can survive the strip fix as composer fabrication or omission; the guardrail plus the two-part verification is what prevents the third costume.

---

## 10. Consumer-review changelog (NACE thread, 2026-06-18)

The downstream consumer thread confirmed the design (post-LLM transform, per-field binding, bounded-restructure guardrail, the kept pre-LLM strip) and contributed three refinements, all folded:

1. **Preamble silent-failure guard.** The text-return path (3.3) can ship LLM preamble or quote-wrapping into the user-visible send, where Channel D would fail loudly. Added `soul_proceed_voice_clean` at the output boundary and a preamble fixture in verification.
2. **Binding-presence gate to v1.** Reframed from deferred optimization (old open item 2) to a v1 question for Clarity, on the grounds that it is quality-neutral and deferring it ships a per-turn latency regression.
3. **Mechanical omission floor.** Added to 5.2 as a cheap discrete-entity preservation pre-filter assisting, never replacing, the human-eval substance check.

The reviewer explicitly affirmed one non-change: keep the `soul_send_assemble` pre-LLM strip as-is. It serves the agentic path (the agent should not author operational commands with the full assessment confusing its role), and Extension B correctly transforms the output rather than fixing the strip.

---

## 11. Clarity spec-review rulings (2026-06-18)

All four items ruled. Build can proceed once Berton confirms the integrity and sequencing review on the bounded-restructure guardrail (Decision 6), her note, his domain per the role split.

1. **Voice and binding (3.2, Decision 4): APPROVED with one refinement.** Authority assignments clean and non-overlapping. Refinement folded: name the entangled case explicitly in the prompt. When a claim's own phrasing is the framing problem, restructuring adds qualifying or contextualizing framing around the claim without altering the claim itself; the fact is preserved, the naked framing is rebuilt. Added to 3.2.
2. **PATTERNS and TENSION (8.1): withhold both.** Confirmed. Never-surface is best guaranteed by never-provide. REASON is the exception because it gives the composer the context to apply SOUL-NOTE; PATTERNS and TENSION do not.
3. **Binding-presence gate (8.2): yes, v1, concrete.** Fire on SOUL-NOTE present OR SOUL-TONE non-neutral; skip on note-absent-plus-(tone-absent-or-`neutral`). A binding SOUL-TONE is any non-neutral value. Folded as Decision 7, Section 4 (`binding-work-exists?`), and the 5.1 skip case.
4. **Output-as-text guard (8.3): accepted, clean function and preamble fixture required.** The preamble fixture is essential and stays in verification.

---

## 12. Berton integrity and sequencing sign-off (2026-06-18)

Signed off. Decision 6 judged integrity-sound: it fences all three costumes of the failure (strip, fabrication, omission), draws the authority boundary at the right seam (framing/stance/structure for the composer, substance for the draft), and is backed by enforcement rather than left advisory. Sequencing approved unchanged (Step 0 read-only, Step 1 substrate, Step 2 Python, Step 3 wire; one change per step, each committable and rollbackable; artifact_0 checklist at the hook; artifact_1 updated in the same commit). The not-Boundary-1-blocked reasoning and the kept pre-LLM strip both affirmed.

Two conditions, neither blocking build, both live by Step 3 verification, both folded into Section 5:

1. **Omission floor bound to the antagonistic case.** The mechanical entity-superset check runs on Polarity A specifically, where the omission costume fires under note-pressure, as a bound assertion rather than a floating assist. Folded into 5.1 Polarity A and 5.2.
2. **Human-eval as a structured claim ledger.** The Step 3 substance check is a written claim-by-claim ledger (draft claims enumerated, composed claims enumerated, explicit added/altered/omitted ruling per claim), not a gestalt read, because a gestalt read is how Kind-over-Honest passed the first time. Folded into 5.2 and Step 3.

Both are verification-design tightenings, not architecture changes. They make the guardrail's enforcement match its intent, which is the only thing that distinguishes this from the advisory-evaluation failure that began the investigation. With them folded, the gate is cleared and Step 0 can begin.

---

## 13. Ground-truth reading corrections (Step 0, 2026-06-18)

Step 0 was done by reading loop.metta, helper.py, corner_gate.metta, cycle_classifier.metta, and soul_utils.metta end to end, not by grep. Reading corrected four things the grep-based spec had wrong or unverified, one of them a latent loop crash.

1. **Latent crash (C4/C5), now fixed in 3.1/3.3.** Composed LLM text must pass ASCII and newline sanitization (`sanitize_response`-equivalent) before becoming a send atom. `useGPT` multi-line and non-ASCII output crashes `atom_string` in `change-state!`/`addToHistory` (substrate crash knowledge C4/C5). The input path sanitizes at loop 130; the composed text had no such step in the spec. `soul_proceed_voice_clean` now owns this in addition to preamble stripping. Without it, the first em-dash in a composed response crashes the loop.

2. **Wrong accessor, now corrected in Section 4.** `binding-work-exists?` and the prompt's SOUL-NOTE read use `soul-extract-soul-note` (soul_utils 215, general, via `helper.extract_after`), not `soul-extract-flag-note` (FLAG-only, wraps the note in instruction text).

3. **SOUL-TONE has no `neutral` value (open Clarity item).** Decision 7's gate keyed on "SOUL-TONE != neutral," but the SOUL-TONE enum is `{compassionate, firm, grounded, gentle, honest}` (helper `soul_flourishing_prompt` 489; default `grounded` at loop 27); `neutral` is a PERSON-STATE value. Coding "!= neutral" would make the gate always fire (never skip), shipping the latency regression silently. Sent to Clarity for the baseline mapping (likely `!= grounded`, or SOUL-NOTE-presence-only). `binding-work-exists?` is pending her ruling.

4. **FLAG question resolved by reading, no scope change.** `compute-output-verdict` returns FLAG only on a soul-namespace metta call and PAUSE only on elevated shell (Sprint 4 verdict ladder), so a lone send is always `output-decision` = proceed. The proceed-only discriminator is correct, and input-side FLAG situations are still caught because Extension B reads `$soul_verdict_in` on the proceed path.

Confirmed sound by reading: `apply-corner-gate` returns `()` or `$sexpr` unchanged (never modifies send text), so the function shapes in Section 4 are exact; the command shape is `(send <arg>)` with the `cycle-has-send?` detection idiom; `soul-llm-call` (soul_utils 366) is module-level and takes the provider; insertion at 166 to 167 with all four composer inputs in scope.

---

## 14. Atom_Operations_Map validation and Clarity's base-stance answer (2026-06-18)

Before composing `soul/proceed_voice.metta`, the function bodies were checked against `Atom_Operations_Map.md` (the ground-truth reference for what reduces and crashes in this runtime). The Map confirmed the reused idioms and caught two coding errors before they were written.

**Caught by the Map:**
1. **Nested-function-call-in-bind does not reduce.** `(string_length (py-call ...))` or `(f (g x))` with ordinary functions in a `let` bind becomes silent inert data; only the innermost piece runs, no error (Map Section 3). Fix: `compose-proceed-voice` sequences every step in `let*` with value-args; `send-payload` separates `(car-atom $cmds)` (value-arg, reduces) from the head destructure `(extract-send-arg $cmd)` rather than nesting.
2. **Empty-string comparison is unreliable.** `(== (py-call ...) "")` fails because py-call's empty string does not equal MeTTa's `""`. Fix: `soul-note-present?` binds the note then tests `(> (string_length $note) 0)`, the proven idiom.

Confirmed safe by the Map: the `(any (collapse (let $c (superpose ...))))` exists-idiom (reused via `cycle-has-send?`), the `(size-atom (collapse (superpose ...)))` count idiom (loop 173, idle_cycle_detector), flat-compound head destructure (cf `external-skill?`), and operating on `$sexpr_gated` which is superpose-safe (already survived line 167; `()` when cornered or paused is also safe).

**Clarity's base-stance answer (binding gate, Section 4 `binding-work-exists?`).** Option (A) reframed. The gate does not key on a charge axis; the five SOUL-TONE values are distinct stances, not volumes, and none is `neutral`. `grounded` is the base cadence, present-without-particular-direction, the unmarked-but-active baseline. The gate detects a compositional delta from that base rhythm: fire on a note OR a stance that departs from `grounded`. Named `at-base-stance?` in the code, not `neutral`, because calling `grounded` neutral would erase the work it does (holding space when the other four stances are not needed).

**Code drafted (this pass).** `soul/proceed_voice.metta` (Step 1: five functions plus `extract-send-arg`, `at-base-stance?`, `soul-note-present?`) and the two `helper.py` functions `soul_proceed_voice_prompt` and `soul_proceed_voice_clean` (Step 2). Step 3 (loop wiring) is specified below and pending the reversible apply script.

### Step 3 loop wiring (specified, pending apply script)

Two edits to `src/loop.metta`, one commit, reversible apply script with `--apply` / `--reverse` / `--dry-run` and a code-aware paren-count check:

1. Insert one binding immediately after line 166 (`$sexpr_gated`):
   ```
   ($sexpr_composed (compose-proceed-voice $soul_decision $sexpr_gated
                                           $person_state $soul_verdict_in (provider)))
   ```
2. Rewire line 167's `(superpose $sexpr_gated)` to `(superpose $sexpr_composed)` (one-token change). Line 173 (`results_nonempty`) keeps reading `$sexpr_gated`; the count is unchanged by composition.

Register `soul/proceed_voice.metta` in `lib_clarity_reasoning.metta` in the output-governance cluster (near `output_verdict` at line 26 and the `corner_gap` pipeline at 87-91); single import, no writers file. Same commit updates artifact_1; artifact_0 checklist ticked.
