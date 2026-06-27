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
   "OUTPUT_FORMAT: Emit one command per line. The rule for each command line, exactly: open with a single left parenthesis, then the skill name as the very first token, then one space, then the argument as one double-quoted string, then a single right parenthesis. One pair of parentheses per line, never two, never more. Nothing before the opening parenthesis and nothing after the closing parenthesis on that line. Examples, each a complete line: (send \"hello there\") and (metta \"(match &self foo bar)\") and (pin \"checking the file now\"). Put as many command lines as the work requires, each on its own line. Do all of your thinking and deliberation BEFORE the command lines, never mixed into them: the command lines are commands only, not reasoning or notes. The argument is always one double-quoted string (multi-word arguments must be a single quoted string), and variables are forbidden. For write-file and append-file, the file content argument may span multiple lines; that is the one place multi-line content belongs. pin takes a brief single-line note, never a monologue.")

;; self-check-guidance: reflective self-check that fires after engaged-idle
;; iterations exceed threshold. Returns empty string when threshold not reached.
;; Refinements from Clarity (May 2): three reflective questions instead of
;; binary work-or-idle framing; "or change direction" addition catches the
;; orbit pattern (where engagement feels active but is circling without advancing).
;; Threshold of 5 (raised from 3) gives multi-step work room to breathe.
;;
;; STEP 5 (May 15 2026): caller in loop.metta retired. The SELF-CHECK
;; prompt surface is no longer assembled into the LLM prompt; TASK-STATE
;; block (Step 4), IDLE-PATTERN block (Step 4.5), and AGENCY-BALANCE block
;; (Step 4.6) now carry the orientation work via observable cycle-level
;; primitives rather than via a counter threshold + reflective questions.
;; The function definition stays intact for queryability and for potential
;; future task-phase-driven gating; the &engaged_idle_count counter is
;; still written by loop.metta but has no readers in v1 (α scope decision,
;; deferred removal to Step 8/9).
(= (self-check-guidance $count)
   (if (< $count 5)
       ""
       "SELF-CHECK: Where are you in your current work? What is the next step? Is there reason to pause or change direction?"))
