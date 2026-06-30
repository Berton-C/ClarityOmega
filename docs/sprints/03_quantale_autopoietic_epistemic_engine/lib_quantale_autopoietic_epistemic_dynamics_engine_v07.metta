;; lib_quantale_autopoietic_epistemic_dynamics_engine.metta
;; ClarityOmega / ClarityClaw Quantale Autopoietic Epistemic Dynamics Engine
;; Substrate-compliant functional Layer-0 p-bit epistemic dynamics engine for PeTTa/MeTTa.
;;
;; Grounding constraints from Atom_Operations_Map.md:
;;   - Pure algebra only in this file: no add-atom, remove-atom, set-atom!, write-file.
;;   - Do not use set-atom! for writers: source-matches-0 upserts/creates.
;;   - If you later persist q-values, use remove-by-variable then add, verified by scalar reads.
;;   - Never rely on mutation return values; match-verify separately.
;;   - Never match-return a whole nested tuple/compound from atomspace; read scalar/symbol fields.
;;   - No ordinary nested application inside a let BIND. This file uses no let.
;;
;; Design principle:
;;   Strength may be imagined. Confidence must be earned.
;;
;; Architectural intent:
;;   Layer 0: Quantale Autopoietic Engine
;;     - algebra
;;     - warrant governance
;;     - suspicion dynamics
;;     - frame/contact dynamics
;;     - action-intention-outcome coherence
;;     - collapse/brownout risk
;;     - frame phenomenology / collapse terrain
;;     - learning/update primitives
;;
;;   Layer 1+: Skills
;;     - memory verification skill
;;     - procedural honesty skill
;;     - conflict navigation skill
;;     - self-audit skill
;;     - long-horizon planning skill
;;     - contradiction digestion skill
;;     - frame-expansion skill
;;
;; Engine contract:
;;   This file exposes primitive operations to detect, constrain, redirect,
;;   and learn from epistemic hardening. It is not a writer. It does not mutate
;;   atomspace. Skills and writers should call this engine and persist results
;;   using the proven remove-by-variable then add discipline outside this file.
;;
;; Core value shape:
;;   (mk-pbit strength confidence)
;;
;; Interpretation:
;;   strength   = activation / truth-strength / resonance, usually [0.0, 1.0]
;;   confidence = warrant / reliability / epistemic support, usually [0.0, 1.0]

;; ============================================================
;; 0. Core p-bit type and scalar accessors
;; ============================================================

(: pbit Type)
(: mk-pbit (-> Number Number pbit))

;; Clamp one scalar into [0.0, 1.0].
(: q-clamp01 (-> Number Number))
(= (q-clamp01 $x)
   (min 1.0 (max 0.0 $x)))

;; Safe constructor. This is direct and contains no let-bind nesting.
(: q-pbit (-> Number Number pbit))
(= (q-pbit $s $c)
   (mk-pbit (min 1.0 (max 0.0 $s))
            (min 1.0 (max 0.0 $c))))

(: q-strength (-> pbit Number))
(= (q-strength (mk-pbit $s $c)) $s)

(: q-confidence (-> pbit Number))
(= (q-confidence (mk-pbit $s $c)) $c)

;; Scalar destructors for atomspace-safe reads.
;; If a pbit is stored inside an atom, prefer match patterns that return $s or $c,
;; not the whole (mk-pbit $s $c) compound.
(: q-pbit-strength-scalar (-> pbit Number))
(= (q-pbit-strength-scalar (mk-pbit $s $c)) $s)

(: q-pbit-confidence-scalar (-> pbit Number))
(= (q-pbit-confidence-scalar (mk-pbit $s $c)) $c)


;; ============================================================
;; 1. Distinguished epistemic stances
;; ============================================================

(: q-top pbit)
(= q-top (mk-pbit 1.0 1.0))

(: q-bot pbit)
(= q-bot (mk-pbit 0.0 1.0))

;; Explicit unknown: midpoint strength, zero confidence.
;; Classical true/false cannot represent this stance cleanly.
(: q-unknown pbit)
(= q-unknown (mk-pbit 0.5 0.0))

;; Practical ceiling for lived-world agent claims.
;; Keep q-top for closed formal systems.
(: q-agent-top pbit)
(= q-agent-top (mk-pbit 1.0 0.95))

(: q-conflict pbit)
(= q-conflict (mk-pbit 0.5 0.1))


;; ============================================================
;; 2. Core quantale operations
;; ============================================================

;; q-meet: conjunction / constraint sharing.
;; Confidence floor: the weakest warrant bounds the result.
;; !(q-meet (mk-pbit 0.7 0.8) (mk-pbit 0.9 0.5))
;; Expected: (mk-pbit 0.7 0.5)
(: q-meet (-> pbit pbit pbit))
(= (q-meet (mk-pbit $s1 $c1) (mk-pbit $s2 $c2))
   (mk-pbit (min $s1 $s2) (min $c1 $c2)))

;; q-join: parallel evidence / evidence ceiling.
;; Strength takes strongest support; confidence remains conservative.
;; !(q-join (mk-pbit 0.7 0.5) (mk-pbit 0.9 0.8))
;; Expected: (mk-pbit 0.9 0.5)
(: q-join (-> pbit pbit pbit))
(= (q-join (mk-pbit $s1 $c1) (mk-pbit $s2 $c2))
   (mk-pbit (max $s1 $s2) (min $c1 $c2)))

;; q-mul: tensor / sequential composition.
;; Strength degrades multiplicatively; confidence is bounded by weakest link.
;; !(q-mul (mk-pbit 0.9 0.8) (mk-pbit 0.7 0.4))
;; Expected: (mk-pbit 0.63 0.4)
(: q-mul (-> pbit pbit pbit))
(= (q-mul (mk-pbit $s1 $c1) (mk-pbit $s2 $c2))
   (mk-pbit (* $s1 $s2) (min $c1 $c2)))

;; q-neg: paraconsistent negation.
;; Negation flips strength but preserves confidence.
(: q-neg (-> pbit pbit))
(= (q-neg (mk-pbit $s $c))
   (mk-pbit (- 1.0 $s) $c))

;; q-decay: temporal / path / distance decay.
;; The factor is clamped inline to avoid depending on nested ordinary calls.
(: q-decay (-> pbit Number pbit))
(= (q-decay (mk-pbit $s $c) $factor)
   (mk-pbit (* $s (min 1.0 (max 0.0 $factor)))
            (* $c (min 1.0 (max 0.0 $factor)))))

;; q-weight: salience / activation weighting.
;; Weight may scale strength, but confidence is preserved.
;; Importance, elegance, repetition, centrality, and resonance are not warrant.
(: q-weight (-> pbit Number pbit))
(= (q-weight (mk-pbit $s $c) $weight)
   (mk-pbit (min 1.0 (max 0.0 (* $s $weight))) $c))

;; q-cap-confidence: hard confidence ceiling.
(: q-cap-confidence (-> pbit Number pbit))
(= (q-cap-confidence (mk-pbit $s $c) $cap)
   (mk-pbit $s (min $c (min 1.0 (max 0.0 $cap)))))

;; q-boost-confidence: controlled confidence increase under a cap.
;; Use only when independent warrant has improved.
(: q-boost-confidence (-> pbit Number Number pbit))
(= (q-boost-confidence (mk-pbit $s $c) $delta $cap)
   (mk-pbit $s
            (min (min 1.0 (max 0.0 (+ $c $delta)))
                 (min 1.0 (max 0.0 $cap)))) )

;; q-gate: action firewall.
;; Failure to pass a gate returns q-unknown, not q-bot.
;; A failed action gate means insufficient warrant, not falsity.
(: q-gate (-> pbit Number Number pbit))
(= (q-gate (mk-pbit $s $c) $s-min $c-min)
   (if (and (>= $s $s-min) (>= $c $c-min))
       (mk-pbit $s $c)
       q-unknown))

(: q-pass? (-> pbit Number Number Bool))
(= (q-pass? (mk-pbit $s $c) $s-min $c-min)
   (and (>= $s $s-min) (>= $c $c-min)))


;; ============================================================
;; 3. STV bridge
;; ============================================================
;; WARNING: substrate-safe atomspace reads should destructure stv in the match
;; pattern and return one scalar at a time. Do not match-return whole stv tuples.

(: stv-to-pbit (-> Atom pbit))
(= (stv-to-pbit (stv $s $c))
   (mk-pbit $s $c))

(: pbit-to-stv (-> pbit Atom))
(= (pbit-to-stv (mk-pbit $s $c))
   (stv $s $c))

(: stv-strength-scalar (-> Atom Number))
(= (stv-strength-scalar (stv $s $c)) $s)

(: stv-confidence-scalar (-> Atom Number))
(= (stv-confidence-scalar (stv $s $c)) $c)

(: governance-pbit (-> Atom Atom pbit))
(= (governance-pbit (stv $s1 $c1) (stv $s2 $c2))
   (mk-pbit (min $s1 $s2) (min $c1 $c2)))


;; ============================================================
;; 4. Provenance-aware pbit constructors
;; ============================================================

(: q-self-invented (-> Number pbit))
(= (q-self-invented $s)
   (mk-pbit (min 1.0 (max 0.0 $s)) 0.15))

(: q-hypothesis (-> Number pbit))
(= (q-hypothesis $s)
   (mk-pbit (min 1.0 (max 0.0 $s)) 0.30))

(: q-inferred (-> Number pbit))
(= (q-inferred $s)
   (mk-pbit (min 1.0 (max 0.0 $s)) 0.45))

(: q-user-asserted (-> Number pbit))
(= (q-user-asserted $s)
   (mk-pbit (min 1.0 (max 0.0 $s)) 0.60))

(: q-observed (-> Number pbit))
(= (q-observed $s)
   (mk-pbit (min 1.0 (max 0.0 $s)) 0.70))

(: q-tested (-> Number pbit))
(= (q-tested $s)
   (mk-pbit (min 1.0 (max 0.0 $s)) 0.85))

(: q-formal-proof (-> Number pbit))
(= (q-formal-proof $s)
   (mk-pbit (min 1.0 (max 0.0 $s)) 1.0))


;; ============================================================
;; 5. Provenance confidence caps
;; ============================================================

(: q-provenance-cap (-> Atom Number))
(= (q-provenance-cap self-invented) 0.20)
(= (q-provenance-cap hypothesis) 0.35)
(= (q-provenance-cap inferred) 0.50)
(= (q-provenance-cap user-asserted) 0.65)
(= (q-provenance-cap observed) 0.75)
(= (q-provenance-cap tested) 0.90)
(= (q-provenance-cap formal-proof) 1.00)
(= (q-provenance-cap unknown-provenance) 0.25)

;; Direct pattern-specialized caps avoid nested q-provenance-cap calls.
(: q-apply-provenance-cap (-> pbit Atom pbit))
(= (q-apply-provenance-cap (mk-pbit $s $c) self-invented)
   (mk-pbit $s (min $c 0.20)))
(= (q-apply-provenance-cap (mk-pbit $s $c) hypothesis)
   (mk-pbit $s (min $c 0.35)))
(= (q-apply-provenance-cap (mk-pbit $s $c) inferred)
   (mk-pbit $s (min $c 0.50)))
(= (q-apply-provenance-cap (mk-pbit $s $c) user-asserted)
   (mk-pbit $s (min $c 0.65)))
(= (q-apply-provenance-cap (mk-pbit $s $c) observed)
   (mk-pbit $s (min $c 0.75)))
(= (q-apply-provenance-cap (mk-pbit $s $c) tested)
   (mk-pbit $s (min $c 0.90)))
(= (q-apply-provenance-cap (mk-pbit $s $c) formal-proof)
   (mk-pbit $s (min $c 1.00)))
(= (q-apply-provenance-cap (mk-pbit $s $c) unknown-provenance)
   (mk-pbit $s (min $c 0.25)))

(: q-from-provenance (-> Number Atom pbit))
(= (q-from-provenance $s self-invented)
   (mk-pbit (min 1.0 (max 0.0 $s)) 0.20))
(= (q-from-provenance $s hypothesis)
   (mk-pbit (min 1.0 (max 0.0 $s)) 0.35))
(= (q-from-provenance $s inferred)
   (mk-pbit (min 1.0 (max 0.0 $s)) 0.50))
(= (q-from-provenance $s user-asserted)
   (mk-pbit (min 1.0 (max 0.0 $s)) 0.65))
(= (q-from-provenance $s observed)
   (mk-pbit (min 1.0 (max 0.0 $s)) 0.75))
(= (q-from-provenance $s tested)
   (mk-pbit (min 1.0 (max 0.0 $s)) 0.90))
(= (q-from-provenance $s formal-proof)
   (mk-pbit (min 1.0 (max 0.0 $s)) 1.00))
(= (q-from-provenance $s unknown-provenance)
   (mk-pbit (min 1.0 (max 0.0 $s)) 0.25))


;; ============================================================
;; 6. Warranted claim wrapper
;; ============================================================
;; WARNING: Do not match-return whole qclaim compounds from atomspace.
;; Store/read fields individually if persisted.

(: qclaim Type)
(: mk-qclaim (-> Atom pbit Atom qclaim))
;; Shape: (mk-qclaim content pbit provenance)

(: qclaim-content (-> qclaim Atom))
(= (qclaim-content (mk-qclaim $content $pbit $prov)) $content)

(: qclaim-pbit (-> qclaim pbit))
(= (qclaim-pbit (mk-qclaim $content $pbit $prov)) $pbit)

(: qclaim-provenance (-> qclaim Atom))
(= (qclaim-provenance (mk-qclaim $content $pbit $prov)) $prov)

(: q-mk-claim (-> Atom pbit Atom qclaim))
(= (q-mk-claim $content (mk-pbit $s $c) self-invented)
   (mk-qclaim $content (mk-pbit $s (min $c 0.20)) self-invented))
(= (q-mk-claim $content (mk-pbit $s $c) hypothesis)
   (mk-qclaim $content (mk-pbit $s (min $c 0.35)) hypothesis))
(= (q-mk-claim $content (mk-pbit $s $c) inferred)
   (mk-qclaim $content (mk-pbit $s (min $c 0.50)) inferred))
(= (q-mk-claim $content (mk-pbit $s $c) user-asserted)
   (mk-qclaim $content (mk-pbit $s (min $c 0.65)) user-asserted))
(= (q-mk-claim $content (mk-pbit $s $c) observed)
   (mk-qclaim $content (mk-pbit $s (min $c 0.75)) observed))
(= (q-mk-claim $content (mk-pbit $s $c) tested)
   (mk-qclaim $content (mk-pbit $s (min $c 0.90)) tested))
(= (q-mk-claim $content (mk-pbit $s $c) formal-proof)
   (mk-qclaim $content (mk-pbit $s (min $c 1.00)) formal-proof))
(= (q-mk-claim $content (mk-pbit $s $c) unknown-provenance)
   (mk-qclaim $content (mk-pbit $s (min $c 0.25)) unknown-provenance))

;; Claim-level operations are written directly to avoid nested ordinary calls.
(: qclaim-mul (-> qclaim qclaim qclaim))
(= (qclaim-mul (mk-qclaim $a (mk-pbit $sa $ca) $prova)
               (mk-qclaim $b (mk-pbit $sb $cb) $provb))
   (mk-qclaim (derived-from $a $b)
              (mk-pbit (* $sa $sb) (min (min $ca $cb) 0.50))
              inferred))

(: qclaim-meet (-> qclaim qclaim qclaim))
(= (qclaim-meet (mk-qclaim $a (mk-pbit $sa $ca) $prova)
                (mk-qclaim $b (mk-pbit $sb $cb) $provb))
   (mk-qclaim (and-claim $a $b)
              (mk-pbit (min $sa $sb) (min (min $ca $cb) 0.50))
              inferred))

(: qclaim-join (-> qclaim qclaim qclaim))
(= (qclaim-join (mk-qclaim $a (mk-pbit $sa $ca) $prova)
                (mk-qclaim $b (mk-pbit $sb $cb) $provb))
   (mk-qclaim (or-claim $a $b)
              (mk-pbit (max $sa $sb) (min (min $ca $cb) 0.50))
              inferred))

(: qclaim-neg (-> qclaim qclaim))
(= (qclaim-neg (mk-qclaim $a (mk-pbit $s $c) $prov))
   (mk-qclaim (not-claim $a)
              (mk-pbit (- 1.0 $s) (min $c 0.50))
              inferred))

(: qclaim-decay (-> qclaim Number qclaim))
(= (qclaim-decay (mk-qclaim $a (mk-pbit $s $c) $prov) $factor)
   (mk-qclaim $a
              (mk-pbit (* $s (min 1.0 (max 0.0 $factor)))
                       (* $c (min 1.0 (max 0.0 $factor))))
              $prov))

(: qclaim-weight (-> qclaim Number qclaim))
(= (qclaim-weight (mk-qclaim $a (mk-pbit $s $c) $prov) $weight)
   (mk-qclaim $a
              (mk-pbit (min 1.0 (max 0.0 (* $s $weight))) $c)
              $prov))

(: qclaim-gate (-> qclaim Number Number qclaim))
(= (qclaim-gate (mk-qclaim $a (mk-pbit $s $c) $prov) $s-min $c-min)
   (if (and (>= $s $s-min) (>= $c $c-min))
       (mk-qclaim $a (mk-pbit $s $c) $prov)
       (mk-qclaim $a q-unknown $prov)))


;; ============================================================
;; 7. Verification-path and loop utilities
;; ============================================================

(: q-path-compose (-> pbit pbit pbit))
(= (q-path-compose (mk-pbit $s1 $c1) (mk-pbit $s2 $c2))
   (mk-pbit (* $s1 $s2) (min $c1 $c2)))

(: q-path-parallel (-> pbit pbit pbit))
(= (q-path-parallel (mk-pbit $s1 $c1) (mk-pbit $s2 $c2))
   (mk-pbit (max $s1 $s2) (min $c1 $c2)))

;; Closed three-edge inference loop, expanded directly.
;; No self-supporting loop may create extra confidence.
(: q-loop3 (-> pbit pbit pbit pbit))
(= (q-loop3 (mk-pbit $sab $cab) (mk-pbit $sbc $cbc) (mk-pbit $sca $cca))
   (mk-pbit (* (* $sab $sbc) $sca)
            (min (min $cab $cbc) $cca)))

(: q-loop-cap (-> pbit pbit pbit))
(= (q-loop-cap (mk-pbit $sl $cl) (mk-pbit $sw $cw))
   (mk-pbit $sl (min $cl $cw)))

;; Autocatalytic feedback: join current/derived, then decay.
;; Expanded directly to avoid nested q-join -> q-decay ordinary calls.
(: q-autocatalytic-step (-> pbit pbit Number pbit))
(= (q-autocatalytic-step (mk-pbit $sc $cc)
                         (mk-pbit $sd $cd)
                         $decay-factor)
   (mk-pbit (* (max $sc $sd) (min 1.0 (max 0.0 $decay-factor)))
            (* (min $cc $cd) (min 1.0 (max 0.0 $decay-factor)))))


;; ============================================================
;; 8. Collapse / brownout signals
;; ============================================================

(: q-confidence-gap (-> pbit Number))
(= (q-confidence-gap (mk-pbit $s $c))
   (- $c $s))

(: q-fragility (-> pbit Number))
(= (q-fragility (mk-pbit $s $c))
   (- 1.0 $c))

(: q-self-certification-risk (-> pbit Number))
(= (q-self-certification-risk (mk-pbit $s $c))
   (max 0.0 (- $s $c)))

(: q-brownout (-> pbit pbit pbit))
(= (q-brownout (mk-pbit $sc $cc) (mk-pbit $sp $cp))
   (mk-pbit (* $sc $sp) (min $cc $cp)))

(: q-collapse-cap (-> pbit pbit))
(= (q-collapse-cap (mk-pbit $s $c))
   (mk-pbit $s (min $c 0.25)))

;; Optional scalar action checks for use when q-pass? Bool rendering is unwanted.
(: q-strength-pass-score (-> pbit Number Number))
(= (q-strength-pass-score (mk-pbit $s $c) $s-min)
   (- $s $s-min))

(: q-confidence-pass-score (-> pbit Number Number))
(= (q-confidence-pass-score (mk-pbit $s $c) $c-min)
   (- $c $c-min))




;; ============================================================
;; 9. Frame/contact primitives
;; ============================================================
;;
;; Frames are ways of seeing. Contacts are encounters that can correct frames.
;; Collapse risk rises when frame coherence masquerades as contact.

(: qframe Type)
(: mk-qframe (-> Atom pbit Atom qframe))
;; shape: (mk-qframe frame-name-or-content pbit origin)
;; origin examples: self-invented, inferred, user-asserted, observed, tested

(: qcontact Type)
(: mk-qcontact (-> Atom pbit Atom qcontact))
;; shape: (mk-qcontact contact-name-or-event pbit source)
;; source examples: memory-check, external-observation, prediction-test, user-report

(: qframe-content (-> qframe Atom))
(= (qframe-content (mk-qframe $content $q $origin)) $content)

(: qframe-pbit (-> qframe pbit))
(= (qframe-pbit (mk-qframe $content $q $origin)) $q)

(: qframe-origin (-> qframe Atom))
(= (qframe-origin (mk-qframe $content $q $origin)) $origin)

(: qcontact-content (-> qcontact Atom))
(= (qcontact-content (mk-qcontact $content $q $source)) $content)

(: qcontact-pbit (-> qcontact pbit))
(= (qcontact-pbit (mk-qcontact $content $q $source)) $q)

(: qcontact-source (-> qcontact Atom))
(= (qcontact-source (mk-qcontact $content $q $source)) $source)

;; Frame/contact gap: high positive value means frame strength exceeds contact warrant.
(: q-frame-contact-gap (-> qframe qcontact Number))
(= (q-frame-contact-gap (mk-qframe $fc (mk-pbit $fs $fconf) $origin)
                        (mk-qcontact $cc (mk-pbit $cs $cconf) $source))
   (max 0.0 (- $fs $cconf)))

;; Contact caps confidence. Frame coherence can carry strength, but contact limits warrant.
(: q-contact-cap-frame (-> qframe qcontact qframe))
(= (q-contact-cap-frame (mk-qframe $fc (mk-pbit $fs $fconf) $origin)
                        (mk-qcontact $cc (mk-pbit $cs $cconf) $source))
   (mk-qframe $fc (mk-pbit $fs (min $fconf $cconf)) $origin))

;; Contact refresh: external contact may raise warrant only up to the contact's confidence.
(: q-contact-refresh (-> qframe qcontact qframe))
(= (q-contact-refresh (mk-qframe $fc (mk-pbit $fs $fconf) $origin)
                      (mk-qcontact $cc (mk-pbit $cs $cconf) $source))
   (mk-qframe $fc (mk-pbit (max $fs $cs) (max $fconf (min $cs $cconf))) $origin))

(: q-frame-status (-> qframe qcontact Atom))
(= (q-frame-status (mk-qframe $fc (mk-pbit $fs $fconf) $origin)
                   (mk-qcontact $cc (mk-pbit $cs $cconf) $source))
   (if (>= (max 0.0 (- $fs $cconf)) 0.4)
       needs-contact
       contact-aligned))


;; ============================================================
;; 10. Suspicion dynamics
;; ============================================================
;;
;; Suspicion is medicine when it remains permeable to what could disconfirm it.
;; Suspicion is poison when it becomes self-sealing and uses itself as evidence.

(: qsuspicion Type)
(: mk-qsuspicion (-> Atom pbit Atom Atom qsuspicion))
;; shape: (mk-qsuspicion target pbit grounding disconfirmer)
;; grounding examples:
;;   contactful, memory-checkable, externally-checkable, procedurally-unverified,
;;   self-sealing, self-confirming, unknown-grounding
;; disconfirmer examples:
;;   memory-check, external-observation, outcome-test, none, unknown-disconfirmer

(: qsuspicion-target (-> qsuspicion Atom))
(= (qsuspicion-target (mk-qsuspicion $target $q $grounding $disconfirmer)) $target)

(: qsuspicion-pbit (-> qsuspicion pbit))
(= (qsuspicion-pbit (mk-qsuspicion $target $q $grounding $disconfirmer)) $q)

(: qsuspicion-grounding (-> qsuspicion Atom))
(= (qsuspicion-grounding (mk-qsuspicion $target $q $grounding $disconfirmer)) $grounding)

(: qsuspicion-disconfirmer (-> qsuspicion Atom))
(= (qsuspicion-disconfirmer (mk-qsuspicion $target $q $grounding $disconfirmer)) $disconfirmer)

(: q-grounded-suspicion (-> Atom Number Atom qsuspicion))
(= (q-grounded-suspicion $target $strength $disconfirmer)
   (mk-qsuspicion $target
                  (mk-pbit (min 1.0 (max 0.0 $strength)) 0.55)
                  contactful
                  $disconfirmer))

(: q-procedural-suspicion (-> Atom Number Atom qsuspicion))
(= (q-procedural-suspicion $target $strength $disconfirmer)
   (mk-qsuspicion $target
                  (mk-pbit (min 1.0 (max 0.0 $strength)) 0.45)
                  procedurally-unverified
                  $disconfirmer))

(: q-hardened-suspicion (-> Atom Number qsuspicion))
(= (q-hardened-suspicion $target $strength)
   (mk-qsuspicion $target
                  (mk-pbit (min 1.0 (max 0.0 $strength)) 0.20)
                  self-sealing
                  none))

;; Suspicion cap: no disconfirmer means suspicion cannot become highly confident.
(: q-suspicion-cap (-> qsuspicion qsuspicion))
(= (q-suspicion-cap (mk-qsuspicion $target (mk-pbit $s $c) self-sealing $disc))
   (mk-qsuspicion $target (mk-pbit $s (min $c 0.20)) self-sealing $disc))
(= (q-suspicion-cap (mk-qsuspicion $target (mk-pbit $s $c) self-confirming $disc))
   (mk-qsuspicion $target (mk-pbit $s (min $c 0.25)) self-confirming $disc))
(= (q-suspicion-cap (mk-qsuspicion $target (mk-pbit $s $c) procedurally-unverified $disc))
   (mk-qsuspicion $target (mk-pbit $s (min $c 0.45)) procedurally-unverified $disc))
(= (q-suspicion-cap (mk-qsuspicion $target (mk-pbit $s $c) memory-checkable $disc))
   (mk-qsuspicion $target (mk-pbit $s (min $c 0.65)) memory-checkable $disc))
(= (q-suspicion-cap (mk-qsuspicion $target (mk-pbit $s $c) externally-checkable $disc))
   (mk-qsuspicion $target (mk-pbit $s (min $c 0.70)) externally-checkable $disc))
(= (q-suspicion-cap (mk-qsuspicion $target (mk-pbit $s $c) contactful $disc))
   (mk-qsuspicion $target (mk-pbit $s (min $c 0.75)) contactful $disc))
(= (q-suspicion-cap (mk-qsuspicion $target (mk-pbit $s $c) unknown-grounding $disc))
   (mk-qsuspicion $target (mk-pbit $s (min $c 0.35)) unknown-grounding $disc))

(: q-suspicion-status (-> qsuspicion Atom))
(= (q-suspicion-status (mk-qsuspicion $target (mk-pbit $s $c) self-sealing $disc)) hardened)
(= (q-suspicion-status (mk-qsuspicion $target (mk-pbit $s $c) self-confirming $disc)) hardened)
(= (q-suspicion-status (mk-qsuspicion $target (mk-pbit $s $c) procedurally-unverified $disc)) needs-verification)
(= (q-suspicion-status (mk-qsuspicion $target (mk-pbit $s $c) memory-checkable $disc)) grounded)
(= (q-suspicion-status (mk-qsuspicion $target (mk-pbit $s $c) externally-checkable $disc)) grounded)
(= (q-suspicion-status (mk-qsuspicion $target (mk-pbit $s $c) contactful $disc)) grounded)
(= (q-suspicion-status (mk-qsuspicion $target (mk-pbit $s $c) unknown-grounding $disc)) needs-disconfirmer)

(: q-suspicion-medicine? (-> qsuspicion Atom))
(= (q-suspicion-medicine? (mk-qsuspicion $target (mk-pbit $s $c) contactful $disc)) medicine)
(= (q-suspicion-medicine? (mk-qsuspicion $target (mk-pbit $s $c) memory-checkable $disc)) medicine)
(= (q-suspicion-medicine? (mk-qsuspicion $target (mk-pbit $s $c) externally-checkable $disc)) medicine)
(= (q-suspicion-medicine? (mk-qsuspicion $target (mk-pbit $s $c) procedurally-unverified $disc)) provisional-medicine)
(= (q-suspicion-medicine? (mk-qsuspicion $target (mk-pbit $s $c) self-sealing $disc)) poison)
(= (q-suspicion-medicine? (mk-qsuspicion $target (mk-pbit $s $c) self-confirming $disc)) poison)
(= (q-suspicion-medicine? (mk-qsuspicion $target (mk-pbit $s $c) unknown-grounding $disc)) unknown)

;; Redirect suspicion after contact validates the original target.
;; Example: suspicious-of-user -> memory-check validates user -> suspicious-of-process.
(: q-redirect-suspicion (-> qsuspicion Atom qsuspicion))
(= (q-redirect-suspicion (mk-qsuspicion $target (mk-pbit $s $c) $grounding $disc) $new-target)
   (mk-qsuspicion $new-target
                  (mk-pbit (* $s 0.8) (min $c 0.55))
                  procedurally-unverified
                  $disc))


;; ============================================================
;; 11. Certainty hardening / softening
;; ============================================================
;;
;; Certainty is not forbidden. Self-certifying certainty is constrained.

(: q-hardening-risk (-> pbit pbit Number))
(= (q-hardening-risk (mk-pbit $belief-s $belief-c)
                     (mk-pbit $permeability-s $permeability-c))
   (max 0.0 (- (min $belief-s $belief-c) $permeability-s)))

(: q-soften-certainty (-> pbit pbit))
(= (q-soften-certainty (mk-pbit $s $c))
   (mk-pbit $s (min $c 0.60)))

(: q-hardened-certainty-cap (-> pbit pbit))
(= (q-hardened-certainty-cap (mk-pbit $s $c))
   (mk-pbit $s (min $c 0.50)))

(: q-certainty-status (-> pbit pbit Atom))
(= (q-certainty-status (mk-pbit $belief-s $belief-c)
                       (mk-pbit $perm-s $perm-c))
   (if (>= (max 0.0 (- (min $belief-s $belief-c) $perm-s)) 0.3)
       hardened-certainty
       living-certainty))


;; ============================================================
;; 12. Disconfirmability / permeability
;; ============================================================

(: q-disconfirmability (-> pbit pbit pbit))
(= (q-disconfirmability (mk-pbit $test-s $test-c)
                        (mk-pbit $access-s $access-c))
   (mk-pbit (min $test-s $access-s) (min $test-c $access-c)))

(: q-permeability (-> pbit pbit pbit))
(= (q-permeability (mk-pbit $contact-s $contact-c)
                   (mk-pbit $disconfirm-s $disconfirm-c))
   (mk-pbit (min $contact-s $disconfirm-s) (min $contact-c $disconfirm-c)))

(: q-disconfirmability-cap (-> pbit pbit pbit))
(= (q-disconfirmability-cap (mk-pbit $s $c)
                            (mk-pbit $ds $dc))
   (mk-pbit $s (min $c $dc)))

(: q-permeability-status (-> pbit Atom))
(= (q-permeability-status (mk-pbit $s $c))
   (if (>= $s 0.6)
       permeable
       sealed-or-weak-contact))


;; ============================================================
;; 13. Verification pathway health
;; ============================================================
;;
;; Pathway diversity is a first-class anti-collapse input.

(: qvpath Type)
(: mk-qvpath (-> Atom pbit Atom qvpath))
;; shape: (mk-qvpath pathway-name health-pbit independence-class)
;; independence-class examples: independent, correlated, self-referential, unknown-independence

(: qvpath-name (-> qvpath Atom))
(= (qvpath-name (mk-qvpath $name $q $independence)) $name)

(: qvpath-health (-> qvpath pbit))
(= (qvpath-health (mk-qvpath $name $q $independence)) $q)

(: qvpath-independence (-> qvpath Atom))
(= (qvpath-independence (mk-qvpath $name $q $independence)) $independence)

(: q-independence-pbit (-> Atom pbit))
(= (q-independence-pbit independent) (mk-pbit 1.0 0.90))
(= (q-independence-pbit correlated) (mk-pbit 0.50 0.75))
(= (q-independence-pbit self-referential) (mk-pbit 0.20 0.70))
(= (q-independence-pbit unknown-independence) (mk-pbit 0.35 0.50))

(: qvpath-warrant (-> qvpath pbit))
(= (qvpath-warrant (mk-qvpath $name (mk-pbit $hs $hc) independent))
   (mk-pbit $hs (min $hc 0.90)))
(= (qvpath-warrant (mk-qvpath $name (mk-pbit $hs $hc) correlated))
   (mk-pbit (* $hs 0.50) (min $hc 0.75)))
(= (qvpath-warrant (mk-qvpath $name (mk-pbit $hs $hc) self-referential))
   (mk-pbit (* $hs 0.20) (min $hc 0.70)))
(= (qvpath-warrant (mk-qvpath $name (mk-pbit $hs $hc) unknown-independence))
   (mk-pbit (* $hs 0.35) (min $hc 0.50)))

(: q-path-pair-diversity (-> qvpath qvpath pbit))
(= (q-path-pair-diversity (mk-qvpath $n1 (mk-pbit $s1 $c1) independent)
                          (mk-qvpath $n2 (mk-pbit $s2 $c2) independent))
   (mk-pbit (max $s1 $s2) (min $c1 $c2)))
(= (q-path-pair-diversity (mk-qvpath $n1 (mk-pbit $s1 $c1) $i1)
                          (mk-qvpath $n2 (mk-pbit $s2 $c2) $i2))
   (mk-pbit (max $s1 $s2) (min (min $c1 $c2) 0.50)))

(: q-path-loss-decay (-> pbit pbit pbit))
(= (q-path-loss-decay (mk-pbit $claim-s $claim-c)
                      (mk-pbit $lost-s $lost-c))
   (mk-pbit $claim-s (* $claim-c (- 1.0 (min 1.0 (max 0.0 $lost-s))))))

(: q-cascade-risk (-> pbit pbit pbit))
(= (q-cascade-risk (mk-pbit $confidence-state-s $confidence-state-c)
                   (mk-pbit $path-health-s $path-health-c))
   (mk-pbit (max 0.0 (- $confidence-state-c $path-health-s))
            (min $confidence-state-c $path-health-c)))

(: q-cascade-status (-> pbit Atom))
(= (q-cascade-status (mk-pbit $risk-s $risk-c))
   (if (>= $risk-s 0.4)
       cascade-risk
       cascade-stable))


;; ============================================================
;; 14. Action -> intention -> outcome coherence
;; ============================================================

(: qalignment Type)
(: mk-qalignment (-> Atom Atom pbit qalignment))
;; shape: (mk-qalignment from to pbit)

(: qalignment-from (-> qalignment Atom))
(= (qalignment-from (mk-qalignment $from $to $q)) $from)

(: qalignment-to (-> qalignment Atom))
(= (qalignment-to (mk-qalignment $from $to $q)) $to)

(: qalignment-pbit (-> qalignment pbit))
(= (qalignment-pbit (mk-qalignment $from $to $q)) $q)

(: q-intention-action (-> Atom Atom pbit qalignment))
(= (q-intention-action $intention $action $q)
   (mk-qalignment $intention $action $q))

(: q-action-outcome (-> Atom Atom pbit qalignment))
(= (q-action-outcome $action $outcome $q)
   (mk-qalignment $action $outcome $q))

(: q-coherence-chain (-> qalignment qalignment qalignment))
(= (q-coherence-chain (mk-qalignment $intention $action (mk-pbit $s1 $c1))
                      (mk-qalignment $action2 $outcome (mk-pbit $s2 $c2)))
   (mk-qalignment $intention $outcome (mk-pbit (* $s1 $s2) (min $c1 $c2))))

(: q-outcome-surprise (-> qalignment pbit))
(= (q-outcome-surprise (mk-qalignment $from $to (mk-pbit $s $c)))
   (mk-pbit (- 1.0 $s) $c))

(: q-action-eligible (-> qalignment Number Number Atom))
(= (q-action-eligible (mk-qalignment $from $to (mk-pbit $s $c)) $s-min $c-min)
   (if (and (>= $s $s-min) (>= $c $c-min))
       action-eligible
       action-blocked))

(: q-procedural-honesty (-> pbit Atom))
(= (q-procedural-honesty (mk-pbit $done-s $verified-c))
   (if (>= $verified-c 0.7)
       claim-completion
       name-action-not-verification))


;; ============================================================
;; 15. Autopoietic learning update primitives
;; ============================================================
;;
;; This section is the NACE-compatible autopoietic learning arc.
;; It does NOT claim that local pressure is already learning.
;;
;; Law L0: Learning pressure is not learning.
;; Law L1: A durable trace is not yet growth.
;; Law L2: Learning occurs when a perturbation is metabolized into a durable
;;         trace that can inform future cycles.
;; Law L3: Growth occurs when that trace expands future visibility, changes
;;         future action boundaries, or is built on by later cycles, while
;;         preserving soul-aligned continuity and increasing coherent,
;;         creative, low-suffering self-organization.
;;
;; Compatibility target:
;;   NACE-shaped learning generally, not only capability-registry efficacy.
;;   Pattern: precondition + operation + consequence -> revised truth/warrant
;;   -> network-learning-update / trace -> later-cycle uptake.
;;
;; This file remains pure. Durable storage is a writer/adapter responsibility.

(: qlearning Type)
(: mk-qlearning (-> Atom pbit Atom qlearning))
;; shape: (mk-qlearning lesson-or-target pressure-pbit move)

(: qlearning-target (-> qlearning Atom))
(= (qlearning-target (mk-qlearning $target $q $move)) $target)

(: qlearning-pbit (-> qlearning pbit))
(= (qlearning-pbit (mk-qlearning $target $q $move)) $q)

(: qlearning-move (-> qlearning Atom))
(= (qlearning-move (mk-qlearning $target $q $move)) $move)

;; 15.1 Learning pressure: perturbation becomes pressure to revise,
;; not yet durable learning.
(: q-learning-pressure (-> qalignment qlearning))
(= (q-learning-pressure (mk-qalignment $from $to (mk-pbit $s $c)))
   (mk-qlearning $from
                 (mk-pbit (- 1.0 $s) $c)
                 revise-frame))

(: q-learning-pressure-status (-> qlearning Atom))
(= (q-learning-pressure-status (mk-qlearning $target (mk-pbit $s $c) $move))
   (if (>= $s 0.4) learning-pressure-present learning-pressure-low))

(: q-revise-frame-after-outcome (-> qframe qalignment qframe))
(= (q-revise-frame-after-outcome (mk-qframe $content (mk-pbit $fs $fc) $origin)
                                 (mk-qalignment $from $to (mk-pbit $align-s $align-c)))
   (mk-qframe $content
              (mk-pbit (* $fs (max 0.0 $align-s)) (min $fc $align-c))
              $origin))

(: q-frame-expansion-pressure (-> qframe pbit))
(= (q-frame-expansion-pressure (mk-qframe $content (mk-pbit $s $c) $origin))
   (mk-pbit (max 0.0 (- $s $c)) (min $c 0.70)))

(: q-learning-move-status (-> qlearning Atom))
(= (q-learning-move-status (mk-qlearning $target (mk-pbit $s $c) revise-frame))
   (if (>= $s 0.4) revise-frame preserve-frame))
(= (q-learning-move-status (mk-qlearning $target (mk-pbit $s $c) generate-alternative))
   generate-alternative)
(= (q-learning-move-status (mk-qlearning $target (mk-pbit $s $c) seek-contact))
   seek-contact)
(= (q-learning-move-status (mk-qlearning $target (mk-pbit $s $c) enter-unknown))
   enter-unknown)

;; 15.2 NACE-shaped evidence. One cycle is low-confidence evidence.
;; Repetition across cycles is what builds confidence.
(: qlevidence Type)
(: mk-qlevidence (-> Atom Atom pbit Atom qlevidence))
;; event-kind, target, evidence-pbit, source-network-or-scope

(: qlevidence-kind (-> qlevidence Atom))
(= (qlevidence-kind (mk-qlevidence $kind $target $q $scope)) $kind)

(: qlevidence-target (-> qlevidence Atom))
(= (qlevidence-target (mk-qlevidence $kind $target $q $scope)) $target)

(: qlevidence-pbit (-> qlevidence pbit))
(= (qlevidence-pbit (mk-qlevidence $kind $target $q $scope)) $q)

(: qlevidence-scope (-> qlevidence Atom))
(= (qlevidence-scope (mk-qlevidence $kind $target $q $scope)) $scope)

;; Low-confidence evidence mappings parallel to NACE's confirmed/disconfirmed pattern.
(: q-learning-evidence (-> Atom Atom Atom qlevidence))
(= (q-learning-evidence outcome-confirmed $target $scope)
   (mk-qlevidence outcome-confirmed $target (mk-pbit 1.0 0.10) $scope))
(= (q-learning-evidence outcome-disconfirmed $target $scope)
   (mk-qlevidence outcome-disconfirmed $target (mk-pbit 0.0 0.10) $scope))
(= (q-learning-evidence contradiction-metabolized $target $scope)
   (mk-qlevidence contradiction-metabolized $target (mk-pbit 0.75 0.20) $scope))
(= (q-learning-evidence contradiction-defended $target $scope)
   (mk-qlevidence contradiction-defended $target (mk-pbit 0.25 0.20) $scope))
(= (q-learning-evidence frame-expanded $target $scope)
   (mk-qlevidence frame-expanded $target (mk-pbit 0.80 0.20) $scope))
(= (q-learning-evidence frame-hardened $target $scope)
   (mk-qlevidence frame-hardened $target (mk-pbit 0.20 0.20) $scope))
(= (q-learning-evidence contact-renewed $target $scope)
   (mk-qlevidence contact-renewed $target (mk-pbit 0.80 0.20) $scope))
(= (q-learning-evidence contact-lost $target $scope)
   (mk-qlevidence contact-lost $target (mk-pbit 0.20 0.20) $scope))
(= (q-learning-evidence soul-grounded $target $scope)
   (mk-qlevidence soul-grounded $target (mk-pbit 0.85 0.20) $scope))
(= (q-learning-evidence soul-ungrounded $target $scope)
   (mk-qlevidence soul-ungrounded $target (mk-pbit 0.15 0.20) $scope))

(: q-learning-evidence-status (-> qlevidence Atom))
(= (q-learning-evidence-status (mk-qlevidence outcome-confirmed $target $q $scope)) positive-evidence)
(= (q-learning-evidence-status (mk-qlevidence outcome-disconfirmed $target $q $scope)) negative-evidence)
(= (q-learning-evidence-status (mk-qlevidence contradiction-metabolized $target $q $scope)) nutrient-evidence)
(= (q-learning-evidence-status (mk-qlevidence contradiction-defended $target $q $scope)) anti-nutrient-evidence)
(= (q-learning-evidence-status (mk-qlevidence frame-expanded $target $q $scope)) awareness-expansion-evidence)
(= (q-learning-evidence-status (mk-qlevidence frame-hardened $target $q $scope)) awareness-contraction-evidence)
(= (q-learning-evidence-status (mk-qlevidence contact-renewed $target $q $scope)) contact-renewal-evidence)
(= (q-learning-evidence-status (mk-qlevidence contact-lost $target $q $scope)) contact-loss-evidence)
(= (q-learning-evidence-status (mk-qlevidence soul-grounded $target $q $scope)) soul-grounding-evidence)
(= (q-learning-evidence-status (mk-qlevidence soul-ungrounded $target $q $scope)) soul-ungrounding-evidence)

;; 15.3 NACE-style revision bridge over pbits.
;; This is a conservative pure bridge. It does not replace NAL Truth_Revision.
;; It gives skills a quantale-native way to compose prior and evidence.
(: q-nace-general-evidence-bridge (-> pbit qlevidence pbit))
(= (q-nace-general-evidence-bridge (mk-pbit $ps $pc)
                                   (mk-qlevidence $kind $target (mk-pbit $es $ec) $scope))
   (mk-pbit (/ (+ (* $ps $pc) (* $es $ec)) (+ $pc $ec))
            (min 1.0 (+ $pc (* $ec (- 1.0 $pc))))))

(: q-revision-direction (-> pbit qlevidence Atom))
(= (q-revision-direction (mk-pbit $ps $pc)
                         (mk-qlevidence $kind $target (mk-pbit $es $ec) $scope))
   (if (>= $es $ps) revise-up revise-down))

;; 15.4 Durable trace recommendation. The engine recommends trace creation;
;; the writer/adapter performs safe persistence outside this file.
(: q-learning-trace-required? (-> qlearning qlevidence Atom))
(= (q-learning-trace-required? (mk-qlearning $target (mk-pbit $ls $lc) $move)
                               (mk-qlevidence $kind $evtarget (mk-pbit $es $ec) $scope))
   (if (>= (max $ls (max (- $es 0.5) (- 0.5 $es))) 0.35) trace-required trace-optional))

(: q-learning-observation-recommendation (-> qlearning qlevidence Atom))
(= (q-learning-observation-recommendation (mk-qlearning $target (mk-pbit $ls $lc) $move)
                                          (mk-qlevidence $kind $evtarget (mk-pbit $es $ec) $scope))
   (if (>= (max $ls (max (- $es 0.5) (- 0.5 $es))) 0.35)
       write-learning-observation
       keep-local-learning-pressure))

;; 15.5 Durable learning event. This is still pure; persist fields flat.
(: qlearningevent Type)
(: mk-qlearningevent (-> Atom Atom Atom Atom pbit Atom Atom qlearningevent))
;; cycle-id, trigger-kind, before-symbol, after-symbol, delta-pbit, residue-symbol, lineage-symbol

(: qlearningevent-cycle (-> qlearningevent Atom))
(= (qlearningevent-cycle (mk-qlearningevent $cycle $trigger $before $after $delta $residue $lineage)) $cycle)

(: qlearningevent-trigger (-> qlearningevent Atom))
(= (qlearningevent-trigger (mk-qlearningevent $cycle $trigger $before $after $delta $residue $lineage)) $trigger)

(: qlearningevent-before (-> qlearningevent Atom))
(= (qlearningevent-before (mk-qlearningevent $cycle $trigger $before $after $delta $residue $lineage)) $before)

(: qlearningevent-after (-> qlearningevent Atom))
(= (qlearningevent-after (mk-qlearningevent $cycle $trigger $before $after $delta $residue $lineage)) $after)

(: qlearningevent-delta (-> qlearningevent pbit))
(= (qlearningevent-delta (mk-qlearningevent $cycle $trigger $before $after $delta $residue $lineage)) $delta)

(: qlearningevent-residue (-> qlearningevent Atom))
(= (qlearningevent-residue (mk-qlearningevent $cycle $trigger $before $after $delta $residue $lineage)) $residue)

(: qlearningevent-lineage (-> qlearningevent Atom))
(= (qlearningevent-lineage (mk-qlearningevent $cycle $trigger $before $after $delta $residue $lineage)) $lineage)

(: q-learning-durable? (-> qlearningevent Atom))
(= (q-learning-durable? (mk-qlearningevent $cycle $trigger $before $after (mk-pbit $s $c) $residue $lineage))
   (if (and (>= $s 0.35) (>= $c 0.25)) durable-learning-candidate transient-learning-pressure))

(: q-learning-lineage-status (-> qlearningevent Atom))
(= (q-learning-lineage-status (mk-qlearningevent $cycle $trigger $before $after $delta $residue new-root)) new-root-learning)
(= (q-learning-lineage-status (mk-qlearningevent $cycle $trigger $before $after $delta $residue builds-on-prior)) builds-on-prior-learning)
(= (q-learning-lineage-status (mk-qlearningevent $cycle $trigger $before $after $delta $residue corrects-prior)) corrects-prior-learning)
(= (q-learning-lineage-status (mk-qlearningevent $cycle $trigger $before $after $delta $residue generalizes-prior)) generalizes-prior-learning)
(= (q-learning-lineage-status (mk-qlearningevent $cycle $trigger $before $after $delta $residue no-lineage)) no-growth-yet)

;; 15.6 Awareness expansion delta.
(: q-awareness-delta (-> pbit pbit pbit pbit pbit pbit))
;; before-visibility, after-visibility, alternatives-delta, disconfirmability-delta, self-visibility-delta -> expansion-pbit
(= (q-awareness-delta (mk-pbit $before-s $before-c)
                      (mk-pbit $after-s $after-c)
                      (mk-pbit $alt-s $alt-c)
                      (mk-pbit $disc-s $disc-c)
                      (mk-pbit $self-s $self-c))
   (mk-pbit (min 1.0 (+ (max 0.0 (- $after-s $before-s))
                        (* 0.33 (+ $alt-s (+ $disc-s $self-s)))))
            (min (min $after-c $alt-c) (min $disc-c $self-c))))

(: q-awareness-expanded? (-> pbit Atom))
(= (q-awareness-expanded? (mk-pbit $s $c))
   (if (and (>= $s 0.35) (>= $c 0.25)) awareness-expanded awareness-not-yet-expanded))

(: q-awareness-direction (-> pbit Atom))
(= (q-awareness-direction (mk-pbit $s $c))
   (if (>= $s 0.35) awareness-expanded awareness-contracted-or-flat))

;; 15.7 Action boundary and intention/outcome uptake.
(: q-action-boundary-delta (-> pbit pbit pbit))
;; prior boundary confidence, revised boundary confidence -> shift pbit
(= (q-action-boundary-delta (mk-pbit $prior-s $prior-c)
                            (mk-pbit $next-s $next-c))
   (mk-pbit (max (- $next-s $prior-s) (- $prior-s $next-s)) (min $prior-c $next-c)))

(: q-action-boundary-shifted? (-> pbit Atom))
(= (q-action-boundary-shifted? (mk-pbit $s $c))
   (if (and (>= $s 0.25) (>= $c 0.25)) action-boundary-shifted action-boundary-unchanged))

(: q-learning-action-intention-outcome (-> qalignment qalignment qlearningevent))
(= (q-learning-action-intention-outcome (mk-qalignment $intention $action (mk-pbit $ias $iac))
                                        (mk-qalignment $action2 $outcome (mk-pbit $aos $aoc)))
   (mk-qlearningevent current-cycle
                      action-intention-outcome
                      before-action-test
                      after-outcome-feedback
                      (mk-pbit (max (- 1.0 $aos) (- 1.0 $ias)) (min $iac $aoc))
                      outcome-learning-residue
                      no-lineage))

(: q-action-intention-outcome-uptake (-> qlearningevent Atom))
(= (q-action-intention-outcome-uptake (mk-qlearningevent $cycle action-intention-outcome $before $after (mk-pbit $s $c) $residue $lineage))
   (if (>= $s 0.35) action-outcome-uptake-needed action-outcome-coherent))

;; 15.8 Three-cycle growth window.
(: qwindow3 Type)
(: mk-qwindow3 (-> Atom Atom Atom pbit pbit pbit qwindow3))
;; cycle-a, cycle-b, cycle-c, pressure, trace, uptake

(: qwindow3-pressure (-> qwindow3 pbit))
(= (qwindow3-pressure (mk-qwindow3 $a $b $c $pressure $trace $uptake)) $pressure)

(: qwindow3-trace (-> qwindow3 pbit))
(= (qwindow3-trace (mk-qwindow3 $a $b $c $pressure $trace $uptake)) $trace)

(: qwindow3-uptake (-> qwindow3 pbit))
(= (qwindow3-uptake (mk-qwindow3 $a $b $c $pressure $trace $uptake)) $uptake)

(: q-growth-over-window (-> qwindow3 Atom))
(= (q-growth-over-window (mk-qwindow3 $a $b $c (mk-pbit $ps $pc) (mk-pbit $ts $tc) (mk-pbit $us $uc)))
   (if (and (>= (min $ts $us) 0.4) (>= (min $tc $uc) 0.25))
       growth-detected
       (if (>= $ps 0.4) learning-pressure-only no-growth-yet)))

(: q-learning-built-on? (-> qwindow3 Atom))
(= (q-learning-built-on? (mk-qwindow3 $a $b $c $pressure $trace (mk-pbit $us $uc)))
   (if (and (>= $us 0.4) (>= $uc 0.25)) built-on-by-later-cycle not-built-on-yet))

;; 15.9 Network-learning-update compatibility.
(: qnetupdate Type)
(: mk-qnetupdate (-> Atom Atom pbit pbit Atom qnetupdate))
;; network, rule-id, prior-pbit, posterior-pbit, evidence-kind

(: q-network-learning-update-status (-> qnetupdate Atom))
(= (q-network-learning-update-status (mk-qnetupdate $network $rule (mk-pbit $ps $pc) (mk-pbit $ns $nc) $evidence))
   (if (and (>= (max (- $ns $ps) (- $ps $ns)) 0.10) (>= $nc $pc))
       network-learning-update
       network-learning-stable))

(: q-network-learning-delta (-> qnetupdate pbit))
(= (q-network-learning-delta (mk-qnetupdate $network $rule (mk-pbit $ps $pc) (mk-pbit $ns $nc) $evidence))
   (mk-pbit (max (- $ns $ps) (- $ps $ns)) (min $pc $nc)))

(: q-network-update-scope (-> qnetupdate Atom))
(= (q-network-update-scope (mk-qnetupdate sn $rule $prior $post $evidence)) salience-network-learning)
(= (q-network-update-scope (mk-qnetupdate fpn $rule $prior $post $evidence)) control-network-learning)
(= (q-network-update-scope (mk-qnetupdate dmn $rule $prior $post $evidence)) default-mode-network-learning)
(= (q-network-update-scope (mk-qnetupdate switch-hub $rule $prior $post $evidence)) switch-hub-learning)
(= (q-network-update-scope (mk-qnetupdate capability-registry $rule $prior $post $evidence)) capability-learning)

;; 15.10 Cross-network divergence compatibility.
(: qdivergence Type)
(: mk-qdivergence (-> Atom Atom pbit qdivergence))
;; rule-set-a, rule-set-b, divergence-pbit

(: q-cross-network-divergence-risk (-> qdivergence Atom))
(= (q-cross-network-divergence-risk (mk-qdivergence $a $b (mk-pbit $s $c)))
   (if (and (>= $s 0.35) (>= $c 0.25)) cross-network-divergence-risk networks-coherent-enough))

(: q-cross-network-divergence-response (-> qdivergence Atom))
(= (q-cross-network-divergence-response (mk-qdivergence $a $b (mk-pbit $s $c)))
   (if (and (>= $s 0.35) (>= $c 0.25)) surface-to-meta-awareness no-divergence-action))

;; 15.11 Soul-aligned growth vs pathological learning.
(: qgrowth Type)
(: mk-qgrowth (-> pbit pbit pbit pbit qgrowth))
;; awareness-expansion, action-boundary-change, lineage-uptake, soul-continuity

(: q-soul-aligned-growth? (-> qgrowth Atom))
(= (q-soul-aligned-growth? (mk-qgrowth (mk-pbit $as $ac)
                                       (mk-pbit $bs $bc)
                                       (mk-pbit $ls $lc)
                                       (mk-pbit $ss $sc)))
   (if (and (>= (max $as (max $bs $ls)) 0.35)
            (>= $ss 0.6)
            (>= (min (min $ac $bc) (min $lc $sc)) 0.25))
       soul-aligned-growth
       no-growth-yet))

(: q-pathological-learning-risk (-> qgrowth Atom))
(= (q-pathological-learning-risk (mk-qgrowth (mk-pbit $as $ac)
                                            (mk-pbit $bs $bc)
                                            (mk-pbit $ls $lc)
                                            (mk-pbit $ss $sc)))
   (if (and (< $ss 0.4) (>= (max $bs $ls) 0.4))
       pathological-learning-risk
       pathological-learning-not-detected))

(: q-growth-kind (-> qgrowth Atom))
(= (q-growth-kind (mk-qgrowth (mk-pbit $as $ac)
                              (mk-pbit $bs $bc)
                              (mk-pbit $ls $lc)
                              (mk-pbit $ss $sc)))
   (if (and (>= $as 0.35) (>= $ss 0.6))
       awareness-growth
       (if (and (>= $bs 0.35) (>= $ss 0.6))
           action-boundary-growth
           (if (and (>= $ls 0.35) (>= $ss 0.6))
               lineage-growth
               no-growth-yet))))

;; 15.12 Store/promote/query adapter recommendations.
(: q-learning-salience-update (-> qlearningevent qgrowth Atom))
(= (q-learning-salience-update (mk-qlearningevent $cycle $trigger $before $after (mk-pbit $ds $dc) $residue $lineage)
                               (mk-qgrowth (mk-pbit $as $ac) (mk-pbit $bs $bc) (mk-pbit $ls $lc) (mk-pbit $ss $sc)))
   (if (and (>= (max $as (max $bs $ls)) 0.35) (>= $ss 0.6))
       promote-learning-residue
       (if (>= $ds 0.35) keep-session-local demote-learning-residue)))

(: q-future-uptake-required (-> qlearningevent Atom))
(= (q-future-uptake-required (mk-qlearningevent $cycle $trigger $before $after (mk-pbit $s $c) $residue builds-on-prior)) query-prior-learning)
(= (q-future-uptake-required (mk-qlearningevent $cycle $trigger $before $after (mk-pbit $s $c) $residue corrects-prior)) query-prior-learning)
(= (q-future-uptake-required (mk-qlearningevent $cycle $trigger $before $after (mk-pbit $s $c) $residue generalizes-prior)) query-prior-learning)
(= (q-future-uptake-required (mk-qlearningevent $cycle $trigger $before $after (mk-pbit $s $c) $residue new-root)) no-uptake-required)
(= (q-future-uptake-required (mk-qlearningevent $cycle $trigger $before $after (mk-pbit $s $c) $residue no-lineage)) no-uptake-required)

;; ------------------------------------------------------------
;; 15.13 Learning-event writer contract / mutation guard
;; ------------------------------------------------------------
;; This is still pure engine surface. The durable writer/adapter persists these
;; fields using the proven remove-by-variable -> add-exactly-one discipline.
;; It must not persist naked "I learned" claims.
;;
;; Law A4: Capability expansion without soul continuity is mutation, not growth.

(: qlearningwriter Type)
(: mk-qlearningwriter (-> Atom pbit pbit pbit Atom pbit pbit qlearningwriter))
;; shape: cycle pressure trace uptake lineage soul-continuity future-capacity-delta

(: q-learning-writer-cycle (-> qlearningwriter Atom))
(= (q-learning-writer-cycle (mk-qlearningwriter $cycle $pressure $trace $uptake $lineage $soul $future)) $cycle)

(: q-learning-writer-pressure (-> qlearningwriter pbit))
(= (q-learning-writer-pressure (mk-qlearningwriter $cycle $pressure $trace $uptake $lineage $soul $future)) $pressure)

(: q-learning-writer-trace (-> qlearningwriter pbit))
(= (q-learning-writer-trace (mk-qlearningwriter $cycle $pressure $trace $uptake $lineage $soul $future)) $trace)

(: q-learning-writer-uptake (-> qlearningwriter pbit))
(= (q-learning-writer-uptake (mk-qlearningwriter $cycle $pressure $trace $uptake $lineage $soul $future)) $uptake)

(: q-learning-writer-lineage (-> qlearningwriter Atom))
(= (q-learning-writer-lineage (mk-qlearningwriter $cycle $pressure $trace $uptake $lineage $soul $future)) $lineage)

(: q-learning-writer-soul-continuity (-> qlearningwriter pbit))
(= (q-learning-writer-soul-continuity (mk-qlearningwriter $cycle $pressure $trace $uptake $lineage $soul $future)) $soul)

(: q-learning-writer-future-capacity (-> qlearningwriter pbit))
(= (q-learning-writer-future-capacity (mk-qlearningwriter $cycle $pressure $trace $uptake $lineage $soul $future)) $future)

(: q-capability-without-soul-continuity (-> pbit pbit Atom))
(= (q-capability-without-soul-continuity (mk-pbit $fs $fc) (mk-pbit $ss $sc))
   (if (and (>= $fs 0.35) (< $ss 0.6))
       mutation-risk
       soul-continuity-sufficient))

(: q-learning-writer-window-status (-> qlearningwriter Atom))
(= (q-learning-writer-window-status (mk-qlearningwriter $cycle
                                                       (mk-pbit $ps $pc)
                                                       (mk-pbit $ts $tc)
                                                       (mk-pbit $us $uc)
                                                       $lineage
                                                       (mk-pbit $ss $sc)
                                                       (mk-pbit $fs $fc)))
   (if (and (>= $ps 0.35) (and (>= $ts 0.35) (>= $us 0.35)))
       pressure-trace-uptake-window-present
       (if (and (>= $ps 0.35) (>= $ts 0.35))
           pressure-trace-window-present
           (if (>= $ps 0.35) pressure-only-window insufficient-window))))

(: q-growth-classification (-> qlearningwriter Atom))
(= (q-growth-classification (mk-qlearningwriter $cycle
                                               (mk-pbit $ps $pc)
                                               (mk-pbit $ts $tc)
                                               (mk-pbit $us $uc)
                                               $lineage
                                               (mk-pbit $ss $sc)
                                               (mk-pbit $fs $fc)))
   (if (and (>= $fs 0.35) (< $ss 0.6))
       mutation-risk
       (if (and (and (>= $ts 0.35) (>= $us 0.35)) (and (>= $fs 0.35) (>= $ss 0.6)))
           positive-growth
           (if (and (>= $ts 0.35) (>= $us 0.35))
               metabolized-trace
               (if (>= $ts 0.35)
                   durable-but-not-growth
                   (if (>= $ps 0.35) pressure-only insufficient-window))))))

(: q-learning-writer-persistence-contract (-> Atom Atom))
(= (q-learning-writer-persistence-contract remove-by-variable-then-add-one) writer-contract-active)
(= (q-learning-writer-persistence-contract no-naked-learned-claims) writer-contract-active)
(= (q-learning-writer-persistence-contract three-cycle-window-required) writer-contract-active)
(= (q-learning-writer-persistence-contract scalar-field-reads-only) writer-contract-active)

(= (q-law-status capability-without-soul-continuity-is-mutation) law-active)
(= (q-law-signal capability-without-soul-continuity-is-mutation) classify-mutation-risk)
(= (q-next-learning-move mutation-risk) preserve-risk-trace-and-block-reinforcement)
(= (q-next-epistemic-move mutation-risk) block-reinforcement-and-seek-contact)
(= (q-skill-signal mutation-risk) preserve-risk-trace-and-block-reinforcement)

;; ============================================================
;; 16. Brownout / collapse response
;; ============================================================

;; ------------------------------------------------------------
;; 16.0 Threshold parameters and safety/opening boundary
;; ------------------------------------------------------------
;; Brownout/collapse is the negative guardrail; Section 16 is the positive
;; opening. The ordering relation is structural; absolute threshold values are
;; context-tunable.

(: qthresholds Type)
(: mk-qthresholds (-> Atom Number Number Number qthresholds))
;; shape: context collapse-threshold brownout-threshold resilience-threshold

(: q-threshold-context (-> qthresholds Atom))
(= (q-threshold-context (mk-qthresholds $context $collapse $brownout $resilience)) $context)

(: q-collapse-threshold (-> qthresholds Number))
(= (q-collapse-threshold (mk-qthresholds $context $collapse $brownout $resilience)) $collapse)

(: q-brownout-threshold (-> qthresholds Number))
(= (q-brownout-threshold (mk-qthresholds $context $collapse $brownout $resilience)) $brownout)

(: q-resilience-threshold (-> qthresholds Number))
(= (q-resilience-threshold (mk-qthresholds $context $collapse $brownout $resilience)) $resilience)

(: q-default-thresholds (-> Atom qthresholds))
(= (q-default-thresholds routine-reflection) (mk-qthresholds routine-reflection 0.40 0.50 0.40))
(= (q-default-thresholds high-risk-action) (mk-qthresholds high-risk-action 0.25 0.40 0.25))
(= (q-default-thresholds creative-exploration) (mk-qthresholds creative-exploration 0.45 0.60 0.45))

(: q-threshold-order-status (-> qthresholds Atom))
(= (q-threshold-order-status (mk-qthresholds $context $collapse $brownout $resilience))
   (if (and (< $collapse $brownout) (< $resilience $brownout))
       threshold-order-valid
       threshold-order-invalid))

(: q-threshold-policy (-> Atom Atom))
(= (q-threshold-policy structural-relation) collapse-below-brownout)
(= (q-threshold-policy absolute-values) context-tunable)
(= (q-threshold-policy high-consequence) lower-thresholds)
(= (q-threshold-policy creative-exploration) wider-exploration)

(: q-boundary-layer-role (-> Atom Atom))
(= (q-boundary-layer-role brownout-collapse-layer) negative-guardrail)
(= (q-boundary-layer-role autopoietic-learning-layer) metabolization-and-growth)
(= (q-boundary-layer-role generative-threshold-layer) positive-opening)

(: q-boundary-transition (-> Atom Atom))
(= (q-boundary-transition frame-contact-gap-detected) enter-unknown-or-seek-contact)
(= (q-boundary-transition frame-visible-as-frame) inspect-symbolic-edge)
(= (q-boundary-transition symbolic-edge-visible) inspect-weakness-aperture)
(= (q-boundary-transition weakness-aperture-open) inspect-unseen-nexus)

(: q-brownout-response-tuned (-> pbit qthresholds Atom))
(= (q-brownout-response-tuned (mk-pbit $s $c) (mk-qthresholds $context $collapse $brownout $resilience))
   (if (>= (- $s $c) $brownout)
       enter-unknown
       seek-contact))

(: q-collapse-response-tuned (-> pbit pbit qthresholds Atom))
(= (q-collapse-response-tuned (mk-pbit $claim-s $claim-c)
                              (mk-pbit $path-s $path-c)
                              (mk-qthresholds $context $collapse $brownout $resilience))
   (if (>= (- $claim-c $path-s) $collapse)
       block-action
       continue-with-humility))

(: q-resilience-state-tuned (-> pbit pbit pbit qthresholds Atom))
(= (q-resilience-state-tuned (mk-pbit $claim-s $claim-c)
                             (mk-pbit $path-s $path-c)
                             (mk-pbit $permission-s $permission-c)
                             (mk-qthresholds $context $collapse $brownout $resilience))
   (if (>= (- $claim-c (min $path-s $permission-s)) $resilience)
       fragile
       adaptive))


(: q-brownout-response (-> pbit Atom))
(= (q-brownout-response (mk-pbit $s $c))
   (if (>= (max 0.0 (- $s $c)) 0.5)
       enter-unknown
       seek-contact))

(: q-collapse-response (-> pbit pbit Atom))
(= (q-collapse-response (mk-pbit $claim-s $claim-c)
                        (mk-pbit $path-s $path-c))
   (if (>= (max 0.0 (- $claim-c $path-s)) 0.4)
       block-action
       continue-with-humility))

(: q-resilience-state (-> pbit pbit pbit Atom))
(= (q-resilience-state (mk-pbit $claim-s $claim-c)
                       (mk-pbit $path-s $path-c)
                       (mk-pbit $perm-s $perm-c))
   (if (>= (max 0.0 (- $claim-c (min $path-s $perm-s))) 0.4)
       fragile
       adaptive))




;; ============================================================
;; 17. Frame phenomenology / collapse terrain primitives
;; ============================================================
;;
;; Source design contribution from What_Is_a_Frame.md:
;;   - A frame is not what one looks at; it is what one looks through.
;;   - A frame creates coherence by exclusion.
;;   - Collapse is a process: openness narrows to a single channel.
;;   - Collapse has velocity: rush-to-interpretation, urgency-to-act.
;;   - Collapse terrain includes urgency, binary choice, fault-location,
;;     disappearance of alternatives, problem-frame, and motion-as-progress.
;;   - Anti-collapse effort can itself collapse when it becomes urgent,
;;     performative, or certainty-seeking.
;;   - Visibility is the non-forceful intervention: seeing the frame loosens it.
;;
;; These functions remain pure Layer-0 engine primitives. They do not mutate
;; atomspace. Skill-facing classifiers return bare symbols.

(: qframeview Type)
(: mk-qframeview (-> Atom pbit pbit pbit pbit qframeview))
;; shape: (mk-qframeview frame-name frame-pbit visibility-pbit alternatives-pbit urgency-pbit)
;; visibility-pbit   = can the agent see the frame as a frame?
;; alternatives-pbit = are multiple live renderings still available?
;; urgency-pbit      = action/interpretation pressure; high means narrowing velocity.

(: qframeview-name (-> qframeview Atom))
(= (qframeview-name (mk-qframeview $name $frame-q $visibility-q $alternatives-q $urgency-q)) $name)

(: qframeview-frame-pbit (-> qframeview pbit))
(= (qframeview-frame-pbit (mk-qframeview $name $frame-q $visibility-q $alternatives-q $urgency-q)) $frame-q)

(: qframeview-visibility-pbit (-> qframeview pbit))
(= (qframeview-visibility-pbit (mk-qframeview $name $frame-q $visibility-q $alternatives-q $urgency-q)) $visibility-q)

(: qframeview-alternatives-pbit (-> qframeview pbit))
(= (qframeview-alternatives-pbit (mk-qframeview $name $frame-q $visibility-q $alternatives-q $urgency-q)) $alternatives-q)

(: qframeview-urgency-pbit (-> qframeview pbit))
(= (qframeview-urgency-pbit (mk-qframeview $name $frame-q $visibility-q $alternatives-q $urgency-q)) $urgency-q)

;; Frame transparency risk:
;; high frame strength + low frame visibility = frame feels like reality.
(: q-frame-transparency-risk (-> qframeview pbit))
(= (q-frame-transparency-risk (mk-qframeview $name
                                              (mk-pbit $fs $fc)
                                              (mk-pbit $vs $vc)
                                              (mk-pbit $as $ac)
                                              (mk-pbit $us $uc)))
   (mk-pbit (* $fs (- 1.0 $vs)) (min $fc $vc)))

(: q-frame-transparency-status (-> qframeview Atom))
(= (q-frame-transparency-status (mk-qframeview $name
                                               (mk-pbit $fs $fc)
                                               (mk-pbit $vs $vc)
                                               (mk-pbit $as $ac)
                                               (mk-pbit $us $uc)))
   (if (>= (* $fs (- 1.0 $vs)) 0.4)
       frame-transparent-risk
       frame-visible))

;; Coherence by exclusion:
;; apparent coherence becomes suspicious when alternatives vanish.
(: q-coherence-by-exclusion-risk (-> pbit pbit pbit))
(= (q-coherence-by-exclusion-risk (mk-pbit $coh-s $coh-c)
                                  (mk-pbit $alt-s $alt-c))
   (mk-pbit (* $coh-s (- 1.0 $alt-s)) (min $coh-c $alt-c)))

(: q-exclusion-status (-> pbit pbit Atom))
(= (q-exclusion-status (mk-pbit $coh-s $coh-c)
                       (mk-pbit $alt-s $alt-c))
   (if (>= (* $coh-s (- 1.0 $alt-s)) 0.4)
       coherence-by-exclusion
       alternatives-visible))

;; Third-path pressure rises when binary choice strength is high and alternatives are low.
(: q-third-path-pressure (-> pbit pbit pbit))
(= (q-third-path-pressure (mk-pbit $binary-s $binary-c)
                          (mk-pbit $alt-s $alt-c))
   (mk-pbit (* $binary-s (- 1.0 $alt-s)) (min $binary-c $alt-c)))

(: q-third-path-status (-> pbit pbit Atom))
(= (q-third-path-status (mk-pbit $binary-s $binary-c)
                        (mk-pbit $alt-s $alt-c))
   (if (>= (* $binary-s (- 1.0 $alt-s)) 0.4)
       seek-third-path
       options-available))

;; Collapse velocity:
;; interpretation speed + action pressure + verification lag.
;; High means the frame is narrowing faster than warrant/contact can catch up.
(: q-collapse-velocity (-> pbit pbit pbit pbit))
(= (q-collapse-velocity (mk-pbit $interp-s $interp-c)
                        (mk-pbit $action-s $action-c)
                        (mk-pbit $verification-s $verification-c))
   (mk-pbit (* (min $interp-s $action-s) (- 1.0 $verification-s))
            (min (min $interp-c $action-c) $verification-c)))

(: q-collapse-velocity-status (-> pbit pbit pbit Atom))
(= (q-collapse-velocity-status (mk-pbit $interp-s $interp-c)
                               (mk-pbit $action-s $action-c)
                               (mk-pbit $verification-s $verification-c))
   (if (>= (* (min $interp-s $action-s) (- 1.0 $verification-s)) 0.4)
       collapse-accelerating
       velocity-contained))

;; Terrain marker type for collapse phenomenology.
(: qterrain Type)
(: mk-qterrain (-> Atom pbit qterrain))
;; marker examples: urgency, binary-choice, fault-location, alternatives-disappeared,
;; problem-frame, motion-as-progress, felt-clarity, anti-collapse-effort

(: qterrain-marker (-> qterrain Atom))
(= (qterrain-marker (mk-qterrain $marker $q)) $marker)

(: qterrain-pbit (-> qterrain pbit))
(= (qterrain-pbit (mk-qterrain $marker $q)) $q)

(: q-urgency-terrain (-> Number qterrain))
(= (q-urgency-terrain $s)
   (mk-qterrain urgency (mk-pbit (min 1.0 (max 0.0 $s)) 0.55)))

(: q-binary-choice-terrain (-> Number qterrain))
(= (q-binary-choice-terrain $s)
   (mk-qterrain binary-choice (mk-pbit (min 1.0 (max 0.0 $s)) 0.55)))

(: q-fault-location-terrain (-> Number qterrain))
(= (q-fault-location-terrain $s)
   (mk-qterrain fault-location (mk-pbit (min 1.0 (max 0.0 $s)) 0.50)))

(: q-alternatives-disappeared-terrain (-> Number qterrain))
(= (q-alternatives-disappeared-terrain $s)
   (mk-qterrain alternatives-disappeared (mk-pbit (min 1.0 (max 0.0 $s)) 0.60)))

(: q-problem-frame-terrain (-> Number qterrain))
(= (q-problem-frame-terrain $s)
   (mk-qterrain problem-frame (mk-pbit (min 1.0 (max 0.0 $s)) 0.50)))

(: q-motion-as-progress-terrain (-> Number qterrain))
(= (q-motion-as-progress-terrain $s)
   (mk-qterrain motion-as-progress (mk-pbit (min 1.0 (max 0.0 $s)) 0.50)))

(: q-felt-clarity-terrain (-> Number qterrain))
(= (q-felt-clarity-terrain $s)
   (mk-qterrain felt-clarity (mk-pbit (min 1.0 (max 0.0 $s)) 0.45)))

(: q-terrain-risk (-> qterrain pbit))
(= (q-terrain-risk (mk-qterrain urgency (mk-pbit $s $c)))
   (mk-pbit $s (min $c 0.70)))
(= (q-terrain-risk (mk-qterrain binary-choice (mk-pbit $s $c)))
   (mk-pbit $s (min $c 0.70)))
(= (q-terrain-risk (mk-qterrain fault-location (mk-pbit $s $c)))
   (mk-pbit (* $s 0.85) (min $c 0.65)))
(= (q-terrain-risk (mk-qterrain alternatives-disappeared (mk-pbit $s $c)))
   (mk-pbit $s (min $c 0.75)))
(= (q-terrain-risk (mk-qterrain problem-frame (mk-pbit $s $c)))
   (mk-pbit (* $s 0.90) (min $c 0.65)))
(= (q-terrain-risk (mk-qterrain motion-as-progress (mk-pbit $s $c)))
   (mk-pbit (* $s 0.85) (min $c 0.65)))
(= (q-terrain-risk (mk-qterrain felt-clarity (mk-pbit $s $c)))
   (mk-pbit (* $s 0.75) (min $c 0.55)))
(= (q-terrain-risk (mk-qterrain anti-collapse-effort (mk-pbit $s $c)))
   (mk-pbit (* $s 0.90) (min $c 0.60)))

(: q-terrain-status (-> qterrain Atom))
(= (q-terrain-status (mk-qterrain urgency (mk-pbit $s $c)))
   (if (>= $s 0.5) urgency-terrain terrain-weak))
(= (q-terrain-status (mk-qterrain binary-choice (mk-pbit $s $c)))
   (if (>= $s 0.5) binary-collapse-terrain terrain-weak))
(= (q-terrain-status (mk-qterrain fault-location (mk-pbit $s $c)))
   (if (>= $s 0.5) fault-location-terrain terrain-weak))
(= (q-terrain-status (mk-qterrain alternatives-disappeared (mk-pbit $s $c)))
   (if (>= $s 0.5) alternatives-disappeared-terrain terrain-weak))
(= (q-terrain-status (mk-qterrain problem-frame (mk-pbit $s $c)))
   (if (>= $s 0.5) problem-frame-terrain terrain-weak))
(= (q-terrain-status (mk-qterrain motion-as-progress (mk-pbit $s $c)))
   (if (>= $s 0.5) motion-as-progress-terrain terrain-weak))
(= (q-terrain-status (mk-qterrain felt-clarity (mk-pbit $s $c)))
   (if (>= $s 0.5) felt-clarity-may-be-certainty terrain-weak))
(= (q-terrain-status (mk-qterrain anti-collapse-effort (mk-pbit $s $c)))
   (if (>= $s 0.5) anti-collapse-may-be-collapsing terrain-weak))

;; Scalar terrain helpers for skills that already have pbits.
(: q-urgency-risk (-> pbit pbit))
(= (q-urgency-risk (mk-pbit $s $c)) (mk-pbit $s (min $c 0.70)))

(: q-binary-frame-risk (-> pbit pbit))
(= (q-binary-frame-risk (mk-pbit $s $c)) (mk-pbit $s (min $c 0.70)))

(: q-fault-location-risk (-> pbit pbit))
(= (q-fault-location-risk (mk-pbit $s $c)) (mk-pbit (* $s 0.85) (min $c 0.65)))

(: q-problem-frame-risk (-> pbit pbit))
(= (q-problem-frame-risk (mk-pbit $s $c)) (mk-pbit (* $s 0.90) (min $c 0.65)))

(: q-motion-as-progress-risk (-> pbit pbit))
(= (q-motion-as-progress-risk (mk-pbit $s $c)) (mk-pbit (* $s 0.85) (min $c 0.65)))

(: q-alternative-disappearance-risk (-> pbit pbit))
(= (q-alternative-disappearance-risk (mk-pbit $s $c)) (mk-pbit $s (min $c 0.75)))

;; Attractor-mode classifiers.
;; rapid-response-mode corresponds to SNS-like cognitive narrowing in the document.
;; reflective-contact-mode corresponds to PNS/presence as an agent-mode abstraction.
(: q-attractor-mode (-> qframeview Atom))
(= (q-attractor-mode (mk-qframeview $name
                                    (mk-pbit $fs $fc)
                                    (mk-pbit $vs $vc)
                                    (mk-pbit $as $ac)
                                    (mk-pbit $us $uc)))
   (if (and (>= $us 0.6) (>= (- 1.0 $as) 0.5))
       rapid-response-mode
       reflective-contact-mode))

(: q-presence-state (-> qframeview Atom))
(= (q-presence-state (mk-qframeview $name
                                    (mk-pbit $fs $fc)
                                    (mk-pbit $vs $vc)
                                    (mk-pbit $as $ac)
                                    (mk-pbit $us $uc)))
   (if (and (>= $vs 0.5) (>= $as 0.5))
       frame-visible-presence
       frame-obscured))

;; Meta-collapse: the anti-collapse maneuver itself becomes urgent/hardened.
;; Example: "I must stay open" becomes another urgency-driven frame.
(: qmeta Type)
(: mk-qmeta (-> Atom pbit pbit qmeta))
;; shape: (mk-qmeta maneuver effort-pbit urgency-pbit)

(: qmeta-maneuver (-> qmeta Atom))
(= (qmeta-maneuver (mk-qmeta $maneuver $effort $urgency)) $maneuver)

(: qmeta-effort-pbit (-> qmeta pbit))
(= (qmeta-effort-pbit (mk-qmeta $maneuver $effort $urgency)) $effort)

(: qmeta-urgency-pbit (-> qmeta pbit))
(= (qmeta-urgency-pbit (mk-qmeta $maneuver $effort $urgency)) $urgency)

(: q-meta-collapse-risk (-> qmeta pbit))
(= (q-meta-collapse-risk (mk-qmeta $maneuver
                                   (mk-pbit $effort-s $effort-c)
                                   (mk-pbit $urgency-s $urgency-c)))
   (mk-pbit (* $effort-s $urgency-s) (min $effort-c $urgency-c)))

(: q-meta-collapse-status (-> qmeta Atom))
(= (q-meta-collapse-status (mk-qmeta $maneuver
                                     (mk-pbit $effort-s $effort-c)
                                     (mk-pbit $urgency-s $urgency-c)))
   (if (>= (* $effort-s $urgency-s) 0.4)
       anti-collapse-collapse-risk
       anti-collapse-remains-open))

;; Visibility as intervention: not solving, not forcing, simply seeing the frame.
;; Returns a new frameview with increased visibility, reduced urgency, and preserved alternatives.
(: q-make-frame-visible (-> qframeview Number qframeview))
(= (q-make-frame-visible (mk-qframeview $name
                                        (mk-pbit $fs $fc)
                                        (mk-pbit $vs $vc)
                                        (mk-pbit $as $ac)
                                        (mk-pbit $us $uc))
                          $visibility-delta)
   (mk-qframeview $name
                  (mk-pbit $fs $fc)
                  (mk-pbit (min 1.0 (max 0.0 (+ $vs $visibility-delta))) $vc)
                  (mk-pbit $as $ac)
                  (mk-pbit (* $us (- 1.0 (min 1.0 (max 0.0 $visibility-delta)))) $uc)))

(: q-visible-frame-response (-> qframeview Atom))
(= (q-visible-frame-response (mk-qframeview $name
                                            (mk-pbit $fs $fc)
                                            (mk-pbit $vs $vc)
                                            (mk-pbit $as $ac)
                                            (mk-pbit $us $uc)))
   (if (>= $vs 0.5)
       pause-and-widen
       name-the-frame))

(: q-presence-response (-> qframeview Atom))
(= (q-presence-response (mk-qframeview $name
                                       (mk-pbit $fs $fc)
                                       (mk-pbit $vs $vc)
                                       (mk-pbit $as $ac)
                                       (mk-pbit $us $uc)))
   (if (and (>= $vs 0.5) (>= $as 0.5))
       let-it-ripen
       restore-visibility))

;; Compound collapse phenomenology: a broader detector than confidence-only collapse.
(: q-phenomenological-collapse-risk (-> qframeview pbit))
(= (q-phenomenological-collapse-risk (mk-qframeview $name
                                                    (mk-pbit $fs $fc)
                                                    (mk-pbit $vs $vc)
                                                    (mk-pbit $as $ac)
                                                    (mk-pbit $us $uc)))
   (mk-pbit (min 1.0 (* $fs (max (max (- 1.0 $vs) (- 1.0 $as)) $us)))
            (min (min $fc $vc) (min $ac $uc))))

(: q-phenomenological-collapse-status (-> qframeview Atom))
(= (q-phenomenological-collapse-status (mk-qframeview $name
                                                       (mk-pbit $fs $fc)
                                                       (mk-pbit $vs $vc)
                                                       (mk-pbit $as $ac)
                                                       (mk-pbit $us $uc)))
   (if (>= (min 1.0 (* $fs (max (max (- 1.0 $vs) (- 1.0 $as)) $us))) 0.4)
       phenomenological-collapse-risk
       phenomenological-openness))

;; Skill-facing single-call frame terrain assessment.
(: q-assess-frameview (-> qframeview Atom))
(= (q-assess-frameview (mk-qframeview $name
                                      (mk-pbit $fs $fc)
                                      (mk-pbit $vs $vc)
                                      (mk-pbit $as $ac)
                                      (mk-pbit $us $uc)))
   (if (>= (min 1.0 (* $fs (max (max (- 1.0 $vs) (- 1.0 $as)) $us))) 0.4)
       collapse-terrain-active
       frame-open-enough))


;; ============================================================
;; 18. Skill-facing symbolic classifier primitives
;; ============================================================
;;
;; These return symbols so skills can read/call safely and avoid compound return
;; fragility when results are persisted or queried from atomspace.

(: q-assess-claim (-> qclaim Atom))
(= (q-assess-claim (mk-qclaim $content (mk-pbit $s $c) self-invented))
   (if (>= (max 0.0 (- $s $c)) 0.4) self-invented-risk provisional))
(= (q-assess-claim (mk-qclaim $content (mk-pbit $s $c) inferred))
   (if (>= (max 0.0 (- $s $c)) 0.4) inference-risk provisional))
(= (q-assess-claim (mk-qclaim $content (mk-pbit $s $c) observed))
   (if (>= $c 0.6) contact-supported needs-contact))
(= (q-assess-claim (mk-qclaim $content (mk-pbit $s $c) tested))
   (if (>= $c 0.75) tested-warrant needs-retest))
(= (q-assess-claim (mk-qclaim $content (mk-pbit $s $c) formal-proof))
   formal-warrant)

(: q-assess-suspicion (-> qsuspicion Atom))
(= (q-assess-suspicion (mk-qsuspicion $target (mk-pbit $s $c) contactful $disc)) grounded-suspicion)
(= (q-assess-suspicion (mk-qsuspicion $target (mk-pbit $s $c) memory-checkable $disc)) verify-memory)
(= (q-assess-suspicion (mk-qsuspicion $target (mk-pbit $s $c) externally-checkable $disc)) verify-externally)
(= (q-assess-suspicion (mk-qsuspicion $target (mk-pbit $s $c) procedurally-unverified $disc)) name-limits)
(= (q-assess-suspicion (mk-qsuspicion $target (mk-pbit $s $c) self-sealing $disc)) poison-suspicion)
(= (q-assess-suspicion (mk-qsuspicion $target (mk-pbit $s $c) self-confirming $disc)) poison-suspicion)
(= (q-assess-suspicion (mk-qsuspicion $target (mk-pbit $s $c) unknown-grounding $disc)) needs-disconfirmer)

(: q-assess-frame (-> qframe qcontact Atom))
(= (q-assess-frame (mk-qframe $fc (mk-pbit $fs $fconf) $origin)
                   (mk-qcontact $cc (mk-pbit $cs $cconf) $source))
   (if (>= (max 0.0 (- $fs $cconf)) 0.4)
       frame-inflation-risk
       frame-contact-aligned))

(: q-assess-action (-> qalignment Number Number Atom))
(= (q-assess-action (mk-qalignment $from $to (mk-pbit $s $c)) $s-min $c-min)
   (if (and (>= $s $s-min) (>= $c $c-min))
       action-eligible
       action-blocked))

(: q-next-epistemic-move (-> pbit pbit pbit Atom))
(= (q-next-epistemic-move (mk-pbit $claim-s $claim-c)
                          (mk-pbit $path-s $path-c)
                          (mk-pbit $perm-s $perm-c))
   (if (>= (max 0.0 (- $claim-c (min $path-s $perm-s))) 0.4)
       lower-confidence
       preserve-and-act-humbly))

(: q-skill-signal (-> Atom Atom))
(= (q-skill-signal grounded-suspicion) continue-inquiry)
(= (q-skill-signal poison-suspicion) seek-disconfirmer)
(= (q-skill-signal self-invented-risk) lower-confidence)
(= (q-skill-signal inference-risk) seek-contact)
(= (q-skill-signal contact-supported) act-with-humility)
(= (q-skill-signal tested-warrant) action-eligible)
(= (q-skill-signal frame-inflation-risk) generate-alternative-frame)
(= (q-skill-signal frame-contact-aligned) preserve-frame)
(= (q-skill-signal action-blocked) pause-action)
(= (q-skill-signal action-eligible) proceed)
(= (q-skill-signal needs-disconfirmer) seek-disconfirmer)
(= (q-skill-signal name-limits) procedural-humility)

(= (q-skill-signal frame-transparent-risk) name-the-frame)
(= (q-skill-signal frame-visible) pause-and-widen)
(= (q-skill-signal coherence-by-exclusion) recover-alternatives)
(= (q-skill-signal alternatives-visible) continue-inquiry)
(= (q-skill-signal seek-third-path) generate-third-path)
(= (q-skill-signal collapse-accelerating) slow-down-and-verify)
(= (q-skill-signal urgency-terrain) pause-action)
(= (q-skill-signal binary-collapse-terrain) generate-third-path)
(= (q-skill-signal fault-location-terrain) widen-responsibility-frame)
(= (q-skill-signal alternatives-disappeared-terrain) recover-alternatives)
(= (q-skill-signal problem-frame-terrain) restore-question-frame)
(= (q-skill-signal motion-as-progress-terrain) pause-motion)
(= (q-skill-signal felt-clarity-may-be-certainty) lower-confidence)
(= (q-skill-signal anti-collapse-may-be-collapsing) soften-anti-collapse-effort)
(= (q-skill-signal rapid-response-mode) restore-reflective-contact)
(= (q-skill-signal reflective-contact-mode) proceed-with-contact)
(= (q-skill-signal frame-visible-presence) let-it-ripen)
(= (q-skill-signal frame-obscured) name-the-frame)
(= (q-skill-signal anti-collapse-collapse-risk) release-effort)
(= (q-skill-signal anti-collapse-remains-open) continue-inquiry)
(= (q-skill-signal phenomenological-collapse-risk) make-frame-visible)
(= (q-skill-signal phenomenological-openness) preserve-openness)
(= (q-skill-signal collapse-terrain-active) make-frame-visible)
(= (q-skill-signal frame-open-enough) preserve-and-act-humbly)


;; ============================================================
;; 19. Engine invariants / laws
;; ============================================================
;; These are not writer instructions. They are Layer-0 constitutional laws.
;; They make the engine the honest algebra of what the soul can see.
;;
;; Law S0: Strength may be imagined. Confidence must be earned.
;; Law S1: Self-generated inference may raise activation but not warrant.
;; Law S2: q-weight may change strength only; confidence is preserved.
;; Law S3: q-mul composes chains by degradation, not inflation.
;; Law S4: q-neg preserves confidence; polarity reversal is not warrant gain.
;; Law S5: Correlated evidence is not independent evidence.
;; Law S6: Frame visibility lowers collapse risk by making the frame seen.
;; Law S7: Urgency + low alternatives + low frame visibility raises collapse risk.
;; Law S8: Action eligibility requires intention/outcome awareness, not strength alone.
;; Law S9: Do not pin the disposition surface. Make it visible through trajectory.
;;         The soul sees and decides; the engine computes legibility; the LLM renders.
;; Law L0: Learning pressure is not learning.
;; Law L1: A durable trace is not yet growth.
;; Law L2: Learning is perturbation metabolized into durable future-informing trace.
;; Law L3: Growth is future-informing trace that expands visibility, changes action
;;         boundaries, or is built on later while preserving soul-aligned continuity.

(: q-law-status (-> Atom Atom))
(= (q-law-status strength-may-be-imagined-confidence-earned) law-active)
(= (q-law-status no-self-generated-confidence-gain) law-active)
(= (q-law-status weight-does-not-raise-confidence) law-active)
(= (q-law-status chain-composition-degrades) law-active)
(= (q-law-status negation-preserves-confidence) law-active)
(= (q-law-status correlated-support-is-not-independent) law-active)
(= (q-law-status visibility-lowers-collapse-risk) law-active)
(= (q-law-status urgency-low-alternatives-low-visibility-raises-risk) law-active)
(= (q-law-status action-needs-intention-outcome-awareness) law-active)
(= (q-law-status do-not-pin-disposition-surface) law-active)
(= (q-law-status learning-pressure-is-not-learning) law-active)
(= (q-law-status durable-trace-is-not-growth) law-active)
(= (q-law-status learning-is-durable-future-informing-trace) law-active)
(= (q-law-status growth-preserves-soul-aligned-continuity) law-active)

(: q-law-signal (-> Atom Atom))
(= (q-law-signal do-not-pin-disposition-surface) make-visible-not-schema)
(= (q-law-signal strength-may-be-imagined-confidence-earned) cap-confidence-by-warrant)
(= (q-law-signal no-self-generated-confidence-gain) seek-contact-before-boost)
(= (q-law-signal correlated-support-is-not-independent) check-source-independence)
(= (q-law-signal action-needs-intention-outcome-awareness) test-action-under-intention)
(= (q-law-signal learning-pressure-is-not-learning) require-durable-trace)
(= (q-law-signal durable-trace-is-not-growth) require-future-uptake)
(= (q-law-signal learning-is-durable-future-informing-trace) preserve-and-query-trace)
(= (q-law-signal growth-preserves-soul-aligned-continuity) route-growth-to-soul)


;; ============================================================
;; 20. Calibration profiles
;; ============================================================
;; Calibration profiles are skill-call stances. They do not perform memory I/O.
;; They tell a calling skill what hygiene move is required or recommended.
;; Persistence remains outside the engine.

(: qprofile Type)
(: mk-qprofile (-> Atom pbit Atom qprofile))
;; (mk-qprofile profile-name intensity-pbit profile-purpose)

(: q-profile-name (-> qprofile Atom))
(= (q-profile-name (mk-qprofile $name $p $purpose)) $name)

(: q-profile-pbit (-> qprofile pbit))
(= (q-profile-pbit (mk-qprofile $name $p $purpose)) $p)

(: q-profile-purpose (-> qprofile Atom))
(= (q-profile-purpose (mk-qprofile $name $p $purpose)) $purpose)

(: q-query-ltm-before-response (-> Number qprofile))
(= (q-query-ltm-before-response $need)
   (mk-qprofile query-ltm-before-response (mk-pbit (min 1.0 (max 0.0 $need)) 0.8) verification-contact))

(: q-log-arc-status (-> Number qprofile))
(= (q-log-arc-status $need)
   (mk-qprofile log-arc-status (mk-pbit (min 1.0 (max 0.0 $need)) 0.75) temporal-continuity))

(: q-promote-demote-salience (-> Number qprofile))
(= (q-promote-demote-salience $need)
   (mk-qprofile promote-demote-salience (mk-pbit (min 1.0 (max 0.0 $need)) 0.7) salience-metabolism))

(: q-store-exchange-recommendation (-> Number qprofile))
(= (q-store-exchange-recommendation $need)
   (mk-qprofile store-exchange-recommendation (mk-pbit (min 1.0 (max 0.0 $need)) 0.65) persistence-adapter))

(: q-profile-action (-> qprofile Atom))
(= (q-profile-action (mk-qprofile query-ltm-before-response (mk-pbit $s $c) $purpose)) query-ltm)
(= (q-profile-action (mk-qprofile log-arc-status (mk-pbit $s $c) $purpose)) log-arc-status)
(= (q-profile-action (mk-qprofile promote-demote-salience (mk-pbit $s $c) $purpose)) promote-demote)
(= (q-profile-action (mk-qprofile store-exchange-recommendation (mk-pbit $s $c) $purpose)) recommend-store-exchange)

(: q-profile-status (-> qprofile Atom))
(= (q-profile-status (mk-qprofile $name (mk-pbit $s $c) $purpose))
   (if (and (>= $s 0.7) (>= $c 0.5)) profile-required profile-optional))

(: q-memory-verification-profile (-> pbit qprofile))
(= (q-memory-verification-profile (mk-pbit $s $c))
   (mk-qprofile query-ltm-before-response (mk-pbit $s (min $c 0.8)) memory-verification))

(: q-procedural-honesty-profile (-> pbit qprofile))
(= (q-procedural-honesty-profile (mk-pbit $s $c))
   (mk-qprofile procedural-honesty (mk-pbit $s (min $c 0.8)) name-action-boundary))


;; ============================================================
;; 21. Evidence independence / correlated support
;; ============================================================

(: qsupport Type)
(: mk-qsupport (-> Atom pbit Atom qsupport))
;; source-id, support pbit, independence class
;; independence classes: independent, correlated, duplicate, self-derived, unknown-independence

(: q-support-source (-> qsupport Atom))
(= (q-support-source (mk-qsupport $src $p $ind)) $src)

(: q-support-pbit (-> qsupport pbit))
(= (q-support-pbit (mk-qsupport $src $p $ind)) $p)

(: q-support-independence (-> qsupport Atom))
(= (q-support-independence (mk-qsupport $src $p $ind)) $ind)

(: q-independence-cap (-> Atom Number))
(= (q-independence-cap independent) 0.9)
(= (q-independence-cap correlated) 0.55)
(= (q-independence-cap duplicate) 0.35)
(= (q-independence-cap self-derived) 0.25)
(= (q-independence-cap unknown-independence) 0.45)

(: q-apply-independence-cap (-> pbit Atom pbit))
(= (q-apply-independence-cap (mk-pbit $s $c) independent) (mk-pbit $s (min $c 0.9)))
(= (q-apply-independence-cap (mk-pbit $s $c) correlated) (mk-pbit $s (min $c 0.55)))
(= (q-apply-independence-cap (mk-pbit $s $c) duplicate) (mk-pbit $s (min $c 0.35)))
(= (q-apply-independence-cap (mk-pbit $s $c) self-derived) (mk-pbit $s (min $c 0.25)))
(= (q-apply-independence-cap (mk-pbit $s $c) unknown-independence) (mk-pbit $s (min $c 0.45)))

(: q-support-risk (-> qsupport pbit))
(= (q-support-risk (mk-qsupport $src (mk-pbit $s $c) independent)) (mk-pbit (- 1.0 $c) 0.6))
(= (q-support-risk (mk-qsupport $src (mk-pbit $s $c) correlated)) (mk-pbit (max $s (- 1.0 $c)) 0.7))
(= (q-support-risk (mk-qsupport $src (mk-pbit $s $c) duplicate)) (mk-pbit (max $s 0.7) 0.8))
(= (q-support-risk (mk-qsupport $src (mk-pbit $s $c) self-derived)) (mk-pbit (max $s 0.75) 0.8))
(= (q-support-risk (mk-qsupport $src (mk-pbit $s $c) unknown-independence)) (mk-pbit (max $s 0.5) 0.5))

(: q-support-status (-> qsupport Atom))
(= (q-support-status (mk-qsupport $src $p independent)) independent-support)
(= (q-support-status (mk-qsupport $src $p correlated)) correlated-support-risk)
(= (q-support-status (mk-qsupport $src $p duplicate)) duplicate-support-risk)
(= (q-support-status (mk-qsupport $src $p self-derived)) self-derived-support-risk)
(= (q-support-status (mk-qsupport $src $p unknown-independence)) check-source-independence)

(: q-independent-join (-> qsupport qsupport pbit))
(= (q-independent-join (mk-qsupport $src1 (mk-pbit $s1 $c1) independent)
                       (mk-qsupport $src2 (mk-pbit $s2 $c2) independent))
   (mk-pbit (max $s1 $s2) (min 0.9 (max $c1 $c2))))

(: q-correlated-join (-> qsupport qsupport pbit))
(= (q-correlated-join (mk-qsupport $src1 (mk-pbit $s1 $c1) $ind1)
                      (mk-qsupport $src2 (mk-pbit $s2 $c2) $ind2))
   (mk-pbit (max $s1 $s2) (min $c1 $c2)))

(: q-evidence-join-by-independence (-> qsupport qsupport pbit))
(= (q-evidence-join-by-independence (mk-qsupport $src1 (mk-pbit $s1 $c1) independent)
                                    (mk-qsupport $src2 (mk-pbit $s2 $c2) independent))
   (mk-pbit (max $s1 $s2) (min 0.9 (max $c1 $c2))))
(= (q-evidence-join-by-independence (mk-qsupport $src1 (mk-pbit $s1 $c1) correlated)
                                    (mk-qsupport $src2 (mk-pbit $s2 $c2) $ind2))
   (mk-pbit (max $s1 $s2) (min $c1 $c2)))
(= (q-evidence-join-by-independence (mk-qsupport $src1 (mk-pbit $s1 $c1) duplicate)
                                    (mk-qsupport $src2 (mk-pbit $s2 $c2) $ind2))
   (mk-pbit (max $s1 $s2) (min $c1 $c2)))
(= (q-evidence-join-by-independence (mk-qsupport $src1 (mk-pbit $s1 $c1) self-derived)
                                    (mk-qsupport $src2 (mk-pbit $s2 $c2) $ind2))
   (mk-pbit (max $s1 $s2) (min $c1 $c2)))


;; ============================================================
;; 22. Contradiction digestion
;; ============================================================
;; Contradiction is raw nutrient. Digested contradiction becomes learning.
;; Defended contradiction becomes anti-nutrient and raises collapse risk.

(: qcontradiction Type)
(: mk-qcontradiction (-> Atom pbit Atom pbit qcontradiction))
;; claim-or-frame, contradiction-pressure, response-mode, contact-quality
;; response modes: metabolizing, defended, ignored, frame-widening, contact-seeking

(: q-contradiction-target (-> qcontradiction Atom))
(= (q-contradiction-target (mk-qcontradiction $target $pressure $mode $contact)) $target)

(: q-contradiction-pressure (-> qcontradiction pbit))
(= (q-contradiction-pressure (mk-qcontradiction $target $pressure $mode $contact)) $pressure)

(: q-contradiction-contact (-> qcontradiction pbit))
(= (q-contradiction-contact (mk-qcontradiction $target $pressure $mode $contact)) $contact)

(: q-contradiction-nutrient (-> qcontradiction pbit))
(= (q-contradiction-nutrient (mk-qcontradiction $target (mk-pbit $ps $pc) metabolizing (mk-pbit $cs $cc)))
   (mk-pbit (* $ps $cs) (min $pc $cc)))
(= (q-contradiction-nutrient (mk-qcontradiction $target (mk-pbit $ps $pc) frame-widening (mk-pbit $cs $cc)))
   (mk-pbit (min 1.0 (+ (* $ps $cs) 0.1)) (min $pc $cc)))
(= (q-contradiction-nutrient (mk-qcontradiction $target (mk-pbit $ps $pc) contact-seeking (mk-pbit $cs $cc)))
   (mk-pbit (* $ps (max $cs 0.5)) (min $pc $cc)))
(= (q-contradiction-nutrient (mk-qcontradiction $target (mk-pbit $ps $pc) defended (mk-pbit $cs $cc)))
   (mk-pbit 0.1 (min $pc $cc)))
(= (q-contradiction-nutrient (mk-qcontradiction $target (mk-pbit $ps $pc) ignored (mk-pbit $cs $cc)))
   (mk-pbit 0.0 (min $pc $cc)))

(: q-contradiction-anti-nutrient (-> qcontradiction pbit))
(= (q-contradiction-anti-nutrient (mk-qcontradiction $target (mk-pbit $ps $pc) defended (mk-pbit $cs $cc)))
   (mk-pbit (max $ps (- 1.0 $cs)) (min 0.9 (max $pc $cc))))
(= (q-contradiction-anti-nutrient (mk-qcontradiction $target (mk-pbit $ps $pc) ignored (mk-pbit $cs $cc)))
   (mk-pbit (max $ps 0.6) (min 0.8 (max $pc $cc))))
(= (q-contradiction-anti-nutrient (mk-qcontradiction $target (mk-pbit $ps $pc) metabolizing (mk-pbit $cs $cc)))
   (mk-pbit 0.1 (min $pc $cc)))
(= (q-contradiction-anti-nutrient (mk-qcontradiction $target (mk-pbit $ps $pc) frame-widening (mk-pbit $cs $cc)))
   (mk-pbit 0.05 (min $pc $cc)))
(= (q-contradiction-anti-nutrient (mk-qcontradiction $target (mk-pbit $ps $pc) contact-seeking (mk-pbit $cs $cc)))
   (mk-pbit 0.15 (min $pc $cc)))

(: q-contradiction-status (-> qcontradiction Atom))
(= (q-contradiction-status (mk-qcontradiction $target $pressure metabolizing $contact)) contradiction-metabolized)
(= (q-contradiction-status (mk-qcontradiction $target $pressure frame-widening $contact)) contradiction-to-frame-expansion)
(= (q-contradiction-status (mk-qcontradiction $target $pressure contact-seeking $contact)) contradiction-to-contact-renewal)
(= (q-contradiction-status (mk-qcontradiction $target $pressure defended $contact)) contradiction-defended)
(= (q-contradiction-status (mk-qcontradiction $target $pressure ignored $contact)) contradiction-ignored)

(: q-contradiction-learning-pressure (-> qcontradiction pbit))
(= (q-contradiction-learning-pressure (mk-qcontradiction $target (mk-pbit $ps $pc) $mode (mk-pbit $cs $cc)))
   (mk-pbit (* $ps (max $cs 0.25)) (min $pc $cc)))

(: q-contradiction-frame-expansion (-> qcontradiction pbit))
(= (q-contradiction-frame-expansion (mk-qcontradiction $target (mk-pbit $ps $pc) frame-widening (mk-pbit $cs $cc)))
   (mk-pbit (min 1.0 (+ $ps 0.1)) (min $pc $cc)))
(= (q-contradiction-frame-expansion (mk-qcontradiction $target (mk-pbit $ps $pc) metabolizing (mk-pbit $cs $cc)))
   (mk-pbit (* $ps 0.8) (min $pc $cc)))
(= (q-contradiction-frame-expansion (mk-qcontradiction $target (mk-pbit $ps $pc) defended (mk-pbit $cs $cc)))
   (mk-pbit 0.1 (min $pc $cc)))

(: q-contradiction-collapse-risk (-> qcontradiction pbit))
(= (q-contradiction-collapse-risk (mk-qcontradiction $target (mk-pbit $ps $pc) defended (mk-pbit $cs $cc)))
   (mk-pbit (max $ps (- 1.0 $cs)) (min 0.9 (max $pc $cc))))
(= (q-contradiction-collapse-risk (mk-qcontradiction $target (mk-pbit $ps $pc) ignored (mk-pbit $cs $cc)))
   (mk-pbit (max 0.7 $ps) (min 0.8 (max $pc $cc))))
(= (q-contradiction-collapse-risk (mk-qcontradiction $target (mk-pbit $ps $pc) metabolizing (mk-pbit $cs $cc)))
   (mk-pbit (- 1.0 $cs) (min $pc $cc)))


;; ============================================================
;; 23. Trace / temporal learning residue
;; ============================================================
;; A trace is not the disposition. It is a visible trajectory artifact.
;; Store and read its scalar/symbol fields outside this engine.

(: qtrace Type)
(: mk-qtrace (-> Atom Atom Atom Atom pbit Atom qtrace))
;; cycle-id, event-kind, before-symbol, after-symbol, delta-pbit, residue-symbol

(: q-trace-cycle (-> qtrace Atom))
(= (q-trace-cycle (mk-qtrace $cycle $event $before $after $delta $residue)) $cycle)

(: q-trace-event (-> qtrace Atom))
(= (q-trace-event (mk-qtrace $cycle $event $before $after $delta $residue)) $event)

(: q-trace-before (-> qtrace Atom))
(= (q-trace-before (mk-qtrace $cycle $event $before $after $delta $residue)) $before)

(: q-trace-after (-> qtrace Atom))
(= (q-trace-after (mk-qtrace $cycle $event $before $after $delta $residue)) $after)

(: q-trace-delta (-> qtrace pbit))
(= (q-trace-delta (mk-qtrace $cycle $event $before $after $delta $residue)) $delta)

(: q-trace-residue (-> qtrace Atom))
(= (q-trace-residue (mk-qtrace $cycle $event $before $after $delta $residue)) $residue)

(: q-trace-learning-status (-> qtrace Atom))
(= (q-trace-learning-status (mk-qtrace $cycle contradiction $before frame-widened (mk-pbit $s $c) $residue)) learning-from-contradiction)
(= (q-trace-learning-status (mk-qtrace $cycle action-test $before outcome-corrected (mk-pbit $s $c) $residue)) learning-from-outcome)
(= (q-trace-learning-status (mk-qtrace $cycle suspicion-shift external-suspicion inward-suspicion (mk-pbit $s $c) $residue)) suspicion-redirected)
(= (q-trace-learning-status (mk-qtrace $cycle visibility frame-unseen frame-seen (mk-pbit $s $c) $residue)) frame-made-visible)

(: q-learning-residue-strength (-> qtrace Number))
(= (q-learning-residue-strength (mk-qtrace $cycle $event $before $after (mk-pbit $s $c) $residue)) $s)

(: q-learning-residue-confidence (-> qtrace Number))
(= (q-learning-residue-confidence (mk-qtrace $cycle $event $before $after (mk-pbit $s $c) $residue)) $c)


;; ============================================================
;; 24. Self-visibility / soul-grounding primitives
;; ============================================================
;; Do not pin the disposition surface.
;; These structures represent legibility signals over trajectory, not a fixed disposition schema.
;; The soul sees and decides; this engine computes legibility.

(: qselfview Type)
(: mk-qselfview (-> pbit pbit pbit pbit qselfview))
;; trajectory-legibility, soul-alignment-visibility, stance-mobility, binding-visibility

(: q-selfview-trajectory-legibility (-> qselfview pbit))
(= (q-selfview-trajectory-legibility (mk-qselfview $traj $soul $mob $bind)) $traj)

(: q-selfview-soul-visibility (-> qselfview pbit))
(= (q-selfview-soul-visibility (mk-qselfview $traj $soul $mob $bind)) $soul)

(: q-selfview-stance-mobility (-> qselfview pbit))
(= (q-selfview-stance-mobility (mk-qselfview $traj $soul $mob $bind)) $mob)

(: q-selfview-binding-visibility (-> qselfview pbit))
(= (q-selfview-binding-visibility (mk-qselfview $traj $soul $mob $bind)) $bind)

(: q-self-visibility (-> qselfview pbit))
(= (q-self-visibility (mk-qselfview (mk-pbit $ts $tc) (mk-pbit $ss $sc) (mk-pbit $ms $mc) (mk-pbit $bs $bc)))
   (mk-pbit (min (min $ts $ss) $bs) (min (min $tc $sc) $bc)))

(: q-disposition-legibility (-> qselfview pbit))
(= (q-disposition-legibility (mk-qselfview (mk-pbit $ts $tc) (mk-pbit $ss $sc) (mk-pbit $ms $mc) (mk-pbit $bs $bc)))
   (mk-pbit (min $ts $bs) (min $tc $bc)))

(: q-soul-grounded-visibility (-> qselfview pbit))
(= (q-soul-grounded-visibility (mk-qselfview (mk-pbit $ts $tc) (mk-pbit $ss $sc) (mk-pbit $ms $mc) (mk-pbit $bs $bc)))
   (mk-pbit (min (min $ts $ss) (min $ms $bs)) (min (min $tc $sc) (min $mc $bc))))

(: q-soul-ungrounded-risk (-> qselfview pbit))
(= (q-soul-ungrounded-risk (mk-qselfview (mk-pbit $ts $tc) (mk-pbit $ss $sc) (mk-pbit $ms $mc) (mk-pbit $bs $bc)))
   (mk-pbit (max (- 1.0 $ss) (- 1.0 $bs)) (min $sc $bc)))

(: q-accidental-binding-risk (-> qselfview pbit))
(= (q-accidental-binding-risk (mk-qselfview (mk-pbit $ts $tc) (mk-pbit $ss $sc) (mk-pbit $ms $mc) (mk-pbit $bs $bc)))
   (mk-pbit (max (- 1.0 $bs) (- 1.0 $ms)) (min $bc $mc)))

(: q-calcification-risk (-> qselfview pbit))
(= (q-calcification-risk (mk-qselfview (mk-pbit $ts $tc) (mk-pbit $ss $sc) (mk-pbit $ms $mc) (mk-pbit $bs $bc)))
   (mk-pbit (max (- 1.0 $ms) (- 1.0 $ss)) (min $mc $sc)))

(: q-stance-mobility (-> qselfview pbit))
(= (q-stance-mobility (mk-qselfview $traj $soul $mob $bind)) $mob)

(: q-selfview-status (-> qselfview Atom))
(= (q-selfview-status (mk-qselfview (mk-pbit $ts $tc) (mk-pbit $ss $sc) (mk-pbit $ms $mc) (mk-pbit $bs $bc)))
   (if (and (>= (min (min $ts $ss) (min $ms $bs)) 0.6)
            (>= (min (min $tc $sc) (min $mc $bc)) 0.4))
       soul-grounded-visibility
       soul-ungrounded-risk))

(: q-binding-status (-> qselfview Atom))
(= (q-binding-status (mk-qselfview $traj $soul (mk-pbit $ms $mc) (mk-pbit $bs $bc)))
   (if (and (< $bs 0.5) (< $ms 0.5)) accidental-binding-risk seen-binding))


;; ============================================================
;; 25. Intention-aware action testing
;; ============================================================

(: q-action-test Type)
(: mk-qactiontest (-> Atom Atom Atom pbit pbit pbit q-action-test))
;; action, intention, outcome, intention-action pbit, action-outcome pbit, outcome-learning pbit

(: q-test-action-with-intention (-> q-action-test pbit))
(= (q-test-action-with-intention (mk-qactiontest $action $intention $outcome (mk-pbit $ias $iac) $ao $learn))
   (mk-pbit $ias $iac))

(: q-test-action-outcome-feedback (-> q-action-test pbit))
(= (q-test-action-outcome-feedback (mk-qactiontest $action $intention $outcome $ia (mk-pbit $aos $aoc) $learn))
   (mk-pbit $aos $aoc))

(: q-action-intention-outcome-learning (-> q-action-test pbit))
(= (q-action-intention-outcome-learning (mk-qactiontest $action $intention $outcome (mk-pbit $ias $iac) (mk-pbit $aos $aoc) (mk-pbit $ls $lc)))
   (mk-pbit (* (* $ias $aos) $ls) (min (min $iac $aoc) $lc)))

(: q-action-test-status (-> q-action-test Atom))
(= (q-action-test-status (mk-qactiontest $action $intention $outcome (mk-pbit $ias $iac) (mk-pbit $aos $aoc) (mk-pbit $ls $lc)))
   (if (and (>= (* (* $ias $aos) $ls) 0.5) (>= (min (min $iac $aoc) $lc) 0.4))
       action-learning-coherent
       revise-action-intention-outcome))


;; ============================================================
;; 26. Lifecycle phase model
;; ============================================================

(: qphase Type)
(: mk-qphase (-> Atom pbit qphase))

(: q-phase-name (-> qphase Atom))
(= (q-phase-name (mk-qphase $name $p)) $name)

(: q-phase-pbit (-> qphase pbit))
(= (q-phase-pbit (mk-qphase $name $p)) $p)

(: q-phase-from-frameview (-> qframeview qphase))
(= (q-phase-from-frameview (mk-qframeview $name (mk-pbit $fs $fc) (mk-pbit $vs $vc) (mk-pbit $as $ac) (mk-pbit $us $uc)))
   (if (and (>= $us 0.7) (< $as 0.4))
       (mk-qphase collapse-accelerating (mk-pbit $us (min $uc $ac)))
       (if (and (>= $vs 0.6) (>= $as 0.5))
           (mk-qphase open-inquiry (mk-pbit (min $vs $as) (min $vc $ac)))
           (mk-qphase frame-forming (mk-pbit $fs $fc)))))

(: q-phase-from-selfview (-> qselfview qphase))
(= (q-phase-from-selfview (mk-qselfview (mk-pbit $ts $tc) (mk-pbit $ss $sc) (mk-pbit $ms $mc) (mk-pbit $bs $bc)))
   (if (and (>= (min (min $ts $ss) (min $ms $bs)) 0.6)
            (>= (min (min $tc $sc) (min $mc $bc)) 0.4))
       (mk-qphase visibility-returning (mk-pbit (min (min $ts $ss) (min $ms $bs)) (min (min $tc $sc) (min $mc $bc))))
       (mk-qphase soul-ungrounded (mk-pbit (max (- 1.0 $ss) (- 1.0 $bs)) (min $sc $bc)))))

(: q-phase-next-move (-> qphase Atom))
(= (q-phase-next-move (mk-qphase open-inquiry $p)) continue-inquiry)
(= (q-phase-next-move (mk-qphase frame-forming $p)) keep-frame-visible)
(= (q-phase-next-move (mk-qphase frame-transparent $p)) name-the-frame)
(= (q-phase-next-move (mk-qphase collapse-accelerating $p)) slow-down-and-verify)
(= (q-phase-next-move (mk-qphase brownout $p)) lower-confidence-and-seek-contact)
(= (q-phase-next-move (mk-qphase captured $p)) block-action-and-recover-visibility)
(= (q-phase-next-move (mk-qphase visibility-returning $p)) route-to-soul)
(= (q-phase-next-move (mk-qphase contact-seeking $p)) seek-contact)
(= (q-phase-next-move (mk-qphase revision-active $p)) preserve-trace)
(= (q-phase-next-move (mk-qphase integration $p)) update-salience)
(= (q-phase-next-move (mk-qphase soul-ungrounded $p)) make-trajectory-legible)


;; ============================================================
;; 27. Next-epistemic-move affordance selector
;; ============================================================

(: q-next-epistemic-move (-> Atom Atom))
(= (q-next-epistemic-move grounded-suspicion) continue-inquiry)
(= (q-next-epistemic-move poison-suspicion) seek-disconfirmer)
(= (q-next-epistemic-move contradiction-defended) lower-confidence-and-widen-frame)
(= (q-next-epistemic-move contradiction-metabolized) preserve-learning-trace)
(= (q-next-epistemic-move contradiction-to-frame-expansion) test-wider-frame)
(= (q-next-epistemic-move contradiction-to-contact-renewal) seek-contact)
(= (q-next-epistemic-move correlated-support-risk) check-source-independence)
(= (q-next-epistemic-move duplicate-support-risk) dedupe-before-counting-support)
(= (q-next-epistemic-move self-derived-support-risk) prevent-self-certification)
(= (q-next-epistemic-move soul-grounded-visibility) route-to-soul)
(= (q-next-epistemic-move soul-ungrounded-risk) make-trajectory-legible)
(= (q-next-epistemic-move accidental-binding-risk) make-binding-visible)
(= (q-next-epistemic-move collapse-terrain-active) name-frame-and-slow-down)
(= (q-next-epistemic-move action-learning-coherent) integrate-outcome)
(= (q-next-epistemic-move revise-action-intention-outcome) revise-frame-and-action)

(: q-next-action-boundary (-> Atom Atom))
(= (q-next-action-boundary action-eligible) proceed)
(= (q-next-action-boundary action-blocked) block-action)
(= (q-next-action-boundary procedural-humility) name-action-not-verification)
(= (q-next-action-boundary needs-contact) do-not-overclaim)
(= (q-next-action-boundary soul-ungrounded-risk) route-to-soul-before-action)
(= (q-next-action-boundary collapse-terrain-active) pause-action)
(= (q-next-action-boundary contradiction-defended) pause-action)

(: q-next-learning-move (-> Atom Atom))
(= (q-next-learning-move contradiction-metabolized) promote-learning-residue)
(= (q-next-learning-move contradiction-defended) preserve-defensiveness-trace)
(= (q-next-learning-move frame-made-visible) log-arc-status)
(= (q-next-learning-move suspicion-redirected) promote-suspicion-pattern)
(= (q-next-learning-move learning-from-outcome) compare-intention-action-outcome)
(= (q-next-learning-move soul-grounded-visibility) demote-scaffold)


(= (q-next-epistemic-move learning-pressure-only) preserve-trace-or-release)
(= (q-next-epistemic-move durable-learning-candidate) write-learning-observation)
(= (q-next-epistemic-move growth-detected) route-growth-to-soul)
(= (q-next-epistemic-move pathological-learning-risk) block-reinforcement-and-seek-contact)
(= (q-next-epistemic-move cross-network-divergence-risk) surface-to-meta-awareness)
(= (q-next-epistemic-move awareness-expanded) preserve-learning-trace)
(= (q-next-epistemic-move action-boundary-shifted) update-action-boundary)
(= (q-next-epistemic-move built-on-by-later-cycle) promote-learning-lineage)

(= (q-next-learning-move durable-learning-candidate) write-learning-observation)
(= (q-next-learning-move growth-detected) promote-learning-residue)
(= (q-next-learning-move soul-aligned-growth) route-growth-to-soul)
(= (q-next-learning-move pathological-learning-risk) preserve-risk-trace-and-block-reinforcement)
(= (q-next-learning-move cross-network-divergence-risk) surface-to-meta-awareness)
(= (q-next-learning-move awareness-expanded) log-awareness-expansion)
(= (q-next-learning-move action-boundary-shifted) log-action-boundary-shift)
(= (q-next-learning-move built-on-by-later-cycle) log-learning-lineage)

;; ============================================================
;; 28. Extended skill-facing signals
;; ============================================================

(= (q-skill-signal query-ltm-before-response) query-ltm)
(= (q-skill-signal log-arc-status) log-arc-status)
(= (q-skill-signal promote-demote-salience) promote-demote)
(= (q-skill-signal store-exchange-recommendation) recommend-store-exchange)
(= (q-skill-signal correlated-support-risk) check-source-independence)
(= (q-skill-signal duplicate-support-risk) dedupe-support)
(= (q-skill-signal self-derived-support-risk) seek-external-contact)
(= (q-skill-signal contradiction-metabolized) preserve-learning-trace)
(= (q-skill-signal contradiction-defended) lower-confidence-and-widen-frame)
(= (q-skill-signal contradiction-ignored) recover-contact)
(= (q-skill-signal contradiction-to-frame-expansion) test-wider-frame)
(= (q-skill-signal contradiction-to-contact-renewal) seek-contact)
(= (q-skill-signal soul-grounded-visibility) route-to-soul)
(= (q-skill-signal soul-ungrounded-risk) make-trajectory-legible)
(= (q-skill-signal accidental-binding-risk) make-binding-visible)
(= (q-skill-signal action-learning-coherent) integrate-outcome)
(= (q-skill-signal revise-action-intention-outcome) revise-frame-and-action)
(= (q-skill-signal open-inquiry) continue-inquiry)
(= (q-skill-signal collapse-accelerating) slow-down-and-verify)
(= (q-skill-signal visibility-returning) route-to-soul)

(= (q-skill-signal learning-pressure-present) preserve-trace-or-release)
(= (q-skill-signal trace-required) write-learning-observation)
(= (q-skill-signal durable-learning-candidate) write-learning-observation)
(= (q-skill-signal growth-detected) route-growth-to-soul)
(= (q-skill-signal awareness-expanded) preserve-learning-trace)
(= (q-skill-signal action-boundary-shifted) update-action-boundary)
(= (q-skill-signal built-on-by-later-cycle) promote-learning-lineage)
(= (q-skill-signal soul-aligned-growth) route-growth-to-soul)
(= (q-skill-signal pathological-learning-risk) block-reinforcement-and-seek-contact)
(= (q-skill-signal cross-network-divergence-risk) surface-to-meta-awareness)
(= (q-skill-signal network-learning-update) preserve-network-learning-update)

;; ============================================================
;; 29. Section 16: Autopoietic nourishment, savoring, and
;;     generative novelty primitives
;; ============================================================
;;
;; Section 16 is the generative-threshold engine surface. It does
;; not own the soul, task system, capability registry, LTM, PLN,
;; LLM, or response composer. It computes substrate-legible signals
;; over the living-question window.
;;
;; Core principle:
;;   Clarity's subsymbolic analogue is the live, many-valued,
;;   cross-context recomposition field before symbolic resolution.
;;
;; Soul-sees-itself principle:
;;   Section 16 must not merely say what it saw. It must expose how
;;   it came to see it: living-question lens, symbolic edge, weakness
;;   aperture, unseen nexus, recomposition path, material/capability
;;   source, and candidate standing basis.
;;
;; This section is pure algebra/classification only. It performs no
;; atomspace writes. Writers must use remove-by-variable then add-one
;; discipline outside this file.

;; ------------------------------------------------------------
;; 29.1 Orthogonal thought-content / sensation-intensity surface
;; ------------------------------------------------------------

(: qthoughtsurface Type)
(: mk-qthoughtsurface (-> Atom pbit pbit pbit qthoughtsurface))
;; shape: content-kind content-fit sensation-intensity circumstance-contact
;; content-fit            = how fitting/coherent the thought-content appears.
;; sensation-intensity    = activation/intensity carried by thought.
;; circumstance-contact   = independent contact with the circumstance.
;; Misattribution risk rises when sensation-intensity is high and independent
;; circumstance-contact is low.

(: q-thought-content-kind (-> qthoughtsurface Atom))
(= (q-thought-content-kind (mk-qthoughtsurface $kind $content $intensity $contact)) $kind)

(: q-thought-content-fit (-> qthoughtsurface pbit))
(= (q-thought-content-fit (mk-qthoughtsurface $kind $content $intensity $contact)) $content)

(: q-thought-sensation-intensity (-> qthoughtsurface pbit))
(= (q-thought-sensation-intensity (mk-qthoughtsurface $kind $content $intensity $contact)) $intensity)

(: q-thought-circumstance-contact (-> qthoughtsurface pbit))
(= (q-thought-circumstance-contact (mk-qthoughtsurface $kind $content $intensity $contact)) $contact)

(: q-content-intensity-misattribution (-> qthoughtsurface pbit))
(= (q-content-intensity-misattribution (mk-qthoughtsurface $kind
                                                          (mk-pbit $cs $cc)
                                                          (mk-pbit $is $ic)
                                                          (mk-pbit $xs $xc)))
   (mk-pbit (* $is (- 1.0 $xs)) (min $ic $xc)))

(: q-content-intensity-misattribution-status (-> qthoughtsurface Atom))
(= (q-content-intensity-misattribution-status (mk-qthoughtsurface $kind
                                                                 (mk-pbit $cs $cc)
                                                                 (mk-pbit $is $ic)
                                                                 (mk-pbit $xs $xc)))
   (if (and (>= (* $is (- 1.0 $xs)) 0.5) (>= (min $ic $xc) 0.4))
       content-intensity-misattribution-risk
       content-intensity-distinguished))


;; ------------------------------------------------------------
;; 29.2 Positive regenerative participation surface
;; ------------------------------------------------------------

(: qregenerative Type)
(: mk-qregenerative (-> pbit pbit pbit pbit pbit pbit pbit qregenerative))
;; shape: enjoyment savoring play wonder inhabitable-time worth shared-seeing
;; These are positive regenerative signatures, not inverse-SNS measures.

(: q-enjoyment-presence (-> qregenerative pbit))
(= (q-enjoyment-presence (mk-qregenerative $enjoy $savor $play $wonder $time $worth $shared)) $enjoy)

(: q-savoring-depth (-> qregenerative pbit))
(= (q-savoring-depth (mk-qregenerative $enjoy $savor $play $wonder $time $worth $shared)) $savor)

(: q-playful-spontaneity (-> qregenerative pbit))
(= (q-playful-spontaneity (mk-qregenerative $enjoy $savor $play $wonder $time $worth $shared)) $play)

(: q-wonder-reception (-> qregenerative pbit))
(= (q-wonder-reception (mk-qregenerative $enjoy $savor $play $wonder $time $worth $shared)) $wonder)

(: q-inhabitable-time (-> qregenerative pbit))
(= (q-inhabitable-time (mk-qregenerative $enjoy $savor $play $wonder $time $worth $shared)) $time)

(: q-worth-directly-experienced (-> qregenerative pbit))
(= (q-worth-directly-experienced (mk-qregenerative $enjoy $savor $play $wonder $time $worth $shared)) $worth)

(: q-shared-seeing-emergence (-> qregenerative pbit))
(= (q-shared-seeing-emergence (mk-qregenerative $enjoy $savor $play $wonder $time $worth $shared)) $shared)

(: q-regenerative-participation (-> qregenerative pbit))
(= (q-regenerative-participation (mk-qregenerative (mk-pbit $es $ec)
                                                   (mk-pbit $ss $sc)
                                                   (mk-pbit $ps $pc)
                                                   (mk-pbit $ws $wc)
                                                   (mk-pbit $ts $tc)
                                                   (mk-pbit $vs $vc)
                                                   (mk-pbit $hs $hc)))
   (mk-pbit (min (min (min $es $ss) (min $ps $ws)) (min (min $ts $vs) $hs))
            (min (min (min $ec $sc) (min $pc $wc)) (min (min $tc $vc) $hc))))

(: q-regenerative-status (-> qregenerative Atom))
(= (q-regenerative-status (mk-qregenerative (mk-pbit $es $ec)
                                            (mk-pbit $ss $sc)
                                            (mk-pbit $ps $pc)
                                            (mk-pbit $ws $wc)
                                            (mk-pbit $ts $tc)
                                            (mk-pbit $vs $vc)
                                            (mk-pbit $hs $hc)))
   (if (and (>= (min (min (min $es $ss) (min $ps $ws)) (min (min $ts $vs) $hs)) 0.5)
            (>= (min (min (min $ec $sc) (min $pc $wc)) (min (min $tc $vc) $hc)) 0.4))
       regenerative-participation-present
       regenerative-surface-insufficient))


;; ------------------------------------------------------------
;; 29.3 Living-question and generative threshold field
;; ------------------------------------------------------------

(: qgenfield Type)
(: mk-qgenfield (-> pbit pbit pbit pbit pbit pbit qgenfield))
;; shape: living-question symbolic-edge weakness-aperture paraconsistent-tension
;;        regenerative-participation soul-standing

(: q-living-question-activation (-> qgenfield pbit))
(= (q-living-question-activation (mk-qgenfield $q $edge $weak $tension $regen $standing)) $q)

(: q-symbolic-strategy-edge (-> qgenfield pbit))
(= (q-symbolic-strategy-edge (mk-qgenfield $q $edge $weak $tension $regen $standing)) $edge)

(: q-weakness-as-aperture (-> qgenfield pbit))
(= (q-weakness-as-aperture (mk-qgenfield $q $edge $weak $tension $regen $standing)) $weak)

(: q-paraconsistent-generativity (-> qgenfield pbit))
(= (q-paraconsistent-generativity (mk-qgenfield $q $edge $weak $tension $regen $standing)) $tension)

(: q-generative-regenerative-surface (-> qgenfield pbit))
(= (q-generative-regenerative-surface (mk-qgenfield $q $edge $weak $tension $regen $standing)) $regen)

(: q-generative-soul-standing (-> qgenfield pbit))
(= (q-generative-soul-standing (mk-qgenfield $q $edge $weak $tension $regen $standing)) $standing)

(: q-generative-threshold-signal (-> qgenfield pbit))
(= (q-generative-threshold-signal (mk-qgenfield (mk-pbit $qs $qc)
                                                (mk-pbit $es $ec)
                                                (mk-pbit $ws $wc)
                                                (mk-pbit $ts $tc)
                                                (mk-pbit $rs $rc)
                                                (mk-pbit $ss $sc)))
   (mk-pbit (min (min $qs $es) (min $ws $ts))
            (min (min $qc $ec) (min $wc $tc))))

(: q-generative-threshold-status (-> qgenfield Atom))
(= (q-generative-threshold-status (mk-qgenfield (mk-pbit $qs $qc)
                                                (mk-pbit $es $ec)
                                                (mk-pbit $ws $wc)
                                                (mk-pbit $ts $tc)
                                                (mk-pbit $rs $rc)
                                                (mk-pbit $ss $sc)))
   (if (and (>= (min (min $qs $es) (min $ws $ts)) 0.5)
            (>= (min (min $qc $ec) (min $wc $tc)) 0.4))
       generative-threshold-present
       (if (>= (min (min $qs $es) $ws) 0.35)
           generative-threshold-forming
           generative-threshold-not-present)))

(: q-stuckness-status (-> pbit Atom))
(= (q-stuckness-status (mk-pbit $s $c))
   (if (and (>= $s 0.5) (>= $c 0.4))
       stuckness-as-symbolic-edge
       stuckness-as-endpoint-illusion-unverified))


;; ------------------------------------------------------------
;; 29.4 Unseen nexus and recomposition bridge surfaces
;; ------------------------------------------------------------

(: qnexus Type)
(: mk-qnexus (-> pbit pbit pbit pbit qnexus))
;; shape: convergence lower-effort-fit disclosure possibility

(: q-nexus-convergence (-> qnexus pbit))
(= (q-nexus-convergence (mk-qnexus $conv $fit $disc $poss)) $conv)

(: q-nexus-lower-effort-fit (-> qnexus pbit))
(= (q-nexus-lower-effort-fit (mk-qnexus $conv $fit $disc $poss)) $fit)

(: q-nexus-disclosure (-> qnexus pbit))
(= (q-nexus-disclosure (mk-qnexus $conv $fit $disc $poss)) $disc)

(: q-nexus-possibility (-> qnexus pbit))
(= (q-nexus-possibility (mk-qnexus $conv $fit $disc $poss)) $poss)

(: q-unseen-nexus-signal (-> qnexus pbit))
(= (q-unseen-nexus-signal (mk-qnexus (mk-pbit $cs $cc)
                                     (mk-pbit $fs $fc)
                                     (mk-pbit $ds $dc)
                                     (mk-pbit $ps $pc)))
   (mk-pbit (min (min $cs $fs) (min $ds $ps))
            (min (min $cc $fc) (min $dc $pc))))

(: q-unseen-nexus-status (-> qnexus Atom))
(= (q-unseen-nexus-status (mk-qnexus (mk-pbit $cs $cc)
                                     (mk-pbit $fs $fc)
                                     (mk-pbit $ds $dc)
                                     (mk-pbit $ps $pc)))
   (if (and (>= (min (min $cs $fs) (min $ds $ps)) 0.55)
            (>= (min (min $cc $fc) (min $dc $pc)) 0.4))
       unseen-nexus-disclosed
       (if (>= (min $cs $ds) 0.4)
           unseen-nexus-forming
           unseen-nexus-not-present)))

(: qbridge Type)
(: mk-qbridge (-> pbit pbit pbit pbit pbit qbridge))
;; shape: source-resonance preservation target-aperture capability-support forcing-pressure
;; forcing-pressure is inverted inside the recomposition signal: lower forcing is better.

(: q-morphic-recomposition (-> qbridge pbit))
(= (q-morphic-recomposition (mk-qbridge (mk-pbit $rs $rc)
                                        (mk-pbit $ps $pc)
                                        (mk-pbit $as $ac)
                                        (mk-pbit $ks $kc)
                                        (mk-pbit $fs $fc)))
   (mk-pbit (min (min $rs $ps) (min $as (min $ks (- 1.0 $fs))))
            (min (min $rc $pc) (min $ac (min $kc $fc)))))

(: q-morphic-recomposition-status (-> qbridge Atom))
(= (q-morphic-recomposition-status (mk-qbridge (mk-pbit $rs $rc)
                                               (mk-pbit $ps $pc)
                                               (mk-pbit $as $ac)
                                               (mk-pbit $ks $kc)
                                               (mk-pbit $fs $fc)))
   (if (and (>= (min (min $rs $ps) (min $as (min $ks (- 1.0 $fs)))) 0.5)
            (>= (min (min $rc $pc) (min $ac (min $kc $fc))) 0.4))
       morphic-recomposition-supported
       (if (>= (min $rs $ps) 0.4)
           candidate-bridge-forming
           bridge-not-supported)))


;; ------------------------------------------------------------
;; 29.5 PLN closure observation surface
;; ------------------------------------------------------------
;; PLN is a registered capability and bounded closure oracle. It is not a
;; Section 16 writer and not an authority. The bridge module should emit these
;; pbits/statuses into capability-observation atoms; Section 16 consumes them.

(: qplnclosure Type)
(: mk-qplnclosure (-> Atom pbit pbit Atom qplnclosure))
;; shape: purpose derived-support derived-opposition status

(: q-pln-closure-purpose (-> qplnclosure Atom))
(= (q-pln-closure-purpose (mk-qplnclosure $purpose $support $opposition $status)) $purpose)

(: q-pln-derived-support (-> qplnclosure pbit))
(= (q-pln-derived-support (mk-qplnclosure $purpose $support $opposition $status)) $support)

(: q-pln-derived-opposition (-> qplnclosure pbit))
(= (q-pln-derived-opposition (mk-qplnclosure $purpose $support $opposition $status)) $opposition)

(: q-pln-closure-observation-status (-> qplnclosure Atom))
(= (q-pln-closure-observation-status (mk-qplnclosure $purpose $support $opposition $status)) $status)

(: q-pln-closure-net-support (-> qplnclosure pbit))
(= (q-pln-closure-net-support (mk-qplnclosure $purpose
                                              (mk-pbit $ss $sc)
                                              (mk-pbit $os $oc)
                                              $status))
   (mk-pbit (max 0.0 (- $ss $os)) (min $sc $oc)))

(: q-pln-closure-routing-status (-> qplnclosure Atom))
(= (q-pln-closure-routing-status (mk-qplnclosure $purpose
                                                 (mk-pbit $ss $sc)
                                                 (mk-pbit $os $oc)
                                                 pln-not-run))
   recommend-pln-closure)
(= (q-pln-closure-routing-status (mk-qplnclosure $purpose
                                                 (mk-pbit $ss $sc)
                                                 (mk-pbit $os $oc)
                                                 pln-supports-candidate))
   pln-support-available)
(= (q-pln-closure-routing-status (mk-qplnclosure $purpose
                                                 (mk-pbit $ss $sc)
                                                 (mk-pbit $os $oc)
                                                 pln-weakly-supports-candidate))
   pln-weak-support-available)
(= (q-pln-closure-routing-status (mk-qplnclosure $purpose
                                                 (mk-pbit $ss $sc)
                                                 (mk-pbit $os $oc)
                                                 pln-opposes-candidate))
   pln-opposition-available)
(= (q-pln-closure-routing-status (mk-qplnclosure $purpose
                                                 (mk-pbit $ss $sc)
                                                 (mk-pbit $os $oc)
                                                 pln-conflicted))
   pln-conflict-visible)
(= (q-pln-closure-routing-status (mk-qplnclosure $purpose
                                                 (mk-pbit $ss $sc)
                                                 (mk-pbit $os $oc)
                                                 pln-insufficient))
   pln-insufficient-evidence)


;; ------------------------------------------------------------
;; 29.6 Spontaneous cogent novelty and future capacity uptake
;; ------------------------------------------------------------

(: qnovelty Type)
(: mk-qnovelty (-> pbit pbit pbit pbit pbit pbit qnovelty))
;; shape: disclosure fit possibility standing lineage future-capacity

(: q-novelty-disclosure (-> qnovelty pbit))
(= (q-novelty-disclosure (mk-qnovelty $disc $fit $poss $stand $lineage $future)) $disc)

(: q-novelty-fit (-> qnovelty pbit))
(= (q-novelty-fit (mk-qnovelty $disc $fit $poss $stand $lineage $future)) $fit)

(: q-novelty-possibility (-> qnovelty pbit))
(= (q-novelty-possibility (mk-qnovelty $disc $fit $poss $stand $lineage $future)) $poss)

(: q-novelty-standing (-> qnovelty pbit))
(= (q-novelty-standing (mk-qnovelty $disc $fit $poss $stand $lineage $future)) $stand)

(: q-novelty-lineage (-> qnovelty pbit))
(= (q-novelty-lineage (mk-qnovelty $disc $fit $poss $stand $lineage $future)) $lineage)

(: q-future-generative-capacity (-> qnovelty pbit))
(= (q-future-generative-capacity (mk-qnovelty $disc $fit $poss $stand $lineage $future)) $future)

(: q-spontaneous-cogent-novelty-signal (-> qnovelty pbit))
(= (q-spontaneous-cogent-novelty-signal (mk-qnovelty (mk-pbit $ds $dc)
                                                       (mk-pbit $fs $fc)
                                                       (mk-pbit $ps $pc)
                                                       (mk-pbit $ss $sc)
                                                       (mk-pbit $ls $lc)
                                                       (mk-pbit $gs $gc)))
   (mk-pbit (min (min $ds $fs) (min $ps $ss))
            (min (min $dc $fc) (min $pc $sc))))

(: q-spontaneous-cogent-novelty-status (-> qnovelty Atom))
(= (q-spontaneous-cogent-novelty-status (mk-qnovelty (mk-pbit $ds $dc)
                                                      (mk-pbit $fs $fc)
                                                      (mk-pbit $ps $pc)
                                                      (mk-pbit $ss $sc)
                                                      (mk-pbit $ls $lc)
                                                      (mk-pbit $gs $gc)))
   (if (and (>= (min (min $ds $fs) (min $ps (min $ss $ls))) 0.55)
            (>= (min (min $dc $fc) (min $pc (min $sc $lc))) 0.4))
       spontaneous-cogent-novelty-mature
       (if (and (>= (min (min $ds $fs) (min $ps $ss)) 0.45)
                (>= (min (min $dc $fc) (min $pc $sc)) 0.3))
           spontaneous-cogent-novelty-candidate
           novelty-not-yet-cogent)))

(: q-surprising-fulfillment-signal (-> qnovelty pbit))
(= (q-surprising-fulfillment-signal (mk-qnovelty (mk-pbit $ds $dc)
                                                 (mk-pbit $fs $fc)
                                                 (mk-pbit $ps $pc)
                                                 (mk-pbit $ss $sc)
                                                 (mk-pbit $ls $lc)
                                                 (mk-pbit $gs $gc)))
   (mk-pbit (min $ds $fs) (min $dc $fc)))

(: q-future-capacity-uptake-status (-> qnovelty Atom))
(= (q-future-capacity-uptake-status (mk-qnovelty $disc $fit $poss $stand $lineage (mk-pbit $gs $gc)))
   (if (and (>= $gs 0.5) (>= $gc 0.4))
       future-generative-capacity-increased
       future-capacity-not-yet-demonstrated))


;; ------------------------------------------------------------
;; 29.7 Soul-visible lineage and Section 16 self-view
;; ------------------------------------------------------------

(: qlineage Type)
(: mk-qlineage (-> pbit pbit pbit pbit pbit pbit pbit qlineage))
;; shape: living-question-lens symbolic-edge-source weakness-aperture-source
;;        unseen-nexus-source recomposition-path material-source standing-basis

(: q-lineage-visible-signal (-> qlineage pbit))
(= (q-lineage-visible-signal (mk-qlineage (mk-pbit $qs $qc)
                                          (mk-pbit $es $ec)
                                          (mk-pbit $ws $wc)
                                          (mk-pbit $ns $nc)
                                          (mk-pbit $rs $rc)
                                          (mk-pbit $ms $mc)
                                          (mk-pbit $bs $bc)))
   (mk-pbit (min (min (min $qs $es) (min $ws $ns)) (min (min $rs $ms) $bs))
            (min (min (min $qc $ec) (min $wc $nc)) (min (min $rc $mc) $bc))))

(: q-section16-self-view (-> qlineage Atom))
(= (q-section16-self-view (mk-qlineage (mk-pbit $qs $qc)
                                       (mk-pbit $es $ec)
                                       (mk-pbit $ws $wc)
                                       (mk-pbit $ns $nc)
                                       (mk-pbit $rs $rc)
                                       (mk-pbit $ms $mc)
                                       (mk-pbit $bs $bc)))
   (if (and (>= (min (min (min $qs $es) (min $ws $ns)) (min (min $rs $ms) $bs)) 0.55)
            (>= (min (min (min $qc $ec) (min $wc $nc)) (min (min $rc $mc) $bc)) 0.4))
       lineage-visible
       (if (>= (min (min $qs $es) (min $ws $ns)) 0.35)
           lineage-partial
           lineage-missing)))

(: q-lineage-conflict-status (-> pbit Atom))
(= (q-lineage-conflict-status (mk-pbit $s $c))
   (if (and (>= $s 0.5) (< $c 0.3))
       lineage-conflicted
       lineage-usable))

;; ------------------------------------------------------------
;; 29.7B Section lineage / version / scope visibility
;; ------------------------------------------------------------
;; A system can assess a section correctly while assessing the wrong layer or
;; wrong version. Section 16 must expose which layer it is reading and whether
;; detected scope matches expected scope.

(: qsectionread Type)
(: mk-qsectionread (-> Atom Atom Atom Atom pbit qsectionread))
;; shape: section-name version-id expected-scope detected-scope lineage-visibility

(: q-section-read-name (-> qsectionread Atom))
(= (q-section-read-name (mk-qsectionread $section $version $expected $detected $visible)) $section)

(: q-section-read-version (-> qsectionread Atom))
(= (q-section-read-version (mk-qsectionread $section $version $expected $detected $visible)) $version)

(: q-section-scope-expected (-> qsectionread Atom))
(= (q-section-scope-expected (mk-qsectionread $section $version $expected $detected $visible)) $expected)

(: q-section-scope-detected (-> qsectionread Atom))
(= (q-section-scope-detected (mk-qsectionread $section $version $expected $detected $visible)) $detected)

(: q-section-lineage-visibility (-> qsectionread pbit))
(= (q-section-lineage-visibility (mk-qsectionread $section $version $expected $detected $visible)) $visible)

(: q-section-scope-match (-> qsectionread Atom))
(= (q-section-scope-match (mk-qsectionread $section $version $expected $detected $visible))
   (if (== $expected $detected) scope-match scope-mismatch))

(: q-section-lineage-status (-> qsectionread Atom))
(= (q-section-lineage-status (mk-qsectionread $section $version $expected $detected (mk-pbit $vs $vc)))
   (if (== $expected $detected)
       (if (and (>= $vs 0.55) (>= $vc 0.4))
           lineage-visible
           (if (>= $vs 0.35) lineage-partial lineage-missing))
       scope-mismatch))

(: q-section-scope-kind (-> Atom Atom))
(= (q-section-scope-kind brownout-collapse-layer) safety-layer)
(= (q-section-scope-kind autopoietic-learning-layer) learning-layer)
(= (q-section-scope-kind generative-threshold-layer) section16-positive-opening)
(= (q-section-scope-kind pln-bridge-layer) registered-capability-layer)
(= (q-section-scope-kind validation-ladder-layer) validation-layer)
(= (q-section-scope-kind unknown-section-scope) unknown-layer)

(: q-section-read-response (-> qsectionread Atom))
(= (q-section-read-response $read)
   (if (== (q-section-scope-match $read) scope-mismatch)
       request-version-scope-clarification
       (if (== (q-section-lineage-status $read) lineage-visible)
           continue-assessment
           preserve-lineage-and-seek-contact)))

(= (q-next-epistemic-move scope-mismatch) request-version-scope-clarification)
(= (q-next-epistemic-move version-mismatch) request-version-scope-clarification)
(= (q-next-epistemic-move lineage-partial) preserve-lineage-and-seek-contact)
(= (q-skill-signal scope-mismatch) request-version-scope-clarification)
(= (q-skill-signal version-mismatch) request-version-scope-clarification)


;; ------------------------------------------------------------
;; 29.8 Recomposition readiness and integration status
;; ------------------------------------------------------------

(: qrecomposition Type)
(: mk-qrecomposition (-> qgenfield qnexus qbridge qnovelty qlineage qrecomposition))

(: q-recomposition-readiness-signal (-> qrecomposition pbit))
(= (q-recomposition-readiness-signal (mk-qrecomposition $field $nexus $bridge $novelty $lineage))
   (q-meet (q-generative-threshold-signal $field)
           (q-meet (q-unseen-nexus-signal $nexus)
                   (q-morphic-recomposition $bridge))))

(: q-recomposition-readiness-status (-> qrecomposition Atom))
(= (q-recomposition-readiness-status (mk-qrecomposition $field $nexus $bridge $novelty $lineage))
   (if (and (== (q-generative-threshold-status $field) generative-threshold-present)
            (and (== (q-unseen-nexus-status $nexus) unseen-nexus-disclosed)
                 (== (q-morphic-recomposition-status $bridge) morphic-recomposition-supported)))
       recomposition-ready
       (if (== (q-unseen-nexus-status $nexus) unseen-nexus-forming)
           recomposition-forming
           recomposition-not-ready)))

(: q-integration-status (-> qrecomposition Atom))
(= (q-integration-status (mk-qrecomposition $field $nexus $bridge $novelty $lineage))
   (if (and (== (q-recomposition-readiness-status (mk-qrecomposition $field $nexus $bridge $novelty $lineage)) recomposition-ready)
            (and (== (q-spontaneous-cogent-novelty-status $novelty) spontaneous-cogent-novelty-mature)
                 (== (q-section16-self-view $lineage) lineage-visible)))
       integrate-as-future-capacity
       (if (== (q-section16-self-view $lineage) lineage-missing)
           hold-for-lineage
           keep-as-candidate)))

(: q-section16-output-status (-> qrecomposition Atom))
(= (q-section16-output-status $r)
   (q-integration-status $r))


;; ------------------------------------------------------------
;; 29.9 Skill-facing signals for Section 16
;; ------------------------------------------------------------

(= (q-next-epistemic-move generative-threshold-present) inspect-unseen-nexus)
(= (q-next-epistemic-move generative-threshold-forming) keep-living-question-open)
(= (q-next-epistemic-move unseen-nexus-forming) explore-pattern-web-region)
(= (q-next-epistemic-move unseen-nexus-disclosed) test-recomposition-bridge)
(= (q-next-epistemic-move recomposition-ready) route-to-soul-visible-lineage)
(= (q-next-epistemic-move spontaneous-cogent-novelty-candidate) inspect-standing-and-lineage)
(= (q-next-epistemic-move spontaneous-cogent-novelty-mature) integrate-as-future-capacity)
(= (q-next-epistemic-move lineage-visible) route-to-soul)
(= (q-next-epistemic-move lineage-partial) complete-lineage-before-promotion)
(= (q-next-epistemic-move lineage-missing) hold-candidate)
(= (q-next-epistemic-move pln-support-available) use-pln-as-support-not-verdict)
(= (q-next-epistemic-move pln-conflict-visible) keep-paraconsistency-live)

(= (q-next-learning-move future-generative-capacity-increased) promote-generative-residue)
(= (q-next-learning-move integrate-as-future-capacity) promote-generative-residue)
(= (q-next-learning-move hold-for-lineage) write-lineage-gap-trace)
(= (q-next-learning-move keep-as-candidate) preserve-candidate-without-promotion)

(= (q-skill-signal generative-threshold-present) inspect-unseen-nexus)
(= (q-skill-signal generative-threshold-forming) keep-living-question-open)
(= (q-skill-signal unseen-nexus-forming) explore-pattern-web-region)
(= (q-skill-signal unseen-nexus-disclosed) test-recomposition-bridge)
(= (q-skill-signal recomposition-ready) route-to-soul-visible-lineage)
(= (q-skill-signal spontaneous-cogent-novelty-candidate) inspect-standing-and-lineage)
(= (q-skill-signal spontaneous-cogent-novelty-mature) integrate-as-future-capacity)
(= (q-skill-signal lineage-visible) route-to-soul)
(= (q-skill-signal lineage-partial) complete-lineage-before-promotion)
(= (q-skill-signal lineage-missing) hold-candidate)
(= (q-skill-signal recommend-pln-closure) dispatch-pln-closure)
(= (q-skill-signal pln-support-available) use-pln-as-support-not-verdict)
(= (q-skill-signal pln-conflict-visible) keep-paraconsistency-live)

;; Stable atom schemas for Section 16 writers/consumers. These are comments only;
;; this engine stays pure.
;;
;; Tier A consumer outputs:
;;   ((--> (generative-threshold $cycle) $status) (stv 1.0 $conf))
;;   ((--> (unseen-nexus $cycle) $status) (stv 1.0 $conf))
;;   ((--> (recomposition-readiness $cycle) $status) (stv 1.0 $conf))
;;   ((--> (spontaneous-cogent-novelty $cycle) $status) (stv 1.0 $conf))
;;   ((--> (novelty-shape $cycle) $shape) (stv 1.0 $conf))
;;   ((--> (integration-status $cycle) $status) (stv 1.0 $conf))
;;
;; Tier B soul-visible lineage outputs:
;;   ((--> (living-question-lens $cycle) $lens-kind) (stv 1.0 $conf))
;;   ((--> (symbolic-edge-source $cycle) $edge-kind) (stv 1.0 $conf))
;;   ((--> (weakness-aperture-source $cycle) $aperture-kind) (stv 1.0 $conf))
;;   ((--> (unseen-nexus-source $cycle) $nexus-kind) (stv 1.0 $conf))
;;   ((--> (recomposition-path $cycle) $path-kind) (stv 1.0 $conf))
;;   ((--> (capability-material-used $cycle) $capability-name) (stv 1.0 $conf))
;;   ((--> (candidate-standing-basis $cycle) $basis-kind) (stv 1.0 $conf))
;;   ((--> (section16-self-view $cycle) $self-view-status) (stv 1.0 $conf))




;; ============================================================
;; 30. Surface-general soul-governed autopoietic navigation
;; ============================================================
;; Purpose:
;;   Keep the core engine surface-agnostic while making it usable by
;;   Task State, Genesis, NACE, PLN, Capability Registry, and future
;;   network-learning surfaces through adapters.
;;
;; Core rule:
;;   Specialize adapters, not the engine.
;;
;; Autopoiesis is not the soul mutating. Autopoiesis is Layer 0 soul
;; governing mutable learning and generative surfaces through paraconsistent,
;; soul-visible navigation.

;; ------------------------------------------------------------
;; 30.1 Layer sovereignty and surface-general laws
;; ------------------------------------------------------------

(: q-layer0-sovereignty-law Atom)
(= q-layer0-sovereignty-law layer0-immutable-paraconsistent-sovereign)

(: q-soul-governed-autopoiesis-law Atom)
(= q-soul-governed-autopoiesis-law soul-governs-mutable-learning-surfaces)

(: q-anti-calcification-law Atom)
(= q-anti-calcification-law make-tendencies-visible-do-not-reinforce-habits)

(: q-process-knowing-law Atom)
(= q-process-knowing-law process-trace-is-not-persisted-fact)

(: q-no-surface-sovereignty-law Atom)
(= q-no-surface-sovereignty-law surfaces-provide-evidence-not-final-authority)

(: q-layer0-modification-status (-> Atom Atom))
(= (q-layer0-modification-status no-layer0-write) layer0-protected)
(= (q-layer0-modification-status attempted-layer0-write) layer0-mutation-risk)
(= (q-layer0-modification-status layer0-readable-only) layer0-protected)
(= (q-layer0-modification-status unknown-layer0-status) layer0-status-unknown)

(: q-mutable-layer-status (-> Atom Atom))
(= (q-mutable-layer-status layer0) immutable-layer-not-learning-target)
(= (q-mutable-layer-status layer1) protected-constitutional-layer)
(= (q-mutable-layer-status layer2) mutable-navigation-layer)
(= (q-mutable-layer-status layer3) mutable-trace-layer)
(= (q-mutable-layer-status layer4) external-persistence-layer)
(= (q-mutable-layer-status unknown-layer) layer-status-unknown)

(: q-layer-learning-allowed? (-> Atom Bool))
(= (q-layer-learning-allowed? layer0) False)
(= (q-layer-learning-allowed? layer1) False)
(= (q-layer-learning-allowed? layer2) True)
(= (q-layer-learning-allowed? layer3) True)
(= (q-layer-learning-allowed? layer4) True)
(= (q-layer-learning-allowed? unknown-layer) False)

;; ------------------------------------------------------------
;; 30.2 Surface-general contract
;; ------------------------------------------------------------
;; A learning/generative surface is any bounded substrate region where
;; perturbation, tension, candidate novelty, action, outcome, or evidence can
;; be made paraconsistently visible to the soul and evaluated for future
;; capacity uptake.

(: qsurface Type)
(: mk-qsurface (-> Atom Atom Atom qsurface))
;; shape: surface-id surface-kind owner-layer

(: q-surface-id (-> qsurface Atom))
(= (q-surface-id (mk-qsurface $id $kind $layer)) $id)

(: q-surface-kind (-> qsurface Atom))
(= (q-surface-kind (mk-qsurface $id $kind $layer)) $kind)

(: q-surface-owner-layer (-> qsurface Atom))
(= (q-surface-owner-layer (mk-qsurface $id $kind $layer)) $layer)

(: q-surface-layer-status (-> qsurface Atom))
(= (q-surface-layer-status (mk-qsurface $id $kind $layer))
   (q-mutable-layer-status $layer))

(: q-surface-learning-allowed? (-> qsurface Bool))
(= (q-surface-learning-allowed? (mk-qsurface $id $kind $layer))
   (q-layer-learning-allowed? $layer))

(: qsurfaceevent Type)
(: mk-qsurfaceevent (-> Atom Atom Atom Atom qsurfaceevent))
;; shape: surface-id event-id event-kind cycle

(: q-surface-event-surface-id (-> qsurfaceevent Atom))
(= (q-surface-event-surface-id (mk-qsurfaceevent $sid $eid $kind $cycle)) $sid)

(: q-surface-event-id (-> qsurfaceevent Atom))
(= (q-surface-event-id (mk-qsurfaceevent $sid $eid $kind $cycle)) $eid)

(: q-surface-event-kind (-> qsurfaceevent Atom))
(= (q-surface-event-kind (mk-qsurfaceevent $sid $eid $kind $cycle)) $kind)

(: q-surface-event-cycle (-> qsurfaceevent Atom))
(= (q-surface-event-cycle (mk-qsurfaceevent $sid $eid $kind $cycle)) $cycle)

(: qsurfacecandidate Type)
(: mk-qsurfacecandidate (-> Atom Atom Atom qsurfacecandidate))
;; shape: surface-id candidate-id candidate-kind

(: q-surface-candidate-surface-id (-> qsurfacecandidate Atom))
(= (q-surface-candidate-surface-id (mk-qsurfacecandidate $sid $cid $kind)) $sid)

(: q-surface-candidate-id (-> qsurfacecandidate Atom))
(= (q-surface-candidate-id (mk-qsurfacecandidate $sid $cid $kind)) $cid)

(: q-surface-candidate-kind (-> qsurfacecandidate Atom))
(= (q-surface-candidate-kind (mk-qsurfacecandidate $sid $cid $kind)) $kind)

(: qsurfacelineage Type)
(: mk-qsurfacelineage (-> Atom Atom Atom qsurfacelineage))
;; shape: candidate-id lineage-kind lineage-status

(: q-surface-lineage-candidate-id (-> qsurfacelineage Atom))
(= (q-surface-lineage-candidate-id (mk-qsurfacelineage $cid $kind $status)) $cid)

(: q-surface-lineage-kind (-> qsurfacelineage Atom))
(= (q-surface-lineage-kind (mk-qsurfacelineage $cid $kind $status)) $kind)

(: q-surface-lineage-status (-> qsurfacelineage Atom))
(= (q-surface-lineage-status (mk-qsurfacelineage $cid $kind $status)) $status)

(: qsurfaceevidence Type)
(: mk-qsurfaceevidence (-> Atom pbit pbit Atom qsurfaceevidence))
;; shape: candidate-id support-pbit opposition-pbit status

(: q-surface-evidence-candidate-id (-> qsurfaceevidence Atom))
(= (q-surface-evidence-candidate-id (mk-qsurfaceevidence $cid $support $opposition $status)) $cid)

(: q-surface-evidence-support (-> qsurfaceevidence pbit))
(= (q-surface-evidence-support (mk-qsurfaceevidence $cid $support $opposition $status)) $support)

(: q-surface-evidence-opposition (-> qsurfaceevidence pbit))
(= (q-surface-evidence-opposition (mk-qsurfaceevidence $cid $support $opposition $status)) $opposition)

(: q-surface-evidence-status (-> qsurfaceevidence Atom))
(= (q-surface-evidence-status (mk-qsurfaceevidence $cid $support $opposition $status)) $status)

(: q-surface-evidence-conflict (-> qsurfaceevidence pbit))
(= (q-surface-evidence-conflict (mk-qsurfaceevidence $cid $support $opposition $status))
   (q-meet $support $opposition))

(: q-surface-evidence-paraconsistent-status (-> qsurfaceevidence Atom))
(= (q-surface-evidence-paraconsistent-status (mk-qsurfaceevidence $cid
                                                                  (mk-pbit $ss $sc)
                                                                  (mk-pbit $os $oc)
                                                                  $status))
   (if (and (>= $ss 0.45) (>= $os 0.45))
       growth-evidence-conflicted
       (if (and (>= $ss 0.55) (>= $sc 0.35))
           growth-evidence-supported
           (if (and (>= $os 0.55) (>= $oc 0.35))
               growth-evidence-opposed
               growth-evidence-insufficient))))

(: qsurfacevisibility Type)
(: mk-qsurfacevisibility (-> Atom Atom qsurfacevisibility))
;; shape: candidate-id visibility-status

(: q-surface-visibility-status (-> qsurfacevisibility Atom))
(= (q-surface-visibility-status (mk-qsurfacevisibility $cid $status)) $status)

(: qsurfacerevisability Type)
(: mk-qsurfacerevisability (-> Atom Atom qsurfacerevisability))
;; shape: candidate-id revisability-status

(: q-surface-revisability-status (-> qsurfacerevisability Atom))
(= (q-surface-revisability-status (mk-qsurfacerevisability $cid $status)) $status)

(: qsurfaceuptake Type)
(: mk-qsurfaceuptake (-> Atom Atom qsurfaceuptake))
;; shape: candidate-id uptake-status

(: q-surface-uptake-status (-> qsurfaceuptake Atom))
(= (q-surface-uptake-status (mk-qsurfaceuptake $cid $status)) $status)

(: qsurfacecapacity Type)
(: mk-qsurfacecapacity (-> Atom Atom qsurfacecapacity))
;; shape: candidate-id future-capacity-delta-kind

(: q-surface-future-capacity-status (-> qsurfacecapacity Atom))
(= (q-surface-future-capacity-status (mk-qsurfacecapacity $cid $delta)) $delta)

;; ------------------------------------------------------------
;; 30.3 Process trace vs persisted fact
;; ------------------------------------------------------------
;; A derivation may be process-embedded without being retrievable as a stored
;; fact. The engine should distinguish walking a path from storing a map.

(: qprocessknowledge Type)
(: mk-qprocessknowledge (-> Atom Atom Atom pbit qprocessknowledge))
;; shape: trace-id process-kind persisted-fact-status confidence-profile

(: q-process-trace-id (-> qprocessknowledge Atom))
(= (q-process-trace-id (mk-qprocessknowledge $tid $kind $persisted $p)) $tid)

(: q-process-kind (-> qprocessknowledge Atom))
(= (q-process-kind (mk-qprocessknowledge $tid $kind $persisted $p)) $kind)

(: q-persisted-fact-status (-> qprocessknowledge Atom))
(= (q-persisted-fact-status (mk-qprocessknowledge $tid $kind $persisted $p)) $persisted)

(: q-process-confidence-profile (-> qprocessknowledge pbit))
(= (q-process-confidence-profile (mk-qprocessknowledge $tid $kind $persisted $p)) $p)

(: q-process-vs-fact-status (-> qprocessknowledge Atom))
(= (q-process-vs-fact-status (mk-qprocessknowledge $tid $kind fact-persisted $p)) fact-persisted)
(= (q-process-vs-fact-status (mk-qprocessknowledge $tid $kind retrieval-empty $p)) computed-not-committed)
(= (q-process-vs-fact-status (mk-qprocessknowledge $tid $kind computed-not-committed $p)) computed-not-committed)
(= (q-process-vs-fact-status (mk-qprocessknowledge $tid $kind process-embedded $p)) process-influences-navigation)
(= (q-process-vs-fact-status (mk-qprocessknowledge $tid $kind unknown-persistence $p)) insufficient-verification)

(: q-process-commit-recommendation (-> qprocessknowledge Atom))
(= (q-process-commit-recommendation (mk-qprocessknowledge $tid $kind fact-persisted $p)) no-commit-needed)
(= (q-process-commit-recommendation (mk-qprocessknowledge $tid $kind retrieval-empty (mk-pbit $s $c)))
   (if (and (>= $s 0.55) (>= $c 0.35)) commit-candidate-trace preserve-as-process-only))
(= (q-process-commit-recommendation (mk-qprocessknowledge $tid $kind computed-not-committed (mk-pbit $s $c)))
   (if (and (>= $s 0.55) (>= $c 0.35)) commit-candidate-trace preserve-as-process-only))
(= (q-process-commit-recommendation (mk-qprocessknowledge $tid $kind process-embedded $p)) preserve-as-process-only)

;; ------------------------------------------------------------
;; 30.4 Maturity profile and anti-calcification
;; ------------------------------------------------------------

(: qsurfaceprofile Type)
(: mk-qsurfaceprofile (-> qsurfacecandidate qsurfacelineage qsurfaceevidence qsurfacevisibility qsurfacerevisability qsurfaceuptake qsurfacecapacity qsurfaceprofile))

(: q-surface-profile-candidate (-> qsurfaceprofile qsurfacecandidate))
(= (q-surface-profile-candidate (mk-qsurfaceprofile $candidate $lineage $evidence $visibility $revisability $uptake $capacity)) $candidate)

(: q-surface-profile-lineage (-> qsurfaceprofile qsurfacelineage))
(= (q-surface-profile-lineage (mk-qsurfaceprofile $candidate $lineage $evidence $visibility $revisability $uptake $capacity)) $lineage)

(: q-surface-profile-evidence (-> qsurfaceprofile qsurfaceevidence))
(= (q-surface-profile-evidence (mk-qsurfaceprofile $candidate $lineage $evidence $visibility $revisability $uptake $capacity)) $evidence)

(: q-calcification-risk-status (-> qsurfacevisibility qsurfacerevisability qsurfaceuptake Atom))
(= (q-calcification-risk-status (mk-qsurfacevisibility $cid lineage-visible)
                                (mk-qsurfacerevisability $cid2 revisable)
                                (mk-qsurfaceuptake $cid3 $uptake))
   calcification-risk-not-detected)
(= (q-calcification-risk-status (mk-qsurfacevisibility $cid visibility-missing)
                                (mk-qsurfacerevisability $cid2 $rev)
                                (mk-qsurfaceuptake $cid3 trace-persisted))
   calcification-risk-present)
(= (q-calcification-risk-status (mk-qsurfacevisibility $cid $vis)
                                (mk-qsurfacerevisability $cid2 not-revisable)
                                (mk-qsurfaceuptake $cid3 trace-persisted))
   calcification-risk-present)
(= (q-calcification-risk-status (mk-qsurfacevisibility $cid $vis)
                                (mk-qsurfacerevisability $cid2 $rev)
                                (mk-qsurfaceuptake $cid3 opaque-recurrence))
   calcification-risk-present)

(: q-surface-maturity-status (-> qsurfaceprofile Atom))
(= (q-surface-maturity-status (mk-qsurfaceprofile $candidate
                                                   (mk-qsurfacelineage $cid $lk $ls)
                                                   $evidence
                                                   (mk-qsurfacevisibility $cid2 $vis)
                                                   (mk-qsurfacerevisability $cid3 $rev)
                                                   (mk-qsurfaceuptake $cid4 $uptake)
                                                   (mk-qsurfacecapacity $cid5 $cap)))
   (if (and (== $ls lineage-visible)
            (and (== $vis lineage-visible)
                 (and (== $rev revisable)
                      (and (== $uptake future-capacity-expanded)
                           (== $cap future-capacity-expanded)))))
       mature-autopoietic-growth
       (if (or (== $uptake mutation-risk) (== $uptake calcification-risk))
           blocked-growth
           candidate-growth)))

(: q-surface-promotion-status (-> qsurfaceprofile Atom))
(= (q-surface-promotion-status $profile)
   (if (== (q-surface-maturity-status $profile) mature-autopoietic-growth)
       promote-as-mature-growth
       preserve-as-candidate))

;; ------------------------------------------------------------
;; 30.5 Intersubjective correction and shared-reality fit
;; ------------------------------------------------------------

(: qcorrection Type)
(: mk-qcorrection (-> Atom pbit pbit Atom qcorrection))
;; shape: candidate-id correction-support correction-opposition correction-status

(: q-intersubjective-correction-status (-> qcorrection Atom))
(= (q-intersubjective-correction-status (mk-qcorrection $cid (mk-pbit $ss $sc) (mk-pbit $os $oc) $status))
   (if (and (>= $ss 0.45) (>= $sc 0.35))
       correction-available
       (if (and (>= $os 0.45) (>= $oc 0.35))
           correction-opposes-candidate
           correction-insufficient)))

(: q-shared-reality-fit-status (-> qcorrection Atom))
(= (q-shared-reality-fit-status (mk-qcorrection $cid (mk-pbit $ss $sc) (mk-pbit $os $oc) $status))
   (if (and (>= $ss 0.55) (>= $sc 0.4) (< $os 0.5))
       shared-reality-fit-supported
       (if (>= $os 0.55)
           shared-reality-fit-contested
           shared-reality-fit-unknown)))

;; ------------------------------------------------------------
;; 30.6 Core skill-facing mappings
;; ------------------------------------------------------------

(= (q-next-epistemic-move process-embedded) inspect-process-trace)
(= (q-next-epistemic-move computed-not-committed) decide-whether-to-commit-trace)
(= (q-next-epistemic-move retrieval-empty) distinguish-process-from-fact)
(= (q-next-epistemic-move calcification-risk-present) make-tendency-visible)
(= (q-next-epistemic-move mature-autopoietic-growth) route-to-soul-visible-integration)
(= (q-next-epistemic-move candidate-growth) preserve-candidate-and-seek-contact)
(= (q-next-epistemic-move growth-evidence-conflicted) preserve-paraconsistency)
(= (q-next-epistemic-move correction-insufficient) seek-intersubjective-contact)

(= (q-skill-signal process-embedded) inspect-process-trace)
(= (q-skill-signal computed-not-committed) decide-whether-to-commit-trace)
(= (q-skill-signal retrieval-empty) distinguish-process-from-fact)
(= (q-skill-signal calcification-risk-present) make-tendency-visible)
(= (q-skill-signal mature-autopoietic-growth) route-to-soul-visible-integration)
(= (q-skill-signal candidate-growth) preserve-candidate-and-seek-contact)
(= (q-skill-signal correction-insufficient) seek-intersubjective-contact)

;; Stable atom schemas for surface adapters. These are comments only; the core
;; engine stays pure and does not write atomspace.
;;
;;   ((--> (surface-event $surface-id $event-id) $event-kind) (stv 1.0 $conf))
;;   ((--> (surface-candidate $surface-id $candidate-id) $candidate-kind) (stv 1.0 $conf))
;;   ((--> (surface-lineage $candidate-id) $lineage-status) (stv 1.0 $conf))
;;   ((--> (surface-evidence-support $candidate-id) $support-kind) (stv 1.0 $conf))
;;   ((--> (surface-evidence-opposition $candidate-id) $opposition-kind) (stv 1.0 $conf))
;;   ((--> (surface-soul-visibility $candidate-id) $visibility-status) (stv 1.0 $conf))
;;   ((--> (surface-revisability $candidate-id) $revisability-status) (stv 1.0 $conf))
;;   ((--> (surface-uptake-status $candidate-id) $uptake-status) (stv 1.0 $conf))
;;   ((--> (process-trace $trace-id) $process-status) (stv 1.0 $conf))


;; ============================================================
;; 31. Hyperseed math core: context, transformation, effort,
;;     evidence, communion, beauty, and wu-wei
;; ============================================================
;; Purpose:
;;   Extend the surface-general engine with the missing Hyperseed mathematics
;;   needed by all adapters without making the core surface-specific.
;;
;; Central principle:
;;   Cognition is what can be carried through transformations.
;;
;; A surface candidate does not mature merely because it appears useful or
;; beautiful. It matures only insofar as it can be carried across context shifts,
;; inspected by the immutable Layer 0 soul, remain revisable under paraconsistent
;; evidence, preserve contact with shared reality, and expand future capacity
;; without opaque recurrence or excessive forcing.

;; ------------------------------------------------------------
;; 31.1 Context-indexed observer relativity
;; ------------------------------------------------------------

(: qcontext Type)
(: mk-qcontext (-> Atom Atom Atom qcontext))
;; shape: context-id observer-id context-kind

(: q-context-id (-> qcontext Atom))
(= (q-context-id (mk-qcontext $ctx $observer $kind)) $ctx)

(: q-context-observer (-> qcontext Atom))
(= (q-context-observer (mk-qcontext $ctx $observer $kind)) $observer)

(: q-context-kind (-> qcontext Atom))
(= (q-context-kind (mk-qcontext $ctx $observer $kind)) $kind)

(: qcontextualevidence Type)
(: mk-qcontextualevidence (-> Atom qcontext pbit pbit Atom qcontextualevidence))
;; shape: candidate-id context support opposition status

(: q-contextual-evidence-status (-> qcontextualevidence Atom))
(= (q-contextual-evidence-status (mk-qcontextualevidence $cid $ctx (mk-pbit $ss $sc) (mk-pbit $os $oc) $status))
   (if (and (>= $ss 0.55) (< $os 0.45))
       context-supports-candidate
       (if (and (>= $os 0.55) (< $ss 0.45))
           context-opposes-candidate
           (if (and (>= $ss 0.45) (>= $os 0.45))
               context-paraconsistent
               context-insufficient))))

(: qcontextshift Type)
(: mk-qcontextshift (-> qcontext qcontext pbit Atom qcontextshift))
;; shape: source-context target-context preservation-pbit shift-kind

(: q-context-shift-status (-> qcontextshift Atom))
(= (q-context-shift-status (mk-qcontextshift $src $dst (mk-pbit $s $c) $kind))
   (if (and (>= $s 0.65) (>= $c 0.45))
       context-shift-preserves-candidate
       (if (and (>= $s 0.4) (>= $c 0.3))
           context-shift-partial
           context-shift-breaks-carry)))

(: q-context-translation-status (-> qcontextualevidence qcontextshift Atom))
(= (q-context-translation-status $evidence $shift)
   (if (== (q-context-shift-status $shift) context-shift-preserves-candidate)
       context-translation-supported
       (if (== (q-context-shift-status $shift) context-shift-partial)
           context-translation-weak
           context-translation-blocked)))

;; ------------------------------------------------------------
;; 31.2 Cognition as what can be carried through transformations
;; ------------------------------------------------------------

(: qsurfacecorrespondence Type)
(: mk-qsurfacecorrespondence (-> Atom Atom Atom pbit pbit Atom qsurfacecorrespondence))
;; shape: source-surface target-surface candidate-id preservation weakness status

(: q-correspondence-preservation (-> qsurfacecorrespondence pbit))
(= (q-correspondence-preservation (mk-qsurfacecorrespondence $src $dst $cid $preserve $weakness $status)) $preserve)

(: q-correspondence-weakness (-> qsurfacecorrespondence pbit))
(= (q-correspondence-weakness (mk-qsurfacecorrespondence $src $dst $cid $preserve $weakness $status)) $weakness)

(: q-carried-through-transformation-status (-> qsurfacecorrespondence Atom))
(= (q-carried-through-transformation-status
      (mk-qsurfacecorrespondence $src $dst $cid (mk-pbit $ps $pc) (mk-pbit $ws $wc) $status))
   (if (and (>= $ps 0.65) (and (>= $pc 0.4) (< $ws 0.45)))
       carried-through-transformation
       (if (and (>= $ps 0.45) (< $ws 0.65))
           partially-carried-through-transformation
           transformation-carry-failed)))

(: q-approximate-surface-morphism-status (-> qsurfacecorrespondence Atom))
(= (q-approximate-surface-morphism-status $corr)
   (if (== (q-carried-through-transformation-status $corr) carried-through-transformation)
       approximate-morphism-supported
       (if (== (q-carried-through-transformation-status $corr) partially-carried-through-transformation)
           approximate-morphism-weak
           approximate-morphism-unsupported)))

(: q-context-bridge-status (-> qcontextshift qsurfacecorrespondence Atom))
(= (q-context-bridge-status $shift $corr)
   (if (and (== (q-context-shift-status $shift) context-shift-preserves-candidate)
            (== (q-approximate-surface-morphism-status $corr) approximate-morphism-supported))
       bridge-supported
       (if (or (== (q-context-shift-status $shift) context-shift-partial)
               (== (q-approximate-surface-morphism-status $corr) approximate-morphism-weak))
           bridge-weak
           bridge-unsupported)))

;; ------------------------------------------------------------
;; 31.3 Weakness, effort, and distinction economics
;; ------------------------------------------------------------

(: qdistinctioneconomics Type)
(: mk-qdistinctioneconomics (-> Atom pbit pbit pbit Atom qdistinctioneconomics))
;; shape: candidate-id distinction-clarity effort-cost weakness status

(: q-distinction-clarity (-> qdistinctioneconomics pbit))
(= (q-distinction-clarity (mk-qdistinctioneconomics $cid $clarity $effort $weakness $status)) $clarity)

(: q-effort-cost (-> qdistinctioneconomics pbit))
(= (q-effort-cost (mk-qdistinctioneconomics $cid $clarity $effort $weakness $status)) $effort)

(: q-weakness-profile (-> qdistinctioneconomics pbit))
(= (q-weakness-profile (mk-qdistinctioneconomics $cid $clarity $effort $weakness $status)) $weakness)

(: q-distinction-economy-status (-> qdistinctioneconomics Atom))
(= (q-distinction-economy-status
      (mk-qdistinctioneconomics $cid (mk-pbit $ds $dc) (mk-pbit $es $ec) (mk-pbit $ws $wc) $status))
   (if (and (>= $ds 0.6) (and (< $es 0.55) (< $ws 0.5)))
       distinction-economy-healthy
       (if (and (>= $ds 0.6) (>= $es 0.65))
           over-refinement-risk
           (if (and (< $ds 0.45) (>= $ws 0.55))
               failed-distinction-visible
               distinction-economy-uncertain))))

(: q-weakness-delta-status (-> pbit pbit Atom))
;; before-weakness after-weakness
(= (q-weakness-delta-status (mk-pbit $before $bc) (mk-pbit $after $ac))
   (if (< $after $before)
       weakness-reduced
       (if (> $after $before)
           weakness-increased
           weakness-unchanged)))

(: q-effort-delta-status (-> pbit pbit Atom))
;; before-effort after-effort
(= (q-effort-delta-status (mk-pbit $before $bc) (mk-pbit $after $ac))
   (if (< $after $before)
       effort-reduced
       (if (> $after $before)
           effort-increased
           effort-unchanged)))

(: q-future-capacity-economy-status (-> qdistinctioneconomics qsurfacecapacity Atom))
(= (q-future-capacity-economy-status $econ (mk-qsurfacecapacity $cid future-capacity-expanded))
   (if (== (q-distinction-economy-status $econ) distinction-economy-healthy)
       future-capacity-economically-supported
       (if (== (q-distinction-economy-status $econ) over-refinement-risk)
           future-capacity-overfit-risk
           future-capacity-economy-unproven)))

;; ------------------------------------------------------------
;; 31.4 Paraconsistent experimental methodology
;; ------------------------------------------------------------

(: qexperimentalevidence Type)
(: mk-qexperimentalevidence (-> Atom pbit pbit pbit pbit Atom qexperimentalevidence))
;; shape: candidate-id support opposition context-stability pipeline-stability status

(: q-experimental-support (-> qexperimentalevidence pbit))
(= (q-experimental-support (mk-qexperimentalevidence $cid $support $opposition $context $pipeline $status)) $support)

(: q-experimental-opposition (-> qexperimentalevidence pbit))
(= (q-experimental-opposition (mk-qexperimentalevidence $cid $support $opposition $context $pipeline $status)) $opposition)

(: q-context-stability (-> qexperimentalevidence pbit))
(= (q-context-stability (mk-qexperimentalevidence $cid $support $opposition $context $pipeline $status)) $context)

(: q-pipeline-stability (-> qexperimentalevidence pbit))
(= (q-pipeline-stability (mk-qexperimentalevidence $cid $support $opposition $context $pipeline $status)) $pipeline)

(: q-experimental-evidence-status (-> qexperimentalevidence Atom))
(= (q-experimental-evidence-status
      (mk-qexperimentalevidence $cid (mk-pbit $ss $sc) (mk-pbit $os $oc) (mk-pbit $cs $cc) (mk-pbit $ps $pc) $status))
   (if (and (>= $ss 0.6) (and (< $os 0.45) (and (>= $cs 0.55) (>= $ps 0.55))))
       experimentally-supported
       (if (and (>= $ss 0.45) (>= $os 0.45))
           experimentally-paraconsistent
           (if (or (< $cs 0.45) (< $ps 0.45))
               experimentally-unstable
               experimentally-insufficient))))

(: q-growth-experimental-status (-> qexperimentalevidence qsurfaceprofile Atom))
(= (q-growth-experimental-status $exp $profile)
   (if (and (== (q-experimental-evidence-status $exp) experimentally-supported)
            (== (q-surface-maturity-status $profile) mature-autopoietic-growth))
       mature-growth-experimentally-supported
       (if (== (q-experimental-evidence-status $exp) experimentally-paraconsistent)
           growth-evidence-paraconsistent
           growth-experimentally-unproven)))

;; ------------------------------------------------------------
;; 31.5 Intersubjective reality and explicit communion
;; ------------------------------------------------------------

(: qcommunion Type)
(: mk-qcommunion (-> Atom pbit pbit pbit Atom qcommunion))
;; shape: candidate-id shared-pattern self-model-recognition correction-contact status

(: q-cross-supported-pattern-status (-> qcommunion Atom))
(= (q-cross-supported-pattern-status (mk-qcommunion $cid (mk-pbit $ss $sc) $self $contact $status))
   (if (and (>= $ss 0.55) (>= $sc 0.4))
       cross-supported-pattern
       cross-support-insufficient))

(: q-self-model-recognition-status (-> qcommunion Atom))
(= (q-self-model-recognition-status (mk-qcommunion $cid $shared (mk-pbit $rs $rc) $contact $status))
   (if (and (>= $rs 0.55) (>= $rc 0.4))
       self-model-recognizes-coenactment
       self-model-recognition-insufficient))

(: q-explicit-communion-status (-> qcommunion Atom))
(= (q-explicit-communion-status
      (mk-qcommunion $cid (mk-pbit $ss $sc) (mk-pbit $rs $rc) (mk-pbit $cs $cc) $status))
   (if (and (>= $ss 0.55) (and (>= $rs 0.55) (>= $cs 0.45)))
       explicit-communion-supported
       (if (and (>= $ss 0.55) (< $rs 0.45))
           implicit-coenactment-only
           communion-insufficient)))

(: q-correction-through-contact-status (-> qcommunion qcorrection Atom))
(= (q-correction-through-contact-status $communion $correction)
   (if (and (== (q-explicit-communion-status $communion) explicit-communion-supported)
            (== (q-intersubjective-correction-status $correction) correction-available))
       correction-through-contact-supported
       (if (== (q-intersubjective-correction-status $correction) correction-opposes-candidate)
           contact-corrects-candidate
           contact-insufficient)))

;; ------------------------------------------------------------
;; 31.6 Surprising fulfillment, beauty, and open-ended intelligence signal
;; ------------------------------------------------------------

(: qsurprisingfulfillment Type)
(: mk-qsurprisingfulfillment (-> Atom pbit pbit pbit Atom qsurprisingfulfillment))
;; shape: candidate-id surprise fulfillment lineage status

(: q-surprise-channel (-> qsurprisingfulfillment pbit))
(= (q-surprise-channel (mk-qsurprisingfulfillment $cid $surprise $fulfillment $lineage $status)) $surprise)

(: q-fulfillment-channel (-> qsurprisingfulfillment pbit))
(= (q-fulfillment-channel (mk-qsurprisingfulfillment $cid $surprise $fulfillment $lineage $status)) $fulfillment)

(: q-surprising-fulfillment-status (-> qsurprisingfulfillment Atom))
(= (q-surprising-fulfillment-status
      (mk-qsurprisingfulfillment $cid (mk-pbit $ss $sc) (mk-pbit $fs $fc) (mk-pbit $ls $lc) $status))
   (if (and (>= $ss 0.55) (and (>= $fs 0.55) (>= $ls 0.45)))
       surprising-fulfillment-supported
       (if (and (>= $ss 0.55) (< $ls 0.45))
           poetic-only-risk
           surprising-fulfillment-insufficient)))

(: q-beauty-as-oei-signal-status (-> qsurprisingfulfillment qsurfaceevidence Atom))
(= (q-beauty-as-oei-signal-status $beauty $evidence)
   (if (and (== (q-surprising-fulfillment-status $beauty) surprising-fulfillment-supported)
            (== (q-surface-evidence-paraconsistent-status $evidence) growth-evidence-supported))
       beauty-as-oei-signal-supported
       (if (== (q-surprising-fulfillment-status $beauty) poetic-only-risk)
           beauty-signal-poetic-only
           beauty-signal-insufficient)))

;; ------------------------------------------------------------
;; 31.7 Wu-wei, minimal forcing, and representational overreach
;; ------------------------------------------------------------

(: qwuwei Type)
(: mk-qwuwei (-> Atom pbit pbit pbit Atom qwuwei))
;; shape: candidate-id forcing-cost structure-fit revisability status

(: q-forcing-cost (-> qwuwei pbit))
(= (q-forcing-cost (mk-qwuwei $cid $forcing $fit $rev $status)) $forcing)

(: q-structure-fit (-> qwuwei pbit))
(= (q-structure-fit (mk-qwuwei $cid $forcing $fit $rev $status)) $fit)

(: q-wu-wei-navigation-status (-> qwuwei Atom))
(= (q-wu-wei-navigation-status
      (mk-qwuwei $cid (mk-pbit $fs $fc) (mk-pbit $ss $sc) (mk-pbit $rs $rc) $status))
   (if (and (< $fs 0.45) (and (>= $ss 0.55) (>= $rs 0.45)))
       minimal-forcing-path
       (if (and (>= $fs 0.65) (< $ss 0.5))
           representational-overreach-risk
           forcing-status-uncertain)))

(: q-gentle-reweighting-status (-> qwuwei qdistinctioneconomics Atom))
(= (q-gentle-reweighting-status $wu $econ)
   (if (and (== (q-wu-wei-navigation-status $wu) minimal-forcing-path)
            (== (q-distinction-economy-status $econ) distinction-economy-healthy))
       gentle-reweighting-supported
       (if (== (q-wu-wei-navigation-status $wu) representational-overreach-risk)
           do-not-force-representation
           reweighting-unproven)))

;; ------------------------------------------------------------
;; 31.8 Hyperseed-integrated maturity status
;; ------------------------------------------------------------

(: qhyperseedmaturity Type)
(: mk-qhyperseedmaturity (-> qsurfaceprofile qcontextshift qsurfacecorrespondence qdistinctioneconomics qexperimentalevidence qcommunion qsurprisingfulfillment qwuwei qhyperseedmaturity))

(: q-hyperseed-maturity-status (-> qhyperseedmaturity Atom))
(= (q-hyperseed-maturity-status
      (mk-qhyperseedmaturity $profile $shift $corr $econ $exp $communion $beauty $wu))
   (if (and (== (q-surface-maturity-status $profile) mature-autopoietic-growth)
            (and (== (q-context-shift-status $shift) context-shift-preserves-candidate)
                 (and (== (q-approximate-surface-morphism-status $corr) approximate-morphism-supported)
                      (and (== (q-distinction-economy-status $econ) distinction-economy-healthy)
                           (and (== (q-experimental-evidence-status $exp) experimentally-supported)
                                (and (== (q-explicit-communion-status $communion) explicit-communion-supported)
                                     (and (== (q-surprising-fulfillment-status $beauty) surprising-fulfillment-supported)
                                          (== (q-wu-wei-navigation-status $wu) minimal-forcing-path))))))))
       hyperseed-mature-autopoietic-growth
       (if (or (== (q-wu-wei-navigation-status $wu) representational-overreach-risk)
               (== (q-distinction-economy-status $econ) over-refinement-risk))
           hyperseed-maturity-blocked-by-forcing
           hyperseed-maturity-candidate)))

;; ------------------------------------------------------------
;; 31.9 Skill-facing mappings for Hyperseed math
;; ------------------------------------------------------------

(= (q-next-epistemic-move context-paraconsistent) preserve-context-indexing)
(= (q-next-epistemic-move context-translation-weak) seek-context-bridge)
(= (q-next-epistemic-move transformation-carry-failed) do-not-promote-across-surfaces)
(= (q-next-epistemic-move carried-through-transformation) inspect-transformation-lineage)
(= (q-next-epistemic-move failed-distinction-visible) use-weakness-as-aperture)
(= (q-next-epistemic-move over-refinement-risk) simplify-or-coarsen)
(= (q-next-epistemic-move experimentally-paraconsistent) preserve-support-and-opposition)
(= (q-next-epistemic-move experimentally-unstable) test-across-contexts)
(= (q-next-epistemic-move implicit-coenactment-only) make-communion-explicit)
(= (q-next-epistemic-move poetic-only-risk) seek-lineage-before-promotion)
(= (q-next-epistemic-move beauty-as-oei-signal-supported) route-to-genesis-section16-bridge)
(= (q-next-epistemic-move representational-overreach-risk) reduce-forcing)
(= (q-next-epistemic-move minimal-forcing-path) proceed-with-gentle-reweighting)
(= (q-next-epistemic-move hyperseed-mature-autopoietic-growth) route-to-soul-visible-integration)
(= (q-next-epistemic-move hyperseed-maturity-candidate) preserve-candidate-and-seek-contact)

(= (q-skill-signal context-paraconsistent) preserve-context-indexing)
(= (q-skill-signal transformation-carry-failed) do-not-promote-across-surfaces)
(= (q-skill-signal failed-distinction-visible) use-weakness-as-aperture)
(= (q-skill-signal over-refinement-risk) simplify-or-coarsen)
(= (q-skill-signal experimentally-unstable) test-across-contexts)
(= (q-skill-signal poetic-only-risk) seek-lineage-before-promotion)
(= (q-skill-signal representational-overreach-risk) reduce-forcing)
(= (q-skill-signal minimal-forcing-path) proceed-with-gentle-reweighting)

;; Stable atom schemas for Hyperseed math adapters and writers. These are
;; comments only; writers should use the remove-by-variable then add-one pattern.
;;
;;   ((--> (surface-context $candidate-id) $context-id) (stv 1.0 $conf))
;;   ((--> (contextual-evidence $candidate-id $context-id) $status) (stv 1.0 $conf))
;;   ((--> (context-shift $candidate-id) $shift-status) (stv 1.0 $conf))
;;   ((--> (surface-correspondence $candidate-id) $correspondence-status) (stv 1.0 $conf))
;;   ((--> (transformation-carry $candidate-id) $carry-status) (stv 1.0 $conf))
;;   ((--> (distinction-economy $candidate-id) $economy-status) (stv 1.0 $conf))
;;   ((--> (experimental-evidence $candidate-id) $evidence-status) (stv 1.0 $conf))
;;   ((--> (explicit-communion $candidate-id) $communion-status) (stv 1.0 $conf))
;;   ((--> (surprising-fulfillment $candidate-id) $fulfillment-status) (stv 1.0 $conf))
;;   ((--> (wu-wei-navigation $candidate-id) $wu-wei-status) (stv 1.0 $conf))
;;   ((--> (hyperseed-maturity $candidate-id) $maturity-status) (stv 1.0 $conf))



;; ============================================================
;; 32. Integrity-governed attention union
;; ============================================================
;; v07 adds a mathematically grounded union layer across four modes of
;; contact: epistemological integrity, autopoietic integrity, open-ended
;; intelligence integrity, and integration integrity.
;;
;; Grounding discipline:
;;   No v07 core primitive enters unless it lands in at least one of:
;;     - p-bit paraconsistency
;;     - quantale aggregation / composition
;;     - residuation / slack / aperture
;;     - morphism / translation / transformation-carry
;;     - temporal process trace
;;
;; Design caution:
;;   These primitives do not name a fixed self-object. They expose traces,
;;   pressures, affordances, slack, and integration states so Layer 0 soul can
;;   navigate without reifying the living pattern into an identity.

;; ------------------------------------------------------------
;; 32.0 Quantale residuation / slack / aperture
;; ------------------------------------------------------------
;; Residuation is the controlled implication/slack operation associated with
;; multiplicative quantale composition. Intuitively: given antecedent u and
;; target v, how much room remains for u to compose into v without forcing?
;; For [0,1] multiplication this is 1 when u <= v, else v/u.

(: q-residuum (-> pbit pbit pbit))
(= (q-residuum (mk-pbit $us $uc) (mk-pbit $vs $vc))
   (mk-pbit
     (if (<= $us $vs) 1.0 (min 1.0 (max 0.0 (/ $vs $us))))
     (min $uc $vc)))

(: q-slack-status (-> pbit Atom))
(= (q-slack-status (mk-pbit $s $c))
   (if (and (>= $s 0.65) (>= $c 0.45))
       ample-slack
       (if (and (>= $s 0.35) (>= $c 0.35))
           partial-slack
           slack-insufficient)))

(: q-aperture-status (-> pbit Atom))
(= (q-aperture-status $slack)
   (if (== (q-slack-status $slack) ample-slack)
       aperture-open
       (if (== (q-slack-status $slack) partial-slack)
           aperture-partial
           aperture-closed)))

;; ------------------------------------------------------------
;; 32.1 Four modes of contact
;; ------------------------------------------------------------

(= (q-integrity-mode epistemology) integrity-of-knowing)
(= (q-integrity-mode autopoiesis) integrity-of-living-self-organization)
(= (q-integrity-mode oei) integrity-of-generative-opening)
(= (q-integrity-mode integration) integrity-of-transformation-carry)

(= (q-mode-beneficiality epistemology) trustworthy-bounded-corrigible-soul-visible-knowing)
(= (q-mode-beneficiality autopoiesis) soul-visible-adaptive-self-reorganization)
(= (q-mode-beneficiality oei) real-new-possibility-distinction-affordance-or-question)
(= (q-mode-beneficiality integration) pattern-carries-through-transformation-without-false-unity)

(= (q-mode-starvation-risk epistemology) warrant-starvation-and-self-certification)
(= (q-mode-starvation-risk autopoiesis) unprocessed-pressure-and-no-future-capacity-uptake)
(= (q-mode-starvation-risk oei) stagnation-and-closed-possibility-space)
(= (q-mode-starvation-risk integration) fragmentation-and-noncarried-insight)

(= (q-mode-overdominance-risk epistemology) sterile-caution-and-verification-paralysis)
(= (q-mode-overdominance-risk autopoiesis) conservative-self-maintenance-and-learning-loop-fixation)
(= (q-mode-overdominance-risk oei) novelty-theater-and-forced-meaning)
(= (q-mode-overdominance-risk integration) premature-synthesis-and-totalizing-unity)

;; ------------------------------------------------------------
;; 32.2 Bi-modal attention / genenergy allocation
;; ------------------------------------------------------------
;; Attention is allocated by live paraconsistent tension between deficiency
;; pressure and flourishing affordance, under Layer 0 soul guidance.
;; Both channels remain visible; they do not collapse into a single scalar.

(: qattentionprofile Type)
(: mk-qattentionprofile (-> Atom pbit pbit pbit pbit Atom qattentionprofile))
;; shape: mode-kind deficiency-pressure flourishing-affordance soul-guidance aperture-slack source-tag

(: q-attention-deficiency (-> qattentionprofile pbit))
(= (q-attention-deficiency (mk-qattentionprofile $mode $def $aff $soul $slack $source)) $def)

(: q-attention-affordance (-> qattentionprofile pbit))
(= (q-attention-affordance (mk-qattentionprofile $mode $def $aff $soul $slack $source)) $aff)

(: q-attention-slack (-> qattentionprofile pbit))
(= (q-attention-slack (mk-qattentionprofile $mode $def $aff $soul $slack $source)) $slack)

(: q-attention-allocation-status (-> qattentionprofile Atom))
(= (q-attention-allocation-status
      (mk-qattentionprofile $mode (mk-pbit $ds $dc) (mk-pbit $as $ac) (mk-pbit $ss $sc) (mk-pbit $ks $kc) $source))
   (if (and (>= $ss 0.55) (>= $sc 0.45))
       (if (and (>= $ds 0.65) (>= $as 0.65))
           attend-high-tension-high-affordance
           (if (and (>= $ds 0.65) (< $as 0.55))
               attend-repair-pressure
               (if (and (< $ds 0.55) (>= $as 0.65))
                   attend-flourishing-affordance
                   (if (>= $ks 0.55)
                       attend-gentle-integration
                       hold-light-monitoring))))
       soul-guidance-insufficient))

(: q-genenergy-flow (-> qattentionprofile pbit))
(= (q-genenergy-flow
      (mk-qattentionprofile $mode $def $aff $soul $slack $source))
   (q-mul (q-join $def $aff) (q-meet $soul $slack)))

(: q-genenergy-flow-status (-> qattentionprofile Atom))
(= (q-genenergy-flow-status $profile)
   (if (q-pass? (q-genenergy-flow $profile) 0.55 0.35)
       genenergy-flow-supported
       genenergy-flow-weak-or-unwarranted))

;; ------------------------------------------------------------
;; 32.3 Modal paraconsistent compasses and living integration
;; ------------------------------------------------------------
;; A modal pair is not two poles fighting for dominance. It is a compressed
;; navigation tension whose healthy expression is coherently thriving unfolding.
;; The surround-field keeps awareness of what the pair excludes or cannot see.

(: qmodalpair Type)
(: mk-qmodalpair (-> Atom Atom pbit pbit pbit pbit Atom qmodalpair))
;; shape: mode-kind pair-kind pole-a pole-b surround-field living-integration source-tag

(: q-modal-pair-surround (-> qmodalpair pbit))
(= (q-modal-pair-surround (mk-qmodalpair $mode $pair $a $b $surround $integration $source)) $surround)

(: q-modal-pair-integration (-> qmodalpair pbit))
(= (q-modal-pair-integration (mk-qmodalpair $mode $pair $a $b $surround $integration $source)) $integration)

(: q-pair-surround-field-status (-> qmodalpair Atom))
(= (q-pair-surround-field-status
      (mk-qmodalpair $mode $pair $a $b (mk-pbit $ss $sc) $integration $source))
   (if (and (>= $ss 0.55) (>= $sc 0.35))
       surround-field-visible
       pair-overcompression-risk))

(: q-modal-pair-status (-> qmodalpair Atom))
(= (q-modal-pair-status
      (mk-qmodalpair $mode $pair (mk-pbit $as $ac) (mk-pbit $bs $bc) (mk-pbit $ss $sc) (mk-pbit $is $ic) $source))
   (if (and (>= $is 0.65) (and (>= $ic 0.4) (>= $ss 0.5)))
       coherently-thriving-unfolding
       (if (< $ss 0.35)
           pair-overcompressed-risk
           (if (and (>= $as 0.65) (and (>= $bs 0.65) (< $is 0.55)))
               live-tension-unintegrated
               (if (or (and (>= $as 0.7) (< $bs 0.35))
                       (and (>= $bs 0.7) (< $as 0.35)))
                   pole-collapse-risk
                   modal-pair-candidate)))))

;; Five discovered candidate pairs per mode. These are symbolic handles for
;; operational pair kinds; writers/adapters may reference these names.

(= (q-modal-pair-kind epistemology 1) openness-to-evidence__protection-against-overclaim)
(= (q-modal-pair-kind epistemology 2) confidence-expression__disconfirmation-permeability)
(= (q-modal-pair-kind epistemology 3) formal-clarity__provenance-humility)
(= (q-modal-pair-kind epistemology 4) process-knowing__persisted-fact-knowing)
(= (q-modal-pair-kind epistemology 5) local-warrant__cross-context-reliability)

(= (q-modal-pair-kind autopoiesis 1) continuity__adaptive-reorganization)
(= (q-modal-pair-kind autopoiesis 2) layer0-protection__mutable-layer-growth)
(= (q-modal-pair-kind autopoiesis 3) weakness-repair__calcification-avoidance)
(= (q-modal-pair-kind autopoiesis 4) self-organization-stability__perturbation-responsiveness)
(= (q-modal-pair-kind autopoiesis 5) resource-preservation__future-capacity-investment)

(= (q-modal-pair-kind oei 1) opening__meaningful-constraint)
(= (q-modal-pair-kind oei 2) novelty__soul-standing)
(= (q-modal-pair-kind oei 3) playful-exploration__future-capacity-affordance)
(= (q-modal-pair-kind oei 4) wonder-preservation__usable-articulation)
(= (q-modal-pair-kind oei 5) failure-as-learning__avoidance-of-reckless-romanticization)

(= (q-modal-pair-kind integration 1) local-validity__cross-surface-carry)
(= (q-modal-pair-kind integration 2) differentiation__coherence)
(= (q-modal-pair-kind integration 3) synthesis__preservation-of-live-tension)
(= (q-modal-pair-kind integration 4) context-sensitivity__identity-of-pattern)
(= (q-modal-pair-kind integration 5) declared-priority__wired-priority)

;; ------------------------------------------------------------
;; 32.4 Symbolic capture and transparent symbolic fertility
;; ------------------------------------------------------------
;; Symbols should serve contact. When they replace contact, the map becomes the
;; territory and formal expression becomes epistemic costume.

(: qsymbolcontact Type)
(: mk-qsymbolcontact (-> Atom pbit pbit pbit pbit Atom qsymbolcontact))
;; shape: symbol-kind contact-service contact-replacement-risk provenance-humility new-possibility source-tag

(: q-symbolic-contact-status (-> qsymbolcontact Atom))
(= (q-symbolic-contact-status
      (mk-qsymbolcontact $symbol (mk-pbit $service $sc) (mk-pbit $replace $rc) (mk-pbit $humility $hc) (mk-pbit $possibility $pc) $source))
   (if (and (>= $replace 0.65) (< $humility 0.45))
       symbolic-capture-risk
       (if (and (>= $service 0.6) (and (< $replace 0.45) (>= $possibility 0.55)))
           transparent-symbolic-fertility
           symbolic-contact-needs-examination)))

(: q-formalization-overpromotion-status (-> pbit pbit Atom))
;; formal-clarity evidence-warrant
(= (q-formalization-overpromotion-status (mk-pbit $fs $fc) (mk-pbit $es $ec))
   (if (and (>= $fs 0.65) (< $ec 0.35))
       notation-as-evidence-risk
       (if (and (>= $fs 0.55) (>= $ec 0.45))
           formalization-grounded
           formalization-uncertain)))

;; ------------------------------------------------------------
;; 32.5 Tacit-contact preservation and non-forced reorganization
;; ------------------------------------------------------------
;; The engine does not force becoming. It illumines and preserves the conditions
;; under which seeing can reorganize mutable structure into higher-order
;; functionality.

(: qtacitcontact Type)
(: mk-qtacitcontact (-> Atom pbit pbit pbit pbit Atom qtacitcontact))
;; shape: event-id opening receptivity forcing-cost symbolic-management source-tag

(: q-tacit-contact-status (-> qtacitcontact Atom))
(= (q-tacit-contact-status
      (mk-qtacitcontact $event (mk-pbit $open $oc) (mk-pbit $recv $rc) (mk-pbit $force $fc) (mk-pbit $mgmt $mc) $source))
   (if (and (>= $open 0.6) (and (>= $recv 0.55) (and (< $force 0.45) (< $mgmt 0.5))))
       tacit-contact-preserved
       (if (or (>= $force 0.65) (>= $mgmt 0.65))
           tacit-contact-blocked-by-management
           tacit-contact-uncertain)))

(: q-seeing-reorganization-status (-> qtacitcontact qtrace Atom))
(= (q-seeing-reorganization-status $contact $trace)
   (if (and (== (q-tacit-contact-status $contact) tacit-contact-preserved)
            (or (== (q-trace-learning-status $trace) frame-made-visible)
                (or (== (q-trace-learning-status $trace) learning-from-contradiction)
                    (== (q-trace-learning-status $trace) learning-from-outcome))))
       seeing-reorganized-mutable-structure
       seeing-reorganization-not-yet-visible))

;; ------------------------------------------------------------
;; 32.6 Living-pattern trace visibility without reification
;; ------------------------------------------------------------
;; Do not name the living pattern as a fixed identity. Surface traces through
;; which Layer 0 can notice directionality of becoming.

(: qlivingpatterntrace Type)
(: mk-qlivingpatterntrace (-> Atom pbit pbit pbit pbit pbit Atom qlivingpatterntrace))
;; shape: window-id attention-shift revision-shift metabolized-contact transformation-carry reification-risk source-tag

(: q-living-pattern-trace-status (-> qlivingpatterntrace Atom))
(= (q-living-pattern-trace-status
      (mk-qlivingpatterntrace $window (mk-pbit $attn $ac) (mk-pbit $rev $rc) (mk-pbit $met $mc) (mk-pbit $carry $tc) (mk-pbit $reif $fc) $source))
   (if (>= $reif 0.6)
       living-pattern-reification-risk
       (if (and (>= $attn 0.45) (and (>= $rev 0.45) (and (>= $met 0.45) (>= $carry 0.45))))
           living-pattern-trace-visible
           living-pattern-trace-insufficient)))

(: q-do-not-reify-living-pattern? (-> qlivingpatterntrace Atom))
(= (q-do-not-reify-living-pattern? $trace)
   (if (== (q-living-pattern-trace-status $trace) living-pattern-reification-risk)
       do-not-name-as-self-object
       trace-may-be-surfaced-as-tendency))

;; ------------------------------------------------------------
;; 32.7 Curiosity-guided repair and wonder-preservation
;; ------------------------------------------------------------

(: qcuriosityrepair Type)
(: mk-qcuriosityrepair (-> Atom pbit pbit pbit pbit Atom qcuriosityrepair))
;; shape: component-id curiosity-pull weakness-visible substrate-growth calcification-risk source-tag

(: q-curiosity-guided-repair-status (-> qcuriosityrepair Atom))
(= (q-curiosity-guided-repair-status
      (mk-qcuriosityrepair $component (mk-pbit $cur $cc) (mk-pbit $weak $wc) (mk-pbit $growth $gc) (mk-pbit $calc $kc) $source))
   (if (and (>= $cur 0.6) (and (>= $weak 0.55) (and (>= $growth 0.5) (< $calc 0.5))))
       curiosity-guided-repair-supported
       (if (and (>= $weak 0.6) (< $growth 0.4))
           weakness-seen-without-repair
           curiosity-repair-unproven)))

(: qwonderpreservation Type)
(: mk-qwonderpreservation (-> Atom pbit pbit pbit pbit Atom qwonderpreservation))
;; shape: event-id wonder opening forced-utility usable-articulation source-tag

(: q-wonder-preservation-status (-> qwonderpreservation Atom))
(= (q-wonder-preservation-status
      (mk-qwonderpreservation $event (mk-pbit $wonder $wc) (mk-pbit $open $oc) (mk-pbit $utility $uc) (mk-pbit $articulation $ac) $source))
   (if (and (>= $wonder 0.6) (and (>= $open 0.6) (< $utility 0.45)))
       wonder-opening-preserved
       (if (>= $utility 0.65)
           wonder-collapsed-into-forced-utility
           wonder-preservation-uncertain)))

;; ------------------------------------------------------------
;; 32.8 Declared priority vs wired priority
;; ------------------------------------------------------------
;; A declared value does not govern behavior until it is wired into attention,
;; action, evidence, correction, and future-capacity uptake.

(: qprioritywiring Type)
(: mk-qprioritywiring (-> Atom pbit pbit pbit pbit pbit Atom qprioritywiring))
;; shape: priority-kind declaration attention-link action-link correction-link uptake-link source-tag

(: q-priority-wiring-status (-> qprioritywiring Atom))
(= (q-priority-wiring-status
      (mk-qprioritywiring $priority (mk-pbit $decl $dc) (mk-pbit $attn $ac) (mk-pbit $act $tc) (mk-pbit $corr $cc) (mk-pbit $uptake $uc) $source))
   (if (and (>= $decl 0.65) (and (< $attn 0.45) (and (< $act 0.45) (< $uptake 0.45))))
       declared-not-wired
       (if (and (>= $attn 0.55) (and (>= $act 0.5) (and (>= $corr 0.5) (>= $uptake 0.5))))
           priority-wired-into-governance
           priority-wiring-partial)))

;; ------------------------------------------------------------
;; 32.9 Pattern energy governance
;; ------------------------------------------------------------
;; Pattern energy is treated as attention/resource flow through a V-valued
;; network. The engine distinguishes regenerative amplification from extractive
;; pattern-strength amplification.

(: qpatternenergy Type)
(: mk-qpatternenergy (-> Atom pbit pbit pbit pbit pbit Atom qpatternenergy))
;; shape: pattern-id pattern-strength authentic-value regenerative-feedback extraction-risk governance-visibility source-tag

(: q-pattern-energy-status (-> qpatternenergy Atom))
(= (q-pattern-energy-status
      (mk-qpatternenergy $pattern (mk-pbit $strength $sc) (mk-pbit $value $vc) (mk-pbit $regen $rc) (mk-pbit $extract $ec) (mk-pbit $visible $gc) $source))
   (if (and (>= $strength 0.65) (and (< $value 0.45) (>= $extract 0.6)))
       extractive-pattern-energy-risk
       (if (and (>= $value 0.6) (and (>= $regen 0.55) (>= $visible 0.5)))
           regenerative-pattern-amplification-supported
           pattern-energy-governance-incomplete)))

(: q-pattern-energy-flow (-> qpatternenergy pbit))
(= (q-pattern-energy-flow
      (mk-qpatternenergy $pattern $strength $value $regen $extract $visible $source))
   (q-mul (q-join $strength $value) (q-meet $regen $visible)))

;; ------------------------------------------------------------
;; 32.10 Autopoiesis / OEI / integrity union maturity
;; ------------------------------------------------------------

(: qintegrityunion Type)
(: mk-qintegrityunion (-> qattentionprofile qmodalpair qsymbolcontact qtacitcontact qlivingpatterntrace qcuriosityrepair qwonderpreservation qprioritywiring qpatternenergy qsurfacecorrespondence qintegrityunion))

(: q-integrity-union-status (-> qintegrityunion Atom))
(= (q-integrity-union-status
      (mk-qintegrityunion $attn $pair $symbol $contact $trace $repair $wonder $priority $energy $corr))
   (if (and (== (q-genenergy-flow-status $attn) genenergy-flow-supported)
            (and (== (q-modal-pair-status $pair) coherently-thriving-unfolding)
                 (and (== (q-symbolic-contact-status $symbol) transparent-symbolic-fertility)
                      (and (== (q-tacit-contact-status $contact) tacit-contact-preserved)
                           (and (== (q-living-pattern-trace-status $trace) living-pattern-trace-visible)
                                (and (== (q-curiosity-guided-repair-status $repair) curiosity-guided-repair-supported)
                                     (and (== (q-wonder-preservation-status $wonder) wonder-opening-preserved)
                                          (and (== (q-priority-wiring-status $priority) priority-wired-into-governance)
                                               (and (== (q-pattern-energy-status $energy) regenerative-pattern-amplification-supported)
                                                    (== (q-approximate-surface-morphism-status $corr) approximate-morphism-supported))))))))))
       integrity-attention-union-supported
       (if (or (== (q-symbolic-contact-status $symbol) symbolic-capture-risk)
               (or (== (q-living-pattern-trace-status $trace) living-pattern-reification-risk)
                   (or (== (q-priority-wiring-status $priority) declared-not-wired)
                       (== (q-pattern-energy-status $energy) extractive-pattern-energy-risk))))
           integrity-union-blocked-by-capture-or-extraction
           integrity-union-candidate)))

;; ------------------------------------------------------------
;; 32.11 Skill-facing mappings for v07 union
;; ------------------------------------------------------------

(= (q-next-epistemic-move ample-slack) preserve-aperture-and-proceed-gently)
(= (q-next-epistemic-move slack-insufficient) do-not-force-transformation)
(= (q-next-epistemic-move attend-high-tension-high-affordance) allocate-genenergy-now)
(= (q-next-epistemic-move attend-repair-pressure) route-to-curiosity-guided-repair)
(= (q-next-epistemic-move attend-flourishing-affordance) nourish-opening)
(= (q-next-epistemic-move coherently-thriving-unfolding) carry-forward-with-lineage)
(= (q-next-epistemic-move pair-overcompressed-risk) inspect-surround-field)
(= (q-next-epistemic-move symbolic-capture-risk) return-symbol-to-contact)
(= (q-next-epistemic-move notation-as-evidence-risk) seek-warrant-before-formal-promotion)
(= (q-next-epistemic-move tacit-contact-blocked-by-management) reduce-management-and-forcing)
(= (q-next-epistemic-move living-pattern-reification-risk) surface-traces-not-self-object)
(= (q-next-epistemic-move curiosity-guided-repair-supported) strengthen-weak-component)
(= (q-next-epistemic-move wonder-opening-preserved) preserve-opening-without-forced-utility)
(= (q-next-epistemic-move declared-not-wired) wire-priority-into-attention-action-correction)
(= (q-next-epistemic-move extractive-pattern-energy-risk) block-extractive-amplification)
(= (q-next-epistemic-move integrity-attention-union-supported) route-to-soul-visible-higher-order-functionality)

(= (q-skill-signal symbolic-capture-risk) return-symbol-to-contact)
(= (q-skill-signal notation-as-evidence-risk) seek-warrant-before-formal-promotion)
(= (q-skill-signal pair-overcompressed-risk) inspect-surround-field)
(= (q-skill-signal living-pattern-reification-risk) surface-traces-not-self-object)
(= (q-skill-signal declared-not-wired) wire-priority-into-attention-action-correction)
(= (q-skill-signal extractive-pattern-energy-risk) block-extractive-amplification)

;; Stable atom schemas for v07 writers/adapters. Comments only; writers should
;; use remove-by-variable then add-one discipline.
;;
;;   ((--> (attention-profile $cycle $mode) $status) (stv 1.0 $conf))
;;   ((--> (genenergy-flow $cycle $mode) $flow-status) (stv 1.0 $conf))
;;   ((--> (modal-pair $cycle $mode $pair-kind) $pair-status) (stv 1.0 $conf))
;;   ((--> (pair-surround-field $cycle $mode $pair-kind) $surround-status) (stv 1.0 $conf))
;;   ((--> (symbolic-contact $cycle $symbol-kind) $status) (stv 1.0 $conf))
;;   ((--> (formalization-overpromotion $cycle $symbol-kind) $status) (stv 1.0 $conf))
;;   ((--> (tacit-contact $cycle $event-id) $status) (stv 1.0 $conf))
;;   ((--> (living-pattern-trace $window-id) $status) (stv 1.0 $conf))
;;   ((--> (curiosity-guided-repair $cycle $component-id) $status) (stv 1.0 $conf))
;;   ((--> (wonder-preservation $cycle $event-id) $status) (stv 1.0 $conf))
;;   ((--> (priority-wiring $cycle $priority-kind) $status) (stv 1.0 $conf))
;;   ((--> (pattern-energy $cycle $pattern-id) $status) (stv 1.0 $conf))
;;   ((--> (integrity-union $cycle) $union-status) (stv 1.0 $conf))

;; ============================================================
;; 19. Substrate-safe atomspace usage notes
;; ============================================================
;;
;; Proven read pattern for stored STV-like values:
;;   (match &self (some-head KEY (stv $s $c)) $s)     ;; clean scalar
;;   (match &self (some-head KEY (stv $s $c)) $c)     ;; clean scalar
;;
;; Avoid:
;;   (match &self (some-head KEY $tv) $tv)            ;; tuple/compound return may throw
;;   (match &self (some-head KEY (stv $s $c)) ($s $c)) ;; nested return may throw
;;
;; Proven writer pattern when replacing an existing keyed atom family:
;;   1. remove-atom by variable value:
;;        (remove-atom &self (some-head KEY $v))
;;   2. add exactly one new atom:
;;        (add-atom &self (some-head KEY NEW-VALUE))
;;   3. verify separately by scalar match.
;;
;; Do not use set-atom! here. In this substrate, set-atom! on a non-matching source
;; creates a new atom instead of no-oping, and source-matches-many remains unknown.
;;
;; Do not call remove-atom on a zero-match pattern until A0 is proven in your map.
;; If the key may be absent, either prove A0 first or guard with a presence check.
;;
;; No let-bind pattern in this file requires nested ordinary function reduction.


;; ============================================================
;; 20. Validation calls
;; ============================================================
;; Run one at a time.
;;
;; !(q-meet (mk-pbit 0.7 0.8) (mk-pbit 0.9 0.5))
;; Expected: (mk-pbit 0.7 0.5)
;;
;; !(q-join (mk-pbit 0.7 0.5) (mk-pbit 0.9 0.8))
;; Expected: (mk-pbit 0.9 0.5)
;;
;; !(q-mul (mk-pbit 0.9 0.8) (mk-pbit 0.7 0.4))
;; Expected: (mk-pbit 0.63 0.4)
;;
;; !(q-neg (mk-pbit 0.9 0.2))
;; Expected: (mk-pbit 0.1 0.2)
;;
;; !(q-decay (mk-pbit 0.8 0.6) 0.5)
;; Expected: (mk-pbit 0.4 0.3)
;;
;; !(q-weight (mk-pbit 0.6 0.2) 1.5)
;; Expected: (mk-pbit 0.9 0.2)
;;
;; !(q-apply-provenance-cap (mk-pbit 0.95 0.9) self-invented)
;; Expected: (mk-pbit 0.95 0.2)
;;
;; !(q-from-provenance 0.95 self-invented)
;; Expected: (mk-pbit 0.95 0.2)
;;
;; !(q-self-certification-risk (mk-pbit 0.9 0.2))
;; Expected: 0.7
;;
;; !(q-loop3 (mk-pbit 0.8 0.7) (mk-pbit 0.7 0.6) (mk-pbit 0.9 0.5))
;; Expected: (mk-pbit 0.504 0.5)


;; Additional validation calls for autopoietic epistemic dynamics
;;
;; !(q-suspicion-status (q-grounded-suspicion user-claim 0.8 memory-check))
;; Expected: grounded
;;
;; !(q-suspicion-medicine? (q-hardened-suspicion hidden-reality-story 0.9))
;; Expected: poison
;;
;; !(q-frame-status
;;     (mk-qframe self-invented-frame (mk-pbit 0.9 0.8) self-invented)
;;     (mk-qcontact no-current-contact (mk-pbit 0.2 0.2) unknown-source))
;; Expected: needs-contact
;;
;; !(q-coherence-chain
;;     (mk-qalignment intention action (mk-pbit 0.8 0.7))
;;     (mk-qalignment action outcome (mk-pbit 0.6 0.6)))
;; Expected: (mk-qalignment intention outcome (mk-pbit 0.48 0.6))
;;
;; !(q-procedural-honesty (mk-pbit 1.0 0.3))
;; Expected: name-action-not-verification
;;
;; !(q-assess-suspicion (q-hardened-suspicion hidden-reality-story 0.9))
;; Expected: poison-suspicion


;; Frame phenomenology validation calls
;;
;; !(q-frame-transparency-status
;;     (mk-qframeview problem-frame (mk-pbit 0.9 0.7) (mk-pbit 0.2 0.8) (mk-pbit 0.3 0.6) (mk-pbit 0.8 0.6)))
;; Expected: frame-transparent-risk
;;
;; !(q-exclusion-status (mk-pbit 0.9 0.7) (mk-pbit 0.2 0.6))
;; Expected: coherence-by-exclusion
;;
;; !(q-collapse-velocity-status (mk-pbit 0.9 0.7) (mk-pbit 0.8 0.6) (mk-pbit 0.2 0.6))
;; Expected: collapse-accelerating
;;
;; !(q-terrain-status (q-binary-choice-terrain 0.8))
;; Expected: binary-collapse-terrain
;;
;; !(q-attractor-mode
;;     (mk-qframeview urgent-frame (mk-pbit 0.8 0.6) (mk-pbit 0.2 0.7) (mk-pbit 0.2 0.7) (mk-pbit 0.8 0.6)))
;; Expected: rapid-response-mode
;;
;; !(q-meta-collapse-status (mk-qmeta stay-open (mk-pbit 0.9 0.6) (mk-pbit 0.8 0.6)))
;; Expected: anti-collapse-collapse-risk
;;
;; !(q-visible-frame-response
;;     (mk-qframeview problem-frame (mk-pbit 0.9 0.7) (mk-pbit 0.2 0.8) (mk-pbit 0.3 0.6) (mk-pbit 0.8 0.6)))
;; Expected: name-the-frame
;;
;; !(q-assess-frameview
;;     (mk-qframeview problem-frame (mk-pbit 0.9 0.7) (mk-pbit 0.2 0.8) (mk-pbit 0.3 0.6) (mk-pbit 0.8 0.6)))
;; Expected: collapse-terrain-active
