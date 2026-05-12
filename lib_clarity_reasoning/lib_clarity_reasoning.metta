;; lib_clarity_reasoning.metta -- ClarityClaw reasoning extensions
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

;; ClarityOmega Continuity of Mind -- identity and collaboration seeds
!(import! &self (library omegaclaw ./soul/identity_kernel))
!(import! &self (library omegaclaw ./soul/memory_protocol))
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

;; Behavioral guidance: substrate-callable text for surfaces previously hardcoded
!(import! &self (library omegaclaw ./soul/behavioral_guidance))

;; Cycle classifier: per-iteration behavioral signature for recent-action populator
!(import! &self (library omegaclaw ./soul/cycle_classifier))

;; Recent-action populator: writes recent-action atoms each iteration with pruning
!(import! &self (library omegaclaw ./soul/recent_action_populator))

;; Recent-action retriever: reads recent-action atoms for YOUR_LAST_ACTION prompt context
!(import! &self (library omegaclaw ./soul/recent_action_retriever))
