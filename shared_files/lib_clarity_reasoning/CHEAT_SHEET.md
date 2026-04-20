;; CHEAT_SHEET.md -- Quick Reference for Common Reasoning Patterns
;; State 5132. Copy-paste ready metta calls.
;;
;; === DEDUCTION (A-->B, B-->C => A-->C) ===
;; (metta (|- ((--> A B) (stv f1 c1)) ((--> B C) (stv f2 c2))))
;;
;; === REVISION (merge evidence for same term) ===
;; (metta (|- ((--> A B) (stv f1 c1)) ((--> A B) (stv f2 c2))))
;;
;; === FRAME-SHIFT TEST ===
;; (metta (|- ((--> A B) (stv f 0.9)) ((--> A B) (stv 0.0 0.5))))
;;
;; === CONFIDENCE CLASSIFIER ===
;; (metta (let $c VAL (if (< $c 0.15) blind-spot (if (< $c 0.4) weak (if (< $c 0.7) moderate (if (< $c 0.9) strong established))))))
;;
;; === NEGATION === Use (stv 0.0 0.9)
;;
;; === BANDS ===
;; 0-0.14 blind-spot | 0.15-0.39 weak | 0.4-0.69 moderate | 0.7-0.89 strong | 0.9+ established
;;
;; === IRREVERSIBILITY GATES ===
;; send HIGH | shell CRITICAL | write-file MEDIUM