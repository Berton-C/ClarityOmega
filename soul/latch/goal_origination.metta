;; Goal Origination Engine - proposes goals from AtomSpace cross-connections
;; Runs during REASON cycles to find bridges neither human nor agent predicted

;; Stage 1: Find all two-hop bridges across domains
(= (find-bridge $a $c $bridge)
   (match &self ((--> $a $bridge) (stv $f1 $c1))
     (match &self ((--> $bridge $c) (stv $f2 $c2))
       (bridge-found $a $c $bridge (stv (* $f1 $f2) (min $c1 $c2))))))

;; Stage 2: Filter for cross-domain bridges only
;; A bridge is cross-domain when start and end belong to different topic clusters
(= (cross-domain-bridge $a $c $bridge $tv)
   (find-bridge $a $c $bridge $tv))

;; Stage 3: Score candidates by novelty and confidence
;; Higher confidence bridges that connect distant concepts score highest
(= (goal-candidate-score $a $c $bridge (stv $f $conf))
   (cross-domain-bridge $a $c $bridge (stv $f $conf)))

;; Stage 4: Package as proposable goal
(= (propose-goal $candidate)
   (match &self (goal-candidate-score $a $c $bridge (stv $f $conf))
     (proposed-goal (explore-connection $a $c) (via $bridge) (confidence $conf))))

;; Integration: call from REASON cycle
(= (reason-cycle-goal-origination)
   (propose-goal all))
