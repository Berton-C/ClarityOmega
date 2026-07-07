;; corner_window_writers.metta -- confirmed-corner command record (writers)
;; V2-MONOLITH 2026-07-06. Discipline 6A: pure readers (cmd-in-corner-window?,
;; filter-corner-cmds) live in corner_gate.metta; writers live here.
;; Record is CONFIRMATION-SCOPED and EPHEMERAL: written while the graded
;; corner is confirmed, cleared on any non-confirmed cycle. Never persistent,
;; never a disposition surface (design v1.3 SSI correction).
;; Probe evidence: record body B5/B6; clear per ADR-005 superpose iteration;
;; the populate driver is if-dispatch composition of the probed parts.

;; TOTALITY-FIX 2026-07-07: guard empty BEFORE superpose; collapse-wrap the drain
;; (state_delta / do-clear-idle-pattern! verified idiom; repro R1=0, fix R3/R4/R5).
(= (do-clear-corner-window!)
   (let $olds (collapse (match &self (corner-window-cmd $c $r) (corner-window-cmd $c $r)))
        (if (== $olds ())
            ()
            (let $_drained (collapse (let $o (superpose $olds)
                                          (remove-atom &self $o)))
                 ()))))

;; TOTALITY-FIX 2026-07-07: empty-batch guard + collapse-wrap so the writer
;; returns exactly one solution and cannot fork the cycle tail (probe S1/S2/S3).
(= (do-record-corner-window! $cmds $cycle-id)
   (if (== $cmds ())
       ()
       (let $_recorded (collapse (let $c (superpose $cmds)
                                      (let $r (repr $c)
                                           (add-atom &self (corner-window-cmd $cycle-id $r)))))
            ())))

;; Cycle driver. Hook ordering: AFTER populate-coupling-verdict (loop line 176),
;; so the gate always filters against the PRIOR cycle's record.
(= (populate-corner-window! $cmds $cycle-id)
   (if (== (corner-confirmed-core) True)
       (do-record-corner-window! $cmds $cycle-id)
       (do-clear-corner-window!)))
