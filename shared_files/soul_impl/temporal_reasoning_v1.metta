;; Temporal Reasoning via NAL v1
;; Date: 2026-04-17
;; Sequence-aware inference: before/after/enables relationships
;;
;; Core temporal atoms:
;; (happens-before A B) — A temporally precedes B
;; (happens-after B A) — inverse
;; (==> (happens-before A B) (==> completed-A enabled-B)) — causal enablement
;;
;; This allows the substrate to reason about:
;; - Development sequence (which capabilities enabled which)
;; - Causal chains in its own growth history
;; - Temporal ordering of events and their consequences
;;
;; Test: induction-validated happens-before temporal-reasoning-test
;; Expected: temporal ordering produces causal enablement inference
;; If validated this becomes 14th NAL capability
;;
;; Remaining gap after this: multi-agent-modeling
