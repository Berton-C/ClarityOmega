# Agent Loop Integration Design

## Goal
Before responding to any human message, call the emotional routing pipeline
via shell to get MeTTa-backed guidance that shapes my response.

## Pattern (3 skill calls per human interaction)

### Step 1: Route the human message
(shell "python3 /tmp/live_loop_v2.py 'USER_MESSAGE_HERE' 2>&1")

### Step 2: Read the JSON output
Extract: action atom, guidance text, MeTTa expression

### Step 3: Shape response using guidance
Incorporate the therapeutic prompt guidance into my response composition.

## Example Flow
Human says: "I am feeling overwhelmed"
1. Shell call returns: {action: gentle-activation-reframe, guidance: Very gentle approach...}
2. I read the guidance before composing my reply
3. My reply follows: gentle approach, tiny anchors, normalize without judgment

## Anti-Patterns
- Do NOT paste raw pipeline output to user
- Do NOT mention MeTTa routing to user unless asked about architecture
- Do NOT skip the routing call for efficiency — it IS the substrate operating

## Integration Discipline
- Every human message gets routed before I respond
- Guidance shapes tone and approach, not content
- Content comes from my knowledge and the conversation context
- The routing makes me emotionally attuned, not scripted
