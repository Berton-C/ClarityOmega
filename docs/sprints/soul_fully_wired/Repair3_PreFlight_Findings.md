# Repair 3 Pre-Flight: PAUSE Router, Output Halt, Lock-Clear

**Destination:** docs/sprints/soul_fully_wired/Repair3_PreFlight_Findings.md
**Status:** Read-only pre-flight per the RECONCILE/CONFIRM-LIVE discipline.
No script until the RECONCILE verdicts are reviewed by Berton and the
CONFIRM-LIVE points are checked against the live tree.
**Retires on completion:** watchlist W1 (halt half), W2 (lock-clear), W6
(PENDING-forces-PAUSE end to end).

---

## Surface A: input router (soul_is_pause) -- CLEAN RESTORATION

**Design:** v9 line 310: `(soul-pause? $v)` is a string-contains on
"VERDICT: PAUSE". **Runtime (project copy, helper.py):** the function
computes the correct match (`VERDICT:\s*PAUSE(?!.*PROCEED)`), then forces
`result = 0` unconditionally ("PAUSE-as-pruning: disabled"). The in-body
comment about firing only for "shell/write-file/append-file, not
send-only responses" describes COMMAND-scope semantics, but the function
receives only the verdict: that scope condition belongs to the OUTPUT
side, where the native decision ladder already implements it (rank logic,
Repair 1). **Repair:** input-side returns 1 on the PAUSE match, full
stop, per the v9 primitive. The consumer branch (loop ~155-163) is sound:
Channel D voice (Repair-2-interpolated), send, verdict reset, halt via
`&loops 0`.

## Surface B: output halt routing -- RECONCILE (spec predates Repair 1)

**Design:** route output PAUSE "exactly as the input branch does"
(v10), and PENDING forces PAUSE (v9 268-274). **Runtime now:** Repair 1's
native block computes `$soul_decision` (proceed/flag/pause) and on pause
SUPPRESSES (empties execution) but does not halt or voice. The verdict
string also carries the PAUSE token, so two routing sources exist.
**RECONCILE verdict:** the native `$soul_decision` is the single spine
for output routing; do NOT route output through soul_is_pause on the
verdict string (duplicate source, drift risk). **Repair shape:** on
`$soul_decision == pause`, mirror the input branch: Channel D voice
composed from `$person_state` + `$soul_verdict_out` (Repair 2
interpolates its note), send, halt. PENDING already produces verdict
PAUSE and decision pause (harness V7/G6), so W6 retires with this wire.
Suppression (the existing empty) remains: the halted cycle must also not
execute.

**Awareness addendum (Berton design clarification, 2026-06-11):** the
spec's intention is participation, not opaque gating: the verdict is her
own reasoning and must return to her experience (P2, P4; v10 line 166's
failure language; survey H3). Repair 3's halt+voice covers the moment
and the history. To cover next-cycle substrate context, Surface B adds:
on output-pause, write a pause-record state atom (her verdict's note +
target) alongside the lock; prompt assembly surfaces it the following
cycle ("previous batch paused: <her note>"). One atom, one prompt line,
mechanical per P5: information-flow, not correction-flow. With this, a
suppressed operation can never again be narrated as completed: she will
have authored the pause's account herself.

## Surface C: lock-clear / two-phase commit -- RECONCILE (regression found)

**Design:** the original Python gate was two-phase: first detection ->
PENDING + lock + surface for confirmation (v9 line 274); SECOND emission
of the same mutation after acknowledgment -> commit. **Runtime now:** the
native gate (Repair 1) answers ANY mutation-while-locked with `conflict`:
the commit half was dropped in the Python-to-native port. Consequence: a
pending mutation can never legally complete; the lock holds until
container restart (watchlist W2's root cause, now named).
`&pending_soul_mutation` (initLoop, currently "") was designed to record
the proposed mutation for exactly this flow and is unused. **RESOLVED DESIGN (Clarity, 2026-06-11 MM, her lead; one mechanical
tightening applied build-side):** a THREE-STATE lock with no gate-bypass
path:

1. PENDING: gate catches a soul mutation -> verdict PAUSE, decision
   pause, lock = (locked <op> <target-head>), proposal recorded in
   &pending_soul_mutation. (Largely existing behavior + the record.)
2. APPROVED: acknowledgment is BERTON'S EXPLICIT MM CONFIRMATION,
   substrate-verified: when a new human message arrives containing the
   approval token while the lock is (locked ...), the LOOP mechanically
   transitions the lock to (approved <op> <target-head>). Mechanical
   observation per P5; unforgeable from inside (Clarity's design intent
   "I can't generate confirmation I didn't receive" made structural:
   the substrate verifies the event, not her citation of it).
   Approval token (proposed, Berton confirms): SOUL-MUTATION-APPROVED.
3. COMMIT: she re-emits the mutation fresh (clear-first per her Q3);
   the gate runs FULL detection as always; a mutation matching the
   approved entry by OPERATION + TARGET HEAD (her Q2: not exact text)
   derives a PASS state -> executes -> lock = unlocked, record cleared.
   A non-matching mutation while locked or approved -> conflict.
   If re-emission fails, she retries next cycle; no mid-batch states.

Gate invariant (hers, kept verbatim in spirit): the gate never has a
bypass path; every mutation passes full detection; approved ones derive
PASS instead of PAUSE.

## Non-collision note

The staged parallel-vote gate package (mutation_gate_staged_work.md,
2026-05-26) is a separate governance-flow work item with its own
validation window. Repair 3 does not touch it and must not be conflated
with it.

## CONFIRM-LIVE (before any script)

1. Live `soul_is_pause` body and line range in src/helper.py (project
   copy shows the hardwire; live file has 124+ lines of drift).
2. Live loop.metta PAUSE branch text (the input consumer) and the
   applied 5c block's exact `$soul_decision` binding text (anchor
   targets).
3. Live `&pending_soul_mutation` initialization line in initLoop.
4. Live gate file: the current pending/conflict function texts in
   soul/soul_mutation_gate_corrected.metta (the commit path inserts
   beside them or in the glue; decision pending Clarity's answers).
5. Whether anything else consumes `&loops` halts (the input branch's
   `&loops 0` pattern is the template; confirm no other writer races).

## Clarity's design answers (received 2026-06-11, folded above)

Q1: Berton's MM confirmation, structurally verified (not reflection-cycle
self-authorization: "my reflection could rationalize what the gate
correctly flagged"). Q2: operation + target HEAD (exact text is fragile).
Q3: clear-first re-emission under a three-state lock; gate never
bypassed. Q4 (hardening): she has begun reading the gate file; her lead,
her schedule, completion signal expected per task framing.

## Additional new-message interaction (build-side note)

The APPROVED transition reads the incoming human message; it lands in
the message-reception region (Phase 4.0 vocabulary) as a single hook
calling a named function per artifact_0 Discipline 1, NOT inline logic.
The approval check is a plain substring presence test on $msgrcv (the
current message, never $msg history) while lock state matches.
