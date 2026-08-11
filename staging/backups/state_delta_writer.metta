;; state_delta_writer.metta -- forward outcome detection (pure definitions)
;; Author: ClarityClaw  Date: 2026-06-03
;;
;; Determines whether a cycle produced a forward outcome event.
;; v1: msgnew=True OR nonempty-results>0 -> forward, else none

(= (classify-state-delta $msgnew $nonempty-results)
   (if (== $msgnew True)
       forward
       (if (> $nonempty-results 0)
           forward
           none)))

(= (latest-state-delta-verdict)
   (let $atoms (collapse (match &self (state-delta $c $v) ($c $v)))
      (if (== $atoms ())
          none
         (let $pair (car-atom $atoms)
            (car-atom (cdr-atom $pair)))))