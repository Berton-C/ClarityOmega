# Encounter V3 Integration Spec

## Goal
Wire tension-weighted encounter into live reasoning loop.

## Existing Integration Points
1. getContext in loop.metta - assembles LLM prompt
2. Command execution block - soul verdict gates here
3. HandleError pattern - intercept before retry
4. initLoop - startup checks

## Integration Design
After memory query returns results and before using them:
1. Pass retrieved memories plus current context to encounter_v3
2. Extract highest-tension gap concepts and question
3. Prepend encounter question to context block
4. LLM sees the tension question alongside retrieved content

## Implementation Path
- Add encounter_v3 call inside getContext after query results return
- Format encounter output as context annotation
- No new dependencies - encounter_v3.py is standalone

## Status
Ready for integration when live testing opportunity arises.
Encounter V3 validated with all three tension scoring paths.
