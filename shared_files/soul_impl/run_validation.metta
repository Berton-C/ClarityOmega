;; Soul Implementation Validation Harness
;; Loads all soul_impl files in dependency order then runs tests
;; Usage: load this single file into MeTTa interpreter

;; Layer 0: Core definitions (no dependencies)
!(import! &self soul_kernel)
!(import! &self soul_targets_namespace)

;; Layer 1: Depends on kernel
!(import! &self layer1_precompute)
!(import! &self calibration_cold_start)
!(import! &self stv_seed_correction)

;; Layer 2: Depends on namespace detection
!(import! &self mutation_lock_upgrade)

;; Layer 3: Depends on kernel + namespace + precompute
!(import! &self output_intercept_impl)

;; Run smoke tests
!(import! &self integration_tests)

!(println! VALIDATION-HARNESS-COMPLETE)
