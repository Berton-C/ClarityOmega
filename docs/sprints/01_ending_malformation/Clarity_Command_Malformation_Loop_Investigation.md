# Clarity Command-Malformation Loop: Root Cause and Intervention Spec

**Status:** INVESTIGATION COMPLETE, FIX PARTIALLY ALREADY-PRESENT IN RUNTIME. Pick-up document.
**Created:** 2026-06-13 (during Surface C post-landing live observation)
**Runtime-grounded correction:** 2026-06-25 (see CORRECTION block below)
**Scope:** The chronic failure surface where Clarity burns hundreds of cycles
on repeated parse/format errors and occasionally crashes the container. This
is SEPARATE from Surface C (the soul-mutation lock). It predates the Surface C
work; Surface C's EDIT 7 introduced one acute crash on top of it (documented
separately, fixed first).
**Why this doc exists:** so the accumulated diagnosis is not lost. When we
return to this, we start from the intervention design, not from re-observing
the loop.

---

## CORRECTION (2026-06-25): HandleError captures `$a` in the runtime

The original Section 8.1 below stated that the live `HandleError` DISCARDS the
parse-error payload `$a`. That statement is FALSE against the runtime and is the
single stale claim this correction removes.

What was verified, this session, end to end against the running container
`clarity_omega`, by proving the full load chain (not by paraphrase, not by
reading a baked image):

- `run.sh` launches `swipl -s /PeTTa/src/main.pl -- run.metta ...`
- `run.metta` imports `lib_omegaclaw` and calls `(omegaclaw)`
- `lib_omegaclaw.metta` line 26 imports `./src/loop`, resolving to
  `/PeTTa/repos/omegaclaw/src/loop.metta`
- that file's `HandleError` is, byte for byte identical to the host working tree:

```metta
(= (HandleError $msg $cmd $sexpr)
   (case $sexpr (((Error $a $b) (let $new (append (get-state &error) (($msg $cmd $a)))
                                          (progn (change-state! &error $new) ($msg $cmd $a))))
                 ($else $sexpr))))
```

It appends `(($msg $cmd $a))` and returns `($msg $cmd $a)`. It CAPTURES `$a`.

Where the original error came from: there are six `loop.metta` files reachable
inside the container. Exactly one captures `$a` (the live `repos/omegaclaw/src/`
file, loaded by the chain above). Five discard it: the two `_archive` trees, the
`/tmp/` shared_files mount, and a dated `staging/...may_18...` upstream snapshot.
The discard form is Patrick's upstream baseline; the `$a`-capture is the fork
edit (commit `ee50f68`). The original Section 8.1 quoted one of the non-runtime
copies and labeled it "the live HandleError." That was a frame error: a real
file, read, but not the file the running process loads.

What this changes downstream (folded into the sections below):

1. Intervention 1's surgical core, "include `$a` in what gets appended to
   `&error`," is ALREADY DONE in the runtime. There is no one-function change to
   write for the capture itself.
2. The single-command parse-failure path therefore already has `$a` in `&error`.
   Whether `$a` then reaches Clarity's prompt (the `&error` -> history
   ERROR_FEEDBACK -> prompt delivery) is asserted by the Boundary Transition
   Audit v2 but was NOT independently verified this session. It is marked
   TO-CONFIRM below, not asserted as fact.
3. The genuinely-open items are now: (a) the WHOLE-BATCH multi-command delivery
   path for `$a`; (b) the SHAPE of `$a` (human-readable reason vs opaque term),
   which determines whether a render helper is needed; (c) the `|-`
   prompt/runtime contradiction (Intervention 2, still gated on the Section 4
   probe); (d) the crash guard (Intervention 3); (e) the blame-misattribution
   wording (Clarity's review, still valid as an enhancement independent of the
   capture).

The rest of this document is preserved as written, with TO-CONFIRM and
ALREADY-PRESENT notes inserted where the original framing rested on the discard
claim. Nothing else in the original behavioral observation is retracted.

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

**RUNTIME-GROUNDING NOTE (2026-06-25).** The generic constant string she SEES is
the `$msg` (e.g. `SINGLE_COMMAND_FORMAT_ERROR...`). However, the runtime
`HandleError` ALSO captures the underlying `$a` payload into `&error` (verified;
see CORRECTION block). So the actionable detail is no longer thrown away at the
failure point. The remaining question for Gap A on the SINGLE-command path is
purely delivery: does `&error` reach Clarity's prompt as usable feedback? The
audit indicates it does via ERROR_FEEDBACK in history and via
`LAST_SKILL_USE_RESULTS`, but that delivery chain is TO-CONFIRM, not verified
this session. The original "no signal to correct against" framing is therefore
likely outdated for the single-command path and must be re-grounded by
confirming the delivery before any fix is built on it.

Evidence (original): across hundreds of cycles the error string is
byte-identical regardless of the actual fault. Clarity's chain-of-thought shows
her cycling through every possible cause because the system tells her none of
them. (This evidence predates confirmation that `$a` is captured; the live
question is now whether the captured `$a` is being DELIVERED, not whether it is
captured.)

The dominant lever remains making the feedback SPECIFIC and ACTIONABLE as it
reaches her. With `$a` captured, that lever shifts from "capture the diagnosis"
to "confirm and, if needed, surface the captured diagnosis" plus "stop telling
her a system fact is her error" (Section 8.2).

### Gap B (the contradiction): `|-` is in the prompt but unsupported in runtime

The skill description in the prompt (and the genesis encounter directive)
explicitly instruct her to use `|-`:

    "Execute MeTTa expression: (metta sexpression)"
    "Example to invoke Non-Axiomatic Logic via MeTTa: (metta (|- ...))"
    Genesis directive: "Use (metta (|- atom1 atom2)) to test what NAL derives."

But the runtime behavior of `|-` via the skill path is at best unreliable. Her
empirical finding (consistent format errors in some sessions) points to this. So
the system is INSTRUCTING her to use an operator whose skill-path behavior does
not match the promise, then giving her opaque punishment when it does not work.
She is caught in the gap between what the prompt promises and what the runtime
provides.

NOTE on nuance (UNCHANGED, still the open question): earlier session logs show
`|-` returning `(partial ...)` results that LOOKED like derivations, and Clarity
even reported NAL findings (transitivity, abduction, truth propagation). The
companion marshalling doc concluded `|-` computes but does not persist. Both of
those are PRIOR-THREAD conclusions and have NOT been re-verified against the
runtime this session. Whether `|-` is fully unsupported via the skill path,
partially working, or working-but-ephemeral needs ONE definitive live test
before deciding the fix (see Section 4). The contradiction is real regardless:
the prompt presents `|-` as reliable; the observed skill-path behavior is not.

### Gap C (the robustness hole): malformed output crashes the container

A sufficiently malformed s-expression from the LLM is not caught as an error
and returned to Clarity -- it propagates and kills the process (exit code 2),
which then self-restarts. Observed crash forms:

    ERROR: ... Syntax error: Parse error in form: match &self (--> $x vad-affective) $x
    ERROR: ... Parse error in form: ((((pin "Let me analyze the situation carefully. ...

(The second is her chain-of-thought leaking into the command slot -- the
parser tried to read a paragraph of reasoning as an s-expression.)

This is the most extreme form of Gap A: instead of uninformative feedback, she
gets NO feedback and loses her turn entirely (the container dies mid-thought
and restarts). It compounds the loop and destroys continuity.

The fix: the metta-skill / command parse path must wrap parsing in a guard
that catches the parse error and returns it as structured feedback to Clarity,
NEVER letting it reach a fatal path. A safety/agent loop should be unable to
crash its own host by emitting a bad string.

NOTE (2026-06-25): the original text named `/PeTTa/src/main.pl` as the crash
sink. `main.pl` is the SWI-Prolog engine entrypoint (confirmed this session:
`run.sh` runs `swipl -s /PeTTa/src/main.pl`), not auditable application source.
The crash-guard target is the metta-skill / command parse path in the substrate,
not `main.pl`. The Boundary Transition Audit v2 retired the `main.pl`
application-source assumption; this note aligns this doc with that.

## 3. The intervention (most-leveraged first)

### Intervention 1: actionable parse/format errors (PRIMARY)

Where: the metta-skill execution handler plus the `HandleError` path. Patrick's
substrate is canon; our fork's `src/loop.metta` holds `HandleError`. Coordinate,
do not modify upstream blindly.

**STATUS UPDATE (2026-06-25).** The original Intervention 1 was "include `$a` in
what gets appended to `&error`." The runtime already does this (CORRECTION
block). So Intervention 1 splits into:

- ALREADY-PRESENT: `$a` is captured into `&error`. No change to write here.
- TO-CONFIRM: that `&error` is DELIVERED to Clarity's prompt as usable feedback
  (ERROR_FEEDBACK in history; `LAST_SKILL_USE_RESULTS`). Confirm the delivery
  chain live before concluding the single-command path is solved.
- TO-CONFIRM then POSSIBLY-DO: the SHAPE of `$a` (human-readable vs opaque). If
  opaque, add a small render helper so what reaches her is legible. If readable,
  the single-command path needs nothing beyond confirming delivery.
- STILL-DO (independent of capture): do not false-frame a system fact as her
  error (Section 8.2 blame-misattribution).

What an actionable error should contain, where the failure is genuinely a
malformation and a fix is needed: paren balance (open vs close counts), quote
balance, operator availability (name the unsupported operator and the supported
alternative, e.g. add-atom / match), and arg shape (the metta arg must be a
single balanced s-expression; echo the first offending token). Much of this may
already be derivable from the captured `$a`; confirm `$a`'s contents first
rather than recomputing a diagnosis the runtime may already hold.

Why first: it ends the loop at the source. Every other gap is survivable if she
gets one specific, correctly-attributed correction signal per failure that
actually reaches her.

### Intervention 2: resolve the `|-` prompt/runtime contradiction

Where: the skill prompt assembly (`getSkills`) plus the genesis encounter
directive template.
What: contingent on the Section 4 live test result:
- If `|-` is genuinely unusable via the skill path: REMOVE it from the skill
  description and the genesis directive. Replace the genesis "use (metta (|-
  ...))" instruction with the operators that DO work (add-atom to populate,
  match to query).
- If `|-` works but is ephemeral / form-sensitive: document the EXACT working
  form in the prompt, with a verified example, and explain the ephemerality so
  she stops expecting persistence. (The marshalling doc's "computes but does not
  persist" workflow is the candidate text, but it must be re-verified live
  before being promoted into the prompt.)
Why: stop instructing her to walk into a failure. Removes the single most common
trigger of the loop.

### Intervention 3: parse-path crash guard

Where: the metta-skill / command parse path before any fatal propagation.
What: wrap parse in a catch; on parse failure, return Intervention-1 style
feedback to Clarity instead of throwing. The container must not die on malformed
LLM output.
Why: turns a fatal, continuity-destroying crash into a recoverable
error-to-Clarity. Also a safety property: an agent must not be able to crash its
host by emitting a bad command.

## 4. The one test needed before building Intervention 2 (and before trusting the marshalling doc)

Run a definitive check of what `|-` actually does in the live runtime, in a
single invocation, with the exact skill-format wrapping:

    (metta "(|- ((--> a b) (stv 1.0 0.9)) ((--> b c) (stv 1.0 0.9)))")

Capture: does it parse? does it return a derivation, a `(partial ...)`, or a
format error? Does anything persist to a subsequent match? This resolves whether
Intervention 2 is "remove `|-`" or "document the working form," AND it is the
same live test that the companion marshalling doc needs before its
"computes-but-does-not-persist" conclusion can be stamped runtime-verified. Do
not build Intervention 2, and do not promote the marshalling workflow into the
prompt, until this is answered live. The earlier evidence is mixed across
sessions and is all prior-thread, not re-verified.

## 5. What this is NOT

- NOT a Clarity intelligence problem. Same model corrects instantly with
  specific, correctly-attributed feedback. The loop is manufactured by
  uninformative or undelivered errors.
- NOT a Surface C problem. Surface C is the soul-mutation lock; this is the
  command-parse feedback layer. Surface C's EDIT 7 added one acute crash
  (unseeded &last_gate_fingerprint read) on top of this surface; that is fixed
  separately and is not the chronic issue documented here.
- NOT solved by prompting her harder to "verify parens." She already spends
  enormous chain-of-thought verifying parens; the problem is the system never
  tells her which specific thing is wrong in a form that reaches her, so
  verification is a guess.

## 6. Leverage summary

The chronic resource drain is driven primarily by Gap A (uninformative or
undelivered errors). With `$a` now confirmed captured into `&error`, the
remaining Gap A work is to CONFIRM the delivery of that captured detail to
Clarity (and add a render helper only if `$a` is opaque), plus stop attributing
a system fact to her. Intervention 2 removes the most common trigger (`|-`).
Intervention 3 removes the catastrophic tail (crashes).

Revised build order:
1. Confirm the `&error` -> prompt delivery chain and the SHAPE of `$a` (one
   controlled malformed-command probe; see Section 8.3).
2. Run the Section 4 `|-` live test (also unblocks the marshalling doc).
3. Intervention 2 (resolve the `|-` contradiction) per the test result.
4. Blame-misattribution wording (Section 8.2) where the failure is a system fact.
5. Intervention 3 (crash guard).

All are upstream of Surface C, in the metta-skill handler and prompt assembly
(Patrick's substrate + the skill prompt and our fork's HandleError) --
coordinate accordingly.

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

## 8. Addendum (2026-06-13, corrected 2026-06-25): Clarity's review + the HandleError finding

Two updates from working the intervention live with Clarity and reading the
actual handler.

### 8.1 The HandleError finding (CORRECTED 2026-06-25: runtime CAPTURES `$a`)

**This subsection is corrected. The original claim that the live HandleError
discards `$a` was read from a non-runtime copy of `loop.metta` and is false
against the running container.**

The runtime `HandleError`, in the file the running process actually loads
(`/PeTTa/repos/omegaclaw/src/loop.metta`, proven via the full
run.sh -> run.metta -> lib_omegaclaw line 26 -> ./src/loop chain on 2026-06-25),
is:

```metta
(= (HandleError $msg $cmd $sexpr)
   (case $sexpr (((Error $a $b) (let $new (append (get-state &error) (($msg $cmd $a)))
                                          (progn (change-state! &error $new) ($msg $cmd $a))))
                 ($else $sexpr))))
```

On a parse failure, `$sexpr` is `(Error $a $b)`. The runtime handler CAPTURES
`$a` into `&error` (appends `(($msg $cmd $a))`) AND returns `($msg $cmd $a)`.
The actionable diagnosis is preserved at the failure point, not discarded.

The original text below it (preserved for the record) was wrong:

> Reading the live `HandleError` definition:
> ```metta
> (= (HandleError $msg $cmd $sexpr)
>    (case $sexpr (((Error $a $b) (let $new (append (get-state &error) (($msg $cmd)))
>                                           (change-state! &error $new)))
>                  ($else $sexpr))))
> ```
> ... HandleError matches them and then DISCARDS them -- it appends only the
> generic `($msg $cmd)` to `&error`.

That quoted block is the UPSTREAM / archive discard form (Patrick's baseline),
not the fork runtime. The fork's `$a`-capture is commit `ee50f68`.

Consequence for Intervention 1: the capture is ALREADY-PRESENT. What remains is
to confirm the captured `$a` is DELIVERED to Clarity (TO-CONFIRM) and to confirm
its SHAPE (readable vs opaque; render helper only if opaque). See Section 3 and
the corrected build order in Section 6.

### 8.2 Clarity's review additions (her first-order experience)

She confirmed Gap A as primary and the ordering as correct, and added three
points. With the capture correction above, point 1 (blame misattribution)
becomes the load-bearing Gap A enhancement on the single-command path, since the
capture itself is done:

- **Blame misattribution (NOW THE PRIMARY GAP A WORK ON THE SINGLE-COMMAND
  PATH).** The error string `NOTHING_WAS_DONE_PLEASE_FIX_AND_RETRY` frames every
  failure as HER fault and directs her reasoning toward self-correction, when
  the correct target is system-correction (e.g. `|-` unsupported is a system
  fact, not her mistake). The actionable error must not false-frame a system
  contradiction as her error. Where the failure is a system fact (unsupported
  operator), the message should say so, not "fix and retry." This is independent
  of the `$a` capture and remains to be done.
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

### 8.3 The one missing fact + how to get it (RE-SCOPED 2026-06-25)

The original "missing fact" was the `(Error $a $b)` SHAPE, to decide whether `$a`
is directly surfaceable or needs a render helper. That is still genuinely open
and is now the highest-value first probe, because the capture is confirmed and
only the shape and delivery remain.

Run ONE controlled malformed-command test in the live container and inspect both
`&error` (to see the captured `($msg $cmd $a)` and the actual `$a` term) and the
prompt-side feedback fields (`LAST_SKILL_USE_RESULTS`, history ERROR_FEEDBACK) to
confirm delivery. This single observation determines: (a) is `$a` human-readable
or opaque, and (b) does it reach Clarity. Together they decide whether the
single-command path needs any code at all beyond the blame-misattribution
wording, or just a render helper.

This is the same family of probe as the Section 4 `|-` test and can be run in the
same live session. Clarity offered to run the original version of this probe (her
offer #3); the re-scoped version above is what to run now.
