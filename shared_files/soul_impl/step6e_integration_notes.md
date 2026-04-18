# Step 6e: Real Query Integration Architecture

## Key Insight
The query skill runs at agent-loop level, not callable from Python runtime.
The pipeline runs in Python. These are different execution contexts.

## Solution: Agent-Loop Orchestration
1. Agent loop receives user message
2. Agent loop calls extract_query_phrases or does it inline
3. Agent loop issues query calls with those phrases
4. Agent loop collects results
5. Agent loop passes results into felt_sense_read_v3 via memory_query_fn

## Status
Pipeline is ready. Bridge is designed. Connection happens at deployment time.
This completes Goal 12 design phase.