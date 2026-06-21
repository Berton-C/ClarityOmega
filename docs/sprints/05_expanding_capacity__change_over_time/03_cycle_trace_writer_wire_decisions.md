05_cycle_trace_writer_wire_decisions.md
The cycle-trace writer produces three atom types per soul cycle: recent-action, state-delta, and cycle-phase. These are the evidence atoms that six dormant detector channels in the MAE need. Without them, the detectors have zero signal.

Atom inventory
Atom type	Produced by cycle-trace writer	Consumed by	Current status
recent-action	YES (new)	orbit_detector, staleness channel, effort-trap channel	MISSING
state-delta	YES (new)	value_drift_detector, poise channel, diagnostics channel	MISSING
cycle-phase	YES (new)	goal_completion_checker, current-goal channel	MISSING
Wire decisions
Where to place the writer: Inside loop.metta between soul-pre-compute and soul-flourishing-prompt. The writer needs both the pre-cycle state (to compute delta) and the cycle output (to record action). Positioning after pre-compute but before the LLM call captures the entering state; a second pass after the LLM output captures the action.
Temporal vs static: Each atom carries a timestamp from the cycle. lib_temporal_v2 decay rules apply. An atom older than N cycles decreases in strength. This prevents the exact accidental binding the governing principles warn against: a stale recent-action atom that reads as current evidence.
Write mechanism: The writer uses add-atom to inject evidence into the active atomspace. It does NOT use the Python bridge. The writer is MeTTa-native. The bridge is for persistence across restarts; the writer is for live-cycle evidence.
Read mechanism: Detectors use match to query recent-action, state-delta, cycle-phase. No special API. The mesh is atomspace-native. Wire-do-not-add: match already exists.
Keystone property: The writer is not a feature. It is the conduit that makes nine detectors possible. Removing it deactivates all six MAE channels plus three standalone detectors. Adding it activates them. Build and wire in one step.
Wire sequence
Write the cycle-trace writer as a MeTTa function: cycle-trace-record
Insert two calls in loop.metta: one pre-LLM (captures state-delta), one post-LLM (captures recent-action, cycle-phase)
Verify atoms appear in atomspace after one cycle
Verify match in each detector returns non-empty for the first time
At that point: nine detectors move from UNWIRED to LIVE
