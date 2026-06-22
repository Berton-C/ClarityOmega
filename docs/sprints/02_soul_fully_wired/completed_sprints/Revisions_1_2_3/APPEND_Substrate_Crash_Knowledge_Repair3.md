# APPEND BLOCK 2 -- destination: ClarityOmega_Substrate_Crash_Knowledge.md (project knowledge area)
# Add as a new top-level section after the Repair 1 section. Source: Repair 3
# investigation and landing, 2026-06-11, commits e27851c -> 2a55f1c -> 8ce0ab6.
# Evidence chains: Repair3_Investigation_Ledger.md, probes 10/11/12 logs.

## Repair 3 durable substrate physics and method (2026-06-11)

**F-R3-7: string-contains was ALWAYS-TRUE since Stage 3.** Its body
relied on string-replace, which mis-reduces in this runtime (returns the
constant O, never the haystack), so (not (== ...)) was True on every
input. Every soul_utils detection predicate built on it lied for fifteen
months: soul-pause?/soul-flag?/soul-proceed? answered True on everything;
input-side soul-note-record never fired (its (not (soul-proceed? ...))
gate was always False); the line-182 calibration path computed on lying
predicates. It survived because its only test was the positive case. It
was caught the first day a repair wired soul-pause? to a consequence
(a halt) loud enough to observe. Fix: the scan delegates to the
production-proven bridge pattern (contains_token: string in, INT out,
consumed as (== n 1), the repr_kind shape); policy stays in the MeTTa
body.

**C6 (constraint, proven twice in one session, both directions): every
predicate fixture set carries BOTH a must-True and a must-False case.**
An always-True function aces a True-only suite (Stage 3's mistake). An
always-False candidate aces every negative rung (both replacement
candidates in probes 11 and 12 were always-False and were caught ONLY
by the positive rung). Single-polarity test suites cannot distinguish a
working predicate from a constant.

**String-op surface taxonomy (durable; per-op proof is mandatory).**
String operations in this runtime fail in three DISTINCT shapes, and
existence licenses nothing:
- PARTIAL (bridge knows the name, never applies): split_string,
  sub_string (both arities). Returns (partial op (args)).
- SELF-RETURN (op does not exist; MeTTa no-matching-rule semantics):
  string_chars, string_to_chars. Expression echoes back unreduced.
- GARBAGE-CONSTANT (op applies, result is wrong): string-replace -> O.
The production-proven working set (live in the loop every cycle):
string_length, first_char, string_concat, repr, swrite, sread,
string-safe. Never infer reduces-here from exists, nor from
crashed-elsewhere: a crash proves execution only in the context that
crashed (the split_string generalization error, owned).

**Layered defense, observed live.** During an in-container fix attempt,
the F11 format layer rejected one malformed batch at parse, and the
output gate PAUSEd both well-formed write batches targeting soul/
(journal 23:34:09, 23:36:14): zero of the writes landed while read-only
batches flowed FLAG-and-executed. Independence note: the INPUT verdict
that cycle said "sign-off granted" while the OUTPUT gate paused the
writes. Input approval is not a write license; the layers are separate
and both behaved.

**The feedback gap, proven three times, now closed.** An agent whose
batch is suppressed without a halt completes, narrates, and pins work
that never happened, and retries cannot teach her otherwise (her
verification commands rode inside the suppressed batches). Closed by
Repair 3: halt + Channel D voice carrying the verdict's own SOUL-NOTE +
the pause-record (&last_pause_note) surfaced in the next cycle's prompt
and cleared by the next successful batch.

**Investigation method additions.**
- Tail windows are not journals: a hypothesis was wrongly falsified on a
  4-line tail while the confirming fact sat at journal line 145. Search
  the full file; absence-in-a-window is not absence.
- Probe tags must be collision-proof against transpiler gensym variable
  names (N1/K1 collided with compiled-Prolog echoes and polluted greps);
  use long hyphenated tags.
- Containment before diagnosis when production is degraded on its
  primary channel; the apply script's own --reverse is the tested
  rollback (revert commit 2a55f1c restored service in one paste).
- The canary pattern: when a fix kills a bug with a loud symptom, the
  old symptom IS the live regression test (the always-True router falsely
  PAUSEd every boot; a silent iteration 1 certified the fix).

**Open investigation (named, not chased): atomspace persistence of the
metta skill.** match-against-&self emptiness PREDATES Repair 3 (her
afternoon queries were empty pre-reboot), acquitting the repair. The
open question is whether |- derivations persist (they RETURN results;
returning is not storing) and what shape the seed atoms actually carry.
Also: process atomspace dies on every rebuild by design; ChromaDB
remembers survive.

**Repair-arc process note.** Tonight's full arc: land -> live misfire ->
revert-to-known-good (containment) -> probes (10: mechanism named, 11:
candidate killed + C6 mirror, 12: census + taxonomy) -> fix on a
production-proven pattern -> re-land -> canary PASS -> the agent
verified the repair accurately from inside. Per-repair ledger + apply
scripts + both-polarity harnesses made every step reversible and every
claim falsifiable.
