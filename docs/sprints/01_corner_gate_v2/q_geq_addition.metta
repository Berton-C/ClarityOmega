;; === q_geq_addition.metta ===
;; DRAFT for Clarity's analysis. Destination: appended to
;; lib_clarity_reasoning/lib_quantale.metta (build step B1, rebuild required).
;;
;; Threshold comparator required by coupling_quantale_merge.metta:89 and
;; cycle_continuity_probe.metta:100, currently undefined anywhere (confirmed
;; firsthand 2026-07-05: lib_quantale read end to end, corner_gap tree
;; grepped). True only when BOTH strength and confidence meet the threshold,
;; matching the merge file's documented intent ("q-geq requires BOTH strength
;; >= and confidence >= the threshold").

(: q-geq (-> pbit pbit Bool))
(= (q-geq (mk-pbit $s1 $c1) (mk-pbit $s2 $c2))
   (and (>= $s1 $s2) (>= $c1 $c2)))

;; B1 verification (throwaway container REPL probe, live loop untouched):
;;   (q-geq (mk-pbit 0.7 0.6) (mk-pbit 0.6 0.5))  expected True
;;   (q-geq (mk-pbit 0.7 0.4) (mk-pbit 0.6 0.5))  expected False (confidence arm)
;;   (q-geq (mk-pbit 0.5 0.9) (mk-pbit 0.6 0.5))  expected False (strength arm)
;; plus the full chain on seeded fixtures: corner-pbit-core reduces to a
;; ground pbit and corner-confirmed-core reduces to True/False.
