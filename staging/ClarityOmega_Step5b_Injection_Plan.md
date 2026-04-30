# ClarityOmega: FREE Mode Directive Injection Plan
## Step 5b -- Documented April 23, 2026

---

## THE GAP

The supervisor directive fires correctly on FREE iterations and prints to the log.
But the LLM never sees it. The LLM receives `$send` (assembled by `soul_send_assemble`)
which contains the human-response prompt, not the supervisor directive.

The spec (Section 3) says: "On FREE iterations, the LLM receives concrete instructions
with success criteria." The current `println!` implementation does not satisfy this.

## WHAT WE KNOW

**soul_send_assemble** (src/helper.py line 327):
- Takes: prompt, soul_context, soul_verdict, person_state, soul_note, lastmessage
- Returns: concatenation of all parameters as one string
- This string becomes `$send` which goes directly to the LLM call
- Simple concatenation, no logic

**The current FREE mode check** (src/loop.metta line 144-148):
- Fires AFTER the LLM has already been called and responded
- Location: inside the PROCEED branch's progn, after $results are executed
- Too late to affect what the LLM does

**The LLM call** (src/loop.metta lines 94-98):
- Uses `$send` as the prompt
- `$send` is computed at lines 88-92 from `soul_send_assemble`

## THE PLAN

One change with two parts:

**Part 1: Compute the idle directive BEFORE $send assembly**

Add a new binding in the let* chain, BEFORE the `$send` line (before current line 88).
This binding computes the FREE mode directive:

```metta
($idle_directive (if (and (not $msgnew)
                          (> (get_time) (+ (get-state &last_human_time) (wakeupInterval))))
                     (py-call (helper.soul_idle_goal_prompt
                                (py-call (helper.extract_username $msg)) ""))
                     ""))
```

When in FREE mode: `$idle_directive` contains the full supervisor directive.
When NOT in FREE mode: `$idle_directive` is an empty string.

**Part 2: Include $idle_directive in $send**

Modify `soul_send_assemble` to accept one additional parameter and append it.
Add a 7th parameter for the idle directive:

```python
def soul_send_assemble(prompt, soul_context, soul_verdict, person_state, soul_note, lastmessage, idle_directive=''):
    # ... existing code ...
    result = (str(prompt) +
              " SOUL_CONTEXT: " + str(soul_context) +
              " SOUL_VERDICT: " + verdict_summary +
              " PERSON_STATE: " + str(person_state) +
              note_section +
              " " + str(lastmessage))
    idle_str = str(idle_directive)
    if idle_str and len(idle_str) > 5:
        result = result + " IDLE_DIRECTIVE: " + idle_str
    return result
```

And update the MeTTa call to pass the new parameter:

```metta
($send (py-call (helper.soul_send_assemble
                $prompt $soul_context_in $soul_verdict_in
                $person_state
                (soul-extract-flag-note $soul_verdict_in)
                $lastmessage
                $idle_directive)))
```

**Part 3: Remove the old println! FREE mode check**

Delete or comment out the current FREE mode check from lines 144-148 (inside the
PROCEED branch's progn). It is replaced by the pre-assembly computation.

## WHY THIS WORKS

- The FREE mode check moves from AFTER the LLM call to BEFORE the $send assembly
- The directive becomes part of the prompt the LLM sees
- On ENGAGED/ATTENDING iterations, $idle_directive is "" and $send is unchanged
- On FREE iterations, $send includes the supervisor directive with GOAL, ACTION, DONE WHEN
- The LLM receives concrete instructions instead of aimless context
- soul_send_assemble gains one optional parameter -- backward compatible (default "")
- The paren structure change is minimal: one new let* binding, one parameter addition

## FILES CHANGED

1. src/helper.py -- add `idle_directive=''` parameter to soul_send_assemble (line 327)
2. src/loop.metta -- add $idle_directive binding before $send, pass to soul_send_assemble, remove old println! check

## RISK

Low. The $idle_directive binding is self-contained. If it errors, it returns "".
The soul_send_assemble change is backward compatible (default parameter).
The LLM already handles varying prompt lengths gracefully.

## VERIFICATION

After rebuild:
1. Container iterates normally
2. On idle iterations beyond wakeupInterval, $send includes "IDLE_DIRECTIVE:" section
3. The LLM's RESPONSE should reference the goal directive instead of "Cycle XXXX. WAITING."
4. On ENGAGED iterations (human message), $send has no IDLE_DIRECTIVE section
