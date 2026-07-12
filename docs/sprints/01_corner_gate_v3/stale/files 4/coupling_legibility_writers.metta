;; ============================================================
;; soul/coupling_legibility_writers.metta -- Corner-Gate v3 writers
;; Draft A.3 payload 2 of 3. Design canon: corner_gate_v3_adapter_design.md.
;; Status: DRAFT A.3 FOR BERTON RATIFICATION. Not imported anywhere yet.
;; History: A.1 resolved Layer-1 blockers B2 (idempotent contact events), B3 (hidden
;; failures increment the fail count; delta read before signature update),
;; writer items 1-6, and A1 (normalized bootstrap).
;;
;; Side-effecting writers for the coupling legibility surface. Pure
;; definitions live in coupling_legibility.metta. Writers are mechanical
;; observation only (P5): they record what happened, never what Clarity IS.
;;
;; MAP COMPLIANCE (Atom_Operations_Map.md, N1 writer doctrine):
;;   Every singleton mutation is remove-by-VARIABLE then add; never
;;   set-atom! (CONTRA-setatom safety correction). Contact events are
;;   remove-specific-then-add (idempotent per ord and surface). All added
;;   values are ground via let* BEFORE add-atom. No match inside if. Nested
;;   ordinary calls are sequenced through their own bindings (py-call
;;   arguments are pre-bound). Return values are never trusted; the harness
;;   verifies by separate reads.
;;
;; HOOK (installed by the monolith at the populate-corner-window! position,
;; AFTER populate-state-delta and populate-coupling-verdict; ordering is
;; load-bearing per state_delta_writer_writers.metta):
;;   ($_ (do-record-coupling-cycle! $metta_cmds $msgnew $k (get-state &error)))
;; RF9 (accepted): the fourth argument carries this cycle error state from
;; the loop context. Single function call per Discipline 1.
;; ============================================================

;; ------------------------------------------------------------
;; Bootstrap: NORMALIZING seeds (A1 ratified). Remove-all then add lands
;; exactly one of each singleton from ANY prior state, including duplicate
;; or stale singletons left by earlier iterations. Runs from initLoop.
;; ------------------------------------------------------------
(= (do-bootstrap-coupling!)
   (let* (($_rb (remove-atom &self (coupling-band-state $b $o)))
          ($_ab (add-atom &self (coupling-band-state window-filling 0)))
          ($_rs (remove-atom &self (command-signature-state $s $n $o2)))
          ($_as (add-atom &self (command-signature-state none 0 0))))
     bootstrap-coupling-done))
;; NOTE: remove-atom on zero match is a safe no-op in this substrate
;; (established substrate fact), so normalization is clean on first boot.

;; ------------------------------------------------------------
;; Contact events: transient, UNIQUE per ord and surface (B2 ratified).
;; Remove the specific ord+surface pair then add: a batch whose heads map to
;; the same surface lands exactly one event, so contact-count is the count
;; of touched surfaces, never the count of commands.
;; ------------------------------------------------------------
(= (do-record-contact-event! $ord $surface)
   (let* (($_r (remove-atom &self (coupling-contact-event $ord $surface)))
          ($_a (add-atom &self (coupling-contact-event $ord $surface))))
     $surface))

(= (do-clear-contact-events!)
   (remove-atom &self (coupling-contact-event $o $s)))
;; Variable-pattern remove clears ALL contact events in one call (map:
;; remove-all proven); zero-match is a safe no-op.

;; ------------------------------------------------------------
;; Surface recording over the batch heads. Classification goes through the
;; TOTAL forms only (B4): unknown heads reduce to no-contact, never leak.
;; Ambient prompt surfaces (task-state, cycle-trace) are deliberately not
;; recorded (RF4 accepted: NC1 must remain possible).
;; ------------------------------------------------------------
(= (record-contacts-for-heads! $ord $heads)
   (if (== $heads ())
       ()
       (let* (($h (car-atom $heads))
              ($t (cdr-atom $heads))
              ($surf (surface-for-head-total $h))
              ($_ (if (== $surf no-contact) () (do-record-contact-event! $ord $surf))))
         (record-contacts-for-heads! $ord $t))))

;; ------------------------------------------------------------
;; Signature singleton writer: remove-by-variable then add.
;; Fail semantics (B3 ratified): failed is decided by the CALLER as
;; visible-error OR (real signature AND state-delta none). Same signature
;; failing increments; a changed signature starts at 1 when failing, else 0.
;; Pin-only and empty batches sign as none and never count as failures.
;; ------------------------------------------------------------
(= (do-set-command-signature! $sig $failed $ord)
   (let* (($prevsig (current-command-signature))
          ($prevcount (current-signature-fail-count))
          ($nextcount (if (== $sig "none")
                          0
                          (if (== $sig $prevsig)
                              (if (== $failed True) (+ $prevcount 1) 0)
                              (if (== $failed True) 1 0))))
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
;; Window eviction: at 3 records, remove the oldest by specific ordinal
;; with variables for every other field (remove-all clears that record
;; whatever its values). Eviction reason: window-cap (ledger).
;; ------------------------------------------------------------
(= (do-evict-oldest-record!)
   (let $count (coupling-window-count)
     (if (>= $count 3)
         (let $old (oldest-coupling-ord)
           (remove-atom &self (coupling-cycle-record $old $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q)))
         ())))

;; ------------------------------------------------------------
;; THE PER-CYCLE RECORDER. One hook call; sequenced bindings calling pure
;; derivations, then exactly one record add. Ordering inside (B3): state
;; delta and prior-signature state are read BEFORE the signature update.
;; Inputs: $cmds executed batch, $msgnew Bool, $ord loop $k, $errstate loop
;; error state (() when clean).
;; ------------------------------------------------------------
(= (do-record-coupling-cycle! $cmds $msgnew $ord $errstate)
   (let* (;; --- mechanical observables, read-first block ---
          ($errvisible (if (== $errstate ()) False True))
          ($delta (latest-state-delta-verdict))
          ($heads (collapse (let $c (superpose $cmds) (car-atom $c))))
          ($crepr (repr $cmds))
          ($sig (py-call (helper.coupling_command_signature $crepr)))
          ($prevsig (current-command-signature))
          ($prevfail (current-signature-fail-count))
          ($prevrec-ord (latest-coupling-ord))
          ($prevccountxs (collapse (match &self (coupling-cycle-record $prevrec-ord $cc $b2 $c2 $d2 $e2 $f3 $f4 $g2 $h2 $i2 $j2 $k2 $l2 $m2 $n2 $p2 $q2) $cc)))
          ($prevccount (if (== $prevccountxs ()) 0 (car-atom $prevccountxs)))
          ($prevmove (latest-coupling-next-move))
          ($windowcount (coupling-window-count))
          ;; --- contact events (idempotent per surface) ---
          ($_clear (do-clear-contact-events!))
          ($_uw (if (== $msgnew True) (do-record-contact-event! $ord user-words) ()))
          ($_fq (if (== $errvisible True) (do-record-contact-event! $ord failed-query) ()))
          ($_rc (record-contacts-for-heads! $ord $heads))
          ($surfaces (coupling-contact-surfaces $ord))
          ($ccount (size-atom $surfaces))
          ($domsurf (dominant-surface-of $surfaces))
          ;; --- failure decision and signature update (B3) ---
          ($hiddenfail (if (== $sig "none") False (if (== $delta none) True False)))
          ($failed (if (== $errvisible True) True $hiddenfail))
          ($failcount (do-set-command-signature! $sig $failed $ord))
          ;; --- Gate H honesty (targets via Python hands; content unread) ---
          ($hasaction (if (== (coupling-contains $heads write-file) True) True
                      (if (== (coupling-contains $heads append-file) True) True
                      (if (== (coupling-contains $heads shell) True) True False))))
          ($hasclaim (if (== (coupling-contains $heads send) True) True False))
          ($atarget (py-call (helper.coupling_action_target $crepr)))
          ($vtarget (py-call (helper.coupling_verify_target $crepr)))
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
          ;; --- accords, support, band, residual, next-move ---
          ($firsthead (if (== $heads ()) pin (car-atom $heads)))
          ($firstclass (command-class-of-total $firsthead))
          ($ileg (task-intention-leg $firstclass $prevmove))
          ($aleg (task-action-leg $errvisible))
          ($oleg (task-outcome-leg $delta))
          ($taccord (derive-accord-summary $ileg $aleg $oleg))
          ($caccord (derive-contact-accord $ccount $windowcount $probe $prevfail))
          ($support (derive-support $ileg $aleg $oleg))
          ($priorband (current-coupling-band))
          ($band (derive-band $support $priorband))
          ($_band (do-set-coupling-band! $band $ord))
          ($residual (derive-residual-gap $support $windowcount))
          ($traceverdict (coupling-trace-verdict-with-current $polverdict))
          ($nextmove (derive-next-move $chainstate $traceverdict $honesty))
          ;; --- context and lineage ---
          ($phase (current-phase))
          ($ctxmsg (if (== $msgnew True) msgnew-present msgnew-absent))
          ($ctxsoul soul-verdict-present)
          ($ts (get_time))
          ($depends (if (== $prevrec-ord 0) none $prevrec-ord))
          ;; --- fold: evict, then land exactly one record, all fields ground ---
          ($_evict (do-evict-oldest-record!))
          ($_add (add-atom &self (coupling-cycle-record $ord $ccount $domsurf $sig
                                   $chainstate $polverdict $taccord $caccord
                                   $support $residual $honesty $nextmove
                                   $phase $ctxmsg $ctxsoul
                                   do-record-coupling-cycle $depends $ts))))
     record-coupling-cycle-done))
;; RF11-RES (ratified): both accords are STORED in the v3-18-field record.
;; The line renders the task accord; contact accord renders only on
;; divergence per the pure-file rule.
;; A.3 NOTE on $traceverdict timing (Berton semantic fix): the stored
;; $next-move derives from coupling-trace-verdict-with-current, which pairs
;; the latest PRIOR stored polarity verdict with the CURRENT cycle verdict,
;; so next-move reflects the actual current 3-cycle trace and never lags.
;; The RENDERED trajectory (composer) reads the full window AFTER the add.
;; RF12 (accepted): $ctx-soul is a surface-presence context marker, not
;; approval status.
;; RF13 (resolved): empty batches yield no heads and sign as none (NC1 path);
;; pin-only batches sign as none and never increment failure state.
