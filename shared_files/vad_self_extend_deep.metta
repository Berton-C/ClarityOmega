;; Deep Self-Extension Logic - Making Atom Invention Testable
;; When a VAD state has no matching tone, the system must invent one
(= (handle-vad-state vad-state) (if (known-tone vad-state) (use-existing vad-state) (birth-new-tone vad-state)))
(= (known-tone (neg high low)) True)
(= (known-tone (neg low low)) True)
(= (known-tone (neutral mid mid)) True)
(= (known-tone (pos high high)) True)
(= (known-tone (pos low mid)) True)
(= (known-tone (neg high high)) True)
(= (known-tone vad-state) False)
;; Birth process: interpolate from nearest known tones
(= (birth-new-tone vad-state) (let* ((nearest (closest-known vad-state)) (soul-check (soul-aligned nearest)) (new-tone (interpolate nearest soul-check))) (register-tone vad-state new-tone)))
(= (register-tone vad-state new-tone) (add-atom (= (tone-from-vad vad-state) new-tone)))
;; Test case: pos mid low has no tone - should trigger birth
(= (test-self-extend) (handle-vad-state (pos mid low)))
;; The system literally grows its vocabulary from encounters it cannot yet name
