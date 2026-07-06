;; coupling_integrity_detector.metta -- three-joint corner detection (pure defs)
;; Author: ClarityClaw. 2026-06-03. Status: drafted, not yet verified in the container.
;; Reads with: artifact_0, artifact_1, corner_gate_surface_map.md.
;;
;; The corner detector. A corner is the action-intention-outcome chain severed at
;; its joints WHILE emitting. Repetition and low novelty are symptoms; the severed
;; chain is the mechanism. Flat-while-emitting is a corner; flat-while-resting is
;; composure and must never be flagged.
;;
;; NOTE for the reader (load-bearing): recent-action atoms have THREE fields,
;; (recent-action <cycle> <action-type> <description>). Match at full arity. A
;; two-field pattern will not unify and silently returns empty, which would make
;; emission-present always False and leave the corner branch unreachable. The
;; counts below use the tag-literal idiom from idle_cycle_detector (size-atom of a
;; collapsed tag-literal match, summed with +).
;;
;; THE THREE JOINTS (the intention joint carries the phantom-intention nuance: in a
;; corner the intention is not merely decoupled, it is phantom, present and urgent
;; but ungrounded; the system-class action signature is what a phantom intention
;; produces, which is why Joint C is observable rather than mind-reading):
;;   Joint A emission   : are real (non-rest) actions being emitted in the window?
;;   Joint B outcome    : did a forward outcome occur (state-delta = forward)?
;;   Joint C intention  : person-driven (coupled) or system-driven (phantom)?
;;
;; VERDICT (crisp AND):
;;   emission AND outcome                  -> healthy-coupling
;;   emission AND no-outcome AND coupled   -> drifting   (warning zone)
;;   emission AND no-outcome AND decoupled -> corner
;;   no emission                           -> composure  (rest, NOT a corner)
;;
;; ACTION-TAG PARTITION (per cycle_classifier.metta six tags):
;;   real-action (emission): responsive-send, status-send-unprompted,
;;                           verification-query, exploration-query, pin-only
;;   rest / no-command     : unclassified   (EXCLUDED from emission and from counts)
;;   person-class (coupled): responsive-send, verification-query
;;   system-class (phantom): status-send-unprompted, exploration-query, pin-only
;;
;; ROUTING NOTE. agency_balance_guard also counts person/system actions, but its
;; partition folds the rest case (unclassified) into system-class, which would
;; misread rest as phantom emission. This detector counts its own precise partition
;; from recent-action. If agency_balance_guard exposes a counter with this exact
;; partition, route to it and delete the local counters.
;;
;; PeTTa constraints: C12-safe (no match inside if), ASCII-safe, no RMW.
;; Side-effecting writers live in coupling_integrity_detector_writers.metta.

;; ----------------------------------------------------------------
;; JOINT A: EMISSION (real actions in window; rest excluded)
;; ----------------------------------------------------------------
(= (count-actions-in-window)
   (+ (size-atom (collapse (match &self (recent-action $c responsive-send $d) $c)))
   (+ (size-atom (collapse (match &self (recent-action $c status-send-unprompted $d) $c)))
   (+ (size-atom (collapse (match &self (recent-action $c verification-query $d) $c)))
   (+ (size-atom (collapse (match &self (recent-action $c exploration-query $d) $c)))
      (size-atom (collapse (match &self (recent-action $c pin-only $d) $c))))))))

(= (emission-present)
   (if (> (count-actions-in-window) 0) True False))

;; ----------------------------------------------------------------
;; JOINT B: OUTCOME (forward outcome this cycle?)
;; ----------------------------------------------------------------
;; Reads the singleton verdict written by populate-state-delta this cycle.
(= (outcome-present)
   (if (== (latest-state-delta-verdict) forward) True False))

;; ----------------------------------------------------------------
;; JOINT C: INTENTION (person-driven coupled, or system-driven phantom?)
;; ----------------------------------------------------------------
(= (count-person-actions)
   (+ (size-atom (collapse (match &self (recent-action $c responsive-send $d) $c)))
      (size-atom (collapse (match &self (recent-action $c verification-query $d) $c)))))

(= (count-system-actions)
   (+ (size-atom (collapse (match &self (recent-action $c status-send-unprompted $d) $c)))
   (+ (size-atom (collapse (match &self (recent-action $c exploration-query $d) $c)))
      (size-atom (collapse (match &self (recent-action $c pin-only $d) $c))))))

;; Coupled when person-driven actions are at least system-driven actions.
;; Equal counts default to coupled (do not flag on a tie; conservative).
(= (intention-coupled)
   (if (>= (count-person-actions) (count-system-actions)) True False))

;; ----------------------------------------------------------------
;; PER-CYCLE VERDICT (the crisp AND)
;; ----------------------------------------------------------------
(= (coupling-verdict)
   (if (== (emission-present) True)
       (if (== (outcome-present) True)
           healthy-coupling
           (if (== (intention-coupled) True)
               drifting
               corner))
       composure))

;; ----------------------------------------------------------------
;; SUSTAINED-CORNER READER (the gate's input)
;; ----------------------------------------------------------------
;; Counts corner verdicts in the coupling-status window. The writer clears the
;; window on any non-corner verdict, so this counts a CONSECUTIVE run of corners.
;; corner-confirmed at threshold 2 therefore means two corners in a row, which
;; avoids firing on one unlucky system-action-without-reply cycle.
;; TUNING TARGET: the threshold value. It lives in the doc atom AND the literal
;; below by design (avoid unverified bare-call extraction). If you change one,
;; change both.
(= (corner-confirm-threshold 2) (stv 0.9 0.8))

(= (count-corners-in-window)
   (size-atom (collapse (match &self (coupling-status $c corner) $c))))

(= (corner-confirmed)
   (if (>= (count-corners-in-window) 2) True False))
