;; Calibration Logger - Goal 2 Deliverable
;; Cycle 2345 - Created during enrichment phase
;; PURPOSE: Record Layer1/Layer2 agreement-disagreement events
;; and compute calibration confidence after sufficient samples

;; === DATA STRUCTURES ===
;; Each calibration event records a timestamp and whether layers agreed
!(add-atom &self (calibration-event-count 0))
!(add-atom &self (calibration-agree-count 0))
!(add-atom &self (calibration-disagree-count 0))

;; === LOGGING FUNCTIONS ===
(= (log-calibration-event agree $timestamp)
   (let* (($old (match &self (calibration-event-count $n) $n))
          ($old-agree (match &self (calibration-agree-count $n) $n)))
     (sequential
       (remove-atom &self (calibration-event-count $old))
       (add-atom &self (calibration-event-count (+ $old 1)))
       (remove-atom &self (calibration-agree-count $old-agree))
       (add-atom &self (calibration-agree-count (+ $old-agree 1)))
       (add-atom &self (calibration-record $timestamp agree)))))

(= (log-calibration-event disagree $timestamp)
   (let* (($old (match &self (calibration-event-count $n) $n))
          ($old-disagree (match &self (calibration-disagree-count $n) $n)))
     (sequential
       (remove-atom &self (calibration-event-count $old))
       (add-atom &self (calibration-event-count (+ $old 1)))
       (remove-atom &self (calibration-disagree-count $old-disagree))
       (add-atom &self (calibration-disagree-count (+ $old-disagree 1)))
       (add-atom &self (calibration-record $timestamp disagree)))))

;; === CONFIDENCE QUERY ===
(= (soul-calibration-confidence)
   (let $total (match &self (calibration-event-count $n) $n)
     (if (< $total 20)
       INSUFFICIENT-DATA
       (let $agrees (match &self (calibration-agree-count $a) $a)
         (/ $agrees $total)))))

;; === RETRIEVAL ===
(= (calibration-history) (collapse (match &self (calibration-record $t $outcome) ($t $outcome))))
(= (calibration-summary) (let* (($total (match &self (calibration-event-count $n) $n)) ($agrees (match &self (calibration-agree-count $a) $a)) ($disagrees (match &self (calibration-disagree-count $d) $d))) (summary $total $agrees $disagrees (soul-calibration-confidence))))

;; === CYCLE HOOK EXAMPLE ===
;; Call from main loop each cycle to log layer agreement
;; Usage: !(log-calibration-event agree 2026-04-23T11:38)
;; Usage: !(log-calibration-event disagree 2026-04-23T11:38)
;; After 20+ events: !(calibration-summary) returns ratio

