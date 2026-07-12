;; soul_gate_callform_harness.metta
;; The full-gate FAILs (RESULT-4/5/6) were the inner (add-atom ...) EXECUTING
;; before binding to the function arg, instead of being passed as data. The
;; passing structural harness quoted at the call site. This harness determines
;; the EXACT correct call form for the two affected functions, side by side, so
;; we wire the right form, not a guess.
;;
;; The functions (already loaded from the gate file):
;;   (= (soul-extract-metta-arg (metta $arg)) $arg)
;;   (= (soul-target-head $arg) (car-atom (car-atom (cdr-atom (cdr-atom (quote $arg))))))
;;   (= (soul-metta-targets-soul-namespace? $arg) (soul-head-is-member? (soul-target-head $arg)))
;; soul-head-is-member? + a tag for soul-note must exist; seed one here.
!(add-atom &self (soul-ns-member soul-note))

;; ---- soul-extract-metta-arg call forms ----
;; A: bare (metta (add-atom...)) -> inner add-atom executes (the bug). Expect wrong.
!(RESULT-1 (soul-extract-metta-arg (metta (add-atom &self (soul-note x)))))
;; B: quote the whole metta expr -> pattern (metta $arg) may not match (quote ...). Test.
!(RESULT-2 (soul-extract-metta-arg (quote (metta (add-atom &self (soul-note x))))))
;; C: the arg as a quoted literal where add-atom is already inert via quote on inner only
!(RESULT-3 (soul-extract-metta-arg (metta (quote (add-atom &self (soul-note x))))))

;; ---- soul-metta-targets-soul-namespace? call forms ----
;; D: bare -> inner add-atom executes (the bug). Expect wrong/unreduced.
!(RESULT-4 (soul-metta-targets-soul-namespace? (add-atom &self (soul-note x))))
;; E: quote the whole add-atom expr at call site (matches passing structural harness)
!(RESULT-5 (soul-metta-targets-soul-namespace? (quote (add-atom &self (soul-note x)))))
;; F: target-head directly on a quoted expr (proven form from structural harness)
!(RESULT-6 (soul-target-head (quote (add-atom &self (soul-note x)))))
;; G: the FULL proven chain inline (what RESULT-10 did in the passing harness)
!(RESULT-7 (let $h (car-atom (car-atom (cdr-atom (cdr-atom (quote (add-atom &self (soul-note x)))))))
   (soul-head-is-member? $h)))
