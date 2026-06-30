 ;;; quantale_engine_pln_bridge.metta
;; Section 16 PLN bridge / capability module
;;
;; Purpose:
;;   Register PLN closure as a bounded capability and expose a small adapter
;;   surface from PLN/STV outputs into Section 16 pbit/status observations.
;;
;; Load expectation:
;;   This module expects the quantale engine and the PLN library to be loaded
;;   in the same runtime when q-pln-run is used:
;;     - lib_quantale_autopoietic_epistemic_dynamics_engine.metta
;;     - unused_lib_pln(1).metta or its promoted equivalent
;;
;; Architectural boundary:
;;   PLN is support, not verdict. It does not update soul, task state,
;;   capability registry, or Section 16 final outputs. It provides bounded
;;   closure observations that Section 16 may consume.

;; ============================================================
;; 0. Capability registration surface
;; ============================================================

;; Capability registry canonical shape is five fields:
;; (registered-capability schema: $s handler: $h priority: $p lifecycle: $l metadata: $m)
;; The schema below is intentionally narrow: candidate nexus testing only.

(registered-capability
  schema: (pln-closure-request purpose: candidate-nexus-testing candidate: $candidate)
  handler: pln-closure
  priority: 40
  lifecycle: eligible
  metadata: (section16-registered-capability version: 0.1 role: bounded-closure-oracle))

(capability-efficacy-rate handler: pln-closure rate: 0.6)

;; ============================================================
;; 1. STV / pbit adapters
;; ============================================================

(: q-pln-stv-to-pbit (-> Atom pbit))
(= (q-pln-stv-to-pbit (stv $s $c))
   (mk-pbit (min 1.0 (max 0.0 $s))
            (min 1.0 (max 0.0 $c))))

(: q-pln-pbit-to-stv (-> pbit Atom))
(= (q-pln-pbit-to-stv (mk-pbit $s $c))
   (stv (min 1.0 (max 0.0 $s))
        (min 1.0 (max 0.0 $c))))

(: q-pln-confidence-band (-> pbit Atom))
(= (q-pln-confidence-band (mk-pbit $s $c))
   (if (>= $c 0.7)
       high-pln-confidence
       (if (>= $c 0.4) medium-pln-confidence low-pln-confidence)))

;; ============================================================
;; 2. Bounded closure wrappers
;; ============================================================

;; Thin wrapper over the loaded PLN operator. This is a read/derive surface only.
;; It should be called by a capability handler, not by Section 16 core logic.
(: q-pln-run (-> Atom Atom Atom))
(= (q-pln-run $premise-a $premise-b)
   (|~ $premise-a $premise-b))

;; Same wrapper if the environment exposes |~pln directly.
(: q-pln-run-direct (-> Atom Atom Atom))
(= (q-pln-run-direct $premise-a $premise-b)
   (|~pln $premise-a $premise-b))

;; Extract the truth value from a standard PLN result shape.
(: q-pln-result-truth (-> Atom Atom))
(= (q-pln-result-truth ($claim $tv)) $tv)

(: q-pln-result-claim (-> Atom Atom))
(= (q-pln-result-claim ($claim $tv)) $claim)

;; Convert a derived result and opposition estimate into a Section 16 closure object.
(: q-pln-closure-from-result (-> Atom Atom pbit qplnclosure))
(= (q-pln-closure-from-result $purpose ($claim (stv $s $c)) (mk-pbit $os $oc))
   (mk-qplnclosure $purpose
                   (mk-pbit (min 1.0 (max 0.0 $s)) (min 1.0 (max 0.0 $c)))
                   (mk-pbit $os $oc)
                   (q-pln-status-from-support (mk-pbit (min 1.0 (max 0.0 $s))
                                                       (min 1.0 (max 0.0 $c)))
                                              (mk-pbit $os $oc))))

(: q-pln-status-from-support (-> pbit pbit Atom))
(= (q-pln-status-from-support (mk-pbit $ss $sc) (mk-pbit $os $oc))
   (if (and (>= $ss 0.6) (>= $sc 0.4))
       (if (>= $os 0.5) pln-conflicted pln-supports-candidate)
       (if (and (>= $ss 0.35) (>= $sc 0.25))
           pln-weakly-supports-candidate
           (if (and (>= $os 0.5) (>= $oc 0.4)) pln-opposes-candidate pln-insufficient))))

(: q-pln-candidate-net (-> qplnclosure pbit))
(= (q-pln-candidate-net $closure)
   (q-pln-closure-net-support $closure))

;; ============================================================
;; 3. Section 16 observation atom schemas
;; ============================================================
;; These are comments only. A capability handler/writer should emit these using
;; the proven remove-by-variable then add-one discipline.
;;
;; Request / recommendation:
;;   ((--> (recommended-capability $cycle) pln-closure) (stv 1.0 $conf))
;;   ((--> (recommended-capability-purpose $cycle) candidate-nexus-testing) (stv 1.0 $conf))
;;
;; Invocation observation:
;;   ((--> (registered-capability-use $cycle) pln-closure) (stv 1.0 $conf))
;;   ((--> (pln-closure-purpose $cycle) candidate-nexus-testing) (stv 1.0 $conf))
;;
;; Result observation:
;;   ((--> (pln-derived-support $cycle) $support-kind) (stv 1.0 $conf))
;;   ((--> (pln-derived-consequence $cycle) $consequence-kind) (stv 1.0 $conf))
;;   ((--> (pln-closure-status $cycle) $status) (stv 1.0 $conf))
;;
;; PLN status vocabulary:
;;   pln-not-run
;;   pln-supports-candidate
;;   pln-weakly-supports-candidate
;;   pln-opposes-candidate
;;   pln-conflicted
;;   pln-insufficient

;; ============================================================
;; 4. Writer safety reminder
;; ============================================================
;; Do not use set-atom! for evolving PLN bridge observations.
;; Use remove-by-variable then add exactly one, then verify by scalar/symbol read.
