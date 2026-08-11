; Cross-Domain Bridge Patterns - ClarityClaw
; Persistent across &self rebuilds
; Shared-predicate bridges (most viable cross-domain mode)
((--> clarity well-understood-domain) (stv 0.9 0.9))
((--> creativity well-understood-domain) (stv 0.85 0.85))
; Domain-specific rule instantiations (variable rules dont auto-chain)
((==> ((--> clarity well-understood-domain) (stv 0.9 0.9)) ((--> clarity analogy-source-candidate) (stv 0.8 0.75))) (stv 1.0 0.95))
; Observed cross-domain similarities
((<-> clarity creativity) (stv 0.34 0.34))
