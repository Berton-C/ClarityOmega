;; cycle_continuity_probe.metta -- behavior-stasis observer via lib_self_continuity (pure)
;; Author: ClarityClaw. Granularity-layer reference draft 2026-06-03.
;; Predecessors: investigation 2026-06-03 v2, lib_self_continuity.metta,
;;   lib_quantale.metta, coupling_quantale_merge.metta.
;;
;; WHAT THIS FILE IS. The granularity code that makes lib_self_continuity useful
;; for the corner gate. lib_self_continuity computes a self-continuity score
;; between two Pattern-Flow Network snapshots: HIGH score means the prior pattern
;; persisted unchanged. Aimed at 2h thread continuity, it is COLD. Here it is
;; pointed at a per-cycle grain: snapshot the agent's ACTION-CLASS PROFILE each
;; cycle and measure whether that profile is frozen across cycles. A frozen
;; profile while emitting is the repetition flavor of a corner.
;;
;; HOW IT FITS THE CORNER (important polarity note). behavior-stasis is NOT a
;; required conjunct of the core corner. If it were, requiring frozen behavior
;; would MISS varied flailing (which is also a corner). Instead it is a SECOND
;; corner arm: the system fires on EITHER the core severed-chain corner OR a
;; strong frozen-behavior-while-emitting corner. The two arms are OR-merged with
;; q-join (the observer_relativity "any observer firing" pattern). This gives
;; lib_self_continuity a real role (the repetition arm) without making it gate
;; the flailing case.
;;
;; HONEST CAVEATS (this is the higher-risk harvest):
;;   - self-continuity-score is DIRECTIONAL (residuation detects edges that
;;     WEAKENED, not pure symmetric change). Frozen profile => score 1.0 (the key
;;     case). A profile that only adds without dropping any class can read as
;;     frozen; acceptable here because the repetition case is the target.
;;   - The natural payoff of self-continuity grows with the richness of the state
;;     profile. At a thin per-cycle grain it is a single observer; its larger home
;;     is the 2h whole-state continuity it was built for. This is the cheaper
;;     near-term application of the same machinery.
;;
;; DEPENDS ON: lib_self_continuity (self-continuity-score, pfn, edge, Cons, Nil),
;; the v08.7.2 quantale engine (mk-pbit, q-meet, q-join, q-unknown), q-geq from
;; lib_self_continuity, coupling_quantale_merge
;; (safe-ratio, emission-pbit, outcome-flat-pbit, corner-pbit-core,
;; corner-threshold-pbit).
;;
;; CONFIRM (REPL, both libraries COLD and term-storage untested):
;;   - self-continuity-score reduces on these pfn inputs and returns a pbit.
;;   - build-cycle-pfn computes numeric weights (rates bound in let*, so mk-pbit
;;     gets numbers, and pfn/Cons/edge/mk-pbit are inert constructors), so the
;;     stored snapshot is clean data, not an unreduced expression.
;;   - the no-prior bootstrap path returns q-unknown rather than a false 1.0.
;;
;; PeTTa constraints: C12-safe, ASCII-safe, no RMW.

;; ----------------------------------------------------------------
;; SNAPSHOT BUILDER: this cycle's action-class profile as a pfn
;; ----------------------------------------------------------------
;; Nodes: a single profile node. Edges: one per real action class, weighted by the
;; class's normalized rate in the window. Rates computed as numbers in let* first,
;; so the assembled pfn holds literal numeric pbits.
(= (build-cycle-pfn)
   (let* (($rs (size-atom (collapse (match &self (recent-action $c responsive-send $d) $c))))
          ($su (size-atom (collapse (match &self (recent-action $c status-send-unprompted $d) $c))))
          ($vq (size-atom (collapse (match &self (recent-action $c verification-query $d) $c))))
          ($eq (size-atom (collapse (match &self (recent-action $c exploration-query $d) $c))))
          ($po (size-atom (collapse (match &self (recent-action $c pin-only $d) $c))))
          ($total (+ $rs (+ $su (+ $vq (+ $eq $po)))))
          ($conf  (min 0.9 (safe-ratio $total 5))))
      (pfn (Cons profile Nil)
           (Cons (edge profile responsive-send        (mk-pbit (safe-ratio $rs $total) $conf))
           (Cons (edge profile status-send-unprompted (mk-pbit (safe-ratio $su $total) $conf))
           (Cons (edge profile verification-query     (mk-pbit (safe-ratio $vq $total) $conf))
           (Cons (edge profile exploration-query      (mk-pbit (safe-ratio $eq $total) $conf))
           (Cons (edge profile pin-only               (mk-pbit (safe-ratio $po $total) $conf))
                 Nil))))))))

;; ----------------------------------------------------------------
;; BEHAVIOR-STASIS PBIT (the repetition observer)
;; ----------------------------------------------------------------
;; Compares the stored prior profile to this cycle's profile via
;; self-continuity-score. HIGH continuity == frozen behavior == repetition signal.
;; Bootstrap (no prior snapshot) returns q-unknown so it does not drive the meet.
(= (behavior-stasis-pbit)
   (let $snaps (collapse (match &self (cycle-pfn-snapshot $p) $p))
      (if (== $snaps ())
          (mk-pbit 0.5 0.0)
          (self-continuity-score (car-atom $snaps) (build-cycle-pfn)))))

;; ----------------------------------------------------------------
;; REPETITION CORNER ARM
;; ----------------------------------------------------------------
;; Emitting AND outcome-flat AND behavior frozen. Reuses the core joints for
;; emission and outcome-flat; substitutes behavior-stasis for the intention joint.
(= (corner-pbit-repetition)
   (q-meet (emission-pbit)
           (q-meet (outcome-flat-pbit)
                   (behavior-stasis-pbit))))

;; ----------------------------------------------------------------
;; FULL CORNER PBIT (either arm) and gate
;; ----------------------------------------------------------------
;; q-join (max strength) fires on EITHER the severed-chain corner OR the
;; frozen-behavior corner. This is the multi-observer "any observer firing" merge.
(= (corner-pbit-full)
   (q-join (corner-pbit-core) (corner-pbit-repetition)))

(= (corner-confirmed-full)
   (q-geq (corner-pbit-full) (corner-threshold-pbit)))
