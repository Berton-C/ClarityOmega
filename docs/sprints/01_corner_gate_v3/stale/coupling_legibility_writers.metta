;; ============================================================
;; soul/coupling_legibility_writers.metta -- Corner-Gate v3 writers
;; Draft A payload 2 of 3. Design canon: corner_gate_v3_adapter_design.md v0.6.
;; Status: DRAFT FOR BERTON LAYER-1 REVIEW. Not imported anywhere yet.
;;
;; Side-effecting writers for the coupling legibility surface. Pure
;; definitions live in coupling_legibility.metta. Writers are mechanical
;; observation only (P5): they record what happened, never what Clarity IS.
;;
;; MAP COMPLIANCE (Atom_Operations_Map.md, N1 writer doctrine):
;;   Every mutation is remove-by-VARIABLE then add. Never set-atom!
;;   (upsert-on-nonmatch creates silent duplicates; CONTRA-setatom safety
;;   correction). Never add-alone on singletons (add-atom is not idempotent).
;;   Remove-all semantics make each swap self-healing from any prior state.
;;   All added values are ground via let* BEFORE add-atom (unreduced-storage
;;   rule). No match inside if. Return values are never trusted; the harness
;;   verifies by separate reads.
;;
;; HOOK (installed by the monolith at the populate-corner-window! position,
;; AFTER populate-state-delta and populate-coupling-verdict; ordering is
;; load-bearing per state_delta_writer_writers.metta):
;;   ($_ (do-record-coupling-cycle! $metta_cmds $msgnew $k (get-state &error)))
;; REVIEW-FLAG RF9: the fourth argument carries this cycle error state from
;; the loop context (the loop itself branches on (get-state &error) at the
;; same site). Single function call per Discipline 1.
;; ============================================================

;; ------------------------------------------------------------
;; Bootstrap: guarded seeds for the two singletons. Runs once from initLoop.
;; Guard pattern: collapse presence, branch, add only when absent.
;; ------------------------------------------------------------
(= (do-bootstrap-coupling!)
   (let* (($bands (collapse (match &self (coupling-band-state $b $o) $b)))
          ($_b (if (== $bands ()) (add-atom &self (coupling-band-state window-filling 0)) ()))
          ($sigs (collapse (match &self (command-signature-state $s $n $o) $s)))
          ($_s (if (== $sigs ()) (add-atom &self (command-signature-state none 0 0)) ())))
     bootstrap-coupling-done))

;; ------------------------------------------------------------
;; Contact events: transient per-cycle records, folded at cycle close
;; (rejection reason: folded-into-record). Plain add is correct here because
;; the recorder clears the family every cycle before the record lands.
;; ------------------------------------------------------------
(= (do-record-contact-event! $ord $surface)
   (add-atom &self (coupling-contact-event $ord $surface)))

(= (do-clear-contact-events!)
   (let $existing (collapse (match &self (coupling-contact-event $o $s) (coupling-contact-event $o $s)))
     (if (== $existing ())
         ()
         (remove-atom &self (coupling-contact-event $o2 $s2)))))
;; NOTE: remove-atom with variables clears ALL contact events in one call
;; (map: variable-pattern remove is remove-all, proven).

;; ------------------------------------------------------------
;; Contact classification from the executed batch.
;; REVIEW-FLAG RF4: v1 surface mapping for markup. Ambient prompt surfaces
;; (task-state, cycle-trace) are NOT recorded as contact: they are present
;; every cycle mechanically and recording them would make NC1 (pin-only
;; cycle records no contact) impossible. Recorded surfaces are her
;; command-driven touches plus mechanically present external input.
;;   msgnew                -> user-words
;;   read-file             -> source-read
;;   shell                 -> tool-result
;;   query/episodes/metta/remember -> runtime-output
;;   write-file/append-file -> runtime-output
;;   search/tavily-search  -> web-query
;;   technical-analysis    -> capability-result
;;   visible error feedback -> failed-query
;;   send/pin              -> no contact event (claim and narration classes)
;; ------------------------------------------------------------
(= (surface-for-head read-file) source-read)
(= (surface-for-head shell) tool-result)
(= (surface-for-head query) runtime-output)
(= (surface-for-head episodes) runtime-output)
(= (surface-for-head metta) runtime-output)
(= (surface-for-head remember) runtime-output)
(= (surface-for-head write-file) runtime-output)
(= (surface-for-head append-file) runtime-output)
(= (surface-for-head search) web-query)
(= (surface-for-head tavily-search) web-query)
(= (surface-for-head technical-analysis) capability-result)
(= (surface-for-head send) no-contact)
(= (surface-for-head pin) no-contact)

(= (record-contacts-for-heads! $ord $heads)
   (if (== $heads ())
       ()
       (let* (($h (car-atom $heads))
              ($t (cdr-atom $heads))
              ($surf (surface-for-head $h))
              ($_ (if (== $surf no-contact) () (do-record-contact-event! $ord $surf))))
         (record-contacts-for-heads! $ord $t))))

;; ------------------------------------------------------------
;; Signature singleton writer: remove-by-variable then add.
;; Consecutive-fail semantics: same signature with a failed cycle increments;
;; a changed signature resets to zero (or one when this cycle itself failed).
;; ------------------------------------------------------------
(= (do-set-command-signature! $sig $failed $ord)
   (let* (($prevsig (current-command-signature))
          ($prevcount (current-signature-fail-count))
          ($nextcount (if (== $sig $prevsig)
                          (if (== $failed True) (+ $prevcount 1) 0)
                          (if (== $failed True) 1 0)))
          ($_r (remove-atom &self (command-signature-state $s $n $o)))
          ($_a (add-atom &self (command-signature-state $sig $nextcount $ord))))
     $nextcount))

;; ------------------------------------------------------------
;; Band singleton writer: remove-by-variable then add.
;; ------------------------------------------------------------
(= (do-set-coupling-band! $band $ord)
   (let* (($_r (remove-atom &self (coupling-band-state $b $o)))
          ($_a (add-atom &self (coupling-band-state $band $ord))))
     $band))

;; ------------------------------------------------------------
;; Window eviction: when the window holds 3 records, remove the oldest by
;; its specific ordinal with variables for every other field (remove-all
;; semantics clear that record whatever its values).
;; ------------------------------------------------------------
(= (do-evict-oldest-record!)
   (let* (($count (coupling-window-count)))
     (if (>= $count 3)
         (let $old (oldest-coupling-ord)
           (remove-atom &self (coupling-cycle-record $old $a $b $c $d $e $f $g $h $i $j $k $l $m $n $p $q)))
         ())))

;; ------------------------------------------------------------
;; THE PER-CYCLE RECORDER. One hook call; everything below is sequenced
;; bindings calling pure derivations, then one record add.
;; Inputs: $cmds the executed batch, $msgnew Bool, $ord the loop $k,
;; $errstate the loop error state (() when clean).
;; ------------------------------------------------------------
(= (do-record-coupling-cycle! $cmds $msgnew $ord $errstate)
   (let* (;; --- mechanical observables ---
          ($errvisible (if (== $errstate ()) False True))
          ($heads (collapse (let $c (superpose $cmds) (car-atom $c))))
          ($_clear (do-clear-contact-events!))
          ($_uw (if (== $msgnew True) (do-record-contact-event! $ord user-words) ()))
          ($_fq (if (== $errvisible True) (do-record-contact-event! $ord failed-query) ()))
          ($_rc (record-contacts-for-heads! $ord $heads))
          ($surfaces (coupling-contact-surfaces $ord))
          ($ccount (size-atom $surfaces))
          ($domsurf (dominant-surface-of $surfaces))
          ;; --- signature and repetition (prior state read BEFORE update) ---
          ($sig (py-call (helper.coupling_command_signature (repr $cmds))))
          ($prevsig (current-command-signature))
          ($prevfail (current-signature-fail-count))
          ($failed (if (== $errvisible True) True (if (== $ccount 0) False False)))
          ($failcount (do-set-command-signature! $sig $failed $ord))
          ;; --- prior-cycle context from the space ---
          ($delta (latest-state-delta-verdict))
          ($prevrec-ord (latest-coupling-ord))
          ($prevccountxs (collapse (match &self (coupling-cycle-record $prevrec-ord $cc $b2 $c2 $d2 $e2 $f2 $g2 $h2 $i2 $j2 $k2 $l2 $m2 $n2 $p2 $q2) $cc)))
          ($prevccount (if (== $prevccountxs ()) 0 (car-atom $prevccountxs)))
          ($prevmove (latest-coupling-next-move))
          ($windowcount (coupling-window-count))
          ;; --- Gate H honesty (targets via Python hands; content unread) ---
          ($hasaction (if (== (coupling-contains $heads write-file) True) True
                      (if (== (coupling-contains $heads append-file) True) True
                      (if (== (coupling-contains $heads shell) True) True False))))
          ($hasclaim (if (== (coupling-contains $heads send) True) True False))
          ($atarget (py-call (helper.coupling_action_target (repr $cmds))))
          ($vtarget (py-call (helper.coupling_verify_target (repr $cmds))))
          ($honesty (derive-honesty-state $hasaction $hasclaim $atarget $vtarget))
          ;; --- D7 derivations ---
          ($repeat (derive-repeat-symbol $failcount))
          ($errsurf (derive-error-surface $errvisible $failcount $delta))
          ($errfb (derive-error-feedback $errvisible))
          ($probe (derive-probe-symbol $sig $prevsig $prevfail))
          ($trace (derive-trace-symbol $windowcount))
          ($chainstate (derive-chain-state $repeat $errsurf $errfb $probe $trace $ccount))
          ($protection (derive-protection $failcount $delta))
          ($contactability (derive-contactability $ccount $prevccount))
          ($suspicion (derive-suspicion $failcount $prevfail))
          ($polarity (derive-polarity $delta $failcount))
          ($winpos (derive-window-position $windowcount))
          ($polverdict (derive-polarity-verdict $protection $contactability $suspicion $polarity $winpos))
          ;; --- accord, support, band, residual ---
          ($ileg (task-intention-leg (command-class-of (if (== $heads ()) pin (car-atom $heads))) $prevmove))
          ($aleg (task-action-leg $errvisible))
          ($oleg (task-outcome-leg $delta))
          ($accord (derive-accord-summary $ileg $aleg $oleg))
          ($support (derive-support $ileg $aleg $oleg))
          ($priorband (current-coupling-band))
          ($band (derive-band $support $priorband))
          ($_band (do-set-coupling-band! $band $ord))
          ($residual (derive-residual-gap $support $windowcount))
          ($nextmove (derive-next-move $chainstate not-computed))
          ;; --- context and lineage ---
          ($phase (current-phase))
          ($ctxmsg (if (== $msgnew True) msgnew-present msgnew-absent))
          ($ctxsoul soul-verdict-present)
          ($ts (get_time))
          ($depends (if (== $prevrec-ord 0) none $prevrec-ord))
          ;; --- fold: evict, then land exactly one record, all fields ground ---
          ($_evict (do-evict-oldest-record!))
          ($_add (add-atom &self (coupling-cycle-record $ord $ccount $domsurf $sig
                                   $chainstate $polverdict $accord
                                   $support $residual $honesty $nextmove
                                   $phase $ctxmsg $ctxsoul
                                   do-record-coupling-cycle $depends $ts))))
     record-coupling-cycle-done))
;; REVIEW-FLAG RF12: $ctxsoul is soul-verdict-present as a constant in v1:
;; the SOUL_VERDICT renders every cycle (verified in live logs). Wiring the
;; actual verdict symbol through the hook is a v1.1 option for markup.
;; REVIEW-FLAG RF13: the $heads extraction takes the head of each executed
;; command via car-atom over the superposed batch; empty batches yield ()
;; and record no head-driven contact (NC1 path).
