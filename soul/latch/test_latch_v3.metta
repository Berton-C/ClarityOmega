;; Load set-atom! implementation
(: set-atom! (-> Atom Expression Expression Atom))
(= (set-atom! $space $atom1 $atom2)
   (progn (remove-atom $space $atom1)
          (add-atom $space $atom2)))

;; Seed initial state
!(add-atom &self (latch-state IDLE))

;; Query initial state
!(println! (INITIAL-STATE: (match &self (latch-state $s) $s)))

;; Transition IDLE -> ENGAGED
!(set-atom! &self (latch-state IDLE) (latch-state ENGAGED))

;; Query after transition
!(println! (AFTER-TRANSITION: (match &self (latch-state $s) $s)))

;; Test guarded transition (should succeed: ENGAGED -> COMPLETING)
!(if (== (match &self (latch-state $s) $s) ENGAGED)
    (set-atom! &self (latch-state ENGAGED) (latch-state COMPLETING))
    (println! GUARD-BLOCKED))

;; Query final state
!(println! (FINAL-STATE: (match &self (latch-state $s) $s)))
