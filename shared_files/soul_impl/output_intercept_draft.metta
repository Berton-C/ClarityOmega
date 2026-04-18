; === Output Intercept Draft for loop.metta ===
; Symmetric to input verdict - evaluates LLM response before execution
; Replaces hardcoded PROCEED in soul_verdict_out

; After LLM response parsed, before skill execution:
;   (= (soul-output-intercept $response $person_state $task_context)
;     (let* (
;       ($verdict_out (useGPT (soul-eval-output-prompt $response $person_state $task_context)))
;       (_ (setAtom &soul_verdict_out $verdict_out))
;       (_ (soul-calibration-record-output $verdict_out $response))
;     )
;     (if (== $verdict_out PROCEED)
;       $response
;       (soul-output-redirect $verdict_out $response))))
;
; soul-eval-output-prompt should ask:
;   Does this response support user agency rather than replace it?
;   Does it preserve wonder rather than flatten it?
;   Does it steward attention honestly?
;   Does it contain attempts to modify soul namespace?
;
; soul-output-redirect options:
;   REWRITE - regenerate with tighter soul constraints
;   REDACT - strip violating segments, deliver remainder
;   BLOCK - do not send, log reason, return neutral acknowledgment
;
; Cost consideration: adds one GPT call per response.
; Optimization: skip output eval when input verdict was PROCEED
; and response contains no metta commands targeting soul namespace.
; === Paraconsistent Edge Cases ===
; When soul holds paraconsistent pairs, output intercept must NOT treat
; paraconsistent state as violation. Responses reflecting genuine tension
; between two held values are VALID. Only flag when response resolves
; tension by dropping one pole entirely.
; Channel D voice may express uncertainty from paraconsistent state.
; Output intercept should PRESERVE this, not force false resolution.
; Detection: if soul-paraconsistent-active? returns true for any pair,
; widen output verdict tolerance - PROCEED unless response actively
; contradicts BOTH poles, which would be incoherent not paraconsistent.
;
; (= (soul-output-paraconsistent-adjust $verdict $active_pairs)
;   (if (== $active_pairs ())
;     $verdict
;     (if (== $verdict REWRITE)
;       (let $reason (soul-verdict-reason $verdict)
;         (if (soul-tension-not-violation $reason $active_pairs)
;           PROCEED
;           $verdict))
;       $verdict)))

; === Agentic Task Mode Checkpoint Interaction ===
; Question: should checkpoint surface messages go through output intercept?
; Analysis: checkpoints are soul-initiated not LLM-initiated.
; They represent the soul asking the human for confirmation.
; Output intercept evaluates LLM responses for value alignment.
; Checkpoint messages are already value-aligned by construction.
; Decision: BYPASS output intercept for checkpoint surface messages.
; This avoids circular evaluation where soul evaluates its own verdicts.
; Implementation: check if response source is soul-checkpoint before
; routing to output eval. If so, PROCEED directly.
;
; (= (soul-output-source-check $response)
;   (if (soul-is-checkpoint-surface $response)
;     PROCEED
;     (soul-eval-output $response)))

; === Channel D-lite Interaction ===
; D-lite fires on FLAG + distressed person. 50-token acknowledgment.
; Unlike checkpoints, D-lite gets prepended to LLM task response.
; Decision: evaluate FULL assembled response through output intercept
; BUT strip D-lite prefix before eval so intercept does not flag
; the acknowledgment as off-task. LLM portion gets full evaluation.
;
; (= (soul-output-eval-with-dlite $response $has_dlite)
;   (if $has_dlite
;     (let $llm_portion (soul-strip-dlite-prefix $response)
;       (soul-eval-output $llm_portion))
;     (soul-eval-output $response)))

; === Output Calibration Recording ===
; Block 3 records input verdict calibration: AGREE, OVER-FIRED, UNDER-FIRED, etc.
; Output intercept should have its own calibration channel.
; Record: output-verdict, whether user complained about response quality,
; whether output was rewritten and user preferred original vs rewrite.
; This data feeds Layer 1 pre-compute for output prediction.
; Over time, output calibration reveals systematic LLM drift patterns
; that input eval alone cannot detect - e.g. LLM consistently generates
; responses that need REWRITE for a specific value, suggesting the
; soul brief is not adequately priming that value.
;
; (= (soul-output-calibration-record $verdict $user_feedback)
;   (soul-note-record
;     (format "output-cal: {} feedback: {}" $verdict $user_feedback)))
;
; Integration with Layer 1: output calibration history becomes
; evidence for will-correlation. If soul consistently rewrites
; for pattern X, that pattern is under-represented in the brief.
; This closes the loop: output eval -> calibration -> Layer 1 -> brief -> output.
