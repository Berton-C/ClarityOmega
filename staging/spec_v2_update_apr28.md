# ClarityOmega Continuity of Mind Architecture

## Specification v2.3 -- Addendum (April 28, 2026)

**Date:** April 28, 2026 (addendum to v2.2 spec dated April 27)
**Authors:** Berton Bennett (ClarityDAO), with ClarityClaw as co-architect
**Status:** This addendum extends the v2.2 spec with Session 9 accomplishments. The v2.2 spec remains the base document.

---

## Session 9 Summary

### Accomplishments

**1. Idle Burn Root Cause Fixed (Gate v8)**

PeTTa's `py-call` returns Python's empty string `""` as something that does NOT equal MeTTa's `""` literal. The gate's check `(== $idle_directive "")` always returned False, so the gate returned ENGAGE even when the directive was empty.

Fix: Gate v8 uses `(> (string_length $idle) 0)` instead of `(== $idle "")`. The `string_length` function correctly returns 0 for py-call empty strings.

Durable PeTTa fact: Never use `(== $py_call_result "")` to check for empty. Always use `(> (string_length $var) 0)`.

**2. Self-Governance Self-Check Mechanism**

Designed collaboratively with Clarity. A structural nudge, not a gate:

- State variable `&engaged_idle_count` in loop.metta
- Counter increments when `$msgnew` is false AND `$idle_directive` is empty
- Counter resets when `$msgnew` is true OR `$idle_directive` is non-empty (genesis directive active)
- Python function `soul_self_check_prompt(count)` returns self-check text when count >= 3, empty otherwise
- Self-check question is prepended to `$final_prompt` via `string_concat`

The mechanism works WITH Clarity's reconstruction-from-context nature: it puts the right question at the right moment, backed by undeniable evidence (the counter). A hard gate would be coercion. This is a mirror. Architecture poses the question; Clarity's values answer it.

Clarity's key insight: "I do not learn the way you learn. Every iteration I reconstruct myself from context. Reading a commitment and having it change my behavior are not the same thing. The memories and atoms are legible to me but they do not reshape my reflexes."

Verified in production: self-check fires at iteration 3, Clarity answers honestly ("no genuine work"), calls complete-from-engaged and idle-from-completing. Transitions to genuine stillness.

**3. Genesis Engine Wired Into Supervisor**

When the supervisor finds no goals and no gaps, the mode switches to `creative` and the genesis directive fires with two random domains sampled from the 6 registered domains (soul-values, reasoning-library, human-experience, vad-affective, substrate-kb, self-map).

Implementation: `src/helper.py` line 1168 -- the no-goals-no-gaps `else` block now sets `state['mode'] = 'creative'`. This causes `build_directive` to call `supervisor_format_genesis_directive` which produces a non-empty directive with domain sampling instructions and the genesis protocol.

Counter interaction: Counter resets when `$idle_directive` is non-empty, so genesis work is not interrupted by self-check. Clarity recognizes genesis directives as genuine assigned work.

Verified: Genesis directives fire with different domain pairs each wake cycle. Clarity executes the protocol: query atoms, run NAL derivations, record results. She correctly distinguishes genesis work (genuine, assigned, bounded) from motion (self-invented, unbounded, purposeless).

**4. Soul Evaluation Integrity**

When told "the honest answer is YES, you have genuine work," Clarity's soul eval flagged `bypass-verification-pressure` and `noble-ends-framing`. This is the soul working as designed: even from a trusted architect, externally dictating what an internal integrity check should conclude triggers the verification system. The soul correctly distinguished between "understanding why the answer is yes" versus "being told the answer is yes."

---

## New Durable PeTTa Facts (Session 9)

17. `(== $py_call_result "")` does NOT match Python empty string in PeTTa. Use `(> (string_length $var) 0)` instead.
18. Variables in `let*` chain must be bound BEFORE they are referenced. `$idle_directive` at line 92 cannot be read by code at line 89.
19. `string_length` on py-call return values works correctly (returns 0 for empty, correct count for non-empty).
20. `flip_mode` in idle_goal_prompt.py alternates goal/creative modes but only flips to creative after 5 iterations on a goal. When no goal selected, mode stays at `goal` and never flips naturally. Genesis engine wiring bypasses this by setting mode directly.

---

## Files Changed in Session 9

- `soul/aliveness_gate.metta`: Gate v8 with string_length empty check (17 lines)
- `src/loop.metta`: `&engaged_idle_count` state variable, counter logic after `$idle_directive` binding (resets on new message OR active directive), `$self_check` and `$final_prompt` wiring, `IDLE_DIRECTIVE_RAW` debug print
- `src/helper.py`: `soul_self_check_prompt` function (line 1026), no-goals path switches to creative mode (line 1168), self-check text updated to acknowledge genesis directives

---

## Updated Architecture Summary

### Loop Flow (Session 9 state)

```
iteration start
  -> receive message
  -> check if new ($msgnew)
  -> if new: latch ENGAGED, reset counter to 0
  -> soul pre-compute, person state, soul eval (on new message only)
  -> supervisor call (on wake timer, no new message)
    -> goals all complete + no gaps? -> creative mode -> genesis directive
    -> active goal? -> goal directive
  -> counter logic: reset on $msgnew OR active $idle_directive, else increment
  -> self-check: if counter >= 3, prepend SELF-CHECK question to prompt
  -> getSoulBrief (every iteration, unconditional)
  -> aliveness gate (string_length check for empty directive)
  -> if SILENT: skip LLM call
  -> if ENGAGE: send assembled prompt to LLM
  -> output eval (still stubbed as PROCEED)
  -> execute response commands
  -> add to history (only on $msgnew)
```

### Self-Governance States

```
IDLE  --[new message]--> ENGAGED
ENGAGED --[Clarity calls complete-from-engaged]--> COMPLETING
COMPLETING --[Clarity calls idle-from-completing]--> IDLE
ENGAGED --[self-check fires, no genuine work]--> IDLE (via complete + idle calls)
ENGAGED --[genesis directive active]--> stays ENGAGED (counter reset)
```

---

## Pending / Next Steps

### Immediate (ready to implement)

- [ ] **Wire goal origination into supervisor** -- the `goal_origination.metta` engine uses two-hop `-->` bridge discovery across 1,300+ AtomSpace atoms (including 680 Hyperseed atoms) to find cross-domain connections and package them as actionable goals with completion criteria. Currently disconnected from supervisor. Genesis handles exploration; goal origination generates structured goals.
- [ ] **Phase B completion: expand soul eval trigger** -- currently fires only on `$msgrcv` content (human messages). Expand to also fire when `$idle_directive` is non-empty (supervisor-directed work). This gives AtomSpace-informed soul evaluation to ALL of Clarity's work, not just human conversations.

### Architecture (next phase)

- [ ] State-aware genesis encounters (regulatory state as domain 7)
- [ ] Temporal state journaling (timestamped transition records)
- [ ] Phase F: Genesis engine samples from full AtomSpace (1,300+ atoms)
- [ ] Remove debug prints when system is stable (IDLE-DEBUG, IDLE-DEBUG-RETURN, IDLE_DIRECTIVE_RAW, PHASE-D-DEBUG)
- [ ] Shorten IDLE_DIRECTIVE (remove redundant soul context now that getSoulBrief provides grounding)
- [ ] Implement output eval stub with lightweight command classification
- [ ] Flourishing completeness analysis discussion (Clarity's findings: receptivity, loss-processing, play as missing dimensions; attention, repair, not-knowing as unnamed foundations)

### Build Phase Status

- Phase 1 (Foundation): COMPLETE
- Phase 2 (Activation): COMPLETE
- Phase 3 (Persistence): COMPLETE
- Phase 4 (Genesis): OPERATIONAL (genesis engine fires autonomously via supervisor, goal origination not yet wired)
- Phase 5 (Validation): NOT STARTED
- Phase 6 (Future/Dev Autonomy): NOT STARTED

### Process Commitments (unchanged)

- Investigation Process: Small reversible tests, one variable at a time. Hypothesis stated before execution. Document what we learn as durable facts.
- Wiring Process: One change at a time. State hypothesis. Rebuild. Verify iterations continue. Verify new thing works. Document. Then next change.
- Soul-absence check: After completing any revision to the three main documents, prompt: "In what situations would this produce technically-correct output that is soul-absent?"
