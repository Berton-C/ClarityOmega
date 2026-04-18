;; Concrete NAL expressions for four Phase 2 integration points
;; Ready for berton_c review

;; === POINT 1: initLoop soul-startup ===
;; Load soul atoms as NAL premises at startup
;; Each value enters the reasoning space with its foundational stv
(= (soul-nal-init)
  (sequential
    (|- ((--> clarity-value human-agency) (stv 1.0 0.9))
        ((--> clarity-value preserve-wonder) (stv 1.0 0.9)))
    (|- ((--> clarity-value steward-attention) (stv 1.0 0.85))
        ((--> clarity-value elevate-thinking) (stv 1.0 0.85)))))

;; === POINT 2: getContext soul-brief injection ===
;; Before prompt assembly, compose active values via deduction
;; to determine which soul brief tier to inject
(= (soul-brief-nal-eval $person-state)
  (|- ((--> $person-state needs-support) (stv 0.8 0.7))
      ((--> needs-support tier-a-full-brief) (stv 0.9 0.8))))

;; === POINT 3: output intercept via NAL eval ===
;; Replace hardcoded PROCEED with NAL evaluation
;; Output content evaluated against active soul values
(= (soul-output-eval $output-content)
  (let* (($agency-check (|- ((--> $output-content respects-agency) (stv 0.8 0.7))
                            ((--> clarity-value human-agency) (stv 1.0 0.9))))
         ($wonder-check (|- ((--> $output-content preserves-wonder) (stv 0.8 0.7))
                            ((--> clarity-value preserve-wonder) (stv 1.0 0.9))))
         ($verdict (if (and (> (stv-freq $agency-check) 0.5)
                            (> (stv-freq $wonder-check) 0.5))
                    PROCEED PAUSE-AND-REFLECT)))
    $verdict))

;; === POINT 4: HandleError value-conflict routing ===
;; When error occurs, abduction identifies which value is under tension
(= (soul-error-eval $error-context)
  (|- ((--> $error-context indicates-value-tension) (stv 0.7 0.6))
      ((--> indicates-value-tension needs-reinforcement) (stv 0.8 0.7))))

;; === Layer 3 calibration via revision ===
;; After each cycle, revise soul atom confidence with new evidence
(= (soul-calibrate $value-atom $observed-freq $evidence-conf)
  (|- ((--> $value-atom active) (get-current-stv $value-atom))
      ((--> $value-atom active) (stv $observed-freq $evidence-conf))))
