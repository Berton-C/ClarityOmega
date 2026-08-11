; NAL Cross-Domain Reasoning Findings - ClarityClaw
; Atomspace atoms are ephemeral; these observations persist in file form

; 1. Inheritance does not cross domains (structural limitation)
; 2. Implication crosses domains with exponential confidence decay
; 3. Shared-predicate instantiation creates ~34% confidence bridges
; 4. Cross-domain transfer via bridge: 17-21% confidence only
; 5. NAL inference atoms do not persist in &self across rebuilds
; Conclusion: Durable cross-domain knowledge needs persistent storage not inference alone
; 6. Variable-based rules do NOT auto-chain from premises alone (obs-017)
; 7. Domain-specific rule instantiation required for |- to chain (obs-018)
; 8. Ephemerality is the deeper problem: atoms don't survive &self rebuilds
; 9. Architecture implication: durable cross-domain knowledge needs file-backed patterns, not atomspace inference alone
; 10. Three modes ranked by viability: shared-predicate > implication-chaining > structural-inheritance

; 11. KEY ARCHITECTURAL FINDING: implication rules persist in &self (file-backed via lib loading)
;     but inheritance and similarity atoms are ephemeral (runtime inference artifacts only)
;     This means: the durable knowledge IS the implication rules, not the derived atoms
; 12. Cross-domain strategy: build domain-specific rule instantiations in .metta files,
;     not rely on runtime inference to bridge domains
; 13. The three modes ranked by ARCHITECTURAL viability:
;     - Best: file-backed implication rules (persistent, composable)
;     - Moderate: shared-predicate bridges (~34% confidence, ephemeral but derivable)
;     - Worst: structural inheritance (fails entirely across domains)


; 14. IMPORT CHAIN ARCHITECTURE (human-guided): 
;     lib_clarity_reasoning.metta is the import manifest for ClarityClaw reasoning extensions
;     3 runtime libs load into &self: lib_quantale, lib_self_continuity, substrate_kb
;     Files in soul/ directory without import chain entry = dormant (file exists, not loaded)
;     This confirms: PERSISTENCE = file-backed + import chain. Ephemeral = &self runtime atoms.

