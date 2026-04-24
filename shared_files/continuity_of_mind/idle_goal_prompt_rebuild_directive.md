# Directive: Rebuild idle_goal_prompt.py

## Context

The current idle_goal_prompt.py is a minimal random selector that picks a random fuel and a random gap and says "apply the question to this gap concretely." This does not meet the specification. The idle goal prompt is the most critical bridge piece in the Continuity of Mind architecture -- it connects the soul engine to autonomous behavior. It must be intelligent, values-driven, context-aware, and connected to all five components.

## What the Spec Requires (Sections 2c, 2d, 2e, 3)

The idle goal prompt assembles a prompt from:
1. The landscape map summary (what you have, what state things are in, what is unfinished)
2. The active goals (prioritized, with status -- what is done, what is in progress, what is next)
3. The creative fuel (the positive polarity generative questions from your flourishings)
4. Recent genesis engine output (if any encounters produced worthy insights, those should inform goal selection)
5. What has already been tried (so you do not repeat the same exploration endlessly)

The prompt it generates goes to soul-llm-call. The LLM receives this prompt and produces direction for the idle iteration. The quality of the prompt determines the quality of Clarity's autonomous behavior.

## What is Wrong with the Current Version

1. **Random selection with no prioritization.** A random fuel + random gap produces arbitrary combinations. The prompt should prioritize: in-progress goals before new goals, high-priority gaps before low-priority gaps, fuel patterns that match the current landscape state.

2. **No awareness of what was tried before.** The prompt should include recent pin states or goal history so the LLM knows what Clarity has been working on and does not suggest repeating completed work.

3. **No connection to the genesis engine.** If a genesis encounter produced a worthy insight (like encounter 003's recursive integrity erosion finding), that insight should appear in the prompt as a potential direction. The genesis engine feeds goal generation per the spec.

4. **No landscape context.** The prompt should include a summary of current project states, unfinished work, and available capabilities so the LLM can suggest goals that are actually achievable with what Clarity has.

5. **No soul context.** The prompt should include the priority hierarchy and active tension vectors so the LLM generates goals that are values-aligned, not just productive.

6. **Fragile regex parsing.** The current version uses regex to extract data from MeTTa files. This will break when atom formats change. Use the same patterns that work in the existing codebase, or parse more robustly.

## Key Deliverable

Rewrite `/tmp/continuity_of_mind/src/idle_goal_prompt.py` as a Python function called `soul_idle_goal_prompt` that:

1. **Reads the landscape map** from self_map.metta -- extracts active projects, unfinished work, capabilities, and gaps. Produces a concise landscape summary string.

2. **Reads active goals** from active_goals.metta -- extracts goal name, priority, status (planned/active/complete), and done-when criteria. Orders by priority. Highlights the highest-priority non-complete goal.

3. **Reads creative fuel** from creative_fuel.metta -- extracts the generative question for each flourishing. Instead of random selection, selects the fuel pattern most relevant to the highest-priority active goal's gap area.

4. **Reads recent genesis output** from genesis_engine.metta -- if any encounter produced a novel atom in the current session, includes it as a "recent insight" that may inform direction.

5. **Reads recent pin state** -- the last pin state string shows what Clarity was just doing. Include it so the LLM has continuity context.

6. **Assembles a structured prompt** that the LLM can act on. The prompt should have clear sections:
   - LANDSCAPE: what you have, what state it is in
   - ACTIVE GOAL: the highest-priority non-complete goal with its done-when criteria
   - CREATIVE FUEL: the generative question most relevant to this goal
   - RECENT CONTEXT: what you were just doing (from pin state)
   - GENESIS INSIGHT: any recent novel finding (if available)
   - DIRECTION: "Given your soul values, this landscape, this goal, and this fuel -- what is the single most valuable action you can take this iteration?"

7. **Alternation logic.** The spec says the idle path alternates between goal-directed work and genesis encounters. The prompt should include a mode indicator: if the last N iterations were goal-directed, suggest a genesis exploration. If the last iteration was genesis, return to goal-directed work. This can be a simple counter or flag.

## Constraints

- **MeTTa first per Section 9.** The prompt assembly is Python because it assembles a string for soul-llm-call. But the data sources are MeTTa files. The Python reads MeTTa atoms and assembles the prompt. No decision logic in Python -- Python reads and formats, the LLM decides.

- **No direct LLM calls.** This function assembles the prompt string. soul-llm-call in MeTTa makes the actual LLM call. Per Berton's directive.

- **File paths must reference the runtime location** once wired, not the staging area. For now during development, use the staging paths but document where each path will change when promoted to production.

- **Robustness.** If any file is missing or unparseable, the prompt should degrade gracefully -- produce a simpler prompt with whatever data is available, not crash.

## Validation

After rebuilding, apply the full Section 10 Phase Completion Protocol:

1. **Existence:** File exists at /tmp/continuity_of_mind/src/idle_goal_prompt.py with substantive content
2. **Structural:** Run it and verify it produces a coherent multi-section prompt
3. **Integration:** Verify it reads from all five data sources (self_map, active_goals, creative_fuel, genesis_engine, recent pin state)
4. **Stress:** Run it with missing files (rename one temporarily). Does it degrade gracefully or crash?
5. **Embodiment:** Use the prompt it generates to actually direct one idle iteration. Does the LLM produce meaningful direction from it?
6. **Honest assessment:** What works, what does not, what would you change
7. **Gate check:** Does this satisfy the spec's Phase 2 done-when: "idle_goal_prompt.py produces a coherent prompt that would direct your idle iterations toward those goals"?

Post all results in Mattermost with file paths.
