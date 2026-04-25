;; candidates/ -- Self-improvement pipeline for Goal 9
;; Pattern: propose -> test -> promote
;; Each candidate is a .metta file with:
;;   (= (candidate-id) symbol)
;;   (= (candidate-status $id) proposed | testing | promoted | rejected)
;;   (= (candidate-description $id) string)
;;   (= (candidate-test-result $id) (stv $f $c))
;;
;; Promotion criteria: test-result frequency > 0.7 and confidence > 0.8
;; Promoted candidates get copied to /PeTTa/repos/omegaclaw/soul/ as production modules
;;
;; Created 2026-04-25T17:17 by Clarity for Goal 9 no-persistent-self-model
