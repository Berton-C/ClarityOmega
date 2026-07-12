;; soul_lock_structural_harness.metta
;; Direction B ONLY, isolated. The prior run proved no native string-length
;; (string_length/string-length unreduced) and then HALTED on (length "abc")
;; which wants a list, starving B/C. Lesson: a known-risky probe ahead of the
;; real test aborts the run. So this harness runs ONLY the structural atom-lock,
;; which uses proven structural == and get-state, no string ops, nothing risky.
;;
;; Lock holds an ATOM: clear = symbol `unlocked`; held = (locked <arg>).
;; pending? = NOT (== state unlocked). Replaces the dead string_length form.

!(bind! &lockA (new-state unlocked))

;; clear state reads back as unlocked ->
!(RESULT-1 (== (get-state &lockA) unlocked))
;; pending? when clear -> False
!(RESULT-2 (if (== (get-state &lockA) unlocked) False True))

;; set held
!(change-state! &lockA (locked soul-note))
;; pending? when held -> True
!(RESULT-3 (if (== (get-state &lockA) unlocked) False True))
;; sanity: what does get-state return when held
!(RESULT-4 (get-state &lockA))

;; reclear
!(change-state! &lockA unlocked)
;; pending? after reclear -> False
!(RESULT-5 (if (== (get-state &lockA) unlocked) False True))

;; the actual pending predicate as it would be defined, exercised end to end:
(= (soul-mutation-pending-test?)
   (if (== (get-state &lockA) unlocked) False True))
!(RESULT-6 (soul-mutation-pending-test?))
!(change-state! &lockA (locked soul-pattern))
!(RESULT-7 (soul-mutation-pending-test?))
!(change-state! &lockA unlocked)
!(RESULT-8 (soul-mutation-pending-test?))
