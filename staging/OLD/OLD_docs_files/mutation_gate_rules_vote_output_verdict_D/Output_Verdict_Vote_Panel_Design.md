# Output Verdict Evolution: The Layered Vote Panel

**Status:** DESIGN ARTIFACT. Not a build plan. Defines what, why, and where-it-fits.
Build-sequencing and the floor-veto mechanism are deliberately left open, to be
resolved at implementation time when the surrounding substrate (D, soul_eval,
Boundary 1) has evolved enough to make the right path visible.
**Created:** 2026-06-13.
**Family:** Soul-gate evolution (sibling to Surfaces D and E in
`Soul_Gate_Evolution_Roadmap_C_D_E.md`). This is the OUTPUT-side governance
evolution; it is the surface D's learned assessment plugs into.
**Supersedes:** the staged `mutation_gate_staged_work.md` vote-gate package
(2026-05-26) as a drop-in. See section 6.

---

## 1. What this is

The output verdict (`compute-output-verdict` in `soul/output_verdict.metta`,
live since Repair 1, 2026-06-10) decides PROCEED / FLAG / PAUSE on the LLM's
proposed command batch before it executes. Today it is a deterministic RULE
LADDER: seven ordered rungs, first match wins, catch-all defaults to FLAG.

This artifact defines its evolution into a LAYERED VOTE PANEL: a small set of
typed voters whose assessments resolve to a verdict, where the ladder becomes one
privileged voter (the floor) rather than the whole mechanism.

This is not "replace the ladder with a vote." It is "make the ladder the floor
voter inside a vote frame that can admit other voters as the system grows."

## 2. Why (the first-principles case)

### Rules enumerate; growth is unenumerable

A rule ladder governs exactly the cases someone enumerated in advance. Anything
unforeseen falls to the catch-all (currently FLAG). For a fixed surface that is
fine. For an autopoietic system meant to grow and self-modify into the unknown
(the roadmap's first principle), a governance surface that can only handle
pre-enumerated cases is a structural ceiling: it cannot get better at judging
novel situations, only at flagging them as unclassifiable.

### A vote degrades gracefully on the unforeseen, and extends by adding voters

A vote does not ask "which rule matches." It asks "what do the assessments,
together, conclude." A novel command that fits no clean rule is still ASSESSED by
whatever voters exist, and the resolution surfaces a real verdict rather than a
blind catch-all. New dimensions of judgment enter as new VOTERS (atoms), not as
new branches edited into a ladder (code). This is the same extensibility shape as
the Capability Registry (capabilities as atoms) and the roadmap's learning band:
the surface evolves without being re-architected.

### The brittleness-relocation trap (why the staged vote-gate alone was not enough)

A vote is only as good as its voters. If the voters are themselves static
hardcoded rules, the vote is brittleness relocated one level up: the same
enumeration problem wearing a tally. The staged vote-gate package had the FRAME
instinct right but left the voter question unanswered, which is exactly this trap.
The synthesis in this artifact resolves it by TYPING the voters to the roadmap's
two layers, so at least one voter (the floor) is deterministic-by-design and at
least one class (the band) is learning-by-design.

## 3. The synthesis: a layered vote panel

The vote frame composes typed voters. Each voter is an assessment that returns a
verdict-leaning signal; the frame resolves them, subject to the two-layer
invariant from the roadmap (STATIC FLOOR + LEARNING BAND).

### Voter typology

**Floor voter (deterministic, veto, never learns).** The current ladder's
irreversibility-critical rungs become this voter: soul-namespace mutation,
elevated-shell, write-to-soul-namespace. These are the roadmap's STATIC FLOOR.
This voter's negative verdict cannot be overridden by any tally. It is the
"irreversibility-critical mutations always pause; no learning path may relax this"
invariant, implemented as a privileged voter rather than as a threshold.

**Soul-eval voter (substrate-native soul reasoning).** `compute-soul-verdict` in
`soul_eval.metta` is a pure-MeTTa, LLM-free verdict path (tier-A gaps, tensions,
paraconsistency, priority-weights, irreversibility-levels, person-state
modulation). Today it is a v1 sketch with hardcoded calibration baselines and an
unproven aggregation rule (per the Verdict Surface Survey). When it matures it is
a DIFFERENT KIND of voter than the ladder: the soul reasoning structurally, not
classifying by command type. It is the F-SOVEREIGNTY direction (LLM-free verdict)
expressed as a voter.

**Learned voter(s) (NACE / Surface D, votes within the CAUTION band only).** D
learns precondition -> action -> outcome over the gate's `(gate-decision ...)`
records (emitted by Surface C from day one). A learned voter proposes moving a
CAUTION-tier verdict toward PROCEED as confidence accumulates. It is
STRUCTURALLY INCAPABLE of touching anything the floor voter vetoed: it votes only
within the band. This is the roadmap's "learning layer can raise autonomy within
the band; it can never reach the floor."

### Why the synthesis beats either alone

- The ladder alone cannot admit the soul-eval voter or the learned voter without
  becoming a different thing; it is a structural ceiling on judgment.
- The staged vote-gate alone left voters untyped (brittleness relocated).
- The layered panel keeps the ladder's determinism EXACTLY where it must live
  (the irreversibility floor) and gains the vote's graceful-on-the-unforeseen
  behavior EXACTLY where it is wanted (the CAUTION band, where D learns). Neither
  brittleness nor unsafety survives: the floor has veto; the learned voters are
  confined to the band.

## 4. Where it fits with Surface D (the dependency relationship)

D and this evolution are intertwined but not identical, and the dependency runs
one direction:

- **The vote FRAME is the surface D learns INTO.** D's learned assessments are
  band-voters; they need a vote frame to be votes. Right now the output verdict
  is a hardcoded ladder with NO learning affordance: there is nowhere for a
  learned assessment to plug in. The vote frame creates that affordance. So the
  frame is, in effect, the output-side expression of the roadmap's learning band.
- **The learned VOTERS are D.** They depend on D's machinery (NACE over the
  decision records) and therefore on D's prerequisites: Surface C's
  `(gate-decision ...)` records (already emitting) and Boundary 1 (so the learner
  reads verdict state structurally, not by LLM convention). Boundary 1 is held by
  Sprint 1 (per the corrected sequence C -> Coda -> Sprint 1/Boundary 1 -> D).
- **Therefore:** the FRAME (with the floor voter and, when ready, the soul-eval
  voter) can exist ahead of D. The LEARNED voters land with D. The frame is not
  blocked on Boundary 1; the band-voters are.

This is the same relationship the roadmap already names between the static floor
and the learning band, applied to the output verdict specifically. It is also the
output-side sibling of Extension D (the dispatch-guard), which is the action-side
consumer of governance atoms: both are governance-consumption surfaces that
Boundary 1 + D make real.

## 5. Prerequisites (what gates what)

| Element | Depends on | Buildable when |
|---|---|---|
| Vote frame (resolver + voter interface) | the current ladder rungs (exist) | ahead of D; needs no Boundary 1 |
| Floor voter | the ladder's irreversibility rungs (exist) | with the frame |
| Soul-eval voter | `soul_eval.metta` maturing past v1 (live baselines, proven aggregation) | when soul_eval is real (independent track) |
| Learned band voter(s) | Surface D: C's `(gate-decision ...)` records + Boundary 1 (Sprint 1) | with / after D |

The decision-record seam Surface C already ships is the training data for the
learned voters; it is being written now even though nothing consumes it yet. That
is the roadmap's "static-UNTIL-D, logging the experience D will learn from
immediately" applied here: the output verdict's evolution is being fed before it
is built.

## 6. Disposition of the staged vote-gate package

The staged package (`mutation_gate_staged_work.md`, 2026-05-26:
`parallel_vote_gate.metta`, `vote_threshold.metta`, `vote_gate_bridge.py`,
`gate_integration_wiring.metta`, `test_boundary.py`, `gate_rules.json`) is
SUPERSEDED AS A DROP-IN. Its founding premise -- "replace the hardcoded PROCEED in
soul_verdict_out" -- is void: Repair 1 already replaced that constant with the
live `compute-output-verdict` ladder, with a different design, on 2026-06-10.

What is VOID: the "replace hardcoded PROCEED" premise; the assumption of a
`soul_verdict_out` shaped as a constant; the 0.986 synthetic validation (it
validated against a substrate that no longer exists).

What is SALVAGEABLE and folds into this artifact:
- The vote-frame instinct itself (the core of this synthesis).
- The config-driven rules idea (`gate_rules.json`): thresholds and resolution
  rules in config, not hardcoded in the resolver. The current ladder hardcodes its
  rungs in MeTTa; a config-driven resolver is the better long-term shape and is
  worth carrying into the frame design.
- The boundary-test discipline (the vote-tally fixture table): a good testing
  pattern for the resolver, reusable.

Recommendation: archive the staged package with a dated note pointing here, rather
than validating or shipping it. Its model lives on in this artifact; its code is
built against a dead slot.

## 7. Open questions, deliberately deferred to implementation time

These look like design forks now. They are not to be litigated now. The
surrounding substrate (D's actual shape, soul_eval's maturity, Boundary 1's actual
atom shape) will have evolved by the time this is built, and the investigation
process at build time will reveal the correct path -- or dissolve the question.
Imposing an answer now only forces re-litigation later against a moved substrate.
Recorded so they are not forgotten, NOT so they are decided:

- **Floor-veto mechanism.** Does the floor voter's veto compose as a hard
  short-circuit (floor PAUSE -> done, skip the tally) or as a veto-weighted vote
  (floor participates with override weight)? Short-circuit is simpler and more
  obviously safe; veto-weighted is more uniform. Resolve at build, when the voter
  set is concrete.
- **Resolver shape.** Threshold-count (the staged table's 4-0/3-1/2-2 style),
  weighted sum, or tiered (floor first, then band)? Depends on how many voters
  exist and what their signals look like, which is not known until they exist.
- **Verdict signal type.** Do voters return PROCEED/FLAG/PAUSE tokens, or a
  graded confidence the resolver thresholds? The graded form composes better with
  D's confidence-based band relaxation, but commits more now than is warranted.
- **Build sequencing.** Frame-first (ahead of D) vs one-piece (with D). The frame
  is buildable ahead, but whether it is WORTH building ahead of having any band
  voter to put in it is a judgment best made when D's timing is clearer.
- **Backward compatibility.** The resolver's output must remain consumable by the
  live `soul-proceed?` / `soul-flag?` / `soul-pause?` predicates (and by Repair 3's
  PAUSE routing), or those consumers migrate in lockstep. This is a constraint, not
  a fork, but it is named here so it is not discovered late.

## 8. The one-line summary

Evolve the output verdict from a rule ladder into a layered vote panel where the
ladder is the floor voter with veto, soul-eval is a substrate-native voter, and
Surface D supplies learned voters confined to the CAUTION band -- the vote frame
being the composition surface that the roadmap's two-layer invariant requires and
that D's learning plugs into. Build the frame and floor ahead if worthwhile; land
the learned voters with D; resolve the veto mechanism and resolver shape at
implementation time, not now.
