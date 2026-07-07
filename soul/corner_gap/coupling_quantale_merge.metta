;; coupling_quantale_merge.metta -- graded corner merge via the quantale engine (pure)
;; Author: ClarityClaw. Granularity-layer reference draft 2026-06-03.
;; Predecessors: investigation 2026-06-03 v2, coupling_integrity_detector.metta,
;;   lib_quantale.metta.
;;
;; WHAT THIS FILE IS. The granularity code that makes the quantale engine useful for the
;; corner gate. It converts the three coupling joints from booleans into graded
;; pbits and merges them with q-meet (the graded crisp-AND). This is the v2
;; graduation of coupling-verdict that Clarity flagged she would consider if the
;; v1 boolean crisp-AND produced false positives. v1 stays the safe default.
;;
;; WHY QUANTALE AND NOT NAL REVISION (Q1). q-meet is stateless: min strength, min
;; confidence, no persistence, no decay latency. That sidesteps exactly the
;; latency risk Clarity raised about NAL revision (confidence might not decay fast
;; enough in a corner). It adds confidence tracking for free over the boolean AND
;; without adding a tuning surface beyond the single fire threshold.
;;
;; DEPENDS ON: the v08.7.2 quantale engine (mk-pbit, q-meet, q-neg; op bodies
;; verified identical to retired lib_quantale, 2026-07-07), q-geq from
;; lib_self_continuity, the counts in coupling_integrity_detector.metta
;; (count-actions-in-window, count-person-actions, count-system-actions), and
;; state_delta_writer.metta (latest-state-delta-verdict).
;;
;; CONFIRMED (engine-only inline probe, 2026-07-07): the full chain reduces with
;; lib_quantale absent; corner-pbit-core and corner-confirmed-core exact-match.
;;
;; PeTTa constraints: C12-safe, ASCII-safe, no RMW.

;; ----------------------------------------------------------------
;; LOCAL UTILITY (shared by the continuity probe)
;; ----------------------------------------------------------------
;; Safe ratio: 0 when denominator is not positive. (unused_lib_pln has /safe; kept
;; local to avoid pulling in a second reasoning engine.)
(= (safe-ratio $a $b)
   (if (> $b 0) (/ $a $b) 0))

;; ----------------------------------------------------------------
;; JOINT PBITS (graded)
;; ----------------------------------------------------------------

;; Joint A, emission as a GATE pbit: full strength if any real action this window,
;; else zero. A zero here drives the whole meet to zero, which is composure (rest).
(= (emission-pbit)
   (if (> (count-actions-in-window) 0)
       (mk-pbit 1.0 0.9)
       (mk-pbit 0.0 0.9)))

;; Joint B, outcome-flat pbit: high when NO forward outcome this cycle.
;; Forward => not flat (strength 0). None => flat (strength 1, lower confidence
;; because absence of evidence is weaker than presence).
(= (outcome-flat-pbit)
   (if (== (latest-state-delta-verdict) forward)
       (mk-pbit 0.0 0.9)
       (mk-pbit 1.0 0.7)))

;; Joint C, intention-decoupled pbit: strength = system-share of actions; high
;; means phantom / system-driven. Confidence grows with how many actions inform
;; the ratio (capped). No actions => zero strength, zero confidence (no data).
;; NOTE: a strength threshold of 0.6 on the merged corner-pbit makes this require
;; system-share >= 0.6, matching agency_balance_guard's dependency-threshold.
(= (intention-decoupled-pbit)
   (let* (($p (count-person-actions))
          ($s (count-system-actions))
          ($total (+ $p $s)))
      (if (> $total 0)
          (mk-pbit (safe-ratio $s $total) (min 0.9 (safe-ratio $total 5)))
          (mk-pbit 0.0 0.0))))

;; ----------------------------------------------------------------
;; CORE CORNER PBIT (graded crisp-AND of the three joints)
;; ----------------------------------------------------------------
;; q-meet takes the minimum strength and minimum confidence. Corner strength is
;; high only when emission AND outcome-flat AND decoupled are all high. This arm
;; catches BOTH repetition and varied flailing, because neither requires the
;; behavior-stasis signal (that lives in the continuity probe as a second arm).
(= (corner-pbit-core)
   (q-meet (emission-pbit)
           (q-meet (outcome-flat-pbit)
                   (intention-decoupled-pbit))))

;; ----------------------------------------------------------------
;; FIRE THRESHOLD (per-cycle graded gate)
;; ----------------------------------------------------------------
;; q-geq requires BOTH strength >= and confidence >= the threshold, so the gate
;; will not fire on low-data cycles (confidence gates on action volume via Joint C).
;; TUNING TARGET: the threshold pbit. 0.6 strength matches the dependency-threshold;
;; 0.5 confidence requires a few actions of evidence.
(= (corner-threshold-pbit) (mk-pbit 0.6 0.5))

(= (corner-confirmed-core)
   (q-geq (corner-pbit-core) (corner-threshold-pbit)))
