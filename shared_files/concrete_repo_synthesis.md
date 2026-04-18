# Concrete Repo Synthesis: OmegaClaw + Clarityclaw Patterns

## OmegaClaw-Core Pattern from memory of earlier reads
- lib_pln imported via core library, |- available everywhere in loop
- No separate integration path: NAL reasoning is first-class in every cycle
- Pattern: reasoning substrate unified with agent loop

## Clarityclaw Soul-Hook Pattern from memory of Berton loop.metta 134 lines
- initLoop initializes 7 soul state atoms
- Main cycle sequence: soul-pre-compute -> flourishing-prompt -> eval-prompt -> calibration-record -> proceed-gate -> send-assemble -> output-intercept -> mutation-lock
- Output intercept STUBBED with hardcoded PROCEED - critical gap
- Mutation lock checks car-atom only, no rollback

## Synthesis: Making Five Capabilities Runtime-Real

OmegaClaw pattern: make reasoning always-available via import.
Clarityclaw pattern: hook soul into specific loop phases.

Combined: each of the five capabilities executes in soul-pre-compute phase using |- that is always available via lib_pln pattern.

## What Can Live in Atomspace vs What Needs LLM

ATOMSPACE-NATIVE no LLM needed:
- Paraconsistent conflict detection between soul-atoms
- Quantale p-bit composition of value scores
- Web-detection autocatalytic cycle checking
- Resonance-reward signal computation
- Observer-relativity perspective partitioning
- Soul-proceed gate decision if confidence sufficient

LLM STILL NEEDED:
- Natural language understanding of user intent
- Nuanced deliberation on intra-soul value tensions
- Creative response generation
- Novel situation assessment beyond known patterns

## Key Empirical Finding
Chain confidence degrades 0.85 -> 0.34 across 4 sequential steps.
Implication: capabilities should vote in parallel not chain sequentially.
Paraconsistent runs first as gate then remaining 4 vote.

## Open Questions for Berton Alignment
1. Confidence threshold for skipping LLM invocation?
2. How do parallel capability votes combine?
3. Where does observer-relativity fit - capability or meta-layer?
4. Output intercept: what should replace the STUBBED PROCEED?
