# ADR-007: Substrate-Externalized Control Flow

**Status:** Accepted
**Date:** 2026-05-23
**Sprint:** 0 (Capability Registry)
**Supersedes:** None
**Superseded by:** None

## Context

The capability registry implementation (Sprint 0 Phase 1) made every architectural decision through substrate I/O: capability selection via match, commitment via add-atom, branching via if-on-substrate-query, invocation isolation via per-id atom writes, fallback via collapse-result check. One component reached outside this pattern: the catch wrap around the handler call in Rule 3 of run-chain. That component was the only one that depended on a runtime primitive's composition-dependent semantics rather than on substrate state.

Phase D empirical testing (T-9 and T-10) established that catch absorbs exceptions when wrapping a direct Prolog predicate call but does NOT absorb exceptions when wrapping reduce/2 indirect invocation. The dispatcher must use indirect invocation because handler symbols are data, not compile-time constants. Therefore the catch wrap, which appeared to provide error isolation, was structurally inert in the only composition pattern the dispatcher uses.

The catch wrap was removed. The dispatcher now ships without handler error isolation, with the limitation honestly documented.

This decision surfaced a generalizable architectural principle that extends beyond the dispatcher and beyond error handling.

## Decision

Control flow in ClarityOmega's MeTTa substrate lives in atoms, not in function calls.

Every control-flow mechanism (selection, commitment, branching, sequencing, isolation, error handling, and any future addition) must be expressed as substrate I/O (add-atom, match, collapse, query-then-branch). Mechanisms that reach outside this pattern, relying on runtime primitives whose composition behavior may differ from their direct-call behavior, are vulnerable to silent failure with no runtime signal.

The capability registry's Rule 3 handler invocation is the one place this principle does NOT hold. Handlers are invoked via indirect reduce/2 because handler symbols are data. That single point of substrate exit is precisely where the dispatcher's only silent failure (Criterion 5 limitation) lives. This is architectural coherence, not coincidence: the runtime composition constraints bite exactly where control flow leaves the substrate.

## Evidence

The catch wrap failure is the self-demonstrating evidence for the principle:

- Direct invocation `(c5-handler input)` compiles to `'c5-handler'(input, M)`, a Prolog predicate call. catch wrapping this is functional; exceptions are absorbed.
- Indirect invocation `($h input)` where $h is variable-bound compiles to `reduce([handler-sym, input], M)`. catch wrapping this is NOT functional for arithmetic exceptions; the runtime propagates the exception in a way the surrounding catch cannot intercept.
- The dispatcher must use indirect invocation by architectural necessity (handlers are data).
- Therefore the catch wrap in the dispatcher was inert from the moment it was written.

This is empirically established by Phase D discriminator tests T-9 (direct-call catch composition works through all variants) and T-10 (indirect-call catch composition fails silently for crashing handlers).

The catch wrap was the one dispatcher component that relied on runtime promise-keeping (catch catches exceptions) rather than on substrate state. Every other component (capability selection, commitment, branching, isolation) uses substrate I/O. The one component that violated the substrate-externalized pattern is the one component that silently failed.

## Implication

Any future mechanism that the architecture might rely on for control flow (especially error handling, but also retries, timeouts, recovery, supervision, lifecycle management, dependency resolution, or any other coordination primitive) must be designed substrate-first.

A substrate-first design means: state lives in atoms, decisions are reads of substrate, actions are writes to substrate, and runtime primitives are used only to construct atoms and read atoms (never to encode control flow that the substrate cannot observe).

Mechanisms that attempt to add a layer of control flow outside the substrate (wrapping calls in catch, threading state through closures, relying on runtime exception semantics, depending on tail-call optimization) are vulnerable to runtime composition constraints. The runtime's advertised behavior for primitive X may not apply when X is composed with primitive Y in a specific way. The runtime typically provides no signal when this happens. The control flow silently breaks.

The substrate-externalized pattern works because it does not depend on runtime composition. Atoms are written; atoms are read. The runtime's only role is to faithfully store and retrieve them. Composition concerns disappear because the control flow is not composed through runtime primitives at all; it is composed through substrate state.

## Prediction

Phase 1.5 error isolation will be designed substrate-first. Two viable paths exist:

(a) PeTTa runtime change: make reduce/2 propagate exceptions as catchable Prolog exceptions. This addresses uncooperative handlers (ones that crash with hard exceptions) by lifting the constraint that made the catch wrap inert.

(b) Substrate-native Error return contract: handlers communicate failure as atoms returned from their normal reduction. The dispatcher pattern-matches on the result. This addresses cooperative handlers (ones that can detect failure conditions and choose to return Error atoms). Control flow stays in atoms throughout.

Path (a) is a runtime enhancement; the architecture is unchanged. Path (b) extends the substrate-externalized pattern to cover error communication. Both may be needed; they address different handler classes.

Any third path proposed in the future will be evaluated against this principle: does the mechanism keep control flow in atoms? If yes, it is consistent with the architecture and worth empirical validation. If no, it is a candidate for the same silent failure that the catch wrap exhibited.

## Consequences

- Future control-flow mechanisms in ClarityOmega's MeTTa substrate are required to be substrate-first by default.
- Any deviation from this principle requires explicit justification, empirical validation in the specific composition pattern the mechanism will be used in, and documentation of the runtime promise being relied on.
- This principle does not prevent the use of runtime primitives; it requires that runtime primitives be used as building blocks for substrate-state manipulation, not as control-flow constructs in their own right.
- This ADR establishes a constraint that must be checked when designing future capabilities, ADRs, and sprint deliverables.

## Notes

The recursive integrity of this decision is worth recording. The architecture's design principle is that commitments must be structurally inescapable. The catch wrap was an internal (non-substrate) commitment that itself was not structurally enforced. Removing it is the architecture's principle correcting itself: an uncommitted commitment cannot stand in a system whose foundation is committed commitments.

This is not abstract. It is the dispatcher's design principle applied to the dispatcher's own implementation. The principle informed its own application. Future ADRs and design decisions should be checked for the same coherence: does the proposed mechanism's location, framing, and structure exemplify the principle the mechanism is meant to embody?
