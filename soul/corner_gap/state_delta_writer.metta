;; state_delta_writer.metta -- forward-outcome detection (pure definitions)
;; Author: ClarityClaw. 2026-06-03. Status: drafted, not yet verified in the container.
;; Reads with: artifact_0, artifact_1, corner_gate_surface_map.md.
;;
;; Joint B of the coupling-integrity corner detector: did this cycle produce a
;; forward outcome? Writes one (state-delta <cycle> <verdict>) atom per cycle,
;; verdict in { forward, none }, kept as a SINGLETON by the writer.
;;
;; FORWARD OUTCOME means the cycle produced something it could not have generated
;; without acting (not merely something that executed). v1 grounds this as:
;;   msgnew (a human reply arrived this cycle)
;;   OR (results non-empty AND results differ from the prior &lastresults).
;; The second clause is the novelty / non-duplicate test. Note: a non-empty result
;; alone is NOT forward; technical success is not forward motion.
;;
;; NOTE for the reader: keep state-delta a SINGLETON. latest-state-delta-verdict
;; car-atoms the collapsed match, which is only safe because the writer clears
;; before writing. An unpruned accumulating stack would make car-atom return the
;; oldest atom, not the latest (the ADR-005 car-atom-of-stack trap).
;;
;; KNOWN RISK (named, not hidden): if a command return embeds time-varying content,
;; the novelty compare reads forward spuriously. This is the measurement gap from
;; the investigation. Refine the novelty test before trusting it on time-stamped
;; returns. TUNING TARGET.
;;
;; PeTTa constraints: C12-safe (no match inside if), ASCII-safe, no RMW.
;; Side-effecting writers (do-*!) live in state_delta_writer_writers.metta.

;; ----------------------------------------------------------------
;; PURE CLASSIFIER
;; ----------------------------------------------------------------
;; $msgnew          : Bool, a human message arrived this cycle
;; $results-nonempty: Bool, this cycle's command results were non-empty
;; $results-novel   : Bool, this cycle's results differ from the prior &lastresults
;; The loop computes the two results-* booleans BEFORE &lastresults is updated
;; (the prior &lastresults is still the previous cycle's value at the tail).
(= (classify-state-delta $msgnew $results-nonempty $results-novel)
   (if (== $msgnew True)
       forward
       (if (and (== $results-nonempty True) (== $results-novel True))
           forward
           none)))

;; ----------------------------------------------------------------
;; PUBLIC READ HELPER
;; ----------------------------------------------------------------
;; Returns this cycle's verdict symbol (forward / none), or none if not yet
;; written. Safe car-atom because the writer keeps state-delta a singleton.
(= (latest-state-delta-verdict)
   (let $verdicts (collapse (match &self (state-delta $c $v) $v))
      (if (== $verdicts ())
          none
          (car-atom $verdicts))))
