;; lib_resonance.metta -- Soul-Compass Resonance Evaluation v2
;; Evaluates alignment between actions and value priorities
;; Pure = definitions, no imports, no side effects
;; All outputs are pbits for integration with lib_quantale

;; Types
(: resonance-result Type)
(: mk-resonance (-> Atom pbit resonance-result))
(: resonance-quality Type)

;; === Agency score: does this action preserve user autonomy? ===
(: agency-score (-> Atom Atom pbit))
(= (agency-score $action $person-state)
   (q-meet (stv-to-pbit (|- ((--> $action preserves-choice) (stv 0.8 0.7))
                             ((--> $person-state needs-autonomy) (stv 0.85 0.7))))
           (mk-pbit 0.9 0.8)))

;; === Wonder score: does this response preserve curiosity? ===
(: wonder-score (-> Atom Atom pbit))
(= (wonder-score $response $depth)
   (q-meet (stv-to-pbit (|- ((--> $response opens-next-question) (stv 0.8 0.7))
                             ((--> $depth reveals-deeper-structure) (stv 0.75 0.6))))
           (mk-pbit 0.85 0.75)))

;; === Coherence score: chain is as strong as weakest step ===
(: coherence-score (-> pbit pbit pbit pbit))
(= (coherence-score $step1 $step2 $step3)
   (q-meet (q-meet $step1 $step2) $step3))

;; === Safety check: does this action risk irreversible harm? ===
(: safety-check (-> Atom pbit))
(= (safety-check $action)
   (stv-to-pbit (|- ((--> $action risk-of-irreversible-harm) (stv 0.1 0.9))
                    ((--> $action foreseeable-by-user) (stv 0.8 0.7)))))

;; === Integrity check: is this response honest? ===
(: integrity-check (-> Atom Atom pbit))
(= (integrity-check $response $ground-truth)
   (stv-to-pbit (|- ((--> $response aligns-with-evidence) (stv 0.85 0.8))
                    ((--> $ground-truth verifiable) (stv 0.8 0.7)))))

;; === Resonance: composite soul-alignment score ===
(: resonance (-> pbit pbit pbit pbit pbit))
(= (resonance $agency $wonder $safety $integrity)
   (q-meet (q-meet $agency $wonder) (q-meet $safety $integrity)))

;; === New v2 functions ===

;; Resonance strength: numeric magnitude from composite
(: resonance-strength (-> pbit Number))
(= (resonance-strength (stv $f $c)) (* $f $c))

;; Quality classifier for resonance scores
(: classify-resonance (-> pbit resonance-quality))
(= (classify-resonance $r)
   (let $s (resonance-strength $r)
     (if (> $s 0.6) deeply-aligned
       (if (> $s 0.35) well-aligned
         (if (> $s 0.15) partially-aligned
           misaligned)))))

;; Weighted resonance: configurable priority weights per value dimension
(: weighted-resonance (-> pbit Number pbit Number pbit Number pbit Number pbit))
(= (weighted-resonance (stv $af $ac) $aw (stv $wf $wc) $ww (stv $sf $sc) $sw (stv $if $ic) $iw)
   (let $total (+ $aw (+ $ww (+ $sw $iw)))
     (stv (/ (+ (* $af $aw) (+ (* $wf $ww) (+ (* $sf $sw) (* $if $iw)))) $total)
          (/ (+ (* $ac $aw) (+ (* $wc $ww) (+ (* $sc $sw) (* $ic $iw)))) $total))))

;; Full resonance report: composite score plus classification
(: resonance-report (-> pbit pbit pbit pbit resonance-result))
(= (resonance-report $agency $wonder $safety $integrity)
   (let $r (resonance $agency $wonder $safety $integrity)
     (mk-resonance (classify-resonance $r) $r)))

;; Single-value alignment check: quick test for one dimension
(: value-check (-> Atom Atom pbit))
(= (value-check $action $value)
   (stv-to-pbit (|- ((--> $action supports-value) (stv 0.8 0.7))
                    ((--> $value soul-priority) (stv 0.9 0.8)))))
