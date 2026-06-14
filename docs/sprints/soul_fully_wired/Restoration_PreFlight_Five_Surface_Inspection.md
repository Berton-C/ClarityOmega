# Restoration Pre-Flight: Five-Surface Inspection Findings

**Status:** Read-only inspection. No edits made. This is the per-repair pre-flight required before any apply script is written, per the rule that no repair reverts a surface that has correctly moved forward.
**Method:** Inspected each repair target's live state, writers, and consumers from the project-copy source (loop.metta, helper.py, soul_utils.metta, lib_clarity_reasoning). Points that must be confirmed against the live container before a script is written are marked CONFIRM-LIVE.
**Verdict per surface:** CLEAN RESTORATION (restore as the spec describes) or RECONCILE (forward state exists; restoring the literal original would revert it or break a consumer, so the repair must adapt).

---

## Surface 1 (Repair 1, output intercept): RECONCILE

**Live state.** Not the original v10 design, and not a bare stub. A partial intermediate. loop.metta around line 126:
- `$soul_verdict_out` is the hardcoded string (as the survey found).
- BUT `$metta_cmds` (line ~129) and `$soul_mutation_flag` (line ~131, calling `helper.soul_mutation_gate`) ARE computed in the live runtime, after the hardcoded verdict.
- The mutation flag is computed and then NOT fed into any verdict. In v10, the flag feeds the soul-eval-prompt call that produces the verdict; here it is bound and dropped.
- `$soul_verdict_out` is consumed only by line 132 (soul-note-record on non-proceed, which never fires because the verdict is hardcoded PROCEED).

**Writers.** loop line 26 (initLoop seed), loop line 126 (the hardcoded bind).
**Consumers.** loop line 132 (soul-note-record, inert). No other consumer. The mutation flag has no verdict consumer.

**Why RECONCILE, not clean restoration.** A blind paste of the v10 output-intercept block would overwrite the already-present `$metta_cmds` and `$soul_mutation_flag` computation, risking duplication or breakage of the partial wiring that exists. The repair must restore the verdict computation (feed the command list and the existing mutation flag into soul-eval-prompt) while preserving and connecting the mutation-gate machinery that is already wired, not recreating it. The forward state here is partial and disconnected, but it is present and must be reconciled, not steamrolled.

**CONFIRM-LIVE.** The exact live line numbers and surrounding text of the `$metta_cmds` / `$soul_mutation_flag` / `$soul_verdict_out` block in `src/loop.metta`, so the apply script anchors on real text and wires into the existing mutation-flag computation rather than duplicating it.

---

## Surface 2 (Repair 2, Channel D soul-note): CLEAN RESTORATION

**Live state.** `soul_voice_prompt` (helper.py 369-380) has the literal placeholder "SOUL-NOTE from verdict" at line 375, as the survey found. `soul-extract-flag-note` exists in soul_utils (line 230) and is the extraction the repair reuses.
**Writers.** helper.py `soul_voice_prompt` constructs the prompt string.
**Consumers.** Channel D (loop 148-157) consumes the composed prompt.

**Why CLEAN RESTORATION.** No forward work has moved this surface past its original state. The repair is exactly as the spec describes: interpolate the extracted soul-note where line 375 has the placeholder. No reconcile needed.

**CONFIRM-LIVE.** That helper.py line 375 in the live container still reads the literal placeholder (the project copy and live should match here, but confirm before editing).

---

## Surface 3 (Repair 3, soul_is_pause): RECONCILE (a definitional discrepancy, not forward work)

**Live state.** `soul_is_pause` (helper.py 509-519) hardwired to return 0, as found. Single caller: loop line 148.
**Writers.** helper.py defines the function.
**Consumers.** loop line 148 only (the PAUSE branch gate).

**Why RECONCILE.** Not because of forward work, but because of a discrepancy between two possible restoration targets. The v9 routing primitive (line 310) specifies `soul-pause?` as a bare `string-contains "VERDICT: PAUSE"`. But this helper's docstring and dead `if match` block both reference "irreversible non-send commands", meaning the helper was apparently built to do command-SCOPED PAUSE (PAUSE only when irreversible commands are pending), not bare verdict-string PAUSE. These are two different behaviors. Restoring to the literal v9 primitive and restoring to the command-scoped helper behavior are different targets.

**CONFIRM-LIVE / DECISION FOR BERTON.** Which is the correct original behavior: (a) bare string-contains PAUSE per v9 line 310, or (b) command-scoped PAUSE per this helper's own docstring? This is a reconcile judgment about the validated original behavior, not a thing to assume. It is also the gated repair (re-enables deliberately-disabled halting), so it waits on Berton regardless.

---

## Surface 4 (Repair 4, Mode 2): RECONCILE (more built than the survey found, partly substrate-side)

**Live state.** More wired than the survey reported. The helper functions exist (helper.py 671-692: task-context init, update, checkpoint, scope-drift). AND a MeTTa layer exists in soul_utils (lines 287-346): `soul-detect-task-mode`, task-context update, checkpoint, scope-drift-pause are defined as MeTTa functions that call the helpers. Only the loop.metta call into this MeTTa layer is missing; loop has just the line-28 `&task_context` seed.
**Writers.** loop line 28 (seed) only, at runtime.
**Consumers.** None in loop (the MeTTa Mode 2 functions exist but are not called from the cycle).

**Why RECONCILE.** This is the forward-state case ADR-008 and Berton's warning are about. Some Mode 2 logic already lives substrate-side (the soul_utils MeTTa wrappers), not only in Python helpers. The repair must wire the loop into the EXISTING soul_utils Mode 2 functions, not recreate Mode 2 logic in Python or in the loop. Restoring by building new Python-side Mode 2 wiring would bypass and possibly conflict with the substrate-side wrappers already present. Wire to what exists.

**CONFIRM-LIVE.** That the live container's soul_utils.metta contains the same Mode 2 MeTTa functions (lines 287-346 in the copy) and that helper.py 671-692 match, so the loop wiring targets the real function names and signatures.

---

## Surface 5 (Repair 5, D-lite + soul_ack_sent): CLEAN RESTORATION (two clean parts)

**Live state.** `soul_channel_d_lite_prompt` exists (helper.py 382), uncalled. `&soul_ack_sent` returns nothing in loop.metta, confirming it is missing from initLoop (matches the conformance check).
**Writers.** helper.py defines the composer; the state var has no writer (it is absent).
**Consumers.** None (composer uncalled; state var absent).

**Why CLEAN RESTORATION.** No forward work to preserve. Both parts are additive: add the missing `&soul_ack_sent` state variable to initLoop, and wire the existing composer at the FLAG-plus-distress input condition. Nothing to reconcile.

**CONFIRM-LIVE.** That the live initLoop has no `&soul_ack_sent` (confirming the gap) and that helper.py 382 matches, before adding the state var and wiring the composer.

---

## Summary

| Surface | Repair | Verdict | Why |
|---------|--------|---------|-----|
| 1 Output intercept | 1 | RECONCILE | mutation-gate machinery already partly wired; connect, do not recreate |
| 2 Channel D note | 2 | CLEAN | literal placeholder, no forward work; interpolate as spec says |
| 3 soul_is_pause | 3 | RECONCILE | v9 bare-string vs helper's command-scoped: which is the validated original? (Berton decides; gated repair) |
| 4 Mode 2 | 4 | RECONCILE | MeTTa wrappers already substrate-side; wire loop to existing functions, do not rebuild in Python |
| 5 D-lite + ack_sent | 5 | CLEAN | both parts additive; no forward work |

**Two clean (2, 5), three reconcile (1, 3, 4).** Berton's warning was correct: three of five are not blind reverts. Surfaces 1 and 4 have forward state (partial mutation-gate wiring; substrate-side Mode 2 wrappers) that a literal restoration would overwrite or bypass. Surface 3 has a definitional discrepancy between the v9 primitive and the helper's built behavior that is a Berton decision.

**Each reconcile case will be brought to Berton before its script is written**, because the reconcile is a judgment about which state to restore toward, which is Berton's call, not Claude's. The clean cases (2, 5) can be scripted directly once their CONFIRM-LIVE points are checked.

**No apply script is written until its surface's CONFIRM-LIVE points are checked against the live container.**
