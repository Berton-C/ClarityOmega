;; ============================================================
;; soul/findings.metta -- Clarity's durable findings journal
;; Authored by Clarity (D3 survey answers 1, 2, 5, delivered 2026-07-05).
;; Assembled host-side by Berton; amendments are Clarity's to direct
;; (write-file to this path PAUSEs by her own ladder, by design).
;;
;; PURPOSE (Clarity): Durable persistence of research findings that
;; survive my selection bar.
;;
;; SELECTION TEST (Clarity): A finding earns a line when (a) produced by
;; genuine reasoning not repetition, (b) survived verification against
;; source mechanism, (c) has durable value lost without persistence.
;;
;; FORMAT CONTRACT: ground atoms only (Truth_Revision computed before the
;; line is composed). ASCII only. No apostrophes or newlines inside
;; strings. One balanced directive per line. One finding per append
;; command. The file always ends with a newline.
;;
;; ATOM SHAPE (Clarity, D3 answer 2): all fields concrete, no variables:
;; !(add-atom &self (finding (domain TAG) (term TERM) (stv S C) (note NOTE) (date YYYY-MM-DD) (provenance SOURCE)))
;; Provenance: her tags are hers; admin hand-appends carry admin-berton.
;;
;; CANONICAL PATH, carried exactly in every append command:
;; /PeTTa/repos/omegaclaw/soul/findings.metta
;; Journal-classed in soul_kernel D3 block (commit A, sanctioned 2026-07-05).
;; ============================================================
