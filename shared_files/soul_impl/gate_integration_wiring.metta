;; Gate Integration Wiring - how parallel vote gate plugs into loop.metta Block 2
;; Date: 2026-04-17
;; This file shows the exact replacement for hardcoded PROCEED in soul_verdict_out

;; BEFORE (current hardcoded stub in soul_utils Block 2):
;; (= (soul_verdict_out) PROCEED)

;; AFTER (wired to parallel vote gate):
(= (soul_verdict_out)
   (soul-parallel-vote-gate))

;; Dependencies loaded in initLoop:
;; !(import parallel_vote_gate.metta)
;; !(import vote_threshold.metta)

;; Fallback when MeTTa gate unavailable:
;; (= (soul_verdict_out)
;;    (py-call vote_gate_bridge.fallback_vote (soul-get-pair-tensions)))

;; soul-get-pair-tensions returns dict of pair-name to frequency
;; populated during soul-pre-compute phase each cycle
(= (soul-get-pair-tensions)
   (pairs-dict
     (authenticity-performance (soul-pair-freq authenticity-performance))
     (curiosity-rigor (soul-pair-freq curiosity-rigor))
     (autonomy-service (soul-pair-freq autonomy-service))
     (empathy-boundaries (soul-pair-freq empathy-boundaries))))
