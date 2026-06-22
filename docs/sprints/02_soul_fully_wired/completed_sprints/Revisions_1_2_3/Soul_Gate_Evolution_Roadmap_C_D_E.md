# Soul-Gate Evolution: Surfaces C, D, E and the Coda Pivot

**Status:** Build-path decision record. 2026-06-11.
**Destination:** docs/sprints/soul_fully_wired/Soul_Gate_Evolution_Roadmap_C_D_E.md
**Authored from:** Berton's first-principles objections (static gate calcifies;
bare-metal blast radius) + grounding read of Coda Phase A v6, ADR-006,
nace_substrate. Sequence confirmed by Berton 2026-06-11.

## First principle this roadmap serves

Clarity is meant to be an autopoietic system that grows and self-modifies
over time. A last-defense gate is the floor, not the ceiling. A gate that
cannot learn calcifies her into permanent parent-mode: a child forever.
The gate must therefore become a LEARNING surface, while never being able
to lower itself to zero. Two layers, always:
- STATIC FLOOR (human-gated, non-learnable): irreversibility-critical
  mutations always pause. No learning path may relax this.
- LEARNING BAND (CAUTION tier only): the system may learn, from its own
  decision history, that a class of mutation no longer needs to pause,
  proposing relaxations that still surface to a human until a confidence
  bar is met. The learning layer can raise autonomy WITHIN the band; it
  can never reach the floor.

A gate that could learn to stop gating is the most dangerous object in
the architecture. This two-layer split is the invariant that prevents it.

## The sequence (confirmed C -> Coda -> D -> E)

### Surface C -- soul-gate substrate (BUILDING NOW, dependency-free)
The lock, the approve/deny transitions, the proposal fingerprint, the
three-state flow. Governs the `metta` self-mutation channel only.
Independent of Coda by the same logic that lets Coda's informational
first-capability ship before Boundary 1 (Phase A lines 177-179): C
PRODUCES governed soul outputs; it needs no registry to read them.
NEW IN C PER FIRST-PRINCIPLES REVIEW: a decision-record seam. Every
pause/approve/deny emits a structured `(gate-decision ...)` atom and a
journal line: D's future training data, written from day one even though
nothing consumes it yet. C is static-UNTIL-D, not static-forever, and it
starts logging the experience D will learn from immediately.

### Coda -- THE PIVOT (hard dependency under D and E)
Sprint 0 Phase 1 completing what it scoped: the dispatcher's first real
capability, and resolution of Boundary 1 (soul-state atoms become
structurally queryable). Phase A lines 177-179 are explicit: until
Boundary 1 resolves, "the registry cannot enforce safety constraints
structurally, only by convention," and a dispatch-guard deciding on soul
Safety state is BLOCKED. That dispatch-guard is the shape of D and E.
Coda is the last thing C does not need and the first thing everything
past C does.

### Surface D -- NACE gate-learning (needs C's records + Coda's Boundary 1)
NACE learns precondition -> action -> outcome over the gate's decision
history (C's `(gate-decision ...)` atoms). It proposes threshold
relaxations WITHIN the CAUTION band only. Requires: (1) C's decision
records as training data; (2) Coda Boundary 1 so the learner reads soul
verdict state structurally, not by LLM convention; (3) a live capability
dispatcher (NACE has nothing to gate or learn from until capabilities
dispatch through a registry: standing project fact).

### Surface E -- command-execution interlock (needs Coda Boundary 1 AND Phase 1.5)
The soul-gate governs `metta` self-mutation. It does NOT govern `shell`,
`network`, or `delete`. In a container the blast radius is the container.
On bare metal, `shell "rm -rf"` / `curl | sh` reaches the host and the
gate stands in front of NONE of it. E is the structural interlock on the
command channel. HARD PREREQUISITE FOR BARE-METAL DEPLOYMENT.
Requires: (1) Coda Boundary 1 (read soul Safety state structurally);
(2) Coda Phase 1.5 -- ADR-006 Criterion 5: the dispatcher ships with NO
handler error isolation (catch is inert under indirect/reduce invocation;
handler symbols are data). A safety interlock that terminates the chain
silently when it crashes is the worst failure mode. E built before Phase
1.5 is a convention-only gate wearing structural clothes: the exact trap
this roadmap exists to forbid. The kernel-guard chmod-444 is a
single-file bandaid, NOT this system.

## The averted illusion (why order is non-negotiable)

Building D or E before Coda produces gates that LOOK structural but
enforce only by convention (LLM-side classification, not substrate
interlock). That is the same lesson string-contains taught at the
predicate level (always-True, tested only positive), now at the
architecture level. A safety mechanism that trains readers to believe
protection exists where it does not is worse than no mechanism. Coda is
what lets D and E be real.

## Bare-metal standing rule

Until Surface E exists and verifies, Clarity stays containerized. The
soul-gate protects her soul from drift; it does not protect the OS from
her tools. These are different protections and only one of them exists
today.
