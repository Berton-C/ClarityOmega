;; calibration_logger_v2.metta -- Dual-backend calibration event logger
;; Author: ClarityClaw autonomous cycle 3528
;; Date: 2026-04-24
;; Purpose: Log calibration events to BOTH AtomSpace (MeTTa-queryable) AND
;;          ChromaDB (persistent, read by soul-calibration-confidence via helper.py)
;; Supersedes: calibration_logger.metta (AtomSpace-only version)
;; Integration: calibration_bridge.py provides ChromaDB write functions

;; ============================================================
;; Section 1: AtomSpace event tracking (preserved from v1)
;; ============================================================
(= (calibration-agree-count) 0)
(= (calibration-disagree-count) 0)
(= (calibration-total-count) 0)

;; ============================================================
;; Section 2: Dual-backend log function
;; Logs to AtomSpace counters AND ChromaDB via py-call bridge
;; ============================================================
(= (log-calibration-event agree $timestamp)
   (superpose
     ((set! (calibration-agree-count) (+ (calibration-agree-count) 1))
      (set! (calibration-total-count) (+ (calibration-total-count) 1))
      (py-call (calibration_bridge.log_calibration_event agree $timestamp AGREE)))))

(= (log-calibration-event disagree $timestamp)
   (superpose
     ((set! (calibration-disagree-count) (+ (calibration-disagree-count) 1))
      (set! (calibration-total-count) (+ (calibration-total-count) 1))
      (py-call (calibration_bridge.log_calibration_event disagree $timestamp DISAGREE)))))

;; ============================================================
;; Section 3: Confidence computation (AtomSpace-side, for fast queries)
;; Returns ratio after minimum 20 samples, else INSUFFICIENT-DATA
;; ============================================================
(= (soul-calibration-confidence-local)
   (if (>= (calibration-total-count) 20)
       (/ (calibration-agree-count) (calibration-total-count))
       INSUFFICIENT-DATA))

;; ============================================================
;; Section 4: Version and status
;; ============================================================
(= (calibration-logger-version) v2-dual-backend-2026-04-24)
(= (calibration-logger-status) live)
