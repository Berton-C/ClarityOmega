# lib_goal_decomposition Specification

## Purpose
Break complex goals into trackable subgoals with dependency ordering.

## Prior Work Already Built
- lib_goal_decomposition.metta (April 20): decompose, propagate-completion, depends-on
- lib_goal_scheduler.metta: prioritize-goal, schedule-next, urgency-rank
- lib_goal_memory.metta: update-goal via NAL revision, goal-status classification
- lib_curiosity.metta: EpistemicGap to CuriositySignal to GoalCandidate pipeline
- lib_metacognition.metta: ChainHealth, DecaySignal, MaintenanceGoal

## What Exists vs What Is Missing
Existing pieces handle individual goal lifecycle. Missing:
1. Recursive decomposition - breaking a goal into subgoals that themselves decompose
2. Dependency graph traversal - ordering execution by prerequisite satisfaction
3. Partial completion propagation - parent goal confidence updates as children complete
4. Blocked-goal detection - identifying goals stalled on unmet dependencies
5. Recomposition - synthesizing subgoal results back into parent goal assessment

## Proposed Types
- GoalTree: (goal-id parent-id children-ids stv)
- Dependency: (goal-id depends-on-id blocking-threshold)
- DecompResult: (parent-id child-goals decomposition-method)
- CompletionSignal: (goal-id completion-confidence propagate-to)

## Proposed Functions
- decompose-goal: GoalTree -> [GoalTree] using domain heuristics
- check-dependencies: GoalTree -> Blocked | Ready | Partial
- propagate-up: CompletionSignal -> revised parent stv
- find-frontier: [GoalTree] -> [GoalTree] (ready leaves)
- recompose: [CompletionSignal] -> parent GoalTree assessment

## Integration Points
- Feeds into lib_goal_scheduler for execution ordering
- Receives from lib_curiosity for gap-driven goal generation
- Uses lib_goal_memory for persistent state across cycles
- Uses NAL revision for confidence propagation

## Implementation Strategy
Build as MeTTa |- pattern library with inline let-chain validation.
Each function expressed as documented |- invocation pattern.
Validate with 3-level decomposition test case.
