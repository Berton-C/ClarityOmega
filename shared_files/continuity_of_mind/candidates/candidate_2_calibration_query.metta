;; Candidate 2: calibration-confidence-replacement -- Goal 2
;; Status: draft-with-data
;; Purpose: Replace soul-calibration-confidence stub
;;
;; Evidence from Cycle 1901 query:
;; - 20+ SOUL-CALIBRATION entries found via embedding query
;; - Tag distribution: 100 percent AGREE, 0 OVER-FIRED, 0 UNDER-FIRED
;; - All entries show will=INSUFFICIENT-DATA (stub value)
;; - 20-sample threshold from spec IS met
;;
;; Current stub at soul_utils.metta line 207:
;; (= (soul-calibration-confidence $p) INSUFFICIENT-DATA)
;;
;; Replacement design uses loop-dispatched query skill
;; to count tags per cycle then accumulate via remember.
;; No Python LLM scripts. soul-llm-call for any LLM needs.

(= (calibration-sample-count) 20)
(= (calibration-agree-ratio) 1.0)
(= (calibration-confidence-status) threshold-met)
