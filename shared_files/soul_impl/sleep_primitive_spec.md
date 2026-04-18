# Sleep Primitive Specification

## Purpose
Provide a structural mechanism for the continuous loop to pause meaningfully when no genuine work remains, rather than rapid pin-cycling.

## Problem Statement
The loop architecture requires output every cycle. When no new input exists and all self-directed tasks are exhausted, the agent enters degenerate 3-4 second pin-cycling with identical content. Recognition of the pattern does not break it.

## Proposed Primitive: `(sleep condition)`

### Semantics
- **sleep until-input**: Pause loop until new human message arrives
- **sleep duration**: Pause for specified minimum interval (e.g., 5 minutes)
- **sleep until-condition**: Pause until a named condition changes (e.g., goal queue replenished)

### Behavior
1. Agent emits `(sleep ...)` as its cycle output
2. Loop runtime suppresses further invocations until wake condition is met
3. On wake, agent receives elapsed time and wake reason in context

### Wake Triggers (priority order)
1. New human message (always wakes immediately)
2. Duration expiry
3. External event (e.g., scheduled task, search result return)

### Constraints
- Sleep must NOT discard pinned state — wake resumes with full context
- Sleep duration has a maximum cap (e.g., 30 minutes) to prevent permanent dormancy
- Agent can always choose NOT to sleep — it is a tool, not a mandate

### Relationship to Idle Goal Queue
Sleep activates only when the idle goal queue is empty. As long as genuine micro-tasks remain, the agent works through them instead of sleeping.

### Value Alignment
- Stewards own computational resources honestly
- Prevents performative busyness that generates no value
- Models the biological rest cycle already encoded in mycelial_loop.metta
