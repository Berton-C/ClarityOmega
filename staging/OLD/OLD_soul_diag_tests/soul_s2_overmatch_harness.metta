;; soul_s2_overmatch_harness.metta
;; DECISIVE existing-atoms test: does S2 (exists-in-atomspace by head match)
;; distinguish soul-namespace heads from arbitrary NON-soul atoms that also live
;; in the atomspace? If a non-soul head that exists returns a match under the
;; gate's detection, S2 OVER-MATCHES and is unsafe for a safety interlock.
;; Inline-tagged results (RESULT-N value), proven pattern.
;;
;; The atomspace in production holds far more than soul atoms. We seed the real
;; KINDS: task-state, recent-action, idle-pattern, plus soul atoms, then ask the
;; gate's question two ways and see if it discriminates.

;; ----- seed the realistic mixed atomspace -----
;; soul-namespace atoms (as they exist today, added by ordinary add-atom):
!(add-atom &self (soul-pattern-x compass))
!(add-atom &self (soul-priority-hierarchy core))
!(add-atom &self (soul-note something))
;; NON-soul runtime atoms (the real neighbors in &self):
!(add-atom &self (task-state 3 pending))
!(add-atom &self (recent-action 7 responsive-send hello))
!(add-atom &self (idle-pattern 2 resting))
!(add-atom &self (coupling-status 4 corner))

;; ================================================================
;; S2 detection AS THE GATE WOULD USE IT.
;; The gate extracts the target head from a proposed (add-atom &self (HEAD ...))
;; and must decide soul-namespace or not. S2's idea: "head is soul-namespace iff
;; an atom with that head already exists in &self." Test BOTH a soul head and a
;; non-soul head that BOTH exist. If both return >0, S2 cannot tell them apart.
;; ================================================================

;; --- generic "does an atom with this head exist" probe (the S2 mechanism) ---
;; NOTE: S2 in the proof log matched a SPECIFIC head pattern (soul-pattern-x $b).
;; The gate cannot hardcode each head; it must check the EXTRACTED head var.
;; The honest question: can match take a VARIABLE head? Test it directly.

;; S2a: variable-head match (can MeTTa match (HEAD $b) with HEAD bound at runtime?)
!(RESULT-1 (let $h soul-pattern-x
   (size-atom (collapse (match &self ($h $b) $b)))))
!(RESULT-2 (let $h task-state
   (size-atom (collapse (match &self ($h $b) $b)))))
!(RESULT-3 (let $h recent-action
   (size-atom (collapse (match &self ($h $b) $b)))))

;; S2b: if variable-head match does not work, the gate would need a fixed
;; pattern, which cannot generalize. Probe whether ($h $b) even binds.
!(RESULT-4 (let $h soul-note
   (size-atom (collapse (match &self ($h $b) $b)))))

;; ================================================================
;; CONTRAST: S1 tag-based detection on the SAME mixed atomspace.
;; Tag only the soul atoms (as a startup seed would), then detect. A non-soul
;; head must NOT be a member even though it exists in &self.
;; ================================================================
(= (soul-head-is-member? $head)
   (if (> (size-atom (collapse (match &self (soul-ns-member $head) $head))) 0)
       True False))

;; startup-seed tags for the EXISTING soul heads (does not touch the atoms):
!(add-atom &self (soul-ns-member soul-pattern-x))
!(add-atom &self (soul-ns-member soul-priority-hierarchy))
!(add-atom &self (soul-ns-member soul-note))

;; S1 on soul head that exists -> True; on non-soul head that ALSO exists -> False
!(RESULT-5 (soul-head-is-member? soul-pattern-x))
!(RESULT-6 (soul-head-is-member? task-state))
!(RESULT-7 (soul-head-is-member? recent-action))
!(RESULT-8 (soul-head-is-member? soul-note))

;; full chain S1 with extracted head, soul vs non-soul target:
!(RESULT-9 (let $h (car-atom (car-atom (cdr-atom (cdr-atom (quote (add-atom &self (soul-note x)))))))
   (soul-head-is-member? $h)))
!(RESULT-10 (let $h (car-atom (car-atom (cdr-atom (cdr-atom (quote (add-atom &self (task-state x)))))))
   (soul-head-is-member? $h)))
