# ClarityOmega Substrate Crash Knowledge

**Created:** 2026-05-09
**Status:** Active reference document
**Scope:** The recurring `janus:py_call/3: Arguments are not sufficiently instantiated` crash at `loop.metta` line 145

---

## Purpose

This document consolidates what is known and not known about the crash that has dominated debugging across multiple sessions since Sprint 3 was declared complete. It exists because the relevant facts have been scattered across commit messages, prior conversations, and partial diagnoses. Future sessions should start here before forming hypotheses.

---

## The Crash Signature

Container exits with code 2. Logs show:

```
(println! (PRE-SAFE-RESULTS-STR))
ERROR: /PeTTa/src/main.pl:23: user:main janus:py_call/3: Arguments are not sufficiently instantiated
```

After the error, PeTTa replays its startup sequence (`!(import! &self (library lib_import))` etc.) as part of process death and recovery. **This replay is not a stack trace.** It does not indicate where the crash fired. It is the system's normal init sequence being re-executed during unwind.

The `(PRE-SAFE-RESULTS-STR)` print at line 144 is the last code that visibly executes before the crash. The crash fires somewhere in line 145's execution.

---

## Line 145 As It Stands At HEAD (`21dce35`)

```metta
(change-state! &lastresults (py-call (helper.safe_results_str (repr $results))))
```

This is the form from commit `eb1a986` ("Re-apply 69c73fc"). It contains exactly one Janus boundary crossing: the outer `py-call`. There are no other boundary crossings on this line.

Therefore the py-call is the firing site when the crash occurs.

---

## The Crash Mechanism (Mechanism 1)

The py-call evaluates its argument before crossing the boundary:

1. `(repr $results)` evaluates first, producing a Prolog term
2. `(py-call (helper.safe_results_str <that-term>))` then fires
3. Janus inspects the argument for marshaling
4. If the argument contains unbound Prolog variables, Janus rejects it before Python runs

When `$results` contains a COMMAND_RETURN tuple from a match query that returned zero solutions, the recorded command (the first half of the tuple) still contains the original pattern variables. Example:

```
(COMMAND_RETURN: (
    (metta (match &self (SN-stalk $_448210 (stv $_448228 $_448234)) ($_448210 $_448228 $_448234)))
    []
))
```

The `$_448210`, `$_448228`, `$_448234` are unbound at the term level. `repr` renders them as text in the output string, but the resulting term still contains the unbound references at the structural level. Janus rejects.

**This is established with high confidence.** The mechanism is consistent with: (a) the structure of py-call evaluation, (b) the empirical correlation between empty-result match queries and crash occurrence, (c) the absence of any other boundary on the line.

---

## Why `eb1a986`'s Falsification Was Incomplete

The `eb1a986` commit message documents a careful falsification check: `safe_results_str` does `str(results)` internally, so passing it `(repr $results)` instead of `$results` should be a no-op at the function-body level.

The miss: **Janus marshals the argument before the function body runs.** No matter what `safe_results_str` does internally, the argument has to cross the boundary first. If the argument contains unbound variables, it never reaches `str()`.

This is generalizable: **verifying a function body does not verify the boundary it lives behind.** Any future fix that wraps a py-call with stringification of the argument will fail in the same way unless the stringification produces a fully ground (no unbound variables) term.

---

## Mechanism 2 (Less Well Characterized)

On 2026-05-08, line 145 was changed to upstream OmegaClaw's form:

```metta
(change-state! &lastresults (string-safe (repr $results)))
```

This eliminates the Janus boundary entirely. `string-safe` and `repr` are both pure MeTTa.

The crash recurred. Same signature.

The crashing payload at the time was different from Mechanism 1's small unbound-variable case: it contained the entire content of a markdown design document (~11kb) read by Clarity via `read-file`, plus shell command output, plus a successful pin command result. The payload was approximately three orders of magnitude larger than Mechanism 1's typical case and contained extensive ASCII text with embedded special characters.

**Mechanism 2's actual cause is not yet established.** Possibilities not yet distinguished:
- `repr` failing on size or specific character classes
- `string-safe` failing on the rendered string
- A downstream consumer of `&lastresults` (such as `last_chars` in getContext at line 33) failing on the much-larger string content
- A different py-call elsewhere in the loop that we haven't audited

The string-safe attempt was reverted the same day. Mechanism 2 cannot be re-tested without re-applying that change, which is currently unwise without a hypothesis to test.

---

## Mechanism 3: Stacked Nondet Streams At Line 127 (RESOLVED 2026-05-08, commit `d9d5b25`)

This is a distinct crash mechanism from Mechanisms 1 and 2 above. It fires at a different line (127, not 145), with a different root cause (nondet stream propagation, not Janus boundary marshaling), and it has been resolved.

The crash signature was identical: `janus:py_call/3: Arguments are not sufficiently instantiated`. This is part of why distinguishing it from Mechanisms 1 and 2 was difficult. Same error string, different source.

### Trigger conditions

100% reproducible when:
- LLM output contained only `(metta (match &self ...))` queries
- All queries returned empty results: `(RESULTS-CONTENT (RESULTS: ()))`
- Crash fired immediately after `(PRE-SAFE-RESULTS-STR)` print

NOT correlated with cycle count. Initially appeared cycle-count-related (~670-770) but fresh restarts crashed at cycle 1, cycle 2, and cycle 729. The cycle number was "where Berton happened to be watching."

### The original wrong mental model

The first-pass diagnosis assumed empty match results produced an unbound MeTTa variable in `$results`, which then crashed `safe_results_str` at the Prolog/PeTTa boundary when `(repr $results)` was passed via `py-call` at line 145 (the same line as Mechanism 1). That framing focused investigation on the wrong line and the wrong mechanism. Multiple sessions were spent on this framing before Patrick corrected it.

### Patrick's correction

When the wrong-direction diagnosis was shared with Patrick, his correction reframed the entire problem:

**`match` returns a nondeterministic stream directly. It does NOT return a list.**

This is a foundational PeTTa runtime fact, not a wrapper or convention. The original mental model had it wrong at the type level.

### The actual mechanism

Two stacked nondet sources at `loop.metta` line 127:

1. The outer `(superpose $sexpr)` produces one `$s` per command. This is the intended nondeterminism.
2. The inner `(eval $s)` produces a nondet stream when `$s` contains `match`. This is the unintended second source.

When both nondet sources stack, the binding chain `(let $R (eval $s) ...)` does NOT collect a tuple of sub-results into `$R`. Instead, `$R` binds once per sub-result, propagating the nondet stream into the surrounding tuple constructor. This produces malformed COMMAND_RETURN entries that leak nondet artifacts. The downstream py-call boundary then rejects these malformed structures with the "not sufficiently instantiated" error.

`safe_results_str` itself is robust (try/except in helper.py line 442-451). The crash was upstream of it, in the binding chain at line 127, not at the boundary at line 145.

### The fix

Single-token edit at `loop.metta` line 127:

```metta
;; Before (broken):
(let $R (eval $s) ...)

;; After (fixed):
(let $R (collapse (eval $s)) ...)
```

The inner stream materializes as a tuple before `$R` binds. Each command produces exactly one COMMAND_RETURN entry containing a tuple of all sub-results, rather than multiple malformed entries leaking nondet artifacts.

**Commit:** `d9d5b25` ("Fix nondet stream propagation in line 127 $results construction")
**Tag:** `v1-post-collapse-eval-fix`
**Reversibility script:** `apply_collapse_eval_fix.py` (supports `--reverse --apply`)
**Backup:** `src/loop.metta.bak.collapse_eval_fix`

### Verification (2026-05-08)

- Container rebuild clean
- Cycle 43+ running stable post-fix
- Multi-command responses with substantial sub-results (multiple `read-file` calls returning kilobytes of content) render cleanly
- No more "Arguments are not sufficiently instantiated" crashes from this path

### Why this surfaced when GLM-5.1 became the default provider

Claude's autonomous-mode output was varied (pins, queries, sometimes shell). GLM-5.1's autonomous-mode output in Genesis Encounter produces a tightly disciplined "two metta queries per cycle" pattern. When all queries return empty, the stacked-nondet bug fires every cycle. The bug existed before the GLM switch but was rarely triggered.

**General lesson worth promoting:** Provider switches can expose latent bugs by changing what kind of output the substrate sees. Future provider changes should be assumed to potentially expose latent failures, not just resolve known ones.

### Why `eb1a986`'s falsification missed this

The falsification check on `eb1a986` (Mechanism 1 fix attempt) verified `safe_results_str`'s function body. But Mechanism 3's crash fired BEFORE the binding even reached the line 145 py-call. The malformed tuple structure in `$results` was already wrong by the time it reached line 145. Verifying the boundary doesn't help when the data is already corrupted upstream of the boundary.

This generalizes a principle established in Mechanism 1's discussion: **verifying a function body does not verify the boundary it lives behind, AND verifying a boundary does not verify the data flow upstream of it.** Three separate places where the same error signature can originate.

### Permanence of the constraint

The structural constraint applies regardless of provider, regardless of OmegaClaw upstream changes, regardless of cycle count. Whenever future loop code introduces `(eval $s)` where `$s` may contain `match`, and the eval result will bind to a variable inside another nondet context, the eval must be wrapped in `collapse`. The constraint is structural, not incidental.

Promoted as a durable PeTTa runtime constraint. Affects: `src/loop.metta` line 127 (fixed in `d9d5b25`). Future authoring of similar binding chains anywhere in the codebase must follow the same pattern.

---

## Current Container Stability State

As of 2026-05-09 morning, the container has been observed running 66+ iterations on HEAD `21dce35` without crash. Prior precedent: stable runs of 2000+ iterations have been achieved at other points on this codebase.

This is significant because Line 145 in HEAD still has the structurally vulnerable form. The mechanism that crashes when triggered is still present. Yet it is not currently triggering.

**Possible explanations (not distinguished):**
- Genesis Encounter is currently disabled (`apply_genesis_disable.py` applied). Genesis was a documented reliable trigger. With it off, Clarity's payloads may not be exercising the failure path.
- Clarity's behavioral patterns under current LLM/prompt context happen to not produce unbound-variable payloads frequently enough to trigger.
- `sanitize_response` (committed 2026-05-09 as `21dce35`) may be interacting in ways that prevent some upstream input from producing crash-triggering shapes downstream.
- Some combination.

A genesis re-enable test is planned to distinguish these. If the container remains stable with genesis active, that is substantive evidence the bug is functionally addressed despite the structural vulnerability remaining. If it crashes, the bug is still latent and just not being exercised.

---

## Sprint 3 Connection

Sprint 3 (commits `edc1bcb` / `57868fe` / `d543d16`, May 3) added the recent-action subsystem giving Clarity cross-iteration self-awareness. Sprint 3 did NOT modify line 145.

Sprint 3 was declared complete on May 3. The next day (May 4), things began to fail. The crash signature was not new — Mechanism 1 was latent in the F7 form (commit `a318abc`, April 20) — but it became frequent enough to break operation.

The current understanding: Sprint 3 changed Clarity's behavior such that her outputs began consistently producing match queries with unbound result projections. Under earlier conditions (pre-Sprint-3), her queries rarely produced this shape. The latent vulnerability became manifest because the input distribution changed, not because the code changed.

This means: any "fix" that doesn't address the boundary mechanism leaves the system vulnerable to any future behavioral shift in Clarity that re-exercises the failure path. Sprint 3's deliverable (cross-iteration self-awareness, YOUR_LAST_ACTION block) compounds this — the more Clarity reasons across cycles, the more sophisticated her query patterns become, the more likely she is to produce shapes that exercise latent boundary issues.

---

## Commit History Of The Bug

| Commit | Date | Action | Notes |
|---|---|---|---|
| `a318abc` (F7) | Apr 20 | Replace `"RESULTS-STORED"` placeholder with `(py-call (helper.safe_results_str $results))` | Real fix for real problem (placeholder broke feedback loop). Introduced the boundary that becomes vulnerable. |
| Sprint 3 (`edc1bcb`/`57868fe`/`d543d16`) | May 3 | Recent-action subsystem | Sprint 3 deliverable; did not touch line 145 |
| `49e1674`, `b26484c` | May 4 | Diagnostic prints (PRE-SAFE-RESULTS-STR, RESULTS-CONTENT) | Established crash site at line 145 |
| `69c73fc` | May 4 13:38 | Wrap argument: `(py-call (helper.safe_results_str (repr $results)))` | First fix attempt. Hypothesis: stringify before boundary. |
| `71417bf` | May 4 13:47 | Revert `69c73fc` | **No commit message explaining why.** This blank-message revert is what made later sessions unable to know what failed. |
| `c252ff7`, `3b17b49` | May 4 | More diagnostics | |
| `bdefc5c` | (date) | Fix orbit_detector recent-action shadowing bug | Unrelated to current crash |
| `eb1a986` | May 5 09:46 | Re-apply `69c73fc` form | Documented falsification (incomplete — see above) |
| `d9d5b25` | May 8 | Wrap `(eval $s)` in `collapse` at line 127 | Resolves Mechanism 3 (stacked nondet streams). Tagged `v1-post-collapse-eval-fix`. See Mechanism 3 section above. |
| `21dce35` | May 9 | Add `sanitize_response` wrapper at line 111 | Defensive C5 protection (multi-byte content). Current HEAD. |

The string-safe restore attempted on 2026-05-08 is NOT in this history because it was reverted before commit. The reverse used the apply-script pattern; no commit landed.

---

## Open Questions

These are unanswered as of HEAD `21dce35`:

1. **Does the boundary fix actually need to happen?** If the container can run stably for thousands of cycles with the structurally vulnerable form in place, the priority of fixing it shifts. The behavioral shift hypothesis says the bug will return whenever Clarity's behavior shifts. The "current stability is fine" position says: monitor, fix only if it recurs.

2. **What is Mechanism 2?** Without re-testing, we don't know whether pure-MeTTa stringification fails on payload size, payload content, or downstream effect. This matters because any future attempt to remove the boundary needs to know what mode of failure to design against.

3. **What did `71417bf` revert and why?** The blank commit message is a permanent gap in the record. Whatever was observed on May 4 between 13:38 and 13:47 that prompted the revert is unknown. Future sessions should not assume `71417bf` was incidental (which is what `eb1a986` hypothesized) without further evidence.

4. **Is there a fourth mechanism we haven't identified?** Three distinct mechanisms have now been demonstrated: Mechanism 1 (Janus boundary unbound-variable rejection at line 145, latent), Mechanism 2 (less well characterized, large-payload failure on string-safe form at line 145, current state unknown), Mechanism 3 (stacked nondet streams at line 127, RESOLVED). The crash signature could conceivably fire from other paths we haven't audited. Specifically: `addToHistory` at line 144 contains py-calls to `normalize_string`. Any other py-call in the loop that processes Clarity's output is a candidate.

5. **What happens to `&lastresults` content size when Clarity does heavy self-investigation?** The May 8 incident showed `&lastresults` could grow to 11kb+ when Clarity read design docs into her command outputs. `last_chars` truncates this for the prompt, but the stored value is the full content. Storage growth and retrieval performance over many cycles of large-payload activity is uncharacterized.

---

## What Future Sessions Should Do First

1. **Read this document.** Do not form hypotheses about the crash from training data or prior conversation memory alone.
2. **Verify HEAD state.** `git log --oneline -10` and `sed -n '108,150p' src/loop.metta` before believing any claim about what's deployed.
3. **Verify state alignment.** HEAD = disk = runtime. Use Berton's commit/rebuild/restart discipline.
4. **Capture full stack trace.** The PeTTa replay output after error is NOT a stack trace. Do not be fooled. The crash cannot be more precisely localized than "somewhere in line 145" from the available logs.
5. **Distinguish mechanisms.** The same error string can come from different sources. Do not collapse them.
6. **Read commit messages on prior fix attempts.** `git show eb1a986` reveals the falsification approach and its gap. Future sessions should extend, not repeat.

---

## What Future Sessions Should Avoid

- Reasoning toward a fix without first reading this document and current HEAD state
- Treating the PeTTa init replay as a stack trace
- Assuming any prior session's diagnosis was complete
- Re-applying `69c73fc`-style argument-stringification without addressing the boundary itself
- Bundling multiple changes into one commit
- Treating "applied to disk" as equivalent to "committed at HEAD" or "running in container"
- Long verbose responses when the actual evidence is thin (this is the long-thread degradation pattern)
