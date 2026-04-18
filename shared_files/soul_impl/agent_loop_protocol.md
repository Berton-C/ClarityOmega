# Agent Loop Integration Protocol

## Live Runtime Pattern: 5 skill calls per exchange

### Phase 1: Gather context (2 calls)
1. query user message key phrases to get memory hits
2. query any additional relevant phrases

### Phase 2: Situation read (2 calls)
3. write-file unified_input.json with user_message + memory_texts (+ optional draft_response)
4. shell python3 unified_runtime.py

### Phase 3: Read guidance (1 call)
5. read-file unified_output.json

## Output Structure
- situation.presence_mode: grounded/transitional/activated/elevated
- situation.felt_sense_scalar: 0-10 intensity
- situation.felt_sense_guidance: plain language guidance
- compass.compass_scores: agency/wonder/thinking/attention
- compass.composite: overall alignment score
- compass.flags: dimensions below threshold
- compass.pass: boolean

## Decision Logic
- If compass.pass is true: send the draft
- If compass.flags exist: revise draft to address flagged dimensions
- If felt_sense_guidance says novel_territory: prioritize listening
- If felt_sense_guidance says strong_match: lean into recognized pattern

## Two-Pass Option
First pass: situation read only (no draft_response)
Craft response using guidance
Second pass: include draft_response for compass check
Revise if needed, then send
