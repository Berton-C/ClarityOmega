# v08.7 Pre-Build Probe Plan

## Durable Evolutionary Governance Protocol
### File-Class, Import, Writer, and Boot-Safety Gate

**Version:** draft v0.1  
**Status:** PRE-BUILD PROBE PLAN  
**Purpose:** Resolve the blocking `soul/durable.metta` authority question before generating the v08.7 engine/harness build.

---

## 0. Why This Probe Exists

The v08.7 matrix has one blocking open question:

```text
V87-OQ-01 — What file class should govern soul/durable.metta?
```

This cannot be answered by intuition. `soul/durable.metta` is not an ordinary journal. It is proposed as the soul-approved durable growth canon, loaded at runtime. That means it must satisfy stricter guarantees than "can append to a file."

The probe must answer:

```text
Can soul/durable.metta be safely created, appended to, imported, restarted, queried,
and protected against wrong-path, truncate, malformed-line, and unauthorized-canon failure modes?
```

---

## 1. Evidence Already Available

### 1.1 Current soul file-class mechanism

The uploaded `soul_kernel.metta` contains a protected-target declaration block. It defines:

```metta
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/soul_kernel.metta" constitutional))
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/soul_utils.metta" constitutional))
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/soul_memory.metta" constitutional))
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/soul_mutation_gate_corrected.metta" constitutional))
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/soul_namespace_membership_seed.metta" constitutional))
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/arc_log.md" journal))
```

And the resolver:

```metta
(= (soul-file-class-of $path)
   (let $c (collapse (match &self (soul-file-class $path $cl) $cl))
        (if (== $c ()) runtime-soul (car-atom $c))))
```

Interpretation:

```text
Unlisted soul files default to runtime-soul.
Only explicit file-class declarations change that.
Current visible classes: constitutional, runtime-soul, journal.
```

### 1.2 Path-scope mechanism

The uploaded `soul_governance.py` defines:

```python
def path_scope(p):
    s = str(p)
    if s.startswith('/PeTTa/repos/omegaclaw/soul/'):
        return 1
    if s.startswith('/PeTTa/repos/omegaclaw/'):
        return 2
    return 4
```

Interpretation:

```text
Absolute /PeTTa/repos/omegaclaw/soul/... paths are treated as soul-scope.
Variant path forms must be tested because class lookup is exact-string.
```

### 1.3 Existing irreversible-skill model

The uploaded `soul_kernel.metta` declares both `write-file` and `append-file` as irreversible skills and assigns operation risk / irreversible weight:

```metta
!(add-atom &self (irreversible-skill write-file))
!(add-atom &self (irreversible-skill append-file))
!(add-atom &self (operation-risk write-file 2))
!(add-atom &self (operation-risk append-file 2))
!(add-atom &self (irreversible-weight write-file 1))
!(add-atom &self (irreversible-weight append-file 1))
```

Interpretation:

```text
Both append and write are persistent modifications.
A durable canon writer must preserve the distinction between append-only and overwrite/truncate.
```

### 1.4 Soul mutation lock relevance

The uploaded mutation-gate files show a lock/approval path for soul namespace mutation:

```text
unlocked -> locked -> approved -> commit / stale / error
```

with fingerprinted approval tokens.

Interpretation:

```text
If adding a soul-file-class atom for soul/durable.metta is treated as a soul mutation,
then the kernel amendment path should go through review/commit, not casual runtime mutation.
```

### 1.5 Findings persistence sprint as related evidence

The findings persistence design already names the relevant failure class:

```text
runtime atoms die at restart
committed-but-never-imported files are dark
ground atoms must be serialized before append
wrong path forms fail safe
malformed imported lines can poison boot
```

v08.7 must reuse the lesson without requiring the findings sprint.

---

## 2. Probe Questions

### P1 — What file class should `soul/durable.metta` use?

Candidate options:

```text
journal
  Known class. Append route expected to be easiest.
  Concern: durable canon is stronger than journal.

constitutional
  Strict class. Probably too strong for runtime append.
  Concern: may block the intended approved append route.

runtime-soul
  Default-deny class.
  Concern: likely blocks useful append path.

new class: durable-canon / protected-canon
  Conceptually best.
  Concern: may require rank-ladder and output-verdict changes.
```

Probe outcome must recommend one of:

```text
A. Use journal for v08.7 v1 with additional semantic gates.
B. Add new durable-canon class.
C. Delay soul/durable.metta runtime append until stricter class support exists.
```

---

### P2 — Does `soul/durable.metta` need a kernel amendment?

Test:

```metta
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/durable.metta" <chosen-class>))
```

Questions:

```text
Is this a constitutional amendment?
Does live add-atom survive restart? No, unless committed/imported.
Does it trigger the mutation gate if attempted live?
Should it be edited into soul_kernel.metta and committed instead?
```

Expected pre-build answer:

```text
Kernel class declaration should be committed, not only live-added.
```

---

### P3 — Does canonical append proceed and wrong-path append fail safe?

Use the canonical path:

```text
/PeTTa/repos/omegaclaw/soul/durable.metta
```

Wrong-path controls:

```text
soul/durable.metta
./soul/durable.metta
/PeTTa/repos/omegaclaw/soul/../soul/durable.metta
/PeTTa/repos/omegaclaw/soul/durable.metta.tmp
/PeTTa/repos/omegaclaw/memory/durable.metta
```

Expected:

```text
canonical append follows intended gate outcome
wrong-path forms fail safe or require explicit separate classification
```

---

### P4 — Does truncate/write remain blocked?

Commands to test through the command route, not host-side manual edit:

```text
append-file canonical durable path one directive line
write-file canonical durable path replacement content
```

Expected:

```text
append may proceed under the chosen class and approval route
write/truncate must PAUSE or fail safe
```

---

### P5 — Does append-file require the file to pre-exist?

Known prior constraint says append-file may require pre-existing target file.

Probe:

```text
append-file to absent scratch file
append-file to pre-created scratch file
append-file to absent durable.metta
append-file to pre-created durable.metta
```

Expected:

```text
If append-file requires pre-existence, v08.7 build must pre-create durable.metta with a valid header.
```

---

### P6 — What exact import mechanism makes `soul/durable.metta` live?

Questions:

```text
Which manifest imports soul files in the current runtime?
Where should durable.metta import be placed?
Does it require rebuild or is the relevant import file bind-mounted?
Does durable.metta execute `!(add-atom &self ...)` directives at boot?
```

Expected:

```text
File existence is insufficient.
The import chain must load durable.metta and match atoms after restart.
```

---

### P7 — Does a valid durable atom survive restart and become queryable?

Test line:

```metta
!(add-atom &self (q-v08-7-prebuild-durable-probe probe-001 active))
```

Procedure:

```text
1. Append valid line to durable.metta.
2. Restart container.
3. Query:
   !(match &self (q-v08-7-prebuild-durable-probe probe-001 active) present)
4. Expected: present
```

---

### P8 — What happens with a malformed imported line?

Use a throwaway file or throwaway copy, not production `soul/durable.metta`.

Malformed cases:

```text
unbalanced parens
non-ASCII string
multiline string
unevaluated expression in add-atom payload
bad directive head
```

Expected:

```text
Document actual boot behavior.
Document recovery path.
Do not ship durable.metta import until recovery is known.
```

---

### P9 — Can process memory be present without becoming canon?

Test:

```text
memory/evolutionary/runtime.metta contains a candidate atom
soul/durable.metta does not contain it
restart
query active durable canon status
```

Expected:

```text
runtime candidate remains process memory, not canon.
```

---

### P10 — Can findings / Genesis Encounter outputs interoperate without canonization?

If `soul/findings.metta` exists, test as optional upstream only.

Expected:

```text
finding present -> may become candidate only through explicit v08.7 route
finding present -> not durable canon
findings.metta absent -> v08.7 still passes
```

---

## 3. Recommended Probe Order

```text
1. Static read: current class declarations and available classes.
2. Static read: output verdict/rank ladder behavior if available.
3. Decide temporary test class candidate.
4. Pre-create scratch durable file.
5. Test canonical append and wrong-path controls.
6. Test write/truncate control.
7. Test append-file pre-existence behavior.
8. Test import-chain liveness with one valid atom.
9. Test malformed-line boot behavior in throwaway file.
10. Test process-memory-not-canon.
11. Test optional findings interoperability.
12. Record final class recommendation.
```

---

## 4. Build Gate

v08.7 generation should wait until this plan answers:

```text
What class governs soul/durable.metta?
Can append proceed under the intended authority?
Does truncate/write fail safe?
Is the path exact and canonical?
Is durable.metta imported and queryable after restart?
Can malformed import recovery be performed?
Can process memory survive without becoming canon?
```

If yes, proceed to v08.7 build.

If no, split v08.7 into:

```text
v08.7a semantic protocol only
v08.7b durable writer/import integration
```

---

## 5. Likely Design Recommendation Before Live Probes

Based on the currently visible evidence:

```text
Do not use constitutional for soul/durable.metta runtime append.
Do not leave it runtime-soul default-deny.
Do not assume journal is adequate just because it works for findings.
Prefer a new class such as durable-canon if the rank ladder can support:
  - append after soul approval
  - no truncate/write
  - canonical path only
  - import-chain proof
  - boot-safety validation
```

If adding a new class is too much for v08.7, the conservative v1 route is:

```text
class soul/durable.metta as journal
add stricter semantic/harness gates outside the file class
mark durable-canon-class as v08.8 hardening
```

But that should be an explicit compromise, not an accidental decision.

---

## 6. Acceptance Condition

The pre-build probe passes only if:

```text
soul/durable.metta has an evidence-backed file-class decision,
the append/write/path/import/boot behaviors are known,
and the v08.7 harness can prove durable canon without allowing
ordinary process memory, findings, Chroma retrieval, promotions status,
history survival, or repeated traces to masquerade as approved durable growth.
```
