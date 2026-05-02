!(import! &self (library lib_import))
;; NOTE: git-import below is effectively a no-op at runtime because the symlink
;; /PeTTa/repos/omegaClaw-Core -> /PeTTa/repos/omegaclaw already exists from
;; Dockerfile-time setup. Active code lives in omegaclaw/, populated from
;; github.com/Berton-C/ClarityOmega at build time, not from this URL at runtime.
!(git-import! "https://github.com/asi-alliance/omegaClaw-Core.git")
!(import! &self (library omegaclaw lib_omegaclaw))

!(omegaclaw)
