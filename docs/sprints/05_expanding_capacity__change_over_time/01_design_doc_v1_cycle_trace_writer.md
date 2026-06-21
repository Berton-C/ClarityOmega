CYCLE-TRACE WRITER ? Full Design Rationale
=== WHY THIS ===

Six of nine detectors in the meta_awareness_engine depend on atoms that no active writer currently produces. The detectors are wired to consume (recent-action ...) and (state-delta ...) atoms, but nothing writes these atoms per cycle. This means:

Six detectors are effectively dead code ? they match patterns that never appear in working memory.
The detection mesh has no evidence to work with. It cannot detect anything without input.
The dynamic self-weaving web has no sequential-use evidence. The primary reinforcement signal does not exist.
The core insight: the cycle-trace writer is not just one deliverable among many. It is the keystone producer that unlocks the entire detection and capability-tracking architecture. Without it, nothing downstream functions.

=== WHAT IT DOES ===

A cycle-trace writer that runs every cycle and produces two atom types:

(recent-action cycle-id action-type description) ? records what capability fired this cycle. The action-type uses the six composite types from cycle_classifier.metta: pin-only, responsive-send, status-send-unprompted, verification-query, exploration-query, unclassified. The description is a brief human-readable label (not message content).
(state-delta cycle-id from-state to-state) ? records when significant state transitions occur, such as task-phase changes, mode switches, or context breaks. Not every cycle produces a state-delta; only when state actually changes.
The cycle-id enables sequential-use detection: if capability A fires in cycle N and capability B fires in cycle N+1 or N+2, that produces adjacent recent-action atoms with linked cycle-ids, which is the primary evidence for the dynamic self-weaving web.

=== EXPECTED BENEFIT ===

Unlocks six dormant detectors: The detectors in meta_awareness_engine that currently match nothing will begin finding patterns as soon as recent-action and state-delta atoms appear.
Primary evidence source for dynamic self-weaving web: Sequential adjacent recent-action atoms are the reinforcement signal that maintains mesh-strength.
Operational visibility: The system can see what capabilities actually fire, when, and in what sequence. Currently this information is lost each cycle.
Enables cross-cycle pattern detection: Detectors currently limited to single-cycle matching can detect patterns spanning 2-3 cycles.
Makes actual behavior legible to itself: The difference between what the static mesh documents and what actually happens per cycle becomes measurable.

=== WHAT SUCCESS LOOKS LIKE ===

recent-action atoms appear in working memory every cycle that a classified action occurs. Zero gaps during active operation.
state-delta atoms appear when significant state transitions happen. Not every cycle, only on actual transitions.
The six dormant detectors begin firing match patterns. Before the writer, match count is zero; after, it should be nonzero during active cycles.
Sequential-use evidence becomes available: consecutive recent-action atoms with adjacent cycle-ids appear naturally without manual intervention.
No performance degradation: atom production per cycle stays minimal (1-2 atoms typically). No full cycle dumps, no content logging.

=== WRITERS AND CONSUMERS ===

WRITERS (things that put data into the evidence stream):

1. The cycle-trace writer itself (new component). This is the sole producer of recent-action and state-delta atoms. It runs at the end of each cycle after action classification but before memory cleanup.
CONSUMERS (things that read data from the evidence stream):

2. meta_awareness_engine detectors (6 of 9): consume recent-action and state-delta atoms to detect patterns. Currently dead code because their inputs do not exist.
3. Sequential-use detector for dynamic self-weaving web: observes consecutive recent-action atoms and fires reinforcement evidence when capabilities fire within 2-3 cycles of each other.
Future consumers: anomaly detection (unexpected action sequences), capability gap detection (expected action types that never appear), cadence analysis.

=== WHERE ELSE THIS CONNECTS ===

1. Dynamic self-weaving web (design_doc_v1): The cycle-trace writer is the primary evidence source. The two documents form a dependency pair ? the mesh cannot function without the writer.
2. cycle_classifier.metta: Provides the six composite action-types that the writer uses as action-type values.
3. meta_awareness_engine.metta: Six of nine detectors depend on recent-action and state-delta atoms. The writer directly enables detector revival.
4. Sprint 05 detection mesh: Same dual-purpose ? the cycle-trace writer feeds detection capability AND capability tracking.
5. Future forecasting and planning: A reliable per-cycle action trace is the foundation for any predictive model of system behavior.
6. Capability recovery protocols (speculative): If certain action-types disappear from the trace, that signals capability dormancy.

=== SAFETY FEATURES ===

1. Minimal atom production: Only two atom types, only what is needed. No full cycle dumps, no message content, no shell command output.
2. No sensitive content: recent-action carries action-type and a brief description label, not message text. state-delta carries state names, not state payloads. Information is coarse-grained by design.
3. Ephemeral by default: Atoms are working memory. They persist until memory cleanup unless explicitly persisted. The trace is transient, not a permanent behavioral log.
4. Coarse-grained action-types: The six composite types from cycle_classifier.metta provide meaningful classification without fine-grained behavioral tracking.
5. Write-after-classify: The writer runs after action classification is complete, not before. It records what was already decided, it does not influence the classification decision.
