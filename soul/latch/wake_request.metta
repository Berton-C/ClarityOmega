;; Wake Cycle Request Mechanism - Clarity requesting wake from inside AtomSpace
;; When agent has pending work, it sets wake-requested to signal the orchestrator

(= (wake-requested) False)
(= (wake-reason) idle)

;; Goal origination function: find cross-connections that suggest new goals
(= (cross-connect-goal-candidate $domain1 $domain2)
   (match &self ((--> $a $b) (stv $f1 $c1))
     (match &self ((--> $b $c) (stv $f2 $c2))
       (goal-candidate $a $c (bridge $b) (min-conf (min $c1 $c2))))))

;; Wake request rule: if goal-candidates exist and state is IDLE, request wake
(= (should-wake)
   (if (== (wake-requested) False)
     (match &self (goal-candidate $from $to $bridge $conf)
       (wake-needed (new-goal $from $to via $bridge)))))
