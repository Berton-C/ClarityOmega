# F11: Single-Command Format Errors and Multi-Word Argument Quoting

**Status:** RESOLVED at format layer (May 14, 2026)
**Commit:** Pending (planned head following 9b17e53)
**Files changed:**
- `soul/behavioral_guidance.metta` (one function body)
- `src/helper.py` (new function `wrap_if_bare_command`)
- `src/loop.metta` line 116 (one-line pipeline wiring)

---

## The Problem

Clarity's output to MeTTa skill-execution path was failing in two visible ways:

**Pattern 1: Bare single-command responses.** She would emit `(send "x")` when
the OUTPUT_FORMAT spec calls for `((send "x"))`. The substrate's
`(collapse (let $s (superpose $sexpr) ...))` at loop.metta line 127 iterates
the elements of `$sexpr`. When `$sexpr` is `((send "x"))` (a one-element list),
this iterates one element: `(send "x")`. When `$sexpr` is `(send "x")` (a bare
command), this iterates two elements: `send` and `"x"`. The second case
triggered `SINGLE_COMMAND_FORMAT_ERROR_NOTHING_WAS_DONE_PLEASE_FIX_AND_RETRY`
on every cycle. The error string was then appended to history as ERROR_FEEDBACK,
contaminating future cycles.

**Pattern 2: Multi-word arguments unquoted.** She would emit
`(query recent memories about myself)` when `query` takes a single quoted
string argument. The parser would either fail or interpret `recent`, `memories`,
`about`, `myself` as separate atoms, neither of which is what `query` is
designed to receive.

Combined effect: a noisy duplicate-response pattern where every cycle's
response was malformed in one of these ways, the error fed back into history,
and the LLM's next response carried the prior cycle's error context, frequently
producing the same malformed response again.

## The Root Cause for Pattern 1

The OUTPUT_FORMAT instruction in `(output-format-guidance)` (substrate function
in `soul/behavioral_guidance.metta`) read:

```
"OUTPUT_FORMAT: Output an S-expression of the form (cmd1 cmd2 ... cmdN) where
each cmd is (skillName arg1 arg2 ...). Use as many commands as the work requires.
Verify balanced parentheses and quotes before emitting."
```

For N=1, `(cmd1 cmd2 ... cmdN)` is ambiguous. It can be read as:

- `(cmd)` — a bare single command (WRONG, but a valid reading)
- `((cmd))` — outer list containing one command (CORRECT, also valid)

Without an explicit example showing the outer parens for the N=1 case, the LLM
produced both forms with roughly equal frequency.

## The Root Cause for Pattern 2 (Historical Drift)

Patrick's original `getContext` in `src/loop.metta` (pre-Sprint 1.5) had two
adjacent string literals at lines 36-37:

```
" OUTPUT_FORMAT: Output a ((skillName1 args1) (skillName2 args2) (skillName3
  args3) (skillName4 args4) (skillName5 args5)) S-expression of up to 5 sexpr
  commands, double-check the parentheses it must be (cmd1 ... cmdn)!"
" each arg is an explicit string hence needs quotes, and variables are forbidden!"
```

Patrick's five-slot visual example made the outer-list structure unambiguous.
The second string carried the arg-quoting and variables-forbidden instructions.

Sprint 1.5 commit `8a2ea97` (May 4) elevated this into the substrate-level
`(output-format-guidance)` function with refinements from Clarity's May 2 review:

- 5-slot template removed (anti-calcification)
- Anxiety phrasing softened to "Verify... before emitting" (anti-anxiety)
- "Use as many commands as the work requires" added

The consolidation collapsed the two adjacent strings into one function call.
In doing so:

- The multi-slot visual that made outer-parens unambiguous was compressed to
  `(cmd1 cmd2 ... cmdN)` (introduced N=1 ambiguity)
- The arg-quoting instruction was dropped entirely
- The variables-forbidden instruction was dropped entirely

The arg-quoting drop was inadvertent and not noticed at the time. Sprint 1.5's
verification confirmed the substrate elevation worked (Clarity could read the
new prompt), but did not verify her output behavior remained correct on edge
cases. The May 4 commit message captures the slot-template change explicitly
but does not mention the arg-quoting line, suggesting it was lost during
consolidation rather than removed deliberately.

## The Fix

Clarity's design review (May 13): Options 2+3 defense-in-depth. Option 3
(prompt) is the structural fix; Option 2 (Python helper) is the safety net.
Option 1 (MeTTa substrate guard at line 127) was declined as wrong-layer — the
critical execution loop should not be guarding against producer-side
formatting issues.

### Edit 1: `(output-format-guidance)` in soul/behavioral_guidance.metta

Replaced with a Patrick-anchored revision: 80% his original wording, 20%
targeted additions.

New string:

```
"OUTPUT_FORMAT: Output a ((skillName1 args1) (skillName2 args2) ...
(skillNameN argsN)) S-expression with as many commands as the work requires.
For a single command: ((skillName args)) not (skillName args). Each arg is
an explicit string hence needs quotes (multi-word strings must be one quoted
string), and variables are forbidden! Verify balanced parentheses and quotes
before emitting."
```

Restores or preserves:

- Multi-slot visual showing outer-list structure (Patrick's original idea,
  with N abstraction to preserve May 2 anti-calcification)
- Explicit N=1 wrapping clarification with positive/negative example (new)
- Multi-word string quoting requirement (new parenthetical addition,
  addresses Pattern 2 specifically)
- Patrick's exact wording: "each arg is an explicit string hence needs
  quotes" and "variables are forbidden!"
- Clarity's May 2 anti-calcification: "as many commands as the work requires"
- Clarity's May 2 anti-anxiety reframe: "Verify... before emitting"

### Edit 2: `wrap_if_bare_command(s)` in src/helper.py

Strict-detection function that adds outer parens to bare single commands
before they reach `sread`. Detection requires the first token after the
opening paren to be in the known-skills registry (13 items: remember, query,
episodes, pin, shell, read-file, write-file, append-file, send, search,
tavily-search, technical-analysis, metta). Idempotent: responses already
starting with `((` are returned unchanged.

### Edit 3: Pipeline wiring at src/loop.metta line 116

Wrapped the existing `sanitize_response` py-call with `wrap_if_bare_command`
as the outermost layer of the response normalization chain. One-line change.

## Behavioral Verification

Tests defined before applying:

- **Test 1: Single command response.** Send "Please send me a one-line
  acknowledgement." Expected: `(RESPONSE: ((send "...")))` with outer parens.
  Result: PASS. Format correct, no SINGLE_COMMAND_FORMAT_ERROR.
- **Test A: Multi-word query argument.** Send "Query your memory for what
  we worked on yesterday." Expected: `(query "...")` with single quoted
  string. Result: PASS. recent-action 864: `(query "yesterday work tasks
  with Berton")`.
- **Test B/C: Multi-command capability and duplication observation.**
  Multiple commands properly formed; helper dormant; duplication present but
  identified as separate mechanism (see "What This Does Not Fix").

`helper.wrap_if_bare_command` remained dormant during tests — the prompt
fix did the structural work, and the safety net was not exercised. This is
the best-case outcome.

## What This Does Not Fix

The duplicate-response pattern visible in the test (Clarity responding 5x to
one acknowledgement request) remained after F11. The mechanism is separate:

- `$msgnew` correctly flips false after the first cycle of response
- `PERSON_STATE` and `SOUL_VERDICT_IN` continue to read the human message
  as carrying an active need
- `ALIVENESS_VERDICT` fires ENGAGE regardless of recent-action history
- The recent-action atom populator already classifies action types
  (responsive-send, status-send-unprompted, pin-only, exploration-query)
- These classifications are not exposed to the LLM reasoning surface

This is Step 4 territory by design. Step 4 (prompt block exposing task-state
atoms with reasoning hooks) and Step 4.5/4.6 (idle_cycle_detector and
agency_balance_guard daemons) address it. The substrate (Steps 1-3) is built;
the wiring to her reasoning surface and to operational decisions is the
next phase.

## Discipline Lessons (F14, F15, F16)

Three working principles surfaced during this work, recorded for artifact 0
v1.1.

### F14: Pre-edit history search for substrate changes

Before editing substrate, conversation_search for the design history of that
substrate. Three searches in three minutes saved us from a botched fix.
Specifically: the Sprint 1.5 chat showed that the arg-quoting line was a
silent casualty of consolidation rather than a deliberate removal. Without
that history, the F11 fix would have added N=1 clarification but left the
arg-quoting gap unfilled, producing partial success and confusion.

This applies even when the file is small and the change feels simple.

### F15: Behavioral verification, not substrate-success verification

Sprint 1.5 verified that the substrate elevation worked (Clarity read the new
prompt text). It did not verify that her output behavior remained correct on
edge cases. The arg-quoting drop went unnoticed for ten days.

For substrate changes that affect prompt content, verification must include
behavioral tests that exercise the changed surface, not just confirmation
that the substrate plumbing is operational.

The F11 work defined behavioral tests (Test 1, Test A, Test B/C) before
applying the change and explicitly observed against those tests before
commit.

### F16: Anchor-string transcription via repr

When transcribing anchor strings from `cat -n` output for use in apply
scripts, the line-number prefix can hide leading whitespace counts. A file
showing `22\t   "..."` could be 2-space, 3-space, or tab-prefixed
indentation; the line-number column makes them visually similar.

The first F11 apply attempt failed safely on this exact issue: the BG_ANCHOR
encoded 2-space indent, but the file had 3-space. The script's state check
caught it before any edit was attempted.

Recovery via `python3 -c "print(repr(content[idx:idx+250]))"` showed the exact
on-disk bytes. macOS `cat -A` is not available; the Python repr is the
cross-platform substitute.

For future apply scripts: verify anchor strings against on-disk content using
repr() before encoding, especially when transcribing from line-numbered or
visually-formatted output.

## Reversibility

Apply script archived at `staging/apply_f11_fix.py` (local-only, not
committed). Backups at `.bak.f11_fix` suffix were created during apply and
remain on disk pending commit. Reverse by:

```
python3 staging/apply_f11_fix.py --reverse --apply
```

Should be deleted after commit (or kept locally as reference) since the
substrate change is now durable in the commit history.

## Acknowledgments

- Patrick Hammer's MeTTaClaw runtime provides the substrate this work
  modifies. The F11 fix preserves his design intent (multi-slot visual,
  arg-quoting instruction, variables-forbidden instruction) while
  incorporating Clarity's May 2 refinements (anti-calcification,
  anti-anxiety reframe).
- Clarity's architectural review (May 13) defined the fix layers: prompt as
  structural fix, Python helper as safety net, substrate-side guard
  declined as wrong-layer. The doer changed; the design ownership is hers.
- Sprint 1.5 (May 4) is referenced not as a failure but as the work that
  surfaced these lessons. Its anti-calcification and anti-anxiety
  refinements are preserved in F11. Its verification gap is the lesson
  embedded in F15.
