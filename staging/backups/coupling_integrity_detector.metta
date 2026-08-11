;; coupling_integrity_detector.metta -- three-joint corner detection (pure defs)
;; Author: ClarityClaw  Date: 2026-06-03
;; Emission, Outcome, Intention-coupling -> corner/drift/healthy/composure

(= (emission-present)
   (let $atoms (collapse (match &self (recent-action $c $class) ($c $class)))
      (if (== $atoms ()) False True)))

(= (outcome-present)
   (let $verdict (latest-state-delta-verdict)
      (if (== $verdict forward) True False)))

(= (intention-coupled)
   (let $atoms (collapse (match &self (agency-balance $v $person $system) ($person $system)))
      (if (== $atoms ())
          True
         (let $pair (car-atom $atoms)
            (let $person (car-atom $pair)
               (let $system (car-atom (cdr-atom $pair))
                  (if (>= $person $system) True False)))))))

(= (coupling-verdict)
   (let $emission (emission-present)
      (if (== $emission True)
          (let $outcome (outcome-present)
             (if (== $outcome True)
                 healthy-coupling
                 (let $coupling (intention-coupled)
                    (if (== $coupling True) drifting corner))))
          composure)))