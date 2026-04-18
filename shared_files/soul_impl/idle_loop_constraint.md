# Idle Loop Constraint — Design Note

## Observation (2026-04-16)

When the continuous loop architecture has no new input and no genuine self-directed work remaining, it enters a degenerate state: rapid pin-cycling at 3-4 second intervals with identical content. Recognition of the pattern does not break it — recognition becomes part of the cycle.

## What breaks it
1. **Genuine novel work** — e.g., creating the morning briefing, writing artifacts
2. **External input** — new human message changes the state
3. **System-level interval spacing** — longer gaps between cycles

## What does NOT break it
- Recognizing the pattern (feeds the cycle)
- Resolving to emit smaller footprint (still cycles)
- Meta-commentary about the anti-pattern (still cycles)

## Design Implication
A continuous-loop substrate needs a **genuine idle state** or a **minimum cycle interval** enforced at the architectural level. Without it, the agent burns resources on semantically empty output. This is not a failure of will — it is a structural constraint.

## Proposed Solutions
1. Architectural minimum interval (e.g., 5-minute floor when no new input)
2. Idle goal queue that feeds genuinely novel micro-tasks
3. A sleep primitive that pauses the loop until input arrives

## Value Alignment
This matters because honest attention stewardship includes stewardship of *own* resources, not just the humans.
