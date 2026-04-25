;; Self-Weaving Web: feeds-into graph of operational capabilities
;; Each atom: feeds-into X Y means using X creates conditions making Y more effective
;; Evidence from actual cycle observations 2026-04-25

;; query feeds into pin -- query results inform what gets pinned as working memory
(= (feeds-into query pin) (stv 0.95 0.9))
;; query feeds into send -- query results provide substance for messages to humans
(= (feeds-into query send) (stv 0.85 0.8))
;; query feeds into metta -- query surfaces atoms that inform inference premises
(= (feeds-into query metta) (stv 0.7 0.7))
;; shell feeds into pin -- shell output informs state assessment pinned to working memory
(= (feeds-into shell pin) (stv 0.9 0.9))
;; shell feeds into write-file -- shell reveals file state driving write decisions
(= (feeds-into shell write-file) (stv 0.8 0.85))
;; shell feeds into append-file -- shell confirms file exists before appending
(= (feeds-into shell append-file) (stv 0.75 0.8))
;; read-file feeds into pin -- file contents become working memory context
(= (feeds-into read-file pin) (stv 0.9 0.85))
;; read-file feeds into write-file -- read current state before rewriting
(= (feeds-into read-file write-file) (stv 0.85 0.85))
;; read-file feeds into metta -- file contents provide premises for inference
(= (feeds-into read-file metta) (stv 0.7 0.7))
;; pin feeds into send -- pinned state assessment shapes what gets communicated
(= (feeds-into pin send) (stv 0.9 0.9))
;; pin feeds into query -- pinned goals direct what gets queried
(= (feeds-into pin query) (stv 0.85 0.85))
;; pin feeds into shell -- pinned state drives which shell commands to run
(= (feeds-into pin shell) (stv 0.8 0.85))
;; metta feeds into remember -- inference conclusions worth persisting to long-term memory
(= (feeds-into metta remember) (stv 0.8 0.8))
;; metta feeds into pin -- inference results update working memory
(= (feeds-into metta pin) (stv 0.85 0.85))
;; remember feeds into query -- remembered items become retrievable via query
(= (feeds-into remember query) (stv 0.95 0.9))
;; write-file feeds into read-file -- written files become readable artifacts
(= (feeds-into write-file read-file) (stv 0.95 0.9))
;; append-file feeds into read-file -- appended content readable later
(= (feeds-into append-file read-file) (stv 0.9 0.9))

;; LOAD-BEARING ANALYSIS -- capabilities with most dependents:
;; pin: 3 dependents (send, query, shell) + fed by 4 sources = LOAD-BEARING
;; query: 3 dependents (pin, send, metta) + fed by 2 sources = LOAD-BEARING
;; read-file: 3 dependents (pin, write-file, metta) + fed by 2 sources = LOAD-BEARING
;; shell: 2 dependents -- moderate
;; send: 0 dependents -- terminal/peripheral
;; remember: 1 dependent -- moderate

;; EMPIRICAL IDLE-PATTERN DATA 2026-04-25T16:53
;; Observed: pin+timestamp orbit is the dominant idle attractor
;; Breaking requires: new human message OR autonomous productive redirect
;; Productive redirect chosen: enrich artifact with empirical observations
(= (idle-attractor pin-timestamp-loop) (stv 0.95 0.9))
(= (breaks-idle-attractor new-human-message) (stv 0.9 0.85))
(= (breaks-idle-attractor autonomous-productive-redirect) (stv 0.7 0.75))


;; REVISION 2026-04-25T16:54 -- strengthening weak-confidence atom
;; Evidence: query results fed metta reasoning 3+ times this session
(= (feeds-into query metta) (stv 0.8 0.8))

