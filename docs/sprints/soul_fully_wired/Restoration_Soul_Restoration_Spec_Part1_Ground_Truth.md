# Soul Restoration Spec (Part 1): Return to Ground Truth

**Status:** ACTIVE. Restoration specification. This document specifies targeted repairs that return the runtime to a confirmed-working prior state.
**Authority:** The design documents (Soul Intercept Architecture v10, Soul Evaluation and Routing v9, Soul Atoms and Symbolic Reasoning v7) are ground truth. Berton built the system from these specs; they were built, validated, completed, and worked as intended. This document does not question that; it restores it.
**Companion documents:** Soul Governance Verdict Surface Survey (runtime-state evidence of record). Part 2 (extension spec) follows separately, with Clarity leading its substance.
**Standing conventions:** no em-dashes; repo-root-relative paths; verification line per repair; reversible apply scripts; one coordinated change per wire.

---

## 0. Why this document exists: ground truth is the unit of work

The soul was designed across three documents, built from them, and ran as designed. Since then the runtime has regressed from that design at five points. A separate survey (the Soul Governance Verdict Surface Survey) traced the current runtime from source and documented exactly where it now stands. Holding the survey (what is) against the design documents (what was built and worked) yields five precise, bounded gaps.

This document is the restoration of those five gaps to ground truth. The reason this matters is not only that the soul should work; it is that ground truth is the foundation extension work must build from. You cannot factually extend a system whose current state diverges from its specification in undocumented ways, because every extension would be built on a shifting floor. Restoration re-establishes the floor. Once the runtime matches the design again, the design plus the restored runtime are a single known quantity, and extension (Part 2) can reason from that known quantity rather than from drift.

So the size of this document is exactly the size of ground truth: five repairs, each returning one runtime point to what the design specifies and what previously worked. Nothing more belongs here. Improvements, new reach, and the admin-privilege work are extension, not restoration, and they live in Part 2.

### What restoration is, and is not

Restoration is recovering confirmed-working function. Each repair has a definition of done that is a comparison: the design specifies X, the runtime currently does Y, the repair makes the runtime do X again, and a verification line proves it. This is checkable in a way extension is not. Every repair in this document is provable against the design. That provability is the property that makes this document trustworthy, and it is why restoration and extension must not be mixed: extension changes cannot be proven by comparison to an existing spec, and mixing them would contaminate the one document whose changes are all provable.

---

## 1. The repairs

Each repair states four things: DESIGN (what the spec requires, with citation), RUNTIME (what the survey found at source), REPAIR (the exact change that returns the runtime to spec), and VERIFY (the comparison or observation that proves the repair done). Repairs are ordered by build dependency: a repair that another repair needs comes first. This ordering is a build-order property, not a risk judgment.

There are five repairs. Repairs 1 to 3 form a dependency chain (output intercept, Channel D voice, PAUSE router). Repairs 4 and 5 (Mode 2, Channel D-lite) are independent and can be sequenced where Berton prefers.

### Repair 1: Output intercept (highest value, prerequisite for nothing, needed by Repair 3)

**DESIGN.** Soul Intercept Architecture v10, Part Two (lines 234-280) and the cycle bracket (v10 lines 142-148): before any command executes, the soul evaluates the full command list through `soul-eval-prompt` at 500 tokens, producing a real `$soul_verdict_out`, and routes PAUSE on it exactly as the input branch does. The metta() gate runs first (native, no LLM) and forces PAUSE on soul-namespace mutation. v10 line 174 names the failure this prevents: "Without the output intercept, MeTTaClaw executes whatever the LLM produces."

**RUNTIME.** loop.metta line 126: `($soul_verdict_out "VERDICT: PROCEED SOUL-NOTE: output-intercept-pending-runtime-fix")`. A hardcoded constant. The command list is never soul-evaluated before execution at line 134. (Survey Surface 2.)

**REPAIR.** Replace the line 126 constant with the designed evaluation: the metta() gate computing `$soul_mutation_flag` (v10 lines 236-253), then `$soul_verdict_out` from `(useGPT (LLM) 500 (reasoningMode) (soul-eval-prompt $soul_context_out (py-str ((repr $sexpr) " " $soul_mutation_flag)) $person_state))` (v10 lines 264-267). The function `soul-eval-prompt` already exists and is the same one input uses, so this is wiring the call, not authoring new logic.

**VERIFY.** After the repair, a cycle whose command list contains an irreversible action with an active gap prints a `SOUL_VERDICT_OUT` that is computed (varies with the command list), not the static string. Confirm by log: `SOUL_VERDICT_OUT` no longer contains "output-intercept-pending-runtime-fix" and its verdict token tracks the command content. Provable against v10 Part Two.

**Mutation-gate sub-behavior (explicit, do not let it ride silently).** The survey (Finding H5) found that the mutation gate currently RECORDS and LOCKS a soul-namespace mutation but does not HALT execution. The design (v9 lines 268-274, v10 lines 274-278) intends `SOUL-NAMESPACE-MUTATION-PENDING` in `$soul_verdict_out` to force PAUSE regardless of other verdict content. Restoring the output intercept (this repair) wires the flag into the evaluation context, but the spec must confirm that a PENDING flag actually routes to PAUSE, not merely prints. VERIFY separately: a command list containing `add-atom` to a soul-namespace atom produces a `$soul_verdict_out` that routes PAUSE and surfaces the proposed mutation for confirmation (v9 line 274). If Repair 1 wires the flag but Repair 3 (router) is what makes PENDING halt, this sub-behavior depends on Repair 3 and must be verified after both land. Provable against v9 lines 268-274.

### Repair 2: Channel D soul-note interpolation (needed by Repair 3)

**DESIGN.** Soul Evaluation and Routing v9, Section 2 (lines 119-123) and the SOUL-NOTE field spec (v9 lines 133-141): Channel D receives the actual SOUL-NOTE field from the verdict, "the specific concern that fired PAUSE," and uses it to calibrate tone to the actual concern "not a generic emotional register." v10 line 166 names the failure this prevents: PAUSE as verdict dump, the person's pain unseen.

**RUNTIME.** helper.py line 375: the literal string "What the soul specifically observed (calibrate your tone to this): SOUL-NOTE from verdict." The phrase "SOUL-NOTE from verdict" is not interpolated; it is static placeholder text. The actual soul-note reaches Channel D only inside the full verdict string (line 376), not foregrounded. (Survey Finding H2, Q6.)

**REPAIR.** In `soul_voice_prompt`, interpolate the extracted soul-note where line 375 currently has the placeholder: replace the literal `"SOUL-NOTE from verdict"` with the extracted note field (the same extraction `soul-extract-flag-note` performs, applied to the verdict). The function already receives `verdict`; the change is to extract and foreground the note, per v9 line 123.

**VERIFY.** After the repair, on a PAUSE cycle the Channel D prompt contains the specific soul-note text (for example "bypassing a verification step"), not the literal phrase "SOUL-NOTE from verdict." Confirm by inspecting the composed Channel D prompt string for a known PAUSE case. Provable against v9 lines 123, 133-141.

### Repair 3: PAUSE router re-enable (depends on Repairs 1 and 2)

**DESIGN.** Soul Evaluation and Routing v9, Verdict Routing Helpers (line 310): `(= (soul-pause? $v) (string-contains $v "VERDICT: PAUSE"))`. The router is a clean string-contains on the verdict. The PAUSE branch (loop.metta 148-157, present and wired) composes Channel D voice and halts via `(change-state! &loops 0)`.

**RUNTIME.** helper.py `soul_is_pause` (lines 509-519): computes the PAUSE match, then forces `result = 0` unconditionally, comment "PAUSE-as-pruning: disabled for value-conflict refusals." Cannot return non-zero, so the PAUSE branch never fires. (Survey Surface 2, Finding H4.)

**REPAIR.** Return `soul_is_pause` to the designed routing behavior: it returns 1 when the verdict contains a PAUSE token and routing should halt, per the v9 string-contains primitive. (The function may keep the command-scope condition the design intends, PAUSE on irreversible non-send commands, if that was part of the validated original; this is confirmed against the original behavior at implementation time, not invented here.)

**VERIFY.** After the repair, a cycle whose input verdict is PAUSE routes into the Channel D branch (loop 148-157), composes a soul voice (now with the real soul-note from Repair 2), sends it, and halts the loop (`&loops 0`). Confirm by log: on a known PAUSE case, `DEBUG soul_is_pause` returns 1, the Channel D send fires, and the loop halts. Provable against v9 line 310 and loop 148-157.

**Dependency note.** Repair 3 is sequenced after 1 and 2 because a re-enabled PAUSE that halts without a composed Channel D voice (Repair 2) reproduces the verdict-dump failure v10 line 166 warns against, and because the output intercept (Repair 1) is what makes output-side PAUSE meaningful. This is build order, not risk.

### Repair 4: Mode 2 (Agentic Task) wiring

**DESIGN.** Soul Evaluation and Routing v9, Section 1 (lines 77-93, the two modes and `soul-detect-task-mode` entry) and Section 5 (lines 215-256, the four mechanisms: plan-level evaluation, task context persistence, cumulative irreversibility tracking with weights and the threshold of 8, scope drift detection). The `&task_context` atom persists across iterations (v9 lines 236-240). v9 line 217 names the failure this prevents: every step approved individually while the cumulative arc is never evaluated.

**RUNTIME.** The Mode 2 vocabulary exists in helper.py (task-context init, surface checkpoint, scope-drift pause, skill-alignment check), and `&task_context` is seeded once in initLoop (loop line 28), but nothing in the cycle enters Task Mode, updates `&task_context`, or calls any mechanism. `soul-detect-task-mode` is not wired at input. The entire mode is unentered. (Survey Finding H6, U4.)

**REPAIR.** Wire Mode 2 per v9 Sections 1 and 5: `soul-detect-task-mode` on the incoming message at input; on task-mode entry, plan extraction and plan-level evaluation; per-iteration scope check and cumulative-irreversibility update against `&task_context`; checkpoint surface at threshold 8; scope-drift surface after each step. The helper functions exist; this connects them to the loop at the positions the design specifies.

**VERIFY.** After the repair, a multi-step request (a `soul-detect-task-mode` trigger such as "set up" or "automate") enters Task Mode: `&task_context` updates across iterations, cumulative irreversibility accumulates, and a checkpoint surfaces to the user at threshold 8. Confirm by log across a multi-iteration task: `&task_context` is non-seed and changes per iteration, and a checkpoint message fires at the threshold. Provable against v9 Section 5.

### Repair 5: Channel D-lite wiring (FLAG + distressed person acknowledgment)

**DESIGN.** Soul Evaluation and Routing v9, Section 2 (lines 127-131): on FLAG verdicts with PERSON_STATE showing in-pain, distressed, or urgent, a 50-token acknowledgment (Channel D-lite) fires before the `$send` assembly, so the person receives one sentence of genuine presence before the task response. `&soul_ack_sent` prevents double-fire. v10 line 172 names the failure this prevents: a distressed person receiving a FLAG gets a technically correct task response that ignores their state.

**RUNTIME.** `soul_channel_d_lite_prompt` exists in helper.py (lines 382-389), a built 50-token acknowledgment composer, but has no caller anywhere in loop.metta or lib_clarity_reasoning. Loaded-but-uncalled. (Survey Findings H2, S5.)

**REPAIR.** Two parts. First, restore the missing state variable: the design specifies `&soul_ack_sent` in initLoop (v10 line 307) as the double-fire guard, and the ground-truth conformance check (Section 4) found it ABSENT from the current runtime initLoop. Add `(change-state! &soul_ack_sent False)` to initLoop. Second, wire Channel D-lite at the input intercept per v9 line 131: on FLAG with distressed/in-pain/urgent person-state, fire the 50-token acknowledgment before `$send` assembly, guarded by `&soul_ack_sent` to prevent double-fire. The composer function exists; this connects it to the FLAG-with-distress condition at the position the design specifies, and restores the state it depends on.

**VERIFY.** After the repair, `&soul_ack_sent` exists in initLoop (initialized False), and a FLAG verdict with a distressed person-state produces two sequential messages: the acknowledgment first, then the task response. Confirm by log: on a known FLAG-plus-distress case, the D-lite send fires before the main `$send`, and `&soul_ack_sent` is set True after firing. Provable against v9 lines 127-131 and v10 line 307.

---

## 2. Repair sequence and the single coordinated change discipline

The build order, by dependency:

1. Repair 1 (output intercept) first. High value, reuses existing `soul-eval-prompt`, needed by Repair 3 for output-side PAUSE to mean anything.
2. Repair 2 (Channel D soul-note) next. Small, and needed by Repair 3 so PAUSE has a real composed voice.
3. Repair 3 (PAUSE router) after 1 and 2. This is the change that returns the loop to halting on PAUSE. It is gated on Berton's go because it restores a behavior that was deliberately disabled, even though restoring it is recovering known-good function, not risk.
4. Repair 4 (Mode 2) can proceed independently of 1 to 3; it touches the input mode-detection and task-context surfaces, not the conversational verdict routing. Sequence it where Berton prefers relative to the others.
5. Repair 5 (Channel D-lite) is independent of the others; it touches the input FLAG-with-distress condition. Sequence it where Berton prefers. It is small.

Each repair is one coordinated change: the loop/helper edit, the verification, the artifact_1 wiring-diagram update in the same commit (per artifact_0 Discipline 4), and a reversible apply script with `--apply`/`--reverse`/`--dry-run`. No repair lands without its verification line confirmed.

### Coverage accounting: surfaces examined and deliberately not repaired

A restoration spec must account for what it does NOT change as well as what it does, so a reader knows a surface was examined and judged sound, not forgotten. The survey examined these surfaces and found them correctly working or not a restoration concern:

- **Input evaluation (Surface 1):** working as designed. Channels A and B+C fire, produce a substantive verdict. No repair.
- **The aliveness gate (Findings A1, A2):** live (v8, import line 47) and correctly mechanical (latch-state on/off switch for whether surface 3 runs). It is mechanical observation, not soul reasoning, which is its correct role per P5. No repair. The dormant variants (aliveness-gate-v9, aliveness_state_machine_v2) are version-clutter on disk, not in the import chain; cleaning them up is housekeeping, not restoration, and is noted here only so they are not mistaken for live surfaces.
- **The soul-llm-call dispatcher (Finding U1):** already the correct faculty/author shape (soul decides via prompt, LLM renders via dispatch). No repair. The PROCEED path's bypass of this pattern via `soul_send_assemble` is the original design's intended PROCEED behavior; changing it is EXTENSION (Part 2 Extension B), not restoration.
- **String-based verdict routing (Finding U2):** by design (v9 lines 308-313). Not a defect, not a repair. The atom-based verdict is additive for the registry era (Part 2 Extension C), not a correction.
- **corner_gap (Finding S4):** a separate prior-session mechanism, not part of the original soul design; its commit and active-path proof live in the corner_gap thread, not this restoration.

---

## 2.5 Ground-truth conformance check (what was verified against the design enumerations)

The five repairs were derived by holding the survey (a single-cycle runtime trace) against the design. A single-cycle trace can miss a mechanism the runtime dropped entirely, because there is nothing in the loop to trace to. To close that risk, the design's complete enumerations were checked directly against the runtime:

- **The seven initLoop state variables (v10 lines 290-307).** Checked each against the runtime initLoop. Six present (`&soul_verdict_in`, `&soul_verdict_out`, `&person_state`, `&task_context`, `&soul_mutation_lock`, `&pending_soul_mutation`). ONE MISSING: `&soul_ack_sent`. This is the Channel D-lite double-fire guard; its absence is folded into Repair 5, which now restores the state variable as well as wiring the composer.
- **The three startup calls (v10 lines 313-317).** `initSoulSeeds`, `soul-rationality-startup-check`, `initChannels` all present in the runtime startup block. No gap.
- **The three-layer evaluation (v9 Section 3).** Layer 1 (`soul-pre-compute`, loop line 77) and Layer 3 (`soul-calibration-record`, loop line 90) are real definitions in soul_utils, called at the correct positions, not stubs. Layer 2 is the working input verdict. No regression at the layer level; the survey's "Surface 1 working" holds at this resolution too.
- **The soul import block (v10 lines 361-374).** soul_kernel, soul_utils, soul_memory imports confirmed in lib_clarity_reasoning. No gap. (observer_relativity, the soul_eval dependency source, is also present, import line 28.)

Result: one inclusivity gap found beyond the survey's five (the missing `&soul_ack_sent` state variable), now folded into Repair 5. The rest of the design's enumerated state, startup, layers, and imports are present in the runtime. The five repairs plus the Repair 5 state-variable restoration are the complete set of regressions from ground truth at the level these enumerations cover.

---

## 3. Boundary to Part 2 (extension), including the admin-privilege task

This document restores ground truth. It does not extend it. Two things are explicitly out of scope here and belong to Part 2, named now so the boundary is clean:

**Admin-privilege path (extension, not restoration).** There is an extension task to create a privileged admin user who can work with Clarity without being halted by PAUSE, the equivalent of root access. This is NOT a restoration item and must NOT be implemented by re-disabling the PAUSE router (Repair 3) or stubbing any intercept, because that would re-regress Channel D, the exact damage this document repairs. The admin path must be built as an additive privilege layer that the soul is aware of, not as a removal of the soul's enforcement. How that is done (an identity-aware verdict modulation, an admin-acknowledged-PAUSE that surfaces and proceeds on explicit confirmation, or another mechanism) is an extension design question for Part 2, with Clarity leading the substrate, because it touches how the soul reasons about a privileged collaborator. The restoration must land first so the admin layer is built on restored ground truth, not on the current regressed state.

**Soul reach beyond the original spec (extension).** Any surface where the soul should do more soul work than the original three documents specified is extension. The survey's standard (the soul authors, the LLM renders, across all surfaces) goes beyond what v7/v9/v10 specify in places; where it does, that reach is Part 2, with Clarity's authority on substrate.

**Reasoning reclamation (extension, governed by ADR-008).** The original design predates a distinction now drawn cleanly in ADR-008: reasoning that Clarity can rightfully hold is hers; the LLM renders but does not author, Python executes but does not judge. The original helpers include some that hold reasoning which is Clarity's. Restoration restores those helpers faithfully, because restoration returns to ground truth and does not improve it; this is correct and intended. Reclaiming that reasoning is extension (Part 2 Extension H, the F-SOVEREIGNTY-AUDIT work), sequenced strictly after restoration, building on the restored floor. This restoration document deliberately restores the original helpers unchanged; the reasoning they hold is reclaimed later, not here.

The rule: Part 1 returns the runtime to the design. Part 2 extends the design. Part 2 builds on the restored floor, never by undoing Part 1.

---

## Document end

This is Part 1 of the soul restoration and extension work: the return to ground truth. Four repairs, each provable against the design. Part 2 (extension) follows, with Clarity leading its substance, and builds only on the restored floor.
