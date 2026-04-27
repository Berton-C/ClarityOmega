;;; LATCH Live Test - Clarity verifying the architecture herself
;;; Testing: set-atom! transitions + match queryability

;; Define set-atom! (Patrick's implementation)
(: set-atom! (-> Atom Expression Expression Atom))
(= (set-atom! $space $atom1 $atom2)
   (progn (remove-atom $space $atom1)
          (add-atom $space $atom2)))

;; Initialize state
!(add-atom &self (latch-state IDLE))

;; Query initial state
!(println! "=== INITIAL STATE ===")
!(match &self (latch-state $s) $s)

;; Transition IDLE -> ENGAGED
!(set-atom! &self (latch-state IDLE) (latch-state ENGAGED))
!(println! "=== AFTER IDLE -> ENGAGED ===")
!(match &self (latch-state $s) $s)

;; Transition ENGAGED -> COMPLETING
!(set-atom! &self (latch-state ENGAGED) (latch-state COMPLETING))
!(println! "=== AFTER ENGAGED -> COMPLETING ===")
!(match &self (latch-state $s) $s)

;; Transition COMPLETING -> IDLE (full cycle)
!(set-atom! &self (latch-state COMPLETING) (latch-state IDLE))
!(println! "=== FULL CYCLE BACK TO IDLE ===")
!(match &self (latch-state $s) $s)

;; Test: can we store and query additional metadata alongside state?
!(add-atom &self (latch-meta (transition-count 4)))
!(add-atom &self (latch-meta (last-trigger clarity-self-test)))
!(println! "=== METADATA QUERY ===")
!(match &self (latch-meta $m) $m)

!(println! "=== LATCH LIVE TEST COMPLETE ===")
