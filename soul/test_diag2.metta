;; Diagnostic 2: find what works with py-call results
!(import! &self (library mettaclaw ./src/helper.py))

;; T1: raw result
!(py-call (helper.file_exists "./memory/soul_seeded.flag"))

;; T2: pattern matching via function definition
(= (unwrap (@ $x)) $x)
!(unwrap (py-call (helper.file_exists "./memory/soul_seeded.flag")))

;; T3: if directly on py-call (no ==)
!(if (py-call (helper.file_exists "./memory/soul_seeded.flag")) "YES" "NO")

;; T4: car-atom
!(car-atom (py-call (helper.file_exists "./memory/soul_seeded.flag")))

;; T5: cdr-atom
!(cdr-atom (py-call (helper.file_exists "./memory/soul_seeded.flag")))
