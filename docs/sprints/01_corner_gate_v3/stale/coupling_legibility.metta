;; ============================================================
;; soul/coupling_legibility.metta -- Corner-Gate v3 pure surface
;; Draft A payload 1 of 3. Design canon: corner_gate_v3_adapter_design.md v0.6.
;; Status: DRAFT FOR BERTON LAYER-1 REVIEW. Not imported anywhere yet.
;;
;; PURPOSE: pure definitions for the coupling legibility surface. Shapes,
;; schema version, threshold constants, reader helpers, dominant-surface
;; cascade, Gate H honesty derivation, D7 mechanical derivations, band
;; position, and the per-field composers the writer calls.
;;
;; Side-effecting writers (do-*!) land in coupling_legibility_writers.metta.
;;
;; ATOM SHAPES (canonical, 17-field record per design doc 3.1):
;;   (coupling-cycle-record $ord $contact-count $dominant-surface $command-sig
;;                          $chain-state $polarity-verdict $accord-summary
;;                          $support $residual-gap $honesty-state $next-move
;;                          $ctx-phase $ctx-msgnew $ctx-soul
;;                          $producer $depends-on $ts)
;;   (coupling-band-state $band $from-ord)                 singleton
;;   (command-signature-state $sig $consecutive-fail-count $last-ord)  singleton
;;   (coupling-contact-event $ord $surface)                transient, folded per cycle
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
(= (coupling-legibility-schema-version) v3-17-field)

;; ------------------------------------------------------------
;; D10 threshold constants. Status: adapter-side tuning targets, not engine
;; law (ratified). Measure 7 collects the tuning data.
;; ------------------------------------------------------------
(= (coupling-lower-band) 0.4)
(= (coupling-upper-band) 0.6)

;; ------------------------------------------------------------
;; Small pure list helpers (recursion on collapsed lists; no match inside)
;; ------------------------------------------------------------
(= (coupling-list-empty $xs) (== $xs ()))

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

;; ------------------------------------------------------------
;; Reader helpers (ratified set of seven; design doc 3.1).
;; Consumers use these; no consumer writes a 17-field match by hand.
;; ------------------------------------------------------------

;; Latest ordinal in the window; 0 when the window is empty.
(= (latest-coupling-ord)
   (let $ords (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $g $h $i $j $k $l $m $n $p $q) $o))
     (if (== $ords ()) 0 (let $h (car-atom $ords) (coupling-max-num $ords $h)))))

;; Oldest ordinal in the window; 0 when empty (eviction support).
(= (oldest-coupling-ord)
   (let $ords (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $g $h $i $j $k $l $m $n $p $q) $o))
     (if (== $ords ()) 0 (let $h (car-atom $ords) (coupling-min-num $ords $h)))))

(= (coupling-window-count)
   (let $ords (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $g $h $i $j $k $l $m $n $p $q) $o))
     (size-atom $ords)))

;; INTERNAL COMPOSITION ONLY. Returns the whole record atom for the latest
;; ordinal. NEVER render, println, or py-str this value: tuple render throws
;; (Atom_Operations_Map read-instrument rule). Display-safe access is the
;; field helpers below.
(= (latest-coupling-record)
   (let* (($o (latest-coupling-ord))
          ($recs (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $g $h $i $j $k $l $m $n $p $q)
                                  (coupling-cycle-record $o $a $b $c $d $e $f $g $h $i $j $k $l $m $n $p $q)))))
     (if (== $recs ()) none (car-atom $recs))))

;; Field helpers: one scalar or symbol each (display-safe).
(= (latest-coupling-support)
   (let* (($o (latest-coupling-ord))
          ($xs (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $g $h $i $j $k $l $m $n $p $q) $g))))
     (if (== $xs ()) not-computed (car-atom $xs))))

(= (latest-coupling-next-move)
   (let* (($o (latest-coupling-ord))
          ($xs (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $g $h $i $j $k $l $m $n $p $q) $j))))
     (if (== $xs ()) not-computed (car-atom $xs))))

(= (latest-coupling-command-sig)
   (let* (($o (latest-coupling-ord))
          ($xs (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $g $h $i $j $k $l $m $n $p $q) $c))))
     (if (== $xs ()) none (car-atom $xs))))

(= (latest-coupling-polarity-verdict)
   (let* (($o (latest-coupling-ord))
          ($xs (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $g $h $i $j $k $l $m $n $p $q) $e))))
     (if (== $xs ()) not-computed (car-atom $xs))))

;; Context helper returns the three ctx fields as three separate reads.
(= (latest-coupling-ctx-phase)
   (let* (($o (latest-coupling-ord))
          ($xs (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $g $h $i $j $k $l $m $n $p $q) $k))))
     (if (== $xs ()) not-computed (car-atom $xs))))

(= (latest-coupling-lineage-producer)
   (let* (($o (latest-coupling-ord))
          ($xs (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $g $h $i $j $k $l $m $n $p $q) $n))))
     (if (== $xs ()) not-computed (car-atom $xs))))

;; Polarity verdict for a SPECIFIC ordinal (trajectory trace consumption).
(= (coupling-polarity-verdict-at $ord)
   (let $xs (collapse (match &self (coupling-cycle-record $ord $a $b $c $d $e $f $g $h $i $j $k $l $m $n $p $q) $e))
     (if (== $xs ()) not-computed (car-atom $xs))))

(= (coupling-support-at $ord)
   (let $xs (collapse (match &self (coupling-cycle-record $ord $a $b $c $d $e $f $g $h $i $j $k $l $m $n $p $q) $g))
     (if (== $xs ()) not-computed (car-atom $xs))))

;; Band singleton reads (scalar and symbol, safe because the writer keeps it
;; a singleton via remove-then-add).
(= (current-coupling-band)
   (let $xs (collapse (match &self (coupling-band-state $b $o) $b))
     (if (== $xs ()) window-filling (car-atom $xs))))

(= (current-coupling-band-ord)
   (let $xs (collapse (match &self (coupling-band-state $b $o) $o))
     (if (== $xs ()) 0 (car-atom $xs))))

;; Signature singleton reads.
(= (current-command-signature)
   (let $xs (collapse (match &self (command-signature-state $s $n $o) $s))
     (if (== $xs ()) none (car-atom $xs))))

(= (current-signature-fail-count)
   (let $xs (collapse (match &self (command-signature-state $s $n $o) $n))
     (if (== $xs ()) 0 (car-atom $xs))))

;; Contact events for an ordinal (surfaces as bare symbols; count by length).
(= (coupling-contact-surfaces $ord)
   (collapse (match &self (coupling-contact-event $ord $s) $s)))

;; ------------------------------------------------------------
;; Dominant-surface cascade (ratified deterministic priority order):
;; failed-query > runtime-output > tool-result/capability-result >
;; source-read > user-words > task-state > cycle-trace > none
;; One order, one function, one writer.
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
;; Command classification.
;; REVIEW-FLAG RF3: v1 command-class table for Berton markup.
;; action-class: produces or changes something. verification-class: reads or
;; queries a target. claim-class: outward claim event (send). narration-class:
;; pin. neutral: everything else.
;; ------------------------------------------------------------
(= (command-class-of write-file) action-class)
(= (command-class-of append-file) action-class)
(= (command-class-of shell) action-class)
(= (command-class-of remember) action-class)
(= (command-class-of read-file) verification-class)
(= (command-class-of query) verification-class)
(= (command-class-of episodes) verification-class)
(= (command-class-of metta) verification-class)
(= (command-class-of send) claim-class)
(= (command-class-of pin) narration-class)
(= (command-class-of search) neutral)
(= (command-class-of tavily-search) neutral)
(= (command-class-of technical-analysis) neutral)

;; ------------------------------------------------------------
;; GATE H: honesty state derivation (design doc 2.5, ratified mapping,
;; verbatim semantics). Targets are strings produced by the Python target
;; extractor; the sentinel string "unknown" means not mechanically knowable.
;; REVIEW-FLAG RF5: v1 claim-present proxy is the presence of a claim-class
;; (send) command in the cycle. Content is never read.
;; unknown target        -> not-computed        (never an accusation)
;; known + no same-target verification -> name-action-not-verification
;; known + same-target verified        -> claim-completion
;; ------------------------------------------------------------
(= (derive-honesty-state $has-action $has-claim $action-target $verify-target)
   (if (== $has-action False) not-computed
   (if (== $has-claim False) not-computed
   (if (== $action-target "unknown") not-computed
   (if (== $verify-target $action-target) claim-completion
       name-action-not-verification)))))

;; ------------------------------------------------------------
;; D7 mechanical derivations (ratified table, Step 0h) feeding the engine
;; reductions with THEIR OWN input vocabulary (quoted arities).
;; ------------------------------------------------------------

;; Self-seeing chain inputs.
(= (derive-repeat-symbol $failcount)
   (if (>= $failcount 2) repeated-failing-command one-off-failing-command))

;; REVIEW-FLAG RF6: v1 hidden-error proxy. Visible error feedback this cycle
;; means visible-error-surface. No visible error while the same signature
;; repeats without forward delta reads hidden-error-surface.
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

;; Chain-state composer: walks the engine self-seeing chain with quoted
;; reductions. Returns the strongest applicable state symbol for the cycle.
;; Order: navigation-change > orientation-shift > newly-visible-surface >
;; loop-capture-seen > healthy contact states.
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

;; TFS-2 polarity state derivations (ratified D7 table).
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

;; Polarity verdict via the quoted engine reduction. Inputs outside the
;; engine seeded combinations reduce to not-computed by the guard below.
(= (derive-polarity-verdict $protection $contactability $suspicion $polarity $pos)
   (let $v (collapse (q-tfs2-polarity-trajectory? $protection $contactability $suspicion $polarity $pos))
     (if (== $v ()) not-computed (car-atom $v))))

;; Trace verdict over the stored window (cycle 3 consumes cycles 1-3).
(= (derive-trace-verdict $v1 $v2 $v3)
   (let $v (collapse (q-tfs2-trace-verdict? same-start $v2 $v3))
     (if (== $v ()) not-computed (car-atom $v))))

;; ------------------------------------------------------------
;; Alignment legs (ratified D7): task accord and contact accord.
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

(= (contact-navigation-leg $probe)
   (if (== $probe corrective-probe) aligned aligned))
;; REVIEW-FLAG RF11: contact navigation leg is aligned in v1 pending the
;; N+1 evaluation wiring (navigation is judged at the NEXT cycle per design
;; doc 2.6). v1 renders the task accord; contact accord joins in v1.1.

(= (derive-accord-summary $i $a $o)
   (q-alignment-triplet-status? $i $a $o))

;; ------------------------------------------------------------
;; Evidence pbits, edges, chain, support.
;; REVIEW-FLAG RF7: v1 evidence constants for markup. Aligned legs carry
;; strength 0.9, misaligned 0.2; mechanical provenance caps confidence 0.7.
;; ------------------------------------------------------------
(= (leg-strength $leg) (if (== $leg aligned) 0.9 0.2))

(= (coupling-pbit-strength (mk-pbit $s $c)) $s)

(= (derive-support $ileg $aleg $oleg)
   (let* (($is (leg-strength $ileg))
          ($as (leg-strength $aleg))
          ($os (leg-strength $oleg))
          ($iapbit (mk-pbit $is 0.7))
          ($aopbit (mk-pbit $os 0.7))
          ($e1 (q-intention-action intention action $iapbit))
          ($e2 (q-action-outcome action outcome $aopbit))
          ($chain (q-coherence-chain $e1 $e2))
          ($cpbit (qalignment-pbit $chain))
          ($s (coupling-pbit-strength $cpbit)))
     $s))

;; ------------------------------------------------------------
;; Band position and hysteresis (quoted engine reduction; D10 constants).
;; REVIEW-FLAG RF10: v1 rapid-flip rule. A flip is current position at one
;; extreme while the stored band is the opposite stable extreme.
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
;; NOTE: within-band holds the PRIOR band per the engine semantics; the
;; stored singleton carries the effective band forward.

;; ------------------------------------------------------------
;; Residual gap (quoted engine reduction; symbolic output).
;; ------------------------------------------------------------
(= (derive-residual-gap $support $windowcount)
   (let* (($hi (coupling-upper-band))
          ($supsym (if (>= $support $hi) target-met current-support))
          ($ressym (if (>= $windowcount 2) residual-available residual-absent)))
     (q-residual-threshold-gap? $supsym target-threshold $ressym)))

;; ------------------------------------------------------------
;; Next epistemic move.
;; REVIEW-FLAG RF8 (prominent): the engine q-next-epistemic-move domain does
;; not include the self-seeing chain states v1 computes. Inventing a mapping
;; would author vocabulary the engine did not define. Per the unfed rule the
;; field carries not-computed in v1; populating it requires Berton-ratified
;; state mapping (candidate: trace-verdict blocked states to the engine
;; pathological-learning entries). Nothing is fabricated.
;; ------------------------------------------------------------
(= (derive-next-move $chainstate $traceverdict)
   not-computed)
