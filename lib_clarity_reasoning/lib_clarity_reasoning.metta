;; lib_clarity_reasoning.metta -- ClarityClaw reasoning extensions
;; Single import point: one line added to lib_omegaclaw.metta
;; Patrick's lib_nal is already imported by lib_omegaclaw -- available in AtomSpace

;; Runtime-ready libraries (promoted from lib_candidates/)
!(import! &self (library omegaclaw ./lib_clarity_reasoning/lib_quantale))
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
