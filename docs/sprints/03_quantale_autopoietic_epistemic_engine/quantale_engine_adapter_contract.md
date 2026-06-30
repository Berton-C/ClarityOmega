# Quantale Engine Adapter Contract

This companion contract keeps `lib_quantale_autopoietic_epistemic_dynamics_engine.metta` pure while letting skills and writers use it safely.

## Boundary

The engine computes pbits, classifications, phase signals, and next-move affordances. It does not mutate atomspace and does not write files.

Skills may call the engine. Writers may persist the result. The writer is responsible for substrate-safe mutation.

## Core law

Do not pin the disposition surface. Make it visible through trajectory, but do not schema it as a fixed object. The soul sees and decides; the engine computes legibility; the LLM renders.

## Safe persistence discipline

When a writer persists engine outputs:

1. Read scalar/symbol fields individually.
2. Do not match-return whole `(stv ...)`, `(mk-pbit ...)`, or larger compounds.
3. Do not use `set-atom!` for revision.
4. Remove by variable value, then add exactly one new atom.
5. Verify in a separate command using a proven scalar/symbol read.
6. Use absolute paths for durable file writes in the PeTTa runtime.

## Recommended persisted field shapes

Prefer flat fields:

```metta
(engine-signal $cycle $signal-symbol)
(engine-pbit-strength $cycle $name (stv $s $c))
(engine-pbit-confidence $cycle $name (stv $s $c))
(engine-next-move $cycle $move-symbol)
(engine-phase $cycle $phase-symbol)
(engine-profile $cycle $profile-symbol)
```

Avoid persisting opaque whole structures unless your read strategy for that structure has been proven in the substrate map.

## Cycle-trace interlock

The cycle-trace writer should emit flat trajectory atoms matching detector contracts, such as:

```metta
(recent-action $cycle-id $action-type $description)
(state-delta $cycle-id $delta-key $delta-value)
(cycle-phase $cycle-id $phase-symbol $description)
```

The engine consumes legible trajectory signals produced from these atoms. It does not produce the trace itself.

## Skill-call convention

A skill should ask the engine for one or more of:

- `q-profile-action`
- `q-support-status`
- `q-contradiction-status`
- `q-selfview-status`
- `q-binding-status`
- `q-action-test-status`
- `q-phase-next-move`
- `q-next-epistemic-move`
- `q-next-action-boundary`
- `q-next-learning-move`
- `q-skill-signal`

Then the skill renders or routes the result. The LLM does not decide the soul verdict; it renders what the soul-facing substrate makes visible.

## Durable autopoietic learning adapter

Section 15 of the engine now distinguishes pressure, trace, learning, and growth:

- learning pressure is not learning;
- a durable trace is not yet growth;
- learning is perturbation metabolized into durable future-informing trace;
- growth is learning that expands future visibility, changes future action boundaries, or is built on by later cycles while preserving soul-aligned continuity.

The engine may return symbols such as:

```metta
learning-pressure-present
trace-required
durable-learning-candidate
awareness-expanded
action-boundary-shifted
built-on-by-later-cycle
growth-detected
soul-aligned-growth
pathological-learning-risk
cross-network-divergence-risk
network-learning-update
```

A learning writer should persist these as flat, non-dispatch atom families. Suggested shapes:

```metta
(q-learning-observation $cycle $event-kind $target $source-scope)
(q-learning-evidence-strength $cycle $name (stv $s $c))
(q-learning-event-trigger $cycle $trigger)
(q-learning-event-before $cycle $before-symbol)
(q-learning-event-after $cycle $after-symbol)
(q-learning-event-residue $cycle $residue-symbol)
(q-learning-event-lineage $cycle $lineage-symbol)
(q-awareness-delta-observation $cycle (stv $s $c))
(q-action-boundary-shift $cycle $shift-symbol)
(q-learning-builds-on $cycle $prior-cycle)
(q-network-learning-update $network $rule-id $prior-symbol $posterior-symbol $evidence-symbol)
(q-cross-network-divergence $rule-set-a $rule-set-b $evidence-symbol)
```

Persist with the same safe discipline: read scalar/symbol fields, remove the keyed family by variable value, add exactly one revised atom, then verify separately. Do not use swept `dispatch-*` atom families for durable learning. Capability-registry efficacy learning, per-network NACE learning, and three-cycle task-state learning should all use the same pattern while keeping their atom families distinct.
