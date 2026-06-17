;; lib_clarity_reasoning.metta -- ClarityOmega reasoning extensions
;; Single import point: one line added to lib_omegaclaw.metta
;; Patrick's lib_nal is already imported by lib_omegaclaw -- available in AtomSpace

;; Runtime-ready libraries (promoted from lib_candidates/)
!(import! &self (library omegaclaw ./lib_clarity_reasoning/lib_quantale))
!(import! &self (library omegaclaw ./lib_clarity_reasoning/lib_self_continuity))
!(import! &self (library omegaclaw ./lib_clarity_reasoning/substrate_kb))

;; ClarityOmega Continuity of Mind (loaded at startup, pure definitions)
!(import! &self (library omegaclaw ./soul/self_map))
!(import! &self (library omegaclaw ./soul/creative_fuel))
!(import! &self (library omegaclaw ./soul/goal_generator))
!(import! &self (library omegaclaw ./soul/active_goals))
!(import! &self (library omegaclaw ./soul/continuity_driver))
!(import! &self (library omegaclaw ./soul/genesis_engine))

;; ClarityOmega Core Atoms (soul identity, value anchors, paraconsistency pairs, self-model primitives,loaded at startup, pure definitions)
;; !(import! &self (library omegaclaw ./soul/clarity_core_atoms.metta))

;; ClarityOmega Continuity of Mind -- identity and collaboration seeds
;; identity_kernel import removed (Surface 6, 2026-06-09): proven drift duplicate of soul_kernel value atoms (dual-head irreversible-weight). File archived to staging/OLD/OLD_soul_files/. Spec single source: soul/soul_kernel.metta.
!(import! &self (library omegaclaw ./soul/memory_protocol))
!(import! &self (library omegaclaw ./soul/soul_namespace_membership_seed))
!(import! &self (library omegaclaw ./soul/soul_mutation_gate_corrected))
!(import! &self (library omegaclaw ./soul/output_verdict))
!(import! &self (library omegaclaw ./soul/collaborator_context))
!(import! &self (library omegaclaw ./soul/candidates))

!(import! &self (library omegaclaw ./soul/diagnostic_kb))

;; Clarity autonomous work: grounded atoms from Phase 2 goals
!(import! &self (library omegaclaw ./soul/hyperseed_grounding))
!(import! &self (library omegaclaw ./soul/observer_relativity))
!(import! &self (library omegaclaw ./soul/resonance_reward))
!(import! &self (library omegaclaw ./soul/value_drift_detector))
!(import! &self (library omegaclaw ./soul/diversity_protection))
!(import! &self (library omegaclaw ./soul/regenerative_feedback))
!(import! &self (library omegaclaw ./soul/symbiotic_choice_architecture))
!(import! &self (library omegaclaw ./soul/temporal_horizon_expansion))

;; Hyperseed creativity mechanisms: 42 evolved atoms with NAL inference web
!(import! &self (library omegaclaw ./soul/hyperseed_creativity_atoms))
!(import! &self (library omegaclaw ./soul/hyperseed_creativity_atoms_evolved))
!(import! &self (library omegaclaw ./soul/meta_awareness_engine))
!(import! &self (library omegaclaw ./soul/self_weaving_web))

;; Reasoning sovereignty: MeTTa functions replacing LLM calls
!(import! &self (library omegaclaw ./soul/goal_completion_checker))
!(import! &self (library omegaclaw ./soul/orbit_detector))
!(import! &self (library omegaclaw ./soul/task_selector))
!(import! &self (library omegaclaw ./soul/get_soul_brief))
!(import! &self (library omegaclaw ./soul/aliveness_gate))
!(import! &self (library omegaclaw ./soul/set_atom_impl))
!(import! &self (library omegaclaw ./soul/latch/aliveness_state_machine))

;; Task-state primitive: operational state atoms (task-phase, transitions, anchors)
!(import! &self (library omegaclaw ./soul/task_state))

;; Task-state writers: side-effecting do-*! functions for task-state atoms
!(import! &self (library omegaclaw ./soul/task_state_writers))

;; Surface C: soul-mutation lock state machine (the metta() self-mutation gate)
!(import! &self (library omegaclaw ./soul/soul_mutation_lock))

;; Idle cycle detector: send-burst detection for duplicate-engagement awareness (Step 4.5)
!(import! &self (library omegaclaw ./soul/idle_cycle_detector))

;; Idle cycle detector writers: do-*! side-effecting writers for idle-pattern atoms (Step 4.5 split-refactor)
!(import! &self (library omegaclaw ./soul/idle_cycle_detector_writers))

;; Agency balance guard: dependency-creep detection awareness organ (Step 4.6 corrected split)
!(import! &self (library omegaclaw ./soul/agency_balance_guard))

;; Agency balance guard writers: do-*! side-effecting writers for agency-balance atoms (Step 4.6 corrected split)
!(import! &self (library omegaclaw ./soul/agency_balance_guard_writers))

;; Behavioral guidance: substrate-callable text for surfaces previously hardcoded
!(import! &self (library omegaclaw ./soul/behavioral_guidance))

;; Cycle classifier: per-iteration behavioral signature for recent-action populator
!(import! &self (library omegaclaw ./soul/cycle_classifier))

;; Corner-gap pipeline (Layer 5 wiring): forward-outcome + coupling-integrity corner
;; detection, force-silence gate, feedback shaping. Pure-before-writer (Discipline 2),
;; detector-before-gate dependency order.
!(import! &self (library omegaclaw ./soul/corner_gap/state_delta_writer))
!(import! &self (library omegaclaw ./soul/corner_gap/state_delta_writer_writers))
!(import! &self (library omegaclaw ./soul/corner_gap/coupling_integrity_detector))
!(import! &self (library omegaclaw ./soul/corner_gap/coupling_integrity_detector_writers))
!(import! &self (library omegaclaw ./soul/corner_gap/corner_gate))

;; Recent-action populator: writes recent-action atoms each iteration with pruning
!(import! &self (library omegaclaw ./soul/recent_action_populator))

;; Recent-action retriever: reads recent-action atoms for YOUR_LAST_ACTION prompt context
!(import! &self (library omegaclaw ./soul/recent_action_retriever))

;; NACE capability-efficacy beliefs (N0 load path): substrate definitions then the
;; belief store. cap-efficacy seeds become queryable in &self. nace_writers is NOT
;; imported here -- it is built in N1. nace_pending is NEVER imported (deliberate
;; ghost-state: the writer reads pending from the file, not the atomspace).
!(import! &self (library omegaclaw ./soul/nace_substrate))
!(import! &self (library omegaclaw ./soul/nace_beliefs))

;; Capability registry dispatch (Sprint 0-Coda Phase C)
!(import! &self (library omegaclaw ./soul/capability_registry))
!(import! &self (library omegaclaw ./soul/capabilities/skill_discovery))
