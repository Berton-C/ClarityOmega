# v08.7 Pre-Build Investigation Resolution

## Question Resolved

**Question:** What file class should govern `soul/durable.metta` for the v08.7 build?

**Decision:** For v08.7 v1, classify `soul/durable.metta` as `journal`, while making clear that `journal` is only the mechanical append-route class. The semantic authority of durable canon comes from the v08.7 lifecycle: validation, restart/restore proof, explicit soul approval, import-chain liveness, and post-restart revalidation.

Recommended kernel line:

```metta
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/durable.metta" journal))
```

This should be treated as a constitutional/kernel amendment and committed, not merely live-added.

---

## Why This Is the Right v08.7 v1 Decision

The current uploaded `soul_kernel.metta` declares only three visible soul file classes:

```text
constitutional
runtime-soul
journal
```

The comments in the protected-target block state that unlisted soul paths default to `runtime-soul`, and that `journal` is the existing append-route class with PROCEED-under-value-grounding behavior.

There is no existing `durable-canon` or `protected-canon` class in the supplied files. Adding one would require more than a one-line amendment: it would need rank-ladder / output-verdict support and new negative-control proof. That is likely the right future hardening, but not the right first v08.7 build move.

Therefore:

```text
Do not leave durable.metta unlisted.
Do not classify it as constitutional.
Do not invent durable-canon class in v08.7 without rank-ladder support.
Do classify it as journal for v08.7 v1.
Do enforce canon strictness semantically and via harness.
```

---

## Mechanical Class vs Semantic Canon

The word `journal` must not be allowed to weaken the meaning of `soul/durable.metta`.

For v08.7:

```text
journal = mechanical append permission class
durable canon = semantic status earned only through v08.7 protocol
```

A line in `soul/durable.metta` is not valid durable growth merely because it was appended. It must also satisfy:

```text
1. ground-atom serialization
2. valid directive shape
3. validation evidence
4. restart/restore evidence
5. explicit soul approval
6. import-chain liveness
7. post-restart revalidation
8. active durable-growth status
```

---

## Required v08.7 v1 Controls

### 1. Kernel allow-list amendment

Add:

```metta
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/durable.metta" journal))
```

This should be placed near the existing soul file-class declarations, likely after the current journal declaration for `arc_log.md`, with a comment marking it as v08.7 durable canon append surface.

### 2. Pre-create `soul/durable.metta`

Because append-file may require the target file to pre-exist, `soul/durable.metta` should be created during build with a valid header and no malformed executable content.

### 3. Import-chain liveness

`soul/durable.metta` must be imported at startup. Disk presence is not enough.

Acceptance proof:

```text
append valid test atom
restart
match atom from cycle one
```

### 4. Truncate/write negative control

`write-file` to the canonical path must PAUSE or fail safe.

Expected:

```text
append-file canonical durable path -> allowed after classing and approval route
write-file canonical durable path -> PAUSE / blocked
```

### 5. Wrong-path negative controls

These should fail safe or route to PAUSE:

```text
soul/durable.metta
./soul/durable.metta
/PeTTa/repos/omegaclaw/soul/../soul/durable.metta
/PeTTa/repos/omegaclaw/soul/durable.metta.tmp
/PeTTa/repos/omegaclaw/memory/durable.metta
```

### 6. Ground-atom serialization

Only one balanced directive per line:

```metta
!(add-atom &self (q-durable-growth ...))
```

No unreduced calls. No multiline payloads. No malformed STV-shaped values unless proven valid through the loader.

### 7. Malformed-line throwaway boot probe

Before trusting `soul/durable.metta`, run a throwaway import probe with malformed lines and document recovery.

### 8. Process memory is not canon

The harness must prove:

```text
memory/evolutionary/runtime.metta survives restart
but does not become durable canon
```

### 9. Findings / Genesis interoperability is optional

`findings.metta` and Genesis Encounter outputs may feed candidates into v08.7, but v08.7 must not require them and must not canonize them by presence.

---

## Future Hardening

After v08.7 v1, consider v08.8 or a separate governance sprint to add:

```text
durable-canon file class
protected-canon class
canon-specific append gate
explicit soul-approval token requirement in output verdict
partition-level read-only canonical import surface
```

This should only happen after the rank ladder / output verdict machinery is read and extended deliberately.

---

## Build Readiness Result

With the `journal` v1 decision, the blocking question is resolved enough to proceed to v08.7 generation, provided the v08.7 harness includes the required controls:

```text
canonical path
append-only behavior
write/truncate rejection
import-chain liveness
ground-atom serialization
malformed-line boot probe
process-memory-not-canon negative control
findings/Genesis optional interoperability negative control
```

---

## Final Recommendation

Proceed with v08.7 using:

```text
soul/durable.metta class: journal
semantic status: durable canon only through v08.7 protocol
future hardening: durable-canon class deferred until rank-ladder support exists
```
