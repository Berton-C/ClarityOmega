# NACE Hook Wiring: Remaining Work and Investigation Handoff

**Status:** Handoff. Sprint 0-Coda Phase C is committed (38737ac); NACE's hard
dependency is now satisfied. This document is the entry point for the next
working session on NACE.
**Reading order:** This first (current state and the gate), then
`nace_implementation_plan.md` (the full step ladder N0 to N6), then
`nace_inloop_hook_spec.md` (the approved hook design).
**Authorship of this work:** the loop hook, the writer file, the wiring, and the
integration are Berton + Claude. Clarity authors substrate atoms and MeTTa logic
where the writer needs new substrate functions; the loop integration is ours.

---

## 1. Where this stands after Phase C

Sprint 0-Coda was a hard dependency for NACE, not a preference. NACE gates and
learns from capability dispatch, and until capabilities dispatched through a live
registry there was nothing to gate and no outcomes to record. Hooking NACE in
before that would have wired a governance-and-learning layer onto a dispatcher
that did not fire.

That dependency is now met. As of commit 38737ac the capability registry
dispatches live each cycle through getContext, skill-discovery is registered and
verified to reach its handler (not fallback), and the dispatch path is proven by
exercise. So NACE now has a live dispatcher to gate (via should-dispatch) and live
dispatch outcomes to learn from (via the recorder). The work below can begin.

What does NOT change because of Phase C: the NACE design itself. The hook spec is
approved, three of the four runtime files are built and verified, and the step
ladder in `nace_implementation_plan.md` stands as written. Phase C satisfied the
dependency; it did not alter the plan.

---

## 2. What NACE is, in one paragraph

When a capability runs, its outcome (worked or failed) revises a belief about
that capability's efficacy. The belief is a NAL truth value `(stv freq conf)`.
Revision is `Truth_Revision` (lib_nal). A dispatch gate `should-dispatch` reads
the belief to decide whether to run a capability. Beliefs persist in files across
cycles and restarts. The loop is the only thing that can run the revision, because
lib_nal is only loaded inside the running loop process.

---

## 3. What is already done and verified

- `soul/nace_substrate.metta`: the definitions, verified live by Clarity.
  `evidence-stv`, `current-efficacy` (defaults to `(stv 0.5 0.0)` for an unknown
  cap), `revise-efficacy` (calls Truth_Revision, verified to reduce live),
  `efficacy-expectation` (Truth_Expectation, verified live), `should-dispatch`
  (gate at expectation >= 0.3), and `updated-belief-atom` (builds the persistable
  atom, with the force-evaluation fix). Truth_Revision and Truth_Expectation are
  confirmed reducing in the live process and checked to the digit against the NAL
  formula.
- `soul/nace_beliefs.metta`: the store, three seed capabilities at agnostic
  `(stv 0.5 0.0)`. Its header still says "Courier writes this file only," which is
  stale (the courier is dead). The header fix is folded into N1, not a separate
  task.
- `soul/nace_pending.metta`: the queue, empty for v1, with header guardrails
  naming valid outcomes and the known-cap constraint.
- `nace_inloop_hook_spec.md`: the hook design, approved by Clarity, all review
  notes folded in, v1 boundaries named.

The fourth runtime file, `soul/nace_writers.metta`, is specced but not built. It
is blocked behind the investigation in Section 5.

---

## 4. What is dead, do not deploy

- `nace_courier.py` (external courier): killed by the fact that nothing external
  reaches lib_nal.
- All run.sh-based verify scripts (`verify_nace.py`, `verify_nace_substrate.py`,
  the `probe_*` NACE scripts): they test in a context where lib_nal is not loaded,
  so their results on any lib_nal function are meaningless. NACE verification
  happens in the live loop.
- `nal_revision.py`: keep as reference only (the Python formula the substrate's
  Truth_Revision is checked against; they agree to the digit). Never on the
  production path.

---

## 5. The investigation that must come first (N0.5, the gate)

This is investigation-first by nature, not a build. It is the same shape of
unknown that the `|-nal` lesson was: something untested in the right context with
a confident-looking plan built on top of it. Resolve it before building anything.

### 5.1 The open question

Does an atomspace read-modify-write of the belief atom compose within a single
live-loop cycle, so that `current-efficacy` sees the revised value the same cycle?

### 5.2 Why it is open

The caller_operations_probe (PROBE E/F) found that `set-atom!`, and by extension
the remove-old + add-new pattern, inside a let-chain in standalone run.sh returned
the unreduced `set-atom!` expression rather than executing the mutation, and the
subsequent read in the same evaluation showed the OLD value. `add-atom` and
`remove-atom` alone worked; the read-then-write-back pattern did not.

This matters because N1's dual-write does exactly that: it reads the belief, then
removes the old belief atom and adds the revised one, so that `current-efficacy`
sees the revision this run. That is a read-modify-write, the exact operation PROBE
E showed not composing in standalone run.sh. So the atomspace-update half of N1 is
NOT proven to work.

There is reason to think it may work in the live loop and not in run.sh: task_state
writers use set-atom! read-modify-write and apparently persist in production, which
is the in-process atomspace persisting while the process runs. But the run.sh
result and the production task_state behavior have not been reconciled for this
exact belief-atom operation. It must be tested in the live loop, not run.sh, the
same context lesson as `|-nal`.

### 5.3 The test (live loop only, via Clarity's metta skill)

Read a belief, write it via set-atom!, read again in the same cycle:

```
(let $old (current-efficacy web-search)
     (let $_ (set-atom! &self (cap-efficacy web-search $old)
                              (cap-efficacy web-search (stv 0.9 0.2)))
          (current-efficacy web-search)))
```

Expect `(stv 0.9 0.2)` if same-cycle read-after-write composes. If it returns the
old `(stv 0.5 0.0)` or an unreduced set-atom! expression, it did not compose (the
PROBE E result), and the fork below applies. Run it in the live process, the
context where set-atom! has its in-process atomspace, not in run.sh.

### 5.4 The fork, resolve here not mid-build

- It composes in the live loop: N1's dual-write is sound. Build as specced.
- It does NOT compose even in the live loop: the atomspace-update half is
  impossible same-cycle, and the architecture must change. Drop the atomspace
  update, write only the file, and accept that current-efficacy reads the revised
  value only after a restart reloads the file, or find another read path that
  re-reads the file. This is a real architecture change, not a tweak, and it is
  decided at N0.5, not discovered during N1.

A note on scope of the answer: even if it composes, there is a designed one-cycle
belief lag (S1). The hook processes pending revisions at Phase 4.0, but that cycle's
dispatch decisions read the belief as it was at cycle start, so a revision applied
this cycle affects next cycle's dispatch, not the current one. That is
architecturally fine (a belief update is evidence for future decisions). The N0.5
question is narrower: does the write land and become readable in-process at all, not
whether it is readable before the same cycle's dispatch.

---

## 6. The build ladder after the gate

From `nace_implementation_plan.md` Section 6, in dependency order. N0 can be done
independently of the N0.5 investigation; N1 onward waits on the N0.5 fork.

- **N0 (load path, can land now):** add two import lines to
  `lib_clarity_reasoning/lib_clarity_reasoning.metta`, for nace_substrate and
  nace_beliefs, after the last soul/ import. Do NOT add nace_pending: the writer
  reads pending entries from the file, not the atomspace, and auto-loading pending
  would create atomspace ghost-state the file-reading writer never processes. This
  asymmetry (substrate + beliefs loaded, pending not) is deliberate. NOTE: verify
  the current state of these imports first, because the Phase C manifest history
  (48a73ba and 38737ac) touched this file; confirm what is already present before
  adding, the same git-status-before-claim discipline used in Phase C.
- **N0.5 (the gate, Section 5):** resolve the read-modify-write question. Blocks
  N1.
- **N1 (build nace_writers.metta):** define `do-process-pending-revisions!` per
  hook spec Section 3: read and parse pending entries from the file, evaluate
  `updated-belief-atom` per entry, dual-write the revised belief (atomspace + file),
  remove the processed entry by full-file rewrite. Pure-vs-writer split: definitions
  stay in nace_substrate.metta, the do-*! writer goes here, register in the manifest.
  Also fix the stale nace_beliefs.metta header in this step. Done criterion: the
  writer reduces without error against a test pending file, nace_beliefs shows the
  revised belief, the processed entry is removed.
- **N2 (loop hook):** one line at Phase 4.0, after message reception, before prompt
  assembly: `($_ (do-process-pending-revisions!))`. Single call, no inline logic.
  Run the hook spec Section 6 checklist and the Artifact 0 Section 3 hook checklist
  before committing.
- **N3 (artifact_1 update, same commit as N2):** Phase 4.0 entry documenting what
  the hook reads, writes, and calls, per the Artifact 0 maintenance contract.
- **N4 (verify in the live loop):** drop a test pending entry using one of the three
  SEED capabilities (not web-search, which only exercises the unknown-cap default
  path; a seed cap exercises the real replace-existing-belief-line path). Run one
  cycle. Confirm the belief in nace_beliefs.metta changed, the in-atomspace atom
  changed (query live), and the pending entry was removed. Verify the revised value
  against the NAL reference formula.
- **N5 (should-dispatch as the registry gate):** the registry consults
  `should-dispatch $cap` before dispatching, reading the efficacy belief. This is
  the gate NACE was built to provide, and it connects directly to the registry
  Phase C just wired live.
- **N6 (the real recorder, closes the loop):** after a capability dispatches and its
  outcome is known, write `(pending-revision $cap confirmed|disconfirmed)` to
  nace_pending.metta. This closes the cycle: dispatch, outcome, pending entry, hook
  revises, belief updates, next dispatch gate sees the new belief.

---

## 7. The other genuinely hard open question (N6, flag now)

Outcome determination. A capability can return a value, time out, throw, return
empty, or return something malformed. Which map to `confirmed` versus
`disconfirmed`? A clean return is confirmed; a thrown exception is likely
disconfirmed; but a timeout, an empty result, or a malformed result are genuinely
ambiguous. This mapping is unaddressed and non-trivial. It likely needs a third
outcome (ambiguous, no revision, the evidence-stv None path) or per-capability
outcome interpreters, and may justify extending evidence-stv beyond its two v1
tokens. Resolve this in N6 design; do not let it surface as a runtime surprise.

---

## 8. Known v1 boundaries (carried from the hook spec)

- Dual-write is not atomic; atomspace and file can diverge on a mid-write crash,
  with restart reverting to the last-good file. Acceptable for v1.
- Race on the pending file: a recorder append during a hook rewrite can lose the
  entry. Fine for the v1 manual writer; the real recorder (N6) needs a lock or an
  append-only handoff.
- Unknown-cap on the write side: current-efficacy defaults safely on read, but the
  dual-write has no belief line to replace for an unknown cap. The real recorder
  needs a defined behavior, append-new or reject.
- Full-file rewrite is a scalability ceiling, fine for 3 to 10 beliefs, not 50+.
  Future: append-only log with compaction, or an indexed store.

---

## 9. The architecture, named

The pending file is a narrow asynchronous interface. The recorder deposits an
intention (capability X had outcome Y); the loop processes it next cycle. The
recorder does not know about Truth_Revision; the revision system does not know
about skill dispatch. This decoupling is what makes NACE sound and extensible: the
real recorder writes to the same surface the v1 test writer used, and the hook does
not change. The pattern (pending file, in-loop hook, substrate revision,
dual-write) is reusable; NACE is the first instance of a generic
capability-learning loop, not the only possible one.

---

## 10. First moves for the next session

1. Decide push first or investigate first (the branch is currently ahead of origin
   after Phase C).
2. Land N0 (the two import lines), after verifying the current manifest state
   against git, since Phase C history touched that file.
3. Run the N0.5 live-loop read-modify-write test (Section 5.3) via Clarity's metta
   skill, read the result in full, and take the fork.
4. Only then build N1.

Do not build N1's dual-write until the N0.5 result is known. Test before building.
