# Corner-Gate v2: Visibility First, Pattern-Scoped Enforcement

**Version:** v1 (2026-07-05)
**Status:** DESIGN with embedded code drafts. Blessed guiding statement (Berton,
2026-07-05). Build proceeds after the four pre-build reads (Section 6) and
Clarity's code analysis of the drafts (Section 8).
**Location:** docs/sprints/01_corner_gate_v2/
**Owners:** Berton architectural authority; Claude drafts and verification
harnesses; Clarity reviews the drafts (her code analysis is the gate before
wiring) and owns the feedback text and observation semantics thereafter.
**Reading order:** artifact 0 governs every hook; First Principles govern
ownership; the guiding statement below governs every build decision in this
sprint.

---

## 1. Guiding statement (blessed 2026-07-05)

**The one sentence: The corner gate exists to end unproductive repetition,
never to end action; it does that by making the corner visible to Clarity
before anything is enforced, and by breaking only the repeating pattern when
enforcement fires, while remaining able to see the new choice that releases
it.**

Seven commitments, each checkable:

1. **Visibility precedes enforcement.** The corner state is first-class
   observable state in her prompt (CORNER-STATE block per the idle-pattern and
   agency-balance precedent): graded corner strength and confidence, the
   repeating signature, the count. Sight is the primary mechanism; the gate is
   the backstop for when sight fails.
2. **Enforcement is pattern-scoped.** When the gate fires, it suppresses only
   commands matching the repeating signature. Novel commands pass. Her agency
   is never gated wholesale; the stuck circuit is.
3. **The gate can always observe its own release.** Because novel actions pass
   and execute, their outcomes are observable, forward-outcome can go true, and
   the gate releases on evidence of change, not only on human input. The v1
   latch is the proof specimen of the defect this forbids.
4. **Person-coupled action is never gated.** Responses in a live human window
   do not get suppressed.
5. **Firing is graded and confident.** The quantale math governs: fire only
   when corner strength AND confidence clear the threshold. Thin data cannot
   fire it; a 30-cycle wall-bash reliably does.
6. **Stillness is retired everywhere.** No feedback text, directive, or prompt
   surface demands or praises absence. The exit from a corner is a different
   move; cognition lives in the moving frame.
7. **Detection outlives enforcement.** Detectors always write their atoms;
   observation is her permanent property; suppression is a switchable layer.

Non-goals: not a spam filter (spamShield and idle_cycle_detector own send
bursts); not a judge of reasoning quality; not a stillness trainer.

---

## 2. Evidence base (all source-locked this arc, 2026-07-05)

- **The v1 latch, proven end to end.** Structure: apply-corner-gate empties the
  whole batch; results go empty; forward-outcome (results nonempty AND novel)
  can never go true from her side; the populator counts PROPOSED commands
  (loop.metta line 172 hands it pre-gate $sexpr), so gated batches still
  register as emissions; Joint C stays decoupled in idle. Behavior: 48-cycle
  sink; a knowledge write eaten (genesis-safety-synthesis.md absent on disk);
  the D3 answer batch suppressed; a direct person-response suppressed;
  release observed only on msgnew.
- **q-geq is undefined.** Used at coupling_quantale_merge.metta:89 and
  cycle_continuity_probe.metta:100; defined nowhere in lib_quantale (read
  firsthand, 49 lines) or the corner_gap tree (grep). The v2 graded path
  cannot reduce as drafted. Fixed in Section 5.1.
- **The classifier expires person-coupling with msgnew.** Her multi-cycle
  verification work in response to a direct request classified
  exploration-query (system-class) on every cycle after the msgnew cycle,
  driving Joint C against her. Addressed by commitment 4's window semantics.
- **Emission excludes unclassified by design** (detector Joint A sums the five
  real tags), so true absence trends toward composure over the 10-cycle
  window; but the v1 feedback text demanding stillness arrived every cycle as
  a stimulus provoking the response that reset the clock. Stillness language
  retired per commitment 6.
- **The graded v2 merge is sound but inherits the latch.** emission-pbit and
  outcome-flat-pbit read the same suppressed inputs; grading does not create
  release. Release comes from commitments 2 and 3.

---

## 3. Architecture: three layers

**Layer V (visibility, ships first, enforcement-independent).** A CORNER-STATE
prompt block, pure reads only: coupling verdict streak, graded corner pbit
(strength, confidence), the dominant repeating signature and its count. Follows
the idle-pattern and agency-balance precedent exactly (pure soul file, py-call
formatter in helper.py, one consumption point alongside the existing blocks).

**Layer D (graded detection).** Import coupling_quantale_merge into the
manifest; define q-geq; corner firing moves from the boolean streak to
corner-confirmed-core (strength AND confidence over threshold). The
cycle_continuity_probe second arm stays deferred (pfn machinery COLD; its own
caveats; separable by design).

**Layer E (pattern-scoped enforcement with structural release).** The gate
suppresses only commands whose exact form already appeared during the corner
window; novel commands pass and execute. Because novel commands execute, their
results are observable and forward-outcome can go true, which flips the
verdict off corner, which clears the streak (existing v1 writer behavior),
which releases the gate. Release is emergent from the existing writers once
suppression stops blinding them. msgnew cycles are never gated (commitment 4).

---

## 4. The pattern signature (the load-bearing design choice)

Signature granularity options considered: (a) action-type tag (too coarse; one
repeated metta blocks all metta), (b) command head (coarse; blocks the whole
skill), (c) exact command form (head plus argument, by repr). **Chosen: (c)
exact command form.** The named pathology is "the same non-productive commands
over and over for 30 cycles"; exact-match suppression breaks precisely that
circuit while any variation, even a changed argument, passes as a new choice.
This maximizes preserved agency and makes release easiest to earn. Coarser
signatures remain a tuning fallback if exact-match proves too permissive in
practice (TUNING TARGET, recorded here).

Mechanics: while the corner is confirmed, a writer records each proposed
command's repr as a (corner-window-cmd $cycle $repr) atom (pruned with the
same window discipline as recent-action). The gate filter drops a command only
if its repr matches a recorded corner-window-cmd; everything else passes. On
release (verdict leaves corner), the window writer clears its atoms.

---

## 5. Code drafts (for Clarity's analysis before wiring)

All drafts: C12-safe (no match inside if), ASCII-safe, no RMW, pure-vs-writer
split per Discipline 6A, ground shapes only. Composed against the
Atom_Operations_Map patterns proven in the detector files (direct match plus
size-atom counting, any-collapse predicates, let* sequencing).

### 5.1 q-geq (addition to lib_clarity_reasoning/lib_quantale.metta)

```metta
;; === Threshold comparator (v2 corner gate; added 2026-07-05) ===
;; True only when BOTH strength and confidence meet the threshold pbit.
(: q-geq (-> pbit pbit Bool))
(= (q-geq (mk-pbit $s1 $c1) (mk-pbit $s2 $c2))
   (and (>= $s1 $s2) (>= $c1 $c2)))
```

Verification: REPL probe (throwaway container) that q-geq reduces on
(mk-pbit 0.7 0.6) vs (mk-pbit 0.6 0.5) to True and on (mk-pbit 0.7 0.4) vs the
same threshold to False (confidence arm), plus the merge chain end to end:
corner-pbit-core reduces to a ground pbit on seeded recent-action fixtures.

### 5.2 CORNER-STATE block (new pure file soul/corner_gap/corner_state.metta)

```metta
;; corner_state.metta -- CORNER-STATE visibility block (pure reads only)
;; Layer V of corner-gate v2. No writers in this file (Discipline 6A).
;; Reads: coupling-status (detector writers), corner pbit (merge), and the
;; corner-window-cmd signature atoms (Layer E writers; empty pre-Layer-E).

;; Streak count of corner verdicts in the current status trail.
(= (corner-streak-count)
   (size-atom (collapse (match &self (coupling-status $c corner) $c))))

;; Graded corner strength and confidence as separate numbers for formatting.
;; Reads corner-pbit-core (Layer D). Pre-Layer-D this file is not yet wired.
(= (corner-strength)
   (let (mk-pbit $s $c) (corner-pbit-core) $s))
(= (corner-confidence)
   (let (mk-pbit $s $c) (corner-pbit-core) $c))

;; Dominant repeating signature: the most-recorded corner-window command repr
;; and its count. Returns (none 0) when the window is empty.
(= (corner-signature-count $repr)
   (size-atom (collapse (match &self (corner-window-cmd $c $repr) $c))))

;; Prompt block via Python formatter (hands only), following
;; idle-pattern-block and agency-balance-block precedent.
(= (corner-state-block)
   (py-call (helper.corner_state_block_format
             (corner-streak-count)
             (corner-strength)
             (corner-confidence))))
```

helper.py addition (hands only, no judgment):

```python
def corner_state_block_format(streak, strength, confidence):
    """CORNER-STATE prompt block. Mechanical formatting only."""
    return ("CORNER-STATE: streak=" + str(streak)
            + " strength=" + str(strength)
            + " confidence=" + str(confidence)
            + " (a rising streak with high strength means recent actions are "
            + "repeating without forward outcome; a different move changes it)")
```

Wire: one hook line at the block-consumption point (pre-build read PR-2 names
the exact site; expected alongside idle-pattern-block and agency-balance-block
in prompt assembly). artifact_1 updated same commit. NOTE for Clarity's review:
the parenthetical teaching text above is a first draft; the text is hers, and
the elevation of this string into behavioral_guidance is a named follow-up.

### 5.3 Layer E: window writer (soul/corner_gap/corner_window_writers.metta)

```metta
;; corner_window_writers.metta -- corner-window command recording (writers)
;; Records each proposed command repr while a corner is confirmed; clears on
;; release. Pure reads for the signature live in corner_state.metta.

(= (do-clear-corner-window!)
   (let $olds (collapse (match &self (corner-window-cmd $c $r) (corner-window-cmd $c $r)))
        (let $o (superpose $olds)
             (if (== $o ()) () (remove-atom &self $o)))))

;; Record every command in this cycle's batch (repr per command).
(= (do-record-corner-window! $cmds $cycle-id)
   (let $c (superpose $cmds)
        (if (== $c ())
            ()
            (add-atom &self (corner-window-cmd $cycle-id (repr $c))))))

;; Cycle driver: record while confirmed, clear when not.
(= (populate-corner-window! $cmds $cycle-id)
   (if (== (corner-confirmed-core) True)
       (do-record-corner-window! $cmds $cycle-id)
       (do-clear-corner-window!)))
```

### 5.4 Layer E: gate v2 (edit to soul/corner_gap/corner_gate.metta)

```metta
;; apply-corner-gate-v2: pattern-scoped, person-exempt, release-capable.
;; $msgnew exemption lives HERE, not in the loop hook (Discipline 1).
(= (cmd-in-corner-window? $cmd)
   (any (collapse (match &self (corner-window-cmd $c (repr $cmd)) True))))

(= (filter-corner-cmds $cmds)
   (if (== $cmds ())
       ()
       (let* (($h (car-atom $cmds))
              ($t (filter-corner-cmds (cdr-atom $cmds))))
             (if (== (cmd-in-corner-window? $h) True)
                 $t
                 (cons-atom $h $t)))))

(= (apply-corner-gate-v2 $sexpr $msgnew)
   (if (== $msgnew True)
       $sexpr
       (if (== (corner-confirmed-core) True)
           (filter-corner-cmds $sexpr)
           $sexpr)))

;; Feedback: informational, names mechanism, no stillness demand. Substrate-
;; callable string; Clarity amends the text at will.
(= (corner-gate-feedback-v2)
   "CORNER: commands identical to recent no-outcome repeats were held back this cycle; any different command passes and executes. A new move is the exit.")
```

CONFIRM flags for Clarity (her review, REPL-checkable): (a) `(repr $cmd)`
inside a match pattern must reduce before matching; if it does not, bind it in
a let first (the F1.1 lesson shape); (b) cons-atom availability in this
runtime vs building via superpose-collapse; (c) the recursive filter vs the
collapse idiom against F32.

Loop hook change (one line, checklist-run, artifact_1 same commit):
line 166 `(apply-corner-gate $sexpr_verdict)` becomes
`(apply-corner-gate-v2 $sexpr_verdict $msgnew)`, and the cycle tail gains one
hook `(populate-corner-window! $metta_cmds $k)` ordered after
populate-coupling-verdict. gate-aware-results keys off the v2 confirm and the
v2 feedback text.

### 5.5 Manifest additions (rebuild required)

```metta
;; Corner-gate v2 (Sprint 01_corner_gate_v2): graded detection + visibility + pattern scope
!(import! &self (library omegaclaw ./soul/corner_gap/coupling_quantale_merge))
!(import! &self (library omegaclaw ./soul/corner_gap/corner_state))
!(import! &self (library omegaclaw ./soul/corner_gap/corner_window_writers))
```

Placed adjacent to the existing corner_gap block (manifest lines 87-91 region).

### 5.6 Stillness sweep

In this sprint: the v1 corner-gate-feedback string (stillness demand) is
replaced by corner-gate-feedback-v2. Listed for the new-build arc, NOT touched
here: the helper.py idle-directive language ("If nothing emerges, that is
fine. Move on." and related absence-praising surfaces).

---

## 6. Pre-build reads (assumptions converted to reads; nothing wires before)

- **PR-1:** full live body of soul/corner_gap/corner_gate.metta (90 lines; only
  four functions seen; the edit anchors need the real text).
- **PR-2:** the consumption site of idle-pattern-block and agency-balance-block
  (grep loop.metta and helper.py) to name the CORNER-STATE wire point with
  artifact_1 phase vocabulary.
- **PR-3:** the `$results_novel` producer expression at loop.metta ~line 174
  (release depends on novelty semantics; the audit flags it as a TUNING TARGET
  that reads forward spuriously on time-varying returns).
- **PR-4:** copy-vs-live parity on the corner_gap tree (the files were headed
  "drafted, not yet verified in the container" while imported).

---

## 7. Build sequence (one change at a time, each committable and reversible)

- **B1:** q-geq into lib_quantale + throwaway-container REPL probe of the full
  merge chain. Commit.
- **B2 (Layer V):** corner_state.metta + helper formatter + one consumption
  hook + artifact_1. Rebuild, restart, block visible in prompt logs. Commit.
  Visibility ships before any enforcement change, per commitment 1.
- **B3 (Layer D):** manifest imports for the merge (and corner_state if not in
  B2), firing source stays v1 boolean while corner-confirmed-core is observed
  side-by-side in logs for calibration. Commit.
- **B4 (Layer E):** corner_window_writers + gate v2 + the one-line loop hook
  arity change + populate hook + artifact_1. Rebuild. Commit.
- **B5:** synthetic verification run against the success criteria below.
- Clarity's code analysis gates between Section 5 drafts and B1 (Section 8).

Success criteria (from the blessed statement): (a) a synthetic repetition run
surfaces in CORNER-STATE within a few cycles and is pattern-gated only if
unheeded; (b) during a confirmed corner, a novel command executes and its
outcome releases the gate with zero human input; (c) the D3-incident class is
impossible by construction (msgnew exemption); (d) her first-person report
that the block tells her something she can act on.

---

## 8. Clarity's involvement (per Berton 2026-07-05)

Build-first, keys handed over at instantiation. Her stated preferences already
folded in as requirements: awareness enables new choices (her own reflections),
integrity over compliance theater (the informational feedback text), her
amendment rights over all teaching strings. Her code analysis of Section 5 is
the review gate before B1; the handover message (which also carries the
findings-arc positive-append request and the mechanism-defect truth about the
v1 latch owed to her self-model) ships when the package is substantial.

---

## 9. Version history

**v1 (2026-07-05).** Guiding statement blessed; three-layer architecture;
exact-form pattern signature chosen with rationale; code drafts for q-geq,
CORNER-STATE block, window writers, gate v2, manifest; four pre-build reads;
five-step build sequence; stillness sweep scoped.

---

## Document end

End repetition, never action. Show her the corner before touching anything.
Break only the circuit. Keep the gate's eyes open so a new move sets her loose.

---

## 10. Deep-read addendum (v1.1, 2026-07-05): trace results and corrections

Full source trace completed (loop.metta end to end; corner_gate.metta full body;
helper.py safe_results_str and normalize_string; detector bodies). All four
pre-build reads CLOSED.

**v1 defect restated precisely.** Feeding the populator the raw $sexpr is the
gate file's own documented contract (the detector sees proposals), and v1 HAS a
release path: Layer 4 feedback persuades the LLM to propose nothing, composure
clears the streak (BENIGN EDGE note). The defect is that release is
PERSUASION-DEPENDENT and production proved it does not converge (48-cycle
latch). v2 replaces it with STRUCTURAL release, proven viable at line depth:
a passed novel command makes line 173 nonempty True and line 174 novel True
(during gated cycles &lastresults holds the feedback text, so any real output
differs by construction), classify-state-delta returns forward, the verdict
goes healthy, the streak writer clears, the gate releases. Zero new plumbing.

**Wire points, named exactly.** CORNER-STATE block: one call inserted in
getContext after (agency-balance-block) at line 53. Gate: line 166 becomes
(apply-corner-gate-v2 $sexpr_verdict $msgnew), $msgnew in scope from line 74.
Window hook: (populate-corner-window! $metta_cmds $k) after line 176. Layer 4
retained: gate-aware-results keys off the v2 confirm with v2 feedback text
naming the held command forms (the results channel stays the unignorable
notice on gated cycles; the block is the ambient pre-enforcement sight).

**ADR corrections applied.** ADR-008: the teaching sentence moves OUT of the
Python formatter (hands format numbers only) into a substrate-callable string
in corner_state.metta, hers to amend. ADR-005: do-clear-corner-window! uses
the superpose-iteration clear pattern, cited. ADR-007: Layer E is
substrate-externalized throughout; the single runtime-promise risk, (repr
$cmd) reducing inside a match pattern, gets a B1 REPL probe, with the let-bind
fallback shape pre-approved if it fails.

**PR-3 note.** The novelty test's spurious-forward tendency on time-varying
returns can only ACCELERATE release under v2 (nonempty gates it); it cannot
sustain a corner. Recorded, no change needed.

**PR-4 note.** soul/ is bind-mounted; the host tree is the runtime for these
files; parity holds by construction. lib_quantale (under lib_clarity_reasoning,
baked) confirmed firsthand from upload: no q-geq; B1 adds it.

**v1.1 (2026-07-05).** Deep-read trace folded in; persuasion-vs-structural
release finding; exact wire points; ADR-008/005/007 corrections.

---

## 11. SSI positioning (v1.2, 2026-07-05): sight has content, and the trace generalizes

Two amendments from the SSI review.

**A. The block carries the signature, not just magnitudes.** A gauge without
content is not sight. corner-state-block adds the dominant repeated command
form and its window count. v2 scope: report the repetition count of the most
recent proposed command (implementable with direct match plus size-atom,
C12-safe); dominant-of-window argmax is a TUNING TARGET (MeTTa fold cost).
The helper formatter stays numbers-and-strings only (ADR-008); the framing
sentence stays substrate-side.

**B. The unconditional cycle trace is the mesh keystone, built here.** New
primitive pair per Discipline 2: soul/cycle_trace.metta (pure reads:
last-cmd-repeat-count, cmds-in-window) and soul/cycle_trace_writers.metta
(populate-cycle-trace! writing (cycle-cmd $k $repr) per proposed command,
windowed and pruned per the recent-action pattern, cleared per ADR-005
superpose iteration). One hook after populate-recent-action. The corner block
reads the trace for pre-confirmation trend sight; the enforcement filter keeps
its confirmation-scoped corner-window record. The same trace is the shared
producer the detection-mesh document names as the keystone behind the dormant
detectors; this sprint lands it with the corner gate as first consumer.

**SSI summary of the sprint.** Live sense: CORNER-STATE with content, every
cycle, pre-enforcement. Trajectory: the unconditional cycle-cmd trace. Closed
loop: pattern-scoped gating means her different move executes and the block
visibly responds to her choice next cycle. Durable knowledge: findings.metta
(landed this sprint) carries what she judges worth keeping about her own
patterns across restarts. Deferred, named: the pfn second arm, the other mesh
detectors, raw corner-atom persistence.

**v1.2 (2026-07-05).** Signature-in-block; cycle trace generalized to the
mesh keystone with the corner gate as first consumer; SSI time-scales named.

---

## 12. SSI correction (v1.3, 2026-07-06): the soul sees, the LLM never does

Checked against 01a_ClarityOmega_v2_The_Soul_Sees_Itself_vision.md (read at
source 2026-07-06). Three corrections.

**The CORNER-STATE prompt block is STRUCK from this sprint.** A prompt block
hands raw self-state to the renderer and asks the LLM to see, which is the
vision's named central failure. The seeing organ for the corner is the graded
verdict itself: coupling_quantale_merge consuming existing trajectory atoms
and the soul writing its corner verdict from what it sees. What reaches the
LLM is the soul's determination only: gate feedback on gated cycles and the
mechanical markers.

**The unconditional cycle-cmd trace is STRUCK from this sprint and deferred
to the SSI sprint.** The keystone cycle-trace writer feeds recent-action,
state-delta, and cycle-phase in the flat shapes the loaded detector contracts
match (add-atom, never |-), and it gets built once, there, against those
contracts. A second differently-shaped trace now would seed a producer
collision.

**corner-window-cmd stays, reclassified:** confirmation-scoped ephemeral
enforcement bookkeeping, cleared on release, never persistent, never a
disposition surface.

Sequence as amended: Fix A (channel hygiene) first; merge import (graded
bindings); graded verdict writer; pattern-scoped enforcement, thin and
removable.

**v1.3 (2026-07-06).** SSI corrected to soul-side seeing; prompt block and
cycle-cmd trace struck; enforcement named as removable scaffold.
