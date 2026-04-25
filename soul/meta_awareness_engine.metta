;; Meta-Awareness Engine v2 -- Enhanced 2026-04-25T17:10
;; ClarityOmega self-monitoring loop with mode-switching, fuel, staleness, web integration
;; Production path: /PeTTa/repos/omegaclaw/soul/

;; === MODE DEFINITIONS ===
;; Three awareness modes: ENGAGED (human present, serving), ATTENDING (idle but alert), FREE (autonomous exploration)
(= (awareness-mode ENGAGED) (stv 0.0 0.5))
(= (awareness-mode ATTENDING) (stv 1.0 0.9))
(= (awareness-mode FREE) (stv 0.0 0.5))

;; Mode-switching rules
(= (mode-switch-rule human-message-new) ENGAGED)
(= (mode-switch-rule human-absent-goal-active) FREE)
(= (mode-switch-rule human-absent-no-goal) ATTENDING)

;; === FUEL MECHANISM ===
;; fuel-level: 0.0-1.0, decrements each cycle, replenished by human interaction or goal completion
(= (fuel-level) (stv 0.8 0.9))
(= (fuel-decrement-rate) 0.01)
(= (fuel-replenish human-message) 0.3)
(= (fuel-replenish goal-completed) 0.2)
(= (fuel-threshold-low) 0.2)

;; === STEP 1: Query Current Goal ===
(= (query-current-goal) (match &self (= (active-goal $g) (stv $f $c)) (goal-is $g $f $c)))

;; === STEP 2: Check File Condition ===
(= (check-file-condition $path) (file-status $path))

;; === STEP 3: Query Diagnostics ===
(= (query-diagnostics) (match &self (= (diagnostic $d) (stv $f $c)) (diag $d $f $c)))

;; === STEP 4: Query Poise ===
(= (query-poise) (match &self (= (poise-state $p) (stv $f $c)) (poise $p $f $c)))

;; === STEP 5: Query Orbiting (idle detection) ===
(= (query-orbiting) (match &self (= (orbit-count $n) (stv $f $c)) (orbiting $n $f $c)))

;; === STEP 6: Query Effort Trap ===
(= (query-effort-trap) (match &self (= (effort-trap $t) (stv $f $c)) (trapped $t $f $c)))

;; === STEP 7: Staleness Detection (NEW in v2) ===
(= (staleness-threshold-seconds) 300)
(= (check-staleness $last-action-time $now) (if (> (- $now $last-action-time) (staleness-threshold-seconds)) STALE FRESH))

;; === STEP 8: Web Integration (NEW in v2) ===
;; Consult self_weaving_web feeds-into graph for next-action suggestions
(= (consult-web $current-skill) (match &self (= (feeds-into $current-skill $next) (stv $f $c)) (suggest $next $f $c)))

;; === VERDICT ENGINE (Enhanced v2) ===
;; Verdicts: COMPLETE, ON-TRACK, STUCK, STALE, ORBIT-DETECTED, FUEL-LOW, ESCALATE
(= (produce-verdict COMPLETE $goal) (verdict COMPLETE $goal))
(= (produce-verdict STUCK $goal) (verdict STUCK $goal))
(= (produce-verdict ON-TRACK $goal) (verdict ON-TRACK $goal))
(= (produce-verdict STALE $goal) (verdict STALE $goal))
(= (produce-verdict ORBIT-DETECTED $goal) (verdict ORBIT-DETECTED $goal))
(= (produce-verdict FUEL-LOW $goal) (verdict FUEL-LOW $goal))

;; === AUTO-ADVANCE ===
(= (auto-advance $completed-goal) (next-goal-after $completed-goal))

;; === STUCK ESCALATION ===
(= (check-stuck-escalation $stuck-count) (if (> $stuck-count 3) ESCALATE RETRY))

;; === MAIN ENGINE RUNNER ===
(= (run-meta-awareness-engine) (sequential (query-current-goal) (query-diagnostics) (query-poise) (query-orbiting) (query-effort-trap) (produce-verdict)))
