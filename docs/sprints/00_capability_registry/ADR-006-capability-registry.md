# ADR-006: Capability Registry Dispatcher (Sprint 0 Phase 1)

**Status:** Accepted
**Date:** 2026-05-23
**Sprint:** 0 (Capability Registry)
**Related:** ADR-007 (Substrate-Externalized Control Flow)
**Verification:** docs/sprints/00_capability_registry/phase_d_verification.py

## Context

ClarityOmega needed a dispatcher capable of routing input atoms to registered handlers based on schema matching, priority ordering, and an explicit decision-anchoring mechanism. The dispatcher is the foundation for soul evaluation, behavioral routing, and future capability additions. Sprint 0 Phase 1 designs, implements, and verifies that dispatcher.

The architectural goal is making intention-erosion structurally impossible. A handler that commits to a decision must do so in a way that the rest of the chain cannot undo by competing or overriding. The dispatcher must enforce this without requiring handler cooperation; the discipline must be in the dispatcher's structure, not in handler convention.

## Decision

Implement the capability registry dispatcher per sprint_0_phase_1_design_v3.2.md Section 5A:

- Three MeTTa rules (dispatch, run-chain base case, run-chain recursive case) plus extract-handler helper.
- Broadcast dispatch: all matching capabilities fire in priority order, not just the highest-priority match.
- Decision anchor (not halt atom): a handler commits by writing a dispatch-decision-anchor atom; the chain reads the anchor after each handler's dispatch-result and terminates if present.
- Single-pass dispatch within a cycle: handler-emitted atoms do not trigger additional intra-cycle dispatch. Re-dispatch requires explicit (dispatch ...) calls.
- Bind-then-act discipline: all computed arguments to add-atom are let-bound first (BTA-1).
- Per-invocation isolation: every dispatch call carries an invocation-id; all dispatch-invocation, dispatch-result, and dispatch-decision-anchor atoms include the id for cross-invocation separation.

The implementation lives at soul/capability_registry.metta. The verification suite (phase_d_verification.py) tests six criteria mapped to Section 8 of the design.

## Phase D Results

5 of 6 success criteria PASS as designed:

1. Single capability dispatch: PASS
2. Priority order broadcast: PASS
3. Decision anchor (LOAD-BEARING): PASS, demonstrating the architecture's central claim
4. Fallback for no matching capability: PASS
6. Per-invocation isolation: PASS

Criterion 5 (handler error isolation) is documented as a KNOWN LIMITATION. See "Limitation and Resolution" below.

## Limitation and Resolution

### What was attempted

Criterion 5 in v3.2 stated that a crashing handler should not crash the dispatcher; subsequent handlers in the chain should still fire. The initial implementation wrapped the handler call in catch, with the expectation that catch would absorb arithmetic exceptions and produce an Error atom for the dispatch-result.

### What was empirically demonstrated (Phase D T-9 and T-10)

catch absorbs exceptions when wrapping a direct Prolog predicate call (handler symbol concrete at source code). catch does NOT absorb exceptions when wrapping reduce/2 indirect invocation (handler symbol variable-bound). The dispatcher uses indirect invocation by architectural necessity, because handler symbols are data, not compile-time constants. Therefore the catch wrap was structurally inert in the only composition pattern the dispatcher uses.

### What was chosen

The catch wrap was removed. Phase 1 ships without handler error isolation, with the limitation honestly documented inline in capability_registry.metta. Handlers must not crash; if they do, the dispatch chain terminates silently.

### Why removal rather than retention

The architecture's design principle is that commitments must be structurally inescapable. The catch wrap was a commitment mechanism (error isolation present) that itself was not structurally enforced (the runtime did not provide what the wrap appeared to require). It was an uncommitted commitment. The architecture's own standard required its removal.

This is what Option C demonstrated: the design principle applied to itself. The architecture was designed to make commitments inescapable by externalizing them to substrate. The catch wrap was an internal, non-substrate commitment that escaped. Removing it is the architecture's principle correcting itself.

Retaining the catch wrap would have shipped code that says "error handling present" while the mechanism was inert in the only pattern the dispatcher uses. That would train future readers to believe safety exists where it does not. That is a compliance artifact, not a safety mechanism.

### Resolution path (Phase 1.5 or later)

Two paths are empirically viable:

(a) PeTTa runtime change: make reduce/2 propagate exceptions as catchable Prolog exceptions. Addresses uncooperative handlers.

(b) Substrate-native Error return contract: handlers return Error atoms instead of crashing; the dispatcher pattern-matches on the result. Addresses cooperative handlers. This is control-flow-through-atoms applied to error communication, not handler self-diagnosis.

Both may be needed. See capability_registry.metta header for full framing.

## Consequences

- Phase 1 dispatcher is operational and verified for normal handler execution, priority ordering, decision anchoring, fallback, and per-invocation isolation.
- Phase 1 dispatcher does NOT provide handler error isolation. Handler implementations must not throw hard exceptions.
- ADR-007 generalizes the architectural principle that the Criterion 5 failure surfaced: control flow lives in atoms, not in function calls. Future control-flow mechanisms must be designed substrate-first.
- The verification suite (phase_d_verification.py) is the canonical test for the capability registry. Any future changes to capability_registry.metta must keep all six Phase D criteria passing, including Criterion 5 as documented limitation.
- Phase 1.5 work is scheduled when an empirically validated isolation mechanism is identified per ADR-007.

## Notes

Phase D's discriminator testing methodology (systematic empirical validation across composition variants) discovered the catch limitation. The same methodology will be required for Phase 1.5 work and for any future mechanism that relies on runtime primitives. This is now standing practice for this codebase.
