;; Diagnostic 3: what py-call return types are transparent to PeTTa?
!(import! &self (library mettaclaw ./src/helper.py))

;; Raw returns — what does each type look like?
!(py-call (helper.file_exists "./memory/soul_seeded.flag"))
!(py-call (helper.file_exists_int "./memory/soul_seeded.flag"))
!(py-call (helper.file_exists_str "./memory/soul_seeded.flag"))

;; Can == match integers?
!(== (py-call (helper.file_exists_int "./memory/soul_seeded.flag")) 1)
!(== (py-call (helper.file_exists_int "./memory/soul_seeded.flag")) (@ 1))

;; Can == match strings?
!(== (py-call (helper.file_exists_str "./memory/soul_seeded.flag")) "true")
!(== (py-call (helper.file_exists_str "./memory/soul_seeded.flag")) (@ "true"))

;; Can if use integer directly?
!(if (py-call (helper.file_exists_int "./memory/soul_seeded.flag")) "IF-INT-YES" "IF-INT-NO")
