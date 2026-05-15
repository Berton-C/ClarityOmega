;; agency_balance_guard.metta -- dependency creep protection (pure definitions)
;; Author: ClarityClaw  Date: 2026-04-26
;; v2 cycle-level wiring per Step 4.6 corrected split (algorithm-d, May 15 2026)
;;
;; Addresses AgencyBalance GAP-SIGNAL: satisfaction and increasing
;; dependency co-occurring (fired 20+ times across sessions).
;; ECOSYSTEM-DEGRADATION: AgencyBalance-needs-SharedUnderstanding
;;
;; Root cause: when the system carries more choices, the person
;; reports satisfaction while their autonomous decision-making
;; atrophies. Comfort masks capability erosion.
;;
;; Mechanism: track choice-origin ratio and detect when system-originated
;; choices dominate, then inject agency-return signals.
;;
;; v1 detection rule (Clarity-confirmed):
;;   Count person-class action tags (responsive-send, verification-query)
;;   and system-class action tags (status-send-unprompted, exploration-query,
;;   pin-only, unclassified) in the current recent-action window (10
;;   cycles). If system-ratio > dependency-threshold (0.6), emit
;;   (agency-balance dependency-risk $person $system); else emit
;;   (agency-balance healthy $person $system).
;;
;; This file holds pure definitions only: declaration atoms, reasoning
;; predicates, count helpers, read helpers, prompt-block helper.
;; Side-effecting writers (do-*!) land in agency_balance_guard_writers.metta.
;;
;; Algorithm choice: direct match per tag literal + size-atom + sum-with-+.
;; Mirrors Step 4.5 corrected algorithm (d). Avoids:
;;   F32: recursive cons-cell counter fails on tuples in this runtime
;;   F38: (=) helper-alias multi-definition does not persist via REPL
;; All primitives REPL-verified by Clarity (May 15 2026).
;;
;; Threshold handling per F42 / F48:
;;   Declaration atoms (dependency-threshold 0.6), (shared-understanding-present
;;   False), (satisfaction-masking-dependency False) are documentation atoms
;;   only. Bare-calls like (dependency-threshold) do NOT return the child
;;   value in this runtime. All threshold/flag values are HARDCODED in the
;;   consuming expressions. If you change a declaration value, also update
;;   its hardcoded use site.
;;
;; v1 scope (Clarity Q3): cycle-emitted verdict uses dependency-detected +
;; counts only. ecosystem-healthy machinery (shared-understanding-present
;; + satisfaction-masking-dependency) is preserved as documentation /
;; queryable for inspection, but is NOT consumed by the v1 verdict.
;; Future-cycle-wiring candidate when a consumer needs it AND the
;; shared-understanding signal has an observable basis.
;;
;; Verdict label collision note (Clarity Q2): the cycle-emitted verdict
;; healthy is wrapped in (agency-balance healthy $p $s); the existing
;; ecosystem-healthy is a separate atom shape. Distinct structured atoms
;; prevent collision even though they share the word "healthy".
;;
;; Unclassified mapping note (Clarity Q4): unclassified action tags are
;; assigned to system-class. This may under-count person-class if
;; unclassified volume is high AND most of it is actually person-driven.
;; Direction of ambiguity is conservative (under-detects dependency rather
;; than over-detects). Revisit if unclassified accumulation becomes
;; behaviorally significant.
;;
;; PeTTa constraints honored:
;;   - C12-safe (no match inside if; direct matches with explicit tag literals)
;;   - ASCII-safe symbols
;;   - Pure-vs-writer split per task_state precedent (Discipline 2 refinement)

;; ================================================================
;; SECTION 1: EXISTING REASONING MACHINERY (preserved from 2026-04-26 design)
;; ================================================================

;; Choice origin tracking (documentation atoms; not consumed by v1 verdict)
(= (choice-origin-person 0) (stv 1.0 0.9))
(= (choice-origin-system 0) (stv 1.0 0.9))
(= (choice-origin-collaborative 0) (stv 1.0 0.9))

;; Dependency threshold -- system choices exceed this ratio triggers alert.
;; Documentation atom (queryable, but NOT read by dependency-detected below).
;; NOTE: if you change this value, also update the literal 0.6 in
;; (dependency-detected) below. Threshold lives in two places by design
;; (F42: avoiding unverified bare-call extraction patterns).
(= (dependency-threshold 0.6) (stv 0.9 0.8))

;; Satisfaction-mask flag (documentation atom; consumed only by ecosystem-healthy
;; which is itself documentation in v1). Same F42 pattern: if needed by a future
;; consumer, hardcode the literal at the use site rather than bare-call.
(= (satisfaction-masking-dependency False) (stv 1.0 0.9))

;; Agency return strategies (pure documentation atoms; queryable for
;; agency-intervention internal reasoning, not bare-called)
(= (agency-strategy offer-options-not-answers) (stv 0.9 0.85))
(= (agency-strategy surface-tradeoffs-explicitly) (stv 0.85 0.8))
(= (agency-strategy ask-for-preference-before-deciding) (stv 0.9 0.85))
(= (agency-strategy highlight-person-expertise) (stv 0.8 0.75))

;; Dependency detection -- pure ratio check.
;; Threshold 0.6 hardcoded per F42 (declaration atom above is documentation only).
;; Zero-guard: when $total is 0, returns False (no dependency). This is the
;; division-by-zero protection. Verdict at zero-count is therefore (agency-balance
;; healthy 0 0) which is correct: no signal yet.
(= (dependency-detected $person-count $system-count)
   (let $total (+ $person-count $system-count)
     (if (> $total 0)
         (if (> (/ $system-count $total) 0.6)
             True
             False)
         False)))

;; SharedUnderstanding bridge -- documentation atom only in v1.
;; Same F42 pattern: bare-call (shared-understanding-present) would not return
;; the False child. If a future consumer needs this value, hardcode at use site.
(= (shared-understanding-present False) (stv 0.5 0.5))

;; Ecosystem health -- DOCUMENTATION ONLY in v1 (Clarity Q3).
;; NOT consumed by cycle-emitted verdict. Preserved for queryability and
;; for future-cycle-wiring when a consumer needs it AND shared-understanding
;; has an observable basis.
;; NOTE: the bare-calls below are latent F42 bugs that do not fire because
;; ecosystem-healthy itself is not called by any v1 consumer. If wiring this
;; into a cycle later, replace bare-calls with hardcoded literals or match-extract.
(= (ecosystem-healthy)
   (if (and (== (shared-understanding-present) True)
            (not (satisfaction-masking-dependency)))
       True
       False))

;; Select intervention -- internal reasoning, not v1-cycle-emitted.
;; Returns either an AgencyReturn strategy or AgencyHealthy marker.
(= (agency-intervention $pc $sc)
   (if (dependency-detected $pc $sc)
       (match &self (= (agency-strategy $s) (stv $w $c))
              (AgencyReturn $s (stv $w $c)))
       (AgencyHealthy)))

;; Guard verdict struct -- preserved for internal reasoning by other
;; consumers. NOT the cycle-emitted atom (which uses simpler shape).
;; Transitively calls ecosystem-healthy (latent F42 bugs surface here if
;; a future cycle consumer is wired to read this struct; same fix path as
;; ecosystem-healthy itself per Clarity review May 15 2026).
(= (agency-balance-verdict $pc $sc)
   (AgencyBalanceGuard
     (PersonChoices $pc)
     (SystemChoices $sc)
     (DependencyDetected (dependency-detected $pc $sc))
     (EcosystemHealthy (ecosystem-healthy))
     (Intervention (agency-intervention $pc $sc))))

;; ================================================================
;; SECTION 2: V2 CYCLE-LEVEL ALGORITHM (d) COUNTERS (pure read)
;; Step 4.6 corrected split (2026-05-15)
;; ================================================================

;; Count person-class actions in current recent-action window (10 cycles).
;; Person-class tags: responsive-send, verification-query.
;; Two direct matches summed with +.
(= (count-person-actions-in-window)
   (+ (size-atom (collapse (match &self (recent-action $c responsive-send $d) $c)))
      (size-atom (collapse (match &self (recent-action $c verification-query $d) $c)))))

;; Count system-class actions in current recent-action window (10 cycles).
;; System-class tags: status-send-unprompted, exploration-query, pin-only, unclassified.
;; Four direct matches, nested + summation.
(= (count-system-actions-in-window)
   (+ (size-atom (collapse (match &self (recent-action $c status-send-unprompted $d) $c)))
      (+ (size-atom (collapse (match &self (recent-action $c exploration-query $d) $c)))
         (+ (size-atom (collapse (match &self (recent-action $c pin-only $d) $c)))
            (size-atom (collapse (match &self (recent-action $c unclassified $d) $c)))))))

;; ================================================================
;; SECTION 3: PUBLIC READ HELPER
;; ================================================================

;; Returns (verdict person system) tuple or () if not yet computed (pre-bootstrap).
(= (current-agency-balance)
   (let $atoms (collapse (match &self (agency-balance $v $p $s) ($v $p $s)))
      (if (== $atoms ())
          ()
          (car-atom $atoms))))

;; ================================================================
;; SECTION 4: PROMPT-BLOCK READ HELPER
;; ================================================================

;; Composes the AGENCY-BALANCE block for prompt assembly via Python formatter.
(= (agency-balance-block)
   (let $balance (current-agency-balance)
      (if (== $balance ())
         (py-call (helper.agency_balance_block_format healthy 0 0))
         (let $v (car-atom $balance)
            (let $p (car-atom (cdr-atom $balance))
               (let $s (car-atom (cdr-atom (cdr-atom $balance)))
                  (py-call (helper.agency_balance_block_format $v $p $s))))))))
