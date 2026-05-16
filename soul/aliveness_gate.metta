;; Aliveness Gate v9 -- Substrate-derived gating (Step 6 task-state primitive consumer)
;; Step 6 of task-state-primitive mini-sprint, May 16 2026.
;;
;; THE DUPLICATE-ENGAGEMENT BUG FIX MOMENT (per spec Section 10):
;; The gate now composes three substrate observation organs to decide
;; ENGAGE vs SILENT, replacing the binary latch-state-only logic with
;; phase + idle-pattern + agency-balance composition.
;;
;; Naming note: the $idle parameter of (aliveness-gate $msgnew $idle)
;; is the IDLE DIRECTIVE STRING from loop.metta line 90 (a Python-helper
;; output, non-empty when wakeup-interval expired and idle work is
;; being prepared). DO NOT confuse with (current-idle-pattern) which
;; is a substrate atom shape reporting the action pattern in the
;; 10-cycle recent-action window. These are different sources; the
;; naming similarity is historical (signature preserved for Step 6
;; per Berton, May 16 2026).
;;
;; Priority order (deliberate, not arbitrary):
;;   First check: idle_directive present OR msgnew -> ENGAGE
;;                (scheduled wakeup work OR active conversation context)
;;   Else (no human signal, no scheduled idle work):
;;     1. send-burst verdict -> SILENT (idle-pattern says too many recent sends)
;;     2. dependency-risk verdict -> SILENT (agency-balance says system-driven)
;;     3. task-phase in {attending, idle, waiting, reflecting} -> SILENT
;;        (nothing worth surfacing per task-state primitive;
;;         attending=aware-but-nothing-to-surface, idle=chosen-silence,
;;         waiting=awaiting-human-event, reflecting=not-yet-ready-to-speak)
;;     4. task-phase in {engaged, research, response-drafting, boundary-detected}
;;        -> fall through to legacy latch-state dispatch (Step 8 removes
;;        this branch; after removal these phases directly ENGAGE)
;;     5. Pre-bootstrap or unhandled phase value -> latch-state dispatch
;;        -> latch-dispatch defaults SILENT for unknown states
;;        (every unhandled path defaults to silence; verified by Clarity
;;         May 16 2026)
;;
;; Per-step pre-bootstrap safety:
;;   (current-idle-pattern) returns () pre-bootstrap -> falls through to
;;     agency-balance check
;;   (current-agency-balance) returns () pre-bootstrap -> falls through to
;;     task-phase check
;;   (current-phase) defaults to attending if no atom (per task_state.metta)
;;     -> SILENT via attending case
;;
;; All transitions for pre-bootstrap and unhandled paths default to SILENT.
;; This is the conservative failure mode: over-silencing beats over-engaging
;; during the Steps 6-8 transition window (Clarity-confirmed May 16 2026).

;; ================================================================
;; SECTION 1: ENTRY POINT
;; Preserves v8 signature for loop.metta line 107 compatibility.
;; ================================================================

(= (aliveness-gate $msgnew $idle)
  (if (> (string_length $idle) 0)
    ENGAGE
    (aliveness-gate-default $msgnew)))

;; ================================================================
;; SECTION 2: DEFAULT BRANCH (idle directive empty)
;; ================================================================

;; msgnew=True with empty idle directive -> ENGAGE
;; (Active conversation signal; gate respects human input direction.)
(= (aliveness-gate-default True) ENGAGE)

;; msgnew=False with empty idle directive -> begin substrate composition.
;; Step 1: check idle-pattern verdict.
(= (aliveness-gate-default False)
  (gate-on-idle-pattern (current-idle-pattern)))

;; ================================================================
;; SECTION 3: IDLE-PATTERN CHECK (Step 1 of priority order)
;; ================================================================

;; Pre-bootstrap: (current-idle-pattern) returns () -> fall through.
(= (gate-on-idle-pattern ())
  (gate-on-agency-balance (current-agency-balance)))

;; Bootstrap normal: ($verdict $count) tuple.
;; send-burst -> SILENT (THE duplicate-engagement bug fix; prevents
;; ENGAGE when too many sends have fired in the recent-action window).
(= (gate-on-idle-pattern ($v $c))
  (if (== $v send-burst)
      SILENT
      (gate-on-agency-balance (current-agency-balance))))

;; ================================================================
;; SECTION 4: AGENCY-BALANCE CHECK (Step 2 of priority order)
;; ================================================================

;; Pre-bootstrap: (current-agency-balance) returns () -> fall through.
(= (gate-on-agency-balance ())
  (gate-on-task-phase (current-phase)))

;; Bootstrap normal: ($verdict $person $system) tuple.
;; dependency-risk -> SILENT (only reached here when msgnew=False per
;; outer dispatch; human input present is handled at entry-point ENGAGE.
;; Spec note: dependency-risk silence applies only-when-no-msgnew per
;; Clarity Q3 May 15 2026.)
(= (gate-on-agency-balance ($v $p $s))
  (if (== $v dependency-risk)
      SILENT
      (gate-on-task-phase (current-phase))))

;; ================================================================
;; SECTION 5: TASK-PHASE CHECK (Step 3 of priority order)
;; Phase vocabulary per task-state-primitive_design.md Section 5.
;; Mapping per Clarity May 16 2026:
;;   SILENCE: attending, idle, waiting, reflecting
;;   ENGAGE-fall-through: engaged, research, response-drafting, boundary-detected
;;   Unknown -> fall through (latch dispatches; defaults SILENT for unknown)
;; ================================================================

(= (gate-on-task-phase attending) SILENT)
(= (gate-on-task-phase idle) SILENT)
(= (gate-on-task-phase waiting) SILENT)
(= (gate-on-task-phase reflecting) SILENT)
(= (gate-on-task-phase engaged) (gate-on-latch-fallback))
(= (gate-on-task-phase research) (gate-on-latch-fallback))
(= (gate-on-task-phase response-drafting) (gate-on-latch-fallback))
(= (gate-on-task-phase boundary-detected) (gate-on-latch-fallback))
(= (gate-on-task-phase $other) (gate-on-latch-fallback))

;; ================================================================
;; SECTION 6: LEGACY LATCH-STATE FALLBACK (Step 4 of priority order)
;; Preserves v8 latch-dispatch logic during Steps 6-8 transition window.
;; Step 8 of mini-sprint removes this section and the latch-state
;; writes in loop.metta lines 94, 99. After Step 8, working/research/
;; response-drafting/boundary-detected go directly to ENGAGE.
;; ================================================================

(= (gate-on-latch-fallback)
  (latch-dispatch (match &self (latch-state $s) $s)))

(= (latch-dispatch IDLE) SILENT)
(= (latch-dispatch ENGAGED) ENGAGE)
(= (latch-dispatch COMPLETING) ENGAGE)
(= (latch-dispatch $other) SILENT)
