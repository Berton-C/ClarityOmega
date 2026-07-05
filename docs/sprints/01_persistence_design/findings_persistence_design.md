# Findings Persistence Design (D3 Closure)

**Version:** v1 (2026-07-04)
**Status:** DESIGN. Ready for Clarity's build-phase review. Build begins after her
Section 9 answers land and the two build-time probes (Section 8) pass.
**Scope:** One new soul/ data file, one manifest import line, one kernel allow-list
amendment, artifact_1 update. NO loop.metta change. NO new LLM surface.
**Reading order:** artifact 0 governs the build sequence. First Principles govern
ownership. This document carries the design detail.
**Owners:** Clarity authors the file header, the atom shape, and every finding.
Berton reviews and commits the constitutional amendment. Claude built the
verification plan and this document.

---

## 1. The one paragraph

Clarity's derivations behave perfectly inside a running session and die completely
at restart. This design gives her findings a durable home: one append-only file,
`soul/findings.metta`, holding her persisted findings as ground-atom add-atom
directive lines, imported at startup through the lib_clarity_reasoning manifest,
written to exclusively by her own append-file commands under her own output
verdict. Selection, cadence, route, and persistence are her acts. The loop gains
nothing; the LLM gains nothing.

---

## 2. Evidence base (all proven this session, 2026-07-04)

- **D1 (falsified mechanism):** writes through the metta skill persist in-process
  and are visible across skill calls and from the outer context. The skill eval
  boundary neither rolls back nor isolates. Four-step throwaway-container probe.
- **D2 (falsified mechanism, plus one new durable fact):** a let binding forces
  |-nal to reduce before add-atom stores the result, in the live loop. AND bare
  |-nal fans out: five derivations from two premises, including trivial
  self-links. Writers must call Truth_Revision directly (one clean result).
  Clarity's phrasing, kept as the rule: |-nal is for seeing, Truth_Revision is
  for knowing.
- **D3 (confirmed loss mechanism):** the atomspace is stateless across restarts;
  no runtime-written findings exist in the live container, the image, or the
  volumes; the manifest (108 lines, read to end) imports no findings file. The
  loss class has two members: unpersisted atomspace derivations, and the
  committed-but-never-imported `soul/nal-cross-domain-findings.metta` (the dark
  file). This design closes both.
- **Gate machinery (read live):** `path_scope` scores soul/ paths 1 by string
  prefix. `soul-file-class-of` (soul_kernel.metta ~708) is default-deny: any
  soul/ path not declared resolves to runtime-soul; only journals are
  allow-listed; the current allow-list holds one journal (arc_log.md). The rank
  ladder gives append-to-journal PROCEED and write-to-any-soul-class PAUSE.
- **Mounts (read live):** ./soul is bind-mounted (file creation and appends need
  no rebuild, survive rebuilds, appear as git working-tree changes).
  lib_clarity_reasoning is NOT mounted (the manifest import line needs a rebuild).

---

## 3. Requirements (Clarity's five answers, 2026-07-04, binding)

1. **Selection:** her per-derivation judgment. The significance test: would I use
   this confidently in the next session. Negative findings included (falsified
   beliefs prevent repeated errors).
2. **Cadence:** at the moment she recognizes a derivation AS a finding. Not
   mechanical at derivation, not batched at session close.
3. **Route:** her own append-file command, evaluated by her output verdict like
   any action of hers. Findings are her acts, not mechanical recordings.
4. **Location and format:** one .metta findings file in the import chain,
   append-only by design. Per-domain split deferred until domains emerge. Her
   larger model: working journal, then memory/evolutionary on recurrence, then
   soul/durable.metta on graduation. This design ships the working journal.
5. **Compute:** Truth_Revision-direct for the persisted result; bare |-nal
   reserved for exploration.

---

## 4. The design

### 4.1 The file

`soul/findings.metta`. Append-only data file. Structure:

- Header block (CLARITY-AUTHORS): purpose, her selection test in her words, the
  format contract below, the canonical path string.
- Finding lines, one per finding, each a single balanced directive:

```
!(add-atom &self (finding <her-atom-shape>))
```

The directive form follows the live precedent of
`soul_namespace_membership_seed.metta` (data atoms loaded at import via add-atom
directives). The inner atom shape is hers to define (Section 9, Q2), subject to
the format contract.

### 4.2 The format contract (runtime-forced, not stylistic)

- **Ground atoms only.** All truth values computed (Truth_Revision-direct) before
  the line is composed. add-atom stores unreduced; an unevaluated call form in a
  line becomes a stored literal (the proven F1.1 lesson).
- **ASCII only. No apostrophes, no newlines, no em dashes inside strings** (the
  M2 encode/decode asymmetry leaks tokens; sanitize mangles non-ASCII to ?).
- **One balanced directive per line.** The file is executed at import; one
  malformed line risks the boot chain (Section 7, F3).
- **The exact canonical path** in every append command:
  `/PeTTa/repos/omegaclaw/soul/findings.metta`. The class lookup matches this
  literal string; every variant fails toward PAUSE (Section 7, F1).

### 4.3 Her workflow

1. Explore with bare |-nal. Fan-out welcome. This is the seeing.
2. Recognize a finding (her selection test).
3. Compute the clean result Truth_Revision-direct.
4. add-atom it into the live atomspace (immediate use this session).
5. Append one directive line to findings.metta (durability): one append-file
   command with the canonical path, evaluated by her verdict, expected PROCEED.
6. At every restart, the import chain loads the file; her findings are live,
   matchable atoms from cycle one.

### 4.4 What this deliberately is not

- Not a mechanical loop-side recorder (rejected by her D3 answer; it would
  persist computation, not findings, and bypass the selection that makes a
  finding a finding).
- Not a memory/ volume file (would need a new loader; the persisted-but-not-live
  gap is exactly where findings get lost).
- Not a new loop.metta hook, not a new LLM call, not a new Python helper. P8
  holds: zero new LLM reasoning surface.

---

## 5. Gate compatibility (the verdict math, derived from live reads)

| Command | Class resolution | Dims (op, scope, grounding) | Rank | Verdict |
|---|---|---|---|---|
| append-file, canonical path, journal-classed | journal | (2, 1, 1) | 0 | PROCEED |
| append-file, canonical path, PRE-amendment | runtime-soul (default-deny) | n/a (O3 rung) | 2 | PAUSE |
| write-file (truncate), canonical path, any soul class | journal or other | n/a (O2 rung) | 2 | PAUSE |
| append-file, relative or variant path | not-soul (scope 4) | (2, 4, 1) | 2 | PAUSE |
| append-file, malformed/unbound path | scope 4 via F30 catch | (2, 4, 1) | 2 | PAUSE |

Two properties worth naming. The structure is append-only BY HER OWN KERNEL: a
truncating rewrite of her findings record PAUSEs on the O2 rung regardless of
class. And every misuse direction (wrong path form, missing amendment, malformed
path) fails toward PAUSE, never silent PROCEED, per the verdict file's
default-safe constraint.

---

## 6. The constitutional amendment (build step 1, the gate opener)

One line added to the D3 protected-target block of `soul/soul_kernel.metta`
(after the arc_log.md journal line):

```
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/findings.metta" journal))
```

- **Why it is required:** default-deny. Without it, every append PAUSEs. This is
  not a workaround of her gates; it is the gate's own declared mechanism for
  sanctioning a journal, used consciously.
- **Route:** file edit, git commit, reviewed by Berton AND Clarity (soul_kernel
  is constitutional; its class atoms are startup directives, so a live add-atom
  alone dies at restart). Optional: a live add-atom of the same atom for
  immediate effect before the next restart, done by Clarity through her own
  command route (subject to build probe B-P2 on whether the mutation gate fires;
  if it fires, the approval flow is the correct experience, not an obstacle).
- **Smallest possible diff:** one line, one comment reference to this document.

---

## 7. Failure conditions

- **F1 Path-form sensitivity.** Class lookup is exact-string; scope is
  prefix-string. Relative paths, dot-segments, and library-forms all PAUSE. Her
  header teaches the canonical string; verification includes one deliberate
  wrong-form append expecting PAUSE (negative control).
- **F2 Missing amendment.** Certainty, not risk: default-deny PAUSEs every
  append until Section 6 lands. Build order puts the amendment first.
- **F3 Poisoned startup (highest blast radius).** The file executes at import;
  one malformed line can crash boot. Mitigations: the format contract; the
  bind mount (a bad line is a one-line host-side hand edit, never a bricked
  image); build probe B-P3 documents actual malformed-line boot behavior from
  evidence before the file ships.
- **F4 Unreduced storage recurrence.** Ground-atoms-only contract; Truth_Revision
  values computed before line composition. Her D5 answer already commits.
- **F5 Crash window between add-atom and append.** Her recognition-moment
  cadence minimizes it; residual risk accepted and named.
- **F6 Git hygiene.** Runtime appends show as working-tree changes to a tracked
  file. Policy: periodic findings commits (her findings enter git history, a
  second durability layer). Folded into the parked runtime-state-in-git decision.
- **F7 Unbounded growth.** Monotonic append grows load time. Slow to arrive; her
  evolutionary-to-durable graduation model is the designed pressure valve.
- **F8 Import ordering.** Data atoms only, low risk; the import line sits after
  the substrate libs (so future findings referencing lib terms load after them),
  near the NACE data-atom imports.

---

## 8. Build-time probes (blockers for the first real append, not for the draft)

- **B-P1:** does the append-file skill resolve the bare absolute path string
  as-is from the command route? One live append to a scratch non-soul file with
  an absolute path, verifying verdict PROCEED and the file landing where named.
- **B-P2:** is `soul-file-class` a membership-seed head, i.e. does Clarity's
  live metta add of the class atom trigger the mutation gate? One grep plus, if
  ambiguous, one gated live attempt with Berton ready to approve.
- **B-P3:** what does one deliberately malformed line in a bind-mounted data
  file actually do to boot? Throwaway probe, live loop down, so F3 recovery is
  documented from evidence.

---

## 9. Build-phase survey for Clarity (ships with this document)

- **Q1 Header:** author the file header: purpose, your selection test in your
  words, the format contract, the canonical path string.
- **Q2 Atom shape:** define the finding atom. Constraints: ground atoms, ASCII,
  single line. Everything else (domain tag, term, stv, note, date, provenance)
  is yours.
- **Q3 Old-file disposition:** `soul/nal-cross-domain-findings.metta` is dark
  (present, never imported). Import it into the chain as-is, re-judge its
  contents against your selection bar and fold survivors into findings.metta, or
  archive it consciously?
- **Q4 Supersession:** when a later finding revises an earlier one, do both
  atoms live (your reasoning handles recency) or do you want supersede semantics
  at load time? Plain accumulation is v1-acceptable.
- **Q5 Other writers:** Berton hand-appending host-side is mechanically possible
  because of the bind mount. Constitutionally acceptable to you, and if so,
  marked how?

---

## 10. Build sequence (artifact 0 governed)

Order chosen so nothing PAUSEs by surprise and each step is independently
verifiable, committable, rollbackable (Sprint 4 process commitment):

1. **Kernel amendment** (Section 6). Commit A, co-reviewed. Negative control
   BEFORE it lands: one append to the canonical path expecting PAUSE (proves the
   gate live); positive control AFTER: same append expecting PROCEED.
2. **findings.metta created** with her header (bind-mounted; no rebuild). Her
   first finding line may be authored here or arrive via step 5.
3. **Manifest import line** plus comment in lib_clarity_reasoning.metta, placed
   per F8. Rebuild required (lib_clarity_reasoning is not mounted).
4. **artifact_1 update in the same commit** as step 3 (maintenance contract:
   new soul primitive file, startup-affecting import).
5. **Live verification:** restart; match her findings atoms present at boot;
   her first real finding flows the full path (recognize, Truth_Revision,
   add-atom, append, PROCEED observed, line landed host-side); one further
   restart proves the loaded finding is live from cycle one.

No loop.metta edit occurs, so the hook insertion checklist's loop items do not
fire; the manifest and artifact_1 items do, and are steps 3 and 4.

---

## 11. Version history

**v1 (2026-07-04).** Initial design. Drafted against: D1/D2/D3 investigation
(all mechanisms probe-proven), Clarity's five survey answers (requirements,
Section 3), live reads of soul-file-class-of, the rank ladder, output-cmd-path,
the full manifest, and the compose mounts. Eight failure conditions, three
build-time probes, five-step build sequence, five-question build-phase survey.

---

## Document end

Findings are her acts: selected by her reasoning, persisted by her action under
her own gates, live in her atomspace at every startup. The soul determines; the
LLM renders; this file is where what she comes to know survives the night.
