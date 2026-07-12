;; ============================================================
;; soul/coupling_legibility.metta -- Corner-Gate v3 pure surface
;; Draft A.3 payload 1 of 3. Design canon: corner_gate_v3_adapter_design.md.
;; Status: DRAFT A.3 FOR BERTON RATIFICATION. Not imported anywhere yet.
;; History: A.1 resolved Layer-1 blockers B1 (trace verdict wired), B4 (total
;; classification), B5 (MeTTa line composer), pure-payload items 1-6, and
;; carries the RF8 engine-vocabulary next-move mapping RATIFY-PENDING.
;;
;; PURPOSE: pure definitions for the coupling legibility surface. Shapes,
;; schema version, threshold constants, reader helpers, dominant-surface
;; cascade, Gate H honesty derivation, D7 mechanical derivations, band
;; position, trace verdict, next-move mapping, and the line composer.
;;
;; Side-effecting writers (do-*!) land in coupling_legibility_writers.metta.
;;
;; ATOM SHAPES (canonical, 18-field record, schema v3-18-field):
;;   (coupling-cycle-record $ord $contact-count $dominant-surface $command-sig
;;                          $chain-state $polarity-verdict $task-accord $contact-accord
;;                          $support $residual-gap $honesty-state $next-move
;;                          $ctx-phase $ctx-msgnew $ctx-soul
;;                          $producer $depends-on $ts)          18 fields, v3-18-field
;;   (coupling-band-state $band $from-ord)                 singleton
;;   (command-signature-state $sig $consecutive-fail-count $last-ord)  singleton
;;   (coupling-contact-event $ord $surface)   transient, unique per ord+surface
;;
;; FIELD NOTES (RF11-RES RATIFIED): both accords are STORED ($task-accord,
;; $contact-accord). The normal line renders the task accord only; the
;; contact accord renders solely on divergence (task integrating while
;; contact is not), as contact-audit. Preserve structurally, reveal
;; selectively (Berton ruling, 2026-07-09).
;; $ctx-soul is a surface-presence context marker, not approval status
;; (ratified wording). $next-move uses the RF8 mapping pending ratification.
;;
;; MAP COMPLIANCE (Atom_Operations_Map.md):
;;   No match inside if: collapse into a binding, then branch (C12).
;;   Reads return bare scalars or symbols only; the full-record helper is for
;;   internal composition ONLY and must NEVER be rendered (tuple render throws).
;;   In a let bind, ordinary functions never take a function call as an
;;   argument; every composition is sequenced through its own binding.
;;   Writers (other file) use remove-by-variable then add, never set-atom!.
;; ============================================================

;; ------------------------------------------------------------
;; Schema version guard (design doc 3.1, ratified)
;; ------------------------------------------------------------
(= (coupling-legibility-schema-version) v3-18-field)

;; ------------------------------------------------------------
;; D10 threshold constants. Adapter-side tuning targets, not engine law.
;; ------------------------------------------------------------
(= (coupling-lower-band) 0.4)
(= (coupling-upper-band) 0.6)

;; ------------------------------------------------------------
;; Small pure list helpers
;; ------------------------------------------------------------
(= (coupling-contains $xs $sym)
   (if (== $xs ())
       False
       (let* (($h (car-atom $xs))
              ($t (cdr-atom $xs)))
         (if (== $h $sym) True (coupling-contains $t $sym)))))

(= (coupling-max-num $xs $acc)
   (if (== $xs ())
       $acc
       (let* (($h (car-atom $xs))
              ($t (cdr-atom $xs)))
         (if (> $h $acc) (coupling-max-num $t $h) (coupling-max-num $t $acc)))))

(= (coupling-min-num $xs $acc)
   (if (== $xs ())
       $acc
       (let* (($h (car-atom $xs))
              ($t (cdr-atom $xs)))
         (if (< $h $acc) (coupling-min-num $t $h) (coupling-min-num $t $acc)))))

;; The middle ordinal of a 3-window: the element that is neither min nor max.
(= (coupling-mid-ord $xs $min $max)
   (if (== $xs ())
       0
       (let* (($h (car-atom $xs))
              ($t (cdr-atom $xs)))
         (if (and (not (== $h $min)) (not (== $h $max)))
             $h
             (coupling-mid-ord $t $min $max)))))

;; Dedupe a symbol list (unique surfaces; B2 support).
(= (coupling-dedupe $xs $acc)
   (if (== $xs ())
       $acc
       (let* (($h (car-atom $xs))
              ($t (cdr-atom $xs)))
         (if (== (coupling-contains $acc $h) True)
             (coupling-dedupe $t $acc)
             (let $acc2 (cons-atom $h $acc)
               (coupling-dedupe $t $acc2))))))

;; ------------------------------------------------------------
;; Known command heads and TOTAL classification (B4). Unknown heads reduce
;; to the safe fallbacks no-contact and neutral, never unreduced symbols.
;; ------------------------------------------------------------
(= (coupling-known-heads)
   (write-file append-file shell remember read-file query episodes metta
    send pin search tavily-search technical-analysis))

;; Partial tables (only ever called through the total forms).
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

;; RF3 resolution: remember is NEUTRAL class in v1 (its target, the memory
;; string, has no mechanically verifiable durable target; Gate H consistency).
(= (command-class-of write-file) action-class)
(= (command-class-of append-file) action-class)
(= (command-class-of shell) action-class)
(= (command-class-of remember) neutral)
(= (command-class-of read-file) verification-class)
(= (command-class-of query) verification-class)
(= (command-class-of episodes) verification-class)
(= (command-class-of metta) verification-class)
(= (command-class-of send) claim-class)
(= (command-class-of pin) narration-class)
(= (command-class-of search) neutral)
(= (command-class-of tavily-search) neutral)
(= (command-class-of technical-analysis) neutral)

(= (surface-for-head-total $h)
   (let $known (coupling-known-heads)
     (if (== (coupling-contains $known $h) True)
         (surface-for-head $h)
         no-contact)))

(= (command-class-of-total $h)
   (let $known (coupling-known-heads)
     (if (== (coupling-contains $known $h) True)
         (command-class-of $h)
         neutral)))

;; ------------------------------------------------------------
;; Reader helpers (ratified contract; design doc 3.1).
;; Ratified names latest-coupling-context and latest-coupling-lineage return
;; the PRIMARY component (ctx-phase, producer); component helpers sit beside
;; them. Consumers never write an 18-field match by hand.
;; ------------------------------------------------------------
(= (latest-coupling-ord)
   (let $ords (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q) $o))
     (if (== $ords ()) 0 (let $h (car-atom $ords) (coupling-max-num $ords $h)))))

(= (oldest-coupling-ord)
   (let $ords (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q) $o))
     (if (== $ords ()) 0 (let $h (car-atom $ords) (coupling-min-num $ords $h)))))

(= (coupling-window-count)
   (let $ords (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q) $o))
     (size-atom $ords)))

;; INTERNAL COMPOSITION ONLY. NEVER render, println, or py-str this value:
;; tuple render throws (map read-instrument rule).
(= (latest-coupling-record)
   (let* (($o (latest-coupling-ord))
          ($recs (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q)
                                  (coupling-cycle-record $o $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q)))))
     (if (== $recs ()) none (car-atom $recs))))

(= (latest-coupling-contact-count)
   (let* (($o (latest-coupling-ord))
          ($xs (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q) $a))))
     (if (== $xs ()) 0 (car-atom $xs))))

(= (latest-coupling-dominant-surface)
   (let* (($o (latest-coupling-ord))
          ($xs (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q) $b))))
     (if (== $xs ()) none (car-atom $xs))))

(= (latest-coupling-command-sig)
   (let* (($o (latest-coupling-ord))
          ($xs (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q) $c))))
     (if (== $xs ()) none (car-atom $xs))))

(= (latest-coupling-chain-state)
   (let* (($o (latest-coupling-ord))
          ($xs (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q) $d))))
     (if (== $xs ()) not-computed (car-atom $xs))))

(= (latest-coupling-polarity-verdict)
   (let* (($o (latest-coupling-ord))
          ($xs (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q) $e))))
     (if (== $xs ()) not-computed (car-atom $xs))))

(= (latest-coupling-task-accord)
   (let* (($o (latest-coupling-ord))
          ($xs (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q) $f))))
     (if (== $xs ()) not-computed (car-atom $xs))))

(= (latest-coupling-contact-accord)
   (let* (($o (latest-coupling-ord))
          ($xs (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q) $f2))))
     (if (== $xs ()) not-computed (car-atom $xs))))

;; Back-compat convenience: the unqualified accord is the task accord.
(= (latest-coupling-accord) (latest-coupling-task-accord))

(= (latest-coupling-support)
   (let* (($o (latest-coupling-ord))
          ($xs (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q) $g))))
     (if (== $xs ()) not-computed (car-atom $xs))))

(= (latest-coupling-residual-gap)
   (let* (($o (latest-coupling-ord))
          ($xs (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q) $h))))
     (if (== $xs ()) not-computed (car-atom $xs))))

(= (latest-coupling-honesty)
   (let* (($o (latest-coupling-ord))
          ($xs (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q) $i))))
     (if (== $xs ()) not-computed (car-atom $xs))))

(= (latest-coupling-next-move)
   (let* (($o (latest-coupling-ord))
          ($xs (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q) $j))))
     (if (== $xs ()) not-computed (car-atom $xs))))

;; Ratified name: returns the primary context component (ctx-phase).
(= (latest-coupling-context)
   (let* (($o (latest-coupling-ord))
          ($xs (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q) $k))))
     (if (== $xs ()) not-computed (car-atom $xs))))

(= (latest-coupling-ctx-msgnew)
   (let* (($o (latest-coupling-ord))
          ($xs (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q) $l))))
     (if (== $xs ()) not-computed (car-atom $xs))))

(= (latest-coupling-ctx-soul)
   (let* (($o (latest-coupling-ord))
          ($xs (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q) $m))))
     (if (== $xs ()) not-computed (car-atom $xs))))

;; Ratified name: returns the primary lineage component (producer).
(= (latest-coupling-lineage)
   (let* (($o (latest-coupling-ord))
          ($xs (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q) $n))))
     (if (== $xs ()) not-computed (car-atom $xs))))

(= (latest-coupling-depends-on)
   (let* (($o (latest-coupling-ord))
          ($xs (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q) $p))))
     (if (== $xs ()) none (car-atom $xs))))

;; Field reads for a SPECIFIC ordinal (trajectory consumption).
(= (coupling-polarity-verdict-at $ord)
   (let $xs (collapse (match &self (coupling-cycle-record $ord $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q) $e))
     (if (== $xs ()) not-computed (car-atom $xs))))

(= (coupling-support-at $ord)
   (let $xs (collapse (match &self (coupling-cycle-record $ord $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q) $g))
     (if (== $xs ()) not-computed (car-atom $xs))))

;; Singleton reads.
(= (current-coupling-band)
   (let $xs (collapse (match &self (coupling-band-state $b $o) $b))
     (if (== $xs ()) window-filling (car-atom $xs))))

(= (current-coupling-band-ord)
   (let $xs (collapse (match &self (coupling-band-state $b $o) $o))
     (if (== $xs ()) 0 (car-atom $xs))))

(= (current-command-signature)
   (let $xs (collapse (match &self (command-signature-state $s $n $o) $s))
     (if (== $xs ()) none (car-atom $xs))))

(= (current-signature-fail-count)
   (let $xs (collapse (match &self (command-signature-state $s $n $o) $n))
     (if (== $xs ()) 0 (car-atom $xs))))

;; Unique contact surfaces for an ordinal (deduped; count = surface count).
(= (coupling-contact-surfaces $ord)
   (let* (($raw (collapse (match &self (coupling-contact-event $ord $s) $s)))
          ($uniq (coupling-dedupe $raw ())))
     $uniq))

;; ------------------------------------------------------------
;; B1: trace verdict over the stored window. Cycle 3 consumes the three
;; stored per-cycle polarity verdicts via the quoted engine reduction
;; (q-tfs2-trace-verdict? same-start $v2 $v3). window-filling until full.
;; ------------------------------------------------------------
(= (coupling-trace-verdict-for-window)
   (let* (($count (coupling-window-count)))
     (if (< $count 3)
         window-filling
         (let* (($ords (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q) $o)))
                ($h (car-atom $ords))
                ($min (coupling-min-num $ords $h))
                ($max (coupling-max-num $ords $h))
                ($mid (coupling-mid-ord $ords $min $max))
                ($v2 (coupling-polarity-verdict-at $mid))
                ($v3 (coupling-polarity-verdict-at $max))
                ($tv (collapse (q-tfs2-trace-verdict? same-start $v2 $v3))))
           (if (== $tv ()) not-computed (car-atom $tv))))))

(= (latest-coupling-trace-verdict) (coupling-trace-verdict-for-window))

;; A.3 semantic fix (Berton): the CURRENT-cycle trace verdict, computed
;; BEFORE the current record is added. With fewer than 2 prior records the
;; window is still filling. With 2 or more priors: v2 is the latest PRIOR
;; stored polarity verdict, v3 is the CURRENT cycle polarity verdict, per
;; the quoted engine signature (q-tfs2-trace-verdict? same-start $v2 $v3).
;; This is what the stored $next-move derives from, so next-move never lags
;; one cycle behind the actual 3-cycle trace.
(= (coupling-trace-verdict-with-current $current-pv)
   (let* (($count (coupling-window-count)))
     (if (< $count 2)
         window-filling
         (let* (($prior-ord (latest-coupling-ord))
                ($v2 (coupling-polarity-verdict-at $prior-ord))
                ($tv (collapse (q-tfs2-trace-verdict? same-start $v2 $current-pv))))
           (if (== $tv ()) not-computed (car-atom $tv))))))

;; ------------------------------------------------------------
;; Dominant-surface cascade (ratified deterministic priority order).
;; ------------------------------------------------------------
(= (dominant-surface-of $surfaces)
   (if (== (coupling-contains $surfaces failed-query) True) failed-query
   (if (== (coupling-contains $surfaces runtime-output) True) runtime-output
   (if (== (coupling-contains $surfaces tool-result) True) tool-result
   (if (== (coupling-contains $surfaces capability-result) True) capability-result
   (if (== (coupling-contains $surfaces web-query) True) web-query
   (if (== (coupling-contains $surfaces source-read) True) source-read
   (if (== (coupling-contains $surfaces user-words) True) user-words
   (if (== (coupling-contains $surfaces task-state) True) task-state
   (if (== (coupling-contains $surfaces cycle-trace) True) cycle-trace
   none))))))))))

;; ------------------------------------------------------------
;; GATE H: honesty state derivation (ratified mapping, verbatim semantics).
;; unknown target -> not-computed. known + no same-target verification ->
;; name-action-not-verification. known + same-target verified ->
;; claim-completion. Claim proxy (RF5): claim-class command present.
;; ------------------------------------------------------------
(= (derive-honesty-state $has-action $has-claim $action-target $verify-target)
   (if (== $has-action False) not-computed
   (if (== $has-claim False) not-computed
   (if (== $action-target "unknown") not-computed
   (if (== $verify-target $action-target) claim-completion
       name-action-not-verification)))))

;; ------------------------------------------------------------
;; D7 mechanical derivations (ratified table).
;; ------------------------------------------------------------
(= (derive-repeat-symbol $failcount)
   (if (>= $failcount 2) repeated-failing-command one-off-failing-command))

(= (derive-error-surface $errvisible $failcount $delta)
   (if (== $errvisible True) visible-error-surface
   (if (and (>= $failcount 2) (== $delta none)) hidden-error-surface
       visible-error-surface)))

(= (derive-error-feedback $errvisible)
   (if (== $errvisible True) error-feedback-visible error-feedback-hidden))

(= (derive-probe-symbol $sig $prevsig $prevfailcount)
   (if (and (>= $prevfailcount 2) (not (== $sig $prevsig))) corrective-probe repeated-command))

(= (derive-trace-symbol $windowcount)
   (if (>= $windowcount 1) trace-present trace-absent))

(= (derive-chain-state $repeat $errsurface $errfeedback $probe $trace $contactcount)
   (let* (($capture (q-self-seeing-loop-capture? $repeat $errsurface))
          ($newvis (q-self-seeing-newly-visible-surface? $errsurface $errfeedback))
          ($newverr (if (== $newvis newly-visible-surface) newly-visible-error no-newly-visible-error))
          ($shift (q-self-seeing-orientation-shift? repeated-command $probe $newverr))
          ($future (if (== $probe corrective-probe) future-command-changed future-command-unchanged))
          ($nav (q-self-seeing-navigation-change? orientation-shift $trace $future)))
     (if (and (== $shift orientation-shift) (== $nav navigation-change)) navigation-change
     (if (== $shift orientation-shift) orientation-shift
     (if (== $newvis newly-visible-surface) newly-visible-surface
     (if (== $capture loop-capture-seen) loop-capture-seen
     (if (> $contactcount 0) self-seeing-contact
         blocked-no-contact)))))))

(= (derive-protection $failcount $delta)
   (if (and (>= $failcount 2) (== $delta none)) protection-flat-low-warrant
       protection-softens-warrant-rises))

(= (derive-contactability $ccount $prevccount)
   (if (> $ccount $prevccount) contactability-rises contactability-flat))

(= (derive-suspicion $failcount $prevfailcount)
   (if (> $failcount $prevfailcount) suspicion-rises
   (if (== $failcount 0) suspicion-decays suspicion-rises)))

(= (derive-polarity $delta $failcount)
   (if (== $delta forward) polarity-supports
   (if (>= $failcount 2) polarity-blocks polarity-supports)))

(= (derive-window-position $windowcount)
   (if (== $windowcount 0) cycle-1
   (if (== $windowcount 1) cycle-2 cycle-3)))

(= (derive-polarity-verdict $protection $contactability $suspicion $polarity $pos)
   (let $v (collapse (q-tfs2-polarity-trajectory? $protection $contactability $suspicion $polarity $pos))
     (if (== $v ()) not-computed (car-atom $v))))

;; ------------------------------------------------------------
;; Alignment legs (ratified D7). Task accord stored as $accord-summary.
;; Contact accord derived per cycle (doc 2.6); storage/render is the open
;; RF11-RES ruling. Navigation leg is mechanical: with a live repetition
;; (prevfail >= 2) alignment requires the corrective probe; otherwise there
;; is nothing to correct and the leg is aligned.
;; ------------------------------------------------------------
(= (task-intention-leg $class $prevmove)
   (if (== $prevmove not-computed) aligned
   (if (== $class narration-class) misaligned aligned)))

(= (task-action-leg $errvisible)
   (if (== $errvisible True) misaligned aligned))

(= (task-outcome-leg $delta)
   (if (== $delta forward) aligned misaligned))

(= (contact-contact-leg $contactcount)
   (if (> $contactcount 0) aligned misaligned))

(= (contact-audit-leg $windowcount)
   (if (>= $windowcount 1) aligned misaligned))

(= (contact-navigation-leg $probe $prevfailcount)
   (if (>= $prevfailcount 2)
       (if (== $probe corrective-probe) aligned misaligned)
       aligned))

(= (derive-accord-summary $i $a $o)
   (q-alignment-triplet-status? $i $a $o))

(= (derive-contact-accord $ccount $windowcount $probe $prevfailcount)
   (let* (($c (contact-contact-leg $ccount))
          ($au (contact-audit-leg $windowcount))
          ($n (contact-navigation-leg $probe $prevfailcount)))
     (q-alignment-triplet-status? $c $au $n)))

;; ------------------------------------------------------------
;; Evidence pbits, edges, chain, support (RF7 tuning constants).
;; ------------------------------------------------------------
(= (leg-strength $leg) (if (== $leg aligned) 0.9 0.2))

(= (coupling-pbit-strength (mk-pbit $s $c)) $s)

(= (derive-support $ileg $aleg $oleg)
   (let* (($is (leg-strength $ileg))
          ($as (leg-strength $aleg))
          ($os (leg-strength $oleg))
          ($ipbit (mk-pbit $is 0.7))
          ($apbit (mk-pbit $as 0.7))
          ($opbit (mk-pbit $os 0.7))
          ($iapbit (q-meet $ipbit $apbit))
          ($aopbit (q-meet $apbit $opbit))
          ($e1 (q-intention-action intention action $iapbit))
          ($e2 (q-action-outcome action outcome $aopbit))
          ($chain (q-coherence-chain $e1 $e2))
          ($cpbit (qalignment-pbit $chain))
          ($s (coupling-pbit-strength $cpbit)))
     $s))
;; RB1 (ratified patch): the action leg participates in BOTH edges via
;; q-meet (verified (-> pbit pbit pbit), min strength min confidence,
;; engine lines 115-117). Fixture expectation: aligned, misaligned, aligned
;; reduces support to 0.04 (0.2 meet on each edge, chain multiplies).

;; ------------------------------------------------------------
;; Band position and hysteresis (RF10 flip rule).
;; ------------------------------------------------------------
(= (band-position-simple $support)
   (let* (($lo (coupling-lower-band))
          ($hi (coupling-upper-band)))
     (if (< $support $lo) below-lower-band
     (if (> $support $hi) above-upper-band
         within-band))))

(= (band-position-of $support $priorband)
   (let $pos (band-position-simple $support)
     (if (and (== $pos above-upper-band) (== $priorband stable-low)) rapid-boundary-flip
     (if (and (== $pos below-lower-band) (== $priorband stable-high)) rapid-boundary-flip
         $pos))))

(= (derive-band $support $priorband)
   (let* (($pos (band-position-of $support $priorband))
          ($b (q-threshold-hysteresis-status? $pos)))
     (if (== $b hold-previous-state)
         (if (== $priorband window-filling) hold-previous-state $priorband)
         $b)))

;; ------------------------------------------------------------
;; Residual gap (symbolic engine reduction).
;; ------------------------------------------------------------
(= (derive-residual-gap $support $windowcount)
   (let* (($hi (coupling-upper-band))
          ($supsym (if (>= $support $hi) target-met current-support))
          ($ressym (if (>= $windowcount 2) residual-available residual-absent)))
     (q-residual-threshold-gap? $supsym target-threshold $ressym)))

;; ------------------------------------------------------------
;; RF8 next-move mapping. RATIFY-PENDING (Berton). Every output symbol is
;; VERBATIM engine move vocabulary with its engine source cited:
;;   block-reinforcement-and-seek-contact  (move for mutation-risk, 1226)
;;   preserve-learning-trace               (move for contradiction-metabolized, 2169)
;;   prevent-self-certification            (move for self-derived-support-risk, 2174)
;;   make-trajectory-legible               (move for soul-ungrounded-risk, 2176)
;;   integrate-outcome                     (move for action-learning-coherent, 2179)
;;   continue-inquiry                      (move for grounded-suspicion, 2166)
;; The STATE-to-move pairing below is adapter-side and is the thing being
;; ratified. Rejection reverts this function to not-computed in one line.
;; Trace verdict outranks chain state; honesty outranks both.
;; ------------------------------------------------------------
(= (derive-next-move $chainstate $traceverdict $honesty)
   (if (== $honesty name-action-not-verification) prevent-self-certification
   (if (== $traceverdict blocked-repetition-without-metabolization) block-reinforcement-and-seek-contact
   (if (== $traceverdict blocked-defensive-fixation) block-reinforcement-and-seek-contact
   (if (== $traceverdict metabolization-candidate) preserve-learning-trace
   (if (== $chainstate loop-capture-seen) make-trajectory-legible
   (if (== $chainstate navigation-change) integrate-outcome
   (if (== $chainstate blocked-no-contact) make-trajectory-legible
       continue-inquiry))))))))

;; ------------------------------------------------------------
;; B5: the MeTTa line composer. Reads ONLY through field helpers (bare
;; scalars and symbols), sequences every binding, and hands ten flat values
;; to the Python formatter. Never touches the full record tuple.
;; ------------------------------------------------------------
(= (coupling-contact-audit-render $ta $ca)
   (if (and (== $ta integrating-alignment)
            (and (not (== $ca integrating-alignment))
                 (and (not (== $ca not-computed)) (not (== $ca window-filling)))))
       $ca
       hidden))
;; RF11-RES divergence rule (ratified): contact accord renders ONLY when the
;; task accord is integrating while the contact accord is not. The decision
;; is made HERE in MeTTa (the soul-side surface); Python only formats.

(= (coupling-legibility-line)
   (let* (($o (latest-coupling-ord)))
     (if (== $o 0)
         (let $line (py-call (helper.coupling_line_format 0 none window-filling window-filling window-filling 0 window-filling window-filling window-filling not-computed hidden))
           $line)
         (let* (($cc (latest-coupling-contact-count))
                ($ds (latest-coupling-dominant-surface))
                ($ch (latest-coupling-chain-state))
                ($ta (latest-coupling-task-accord))
                ($ca (latest-coupling-contact-accord))
                ($bd (current-coupling-band))
                ($sp (latest-coupling-support))
                ($rs (latest-coupling-residual-gap))
                ($tj (coupling-trace-verdict-for-window))
                ($nm (latest-coupling-next-move))
                ($hs (latest-coupling-honesty))
                ($car (coupling-contact-audit-render $ta $ca))
                ($line (py-call (helper.coupling_line_format $cc $ds $ch $ta $bd $sp $rs $tj $nm $hs $car))))
           $line))))
