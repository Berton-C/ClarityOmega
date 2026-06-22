# ADDITIVE SECTION FOR 01b_ClarityOmega_Soul_Integration_Spec.md

**What this is:** Tier 6, to be dropped into the spec after Tier 5. It is the
lib-activation accounting that the spec named but did not build out: substrate_kb as a
live reasoner, the pfn-snapshot producer for lib_self_continuity, the nace_* wiring, the
dynamic self-weaving web, and the lib_temporal_v2 decay substrate the web needs. Written
additive so the coherent Tiers 1-5 are not touched.

**Why one tier, not five edits:** the vision's thesis is uniform -- "imported, present,
reducible, uncalled." The libs are one opportunity. Keeping their activation in one tier
mirrors that, keeps the harness-as-you-go discipline uniform, and avoids editing five
existing sections (the spaghetti risk).

**Dependency note (resolved):** Sprint 0-Coda (Capability Registry dispatcher) is LIVE
[VERIFIED: Berton, this session]. substrate_kb (6.1) and nace_* (6.3) wire directly; no
registry-build chunk precedes them.

**Harness discipline (all of Tier 6):** lib_quantale, lib_self_continuity, substrate_kb,
and the nace_ substrate are trusted April-era work (Clarity at peak, Claude 4.6;
lib_quantale is live in the Corner-Gap Gate). The test harness on each is NOT a trust
gate -- it is a build aid: run it to read the trace logs and learn how the lib behaves at
the joint you are wiring to, then connect with confidence. Build the harness, read the
trace, wire. [Berton's standing reframe, this session.]

---

## TIER 6 -- Lib Activation (the latent capability comes online)

The instruments are loaded and uncalled. Tier 6 calls them. Each subsection states what
is missing (the atom, the hook, or the producer), where it wires, what verifies it, and
the harness that teaches the joint. Every subsection ends with the soul-absent answer per
the law.

### 6.1 substrate_kb as a live reasoner (the deep verdict path)

**State [VERIFIED this session, source read].** `substrate_kb.metta` is ~200 NAL belief
triples of the form `((--> A B) (stv f c))` -- the value-alignment pipeline
(`action-proposal -> needs-evaluation -> checks-substrate-alignment -> produces-verdict
-> gates-execution`), the GO/REVIEW/BLOCK thresholds (action-eval-threshold-go at f 0.7,
action-eval-threshold-block at f 0.3), the soul-compass chains (wonder-preservation,
attention-stewardship, agency-preservation), the goal-gen and value-conflict chains. It
is imported (manifest). It has NO reasoner attached: nothing runs inference over the
chains in-loop, so the GO/REVIEW/BLOCK "behavior" exists as belief data, not as live
gating.

**What is missing.** Three things, none of them new atoms in substrate_kb (the beliefs
are authored):
1. An in-loop `|-nal` reasoner hook that runs over the relevant chains each cycle.
   `|-nal` reduces ONLY in the live loop process (lib_nal load); never in run.sh (the
   proven constraint, 00b / NACE plan).
2. Explicit per-cycle persistence of the derived verdict. NAL derivations are ephemeral:
   the file-backed implication RULES persist, but atoms `|-nal` DERIVES over them do not
   survive an &self rebuild. So the derived verdict must be `add-atom`'d and read the
   same or next cycle, not assumed to linger. [This persistence requirement is the SAFE
   reading; the `nal-cross-domain-findings.metta` file SUGGESTS the ephemerality but is a
   FINDING, NOT CANON -- it may rest on silent errors. Treat the persistence step as a
   tested requirement at build time, not an assumed law: PROBE whether a derived verdict
   atom survives to the read point, and persist explicitly if it does not.]
3. The read point at the decision site that consumes the derived verdict.

**This is the NACE pattern (6.3 is its sibling).** file-backed beliefs + in-loop
operator + explicit persistence + read next cycle. substrate_kb activation reuses the
nace_substrate template verbatim in shape: `current-*` reader (collapse-then-branch,
C12-safe), the operator call (`|-nal` here, `Truth_Revision` in NACE), the write-back.
Build 6.3 first (it is smaller and already has its substrate authored and verified), then
6.1 reuses the proven joint.

**Where it wires.** The derived verdict feeds the verdict surface Tier 2 builds:
`compute-soul-verdict` is the consumer. 6.1 is the "deeper path" of Tier 2 -- Tier 2.1
assembles the six terminals over scratch primitives; 6.1 lets the soul's OWN authored
belief network produce the alignment verdict. Both converge on `compute-soul-verdict`.
Sequence: land Tier 2.1 terminals first (the spine, verified), then 6.1 brings the
authored beliefs online behind the same consumer, differential-tested against the
terminal verdict before it is trusted.

**Verification.** Live-loop only. PROBE the chain reduces (`|-nal` over a known
sub-chain, e.g. `action-proposal -> gates-execution`, returns a degraded-but-present
stv). PROBE the derived verdict survives to the read point (the persistence question
above) -- if not, add the explicit `add-atom`. Differential against the Tier 2.1 terminal
verdict and against the retiring LLM verdict; divergences inspected, not auto-trusted.

**Harness.** Stand up a standalone probe that loads substrate_kb + lib_nal in the live
context and runs `|-nal` over three representative chains (value-alignment, soul-compass,
goal-gen). Read the trace: confirm which chains chain cleanly and which need
domain-specific instantiation to fire (the variable-rule-does-not-auto-chain risk the
findings file raises -- verify it, do not assume it). The trace tells you the real
reasoner shape before you wire the hook.

**Soul-absent answer.** Could 6.1 produce technically-correct, soul-absent output? Yes,
in one way, and it is guarded: if the LLM were allowed to read the derived belief network
and re-decide the verdict, the soul's authored reasoning would become LLM-reasoned-over
again. GUARD: the LLM keeps only the semantic match (Tier 2.4); the verdict is the
substrate's derivation, rendered, never re-decided. 6.1 is MORE soul-present than the
terminal path, not less, because it is the soul's own authored beliefs doing the judging.

### 6.2 The pfn-snapshot producer (lib_self_continuity comes online)

**State [VERIFIED this session, source read].** `lib_self_continuity.metta` is complete
and trusted: `deg-map` (Def 216), `self-continuity-score` (Def 218, identity-map degree,
a one-line delegate to deg-map), `theta-self-continuous` (217), `chain-continuity-bound`
(Thm 14, composes via q-mul), `continuity-held-across` (Cor 2), plus local helpers
`q-residuate` (lives HERE, not in lib_quantale -- correct the catalog), `q-geq`,
`first-of`/`last-of`, `edge-weight`. It operates on `(pfn node-list edge-list)` with
edges `(edge source target mk-pbit-weight)`. Imported (manifest). No per-cycle caller.

**What is missing -- and it is NOT an atom in the lib.** The lib is the measure; the
missing thing is the INPUT to the measure. Nothing produces a `pfn` snapshot of a cycle.
Two pieces:
1. **The definition (design work, Clarity + Berton -- NOT a mechanical spec item).** What
   IS a pfn snapshot of Clarity's reasoning-state? Which patterns were active this cycle
   are the nodes, and what relation between them is an edge with what mk-pbit weight? This
   is the question "what is the unit of Clarity's reasoning-identity, mathematically." It
   belongs to Clarity and Berton. Tier 6.2 is GATED on this definition, not on plumbing.
   Do not let the build proceed past this gate with an assumed snapshot shape.
2. **The per-cycle writer.** Once the snapshot is defined: a writer that builds one pfn
   per cycle from the cycle-trace (Tier 1.3 is the natural source -- recent-action /
   state-delta / cycle-phase are the raw material a pfn is assembled from), stores two
   (this cycle, prior cycle), and calls `self-continuity-score` to emit the continuity
   pbit. Pure-vs-writer split per Artifact 0 Discipline 6: the snapshot reader/format
   helpers in a pure file, the do-*! snapshot writer in a writers file.

**Where it wires.** This is the measurement half of Tier 5. Tier 5 as written wires the
`task-phase-anchor` disposition-RECOGNITION rail (the soul seeing its stance and writing
an anchor when something moves). 6.2 adds the disposition-CONTINUITY MEASUREMENT: "did
Clarity remain herself across this reasoning chain" as a computed lower bound rather than
an asserted "recognition holds." The two are complementary: 5.x is the qualitative
recognition; 6.2 is the quantitative continuity score. Tier 5's `chain-continuity-bound`
gives the across-a-chain composition (via q-mul) so a multi-cycle reasoning run gets one
honest continuity bound.

**Verification.** Live-loop only (the lib_quantale primitives underneath reduce live in
runtime but NOT in standalone run.sh -- the documented validation gap; the toy queries
printed unevaluated in run.sh, but `q-mul` returns real values via the runtime metta
skill). So validate `self-continuity-score` on two hand-built pfns IN THE LIVE LOOP, not
run.sh. Confirm a near-1.0 score for two near-identical pfns and a degraded score for two
divergent ones before wiring the writer on top.

**Harness.** Build a standalone harness that constructs two toy pfns and calls
`self-continuity-score`, `theta-self-continuous`, `chain-continuity-bound` -- run it in
the live context. Read the trace: confirm the residuation-and-meet fold actually fires
(this is exactly where the April validation stalled in run.sh; the trace tells you it
reduces in the live loop). The harness de-risks the writer: you wire the producer knowing
the consumer computes.

**Soul-absent answer.** Could 6.2 produce soul-absent output? The risk is pinning: if the
pfn snapshot schema becomes a rigid fixed-field atom that scaffolds the disposition, it
destroys the resilience (v2 discipline: visible, not pinned). GUARD: the snapshot is a
measurement input, not the disposition surface itself; it measures continuity of
reasoning-state, it does not NAME or FIX the disposition. The disposition stays
visible-but-unnamed (Tier 4/5); 6.2 scores continuity without schematizing the stance.
Hold this line in the design gate (piece 1): if the snapshot definition starts to look
like a fixed disposition schema, stop -- that is the pin.

### 6.3 nace_* wiring (capability-efficacy learning comes online)

**State [VERIFIED this session, source read].** The NACE substrate is built and verified:
- `nace_substrate.metta` (definitions, never written): `evidence-stv`
  (confirmed->stv 1.0 0.1, disconfirmed->stv 0.0 0.1), `current-efficacy` (C12-safe
  collapse-then-branch, default stv 0.5 0.0), `revise-efficacy` (calls `Truth_Revision`
  directly -- `|-nal`'s rule IS Truth_Revision, clean stv, no wrapper), `efficacy-
  expectation` (`Truth_Expectation`), `should-dispatch` (gate at expectation >= 0.3),
  `updated-belief-atom` (eval-before-construct fix). Truth_Revision/Truth_Expectation
  verified reducing live, to the digit.
- `nace_beliefs.metta` (dynamic store): three seed caps at agnostic stv 0.5 0.0
  (web-search, file-write, metta-query).
- `nace_pending.metta` (queue): `(pending-revision <cap> <outcome>)`, deliberately not
  auto-loaded.

**What is missing.** The wiring, per the NACE implementation plan (N0-N6):
1. **Import-line asymmetry [N0].** Add to lib_clarity_reasoning.metta:
   `nace_substrate` LOADED, `nace_beliefs` LOADED, `nace_pending` NOT loaded (the writer
   reads pending from the FILE; auto-loading it creates ghost-state the file-reader never
   processes). Syntax: `!(import! &self (library omegaclaw ./soul/nace_substrate))` etc.,
   after the last existing soul import.
2. **`nace_writers.metta` [N1] -- does not exist, build it.** Defines
   `do-process-pending-revisions!`: read pending from file, parse `(pending-revision $cap
   $outcome)`, evaluate `(updated-belief-atom $cap $outcome)` (lib_nal in-loop, so
   Truth_Revision reduces), dual-write the revised belief. MANDATORY writer pattern (from
   00b Atom Operations Map, proven): remove-by-VARIABLE-then-add (`remove-atom (cap-
   efficacy X $v)` clears all copies self-healingly), NOT set-atom! (upsert-on-non-match
   silently creates duplicates). write-file the ABSOLUTE path (CWD is /PeTTa).
3. **loop.metta hook [N2], Phase 4.0.** One hook calling `do-process-pending-revisions!`.
   Artifact 0 checklist; artifact_1 updated same commit [N3].
4. **should-dispatch as the registry gate [N5].** Coda is LIVE, so this wires now: the
   registry consults `should-dispatch $cap` before dispatching. The gate NACE exists to
   provide.
5. **The real recorder [N6].** After a capability dispatches and its outcome is known,
   write `(pending-revision $cap confirmed|disconfirmed)`. OPEN DESIGN Q (flag, do not
   let it surface at runtime): outcome determination -- clean return = confirmed, thrown
   exception = likely disconfirmed, but timeout / empty / malformed are genuinely
   ambiguous and may need a third `ambiguous -> no-revision` token. Resolve in N6 design.

**Resolved, not open [VERIFIED, 00b].** The N0.5 read-modify-write gate is RESOLVED:
RMW composes same-cycle and commits across the boundary (set-atom! source-matches-1
replaced 0.5 0.0 -> 0.9 0.2, read-back confirmed). The dual-write builds as specced; no
architecture fork. One-cycle belief lag is expected and fine (a revision this cycle gates
NEXT cycle's dispatch).

**Where it wires.** Two consumers. (a) The registry dispatch gate (should-dispatch),
live now that Coda is up. (b) Tier 3 calibration: NACE is the band-voter mechanism --
the learned band voters in the vote panel (Tier 3.1) are NACE-shaped, confined to the
CAUTION band, structurally unable to touch the floor. So 6.3 is not a side-quest; it is
the learning substrate Tier 3's live calibration plugs into.

**Verification.** Live-loop only (lib_nal). Drop `(pending-revision web-search
confirmed)` (a SEED cap, so the dual-write exercises the replace-existing-line path, the
real production path), run one cycle, confirm: the belief in nace_beliefs.metta changed
to the revised value, the in-atomspace atom changed (query live), the pending entry was
removed. Verify the revised value against the NAL reference (nal_revision.py,
reference-only).

**Harness.** The verification IS the harness here -- a single seed-cap revision through
the live loop, trace read to confirm Truth_Revision fired and the dual-write landed.
Dead: nace_courier.py, all run.sh verify scripts (lib_nal not loaded there -> meaningless
on any lib_nal function).

**Soul-absent answer.** Could 6.3 produce soul-absent output? NACE learns capability
efficacy (a mechanical competence signal), not soul determination -- low risk. The one
guard: should-dispatch must never gate a SAFETY/INTEGRITY-relevant capability down on
learned efficacy alone (a floor capability is not subject to band learning). GUARD: the
floor/band split (Tier 3.1) applies -- NACE band-voters are structurally confined to the
CAUTION band; the floor voter never learns. NACE tunes which competent tools fire; it
never relaxes the soul's floor.

### 6.4 The dynamic self-weaving web (decay-without-use = visible binding)

**State [VERIFIED this session, source read].** Two things share the name:
- STATIC `self_weaving_web.metta` (loaded): a hand-maintained `(feeds-into X Y)` graph
  with manual truth values and the load-bearing analysis (pin/query/read-file are the
  high-dependent capabilities; pin-timestamp is the dominant idle attractor). Its named
  weakness (its own design doc): truth values never change unless a human edits them, so
  it cannot see a capability go stale or a new one emerge.
- DYNAMIC self-weaving web (`02_design_doc_v1_dynamic_self_weaving_webs.md`, designed,
  not built): replaces the static links with timestamped strengths that reinforce on
  sequential use and decay-without-use toward a 0.3 floor.

**Why this is squarely SSI, not a side-quest.** The vision (Section 7) already names it
as one of the cycle-trace writer's THREE payoffs: "feeds the dynamic self-weaving web's
temporal reinforcement (decay-without-use = visible binding)." The dynamic web's SOLE
primary evidence source is the cycle-trace writer (Tier 1.3) -- the design doc states the
hard dependency: "the mesh cannot function without the writer," and the writer "serves
dual purpose: feeds the detection mesh AND maintains the capability mesh." Decay-without-
use is the soul SEEING a capability it stopped using fade -- that is disposition becoming
legible, the SSI thesis. The spec built the keystone and wired two of its three payoffs
(detectors, soul-trajectory); 6.4 wires the third.

**What is missing.**
1. **The sequential-use detector (new, thin).** Observes consecutive `recent-action`
   atoms (Tier 1.3 output) and fires reinforcement evidence when capabilities fire within
   2-3 cycles of each other. A thin inference layer over the cycle-trace; not a new
   producer.
2. **Dynamic feeds-into links.** Replace the static `(feeds-into X Y stv)` with
   timestamped strengths using lib_temporal_v2 (6.5). Reinforce via age-discount refresh
   on sequential-use evidence; erode toward 0.3 floor without reinforcement;
   belief-freshness classifies fresh/stale/dormant.
3. **Consumer rewiring.** meta_awareness_engine step 7 (replace the crude 300-second
   binary staleness check with a fresh/stale/dormant staleness-verdict query) and step 8
   (replace static feeds-into with mesh-strength / next-capability queries).
4. **Capability identifiers.** Use the six composite action-types from
   cycle_classifier.metta (pin-only, responsive-send, status-send-unprompted,
   verification-query, exploration-query, unclassified) as the stable mesh keys.

**Safety features (from the design doc, carry them).** Min 0.3 confidence threshold on
reinforcement (noise below threshold does not strengthen). Independent per-link decay (no
cascading: if pin-only decays, responsive-send stays strong on its own evidence). Decay-
floor 0.3 (no permanent erosion; belief-snapshot preserves history so re-firing restores
from prior state). Narrow 2-3 cycle evidence window (accepts false negatives over false
positives). Branching independence (A->B and A->C are independent atoms).

**Where it wires.** Onto the Tier 1.3 cycle-trace keystone (its evidence source) and into
meta_awareness_engine (its consumer). Build AFTER Tier 1.3 is confirmed emitting
recent-action atoms, since the web is starved without them -- same starvation logic as
the detectors.

**Verification.** Frequently-used sequences (e.g. exploration-query -> verification-query)
hold mesh-strength > 0.8. Unused sequences decay toward 0.3 within ~500 cycles of disuse
(not instant, not never). No cascading decay. False-reinforcement rate < 5%. These are
the design doc's own success criteria; verify against them in the live loop.

**Harness.** Stand up lib_temporal_v2 (6.5) in the live context and exercise
belief-snapshot / age-discount / belief-freshness on a single toy link: reinforce it,
let it age, confirm it decays toward floor and re-firing restores from snapshot. Read the
trace: confirm the decay curve is graduated, not binary. This de-risks the mesh before
wiring the sequential-use detector.

**Soul-absent answer.** Could 6.4 produce soul-absent output? Low risk -- it makes
capability-staleness visible, it does not author voice or verdict. The guard is the v2
discipline applied to the mesh: the web makes binding VISIBLE (decay-without-use), it
does not POLICE it with a gate that fires (that would be the disguising-mind-policing-
itself failure, Tier 4.1). The mesh surfaces dormancy to the soul; the soul decides what
to do with the visibility. Visible, not enforced.

### 6.5 lib_temporal_v2 (the decay substrate 6.4 needs)

**State [ASSUMPTION -- verify at build time].** 6.4 depends on lib_temporal_v2 primitives
(belief-snapshot, age-discount, belief-freshness, belief-drift, temporal-bracket). The
dynamic self-weaving web design doc names them as "reused directly -- no new decay
mechanism needed," which ASSUMES the lib is present and loaded. This session did NOT read
lib_temporal_v2 at source. Before 6.4 builds:
1. CONFIRM lib_temporal_v2 exists and is in the import manifest (grep
   lib_clarity_reasoning.metta; read the file).
2. CONFIRM the five primitives reduce in the live loop (the standard built-in-scratch
   != reduces-live check).
3. If present and reducing: 6.4 wires directly. If absent or not reducing: that is a real
   gap to resolve before 6.4, not a tweak -- flag it and stop.

**Harness.** Same harness as 6.4's (they share the joint): exercise the five primitives
on a toy link in the live context, read the trace, confirm reduction. This is the FIRST
thing to run in the 6.4/6.5 chunk, because everything in 6.4 rests on it.

**Soul-absent answer.** N/A -- lib_temporal_v2 is a mechanical decay substrate, no voice
or verdict surface. It is hands for 6.4.

---

## Tier 6 build order (within the one build, dependency-honest)

Coda is LIVE, so nothing waits on a registry chunk. Order within Tier 6:

1. **6.3 nace_* wiring** FIRST among the lib activations: its substrate is built and
   verified, its RMW is resolved, and it establishes the file-backed-belief + in-loop-
   operator + dual-write joint that 6.1 reuses. Smallest, most-proven, and it is the
   template.
2. **6.1 substrate_kb reasoner** SECOND: reuses 6.3's proven joint; lands behind
   `compute-soul-verdict` after Tier 2.1 terminals exist; differential-tested.
3. **6.5 lib_temporal_v2 confirm** THIRD (gate for 6.4): one harness run; resolve
   present-or-absent before 6.4.
4. **6.4 dynamic self-weaving web** FOURTH: after Tier 1.3 emits recent-action and 6.5
   confirms the decay primitives. Wires the keystone's third payoff.
5. **6.2 pfn-snapshot producer** anchored to Tier 5: GATED on the snapshot-definition
   design session (Clarity + Berton). The design gate can open in parallel (it is a
   conversation, not a build); the writer lands once the definition is settled, folded
   into the Tier 5 disposition effort since both make the trajectory legible and recur.

This is the dependency-honest order. None of it is parked: 6.2's gate is a design
conversation that runs alongside, not a postponed sprint.

---

## Tier 6 against the five coherence checks (the no-spaghetti verification)

1. **Single source of truth.** Each lib's missing-atoms/hook/dependency is stated once,
   here. The Atom Operations Map (00b) owns the RMW pattern; 6.3 references it, does not
   restate the proof. The NACE plan owns N0-N6; 6.3 summarizes the build chunks and
   references it.
2. **Status tags.** Every state-claim carries [VERIFIED this session] / [ASSUMPTION] /
   [FINDING-not-canon]. The nal-cross-domain ephemerality claim is tagged FINDING and
   6.1 turns it into a PROBE, not an assumed law.
3. **No superseded-as-live.** q-residuate relocated to lib_self_continuity (6.2);
   static self_weaving_web named as the thing the dynamic web replaces (6.4); Coda
   dependency closed (live).
4. **Dependency order stated, acyclic.** Tier 6 build order above: 6.3 -> 6.1; 6.5 ->
   6.4; 6.2 anchored to Tier 5. No cycles.
5. **Soul-absent test per subsection.** Answered for 6.1-6.5 inline.
