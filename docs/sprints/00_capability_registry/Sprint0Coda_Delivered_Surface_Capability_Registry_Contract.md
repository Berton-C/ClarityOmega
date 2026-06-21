# Sprint 0-Coda Delivered Surface: The Capability Registry Contract

**Purpose:** The definitive specification of what Sprint 0-Coda delivered. This is a
CONTRACT document. Downstream sprints (Capability Registry Sprint 1+, Task State
sprints, NACE, the soul-state-producer, any future capability author) code against
exactly what is written here. If a downstream design contradicts this document, the
downstream design is wrong unless this document is formally revised first.
**Authority:** Every claim below is quoted or paraphrased from the deployed source as
of commit `38737ac`: `soul/capability_registry.metta` (the promoted Path C dispatcher
with the per-cycle sweep), `soul/capabilities/skill_discovery.metta` (the first
production capability and the getContext accessor), and the getContext integration in
`src/loop.metta`. Companion: `ADR-006` (registry decision), `ADR-007` (substrate
externalized control flow), `artifact_0_loop_extension_contract.md` (the disciplines),
`artifact_1` (the wiring diagram).
**Status of the surface:** Live in production. Verified by exercise (phase_d,
live_path, anchor_fallback). Six-of-six dispatch-atom sweep patterns proven.

---

## 0. What Sprint 0-Coda delivered, in one paragraph

A live, substrate-resident capability dispatcher. Capabilities are registered as data
atoms, not code. Each cycle the loop fires `dispatch` with an input atom; the dispatcher
matches registered capabilities by schema, runs them through an extensible filter
pipeline, sorts the survivors by priority, and runs the chain until a handler anchors a
decision or the chain exhausts. Dispatch writes transient record atoms describing what
happened, which are swept clean each cycle so they do not accumulate. The first
production capability, `skill-discovery`, sources the SKILLS block of the prompt. The
whole thing is dispatched live from `getContext` via a single named accessor. This is
the surface every future capability plugs into.

---

## 1. The two extension points (the whole point of the surface)

The registry is designed to be extended in exactly two ways, both by adding data atoms,
neither by editing registry code. This is the load-bearing design property. If you find
yourself editing `capability_registry.metta` to add a capability or a new eligibility
dimension, stop: the surface is built so you should not have to.

**Extension point 1: register a capability (handler registration).** Add one
`(registered-capability ...)` atom and define its handler function. The dispatcher picks
it up by `match`. This is how every new capability enters the system.

**Extension point 2: register a filter step (eligibility-dimension registration).** Add
one `(capability-filter-step order: $n step: $fn)` atom and define the step function.
The pipeline picks it up by `match` and `msort`. This is how a new eligibility dimension
(trust, scope, cost, soul-Safety) is added without touching `resolve-and-filter-entries`
or any other registry code.

Both are detailed below with their exact schemas.

---

## 2. Registering a capability (extension point 1)

### 2.1 The canonical registration schema (LOAD-BEARING INVARIANT)

```
(registered-capability
   schema:    <input-atom-pattern>
   handler:   <handler-symbol>
   priority:  <number>
   lifecycle: <lifecycle-symbol>      ;; e.g. active
   metadata:  <atom>)                 ;; e.g. () or provenance/version data
```

`registered-capability` is FIVE fields. This is an invariant, quoted from the
dispatcher source: "Every consumer that matches registered-capability MUST use this
5-field shape. A 4-field matcher silently fails to couple (structural match is exact in
MeTTa: no error, no warning, just an empty match and a silent fallback). Any future
consumer that deviates from this arity is a defect by definition."

Consequence for downstream sprints: when you read `registered-capability` atoms (e.g. a
Sprint 1 capability that enumerates capabilities, or a Task State capability that
inspects the registry), you MUST match all five fields. A four-field match returns empty
and you will silently get a fallback with no error. This is the single most common way to
mis-couple to this surface. The `metadata` field exists precisely so the shape is stable
while annotations evolve; put your extensible data there, do not add or drop fields.

### 2.2 The handler contract

The handler is a function `(= (<handler-symbol> $input-atom) <result>)`. Contract:

- It receives the dispatched input atom.
- It returns a result atom. The result is written verbatim into a `dispatch-result`
  atom by run-chain (see Section 4), so the result shape is the handler's public output
  contract; downstream consumers read it from `dispatch-result`.
- If it returns the symbol `decision-anchor`, the chain STOPS at this handler (it
  anchors the decision). Any other return value lets the chain continue to the next
  candidate. This is the only control signal a handler has over the chain.
- A handler MAY be read-only (write no atoms), as `skill-discovery` is. A handler that
  writes atoms is permitted but those writes are the handler's responsibility, not the
  registry's, and are NOT swept by the dispatch sweep (Section 6).

### 2.3 The worked example: skill-discovery (the delivered first capability)

```
(eligible-lifecycle active)                          ;; eligibility seed, see 3.2

(registered-capability
   schema: (skill-request cycle: $k)
   handler: skill-discovery
   priority: 100
   lifecycle: active
   metadata: ())

(= (skill-discovery $request)
   (let* (($capabilities (collapse (match &self
                                          (registered-capability
                                            schema: $s handler: $h priority: $p
                                            lifecycle: active metadata: $m)
                                          ($s $h $p $m))))
          ($formatted (format-skill-set $capabilities)))
         (skill-set skills: $formatted)))
```

Note the schema `(skill-request cycle: $k)` carries a variable `$k`. Dispatch matches a
concrete input like `(skill-request cycle: 7)` against this by unification: `$k` binds 7.
This is how a single registration serves every cycle. Capabilities whose input varies per
call use this variable-in-schema pattern.

---

## 3. How dispatch works (the runtime the surface exposes)

### 3.1 The dispatch call

```
(dispatch <input-atom> <invocation-id>)
```

`invocation-id` is any value that distinguishes this dispatch from others in the same
process lifetime. The loop uses the cycle counter `$k` (monotonic, distinct per cycle,
no counter atom needed). It is the key under which this dispatch's record atoms are
written and read. If you call dispatch yourself, supply an id you can read back by.

### 3.2 The dispatch pipeline, in order (from source)

1. `sweep-dispatch-atoms!` runs first, clearing the PRIOR invocation's transient record
   atoms (Section 6).
2. `(dispatch-invocation invocation-id: input-atom:)` is written.
3. `match` finds every `(registered-capability schema: <input> ...)` whose schema unifies
   with the input atom, producing raw candidate entries.
4. `resolve-and-filter-entries` runs each candidate through the filter pipeline (Section 5).
5. If NO candidate survives, the fallback branch writes
   `(dispatch-fallback-activated invocation-id: input-atom: reason:)` and dispatch ends.
   The `reason` is a load-bearing two-value vocabulary, see 3.3.
6. If candidates survive, they are sorted by priority (`msort`) and `run-chain` runs them
   in order (Section 4).

### 3.3 The fallback reason vocabulary (LOAD-BEARING INVARIANT)

When dispatch falls back, `reason` is exactly one of two symbols, and they demand
OPPOSITE responses. Quoted from source:

- `reason: no-matching-capability` — nothing matched the schema. The agent genuinely
  lacks a capability for this input. Correct response: acquire a capability.
- `reason: all-candidates-filtered` — capabilities matched but every one was filtered out
  (ineligible lifecycle, low efficacy, a block step). The agent HAS a capability; it was
  suppressed. Correct response: investigate the filter. Do NOT acquire a duplicate.

The source is explicit that this is a Safety-adjacent distinction: "Every reader of
dispatch-fallback-activated MUST branch on both reasons." Conflating them steers the
agent toward wrong remediation and compounds in the capability-management loop.
(Sprint 1 will enrich `all-candidates-filtered` with WHICH filter step dropped each
candidate; the plumbing for that already exists in the filter steps' `filtered-out`
returns.)

---

## 4. run-chain and the result contract

run-chain runs the sorted candidates in order. For each candidate it:

1. Writes `(capability-invoked invocation-id: handler: input-atom:)`.
2. Calls `(handler input-atom)` to get `$result`.
3. Writes `(dispatch-result invocation-id: result: handler:)` — ALWAYS, before any anchor
   decision. This is the atom downstream consumers read to get a capability's output.
4. If `$result` is `decision-anchor`, writes `(dispatch-chain-anchored invocation-id:
   anchor-handler:)` and STOPS. Otherwise recurses to the next candidate.
5. If the chain runs out of candidates, writes `(dispatch-chain-exhausted invocation-id:)`.

So after a dispatch, exactly one of these end-states exists for that invocation-id: an
anchored result, an exhausted chain, or a fallback. And for every handler that ran, a
`dispatch-result` exists carrying its output.

**The result-reading contract for downstream consumers.** To get a capability's output,
match `dispatch-result` by your invocation-id and the result shape you expect:

```
(match &self
   (dispatch-result invocation-id: <your-id> result: <your-result-pattern> handler: $h)
   <projection>)
```

This is exactly how the skills accessor reads skill-discovery's output (Section 7). A
consumer must read within the same cycle it dispatched, because the sweep clears the
result at the top of the next dispatch (Section 6).

---

## 5. The filter pipeline (extension point 2)

### 5.1 What it is

Each candidate is carried through registered filter steps as a `pipeline-entry`:

```
(pipeline-entry handler: $h lifecycle: $l priority: $p efficacy: $e)
```

Accessors (`pe-handler`, `pe-lifecycle`, `pe-priority`, `pe-efficacy`) and single-field
constructors (`pe-with-lifecycle`, `pe-with-priority`, `pe-with-efficacy`) are provided.

### 5.2 The step contract

A filter step is a function `(= (<step-fn> $entry) <result>)` where the result is either a
`pipeline-entry` (possibly enriched) or the symbol `filtered-out`. If any step returns
`filtered-out`, the candidate is dropped from the chain. Steps run in ascending `order`.

### 5.3 Registering a new step (the second extension point)

```
(capability-filter-step order: <n> step: <step-fn>)
(= (<step-fn> $entry) ...)   ;; returns enriched pipeline-entry, or filtered-out
```

That is all. `apply-filter-pipeline` discovers steps by `match`, sorts them by `order`
via `msort`, and walks them. No change to `resolve-and-filter-entries` or any registry
code is needed. This is the designed path for adding trust, scope, cost, or
soul-Safety eligibility dimensions.

### 5.4 The three delivered steps (seeded)

```
(capability-filter-step order: 10 step: lifecycle-filter-step)   ;; resolve + eligibility gate
(capability-filter-step order: 20 step: priority-filter-step)    ;; resolve priority (enrich only)
(capability-filter-step order: 30 step: efficacy-filter-step)    ;; resolve + efficacy gate (>= 0.3)
```

- `lifecycle-filter-step` resolves the candidate's lifecycle and gates on `eligible?`,
  which is True iff an `(eligible-lifecycle <l>)` atom exists. The seed
  `(eligible-lifecycle active)` lives in `skill_discovery.metta`; without an
  `eligible-lifecycle` atom for a candidate's lifecycle, it is filtered out. (This is the
  single most common reason a newly registered capability silently never runs: its
  lifecycle is not seeded as eligible.)
- `priority-filter-step` resolves priority and enriches; it never filters.
- `efficacy-filter-step` resolves efficacy (default 1.0 when no efficacy data) and gates
  at `>= 0.3`.

### 5.5 The observation-override model (how learning will steer dispatch)

`resolve-lifecycle`, `resolve-priority`, `resolve-efficacy` each check for an observation
atom and prefer it over the registered value:

```
(capability-lifecycle-observation handler: $h lifecycle: $observed)
(capability-priority-observation  handler: $h priority:  $observed)
(capability-efficacy-observation  handler: $h efficacy:  $observed)
```

If an observation atom exists for a handler, its value overrides the registered value in
the pipeline. This is the seam by which a learning system (NACE) steers dispatch WITHOUT
editing registrations: write an observation atom, and the next dispatch resolves to it.
Downstream sprints that want to influence dispatch eligibility dynamically write these
observation atoms; they do not mutate `registered-capability`. NOTE: as of delivery,
nothing writes these observation atoms; that is NACE's job (see its plan). They are the
designed interface for it.

---

## 6. The retention contract (what persists, what does not)

`sweep-dispatch-atoms!` runs at the TOP of every `dispatch`, before any write. It removes
all six transient record-atom families by variable pattern (remove-all, self-healing):
`dispatch-invocation`, `capability-invoked`, `dispatch-result`, `dispatch-chain-exhausted`,
`dispatch-chain-anchored`, `dispatch-fallback-activated`.

**Contract consequence, critical for downstream consumers:** the record atoms from
invocation k live only from `dispatch(k)` until the top of `dispatch(k+1)`. They are
TRANSIENT. A consumer that needs a dispatch result, fallback reason, or anchor MUST read
it within the same cycle the dispatch occurred. Do NOT design a consumer that expects to
read a prior cycle's dispatch records; they are gone.

**What is NOT swept, and is therefore safe to treat as durable within the process:**
everything that is not one of those six families. Specifically: `registered-capability`,
`capability-filter-step`, `eligible-lifecycle`, the three `capability-*-observation`
atoms, and anything a handler writes on its own. The sweep is surgical to the six
transient families. Clarity confirmed this boundary. If a future capability needs durable
cross-cycle dispatch state, it must write a NON-dispatch-* atom (or a file), because
anything matching the six swept shapes will be cleared.

**Why the sweep exists:** `add-atom` is not idempotent; without the sweep the six families
accumulate unbounded across the process lifetime. The sweep bounds them to one cycle's
worth. A restart clears all of them regardless (runtime atomspace is not persisted).

---

## 7. The live integration: how the loop uses the surface today

getContext in `src/loop.metta` sources the SKILLS block through one named accessor
(Artifact 0 Discipline 1):

```
(let* (($skills-str (dispatch-skills $k))
       ($skills-len (size-atom $skills-str))
       ($_marker   (println! (DIAG-CYCLE-DISPATCH invocation-id: $k skills-len: $skills-len))))
   ... " SKILLS: " $skills-str ...)
```

`dispatch-skills` (in `skill_discovery.metta`) is the canonical example of a consumer
using this surface end to end:

```
(= (dispatch-skills $k)
   (let $_ (dispatch (skill-request cycle: $k) $k)        ;; fire dispatch this cycle
        (first-skill-or-default                            ;; read THIS cycle's result, with fallback
          (collapse (match &self
                          (dispatch-result invocation-id: $k
                                           result: (skill-set skills: $s) handler: $_h)
                          $s)))))
```

It dispatches, then reads `dispatch-result` for this cycle, and falls back to `(getSkills)`
if the read is empty so a dispatch miss can NEVER crash prompt assembly. Two things every
consumer should copy from this:

1. Dispatch and read in the same cycle, keyed by the same invocation-id.
2. Always have a fallback for the empty read, so the consumer cannot fail the loop.

`size-atom` (not `string_length`) is used on the skills value because the value is a
compound list; a scalar string op throws on a compound per the Atom Operations Map
read-instrument rule. Any consumer measuring a compound result must use `size-atom`.

### 7.1 Option (a) vs Option (b): the current content state

The surface is fully live, but the CONTENT skill-discovery emits is still the legacy
hardcoded list: `(= (format-skill-set $capabilities) (getSkills))`. This is "Option (a)":
the dispatch path is the source, but the bytes equal the old `getSkills` output
(skills-len 21), so the prompt the LLM sees is unchanged. This was deliberate, to wire and
verify the surface without changing model-facing content in the same step.

"Option (b)", which is Sprint 1's job: replace `format-skill-set`'s body with real
`(registered-capability ...)` formatting (context-filtered), and retire `getSkills` after
a parity check. Until then, capabilities registered for content purposes will not change
the SKILLS block, because `format-skill-set` ignores its `$capabilities` argument and
returns `getSkills`. Sprint 1 changes that one function body. THIS is the line where the
registry's value becomes model-visible.

---

## 8. Known limitations delivered with the surface (do not rediscover)

- **Criterion 5 (the catch limitation).** `catch` absorbs exceptions from direct Prolog
  predicate calls, but silently fails to catch when wrapping a `reduce/2`-mediated
  indirect invocation, which is the only pattern available since handler symbols must be
  data. Net: a handler that throws via the indirect path is not reliably caught by the
  dispatcher. A cooperative handler should return an error value rather than throw; an
  uncooperative one needs a PeTTa-runtime change. This is a documented limitation, not a
  bug to fix mid-sprint.
- **Boundary 1 (the Safety-tier deficit).** The registry can `match` only atomspace atoms.
  The soul's governance verdict is NOT an atom (it is `change-state!` prompt-space state),
  so the registry CANNOT read soul Safety state today. Consequence, and this is a hard
  gate from the Coda design: no governance-deciding capability may register until the
  soul-state-producer work-package closes Boundary 1. skill-discovery is tolerable because
  it is informational and makes no governance decision. A dispatch-guard that gates
  invocations on soul Safety is DESIGN-blocked on this. (See the soul-state-producer
  handoff.)
- **Filter-drop attribution is coarse.** Today `all-candidates-filtered` does not say
  which step dropped which candidate. The `filtered-out` returns carry the information;
  surfacing it is Sprint 1 work.

---

## 9. The arity / shape invariants, collected (the defect-by-definition list)

A single reference list of the structural contracts. Violating any of these produces a
silent empty match and a fallback, with no error, which is the hardest class of bug on
this surface. Quoted or derived from source:

1. `registered-capability` is exactly 5 fields: schema, handler, priority, lifecycle,
   metadata. Match all five.
2. `dispatch-result` is exactly 3 fields: invocation-id, result, handler. Read all three.
3. `capability-invoked` is 3 fields: invocation-id, handler, input-atom.
4. `dispatch-fallback-activated` is 3 fields: invocation-id, input-atom, reason. Branch on
   both reason values.
5. `dispatch-chain-anchored` is 2 fields: invocation-id, anchor-handler.
6. `dispatch-chain-exhausted` and `dispatch-invocation` carry invocation-id (+ input-atom
   for the latter).
7. `capability-filter-step` is 2 fields: order, step.
8. `pipeline-entry` is 4 fields: handler, lifecycle, priority, efficacy.
9. The three observation atoms are 2 fields each (handler + the observed value).
10. A handler returning `decision-anchor` stops the chain; any other value continues it.

If you write a matcher or a writer for any of these, match the field count and field
labels exactly. There is no arity error in MeTTa; a wrong shape just does not couple.

---

## 10. How specific downstream sprints use this surface

### 10.1 Capability Registry Sprint 1 (Category O + B5 + P1)

Sprint 1 is the capability-authoring expansion. Against this surface it will, at minimum:
register individual skills as `(registered-capability ...)` atoms (extension point 1,
using `metadata` for per-skill annotation); replace `format-skill-set` to emit real
context-filtered registrations and retire `getSkills` (the Option (a) to (b) move,
Section 7.1); and likely add filter steps for context-relevance (extension point 2,
Section 5.3). Sprint 1 does NOT modify the dispatcher, run-chain, the sweep, or the
invariants in Section 9; it adds atoms and changes one formatter body. Sprint 1 also owns
enriching `all-candidates-filtered` with per-step drop attribution (Section 8).

### 10.2 Task State sprints

Task-state primitives interact with this surface in one of two ways, and the choice is a
design decision, not a default:

- If a task-state capability needs to be DISPATCHED (e.g. a handler that surfaces task
  context when a `(task-request ...)` input fires), it registers as a normal capability
  (Section 2) and reads its result via `dispatch-result` (Section 4). It must respect the
  retention contract (Section 6): dispatch and read same-cycle.
- If task-state is purely producing/consuming durable state (phases, cycles-since-input,
  pending threads), it does NOT go through dispatch at all; it writes its own NON-dispatch-*
  atoms, which the sweep never touches (Section 6). The task_state / task_state_writers
  pure-vs-writer split (Artifact 0 Discipline 6) is the pattern, independent of this
  registry.

The key contract for Task State: anything it writes that matches one of the six swept
dispatch-* shapes WILL be cleared each cycle. Task-state atoms must use their own atom
families, which they do. There is no collision today; this note exists so a future
task-state atom is never named into the swept set by accident.

### 10.3 NACE (the learning consumer)

NACE steers dispatch by writing the observation atoms in Section 5.5
(`capability-efficacy-observation` and siblings), which `resolve-efficacy` /
`resolve-priority` / `resolve-lifecycle` already prefer over registered values. NACE does
NOT edit registrations and does NOT edit the dispatcher. The `should-dispatch` gate NACE
builds reads efficacy beliefs to decide eligibility; wiring it as a filter step (extension
point 2) is the clean integration, because that is the registered way to add an
eligibility dimension. This surface was built with that seam in place; NACE fills it.

### 10.4 The soul-state-producer / dispatch-guard (governance)

Blocked on Boundary 1 (Section 8). Once soul state is a queryable `(soul-state ...)` atom,
the dispatch-guard is added as a filter step (extension point 2) that gates candidates on
soul Safety state, or as a capability that anchors. Either way it plugs into the existing
extension points; it does not modify the dispatcher. It MUST NOT register until Boundary 1
closes.

---

## 11. What Sprint 0-Coda did NOT deliver (scope boundaries)

So downstream sprints do not assume capability that is not there:

- It did not migrate the 14 hardcoded skills to individual registrations. One capability
  (skill-discovery) is registered. Bulk migration is Sprint 1.
- It did not make registry content model-visible. Option (a) holds; `format-skill-set`
  returns `getSkills`. Option (b) is Sprint 1.
- It did not deliver any learning. The observation-override seam exists; nothing writes to
  it. That is NACE.
- It did not deliver governance enforcement. The registry cannot read soul verdicts
  (Boundary 1). No dispatch-guard exists.
- It did not make handler exceptions reliably catchable on the indirect path (Criterion 5).
- It did not deliver durable cross-cycle dispatch records. Records are transient by
  contract (the sweep).

---

## 12. The one-paragraph contract summary (paste into any sprint that touches this)

The capability registry (`soul/capability_registry.metta`, live at 38737ac) dispatches by
matching `(registered-capability schema: handler: priority: lifecycle: metadata:)` (FIVE
fields, exact-match-or-silent-fallback) against an input atom, running survivors through a
registered filter pipeline (add `(capability-filter-step order: step:)` to extend
eligibility dimensions, never edit registry code), sorting by priority, and running the
chain until a handler returns `decision-anchor` or it exhausts. Results are read from
`(dispatch-result invocation-id: result: handler:)` SAME-CYCLE, because a per-cycle sweep
clears all six transient dispatch-* families at the top of each dispatch; only
non-dispatch-* atoms (registrations, filter steps, eligibility seeds, observation atoms,
handler-owned atoms) persist. Dynamic steering is done by writing
`capability-*-observation` atoms (resolved in preference to registered values), not by
editing registrations. Today content is Option (a) (skill-discovery returns `getSkills`);
Sprint 1 moves to Option (b). Governance capabilities are blocked until Boundary 1 closes.
Match every atom's field count exactly; a wrong arity does not error, it silently fails to
couple.
