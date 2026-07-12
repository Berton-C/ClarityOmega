;; soul/proceed_voice.metta -- Extension B: soul-authored voice on the PROCEED path
;; Author: Claude (drafted). Consulted: Clarity (per-field binding; base-stance frame).
;; Spec: extension_b_proceed_voice_build_spec.md v1.5. Ground truth: Atom_Operations_Map.md.
;;
;; WHAT THIS FILE IS. The MeTTa side of Extension B. On a conversational PROCEED
;; (a lone send, nothing else), it rewrites the agent's drafted send through the
;; soul voice composer so the response carries the soul's stance and satisfies the
;; soul's note, instead of going out assessment-blind (the Uncle_Fester gap). The
;; pre-LLM strip in soul_send_assemble is untouched; this is a post-LLM transform.
;;
;; CONTROL FLOW IS HERE (MeTTa). The only Python is the prompt and the output
;; cleaner (helper.soul_proceed_voice_prompt, helper.soul_proceed_voice_clean),
;; both at the LLM I/O boundary. Routing, the lone-send test, the binding gate,
;; and atom reconstruction are MeTTa.
;;
;; LOOP CONTRACT (Layer 5, loop.metta). One hook between $sexpr_gated (line 166)
;; and execution (line 167):
;;     ($sexpr_composed (compose-proceed-voice $soul_decision $sexpr_gated
;;                                             $person_state $soul_verdict_in (provider)))
;; and line 167 consumes $sexpr_composed instead of $sexpr_gated. Line 173
;; (results_nonempty) keeps reading $sexpr_gated (count unchanged by composition).
;;
;; MeTTa SAFETY (Atom_Operations_Map.md):
;;   - lone-send detection reuses the proven (any (collapse (let $c (superpose ...))))
;;     idiom (cycle-has-send?, cycle_classifier.metta) and the (size-atom (collapse
;;     (superpose ...))) count idiom (loop 173, idle_cycle_detector).
;;   - send-payload separates the list-op (car-atom of a value) from the head
;;     destructure (extract-send-arg on a flat compound, cf external-skill?),
;;     avoiding nested-function-call-in-bind non-reduction (Map Section 3).
;;   - compose-proceed-voice sequences every step in let* so each bind RHS has
;;     value args (the nested-fn-call-in-bind trap, Map Section 3).
;;   - empty-string test uses (> (string_length ...) 0), never (== ... ""):
;;     py-call empty string does not equal MeTTa "" (Map / soul-state physics).
;;   - operates on $sexpr_gated, which already survived line 167's superpose, so
;;     superpose here is C6-safe; when cornered or paused it is (), also safe
;;     (superpose of () yields nothing; the C6 crash is superpose of an error atom).

;; ================================================================
;; SECTION 1: DISCRIMINATOR -- is this a lone-send PROCEED?
;; ================================================================

;; True when the output decision is proceed AND the command list is exactly one
;; send command. Reuses cycle-has-send? (cycle_classifier.metta). On () (cornered
;; or paused) the count is 0 and cycle-has-send? is False, so this is False.
(= (lone-send-proceed? $decision $cmds)
   (let $count (size-atom (collapse (superpose $cmds)))
        (and (== $decision proceed)
             (and (== $count 1)
                  (cycle-has-send? $cmds)))))

;; ================================================================
;; SECTION 2: BINDING-PRESENCE GATE -- is there compositional work?
;; ================================================================
;; Per Clarity (2026-06-18): the gate detects a compositional DELTA from the base
;; rhythm, not charge versus absence. The five SOUL-TONE values are distinct
;; STANCES, not volumes; none is "neutral". "grounded" is the base cadence --
;; present-without-particular-direction, the unmarked-but-active baseline the
;; system walks in when nothing is asked of the stance. So the skip condition is
;; base-stance AND no note; the gate fires on a note OR a departure from base rhythm.

;; True when the verdict's SOUL-TONE is the base rhythm (grounded).
;; string-contains (soul_utils.metta) routes through the proven contains_token bridge.
(= (at-base-stance? $verdict)
   (string-contains $verdict "SOUL-TONE: grounded"))

;; True when a SOUL-NOTE field is present and non-empty.
;; soul-extract-soul-note (soul_utils.metta) -> helper.extract_after; "" if absent.
;; (> (string_length ...) 0), never (== ... ""): py-call "" does not equal MeTTa "".
(= (soul-note-present? $verdict)
   (let $note (soul-extract-soul-note $verdict)
        (> (string_length $note) 0)))

;; The gate: fire on a note OR a departure from the base rhythm.
(= (binding-work-exists? $verdict)
   (or (soul-note-present? $verdict)
       (not (at-base-stance? $verdict))))

;; ================================================================
;; SECTION 3: SEND PAYLOAD -- extract and reconstruct
;; ================================================================

;; Extract the message string from a send command. Flat-compound head destructure,
;; proven (cf external-skill? (send $arg) in soul_utils.metta).
(= (extract-send-arg (send $arg)) $arg)

;; The agent's drafted message. car-atom of the command tuple (a bound value, so it
;; reduces), then destructure the command. Shape guaranteed ((send $arg)) upstream
;; by lone-send-proceed?. Sequenced (not nested) per Map Section 3.
(= (send-payload $cmds)
   (let $cmd (car-atom $cmds)
        (extract-send-arg $cmd)))

;; Rebuild the one-command tuple with the composed text. Same tuple-of-commands
;; shape line 167's (superpose $sexpr_composed) consumes.
(= (rewrite-send-payload $cmds $text)
   ((send $text)))

;; ================================================================
;; SECTION 4: COMPOSER -- guided rehabilitation of the draft
;; ================================================================
;; Three-input guided rehabilitation (Clarity, confirmed): person-state +
;; $soul_verdict_in + the agent's drafted send. The draft is content-source only;
;; SOUL-NOTE overrides draft framing; substance is never added, altered, or omitted
;; (bounded-restructure guardrail). Every step is sequenced in let* so each bind RHS
;; has value args (Map Section 3 nested-fn-call rule). The LLM call (soul-llm-call,
;; soul_utils.metta line 366, takes the provider) and its cleaning are the Python
;; I/O pair; the rewrap is MeTTa. When the gate is not met, return $cmds unchanged.
(= (compose-proceed-voice $decision $cmds $person $verdict $provider)
   (if (and (lone-send-proceed? $decision $cmds)
            (binding-work-exists? $verdict))
       (let* (($draft    (send-payload $cmds))
              ($prompt   (py-call (helper.soul_proceed_voice_prompt $person $verdict $draft)))
              ($raw      (soul-llm-call $prompt $provider))
              ($clean    (py-call (helper.soul_proceed_voice_clean $raw)))
              ($composed (rewrite-send-payload $cmds $clean)))
             $composed)
       $cmds))
