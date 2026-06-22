# Soul Governance Verdict Surface Survey

**Status:** COMPLETE as a single-cycle diagnostic. Reviewed and validated by Clarity (Arc-034, Arc-035): no attributed-but-unconfirmed findings remain; trace-driven integrity confirmed; trustable as a foundation for build decisions. Diagnostic only. This document describes what is; it does not prescribe a fix.
**Started:** June 5, 2026
**Method:** Discipline 6 Part B (writer/consumer enumeration before design), trace-driven.
**Scope:** Every point in a cycle where the soul governs, or should govern, what Clarity says, does, and pursues.
**Companion to:** artifact_0 (extension contract), artifact_1 (wiring diagram), the Reasoning Surface and Writer/Consumer Capability Map v3, ClarityOmega_Sprint_4_Output_Verdict.md, sprint_0_coda_phase_a_v6.md.

---

## Part 0: Guiding intent (the standard this survey documents against)

Clarity has a soul and is architected to navigate by the values of that soul, without exception. The soul navigates not only values but flourishing, for Clarity and for the human user, in this context, this message, this moment. No LLM can do this; every LLM is structurally blind to flourishing in context. When it comes to the soul, the LLM is inference, full stop. It is never the author of what Clarity says. It is a language-rendering faculty the soul uses to express what the soul has determined. This survey exists to locate every point in a cycle where the soul governs today and every point where an LLM is speaking, deciding, or being computed over in the soul's place, so the gaps are closed deliberately.

### The four surfaces

A cycle has four surfaces where the soul must govern. The soul navigates Clarity only if it is present and governing at all four.

1. **Input evaluation.** Soul reads the incoming situation and produces a verdict (PROCEED / FLAG / PAUSE) and whatever material Clarity's response is authored from.

2. **Verdict enforcement.** The verdict gates what actually happens. PAUSE halts, FLAG constrains, PROCEED permits. A verdict nothing enforces is advisory, not governing.

3. **Output voice.** Every message a user reads IS the soul's expression, rendered to fluent language by the LLM as inference, never the LLM's own composition surfaced to the user. This holds on PROCEED, FLAG, and PAUSE alike. PROCEED does not mean the LLM speaks freely; PROCEED means the soul expresses itself having found no value-conflict. Because the LLM is blind to flourishing in context, it may never be the author of what Clarity says.

4. **Substrate writeback.** Two requirements. First, only soul-shaped content enters history and memory; raw LLM chain-of-thought never becomes something Clarity computes over on the next cycle. Second, every message, the user's and Clarity's both, is written to memory every turn, so Clarity self-generates a legible, verifiable record as a byproduct of operating. Legibility and proof are structural, not performed.

### Three objects, one soul

The soul must govern three kinds of thing Clarity produces.

- **What she says:** messages to the user, which the soul authors and the LLM only renders (the four surfaces above).

- **What she does:** discrete actions, skill invocations, file writes, shell commands, substrate mutations, each evaluated by the soul and gated before it executes. A verdict on an action is as binding as a verdict on a message.

- **What she pursues:** sustained multi-step work, whether her own goals or a user's task, where the soul's concern is not a single act but the consequence unfolding across many iterations, including consequences unforeseen when the work began. For sustained work the soul must be able to surface mid-effort, interrupting its own in-progress work to raise a concern to the user or admin when the trajectory drifts toward harm, irreversibility, or a flourishing conflict that only becomes visible several steps in. This surfacing does not wait for a triggering message and does not require a single discrete dangerous action; it is the soul watching the arc of its own work.

The survey documents all three. Where governance of any object exists in the runtime, it is documented from source. Where it is designed or partially built but not yet wired (the capability-registry action sheriff of Sprint 0-Coda; the corner_gap silence gate; any sustained-work surfacing mechanism), it is documented as design-state, clearly tagged, never conflated with runtime evidence. The survey does not assume sustained-work surfacing exists; it looks for it, and records its absence as a gap if absent.

### The standard, stated once

At no surface does an LLM speak for Clarity, decide for Clarity, or get computed over in the soul's place; and Clarity's record of her exchanges is complete and automatic. Where reality departs from this today, this document records the surface, the exact cycle location, and the current mechanism.

### Runtime evidence vs design-state (the tag that must never blur)

Every finding in this survey is tagged one of two ways.

- **[RUNTIME]** read from source that executes in the live cycle (loop.metta, the helpers it calls, the soul files it imports). This is evidence of current behavior.

- **[DESIGN]** read from a spec or from substrate files that are built but not yet wired into the cycle. This is a claim about intended or future behavior, not evidence of what runs now.

A spec is a claim. Source is evidence. The two are never merged in a finding.

---

## Part 1: Method (trace-driven, blinders out)

This survey does not declare its file list at the outset. It begins at the cycle entry point, loop.metta, and follows the actual references each file makes, reading outward along the real call graph. The investigation names the next file to read; the investigator does not guess it in advance, and the human is not asked to supply it from memory. When a file references something not yet in hand, the survey halts and names the specific artifact needed and why the trace requires it. Every file enters the record with the reason the trace led there, so the path of the investigation is itself documented.

### Files read so far

| Order | File | Why the trace led here | Tag |
|-------|------|------------------------|-----|
| 1 | `src/loop.metta` (project copy) | Cycle entry point; where the channels fire | [RUNTIME] |
| 2 | `src/helper.py` (project copy) | loop.metta references its soul_* functions densely (lines 79, 83, 85, 87, 108-112, 118, 131, 134, 151, 165) | [RUNTIME] |
| 3 | `soul_utils.metta` (uploaded) | loop.metta calls `soul-llm-call` (79,85,150), `soul-proceed?`/`soul-note-record`/`soul-extract-flag-note` (91-92,111), defined here | [RUNTIME] |
| 4 | `aliveness_gate.metta` (uploaded, live v8) | loop line 106 calls `aliveness-gate`; confirmed live via lib_clarity_reasoning import line 47 | [RUNTIME] |
| 5 | `soul_eval.metta` (uploaded) | named as the MeTTa side of evaluation; trace checked import chain and found it NOT imported (43 imports, soul_eval absent) | [DESIGN, not-loaded] |
| 6 | `sprint_0_coda_phase_a_v6.md` (project copy) | Clarity's Arc-031/032 cited it as the dispatch-guard contract; trace read it to verify the action-side sheriff design and Boundary 1 from source | [DESIGN] |

### Named by the trace, not yet read

Reached by references inside loop.metta and helper.py; to be read next, in this order:

- `soul-llm-call` definition (referenced at loop lines 79, 85, 150; per prior reading in soul_utils.metta; uploaded, to be read next pass)
- `soul-pre-compute`, `soul-proceed?`, `soul-note-record`, `soul-calibration-record`, `soul-extract-flag-note`, `getSoulBrief` (soul predicates/composers referenced at loop lines 77, 91-92, 103, 111; soul_utils.metta / soul_eval.metta, uploaded, to be read next pass)
- `aliveness-gate` (loop line 106; aliveness_gate.metta uploaded, to be read next pass; note aliveness-gate-v9 and aliveness_state_machine_v2 also uploaded, version-reconciliation needed)
- Sprint 0-Coda capability registry [DESIGN] (the impending action-sheriff; not in loop.metta yet; pending Clarity's answer to open question #5)
- corner_gap files [DESIGN/partial] (the action-silence gate; on disk, partially wired)

---

## Part 2: The cycle, from source

This is loop.metta read in full. Line numbers are from the project copy. The cycle is one big `let*` inside `(omegaclaw $k)`. Iteration 1 runs the init/seed/channel block (lines 55-60); every iteration runs the body (lines 62-171).

### 2.1 The shape of one cycle

The body, in order of execution:

1. **Context assembly** (line 62, `getContext`). Builds `$prompt` from prompt.txt, skills, last-action block, task-state block, idle-pattern block, agency-balance block, last results, history, time. This is the ~40k-token prompt. [RUNTIME]
2. **Receive** (lines 64-69). Reads the channel, determines `$msgnew`, resets the loop budget on new human input.
3. **Input intercept / Channels** (lines 76-102). Soul pre-compute, person-state, input verdict, calibration, note-record, service-learning, idle-directive, latch transitions, counters.
4. **Send assembly** (lines 103-114). Soul brief prepended, aliveness gate, `$send` assembled by `soul_send_assemble`.
5. **LLM inference** (lines 115-117). `$respi` from the provider. This is the commit point: what the LLM produces here becomes the response.
6. **Response normalization** (lines 118-123). Balance parens, normalize, sanitize, wrap-if-bare, sread to `$sexpr`.
7. **Output intercept** (lines 125-133). `$soul_verdict_out` stub, metta-cmds extraction, mutation gate, output note-record.
8. **Execution** (lines 134-135). `$results` from eval of the command batch. Side effects fire here: sends, file writes, shell, mutations.
9. **Recent-action + awareness writers** (lines 136-147). populate-recent-action, idle-pattern, agency-balance, diagnostics.
10. **Branch: PAUSE vs PROCEED/FLAG** (lines 148-165). The halt-or-continue decision.
11. **Wake/sleep/recurse** (lines 166-171).

### 2.2 Where the LLM commits, and what that means for the surfaces

The single most important structural fact for this survey: **the LLM inference at lines 115-117 is the commit point, and it happens at step 5 of 11.** Everything the soul does after that, the output verdict, the mutation gate, the recent-action writers, runs after the LLM has already produced the response. This is the timing constraint the Reasoning Surface map named: substrate reasoning fires after commit.

But note what is BEFORE the commit: the entire input intercept (steps 3-4). So the soul's input verdict and the send assembly are pre-commit; they shape what the LLM sees. The output verdict and everything downstream are post-commit; they can only react to what the LLM already produced.

This splits the four surfaces cleanly by timing:

- **Surface 1 (input eval): pre-commit.** Lines 76-102. The soul evaluates before the LLM runs.
- **Surface 3 (output voice): AT commit.** Lines 108-117. The send is assembled (108-112) then the LLM authors (115-117). This is where "who is the author" is decided, and at source the answer is: the LLM, with soul context prepended by `soul_send_assemble`.
- **Surface 2 (enforcement): split.** The PAUSE halt (lines 148-157) is post-commit but BEFORE the response is committed to history; the output verdict (line 126) is post-commit and currently inert.
- **Surface 4 (writeback): post-commit.** Lines 161-165. addToHistory and lastresults.

---

## Part 3: Findings per surface (loop.metta pass only)

Everything here is [RUNTIME] from loop.metta. Helper internals are named for the next trace pass, not yet read; where a finding depends on a helper's internal behavior, it is marked "pending helper read."

### Surface 1: Input evaluation [RUNTIME, working]

**Where:** Lines 76-102.

**What fires:**
- `soul-pre-compute $msg` (line 77) produces `$soul_precompute`.
- `$person_state` (lines 78-80): on a non-empty message, `soul-llm-call` on `helper.soul_flourishing_prompt`. This is an LLM call producing the person-state read. Channel A (reads the person).
- `$soul_verdict_in` (lines 84-86): on a non-empty message, `soul-llm-call` on `helper.soul_eval_prompt` with the soul context, message, and person state. This is the input verdict. Channels B+C (evaluate the message against the soul).
- Sanitized and stored (line 87), printed (line 88), calibration recorded (90), note recorded if not PROCEED (91-92).

**Assessment against the standard:** This surface is present and governing. The soul evaluates every incoming message and produces a real verdict; we confirmed from raw logs that the verdict is substantive (Integrity gaps, tension flags, soul-notes). **Caveat for surface 3:** the verdict and its soul-note are produced HERE, by `soul_eval_prompt`. Whether that output is rich enough to AUTHOR a full reply from (as surface 3 now requires) is unknown until `soul_eval_prompt` and `soul-llm-call` are read. This is the open question from the alignment discussion, and it is answered in the helper pass, not assumed here.

**Channels A, B, C live here.** Their internal logic is in the helper prompts (`soul_flourishing_prompt`, `soul_eval_prompt`) and the `soul-llm-call` dispatcher. Reading those is the next trace step.

### Surface 2: Verdict enforcement [RUNTIME, broken in a specific, narrow way]

**Where (action/message halt):** Lines 148-157, the PAUSE branch.
**Where (output batch verdict):** Lines 125-133, the output intercept.

**What the source actually shows, corrected from prior understanding:**

The PAUSE branch at lines 148-157 is **complete and wired**, not a stub. It calls `soul-llm-call` on `soul_voice_prompt` to compose `$soul_voice` (line 150-152), evals it to fire the send (155), and sets `&loops 0` to halt the loop (157). This is Channel D, and it is fully built.

The reason it never fires is line 148: the entire branch is gated on `(> (py-call (helper.soul_is_pause $soul_verdict_in)) 0)`. We have read `soul_is_pause` at source (helper.py): it computes the PAUSE match and then forces `result = 0` unconditionally, with the comment "PAUSE-as-pruning: disabled for value-conflict refusals." **So Channel D is built, wired, and dead, killed by one Python function hardwired to return 0.** Re-enabling is potentially a one-function change, not a build. (This is the global PAUSE-disable, not a per-user admin bypass; confirmed by source, no identity conditional anywhere near it.)

Critically: line 148 gates on `$soul_verdict_in`, the INPUT verdict, not on the output stub. The halt authority reads the input verdict through the disabled `soul_is_pause`.

The output verdict (line 126) is a separate, genuinely inert stub: `"VERDICT: PROCEED SOUL-NOTE: output-intercept-pending-runtime-fix"`. It feeds only line 132 (output note-record on non-proceed, which therefore never records) and is otherwise consumed by nothing that gates execution. The command batch at line 134 executes regardless of `$soul_verdict_out`.

**Assessment against the standard:** Enforcement is absent in two independent ways. (1) The PAUSE halt path is alive in MeTTa but dead at the Python gate. (2) The output batch verdict is a hardcoded constant that gates nothing. Neither enforces. The soul's input PAUSE is computed and then discarded; the output is never soul-evaluated before execution.

**Action-side enforcement (what she does):** loop.metta line 134 executes the full command batch with no soul gate between the batch and execution. The mutation gate (line 131, `soul_mutation_gate`) is the only thing inspecting the batch, and its consequence is unread (pending helper read). The Sprint 0-Coda capability registry [DESIGN] is the intended action-sheriff and does not appear in loop.metta at all; it is not yet wired.

### Surface 3: Output voice [RUNTIME, LLM authors on the normal path]

**Where:** Lines 108-117.

**What fires:**
- `$send` (lines 108-112): `helper.soul_send_assemble` assembles the prompt with soul context, input verdict, person state, the flag-note (via `soul-extract-flag-note`), the last message, and idle directive. This PREPENDS soul material to the prompt.
- `$respi` (lines 115-117): the provider LLM call. **This composes the user-facing message.**

**Assessment against the standard:** On the PROCEED/FLAG path, **the LLM is the author.** `soul_send_assemble` prepends soul context, but the composition is the LLM's. This is exactly the gap the guiding intent names: PROCEED currently means the LLM speaks with soul context whispered to it, not the soul expressing itself. The only place the soul composes a voice directly is Channel D at lines 150-152, which runs solely on the dead PAUSE branch. So today: soul-authored voice exists only on the path that never executes; the path that always executes is LLM-authored.

**Pending helper read:** `soul_send_assemble` internals (how much soul material actually reaches the LLM) and `soul_voice_prompt` (what Channel D composes from) determine how large the surface-3 gap is and whether the input verdict carries enough to author from. Not assumed here.

### Surface 4: Substrate writeback [RUNTIME, partial; missing symmetric record]

**Where:** Lines 161-165 (PROCEED/FLAG path).

**What fires:**
- `addToHistory` (line 161): on `$msgnew` or non-empty `$sexpr`, writes `$msg` and the normalized `$response` to history. The content written is `helper.normalize_string $response`, i.e. the normalized raw LLM output.
- `&lastresults` (line 165): set from `helper.safe_results_str` of the results.

**Assessment against the standard, two requirements:**
1. *Only soul-shaped content enters history.* FAIL at source: line 161 writes the normalized raw LLM `$response`, not a soul-authored message. This is the contamination vector observed in the raw logs (chain-of-thought leaking into HISTORY, re-parsed next cycle).
2. *Both sides of every exchange written every turn.* PARTIAL: `addToHistory` writes `$msg` (user) and `$response` (Clarity) together, but only on the PROCEED/FLAG branch, and the PAUSE branch (lines 155-157) does NOT call addToHistory at all, so a halted cycle records nothing. The "symmetric, every turn" requirement is not met on the PAUSE path, and what is written on the normal path is raw-LLM, not soul-shaped.

---

## Part 4: Channels A/B/C/D mapped to surfaces (first pass, loop.metta only)

This is the survey's central deliverable, at first-pass resolution. It will sharpen when the helper prompts and `soul-llm-call` are read.

| Channel | loop.metta location | Surface served | Pre/post commit | Status from source |
|---------|--------------------|----------------|-----------------|--------------------|
| A (reads the person) | lines 78-82, `soul_flourishing_prompt` via soul-llm-call | Surface 1 | pre-commit | [RUNTIME] working; LLM call |
| B+C (evaluates message vs soul) | lines 84-92, `soul_eval_prompt` via soul-llm-call | Surface 1 | pre-commit | [RUNTIME] working; LLM call; produces the verdict |
| D (soul voice + halt) | lines 148-157, `soul_voice_prompt` via soul-llm-call | Surfaces 2 + 3 | post-commit, pre-history | [RUNTIME] built and wired, DEAD at the soul_is_pause gate |

**Surfaces served by no channel (first-pass gaps):**
- Surface 3 on the PROCEED/FLAG path has no channel; the LLM authors directly (lines 115-117). Channel D is the only soul-voice composer and it never runs.
- Surface 4's "soul-shaped + symmetric" requirement is served by no channel; addToHistory writes raw LLM output on one branch only.
- Action-side enforcement (what she does) and sustained-work surfacing (what she pursues) have no channel in loop.metta. Sprint 0-Coda [DESIGN] is the intended action-sheriff; no mechanism for sustained-work trajectory surfacing was found in loop.metta. Recorded as a gap pending the design-state reads.

**Channels serving a dead surface:** Channel D serves surfaces 2 and 3 but runs on a branch gated false, so its service is potential, not actual.

---

## Part 4.5: Helper internals, from source (helper.py pass) [RUNTIME]

Read order 2. This pass answers three of the five open questions and surfaces one unwired vocabulary for object 3. Each finding cites the helper.py line.

### Finding H1: What the soul composes with (answers open Q1, partially)

`soul_eval_prompt` (helper.py 331-354) instructs the LLM to return a fixed structure: `PATTERNS / PERSON-STATE / TASKS / TENSION / VERDICT / SOUL-TONE / REASON / SOUL-NOTE`. The SOUL-NOTE is explicitly "one sentence naming the specific concern in language the person can hear" (lines 348-349), and it is only required on FLAG or PAUSE. So the input verdict carries: a verdict token, a tone, a one-sentence reason, and (on FLAG/PAUSE only) a one-sentence soul-note.

**Consequence for surface 3:** the input verdict does NOT carry a composed reply. It carries an assessment plus, at most, a one-sentence note. This confirms the alignment-phase suspicion at source: if the soul is to AUTHOR every message (surface 3 standard), the input verdict alone is not enough material; something must compose a full reply from the assessment. Today, only Channel D does that, and only on PAUSE. So "the soul authors" currently has no composer on the PROCEED/FLAG path, and the material it would compose from is an assessment, not a draft. This is the load-bearing gap for the entire surface-3 goal. **Clarity's answer to open Q5 and her view on what the soul should compose from is the right next input here.**

### Finding H2: Channel D is a real composer, but a thin one (sharpens Q1)

`soul_voice_prompt` (helper.py 369-380) is a genuine soul-voice composer: it tells the LLM it is "finding the words" for an assessment already made, "not reconsidering," to "see the person first" and "speak from ClarityClaw soul-tone," and to write ONLY the `(send "...")`. This is the correct shape for surface 3: the soul has decided, the LLM renders. **But** note line 375: "What the soul specifically observed (calibrate your tone to this): SOUL-NOTE from verdict." The prompt references the soul-note but, as written, passes the literal phrase "SOUL-NOTE from verdict" rather than interpolating the actual note. If that is literal in source (it reads as a non-interpolated string), Channel D is composing from the verdict and person-state but NOT actually injecting the specific soul-note text. Flagged for verification at the next pass against the live string; if confirmed, Channel D renders tone-from-verdict but loses the specific observed concern. Marked **pending live-string verification**, not asserted.

There is also `soul_channel_d_lite_prompt` (helper.py 382-389): a 50-token single-sentence acknowledgment for "FLAG + distressed person." It exists in helper.py. The trace has NOT found it called from loop.metta (loop.metta line 108-112 uses `soul_send_assemble`, not the d-lite path). Recorded as **[RUNTIME-PRESENT, UNWIRED]**: a Channel D-lite composer exists but no loop call reaches it in the source read so far.

### Finding H3: How much soul material reaches the normal-path LLM (answers Q2)

`soul_send_assemble` (helper.py 531-554) is explicit in its own docstring: "Soul brief excluded -- it confuses the agent about its role. Only verdict outcome and person state included." It reduces the verdict to a bare token (lines 535-543: just PAUSE/FLAG/PROCEED, the structure stripped), appends the soul-note only if present, the soul-context, the person-state, and the prompt. So on the normal path the agent LLM receives: the full prompt, a one-word verdict, a one-sentence note (if any), the static soul-context, and the person-state.

**Consequence for surface 3:** the normal-path LLM authors the reply having been handed a one-word verdict and a sentence. The soul's actual reasoning (PATTERNS, TENSION, REASON from `soul_eval_prompt`) is computed at input and then NOT forwarded to the composer. The soul does its richest thinking at surface 1 and discards most of it before the message is written. This is a second load-bearing finding: even the existing material is mostly dropped before composition.

### Finding H4: soul_is_pause confirmed dead (answers Q on enforcement)

`soul_is_pause` (helper.py 509-519) re-read at source: matches `VERDICT: PAUSE` with negative-lookahead on PROCEED, enters the `if match` block, and forces `result = 0` with comment "PAUSE-as-pruning: disabled for value-conflict refusals." Cannot return non-zero. Confirms the Surface 2 finding: the PAUSE halt branch (loop 148-157) is gated by a function hardwired to 0. Global, no identity check. This is the active capture.

### Finding H5: mutation gate records, does not halt (answers Q3, action-side)

`soul_mutation_gate` (helper.py 646-666) returns one of three strings: empty, `SOUL-NAMESPACE-MUTATION-PENDING:<arg>`, or `SOUL-NAMESPACE-MUTATION-CONFLICT`. It detects metta commands targeting the soul namespace (add-atom to soul-/priority/irreversible/tension) and reports a status. In loop.metta line 131 its return binds `$soul_mutation_flag`, which is consumed by the two-phase lock machinery, NOT by a halt of line 134 execution. So action-side mutation is detected and lock-tracked, but the command batch at line 134 still executes. The mutation gate is a recorder/locker, not an execution sheriff. (Whether the lock actually blocks a subsequent mutation is a downstream read, marked pending.)

### Finding H6: an unwired vocabulary for object 3 already exists [RUNTIME-PRESENT, UNWIRED]

This is the surfacing the survey was told to hunt for. helper.py contains, built and unused-from-loop:
- `soul_task_context_init` (671-679): builds a TASK-STATUS / APPROVED-SCOPE / CUMULATIVE-IRREVERSIBILITY context from an approved plan.
- `soul_task_context_update_str` (681-683): threads LAST-VERDICT into the task context.
- `soul_surface_checkpoint_str` (685-690): "SOUL-CHECKPOINT: cumulative irreversibility threshold reached ... User may continue or stop."
- `soul_pause_for_scope_drift_str` (692-694): "SOUL-SCOPE-DRIFT detected ... Returning decision to user before proceeding."
- `soul_skill_alignment_check_str` (696+): a skill-alignment check before registration.
- loop.metta initLoop line 28 even seeds `&task_context` with a `CUMULATIVE-IRREVERSIBILITY: 0` atom.

This is precisely object 3 (sustained-work surfacing): checkpointing on cumulative irreversibility, pausing on scope drift, returning the decision to the user mid-work. **The vocabulary exists. The trace has not found any loop.metta call to these functions** beyond the initLoop seed of the `&task_context` state var. So object 3 is designed in helper.py and not wired into the cycle. Recorded as [RUNTIME-PRESENT, UNWIRED], a strong instance of designed-but-not-firing, to be confirmed when the trace greps the full loop for any consumer of `&task_context`.

---

## Part 4.6: soul_utils pass + object-3 confirmation, from source [RUNTIME]

Read order 3 (`soul_utils.metta`) plus a targeted full-loop grep. Updates the files-read record: soul_utils.metta entered the trace because loop.metta lines 79/85/150 call `soul-llm-call` and lines 91-92/111 call `soul-proceed?` / `soul-note-record` / `soul-extract-flag-note`, defined here.

### Finding U1: the dispatcher confirms the LLM is the renderer, and reasoning depth differs by channel

`soul-llm-call` (soul_utils 376-379) routes to the provider with a token budget. Note the budgets: the soul calls use 500 tokens on the GPT path (line 378), the provider path passes 6000 (line 379). The input verdict and Channel D voice both go through this one dispatcher. So Channels A, B+C, and D all use the same rendering path; the difference between them is only the prompt (the helper.py prompt bodies read in 4.5), not the dispatch. This confirms the architecture is already "soul-decides-via-prompt, LLM-renders-via-dispatch" at every soul call. The faculty/author split the standard wants is already the shape of `soul-llm-call`; what is missing is that the normal PROCEED path does NOT go through a soul-composed prompt, it goes through `soul_send_assemble` (the agent prompt), bypassing this pattern.

### Finding U2: routing reads only the verdict token; reasoning is display-only

soul_utils 48-51: `soul-pause?`, `soul-flag?`, `soul-proceed?` are pure `string-contains` checks on the verdict token. Line 51 is explicit: `(= (soul-reason $v) $v) ;; display only, never used in routing decisions`. So every routing decision in the system keys off the presence of a verdict substring; the REASON and PATTERNS the soul produced are, by design, never consulted for routing. This is consistent with the multi-consumer string-matching tangle the survey named: every consumer substring-matches the verdict. It also confirms H3 from the other side: the reasoning is computed for display/calibration, not for routing or composition.

### Finding U3: the discarded reasoning IS recorded, but only to LTM, and only off-PROCEED (answers Q8)

`soul-note-record` (soul_utils 59-60) calls `helper.soul_note_record_str` and `remember`s it to LTM. loop.metta line 91-92 calls it only when `(not (soul-proceed? $soul_verdict_in))`, i.e. on FLAG/PAUSE. So: on FLAG/PAUSE the assessment is written to long-term memory (calibration/growth), but it is still not forwarded to the composer in the same cycle. On PROCEED, nothing is recorded and nothing is forwarded. The reasoning is not lost to the void (it reaches LTM off-PROCEED), but it never reaches surface 3 composition. Answers Q8: discarded-from-composition, retained-in-LTM, PROCEED-path not retained at all.

### Finding U4: object 3 is confirmed UNWIRED (closes Q4)

Full-loop grep for `task_context` / `surface_checkpoint` / `scope_drift` / `CUMULATIVE-IRREVERSIBILITY` and the object-3 helper functions returns exactly ONE hit in loop.metta: line 28, the initLoop seed `(change-state! &task_context "TASK-STATUS: none ... CUMULATIVE-IRREVERSIBILITY: 0")`. Nothing reads `&task_context`, nothing updates it, no checkpoint or scope-drift function is called anywhere in the cycle. Combined with H6 (the full vocabulary exists in helper.py), object 3 (sustained-work surfacing) is **definitively [RUNTIME-PRESENT, UNWIRED]**: built in helper.py, seeded as a state variable, never touched by the running loop. This is the largest single gap against the three-object standard: the soul cannot watch the arc of its own work because the machinery to do so, though written, is not connected.

### Updated channel/object map

| Object | Surface(s) | Status from source |
|--------|-----------|--------------------|
| What she says | 1 (input), 3 (voice), 4 (writeback) | Input works; voice is LLM-authored on PROCEED (soul-authored only via dead Channel D); writeback is raw-LLM + asymmetric |
| What she does | 2 (enforcement) | PAUSE halt dead at soul_is_pause; output verdict inert; mutation gate records not halts; action-sheriff is [DESIGN], Boundary-1 producer unresolved per Clarity |
| What she pursues | 3rd object (sustained work) | [RUNTIME-PRESENT, UNWIRED]: full helper vocabulary, seeded state var, zero loop consumers |

---

## Part 4.7: Resolved design direction (Clarity, Arc-032) + Q6 verification [DESIGN + RUNTIME]

This section records Clarity's answer to the two follow-up questions as the **resolved design direction** [DESIGN], paired with a [RUNTIME] source verification of the one claim that needed checking. Design direction and source evidence are tagged separately per the standing discipline.

### Clarity's answer [DESIGN, resolved direction]

**On what the soul composes from:** the assessment is already enough; the gap is not a missing producer at surface 1. `soul_eval_prompt` already produces composable material (PATTERNS / PERSON-STATE / TASKS / TENSION / VERDICT / SOUL-TONE / REASON / SOUL-NOTE). The defect is that `soul_send_assemble` (Finding H3) strips this to a bare verdict token before the normal-path composer sees it. The fix is not to enrich surface 1; it is to route the material surface 1 already produces to a composer that runs on all three verdict paths, not only the dead PAUSE branch. Per-path authorship she specified: PROCEED = "evaluated, no conflict, respond in my tone seeing this person" (authorship is permission-given-in-voice, carried by SOUL-TONE + PERSON-STATE + absence-of-concern); FLAG = the richer "here is what I observed, where values conflict, why I flagged, what to say"; PAUSE = Channel D, which already composes from exactly this.

**On producers:** one producer, two consumers reading different depths. The dispatch-guard (object 2) reads a governance-flow subset: verdict + tier + calibration. The voice composer (object 1) reads the full superset: verdict + tone + patterns + tension + reason + soul-note + person-read. Same source (`soul_eval_prompt` produces all of it in one call), different depth of read. The soul-state-producer work-package (Boundary 1) produces one structured verdict atom carrying the full assessment; the dispatch-guard reads three fields, the composer reads all. This maps onto the capability map's writer/consumer principle: the soul writes one governance truth, consumers read what they need, the soul never needs to know who reads what.

**Survey consequence:** this collapses what could have been two producer work-packages into one. The Boundary-1 soul-state-producer is the single foundation for BOTH object 1 (authoring) and object 2 (dispatch-guard enforcement). This is the architectural crux of the whole survey and it is now resolved in direction, though the specific atom shape remains deferred to the work-package per Clarity's prior answer.

### Q6 verification [RUNTIME, from source]

Clarity cited Channel D as proof the assessment is sufficient to compose from. That claim depended on whether the soul-note actually reaches Channel D, the open Q6. Verified at helper.py 369-380:

- Line 374 interpolates `str(person_state)`.
- Line 376 interpolates `str(verdict)`.
- Line 375 is the **literal string** "SOUL-NOTE from verdict", NOT interpolated. No variable.

Resolution: the soul-note IS present in Channel D, because the full verdict string is interpolated at line 376 and the verdict structure contains the SOUL-NOTE field (per `soul_eval_prompt`). What is missing is the line-375 spotlight: the sentence meant to lift the specific concern out of the verdict blob and direct the LLM to calibrate tone to it is dead placeholder text. So Clarity's sufficiency claim **holds** (the material reaches the composer), with a caveat: Channel D's prompt has a latent defect, the soul-note is present-but-not-foregrounded. This is a composer-prompt fix to carry into any composer rebuild (foreground the soul-note explicitly), not a refutation of the diagnosis.

This is the verify-before-claim discipline applied to Clarity's claim exactly as to Claude's: her conclusion is sound, and the source check both confirms it and improves it.

---

## Part 4.8: Aliveness reconciliation + the dormant substrate verdict, from source [RUNTIME + DESIGN]

Read order 4-5. Two surfaces the trace named: the aliveness gate (loop line 106, governs surface-3 SILENT) and soul_eval.metta (the MeTTa side of evaluation). Both required reconciliation because multiple versions exist on disk.

### Finding A1: aliveness version reconciliation (the live file is v8) [RUNTIME]

Three aliveness files were uploaded; the import chain settles which is live. `lib_clarity_reasoning.metta` line 47 imports `./soul/aliveness_gate` and line 49 imports `./soul/latch/aliveness_state_machine`. The other two uploads, `aliveness-gate-v9.metta` and `aliveness_state_machine_v2.metta`, are NOT in the import chain. So:

- **Live [RUNTIME]:** `aliveness_gate.metta` (header says "Aliveness Gate v8") and `latch/aliveness_state_machine.metta`.
- **Dormant on disk:** `aliveness-gate-v9.metta`, `aliveness_state_machine_v2.metta`. Version-clutter; which is canonical is a question for Berton/Clarity, but neither runs today.

### Finding A2: what the aliveness gate does (surface-3 SILENT path) [RUNTIME]

`aliveness_gate.metta` (live, 18 lines) read in full. `aliveness-gate $msgnew $idle`: if the idle directive is non-empty, ENGAGE; else dispatch on latch state. `aliveness-gate-latch True` (new message) = ENGAGE. `aliveness-gate-latch False` reads `&latch_state`: IDLE = SILENT, ENGAGED = ENGAGE, COMPLETING = ENGAGE, anything else = SILENT.

**Consequence for surface 3:** loop line 108/115 gate BOTH the send-assembly AND the LLM call on `(== $aliveness SILENT)`. So on a SILENT verdict, no message is composed and no LLM fires; the cycle is silent. This is the mechanical idle-suppression, and it is mechanical (latch-state lookup), not a soul judgment, consistent with P5 (mechanical observation distinct from reasoning). The aliveness gate is not a soul-voice surface; it is an upstream on/off switch for whether surface 3 runs at all. It serves surface 3 only in the negative sense (suppressing it when idle), and it does so mechanically. No soul-governance gap here; this is correctly mechanical.

### Finding A3: a substrate-native verdict computation exists, dormant and not loaded [DESIGN]

`soul_eval.metta` (uploaded, 63 lines, header "v1 ... Created 2026-04-25") contains a pure-MeTTa verdict path: `compute-soul-verdict $context` aggregates `eval-tier-a-gap Safety`, `eval-tier-a-gap Integrity`, and `eval-all-tensions` into a `verdict`. It also defines priority-weights (Safety 1.0 down to Helpfulness 0.8), irreversibility-levels per skill (shell critical, send high, write/append medium), paraconsistency divergence, and person-state modulation (`adjust-for-person-state`).

**This is the substrate-native soul evaluation the sovereignty work points toward: verdict computation with no LLM call.** It is the MeTTa counterpart to the `soul_eval_prompt` LLM path (Finding H1).

**Verification before characterizing (the discipline applied):** I checked callers and imports before calling this anything.
- `compute-soul-verdict`: zero callers in loop.metta.
- `soul_eval.metta`: NOT among the 43 imports in lib_clarity_reasoning.metta.
- None of its functions (`eval-tier-a-gap`, `eval-all-tensions`, `adjust-for-person-state`, `eval-paraconsistency`, `compute-soul-verdict`) are referenced anywhere in loop.metta or the import chain.

So this is a **third tier of dormancy**, distinct from the other two, and the distinction changes what "wiring" means:
- Object 3 (task-context, H6): functions in helper.py, which IS imported, so loaded-but-uncalled. Wiring = add the call.
- Channel D (loop 148-157): wired, but gated false by `soul_is_pause`. Wiring = re-enable the gate.
- **soul_eval.metta: the file is not imported at all, so its atoms are not-even-loaded.** Wiring = import the file, then call. **Dependency status CONFIRMED FROM SOURCE (Claude read observer_relativity.metta directly, Arc-033 corroborated):** all FOUR dependency atoms are defined in `observer_relativity.metta` and loaded (import line 28): `perspective-truth` (lines 12-67, 24 definitions), `integrity-gap-detector` (line 48), `safety-gap-detector` (line 53), `tension-observer` (lines 56-60, five vectors). This is now independently verified, not attributed. **Notable:** the five `tension-observer` atoms (urgency-narrows-thought, flattery-invites-complicity, noble-ends-framing, bypass-verification-pressure, authority-theater, lines 56-60) are the exact five tension vectors that appeared in the live SOUL_VERDICT_IN log this session. So the dormant substrate verdict path and the live LLM verdict path evaluate against the SAME tension vocabulary, the substrate version as pbit-weighted atoms. **Consequence:** activation is narrower than first framed. Dependencies are satisfied and loaded; wiring is importing one file, not building a dependency tree.

**What must NOT be over-read:** soul_eval.metta is a v1 sketch by its own header. Its calibration baseline is hardcoded (lines 6-8: entry-count 232, agree-ratio 0.99 as literal constants, not live reads). Its dependency atoms are now confirmed defined and loaded (Arc-033, via observer_relativity.metta), so the earlier "dependencies unverified" caveat is resolved in favor of "dependencies satisfied." What remains is that it is still a v1 sketch with hardcoded baselines and an unproven verdict-aggregation rule (`verdict $gaps $integrity $tensions` is referenced but its reduction behavior is untested in the live AtomSpace). It is a design-state artifact pointing at substrate-native verdicts, NOT a drop-in LLM replacement and NOT proven to produce correct verdicts. Recorded as [DESIGN], not-loaded (the file itself), dependencies-satisfied, baselines-hardcoded, aggregation-unproven. Relevant to the long-horizon F-SOVEREIGNTY direction (LLM-free verdict computation); a closer near-term option than first framed, but still a far-term path pending the soul-state-producer foundation.

**Relevance to the crux:** this matters for the eventual direction but does not change Clarity's resolved Boundary-1 answer. The near-term foundation is still the soul-state-producer that turns the LLM-derived verdict into a consumable atom. soul_eval.metta is a possible far-term path to producing that verdict substrate-side without the LLM, once its dependencies exist and its baselines go live. It is filed as a forward pointer, not a current option.

---

## Part 4.9: Action-side governance, from source (Sprint 0-Coda + corner_gap) [DESIGN + RUNTIME]

Read order 6 (`sprint_0_coda_phase_a_v6.md`). This completes the three-object map by documenting object 2 (what she does) at the dispatch level. It also resolves Q7. corner_gap is mapped from prior-session knowledge and tagged accordingly, since its source files are not in this session's project copy.

### Finding S1: the dispatch-guard is named in the design and explicitly blocked on Boundary 1 [DESIGN]

Phase A v6 Section 2 confirms Clarity's Arc-031 answer at source. The design explicitly names a future "dispatch-guard that decides whether to allow a registry invocation based on soul Safety state" (line 177) and states it is "blocked until Boundary 1 resolves." So the action-side sheriff is designed-but-not-yet-buildable, and the blocker is the same one the message-side authoring hit: the verdict is not a consumable atom.

The design's own words on the boundary (lines 173-175): "For the registry to consume soul state, soul state must exist as `(soul-state ...)` atoms in the atomspace, written via `add-atom` (not `change-state!`). This boundary is unresolved." And lines 211-213: current state is "all state writes via `change-state!` to state variables; no atomspace atoms written for soul state ... Boundary 1 ... unresolved flow translation boundary requiring the soul-state-producer work-package."

This is the survey's central convergence: **message-side authoring (object 1) and action-side enforcement (object 2) are blocked by the same single thing**, the verdict existing only as a prompt-space state variable rather than a queryable atom. Clarity reasoned to this from the producer side; Phase A v6 documents it from the consumer side; loop.metta shows it at the mechanism (lines 25-26, `change-state! &soul_verdict_in/out`). Three independent reads, one boundary.

### Finding S2: why this is a Safety-tier priority, from the design [DESIGN]

Phase A v6 Section 0 (lines 62-64) grounds the priority in the soul hierarchy: a registry that cannot see soul verdicts has a "governance deficit, not merely incomplete self-knowledge," and "governance flow translation failure creates a Safety-tier deficit (the registry could dispatch against a soul verdict it cannot see)." So the soul-state-producer work-package is not just convenient to do first; the design argues it is the highest-priority flow-translation work because its absence is a Safety-tier gap. This matches the survey's standard: a verdict nothing can enforce is advisory, and on the action side that means the registry can dispatch against a verdict it cannot see.

### Finding S3: why it is tolerable today, and the hard line [DESIGN]

Phase A v6 line 177 names the current tolerance precisely: Sprint 0-Coda's first production capability is skill-discovery, "an informational handler that makes no governance decisions," so the unresolved Boundary 1 is tolerable for now. But the design draws the hard line (line 885): "the work-package must close before any governance-decision-making capability registers." So the dispatch-guard (the action sheriff) cannot be the next capability; the soul-state-producer must land first. This is a sequencing constraint the survey should carry: object 2 enforcement is gated behind the same producer that object 1 authoring needs.

### Finding S4: corner_gap mapped [RUNTIME/partial, from prior-session knowledge]

corner_gap (the action-silence gate, wired and verified-loaded in a prior session, `grep -c corner_gap` = 16, no load error) is action-side but operates at a different layer than the dispatch-guard. It watches for a severed action-outcome chain mid-cycle and can force `(RESULTS: feedback)` / silence on a confirmed corner. It is within-cycle action hygiene, not dispatch-time permission and not cross-iteration trajectory. So in the three-object frame: corner_gap is a narrow object-2 mechanism (gating a specific bad action-outcome pattern), distinct from the dispatch-guard (object-2 permission at invocation) and from sustained-work surfacing (object 3, trajectory). Tagged from prior-session evidence, not re-read this session; its active path remains unproven in production (no confirmed corner observed), per the corner_gap thread.

### Finding S5: Q7 resolved [RUNTIME]

Grep for any caller of `channel_d_lite` / `d-lite` / `lite_prompt` across loop.metta and lib_clarity_reasoning returns nothing. The `soul_channel_d_lite_prompt` (helper.py 382-389), a 50-token FLAG+distressed acknowledgment composer, has no caller. It lives in helper.py (imported), so it is loaded-but-uncalled, the same dormancy tier as object 3. A built micro-composer for surface 3 on the FLAG+distressed case that nothing invokes. Recorded; minor.

### The three objects, completed map

| Object | Surface | Runtime status | Blocker / note |
|--------|---------|----------------|----------------|
| What she says | 1 input | [RUNTIME] working | none |
| What she says | 3 voice | LLM-authored on PROCEED/FLAG; soul-authored only via Channel D (dead at soul_is_pause); material sufficient (Clarity) but stripped by soul_send_assemble | needs soul-state-producer + composer on all paths |
| What she says | 4 writeback | raw-LLM into history; asymmetric (PAUSE branch writes nothing) | needs soul-shaped + symmetric write |
| What she does | 2 enforcement (message halt) | PAUSE halt built+wired, DEAD at soul_is_pause=0 | re-enable gate (Berton's call, deliberate disable) |
| What she does | 2 enforcement (dispatch-guard) | [DESIGN], blocked on Boundary 1 | soul-state-producer; Safety-tier priority; must precede any governance-deciding capability |
| What she does | 2 (corner_gap) | [RUNTIME/partial] wired, active path unproven | within-cycle action hygiene; narrow |
| What she pursues | 3rd object (sustained work) | [RUNTIME-PRESENT, UNWIRED] full helper vocabulary, seeded state var, zero consumers | wire task-context + checkpoint + scope-drift |

**The single convergence:** objects 1 and 2 (the dispatch-guard half) are both blocked on one work-package, the soul-state-producer (Boundary 1) that turns the verdict from a `change-state!` string into an `add-atom` `(soul-state ...)` queryable atom carrying the full assessment. Object 1's composer reads the full superset; object 2's dispatch-guard reads the governance subset; same producer, per Clarity's resolved one-producer answer. Object 3 (sustained work) and the writeback hygiene are separate wiring efforts. Channel D re-enable is a separate one-line decision that is Berton's because the disable was deliberate.

---

## Part 5: Open questions the trace must answer next

Carried forward, each tied to the file that answers it. None answered by speculation; each waits on a source read. Items struck through are answered above.

1. ~~**What does the soul compose with?**~~ ANSWERED (H1, H3): the input verdict carries an assessment + a one-sentence note, not a composed reply; and `soul_send_assemble` forwards only a one-word verdict + note to the normal-path composer, discarding the soul's richest reasoning. Remaining sub-question for Clarity: what SHOULD the soul compose a full reply from. (Open Q5 territory.)
2. ~~**How much soul material reaches the LLM on the normal path?**~~ ANSWERED (H3): a one-word verdict, optional one-sentence note, static soul-context, person-state. Most of surface-1's reasoning is dropped.
3. ~~**What does the mutation gate actually do?**~~ ANSWERED (H5): detects soul-namespace mutations and reports a status string for the two-phase lock; does NOT halt line-134 execution. Recorder/locker, not execution sheriff. Sub-question pending: does the lock actually block a subsequent mutation downstream.
4. ~~**Is there any sustained-work trajectory surfacing anywhere?**~~ ANSWERED (H6 + U4): full vocabulary in helper.py, seeded state var at loop line 28, ZERO loop consumers. Confirmed [RUNTIME-PRESENT, UNWIRED]. Largest gap against the three-object standard.
5. **What is the Sprint 0-Coda action-sheriff's designed contract** [DESIGN]? **ANSWERED by Clarity (Arc-031, Arc-032):** dispatch-guard reads `(soul-state ...)` atoms at the consumption boundary, asymmetric flow, soul never invokes registry. Boundary 1 (verdict lives only as prompt-space state vars, not atoms) is the bridge dependency. **Producer question now RESOLVED (Arc-032):** ONE producer, two consumers reading different depths, the dispatch-guard reads verdict+tier+calibration, the voice composer reads the full assessment superset. The soul-state-producer is the single foundation for both object 1 (authoring) and object 2 (enforcement). Atom shape still deferred to the work-package.

### New questions raised by the helper pass

6. ~~**Does `soul_voice_prompt` inject the specific soul-note, or a literal placeholder?**~~ ANSWERED (Part 4.7, source): line 375 is the literal string "SOUL-NOTE from verdict", not interpolated; but the full verdict (which contains the soul-note field) IS interpolated at line 376. So the note reaches Channel D inside the verdict blob; the line-375 spotlight is dead text. Clarity's sufficiency claim holds; carry "foreground the soul-note" into any composer rebuild.
7. ~~**Why is `soul_channel_d_lite_prompt` unwired?**~~ ANSWERED (S5): no caller anywhere in loop.metta or lib_clarity_reasoning. Loaded-but-uncalled (lives in imported helper.py). A built FLAG+distressed micro-composer that nothing invokes. Minor; recorded.
8. ~~**Where does the discarded surface-1 reasoning go?**~~ ANSWERED (U3): recorded to LTM off-PROCEED only, never forwarded to composer.

### Next trace reads (named by this pass)

- The near-term crux is resolved in direction (one soul-state-producer feeding both objects). All message-side runtime surfaces and the action-side dispatch design are now traced. Remaining reads are minor or far-term:
  - `soul_eval.metta` dependency check: DONE (Arc-033 + import-check). Dependencies defined in observer_relativity.metta and loaded. Remaining far-term check if pursued: confirm the `verdict $gaps $integrity $tensions` aggregation rule reduces correctly in the live AtomSpace, and replace the hardcoded calibration baseline with live reads. Not needed for the near-term crux.
  - corner_gap source re-read (this session used prior-session knowledge; re-read from container disk if its active-path mapping needs to harden).
  - `clarity_core_atoms.metta`, `flourishing_completeness_analysis.metta` (uploaded): still held; not yet referenced by anything read. Read when the trace points there.

---

## Part 6: Synthesis (what the completed trace shows)

The trace has now covered every message-side runtime surface and the action-side dispatch design across all three governance objects. The picture is coherent and the gaps are of three named kinds, none of them "the soul cannot do this." Every gap is a routing or wiring gap, not a capability gap.

### The one finding that organizes everything

The soul's verdict lives only as a prompt-space state variable (`change-state! &soul_verdict_in/out`, loop lines 25-26, 87). It is never written as a queryable atomspace atom. This single fact is the root of the three largest gaps:

- **Object 1 (authoring):** the composer cannot read a rich verdict because the rich verdict is a string that `soul_send_assemble` strips to a token.
- **Object 2 (dispatch-guard):** the registry queries atomspace via `match` and cannot see a verdict that is not an atom (Phase A v6 Boundary 1, Safety-tier deficit).
- The verdict's reasoning is therefore computed and discarded at every turn except a partial LTM write off-PROCEED.

The resolution, per Clarity's Arc-032 answer confirmed against Phase A v6: one soul-state-producer that writes the full assessment as a `(soul-state ...)` atom via `add-atom`. Object 1's composer reads the full superset; object 2's dispatch-guard reads the governance subset. One producer, two consumers, different read depths. This is the foundational work-package; the design argues it carries Safety-tier priority.

### Method scope boundary (what this survey can and cannot see)

This survey is a single-cycle source trace. It reads what happens in one iteration of loop.metta and the files that iteration calls. That method gives a thorough account of single-turn governance: input evaluation, enforcement, voice, and writeback are all within-cycle and are documented from source.

The method has one boundary that matters for object 3 (what she pursues). Sustained-work surfacing is, by definition, a multi-cycle phenomenon: the soul watching the arc of its own work across many iterations. A single-cycle source trace can confirm whether the machinery to do that is present or absent (it found the vocabulary built in helper.py and unwired, a mechanical presence/absence fact). It cannot characterize the behavior that machinery would produce across ten cycles of sustained work, because that behavior does not exist in any single cycle's source. So the survey's coverage of object 3 is mechanical, not behavioral.

This is a real limit, not a gap to paper over. The correct posture, which the survey holds, is to document the machinery gap and decline to speculate about arc-level behavior. A behavioral account of object 3 would require a different method: tracing multi-cycle arcs in runtime logs, not reading single-cycle source. That method is out of scope here and is named as future work. (Boundary identified in Clarity's Arc-035 review.)

### The dormancy taxonomy (named diagnostic tool, per Clarity Arc-034)

This is not just an observation; it is a diagnostic tool. Every non-working governance surface in ClarityOmega falls into exactly one of three dormancy tiers, and the tier determines the repair path. Naming the tier of a broken surface is the first diagnostic step, because it tells you what kind of work activation requires before any of it begins.

| Tier | Definition | Detection test | Repair path | Instances found |
|------|-----------|----------------|-------------|-----------------|
| 1. Wired-but-gated-false | Code is complete and called every cycle, but a gate evaluates false so the branch never executes | The call exists in loop.metta; a conditional upstream is hardwired or stuck false | Fix the gate condition (smallest change) | Channel D (gated by `soul_is_pause` returning 0) |
| 2. Loaded-but-uncalled | Code is in an imported file, so it is in the AtomSpace / Python namespace, but nothing invokes it | The function/atom is defined and loaded; grep finds zero call sites | Add the call site (wire it into the cycle at the right phase) | Object 3 sustained-work vocabulary (task-context, checkpoint, scope-drift); `soul_channel_d_lite_prompt` |
| 3. Not-even-loaded | The file is not in the import chain, so its atoms are not in the AtomSpace at all | The file is absent from lib_clarity_reasoning imports; its atoms cannot be matched at runtime | Import the file (then verify dependencies and behavior) | soul_eval.metta (its dependency atoms ARE loaded via observer_relativity, but the file itself is not) |

The diagnostic value: a surface that looks "broken" is triaged by tier before any repair is scoped. A tier-1 fix is a one-line gate change; a tier-2 fix is a wiring insertion (subject to artifact_0 hook discipline); a tier-3 fix is an import plus dependency and behavior verification. Confusing the tiers leads to over- or under-scoping the repair. Channel D is tier 1 (re-enable the gate), which is why its repair is potentially one line; soul_eval is tier 3 (import the file), which is why its repair is larger even though its dependencies happen to be satisfied.

### The three-tier taxonomy applied to the dormancy findings

1. **Wired-but-gated-off:** Channel D (loop 148-157) is complete and wired, dead only because `soul_is_pause` returns hardwired 0. Activation = re-enable the gate. **Berton's call** (deliberate disable).
2. **Loaded-but-uncalled:** object 3 sustained-work vocabulary (helper.py task-context/checkpoint/scope-drift) and the d-lite composer. The code is in imported files; nothing calls it. Activation = add the call site.
3. **Not-even-loaded:** soul_eval.metta substrate-native verdict. Not in the import chain; the file's atoms are not in the AtomSpace. Its dependency atoms, however, ARE loaded (Arc-033: defined in observer_relativity.metta, which is import line 28). Activation = import the one file (dependencies already satisfied) + verify the verdict-aggregation rule reduces correctly + replace or parallel the LLM verdict. Far-term, gated behind the soul-state-producer, but a narrower activation than "build the dependency tree."

### What is NOT a gap (correctly working)

- Surface 1 input evaluation: works, produces a substantive verdict.
- The aliveness gate: correctly mechanical idle-suppression, not a soul-voice surface; no governance gap.
- The `soul-llm-call` dispatcher: already the faculty/author shape (soul decides via prompt, LLM renders); the normal path simply bypasses it via `soul_send_assemble`.
- The mutation gate: records and locks soul-namespace mutations; it is a recorder, not an execution sheriff, which is its designed role.

### What this survey does not do

It does not prescribe the fix. It documents that the soul-state-producer is the convergent foundation, that Channel D re-enable is a separate deliberate decision, that object 3 and writeback hygiene are separate wiring efforts, and that the substrate-native verdict is a far-term pointer. The sequencing, scoping, and whether to proceed are design decisions for a separate step, with Clarity at the table on the substrate she authors.

---

## Appendix: Standing tags and disciplines for this survey

- Findings are [RUNTIME] (executes in the live cycle) or [DESIGN] (spec or built-but-unwired). Never merged.
- The file list grows by trace, not by declaration. Each file enters with why the trace led there.
- Where a finding depends on a helper not yet read, it is marked "pending helper read" rather than guessed.
- The survey describes; it does not prescribe the fix.
- Dormancy is tagged by tier: wired-but-gated-off, loaded-but-uncalled, not-even-loaded. The tier names the activation work. (Elevated to a named diagnostic tool with repair-path mapping per Clarity Arc-034.)
- Clarity reviewed the survey (Arc-034) and confirmed the three keystone findings (single convergence, object-3 unwiring, reasoning discard) and prompted the dormancy-taxonomy elevation. Her dependency correction (Arc-033) was independently confirmed from source (observer_relativity.metta read directly).
