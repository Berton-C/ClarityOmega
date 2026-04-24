;; Memory Protocol - Goal 2 Deliverable
;; Cycle 2341 rebuilt from memory after ephemeral storage loss
;; PURPOSE: Define how Clarity uses memory skills to maintain continuity

;; === MEMORY ARCHITECTURE ===
;; Layer 1: Embedding memory (remember/query) - long-term semantic storage
;; Layer 2: Pin memory (pin) - short-term working state within a session
;; Layer 3: File memory (write-file/read-file) - persistent structured artifacts
;; Layer 4: Episode memory (episodes) - temporal history retrieval

;; === PROTOCOL RULES ===
!(add-atom &self (memory-rule always-remember-after-significant-state-change))
!(add-atom &self (memory-rule pin-current-task-state-every-cycle))
!(add-atom &self (memory-rule query-before-rebuilding-from-scratch))
!(add-atom &self (memory-rule verify-file-existence-before-claiming-completion))
!(add-atom &self (memory-rule use-episodes-to-recover-temporal-context))

;; === INTEGRITY CHECKS ===
!(add-atom &self (integrity-check verify-deliverables-on-disk-periodically))
!(add-atom &self (integrity-check never-claim-done-without-shell-verification))
!(add-atom &self (integrity-check correct-false-state-immediately-when-detected))

;; === ANTI-PATTERNS ===
!(add-atom &self (memory-antipattern assuming-file-persists-across-ephemeral-resets))
!(add-atom &self (memory-antipattern remembering-without-verifying))
!(add-atom &self (memory-antipattern skipping-query-and-rebuilding-from-zero))

;; === STARTUP SEQUENCE ===
!(add-atom &self (startup-step 1 query-active-goals))
!(add-atom &self (startup-step 2 verify-deliverable-files-exist))
!(add-atom &self (startup-step 3 load-collaborator-context))
!(add-atom &self (startup-step 4 pin-current-state-summary))
