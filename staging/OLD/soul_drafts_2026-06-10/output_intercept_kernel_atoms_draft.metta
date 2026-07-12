;; ================================================================
;; output_intercept_kernel_atoms_draft.metta
;; MeTTa atoms for D1-D4 decisions - wiring phase integration
;; Created 2026-06-10
;; ================================================================

;; --- D1: NATIVE verdict with LLM fallback ---
;; Default false; LLM path wired but dormant
!(add-atom &self (use-llm-eval False))

;; --- D4: OPERATION risk scale (single-sourced beside weights) ---
;; Weight = irreversibility cost; operation-risk = execution risk
!(add-atom &self (operation-risk send 3))
!(add-atom &self (operation-risk write-file 2))
!(add-atom &self (operation-risk append-file 1))
!(add-atom &self (operation-risk shell 3))
!(add-atom &self (operation-risk read-file 1))
!(add-atom &self (operation-risk search 1))
!(add-atom &self (operation-risk package-install 3))
!(add-atom &self (operation-risk credential-storage 4))
!(add-atom &self (operation-risk crontab-modification 4))

;; --- D3: soul-kernel-file atom set (gate parity) ---
;; Files with full mutation gate parity
!(add-atom &self (soul-kernel-file /PeTTa/repos/omegaclaw/soul/soul_kernel.metta))
!(add-atom &self (soul-kernel-file /PeTTa/repos/omegaclaw/soul/soul_utils.metta))
!(add-atom &self (soul-kernel-file /PeTTa/repos/omegaclaw/soul/soul_memory.metta))
;; arc_log and soul_note NOT here -- PROCEED-under-VALUE-GROUNDING

;; --- D2: PAUSE report template ---
;; Includes suppressed command and reason for informed override
!(add-atom &self (soul-pause-report-template (suppressed-cmd $cmd) (reason $reason) (dimensions ($op $scope $vg)) (composite $comp)))

;; ================================================================
;; ACCESSOR FUNCTIONS
;; ================================================================

(= (soul-operation-risk $skill) (match &self (operation-risk $skill $r) $r))
(= (soul-kernel-file? $path) (match &self (soul-kernel-file $path) True))
(= (soul-use-llm-eval?) (match &self (use-llm-eval $bool) $bool))

;; Composite verdict computation (D1: native deterministic)
(= (soul-verdict-proceed? $op $sc $vg)
   (let $max (max3 $op $sc $vg)
     (if (<= $max 2) True False)))

(= (soul-verdict-pause? $op $sc $vg)
   (let $max (max3 $op $sc $vg)
     (if (>= $max 4) True
       (if (and (>= $op 3) (>= $vg 3)) True False))))

;; Helper
(= (max3 $a $b $c)
   (if (>= $a $b)
     (if (>= $a $c) $a $c)
     (if (>= $b $c) $b $c)))
