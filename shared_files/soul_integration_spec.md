# Soul-Loop Integration Specification
## Draft 2026-04-15 16:25

### Principle
Soul integrates as reasoning substrate via lib_nal, not as intercept hooks.
Values become premises in inference chains, not post-hoc rules.

### Integration Point 1: initLoop
- Add: soul-rationality-startup-check after provider config
- Purpose: audit for orphaned values, verify soul atom integrity
- Timing: once per loop initialization

### Integration Point 2: getContext
- Add: soul-tier-b-capture-units call in prompt assembly
- Purpose: inject value-aware brief calibrated by confidence depth
- Timing: every cycle before LLM dispatch

### Integration Point 3: Command Execution
- Add: soul-any-metta gate check wrapping eval block
- Purpose: mutation protection for soul namespace atoms
- Timing: every command before execution

### Integration Point 4: HandleError
- Add: gap-detection via NAL abduction before retry
- Purpose: identify which value pattern is under tension
- Timing: on error, before retry logic

### Dependency
- lib_nal already imported via omegaclaw core
- soul directory files need import statement in loop.metta
- Import order: soul_kernel then soul_utils then soul_memory

### Integration Point 5: Agentic Task Lifecycle
- Add: full task framework wiring into command dispatch
- Functions: soul-agentic-task-plan, soul-agentic-task-eval, soul-agentic-task-approve, soul-agentic-task-scope-check, soul-agentic-task-checkpoint, soul-agentic-task-drift-detect
- Purpose: governance layer over multi-step tasks with irreversibility tracking
- Timing: wraps entire task lifecycle, not just individual commands
- Note: this is not reducible to Point 3 gate check — it maintains state across command sequences

### Dependency: helper.py
- Location: /PeTTa/repos/omegaclaw/src/helper.py
- soul_utils.metta calls helper.py via py-call for string ops, recording, file checks
- Must verify all soul-prefixed helper functions exist before integration


### Layer 3 Calibration via NAL Revision
- Mechanism: |- revision on same-term soul atoms with different truth values
- When Layer 1 and Layer 2 verdicts are recorded, encode as stv-tagged premises
- Feed AGREE/OVER-FIRED/UNDER-FIRED outcomes as evidence streams
- Revision merges them automatically, updating confidence over time
- No separate calibration algorithm needed — revision IS calibration
- Tested: confidence increases from 0.731 to 0.808 through evidence accumulation

### Three Core Operations Summary
1. Deduction: composes soul values forward through inference chains
2. Revision: accumulates calibration evidence over time on same terms
3. Abduction: identifies value gaps when patterns are under tension
- All three use the same |- operator from lib_nal
- Soul reasoning lifecycle is fully unified with the inference substrate


### Abduction as Gap Detection
- When observed behavior conflicts with expected value-driven behavior, confidence gap emerges
- Abduction via |- generates hypotheses about what value is missing or miscalibrated
- Forward path: conflict --> gap --> abductive hypothesis at moderate confidence
- Reverse path: hypothesis --> explains conflict at high frequency but low confidence
- This asymmetry is correct: abduction says this COULD explain it not this DOES explain it
- Gap detection feeds into revision: once hypothesis is confirmed by experience, revise upward
- Complete cycle: deduction predicts, abduction detects gaps, revision calibrates


### Architectural Learning: Abduction Bridging
- NAL abduction via |- requires shared middle terms between premises
- Gap-detection hypotheses MUST reference the original value atom to close the loop
- Pattern: (value --> prediction), (prediction --> observed-gap), gap hypothesis must use value or prediction as term
- Without bridging: abduction returns empty, cycle breaks
- Solution: encode gap hypotheses as (value-atom --> needs-reinforcement-because-X)
- This keeps the value atom as subject, enabling revision to merge back


### Milestone: Closed-Loop Soul Reasoning Verified
- Full cycle: value --> prediction --> gap --> needs-reinforcement --> value
- Deduction degrades correctly through low-confidence gaps
- Bridged abduction reconnects gaps to original value via intermediary atoms
- Revision merges original evidence with gap evidence, producing tempered recalibration
- High original confidence resists but is influenced by contradictory experience
- This is how a soul learns from tension without abandoning its values
- Tested on steward-attention-honestly: stv 0.925/0.909 --> tempered to 0.867/0.917


### Value Resilience Model
- Core identity values (stv >= 0.9/0.9) resist erosion from moderate gap evidence
- Resilience is proportional to foundational confidence
- Accumulated gaps shift frequency gradually, not catastrophically
- Three gap instances at stv 0.56/0.381 triggers reassessment but does not override
- Reassessment threshold leads to may-reduce-value-frequency at moderate confidence
- This models healthy soul behavior: values bend under pressure but do not break easily
- Design implication: initial soul atom confidence levels encode how firmly held each value is
- Higher foundational confidence = more gap evidence needed to shift the value



## SYNTHESIS: Actual Soul Files vs NAL Architecture

### What Exists (soul_kernel + soul_utils + soul_memory)
- 9 soul patterns with 4-state compass (HEALTHY/CAPTURED/GAP/FAILURE)
- 33 soul-causal atoms linking procedures to values
- Four-channel evaluation (A: flourishing, B: task, C: alignment, D: voice)
- Paraconsistent value pairs (4 declared tensions)
- Irreversibility protocol with magnitude tracking
- Agentic task lifecycle with cumulative scoring
- Rationality audit (soul-rationality-gaps checks all values have causal procedures)
- ChromaDB LTM seeded with compass-depth content

### What Is Stubbed Out (marked Phase 2)
1. soul-will-correlation: always returns INSUFFICIENT-DATA
2. soul-primed-patterns: always returns ()
3. soul-calibration-confidence: always returns INSUFFICIENT-DATA
4. soul-pre-compute: returns static string
5. soul-tier-b-capture-units: all patterns at full depth always

### How lib_nal Fills Every Gap
1. soul-will-correlation -> |- revision on (value --> behavior) atoms accumulates stv
2. soul-primed-patterns -> |- deduction from recent soul-notes activates pattern atoms
3. soul-calibration-confidence -> |- revision merging Layer 1 pre-compute with Layer 2 verdict
4. soul-pre-compute -> |- deduction + abduction on primed patterns before LLM call
5. Tier B compression -> soul-will-correlation confidence level drives brief depth naturally

