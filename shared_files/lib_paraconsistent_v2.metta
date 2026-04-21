;; lib_paraconsistent.metta -- Paraconsistent Logic for ClarityOmega v2
;; Tolerates contradictions without explosion, routes through tension
;; Pure = definitions only, no imports, no side effects

;; Types
(: tension-level Type)
(: tension-report Type)
(: mk-tension-report (-> Atom tension-level Number tension-report))

;; === Classify tension between two beliefs ===
(: classify-tension (-> pbit pbit tension-level))
(= (classify-tension (stv $f1 $c1) (stv $f2 $c2))
   (let $delta (max (- $f1 $f2) (- $f2 $f1))
     (let $conf (min $c1 $c2)
       (if (> (* $delta $conf) 0.5) critical-tension
         (if (> (* $delta $conf) 0.25) active-tension
           (if (> (* $delta $conf) 0.1) mild-tension
             no-tension))))))

;; === Temporary routing: hold both sides without collapsing ===
(: temp-route (-> Atom Atom Atom Atom))
(= (temp-route $belief1 $belief2 $context)
   (hold-both $belief1 $belief2 $context))

;; === Hold contradiction: explicit marker that both are retained ===
(: hold-contradiction (-> Atom Atom Atom))
(= (hold-contradiction $a $b)
   (paraconsistent-pair $a $b))

;; === Soul-goal tension: does a goal conflict with a soul value? ===
(: soul-goal-tension (-> Atom Atom pbit tension-level))
(= (soul-goal-tension $goal $value $strength)
   (classify-tension $strength (stv 1.0 0.9)))

;; === Introspect tension: surface the tension as a named report ===
(: introspect-tension (-> Atom Atom pbit tension-report))
(= (introspect-tension $a $b $strength)
   (mk-tension-report (tension-between $a $b) (classify-tension $strength (stv 1.0 0.9)) 0.0))

;; === New v2 functions ===

;; Tension strength: numeric magnitude of contradiction
(: tension-strength (-> pbit pbit Number))
(= (tension-strength (stv $f1 $c1) (stv $f2 $c2))
   (* (max (- $f1 $f2) (- $f2 $f1)) (min $c1 $c2)))

;; Severity classifier with finer grain
(: tension-severity (-> Number tension-level))
(= (tension-severity $mag)
   (if (> $mag 0.7) explosive-tension
     (if (> $mag 0.5) critical-tension
       (if (> $mag 0.25) active-tension
         (if (> $mag 0.1) mild-tension
           no-tension)))))

;; Dialectical hold: maintain contradiction productively with a reason
(: dialectical-hold (-> Atom Atom Atom tension-report))
(= (dialectical-hold $a $b $reason)
   (mk-tension-report (dialectic $a $b $reason)
     active-tension
     0.0))

;; Multi-tension aggregator: worst tension across a pair set
(: worst-tension (-> tension-level tension-level tension-level))
(= (worst-tension explosive-tension $any) explosive-tension)
(= (worst-tension $any explosive-tension) explosive-tension)
(= (worst-tension critical-tension $any) critical-tension)
(= (worst-tension $any critical-tension) critical-tension)
(= (worst-tension active-tension $any) active-tension)
(= (worst-tension $any active-tension) active-tension)
(= (worst-tension mild-tension $any) mild-tension)
(= (worst-tension $any mild-tension) mild-tension)
(= (worst-tension no-tension no-tension) no-tension)

;; Resolution candidate: propose which belief to weaken if forced
(: resolution-candidate (-> Atom pbit Atom pbit Atom))
(= (resolution-candidate $a (stv $f1 $c1) $b (stv $f2 $c2))
   (if (< (* $f1 $c1) (* $f2 $c2)) $a $b))
