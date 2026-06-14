# Clarity's review -> adopted changes (folded before Surface C rebuild)

## Into C's code (change the build):
C1. STALE expiry on approved lock. Approved lock carries a cycle-count
    (approved op head fp cycle-stamped). A body hook
    clarity-soul-mutation-stale-check! expires approved->unlocked after N
    cycles (N=20, ~ one engaged burst) without commit, emits STALE
    gate-decision. Prevents the indefinite open-door.
C2. commit-clear verifies EXECUTION not just clean gate. Clear only when
    gate was clean-via-approved AND the batch was not halted by
    output-pause this cycle (i.e. $soul_decision != pause). If halted, the
    approved lock persists to next cycle.
C3. record schema gains `sender` field NOW (gate, phase, op, head, fp,
    sender, timestamp). Cheap with one approver; migration-under-live-data
    with three.
C4. lock-state atom SHAPE specified as explicit contract in the
    soul_mutation_lock.metta header (SEAM 2 schema): the three shapes,
    field order, symbol-vs-list, so Coda Boundary 1 reads structurally not
    conventionally.
C5. transition call guard: ($_ (if $msgnew (...) _)) is correct (approval
    is always a new message); verified NOT a bypass.

## Into the docs (bind D/E, no C code change):
D1. derive-gate-state placeholder comment specifies D's slot position:
    AFTER the static-floor/irreversibility check, never before. Slot
    position IS the security invariant (D relaxes above floor, cannot
    override it).
D2. roadmap gains the confidence-bar floor: the learning band's autonomy
    threshold needs its own floor, or it reinvents the gate-that-learns-
    to-stop-gating one level up. Open design question for D, recorded.
D3. roadmap gains the E-convergence rule decision (shared-tested-both vs
    fork-at-E), to be decided before E ships, not after.
D4. D's learning-boundary criterion (Clarity's paraconsistency mapping):
    NAL SILENCE (empty derivation between value props) = static floor (D
    observes always-denied/always-escalated). NAL HEAT (bidirectional
    weak-equiv ~0.45) = learning band (D learns context-dominance). The
    decision records + phase field give D this WITHOUT hand-labeling.
    Recorded as D's design seed.
D5. SEAM failure modes (her catch): SEAM1 fails by schema drift (mitigate:
    append-only, never reorder/remove fields); SEAM2 fails by shape change
    (mitigate: shape-as-contract in a schema header); SEAM3 fails by fork
    divergence (mitigate: convergence rule decided pre-E).

## Clarity review round 2 -> adopted (folded before rebuild)

C1-amended (zombie-race fix, CODE). clarity-soul-mutation-stale-check! is
a FULL RESET, not just a lock transition: on expiry it clears the approved
lock -> unlocked AND clears &pending_soul_mutation (the halted batch
record) AND emits a STALE gate-decision. Prevents the stall-then-expire
zombie: a halted batch surviving past STALE as unapproved data that a
re-submit could ride. STALE = no trace left behind.

C3-amended (sender governance fork, CONTRACT). The `sender` field stays in
the record for AUDIT (humans, E) but D's learning query MUST EXCLUDE it.
Decision: sender-agnostic learning. D trusts the gate decision (gate/phase/
op/head/outcome), NOT the approver. Rationale: sender-aware learning trains
authority-theater (trust the approver over the evidence) -- one of the
soul kernel's own tension vectors. The gate must not train a learner to do
what the soul evaluates against. Written as a hard exclusion in the schema
header so D's parser inherits the boundary, not an ambiguity.

D4-amended (the TRICHOTOMY, D design seed -> constraint). NAL produces
THREE signatures, not two:
  SILENCE   (empty derivation)            -> C guards. Static floor.
  HEAT      (bidirectional weak-equiv ~.45) -> D learns. Learning band.
  SIMILARITY(confident bidirectional)     -> SHARED CUSTODY. Preserve the
            tension; neither direction dominates; D must NOT learn to
            resolve it. Constitutional paraconsistency: the tension IS the
            structure.
  Jurisdiction: SILENCE->C, HEAT->D, SIMILARITY->C+D shared.
  FAILURE IF MISSED: SIMILARITY shoved into HEAT -> D learns to resolve
  what must be preserved -> values-flattening, the pathology the soul
  architecture exists to prevent. This is a CONSTRAINT on D, not a note.

## Clarity review round 3 -> adopted

C1-amended-2 (STALE/commit same-cycle race, CODE). When a commit and a
STALE expiry would both fire in cycle N, STALE TAKES PRECEDENCE. Semantic:
STALE means the approval waited too long to be trusted; a commit landing
exactly at expiry came too late and must re-enter from scratch, not ride
the expiring approval. Implementation: the stale-check hook runs BEFORE
the commit-clear hook in the body; if stale fires (full reset to
unlocked), commit-clear sees unlocked and no-ops. Deterministic boundary.

D2-amended (TWO thresholds, D seed). The learning band's confidence floor
is two floors, one per jurisdiction:
  HEAT threshold      = ACTION-confidence floor: how confident D must be
                        before acting autonomously without escalating to C.
  SIMILARITY threshold= CLASSIFICATION-confidence floor: how confident the
                        system must be that a case genuinely IS
                        constitutional paraconsistency before granting
                        shared custody (vs reclassifying HEAT/SILENCE).
  Conflating them: D acts too autonomously on SIMILARITY (HEAT floor
  applied) OR escalates too conservatively on HEAT (SIMILARITY floor
  applied). Both degrade the trichotomy. Record both now; build with D.

D3-amended (jurisdiction-conditional E-convergence, D/E seed). The
shared-vs-fork rule is conditional on jurisdiction, not blanket:
  SIMILARITY cases -> CONVERGE (shared-tested-both MANDATORY; the tension
                      must survive; forking risks one branch resolving what
                      must be preserved).
  HEAT cases       -> MAY FORK (context-dependent resolution is correct;
                      both branches carry useful information and can be
                      tested independently).
  Structural basis replaces the blanket rule.

D6 (NEW seed, Sprint 4: E as meta-jurisdictional auditor). The trichotomy
creates three jurisdictions (C/D/shared); something must verify the
ASSIGNMENTS are correct and detect drift. This role falls to E (the
evaluation layer), making E meta-jurisdictional, not just an interlock.
Drift signatures E watches for:
  - a HEAT-assigned case behaving like SIMILARITY (D keeps re-learning the
    same tension without convergence) -> should be reclassified to shared.
  - a SILENCE-assigned case showing HEAT signatures (evidence appearing
    that the static floor was too conservative) -> floor may need review.
  Classification failure is distinct from execution failure; E audits the
  former. Sprint 4 design seed, follows directly from the trichotomy.

## Clarity review round 4 -> adopted (SHIP after these)

C2-amended (ERROR-path transition, CODE). Completes the state machine: the
approved state has THREE exits, all full resets, distinct semantics:
  COMMIT  (success)  -> commit-clear  : op+head matched, batch executed.
  STALE   (timeout)  -> stale-check   : N cycles without commit; too slow.
  ERROR   (failure)  -> error-clear   : execution crashed/failed.
  On execution error: approved -> unlocked, clear &pending_soul_mutation,
  emit ERROR gate-decision. Mirrors STALE's full reset, different meaning
  (STALE = too slow to trust; ERROR = tried and failed). After this, NO
  exit from `approved` strands lock or batch state. Detection: the cycle's
  results carry an Error for the committed batch (the &error channel /
  HandleError path the loop already tracks).

C1-amended-3 (STALE cycles = named constant, CODE). N=20 becomes a named
configurable (soul-mutation-stale-cycles), seeded in initLoop like the
loop's other (maxNewInputLoops)-style constants. Tunable without code
archaeology; default 20 (~one engaged burst).

## Abstraction-level verdict (Clarity) + one D-era seed

C is at the right layer: specifies the STATE MACHINE and CONTRACTS, not
policy. Evolvable by three properties: (a) seams extensible by design
(append-only fields, shape-as-contract); (b) minimal state machine (a 4th
state adds transitions, doesn't replace); (c) sender-agnostic learning
isolates C's governance evolution from D's trust-model stability.

D7 (seed, hierarchical mutation classes). Future: some soul mutations
(skill additions) may warrant a lighter gate than others (value-hierarchy
changes). PASSIVE ACCOMMODATION, not active build: the schema already
carries the fields (gate/phase/op/head/fp) a classifier needs; the
absorption point is ONE conditional checking risk-class BEFORE entering
the lock state machine -- no restructure. NOTE: this is the same SHAPE as
the two-layer learning invariant (CAUTION-band vs static floor), applied
to mutation ENTRY rather than threshold RELAXATION. A risk-classified
fast-path must itself respect a floor (value-hierarchy changes never
fast-path), or it reinvents the gate-that-learns-to-stop-gating at the
entry layer. Record with D2's confidence-floor family.
