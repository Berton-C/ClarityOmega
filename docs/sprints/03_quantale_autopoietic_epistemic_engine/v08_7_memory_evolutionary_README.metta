;; ===========================================================================
;; memory/evolutionary/README.metta
;; v08.7 Durable Evolutionary Governance Protocol process-memory topology.
;; ===========================================================================
;; This directory is process memory, not durable canon.
;; Runtime observations, pending candidates, validation records, restart proofs,
;; and rejected/audit traces may survive restart here without becoming approved
;; durable growth.
;;
;; Canon lives only in: /PeTTa/repos/omegaclaw/soul/durable.metta
;; and only after v08.7 validation, restart proof, soul approval, import-chain
;; liveness, and post-restart revalidation.

(q-v08-7-evolutionary-directory memory/evolutionary)
(q-v08-7-process-file runtime memory/evolutionary/runtime.metta)
(q-v08-7-process-file pending memory/evolutionary/pending.metta)
(q-v08-7-process-file validation memory/evolutionary/validation.metta)
(q-v08-7-process-file restart memory/evolutionary/restart.metta)
(q-v08-7-process-file rejected memory/evolutionary/rejected.metta)
(q-v08-7-process-file index memory/evolutionary/index.metta)
(q-v08-7-process-file archive memory/evolutionary/archive)
(q-v08-7-process-law evolutionary-memory-is-process-not-canon)
