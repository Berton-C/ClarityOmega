;; soul/cycle_classifier.metta
;; Per-cycle behavioral classifier for recent-action populator
;;
;; Takes the parsed command list ($sexpr) from an iteration plus the $msgnew
;; flag (was there a new human message this cycle), produces:
;;   - $action-type: a composite tag describing the cycle's behavioral signature
;;   - $description: a short evidence string for the orbit detector to match against
;;
;; Six composite tags per Clarity's design (May 3, 2026):
;;   - responsive-send     : send fired in response to a human message
;;   - status-send-unprompted : send fired with no preceding human message
;;   - verification-query  : metta or shell command that checks state
;;   - exploration-query   : metta/query not tied to a human request
;;   - pin-only            : cycle contained only pin commands, no outward action
;;   - claim-send          : send containing assertions about state or results
;;
;; Pattern note (May 3, 2026): Helper predicates use the (any (collapse ...))
;; idiom established in soul_utils.metta lines 42, 143 and soul_kernel.metta line 383.
;; Earlier draft used (== (collapse ...) ()) which had a collapse-semantics trap
;; (collapse of () markers does not return () but a list of () markers).
;; Clarity's review caught the issue; rewrite verified against three independent
;; uses of the idiomatic pattern in existing soul/ code.
;;
;; Network: SN (orbit detection input) and future SWITCH-HUB (work-burst classification).

;; --- Helper predicates: command type detection ---

;; Check if a command list contains any send command
(= (cycle-has-send? $cmds)
   (any (collapse (let $c (superpose $cmds)
                    (== (car-atom $c) send)))))

;; Check if a command list contains any metta command
(= (cycle-has-metta? $cmds)
   (any (collapse (let $c (superpose $cmds)
                    (== (car-atom $c) metta)))))

;; Check if a command list contains any query command
(= (cycle-has-query? $cmds)
   (any (collapse (let $c (superpose $cmds)
                    (== (car-atom $c) query)))))

;; Check if a command list contains any shell command
(= (cycle-has-shell? $cmds)
   (any (collapse (let $c (superpose $cmds)
                    (== (car-atom $c) shell)))))

;; Check if a command list contains any pin command
(= (cycle-has-pin? $cmds)
   (any (collapse (let $c (superpose $cmds)
                    (== (car-atom $c) pin)))))

;; Check if cycle contains only pin commands (no send, metta, query, shell)
(= (cycle-is-pin-only? $cmds)
   (and (cycle-has-pin? $cmds)
        (and (not (cycle-has-send? $cmds))
             (and (not (cycle-has-metta? $cmds))
                  (and (not (cycle-has-query? $cmds))
                       (not (cycle-has-shell? $cmds)))))))

;; --- Main classifier: produces composite action-type tag ---

;; classify-cycle-action-type returns one of the six composite tags
;; based on command set and human-message presence
(= (classify-cycle-action-type $cmds $msgnew)
   (if (cycle-is-pin-only? $cmds)
       pin-only
       (if (cycle-has-send? $cmds)
           (if $msgnew
               responsive-send
               status-send-unprompted)
           (if (or (cycle-has-metta? $cmds) (cycle-has-shell? $cmds))
               (if $msgnew
                   verification-query
                   exploration-query)
               (if (cycle-has-query? $cmds)
                   exploration-query
                   unclassified)))))

;; --- Description: short evidence string from first command ---

;; classify-cycle-description returns a short string summarizing what the cycle did
;; Takes the first command's full form (truncated by Python helper later if needed)
(= (classify-cycle-description $cmds)
   (if (== $cmds ())
       ""
       (car-atom $cmds)))
