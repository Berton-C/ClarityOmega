# NACE In-Loop Revision: Hook Spec (Draft for Review)

**Status:** DRAFT for Berton/Clarity review. Not yet implemented.
**Governs:** A loop.metta hook plus soul-side reader, per artifact_0 disciplines.
**Supersedes:** The external `nace_courier.py` model (dead: nothing external reaches the live atomspace, confirmed by Clarity's reading of loop.metta + metta_bridge.py).

---

## 0. Why this changed

The external courier could not work. The live atomspace (where lib_nal's
Truth_Revision reduces) is only reachable from inside the running loop process.
Any external script (run.sh, docker exec) starts a fresh process without lib_nal,
which is the non-reduction we kept hitting. So the revision must run inside the
loop. This spec scopes that as a per-cycle hook following artifact_0.

What survives unchanged: `soul/nace_substrate.metta` (definitions, verified live
by Clarity), `soul/nace_beliefs.metta` (the store), and the principle (revision
is substrate's Truth_Revision; files are persistence). What changes: the loop
drives the revision each cycle from pending data, not an external script.

---

## 1. Surface investigation (Discipline 6 Part B)

Filling the template before designing, against actual loop.metta.

**Surface name:** efficacy belief atoms `(cap-efficacy $cap (stv $f $c))` plus a
new pending-revision file.

**A. Writers (atoms going INTO the surface)**
- Belief atoms: written by the loop's new revision hook (this spec), to
  `soul/nace_beliefs.metta`. No other writer.
- Pending-revision entries: written by whatever records a skill outcome (the
  "recorder," see open question Q1). Written to `soul/nace_pending.metta`.

**B. Consumers (atoms going OUT of the surface)**
- Belief atoms read by: the dispatch gate `(should-dispatch $cap)` (future
  registry wiring), and by `current-efficacy` inside the revision itself.
- Pending entries read by: the loop's revision hook, each cycle.

**C. Intermediate transformations**
- `updated-belief-atom` -> `revise-efficacy` -> `Truth_Revision` (lib_nal).
  All in nace_substrate.metta, all verified to reduce live.

**D. Configuration levers**
- `wakeupInterval` (initLoop): sets cycle cadence. The revision hook runs once
  per cycle, so cadence = wakeupInterval. No new constant needed.
- Dispatch threshold 0.3: lives in nace_substrate.metta `should-dispatch`.

**E. Other consumers downstream**
- The beliefs file is read at startup into the atomspace via `initSoulSeeds`
  (loop.metta line 58: "seed soul memory once at startup"). The loop then
  operates on in-atomspace atoms; it does NOT re-read soul files each cycle.
  RESOLVED (Clarity, from source): therefore the revision hook MUST dual-write,
  update the in-atomspace belief atom (remove old + add new) AND write the
  beliefs file. File-only would not be seen until restart; atomspace-only would
  not survive restart. Both are required.

**F. Design questions deferred to Clarity**
- Q1 (recorder): what records "capability X had outcome Y" into the pending
  file? In the current state there is no skill-dispatch accounting yet. For the
  first version, the recorder can be a manual/test writer; the real recorder is
  the future registry wiring (Clarity's Steps 3-4). The hook does not depend on
  who writes pending entries, only that they appear in the file. RESOLVED
  (Clarity agrees): v1 manual/test writer, real recorder defers to registry.
- Q2 (caching): RESOLVED above. The loop caches at startup; dual-write required.

---

## 2. File format

Two files, both in `soul/`, both persistent, both survive restart (files-are-
the-store, the settled persistence model; state-variables vanish on restart so
they are NOT used here).

**`soul/nace_beliefs.metta`** (exists): the belief store.
```
(cap-efficacy web-search   (stv 0.5 0.0))
(cap-efficacy file-write   (stv 0.5 0.0))
(cap-efficacy metta-query  (stv 0.5 0.0))
```

Initial confidence 0.0 means no evidence yet. After one `confirmed` revision,
Truth_Revision of (stv 0.5 0.0) with (stv 1.0 0.1) yields (stv 1.0 0.1): a
0.0-confidence prior contributes zero weight, so first evidence fully determines
the result. The 0.0 initial state is absorbent (yields cleanly to first
evidence), not fragile. Correct initial state for an untested capability.

**`soul/nace_pending.metta`** (new): pending revision entries. One atom per
unprocessed outcome. Shape:
```
(pending-revision <cap> <outcome>)
```
e.g. `(pending-revision web-search confirmed)`. The loop processes these each
cycle and removes each after applying it. Empty file (or no pending-revision
atoms) means nothing to do.

**Valid outcome values** (must match nace_substrate.metta's evidence-stv
mapping): `confirmed` and `disconfirmed`. These are the only two tokens
evidence-stv accepts (confirmed -> (stv 1.0 0.1), disconfirmed -> (stv 0.0 0.1)).
A pending-revision with any other outcome token has no evidence mapping and must
be rejected by the recorder, not silently processed. If a third outcome
(ambiguous, weighted) is added later, it is added to evidence-stv first, then
becomes a valid pending token.

Why a file, not a state variable: efficacy data and its pending queue must
survive restart. `&pending_soul_mutation` is a within-cycle lock that clears
intentionally; it is the right tool for its job and the wrong tool here. Same
reasoning that put beliefs in a file puts the pending queue in a file.

---

## 3. The hook (Discipline 1, 3)

**One hook line, one named function, landing in a named phase.**

**Phase location:** Phase 4.0 (Iteration entry), in the per-cycle `let*`,
AFTER the message-reception block (after the `do-set-last-activity!` hook at
current line 75) and BEFORE prompt assembly (Phase 4.3). Rationale: revision is
mechanical bookkeeping on observed outcomes, it belongs with the other
mechanical observations at iteration entry, not in reasoning or output phases.
It must run before the dispatch gate would be consulted in prompt assembly, so
the belief is current when read.

**Hook line (the single call):**
```metta
($_ (do-process-pending-revisions!))
```

`do-process-pending-revisions!` is one function. The hook does no dispatch, no
arithmetic, no inline state writes. It calls one named writer. (Discipline 1.)

**What the function does (defined soul-side, NOT inline in loop.metta):**

Read mechanism note (Clarity): pending entries written to the file mid-run are
NOT in the atomspace (initSoulSeeds loaded at startup only). So the hook must
NOT use `match &self` for pending entries; it reads the file directly. This also
keeps transient pending data out of the atomspace.

1. Read pending entries: `read-file soul/nace_pending.metta`, parse the
   `(pending-revision $cap $outcome)` entries from the string. (NOT match &self.)
2. For each entry: evaluate `(updated-belief-atom $cap $outcome)`. lib_nal is
   loaded here, so Truth_Revision reduces. This is the whole point of in-loop.
3. DUAL-WRITE the revised belief (Q2 resolved, both required):
   a. Atomspace: remove the old `(cap-efficacy $cap ...)` atom and add the new
      one, so current-efficacy sees the revised value THIS run.
   b. File: rewrite `soul/nace_beliefs.metta` with the new value, so it survives
      restart.
4. Remove the processed `(pending-revision ...)` entry from the pending file.

Sequential processing is intentional and NAL-correct: if the pending file holds
two entries for the same capability in one cycle (confirmed then disconfirmed),
the second revision revises the RESULT of the first. NAL revision accumulates
evidence, so this is correct, not an ordering bug. Order within a cycle follows
file order.

File-operation constraint (Clarity): the loop has only `write-file` (overwrite
whole file) and `append-file`, NO replace-line primitive. So steps 3b and 4 each
require: read-file the whole file, do the string replacement/removal, write-file
the whole file back. The writer functions must implement full-file rewrite, not
line edits. This is real implementation complexity to budget for, not a detail.

All cognition (the revision) is Truth_Revision in the substrate. The function's
hands work (read file, string-edit, write file, atomspace remove/add) uses the
loop's existing primitives, not external Python.

---

## 4. File organization (Discipline 2, 6 Part A)

Per-primitive, pure-vs-writer split, matching the task_state precedent:

- `soul/nace_substrate.metta` (exists): PURE definitions. Atom shapes, evidence
  mapping, read helpers (current-efficacy), and the compute functions
  (revise-efficacy, updated-belief-atom, efficacy-expectation, should-dispatch).
  Header states: "Side-effecting writers (do-*!) land in nace_writers.metta."
- `soul/nace_writers.metta` (NEW): the side-effecting writer
  `do-process-pending-revisions!` and any do-*! helpers it needs (the
  file-writing steps). This is where the hands-that-touch-files live.
- Both register in `lib_clarity_reasoning/lib_clarity_reasoning.metta`.

This keeps nace_substrate.metta queryable without side effects (Clarity already
tests revise-efficacy etc. live with no file writes), and isolates the
file-mutating code in the writers file.

---

## 5. Maintenance contract (Discipline 4)

The implementing commit includes, together:
1. `soul/nace_writers.metta` (the writer).
2. `soul/nace_pending.metta` (initial empty pending file).
3. lib_clarity_reasoning.metta import line for nace_writers.
4. The loop.metta hook line in Phase 4.0.
5. `artifact_1_loop_metta_wiring_diagram.md` Section 4 update for Phase 4.0:
   document that the hook reads nace_pending, writes nace_beliefs, calls
   do-process-pending-revisions!, serves the capability-registry (SN network).

---

## 6. Hook insertion checklist (Section 3 of artifact_0)

```
[x] Single function call (do-process-pending-revisions!)
[x] verb-noun! form
[x] No conditional dispatch / raw set-atom! / multi-step logic in the hook
[x] Function defined soul-side (nace_writers.metta), not inline
[x] New file groups one primitive's writers (Discipline 2)
[x] Imported in lib_clarity_reasoning.metta
[x] Insertion named with phase vocabulary (Phase 4.0, after line 75)
[x] References existing landmark (after do-set-last-activity! hook)
[ ] artifact_1 Section 4 updated SAME COMMIT  (do at implementation)
[ ] Dual-write verified: belief atom updated in BOTH atomspace and file SAME CYCLE (do at impl)
[ ] Pending read via read-file, NOT match &self (do at impl)
[ ] Full-file rewrite for beliefs and pending edits (no replace-line) (do at impl)
[ ] Paren count verified before/after  (do at implementation)
[ ] Container rebuild + restart planned  (do at implementation)
[ ] Atom queryability verified  (do at implementation)
[ ] Reverse path tested  (do at implementation)
```

---

## 7. Open questions: RESOLVED (Clarity review)

**Q1 (recorder):** RESOLVED. V1 uses a manual/test writer that drops
`(pending-revision cap outcome)` entries into the pending file. The real
recorder defers to the future registry wiring (Steps 3-4). The hook is
independent of who writes pending entries.

**Q2 (caching):** RESOLVED. The loop caches soul atoms at startup via
initSoulSeeds and does not re-read files each cycle. Therefore dual-write is
required: the hook updates BOTH the in-atomspace belief atom (remove + add) and
the beliefs file. Folded into Section 1E and Section 3.

**Q3 (phase placement):** RESOLVED. Phase 4.0 after line 75 confirmed correct by
Clarity (revision is mechanical bookkeeping, runs before the dispatch gate is
consulted). No alternative preferred.

All three open questions are closed. The spec is ready to implement pending your
final review. The read-mechanism fix (read-file not match), the dual-write, the
full-file-rewrite constraint, and the outcome vocabulary are all folded in.

---

## 7.5 Known v1 boundaries (Clarity, second review)

These are acknowledged limits of v1, not bugs. Named so they are visible, not
invisible. None block v1; all matter when the real recorder arrives.

- **Dual-write is not atomic.** If the atomspace update succeeds but the file
  write fails (or a crash lands between them), the stores diverge: atomspace has
  the revision, file has the stale belief. On restart, initSoulSeeds loads the
  stale file and the revision is silently lost. Acceptable for v1 (container
  file-write failure is rare). Revisit if durability becomes critical (the file
  write could go first, or a write-ahead marker added).
- **Race on the pending file.** If a recorder appends to nace_pending.metta
  while the hook is mid-rewrite (read, process, write-back), an entry appended
  between the read and the write is lost. Fine for the v1 manual/test recorder;
  a structural gap when the real recorder arrives. The existing
  &pending_soul_mutation lock is within-cycle only and does not cover this. A
  real recorder will need a lock or an append-only handoff.
- **File-not-exists.** The hook assumes nace_pending.metta exists (created in
  the implementing commit). If deleted, read-file throws. A defensive
  exists-check or try/catch around the read is a nice-to-have for resilience,
  not a v1 blocker.

Implementation-time verification points (Clarity):
- Confirm do-process-pending-revisions! has access to read-file, write-file,
  remove-atom, add-atom, and the nace_substrate functions in the context where
  nace_writers.metta runs. Expected available (loop loads lib_clarity_reasoning
  which includes the soul files), but verify at implementation.

- **Pending file header (v1 UX):** the initial empty nace_pending.metta should
  carry a header comment naming valid outcomes, as a guardrail against manual
  entry errors: `; Valid outcomes: confirmed, disconfirmed. See nace_substrate
  evidence-stv.` Cheap, helpful.

- **Unknown-cap edge (real-recorder concern, write-side):** if a pending entry
  names a capability with no line in nace_beliefs.metta, the READ side is safe:
  current-efficacy returns the default (stv 0.5 0.0) for an unknown cap (it has
  a default branch), so the revision computes a valid result. The edge is on the
  WRITE side: the dual-write tries to replace the matching cap-efficacy line, and
  there is none. The real recorder needs a defined behavior here: append a new
  belief line for the new cap (treating it as newly-discovered), or reject the
  entry as invalid. For v1 (manual/test recorder writing only known caps) this
  does not arise. Name it for the real-recorder phase: decide append-new vs
  reject before the recorder can emit unknown caps.

---

## 8. What this is NOT

- NOT an external courier (dead: external processes lack lib_nal).
- NOT a run.sh invocation (dead: same reason).
- NOT new LLM reasoning (the loop mechanically processes pending data; the LLM
  is not involved in the revision).
- NOT a state-variable queue (lost on restart; files are the store).

The revision is Truth_Revision in the substrate, driven by the loop reading a
pending file each cycle, writing results to the beliefs file. Cognition in
MeTTa, files for state, the loop as the only thing that can reach lib_nal.
