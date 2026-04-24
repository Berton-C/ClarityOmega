;; Candidate 2: soul-calibration-confidence replacement
;; Replaces stub at soul_utils.metta line 207
;; Uses py-call to helper.soul_calibration_confidence_query
;; NO LLM calls. ChromaDB read-only. soul-llm-call is sole LLM interface.
;;
;; Current stub:
;; (= (soul-calibration-confidence $p) INSUFFICIENT-DATA)
;;
;; Replacement:
(= (soul-calibration-confidence $p)
   (py-call (helper.soul_calibration_confidence_query $p)))
;;
;; Promotion path:
;; 1. Add soul_calibration_confidence_query to src/helper.py
;; 2. Replace line 207 in soul/soul_utils.metta
;; 3. Verify via metta eval
