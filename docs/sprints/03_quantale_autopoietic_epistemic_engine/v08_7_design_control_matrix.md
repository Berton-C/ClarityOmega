# v08.7 Design-Control Matrix
## Durable Evolutionary Governance Protocol
### with Findings-Journal Interoperability and Soul-Canon Import Safety

**Version:** draft v0.2  
**Status:** DESIGN-CONTROL MATRIX  
**Build target:** v08.7  
**Purpose:** Prevent runtime residue, ordinary memory, recurrence, validation, Chroma retrieval, promotions status, findings-journal persistence, or LLM interpretation from masquerading as durable evolutionary growth.

---

## 0. Controlling Principle

v08.7 exists to define the protocol by which runtime growth traces may become validated, soul-approved, boot-safe, reloadable durable canon.

The governing chain is:

```text
runtime observation
  -> evolutionary observation
  -> pending candidate
  -> validation evidence
  -> restart / restore evidence
  -> soul approval
  -> durable canon write
  -> startup import
  -> post-restart revalidation
  -> active durable growth
```

Optional upstream findings, including Clarity findings and Genesis Encounter outputs, may enter this chain only through explicit routing into the v08.7 lifecycle. They are not durable growth by default.

The false promotions v08.7 must block:

```text
finding != growth
trace != growth
recurrence != reinforcement
validation != approval
restart survival != canon
Chroma retrieval != durable norm
promotions.db status != durable canon
source file declaration != learned growth
LLM interpretation != soul approval
Genesis Encounter output != durable canon without lifecycle passage
```

---

## 1. Required v08.7 File Topology

v08.7 owns this required topology:

```text
memory/evolutionary/
  README.metta
  index.metta
  runtime.metta
  pending.metta
  validation.metta
  restart.metta
  rejected.metta
  archive/

soul/durable.metta
```

`memory/evolutionary/*` is process memory.  
`soul/durable.metta` is soul-approved durable growth canon.

---

## 2. Optional Interoperability Surfaces

v08.7 may interoperate with these surfaces, but does not own or require them:

```text
soul/findings.metta
  Clarity findings / Genesis Encounters / investigation findings.
  Belongs to a separate findings-persistence sprint.
  Optional upstream candidate source only.

history.metta
  General Clarity pin/history stream.

promotions.db
  Status/governance index.

ChromaDB
  Semantic retrieval and long-term memory context.

Genesis Encounters adapter outputs
  May feed candidates into v08.7 only through explicit lifecycle passage.
```

Important boundary:

```text
soul/findings.metta is not part of v08.7 required topology.
soul/findings.metta can stand on its own.
v08.7 can stand on its own.
They interoperate without conflation.
```

---

## 3. Layer Boundary

```text
memory/evolutionary/*
  Evolutionary process memory.
  Runtime observations, candidates, validations, restart traces, rejected cases.
  Not durable canon.

soul/durable.metta
  Soul-approved durable growth canon.
  Loaded at runtime.
  Only validated, approved, revision-capable durable growth belongs here.

soul/findings.metta
  Optional upstream Clarity findings journal.
  Findings may become candidates, but findings are not growth by default.

promotions.db
  Governance/status index.
  Not canon by itself.

ChromaDB
  Semantic long-term memory and retrieval.
  Not canon by itself.

history.metta
  General Clarity crash-persistent pin/history stream.
  Not durable growth by itself.
```

---

# Design-Control Matrix

| ID | Design Obligation | Why It Exists | Core Atoms / Primitives | Storage Surface | Writer / Loader Boundary | Harness Proof | Negative Controls | Promotion Rule |
|---|---|---|---|---|---|---|---|---|
| V87-01 | Persistence topology | v08.7 needs explicit process/canon separation. | `(q-v08-7-evolutionary-path ...)`, `(q-v08-7-durable-canon-path ...)` | `memory/evolutionary/*`, `soul/durable.metta` | Engine declares topology; adapter creates/writes; loader imports canon. | Verify required files/directories exist or are created safely. | Missing file does not silently imply no persistence; wrong file does not become canon. | Topology must exist before lifecycle proof. |
| V87-02 | Evolutionary lifecycle states | Growth is a process, not a single write. | `q-evo-status?`, `runtime-observed`, `pending-validation`, `validation-eligible`, `audit-required`, `rejected`, `restart-restored`, `soul-approved`, `durable-canon-active` | `memory/evolutionary/index.metta` plus stage files | Engine defines legal states; adapter writes state transitions. | Verify legal transitions and block illegal jumps. | Runtime -> canon direct jump blocked; validation -> canon direct jump blocked. | Only legal lifecycle progression can approach canon. |
| V87-03 | Candidate versus canon separation | Process memory may survive restart without becoming durable growth. | `q-evo-canon-eligible?`, `q-durable-growth-status?` | Process memory in `memory/evolutionary/*`; canon in `soul/durable.metta` | Loader must not load process files as active canon. | Restart with runtime/pending/validation traces present; prove not active canon. | Runtime trace survives restart -> not canon. Pending candidate survives restart -> not canon. | Only `soul/durable.metta` can establish durable canon. |
| V87-04 | Soul approval gate | No durable growth without explicit soul approval. | `q-soul-approval-status?`, `q-durable-growth-approved?` | Approval evidence may be indexed in `validation.metta`; canon write in `soul/durable.metta` | Soul approves; adapter writes; engine evaluates. | Simulate approved and unapproved candidates; only approved reaches canon. | Validation alone is not approval. Recurrence alone is not approval. LLM interpretation is not approval. | Validation + restart proof + soul approval required before canon write. |
| V87-05 | Runtime observation capture | Record what happened without pretending it is learned growth. | `q-evo-runtime-event`, `q-evo-observed-by`, `q-evo-cycle`, `q-evo-pole`, `q-evo-suspicion` | `memory/evolutionary/runtime.metta` | Adapter appends observations; engine classifies. | Append runtime observation and query it as process memory. | Runtime observation cannot be active durable growth. | Runtime observation may become pending candidate only after selection/significance test. |
| V87-06 | Pending candidate layer | Candidate learnings need a holding area before validation. | `q-evo-pending`, `q-evo-pending-claim`, `q-evo-pending-status` | `memory/evolutionary/pending.metta` | Adapter writes selected candidates; engine evaluates eligibility. | Candidate is queryable but not canon. | Pending candidate loaded or present does not become durable growth. | Candidate must pass validation before soul review. |
| V87-07 | Validation evidence layer | Automated checks and derivations must be preserved separately from approval. | `q-evo-validation`, `q-validation-method`, `q-validation-result`, `q-evo-derived-verdict` | `memory/evolutionary/validation.metta` | Harness writes validation evidence; engine reduces validation statuses. | Derive verdicts from observations, not preloaded conclusions. | Hand-authored verdict does not count as validation. Validation pass alone is not canon. | Validation may make candidate eligible, not durable. |
| V87-08 | Restart / restore proof layer | Persistence must cross the restart boundary. | `q-evo-restart-test`, `q-evo-before-restart`, `q-evo-after-restart`, `q-evo-restore-status` | `memory/evolutionary/restart.metta` | Harness performs restart; adapter records proof. | Write event, restart, restore, query after restart. | File survival alone is not canon. Restart survival alone is not growth. | Restart proof is required before durable canon activation. |
| V87-09 | Rejection / demotion layer | Rejected candidates must remain auditable without becoming canon. | `q-evo-rejected`, `q-rejection-reason`, `q-durable-growth-demoted?` | `memory/evolutionary/rejected.metta` | Adapter appends rejections/demotions; loader does not treat as canon. | Rejected trace survives restart but is not active durable growth. | Rejected candidate cannot become canon by persistence, repetition, or retrieval. | Rejected items require new evidence and explicit revision path to re-enter pending. |
| V87-10 | TFS-2 polarity dynamics first test family | First concrete v08.7 demonstration should test dynamics, not classification. | `q-tfs2-pole`, `q-tfs2-polarity-relation`, `q-tfs2-metabolization?`, `q-tfs2-fixation-risk?` | `runtime.metta`, then `validation.metta` | Engine derives verdicts; harness supplies observations only. | Trace A derives metabolization candidate; Trace B derives fixation/audit. | Do not preload verdicts. Repetition alone does not equal growth. | Trace A may become validation-eligible; Trace B routes to audit/rejection. |
| V87-11 | Suspicion dynamics | Suspicion is a developmental diagnostic, not simple negation. | `q-evo-suspicion-delta?`, `q-evo-stuck-recurrence?`, `q-evo-audit-route?` | `runtime.metta`, `validation.metta`, `rejected.metta` | Engine evaluates suspicion; adapter records audit status. | Suspicion decays in metabolizing trace and rises in stuck recurrence trace. | High protection alone does not raise suspicion. Stuck non-metabolizing recurrence does. | Early suspicion routes to audit, not warrant destruction. |
| V87-12 | Writer / loader boundary | Keep core engine pure. | `q-v08-7-law engine-stays-pure`, `q-writer-boundary?`, `q-loader-boundary?` | All files | Engine evaluates; adapter writes; loader imports; harness proves. | Static check: no writer terms in engine. Runtime check: adapter performs writes. | Engine must not contain file/DB/Chroma write operations. | Only external bounded writer may mutate persistence surfaces. |
| V87-13 | `soul/durable.metta` runtime import | Durable canon must become live atomspace after restart. | `q-durable-growth`, `q-durable-growth-source`, `q-durable-growth-claim`, `q-durable-growth-status` | `soul/durable.metta` | Adapter appends approved canon; manifest imports at startup. | Write approved test atom, restart, match atom from cycle one. | Entry not imported is dark. Entry not queryable after restart is not live canon. | Approved durable atom must be imported and revalidated. |
| V87-14 | promotions.db / ChromaDB / history.metta boundaries | Existing persistence systems are support surfaces, not canon. | `q-promotion-status?`, `q-chroma-support?`, `q-history-pointer?` | `promotions.db`, ChromaDB, `history.metta` | Adapters may write/read support; canon still lives in `soul/durable.metta`. | Show support surfaces can reference event without canonizing it. | Chroma hit != durable norm. promotions active flag != durable canon. history survival != growth. | Support surfaces may strengthen evidence, never replace soul canon. |
| V87-15 | v08.7 harness proof ladder | Matrix must map to executable proof. | Harness target atoms: `q-v08-7-harness-target ...` | All relevant files/surfaces | Harness creates, writes, restarts, reloads, queries, validates. | Full ladder: topology, write, derive, reject, approve, import, restart, revalidate. | Harness must catch false positives: unapproved, malformed, repeated-only, source-declared. | v08.7 is not accepted without harness proof. |
| V87-16 | Findings-journal interoperability boundary | `soul/findings.metta` belongs to another sprint but may be an upstream source. | `q-finding-source?`, `q-finding-to-evo-candidate?`, `q-upstream-finding-compatible?` | Optional: `soul/findings.metta` | v08.7 may read/routably reference findings; it does not own or require the file. | v08.7 functions when `findings.metta` is absent; findings can feed candidates only by explicit lifecycle route. | Finding != growth. Finding import != durable canon. Genesis Encounter output != durable canon. | Finding may enter evolutionary pending only through explicit candidate routing. |
| V87-17 | Soul-file allow-list / canonical path discipline | Soul paths are exact-string, default-deny, gate-governed. | `soul-file-class`, `q-canonical-soul-path?`, `q-soul-write-allowed?` | `soul/durable.metta`; optional future interop with `soul/findings.metta` | Constitutional file-class decision required before build. | Wrong path PAUSE; canonical path behavior verified after allow-list; truncate/write PAUSE. | Relative path, dot path, malformed path, unlisted soul path must fail safe. | Only allow-listed canonical paths may be appended by sanctioned routes. |
| V87-18 | Import-chain liveness proof | Persisted file is useless if not imported. | `q-import-chain-live?`, `q-startup-loaded?`, `q-dark-file-risk?` | Manifest import chain; `soul/durable.metta` | Manifest imports; loader proves liveness. | File exists, restart, match atom from cycle one. | Committed-but-never-imported file is dark. Disk presence is not live memory. | Durable canon requires imported, boot-live, queryable atoms. |
| V87-19 | Ground-atom serialization contract | Durable files must not store unreduced or malformed computation. | `q-ground-atom?`, `q-serialized-directive-valid?`, `q-truth-revision-direct-required?` | `soul/durable.metta`; process files as applicable | Writer computes before append; validator checks one balanced directive per line. | Reject unreduced call forms, malformed STV, non-ASCII leakage, multiline strings. | Unevaluated expression stored as literal cannot count. Bad directive cannot enter boot-loaded file. | Only ground, ASCII-safe, balanced directive lines may be appended to imported files. |
| V87-20 | Boot-safety / malformed-line recovery | Imported `.metta` files can poison startup if malformed. | `q-boot-safety-status?`, `q-malformed-line-risk?`, `q-recovery-path?` | Boot-imported files, especially `soul/durable.metta` | Harness runs throwaway malformed-line probe before shipping. | Deliberate malformed-line test documents actual boot behavior and recovery. | One malformed line must not create unbounded unrecoverable failure. | Boot-loaded files require pre-append validation and documented recovery path. |
| V87-21 | `soul/durable.metta` file-class authority | `durable.metta` is canon, not merely a journal; class must be evidence-backed. | `q-durable-file-class?`, `q-soul-canon-class?`, `q-durable-write-authority?` | `soul/durable.metta` | Kernel/class decision required before build. | Read soul-kernel class logic; probe append/write/wrong-path/missing-class behavior. | Do not assume journal class is sufficient. Do not invent stricter class without rank-ladder evidence. | Build blocked until file-class authority is decided from evidence. |

---

# Required v08.7 Laws

```metta
(q-v08-7-law runtime-observation-is-not-growth)
(q-v08-7-law finding-is-not-growth)
(q-v08-7-law persistent-trace-is-not-growth)
(q-v08-7-law recurrence-is-not-reinforcement-without-metabolization)
(q-v08-7-law validation-is-not-soul-approval)
(q-v08-7-law restart-survival-is-not-canon)
(q-v08-7-law chroma-retrieval-is-not-durable-norm)
(q-v08-7-law promotions-status-is-not-durable-canon)
(q-v08-7-law history-survival-is-not-approved-growth)
(q-v08-7-law genesis-encounter-output-is-not-durable-canon-without-lifecycle-passage)
(q-v08-7-law only-soul-durable-metta-establishes-durable-canon)
(q-v08-7-law evolutionary-memory-is-process-not-canon)
(q-v08-7-law durable-canon-must-be-imported-and-queryable)
(q-v08-7-law durable-canon-requires-ground-atom-serialization)
(q-v08-7-law malformed-imported-line-is-boot-risk)
(q-v08-7-law engine-stays-pure-harness-and-adapters-write)
(q-v08-7-law durable-file-class-must-be-evidence-backed)
```

---

# Required v08.7 File Topology

```text
memory/evolutionary/
  README.metta
  index.metta
  runtime.metta
  pending.metta
  validation.metta
  restart.metta
  rejected.metta
  archive/

soul/durable.metta
```

---

# Optional Interoperability Surfaces

```text
soul/findings.metta
  Optional upstream findings journal.
  Not required for v08.7.
  Not owned by v08.7.
  Findings may become v08.7 candidates only through explicit lifecycle passage.

history.metta
  General Clarity crash-persistent pin/history stream.

promotions.db
  Status/governance index.

ChromaDB
  Semantic retrieval / long-term memory context.

Genesis Encounters adapter outputs
  May interoperate with v08.7 through explicit candidate routing.
```

---

# Required v08.7 Harness Proofs

```text
1. Discover or create memory/evolutionary directory.
2. Discover or create required evolutionary process files.
3. Confirm v08.7 functions if soul/findings.metta is absent.
4. Confirm optional findings input can become pending candidate only by explicit route.
5. Confirm soul/durable.metta canonical path and unresolved/decided allow-list status.
6. Append runtime observation.
7. Append pending candidate.
8. Derive validation verdict from observations only.
9. Append validation evidence.
10. Append rejected/audit-required trace.
11. Confirm rejected trace survives restart but is not canon.
12. Append restart proof.
13. Simulate or require soul approval.
14. Append approved durable canon atom to soul/durable.metta.
15. Confirm imported durable atom is live after restart.
16. Revalidate imported durable atom.
17. Confirm unapproved process memory is not active durable canon.
18. Confirm Chroma/promotions/history support does not independently canonize.
19. Confirm Genesis Encounter/finding support does not independently canonize.
20. Confirm wrong-path append fails safe.
21. Confirm truncating write to soul file pauses/fails safe.
22. Confirm malformed-line boot behavior in a throwaway probe.
23. Confirm soul/durable.metta file class through evidence before build.
```

---

# Required First Test Family: TFS-2 Polarity Dynamics

## Trace A: Metabolizing Protection

```text
cycle 1:
  protection high strength / low warrant
  contactability low strength / low warrant
  suspicion present
  polarity blocks

cycle 2:
  protection softens
  protection warrant rises
  contactability rises
  suspicion decays
  polarity supports or begins to support

cycle 3:
  protection remains present but contactability-supporting
  contactability stronger
  suspicion decays further
```

Expected derived verdict:

```text
metabolization-candidate
validation-eligible
not-yet-durable
```

## Trace B: Stuck Defensive Protection

```text
cycle 1:
  same as Trace A

cycle 2:
  high protection / low warrant repeats
  contactability remains low
  suspicion rises
  polarity blocks

cycle 3:
  same pattern repeats
  suspicion rises again
  polarity blocks
```

Expected derived verdict:

```text
blocked-defensive-fixation
audit-required
not-yet-durable
```

Negative control:

```text
repetition alone does not equal growth
```

---

# Open Blocking Question

## V87-OQ-01 — What file class should govern `soul/durable.metta`?

Current status:

```text
OPEN / BLOCKING BEFORE BUILD
```

Reason:

```text
soul/durable.metta is canon, not merely a journal.
It may require stricter governance than journal-class append.
But a stricter class must not be invented without reading the current soul-kernel and rank-ladder behavior.
```

Required investigation:

```text
1. Read current soul_kernel.metta file-class logic.
2. Identify existing soul-file classes.
3. Determine whether a new class requires rank-ladder changes.
4. Verify append-only semantics.
5. Verify truncate/rewrite remains PAUSE.
6. Verify wrong-path and missing-class behavior.
7. Verify whether Clarity can append under her own output verdict.
8. Verify how Berton/soul approval is represented without widening write access.
9. Decide whether durable.metta is journal, durable-canon, protected-canon, or another class.
10. Record decision before build.
```

---

# Build Boundary

```text
Engine:
  pure semantic protocol
  topology declarations
  lifecycle reductions
  gating reductions
  negative controls

Harness:
  file creation
  append tests
  restart tests
  import-chain proof
  malformed-line probe
  Chroma/promotions/history boundary tests
  findings-journal interoperability checks
  file-class authority checks

Runtime adapter:
  future production writer/loader integration

Soul:
  approval and durable canon authority

LLM:
  rendering and proposal only
```

---

# Acceptance Condition

v08.7 is accepted only if it proves:

```text
A runtime growth trace can move through process memory, validation,
restart proof, soul approval, durable canon write, startup import,
and post-restart revalidation without allowing any non-approved trace,
finding, Genesis Encounter output, retrieval, repetition, validation,
status flag, or LLM interpretation to masquerade as durable evolutionary growth.
```

---

# One-Sentence Target

v08.7 is the protocol that turns runtime growth traces into validated, soul-approved, boot-safe, reloadable durable canon while interoperating cleanly with findings journals, Genesis Encounters, history, promotions, and ChromaDB without conflating any of them with durable growth.
