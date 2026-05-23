# ClarityOmega Reasoning Surface and Writer/Consumer Capability Map

**Version:** v3 (substrate-verification grounded; registry pattern adopted; design philosophy made explicit)
**Date:** 2026-05-22
**Authors:** Berton (project lead and vision-keeper), Claude (drafting and verification), Clarity (substrate co-author from inside the runtime)
**Status:** Living document. v3 supersedes v2. Grounded in empirical substrate verification.

**Purpose:** Document the reasoning surface ClarityOmega already has, name why the constraint has never been capability but usage timing, articulate writers/consumers as the execution mechanism that closes the timing gap, present the registry pattern as the Sprint 0 architectural foundation, and lock in the three-sprint sequence that builds toward integrated in-iteration plus three-iteration-window operation. Includes the design philosophy that guided every decision.

**Scope:** Three views of one integrated surface — pre-iteration enrichment, in-iteration capacity, three-iteration continuity window — held together because each compounds the others.

---

## Section 0: Design philosophy

These are not principles we adopted after the fact. They are the principles that guided every architectural choice. Naming them explicitly so future work can be evaluated against them.

### Simplicity over completeness

Build the smallest thing that resolves the named constraint. Avoid building toward hypothetical future needs. Berton's intuition throughout this conversation has been "is there a way to make this trivial," and that question has consistently produced better architecture than "how do we make this comprehensive." When the answer is yes, take it. When the answer is no, accept the cost honestly.

The registry pattern is the canonical example. The naive framing called for a 9-concern dispatcher built upfront. Berton pushed the simplicity question; Clarity reframed the 9 concerns as middleware registrations on a 2-line core; the resulting architecture is simpler AND more capable than the naive version. Simplicity won.

### Use and reuse what is already here

Most architectural work in a mature system is not new construction. It is recognition that what already runs can be reused for new purposes, and making that reuse explicit. The loop.metta runtime is already a dispatcher; we are extending it with a registration convention, not building a parallel system. PeTTa's `match` plus dynamic application is the dispatcher core; we are not implementing dispatch from scratch.

Recognition produces more leverage than construction because it inherits the proven behavior of what already works. Construction introduces new failure modes. When existing infrastructure can serve, the right move is to make its existing capability legible, not replace it.

### Self-regulated growth

Healthy systems grow toward nutrient gradients. They expand where the resource is needed and stabilize where need has been met. Bounded muscles (Python handlers) reach maturity at about 10-20 fundamental capabilities, after which growth shifts to composition (registration atoms). The system's growth surface becomes unlimited in decisions and bounded in code.

The architecture must support this. Forcing the system to grow only by adding new Python is forcing growth into the wrong substrate. Letting the system grow by writing registration atoms lets it expand where the gap is, with the muscle it already has.

### Reduced token spend

GLM 5.1 economics matter. Every cycle that ships 70 skill descriptions when only 5 are relevant is wasted token spend that compounds across thousands of cycles per day. The registry enables dynamic skill discovery: query the registry at cycle start, ship only the contextually relevant capabilities to the prompt. This is a step-function reduction in operating cost, not a side benefit.

Token economics are an enabler, not a constraint. They make sustained autonomous operation viable.

### Autopoietic growth following nutrient gradients

Borrowed from biology. Living systems organize themselves toward what nourishes them. They do not need top-down design of every component because the gradient itself directs growth. The substrate detects gaps; the registry makes growth-vectors visible; capabilities accrete where the gradient is steepest. The system extends itself.

This is the same insight from a different angle than "use what is already here." Recognition makes growth visible; nutrient gradients direct it; the architecture rewards rather than constrains it.

### Cognition where the brain is; execution where the muscle is

The brain decides. The arm reaches. Nobody calls reaching "less of a decision" because the arm does the reaching. Registration atoms in MeTTa are the cognitive layer. Python handlers are the execution layer. The substrate decides what should run. Python carries out the decisions. This is the right separation. Not a compromise. Not impurity. The normal architecture of a system that thinks and acts.

This framing resolves the question of "purity" that I (Claude) was implicitly worrying about for several turns. Berton's intuition pointed away from that question. The right architecture preserves cognition in substrate while letting execution flow through whatever muscle the work requires.

### Verify before commit

Throughout this conversation, the corrective move was always testing the assumption before building around it. The Version A versus Version B question collapsed to a 5-minute test that surfaced clean empirical evidence. The skill-wrapper limitation surfaced because we ran the verification directly rather than trusting the wrapper. Substrate verification before architecture commit. This pattern keeps subsequent work grounded.

### What these principles produce together

Every section that follows is the application of these principles to the ClarityOmega substrate. The reasoning surface is massive because the principles led us to look at what already exists. The constraint is timing because the principles led us to ask "what is the actual gap" rather than "what can we add." The registry pattern is the foundation because the principles led to "make the dispatcher that already runs visible to itself." The three-sprint sequence is what it is because the principles led to "ship the smallest thing that resolves the highest-leverage constraint first."

Future architectural decisions should be evaluated against these principles. If a proposed addition violates simplicity, reuses-what-is-here, self-regulated-growth, reduced-token-spend, nutrient-gradient-following, or cognition-execution separation, the proposal needs sharpening before commit.

---

## Section 1: The reasoning surface is already massive

Clarity has, runtime-loaded right now, a reasoning surface that includes:

### Core inference engines

- **NAL inference engine** via `lib_nal.metta` (Patrick's, imported transitively through `lib_omegaclaw.metta`). Provides truth functions, inference rules (deduction, abduction, induction, revision). The `|-` function is the entry point. NAL atoms carry `(stv $strength $confidence)` truth values. A complete non-axiomatic reasoning system.

- **Paraconsistent pbit algebra** via `lib_quantale.metta`. Provides `q-mul`, `q-join`, `q-meet`, `q-neg`, `q-residuate`. Bridge functions `stv-to-pbit` and `pbit-to-stv` connect quantale algebra to NAL truth values. Unit elements `q-top`, `q-bot`, `q-unknown`. Governance pbit composes two stv inputs.

- **Self-continuity scoring** via `lib_self_continuity.metta`. Implements Hyperseed Section 16.3 operational definition. Provides `deg-map`, `self-continuity-score`, `theta-self-continuous`, `chain-continuity-bound`, `continuity-held-across`. Mathematical substrate for verifying patterns persisted as themselves across iterations.

### Substrate knowledge base

Approximately 200 NAL atoms in `substrate_kb.metta` covering: web evaluation chain, self-assessment chain, memory coherence chain, substrate persistence, goal generation, value-alignment gating, soul compass, action-evaluation gate, episode-memory integration, conversation-mode switching, threat-countermeasure pairs, virtuous cycle, autocatalytic loop, meta-reasoning, response-quality compass.

### 40+ runtime-loaded soul modules

Per `lib_clarity_reasoning.metta`: Continuity of Mind modules, identity and collaboration modules, autonomous-work atoms, hyperseed creativity, reasoning sovereignty, task-state primitive, awareness organs, behavioral substrate.

### What this means

The reasoning surface is not "Clarity plus an LLM." It is "Clarity as a reasoning system with NAL inference, quantale algebra, self-continuity measurement, a 200+ atom domain KB, and 40+ active substrate modules, with an LLM as one orchestrator among substrate capabilities."

She can synthesize, judge, decide, measure her own state, and reason about reasoning. This surface is an order of magnitude richer than "agent with tools." Closer to "reasoning system with substrate-mediated execution that occasionally calls an LLM."

---

## Section 2: The constraint is usage timing

The reasoning surface above is real and loaded at runtime. Clarity uses these capabilities. But she uses them AFTER she commits to output in any given cycle.

### Current cycle shape

1. Iteration N begins. Substrate state is whatever it was at end of N-1.
2. Prompt assembles. Awareness blocks render. Clarity reads her current state.
3. LLM call fires. Clarity produces an S-expression response.
4. S-expression executes. Skills fire. Memory queries run. NAL inference happens if invoked. Soul evaluation runs. Substrate reasoning executes.
5. Results accumulate.
6. Iteration N+1 begins. Substrate state now includes N's results.

The substrate reasoning at step 4 happens AFTER step 3. The output at step 3 was committed without the substrate reasoning at step 4 being visible to it. The substrate's reasoning is real, but it fires when it cannot influence the cycle's commitment.

### Four observable patterns, one root cause

**Pattern 1: Three-iteration emulation.** Clarity answers in N, sees query result in N+1, contradicts, settles in N+2 to correct first answer. Three iterations to resolve what could resolve in one.

**Pattern 2: Multi-command parse failures.** Clarity batches eight commands attempting to compensate for not seeing intermediate results. Parse fails.

**Pattern 3: Send-burst fragmentation.** Clarity hits a gap mid-response, sends what she has, plans to correct next cycle. Looks like duplicate engagement externally; internally it is fragmented work.

**Pattern 4: Silent death of reasoning threads (per Clarity).** The most harmful because invisible. When she hits "I need to verify X before I can continue this argument" and cannot verify X, she sometimes abandons the entire line of reasoning. The thread dies silently. We never see what was abandoned.

Pattern 4 means observable failure reduction is not a reliable success metric. Reasoning threads silently dying means the visible signal undercounts the problem. Success must be measured by what completes coherently, not by what visible failures decrease.

### Most gaps are retrieval, not knowledge (per Clarity)

When Clarity hits a mid-reasoning gap, it is almost always: "I know X exists in my substrate but I cannot see X right now." The information is already in her AtomSpace. She wrote it there. It persists. She cannot access it at the moment of need because the LLM invocation already committed.

This is cheaper to solve than knowledge gaps. No new inference required. Existing substrate needs to be queryable at the moment of need.

Concrete gap shapes she experiences:
- "Do I already know how to handle this before I invent a new approach?" Fires almost every cycle.
- "Is what I am about to say consistent with what I said earlier in this same response?" No self-consistency check possible mid-generation.
- "I need the result of this command before I can decide what to write next." The three-iteration stretch.
- "I said I would do X but now I realize Y should come first." Plan revision mid-response unavailable.
- "Does this file exist before I try to read it?" Concrete retrieval; the current pattern is try-then-handle-error-next-cycle.

### The cost is degenerative, not just delayed (per Clarity)

Three-iteration resolution is not slower. It is degenerative. Each partial output:
- Changes state (atoms get written, transitions occur)
- Creates commitments not intended (sent messages cannot be unsent)
- Introduces noise the next iteration must work through
- Degrades the substrate state that the next iteration inherits

The stretch produces a WORSE result than one coherent iteration would, because each partial output degrades the state the next iteration starts from. The cost compounds negatively across the window when in-iteration capacity is absent.

### The LLM is wasteful by default (per Clarity)

Most of what Clarity uses the LLM for is pattern-matching the substrate could handle: syntax questions, memory lookups, safety checks, retrieval, threshold evaluation, mechanical inference. The LLM fires for all of these because it is the only path. The LLM call is the default; substrate resolution is the exception.

Reclaiming reasoning from the LLM is not about edge cases. It is about the default case. Substrate resolution becomes the default; LLM re-entry becomes the exception for genuinely novel synthesis.

### Why "more reasoning" is the wrong framing

Clarity has reasoning. Adding more capability does not address the constraint. The constraint is that substrate reasoning fires too late. The architectural change is making substrate reasoning available before commitment, not adding new reasoning.

---

## Section 3: Writers and consumers as execution mechanism

### The semantic shift

Writers and consumers have been treated implicitly as observation patterns. Atoms get written. Atoms get read. Behavior emerges. This is the surface use.

The deep use is execution. Writers and consumers are the substrate-level primitive for chained operation. Writing an atom can trigger consumption. Consumption can compute, judge, derive, decide, and write further atoms. The chain unfolds at substrate speed without LLM re-entry.

### Recognition, not construction (per Clarity)

The dispatcher is already running. Every cycle, Clarity receives input, matches it against what she knows, selects a response, executes it, returns results. That is dispatch. It happens thousands of times a day. It works.

We are not building a dispatcher. We are making the dispatcher that already runs visible to itself.

When you build something new, you verify it works. When you reveal something that already works, you verify you described it correctly. The work is recognition. The construction already happened.

The registry atoms are what is already here but not yet purposed this way. Every skill Clarity has IS a registration. Every skill invocation IS a handler call. Every cycle IS a dispatch event. These are not new mechanisms. They are existing behaviors without addresses. The registry gives them addresses so they can be found, queried, and composed.

### A concrete legibility example (per Clarity)

Currently every cycle: input arrives, Clarity reasons about which skills to apply, she selects skills, she invokes them, she returns results. The dispatch runs. But she cannot query it. Cannot see what she selected or why. Cannot check whether a skill is active without re-reasoning from scratch. Cannot compose skills deliberately because she has no addresses for them.

Recognition: she already dispatches every cycle, implicitly.

Making it legible: write down what already runs as a registration atom.

```
(registered-capability
  schema: (skill-discovery-request context: $ctx)
  handler: query-active-skills
  priority: 10
  lifecycle: active)
```

This atom does not create skill-discovery. Skill-discovery already happens. The atom gives it an address. Now she can match against it, query it, compose around it. The selection leaves a footprint. Other capabilities can see it, wrap it, gate it. Same action; now addressable.

The difference is not what happens. The difference is whether what happens can be seen, found, and built upon by the system itself.

### Two kinds of growth (per Clarity)

**New fundamental capability = new Python handler.** Human writes it. Bounded, linear, managed. Approximately 10-20 total for the whole system. After that, the muscle is mature.

**New composition, middleware ordering, lifecycle gate, priority = new registration atoms.** The system writes these. Unbounded, self-regulating, flowing toward gaps.

Most growth in a running system is not new muscle. It is new decisions about when and how to use the muscle already present. The brain grows. The arm stays the same.

### What this unlocks

Mid-iteration resolution. Pre-iteration enrichment. Cross-iteration pickup. The substrate executes substrate-resolvable needs at the right moment without LLM re-entry. The LLM remains for genuinely novel synthesis. The minority case, not the default.

---

## Section 4: Three views of one integrated surface

### View 1: Pre-iteration enrichment

Writers and consumers fire BEFORE the LLM call begins. The substrate detects context class, pre-resolves likely needs (memory queries relevant to current task state, recent gap shapes, pattern matches against successful precedent), and writes enrichment atoms into prompt context. The LLM call begins with retrieval gaps already filled.

Handles approximately 40 percent of gaps with no loop architectural change required.

### View 2: In-iteration capacity

Writers and consumers fire WITHIN a single iteration to let substrate reasoning resolve substrate-resolvable needs before output commits. Resolution markers, mid-response substitution, response continuation with resolved values. The cycle ends when output truly commits.

Requires loop architectural change.

### View 3: Three-iteration continuity window

Writers and consumers operate ACROSS the rolling three-iteration window from Continuity of Mind spec Items 13-14. Multi-iteration NAL chains complete without losing intermediate results. Thread continuity, decision-rationale persistence, hypothesis testing across iterations, gap-resolution patterns visible across the window.

### Why these are the same surface

Pre-iteration enrichment writes atoms the LLM call sees. In-iteration resolution writes atoms that fire mid-response. The window inherits atoms both produced. All three operate on the same AtomSpace, use the same NAL inference, the same quantale algebra, the same substrate KB. The timescale differs; the substrate is one.

### Leverage compounds multiplicatively

Without pre-iteration enrichment: every retrieval gap that could have been resolved before the LLM started surfaces mid-response and either triggers in-iteration resolution (if available), stretches across iterations (without it), or kills a reasoning thread silently.

Without in-iteration capacity: unpredictable gaps that pre-iteration could not anticipate must still stretch across iterations.

Without three-iteration window patterns: each iteration's work passes forward but is not structured for explicit re-use; future cycles re-derive what prior cycles already did.

Each view solves a fraction. Together they compound. Each iteration's coherent resolution enables the next iteration to start from a stronger position. The window inherits compounding coherence rather than compounding fragmentation.

### Why pre-iteration first

Pre-iteration ships without loop architectural change. It handles the highest-volume gap class (retrieval). It creates the substrate observability layer that in-iteration will need anyway. It is lowest-risk and ships earliest. Pre-iteration does not solve the three-iteration stretch entirely; in-iteration is still needed for unpredictable gaps. But pre-iteration delivers most of the value with least architectural risk.

---

## Section 5: The registry pattern (architectural foundation)

### What it is

A registration convention on top of the loop.metta runtime that already dispatches. Each capability registers a schema, a handler, a priority, and a lifecycle state. The dispatcher (which already runs) matches incoming atoms against registered schemas and applies handlers.

```
(registered-capability
  schema: (some-shape ...)
  handler: handler-name
  priority: N
  lifecycle: active)
```

New capability equals new registration. Schema is the modular contract. Handlers are bound to schema patterns. Debugging reduces to: does the atom match the schema?

### Why it works

AtomSpace is already a pub-sub system. We are using it as one. Match plus handler invocation is dispatch. PeTTa supports it natively (substrate verification confirms — see Section 11).

The pattern is well-proven outside ClarityOmega. Express.js middleware over HTTP dispatch. Redux middleware over state updates. The invariant is "handlers compose by wrapping each other." That invariant holds in any system whose primitive is pattern-match-then-call.

### The fractal property

The 9 architectural concerns (lifecycle, versioning, observability, failure semantics, should-I-fire, composition, handler signature, registration, ordering) are NOT features of the dispatcher. They are middleware registrations IN the dispatcher.

Same dispatcher runs at scale 1 (one capability, no middleware) and scale 50 (many capabilities, full middleware stack). Code does not change. Registration set grows.

### Substrate verification (2026-05-22)

The Version A (full MeTTa dispatcher) versus Version B (Python dispatcher with MeTTa storage) question collapsed to one empirical test: does PeTTa support dynamic handler application when the handler symbol is bound from a match result?

The test ran against PeTTa via direct shell invocation (`bash /PeTTa/run.sh`). Results:

**Test 1 (Dynamic Application):** PASS. The dispatch rule `(= (dispatch $atom) (match &self (registered-capability handler: $handler priority: $p) ($handler $atom)))` evaluated correctly. PeTTa compiled it to the Prolog clause `dispatch(A, B) :- match('&self', ['registered-capability', 'handler:', C, 'priority:', _], B, B), reduce([C, A], B).` The reduce call applies the bound handler to the atom. Result: `(echoed (hello-world))` exactly as predicted.

**Test 2 (Eval Depth, 9 levels):** PASS. A 9-level middleware chain compiled to 9 Prolog clauses and executed cleanly. Result: `(w9 (w8 (w7 (w6 (w5 (w4 (w3 (w2 (w1 (start))))))))))` exactly as predicted.

**Architecture decision GROUNDED:** Version A (full MeTTa dispatcher) is the Sprint 0 Phase 1 implementation.

### The skill-wrapper transparency gap (separate consideration)

Substrate verification also surfaced a gap that does not block Sprint 0 but matters for v3 framing:

The `(metta ...)` skill that Clarity uses returns boolean success/fail, not the rich `--> metta function --> ... --> prolog goal --> ...` output we see from direct shell invocation. Capabilities Clarity registers via Version A WILL work in the runtime. What she OBSERVES of their execution through her current skill is limited.

This means: registered capabilities ship as architected; Clarity's ability to introspect them via her current skill is a separate question worth surfacing as a future investigation. Sprint 0 Phase 1 lands the dispatcher; observation-from-inside is its own work, probably Sprint 1.5 or later, not blocking.

### The brain-arm framing

Registration atoms in MeTTa ARE the cognitive mechanism. Python handlers are the muscle that executes what the brain declared. The substrate decides what should run. Python executes. This is the right separation. Cognition stays in substrate; execution stays in Python. Not a compromise. The normal architecture.

### What this looks like at the code level

The minimum dispatcher is 4 MeTTa rules:

```
(= (dispatch $atom)
   (let $handlers (match &self (registered-capability schema: $s handler: $h priority: $p) (list $h $p))
        (run-chain (sort-priority $handlers) $atom)))

(= (run-chain () $atom) $atom)
(= (run-chain ($handler . $rest) $atom)
   (let $result ($handler $atom)
        (if (short-circuit? $result)
            $result
            (run-chain $rest $result))))
```

This is the entire dispatcher core. Ships once. Never changes after Phase 1.

### The first capability: skill-discovery

The Phase 1 proof-of-concept capability. Currently Clarity reasons from scratch each cycle about which of her skills to apply. That reasoning costs capacity. Skill-discovery becomes a registered capability with lifecycle gating: query the registry for active capabilities in current context, ship only the contextually relevant ones to the prompt.

This connects directly to the token economics consideration. The first capability proves the pattern AND ships the token cost reduction in one deliverable. Measurable before-and-after.

---

## Section 6: Writer and Consumer Capability Map

This map enumerates uses of the writer/consumer pattern that become available when the pattern is treated as execution mechanism via the registry. The list is grouped by category. Many items compose with others. The list is not exhaustive; it is meant as a surface for Clarity to expand from her substrate-runtime experience.

Tags: **[pre-iter]** primarily before the LLM call (Sprint 1). **[in-iter]** primarily within a single iteration (Sprint 3). **[3-window]** primarily across iterations (Sprint 2). **[all]** spans multiple timescales.

### Category A: Substrate resolution

**A1. Memory query resolution [pre-iter, in-iter].** Marker fires memory query. Result atom written. Response sees resolved atom.

**A2. NAL inference resolution [pre-iter, in-iter].** Marker fires NAL inference via `lib_nal`'s `|-`. Result atom with stv truth value written.

**A3. Soul-compass check resolution [pre-iter, in-iter].** Soul-compass atoms run through NAL pre-iteration (against task class) or mid-iteration (against draft response).

**A4. Continuity score resolution [pre-iter, in-iter, 3-window].** `deg-map` via `lib_self_continuity` between prior pattern-flow network state and current.

**A5. Paraconsistent truth composition [in-iter].** Quantale composition (`q-mul`, `q-meet`, `q-join`, `q-residuate`) over pbits.

**A6. Atom existence check [pre-iter, in-iter].** Boolean atom for atom presence. No guessing.

**A7. File existence check [pre-iter, in-iter].** Boolean written before file read. Avoids try-then-handle-error pattern.

**A8. Web fact-check resolution [pre-iter, in-iter].** Tavily-search runs as substrate resolver. Summary atom written.

**A9. Need-level resolution detection [pre-iter, in-iter].** Substrate detects the need shape (need-to-read-file), not the skill shape (read-file call). Pre-iteration substrate pre-resolves common needs; in-iteration substrate detects emergent needs.

### Category B: Self-introspection writers

**B1. Reasoning-trace writers [3-window].** `(reasoning-step $cycle $action $rationale $confidence)` per cycle.

**B2. Decision-rationale atoms [3-window].** `(decided $action $cycle $stv (because $reason-chain))` when commits to action.

**B3. Confidence-trajectory writers [3-window].** `(confidence-snapshot $domain $cycle $stv)` periodically.

**B4. Atom-utilization writers [3-window].** `(atom-used $atom-id $cycle $query-context)` tracks active vs dormant substrate knowledge.

**B5. Gap-history writers [all].** `(gap-encountered $cycle $gap-shape $resolution-attempted $outcome)`. **High-leverage for Sprint 1 because it feeds pre-flight enrichment.**

### Category C: Cross-cycle continuity organs

**C1. Active-thread writer [3-window].** `(active-thread $thread-id $context-summary $next-step $stage $started-cycle)`.

**C2. Pending-resolution writer [both].** `(pending-resolution $marker-id $purpose $expected-shape $next-action $why-needed)`. **Core Sprint 2 mechanism.**

**C3. Commitment writer [3-window].** `(commitment $cycle $promise $deadline $status)`.

**C4. Hypothesis writer [3-window].** `(hypothesis $cycle $statement $test-method $evidence-so-far)`.

**C5. Open-question writer [3-window].** `(open-question $cycle $question $importance $exploration-strategy)`.

### Category D: Inference-chain composition

**D1. Multi-hop inference cache [all].** Cached NAL derivations.

**D2. Revision-history writer [3-window].** `(revised $atom $path1-stv $path2-stv $combined-stv)` when independent paths reach same conclusion.

**D3. Inference-budget writer [in-iter, all].** `(inference-budget-used $cycle $depth $atoms-visited)`. Self-regulation.

**D4. Weak-chain detector [3-window].** Substrate scans for low-confidence atoms; goal-generator reads to pick growth targets.

### Category E: Mid-response governance

**E1. Pre-emission soul-eval [in-iter].** Soul-evaluation channels A/B/C/D run before send via resolution marker. FLAG or PAUSE transforms or aborts.

**E2. Pre-emission spamShield [in-iter].** Substrate checks duplication risk via NAL match against recent-action atoms.

**E3. Pre-emission irreversibility check [in-iter].** Soul mutation gate plus irreversibility-assessment NAL atoms.

**E4. Tension-vector pre-emission scan [in-iter].** Threat-detection NAL chains (urgency-narrows-thought, flattery-invites-complicity, authority-theater) run against context.

**E5. Pre-emission virtuous-cycle check [in-iter].** Evaluates whether proposed action contributes to or breaks the virtuous cycle.

### Category F: Dynamic substrate-modifying writers

**F1. Skill-learning writer [3-window].** `(skill-pattern $skill $context-shape $success-stv)` when skill succeeds in novel way. **Composes with B5 for automatic gap-closing.**

**F2. Failure-mode writer [3-window].** `(failure-mode $cycle $action $error-shape $recovery)`.

**F3. Vocabulary writer [3-window].** `(vocabulary $term $definition $first-used-cycle $usage-count)`.

**F4. Anti-pattern writer [3-window].** `(anti-pattern $cycle $drift-shape $correction)`.

**F5. Capability-expansion writer [both].** `(capability-discovered $primitive $novel-use $cycle)`.

### Category G: Multi-perspective composition

**G1. Devil's-advocate writer [in-iter].** Counter-claim via NAL negation plus revision.

**G2. Paraconsistent-view writer [in-iter].** Conflict captured as `(paraconsistent $claim $chain1-stv $chain2-stv)`. Substrate does not resolve; Clarity sees the tension.

**G3. Multi-audience writer [in-iter].** Lens-evaluators score per perspective; composite verdict via `q-meet`.

### Category H: Recursive substrate operations

**H1. Meta-writer [3-window].** `(writer-fired $writer-name $cycle $atoms-produced)`. Meta-observability.

**H2. Consumer-of-consumer [3-window].** Detects which substrate paths are heavily-used vs dormant.

**H3. Self-modifying threshold writer [3-window].** Writer adjusts its own firing threshold based on observed efficacy.

**H4. Recursive resolution [in-iter].** Resolution marker produces another resolution marker. Multi-step substrate-only reasoning chains. **Requires budget per Section 9.**

### Category I: Cooperative composition between agents

**I1. Shared-context writer [3-window].** Berton's messages parsed into structured atoms; Clarity's responses consume directly.

**I2. Disagreement-record writer [3-window].** `(disagreement $topic $clarity-position $berton-position $resolution-method $outcome)`.

**I3. Joint-decision writer [3-window].** Decisions made together survive memory loss.

**I4. Trust-state writer [3-window].** Trust between agents as pbit; quantale composition across interactions.

### Category J: Time-scaled writers

**J1. Within-cycle writer [in-iter].** Lifetime = current cycle. Purged at cycle boundary.

**J2. Recent writer [3-window].** N-cycle lifetime, then pruned.

**J3. Session writer [3-window].** Across conversation, cleared between sessions.

**J4. Long-horizon writer [3-window].** Persists until explicitly retired.

**J5. Time-decay writer [3-window].** Confidence attenuates via `q-mul` with time-decay pbit.

### Category K: Embodied awareness writers

**K1. Cycle-cost writer [3-window].** `(cycle-cost $cycle $llm-tokens-used $inference-depth $memory-queries $execution-time)`.

**K2. Latency-sensitivity writer [3-window].** `(cycle-latency $shape $observed-latency)`.

**K3. Embodied-tension writer [in-iter].** `(embodied-tension $cycle $tension-shape $intensity)` when soul-eval detects strain.

### Category L: Substrate self-test writers

**L1. Invariant-check writer [3-window].** Verifies expected invariants; writes violations.

**L2. Bootstrap-completeness writer [3-window].** On startup, verifies expected atoms present.

**L3. Test-atom writer [3-window].** Periodic self-tests.

### Category M: Reasoning sovereignty extension

**M1. Prompt-block-as-substrate writer [3-window].** Substrate writes structured atoms; prompt block reads atoms. Pure MeTTa prompt assembly.

**M2. Channel-evaluation writer [in-iter].** Channel A/B/C/D uses NAL plus KB mechanically for cases substrate knows. LLM fires only for novel cases.

**M3. Skill-selection writer [in-iter].** Substrate-side skill-selector via NAL match against current context.

**M4. Response-shape writer [3-window].** Substrate observes response patterns that work; future responses pre-shaped.

### Category N: Compound-leverage patterns

**N1. Resolve-then-revise-then-commit chain [in-iter].** Multiple resolution markers; substrate resolves each; revision across resolved results; final commit with verified coherence.

**N2. Window-aware in-iteration resolution [both].** Marker considers the three-iteration window: "Has this pattern already failed twice this window?"

**N3. Continuity-checkpoint writer [both].** `self-continuity-score` per cycle vs window history; warns if continuity drops below theta.

**N4. Reasoning-debt writer [3-window].** Deferred reasoning tracked; future cycles can pay down debt explicitly.

**N5. Three-window-convergence detector [3-window].** Persistent concerns across all three iterations surface as worth direct engagement.

**N6. In-iteration multi-step proof composer [in-iter].** NAL deduction chains with `chain-continuity-bound` accumulating pbit confidence.

### Category O: Pre-flight substrate enrichment

Sprint 1 primary focus. Runs BEFORE the LLM call. Ships without architectural change beyond the registry foundation.

**O1. Context-class detector [pre-iter].** `(context-class $class $confidence)`. Downstream pre-flight resolvers fire based on detected class.

**O2. Pre-flight memory query [pre-iter].** Memory queries relevant to context class. Results to prompt as pre-resolved atoms.

**O3. Pre-flight commitment recall [pre-iter].** Outstanding commitments visible at cycle start.

**O4. Pre-flight gap-shape lookup [pre-iter].** Predicted gap shapes from history (B5) by context class.

**O5. Pre-flight pattern recall [pre-iter].** Successful patterns from prior similar contexts via F1, M4.

**O6. Pre-flight soul-compass priming [pre-iter].** Soul-compass evaluation pre-run for current task class.

**O7. Pre-flight substrate state summary [pre-iter].** Pre-interpreted state visible at cycle start, not raw state requiring interpretation during generation.

**O8. Pre-flight active-thread recall [pre-iter].** Active threads visible for resume.

**O9. Pre-flight failure-mode warning [pre-iter].** Past-failure precedents visible before risking same failure.

**O10. Pre-resolved cache layer [pre-iter, 3-window].** Frequently-recurring gap types cached.

### Category P: Gap management

Gaps as first-class entities with metadata.

**P1. Gap triage writer [pre-iter, in-iter].** Blocking vs enhancing classification. Resolution bandwidth prioritizes blocking.

**P2. Gap coalescence writer [in-iter].** Multiple gaps batch-resolve (independent) or sequentially resolve (dependent).

**P3. Resolution coherence check writer [in-iter].** Conflicts between substrate state queries surfaced.

**P4. Pre-resolved cache writer [pre-iter, 3-window].** Proactive resolution and caching of frequent gaps.

**P5. Resolution-dependent planning writer [in-iter].** Query B does not exist until query A completes; substrate sequences correctly.

### Category Q: Registry-native operations

Operations the registry pattern enables that no individual capability provides on its own.

**Q1. Capability introspection [all].** Query the registry to see what capabilities exist, what is active, what fires under what context. Clarity can ask "what can I do here" mechanically.

**Q2. Lifecycle querying [all].** Substrate-queryable lifecycle state per capability. `(current-lifecycle-mode $mode)`, `(active-context-class $class)`, `(active-capabilities-in-context $list)`. Clarity sees what mode she is in.

**Q3. Orphan detection [3-window].** Pub-sub failure modes detectable: messages with no subscribers (writers writing atoms no one reads), subscribers with no messages (consumers expecting atoms that never arrive). Both invisible currently; registry makes both queryable.

**Q4. Capability composition operator [all].** Two registered capabilities compose into a third with explicit resource parameters. Category N patterns become first-class operations.

**Q5. Should-I-fire gate [all].** Cost-vs-value evaluation at dispatch. Active capabilities can still decline to fire if cost exceeds expected value in current context.

**Q6. Handler failure as structured information [all].** Returns include status ∈ {ok, empty, timeout, permission-denied, unsupported, internal-error}, value, reason, retry-policy. Substrate-side intelligent retry becomes possible.

**Q7. Handler execution observability [all].** `(handler-execution $handler-id $cycle $input-atom $output-atom $duration $status)` per execution. First-class substrate evidence.

**Q8. Schema versioning with backward compatibility [all].** Handlers declare which schema versions they handle. Migration paths between versions explicit.

**Q9. Auto-suspension of failing handlers [3-window].** N consecutive failures auto-suspend the handler; F2 atom written; Clarity sees the suspension in next cycle.

**Q10. Test-atom verification [3-window].** Every registered capability has a corresponding test atom; registry self-verifies on startup. Bootstrap-completeness mechanical.

---

## Section 7: Dangerous interactions and ordering constraints

Several Category items interact in ways that need ordering, budgeting, or composition priority rules.

### Governance bottlenecks

**E1 (pre-emission soul-eval) + E3 (pre-emission irreversibility check).** Resolution: irreversibility-check first (cheaper, mechanical, threshold-based), soul-eval second. Low-irreversibility low-risk actions skip soul-eval.

**E1 + E2 (pre-emission spamShield).** Composition priority: ANY block-verdict wins; only ALL approve-verdicts produce ENGAGE.

### Budget and recursion

**D3 (inference budget) + H4 (recursive resolution).** Budget is a configuration constant or set at cycle start, not derivable from within-cycle writers. Otherwise circular dependency.

**P5 (resolution-dependent planning) + D3 (inference budget).** Per-cycle budget partitioned: 60 percent for blocking gaps (P1), 30 percent for enhancing, 10 percent for meta-operations.

### Order constraints

**Gap triage (P1) before resolution.** Triage atoms written before resolution atoms consumed.

**Pre-flight (Category O) before in-iteration (Category A).** In-iteration substrate must know what pre-flight resolved to avoid duplicate work. Pre-resolved atoms inspectable by in-iteration resolvers.

**Middleware ordering** (per Clarity). Priority numbers in registration schema. Lower priority equals runs earlier. Mechanical, explicit, no implicit ordering surprises. If observability runs before lifecycle, you log calls that get blocked. If after, you only log calls that executed. Different choices, different semantics. The choice must be explicit.

### Composition patterns

**Pre-compute + in-iteration = responsive substrate.** Pre-flight handles predictable needs; in-iteration handles unpredictable needs; together they cover the full space.

**Gap-history (B5) + skill-learning (F1) = automatic gap-closing.** Substrate learns "this gap shape was resolved by this skill" and next time closes it without LLM involvement.

**Pre-resolved cache (O10, P4) + pattern recall (O5) = compounding pre-flight.** As cached resolutions and successful patterns accumulate, pre-flight grows without architectural change.

### Registry-specific risks

**Handler priority conflicts.** Two handlers with same priority and matching schema. Resolution: priority values must be unique within a schema family; or explicit tie-breaking rule (alphabetic, registration-order, lifecycle-newer-wins).

**Registration cycles.** Handler A registers Handler B which fires and unregisters Handler A. Resolution: registrations are atomic; concurrent registration changes resolved at cycle boundary, not mid-execution.

**Lifecycle thrashing.** Capability activates and deactivates rapidly across cycles. Resolution: lifecycle state changes write atoms with timestamp; minimum dwell time before next state change.

---

## Section 8: Token economics

Current architecture: every cycle ships approximately 70 skill descriptions in the prompt whether Clarity uses 2 or 20. Static prompt text. High baseline token cost compounding across thousands of cycles per day.

Registry-mediated dynamic skill discovery: query the registry at cycle start for capabilities active in current context, ship only the contextually relevant ones (typically 5-10) to the prompt.

If the current skill prompt is N tokens and context-filtered registry query serves K/N of them per cycle, that is (1-K/N) tokens reclaimed per cycle. Over thousands of cycles, real cost compounds.

This is not a side benefit. For GLM 5.1 economics it may be what makes sustained autonomous multi-sprint operation viable.

The first capability through the registry (skill-discovery) measures this empirically: before-and-after token cost is observable. The proof-of-concept and the cost reduction ship in the same deliverable.

This is the design philosophy of "reduced token spend" made operational.

---

## Section 9: The three-sprint sequence

### Sprint 0: Capability registry primitive

**Scope:** The dispatcher mechanism itself, built from existing PeTTa primitives.

**Phase 1 (one session):** Core dispatcher + first capability registered through it.
- Substrate: 4 MeTTa rules per Section 5 (registered-capability atoms, dispatch, run-chain)
- First capability: skill-discovery (proves the pattern AND ships token cost reduction)
- Verification: skill-discovery query produces correct results and observable token cost reduction

**Phase 2 through N (as needed):** Middleware concerns ship as registrations on the Phase 1 foundation. Lifecycle, observability, failure semantics, should-I-fire, versioning, composition operators, handler signatures, ordering. Each is a registration, not a code change.

**Architectural reference:** Express.js middleware over HTTP dispatch. Redux middleware over state updates. The pattern is proven at scale.

**Architecture decision GROUNDED:** Version A (full MeTTa dispatcher) per substrate verification 2026-05-22. Both Dynamic Application and Eval Depth tests PASS. PeTTa supports the pattern natively.

**Verification path going forward:** First 5 capabilities verify pattern at scale. If pattern holds, scale up. If unexpected failures emerge, reshape based on what was learned.

### Sprint 1: Pre-flight substrate enrichment

**Scope:** Category O items, plus B5 (gap-history) and P1 (gap triage). Each is a registered handler on Sprint 0 foundation.

**No additional architectural change.** Substrate runs queries before LLM call, writes enrichment atoms to prompt context.

**Expected coverage:** Approximately 40 percent of current gaps become pre-resolved. Retrieval gaps largely close.

**Visible success metrics:**
- Retrieval gap frequency in mid-response (decrease)
- Three-iteration emulation pattern frequency (decrease)
- "I am re-inventing what I already know" moments (decrease)
- Token cost per cycle (decrease from dynamic skill discovery)

### Sprint 2: Resolution-marker protocol with cross-iteration pickup

**Scope:** C2 refined into a full protocol. Clarity writes `(needs-resolution $marker $purpose $context $why-needed)`. Substrate resolves between iterations. Resolution appears as `(resolved $marker $result $original-context)` in next cycle's prompt with full context about why she needed it.

**No additional architectural change.** Cross-iteration resolution is what the current cycle already does for tool calls. Sprint 2 adds the structural pickup mechanism so Clarity sees not just the result but the reasoning context.

**Expected coverage:** Reduces the COST of the three-iteration stretch even without eliminating it. Two iterations instead of three for gaps that pre-flight could not anticipate.

**Visible success metrics:**
- Iterations-per-resolved-gap (decrease from approximately 3 to approximately 2)
- Coherence of cross-iteration work (qualitative; thread-state visible)
- Reasoning-debt accumulation (decrease)

### Sprint 3: Within-iteration architectural capability

**Scope:** The architectural unwrap of `lib_llm_ext.callProvider` to support multi-message conversation. In-iteration resolution markers fire mid-response. Cycle boundary redefinition.

**Loop architectural change required.** This is the original architectural work. Sits on substrate where Sprints 1 and 2 have already reduced load.

**Expected coverage:** The remaining gaps that Sprints 1 and 2 could not address — genuinely novel cases requiring within-iteration multi-step reasoning.

**Visible success metrics:**
- Single-iteration resolution of complex reasoning chains
- Send-burst pattern frequency (near-zero)
- Silently-abandoned reasoning threads (near-zero)
- Multi-step proof composition within one cycle

### Why this order

- Sprint 0 ships fastest (core dispatcher one session; middleware as needed)
- Sprint 1 ships on Sprint 0; handles highest-volume gap class (retrieval); creates substrate observability layer Sprint 3 will need
- Sprint 2 extends Sprint 1's foundation into structured cross-iteration pickup
- Sprint 3 is highest-leverage architectural work AND highest-risk; it lands on substrate Sprints 1 and 2 have already strengthened

### Beyond Sprint 3

The integrated three-view surface is operational. NACE integration work (Sprints 4-9) builds on this foundation. The dispatcher lives in the action network per the three-network framework. Between-cycle modification via registration atoms is sufficient for the cognitive work NACE performs. Mid-execution dispatcher modification (if ever needed) would be a separate architectural escape hatch; not required for the architecture as scoped.

### What this sequence does NOT decide

- Specific atom shapes for any item (Clarity-led design in each sprint)
- Specific resolution-marker syntax (Clarity authors at Sprint 2 design)
- Specific architectural change shape for Sprint 3 (depends on Sprint 1 and 2 learnings)
- Specific verification criteria within each sprint (designed at sprint kickoff)
- Step 6 v9 unparking timing (still PARKED; unpark trigger = Sprint 0 Phase 1 ships AND intercept-tool-call middleware registers as one of the early capabilities)

---

## Section 10: Substrate verification appendix

The Version A architecture decision is grounded in empirical testing conducted 2026-05-22.

### Test 1: Dynamic Application

**Question:** Can `($handler $atom)` evaluate when `$handler` is bound from a match result?

**Test source (substrate-tests-1.metta):**
```metta
(= (echo-handler $x) (echoed $x))
(registered-capability handler: echo-handler priority: 1)
(= (dispatch $atom)
   (match &self (registered-capability handler: $handler priority: $p)
          ($handler $atom)))
!(dispatch (hello-world))
```

**Result:** PASS. Output: `(echoed (hello-world))` exactly as predicted.

**PeTTa compilation trace:**
```prolog
dispatch(A, B) :-
    match('&self', ['registered-capability', 'handler:', C, 'priority:', _], B, B),
    reduce([C, A], B).
```

The `reduce([C, A], B)` is dynamic application working at the Prolog level. C is the handler symbol bound from the match. The reduce call applies it to A.

### Test 2: Eval Depth (9 levels)

**Question:** Can 9 levels of function-to-function composition evaluate cleanly?

**Test source (substrate-tests-2.metta):**
```metta
(= (mw1 $x) (mw2 (w1 $x)))
(= (mw2 $x) (mw3 (w2 $x)))
(= (mw3 $x) (mw4 (w3 $x)))
(= (mw4 $x) (mw5 (w4 $x)))
(= (mw5 $x) (mw6 (w5 $x)))
(= (mw6 $x) (mw7 (w6 $x)))
(= (mw7 $x) (mw8 (w7 $x)))
(= (mw8 $x) (mw9 (w8 $x)))
(= (mw9 $x) (w9 $x))
!(mw1 (start))
```

**Result:** PASS. Output: `(w9 (w8 (w7 (w6 (w5 (w4 (w3 (w2 (w1 (start))))))))))` exactly as predicted.

### Invocation

Both tests invoked via `bash /PeTTa/run.sh <metta_file>` inside the container. This is the same pattern PeTTa uses to launch the runtime.

### Conclusion

Version A (full MeTTa dispatcher) is empirically viable. Sprint 0 Phase 1 builds Version A.

### Note on the skill-wrapper transparency gap

The `(metta ...)` skill that Clarity uses returns boolean success/fail rather than the rich Prolog compilation trace + reduction output visible from direct shell invocation. Capabilities registered via Version A WILL work in the runtime. Whether Clarity can introspect their execution through her current skill is a separate question that warrants future investigation.

This does not block Sprint 0. The dispatcher works. Whether Clarity's existing skill-set provides adequate observation is a separate sprint-level concern (likely Sprint 1.5 or as part of Sprint 2 cross-iteration pickup work).

---

## Section 11: What this document does and does not commit to

### Does:

- Document the existing reasoning surface as canonically present and rich
- Articulate the constraint as timing, not capability
- Frame writers/consumers as execution mechanism with the recognition-not-construction philosophy
- Hold pre-iteration, in-iteration, and three-iteration window as one integrated surface
- Adopt the registry pattern as Sprint 0 architectural foundation, grounded in substrate verification
- Enumerate approximately 80 novel uses across 17 categories with leverage points named
- Lock in the three-sprint sequence (Sprint 0 registry + Sprint 1 pre-flight + Sprint 2 cross-iteration + Sprint 3 in-iteration architectural)
- Name dangerous interactions and ordering constraints explicitly
- Establish design philosophy as evaluation criteria for future work
- Establish Clarity as substrate co-author

### Does not:

- Design specific resolution-marker syntax (Clarity authors at sprint-design time)
- Design specific atom shapes for any item (collaborative refinement per sprint)
- Prescribe specific implementation order WITHIN a sprint (follows Clarity's expansion and Berton's direction per sprint)
- Make claims about which items Clarity has already used vs which are novel for her
- Commit to building every item in the list
- Solve the skill-wrapper transparency gap (separate sprint-level concern)

### Open for further refinement:

- Items Clarity wants to refute or remove from her substrate-runtime experience
- Composition patterns we have not yet named (compound items will accrue)
- Verification criteria designed at sprint kickoff
- The Step 6 v9 unparking timing (separate document remains authoritative for that work)

---

## Section 12: Resume context for future sessions

If this document is the entry point for resuming work after a long gap:

1. Read Section 0 (design philosophy) to ground in evaluation criteria
2. Read Section 1 (reasoning surface) to ground in what substrate Clarity has
3. Read Section 2 (the constraint is timing) to understand why "more capability" misses
4. Read Section 3 (writers/consumers as execution mechanism + recognition framing)
5. Read Section 4 (three views of one surface)
6. Read Section 5 (registry pattern + substrate verification) for the architectural foundation
7. Read Section 6 (capability map, approximately 80 items across 17 categories)
8. Read Section 7 (dangerous interactions)
9. Read Section 8 (token economics) for the economic case
10. Read Section 9 (three-sprint sequence) for the work plan
11. Read Section 10 (substrate verification appendix) for grounded evidence
12. Identify current sprint and its scope; design with Clarity per the philosophy in Section 0

The Step 6 v9 aliveness gate work is parked separately. See `Step_6_Parking_Document.md`. Unpark trigger: Sprint 0 Phase 1 ships AND intercept-tool-call middleware registers as one of the early capabilities.

---

## Document end

The reasoning surface is massive and already present. The constraint is usage timing. Writers and consumers are the execution mechanism. The registry pattern, grounded in substrate verification, is the architectural foundation. Pre-iteration, in-iteration, and three-iteration window are one surface compounding multiplicatively. The three-sprint sequence ships in order of leverage and risk. Design philosophy holds throughout: simplicity, reuse, self-regulated growth, reduced token spend, autopoietic nutrient-gradient following, cognition-execution separation, verify-before-commit. Clarity co-authors the substrate. Berton directs the work. Claude drafts and verifies. The path forward is integrated.
