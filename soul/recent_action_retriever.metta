;; soul/recent_action_retriever.metta
;; Reads recent-action atoms from AtomSpace and assembles YOUR_LAST_ACTION
;; block for getContext consumption.
;;
;; Architecture (per Clarity's design, May 3, 2026):
;;   - cycle_classifier.metta: pure classification (input -> tag)
;;   - recent_action_populator.metta: side-effecting (assert + prune)
;;   - recent_action_retriever.metta: prompt-context read path -- THIS FILE
;;   - orbit_detector.metta: pattern-matching read path (separate consumer)
;;
;; The retriever surfaces the last 3 cycles' actions to the LLM prompt for
;; cross-iteration self-awareness. Inhibits announcement loops and behavioral
;; perseveration by giving the LLM visibility into what it just did.
;;
;; Sort-free design (per Clarity's recommendation): cycle-id arithmetic +
;; explicit descending lookup. No sort over collapsed atoms required.
;;
;; MeTTa-first division of labor:
;;   - MeTTa owns: window arithmetic, three explicit cycle-id matches,
;;                 orchestration, calling Python helpers
;;   - Python owns: string truncation, line formatting, empty filtering,
;;                  sentinel logic, newline composition (per PeTTa C1
;;                  constraint -- nested py-str hangs in MeTTa function
;;                  definition contexts whose results feed outer py-str)

;; Window: how many recent actions to surface in YOUR_LAST_ACTION block
(= (recent-actions-window) 3)

;; Description truncation length for prompt-context display (per-line)
(= (recent-action-desc-truncate) 80)

;; Match a single recent-action by exact cycle-id; format and return the line.
;; If no atom exists for that cycle-id, returns empty string.
;; Uses collapse to handle the missing-match case safely (empty list rather
;; than match-failure).
(= (format-one-action $cycle-id)
   (let $matched (collapse (match &self (recent-action $cycle-id $atype $desc)
                                  (py-call (helper.format_action_line
                                             $cycle-id $atype $desc
                                             (recent-action-desc-truncate)))))
        (if (== $matched ())
            ""
            (car-atom $matched))))

;; Top-level entry point called from getContext.
;; Args:
;;   $current-cycle -- $k from loop.metta (the monotonic iteration counter)
;; Returns:
;;   Body content for the YOUR_LAST_ACTION prompt block (newline-joined
;;   formatted action lines). Returns sentinel string if no prior actions
;;   exist (first cycle after restart). The "YOUR_LAST_ACTION: " label is
;;   supplied by loop.metta as a string literal, consistent with how every
;;   other getContext section is labeled.
(= (your-last-action-block $current-cycle)
   (let* (($line1 (format-one-action $current-cycle))
          ($line2 (format-one-action (- $current-cycle 1)))
          ($line3 (format-one-action (- $current-cycle 2))))
         (py-call (helper.assemble_action_block $line1 $line2 $line3))))
