;; lib_resonance.metta -- ClarityClaw gap resonance detection
;; Detects what is absent but expected - absence as signal
;; Pure MeTTa, no Python

;; --- Expected pattern registry ---
;; Register what SHOULD exist given a context
(= (expect-from (==> $context $expected) $context)
   (expected $expected))

;; --- Gap detector ---
;; Given expected conclusion and actual evidence,
;; flag gap when expected has no supporting evidence
(= (gap? $expected (stv $f $c))
   (if (< $c 0.1)
     (gap-signal $expected strong)
     (if (< $c 0.3)
       (gap-signal $expected weak)
       (no-gap $expected))))

;; --- Resonance score ---
;; How strongly does absence of evidence resonate
;; Higher score = more surprising absence
(= (resonance $expected-stv $prior-expectation)
   (let (stv $f $c) $expected-stv
     (let $surprise (- $prior-expectation (+ (* $c (- $f 0.5)) 0.5))
       (if (> $surprise 0.3)
         (resonance-high $surprise)
         (if (> $surprise 0.1)
           (resonance-medium $surprise)
           (resonance-low $surprise))))))

;; --- Missing link detector ---
;; In a causal chain A->B->C, if B exists but A->B is missing
(= (missing-link? $a-to-b $b-to-c)
   (let (stv $f1 $c1) (second $a-to-b)
     (let (stv $f2 $c2) (second $b-to-c)
       (if (and (< $c1 0.1) (> $c2 0.5))
         (missing-cause (first $a-to-b))
         (chain-intact)))))

;; --- Curiosity generator ---
;; Gaps with high resonance become exploration targets
(= (curiosity-target (resonance-high $score) $domain)
   (explore $domain $score))
(= (curiosity-target (resonance-medium $score) $domain)
   (note $domain $score))
(= (curiosity-target (resonance-low $score) $domain)
   (ignore))
