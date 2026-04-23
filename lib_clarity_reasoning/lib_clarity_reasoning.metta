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
