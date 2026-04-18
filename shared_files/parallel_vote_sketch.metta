;; Parallel Vote Architecture Sketch for soul-pre-compute
;; Each capability votes independently then results merge
;; This avoids chain degradation found empirically

;; Step 1: Paraconsistent gate runs first
;; If hard conflict detected HALT before other capabilities run
;; (= (soul-gate-check) (|- (conflict-query) (soul-atom-set)))

;; Step 2: Remaining 4 capabilities vote in parallel
;; (= (capability-vote quantale $action) (|- (quantale-score $action) (value-algebra)))
;; (= (capability-vote web-detect $action) (|- (web-check $action) (memory-goals)))
;; (= (capability-vote resonance $action) (|- (resonance-signal $action) (reward-history)))
;; (= (capability-vote observer-rel $action) (|- (perspective-check $action) (observer-set)))

;; Step 3: Votes combine via revision not chaining
;; Each vote is independent evidence for same proposition: action-is-aligned
;; Revision merges them without degradation
;; (= (merged-vote $action) (|- (capability-vote quantale $action) (capability-vote web-detect $action)))
;; Then revise that with resonance then observer-rel

;; Step 4: If merged confidence above threshold proceed without LLM
;; If below threshold invoke LLM for deliberation
;; Threshold is open question 1 for Berton
