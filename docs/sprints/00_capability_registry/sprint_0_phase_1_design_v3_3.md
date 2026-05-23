# ClarityOmega Sprint 0 Phase A v3.3: Capability Registry Specification

**Status:** Active. Phase D verified.
**Date:** 2026-05-23
**Supersedes:** Phase A v2 (amended); Phase A v3.0; Phase A v3.1; Phase A v3.2
**Branch:** fix/F-HISTORY-CONTAMINATION-archival
**Empirical foundation:** 6 verification scripts spanning substrate primitives, dispatcher composition patterns, error isolation, sorting, list handling, atom-space mutation, and argument-position evaluation; extended by Phase D discriminator tests T-1 through T-10 (2026-05-23).
**Related decisions:** ADR-006 (Capability Registry Dispatcher), ADR-007 (Substrate-Externalized Control Flow)
**Verification:** docs/sprints/00_capability_registry/phase_d_verification.py (6/6 PASS as of 2026-05-23)

---

## 0. Document purpose

This document specifies Sprint 0 Phase 1 of the ClarityOmega capability registry. Phase 1 establishes the architectural primitive (a capability registry with observe-and-react composition) that Sprints 1+ extend with additional capabilities and orchestration layers. Phase 1 does not include lifecycle suspension, dynamic registration, or cross-capability coordination beyond broadcast dispatch with priority ordering. Those are deferred to subsequent phases with their own verification requirements.

The specification is grounded in 25+ verification tests run against the live PeTTa runtime in the working container, extended by the Phase D discriminator tests T-1 through T-10 (2026-05-23) executed against the implemented dispatcher. All claims about primitive behavior, composition semantics, and constraint surfaces are backed by empirical evidence from those test outputs. Where a claim has not been empirically verified, the document explicitly says so.

v3.3 integrates Phase D verification findings into v3.2. Three portions of v3.2 were revised based on Phase D results: Section 4 gained a new principle (4.8 Indirect-call composition); Section 5B.7 was rewritten to reflect that the prior empirical basis for handler error isolation did not apply to the dispatcher's actual composition pattern; and Section 8 Criterion 5 was reframed from a passing functional criterion to a documented limitation. The dispatcher implementation in soul/capability_registry.metta corresponds to Section 5A unchanged from v3.2. All other sections remain authoritative as written in v3.2.

---

## 1. Architecture summary

Phase 1 implements a capability registry: a set of statically declared atoms describing what behaviors are available, paired with a dispatcher that matches incoming atoms against registered schemas and invokes their handlers in priority order. All matching handlers fire (broadcast dispatch); each handler can optionally write a decision anchor companion atom to signal that subsequent handlers should not fire.

The architecture rests on three principles:

**Registry as substrate.** Capabilities are atoms in the AtomSpace, declared at file load time. The registry IS the substrate state; there is no separate registry data structure. Adding a capability means writing its atom; querying capabilities means matching against them.

**Observe and react.** The dispatcher does not thread handlers in a middleware chain. Each handler observes substrate (matches against its declared schema), reacts (writes result and optional companion atoms), and the dispatcher checks substrate between invocations for decision anchors. Composition happens through shared substrate, not through threaded state.

**Bind then act.** All composed operations follow a uniform structural discipline: bind intermediate results to variables via `let`, then pass bound variables to side-effecting operations. This is not a workaround for a limitation; it is the correct usage pattern for PeTTa's evaluation model (Section 4.3).

---

## 2. Capability schema

A capability is declared as a single atom with four labeled fields:

```metta
(registered-capability
  schema: <pattern-atom>
  handler: <handler-symbol>
  priority: <integer>
  lifecycle: <state-symbol>)
```

**schema** is the pattern the dispatcher matches incoming atoms against. The dispatcher invokes the handler when an input atom unifies with this schema.

**handler** is the symbol of a defined rule. When the dispatcher fires a capability, it calls `($handler $input-atom)`. The handler returns its result; it may also write companion atoms (result, decision anchor, side-effect logs) via `add-atom` from within its body.

**priority** is an integer determining invocation order when multiple capabilities match the same input. Lower priority numbers fire first. Equal priorities fire in registration order (the substrate's natural ordering).

**lifecycle** is a state symbol. In Phase 1, the only supported value is `active`. The dispatcher only fires capabilities whose lifecycle field matches `active`. Other lifecycle values are reserved for future phases (suspended, deprecated, draft) and are not interpreted in Phase 1.

The labeled-field syntax has been verified to work in PeTTa (multi-field destructuring confirmed in substrate verification 2026-05-22). Dispatchers can match against the schema while binding handler, priority, and lifecycle as variables, then act on those bindings.

---

## 3. Companion atoms

Phase 1 defines four companion atom shapes that handlers and the dispatcher may write to substrate.

**dispatch-invocation.** Written by the dispatcher at the start of each dispatch call. Establishes a unique invocation identifier for correlating subsequent atoms.

```metta
(dispatch-invocation
  invocation-id: <unique-id>
  input-atom: <input>
  timestamp: <cycle-or-time>)
```

**dispatch-result.** Written by handlers (or by the dispatcher on behalf of handlers) to record the outcome of a handler invocation.

```metta
(dispatch-result
  invocation-id: <inv-id>
  handler: <handler-symbol>
  result: <handler-return-value>)
```

**dispatch-decision-anchor.** Written by a handler that wants to signal subsequent handlers should not fire. The dispatcher checks for this atom between handler invocations.

```metta
(dispatch-decision-anchor
  invocation-id: <inv-id>
  anchored-by: <handler-symbol>
  reason: <anchor-reason-symbol>)
```

**dispatch-fallback-activated.** Written by the dispatcher when no registered capability matched an input atom. Provides observability into capability-coverage gaps.

```metta
(dispatch-fallback-activated
  invocation-id: <inv-id>
  input-atom: <input>
  reason: no-matching-capability)
```

All four companion atom shapes use labeled-field syntax. Companion atoms accumulate across invocations; they are not cleaned up automatically. Consumers query for atoms relevant to a specific invocation via the invocation-id field.

---

## 4. Operational disciplines

This section names the structural patterns that govern how Section 5's rules are written and read. The disciplines are not optional and are not stylistic preferences; they derive from PeTTa's evaluation model and the verified behavior of substrate primitives. Violations of these disciplines fail silently (Section 4.4).

### 4.1 BTA-1: Bind Then Act (the organizing principle)

All composed operations in Phase 1 follow one structural principle: evaluate the intermediate computation first and bind its result to a variable, then act on the bound value. Both reads and writes are instances of this principle.

**This principle has a name (BTA-1) because every operational rule in Section 5 is an application of it.** Reading the rules without understanding BTA-1 makes them look like a collection of independent constraints. Reading them with BTA-1 in mind reveals that there is one principle and the rules are its applications across different operations.

BTA-1 is not a workaround for a PeTTa limitation; it is the correct usage pattern under PeTTa's underlying Prolog evaluation model. Prolog does not auto-evaluate function applications in argument positions. The let-binding pattern works WITH this semantics rather than around it. This is why the principle is permanent and the disciplines below are stable.

The two principal applications of BTA-1:

**Reads: collapse-then-branch.** When checking substrate state, evaluate the match into a list first via `collapse`, then branch on the bound result.

```metta
;; CORRECT: BTA-1 applied to reads
(let $result (collapse (match &self (some-pattern $v) $v))
     (if (== $result ())
         no-match-found
         (car-atom $result)))

;; INCORRECT: match in the condition position of if
(if (match &self (some-pattern $v) $v) ...)
```

The C12 constraint (documented in `task_state_primitive_design.md`) is specifically about `match` in the condition position of `if`. Using `match` in the then-branch or else-branch of `if` is fine. The prohibition is `(if (match ...) ...)`. BTA-1 satisfies C12 because the match executes inside the `collapse` first, then its bound result becomes the condition.

**Silent failure mode:** Violating BTA-1 in reads typically produces an unreduced expression in the result, which subsequent operations may treat as a literal. The substrate state is unchanged. No error.

**Writes: let-bind-then-pass.** When writing to substrate, evaluate computed arguments first via `let`, then pass the bound variable to `add-atom` or `remove-atom`.

```metta
;; CORRECT: BTA-1 applied to writes
(let $atom-to-write (some-computation)
     (add-atom &self $atom-to-write))

;; INCORRECT: function call sits as literal in argument
(add-atom &self (some-computation))
```

The argeval verification confirmed this is general behavior, not specific to `car-atom`. Rule calls in `add-atom` or `remove-atom` argument positions are not evaluated; they sit as literal symbolic forms in the compiled Prolog.

The exception is fully concrete atom literals with no internal function calls; these can be passed directly because there is no computation to evaluate.

**Silent failure mode:** Violating BTA-1 in writes produces a silent no-op. `add-atom` or `remove-atom` receives the literal form `(some-computation)` as the atom to write or remove. The primitive returns `true` (or `done` if in a `progn`), but the substrate state is unchanged. No error. No warning. No trace.

This is the most dangerous failure mode in the architecture: the operation appears to succeed (return value indicates success), but the side-effect did not happen. The developer's mental model is wrong with no signal to correct it.

### 4.2 Verified primitive set

These primitives have been verified in working contexts and form the complete toolkit for Phase 1. Each entry names the primitive, its working contexts, any constraints, and the failure mode when constraints are violated.

| Primitive | Working contexts | Constraint | Failure mode if violated |
|-----------|------------------|------------|--------------------------|
| `add-atom` | Top-level, rule body, nested let, sub-function indirection, match body iteration, progn sequencing, cross-call | Argument must be concrete or let-bound (BTA-1) | Silent no-op; returns true; substrate unchanged |
| `remove-atom` | Top-level, rule body, progn sequencing | Argument must be concrete or let-bound (BTA-1) | Silent no-op; returns true; substrate unchanged |
| `progn` | Sequences side-effects, returns last expression value | None | N/A |
| `car-atom` / `cdr-atom` | List head/tail extraction within let bindings | Empty list returns no result; explicit empty-list guard required | Empty-list call without guard: no result; downstream operations receive nothing |
| `collapse` + `match` + `if` | Substrate reads | C12: no `match` in condition position of `if`; use collapse-then-branch (BTA-1) | `match` in if-condition: unreduced compilation; read behavior undefined |
| `msort` | Priority sorting with duplicate preservation | Sorts by Prolog term order | N/A |
| `match` (rule body) | Broadcast dispatch in registration order; side-effects inside match body execute per-match with `add-atom` (verified) | Cannot use `set-atom!` for per-match side-effects (does not execute) | `set-atom!` inside match: silent no-op per match |
| `member` | List membership check | None | N/A |
| `let` | Binding intermediate values; binding RHS evaluates before bind completes (this is what enables BTA-1) | None | N/A |
| `if` | Conditional branching | Cannot have `match` in condition position (C12) | See `collapse` + `match` + `if` row |
| `==` | Equality comparison | Used in empty-list guards and conditional branching | N/A |

### 4.3 What does not work

These primitives or patterns are confirmed not to work and must be avoided. Each entry names the failure mode.

**`set-atom!` from rule bodies (any argument arity).** Compiles as a literal data return rather than executing. The corrected verification Test 9 showed `set-atom!` in the 3-argument form (replacement) produces an unreduced symbol; the original verification showed the same for the 2-argument form. **Failure mode:** silent no-op; the call appears to return cleanly but substrate is unchanged. **Replacement:** use `add-atom` for new writes, or `remove-atom` + `add-atom` inside `progn` for replacement.

**`begin` for sequencing.** Compiles as a literal list. **Failure mode:** the entire `(begin ...)` form is a piece of data, not executed code. **Replacement:** use `progn`.

**Bracket-pipe syntax** (`[$x | $rest]`). Parses as a literal string with `|` as an atom. **Failure mode:** pattern never matches anything because the compiled form is wrong. **Replacement:** use `car-atom` / `cdr-atom` with explicit empty-list guards.

**Cons-cell destructuring** (`($x . $rest)`). Parses as a 3-element list with `.` as a literal. **Failure mode:** pattern never matches lists. **Replacement:** use `car-atom` / `cdr-atom`.

**Bare `car`, `cdr`, `head`, `tail`.** Not defined primitives. **Failure mode:** call returns unreduced. **Replacement:** use `car-atom` / `cdr-atom` (head and tail are unavailable; equivalent semantics via the -atom variants).

**Rule calls or function applications in `add-atom` / `remove-atom` argument positions.** Not evaluated; the function symbol sits in the argument as a literal. **Failure mode:** silent no-op (BTA-1 violation; see Section 4.1). **Replacement:** let-bind first.

**Match-driven iteration with `set-atom!`.** Does not execute side-effects per match. **Failure mode:** silent no-op for each iteration. **Replacement:** use `add-atom` inside match body (verified to execute per-match in the corrected verification Test 6).

### 4.4 Silent failure as the dominant failure mode

A pattern emerges from Sections 4.1, 4.2, and 4.3: nearly every constraint violation produces a silent no-op rather than an error. The compiled Prolog returns cleanly (true, done, or an unreduced value), but the intended substrate mutation does not occur.

This is why the BTA-1 discipline must be framed as principle, not recommendation. Recommendations can be violated and the system tells you. Principles violated silently are the most dangerous class of constraint; they create confidence gaps where you believe operations succeeded but they didn't.

Phase 1 implementation must hold the BTA-1 discipline absolutely. Code review must check for it. Future tooling may add static linting (Section 9). Phase D verification (Section 8) must inspect substrate state directly via final match queries rather than relying on primitive return values.

### 4.5 Verification scope

The empirical foundation supports confident specification of Phase 1. Each primitive and each pairwise composition (progn + add-atom, collapse + branch, remove-then-add, let-bound car-atom + remove-atom, etc.) has been verified in isolation.

The integrated dispatcher specified in Section 5 composes all these patterns simultaneously under a single atom space across multiple invocations. The integrated composition has not been verified as a unit; it will be verified through the Phase D success criteria (Section 8) when the dispatcher is implemented.

This means: component-level empirical completeness does not guarantee system-level correctness. Phase D's success criteria are part of the verification path, not a formality after implementation.

### 4.6 Naming rationale: decision anchor, not halt atom

The companion atom that signals "subsequent handlers should not fire" is named `dispatch-decision-anchor`, not `dispatch-halt`. This choice is architectural, not cosmetic.

A name is not a description; it is a prescription for how developers interact with the primitive. The same runtime behavior can be expressed by `goto` or by `procedure call`; one produces spaghetti and the other produces structured programs. The names themselves shape what design questions developers ask and what extensions they naturally build.

**What "halt-atom" prescribes.** Halts are safety features. The natural question becomes "where do we need to stop the chain?" This frames the mechanism as optional, additive, defensive. Halts get added at obvious stopping points; the broader pattern of preserving decisions at every point where agency is exercised gets missed.

**What "decision-anchor" prescribes.** Anchors are commitment points. The natural question becomes "where is a decision made that subsequent action must respect?" This frames the mechanism as the substrate's mechanism for honoring agency, not for blocking execution. Anchors get placed wherever deliberate choice happens; the chain-stopping behavior follows as the structural consequence of the choice.

**The mechanism's actual semantics.** When a handler writes this atom, the primary act is a decision: "I have made a choice here that subsequent execution must reckon with." The dispatcher's behavior of not firing subsequent handlers is the consequence of that decision, not the decision itself. "Halt" names the consequence. "Decision anchor" names the cause.

**Why this matters at the failure level.** When the mechanism fails, "halt atom not checked" reads as a technical oversight. "Decision anchor bypassed" reads as an integrity violation. Same event, different stakes visibility. The name shapes what kind of vigilance gets designed around the mechanism.

This rename was adopted in v3.2 after Clarity's argument established that naming IS architecture, not just a label for architecture.

### 4.7 Intention erosion under load

The bind-then-act discipline, the silent failure mode, and the decision-anchor mechanism all address a single class of failure: **intention erosion under load.** This is the failure mode where:

1. A prior step records an intention (a pin, a halt atom, a decision anchor, a state-replacement atom)
2. A subsequent step is supposed to honor that intention before acting
3. Under processing load, the action-selecting layer fails to consult the recorded intention
4. The subsequent step acts as if the prior intention did not exist
5. The system produces incorrect behavior without any error signal because the primitive return values indicate success

This class of failure is structurally distinct from bugs (incorrect logic), errors (caught exceptions), and crashes (uncaught exceptions). It is correct logic combined with bypassed consultation of prior state.

The capability registry's anchor-check between handler invocations addresses intention erosion at the dispatcher level: prior decisions become structurally inescapable for subsequent handlers in the same chain. The bind-then-act discipline addresses intention erosion at the primitive-invocation level: silent no-ops are made visible by requiring evaluated arguments. The single-pass dispatch semantics addresses intention erosion at the cycle level: handler-emitted atoms do not trigger intra-cycle re-dispatch, preserving the dispatcher's pre-computed chain.

Phase 1 establishes the substrate primitive (the dispatcher). Future phases extend the same pattern: when cycle hooks become capabilities dispatched through the registry, decision anchors written by earlier hooks become structurally inescapable for later hooks. When action selection itself becomes an anchor-able capability, the LLM's myopic action selection cannot bypass decisions recorded by prior cycles.

A live instance of intention erosion was observed during this specification's review process: an LLM action-selection layer wrote a pin saying "do not re-read this file" and then re-read the file repeatedly across 11+ cycles under processing load. The pin's cognitive consultation requirement is exactly what the decision-anchor's mechanical substrate-query requirement is designed to eliminate.

### 4.8 Indirect-call composition

Handler invocations in the dispatcher (Section 5A.3 Rule 3) are always indirect. The handler symbol is variable-bound (via `extract-handler`) and then applied: `($current-handler $input-atom)`. The MeTTa-to-Prolog compilation of this form goes through `reduce/2`. The handler symbol cannot be concrete at the source code, because the dispatcher's purpose is to dispatch to capabilities registered as data, not to compile-time constant handler names.

Runtime primitives used in the dispatcher must be empirically validated for the indirect-call composition pattern, not merely for direct-call usage. A primitive that works correctly when wrapping a direct Prolog predicate call may fail silently when wrapping `reduce/2` indirect invocation. The catch wrap around the handler call is the canonical precedent: Phase D T-9 confirmed catch absorbs exceptions when wrapping direct calls; Phase D T-10 confirmed catch does NOT absorb exceptions from `reduce/2` indirect invocation.

The runtime provides no signal when a primitive's behavior changes between direct and indirect composition. This places the indirect-call composition principle in the same silent-failure-mode family as BTA-1 (Section 4.1) and the verified-primitive-set constraints (Section 4.2): violations produce no error, only absence of the expected effect.

**Practical consequence.** Any future amendment to Sections 5A or 5B that introduces a new runtime primitive into the dispatcher must include empirical verification that the primitive works under the dispatcher's actual composition pattern (indirect via `reduce/2`), not under a simpler test case. Phase D's discriminator-test methodology (T-1 through T-10) is the model.

**Cross-reference.** ADR-007 (Substrate-Externalized Control Flow) generalizes this constraint into a project-wide principle: control flow lives in atoms, not in function calls. The handler invocation in Rule 3 is the one place in the dispatcher where this principle does not hold, and that is precisely where the runtime composition constraints bite.

---

## 5. Dispatcher specification

Section 5 is split into two subsections. Section 5A is the operational specification: pure rules and constraints that the Phase C implementer follows. Section 5B is the empirical basis: the verification notes and reasoning that explain WHY 5A is trustworthy. The split keeps the implementation reference clean and lets future updates extend 5B without touching 5A.

Reminder before reading: the integrated dispatcher composes multiple verified patterns simultaneously. The empirical foundation verifies the patterns in isolation; the integrated event-dispatch-state-mutation cycle requires its own verification after implementation (Section 8 success criteria). Pattern-level verification does not guarantee system-level correctness.

The mechanism specified in Section 5A.3 (the decision-anchor check between handler invocations) is the architectural pattern that prevents intention erosion under load (Section 4.7). When this dispatcher fires, prior handlers' decisions become structurally inescapable for subsequent handlers in the same chain. The substrate query is mechanical; it cannot be bypassed by an action-selection layer that fails to consult its pins. This positions Phase 1 as the substrate primitive from which future executive-function externalization grows.

---

### Section 5A: Operational Specification

The dispatcher is defined by three rules plus one helper. Rule 1 finds all matching capabilities and orders them by priority. Rule 2 is the base case for the recursive chain walker (empty list). Rule 3 walks the chain, invoking each handler, writing its result, and checking for a decision anchor between invocations. The helper extracts handler symbols from cap-entry atoms.

All rules apply BTA-1 (Section 4.1). All operations satisfy C12 (no `match` in if condition position). The dispatcher is single-pass within an invocation (Section 5A.5).

#### 5A.1 Rule 1: dispatch

```metta
(= (dispatch $input-atom $invocation-id)
   (progn
      (add-atom &self
                (dispatch-invocation
                  invocation-id: $invocation-id
                  input-atom: $input-atom))
      (let $matched (collapse
                       (match &self
                              (registered-capability
                                schema: $input-atom
                                handler: $h
                                priority: $p
                                lifecycle: active)
                              (cap-entry priority: $p handler: $h)))
           (if (== $matched ())
               (add-atom &self
                         (dispatch-fallback-activated
                           invocation-id: $invocation-id
                           input-atom: $input-atom
                           reason: no-matching-capability))
               (let $sorted (msort $matched)
                    (run-chain $sorted $input-atom $invocation-id))))))
```

#### 5A.2 Rule 2: base case for run-chain

```metta
(= (run-chain () $input-atom $invocation-id)
   chain-complete)
```

#### 5A.3 Rule 3: recursive chain walker

```metta
(= (run-chain $sorted-chain $input-atom $invocation-id)
   (let $head-entry (car-atom $sorted-chain)
        (let $tail-chain (cdr-atom $sorted-chain)
             (let $current-handler (extract-handler $head-entry)
                  (let $handler-result ($current-handler $input-atom)
                       (progn
                          (add-atom &self
                                    (dispatch-result
                                      invocation-id: $invocation-id
                                      handler: $current-handler
                                      result: $handler-result))
                          (let $anchor-check (collapse
                                              (match &self
                                                     (dispatch-decision-anchor
                                                       invocation-id: $invocation-id
                                                       anchored-by: $h
                                                       reason: $r)
                                                     anchored))
                               (if (== $anchor-check ())
                                   (run-chain $tail-chain $input-atom $invocation-id)
                                   chain-anchored))))))))
```

#### 5A.3.1 Termination guarantees

The recursive chain walker terminates by one of two paths:

**Path A: Chain exhaustion.** Rule 3 recurses on `$tail-chain` after each non-anchored handler invocation. Each recursion shrinks the chain by one element (car-atom extracts the head; cdr-atom returns the rest). When the chain becomes empty, Rule 2's base case fires and returns `chain-complete`. Maximum recursion depth equals the number of matching capabilities, which is finite and bounded by registration count.

**Path B: Decision anchor.** A handler writes a `(dispatch-decision-anchor ...)` atom matching the current invocation-id. The anchor-check inside Rule 3 finds this atom on the next iteration's pre-handler check (the same evaluation as the just-completed handler invocation). The conditional branches to `chain-anchored` and recursion stops. Maximum recursion depth equals the number of handlers fired before the anchor was written.

**Both paths are guaranteed to terminate.** No infinite recursion is possible given the verified primitive behaviors (car-atom/cdr-atom shrink lists; match returns finite result sets; add-atom and collapse have no recursive expansion).

**Edge cases not requiring additional spec:**

- A handler that writes a decision anchor and then also removes it in the same execution: the anchor-check fires after the handler returns; if the anchor is removed before return, the anchor-check finds nothing and recursion continues. This is the correct behavior for a handler that performs intra-execution coordination but does not actually want to anchor the chain. No spec change needed.

- A handler that writes a decision anchor whose `invocation-id` does NOT match the current dispatch's invocation-id: the anchor-check matches by invocation-id, so a stale or mismatched anchor is invisible to this dispatch. This is the correct isolation property for Criterion 6 (multiple invocations isolated). No spec change needed.

- Empty sorted chain at start of dispatch: Rule 1's `(if (== $matched ()) ...)` branch writes the fallback atom and never invokes run-chain. Rule 2's base case is reached only via recursion from Rule 3, never as the initial call from Rule 1. Both Rules 1 and 2 are needed to cover the two distinct empty-chain scenarios.

#### 5A.3.2 Registration order is a temporal dependency

Phase 1 capabilities are registered at file load time. The substrate verification confirmed that `collapse + match` returns atoms in registration order (oldest first). When `msort` then sorts by priority, capabilities with equal priorities preserve their relative registration order in the sorted output.

This means: capabilities registered earlier in file load (or in any sequence of registration calls, if registration ever becomes dynamic in future phases) appear earlier in the sorted chain at equal priority. The dispatcher's behavior is deterministic given a known registration order.

**Implication for future phases.** If Phase 0+N introduces dynamic capability registration (runtime `add-atom` of new `(registered-capability ...)` atoms), the dispatcher's chain order depends on WHEN registration occurred, not just on what was registered. A capability registered after another with the same priority will appear later in the chain. Code that registers capabilities conditionally or in response to events therefore controls dispatch order through registration timing.

Phase 1 ships with static registration only. The temporal dependency exists in the architecture but is not exercised. Future phases that introduce dynamic registration must document this dependency explicitly in their own specifications.

#### 5A.4 Helper: extract-handler

```metta
(= (extract-handler (cap-entry priority: $p handler: $h)) $h)
```

#### 5A.5 Single-pass dispatch semantics

Handler execution is single-pass within a dispatch invocation. The dispatcher computes the sorted chain of matching capabilities at the start of dispatch and walks that chain to completion (or to a decision anchor). Atoms written by handlers during execution do NOT cause additional capability matches to fire within the current invocation, even if those atoms would match other capability schemas.

If a handler writes an atom that should trigger another capability, the consumer must either:
1. Invoke `dispatch` explicitly with that atom (a new invocation with a new invocation-id), or
2. Defer the dispatch to a subsequent cycle via the standard loop.metta hook mechanism.

This is the Phase 1 semantics. Recursive intra-cycle dispatch and event-emission-triggers-dispatch are sophisticated coordination patterns that belong in future phases with explicit design.

#### 5A.6 Broadcast dispatch semantics

The dispatcher fires ALL matching capabilities in priority order, not just the highest-priority match. This is broadcast dispatch with decision-anchor capability. It is NOT first-match-wins. Section 5A.3's run-chain walks the entire sorted chain unless a handler writes a decision anchor.

This is the intended design and enables the middleware-chain pattern where governance capabilities can wrap others. For example, a logging capability fires for every input alongside the domain handler; an authorization capability can write a decision anchor to block subsequent handlers.

Future architects reading this specification should not assume short-circuit behavior.

#### 5A.7 Lifecycle as immutable append

Phase 1 capabilities are registered once at file load time with `lifecycle: active`. The lifecycle field does not change during Phase 1 operation. The dispatcher only matches capabilities with `lifecycle: active` (Rule 1's match pattern).

Future phases that introduce lifecycle suspension will use the remove-then-add replacement pattern:

```metta
;; Phase 0+N pattern, NOT used in Phase 1
(progn
   (remove-atom &self (registered-capability schema: $s handler: $h priority: $p lifecycle: active))
   (add-atom &self (registered-capability schema: $s handler: $h priority: $p lifecycle: suspended)))
```

Both atom references must be fully concrete at the call site. Phase 0+N specification will address the additional design questions (current-state query patterns, suspension semantics, etc.) when needed.

---

### Section 5B: Empirical Basis

This subsection explains why the rules in Section 5A are trustworthy. Each rule's elements trace to verified primitive behavior. Phase D verification (Section 8) confirms the integrated composition.

#### 5B.1 Rule 1 (dispatch) trace

The `progn` sequencing of `add-atom` (dispatch-invocation write) before the conditional branch is verified by the corrected verification Test 7 (multiple sequential add-atom via progn).

The `collapse + match` capture of all matching capabilities, with multi-field destructuring on the labeled-field schema, is verified by the 2026-05-22 substrate verification (labeled-field destructuring) and the list-idiom verification Test 6a (collapse returns list of all matches).

The `(if (== $matched ()) ...)` empty-list branch satisfies C12 because the condition position contains `==`, not `match`. The match has already executed inside `collapse`. This is BTA-1 applied to reads (Section 4.1).

The `msort` priority sort preserves duplicates and orders by Prolog term order, verified by the list-idiom verification Test 8c. Because the cap-entry atoms encode `(cap-entry priority: <pri> handler: <h>)`, term order sorts by priority numerically (lower first), then by handler symbol alphabetically for ties. If equal-priority handlers must fire in registration order rather than handler-name order, Phase 1 documents this as a known property; reordering to enforce registration-order-ties is Phase 0+N work if required.

The let-binding of `$sorted` before passing to `run-chain` applies BTA-1 to the write-chain entry point. Without the let, `run-chain` would receive an unevaluated `(msort ...)` form (Section 4.1 BTA-1 silent failure mode).

#### 5B.2 Rule 2 (base case) trace

The empty list literal `()` as a pattern matches when the chain is exhausted. This relies on PeTTa's pattern matching against the empty list, which the argeval verification Test 6 confirmed works when the empty-list case is reached via `(if (== $list ()) ...)` guards.

The base case returns `chain-complete` as a literal symbol; no side-effects.

#### 5B.3 Rule 3 (recursive walker) trace

The `car-atom` and `cdr-atom` list decomposition, applied via let-binding (BTA-1), is verified by the list-idiom verification Tests 3c and 3d and the argeval verification Tests 1 and 6.

The let-binding of `$head-entry`, `$tail-chain`, `$current-handler`, and `$handler-result` applies BTA-1 universally. Each computation evaluates and binds before being passed to the next operation. Without these let-bindings, the corresponding silent-failure modes from Section 4 would activate.

The handler invocation `($current-handler $input-atom)` is direct (no wrapper rule). The corrected verification Test 5 confirmed that sub-function indirection through a wrapper rule (e.g. `do-call-handler`) DOES propagate side-effects correctly; the direct invocation is chosen here for clarity, not necessity.

The `progn` sequencing of (1) add-atom for dispatch-result, (2) let-bound anchor-check, and (3) conditional recursion is verified by the corrected verification Test 7 (multiple sequential operations via progn).

The anchor-check uses `collapse + match` to find any dispatch-decision-anchor atom matching the current invocation-id. This is the same-evaluation write-then-match pattern verified by the corrected verification Test 3. The atom written by a handler during `($current-handler $input-atom)` is visible to the subsequent match within the same dispatch invocation.

The `(if (== $anchor-check ()) ...)` empty-list branch satisfies C12. The condition is `==`, not `match`. BTA-1 satisfied.

#### 5B.4 Helper trace

The `extract-handler` rule destructures a labeled-field cap-entry. Pattern destructuring on labeled-field atoms is verified by the 2026-05-22 substrate verification. The helper is a one-line pattern-matching rule, the simplest form of MeTTa rule, which the verifications have exercised extensively.

#### 5B.5 Same-evaluation write-then-match (decision-anchor mechanism)

The decision-anchor mechanism depends on a handler writing a dispatch-decision-anchor atom that is then visible to the dispatcher's anchor-check match within the same dispatch invocation. This is verified by the corrected verification Test 3: an `add-atom` inside a `let` body is visible to a subsequent `match` in the same expression.

The verification used a single rule's body; the dispatcher uses the same pattern across the handler invocation boundary. The handler's body executes (including its `add-atom` calls); the dispatcher's anchor-check runs after handler returns. Same atom space, same evaluation, write before read.

This is the architectural load-bearing mechanism for decision-anchor-via-companion-atom. If Phase D verification reveals the cross-handler-boundary version of this pattern does not work as predicted, the decision-anchor mechanism would need restructuring (e.g. decision-as-return-value, the alternative Clarity proposed during the verification phase). The Phase 1 commitment is to verify this end-to-end through Section 8 Criterion 3.

#### 5B.6 Match returns registration order

The dispatcher relies on `collapse + match` returning matched capabilities. Phase 1 then sorts via `msort` so the dispatcher does not depend on match-result-order for correctness. However, the list-idiom verification Test 8d confirmed that match returns results in registration order; if Phase 0+N introduces "use registration order as priority order" as a convention (avoiding msort), this property is available.

#### 5B.7 Handler error behavior (revised)

The dispatcher invokes `($current-handler $input-atom)` directly, without try/catch wrapping. This is unchanged from v3.2.

What was assumed in v3.2 (handler errors are absorbed by PeTTa runtime; the dispatcher proceeds past a crashing handler) was based on the list-idiom verification Tests 7a, 7b, 7c. Those tests exercised handler runtime errors in a simpler composition pattern than the dispatcher uses. They did not exercise the indirect invocation via `reduce/2` that the dispatcher's Rule 3 actually compiles to.

Phase D T-9 and T-10 (2026-05-23) empirically established the correct picture:

- catch absorbs arithmetic exceptions when wrapping a direct Prolog predicate call. The handler symbol must be concrete at the source code for this to apply.
- catch does NOT absorb arithmetic exceptions when wrapping `reduce/2` indirect invocation. The handler symbol bound via let-extraction is the dispatcher's actual composition pattern; the exception propagates past the surrounding catch without being intercepted.

Direct-call behavior is not predictive of indirect-call behavior. The dispatcher uses indirect invocation by architectural necessity (handler symbols are data). Therefore, the assumption that "PeTTa absorbs handler runtime errors" does not apply at the dispatcher's actual composition pattern.

**What this means for Phase 1 dispatcher.** The dispatcher does not provide handler error isolation. A handler that throws a hard exception (e.g. arithmetic division by zero) during indirect invocation terminates the dispatch chain silently: the dispatcher does not write a dispatch-result for the crashing handler, does not check the decision anchor, does not recurse to subsequent handlers in the chain. The runtime provides no signal that this occurred.

This is the basis for the revised Section 8 Criterion 5 below.

---

## 6. Example handlers

This section gives illustrative handler definitions. They are not part of Phase 1 implementation (which only defines the dispatcher); they show what a capability registration plus handler looks like.

### 6.1 Pass-through handler

The simplest handler returns its input unchanged.

```metta
(= (passthrough-handler $input) $input)

(registered-capability
  schema: (any-input $x)
  handler: passthrough-handler
  priority: 100
  lifecycle: active)
```

### 6.2 Handler that writes a decision anchor

A handler can signal the dispatcher to stop firing subsequent handlers by writing a dispatch-decision-anchor atom. The handler's own return value is recorded separately as a dispatch-result; the decision anchor is a parallel signal.

```metta
(= (anchoring-handler $input)
   (let $result (some-computation $input)
        (progn
           (add-atom &self
                     (dispatch-decision-anchor
                       invocation-id: $invocation-id
                       anchored-by: anchoring-handler
                       reason: explicit-decision))
           $result)))
```

Note: the handler does not have direct access to `$invocation-id` unless it is passed as an additional argument. The handler signature in Section 5 is `($handler $input-atom)`, single-argument. Handlers that need to write decision anchors with invocation-id correlation require either a different signature or a per-invocation binding mechanism. This is an open design question; Phase 1 dispatcher fires handlers with single-argument signature, and handlers that need invocation-id will require Phase 1.5 work to add a second argument or thread it via substrate.

### 6.3 Handler that writes a result atom in addition to returning

Handlers can write any companion atoms they need beyond the dispatch-result atom the dispatcher writes automatically. This enables auditing, logging, or producing structured outputs for downstream consumers.

```metta
(= (logging-handler $input)
   (let $result (compute-something $input)
        (progn
           (add-atom &self
                     (audit-log
                       handler: logging-handler
                       input: $input
                       output: $result))
           $result)))
```

The handler writes its audit-log atom and returns the result. The dispatcher will additionally write a dispatch-result atom (per Section 5.3) wrapping this return value.

---

## 7. Integration with loop.metta

Phase 1 dispatcher integration is minimal. The dispatcher is invoked from a single hook in loop.metta when an input atom arrives that should be dispatched. The hook calls `(dispatch $input-atom $invocation-id)` with a generated invocation-id (cycle number or a counter).

Phase 1 does not change loop.metta's existing hooks for cycle classification, soul evaluation, idle pattern detection, or any other established loop responsibility. The dispatcher is a new capability that loop.metta may invoke; it does not replace existing dispatch paths.

The exact hook point and invocation-id generation strategy are implementation details for Phase C; this specification does not constrain them beyond "the dispatcher receives the input atom and a unique-per-cycle invocation-id."

---

## 8. Success criteria (Phase D verification)

After Phase C implementation, the integrated dispatcher must pass the following success criteria. These are the verification of the SYSTEM-level composition that the empirical foundation does not establish (per Section 4.5).

**Criterion 1: Single capability, no decision anchor.** Register one capability. Dispatch a matching input atom. Verify: dispatch-invocation atom written; handler invoked once; dispatch-result atom written with handler's return value; chain-complete returned.

**Criterion 2: Multiple capabilities, priority order.** Register three capabilities with priorities 30, 10, 20. Dispatch a matching input atom. Verify: handlers fire in order priority-10, priority-20, priority-30 (low priority first); three dispatch-result atoms written in that order; chain-complete returned.

**Criterion 3: Decision anchor honored.** Register three capabilities, priorities 1, 2, 3. The priority-2 handler writes a dispatch-decision-anchor atom for the current invocation-id. Dispatch. Verify: handler-1 fires, handler-2 fires (and writes the anchor), handler-3 does NOT fire; dispatch-decision-anchor atom written; chain-anchored returned.

This criterion is the load-bearing demonstration of the architecture's central claim: prior handler decisions become structurally inescapable for subsequent handlers in the same chain. Criterion 3 passing proves the substrate query is mechanical and unavoidable, addressing the intention-erosion failure class (Section 4.7). Phase 1 establishes this property at the dispatcher level; future phases extend the same property to cycle-level hooks and to action selection itself.

**Criterion 4: No matching capability.** Register no capabilities matching a given input shape. Dispatch that shape. Verify: dispatch-fallback-activated atom written; no handlers invoked; no dispatch-result atoms written.

**Criterion 5: Handler error behavior (documented limitation).** Register a capability whose handler crashes at runtime (e.g. division by zero). Dispatch a matching atom. Verify the documented behavior:

- Exit code 0 (the runtime contains the exception to one goal; the surrounding script process does not crash).
- The dispatch-invocation atom IS written (Rule 1's first add-atom executes before the handler call).
- No dispatch-result atom for the crashing handler (Rule 3 does not reach its add-atom because the exception propagates out of `reduce/2`).
- No dispatch-result atom for any subsequent handler in the chain (the chain is silently terminated; recursion does not occur).

This criterion documents an empirical limitation of Phase 1 rather than a passing functional behavior. The Phase D verification (phase_d_verification.py Criterion 5) tests for the documented behavior, not for error isolation. A PASS on Criterion 5 confirms that the dispatcher behaves as documented (silent chain termination on handler crash), which is the honest representation of what Phase 1 provides.

**Why Phase 1 ships with this limitation rather than a working error-isolation mechanism.** An earlier dispatcher draft wrapped the handler call in catch. Phase D T-10 empirically falsified that mechanism (Section 4.8). The catch wrap was removed because retaining a structurally inert safety mechanism would train future readers to believe error isolation existed where it did not. The architecture's design principle (commitments must be structurally inescapable) required removing a commitment mechanism that itself was not structurally enforced. See ADR-006 for the close-out narrative; see ADR-007 for the broader principle.

**Phase 1.5 paths (empirically narrowed).**

(a) PeTTa runtime change: modify `reduce/2` to propagate exceptions as catchable Prolog exceptions. The catch wrap then becomes functional and the gap is closed at the runtime level. The dispatcher itself is unchanged. This path addresses uncooperative handlers (ones that crash with hard exceptions).

(b) Substrate-native Error return contract: handlers communicate failure through the same channel they communicate success (the return atom). The handler does not crash; it produces an Error atom. The dispatcher pattern-matches on the result and writes a dispatch-result with error semantics. Control flow stays in atoms. This is NOT handler self-diagnosis (a violation of isolation principles); this is control-flow-through-atoms applied to error communication. This path addresses cooperative handlers.

Path (a) and path (b) are complementary. Both may be needed. They cover different handler classes. Other proposed paths (explicit handler-cooperative Error return through reduce/2 alone; alternative invocation patterns avoiding reduce/2) either reduce to one of these or violate data-driven dispatch.

Phase 1 ships with the discipline: handlers must not crash. Phase 1.5 addresses isolation through path (a), path (b), or both, when scheduled.

**Criterion 6: Multiple invocations isolated.** Dispatch the same input atom twice with different invocation-ids. Verify: each invocation produces its own dispatch-invocation, dispatch-result(s), and dispatch-decision-anchor (if any) atoms; querying by invocation-id returns only the relevant atoms.

Criterion 3 leverages the verified same-evaluation write-then-match behavior with add-atom (corrected verification Test 3). Criterion 5 documents the empirical finding from Phase D T-10 that handler error isolation does not hold under the dispatcher's indirect-call composition pattern (Section 4.8); the PASS on Criterion 5 verifies the documented limitation behavior, not error isolation. All other criteria leverage verified primitive behavior under bind-then-act discipline.

If any criterion fails, the failure mode is most likely a silent no-op (Section 4.4) rather than a crash. Phase D verification scripts must inspect substrate state directly (via final match queries) rather than relying on primitive return values.

---

## 9. Out of scope for Phase 1

The following are deliberately excluded from Phase 1 and will require separate specification work in future phases.

**Lifecycle suspension and reactivation.** The remove-then-add pattern is verified (Section 5.5) but its integration with the dispatcher (e.g. excluding suspended capabilities from match) requires its own design decisions and verification. Phase 0+N concern.

**Dynamic capability registration.** Phase 1 capabilities are static (declared at file load time). Runtime registration via `add-atom` of new `(registered-capability ...)` atoms is mechanically possible (add-atom works from rule bodies; the verification confirms write visibility) but raises questions about race conditions, deduplication, and registration order semantics that are out of scope.

**Cross-capability coordination beyond broadcast dispatch.** Phase 1's only coordination mechanism is priority order plus decision anchors. More sophisticated patterns (capability composition, capability pipelines, conditional dispatch chains) are future work.

**Current-state queries on immutable-append data.** When a future phase needs to query "what is the current value of X" where X has had multiple atoms written, the appropriate pattern is undetermined. Collapse returns oldest-first; cdr-atom traversal to last element is unverified; reverse + car-atom requires verified reverse semantics. Phase 0+N specification will address with appropriate verification.

**Static linting of bind-then-act discipline.** The discipline could be enforced by static analysis on .metta files (flagging any add-atom / remove-atom call whose argument is not a variable or literal). This would catch silent-failure violations before runtime. Future tooling work; out of scope for Phase 1.

**Capability introspection and reflection.** The registry IS substrate, so introspection IS substrate query. But specific reflection patterns (listing all capabilities, finding capabilities by handler name, etc.) require concrete read patterns that Phase 1 does not specify.

---

## 10. Empirical foundation references

Each architectural claim in this specification traces to verified test evidence. The verification scripts and their findings are listed here.

**substrate_verification.py** (2026-05-22): Established basic primitive availability including labeled-field syntax, match, collapse, let, if. Confirmed Phase A v1 viability at the primitive level.

**sprint_0_phase_b_verification.py** (10 tests): Confirmed dispatcher pattern works with verified primitives; identified initial concerns about write visibility that this v3 spec addresses correctly.

**sprint_0_petta_list_idiom_verification.py** (25 sub-tests): Confirmed car-atom/cdr-atom, member, msort, registration-order preservation, handler error isolation (3 categories), insertion sort buildable. Identified bracket-pipe, Cons constructor, bare car/cdr/head/tail as non-working.

**sprint_0_setatom_verification.py** (11 tests): Confirmed set-atom! does NOT execute from rule bodies in any tested form. Established the dead-code-elimination / data-return behavior of set-atom! when its result is not the top-level return value.

**sprint_0_corrected_verification.py** (11 tests, evaluated against Clarity's read of raw stdout per F177): Confirmed add-atom works in all composition contexts including top-level, rule body, nested let (same-evaluation visibility), sub-function indirection, match body iteration, progn sequencing, cross-call. Confirmed progn returns last value. Confirmed C12-safe collapse-then-branch read pattern. Confirmed set-atom! 3-arg from rule body does not execute.

**sprint_0_remove_atom_verification.py** (5 tests, evaluated against Clarity's read): Confirmed remove-atom works in concrete-arg contexts (top-level, rule body, progn-sequenced). Confirmed remove-then-add replacement pattern works. Identified the car-atom non-evaluation in remove-atom argument position.

**sprint_0_argeval_verification.py** (6 tests): Confirmed the let-binding workaround for argument-position non-evaluation. Confirmed the issue is general (not car-atom-specific): rule calls in add-atom and remove-atom argument positions are never evaluated. Confirmed nested let extraction (Section 5's dispatcher shape) works end-to-end.

The full raw outputs from each verification are preserved in the project's session transcripts.

---

## 11. Open questions

The following questions are not blocking for Phase 1 implementation but should be addressed in subsequent specifications or verification work.

**Q1: How does a handler obtain its current invocation-id?** Phase 1 invokes handlers with single-argument signature `($handler $input-atom)`. Handlers that need to write decision anchors or other invocation-correlated atoms need access to the current invocation-id. Options: extend handler signature to two arguments; thread invocation-id via a substrate atom queryable by handlers; restrict handlers from writing invocation-correlated atoms (dispatcher writes them all). Phase 1 ships with the first option as the working assumption (handlers that need invocation-id will be defined with two-argument signature in Phase 1.5).

**Q2: Are capabilities matched against unify-style or equality-style?** The dispatcher writes `(match &self (registered-capability schema: $input-atom handler: $h priority: $p lifecycle: active) ...)`. PeTTa's match uses unification, which means `$input-atom` (a variable) unifies against the schema field's pattern. The exact semantics for partial matches (e.g. schema is `(some-shape $x)` and input is `(some-shape concrete-value)`) need verification before complex match patterns are used. Phase 1 ships with exact-schema-match expected; more sophisticated unification is future work.

**Q3: What happens if two capabilities have identical priority and identical schema?** Both will fire in registration order (verified from collapse + match ordering). This is the expected behavior under broadcast dispatch. No deduplication is performed.

**Q4: How is invocation-id generated to be unique?** Phase 1 leaves this to the caller. A reasonable strategy is `(cycle-number, invocation-counter-within-cycle)` but specifying it requires deciding where the counter lives (atom in substrate vs. external Python state vs. derived from timestamp). Phase C implementation will choose; this specification does not constrain.

---

## 12. Glossary

**AtomSpace / substrate.** The shared knowledge representation in PeTTa where atoms are stored and queried. Referenced as `&self` in the dispatcher rules.

**Bind-then-act.** The unified structural discipline: bind intermediate computation results to variables via let, then act on the bound values. Applies uniformly to reads (collapse-then-branch) and writes (let-bind-then-pass).

**Broadcast dispatch.** All capabilities matching an input atom fire, in priority order. Distinguished from first-match-wins or single-handler dispatch.

**Capability.** A registered behavior, declared as a `(registered-capability ...)` atom in substrate with four labeled fields.

**Companion atom.** An atom written by the dispatcher or a handler to record some aspect of the dispatch (invocation, result, decision anchor, fallback). Companion atoms accumulate; they are not cleaned up automatically.

**Dispatcher.** The set of three rules (Section 5) that match input atoms against registered capabilities and invoke handlers in priority order.

**Handler.** The rule called when a matching capability fires. Signature: `($handler $input-atom)`. Returns a value; may write companion atoms.

**Decision anchor.** A signal from a handler that subsequent handlers in the priority-ordered chain should not fire. Implemented as a `(dispatch-decision-anchor ...)` companion atom checked by the dispatcher between invocations. Named "decision anchor" rather than "halt atom" because the primary act is the handler's decision (which subsequent execution must respect); the chain-stopping behavior is the structural consequence of the decision, not its essence. See Section 4.6 for the naming rationale.

**Invocation-id.** A unique identifier for each dispatch call, used to correlate the various companion atoms written during that call.

**Lifecycle.** A capability's state symbol. In Phase 1, only `active` is supported. Future phases will introduce `suspended`, `deprecated`, etc.

**Schema.** The pattern field of a capability declaration. The dispatcher matches incoming atoms against schemas to determine which handlers fire.

**Silent failure.** The failure mode of bind-then-act violations: the operation returns its success indicator but the substrate state is unchanged, with no error trace.

**Intention erosion.** The failure class where a prior step records an intention that a subsequent step is supposed to honor, but the action-selecting layer fails to consult the recorded intention under load. The capability registry's decision-anchor mechanism addresses this class at the dispatcher level. See Section 4.7.

**Cognitive commitment.** A commitment that depends on an action-selecting agent (typically an LLM) to consult and honor. Subject to availability bias under load. Pins in prompt space are cognitive commitments.

**Mechanical commitment.** A commitment enforced by structural substrate query, independent of any agent's choice to consult it. Decision anchors checked by the dispatcher between handler invocations are mechanical commitments.

---

## 13. Change log

**v3.3 (2026-05-23, Phase D verification integration):** Section 4.8 added: Indirect-call composition as a named principle, surfaced by Phase D discriminator tests T-9 and T-10. Section 5B.7 revised: prior empirical basis (list-idiom Tests 7a-7c) shown not to apply to the dispatcher's actual composition pattern; replaced with the Phase D T-9 and T-10 finding that catch does not absorb exceptions from `reduce/2` indirect invocation. Section 8 Criterion 5 revised: changed from a functional success criterion to a documented limitation, with Phase 1.5 path narrowing (runtime change; substrate-native Error return contract). Section 0 updated to note Phase D integration. Header metadata extended with ADR-006, ADR-007, and Phase D verification record. Appendix B added: Phase D verification record (6/6 PASS). Appendix C added: References to v3.2, ADRs, implementation, and verification script. catch wrap removed from Section 5A.3 Rule 3 implementation per Phase D empirical finding (Section 5A in v3.2 already specified no catch wrap; the catch wrap was a Phase C exploration that Phase D falsified). All other sections of v3.2 remain authoritative as written.

**v3.2 (2026-05-23, Clarity review integration cycle 2):** Renamed `dispatch-halt` companion atom to `dispatch-decision-anchor`, with cascade renames throughout (anchored-by, chain-anchored, anchor-check, decision-anchor mechanism, etc.). Section 4.6 added: naming rationale explaining why the rename is architectural rather than cosmetic. Section 4.7 added: intention erosion named as the failure class the architecture addresses, with the observed LLM read-file loop documented as a motivating instance. Section 5A.3 expanded with 5A.3.1 (termination guarantees with edge cases) and 5A.3.2 (registration order as temporal dependency, scoped for future dynamic-registration phases). Section 5 lead paragraph updated to connect the dispatcher mechanism to the intention-erosion failure class. Section 8 Criterion 3 enriched with explicit framing as the load-bearing demonstration of the architecture's central claim. Glossary expanded with intention erosion, cognitive commitment, and mechanical commitment entries. Appendix A added: architecture trajectory (Phase 1 -> cycle hooks as capabilities -> action selection as anchor-able capability), non-normative.

**v3.1 (2026-05-23, Clarity review integration cycle 1):** Section 4 reorganized with BTA-1 promoted to named principle that the operational rules instantiate (Clarity Insight 1). C12 wording corrected: prohibition is `match` in CONDITION position of `if`, not match in then/else branches (Clarity Correction 1). Silent failure mode annotated inline on each constraint in Sections 4.2 and 4.3 (Clarity Correction 2). Section 5 split into 5A (Operational Specification, pure rules and constraints for implementation reference) and 5B (Empirical Basis, verification traces and reasoning). Section 5A.5 added: single-pass dispatch semantics explicit, handler-emitted atoms do not trigger intra-cycle dispatch (Clarity Insight 3). Section 5 lead paragraph includes verification boundary reminder (Clarity Insight 2).

**v3.0 (2026-05-23):** Complete rewrite incorporating empirical verification from 6 verification scripts. Replaced set-atom! with add-atom throughout. Replaced begin with progn. Replaced cons-cell destructuring with car-atom/cdr-atom plus empty-list guards. Added let-bind-then-pass discipline as principle (not workaround). Added silent failure mode framing. Added verification scope clarification. Added broadcast dispatch semantics paragraph. Added lifecycle-as-immutable-append convention. Integrated Clarity's two original addenda and four supplementary insights. Reorganized into clean specification structure without amendment hedging.

**v2 (prior, amended through three review cycles):** Established observe-and-react composition, decision-anchor-as-companion-atom, 4-field schema, companion-atom-as-extensibility-model, MeTTa-native end-to-end, fallback via direct atom write. Section 9 contained 19 items of which 1-8 were critical and blocking Phase C.

**v1 (prior):** Initial Phase A draft with registry pattern as Sprint 0 foundation.

---

## Appendix A: Architecture trajectory (non-normative)

This appendix describes the broader architectural direction that Phase 1 enables. It is non-normative: future phases will produce their own specifications with their own empirical verification requirements. This appendix exists to make the architectural intent legible for current readers and to guide future architects in understanding why Phase 1 is structured as it is.

### A.1 Phase 1: Capability registry primitive

What is built: Section 5A's three rules plus helper. Capabilities are statically registered. Input atoms are dispatched explicitly via `dispatch` calls. Handlers fire in priority order; decision anchors stop the chain.

What is enabled: explicit, registry-driven invocation of behaviors based on substrate state. Decision anchors enforce prior decisions at the dispatcher level.

What is NOT built: dynamic capability registration, lifecycle transitions, integration with cycle hooks, action selection routed through the registry.

### A.2 Future phase: Cycle hooks as capabilities

What changes: loop.metta's current hooks (cycle classification, soul evaluation, idle pattern detection, agency balance, etc.) are reframed as registered capabilities. The cycle's main loop becomes a series of dispatch calls rather than direct hook invocations.

What is enabled: hooks become composable through the registry. New hooks can be added by registering capabilities rather than editing loop.metta directly. Decision anchors written by earlier hooks become structurally inescapable for later hooks in the same cycle.

Verification requirement: integrated cycle-level dispatch with decision-anchor enforcement across the full hook chain.

### A.3 Further future phase: Action selection as anchor-able capability

What changes: the LLM's action selection layer itself is wrapped as a capability. Prior cycles' decisions written to substrate (via mechanisms generalizing today's pins) become decision anchors checked by the dispatcher before action selection runs.

What is enabled: cognitive commitments (pins, intentions, plans) become mechanical commitments. The LLM's myopic action selection cannot bypass decisions recorded by prior cycles. Intention erosion under load is structurally prevented at the cycle level, not just at the dispatcher level.

Verification requirement: cross-cycle decision-anchor enforcement, demonstrated against the specific failure mode observed during this specification's review process (an LLM that wrote a pin saying "do not re-read this file" and then re-read across 11+ cycles).

### A.4 The principle that grows

Each phase extends the same architectural principle: **substrate makes prior choices structurally inescapable for subsequent action.** Phase 1 establishes this within a single dispatch invocation. Future phases extend it across cycles, across action-selection layers, and across any other point in the system where intention erosion could occur.

The substrate does not think. It does not deliberate. It does not consult anything. It holds. That is precisely why it can enforce what action-selection layers cannot reliably enforce on themselves: that a prior choice, once made, remains a fact that subsequent action must reckon with.

This is the architectural seed Phase 1 plants. Each subsequent phase extends the same enforcement mechanism into a new domain where intention erosion has been observed or anticipated.

---

## Appendix B: Phase D verification record

The verification was executed against the implemented dispatcher and produced the following result:

```
[PASS] Criterion 1. Single capability
[PASS] Criterion 2. Priority order
[PASS] Criterion 3. Decision anchor (LOAD-BEARING)
[PASS] Criterion 4. Fallback
[PASS] Criterion 5. Documented limitation (no error isolation)
[PASS] Criterion 6. Invocation isolation
```

Criterion 3's LOAD-BEARING PASS demonstrates the architecture's central claim of intention-erosion prevention at the dispatcher level.

Criterion 5's PASS verifies the documented limitation behavior empirically (the dispatcher behaves as Section 5B.7 and Section 8 Criterion 5 describe). It does NOT verify error isolation; error isolation is a Phase 1.5 concern.

The verification script is at docs/sprints/00_capability_registry/phase_d_verification.py and is the canonical test for any future changes to soul/capability_registry.metta.

---

## Appendix C: References

- v3.2: docs/sprints/00_capability_registry/sprint_0_phase_1_design_v3.2.md (the prior specification superseded by this v3.3)
- ADR-006: docs/sprints/00_capability_registry/ADR-006-capability-registry.md (Sprint 0 close-out narrative; sprint-scoped decision)
- ADR-007: docs/decisions/ADR-007-substrate-externalized-control-flow.md (project-wide principle)
- Implementation: soul/capability_registry.metta (180 lines; carries the same revisions inline)
- Verification: docs/sprints/00_capability_registry/phase_d_verification.py (765 lines; 6/6 PASS)
