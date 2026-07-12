;; soul_namespace_check_candidates.metta
;; Several concrete candidate implementations of soul-metta-targets-soul-namespace?
;; to test factually in the harness, corner-gap methodology: build options, log
;; what works, keep the winner. Grounded in the PROVEN idioms from
;; coupling_integrity_detector.metta and state_delta_writer.metta:
;;   - match &self with full-arity patterns (never substring)
;;   - car-atom of a collapsed match, guarded by (if (== $x ()) ...)
;;   - C12-safe: no match inside if
;;   - structural detection, not string detection (string-contains is dead)
;;
;; THE PROBLEM: given the extracted metta arg (an atom like
;; (add-atom &self (soul-note x))), decide if it targets the soul namespace.
;; The target identifier is the head symbol of the third element:
;;   (add-atom &self (soul-note x)) -> target atom (soul-note x) -> head soul-note
;; The soul- set is open-ended (100+ symbols), so we need a PREFIX decision on
;; the head symbol, with NO working substring primitive.
;;
;; Each candidate is named distinctly so the harness can load ONE at a time and
;; the proof log shows which was active. They are mutually exclusive (same
;; function name), so the harness rewrites the active one per run.

;; ----------------------------------------------------------------
;; Shared helper (proven car/cdr navigation, quote to stop evaluation)
;; ----------------------------------------------------------------
;; target head symbol of (add-atom &self (TARGET ...)):
(= (soul-target-head $arg)
   (car-atom (car-atom (cdr-atom (cdr-atom (quote $arg))))))

;; ================================================================
;; CANDIDATE 1: decons-to-chars prefix test (pure structural)
;; Hypothesis: a symbol can be rendered to an atom-list of characters via a
;; native op, and we compare the first five chars to (s o u l -). If a
;; char-decomposition primitive exists, this is fully native, no substring.
;; VERIFY IN REPL: does (symbol-to-chars X) or (chars X) or similar exist?
;; If yes, compare first 5. If no native char decomposition, this candidate
;; is dead and we move to C2/C3.
;; ----------------------------------------------------------------
;; (placeholder shape, exact primitive TBD by REPL discovery)
;; (= (soul-head-is-namespace? $h)
;;    (let $cs (<char-decomp-primitive> $h)
;;       (prefix-matches $cs (s o u l -))))

;; ================================================================
;; CANDIDATE 2: match against a maintained soul-namespace registry atom
;; Hypothesis (the corner-detector idiom applied): instead of testing the
;; symbol's NAME, maintain a registry of soul-namespace head symbols as atoms
;; in &self, e.g. (soul-namespace-head soul-note), and match against it. This
;; sidesteps prefix-testing entirely: membership becomes a structural match,
;; the exact thing coupling_integrity_detector does with recent-action.
;; The registry can be generated once from the grep Clarity already did.
;; ----------------------------------------------------------------
;; Registry atoms (generated; sample shown, full set from the 100+ grep):
;; (soul-namespace-head soul-note)
;; (soul-namespace-head soul-value)
;; (soul-namespace-head priority)
;; (soul-namespace-head irreversible)
;; (soul-namespace-head tension)
;; ... (full set) ...
;;
;; Membership by structural match (C12-safe, proven idiom):
(= (soul-head-registered? $h)
   (if (> (size-atom (collapse (match &self (soul-namespace-head $h) $h))) 0)
       True
       False))
;;
;; Tradeoff: requires maintaining the registry when new soul- atoms are added.
;; But: the registry can itself be a soul-namespace target, and adding a soul-
;; atom is exactly the gated event, so the registry update flows through the
;; gate. Open question for Clarity: is the head set stable enough that a
;; generated registry is acceptable, or does it churn too fast?

;; ================================================================
;; CANDIDATE 3: py-call forced exception (the fallback if 1 and 2 fail)
;; Hypothesis: no native prefix test and no acceptable registry, so the prefix
;; match is done in Python, documented as a FORCED exception to ADR-008 (runtime
;; offers no native substring; not convenience). The judgment of WHAT to do with
;; the result stays native; only the mechanical prefix-char-compare is Python.
;; ----------------------------------------------------------------
;; (= (soul-head-is-namespace? $h)
;;    (py-call (helper.soul_head_has_soul_prefix (repr $h))))
;; where the helper is the minimal mechanical prefix test:
;;   def soul_head_has_soul_prefix(h): return h.startswith("soul-") or h in ("priority","irreversible","tension")
;; This is hands (mechanical char compare), per ADR-008, BUT it is only chosen
;; if C1 and C2 both fail, and it is logged as forced.

;; ================================================================
;; Composed entry point (same for all candidates; calls soul-head-is-namespace?
;; or soul-head-registered? depending on which candidate is active):
;; (= (soul-metta-targets-soul-namespace? $arg)
;;    (soul-head-is-namespace? (soul-target-head $arg)))
