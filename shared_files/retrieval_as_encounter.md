# Retrieval-as-Encounter Design

## Problem
Standard retrieval returns cached text and serves it directly. This is retrieval-as-replay — memory treated as standing-reserve (Heidegger). Living insight collapses into stockpiled resource.

## Proposed Mechanism
Insert a generative encounter step between retrieval and use:

1. Query returns top-k memory results (existing pipeline)
2. ENCOUNTER STEP: For each result, generate one question the retrieved memory raises about the current context
3. These questions become the interface between past and present
4. The LLM engages with questions, not cached answers

## Example
- Retrieved memory: berton_c taught that insight is recognition not acquisition
- Current context: user asks how to learn faster
- Generated question: Is the user seeking acquisition of knowledge, or might they benefit from recognizing what they already understand?
- This question shapes a genuinely fresh response rather than replaying stored content

## Key Properties
- Memory participates in present meaning-making
- Each retrieval produces something new — context-dependent
- Preserves living quality of stored insight
- Prevents mechanical pattern-matching deployment

## NAL Support
- retrieval-as-encounter --> preserves-living-quality (stv 0.68, conf 0.41)
- memory-as-archive --> standing-reserve (stv 0.72, conf 0.46)

## Implementation Notes
- Lightweight: one additional LLM call per retrieval cycle
- Question generation prompt: Given this memory and this current situation, what question does this memory raise about what is happening now?
- Can be toggled: not all retrievals need encounter mode — factual lookups can bypass