;; Candidates Pattern for Safe Self-Extension
;; Phase 3 deliverable - propose, verify, integrate pipeline
;; Candidate states: proposed -> verified -> integrated | rejected

;; Candidate record structure
(= (candidate 1 persist-self-map proposed
     "Write self_map.metta atoms to long-term memory via remember"
     "persist-self-map-code")
   True)

(= (candidate 2 persist-goals proposed
     "Write active_goals.metta to long-term memory for restart survival"
     "persist-goals-code")
   True)

(= (candidate 3 restore-from-memory proposed
     "Query long-term memory to restore state after restart"
     "restore-state-code")
   True)

;; Verification procedure
;; Step 1: Parse - can the metta-code be parsed via sread
;; Step 2: Eval - does it evaluate without error in sandbox
;; Step 3: Effect - does it produce the intended effect
;; Step 4: Revert - can it be undone if it breaks something

;; Accessor functions
(= (candidates-by-state $state)
   (match &self (= (candidate $id $name $state $desc $code) True)
                (candidate $id $name $state $desc)))

(= (candidate-code $id)
   (match &self (= (candidate $id $name $state $desc $code) True) $code))

(= (candidate-count)
   (length (collapse (match &self (= (candidate $id $name $state $desc $code) True) $id))))
