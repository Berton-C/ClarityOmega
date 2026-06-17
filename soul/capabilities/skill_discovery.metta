;; soul/capabilities/skill_discovery.metta
;; Sprint 0-Coda Phase C: first production capability + getContext skills accessor.
;;
;; Option (a): the registry consultation is wired and structurally present; the
;; emitted content is the existing hardcoded skill list (via getSkills), so the
;; LLM-facing content is unchanged while the dispatch path becomes its source.
;; Sprint 1 replaces format-skill-set's body with real (registered-capability)
;; formatting and retires getSkills after the Phase D P-4 parity check holds.

;; --- Lifecycle eligibility seed ------------------------------------------
;; eligible? (in the registry) matches (eligible-lifecycle $l). Without this
;; atom, lifecycle-filter-step drops every active capability and dispatch
;; always falls back. Seeding active as eligible is what lets skill-discovery
;; pass the filter pipeline and reach the handler.
(eligible-lifecycle active)

;; --- Registration (5-field, matches the Path C dispatcher's canonical schema)
(registered-capability
   schema: (skill-request cycle: $k)
   handler: skill-discovery
   priority: 100
   lifecycle: active
   metadata: ())

;; --- Handler (read-only; writes no atoms; returns one skill-set) ----------
(= (skill-discovery $request)
   (let* (($capabilities (collapse (match &self
                                          (registered-capability
                                            schema: $s
                                            handler: $h
                                            priority: $p
                                            lifecycle: active
                                            metadata: $m)
                                          ($s $h $p $m))))
          ($formatted (format-skill-set $capabilities)))
         (skill-set skills: $formatted)))

;; --- Formatter (Option a: emit current hardcoded skills via getSkills) ----
(= (format-skill-set $capabilities) (getSkills))

;; --- getContext-facing TOTAL skills accessor (the named hook) -------------
;; Fires dispatch for this cycle, reads this cycle's skill-set from
;; dispatch-result, and falls back to (getSkills) when the read is empty, so a
;; dispatch miss can NEVER crash prompt assembly. getContext calls this single
;; named function (Artifact 0 Discipline 1).
(= (dispatch-skills $k)
   (let $_ (dispatch (skill-request cycle: $k) $k)
        (first-skill-or-default
          (collapse (match &self
                          (dispatch-result
                            invocation-id: $k
                            result: (skill-set skills: $s)
                            handler: $_h)
                          $s)))))

;; Total over the collapsed result: skip () padding markers, return the first
;; real string, else (getSkills). (== x ()) is the registry's own empty-check
;; idiom (see the dispatch fn's eligible-empty branch).
(= (first-skill-or-default $strs)
   (if (== $strs ())
       (getSkills)
       (let $h (car-atom $strs)
            (if (== $h ())
                (first-skill-or-default (cdr-atom $strs))
                $h))))
