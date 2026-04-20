;; lib_web_detect.metta -- ClarityClaw causal web pattern detection
;; Detects convergence, divergence, and cycles in implication webs
;; Pure MeTTa, no Python

;; --- Convergence detector ---
;; Two different causes both imply same effect
(= (converge? (==> $a $c) (==> $b $c))
   (convergence $c ($a $b)))

;; --- Divergence detector ---
;; One cause implies two different effects
(= (diverge? (==> $a $b) (==> $a $c))
   (divergence $a ($b $c)))

;; --- Causal strength via deduction ---
;; Chain two implications and measure resulting confidence
(= (causal-chain $ab $bc)
   (|- $ab $bc))

;; --- Support weight ---
;; Count how many independent paths support a conclusion
;; Uses revision to combine independent evidence
(= (support-merge $path1-stv $path2-stv)
   (|- ($conclusion $path1-stv) ($conclusion $path2-stv)))

;; --- Weakest link ---
;; In a causal chain find the minimum confidence
(= (weak-link (stv $f1 $c1) (stv $f2 $c2))
   (if (< $c1 $c2) (stv $f1 $c1) (stv $f2 $c2)))

;; --- Amplification detector ---
;; When revised evidence is stronger than either input alone
(= (amplified? (stv $f1 $c1) (stv $f2 $c2) (stv $fr $cr))
   (if (and (> $cr $c1) (> $cr $c2))
     True False))
