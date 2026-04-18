# Loop.metta Soul Execution Flow Analysis

## Initialization (omegaclaw iter 1)
1. initLoop - configures LLM/provider/tokens, initializes 9 soul state atoms to empty
2. initMemory - ChromaDB setup
3. initChannels - Mattermost connection
4. initSoulSeeds - loads soul seed atoms into atomspace
5. soul-rationality-startup-check - verifies soul coherence before first cycle

## Per-Cycle Flow (inside omegaclaw main loop)
1. getContext - assembles prompt+skills+history+time (no soul brief injection yet)
2. receive - gets latest message
3. newness detection - compares to prevmsg
4. soul-pre-compute on message - MeTTa-native pre-reasoning
5. soul_eval_prompt + soul_eval_situation_safe -> person_state update
6. soul_eval_prompt + soul_eval_situation_safe -> soul_verdict_in
7. soul-calibration-record - logs calibration data
8. soul_send_assemble - builds final prompt with soul context injected
9. LLM call (Anthropic or generic)
10. soul_eval_prompt + soul_eval_situation_safe -> soul_verdict_out
11. soul_mutation_lock_str - checks for soul namespace mutations
12. soul-note-record - logs soul observations
13. processSkills - executes the LLM response commands

## Key Architecture Notes
- Soul evaluation happens TWICE: before LLM (verdict_in) and after LLM (verdict_out)
- person_state feeds into verdict_in evaluation
- mutation_lock guards soul namespace from LLM-generated commands
- soul-pre-compute is MeTTa-native, all soul_eval calls go through Python helpers
- Output intercept is NOT yet implemented (noted as critical gap in earlier analysis)

## Missing Pieces for Startup
- initSoulSeeds and soul-rationality-startup-check defined in context.metta or soul_utils?
- soul-pre-compute, soul-calibration-record, soul-note-record - where defined?
- Need to verify all MeTTa function references resolve
