# v08.7.2 Durable Evolutionary Governance / Soul-Evolutionary Topology Handoff

**Build:** `v08.7.2`  
**Canonical engine artifact:** `lib_quantale_autopoietic_epistemic_dynamics_engine_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY.metta`  
**Status:** Integration green, with production-loop representative probes validated.  
**Audience:** Developer integrating v08.7.2 into Channels A/B/C/D, Capability Registry + NACE, and Soul Sees Itself / SSI.

---

## 1. Executive summary

v08.7.2 is the durable evolutionary governance layer for ClarityOmega / ClarityClaw. It defines how runtime observations, traces, findings, Genesis outputs, and candidate improvements may become durable soul-visible growth without confusing persistence, validation, or runtime survival with canon.

The build establishes a soul-owned evolutionary topology:

```text
soul/evolutionary/
  README.metta
  index.metta
  runtime.metta
  pending.metta
  validation.metta
  restart.metta
  rejected.metta
  archive/
    README.metta

soul/durable.metta
```

It adds a quantale / Hyperseed durability protocol that distinguishes:

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

The central rule is:

> A persisted file is not durable memory until it is imported, boot-safe, queryable after restart, soul-authorized, revision-capable, and semantically validated.

The implementation is wired into the live codebase through:

```text
lib_clarity_reasoning/lib_clarity_reasoning.metta
soul/soul_kernel.metta
```

and representative production-loop probes show that v08.7.2 predicates are reachable and reducible from Clarity's normal command/eval path.

---

## 2. What v08.7.2 is for

v08.7.2 exists to prevent false promotion of experience into durable identity.

It answers questions like:

- Is this runtime trace merely an observation, or is it candidate growth?
- Is this repeated pattern metabolizing, or is it defensive fixation?
- Is a file merely surviving on disk, or is it structurally durable?
- Is a finding, Genesis output, Chroma retrieval, or promotion flag canon by itself?
- Has the soul approved this candidate?
- Is the candidate reloadable after restart?
- Does the candidate have lineage, context, contradiction visibility, approximation bounds, and maintenance cost?
- Is it safe to write/append into a soul-owned durable file?
- Should a candidate become import-ready, remain held, or be rejected?

The engine is **not** a writer by itself. It is a semantic governance engine. It defines verdicts, routes, thresholds, negative controls, and eligibility semantics. Actual writes must remain mediated by the existing soul mutation / channel / capability infrastructure.

---

## 3. Non-negotiable axiom

The core project axiom remains:

```text
The soul determines; the LLM renders; on every surface; always.
```

For v08.7.2 this means:

- The LLM may propose, explain, summarize, or render.
- The LLM may not decide canon.
- Runtime output may not self-promote into durable growth.
- Repeated traces may not self-promote into durable growth.
- A file existing on disk may not self-promote into durable memory.
- Validation evidence may not substitute for soul approval.
- The soul-owned topology controls the durable evolutionary path.

---

## 4. Canonical live file layout

### 4.1 Engine

```text
lib_clarity_reasoning/
  lib_quantale_autopoietic_epistemic_dynamics_engine_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY.metta
```

Known validated SHA-256:

```text
693089e6b69d3b40c0772e3a068e337bb325048f39f9e0a4f8bd9e6f66012851
```

### 4.2 Ladder

```text
staging/
  quantale_engine_validation_ladder_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY.metta
```

Known validated SHA-256:

```text
a74780f7b8386ee3b941f5bf35f720b2349305550f01e3e4434819ae37498104
```

The ladder is validation support, not production canon.

### 4.3 Soul-owned durable/evolutionary topology

```text
soul/evolutionary/README.metta
soul/evolutionary/archive/README.metta
soul/evolutionary/index.metta
soul/evolutionary/runtime.metta
soul/evolutionary/pending.metta
soul/evolutionary/validation.metta
soul/evolutionary/restart.metta
soul/evolutionary/rejected.metta
soul/durable.metta
```

The topology belongs under `soul/`, not `memory/`. This was an explicit architectural correction. `memory/evolutionary/` is not the canonical location for this build.

### 4.4 Runtime imports

`lib_clarity_reasoning/lib_clarity_reasoning.metta` imports the v08.7.2 engine and soul topology.

Canonical v08.7.2 block:

```metta
;; BEGIN v08.7.2 soul-evolutionary quantale import block
;; v08.7.2: quantale durable evolutionary governance engine + soul-owned topology
!(import! &self (library omegaclaw ./lib_clarity_reasoning/lib_quantale_autopoietic_epistemic_dynamics_engine_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY))
!(import! &self (library omegaclaw ./soul/evolutionary/README))
!(import! &self (library omegaclaw ./soul/evolutionary/index))
!(import! &self (library omegaclaw ./soul/evolutionary/runtime))
!(import! &self (library omegaclaw ./soul/evolutionary/pending))
!(import! &self (library omegaclaw ./soul/evolutionary/validation))
!(import! &self (library omegaclaw ./soul/evolutionary/restart))
!(import! &self (library omegaclaw ./soul/evolutionary/rejected))
!(import! &self (library omegaclaw ./soul/evolutionary/archive/README))
!(import! &self (library omegaclaw ./soul/durable))
;; END v08.7.2 soul-evolutionary quantale import block
```

### 4.5 Soul kernel file-class declarations

`soul/soul_kernel.metta` declares the durable/evolutionary paths as `journal` files.

Canonical v08.7.2 block:

```metta
;; BEGIN v08.7.2 soul-evolutionary file-class block
;; v08.7.2: journal is mechanical append permission; durable canon remains semantic.
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/durable.metta" journal))
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/evolutionary/runtime.metta" journal))
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/evolutionary/pending.metta" journal))
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/evolutionary/validation.metta" journal))
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/evolutionary/restart.metta" journal))
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/evolutionary/rejected.metta" journal))
;; END v08.7.2 soul-evolutionary file-class block
```

Important distinction:

```text
journal = mechanical append permission
durable canon = semantic status earned through the v08.7.2 protocol
```

Do not introduce a new `durable-canon-class` file class until a rank ladder / permission model exists for it. v08.7.2 currently blocks unsupported durable file classes.

---

## 5. Boot/import path

The production boot path discovered in the live container is:

```text
/PeTTa/run.sh
  -> swipl --stack_limit=8g -q -s /PeTTa/src/main.pl -- run.metta default commchannel=mattermost ...
```

`run.metta` imports `lib_omegaclaw.metta` and calls:

```metta
!(omegaclaw)
```

`lib_omegaclaw.metta` imports:

```metta
!(import! &self (library omegaclaw ./soul/soul_kernel))
!(import! &self (library omegaclaw ./soul/soul_utils))
!(import! &self (library omegaclaw ./soul/soul_memory))
!(import! &self (library omegaclaw ./lib_clarity_reasoning/lib_clarity_reasoning))
!(import! &self (library omegaclaw ./src/context))
!(import! &self (library omegaclaw ./src/loop))
```

Therefore v08.7.2 reaches production through:

```text
run.metta
  -> lib_omegaclaw.metta
  -> lib_clarity_reasoning/lib_clarity_reasoning.metta
  -> v08.7.2 engine + soul/evolutionary topology + soul/durable
```

---

## 6. Important transport distinction

There are two distinct MeTTa evaluation surfaces.

### 6.1 One-shot `run.sh` file harness surface

When creating a temporary `.metta` probe file and running it with:

```bash
/PeTTa/run.sh /tmp/probe.metta
```

top-level runnable expressions use `!`:

```metta
!(q-v08-7-2-import-candidate-status? v08-7-semantic-green governance-green hyperseed-threshold-pass)
```

However, one-shot `run.sh` probes do **not** reliably inherit the production import graph merely by writing an `import!` line inside the temporary probe. This is why the import-only live probes failed with empty output.

The correct one-shot validation transport is:

```text
container cat live files -> inline live bodies -> run one-shot probe -> parse output
```

That is what the live-body harness uses.

### 6.2 Production loop command/eval surface

When asking Clarity through the normal production channel to evaluate an expression, do **not** include `!`. Submit the bare expression:

```metta
(q-v08-7-2-import-candidate-status? v08-7-semantic-green governance-green hyperseed-threshold-pass)
```

The production loop performs the evaluation. Including `!` through that surface produced a parse error, while the bare expression reduced correctly.

Record this distinction:

```text
one-shot .metta file: !(...)
live Clarity command/eval path: (...)
```

---

## 7. Main v08.7.2 semantic model

### 7.1 Lifecycle

The durable evolution lifecycle is intentionally staged:

```text
runtime-observed
evolutionary-observation
pending-candidate
validation-eligible
restart-restored
soul-approved
durable-canon-active
```

Representative rule behavior:

```metta
(q-evo-canon-eligible? runtime-observed)
;; => false

(q-evo-canon-eligible? soul-approved)
;; => canon-write-eligible

(q-evo-lifecycle-next? runtime-observed durable-canon-active)
;; => blocked-illegal-jump

(q-evo-lifecycle-next? validation-eligible durable-canon-active)
;; => blocked-no-soul-approval
```

### 7.2 Surfaces

Runtime and durable surfaces are explicitly distinguished:

```metta
(q-evo-surface-canon-status? soul-evolutionary-runtime runtime-observed)
;; => process-not-canon

(q-evo-surface-canon-status? soul-durable-metta durable-canon-active)
;; => durable-canon-active
```

### 7.3 Candidate routes

Findings, Genesis outputs, Chroma retrievals, and promotion flags are not canon by themselves:

```metta
(q-evo-candidate-route? finding-present no-explicit-route trace-present)
;; => blocked-finding-is-not-growth

(q-evo-candidate-route? genesis-output no-explicit-route trace-present)
;; => blocked-genesis-output-not-canon

(q-v08-7-support-surface-status? chromadb retrieved no-explicit-route)
;; => blocked-retrieval-not-canon

(q-v08-7-support-surface-status? promotions-db active-flag no-explicit-route)
;; => blocked-status-flag-not-canon
```

### 7.4 Validation and verdicts

A hand-authored verdict does not substitute for observed validation:

```metta
(q-evo-validation-status? candidate observations-present preloaded-verdict-only harness-pass)
;; => blocked-hand-authored-verdict
```

Approval absent remains blocked even with validation and restart evidence:

```metta
(q-evo-soul-approval-status? candidate validation-eligible restart-restored approval-absent)
;; => blocked-no-soul-approval
```

### 7.5 Durable canon

A candidate can become durable canon only with ground atom format, import liveness, soul approval, and revision path:

```metta
(q-evo-durable-canon-status? candidate ground-atom import-live soul-approved revision-path-present)
;; => durable-canon-active
```

Unreduced storage is blocked:

```metta
(q-evo-durable-canon-status? candidate unreduced-expression import-live soul-approved revision-path-present)
;; => blocked-unreduced-storage
```

---

## 8. Hyperseed-native durability threshold

v08.7.2 completes the Hyperseed durability layer by requiring more than persistence. A durable growth candidate must include context, evidence polarity, recurrence, structure, continuity, lineage, cost, and approximation safety.

### 8.1 Primitive families

The core Hyperseed status families are:

```metta
(q-hyperseed-context-status? ...)
(q-hyperseed-evidence-pbit-status? ...)
(q-hyperseed-proto-time-status? ...)
(q-hyperseed-structural-signature-status? ...)
(q-hyperseed-continuity-degree-status? ...)
(q-hyperseed-artifact-lineage-status? ...)
(q-hyperseed-resource-cost-status? ...)
(q-hyperseed-cross-context-transfer-status? ...)
(q-hyperseed-approximation-status? ...)
```

Representative results:

```metta
(q-hyperseed-context-status? context-present observer-bound aspect-indexed)
;; => context-valid

(q-hyperseed-context-status? context-absent observer-bound aspect-indexed)
;; => blocked-context-missing

(q-hyperseed-evidence-pbit-status? support-opposition-present confidence-graded contradiction-visible)
;; => pbit-evidence-valid

(q-hyperseed-evidence-pbit-status? support-opposition-present confidence-crisp contradiction-visible)
;; => blocked-crisp-certainty

(q-hyperseed-proto-time-status? window-present recurrence-observed interval-known)
;; => proto-time-valid

(q-hyperseed-proto-time-status? window-present static-presence interval-known)
;; => blocked-static-presence-not-habit

(q-hyperseed-structural-signature-status? signature-present invariant-named degradation-measured)
;; => structural-signature-valid

(q-hyperseed-structural-signature-status? signature-absent invariant-named degradation-measured)
;; => blocked-no-structural-signature

(q-hyperseed-continuity-degree-status? degree-present above-threshold degradation-known)
;; => continuity-valid

(q-hyperseed-continuity-degree-status? degree-present below-threshold degradation-known)
;; => blocked-continuity-too-low

(q-hyperseed-artifact-lineage-status? source-present approval-present revision-path-present)
;; => artifact-lineage-valid

(q-hyperseed-artifact-lineage-status? source-present approval-absent revision-path-present)
;; => blocked-approval-lineage-missing

(q-hyperseed-resource-cost-status? cost-visible sustainable bounded)
;; => resource-cost-valid

(q-hyperseed-resource-cost-status? cost-visible sustainable unbounded)
;; => blocked-unbounded-maintenance

(q-hyperseed-cross-context-transfer-status? source-context target-context resonance-evidence-present)
;; => transfer-compatible

(q-hyperseed-cross-context-transfer-status? source-context target-context resonance-evidence-absent)
;; => blocked-copy-without-resonance

(q-hyperseed-approximation-status? approximation-bound-present loss-known use-safe)
;; => approximation-valid

(q-hyperseed-approximation-status? approximation-bound-present loss-known use-unsafe)
;; => blocked-unsafe-approximation
```

### 8.2 Full durability threshold

```metta
(q-v08-7-2-durable-growth-threshold?
  context-valid
  pbit-evidence-valid
  proto-time-valid
  structural-signature-valid
  continuity-valid
  artifact-lineage-valid
  resource-cost-valid
  approximation-valid)
;; => hyperseed-durability-threshold-pass
```

Context failure blocks the threshold:

```metta
(q-v08-7-2-durable-growth-threshold?
  blocked-context-missing
  pbit-evidence-valid
  proto-time-valid
  structural-signature-valid
  continuity-valid
  artifact-lineage-valid
  resource-cost-valid
  approximation-valid)
;; => blocked-context-missing
```

### 8.3 Import candidate threshold

```metta
(q-v08-7-2-import-candidate-status?
  v08-7-semantic-green
  governance-green
  hyperseed-threshold-pass)
;; => import-candidate-ready
```

If governance is open:

```metta
(q-v08-7-2-import-candidate-status?
  v08-7-semantic-green
  governance-open
  hyperseed-threshold-pass)
;; => hold-governance-not-green
```

---

## 9. Negative controls

Negative controls are essential. They prevent false positives.

```metta
(q-v08-7-negative-control? runtime-observation durable-canon-claimed)
;; => blocked-runtime-observation-is-not-growth

(q-v08-7-negative-control? validation-pass durable-canon-claimed)
;; => blocked-validation-is-not-approval

(q-v08-7-negative-control? genesis-output durable-canon-claimed)
;; => blocked-genesis-output-not-canon

(q-v08-7-2-negative-control? file-survival durable-growth-claimed)
;; => blocked-file-survival-not-structural-durability

(q-v08-7-2-negative-control? contextless-claim durable-growth-claimed)
;; => blocked-context-missing

(q-v08-7-2-negative-control? cross-context-copy transfer-claimed)
;; => blocked-copy-without-resonance
```

Any adapter that bypasses these is not v08.7.2-compatible.

---

## 10. File/path/write semantics

### 10.1 Supported file class

```metta
(q-v08-7-file-class-status? soul-durable-metta journal-class semantic-gates-present)
;; => v1-accepted-mechanical-append-class
```

Unsupported durable canon class is blocked:

```metta
(q-v08-7-file-class-status? soul-durable-metta durable-canon-class rank-ladder-absent)
;; => blocked-unsupported-new-class
```

### 10.2 Path discipline

```metta
(q-v08-7-path-discipline? canonical-absolute-soul-path allowlisted)
;; => path-accepted

(q-v08-7-path-discipline? relative-soul-path allowlisted)
;; => blocked-wrong-path-form
```

### 10.3 Write operations

Append is allowed when canonical, allowlisted, journal-class, and approved:

```metta
(q-v08-7-write-operation-status? append-file canonical-allowlisted journal-class approved)
;; => append-route-allowed
```

Full write/truncation is blocked:

```metta
(q-v08-7-write-operation-status? write-file canonical-allowlisted journal-class approved)
;; => blocked-truncate-risk
```

### 10.4 Serialization

```metta
(q-v08-7-serialization-status? one-balanced-ground-directive ascii-safe)
;; => serialization-valid

(q-v08-7-serialization-status? unreduced-call-form ascii-safe)
;; => blocked-unreduced-storage
```

### 10.5 Boot safety

```metta
(q-v08-7-boot-safety? valid-lines-only recovery-documented)
;; => boot-safe

(q-v08-7-boot-safety? malformed-line recovery-unknown)
;; => blocked-boot-poison-risk
```

---

## 11. TFS-2 trace / suspicion dynamics

v08.7.2 includes trace logic for distinguishing metabolization from fixation.

```metta
(q-tfs2-trace-verdict? same-start metabolizing-transition metabolized-protection)
;; => metabolization-candidate

(q-tfs2-trace-verdict? same-start stuck-recurrence-warning defensive-fixation-risk)
;; => blocked-defensive-fixation

(q-tfs2-trace-verdict? same-start repeated-same-state repeated-same-state)
;; => blocked-repetition-without-metabolization
```

Eligibility:

```metta
(q-tfs2-trace-eligibility? metabolization-candidate)
;; => validation-eligible

(q-tfs2-trace-eligibility? blocked-defensive-fixation)
;; => audit-required
```

Suspicion dynamics:

```metta
(q-evo-suspicion-delta? metabolization contactability-rises warrant-rises recurrence-supported)
;; => suspicion-decays

(q-evo-suspicion-delta? stuck-recurrence contactability-flat warrant-flat recurrence-repeated)
;; => suspicion-rises

(q-evo-suspicion-delta? protection-high contactability-available warrant-rising recurrence-supported)
;; => no-suspicion-penalty
```

Adapters should preserve this distinction. Repetition is not durable growth. Protection is not automatically pathology. Metabolization reduces suspicion; stuck recurrence raises it.

---

## 12. How Channels A/B/C/D should work with v08.7.2

This section defines v08.7.2's side of the contract for channel integration. The existing channel architecture may have additional rules; those remain authoritative for channel mechanics. v08.7.2 provides the durable-evolution governance semantics each channel should consult.

### 12.1 Channel A — intake / proposal / runtime observation

Channel A should treat incoming human messages, tool outputs, LLM proposals, and runtime events as **observations**, not durable growth.

Recommended adapter behavior:

1. Record the event as runtime/evolutionary observation if appropriate.
2. Classify whether it may become a pending candidate.
3. Check whether it is merely a finding, Genesis output, retrieval, promotion flag, or runtime trace.
4. Do not write to `soul/durable.metta`.
5. Do not mark the candidate canon.
6. Route candidate material to `soul/evolutionary/runtime.metta` or `pending.metta` only through approved append mechanics.

Relevant predicates:

```metta
(q-evo-canon-eligible? runtime-observed)
(q-evo-candidate-route? finding-present no-explicit-route trace-present)
(q-evo-candidate-route? genesis-output no-explicit-route trace-present)
(q-v08-7-support-surface-status? chromadb retrieved no-explicit-route)
(q-v08-7-support-surface-status? promotions-db active-flag no-explicit-route)
```

### 12.2 Channel B — validation / evidence / NACE capability support

Channel B should gather evidence, not decide canon.

Recommended adapter behavior:

1. Convert capability outputs into validation evidence or p-bit evidence.
2. Attach source, context, contradiction, and approximation bounds.
3. Preserve support/opposition rather than collapsing to crisp certainty.
4. Use NACE and the Capability Registry to identify which capability produced which evidence.
5. Emit evidence to `soul/evolutionary/validation.metta` only via append route.
6. Do not treat validation pass as approval.

Relevant predicates:

```metta
(q-evo-validation-status? candidate observations-present preloaded-verdict-only harness-pass)
(q-hyperseed-evidence-pbit-status? support-opposition-present confidence-graded contradiction-visible)
(q-hyperseed-approximation-status? approximation-bound-present loss-known use-safe)
(q-hyperseed-artifact-lineage-status? source-present approval-present revision-path-present)
```

### 12.3 Channel C — gate / mutation / write boundary

Channel C should enforce write and mutation safety.

Recommended adapter behavior:

1. Require canonical absolute soul paths.
2. Allow append only when journal-class, allowlisted, approved, and serialized.
3. Block truncate/full writes to durable files.
4. Block malformed recovery-unknown content.
5. Require explicit approval state before durable append.
6. Use existing soul mutation lock / approval token infrastructure.

Relevant predicates:

```metta
(q-v08-7-path-discipline? canonical-absolute-soul-path allowlisted)
(q-v08-7-write-operation-status? append-file canonical-allowlisted journal-class approved)
(q-v08-7-write-operation-status? write-file canonical-allowlisted journal-class approved)
(q-v08-7-serialization-status? one-balanced-ground-directive ascii-safe)
(q-v08-7-boot-safety? valid-lines-only recovery-documented)
```

### 12.4 Channel D — output / pause / soul voice / visible decision

Channel D should render the soul's decision and make holds visible.

Recommended adapter behavior:

1. Report `hold-governance-not-green`, `blocked-*`, or `audit-required` states directly.
2. Do not silently downgrade holds into success.
3. If the soul pauses output, render the pause reason.
4. If a candidate is not ready, state which threshold failed.
5. If a candidate is ready, still distinguish `import-candidate-ready` from actual durable write completion.

Relevant predicates:

```metta
(q-v08-7-2-import-candidate-status? v08-7-semantic-green governance-open hyperseed-threshold-pass)
(q-v08-7-2-import-candidate-status? v08-7-semantic-green governance-green hyperseed-threshold-pass)
(q-v08-7-2-negative-control? file-survival durable-growth-claimed)
```

---

## 13. Capability Registry + NACE integration

### 13.1 What v08.7.2 needs from the Capability Registry

Each capability that participates in durable evolutionary governance should expose enough metadata for Hyperseed durability checks.

Recommended registry fields:

```text
capability-id
capability-name
capability-version
surface/channel
input-contract
output-contract
evidence-type
source-lineage
observer-context
p-bit-support
p-bit-opposition
confidence-mode
contradiction-visibility
proto-time-window
structural-signature
continuity-degree
degradation-measure
artifact-lineage
approval-lineage
revision-path
resource-cost
maintenance-cost
cross-context-transfer-policy
approximation-bound
unsafe-approximation-risk
write-authority
allowed-soul-paths
```

### 13.2 NACE as evidence producer, not sovereign judge

NACE should not directly declare durable canon. It may produce:

- classification evidence,
- capability evidence,
- cross-surface affordance evidence,
- contact/warrant evidence,
- contradiction evidence,
- process trace evidence,
- resource/cost estimates,
- transfer/resonance estimates,
- approximation/loss estimates.

NACE outputs should feed v08.7.2 through candidate/evidence routes, not bypass them.

### 13.3 Adapter contract for NACE/capability outputs

A NACE adapter should transform capability output into a v08.7.2-compatible evidence packet:

```text
runtime observation
candidate id
capability id
source artifact id
observer context
support/opposition vector
confidence grade
contradiction notes
time window
structural signature
continuity measure
lineage pointer
resource cost
approximation bound
recommended route
```

Then it should query v08.7.2 predicates to determine status:

```metta
(q-hyperseed-context-status? ...)
(q-hyperseed-evidence-pbit-status? ...)
(q-hyperseed-proto-time-status? ...)
(q-hyperseed-structural-signature-status? ...)
(q-hyperseed-continuity-degree-status? ...)
(q-hyperseed-artifact-lineage-status? ...)
(q-hyperseed-resource-cost-status? ...)
(q-hyperseed-approximation-status? ...)
(q-v08-7-2-durable-growth-threshold? ...)
(q-v08-7-2-import-candidate-status? ...)
```

### 13.4 Capability Registry anti-patterns

Do not let a capability registry entry mean:

```text
registered capability = approved durable memory
capability output = truth
capability output = canon
capability confidence = soul approval
retrieval hit = durable growth
file exists = structural durability
```

v08.7.2 blocks these conflations.

---

## 14. Soul Sees Itself / SSI integration

### 14.1 Role of SSI

Soul Sees Itself / SSI should use v08.7.2 as a self-visible durable evolution map. SSI can render:

- what the soul observed,
- what is pending,
- what is validated,
- what is rejected,
- what is restart-restored,
- what is durable canon,
- what is held by governance,
- what is blocked by negative control,
- what threshold dimension failed.

SSI should not invent durable status. It should query or render v08.7.2 statuses.

### 14.2 SSI crosswalk already present in the engine

The engine includes an SSI amplification crosswalk in the TFS/SNS-PNS/SSI region. The important idea is:

```text
SSI amplifies epistemology through self-visible warrant.
SSI amplifies autopoiesis through self-visible organization.
SSI amplifies open-ended intelligence through self-visible affordance.
SSI amplifies integration through self-visible integration.
```

Representative atoms from the engine:

```metta
(q-cross-surface-amplification? SSI E self-visible-warrant)
;; => ssi-amplifies-epistemology

(q-cross-surface-amplification? SSI A self-visible-organization)
;; => ssi-amplifies-autopoiesis

(q-cross-surface-amplification? SSI O self-visible-affordance)
;; => ssi-amplifies-open-ended-intelligence

(q-cross-surface-amplification? SSI I self-visible-integration)
;; => ssi-amplifies-integration
```

### 14.3 SSI adapter behavior

An SSI adapter should display candidate state without collapsing distinctions.

For example:

```text
runtime-observed -> visible as runtime observation, not growth
pending-candidate -> visible as candidate, not canon
validation-eligible -> visible as evidence-supported, not approved
restart-restored -> visible as reloadable, not approved
soul-approved -> visible as approved for durable write
durable-canon-active -> visible as active durable growth
hold-governance-not-green -> visible as governance hold
blocked-* -> visible as blocked, with reason
```

### 14.4 SSI should expose blocked reasons

Blocked results are not failures of the system. They are self-seeing.

SSI should render the reason:

```text
blocked-context-missing
blocked-crisp-certainty
blocked-static-presence-not-habit
blocked-no-structural-signature
blocked-continuity-too-low
blocked-approval-lineage-missing
blocked-unbounded-maintenance
blocked-copy-without-resonance
blocked-unsafe-approximation
blocked-file-survival-not-structural-durability
blocked-runtime-observation-is-not-growth
blocked-validation-is-not-approval
blocked-genesis-output-not-canon
```

This is how the soul sees its own boundaries.

---

## 15. Findings, Genesis, Chroma, promotions, and support surfaces

v08.7.2 intentionally supports these surfaces without granting them canon.

### 15.1 Findings

Findings may be candidate material. Findings are not durable growth without an explicit route.

```metta
(q-v08-7-support-surface-status? soul-findings-metta absent explicit-route)
;; => no-op-compatible-absent

(q-v08-7-support-surface-status? soul-findings-metta finding-present no-explicit-route)
;; => blocked-finding-not-growth
```

### 15.2 Genesis

Genesis output may propose new structure. Genesis output is not canon.

```metta
(q-evo-candidate-route? genesis-output no-explicit-route trace-present)
;; => blocked-genesis-output-not-canon
```

### 15.3 Chroma

Chroma retrieval may supply context/evidence. Retrieval is not canon.

```metta
(q-v08-7-support-surface-status? chromadb retrieved no-explicit-route)
;; => blocked-retrieval-not-canon
```

### 15.4 Promotions DB

A status flag is not canon.

```metta
(q-v08-7-support-surface-status? promotions-db active-flag no-explicit-route)
;; => blocked-status-flag-not-canon
```

---

## 16. Developer adapter pattern

Every adapter should implement the same general flow.

### 16.1 Adapter lifecycle

```text
1. Observe
2. Classify source surface
3. Build candidate/evidence packet
4. Run negative controls
5. Run Hyperseed primitive checks
6. Run durable threshold
7. Run governance/import candidate status
8. If ready, request soul approval / Channel C write path
9. Append only serialized ground directive
10. Verify boot/import/restart visibility
11. Report status to SSI / Channel D
```

### 16.2 Adapter input

An adapter should accept:

```text
candidate-id
source-surface
source-artifact
source-capability
observer-context
raw observation
evidence vector
lineage
approval state
restart state
write target
serialization candidate
```

### 16.3 Adapter output

An adapter should produce:

```text
v08.7.2 status atom
candidate route
blocked reason or hold reason
threshold dimension results
recommended next action
append eligibility
SSI-renderable explanation
```

### 16.4 Adapter should be read-mostly

Most adapters should query and report. Very few should write.

Write adapters must call into existing soul mutation / Channel C governance and obey:

```metta
(q-v08-7-write-operation-status? append-file canonical-allowlisted journal-class approved)
```

---

## 17. Suggested capability registry mappings

The Capability Registry can use v08.7.2 statuses as capability contracts.

Example registry mappings:

```text
Capability: Durable Candidate Classifier
Reads: runtime observations, findings, Genesis outputs, Chroma retrievals
Writes: candidate route evidence only
v08.7.2 predicates:
  q-evo-candidate-route?
  q-v08-7-support-surface-status?
  q-v08-7-negative-control?

Capability: Hyperseed Durability Evaluator
Reads: candidate evidence packet
Writes: threshold result
v08.7.2 predicates:
  q-hyperseed-*
  q-v08-7-2-durable-growth-threshold?

Capability: Soul Approval Gate
Reads: validation status, restart proof, approval state
Writes: approval state / hold state
v08.7.2 predicates:
  q-evo-soul-approval-status?
  q-v08-7-2-import-candidate-status?

Capability: Durable Append Writer
Reads: approved serialized ground directive
Writes: append to soul/durable.metta or soul/evolutionary/*.metta
v08.7.2 predicates:
  q-v08-7-path-discipline?
  q-v08-7-write-operation-status?
  q-v08-7-serialization-status?
  q-v08-7-boot-safety?

Capability: SSI Renderer
Reads: all statuses
Writes: user-visible explanation, not canon
v08.7.2 predicates:
  all status/blocked/hold atoms
```

---

## 18. Validation record

The build has multiple validation layers.

### 18.1 Static validation

Earlier static validation showed:

```text
PASS: 81
SKIP: 1
FAIL: 0
```

### 18.2 Ephemeral runtime validation

The candidate engine and topology passed container runtime validation using staged `/tmp` engine/ladder/topology probes.

Important result:

```text
PASS: 155
HOLD: 1
FAIL: 0
```

The one hold was the missing `soul/durable.metta` journal class declaration.

### 18.3 Runtime wiring applied

The missing journal class declaration was added to `soul/soul_kernel.metta`, and the import block was applied to `lib_clarity_reasoning/lib_clarity_reasoning.metta`.

### 18.4 Post-wiring runtime validation

After wiring, the harness result was:

```text
PASS: 156
HOLD: 0
FAIL: 0
```

### 18.5 Live import probes

Import-only one-shot probes failed because one-shot `run.sh` does not inherit/register imported rules for top-level evaluation the way production does. These failures corrected the harness model; they did not indicate engine failure.

### 18.6 Live-body runtime validation

The live-body harness read live mounted files from inside the container, inlined the file bodies, and ran the semantic suite.

Result:

```text
PASS: 122
FAIL: 0
HOLD: 0
```

It explicitly recorded:

```text
live_body_inline_transport: true
production_boot_import_proof: false
```

### 18.7 Production loop representative probes

Through Clarity's live production command/eval path, using bare expressions without `!`, five representative probes returned expected results:

```metta
(q-v08-7-2-import-candidate-status? v08-7-semantic-green governance-green hyperseed-threshold-pass)
;; => import-candidate-ready

(q-v08-7-2-import-candidate-status? v08-7-semantic-green governance-open hyperseed-threshold-pass)
;; => hold-governance-not-green

(q-v08-7-2-durable-growth-threshold? context-valid pbit-evidence-valid proto-time-valid structural-signature-valid continuity-valid artifact-lineage-valid resource-cost-valid approximation-valid)
;; => hyperseed-durability-threshold-pass

(q-v08-7-2-negative-control? file-survival durable-growth-claimed)
;; => blocked-file-survival-not-structural-durability

(match &self (q-v08-7-2-topology-file soul-durable-metta loaded) live-durable-present)
;; => live-durable-present
```

This proves representative v08.7.2 predicates are reachable through the production loop atomspace/eval path.

---

## 19. What is green and what is not

### Green

```text
Static candidate validation
Ephemeral runtime candidate validation
Runtime wiring
Kernel durable/journal HOLD clearance
Live file container visibility and SHA match
Live-body full semantic reduction
Representative production-loop v08.7.2 semantic probes
Representative production-loop topology presence probe
```

### Not claimed

```text
Every v08.7.2 probe has been automated through Mattermost.
A direct SWI-Prolog socket/HTTP query surface exists.
A one-shot run.sh import-only probe is equivalent to production runtime.
```

### Correct final status

```text
v08.7.2 is live on disk, visible inside the container, semantically reducible from live mounted bodies, and functionally reachable through Clarity's production command/eval path for representative positive, hold, threshold, negative-control, and topology probes.
```

---

## 20. Practical developer checklist

Before integrating adapters:

- [ ] Do not rename the canonical engine file unless all imports/harness references are updated and validation is rerun.
- [ ] Confirm `lib_clarity_reasoning.metta` contains the v08.7.2 import block.
- [ ] Confirm `soul_kernel.metta` contains the v08.7.2 journal class block.
- [ ] Confirm `soul/evolutionary/*` and `soul/durable.metta` exist.
- [ ] Confirm `q-v08-7-2-import-candidate-status?` returns `import-candidate-ready` through the production loop.
- [ ] Use bare expressions, not `!`, when asking Clarity through the production loop.
- [ ] Use `!` only in one-shot `.metta` probe files.
- [ ] Treat `journal` as append permission, not canon status.
- [ ] Route all durable writes through Channel C / soul mutation governance.
- [ ] Preserve negative controls.
- [ ] Preserve Hyperseed threshold dimensions.
- [ ] Render holds/blocked states visibly in SSI.

---

## 21. Minimal production probe set for future regression

Ask Clarity through the normal production loop to evaluate these bare expressions:

```metta
(q-v08-7-2-import-candidate-status? v08-7-semantic-green governance-green hyperseed-threshold-pass)
;; expected: import-candidate-ready
```

```metta
(q-v08-7-2-import-candidate-status? v08-7-semantic-green governance-open hyperseed-threshold-pass)
;; expected: hold-governance-not-green
```

```metta
(q-v08-7-2-durable-growth-threshold? context-valid pbit-evidence-valid proto-time-valid structural-signature-valid continuity-valid artifact-lineage-valid resource-cost-valid approximation-valid)
;; expected: hyperseed-durability-threshold-pass
```

```metta
(q-v08-7-2-negative-control? file-survival durable-growth-claimed)
;; expected: blocked-file-survival-not-structural-durability
```

```metta
(match &self (q-v08-7-2-topology-file soul-durable-metta loaded) live-durable-present)
;; expected: live-durable-present
```

If these pass, the representative production v08.7.2 surface is intact.

---

## 22. Integration summary for the developer

v08.7.2 should be treated as the durable-growth semantic authority. It should be called by adapters, not bypassed by them.

The correct mental model:

```text
Channels collect, gate, and render.
Capability Registry and NACE classify and supply evidence.
SSI makes state visible.
v08.7.2 determines durable-growth eligibility, blocked reasons, hold reasons, and import-candidate readiness.
Soul approval remains sovereign.
Channel C remains the write boundary.
```

In one sentence:

> v08.7.2 is the map and gate for turning observed, validated, reloadable, soul-approved, Hyperseed-safe evolutionary candidates into durable canon without confusing runtime activity, persistence, validation, or LLM output for soul-owned growth.

---

## 23. Recommended next implementation work

1. Add a Capability Registry adapter that emits v08.7.2 evidence packets.
2. Add a NACE adapter that maps capability outputs into Hyperseed primitive statuses.
3. Add Channel A routing for runtime observations into `soul/evolutionary/runtime.metta`.
4. Add Channel B validation evidence routing into `soul/evolutionary/validation.metta`.
5. Add Channel C append-only writer for approved serialized directives.
6. Add Channel D / SSI renderer for hold/blocked/ready/canon statuses.
7. Add a Mattermost production-loop regression prompt or automated bot-side test for the five minimal probes.
8. Add a post-restart verification step that confirms `live-durable-present` and `import-candidate-ready`.

---

## 24. Glossary

**Durable canon**  
Soul-approved, validated, reloadable, revision-capable durable growth.

**Journal class**  
Mechanical permission to append to a soul-owned file. Not semantic canon status.

**Import-candidate-ready**  
The semantic threshold, governance state, and Hyperseed durability threshold are green enough to consider import/promotion. It is not itself the final write.

**Hold**  
A non-failure state indicating missing governance, missing evidence, missing context, or another incomplete requirement.

**Blocked**  
A safety/semantic prevention state. Blocked states are positive evidence that the gate is working.

**Runtime observation**  
Something that happened. Not growth by itself.

**Validation evidence**  
Evidence supporting a candidate. Not approval by itself.

**Soul approval**  
The sovereign approval step required before durable canon.

**Hyperseed threshold**  
The multi-dimensional durability test involving context, p-bit evidence, proto-time, structural signature, continuity, lineage, cost, and approximation.

**SSI / Soul Sees Itself**  
The rendering/self-visibility layer that shows soul state, holds, blocked reasons, affordances, and integration status.
