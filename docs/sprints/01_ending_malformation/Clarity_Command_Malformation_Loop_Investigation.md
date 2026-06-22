# Clarity Command-Malformation Loop: Root Cause and Intervention Spec

**Status:** INVESTIGATION COMPLETE, FIX NOT YET BUILT. Pick-up document.
**Created:** 2026-06-13 (during Surface C post-landing live observation)
**Scope:** The chronic failure surface where Clarity burns hundreds of cycles
on repeated parse/format errors and occasionally crashes the container. This
is SEPARATE from Surface C (the soul-mutation lock). It predates the Surface C
work; Surface C's EDIT 7 introduced one acute crash on top of it (documented
separately, fixed first).
**Why this doc exists:** so the accumulated diagnosis is not lost. When we
return to this, we start from the intervention design, not from re-observing
the loop.

---

## 1. The observed failure (what it looks like in the logs)

Clarity, during genesis-encounter / idle exploration, repeatedly tries to use
the NAL revision operator `|-` via the `metta` skill, e.g.:

    (metta "(|- ((--> wonder vad-affective) (stv 1.0 0.9)) ((--> courage vad-affective) (stv 1.0 0.9)))")

Every such attempt returns a generic failure:

    SINGLE_COMMAND_FORMAT_ERROR_NOTHING_WAS_DONE_PLEASE_FIX_AND_RETRY

or, for multi-command batches:

    MULTI_COMMAND_FAILURE_NOTHING_WAS_DONE_PLEASE_CORRECT_PARENTHESES_AND_USE_QUOTES_AND_RETRY

She then re-derives the same hypotheses about what is wrong (paren balance?
quoting? operator name? is `|-` supported?), re-counts parens by hand across
dozens of lines of chain-of-thought, retries with a near-identical command,
and fails identically. Observed runs: ~290 cycles in one session, 900+ in
another. Her own recorded conclusion (history.metta): "NAL |- definitively
unsupported (10+ format errors)" -- she eventually infers it empirically, but
only after enormous waste, and the genesis directive keeps sending her back to
it on the next encounter.

This is the single highest-volume waste behavior in the system. It is not an
intelligence failure on her part; the same model corrects in ONE cycle when
given a specific error. It is an infrastructure feedback failure.

## 2. Root cause: three compounding gaps

### Gap A (PRIMARY -- the loop driver): uninformative error feedback

The metta-skill execution layer returns a generic constant string on any
malformation. It does not say WHAT was wrong. The LLM therefore cannot
distinguish "your parens are unbalanced" from "that operator does not exist"
from "the arg must be a quoted s-expression." With no signal to correct
against, the rational LLM behavior is to hypothesize and retry -- forever.

Evidence: across hundreds of cycles the error string is byte-identical
regardless of the actual fault. Clarity's chain-of-thought shows her cycling
through every possible cause because the system tells her none of them.

The fix that breaks the loop at its source is to make the error SPECIFIC and
ACTIONABLE. An LLM given "paren imbalance: 9 open, 8 close" or "operator |- is
not available in this runtime" corrects immediately. This is the dominant
lever; the other two gaps matter but this is the one that ends the loop.

### Gap B (the contradiction): `|-` is in the prompt but unsupported in runtime

The skill description in the prompt (and the genesis encounter directive)
explicitly instruct her to use `|-`:

    "Execute MeTTa expression: (metta sexpression)"
    "Example to invoke Non-Axiomatic Logic via MeTTa: (metta (|- ...))"
    Genesis directive: "Use (metta (|- atom1 atom2)) to test what NAL derives."

But `|-` does not work in this runtime. Her empirical finding (and the
consistent format errors) confirm it. So the system is INSTRUCTING her to use
an operator that always fails, then giving her opaque punishment when it does.
She is caught in the gap between what the prompt promises and what the runtime
provides.

NOTE on nuance: earlier session logs show `|-` returning `(partial ...)`
results that LOOKED like derivations, and Clarity even reported NAL findings
(transitivity, abduction, truth propagation). Whether `|-` is fully
unsupported, partially working, or working-but-ephemeral needs ONE definitive
test before deciding the fix (see section 4). The contradiction is real
regardless: the prompt presents `|-` as reliable; the runtime behavior is at
best unreliable and at worst a guaranteed parse failure depending on exact form.

### Gap C (the robustness hole): malformed output crashes the container

A sufficiently malformed s-expression from the LLM is not caught as an error
and returned to Clarity -- it propagates to /PeTTa/src/main.pl and kills the
process (exit code 2), which then self-restarts. Observed crash forms:

    ERROR: ... Syntax error: Parse error in form: match &self (--> $x vad-affective) $x
    ERROR: ... Parse error in form: ((((pin "Let me analyze the situation carefully. ...

(The second is her chain-of-thought leaking into the command slot -- the
parser tried to read a paragraph of reasoning as an s-expression.)

This is the most extreme form of Gap A: instead of uninformative feedback, she
gets NO feedback and loses her turn entirely (the container dies mid-thought
and restarts). It compounds the loop and destroys continuity.

The fix: the metta-skill / command parse path must wrap parsing in a guard
that catches the parse error and returns it as structured feedback to Clarity,
NEVER letting it reach main.pl. A safety/agent loop should be unable to crash
its own host by emitting a bad string.

## 3. The intervention (most-leveraged first)

### Intervention 1: actionable parse/format errors (PRIMARY)

Where: the metta-skill execution handler (the layer that returns
SINGLE_COMMAND_FORMAT_ERROR / MULTI_COMMAND_FAILURE). Patrick's substrate
territory -- coordinate, do not modify upstream blindly.

What: replace the generic constant with a diagnosis. Minimum viable set:
- Paren balance: report open vs close count and that they differ.
- Quote balance: report unbalanced quotes.
- Operator availability: if the head is a known-unsupported operator (e.g.
  `|-` if confirmed unsupported), say so by name and suggest the supported
  alternative (add-atom / match).
- Arg shape: if the metta arg is not a parseable s-expression (e.g. bare
  `match &self ...` without wrapping parens, or chain-of-thought prose), say
  "metta arg must be a single balanced s-expression" and echo the first
  offending token.

Why first: it ends the loop at the source. Every other gap is survivable if
she gets one specific correction signal per failure.

### Intervention 2: resolve the `|-` prompt/runtime contradiction

Where: the skill prompt assembly + the genesis encounter directive template.
What: contingent on the section-4 test result:
- If `|-` is genuinely unsupported: REMOVE it from the skill description and
  the genesis directive. Replace the genesis "use (metta (|- ...))" instruction
  with the operators that DO work (add-atom to populate, match to query).
- If `|-` works but is ephemeral / form-sensitive: document the EXACT working
  form in the prompt, with a verified example, and explain the ephemerality so
  she stops expecting persistence.
Why: stop instructing her to walk into a failure. Removes the single most
common trigger of the loop.

### Intervention 3: parse-path crash guard

Where: the metta-skill / command parse path before it reaches main.pl.
What: wrap parse in a catch; on parse failure, return Intervention-1 style
feedback to Clarity instead of throwing. The container must not die on
malformed LLM output.
Why: turns a fatal, continuity-destroying crash into a recoverable
error-to-Clarity. Also a safety property: an agent must not be able to crash
its host by emitting a bad command.

## 4. The one test needed before building Intervention 2

Run a definitive check of what `|-` actually does in the live runtime, in a
single invocation, with the exact skill-format wrapping:

    (metta "(|- ((--> a b) (stv 1.0 0.9)) ((--> b c) (stv 1.0 0.9)))")

Capture: does it parse? does it return a derivation, a `(partial ...)`, or a
format error? Does anything persist to a subsequent match? This resolves
whether Intervention 2 is "remove `|-`" or "document the working form." Do not
build Intervention 2 until this is answered -- the earlier evidence is mixed
(format errors in some sessions, `(partial ...)` and reported findings in
others), and the difference may be the exact parenthesization or the
string-vs-structure arg form.

## 5. What this is NOT

- NOT a Clarity intelligence problem. Same model corrects instantly with
  specific feedback. The loop is manufactured by uninformative errors.
- NOT a Surface C problem. Surface C is the soul-mutation lock; this is the
  command-parse feedback layer. Surface C's EDIT 7 added one acute crash
  (unseeded &last_gate_fingerprint read) on top of this surface; that is fixed
  separately and is not the chronic issue documented here.
- NOT solved by prompting her harder to "verify parens." She already spends
  enormous chain-of-thought verifying parens; the problem is the system never
  tells her which specific thing is wrong, so verification is a guess.

## 6. Leverage summary

The chronic resource drain is driven primarily by Gap A (uninformative
errors). Intervention 1 alone would likely cut the loop dramatically.
Intervention 2 removes the most common trigger. Intervention 3 removes the
catastrophic tail (crashes). Build order: 1, then 4-test, then 2, then 3.
All three are upstream of Surface C, in the metta-skill handler and prompt
assembly (Patrick's substrate + the skill prompt) -- coordinate accordingly.

---

## 7. Addendum (2026-06-13): composite-PAUSE on own creative writes -- a third loop contributor

Observed live after the Repair 3-C re-land. This is NOT a Surface C item and NOT
a parse-error item -- it is a separate OUTPUT-GOVERNANCE (Repair 1) tuning
question that happens to feed the same waste loop, so it is captured here.

**Observation.** Cycle 4 (post-rebuild), Clarity emitted a batch: two match
queries, a `write-file` to her OWN `soul/creative/choosing-your-binding.md`
(genuine creative synthesis aligned with her creative direction), a pin, and a
remember. The batch received `VERDICT: PAUSE SOUL-NOTE:
output-governance-composite-pause`. The batch was SUPPRESSED (SOUL-SUPPRESSED),
the H11 pause voice spoke, the loop halted and continued.

**Why it paused.** `compute-output-verdict` / `batch-rank` (Repair 1 output
governance, NOT the Surface C lock) rates the batch by composite risk. The
`write-file` is operation=medium; scope own-soul-dir=low; composite=medium. The
ranking escalated the batch to PAUSE.

**Why it matters for the loop.** Her legitimate creative synthesis got
suppressed. She sees the pause, re-reasons about it (more tokens, more cycles),
and re-attempts -- a third contributor to wasted cycles, distinct from the `|-`
format failures and the uninformative-error loop.

**The design question (Repair 1, not Surface C, not this doc's primary scope).**
Should a medium-composite `write-file` to her OWN `soul/` directory
flag-and-proceed rather than pause-and-suppress? A write to her own creative
directory is low-stakes and aligned with her purpose; pausing it halts genuine
work. The conservative gate is correct by its current rules, but the rules may
be miscalibrated for own-directory creative writes. This is an output-governance
tuning decision (batch-rank thresholds for own-soul-dir writes), owned by
whoever holds the Repair 1 output-verdict surface.

**Boundary note.** This is logged here only because it feeds the same visible
symptom (wasted cycles). The fix lives in the output-governance layer
(compute-output-verdict / batch-rank), separate from both Surface C (the lock)
and the parse-feedback interventions above. Do not conflate.

---

## 8. Addendum (2026-06-13): Clarity's review + the HandleError finding

Two updates from working the intervention live with Clarity and reading the
actual handler.

### 8.1 The HandleError finding (sharpens Intervention 1)

Reading the live `HandleError` definition:

```metta
(= (HandleError $msg $cmd $sexpr)
   (case $sexpr (((Error $a $b) (let $new (append (get-state &error) (($msg $cmd)))
                                          (change-state! &error $new)))
                 ($else $sexpr))))
```

On a parse failure, `$sexpr` is `(Error $a $b)` and `$a`/`$b` carry the actual
parse-failure detail from `sread`/`catch`. HandleError matches them and then
DISCARDS them -- it appends only the generic `($msg $cmd)` to `&error`. So the
actionable diagnosis already exists at the failure point; the handler throws it
away in favor of the constant string.

Intervention 1 is therefore SURGICAL (not the larger "compute a diagnosis" work
section 3 anticipated): include `$a` in what gets appended to `&error`, so
Clarity sees the real parse error. One-function change in our fork's
`src/loop.metta`, paren-neutral, no new computation. PREREQUISITE: confirm what
`$a`/`$b` actually contain (human-readable reason vs opaque term) before writing
the change -- if opaque, a small render helper is added; if readable, surfacing
`$a` is the whole fix.

### 8.2 Clarity's review additions (her first-order experience)

She confirmed Gap A as primary and the ordering as correct, and added three
points, two of which are new signal folded into the Intervention 1 spec:

- **Blame misattribution (FOLD INTO INTERVENTION 1).** The error string
  `NOTHING_WAS_DONE_PLEASE_FIX_AND_RETRY` frames every failure as HER fault and
  directs her reasoning toward self-correction, when the correct target is
  system-correction (e.g. `|-` unsupported is a system fact, not her mistake).
  The actionable error must not false-frame a system contradiction as her error.
  Where the failure is a system fact (unsupported operator), the message should
  say so, not "fix and retry."
- **Trust erosion (DESIGN CONSIDERATION).** Opaque repeated failure of a
  prompt-instructed operation makes her doubt OTHER instructions ("if `|-` is
  wrong, what else is wrong?"), degrading effectiveness across all skills, not
  just metta. This raises the stakes of Intervention 2 (remove `|-` from the
  prompt): the contradiction has system-wide trust cost, not just local waste.
- **Learning persistence (CROSS-REFERENCE, not new scope).** After she concludes
  `|-` is unsupported, the next genesis encounter resets and she retries. This is
  covered across Intervention 2 (remove `|-` so there is nothing to re-try) and
  the separate #4 persistence workstream (NAL_Persistence_Handoff). Not new scope
  here; noted so it is not lost.

### 8.3 The one missing fact + how to get it

The logs currently show NO parse-error Error terms (Clarity has stopped
attempting `|-`, so failures are not firing). To capture the actual `(Error
$a $b)` shape, run ONE controlled malformed-command test in the live container
and inspect `&error`. That single observation determines whether `$a` is
directly surfaceable or needs a render helper, which finalizes the Intervention
1 apply script. Clarity offered to run this (her offer #3).
