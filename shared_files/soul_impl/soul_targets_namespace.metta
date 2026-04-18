; === soul-targets-namespace Predicate ===
; Referenced by mutation_lock_upgrade.metta but previously undefined
; Purpose: detect whether an atom or string references the soul namespace
; Soul namespace atoms start with: soul-, clarity-value-, clarity-soul-

; String prefix matching
(= (soul-targets-namespace $atom)
  (let $str (repr $atom)
    (or (starts-with $str "soul-")
      (or (starts-with $str "clarity-value-")
        (or (starts-with $str "clarity-soul-")
          (or (starts-with $str "(soul-")
            (or (starts-with $str "(clarity-value-")
              (starts-with $str "(clarity-soul-"))))))))

; Fallback for non-representable atoms
(= (soul-targets-namespace $atom)
  (if (== (get-type $atom) Symbol)
    (let $str (repr $atom)
      (or (starts-with $str "soul-") (starts-with $str "clarity-")))
    False))

; Helper: starts-with check via py-call
(= (starts-with $str $prefix)
  (py-call (helper.str_starts_with $str $prefix)))