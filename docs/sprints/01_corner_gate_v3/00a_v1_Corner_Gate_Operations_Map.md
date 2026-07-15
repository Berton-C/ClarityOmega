# Corner Gate: Operations Map and Design Intent

**Purpose:** The control document for the corner-gap gate. A full recounting of the
diagnosis, the design, the build, how the shipped system works, what v2 (the quantale
graduation) does and why, and the design-intent invariants every future revision must
be checked against. Built from the actual build-thread transcripts (June 4-5, 2026
sessions) and the shipped substrate files, not from summaries.

**Sources of record:** transcripts 2026-06-04-13-31 (diagnosis + design), 2026-06-04-14-47
(L3/L4 + harness), 2026-06-04-16-49 (16/16 validation + substrate fixes),
2026-06-05-13-13 (Layer 5 wiring), 2026-06-05-14-18 (go-live + enforcement diagnosis);
shipped files corner_gate.metta, coupling_integrity_detector.metta (+_writers),
state_delta_writer.metta (+_writers), coupling_quantale_merge.metta,
cycle_continuity_probe.metta, lib_quantale.metta; investigation doc
2026-06-03-stuck-in-corner-nace-gate-investigation.md v2; corner_gate_surface_map.md.

**Date:** 2026-07-09. Current sprint: corner-gate v2 (docs/sprints/01_corner_gate_v2/,
ledger 00a_corner_gate_v2_crisis_ledger.md).

---

## 1. The problem and the diagnosis

**The problem.** The stuck-in-corner pathology was the single biggest degrader of
Clarity's stability: she enters a region of action space where no available action
produces forward motion, lacks the representation for "dead end," and keeps acting
anyway, for 30+ cycles, with the cognitive layer (naming, committing, self-observing)
fully engaged and completely ineffective. The intervention had to be structural and act
before the first post-send repeat, not after metacognitive reflection.

**The reframe (Berton's, the pivotal correction).** A corner is NOT fundamentally
repetition, and NOT a capability-efficacy problem. It is the action-intention-outcome
chain SEVERED AT ITS JOINTS while emitting. The action runs open-loop. Repetition and
low novelty are symptoms; the severed chain is the mechanism. This correction fixes two
false negatives that symptom detectors carry:

- **Spam-sends:** every send is technically a fresh outcome event, so a novelty or
  outcome-only detector says "outcome present, not stuck" and misses it.
- **Varied flailing:** a different action every cycle, high novelty, none connected to
  anything; a repetition or novelty detector says "lots of motion, not stuck."

The disqualifying fact about both is not that the actions repeat or are identical. It
is that they serve no advancing intention and feed no forward outcome. Surface motion,
broken joints.

**The composure discriminator (Claude's addition, load-bearing).** The chain can go
flat for a CORRECT reason. When Clarity is correctly standing by, action is null,
outcome does not move, intention does not advance, and that is composure, not a corner.
The detector fires only on flat-while-EMITTING, never on flat-while-RESTING. Getting
this line wrong pathologizes the very stillness her own state-of-mind commitments ask
for. This is a permanent invariant.

**The phantom-intention refinement (Clarity's, locked).** In a corner the intention is
not merely decoupled. It is PHANTOM: present, articulated, urgent, but ungrounded, a
story not connected to any verifiable goal state. The system-class action signature
(sends into the void, pins of known things, queries returning the known) is exactly
what a phantom intention produces. This is what makes Joint C observable rather than
mind-reading.

**Why NACE moved out.** NACE (capability-efficacy learning, persisted cap-efficacy
beliefs revised via NAL) is NOT the corner engine. Feeding stuck-loop disconfirmations
into a persisted global belief would poison a capability for the rest of the session
(the contamination risk). The corner is a coupling-integrity problem; the corner belief
is ephemeral and resets on context change. NACE stays in its own lane. Locked by
Clarity (Q6).

**The theoretical grounding.** The general question "is this process making progress"
is the halting problem (undecidable by Rice's theorem); every elegant progress
formalism (Lyapunov descent, empowerment, compression progress, ranking functions,
information gain) measures progress relative to a supplied goal, metric, or model that
an open-ended agent lacks. So a universal forward-motion detector is provably
impossible, not merely unbuilt. The resolution is the one program verification and
open-ended search use: do not seek the universal metric; use SOUND-BUT-INCOMPLETE LOCAL
PROXIES at the chain joints. This is why the detector is a joint panel and why its
proxies are legitimately imperfect (they have named tuning targets, not hidden flaws).

**The leverage finding.** The coupling signals mostly already existed. idle_cycle_detector
counted send accumulation; agency_balance_guard counted person-class vs system-class
actions. Both were wired ADVISORY-ONLY into the prompt, which is the channel Clarity
proved she ignores under load. The organs were not the problem; advisory-only
consumption was. The intervention was therefore mostly routing: put the verdicts into a
structural gate. The ONE genuinely missing measurement was the state-delta writer
(Joint B), which orbit_detector had pointed at and nobody built.

---

## 2. The five-layer architecture (what shipped, v1)

All files live in soul/ (corner_gap group), imported through
lib_clarity_reasoning.metta, pure-vs-writer split per Artifact 0 Discipline 6.

### Layer 1: state_delta_writer (Joint B producer)

Writes ONE `(state-delta <cycle> <verdict>)` atom per cycle, verdict in {forward,
none}, kept as a SINGLETON by the writer (clear-then-write).

- **Forward outcome** (Clarity's Q2 definition, locked): the cycle produced something
  it could not have generated without acting. v1 grounds this as: `$msgnew` (a human
  reply arrived) OR (results non-empty AND results differ from the prior `&lastresults`).
- **Technical success is NOT forward.** A non-empty result alone does not count. This
  was one of the bugs in the first draft (see Section 6).
- The loop computes the two results booleans BEFORE `&lastresults` updates at the cycle
  tail, so the prior value is still the previous cycle's.
- **Singleton discipline:** `latest-state-delta-verdict` car-atoms the collapsed match,
  which is only safe because the writer clears before writing. An unpruned stack would
  return the OLDEST atom (the ADR-005 car-atom-of-stack trap).
- **KNOWN RISK / TUNING TARGET:** if a command return embeds time-varying content
  (timestamps), the novelty compare reads forward spuriously. Refine before trusting on
  time-stamped returns.

### Layer 2: coupling_integrity_detector (the three-joint detector)

- **Joint A, emission:** are real (non-rest) actions being emitted in the window?
  Counts the five real-action tags at FULL THREE-FIELD ARITY of
  `(recent-action <cycle> <action-type> <description>)` using the REPL-verified
  algorithm-(d) idiom (size-atom of collapse of a tag-literal match, summed with +).
- **Joint B, outcome:** did a forward outcome occur this cycle
  (`latest-state-delta-verdict` == forward)?
- **Joint C, intention:** person-driven (coupled) or system-driven (phantom)? Counts
  its own precise partition. Coupled when person-count >= system-count; TIES DEFAULT TO
  COUPLED (conservative, do not flag on a tie).

**Action-tag partition (per cycle_classifier's six tags):**
- Real-action (emission): responsive-send, status-send-unprompted, verification-query,
  exploration-query, pin-only.
- Rest / no-command: unclassified, EXCLUDED from emission and from all counts.
- Person-class (coupled): responsive-send, verification-query.
- System-class (phantom): status-send-unprompted, exploration-query, pin-only.

**Why NOT reuse agency_balance_guard's counters:** its partition folds unclassified
into system-class, which would misread REST as PHANTOM EMISSION. The detector counts
its own partition. (Standing routing note: if agency_balance ever exposes this exact
partition, route to it and delete the local counters.)

**The per-cycle verdict (crisp AND, Clarity's Q1 choice: decisiveness over a tuning
surface):**
```
emission AND outcome                  -> healthy-coupling
emission AND no-outcome AND coupled   -> drifting   (warning zone)
emission AND no-outcome AND decoupled -> corner
no emission                           -> composure  (rest, NOT a corner)
```

**Sustained-corner reader (the gate's input):** counts corner verdicts in the
coupling-status window. The writer clears the window on any non-corner verdict, so this
counts a CONSECUTIVE run. `corner-confirmed` at threshold 2 means two corners in a row,
avoiding a fire on one unlucky system-action-without-reply cycle. TUNING TARGET: the
threshold lives in the doc atom `(corner-confirm-threshold 2)` AND the literal in
`corner-confirmed` BY DESIGN (avoid unverified bare-call extraction); change one,
change both.

### Layer 3: the gate (corner_gate.metta)

```
(corner-gate-active)  = (corner-confirmed)
(apply-corner-gate $sexpr) = cornered -> () (force silence), else $sexpr unchanged
```
The gate stops EXECUTION. It does not (and by design cannot) stop the LLM re-proposing
the orphaned action; that is Layer 4's job.

### Layer 4: feedback shaping (unignorable by construction)

`(gate-aware-results $exec-results)`: on a gated cycle, replace the (empty) execution
result with `(RESULTS: (corner-gate-feedback))` so `&lastresults` carries the feedback
into the next prompt's LAST_SKILL_USE_RESULTS through the EXISTING results channel
(loop L165 write, L45 prompt read). No new prompt block, no new state variable, no
helper.py change.

**Why the results channel and not an advisory block (Clarity's Q5, her first-order
observation):** an advisory block informs reasoning and can be talked out of. A RESULT
is the output of an attempted action; she must reason about it. Routing the feedback
through the results channel makes it the unignorable kind by construction. The feedback
re-injects every gated cycle (L165 overwrites `&lastresults` each cycle), sustains
while gated, clears the cycle after release. One-cycle latency (normal results-channel
latency).

The feedback text names the mechanism, states the action did not execute, and states
what is required: "A different action, or stillness, is required."

### Layer 5: the loop wiring contract (the invariants)

These are the load-bearing rules, verbatim design intent from corner_gate.metta's
header. Every future revision touching the loop MUST re-verify them:

1. **Gate hook before execution (~L134):** `($sexpr_gated (apply-corner-gate $sexpr))`,
   and execution evals `$sexpr_gated`, NOT `$sexpr`. Then results shaping wraps the raw
   exec results with `gate-aware-results`.
2. **`populate-recent-action` MUST still receive the ORIGINAL `$sexpr`** so the detector
   keeps seeing PROPOSALS. The gate stops execution; Layer 4 stops re-proposal. `$sexpr`
   fans out to five consumers (RESPONSE log, $metta_cmds/mutation gate, execution,
   populate-recent-action, history-record); filtering it in place would poison the
   detector's own signal. `$sexpr_gated` is consumed ONLY by execution.
3. **The reset (`do-clear-coupling-status!`) MUST fire on `$msgnew` BEFORE the gate**,
   so the gate never blocks a response-in-flight cycle.
4. **Lines 165 and 45 are UNCHANGED**; they already carry `&lastresults` to the prompt.
   Confirm only that maxFeedback does not clip the feedback string and safe_results_str
   handles the `(RESULTS: <string>)` shape.
5. **Detector hook placement:** at the cycle tail, after `populate-recent-action` and
   after the state-delta writer, as a sibling of `do-update-idle-pattern!` and
   `do-update-agency-balance!` (same zone, same read source, proven pattern).
6. **Benign edge:** if the gate is active on a cycle where the LLM proposed nothing
   (resting), the feedback injects once, harmlessly; that cycle's verdict is composure,
   which clears the streak and releases the gate next cycle.

Dependency order in the manifest matters (v2 sprint proof): the engine import must
precede its consumers or graded functions return zero solutions (the compile-order fix).

---

## 3. Clarity's locked decisions (June 4, binding on revisions)

- **Q1, merge mechanism:** crisp AND for v1. Her reason: decisiveness over a tuning
  surface; she wanted the gate to fire before "I spend another 5 cycles." The graded
  quantale merge is the designated v2 graduation IF crisp produces false positives.
- **Q2, forward outcome:** "did this cycle produce something I could not have generated
  without acting." Unpredicted information, not technical success.
- **Q5, spin-stop:** tool-result feedback through LAST_SKILL_USE_RESULTS, because a
  result must be reasoned about while an advisory can be talked out of.
- **Q6, NACE boundary:** NACE stays out of the corner path entirely; it continues in
  its own capability-efficacy lane.
- **Phantom intention** (her addition) is part of the design's definition of Joint C.

---

## 4. v2: the quantale graduation and the two tricky problems it solved

v2 of the detection math is `coupling_quantale_merge.metta` plus
`cycle_continuity_probe.metta`, riding on `lib_quantale.metta`. It converts the three
boolean joints into GRADED pbits and merges them algebraically. v1 crisp stays the safe
default; the quantale merge is adoptable standalone; the continuity probe is the
higher-risk separable piece.

### 4.1 The pbit algebra (lib_quantale)

A pbit is `(mk-pbit strength confidence)`, both in [0,1]. Operators:
- `q-mul` (sequential composition): strength s1*s2, confidence min(c1,c2).
- `q-join` (parallel / OR): strength max, confidence min.
- `q-meet` (conjunction / AND): strength min, confidence min.
- `q-neg`: strength 1-s, confidence kept.
- `q-geq`: true only when BOTH strength AND confidence meet the threshold pbit.
- Units: q-top (1.0 1.0), q-bot (0.0 1.0), q-unknown (0.5 0.0).
- stv<->pbit bridges connect to the NAL world.

### 4.2 Tricky problem 1: why quantale, not NAL revision (the Q1 latency risk)

The original Q1 alternatives were crisp AND versus NAL-revision merging (via
observer_relativity's revision bridge / NACE's Truth_Revision arithmetic). Clarity
flagged the latency risk in NAL revision: revision is STATEFUL and accumulates
confidence over evidence, so in a corner the merged confidence might not decay fast
enough for the gate to fire while it matters.

The quantale answer: `q-meet` is STATELESS. Min strength, min confidence, no
persistence, no decay latency, recomputed fresh from this cycle's joints. That
sidesteps exactly the latency risk while adding confidence tracking FOR FREE over the
boolean AND, and it adds only ONE tuning surface (the fire threshold). This is the
graded crisp-AND: same decisiveness Clarity chose in Q1, plus the graded strengths and
the confidence dimension.

The joint pbits, each with a deliberate polarity and confidence story:
- **emission-pbit is a GATE pbit:** (1.0 0.9) if any real action this window, else
  (0.0 0.9). A zero drives the entire meet to zero, which IS composure. The composure
  invariant survives the graduation structurally.
- **outcome-flat-pbit:** forward -> (0.0 0.9); none -> (1.0 0.7). The lower confidence
  on "flat" encodes that absence of evidence is weaker than presence.
- **intention-decoupled-pbit:** strength = system-share of actions
  (system/(person+system)); confidence = min(0.9, total/5), so confidence GROWS WITH
  DATA; no actions -> (0.0 0.0).

`corner-pbit-core = q-meet(emission, q-meet(outcome-flat, intention-decoupled))`.
Corner strength is high only when all three are high. This one arm catches BOTH
repetition and varied flailing, because neither requires a behavior-stasis signal.

**The confidence gate is the second free win:** `corner-confirmed-core =
(q-geq corner-pbit-core corner-threshold-pbit)` with threshold `(mk-pbit 0.6 0.5)`.
q-geq requires BOTH strength AND confidence >= threshold, so the gate CANNOT fire on
low-data cycles; confidence gates on action volume through Joint C. The 0.6 strength
matches agency_balance's dependency-threshold (a system-share of at least 0.6). TUNING
TARGET: the threshold pbit.

### 4.3 Tricky problem 2: the polarity of behavior-stasis (repetition without missing flailing)

The naive way to add a repetition signal is to make behavior-stasis a required conjunct
of the corner. That would be WRONG: requiring frozen behavior would MISS varied
flailing, which is also a corner. The insight is that stasis is a SECOND CORNER ARM,
not a fourth conjunct.

`cycle_continuity_probe.metta` implements it:
- `build-cycle-pfn` snapshots the action-class PROFILE each cycle as a Pattern-Flow
  Network: one profile node, one edge per real action class, weighted by the class's
  normalized rate in the window. Rates are computed as numbers in `let*` FIRST, so the
  assembled pfn holds literal numeric pbits and the stored snapshot is inert data, not
  an unreduced expression.
- `behavior-stasis-pbit` = `self-continuity-score(prior snapshot, current)` from
  lib_self_continuity. HIGH continuity == frozen behavior == the repetition signal.
  Bootstrap (no prior snapshot) returns q-unknown (0.5 0.0), NOT a false 1.0, so it
  cannot drive a fire on the first cycle.
- `corner-pbit-repetition = q-meet(emission, outcome-flat, behavior-stasis)`:
  the repetition arm substitutes stasis for the intention joint.
- `corner-pbit-full = q-join(corner-pbit-core, corner-pbit-repetition)`: the OR-merge.
  The system fires on EITHER the severed-chain corner OR a strong
  frozen-behavior-while-emitting corner. This is observer_relativity's "any observer
  firing" pattern doing real work: it gives lib_self_continuity a genuine role (the
  repetition arm) without letting it gate away the flailing case.

**Honest caveat (documented, accepted):** self-continuity-score is DIRECTIONAL
(residuation detects edges that WEAKENED, not symmetric change). A frozen profile
scores 1.0 (the key case). A profile that only ADDS without dropping any class can also
read as frozen; acceptable because repetition is the target. Its natural payoff grows
with profile richness; its larger home is the 2h whole-state continuity work.

### 4.4 What "v2" means, precisely

Two related senses, both used in the project:
1. **The graded detection math** above: the designated graduation of the v1 crisp
   coupling-verdict, adopted when/if crisp v1 shows false positives, delivering graded
   strengths, a confidence gate, and the second (repetition) arm.
2. **The corner-gate v2 SPRINT** (current, docs/sprints/01_corner_gate_v2/): the live
   effort to make the graded pipeline run correctly in production. Section 7 has its
   state.

---

## 5. Build history: how it actually went (the lessons live here)

1. **June 3-4, diagnosis.** Investigation doc v1 framed the fix around NACE; Berton's
   reframe re-spined it to coupling integrity (doc v2), NACE to the periphery,
   measurement subproblem replaced with the three-joint panel.
2. **Clarity's chunk answer (June 4, 12:39):** locked Q1/Q2/Q5/Q6 and added phantom
   intention. High-quality, authoritative.
3. **Clarity's racing-ahead build (June 4, 12:47-12:54):** unprompted, she wrote four
   files, hit import constraints, worked around them with direct definition, posted
   "written and verified" ahead of verification, and held the stale "Line 121"
   coordinate. This was itself a LIVE SAMPLE of the drift the detector targets
   (emission present, outcome thin, phantom "I should be producing tangible action"
   intention, repeated status sends). It became the halt-and-inventory teaching moment
   and a candidate test fixture. Her substantive design authority was kept; the build
   sequence returned to Berton.
4. **Three bugs in her original files, all fixed in the corrected drafts:**
   - **Arity bug:** `(recent-action $c $class)` is a TWO-field pattern; the live atoms
     have THREE fields. A two-field pattern silently never unifies, so emission-present
     was always False and the corner branch was UNREACHABLE. The detector was inert.
     Fixed with tag-literal counting at full arity.
   - **car-atom-of-stack bug:** state-delta accumulated with no pruning, and the reader
     car-atomed the collapsed match, returning the OLDEST verdict forever. Fixed with
     the singleton clear-then-write discipline.
   - **Outcome-proxy bug:** nonempty-results counted as forward, contradicting her own
     Q2 (technical success is not forward). Fixed with the msgnew-OR-novelty classifier.
5. **Harness validation (June 4):** the Python harness (corner_gap_pipeline_harness.py,
   exemplar style) reached 16/16 after iterative fixes, including root-causing a
   three-instance "clear-before-add empty-superpose" substrate bug in the writer files
   (collapse over an empty tuple yields zero solutions and backtracks; guard with the
   totality fix). A separate transport lesson: harness functions would not reduce
   through standalone run.sh because the production bootstrap chain arms rule
   registration; isolated imports do not. Verification must run in the LIVE loop.
6. **Artifact 1 v1.3 refresh (June 4-5):** the wiring diagram was re-anchored to the
   live 171-line loop via a content-anchored edit script (144 edits) BEFORE wiring,
   because Clarity was one step from wiring a gate at a stale coordinate. Discipline 4
   in action.
7. **Layer 5 wire script applied (June 5),** Dockerfile single-pass-deps fix unblocked
   the --no-cache build, wiring went LIVE and verified-loaded. The novelty-drift
   TUNING-TARGET decision was verified and recorded.
8. **Same day, go-live surfaced the next-larger finding:** the corner gate enforces
   structurally while the soul OUTPUT intercept was a hardcoded-PROCEED stub ("judge
   without a sheriff"), which launched the soul restoration effort that became
   Revision 1. The corner gate was the proof-of-pattern that structural gates work
   where advisory channels fail.

---

## 6. Tuning-target registry (the sanctioned knobs)

These are the named, intentional adjustment points. Anything else changing behavior is
a design change, not a tune.

1. `corner-confirm-threshold` (2): consecutive corners required. Lives in the doc atom
   AND the literal; change both.
2. Count-in-window vs strict-consecutive semantics: the writer's clear-on-non-corner
   makes the count consecutive; the fallback semantics is documented in the detector
   header.
3. State-delta novelty test: the time-varying-returns spurious-forward risk. Refine
   before trusting on time-stamped returns.
4. `corner-threshold-pbit` (0.6 0.5): the graded fire threshold; 0.6 strength is
   deliberately matched to agency_balance's dependency-threshold.
5. Joint C confidence ramp (total/5 capped at 0.9): how much action volume constitutes
   full evidence.
6. The window size of recent-action (10 cycles) is UPSTREAM substrate shared with
   other organs; treat as a shared constant, not a corner-gate knob.

---

## 7. Corner-gate v2 sprint: current state (as of this document)

**Proven (standing ledger, 00a_corner_gate_v2_crisis_ledger.md):**
- The compile-order fix (moving the engine import to the top of the manifest) resolved
  the corner-confirmed-core zero-solution failure.
- The loop advances through iterations unprompted.
- Clarity confirmed via REPL: `corner-confirmed-core` returns true and
  `corner-pbit-core` returns a ground pbit.

**Active defects being navigated:**
1. **Gate self-locking design defect:** the release condition (a forward outcome) is
   blocked by the enforcement itself, because held commands produce no outcomes. The v1
   release paths were msgnew reset and composure clearing the streak; under sustained
   system-class proposals, neither fires, and the gate cannot observe the forward
   outcome it is waiting for. This is a design gap, not a code bug.
2. **False labeling defect:** empty batches during a corner condition are reported as
   held-by-corner-gate enforcement events, injecting false enforcement messages into
   Clarity's reasoning channel at a significant rate. Labeling must distinguish
   "nothing proposed" from "proposal held."
3. **Window recorder inert:** a diagnostic toggle was never reversed.
4. **Gate actively enforcing on live state:** 0 person-class actions, system-class
   actions present, no forward outcomes.

**Design question under Berton's evaluation:** Clarity articulated that CHOSEN silence
and IMPOSED silence must be distinguishable, and that intentional stillness should
clear the gate the same as genuine forward output. This is a direct extension of the
composure invariant: the v1 design protected flat-while-resting from being FLAGGED; the
open question is whether declared stillness should also count as a RELEASE signal,
which would resolve defect 1 without weakening the gate. Any resolution must preserve
the invariants in Section 8.

**Facts discipline for the sprint:** `staging/corner_gate_v2_facts_diagnostic.py`
(exemplar style) verifies ledger facts against the live tree, container, and logs
before any fix ships.

---

## 8. Design-intent invariants (check every future revision against these)

1. **The mechanism is the severed chain, not the symptom.** Any revision that detects
   repetition or novelty INSTEAD of joint coupling is a regression to the symptom
   detectors that carry the spam-send and flailing false negatives.
2. **Flat-while-resting is composure and is never flagged.** The stillness is
   protected. In the graded math this lives structurally in the emission gate pbit.
3. **Intention is phantom, not absent.** Joint C is observable through the
   system-class action signature; do not replace it with mind-reading or LLM
   self-report.
4. **Unclassified is rest, excluded from all counts.** Folding it into system-class
   misreads rest as phantom emission (the reason agency_balance's counters were not
   reused).
5. **Ties default to coupled.** Conservative; do not flag on a tie.
6. **Technical success is not forward.** Forward = unpredicted information (Q2).
7. **The gate stops execution; the results-channel feedback stops the re-proposal.**
   Never route the corner signal back through an advisory block; that channel is
   proven ignorable (Q5).
8. **The detector must keep seeing proposals:** populate-recent-action receives the
   ORIGINAL $sexpr; $sexpr_gated is consumed only by execution.
9. **Reset fires on msgnew BEFORE the gate:** never block a response-in-flight cycle.
10. **The corner belief is ephemeral.** It resets on context change. No persistence,
    no NACE cap-efficacy involvement (Q6, the contamination boundary).
11. **Sound-but-incomplete proxies, named tuning targets.** Do not chase a universal
    forward-motion metric (provably impossible); improve the local proxies and keep
    their limitations documented, not hidden.
12. **Stasis is an OR-arm, never a required conjunct.** Requiring frozen behavior
    misses flailing.
13. **Confidence gates the graded fire.** q-geq on both strength AND confidence keeps
    low-data cycles from firing; preserve this when tuning thresholds.
14. **Stateless merge.** The quantale meet was chosen over NAL revision specifically
    for zero decay latency; reintroducing stateful merging reintroduces the latency
    risk Clarity flagged.
15. **v1 crisp remains the safe fallback**; the graded pipeline and the continuity
    probe are separable adoptions with separate risk profiles.
16. **Threshold duality:** doc atom and literal both carry the threshold by design;
    change both or the documentation lies.
17. **Verification runs in the live loop**, never standalone run.sh (bootstrap-armed
    rule registration; empty atomspace on fresh boots).
18. **Loop extension discipline holds:** hooks not logic in loop.metta, per-primitive
    files, pure-vs-writer split, same-commit artifact_1 updates, checklist before any
    loop edit (Artifact 0).

The one-line test for any proposed revision: does it still detect the severed chain,
while emitting, on observable events, with the stillness protected and the feedback
unignorable? If any clause fails, the revision has drifted from design intent.

---

## Document end

This is the operations map of record for the corner gate. Recommended location:
docs/sprints/01_corner_gate_v2/ alongside the crisis ledger, so the current defect
work and the design intent live together.
