# Compass Scoring - Live Agent Loop Wiring Spec

## Integration Point
Between LLM response generation and skill execution/send in omegaclaw main loop.

## Flow
1. LLM generates response S-expression
2. Parse response to extract send commands and draft text
3. RewriteLoop.start(draft_text) returns metta_calls
4. Execute metta_calls via metta skill, collect results
5. RewriteLoop.feed_metta_results(results) returns phase
6. If phase is scoring: repeat steps 4-5
7. If phase is approved: proceed with original send
8. If phase is needs_rewrite: use rewrite_prompt to regenerate via LLM then RewriteLoop.submit_rewrite and repeat from step 4
9. If phase is max_attempts: send with annotation that compass scoring was inconclusive

## File-Mediated Option - simpler
- Before send: write draft to /tmp/compass_input.json
- Shell call: python3 compass_check.py
- Read /tmp/compass_output.json for verdict
- Avoids modifying loop.metta directly
- Loses live metta integration but works immediately

## Recommended Path
Start with file-mediated approach for immediate functionality.
Migrate to native metta integration as second step.
