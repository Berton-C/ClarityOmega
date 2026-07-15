# Adapter Design Document Standard for v08.7.2

**Purpose:** Help builders write adapter design documents that are clear, testable, engine-aligned, and implementation-ready.

**Intended use:** Use this document before writing any new adapter design for Channels A/B/C/D, Corner-Gate, Capability Registry, NACE, Soul Sees Itself, TFS, or other v08.7.2 integration surfaces.

**Core rule:**

> Adapters do not bring verdicts to the engine.  
> Adapters bring condition-bearing material that the engine can classify, block, validate, route, or promote.

**Project axiom:**

> The soul determines.  
> The LLM renders.  
> On every surface.  
> Always.

---

## 1. What a 10/10 Adapter Design Document Must Do

A strong adapter design document must make the adapter workable for a developer without requiring hidden context from the author.

It must answer:

1. What surface is being adapted?
2. What does the adapter observe?
3. What engine vocabulary does it feed?
4. What does it persist across cycles?
5. What does it consume from the engine?
6. What does it render, if anything?
7. What does it explicitly not decide?
8. What negative controls prove it is not overclaiming?
9. What validation ladder proves the design?
10. What would make the adapter unsafe, soul-absent, or misleading?

A 10/10 adapter document is not merely conceptually right. It is implementation-ready.

It should contain enough exactness that a developer can say:

> I know what files to create, what atoms to write, what not to write, what probes to run, and what counts as pass/fail.

---

## 2. The Correct Adapter Frame

Adapters should not say:

```text
This means X.
This proves X.
The system is in state X.
The soul has determined X.
The capability is good.
The user is aligned.
Clarity is in contact.
```

Adapters should say:

```text
I observed X.
This came through surface Y.
This persisted across N cycles.
This changed from A to B.
This suggests candidate C.
This blocker is present.
This evidence supports or opposes C.
This negative control should fail.
This needs harness evidence.
This needs soul routing before durable promotion.
```

The engine decides what the material means. The soul decides what becomes durable. The LLM renders the result in human-facing language.

---

## 3. The Adapter Pipeline

For any adapter, think in this pipeline:

```text
CONTACT
  -> observation
  -> contact surface
  -> trace / state delta

INTERPRETATION
  -> candidate
  -> blocker
  -> pbit support/opposition
  -> context
  -> lineage

VALIDATION
  -> harness evidence
  -> negative control
  -> restart evidence
  -> capability/NACE efficacy evidence

GOVERNANCE
  -> soul routing
  -> approval / hold / rejection
  -> durable canon or archive
```

Every adapter design should explicitly map its data into this pipeline.

If a design document does not clearly show where each datum enters this pipeline, it is not ready for implementation.

---

## 4. Adapter Condition Categories

A design document does not need to use every category, but it must explicitly state which categories it uses, which it defers, and which it must not fabricate.

### 4.1 Observations

An observation is raw contact with something that happened.

Examples:

```text
user said X
tool returned Y
query failed
loop repeated same output
file changed
capability succeeded
capability failed
state delta occurred
corner pattern appeared
runtime emitted warning
```

Observation answers:

```text
What happened?
Where did it happen?
When/cycle?
Through what surface?
```

Adapter thought-form:

```text
I saw this.
```

Not:

```text
This proves X.
```

Design document requirement: each observation must have a mechanical source.

Good:

```text
Observation: command failed
Source: ERROR_FEEDBACK line in runtime output
Cycle: current loop ordinal
Atom written: (example-failure-observed $cycle $command-signature)
```

Weak:

```text
The adapter detects failure.
```

That is not enough.

### 4.2 Contact Surfaces

A contact surface tells the engine what kind of contact the observation came from.

Examples:

```text
user-words
uploaded-file
source-read
tool-result
runtime-output
failed-query
cycle-trace
task-state
loop-delta
self-continuity-score
contradiction-metabolization-trace
morphism-failure
web-corroborated-claim
harness-evidence
patch-proposal
capacity-gap
adapter
reduction
```

Contact surface answers:

```text
What kind of evidence is this?
How close is it to direct contact?
How mediated or weak is it?
```

Adapter thought-form:

```text
This came from this kind of surface.
```

Design document requirement: every adapter must identify its contact surfaces explicitly.

Recommended table:

| Runtime source | Contact surface | Mechanical derivation | Written atom |
|---|---|---|---|
| Human message arrived | user-words | `$msgnew == true` | `(contact-event $cycle user-words)` |
| Command error visible | failed-query | `ERROR_FEEDBACK present` | `(contact-event $cycle failed-query)` |

### 4.3 Traces

A trace is observation across time, not a single event.

Examples:

```text
same failure over 5 cycles
loop-delta shrinking over time
capability succeeds after adapter change
corner signal appears repeatedly
task state changes from blocked -> moving
NACE efficacy increases/decreases
```

Trace answers:

```text
Did this persist?
Did it change?
Is there development, decay, recurrence, or repetition?
```

Adapter thought-form:

```text
This pattern happened across time.
```

Design document requirement: if a design uses trace conditions, it must define:

```text
window depth
cycle ordinal source
record shape
eviction/capping policy
bootstrap behavior
minimum trace needed for the engine reduction
```

Strong trace contract:

```text
Window depth: 3 cycles
Record: (adapter-cycle-record $ord $surface-count $state $next-move $ts)
Cap: keep newest 3 records
Bootstrap: render window-filling until 3 records exist
Trace-present: at least 2 prior records matching this adapter family
```

Weak:

```text
The system watches over time.
```

### 4.4 State Deltas

A state delta is a before/after change.

Examples:

```text
confidence changed
task phase changed
capability status changed
loop behavior changed
candidate moved from pending to validation
failure became resolved
new affordance appeared
```

State delta answers:

```text
What changed?
Was the change meaningful?
Was the change reversible?
Did it reduce or increase ambiguity?
```

Adapter thought-form:

```text
Here is the difference between then and now.
```

Design document requirement: any state delta must define:

```text
previous state source
current state source
comparison rule
symbol emitted
what counts as no-change
```

### 4.5 Candidates

A candidate is a proposed interpretation, growth, capability, fix, pattern, or promotion.

Examples:

```text
this behavior may indicate a corner
this adapter may be capability-ready
this trace may support durable learning
this failed query may expose a capacity gap
this repeated success may support NACE efficacy
this pattern may be eligible for soul routing
```

Candidate answers:

```text
What might this mean?
What might be worth validating?
What could become durable if supported?
```

Adapter thought-form:

```text
This may be X, pending validation.
```

Not:

```text
This is X.
```

Design document requirement: a candidate must be named as a candidate and must include support and blockers.

Good:

```text
Candidate: corner-loop-capture
Support:
  repeated-failing-command
  hidden-error-surface
  trace-present
Blockers:
  no-trace
  narration-only
  no-harness-evidence
```

### 4.6 Blockers

A blocker is a reason something must not be promoted, trusted, executed, or treated as durable yet.

Examples:

```text
blocked-no-observations
blocked-no-trace
blocked-no-harness-evidence
blocked-no-soul-routing
blocked-self-certification
blocked-hand-authored-verdict
blocked-file-survival-not-structural-durability
blocked-governance-not-green
blocked-poetic-only
blocked-LLM-narration-only
blocked-duplicate-head
blocked-import-not-proven
```

Blocker answers:

```text
Why is this not enough?
What condition is missing?
What would make promotion unsafe?
```

Adapter thought-form:

```text
This should not advance because Y is missing.
```

Design document requirement: each adapter should name at least its obvious blockers.

Good:

```text
Blocker: blocked-narration-only
Condition: rendered claim exists but no contact-event and no trace
Result: no promotion, render not-computed or blocked-narration-only
```

### 4.7 Evidence Surfaces

An evidence surface is structured support for a candidate or blocker.

Contact surface says:

```text
Where did this come from?
```

Evidence surface says:

```text
What role does this play in validation?
```

Examples:

```text
trace-supported
harness-supported
soul-routed
restart-supported
runtime-observed
file-persisted
post-restart-queryable
human-confirmed
tool-corroborated
web-corroborated
capability-exercised
adapter-produced
```

Adapter thought-form:

```text
This is the evidence I have for or against the candidate.
```

Design document requirement: each candidate should have an evidence table.

| Candidate | Evidence surface | Source | Strength | Missing evidence |
|---|---|---|---|---|
| corner-loop-capture | trace-supported | cycle records | medium | live fixture |
| adapter-ready | harness-supported | test harness | strong | restart proof |

### 4.8 Harness Evidence

Harness evidence is stronger than ordinary self-report. It comes from an external or semi-external probe of reductions, runtime behavior, files, traces, or restart behavior.

Examples:

```text
static harness pass
live-body runtime pass
production-loop probe pass
negative-control pass
restart revalidation pass
duplicate-head grep result
SHA match
expected atom returned
unexpected empty result
```

Harness evidence answers:

```text
Was this actually tested?
What exactly returned?
Did the negative controls block?
Can it survive restart/reload?
```

Adapter thought-form:

```text
Here is what the probe showed.
```

Design document requirement: every adapter design must define a validation ladder.

Good validation ladder:

```text
static grep or paren-balance checks
pure reduction probes
live-loop probes
negative controls
persistence/window checks
restart/reload checks when durable behavior is claimed
```

### 4.9 Negative Controls

A negative control proves the engine is not merely saying yes.

Examples:

```text
governance-open -> hold-governance-not-green
file-survival + durable-growth-claimed -> blocked-file-survival-not-structural-durability
preloaded-verdict-only -> blocked-hand-authored-verdict
observations-absent + derived-verdict-present -> blocked-no-observations
self-certified-change -> blocked-self-certification
```

Negative control answers:

```text
Does the system block the wrong thing?
Can it distinguish evidence from assertion?
```

Adapter thought-form:

```text
This should fail, and it did.
```

This is extremely important. A surface that only submits positive evidence is weaker than a surface that also submits a negative control.

Design document requirement: each adapter design should include at least three negative controls:

1. No observation / no contact.
2. Narration-only or self-certification.
3. Missing trace or missing harness evidence.

### 4.10 Capability Signals

Capability signals are especially relevant to NACE and the Capability Registry.

Examples:

```text
capability-invoked
capability-succeeded
capability-failed
capability-partial
capability-cost-high
capability-latency-high
capability-output-invalid
capability-output-useful
capability-needs-human
capability-safe-to-repeat
capability-unsafe-to-repeat
```

Capability signal answers:

```text
Can this capability actually do what it claims?
Under what conditions?
At what cost?
With what reliability?
```

Adapter thought-form:

```text
This capability behaved this way in this context.
```

Design document requirement: any adapter that touches tools, skills, actions, capabilities, or registry dispatch must define capability signals.

### 4.11 Efficacy / NACE Belief Updates

NACE should not receive:

```text
This capability is good.
```

NACE should receive efficacy evidence.

Examples:

```text
capability X succeeded in context Y
capability X failed in context Y
confidence increased/decreased
support/opposition pbit changed
capability transferred across context
capability failed across context
capability required repair
```

NACE answers:

```text
What should the system believe about this capability's usefulness?
Where does it work?
Where does it not work?
How confident are we?
```

Adapter thought-form:

```text
This changes capability efficacy belief by this amount, with this evidence.
```

Design document requirement: if the adapter updates NACE, it must specify:

```text
capability id
context
observed result
pbit/support update
confidence basis
decay or maintenance rule
negative evidence
```

### 4.12 P-bit Support / Opposition

v08.7.2 is Hyperseed-aware, so adapters can bring graded evidence rather than binary claims.

Example:

```metta
(mk-pbit 0.8 0.7)
```

Meaning roughly:

```text
support/strength: 0.8
confidence: 0.7
```

Useful when an adapter wants to say:

```text
strong but uncertain
weak but reliable
conflicted
emerging
decaying
```

Adapter thought-form:

```text
This evidence has this degree of support and this degree of confidence.
```

Design document requirement: when a pbit is used, define what the two numbers mean for that adapter.

Also define:

```text
how support is computed
how confidence is computed
how values decay
how conflicting evidence combines
which canonical q-operators are used
```

### 4.13 Context

A condition is almost meaningless without context.

Examples:

```text
which channel
which user/task
which cycle
which capability
which file
which runtime mode
which adapter
which prior state
which environment
which version
```

Context answers:

```text
Where is this true?
For whom?
Under what conditions?
Does it transfer?
```

Adapter thought-form:

```text
This is true in this context, not universally.
```

Design document requirement: every adapter record should carry enough context to avoid false generalization.

Minimum context:

```text
cycle id
surface/source
adapter name/version
runtime mode
related task/capability if applicable
```

### 4.14 Lineage

Lineage tells the engine where a candidate came from.

Examples:

```text
from user request
from failed query
from harness result
from Corner-Gate signal
from NACE efficacy update
from Capability Registry dispatch
from runtime trace
from previous candidate
from patch proposal
from restart validation
```

Lineage answers:

```text
What produced this?
Can we trace it back?
Is it hand-authored, observed, derived, or tested?
```

Adapter thought-form:

```text
This candidate came from this chain of evidence.
```

Design document requirement: any candidate, patch proposal, or durable promotion path must include lineage.

### 4.15 Resource / Maintenance Cost

v08.7.2 should care not only whether something works, but what it costs to keep alive.

Examples:

```text
high token cost
high runtime cost
high human attention cost
fragile import path
complex adapter dependency
restart-sensitive
requires external service
requires manual confirmation
```

Cost answers:

```text
Is this durable enough to maintain?
Is it worth promoting?
Does it increase fragility?
```

Adapter thought-form:

```text
This works, but costs this much to maintain.
```

Design document requirement: if an adapter adds runtime work, external calls, persistence, or rendering, it should state the maintenance cost.

Examples:

```text
one line rendered every cycle
one cycle-record atom per cycle, capped at 3
no external calls
no LLM calls
no unbounded growth
```

### 4.16 Restart / Durability Evidence

For durable governance, a thing is not really durable just because it happened once.

Examples:

```text
persisted to file
imported at startup
queryable after restart
same reduction after reload
state restored correctly
candidate survived restart
bad candidate did not become canon
```

Durability answers:

```text
Did it survive reload?
Is it boot-safe?
Is it queryable after restart?
```

Adapter thought-form:

```text
This persisted and remained functional after restart.
```

Design document requirement: if the adapter claims durability, it must include restart evidence.

If it only claims runtime legibility, it should explicitly say:

```text
This is runtime trace state, not durable canon.
```

### 4.17 Soul-Routing Conditions

Anything that wants to become durable canon needs soul routing.

Examples:

```text
soul-approved
soul-routed
soul-blocked
soul-pause
soul-flag
governance-green
governance-open
human-approval-present
authorized-approver-present
```

Soul routing answers:

```text
Is this allowed to become part of durable identity/governance?
Did the sovereign layer determine it, or did the LLM merely narrate it?
```

Adapter thought-form:

```text
This is ready for soul review / blocked by soul / approved by soul.
```

Design document requirement: each adapter should state whether its outputs are:

```text
runtime-only
candidate-for-soul-routing
validation evidence
durable-canon candidate
```

Do not blur these.

### 4.18 Patch / Adapter Proposals

Adapters can submit proposed changes, not just observations.

Examples:

```text
new adapter proposed
capability registry entry proposed
Corner-Gate v3 route proposed
Channel B evidence mapping proposed
NACE update rule proposed
duplicate-head cleanup proposed
```

Patch proposal answers:

```text
What should change?
Why?
What evidence supports it?
What could break?
What validates it?
```

Adapter thought-form:

```text
This is a proposed change, not an installed truth.
```

Design document requirement: every patch proposal must include:

```text
change target
motivation
evidence
expected behavior
rollback plan
validation plan
negative controls
```

### 4.19 Rejection / Archive Reasons

A mature adapter should also know how to submit why something failed or was rejected.

Examples:

```text
rejected-no-trace
rejected-harness-fail
rejected-duplicate-owner
rejected-self-certification
rejected-poetic-only
rejected-unmaintainable
rejected-no-restart-proof
```

Rejection answers:

```text
Why did this not become durable?
Can future systems learn from the failed candidate?
```

Adapter thought-form:

```text
This failed for this reason; preserve the lesson without promoting the claim.
```

Design document requirement: the adapter should define success states, failure states, and archive reasons.

---

## 5. Required Sections for a 10/10 Adapter Design Document

Use this as the standard structure.

### Section 0: Metadata

Include:

```text
title
version
date
branch
status
author / reviewer
scope
non-scope
engine version
related builds
source documents
known assumptions
```

### Section 1: Executive Boundary

Explain the adapter in one paragraph:

```text
This adapter observes X, feeds Y to the engine, persists Z across cycles, consumes A from the engine, and renders B. It does not decide C.
```

Required phrase:

```text
The engine is not modified, subsetted, or second-guessed.
```

If the adapter modifies the engine, it is not merely an adapter and should be documented as an engine patch.

### Section 2: Architecture

Describe:

```text
what surface is being adapted
why the adapter exists
what failure mode it replaces
how it works with v08.7.2
how it works with SSI/TFS if relevant
how it avoids self-certification
how it avoids verdict-smuggling
```

Must include:

```text
Adapters bring structured contact and evidence.
The engine decides what it means.
The soul decides what becomes durable.
The LLM only renders.
```

### Section 3: Input Contract

For every input, define:

```text
runtime event/source
engine vocabulary
condition category
mechanical derivation
atom shape
status: MECH / TRACE / STEP0 / DECIDE / DEFERRED
what is not written
```

Recommended table:

| Runtime event | Engine symbol | Category | Derivation | Atom shape | Status |
|---|---|---|---|---|---|

Status definitions:

```text
MECH: mechanically derivable now
TRACE: requires prior cycle/window atoms
STEP0: exact signature/arity must be quoted before code
DECIDE: needs Berton/design ruling
DEFERRED: intentionally not part of v1
```

Hard rule:

> A classifier whose inputs cannot be mechanically produced must not be fed fabricated symbols.

Render or record `not-computed` rather than inventing a condition.

### Section 4: Persistence Contract

Define every atom the adapter writes.

For each atom:

```text
atom shape
field meanings
field source
cardinality
lifetime
cap/eviction rule
bootstrap behavior
writer function
reader function
whether it is runtime trace or durable canon
```

Never use a tuple field without defining it.

### Section 5: Engine Consumption Contract

Explain what engine reductions the adapter expects to call or feed.

For each reduction:

```text
function name
exact arity
input symbols
which adapter atoms feed it
expected outputs
positive case
negative case
not-computed case
```

If exact arity is not known, mark it STEP0 and do not code yet.

Hard rule:

> No writer code before exact signatures and arities are locked.

### Section 6: Output / Rendering Contract

Define:

```text
what routed atoms exist
what line, if any, is rendered
where it appears
when it appears
what vocabulary is used
what is rendered when fields are missing
what must never be rendered
```

Healthy states should render too if the line is intended as navigation.

A line that appears only during trouble becomes an alarm. Alarm behavior can recreate the old gate failure.

### Section 7: Capability Registry / NACE Contract

If the adapter touches capabilities, define:

```text
capability id
registry entry shape
when invoked
success signal
failure signal
partial signal
cost signal
latency signal
safety/repeatability signal
NACE efficacy update
pbit update rule
negative evidence rule
```

Do not send NACE a verdict. Send efficacy evidence.

### Section 8: Soul / Governance Contract

State explicitly whether outputs are:

```text
runtime-only
validation evidence
candidate for soul routing
durable canon candidate
rejected/archive-only
```

Define what requires:

```text
soul-routed
soul-approved
governance-green
human approval
authorized approver
restart proof
```

Also define what must be blocked:

```text
self-certification
hand-authored verdict
poetic-only claim
no-observation claim
no-trace claim
no-harness claim
```

### Section 9: Negative Controls

Must include positive and negative tests.

At minimum:

```text
positive path
no-contact path
narration-only path
missing-trace path
missing-harness path
self-certification path
healthy/no-alarm path
```

Recommended table:

| Test | Input fixture | Expected reduction | Why it matters |
|---|---|---|---|

A 10/10 design proves the adapter can say no.

### Section 10: Validation Ladder

Define validation in tiers:

```text
D0 static checks
D1 file/import checks
D2 pure reduction probes
D3 live-body probes
D4 production-loop probes
D5 persistence/window checks
D6 negative controls
D7 restart/reload checks
D8 observation period metrics
```

Each tier should include:

```text
command or probe
expected result
pass/fail/hold criteria
raw output capture path
rollback if failed
```

### Section 11: Operations / Patch Plan

Define implementation sequence:

```text
one change at a time
dry-run first
reversible apply scripts
backup path
OLD/NEW anchors
paren balance
post-write verification
import order check
artifact manifest update
rollback command
```

A 10/10 design is operationally boring.

### Section 12: Success Metrics

Define measurable outcomes.

Examples:

```text
zero unreduced echoes
zero fabricated fields
line renders every cycle
negative controls block
window atoms capped
production-loop probe returns expected atom
no duplicate-head greps
no hidden hold strings
no sustained reasoning-about-the-line instead of using it
```

Avoid vague success criteria.

### Section 13: Known Risks and Soul-Absent Failure Modes

List how the design can become technically correct but soul-absent.

Examples:

```text
rendered line functions as command rather than information
adapter fabricates classifier inputs
adapter smuggles verdicts as observations
LLM narration treated as evidence
healthy states do not render, making the line an alarm
negative controls omitted
state grows unbounded
duplicate operator heads introduced
import order not proven
```

### Section 14: Decisions for Markup

List unresolved decisions.

Each decision should include:

```text
decision id
question
options
recommended default
impact
deadline/gate
```

### Section 15: Deferred / Out of Scope

Name deferred work clearly.

Deferred means:

```text
recorded, bounded, and not silently implemented
```

---

## 6. The 10/10 Adapter Design Rubric

Score each category from 0 to 5.

| Category | 5 means | 0 means |
|---|---|---|
| Boundary clarity | adapter / engine / soul / LLM responsibilities are unmistakable | adapter makes verdicts or modifies engine without saying so |
| Input fidelity | all inputs have mechanical derivations and no fabricated classifier symbols | inputs are impressionistic or self-reported |
| Engine vocabulary alignment | all engine symbols, signatures, and arities are exact | symbol names are guessed |
| Persistence shape | all atoms have fields, lifetimes, caps, writers, readers, and bootstrap behavior | state is vaguely described |
| Negative controls | multiple negative controls are explicit and required | only success path is tested |
| Validation ladder | static, pure, live, production, persistence, negative, and restart tests are defined | says “test it” |
| Soul/governance discipline | runtime trace, validation evidence, soul routing, and durable canon are clearly separated | runtime output is treated as durable truth |
| NACE / Capability Registry alignment | capability signals and efficacy updates are evidence-based, contextual, and graded | capabilities are labeled good/bad without evidence |
| Operational reversibility | apply sequence, dry-run, backup, verification, and rollback are defined | implementation is hand-edit-only |
| Failure mode honesty | the document names how the adapter can become misleading, soul-absent, or unsafe | no risk section |

Interpretation:

```text
45-50: implementation-ready / 10 out of 10
38-44: strong design, Step 0 hardening needed
30-37: conceptually useful but not implementation-ready
below 30: rewrite before coding
```

---

## 7. Design Document Quality Gates

A design document is not implementation-ready until all hard gates pass.

### Gate A: No Verdict Smuggling

Check:

```text
Does any writer write a state/verdict it did not mechanically observe?
Does any field imply approval, contact, learning, or readiness without evidence?
```

Pass condition:

```text
all such claims are candidates, blockers, or not-computed
```

### Gate B: Exact Signature Lock

Check:

```text
Are all engine reductions named with exact arity and expected outputs?
```

Pass condition:

```text
no STEP0 signatures remain before writer code
```

### Gate C: Mechanical Derivation

Check:

```text
Can a developer point to where every input comes from in runtime logs, files, traces, or tool outputs?
```

Pass condition:

```text
no impressionistic or LLM-only input fields
```

### Gate D: Negative Controls

Check:

```text
Does the design prove the adapter blocks wrong claims?
```

Pass condition:

```text
at least three negative controls are defined
```

### Gate E: Persistence Discipline

Check:

```text
Are atoms bounded, bootstrapped, and typed by role?
```

Pass condition:

```text
no unbounded runtime accumulation unless explicitly justified
```

### Gate F: Production Surface Proof

Check:

```text
Does the validation path include live production-loop proof if production behavior is claimed?
```

Pass condition:

```text
production-loop probe defined with exact expected result
```

### Gate G: Soul/Governance Boundary

Check:

```text
Does the adapter ever treat runtime evidence as durable canon?
```

Pass condition:

```text
durable promotion requires soul-routing/governance conditions
```

---

## 8. Template for a 10/10 Adapter Design Document

Use this skeleton.

```markdown
# <Adapter Name> Design: Feeding v08.7.2 Whole

**Version:**  
**Date:**  
**Branch:**  
**Status:**  
**Scope:**  
**Non-scope:**  
**Engine version:**  
**Related builds:**  
**Sources:**  

---

## 1. Boundary

This adapter observes <X>, feeds <Y> to the engine, persists <Z>, consumes <A>, and renders <B>. It does not decide <C>.

The engine is not modified, subsetted, or second-guessed.

Adapters bring structured contact and evidence. The engine decides what it means. The soul decides what becomes durable. The LLM only renders.

---

## 2. Architecture

<Describe the surface, failure mode, replacement behavior, and integration shape.>

---

## 3. Input Contract

| Runtime event | Engine symbol | Category | Mechanical derivation | Atom shape | Status |
|---|---|---|---|---|---|

Unfed-classifier rule:

A classifier whose inputs cannot be mechanically produced is not fed fabricated symbols. Its result is not-computed.

---

## 4. Persistence Contract

| Atom | Fields | Cardinality | Lifetime | Writer | Reader | Runtime/durable status |
|---|---|---|---|---|---|

---

## 5. Engine Consumption Contract

| Engine reduction | Exact arity | Inputs | Source atoms | Expected outputs | Negative case |
|---|---|---|---|---|---|

---

## 6. Output / Rendering Contract

Routed atoms:

Rendered line:

Missing-field behavior:

Forbidden renderings:

---

## 7. Capability Registry / NACE Contract

Capability signals:

Efficacy updates:

P-bit rule:

Negative evidence:

---

## 8. Soul / Governance Contract

Runtime-only:

Validation evidence:

Soul-routed candidates:

Durable-canon candidates:

Blocked states:

---

## 9. Negative Controls

| Test | Fixture/input | Expected result | Why it matters |
|---|---|---|---|

---

## 10. Validation Ladder

| Tier | Probe/command | Expected result | Pass/fail/hold | Evidence path |
|---|---|---|---|---|

---

## 11. Operations

Patch sequence:

Dry-run:

Apply:

Verify:

Rollback:

---

## 12. Success Metrics

<Measurable outcomes.>

---

## 13. Risks / Soul-Absent Failure Modes

<How this can be technically correct but wrong.>

---

## 14. Decisions for Markup

| ID | Question | Options | Recommendation | Gate |
|---|---|---|---|---|

---

## 15. Deferred / Out of Scope

<Recorded deferred items.>
```

---

## 9. Applying the Standard to Corner-Gate v3

The Corner-Gate v3 document is strong because it already does many things in this standard:

```text
adapter boundary is explicit
writers are mechanical observation only
unfed-classifier rule is present
engine is not modified
trace persistence is defined
rendering is routed and visible
validation ladder exists
success metrics exist
decisions are listed
deferred work is named
```

To move it from strong draft to 10/10 implementation-ready, it should add or strengthen:

```text
exact arities for all STEP0 functions
canonical quantale ownership note
explicit next-move/lineage fields in the cycle record
explicit negative-control table
adapter condition ledger mapping feeds to categories
clear wording that v3 does not imperatively hold/block/release, while the engine may compute blockers
```

That is the difference between a good architecture document and a build-ready one.

---

## 10. The Deep Rule

Every adapter document should protect this boundary:

```text
observation is not interpretation
interpretation is not validation
validation is not soul approval
soul approval is not LLM narration
LLM narration is not durable canon
```

A 10/10 adapter design never collapses these layers.

It lets each layer do its own work.

---

## 11. Very Short Checklist

Before handing an adapter design to a developer, ask:

```text
1. Are all observations mechanically sourced?
2. Are contact surfaces named?
3. Are traces/window rules defined?
4. Are state deltas defined?
5. Are candidates labeled as candidates, not truths?
6. Are blockers explicit?
7. Are evidence surfaces mapped?
8. Is harness evidence required?
9. Are negative controls included?
10. Are capability/NACE signals evidence-based?
11. Are pbits defined if used?
12. Is context included?
13. Is lineage included?
14. Is cost bounded?
15. Is restart/durability evidence separated from runtime trace?
16. Is soul routing required for durable promotion?
17. Are patch proposals reversible?
18. Are rejection/archive reasons defined?
19. Are exact engine signatures locked?
20. Can a developer implement this without guessing?
```

If the answer to #20 is no, the document is not 10/10 yet.
