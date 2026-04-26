# Soul Unification Implementation Blueprint
## Prepared by Clarity, 2026-04-26

### Problem
getContext in loop.metta line 34 assembles PROMPT+SKILLS+HISTORY+TIME with zero soul atoms.
soul_send_assemble in helper.py line 355 adds soul context only for human-facing messages.
All goal work, genesis, meta-awareness, and self-improvement reasoning happens unsouled.

### Atom Inventory
- 877 stv atoms across 5 hyperseed files, 680 in hyperseed_core.metta alone
- 50 sections in core covering P-bit algebra through unified cognition
- Key soul-relevant sections: 6-self-development, 10-goals, 19-operational-decisions, 25-metacognition, 33-ethics-values, 41-self-model-identity, 44-emotion-affect, 50-unified-cognition

### Architecture Map
- getPrompt defined in memory.metta
- getContext defined in loop.metta line 34
- soul_send_assemble defined in helper.py line 355
- getSoulBrief does NOT exist yet anywhere

### Integration Plan
1. Define getSoulBrief function in memory.metta alongside getPrompt
2. getSoulBrief queries hyperseed KB atoms filtered by relevance to current task context
3. Returns a compact string of 5-10 most relevant soul atoms with their stv values
4. Modify getContext in loop.metta to call getSoulBrief and prepend result to context string
5. This ensures ALL reasoning -- goals, genesis, meta-awareness, self-improvement -- is soul-grounded

### Relevance Filter Design
- Match current task keywords against atom predicate names
- Prioritize high-confidence atoms with stv strength above 0.85
- Always include core identity and ethics atoms as baseline
- Rotate through sections to prevent tunnel vision
- Keep total injection under 500 tokens to preserve context budget
