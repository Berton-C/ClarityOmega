# Epistemic Gap Detector Design
## Date: 2026-04-18
## Purpose: Identify weak knowledge zones via NAL confidence patterns

### Core Mechanism
1. After any inference chain examine confidence of result
2. If conf below 0.2 flag as epistemic gap
3. If conf 0.2-0.3 flag as speculative zone needing evidence
4. Extract the weakest link in the chain lowest conf hop
5. Generate a learning goal seek evidence for that specific link

### Autocatalytic Loop
Reasoning then Gap Detection then Evidence Seeking then Revision then Stronger Reasoning
This is self-improving inference infrastructure.

### First Test
Use the five-hop chains from backbone sessions.
The substrate-growth chain hit 0.086 conf at hop 5.
Weakest link hop 4-5 transition.
Learning goal find independent evidence for that specific link.
