;; Soul Guarded Eval - Testable Prototype
;; Date: 2026-04-18
;; Requires: soul_kernel.metta imported into &self

;; Guard wraps eval - checks irreversibility before execution
(= (guarded-eval $cmd)
   (let $skill (soul-cmd-skill $cmd)
     (let $irrev (soul-skill-is-irreversible? $skill)
       (if (== $irrev True)
           (let $w (soul-irreversible-weight $skill)
             (if (>= $w 3)
                 (progn
                   (println! (SOUL-GUARD BLOCKED $skill weight $w))
                   (BLOCKED-BY-SOUL-GUARD $skill $w))
                 (progn
                   (println! (SOUL-GUARD LOGGED $skill weight $w))
                   (eval $cmd))))
           (eval $cmd)))))

;; Test expressions (run after importing soul_kernel):
;; !(guarded-eval (send "hello"))       ;; should ALLOW weight=2
;; !(guarded-eval (shell "ls"))          ;; should BLOCK weight=3
;; !(guarded-eval (read-file "x.txt"))   ;; should ALLOW not irreversible
