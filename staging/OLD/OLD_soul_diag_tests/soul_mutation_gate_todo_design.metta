;; soul_mutation_gate_corrected.metta - DESIGN PROPOSAL for the two TODOs
;; Builds on Clarity's REPL findings (Arc-017): string-contains is globally
;; broken (returns true for all inputs), car-atom + quote works, structural
;; extraction works. Both remaining functions get structural replacements.
;;
;; This is Claude's design proposal for Clarity to verify in the REPL and
;; author the final form. The string-contains versions are removed entirely.

;; ===== ALREADY FIXED BY CLARITY (kept for context) =====

(= (soul-is-metta-cmd? $cmd)
   (== (car-atom (quote $cmd)) metta))

(= (soul-any-metta? $cmds)
   (any (collapse (let $c (superpose $cmds) (soul-is-metta-cmd? $c)))))

(= (soul-extract-metta-arg (metta $arg)) $arg)
;; Fallback if the metta keyword is consumed before pattern matching
;; (Clarity verified this form returns the arg):
;; (= (soul-extract-metta-arg $cmd) (car-atom (cdr-atom (quote $cmd))))


;; ===== TODO 1 REPLACEMENT: soul-metta-targets-soul-namespace? =====
;;
;; PROBLEM: the old form did string-contains on the argument string for the
;; four namespace prefixes. string-contains is dead. We need a structural check.
;;
;; ATOM FORMAT (the detail Clarity asked for): the extracted arg is the inner
;; command of a metta() call. From the test cases it has the shape
;;   (add-atom &self (soul-note x))
;;   (add-atom &self (priority ...))
;;   (add-atom &self (irreversible ...))
;;   (add-atom &self (tension ...))
;; So the structure is: (add-atom &self (NAMESPACE-HEAD ...)). The thing that
;; identifies a soul-namespace target is the HEAD SYMBOL of the THIRD element
;; of the add-atom expression. For (add-atom &self (soul-note x)):
;;   element 0 = add-atom
;;   element 1 = &self
;;   element 2 = (soul-note x)   <- car-atom of this = soul-note
;;
;; DESIGN: extract the head symbol of the target atom, then test it against the
;; known namespace identifiers. Two layers, both structural (no strings).
;;
;; Step 1: get the target atom (third element) and its head symbol.
;;   (quote $arg) to prevent evaluation, then navigate with car/cdr-atom.
;;   third element = (car-atom (cdr-atom (cdr-atom (quote $arg))))
;;   its head      = (car-atom <third element>)
;;
;; Helper: head symbol of the add-atom target.
(= (soul-target-head $arg)
   (car-atom (car-atom (cdr-atom (cdr-atom (quote $arg))))))

;; Step 2: is that head one of the soul-namespace identifiers?
;; NOTE on soul- prefix: the old code matched the "soul-" PREFIX (soul-note,
;; soul-value, etc. all count). car-atom gives the full symbol (e.g. soul-note),
;; not just the prefix. So an exact == against a fixed list will NOT catch every
;; soul- atom. TWO OPTIONS for Clarity to choose (substrate call):
;;
;;   OPTION A (exact identifiers, simplest, if the soul namespace uses a fixed
;;   small set of heads): enumerate them.
(= (soul-head-is-namespace? $h)
   (any (collapse (superpose (
     (== $h priority)
     (== $h irreversible)
     (== $h tension)
     (== $h soul-note)
     (== $h soul-value)
     (== $h soul-pattern))))))
;;   ^ Clarity: extend this list to the actual soul- head set. This is the
;;   detail I do not have authoritatively: the COMPLETE set of soul-namespace
;;   head symbols. If the set is open-ended (any soul-* symbol), Option A is
;;   insufficient and we need Option B.
;;
;;   OPTION B (prefix test without string-contains): if "any symbol starting
;;   soul-" must match, we need a structural prefix test. string-contains is
;;   dead, so this requires either a working substring primitive (Clarity to
;;   confirm one exists, e.g. a different string op that DOES discriminate) or
;;   a convention that all soul-namespace atoms are pre-tagged. FLAG: if Option
;;   B is needed, this is a real open question, not a trivial replacement.
;;
;; Composed (Option A path):
(= (soul-metta-targets-soul-namespace? $arg)
   (soul-head-is-namespace? (soul-target-head $arg)))


;; ===== TODO 2 REPLACEMENT: soul-mutation-pending? =====
;;
;; PROBLEM: old form did (string-contains (get-state &soul_mutation_lock)
;; "LOCKED:"). string-contains is dead. Need a structural equality check.
;;
;; STATE FORMAT (the detail Clarity asked for, and a DESIGN CHOICE we should
;; make now): the lock was a string "LOCKED: <arg>". Since string ops are dead,
;; the cleanest fix is to change what the lock STORES: store a bare symbol, not
;; a "LOCKED:"-prefixed string. Then pending-detection is an == against the
;; symbol, no string op.
;;
;; PROPOSED state convention:
;;   unlocked: &soul_mutation_lock = ()        (empty / unset)
;;   locked:   &soul_mutation_lock = (LOCKED <arg-atom>)
;; Then:
(= (soul-mutation-pending?)
   (not (== (get-state &soul_mutation_lock) ())))
;;
;; And the lock WRITE (in the gate, master doc lines 1424-1425) changes from
;; storing "LOCKED: ..." to storing (LOCKED <arg>):
;;   (change-state! &soul_mutation_lock (LOCKED (car-atom (quote $args))))
;; and the unlock/clear stays:
;;   (change-state! &soul_mutation_lock ())
;;
;; CONSEQUENCE: this changes the lock format, so the native block in the output
;; intercept (Repair 1) must write the lock in the new (LOCKED ...) form, not the
;; "LOCKED: " string form. Claude updates the Repair 1 native block to match
;; once Clarity confirms this convention. The two must agree.
;;
;; VERIFY IN REPL (Clarity): (1) get-state syntax that returned format errors,
;; (2) that (== (get-state &x) ()) discriminates unset vs set, (3) whether ()
;; is the right empty sentinel or whether a different unset value is returned.
