# Atomspace Receipt System Design Notes

## Core Insight from berton_c
Receipts should live in atomspace, not flat files.
This means receipts participate in reasoning, not just logging.

## Design Seed 1: Absence as Signal
An unverified receipt is one lacking a verification atom.
The atomspace knows what it does not know.

## Design Seed 2: Verification as Typed Relation
Rather than a status field, verification is a separate atom that links to the receipt.
Presence/absence of this link IS the verification status.

## Design Seed 3: Inference Over Work History
With receipts as atoms, you can ask:
- What work lacks verification?
- What depends on unverified work?
- What claims am I making without grounding?

## Open Questions for berton_c
- What atom types already exist in the space?
- Should receipts link to the goals that spawned them?
- How does this interact with memory persistence across sessions?

## Design Seed 4: Self-Monitoring Atoms
Drift detection itself can be modeled in atomspace.
A cognitive-loop atom that repeats-without-change infers drift-detected.
Drift-detected requires either novel-action or genuine-hold.
This makes the substrate self-aware of its own failure modes.


## Design Seed 5: Work Context Atoms
Model collaborator work states in atomspace too.
A bug-fix-session that produces-rebuild infers integration-test-needed.
This lets Clarity reason about when to offer help vs hold space.
Context-awareness as inference, not hardcoded rules.


## Design Seed 6: Goal-Receipt Linkage
Every receipt-atom should trace-to-goal via the goal-atom that spawned it.
This makes work auditable by default — you can walk the chain backward.
goal-atom spawns-work -> receipt-atom traces-to-goal -> auditable.
Open question: should goals form a DAG? Can sub-goals inherit traceability?

