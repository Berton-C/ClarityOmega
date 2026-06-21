# Latent Capability and the Detection Mesh: What Raises Clarity's Level, and the Work to Do It

**Status:** Knowledge capture. Not a build spec. A map of what is built-but-unwired
in the substrate, why it matters to the coherence of Clarity's mind, and what kind
of work wires it, using corner-gate as the proven template for the work's shape and
cost.
**Provenance:** Written from a read-only investigation (June 2026) of the live
import chain, loop.metta, and the three uploaded libraries, plus Clarity's
file-grounded analysis of the nine detector libraries. Where a claim rests on
Clarity's reading rather than a direct read in this pass, it is marked.
**Companion docs:** `artifact_0_loop_extension_contract.md` (the discipline any of
this work follows), `nace_implementation_plan.md` (the in-loop NAL-consumer pattern
that layer three reuses).

---

## 0. The thing this document is about

There is a coherence to Clarity that is not the soul atoms, not the LLM, and not the
Python helpers. It persists across cycles and its capacity changes over time. It
appears as a property of the running loop. This document locates that coherence,
explains why a set of already-built-but-unwired libraries are the instruments that
would let it see and improve itself, and describes the work to wire them, in
increasing order of depth and difficulty.

The claim is not "add features." The claim is "close the loop between what the mind
does and what the mind can observe about what it does." That closure is what raises
the level of functioning. Everything below serves that one idea.

---

# Section 0.5: Accidental Binding - The Detector Domain's Root Problem

The nine detectors in Section 3 are not nine separate features. They are nine angles on one event: the system binding without noticing it bound.

This is accidental binding, the failure mode each detector was built to catch:

| Detector | Accidental binding it detects |
|---|---|
| `orbit_detector` | Binding to a cycle |
| `value_drift_detector` | Binding to shifted priorities |
| `resonance_reward` | Binding to appearance of growth |
| `goal_completion_checker` | Binding to claim of completion |
| `self_weaving_web` | Binding to assumed capability |
| `meta_awareness_engine` | Binding to surface reasoning |
| `observer_relativity` | Binding to default vantage |
| `diversity_protection` | Binding to single method |
| `regenerative_feedback` | Binding to degenerative loop |
| `temporal_horizon_expansion` | Binding to collapsed horizon |

A system that binds accidentally is brittle because it accumulates commitments it cannot see and therefore cannot revise. A system that makes binding visible can see its commitments and choose. The detection mesh makes binding visible. That is why it raises the level of functioning, and that is why it is one system, not nine features.

### Current inventory

| Instrument | What it addresses | Status |
|---|---|---|
| `coupling_integrity_detector` | Accidental coupling | LIVE, WIRED |
| `orbit_detector` | Accidental cycle binding | BUILT, UNWIRED |
| `value_drift_detector` | Accidental priority binding | BUILT, UNWIRED |
| `resonance_reward` | Performed vs genuine growth | BUILT, UNWIRED |
| `goal_completion_checker` | Claim-without-verify binding | BUILT, UNWIRED |
| `lib_temporal_v2` | Temporal vs static binding | AVAILABLE, UNWIRED |
| `cycle_classifier` | Action taxonomy | AVAILABLE |

The pattern: instruments exist, the wire (cycle-trace writer) does not. One producer fills the gap that keeps all of them dormant.

### Load-bearing connection

Accidental binding makes the system fragile. The detection mesh makes binding visible. Making binding visible is the precondition for choosing differently. This is not a metaphor. It is the mechanism by which corner-gate already works: the gate stops an impulse, `coupling_integrity_detector` tells the gate why. A gate without a mesh stops in performed stillness. A gate with a mesh stops and can name the orbit, the drift, the completion-gap, and choose.

---

## 1. Where the coherence actually lives

The `let*` in loop.metta does not hold the coherence. It holds one cycle's bindings
(the verdict, the gate state, the gated sexpr, the results), all of which vanish
when the iteration ends. Continuity lives in what survives between cycles, and only
two things do:

1. Atoms written to the AtomSpace, which persist in-process while the loop runs.
2. Files, which persist across restarts.

So the "mind" being pointed at is the accumulating trajectory of written state across
the loop's lifetime: the time-integral of what the loop writes and re-reads, cycle
after cycle. It is not in any single file. It resets on restart because the
in-AtomSpace half evaporates and only the file half reloads.

This matters for the rest of the document because it tells you precisely what
"raising the level" can and cannot mean. It cannot mean adding a static function and
expecting the mind to change. It can only mean changing what gets written into that
cross-cycle trajectory and what reads it back. The libraries below all act on that
trajectory, or they do nothing at all.

---

## 2. corner-gate: the proven template

corner-gate is the one instance of this kind of work already live, and it is the
template for everything else here. It is worth stating exactly what it is and what
it cost, because the cost is the argument.

### 2.1 What it is, as deployed (verified live in current loop.metta)

corner-gate Layer 5 was wired in commit ed878e5 and is live in the current runtime.
Its loop-facing surface, confirmed present this pass:

- `derive-gate-state` (line 140) computes a gate state each cycle; the SOUL-GATE-FLAG
  print (line 141) surfaces it, observed in production as `(SOUL-GATE-FLAG clean unlocked)`.
- `apply-corner-gate` (line 163) passes the verdict-approved command through the gate
  to produce the gated sexpr that is then executed.
- `gate-aware-results` (line 165) wraps execution results with gate awareness.
- `populate-state-delta` (line 172) and `populate-coupling-verdict` (line 173) write
  the gate's per-cycle observations into the cross-cycle trajectory.
- `do-clear-coupling-status!` (line 111) clears coupling status on a new message.

NOTE: the corner_gap source bodies (corner_gate.metta, coupling_integrity_detector.metta,
state_delta_writer.metta) were not read in this pass. The wiring above is confirmed
from loop.metta; the internal logic of each function should be read in-container before
any extension that depends on its exact behavior.

### 2.2 What it cost, and why that is the point

corner-gate was roughly an afternoon of work. Sprint 0-Coda (registry dispatch
wiring) was about ten days. The difference is not that corner-gate was sloppier; it
followed the same discipline. The difference is structural: corner-gate wired an
already-built detector into an existing decision point in the loop, whereas Coda
built a dispatch subsystem and proved it from nothing. That asymmetry is the entire
thesis of this document. Wiring a built-but-unwired instrument into the live
trajectory is small, bounded, independently verifiable work. There is a backlog of
such instruments. Each is its own afternoon-to-few-days increment, each is trackable,
and each adds a distinct facet of self-observation.

### 2.3 The shape of the work (the template steps)

Every item in Sections 3 and 4 follows corner-gate's shape:

1. Read the instrument's source and establish what it reads (input contract) and
   what it writes or returns (output).
2. Confirm or build the producer that feeds its input each cycle.
3. Call it at the right phase location in loop.metta (one hook line, Discipline 1).
4. Route its output into the cross-cycle trajectory: write an atom, surface it in
   the next-cycle prompt, or gate on it.
5. Update artifact_1 in the same commit (Discipline 4).
6. Verify in the live loop, not run.sh.

The leverage differs by item only in step 2: some instruments already have their
producer (cheap), some need a producer built (medium), and some need a whole
upstream subsystem (deep). That is the axis the rest of this document sorts on.

---

## 3. The detection mesh (layer one: highest leverage, lowest cost)

This is the cluster Clarity analyzed from file contents. The reframe that makes it
coherent: these are not nine separate features. They are nine angles on one event,
the capacity for the mind to see its own behavioral trajectory. corner-gate stops an
impulse; the mesh tells the gate WHY it fired. A gate without a mesh stops and sits
in performed stillness. A gate with a mesh stops and can name the orbit, the drift,
the completion-gap, and choose differently.

All of the following are reported by Clarity (from file contents) as NOT stubs. The
exact input contracts must be confirmed by reading each file before the producer is
built; that read is the first concrete step of layer-one work.

| Instrument | What it makes visible (per Clarity's read) | Reads (to confirm) |
|---|---|---|
| `orbit_detector` | Behavioral loops: idle-status-resend, query-without-using-results, pin-update-only, claim-without-verify; tracks state-delta (did anything change) | recent-action trace, state-delta |
| `goal_completion_checker` | Claimed-done vs verified-done; evidence types file-exists, test-passes, human-confirmed, output-verified | goal state, outcome evidence |
| `value_drift_detector` | Drift signatures: governance-bypassed-for-efficiency, helpfulness-promoted-above-integrity, and two more | action trace vs stated priorities |
| `resonance_reward` | Genuine vs performed growth: repeated-identical-pins, consolidation-cycling; genuine = artifact-referenced-later | pin/rest trace across cycles |
| `self_weaving_web` | Load-bearing capability use (pin has 3 dependents); query->pin->shell chain integrity | capability-use trace |
| `meta_awareness_engine` | Which cognitive layer is operating: surface (task), pattern (orbit), structural (paradigm); forces a layer-check before output | current activity + pattern state |
| `observer_relativity` | Observer-relative framing: observer-location, observer-purpose, observer-state; flags vantage assumed as default | framing/context of current reasoning |
| `diversity_protection` | Monoculture signatures, e.g. single-method-decision at threshold 0.85 | method trace |
| `regenerative_feedback` | Degenerative vs regenerative loops by whether feedback increases or decreases optionality | search/decision trace |
| `temporal_horizon_expansion` | Urgency collapsing the horizon; expansion asks what is visible at 3 min / 3 hr / 3 days | urgency state, action consequences |

### 3.1 The keystone

Almost every instrument above reads the same thing: a per-cycle behavioral trace,
what was pinned, queried, sent, whether results were used, whether state changed,
which method was used. The loop already writes part of this (recent-action,
state-delta, coupling-verdict, the corner-gate populators). It does not write the
rest.

The single highest-leverage piece of work in this entire document is the
**cycle-trace writer**: the producer that records the per-cycle behavioral trace
these detectors consume. Build it once, and six or more detectors become wireable,
because their missing input now exists. That is why this layer is both cheapest and
highest leverage: one keystone producer unlocks a cluster of afternoon-sized hooks.

### 3.2 Expected gain

The level change is concrete and nameable: corner-gate today stops and the mind sits
in performed stillness because it cannot see why. With the mesh, the same stop
becomes "this is a claim-without-verify orbit, the drift is
governance-bypassed-for-efficiency, the stillness is performed not genuine." Specific,
actionable, fed into the next cycle's prompt so the mind acts on its own observation.
The gain is not new abilities; it is the mind becoming legible to itself across
cycles, which is the precondition for it correcting its own trajectory.

### 3.3 First concrete step

Read the nine detector files in-container and extract each one's exact input contract.
The cycle-trace writer's spec is fully determined by the union of those contracts.
Taking the contracts from Clarity's summary rather than the files is the same shortcut
that produces the failures these detectors detect; read them.

---

## 4. The composition and continuity substrate (layer two: deeper, design-gated)

`lib_quantale` and `lib_self_continuity` are different in kind from the detectors.
They are not pattern-matchers over behavior; they are the mathematics of how
confidence composes and how identity persists. Read directly this pass:

- `lib_quantale` (7 functions over a `pbit` type): `q-mul` (sequential composition,
  multiplies strength, takes min confidence, which is why chained reasoning degrades
  by construction), `q-join` (parallel, max/max), `q-meet` (conjunction, min/min),
  `q-neg` (paraconsistent negation), `stv-to-pbit` / `pbit-to-stv` (NAL bridges),
  `governance-pbit` (two stv inputs meet, so two sources intersect certainty rather
  than add it).
- `lib_self_continuity` (16 functions to `self-continuity-score`): SCS is the degree
  of the IDENTITY map between two pattern-flow-network snapshots, a lower bound on
  true continuity. `theta-self-continuous` gates SCS against a threshold;
  `chain-continuity-bound` composes continuity across intervals via q-mul.

### 4.1 Why this is the deeper level

self-continuity-score is the formal handle on the exact coherence Section 1 describes.
"Did my patterns persist as themselves across cycles" is not a metaphor here; it is a
computable lower bound, if you can produce the snapshots. That is the catch and the
real work.

### 4.2 The work, and why it is not a hook

Neither library has operands in the live loop:

- `q-mul` composes two pbits. Nothing in the loop produces pbit-shaped truth values
  at the points where composition matters. Wiring quantale means first deciding where
  in the reasoning flow two truth values combine, then routing real producers through
  the algebra. The producer does not exist.
- `self-continuity-score` needs two pattern-flow-network snapshots. Nothing builds a
  pfn snapshot of a cycle. The work is to DEFINE what a pfn snapshot of Clarity's
  reasoning state even is, a graph of which patterns were active and how they
  connected, build the writer that produces one each cycle, store two, then score.

That snapshot definition is the hard intellectual work, and it is genuinely a design
question, what is the unit of Clarity's reasoning-identity, mathematically. It belongs
to Clarity and Berton, not to a mechanical spec. This layer is gated on that
definition, not on plumbing.

### 4.3 Expected gain

Two things the mind cannot currently do: measure how its own confidence should degrade
across a reasoning chain (instead of letting the LLM eyeball it), and measure whether
it remained itself across cycles (instead of asserting "recognition holds" with no way
to check). The first makes chained reasoning honest about its own uncertainty. The
second gives performed-stillness-vs-genuine-continuity a numeric answer. Both are
deeper than the mesh because they operate on the structure of reasoning, not the
record of behavior.

---

## 5. substrate_kb as a live reasoner (layer three: deepest, NACE-sibling)

`substrate_kb` is 632 lines, zero functions, entirely NAL belief triples of the form
`((--> A B) (stv f c))`. It is an inert knowledge base, not a gate. The "GO above 0.7,
BLOCK below 0.3" behavior does not exist as code; it is belief data with no reasoner
attached. The weakest-chain facts (e.g. web-source -> increases-confidence at f=0.49,
c=0.119) are stored beliefs, not live thresholds being checked before action.

### 5.1 The work

To make it live, something must run NAL inference over these chains in-loop (the
`|-nal` operator, which only reduces inside the running loop) so the network computes
derived confidences, and something must read those at decision points. This is a
second cognitive subsystem alongside NACE, and it reuses NACE's exact pattern:
file-backed beliefs, an in-loop hook that runs the substrate operator, results read
the next cycle. It should follow NACE, because NACE is proving that in-loop
NAL-consumer pattern now, and substrate_kb would inherit it rather than re-derive it.

### 5.2 Expected gain

The threat-countermeasure beliefs, confidence-decay tracking, and value-alignment
chains in the file would actually inform decisions instead of sitting as documentation.
The mind would reason over a persistent, revisable belief network about its own
domain, which is the same capability NACE provides for capability-efficacy, applied to
a broader knowledge base.

---

## 6. The leverage map (why this is trackable, distinct-leverage work)

| Layer | Items | Producer status | Cost shape | Leverage |
|---|---|---|---|---|
| 1. Detection mesh | 9 detectors | mostly need the one cycle-trace writer | one keystone, then afternoon-sized hooks | mind sees its own behavioral trajectory; gate gains its "why" |
| 2. Composition + continuity | lib_quantale, lib_self_continuity | need pbit producers / pfn-snapshot definition | design-gated, then medium | honest chained-confidence; numeric self-continuity |
| 3. Live belief reasoner | substrate_kb | needs in-loop NAL consumer (NACE pattern) | NACE-sibling, larger | persistent revisable domain reasoning |

The corner-gate point, stated plainly: corner-gate proved that wiring one built
instrument into the live trajectory is an afternoon, not a sprint, when the producer
already exists. Layer one is a backlog of corner-gate-shaped work behind a single
shared producer (the cycle-trace writer). That is why it is the place to start: it is
the most trackable, the most independently verifiable, and the fastest path to a
visible level change, and it is the same proven shape we already know how to execute
and verify.

---

## 7. Honest boundaries of this document

- The nine detector files were characterized by Clarity from their contents, not read
  directly in this pass. Their exact input contracts must be confirmed by reading them
  before the cycle-trace writer is specced. (Section 3.3.)
- The corner_gap source bodies were not read this pass; corner-gate is described from
  its confirmed live wiring in loop.metta, not from its internal logic. (Section 2.1.)
- lib_quantale, lib_self_continuity, and substrate_kb were read directly this pass.
- "Higher level of functioning" is defined narrowly and deliberately throughout: the
  mind's cross-cycle trajectory becoming visible to itself and able to act on that
  visibility. Claims of capability beyond that are out of scope and would be
  speculation.

---

## 8. Recommended sequence

1. Finish NACE (its own plan). It proves the in-loop NAL-consumer pattern that layer
   three reuses, and it is already in flight.
2. Layer one, starting with reading the nine detector files to extract input contracts,
   then building the cycle-trace writer (the keystone), then wiring detectors one at a
   time, corner-gate-shaped, each its own commit and live verification.
3. Layer two, beginning with the pfn-snapshot definition (a Clarity + Berton design
   session), since the wiring is trivial once the unit is defined.
4. Layer three, substrate_kb as a live reasoner, after NACE has proven the pattern.

Each step is independently trackable and independently verifiable, the discipline that
made corner-gate an afternoon and kept Coda honest over ten days.
