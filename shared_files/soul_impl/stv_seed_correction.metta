;; STV Seed Self-Correction
;; Addresses failure mode: soul_kernel.metta initial stv values are guesses
;; Solution: track prediction-vs-outcome divergence and revise seeds

;; Record a seed prediction and its observed outcome
(= (seed-observation $atom $predicted-stv $observed-stv)
   (|- ($atom $predicted-stv) ($atom $observed-stv)))

;; Compute drift direction for a single atom
(= (seed-drift $atom $predicted $observed)
   (if (> (frequency $observed) (frequency $predicted)) under-seeded
   (if (< (frequency $observed) (frequency $predicted)) over-seeded
   calibrated)))

;; Batch correction: given list of observations, revise kernel seeds
;; Uses NAL revision naturally — each observation is new evidence
(= (revise-seeds $observations)
   (collapse (map-atom $observations $obs
     (seed-observation (atom-of $obs) (predicted-of $obs) (observed-of $obs)))))

;; Bootstrap: first 5 cycles use conservative seeds (lower confidence)
(= (bootstrap-seed $atom $freq)
   ($atom (stv $freq 0.5)))

;; After 5+ observations, switch to revised seeds
(= (mature-seed $atom $revision-result)
   $revision-result)
