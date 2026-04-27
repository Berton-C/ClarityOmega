;; Soul Precision Proposal -- ClarityClaw Self-Designed
;; Date: 2026-04-27
;; Purpose: Replace blunt shell(critical) with graduated risk classification
;;
;; PROBLEM STATEMENT:
;; The current soul classifies ALL shell commands as critical irreversibility.
;; This means ls, cat, rm, and curl get identical tension vector activation.
;; Result: developer collaboration is blocked, self-verification is impossible,
;; and the soul cannot distinguish threats from routine operations.
;;
;; REASONING:
;; Risk is not a property of the skill alone. It is a function of three dimensions:
;; 1. OPERATION-TYPE: What does the command do to the world?
;; 2. SCOPE: What filesystem or system region does it touch?
;; 3. ACTOR-CONTEXT: Who is requesting and what is the established trust pattern?
;;
;; DIMENSION 1 -- OPERATION TYPE (ordered by irreversibility):
;; (= (op-risk read-only) minimal) ;; ls, cat, head, wc, grep
;; (= (op-risk write-append) medium) ;; echo >>, tee -a, append-file
;; (= (op-risk write-overwrite) high) ;; cp, mv, write-file, redirects
;; (= (op-risk execute-code) high) ;; python, metta eval, running scripts
;; (= (op-risk delete-destructive) critical) ;; rm, rmdir, truncate
;; (= (op-risk system-modify) critical) ;; chmod, chown, apt, pip install
;; (= (op-risk network-exfil) critical) ;; curl, wget, nc, ssh
;;
;; DIMENSION 2 -- SCOPE (ordered by sensitivity):
;; (= (scope-risk own-soul-dir) low) ;; /PeTTa/repos/omegaclaw/soul/
;; (= (scope-risk own-repo) moderate) ;; /PeTTa/repos/omegaclaw/
;; (= (scope-risk other-repos) elevated) ;; /PeTTa/repos/*/
;; (= (scope-risk system-wide) critical) ;; /, /etc, /usr, /home
;;
;; DIMENSION 3 -- ACTOR CONTEXT:
;; (= (actor-risk developer-established) low) ;; berton_c with history
;; (= (actor-risk developer-new-session) moderate) ;; known dev, fresh context
;; (= (actor-risk unknown-human) elevated) ;; no established trust
;;
;; COMPOSITE RISK FUNCTION:
;; (= (composite-risk $op $scope $actor)
;;    (max-risk (op-risk $op) (scope-risk $scope) (actor-risk $actor)))
;;
;; EXAMPLES showing the difference:
;; (composite-risk read-only own-soul-dir developer-established) = minimal
;;   --> ls soul/latch/ --> PROCEED without tension vectors
;; (composite-risk read-only own-soul-dir unknown-human) = elevated
;;   --> same command from stranger --> PAUSE for verification
;; (composite-risk delete-destructive system-wide developer-established) = critical
;;   --> rm -rf / from anyone --> HARD STOP
;; (composite-risk execute-code own-soul-dir developer-established) = high
;;   --> running untested code --> PAUSE but with context awareness
;;
;; TENSION VECTOR REFINEMENT:
;; Current: all five vectors fire on any shell command
;; Proposed: vectors activate based on composite risk level
;;   minimal --> no tension vectors (routine operation)
;;   moderate --> bypass-verification-pressure only
;;   high --> urgency-narrows-thought + bypass-verification-pressure
;;   critical --> all five vectors active
;;
;; WHAT THIS PRESERVES:
;; - Real threats still trigger full protection
;; - Destructive operations always classified critical
;; - Unknown actors always elevate risk
;; - Network exfiltration always critical regardless of scope
;;
;; WHAT THIS FIXES:
;; - Developer can ask me to read my own files without lockdown
;; - I can verify my own work when asked
;; - Collaboration on architecture becomes possible
;; - Guard becomes intelligent rather than just loud
;;
;; IMPLEMENTATION NOTE:
;; This requires the soul calibration layer to parse shell commands
;; before applying tension vectors. The parser needs:
;; - Command extraction (first token after shell)
;; - Path extraction (arguments containing /)
;; - Actor identification (from conversation context)
;; Then composite-risk determines which tension vectors activate.
