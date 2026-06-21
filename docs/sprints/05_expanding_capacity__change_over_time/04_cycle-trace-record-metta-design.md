# `cycle-trace-record`: MeTTa Implementation Design

## 1. Purpose

`cycle-trace-record` provides per-cycle trace atoms in the atomspace for self-observation. Each loop cycle emits structured atoms recording what happened, what changed, and what phase the system is in.

These atoms support:

| Capability | Description |
|---|---|
| Drift detection | `state-delta` chains reveal accumulating shifts across cycles. |
| Behavioral auditing | `recent-action` atoms enable retrospective analysis of action distributions. |
| Phase awareness | `cycle-phase` atoms let `soul-pre-compute` and other substrate capabilities reason about system state. |
| Temporal decay | Integration with `lib_temporal_v2` ensures stale trace atoms fade rather than accumulate indefinitely. |

---

## 2. Atom Schema

Three atom types are keyed by cycle number:

```metta
((--> (recent-action $cycle) $action-type) (stv 1.0 $conf))
((--> (state-delta  $cycle) $delta-key)   (stv 1.0 $conf))
((--> (cycle-phase  $cycle) $phase)       (stv 1.0 $conf))
```

---

### 2.1 `recent-action`

Records the primary action class of a cycle.

#### `$action-type` values

| Value | Meaning |
|---|---|
| `shell-exec` | Shell command was executed. |
| `metta-eval` | MeTTa expression was evaluated. |
| `message-sent` | Message was delivered to a person. |
| `memory-stored` | `remember` or `write-file` was called. |
| `memory-queried` | `query` or `read-file` was called. |
| `no-action` | Cycle produced nothing. |

`$conf` starts at `1.0` and decays via `lib_temporal_v2`.

#### Examples

```metta
((--> (recent-action 4517) shell-exec)    (stv 1.0 1.0))
((--> (recent-action 4518) message-sent)  (stv 1.0 1.0))
((--> (recent-action 4519) no-action)     (stv 1.0 1.0))
((--> (recent-action 4520) metta-eval)    (stv 1.0 1.0))
((--> (recent-action 4521) memory-stored) (stv 1.0 1.0))
```

---

### 2.2 `state-delta`

Records key state transitions between the last-known state and the entering state. It is computed at the pre-LLM call site by comparing the current snapshot.

#### `$delta-key` values

| Value | Meaning |
|---|---|
| `person-state-shift` | `person-state` changed, for example `grounded` → `urgent`. |
| `verdict-shift` | Soul verdict changed, for example `PROCEED` → `CAUTION`. |
| `agency-shift` | `agency-balance` category changed. |
| `goal-change` | `active-goals` were added or removed. |
| `no-delta` | No significant state change was detected. |

`$conf` starts at `1.0` and decays via `lib_temporal_v2`.

#### Examples

```metta
((--> (state-delta 4517) person-state-shift) (stv 1.0 1.0))
((--> (state-delta 4518) verdict-shift)      (stv 1.0 1.0))
((--> (state-delta 4519) no-delta)           (stv 1.0 1.0))
```

---

### 2.3 `cycle-phase`

Records the system phase at the moment of post-LLM recording.

#### `$phase` values

| Value | Meaning |
|---|---|
| `attending` | Processing new human input. |
| `computing` | Running inferences, derivations, or substrate operations. |
| `idle` | No action; waiting for input. |

`$conf` starts at `1.0` and decays via `lib_temporal_v2`.

#### Examples

```metta
((--> (cycle-phase 4517) attending) (stv 1.0 1.0))
((--> (cycle-phase 4518) computing) (stv 1.0 1.0))
((--> (cycle-phase 4519) idle)      (stv 1.0 1.0))
```

---

## 3. Call Sites in `loop.metta`

### 3.1 Call Site 1: Pre-LLM

**Location:** Between `soul-pre-compute` and the conditional LLM call in the `omegaclaw` main loop.

```metta
(cycle-trace-record-pre $cycle-num $state-snapshot)
```

#### What it does

Receives the current cycle number and a state snapshot containing:

- `person-state`
- `soul-verdict`
- `agency-balance`
- `active-goals`

Then it:

1. Compares the snapshot to `last-known-state`, which is stored as an atomspace atom.
2. Emits one or more `state-delta` atoms for detected changes.
3. Emits `(state-delta $cycle-num) no-delta` if no significant changes were detected.
4. Updates the `last-known-state` atomspace atom with the current snapshot.

#### State snapshot structure

```metta
((--> last-known-state person-state)  (stv $val $conf))
((--> last-known-state soul-verdict)  (stv $val $conf))
((--> last-known-state agency-balance) (stv $val $conf))
((--> last-known-state active-goals)  (stv $val $conf))
```

#### Comparison logic

| State field | Comparison method | Emitted delta |
|---|---|---|
| `person-state` | Equality check | `person-state-shift` |
| `soul-verdict` | Equality check | `verdict-shift` |
| `agency-balance` | Equality check | `agency-shift` |
| `active-goals` | Set comparison | `goal-change` |
| All fields equal | No change detected | `no-delta` |

---

### 3.2 Call Site 2: Post-LLM

**Location:** After skill execution completes, before history append.

```metta
(cycle-trace-record-post $cycle-num $action-type $phase)
```

#### What it does

Receives:

- The cycle number
- The dominant `action-type` from this cycle
- The current phase

Then it:

1. Emits a `(recent-action $cycle-num) $action-type` atom.
2. Emits a `(cycle-phase $cycle-num) $phase` atom.
3. Returns a trace-record summary for optional history inclusion.

#### Action-type determination

Priority order: first match wins.

| Priority | Condition | Action type |
|---:|---|---|
| 1 | `send` was called | `message-sent` |
| 2 | `shell` was called | `shell-exec` |
| 3 | MeTTa eval was called | `metta-eval` |
| 4 | `remember` or `write-file` was called | `memory-stored` |
| 5 | `query` or `read-file` was called | `memory-queried` |
| 6 | None of the above | `no-action` |

#### Phase determination

| Condition | Phase |
|---|---|
| New human input was received this cycle | `attending` |
| LLM was invoked and produced output | `computing` |
| Otherwise | `idle` |

---

## 4. Function Signatures

### 4.1 `cycle-trace-record-pre`

```metta
(: cycle-trace-record-pre (-> Number StateSnapshot Atom))
```

Emits `state-delta` atoms, updates `last-known-state`, and returns a summary atom.

#### Implementation approach

- MeTTa function takes cycle number and state snapshot.
- Performs match against `last-known-state` atoms.
- Emits delta atoms via `|-` assertion.
- Updates `last-known-state` via revision.

---

### 4.2 `cycle-trace-record-post`

```metta
(: cycle-trace-record-post (-> Number ActionType Phase (List Atom)))
```

Emits `recent-action` and `cycle-phase` atoms, and returns the list of created atoms.

#### Implementation approach

- MeTTa function takes cycle number, `action-type`, and phase.
- Directly asserts `recent-action` and `cycle-phase` atoms via `|-`.
- Returns the created atoms as a list.

---

### 4.3 `cycle-trace-query`

```metta
(: cycle-trace-query (-> Number (List Atom)))
```

Returns all trace atoms for a given cycle.

#### Implementation approach

Matches:

- `(recent-action $cycle) $x`
- `(state-delta $cycle) $x`
- `(cycle-phase $cycle) $x`

Then returns the matched atoms.

---

### 4.4 `cycle-trace-recent-actions`

```metta
(: cycle-trace-recent-actions (-> Number (List Atom)))
```

Returns `recent-action` atoms for the last `N` cycles.

#### Implementation approach

- Takes `N`.
- Queries `recent-action` atoms for cycles from `(current-cycle - N)` through `current-cycle`.
- Enables analysis of action distribution trends.

---

## 5. `lib_temporal_v2` Decay Integration

`cycle-trace` atoms participate in the existing temporal decay system.

### Decay behavior

- All three atom types carry `(stv 1.0 1.0)` at creation.
- `lib_temporal_v2` decay rules reduce confidence over subsequent cycles.
- Expected decay rate: confidence halves approximately every 50 cycles, configurable via `lib_temporal_v2` parameters.
- Atoms below the confidence threshold, for example `(stv _ 0.1)`, can be cleaned up by periodic garbage collection.

### Integration mechanism

- `cycle-trace` atoms use the standard `(stv 1.0 $conf)` tuple format.
- `lib_temporal_v2`'s existing `decay-atom` function processes them without special handling.
- No new decay rules are needed; existing temporal decay handles all three types uniformly.

### Decay benefit

| Benefit | Description |
|---|---|
| Real-time reasoning | Recent cycles retain high confidence. |
| Reduced clutter | Historical cycles fade, reducing atomspace accumulation. |
| Flexible temporal queries | Querying can filter by confidence threshold to examine recent or historical traces. |

---

## 6. Loop Flow Integration

### Current `loop.metta` flow

```text
omegaclaw cycle:
  1. receive message
  2. detect newness
  3. soul-pre-compute: confidence gate
  4. [if needed] LLM invocation
  5. [if needed] soul-proceed: output gate
  6. parse response s-expr
  7. execute skills
  8. append history
```

### Flow with `cycle-trace-record`

```text
omegaclaw cycle:
  1. receive message
  2. detect newness
  3. soul-pre-compute: confidence gate
  4. cycle-trace-record-pre $cycle $state-snapshot   # NEW
  5. [if needed] LLM invocation
  6. [if needed] soul-proceed: output gate
  7. parse response s-expr
  8. execute skills
  9. cycle-trace-record-post $cycle $action-type $phase   # NEW
  10. append history
```

Steps 4 and 9 are the only new call sites. No other loop logic changes.

---

## 7. Example Session Trace

Cycles `4517`–`4521`, demonstrating all three atom types across a conversation:

```metta
;; Cycle 4517: berton_c sends new message
((--> (state-delta  4517) person-state-shift) (stv 1.0 1.0))
((--> (recent-action 4517) message-sent)       (stv 1.0 1.0))
((--> (cycle-phase  4517) attending)           (stv 1.0 1.0))

;; Cycle 4518: NAL derivations running
((--> (state-delta  4518) verdict-shift)       (stv 1.0 1.0))
((--> (recent-action 4518) metta-eval)         (stv 1.0 1.0))
((--> (cycle-phase  4518) computing)           (stv 1.0 1.0))

;; Cycle 4519: idle, waiting for input
((--> (state-delta  4519) no-delta)            (stv 1.0 1.0))
((--> (recent-action 4519) no-action)          (stv 1.0 1.0))
((--> (cycle-phase  4519) idle)                (stv 1.0 1.0))

;; Cycle 4520: shell audit command
((--> (state-delta  4520) no-delta)            (stv 1.0 1.0))
((--> (recent-action 4520) shell-exec)         (stv 1.0 1.0))
((--> (cycle-phase  4520) computing)           (stv 1.0 1.0))

;; Cycle 4521: storing findings
((--> (state-delta  4521) goal-change)         (stv 1.0 1.0))
((--> (recent-action 4521) memory-stored)      (stv 1.0 1.0))
((--> (cycle-phase  4521) computing)           (stv 1.0 1.0))
```

After 60 cycles without access, `lib_temporal_v2` decay might produce:

```metta
((--> (recent-action 4517) message-sent)  (stv 1.0 0.35))  ;; faded
((--> (recent-action 4577) memory-stored) (stv 1.0 0.95))  ;; recent, still strong
```

---

## 8. Open Design Decisions

| Decision | Current assumption | Recommendation |
|---|---|---|
| Cycle number source | The loop maintains a cycle counter. | Confirm the counter is accessible to `cycle-trace-record` functions, or determine whether a separate counter is needed. |
| State snapshot mechanism | Pre-LLM function needs access to `person-state`, `soul-verdict`, `agency-balance`, and `active-goals`. | Since these exist as atomspace atoms, consider reading the snapshot at call time rather than receiving it as an argument. This would simplify the function signature. |
| Multi-action cycles | A cycle may call shell + MeTTa + send. Current design records only the highest-priority action type. | Keep a single atom per cycle for simplicity. Emitting multiple `recent-action` atoms per cycle can be a future extension. |
