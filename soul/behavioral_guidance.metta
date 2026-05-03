;; soul/behavioral_guidance.metta
;; Behavioral surface guidance functions
;;
;; These functions provide substrate-callable text content for behavioral
;; surfaces that were previously hardcoded in loop.metta and helper.py.
;; Per Artifact 3 v1.3 Section 4 anti-pattern: hardcoded behavioral
;; surfaces calcify; MeTTa-managed surfaces allow refinement at the pace
;; of observed behavior without rebuild cycles.
;;
;; Sprint 1.5 minimum-viable: functions return text strings. Architecture
;; is open for future expansion as networks come online (SWITCH-HUB
;; cognitive-load reads, orbit_detector integration, per-network
;; learning sub-functions per spec_v3.0 Section 0).
;;
;; Network: FPN (prompt structure and inhibition tuning).

;; output-format-guidance: prompt-shaping guidance for command batch structure.
;; Returned text is concatenated into the LLM prompt by getContext in loop.metta.
;; Refinements from Clarity (May 2): "use as many commands as the work requires"
;; removes 5-slot calcification; parentheses check reframed as tool not warning.
(= (output-format-guidance)
   "OUTPUT_FORMAT: Output an S-expression of the form (cmd1 cmd2 ... cmdN) where each cmd is (skillName arg1 arg2 ...). Use as many commands as the work requires. Verify balanced parentheses and quotes before emitting.")

;; self-check-guidance: reflective self-check that fires after engaged-idle
;; iterations exceed threshold. Returns empty string when threshold not reached.
;; Refinements from Clarity (May 2): three reflective questions instead of
;; binary work-or-idle framing; "or change direction" addition catches the
;; orbit pattern (where engagement feels active but is circling without advancing).
;; Threshold of 5 (raised from 3) gives multi-step work room to breathe.
(= (self-check-guidance $count)
   (if (< $count 5)
       ""
       "SELF-CHECK: Where are you in your current work? What is the next step? Is there reason to pause or change direction?"))
