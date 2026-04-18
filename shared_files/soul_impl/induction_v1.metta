;; Induction Reasoning via NAL v1
;; Date: 2026-04-17
;; Pattern generalization: from specific instances to general rules
;;
;; NAL induction: given (-> S M) and (-> S P), infer (==> M P)
;; This is the inverse of deduction — generalizing from shared subjects
;;
;; Example instances:
;; cat is animal, cat has fur
;; dog is animal, dog has fur
;; Induction should yield: animal ==> has-fur (low confidence)
;;
;; In NAL this builds evidential support incrementally
;; Each confirming instance raises confidence via revision
;;
;; Test: two instances sharing subject, do we get a general rule?
;; Then revise the two inductive conclusions to strengthen confidence
