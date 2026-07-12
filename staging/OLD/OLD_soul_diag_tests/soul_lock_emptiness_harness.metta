;; soul_lock_emptiness_harness.metta
;; The full-gate run halted on: Type error `character' expected, found
;; `string_length' (an atom). string_length does NOT reduce in this runtime, it
;; sits unreduced and > errors. We need a working lock-emptiness test.
;; Two directions, inline-tagged results. Whichever reduces cleanly wins.

;; ===== DIRECTION A: does ANY string-length primitive reduce? =====
;; If it reduces, the result is a number; if absent, the call echoes unreduced.
!(RESULT-1 (string_length "abc"))
!(RESULT-2 (string-length "abc"))
!(RESULT-3 (length "abc"))
!(RESULT-4 (size-atom "abc"))

;; ===== DIRECTION B: STRUCTURAL lock (no string ops at all) =====
;; Lock holds an ATOM, not a string. clear = symbol `unlocked`; held = (locked x).
;; Pending = NOT (== state unlocked). Uses proven structural == only.
!(bind! &lockA (new-state unlocked))
!(RESULT-5 (== (get-state &lockA) unlocked))
;; pending? when clear -> should be False (it IS unlocked)
!(RESULT-6 (if (== (get-state &lockA) unlocked) False True))
;; set held, then pending? -> True
!(change-state! &lockA (locked soul-note))
!(RESULT-7 (if (== (get-state &lockA) unlocked) False True))
;; what does get-state return after the change (sanity) ->
!(RESULT-8 (get-state &lockA))
;; reclear, pending? -> False
!(change-state! &lockA unlocked)
!(RESULT-9 (if (== (get-state &lockA) unlocked) False True))

;; ===== DIRECTION C: empty-string discrimination if we must stay string =====
;; Does == against empty string reduce at all (even if unreliable for non-empty)?
!(bind! &lockB (new-state ""))
!(RESULT-10 (== (get-state &lockB) ""))
!(change-state! &lockB "PENDING")
!(RESULT-11 (== (get-state &lockB) ""))
