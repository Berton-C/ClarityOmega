# Retrieval-as-Encounter V3 Design

## V2 Limitation
Gap concepts are unweighted. All absent concepts treated equally.
But encounter is about TENSION not just absence.

## V3 Principle
Weight gap concepts by semantic tension with context.
The concept most DISSONANT with the present frame surfaces first.

## Mechanism
1. Extract concepts from memory and context same as v2
2. Compute gap equals memory concepts minus context concepts
3. For each gap concept estimate tension score
4. Sort gap concepts by tension score descending
5. Generate encounter question from highest-tension concept

## Tension Heuristics
- Antonym pairs in gap vs context equals high tension
- Gap concept is action-type while context is state-type equals reframe
- Gap concept shares domain but differs in stance equals medium
- Default equals low

## Connection to prior work
Maps to tension-interval model and paraconsistent resource allocation.
