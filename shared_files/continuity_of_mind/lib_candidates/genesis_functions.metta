;; Genesis Engine Function Implementations
;; Candidate file per spec Section 4a -- test before promoting
;; Date: 2026-04-22

;; --- sample-atom-from ---
;; Given a domain tag, return atoms registered in that domain.
;; Uses pattern matching against genesis-domain-registry atoms.
(= (sample-atom-from $domain)
   (match &self (genesis-domain-registry $domain $atom $source) $atom))

;; --- paraconsistency-test ---
;; Given two values, check if they form a known paraconsistency pair.
;; Returns tension-confirmed or tension-not-found.
(= (paraconsistency-test $v1 $v2)
   (if (match &self (genesis-paraconsistency-pair $v1 $v2) True)
       (tension-confirmed $v1 $v2)
       (if (match &self (genesis-paraconsistency-pair $v2 $v1) True)
           (tension-confirmed $v2 $v1)
           (tension-not-found $v1 $v2))))

;; --- genesis-hold ---
;; Hold two atoms in conjunction without resolving the tension.
;; Returns a HeldTension structure preserving both sides.
(= (genesis-hold $atom1 $atom2 $tension-type)
   (HeldTension $atom1 $atom2 $tension-type
     (genesis-hold-principle Examine-what-emerges-from-tension-itself)))

;; --- genesis-create ---
;; Given a HeldTension, use NAL to derive a novel insight.
;; The caller supplies the insight name and description after reflection.
(= (genesis-create (HeldTension $a1 $a2 $ttype $principle) $insight-name $description)
   (genesis-output $insight-name $description
     (cross-domain $a1 $a2)))
