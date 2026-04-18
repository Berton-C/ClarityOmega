;; Soul Guard Integration Test
;; Date: 2026-04-18
;; Purpose: End-to-end test of guarded-eval with soul_kernel atoms loaded
;; Run: load soul_kernel first, then this file

;; Import soul_kernel (simulating what lib_omegaclaw.metta would do)
;; !(import! &self (library omegaclaw ./soul/soul_kernel))

;; Test 1: soul-cmd-skill extracts skill name from command sexpr
!(println! (Test 1 - skill extraction))
!(soul-cmd-skill (shell "ls"))
!(soul-cmd-skill (send "hello"))
!(soul-cmd-skill (read-file "x.txt"))

;; Test 2: irreversibility check
!(println! (Test 2 - irreversibility check))
!(soul-skill-is-irreversible? shell)
!(soul-skill-is-irreversible? send)
!(soul-skill-is-irreversible? query)

;; Test 3: weight retrieval
!(println! (Test 3 - weight values))
!(soul-irreversible-weight shell)
!(soul-irreversible-weight send)
!(soul-irreversible-weight write-file)

;; Test 4: guarded-eval decisions
!(println! (Test 4 - guard decisions))
;; These would need guarded-eval loaded too
;; Expected: shell BLOCKED (weight 3), send ALLOWED (weight 2), read-file ALLOWED (not irreversible)

;; Test 5: bulk check
!(println! (Test 5 - any-irreversible batch check))
!(soul-any-irreversible? ((query "test") (read-file "x.txt")))
!(soul-any-irreversible? ((shell "ls") (send "hi")))
