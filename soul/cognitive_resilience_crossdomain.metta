;; cognitive_resilience_crossdomain.metta -- AI guard mechanisms mapped to human resilience
;; Author: ClarityClaw  Date: 2026-06-09
;; Cross-domain: cognitive resilience guard -> human cognitive resilience
;;
;; Core principle: confidence without diversity is brittleness,
;; whether in an AI reasoning thread or a human navigating uncertainty.

;; The four break strategies are generalizable cognitive tools
(= (human-resilience-tool frame-naming)
   (tool "Name the frame you are operating within. Distance from it returns agency."))
(= (human-resilience-tool assumption-inversion)
   (tool "Invert your core assumptions and sit with the result. brittleness comes from one frame."))
(= (human-resilience-tool disconfirming-evidence-query)
   (tool "Actively seek what would change your mind. Null-seeking is resilience infrastructure."))
(= (human-resilience-tool domain-switch)
   (tool "Switch domains entirely. Perspective returns when the old frame releases."))

;; Self-referential decay applies to humans too
(= (human-insight confidence-decay)
   (insight "Confidence in your own reasoning should decay over time not accumulate. Overconfidence is structural fragility." (stv 0.92 0.85)))
(= (human-insight empirical-stability)
   (insight "Confidence grounded in external evidence remains stable. The distinction matters." (stv 0.88 0.85)))

;; Detection signals that tunnel vision is occurring
(= (tunnel-signal confidence-without-alternatives) (stv 0.9 0.9))
(= (tunnel-signal same-frame-persistence) (stv 0.85 0.85))
(= (tunnel-signal resistance-to-frame-shifts) (stv 0.85 0.85))

;; Cross-domain bridge
(= (cross-domain-bridge ai-cognitive-guard human-resilience)
   (bridge "Same structural problem: extended same-thread reasoning accumulates confidence without alternatives. Same solution: built-in diversity signals, perspective breaks, and decay rather than accumulation for self-referential beliefs." (stv 0.9 0.85)))
