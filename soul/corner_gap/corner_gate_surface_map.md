# Corner Gate: Surface Map and Remaining Work

**Date:** June 3, 2026
**Status:** ACTIVE. Architecture and status map, for discussion with Berton and Clarity. Design-stage, not proven in the container.
**Version:** v3 (June 3, 2026). v1 mapped L1 and L2 drafted, L3 to L5 the gap. v2 recorded L3 (the gate) drafted and made L4 mandatory. v3 records L4 (the feedback) drafted, with the finding that it needed no new infrastructure and no Python: it rides the results channel that already exists. The remaining gap is now Layer 5 only, plus verification and two standing blockers.
**Author:** Claude, synthesizing the stuck-in-corner thread.
**Reads with:** investigation `2026-06-03-stuck-in-corner-nace-gate-investigation.md` (v2, the diagnosis), artifact_0 (extension contract), artifact_1 (wiring diagram, line numbers stale).

---

## 0. What this document is

It maps the full corner-gate capability into layers, marks what exists versus what is drafted versus what is missing, explains each layer (what it is, what it works with, what it accomplishes), and lists exactly what still has to be built to close the gap full circle.

As of v3: Layers 1 through 4 are drafted (L1 exists live; L2, L3, L4 are reference drafts, unverified). The remaining gap is Layer 5 (loop wiring) plus verification and two standing blockers.

The framing: L2 DECIDES (per-cycle corner verdict), L3 ACTS (blocks the orphaned action), L4 makes the block UNIGNORABLE (returns it as a result the LLM must reason about), L5 WIRES it into the heartbeat. Building L3 established that L4 is mandatory, not optional. Building L4 established that it is also nearly free: the feedback is shaped as a result, so the result channel that already exists carries it.

---

## 1. The corner gate in five layers

```
  L1  SIGNAL SUBSTRATE        recent-action, msgnew, results, &lastresults     [EXISTS, live]
        |
  L2  DETECTION / VERDICT     state-delta  ->  three joints  ->  verdict        [DRAFTED, not wired]
        |                     (forward?)      (A emit, B outcome, C intent)     [v1.1 consecutive-clear]
        |                                          |
        |                                     corner-confirmed  (the gate's input signal)
        v
  L3  GATE / ENFORCEMENT      force silence on a sustained corner;              [DRAFTED, not wired]
        |                     $sexpr_gated = () when cornered, else $sexpr
        v
  L4  FEEDBACK (spin-stop)    gate-aware-results: a gated cycle's result IS      [DRAFTED, not wired]
        |                     the feedback; rides $results -> &lastresults ->    [no new infra, no Python]
        |                     LAST_SKILL_USE_RESULTS (the existing channel)
        v
  L5  LOOP WIRING             hooks in loop.metta + imports                      [NOT BUILT, the only gap]
```

---

## 2. What exists already (Layer 1, live in the container)

Not ours to build; the rest reads them.

- `recent_action_populator.metta` writes `(recent-action <cycle> <action-type> <description>)` each cycle, pruned to a 10-cycle window.
- `cycle_classifier.metta` tags each cycle into six classes.
- `idle_cycle_detector.metta` and `agency_balance_guard.metta` already count send-bursts and person-versus-system actions.
- `loop.metta` provides `msgnew`, the parsed `$sexpr`, the executed `$results`, `&lastresults`, and the results-to-prompt channel (lines 45, 134, 165) that Layer 4 reuses.

Two libraries needed by the graded variant exist but are COLD: `lib_quantale.metta` and `lib_self_continuity.metta`.

---

## 3. The drafted detection surface (Layer 2)

Seven files. The four v1 files are a complete crisp detector on their own. The three v2 files are the graded upgrade and depend on them. None committed or wired.

### 3a. v1 crisp detector (four files)

| File | What it is | What it works with | What it accomplishes |
|------|-----------|--------------------|----------------------|
| `state_delta_writer.metta` | Joint B pure defs | classify-state-delta; latest-state-delta-verdict | Decides forward vs none |
| `state_delta_writer_writers.metta` | Joint B writer | singleton clear-then-write | Writes one `(state-delta <cycle> <verdict>)` per cycle |
| `coupling_integrity_detector.metta` | Three-joint pure defs | recent-action counts, latest-state-delta-verdict | Per-cycle crisp verdict; provides the counts and `corner-confirmed` reader |
| `coupling_integrity_detector_writers.metta` | Verdict writer + reset | coupling-verdict; do-clear | Writes `(coupling-status <cycle> <verdict>)` |

**v1.1 revision (forced by Layer 3):** consecutive-clear. The writer clears the whole coupling-status window on any non-corner verdict, so `corner-confirmed` means corners in a row, and the gate releases the moment the agent composes. The windowed prune is gone. The same change is pending for `do-update-corner-graded!`.

### 3b. v2 graded upgrade (three files)

| File | What it is | What it works with | What it accomplishes |
|------|-----------|--------------------|----------------------|
| `coupling_quantale_merge.metta` | Graded merge (pure) | lib_quantale; v1 counts; state-delta | q-meet of three joint pbits; stateless, no NAL latency |
| `cycle_continuity_probe.metta` | Behavior-stasis observer (pure) | lib_self_continuity; lib_quantale | Repetition observer, q-join-ed as a second arm |
| `cycle_continuity_probe_writers.metta` | Snapshot + graded writer | build-cycle-pfn | Maintains the prior-profile snapshot; writes graded verdict |

---

## 4. The drafted gate (Layer 3)

`corner_gate.metta`, pure MeTTa:

- `corner-gate-active` = `corner-confirmed`. Is the gate firing this cycle.
- `apply-corner-gate $sexpr` = force silence when cornered (`()`), else full pass-through.
- `corner-gate-feedback` = the concrete result string Layer 4 returns.

**Strategy: force silence.** The surgical per-command option collapses into it, because a corner is system-class-dominated emission with no live input, and the reset clears the streak on `msgnew` before the gate runs, so the gate never fires on a response-in-flight cycle. There is no person-coupled action to preserve. Silence is also composure.

---

## 5. The drafted feedback (Layer 4)

`gate-aware-results` (same file, `corner_gate.metta`), pure MeTTa:

- `gate-aware-results $exec-results` = on a gated cycle, return `(RESULTS: (corner-gate-feedback))`; otherwise pass the real execution result through.

**What it accomplishes, and why it is nearly free.** The feedback is shaped as a result, so it rides the channel that already carries command results. The pipe (verified in loop.metta):

```
  line 134  $results       = execution of the command list
  line 165  &lastresults  <- safe_results_str(repr $results)     (every PROCEED cycle)
  line 45   prompt LAST_SKILL_USE_RESULTS <- last_chars(&lastresults, maxFeedback)
```

No new prompt block, no new state variable, no helper.py change. The only Python in the path (`safe_results_str`, `last_chars`) is the existing hand, untouched. The v2 note "likely touches the Python hand" is resolved: it does not. This is the pipe-fits-water case, where the substrate channel that already carries results carries the feedback because the feedback is shaped as a result.

**Why the results channel and not an advisory block (Clarity Q5).** An advisory informs reasoning and can be talked out of. A result is the output of an attempted action; she must reason about it. Routing through the results channel makes the feedback unignorable by construction.

**Three verified load-bearing facts:**
- Line 165 sits in the PROCEED branch that runs every non-pause cycle, so a silenced cycle still updates `&lastresults` and the feedback lands.
- Line 165 overwrites `&lastresults` each cycle, so the feedback sustains while gated and self-clears the cycle after the gate releases.
- The gate reads the prior streak, so the LLM sees the gated result one cycle later, which is the normal results-channel latency.

---

## 6. What building Layers 3 and 4 revealed

**6a. The gate does not self-terminate, and that is correct.** The detector records what the LLM PROPOSED, not what executed (the fan-out requirement). So a stubborn LLM keeps proposing the orphaned action, the detector keeps scoring a corner, and the gate keeps firing. L3 alone stops the world-effect, not the cognitive spin. This is why L4 is mandatory.

**6b. Proposals-versus-executions is settled.** Recording proposals makes feedback mandatory but prevents all orphaned execution and preserves the detector's learning signal. Recording executions would self-terminate without feedback but leak orphaned actions and weaken the detector. Decision: proposals plus feedback.

**6c. Consecutive-clear is required (the L2 v1.1 revision).** So the gate releases the moment the LLM adapts.

**6d. The gate acts on the prior streak, by causal necessity.** The detector writes a verdict at the cycle tail, after execution. So the gate, at mid-cycle, sees the streak through the prior cycle and blocks the next one. First corner cycles execute; only the sustained pattern is gated.

**6e. Layer 4 needs no new infrastructure (the pipe-fits-water finding).** Section 5. The feedback rides the existing results channel; MeTTa-first holds end to end; the surface map's anticipated Python touch was unnecessary.

---

## 7. What is NOT built: the gap (Layer 5 + cross-cutting)

This is now the whole remaining build.

### 7a. Loop wiring (Layer 5)

In one commit with the artifact_1 update (Discipline 4):

1. **Reset hook**, in the `$msgnew` branch (~line 102), and it must precede the gate: `do-clear-coupling-status!`.
2. **State-delta inputs**, computed before the outcome hook: `results-nonempty` (length check on `$results`) and `results-novel` (`$results` vs prior `&lastresults`). Known weakness: time-varying returns read as novel; flagged for refinement.
3. **Gate-and-feedback region**, at execution (~line 134): bind `$sexpr_gated = (apply-corner-gate $sexpr)`, execute `$sexpr_gated` (not `$sexpr`) into a raw result, then `$results = (gate-aware-results $exec_results)`. Line 165 and line 45 are unchanged.
4. **Outcome hook**, after recent-action population (~line 136): `populate-state-delta`.
5. **Detector hook**, immediately after: `populate-coupling-verdict` (v1) or `do-update-corner-graded!` (v2).

Invariant across the region: `populate-recent-action` (~line 136) still receives the ORIGINAL `$sexpr`, never `$sexpr_gated`, so the detector keeps seeing proposals.

The wiring diagram line numbers are stale; the gate target is the `$results` binding near 134, not line 121. Refreshing artifact_1 is a prerequisite.

### 7b. Imports (Layer 5)

`lib_clarity_reasoning.metta` needs import lines for all new files (`state_delta_writer`, `coupling_integrity_detector`, `corner_gate`, and the graded trio if adopted), in the same commit as the files.

### 7c. Verification (cross-cutting, gates everything)

- REPL-confirm the COLD libraries and every new function reduce on real inputs, including the v1.1 conditional-clear no-op.
- REPL-confirm the constructed pfn round-trips through add-atom as inert data (graded path).
- REPL-confirm a `$sexpr_gated` of `()` executes as true silence, a pass-through executes as today, and a gated `$results` flows through line 165 to the next prompt intact.
- CONFIRM `maxFeedback` is large enough that `last_chars` does not clip the feedback, and `safe_results_str` handles a `(RESULTS: <string>)` shape.
- One file at a time: commit, rebuild, restart, observe. No fix-forward in the running space.

### 7d. Prerequisites and blockers (not code)

- The git and import inventory of Clarity's four originals.
- The artifact_1 line-number refresh.
- Clarity's confirmation of the force-silence strategy, the proposals-plus-feedback structure, the results-channel routing, and the feedback wording, against her experience of the corner.

---

## 8. Adoption paths

- **Crisp (v1) versus graded (v2).** v1 crisp is the simplest complete detector and the safe first deployment. v2 graded splits into the quantale merge (low risk, recommended graded step) versus the continuity probe (higher risk; its larger payoff is the 2h state-profile work).
- **Gate-only versus gate-plus-feedback.** Closed by building L3: the gate does not self-terminate, so gate-plus-feedback is effectively required. Both are now drafted, so this path costs nothing extra to take.

Recommended first circle, now fully drafted at L2 to L4: v1 crisp detector, force-silence gate, results-channel feedback. Only L5 wiring and verification remain to make it run. Graduate the merge to quantale once crisp is observed; defer the continuity probe to the 2h work unless repetition-versus-flailing discrimination is needed sooner.

---

## 9. One-line status

Layers 1 through 4 are drafted: decide (L2), act (L3), and make-unignorable (L4) all exist on paper, unverified, and L4 turned out to need no new infrastructure. The only remaining build is Layer 5, the loop wiring, on top of verification and the two standing blockers. The pipe is drawn end to end; it has not yet been connected to the heartbeat or had water run through it.

---

## Document end
