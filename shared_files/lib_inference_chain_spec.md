# lib_inference_chain Specification

## Purpose
Automate multi-step NAL inference without manual chaining.

## Prior Work
- Manual chaining confirmed working up to 5 hops (April 18-20)
- Confidence degrades honestly per hop: practical limit ~4-5 steps
- lib_meta_inference.metta: route-inference selects inference type
- lib_revision_accumulator.metta: evidence merging at endpoints

## What Is Missing
1. Backward chaining - given target conclusion find premise path
2. Forward chaining - given premises derive all reachable conclusions
3. Chain termination - stop when confidence drops below threshold
4. Path selection - choose highest-confidence path among alternatives
5. Cycle detection - prevent infinite loops in inference graph

## Proposed Types
- InferenceStep: (premise1 premise2 rule result stv)
- ChainPath: [InferenceStep] with cumulative confidence
- ChainGoal: (target-statement min-confidence max-depth)
- ChainResult: (path final-stv steps-used)

## Proposed Functions
- backward-chain: ChainGoal -> [ChainResult]
- forward-chain: [Statement] -> [ChainResult] with depth limit
- best-path: [ChainResult] -> ChainResult by confidence
- chain-confidence: ChainPath -> stv (cumulative degradation)
- terminate-check: ChainPath -> Continue | Stop

## Implementation Notes
MeTTa |- operator is the engine. Chaining wraps repeated
|- calls with intermediate result capture via let-bindings.
Backward chaining requires pattern matching on available
premises - may need MeTTa match expressions.
