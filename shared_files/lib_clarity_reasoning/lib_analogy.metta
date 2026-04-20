;; lib_analogy.metta -- Analogical reasoning via NAL
;; PERMANENT PATTERN (states 5100-5106): NAL inference steps
;; are atomic. |- does not accept dynamically-bound atoms.
;; Pipeline requires explicit two-phase agent-loop invocation.
;; Tested: nested let, let-star, collapse+superpose all fail.
;; Direct literal calls work perfectly.
;;
;; Usage pattern for agent loop:
;;   Phase 1: (|- shared-A shared-B) -> extract literal result
;;   Phase 2: (|- literal-from-phase1 unique-prop) -> transfer
;;   Confidence: 0.9 -> 0.45 -> 0.29-0.41 through chain
;;
;; This is epistemically correct: longer chains = lower confidence.

(: analogy-result Type)
(: mk-analogy (-> Atom Atom Atom analogy-result))
