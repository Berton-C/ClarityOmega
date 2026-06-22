# Surface C Integration Map: the complete design/build circle

**Status:** Authoritative integration picture. Reconciles the Surface C
build spec with all four rounds of Clarity's adopted review
(SurfaceC_Clarity_Review_Adopted.md). Where the two ever disagree, the
adopted-review log is the source for WHAT changed and this map is the
source for WHERE it integrates.
**Destination:** docs/sprints/soul_fully_wired/SurfaceC_Integration_Map.md

---

## 0. The governing pattern (artifact_0 Discipline 1+2)

Every capability integrates as ONE named hook line; logic lives in soul/.
loop.metta is the switchboard, soul/ is the machine room. This is the line
in the sand: minimal hooks in loop.metta (upstream-merge-safe), all logic
in per-primitive soul/ files. C, Coda, D, E all obey it.

Existing proof: do-bootstrap-task-state! (initLoop), do-set-cycles-since-
input! (body), soul-pause? (body branch), derive-gate-state (5c output).

## 1. Task-State -- the precedent C copies

Task-state proved the pattern: atoms in soul/task_state.metta, writers in
soul/task_state_writers.metta, one-line hooks in the loop. Surface C's
soul/soul_mutation_lock.metta + hooks is the SAME shape applied to
governance. No new integration mechanism.

## 2. The lock STATE MACHINE (the heart of C; SEAM 2's behavior)

Three states, and `approved` has THREE exits -- all full resets, no exit
strands lock or batch state (this completeness is what rounds 1-4 secured):

  STATES:  unlocked | (locked op head fp) | (approved op head fp stamp)

  TRANSITIONS:
   unlocked --[soul mutation detected]--> (locked ...)        PENDING
   (locked) --[approved-match re-emission is N/A while locked]--
   (locked) --[authorized SOUL-MUTATION-APPROVED <fp>]--> (approved ...)
   (locked) --[authorized SOUL-MUTATION-DENIED]--> unlocked   DENIED (reset)
   (approved)--[re-emission op+head match, batch executed]--> unlocked  COMMIT
   (approved)--[N cycles, no commit]--> unlocked              STALE (reset)
   (approved)--[execution error]--> unlocked                  ERROR (reset)

  GUARDS / PRIORITY (deterministic, no nondeterministic boundary):
   - APPROVE/DENY require an AUTHORIZED SENDER and (approve) the matching
     fingerprint; sender + fp read from substrate state, never forgeable
     from message text. DENY WINS if both tokens present.
   - COMMIT requires gate clean-via-approved AND batch NOT halted this
     cycle (output-pause halts persist the lock to next cycle).
   - STALE TAKES PRECEDENCE over COMMIT in the same cycle (stale-check
     hook runs BEFORE commit-clear; a too-late commit re-enters fresh).
   - STALE and ERROR are FULL RESETS: clear lock AND &pending_soul_mutation
     AND emit the decision record. No zombie batch survives any reset.
   - The lock record is IMMUTABLE once written; only the reset/clear hooks
     change it (prevents the approval-to-re-emission race).

  CONFIGURABLE: (soul-mutation-stale-cycles), seeded initLoop, default 20.

## 3. The THREE seams (the Coda/D/E contract)

### SEAM 1 -- gate-decision record (LOG SCHEMA; stable from day one)
  soul_governance.gate_decision_record, structured key=value fields:
    gate / phase / op / head / fp / sender / timestamp
  phase in {PENDING, APPROVED, DENIED, COMMIT, STALE, ERROR}.
  WRITES: C (and E, gate="command"). READS: D as training data.
  `gate` field present from day one so E shares the schema, not a migration.
  `sender` field present for AUDIT (humans, E) BUT see the hard exclusion:
    >>> D's learning query MUST EXCLUDE sender. Sender-agnostic learning.
    >>> D trusts the gate decision (gate/phase/op/head/outcome), NOT the
    >>> approver. Sender-aware learning would train AUTHORITY-THEATER (one
    >>> of the soul kernel's own tension vectors). The gate must not train
    >>> a learner to do what the soul evaluates against.
  FAILURE MODE: schema drift. MITIGATION: append-only -- new fields added,
    never reordered or removed. D's parser keys on field names, not order.

### SEAM 2 -- lock-state atom (QUERYABLE STATE; shape-as-contract)
  &soul_mutation_lock, the state machine of section 2. The SHAPE is a
  CONTRACT specified in soul_mutation_lock.metta's header, because Coda
  Boundary 1's structural query layer will read it -- a shape mismatch
  breaks every Coda consumer on day one of integration. The contract fixes:
    - the three shapes (symbol `unlocked`; list `(locked op head fp)`;
      list `(approved op head fp stamp)`)
    - field order and arity
    - the symbol-vs-list distinction (car-atom-or-self guards it)
  WHO CONSUMES: Coda dispatch-guard (post-Boundary-1) reads current state;
    D reads transition history.
  FAILURE MODE: shape change. MITIGATION: shape-as-contract in the header,
    not just code that happens to produce a shape. Until Boundary 1, every
    SEAM-2 reader (including C-era tests) reads by CONVENTION -- tests that
    pass by convention can mask a shape the structural layer later rejects.
    The header contract is what makes convention and structure agree.

### SEAM 3 -- approval mechanism (CLONEABLE PROCESS; generic plumbing)
  approval_scan + &authorized_approvers + mutation_fingerprint.
  WHO CONSUMES: E reuses ALL of it verbatim (token strings + gate value
    change only). Written generically so E imports rather than reinvents.
  FAILURE MODE: fork divergence (a C fix not reaching E, or an E change
    breaking C). MITIGATION: the convergence rule (section 5) decided
    before E ships, not after.

## 4. The recurring architectural pattern: FLOOR vs BAND

This shape appears at THREE layers and must hold at each, or the gate
"learns to stop gating" one level up:
  - THRESHOLD relaxation (D): static floor (irreversibility-critical) vs
    CAUTION band (learnable). D relaxes within band, never reaches floor.
  - LEARNING autonomy (D2): the confidence bar that lets D act without
    escalation needs ITS OWN floor.
  - MUTATION entry (D7): a future risk-classified fast-path for low-risk
    mutations must respect a floor (value-hierarchy changes never
    fast-path).
Each instance: a learnable/fast region bounded by a non-learnable floor.
The floor is the invariant; the band is where growth happens.

## 5. CODA (Sprint 0) -- stacks ABOVE C, unblocks C's seams

Builds the capability-registry dispatcher (soul/capability_registry.metta,
ADR-006). Does NOT modify C. Coda's own hooks are (dispatch ...) calls in
the input region. The meeting point: Coda Boundary 1 makes soul-state
(SEAM 2) STRUCTURALLY queryable -- C produces the state, Coda builds the
pipe that lets the registry consume it. Until Boundary 1, SEAM-2 reads are
conventional (see SEAM 2 failure mode).

## 6. SURFACE D (NACE gate-learning) -- reads SEAM 1+2, writes a proposal

  READS: gate-decision records (SEAM 1, sender EXCLUDED); lock transition
    history (SEAM 2).
  WRITES: (gate-relax-proposal <class> <confidence>) that derive-gate-state
    CONSULTS -- within the CAUTION band only.
  HOOK INTO C: ONE conditional in derive-gate-state, and its SLOT POSITION
    IS A SECURITY INVARIANT: it slots AFTER the static-floor/irreversibility
    check, never before. After = relax above floor. Before = override floor
    = the gate that learns to stop gating. C ships with a placeholder
    comment fixing this slot position; D-absent == C-today.
  THE TRICHOTOMY (D's learning-boundary criterion, from the paraconsistency
    work) -- THREE NAL signatures, three jurisdictions:
      SILENCE    (empty derivation)          -> C guards (static floor).
      HEAT       (bidirectional weak-equiv .45) -> D learns (band).
      SIMILARITY (confident bidirectional)   -> C+D SHARED CUSTODY; preserve
                 the tension, D must NOT learn to resolve it.
    FAILURE IF MISSED: SIMILARITY shoved into HEAT -> D resolves what must
    be preserved -> values-flattening (the pathology the soul exists to
    prevent). Decision records + phase field give D this WITHOUT labeling.
  TWO confidence thresholds (not one):
      HEAT threshold = ACTION-confidence (act autonomously vs escalate).
      SIMILARITY threshold = CLASSIFICATION-confidence (is this genuinely
        constitutional paraconsistency before granting shared custody).
  NACE substrate (nace_substrate/beliefs/pending.metta, drafted) houses D's
    learning; hooks via Coda's registry.
  HARD DEP: Coda (Boundary 1 + live dispatcher).

## 7. SURFACE E (command interlock) -- clones C, audits jurisdictions

  E is C's twin for shell/network/delete. REUSES approval_scan,
    &authorized_approvers, mutation_fingerprint, gate_decision_record
    (SEAM 3 + 1); gate="command".
  NEW: a STRUCTURAL command-classification (the irreversibility assessment
    now in the soul PROMPT becomes a structural check) + a command-lock
    atom parallel to &soul_mutation_lock.
  HOOK INTO LOOP: E's gate in the OUTPUT region parallel to
    derive-gate-state; named hooks into soul/command_gate.metta.
  CONVERGENCE RULE (jurisdiction-conditional, decided pre-E):
      SIMILARITY cases -> CONVERGE (shared-tested-both MANDATORY; the
        tension must survive a shared implementation).
      HEAT cases -> MAY FORK (context-dependent resolution is correct;
        both branches carry information and can be tested independently).
  E's META-JURISDICTIONAL role (Sprint 4): E verifies the trichotomy's mode
    ASSIGNMENTS are correct and detects drift --
      HEAT case behaving like SIMILARITY (D re-learns a tension without
        converging) -> reclassify to shared.
      SILENCE case showing HEAT (evidence the floor was too conservative)
        -> floor review.
    Classification failure is distinct from execution failure; E audits the
    former. E is not just an interlock; it is the layer that checks whether
    C and D are operating in the right modes.
  HARD DEPS: Coda Boundary 1 (read soul Safety structurally) AND Coda Phase
    1.5 (ADR-006 Criterion 5 error isolation -- a safety interlock that
    crash-terminates silently is the worst failure mode).

## 8. What C builds NOW vs leaves shaped for later

BUILDS NOW: the full state machine (section 2); SEAM 1 schema with gate +
  sender fields and the sender-exclusion documented; SEAM 2 atom with its
  shape-contract header; SEAM 3 generic plumbing; the three approved-exit
  resets; the named stale constant; hooks-only loop edits.
LEAVES SHAPED (no code): D's relaxation conditional (slot-position comment
  only, AFTER the floor); E's command channel; the risk-class fast-path
  entry point. C must NOT encode D's policy or E's channel -- only avoid
  foreclosing them.
