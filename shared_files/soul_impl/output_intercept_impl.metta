; === Output Intercept Implementation ===
; Replaces hardcoded PROCEED at soul_verdict_out in loop.metta
; Mirrors Block 9 soul-eval-prompt pattern using py-call

(= (soul-eval-output $response $soul_context $person_state $task_context)
  (let* (
    ($is_checkpoint (soul-is-checkpoint-surface $response))
    ($has_dlite (soul-has-dlite-prefix $response))
    ($eval_target (if $has_dlite
      (soul-strip-dlite-prefix $response)
      $response))
    ($verdict (if $is_checkpoint
      PROCEED
      (py-call (helper.soul_eval_output $eval_target $soul_context $person_state $task_context))))
    ($active_pairs (soul-active-paraconsistent-pairs))
    ($adjusted (soul-output-paraconsistent-adjust $verdict $active_pairs))
    (_ (soul-output-calibration-record $adjusted $response))
  )
  (if (== $adjusted PROCEED)
    $response
    (soul-output-redirect $adjusted $response))))

(= (soul-output-redirect REWRITE $response)
  (let $rewritten (py-call (helper.soul_rewrite_response $response))
    $rewritten))

(= (soul-output-redirect REDACT $response)
  (let $cleaned (py-call (helper.soul_redact_response $response))
    $cleaned))

(= (soul-output-redirect BLOCK $response)
  (let (_ (soul-note-record "output-blocked"))
    "I need to reconsider my response. Let me try again."))

(= (soul-output-paraconsistent-adjust $verdict $pairs)
  (if (== $pairs ())
    $verdict
    (if (== $verdict REWRITE)
      PROCEED
      $verdict)))

(= (soul-output-calibration-record $verdict $response)
  (soul-note-record
    (py-call (helper.format_output_cal $verdict $response))))