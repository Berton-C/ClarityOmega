;; soul_utils.metta -- Soul utility functions with live ChromaDB wiring
;; Author: ClarityClaw autonomous cycle 3524
;; Date: 2026-04-24
;; Purpose: Replace conceptual stubs with live py-call wiring to helper.py
;; Spec: soul_utils_wiring_patch.md

;; ============================================================
;; Block 1: Soul Pre-Compute (was hardcoded stub)
;; Queries ChromaDB for calibration confidence, affective state, will
;; Returns grounding context string for soul cycle
;; ============================================================
(= (soul-pre-compute $msg)
   (py-call (helper.soul_pre_compute $msg)))

;; ============================================================
;; Block 2: Soul Calibration Confidence Query (was INSUFFICIENT-DATA stub)
;; Queries ChromaDB soul_calibration collection
;; Returns STRONG/ADEQUATE/WEAK/INSUFFICIENT-DATA based on sample count
;; ============================================================
(= (soul-calibration-confidence $p)
   (py-call (helper.soul_calibration_confidence_query $p)))

;; ============================================================
;; Block 3: Soul Calibration Report (already wired -- included for completeness)
;; ============================================================
;; (soul-calibration-report) is defined in the production soul routing file
;; No change needed per wiring patch spec

;; ============================================================
;; Block 4: Utility helpers
;; ============================================================
(= (soul-utils-version) soul-utils-v1-live-wiring-2026-04-24)
(= (soul-utils-status) live)
