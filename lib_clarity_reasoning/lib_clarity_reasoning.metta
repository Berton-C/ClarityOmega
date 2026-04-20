;; lib_clarity_reasoning.metta -- ClarityClaw reasoning extensions
;; Single import point: one line added to lib_omegaclaw.metta
;; Patrick's lib_nal is already imported by lib_omegaclaw -- available in AtomSpace

;; Runtime-ready libraries (promoted from lib_candidates/)
!(import! &self (library omegaclaw ./lib_clarity_reasoning/lib_quantale))
