;; Diagnostic: what does py-call file_exists actually return?
!(import! &self (library mettaclaw ./src/helper.py))
!(py-call (helper.file_exists "./memory/soul_seeded.flag"))
!(== (py-call (helper.file_exists "./memory/soul_seeded.flag")) (@ true))
!(== (py-call (helper.file_exists "./memory/soul_seeded.flag")) (@ True))
!(== (py-call (helper.file_exists "./memory/soul_seeded.flag")) True)
