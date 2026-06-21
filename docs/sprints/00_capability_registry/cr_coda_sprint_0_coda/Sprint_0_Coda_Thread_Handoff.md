# Sprint 0-Coda: Thread Handoff

**Purpose:** Bring a fresh Claude thread to speed on Sprint 0-Coda (Capability
Registry: dispatcher + first capability), with the dependency chain stated
precisely so the work is scoped correctly and does not over-reach into Boundary 1
(which is Sprint 1, not Coda).
**Created:** 2026-06-13. **Author context:** handed off from the thread that
completed Surface C (soul-mutation gate substrate + detection coverage).
**Read alongside:** `CLAUDE_ORIENTATION.md` (project conventions),
`artifact_0_loop_extension_contract.md` (hook discipline), and the authoritative
Coda spec named in section 4 below.

---

## 1. The one-paragraph orientation

ClarityOmega is a soul-augmented MeTTa/PeTTa agent (Clarity) on Docker. The soul
is the reasoning substrate, not a value filter. Berton is architectural authority;
Clarity authors her own soul/ MeTTa and is authoritative on substrate questions;
Claude does Python/Docker/diagnostics/spec. Repo root `/PeTTa/repos/omegaclaw/`,
container `clarity_omega`, compose service `clarityclaw`, branch
`fix/F-HISTORY-CONTAMINATION-archival`. Rebuild:
`docker compose build --no-cache clarityclaw && docker compose up -d`. The gate
and most substrate fire only in the live loop on Clarity's emitted commands; bare
run.sh probes cannot reach `(metta ...)`, `|-`, skills, or helper.* (no skill
chain). Conventions: no em-dashes, surgical `git add` (never `git add .`), apply
scripts with `--apply/--reverse/--dry-run` + paren-delta-zero + backup, one change
per commit per verification, read live source before claiming.

## 2. Where Coda sits in the sequence (PRECISE)

The soul-gate evolution sequence is **C -> Coda -> Sprint 1 (Boundary 1) -> D -> E**.
This precision matters: a common misread is "Coda unblocks D and E." It does not.
**Coda ships the dispatcher live but stops BEFORE Boundary 1. Sprint 1 holds
Boundary 1. D and E depend on Boundary 1, therefore on Sprint 1, not on Coda.**

```
Surface C  (DONE to this point: gate substrate + detection coverage committed f956985)
   |
   v
Sprint 0-Coda  (THIS WORK: dispatcher live + first capability skill-discovery)
   |             ships with Boundary 1 UNRESOLVED -- tolerable because the first
   |             capability is informational (reads no soul verdict)
   v
Sprint 1  (HOLDS BOUNDARY 1: soul-state becomes structurally queryable as
   |        (soul-state ...) atoms via add-atom, not just change-state! strings)
   |
   +--> Surface D  (NACE gate-learning; needs C's (gate-decision ...) records
   |                + Boundary 1 so it reads verdict state structurally)
   +--> Surface E  (command-execution interlock for shell/network/delete;
                    needs Boundary 1 + Coda Phase 1.5 / ADR-006 Criterion 5;
                    hard prereq for bare-metal deployment)
```

Why the order is non-negotiable (from the roadmap): building D or E before
Boundary 1 produces gates that LOOK structural but enforce only by convention
(LLM-side classification, not substrate interlock). That is the string-contains
lesson (always-True, tested only positive) at the architecture level. Boundary 1
is what lets D and E be real.

## 3. What Sprint 0-Coda actually ships (scope boundary)

Sprint 0 Phase 1 scoped "core dispatcher + first capability." At Sprint 0 close,
ONLY the dispatcher landed (committed, 180 lines, `soul/capability_registry.metta`,
NOT yet imported in the manifest). Sprint 0-Coda finishes the scope: it wires the
dispatcher to runtime and lands the first production capability.

**In scope (Coda):**
- Wire the dispatcher into runtime (manifest import + getContext dispatch insertion).
- Land the first capability: `skill-discovery` (`soul/capabilities/skill_discovery.metta`)
  -- proves the registration->dispatch->match->collapse pattern AND reduces token
  cost (ships only contextually relevant skills instead of ~70 every cycle).
- Phase C: five coordinated changes in one commit (substrate reshape to Path C,
  new capability file, manifest import, getContext insertion, artifact_1 update).
- Phase D: run `phase_d_coda_verification.py`, criteria P-1..P-7, record whether
  Criterion 5 (silent chain termination on handler crash) fires in production.
- Extract ADR-008 (two-dispatcher consequence) and ADR-009 (Substrate Fractal
  Invariant) at close-out.

**NOT in scope (defer, do not pull in):**
- Boundary 1 / the soul-state-producer (that is Sprint 1; design begins AFTER
  Coda Phase D verifies).
- Bulk migration of the 14 hardcoded skill descriptions to per-capability atoms
  (Sprint 1+; needs context-filtering to be useful first).
- The dispatch-guard that reads soul Safety state (blocked until Boundary 1).
- Phase 1.5 handler error isolation (ADR-006 Criterion 5 fix) unless Phase D shows
  it firing frequently.

**The tolerated-gap fact to carry:** during Coda the registry fires WITHOUT
reading soul verdicts. This is fine ONLY because skill-discovery is informational
(queries `(registered-capability ...)` atoms and formats them; makes no governance
decision). The moment a capability needs a soul verdict, Boundary 1 is required --
that is the Sprint 1 trigger.

## 4. The authoritative spec to work from

**`docs/sprints/00_capability_registry/sprint_0_coda_phase_a_v6.md`** is THE spec.
It is at v6 (the v5->v6 cycle added the Path C substrate reshape as "Change 0").
Work from v6, not earlier versions. Key sections:
- Section 1: Coda framing (why it is Sprint 0 Phase 1 finishing, not a new sprint).
- Section 2: the two-dispatcher architecture, asymmetric flow (soul -> registry,
  never reverse), and the two flow-translation boundaries (Boundary 1 unresolved).
- Section 5/6: the skill-discovery handler, registration atom, formatter.
- Section 7: the five Phase C changes + the exact getContext insertion shape.
- Section 8: Phase D dual-path parity verification (registry path vs hardcoded
  getSkills; getSkills stays callable until parity passes -- do NOT remove it in
  the wiring commit).
- Section 9: free empirical -- observe whether Criterion 5 fires in production.

Supporting docs (read as needed, not first):
- `ADR-006-capability-registry.md` -- the dispatcher decision + Criterion 5
  limitation (handler crash terminates chain silently under reduce/2 indirect
  invocation; catch is inert there). LOAD-BEARING for E and Phase 1.5.
- `sprint_0_phase_1_design_v3_3.md` -- the Sprint 0 Phase 1 origin design; Section
  5 has the per-invocation isolation primitive; Q4 deferred invocation-id source
  to Phase C.
- `ADR-007-substrate-externalized-control-flow.md` -- project-wide control-flow
  principle the dispatcher instances.
- `staging/capability_registry_path_c_draft.metta` -- the 228-line Path C draft
  that replaces the 180-line registry in Change 0.

## 5. The open resolution Coda must make (flagged so it is not missed)

`gensym-invocation-id` -- the per-invocation isolation primitive in the getContext
insertion -- has its SOURCE deferred to Phase B resolution (v3.3 Q4 -> Phase A v4
Section 7). Before the Phase C apply script can be drafted, Coda must resolve
which of three sources to use: (i) an existing runtime primitive (`gensym` or
equivalent) if one exists, (ii) a helper.py function, or (iii) a MeTTa-defined
counter. The Phase D verification needs per-invocation isolation asserted, which
cannot be drafted without knowing the ID source. RESOLVE THIS EARLY in the thread.

## 6. State at handoff

- Branch `fix/F-HISTORY-CONTAMINATION-archival`, 2 commits ahead of origin
  (Intervention 1 Piece 1a `ee50f68`; Surface C detection coverage + docs
  `f956985`). Unpushed -- Berton's call on push.
- `soul/capability_registry.metta` exists (Sprint 0 close), NOT imported in
  `lib_clarity_reasoning/lib_clarity_reasoning.metta`. Coda Phase C wires it.
- Surface C is committed to "substrate + detection coverage." Its open tail items
  (live gate-mechanism test via a safe probe head; the general untagged-fallback
  Fix 2) are INDEPENDENT of Coda and do not block it.
- The container is running and iterating clean (last observed iterations all
  `(SOUL-GATE-FLAG clean unlocked)`).

## 7. First moves for the Coda thread

1. Read `sprint_0_coda_phase_a_v6.md` end to end (it is the spec).
2. Read `src/loop.metta` getContext (the insertion site) and
   `soul/capability_registry.metta` (the dispatcher being wired) from live source.
3. Resolve `gensym-invocation-id` source (section 5 above) -- it gates the apply
   script.
4. Draft the Phase C apply script (five changes, one commit, reversible) per the
   v6 Section 7 plan and artifact_0 hook discipline.
5. Ask Berton before applying -- confirm the gensym resolution and the apply plan.
```

## 8. What defines D and E (for when Sprint 1 + D/E come up)

You asked which committed docs define the D and E work. Recorded here so the
sequence is traceable:

- **Spine for both:** `Soul_Gate_Evolution_Roadmap_C_D_E.md` -- scope, dependency
  order, and the two-layer invariant (STATIC FLOOR human-gated + LEARNING BAND
  CAUTION-tier-only; a gate that could learn to stop gating is forbidden).
- **Surface D + Boundary 1 substrate:**
  `Restoration_Soul_Extension_Spec_Part2_Accumulating_Knowledge.md` -- defines
  Extension C (the soul-state-producer = Boundary 1's work-package), Extension D
  (the dispatch-guard that reads `(soul-state ...)` and terminates a dispatch on a
  negative verdict), and Extension E/F. D's prerequisites live here.
- **Surface E prereqs:** `ADR-006-capability-registry.md` (Criterion 5 / Phase 1.5
  / handler error isolation) + `sprint_0_coda_phase_a_v6.md` Section 9 (where Phase
  1.5 observation lives).
- **Verdict-surface map for both:**
  `Restoration_Soul_Governance_Verdict_Surface_Survey.md` -- the writer/consumer
  survey of the governance verdict surface; what currently writes/reads verdicts,
  i.e. what Boundary 1 must translate into queryable atoms.
- **Gate decision records (D's training data):** emitted by Surface C from day one
  via `soul_governance.gate_decision_record` (PENDING/APPROVED/DENIED/COMMIT/STALE/
  ERROR) to the governance journal. D learns over these.
