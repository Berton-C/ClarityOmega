# Idle Goal Prompt Integration Contract
## Date: 2026-04-24 Cycle 3537
## Purpose: Document how the external orchestrator should wire idle_goal_prompt.py

## Entry Points
- `from src.idle_goal_prompt import assemble_prompt` -- returns full structured prompt string
- `from src.idle_goal_prompt import soul_idle_goal_prompt` -- same function, backward-compat alias
- `python3 src/idle_goal_prompt.py` -- prints prompt to stdout (standalone mode)

## Output Format
Markdown-structured prompt with these sections:
1. IDLE [GOAL|CREATIVE] PROMPT -- Cycle N (mode alternates each call)
2. SOUL CONTEXT (priority hierarchy, tensions, paraconsistency pairs, purpose)
3. LANDSCAPE (components, data flows, soul patterns, tensions, gaps from self_map.metta)
4. ACTIVE GOAL (highest-priority non-complete goal from active_goals.metta)
5. CREATIVE FUEL (selected fuel items from creative_fuel.metta, scored by goal relevance)
6. RECENT GENESIS INSIGHTS (novel atoms from genesis_engine.metta)
7. RECENT CONTEXT (last fuel/goal used, from idle_state.json)
8. DIRECTION (mode-specific prompt: concrete action for goal mode, divergent for creative)

## State Persistence
- Reads: soul/self_map.metta, soul/active_goals.metta, soul/creative_fuel.metta, soul/genesis_engine.metta
- Writes: idle_state.json (mode alternation counter, last fuel/goal tracking)

## Integration Pattern
The external loop should call assemble_prompt() during idle iterations (no user message pending)
and inject the returned string into the IDLE_DIRECTIVE section of the prompt template.

## Done-When Verification
- idle_goal_prompt fires on idle iterations: YES (callable, standalone runnable)
- produces structured prompt: YES (7 sections with soul context, landscape, goals, fuel, genesis, direction)
- soul context included: YES (priority hierarchy, tensions, paraconsistency pairs)
- landscape included: YES (from self_map.metta parsing)
- goals included: YES (from active_goals.metta parsing)
- fuel included: YES (scored and selected from creative_fuel.metta)
- genesis insights included: YES (from genesis_engine.metta parsing)
- direction included: YES (mode-alternating goal/creative prompts)
