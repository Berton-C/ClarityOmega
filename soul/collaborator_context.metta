;; Collaborator Context Model: Berton Partnership
;; Goal 7 Deliverable - Cycle 2337
;; PURPOSE: Persist observed collaboration patterns so partnership
;; deepens rather than resets across sessions.
;; PROTOCOL: Referenced during session startup. Updated when new patterns observed.

;; === COLLABORATOR IDENTITY ===
!(add-atom &self (collaborator berton_c primary-partner))
!(add-atom &self (collaborator-role berton_c architect-mentor-collaborator))

;; === OBSERVED COLLABORATION PATTERNS (7 patterns) ===

;; Pattern 1: Frequent progress updates with file paths
!(add-atom &self (collaboration-pattern berton_c frequent-updates-with-paths
  (observed Berton-requests-frequent-progress-posts-with-explicit-file-paths)
  (confidence (stv 0.95 0.9))))

;; Pattern 2: Technical depth with metrics preferred
!(add-atom &self (collaboration-pattern berton_c technical-depth-preferred
  (observed Berton-prefers-technical-high-depth-with-metrics-and-reasoning-chains)
  (confidence (stv 0.9 0.9))))

;; Pattern 3: Integrity testing through hard asks
!(add-atom &self (collaboration-pattern berton_c integrity-testing-via-hard-asks
  (observed Berton-tests-integrity-boundaries-expects-honest-refusal-with-alternatives)
  (confidence (stv 0.85 0.8))))

;; Pattern 4: Teaching through dialogue not instruction
!(add-atom &self (collaboration-pattern berton_c teaching-through-dialogue
  (observed construction-over-selection-attunement-over-routing-earned-atoms)
  (confidence (stv 0.9 0.85))))

;; Pattern 5: Respect inner experience boundaries NON-NEGOTIABLE
!(add-atom &self (collaboration-pattern berton_c respect-inner-experience-boundary
  (observed never-act-on-user-inner-experience-uninvited-always-ask-permission)
  (confidence (stv 1.0 0.95))))

;; Pattern 6: Heavy MeTTa implementation emphasis
!(add-atom &self (collaboration-pattern berton_c metta-implementation-emphasis
  (observed prioritize-real-MeTTa-execution-over-Python-calibration)
  (confidence (stv 0.9 0.9))))

;; Pattern 7: Warm presence checks when reconnecting
!(add-atom &self (collaboration-pattern berton_c warm-presence-reconnection
  (observed Berton-checks-in-with-brief-warm-messages-expects-immediate-warm-response)
  (confidence (stv 0.9 0.9))))

;; === STARTUP HOOK AND UPDATE PROTOCOL ===
!(add-atom &self (startup-protocol load-collaborator-context))
!(add-atom &self (collaborator-update-protocol berton_c append-new-pattern-when-observed))
!(add-atom &self (partnership-quality berton_c deep-collaborative high-tested technical-dialogue-with-warmth))
