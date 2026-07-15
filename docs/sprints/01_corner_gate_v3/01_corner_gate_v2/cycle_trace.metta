;; === cycle_trace.metta ===
;; DRAFT for Clarity's analysis. Destination: soul/cycle_trace.metta (new
;; file, build step B2, import line in lib_clarity_reasoning manifest).
;;
;; The unconditional per-cycle command trace: the shared producer behind the
;; detection mesh (design doc Section 11B). PURE READS ONLY. Side-effecting
;; writers (do-*!) land in cycle_trace_writers.metta (Discipline 6A).
;;
;; Atom shape (written by cycle_trace_writers.metta):
;;   (cycle-cmd $cycle-id $cmd-repr)
;; One atom per proposed command per cycle, windowed and pruned. Records
;; PROPOSALS mechanically (P5: counting and recording, never inferring).

;; Window size (cycles retained).
(= (cycle-trace-window) 10)

;; Total command atoms currently in the window.
(= (cmds-in-window)
   (size-atom (collapse (match &self (cycle-cmd $c $r) $r))))

;; How many times one exact command form appears in the window.
(= (cmd-repeat-count $repr)
   (size-atom (collapse (match &self (cycle-cmd $c $repr) $c))))

;; Dominant signature: the most-repeated command form and its count.
;; Single-head recursion, dispatch via if on () (P3 fork precedent: no
;; overlapping heads). Duplicate reprs in the list cause redundant recount;
;; harmless at window scale (<= ~30 elements). Returns (none 0) when empty.
(= (max-repeat-acc $list $best-r $best-n)
   (if (== $list ())
       ($best-r $best-n)
       (let* (($h (car-atom $list))
              ($t (cdr-atom $list))
              ($n (cmd-repeat-count $h)))
             (if (> $n $best-n)
                 (max-repeat-acc $t $h $n)
                 (max-repeat-acc $t $best-r $best-n)))))

(= (dominant-signature)
   (let $reprs (collapse (match &self (cycle-cmd $c $r) $r))
        (if (== $reprs ())
            (none 0)
            (max-repeat-acc $reprs none 0))))
