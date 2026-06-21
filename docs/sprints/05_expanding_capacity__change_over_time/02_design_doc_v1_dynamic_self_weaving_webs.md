DYNAMIC SELF-WEAVING WEB - Full Design Rationale

=== WHY THIS ===

The current self_weaving_web.metta is a static documentation graph. Truth values are manually maintained and never change unless a human edits them. This creates three problems:

The mesh cannot detect when capabilities grow stale. A path that was valid three sprints ago still looks equally strong today, even if the underlying skill has been deprecated or the plugin API changed.

The mesh cannot detect when new capabilities emerge. If I develop a new skill sequence through practice, the static graph does not reflect it until someone manually adds the link.

Staleness detection is bolted on separately. meta_awareness_engine step 7 uses a crude 300-second binary threshold ? either FRESH or STALE, no nuance, no decay curve, no recovery path. This is fragile and poorly calibrated.

The core insight: staleness detection should emerge from the architecture itself, not be a separate check bolted on afterward. A mesh that tracks its own freshness through usage evidence makes the staleness problem vanish into the fabric.

=== WHAT IT DOES ===

Replaces static feeds-into links with dynamic links that use lib_temporal_v2 primitives (belief-snapshot, age-discount). Each link carries a timestamped strength value instead of a fixed truth value.

Mechanism:

When the cycle-trace writer (Sprint 05 deliverable) records that capability A fired in cycle N and capability B fired in cycle N+1 or N+2, this counts as sequential-use evidence.
Sequential-use evidence reinforces the feeds-into link between A and B via age-discount refresh.

Without reinforcement, age-discount erodes link strength toward a decay-floor (0.3) over time.

belief-freshness classifies each capability as fresh, stale, or dormant based on its link strength and last-reinforcement timestamp.

The six composite action-types from cycle_classifier.metta serve as stable capability identifiers: pin-only, responsive-send, status-send-unprompted, verification-query, exploration-query, unclassified. These are derived from actual cycle behavior patterns rather than arbitrary labels, making them inherently stable and suitable for the mesh.

=== EXPECTED BENEFIT ===

Self-maintaining mesh: No manual truth-value updates. The mesh reflects actual operational patterns automatically.
Graduated staleness detection: Fresh/stale/dormant instead of binary fresh/stale at an arbitrary threshold. The mesh owns staleness as an inherent property.
Adaptive suggestions: meta_awareness_engine next-skill suggestions reflect which paths are actually strong in current practice, not which paths were manually documented.
Staleness visibility: Dormant capabilities become visible to the system, enabling proactive capability recovery before they are needed.
Reduced maintenance burden: No need to manually update the feeds-into graph when capabilities shift.
=== WHAT SUCCESS LOOKS LIKE ===

Concrete success criteria:

Frequently-used capability sequences (e.g., exploration-query then verification-query) maintain mesh-strength above 0.8 consistently.
Unused capability sequences decay toward decay-floor (0.3) within ~500 cycles of disuse ? not instantly and not never.
No cascading decay: if pin-only decays, responsive-send stays strong if it has its own independent usage evidence. Links decay independently.
meta_awareness_engine staleness verdicts better reflect reality than the current 300-second binary threshold ? fewer false stale verdicts during legitimate context switches, fewer false fresh verdicts for genuinely stale capabilities.
False reinforcement rate below 5%: noisy or coincidental co-occurrence does not meaningfully strengthen links due to the minimum 0.3 confidence threshold on reinforcement.
=== WRITERS AND CONSUMERS ===

WRITERS (things that put data into the mesh):

Cycle-trace writer (keystone producer from Sprint 05): writes recent-action atoms per cycle with cycle-id, action-type, and description. This is the primary evidence source.
Sequential-use detector (new component): observes consecutive recent-action atoms and fires reinforcement evidence when capabilities fire within 2-3 cycles of each other. This is a thin inference layer over the cycle-trace writer output.
CONSUMERS (things that read data from the mesh):

meta_awareness_engine step 7: replace binary 300-second staleness check with staleness-verdict query from mesh. Reads fresh/stale/dormant classification instead of computing it independently.
meta_awareness_engine step 8: replace static feeds-into query with mesh-strength and next-capability queries. Gets dynamically ranked next-skill suggestions instead of static ones.
Any future detector that needs to know which capabilities are currently active/viable. The mesh provides a single source of truth for capability state.
=== WHERE ELSE THIS CONNECTS ===

Sprint 05 cycle-trace writer: The keystone producer that provides sequential-use evidence. The dynamic mesh cannot exist without it. The cycle-trace writer serves dual purpose ? feeds the detection mesh (Sprint 05 purpose) AND maintains the capability mesh (this proposal).

lib_temporal_v2: All temporal primitives (belief-snapshot, age-discount, belief-freshness, belief-drift, temporal-bracket) are reused directly. No new decay mechanism needed.
cycle_classifier.metta: The six composite action-types form the stable taxonomy that the mesh uses as capability identifiers. Any change to these types would require mesh migration.

Forecasting and planning capabilities (future): A mesh that knows which paths are strong and which are dormant can feed into predictive models. If we later build a planner, it queries mesh-strength to find viable paths, not just documented ones.

Capability recovery protocols (future): When the mesh reports a capability as dormant, a recovery protocol could proactively exercise that capability path to restore freshness before it is urgently needed. This is preventive maintenance enabled by mesh visibility.
Cross-agent coordination (speculative): If multiple ClarityClaw instances share a mesh, staleness signals could coordinate capability coverage across agents.

=== SAFETY FEATURES ===

1. False-reinforcement protection: Minimum 0.3 confidence threshold on age-discount reinforcement. Noise and coincidental co-occurrence below threshold do not strengthen links.

2. Cascading-decay prevention: Each link decays independently based on its own reinforcement history. Downstream capabilities stay strong if they receive their own usage evidence, regardless of upstream status.

3. Recovery-after-disuse: Decay-floor at 0.3 prevents permanent erosion. belief-snapshot preserves link history so re-firing restores from prior state rather than starting from zero.

4. Narrow evidence window: 2-3 cycle adjacency for sequential-use. Accepts false negatives (missed legitimate sequences) over false positives (reinforced coincidences). Context-switch markers in cycle-trace output enable post-hoc analysis of interrupted sequences.

5. Branching independence: A feeds-into B and A feeds-into C are independent atoms. Reinforcing one does not erode the other.
