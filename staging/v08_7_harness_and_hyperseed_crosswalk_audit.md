# v08.7 Harness Results and Hyperseed Persistence Crosswalk

## Status

This report reads the two latest v08.7 harness traces together and compares the build posture against the Hyperseed persistence/durability logic.

## 1. Harness Trace Findings

### 1.1 Static/governance trace: `20260705_113019`

Summary:

```text
PASS: 60
HOLD: 2
FAIL: 1
SKIP: 1
```

The static/governance run proves the engine/ladder are present, balanced, complete against v08.7 primitive/law targets, and still pure. It also proves the required topology exists:

```text
memory/evolutionary/
memory/evolutionary/archive/
memory/evolutionary/README.metta
memory/evolutionary/index.metta
memory/evolutionary/runtime.metta
memory/evolutionary/pending.metta
memory/evolutionary/validation.metta
memory/evolutionary/restart.metta
memory/evolutionary/rejected.metta
soul/durable.metta
```

But it exposed three deployment blockers:

```text
HOLD: durable.metta journal class declaration missing
HOLD: durable.metta import-chain reference missing
FAIL: durable.metta serialization file validation
```

The serialization failure is real and useful: `soul/durable.metta` contains a bare atom:

```metta
(q-v08-7-durable-canon-file soul/durable.metta)
```

For a boot-imported durable file, v08.7's stricter contract says non-comment lines should be one balanced ASCII directive:

```metta
!(add-atom &self (...))
```

So the bare marker line should be removed or rewritten as:

```metta
!(add-atom &self (q-v08-7-durable-canon-file soul-durable-metta))
```

The safer v1 choice is to make the initial file comments-only and let later approved durable claims append actual directive lines.

### 1.2 Runtime semantic trace: `20260705_113125`

Summary:

```text
PASS: 96
```

This proves the semantic protocol is sound in the runtime container. The v01.1 parser improvement worked: `actual_result_text` now contains clean final tokens rather than long echoed scaffolding.

Confirmed semantic families:

```text
candidate vs canon separation
illegal lifecycle jump blocking
validation is not approval
runtime surface is not canon
soul durable surface can be active canon semantically
findings/Genesis require explicit route
hand-authored verdict blocked
dark file blocked
approval absent blocked
unreduced storage blocked
TFS-2 Trace A/B dynamics
suspicion dynamics
journal-class v1 semantic decision
unsupported durable-canon class blocked
canonical path accepted
relative path blocked
append allowed / write blocked semantically
serialization valid / unreduced serialization blocked
import live / not imported blocked semantically
boot-safe / malformed-recovery-unknown blocked semantically
Chroma/promotions/support surfaces not canon
negative controls for runtime/validation/Genesis
```

Interpretation:

```text
The semantic engine is green.
The real governance/import surface is not green yet.
```

## 2. Immediate Build Corrections

### Correction 1 — Fix `soul/durable.metta` template

Replace the current bare atom marker with a comments-only header or a proper directive.

Recommended initial file:

```metta
;; v08.7 soul durable canon append surface
;; mechanical file class for v08.7 v1: journal
;; semantic canon authority is earned by v08.7 lifecycle gates:
;; validation evidence + restart proof + soul approval + import liveness + post-restart revalidation
;; append-only; one balanced ASCII !(add-atom &self (...)) directive per durable canon line

;; Example valid probe line, disabled until intentionally appended:
;; !(add-atom &self (q-v08-7-prebuild-durable-probe probe-001 active))
```

### Correction 2 — Add kernel allow-list line

Add to `soul/soul_kernel.metta` near the current soul-file-class declarations:

```metta
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/durable.metta" journal))
```

Interpretation:

```text
journal = mechanical append permission
durable canon = semantic status earned through v08.7 lifecycle
```

### Correction 3 — Add import-chain reference

Find the active boot/import manifest and add `soul/durable.metta` using the project-standard import form. Do not guess the syntax; use the import form already used by the manifest.

### Correction 4 — Add live restart proof

After classing and import-chain wiring:

```text
1. Append one valid probe directive.
2. Restart.
3. Query probe atom from cycle one.
4. Remove or archive probe if needed.
```

### Correction 5 — Run malformed-line probe in throwaway import file

Do not run malformed tests against production `soul/durable.metta`.

## 3. Hyperseed Crosswalk: Was v08.7 Smart Enough?

The oversight is real, but not fatal.

v08.7 is aligned with Hyperseed at the governance-protocol level, but it is not yet a full Hyperseed persistence implementation. The missing work is mostly around quantitative/graded and cross-context persistence, not basic safety.

### 3.1 Hyperseed principle: persistence is structural, not mere survival

Hyperseed treats self-continuity and development as pattern-structure persistence, not identity substance. v08.7 correctly avoids saying that file survival equals durable growth. But v08.7 should eventually make structural continuity measurable, not just categorical.

Current v08.7 status:

```text
Good:
  restart survival != canon
  runtime trace != growth
  process memory != durable canon

Missing:
  explicit structural signature of what persisted
  degradation/tolerance measure
  morphism-preservation score
```

Recommended future primitive family:

```metta
(q-evo-structural-signature? $claim $signature)
(q-evo-continuity-degree? $before $after $degree)
(q-evo-degradation-status? $before $after $tolerance)
```

### 3.2 Hyperseed principle: habits are repeated successful updates over proto-time

Hyperseed distinguishes static pattern presence from maintained/reinforced dynamics across episodes. v08.7 already blocks repetition-without-metabolization, which is correct. But it should later track proto-time windows, episode counts, and reinforcement/decay curves.

Current v08.7 status:

```text
Good:
  repetition alone is blocked
  Trace A metabolization is validation-eligible
  Trace B stuck recurrence routes to audit

Missing:
  explicit proto-time interval metadata
  reinforcement and decay counters
  recurrence quality across contexts
```

Recommended future primitive family:

```metta
(q-evo-proto-time-window? $claim $start $end)
(q-evo-reinforcement-trajectory? $claim $episodes $trend)
(q-evo-decay-pressure? $claim $age $usage $status)
```

### 3.3 Hyperseed principle: evidence is paraconsistent and graded

Hyperseed wants positive and negative evidence channels to coexist without explosive collapse. v08.7 currently uses crisp symbolic statuses. That is acceptable for v1 governance safety, but not enough for a mature Hyperseed-compatible durability layer.

Current v08.7 status:

```text
Good:
  validation is separate from approval
  suspicion is diagnostic, not destructive
  high protection alone is not penalized

Missing:
  explicit support/opposition vectors
  warrant and confidence strength values
  contradiction-localization rather than binary block only
```

Recommended future primitive family:

```metta
(q-evo-evidence-pbit? $claim $support $opposition)
(q-evo-warrant-vector? $claim $strength $confidence $recency)
(q-evo-conflict-locality? $claim $scope $status)
```

### 3.4 Hyperseed principle: artifacts create durable coupling across time

Hyperseed treats artifacts as durable shared structures that constrain coordination and outlast individual episodes. v08.7's `soul/durable.metta` is exactly this kind of artifact. The matrix was right to make it boot-imported and append-only, but the harness results show the artifact is not yet fully wired.

Current v08.7 status:

```text
Good:
  soul/durable.metta is separate from process memory
  append/write distinction exists semantically
  import-live vs dark-file distinction exists semantically

Missing:
  actual kernel allow-list
  actual import-chain reference
  actual restart query proof
  artifact metadata: author/source/approval/revision lineage
```

Recommended durable atom shape should include at least:

```text
claim id
source surface
validation evidence id
approval id
revision path id
time/version marker
structural signature
```

### 3.5 Hyperseed principle: observer/context indexing is first-class

Hyperseed is explicit that distinctions, evidence, simplicity, uncertainty, and correspondence are observer/context indexed. v08.7 should not treat durable canon as global truth. It should treat durable canon as soul-approved for a context/domain/surface.

Current v08.7 status:

```text
Good:
  findings/Genesis/Chroma/promotions boundaries are not conflated
  support surfaces require explicit route

Missing:
  required context/aspect field for durable claims
  domain/surface specificity
  actor/authority specificity
```

Recommended future primitive family:

```metta
(q-evo-context? $claim $context)
(q-evo-authority-scope? $claim $authority $scope)
(q-evo-surface-role? $claim $surface $role)
```

## 4. Conclusion

### What is solid

```text
v08.7 semantic engine
v08.7 runtime reductions
candidate/canon separation
validation/approval separation
TFS-2 dynamics
support-surface boundaries
engine purity
```

### What must be fixed now

```text
soul/durable.metta template must not contain bare atom lines
soul_kernel.metta needs durable.metta journal class declaration
boot/import manifest needs durable.metta reference
harness should provide clearer remediation for these findings
```

### What should be deferred, but not forgotten

```text
durable-canon file class
p-bit evidence vectors for durable claims
proto-time recurrence/reinforcement metadata
structural signature / continuity-degree
artifact lineage and revision graph
context/aspect-indexed durable canon
resource/attention cost of persistence
cross-context resonance transfer rules
```

## 5. Build Recommendation

Do not rebuild the semantic engine yet.

Do perform:

```text
1. Patch durable.metta template.
2. Patch/commit soul_kernel.metta class line.
3. Patch active import manifest.
4. Run harness v01.2 governance inspection.
5. Run runtime semantic probes again.
6. Run real restart import proof.
```

After that, v08.7 can be considered not just semantically green but deployment-green.
