;; === corner_state.metta ===
;; DRAFT for Clarity's analysis. Destination: soul/corner_gap/corner_state.metta
;; (new file; basic block wires at B2, full block swaps in at B3).
;;
;; Layer V of corner-gate v2: the CORNER-STATE visibility block. PURE READS
;; ONLY. No writers in this file. Information-flow per P4; the framing text is
;; substrate-side and Clarity's to amend (ADR-008: the Python formatter
;; handles numbers and strings mechanically, never framing).

;; Streak of corner verdicts in the current status trail (v1 detector atoms).
(= (corner-streak-count)
   (size-atom (collapse (match &self (coupling-status $c corner) $c))))

;; Framing sentence: SUBSTRATE-SIDE, hers to amend. First draft text.
(= (corner-state-teaching)
   "CORNER-STATE reads action repetition against forward outcome. A rising repeat-count means one command form keeps being proposed without producing change; any different move alters the trajectory.")

;; ---- B2 basic block (streak + signature from the cycle trace) ----
(= (corner-state-block)
   (let ($sig $n) (dominant-signature)
        (py-str ((py-call (helper.corner_state_block_format
                           (corner-streak-count) $sig $n (cmds-in-window)))
                 " " (corner-state-teaching)))))

;; ---- B3 full block (adds graded strength and confidence once
;;      coupling_quantale_merge is imported; swap the getContext call from
;;      corner-state-block to corner-state-block-graded in the B3 commit) ----
(= (corner-strength)
   (let (mk-pbit $s $c) (corner-pbit-core) $s))
(= (corner-confidence)
   (let (mk-pbit $s $c) (corner-pbit-core) $c))

(= (corner-state-block-graded)
   (let ($sig $n) (dominant-signature)
        (py-str ((py-call (helper.corner_state_block_format_graded
                           (corner-streak-count) $sig $n (cmds-in-window)
                           (corner-strength) (corner-confidence)))
                 " " (corner-state-teaching)))))
