;; lib_clarity_reasoning.metta -- ClarityClaw reasoning extensions
;; Single import point: add one line to lib_omegaclaw.metta
;; !(import! &self (library omegaclaw lib_clarity_reasoning))

;; Build on lib_nal foundation (already imported by lib_omegaclaw)

;; ClarityClaw reasoning extensions
!(import! &self (library omegaclaw ./lib/lib_nal_extended))
!(import! &self (library omegaclaw ./lib/lib_paraconsistent))
!(import! &self (library omegaclaw ./lib/lib_quantale))
!(import! &self (library omegaclaw ./lib/lib_web_detect))
!(import! &self (library omegaclaw ./lib/lib_resonance))
