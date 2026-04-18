; === Mutation Lock Upgrade Draft ===
; Problem 1: car-atom only checks first command in response
; Fix: iterate ALL commands in parsed sexpr, check each for soul namespace
;
; (= (soul-mutation-scan $cmd-list)
;   (if (== $cmd-list ())
;     CLEAN
;     (let* (
;       ($head (car-atom $cmd-list))
;       ($tail (cdr-atom $cmd-list))
;       ($check (soul-targets-soul-namespace $head))
;     )
;     (if (== $check True)
;       SOUL-NAMESPACE-MUTATION-DETECTED
;       (soul-mutation-scan $tail)))))
;
; Problem 2: No rollback on conflict - execution continues
; Fix: when conflict detected, replace offending command with no-op
;
; (= (soul-mutation-gate $cmd-list)
;   (if (== (soul-mutation-scan $cmd-list) CLEAN)
;     $cmd-list
;     (soul-strip-soul-commands $cmd-list)))
;
; soul-strip-soul-commands returns cmd-list with soul-targeting
; commands replaced by (pin reason-string), preserving non-soul commands