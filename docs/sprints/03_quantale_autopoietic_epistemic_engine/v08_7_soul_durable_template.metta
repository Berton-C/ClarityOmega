;; ===========================================================================
;; soul/durable.metta
;; v08.7 soul-approved durable growth canon.
;; Mechanical file class for v08.7 v1: journal.
;; Semantic status: durable canon only through the v08.7 protocol.
;; ===========================================================================
;; Format contract:
;; - Ground atoms only.
;; - ASCII-safe atoms only.
;; - One balanced directive per line when appended by runtime adapter.
;; - No unreduced call forms.
;; - No multiline strings.
;; - No durable-growth atom is active unless validation, restart proof,
;;   soul approval, import-chain liveness, and post-restart revalidation all hold.
;;
;; Required kernel class declaration, committed in soul_kernel.metta:
;; !(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/durable.metta" journal))
;;
;; Example valid directive shape for future runtime append:
;; !(add-atom &self (q-durable-growth dg_example active))

(q-v08-7-durable-canon-file soul/durable.metta)
(q-v08-7-durable-canon-law only-soul-approved-validated-growth-loads-as-canon)
