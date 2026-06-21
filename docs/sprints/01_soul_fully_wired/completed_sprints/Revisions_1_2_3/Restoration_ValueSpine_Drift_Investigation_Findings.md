# Value-Spine Drift Investigation: Findings and Evidence Chain

**Status:** Read-only investigation record. The full evidence behind Surface 6 of the
restoration pre-flight. This is the roadmap (what we did, how we arrived at each
conclusion) and the knowledge source the Revision 1 script pulls from. Sibling to
Master_Doc_Compliance_Findings and Inverse_Audit_Runtime_Beyond_Doc.
**Mandate under which this was conducted (Berton):** one spine, the soul, navigating from
a single consistent set of spec-defined values across all surfaces. Prove a divergence is
drift-in-application before fixing it; until proven drift, it stays under investigation.
Once proven drift: fix the drift files and the production files consuming the drift so
everything doing real runtime work uses spec, and archive the non-runtime files.

---

## 1. The spec single source (ground truth)

`soul/soul_kernel.metta` is the spec source for the value-spine. Proven by source read:
- Priority: `(priority A N)` x5, accessor `soul-priority-hierarchy` (L328).
- Tensions: `(tension-vector T)` x5 (L280-284), accessor `soul-all-tensions` (L333).
- Irreversibility: numeric `(irreversible-weight skill N)` x7 (L479-485), accessor
  `soul-irreversible-weight` (L508: `(match &self (irreversible-weight $skill $w) $w)`).
- Paraconsistency: `(soul-paraconsistent-pair A B)` x4 (L428-431), accessor
  `soul-paraconsistent-pairs` (L502), predicate `soul-paraconsistent?` (L505).
- Patterns: `(soul-pattern Name "desc")` + companions (pole+/pole-/signal/felt/moat/anti/
  proxy/gap), the nine flourishings.

Container atom-count greps proved these are LIVE in the running process (not just declared):
priority=5, paraconsistent-pair=4, tension-vector and irreversible-weight present. The
boot log confirmed initSoulSeeds loads prose via `(remember ...)` into ChromaDB AND
soul_kernel atoms load via import; these are two separate mechanisms.

NOTE on harness artifacts: a fresh-process harness (docker exec run.sh) boots an EMPTY
atomspace and cannot reach the live loop process's memory, so it wrongly reported the
value atoms absent. Live atomspace state = docker logs of the running process. This
distinction matters for all future verification: verify against the live process, not a
fresh boot.

---

## 2. The four parallel representations (the fragmentation map)

The investigation found paraconsistency declared in FOUR different shapes across the tree.
This map is the core finding; the classification follows from it.

1. `soul_kernel.metta`: `(soul-paraconsistent-pair A B)` data atoms. SPEC.
2. `genesis_engine.metta` L22-25: `(= (paraconsistency-pair N) (pair A B))`, indexed
   function 1-4. Same four pairs as spec, different shape.
3. `proposed_tension_atoms.metta`: `(= (paraconsistency-pair V1 V2) ...)`, named-arg
   function, DIFFERENT pairs (Integrity/SharedUnderstanding, Safety/CreativeTranscendence,
   WonderPreservation/TimeCoherence), filename "proposed".
4. `soul_flourishing_extensions.metta`: `(add-atom (paraconsistency-pair A B "desc"))`,
   data atoms with descriptions, pairs among Receptivity/LossProcessing/Play.

Plus `identity_kernel.metta`: `(paraconsistency-pair A B)` (no description), part of a
full rebuild of all four value families.

The same fragmentation, in lesser degree, appears in tension-vector: `tension_auto_logger.metta`
declares `(= (known-tension-vector N) name)` x5 = soul_kernel's five tensions in a local
indexed shape.

---

## 3. The expressive-capacity test (how drift-vs-capability was settled)

Per the mandate, a parallel representation is DRIFT if it re-expresses what spec already
provides, and CAPABILITY if it expresses something spec genuinely cannot. The test applied
to each parallel form, by comparing its content against the spec content:

- **genesis_engine `(paraconsistency-pair N)`:** the four pairs are Safety/Helpfulness,
  AgencyBalance/PurposeBeyondUtility, TimeCoherence/CreativeTranscendence,
  SharedUnderstanding/WonderPreservation. IDENTICAL to soul_kernel's four. Expresses
  nothing spec cannot. DRIFT (same content, indexed-function shape). genesis_engine is real
  capacity (the encounter/genesis machinery), but its paraconsistency REPRESENTATION drifted.
- **identity_kernel (all four families):** priority-rank, tension-vector (exact dup of
  spec), paraconsistency-pair, magnitude irreversible-weight. Same canonical values as spec,
  rebuilt in divergent shapes from memory (header: cycle-2340 rebuild after storage loss).
  DRIFT. Every atom spec-duplicate or spec-divergent; none unique.
- **proposed_tension_atoms:** DIFFERENT pairs than spec, filename "proposed". Not spec, not
  consumed, not imported. A PROPOSAL, archival.
- **soul_flourishing_extensions:** pairs among Receptivity/LossProcessing/Play, patterns
  BEYOND the canonical nine (AgencyBalance, CognitiveResilience, ConnectionDepth,
  WonderPreservation, TimeCoherence, PurposeBeyondUtility, SharedUnderstanding,
  CreativeTranscendence, AttentionStewardship). Expresses something spec CANNOT (three new
  flourishings). This was the ONE drift-vs-capability question that needed Berton.
  RESOLUTION (Berton): these are kernels of an idea Clarity proposed, highly unrefined,
  4-5 days of real work from being seriously considerable as additions to the nine. As is,
  they are future-work, NOT a sanctioned capability extension. ARCHIVAL, flagged future-work.
- **tension_auto_logger `(known-tension-vector N)`:** soul_kernel's five tensions in a
  local indexed shape. Same drift pattern as genesis_engine, but not imported, not
  consumed. ARCHIVAL/cleanup.

CONCLUSION: no genuine-capability case survives. Every parallel representation is either
drift (genesis_engine, identity_kernel) or a non-runtime proposal/kernel (the rest).

---

## 4. Why option (a) single-source is mandate-forced (not preference)

Two fix options were weighed:
- (a) runtime files STOP declaring value atoms and QUERY soul_kernel's spec atoms.
- (b) reshape each file's local declarations to the spec SHAPE.

(b) gives the right shape but leaves MULTIPLE SOURCES (genesis_engine + identity_kernel +
soul_kernel each still declaring the same four pairs). Multiple sources that agree today can
drift apart tomorrow. The mandate's words are "a single consistent set." Only (a) yields a
single source = one spine. Therefore (a) is FORCED by the mandate, not chosen by preference.

---

## 5. The import chain (what is runtime vs non-runtime)

`lib_clarity_reasoning/lib_clarity_reasoning.metta` L6-91, the runtime import chain, loads:
genesis_engine (L16), continuity_driver (L15), identity_kernel (L22), and many others.
It does NOT load: proposed_tension_atoms, flourishing_extentions/, proposed_substrate_capacities,
flourishing_completeness_analysis, hyperseed_extensions/, tension_auto_logger.

This is the fix-vs-archive test ("in production using the drift" = fix; not loaded =
archive). It proved the clean split:
- IN RUNTIME (fix to spec): genesis_engine, continuity_driver, identity_kernel.
- NON-RUNTIME (archive): the six files above.

---

## 6. The consumer sweeps (who reads the drift shapes)

Three container sweeps established the consumer set:
1. priority-rank / paraconsistency-pair across soul/: returned only the files classified
   here (declarations), no external consumer beyond continuity_driver.
2. magnitude irreversible-weight / tension-vector across the import chain (excluding
   already-read files): returned soul_kernel (spec source, expected), the committed
   gate seed (tags, expected), my two session harnesses (scaffolding), and
   tension_auto_logger (a declaration, not imported, not consumed).
3. soul-pattern across the chain (excluding spec + classified files): returned three
   goal-comment-only files (symbiotic_choice_architecture, temporal_horizon_expansion,
   diversity_protection L2), one correct CONSUMER (soul_utils L118
   `(match &self (soul-pattern $p $_))`), and the gate seed. NO divergent pattern declarer.

RESULT: the ONLY runtime consumer of a drift shape is `continuity_driver.metta` L52,
inside `(check-soul-file genesis-engine)`, a startup load-probe calling
`(paraconsistency-pair 1)` and testing empty/non-empty. The flourishing-pattern family is
CLEAN (no fifth drift family). The drift scope is exactly four value families in two
producer files with one consumer.

NAMING-COLLISION GUARD: continuity_driver L234/277/279 use `(priority ...)` for
goal-priority (goal-gap/goal-action ordering), a DIFFERENT namespace from the value
hierarchy `(priority Safety 1)`. These MUST NOT be touched.

---

## 7. The redirect target (proven survivor)

continuity_driver L52 uses genesis_engine's `(paraconsistency-pair 1)` only as a
presence-probe (does genesis_engine load). The content does not matter, only empty vs
non-empty. A naive redirect to the spec accessor would BREAK the probe's purpose: it would
then verify soul_kernel loaded, not genesis_engine (a false check).

Correct redirect: point the probe at a SURVIVING genesis_engine-specific symbol.
`(paraconsistency-test Safety Helpfulness)` (genesis_engine L196) survives the fix (we
remove only L22-25, the paraconsistency-PAIR declarations, not paraconsistency-TEST) and
reduces to `(tension-confirmed Safety Helpfulness)` when genesis_engine is loaded. So the
redirected probe checks `== (tension-confirmed Safety Helpfulness)`, preserving "did
genesis_engine load" with a minimal target swap, no logic change.

---

## 8. The dual-head consequence (why this is a Repair 1 prerequisite)

identity_kernel declares magnitude `(irreversible-weight send high)`; soul_kernel declares
numeric `(irreversible-weight send 2)`. While both load, `soul-irreversible-weight send`
returns BOTH values (a nondeterministic two-value result). Repair 1's value-grounding
verdict reasons over irreversibility weights; a nondeterministic weight makes the verdict
nondeterministic, hence unsound. Removing identity_kernel resolves the accessor to a single
numeric value. This is why Surface 6 is a prerequisite-within-Revision-1 for Repair 1: the
verdict cannot be built soundly until the value atoms are single-source.

---

## 9. Reverse-regression check (against the inverse-audit PRESERVE list)

Does the fix endanger any preserved post-doc capability (P-1..P-10)?
- P-6 (idle/genesis): the fix edits genesis_engine. Its own logic (paraconsistency-test
  L196-204 hard-codes pairs in its own clauses; genesis-hold, genesis-create,
  flourishing-test) does NOT consume the `(paraconsistency-pair N)` declarations being
  removed. They are orphaned within genesis_engine, used only by the redirected
  continuity_driver L52 probe. Removing L22-25 does not touch P-6. Evidence: genesis_engine
  usage grep.
- P-1 (task-state): no overlap (value atoms vs task-state).
- P-2..P-5, P-7..P-10: do not declare or consume the drift shapes (sweep-confirmed).
- Archival set: not imported, not consumed; archiving removes no live capability.
No PRESERVE item endangered. The fix passes the guard.

---

## 10. The fix (what Surface 6's script does), with evidence pointers

1. Remove identity_kernel import (lib_clarity_reasoning L22) + archive identity_kernel.metta.
   Justified by sections 3 (all-drift), 5 (in runtime), 6 (nothing consumes its shapes),
   8 (resolves dual-head).
2. Remove genesis_engine paraconsistency-pair declarations (L22-25). Justified by 3 (drift),
   9 (orphaned, P-6 safe). Real logic stays.
3. Redirect continuity_driver L52 to `(paraconsistency-test Safety Helpfulness)`. Justified
   by 6 (sole consumer) + 7 (proven survivor target). Paired with edit 2 in one change.
4. Archive the six non-runtime files to staging/OLD/OLD_soul_files/. Justified by 5
   (not imported) + 6 (not consumed) + 3 (proposals/kernels, Berton archival).
5. Remove session scaffolding (soul_accessor_live_harness, soul_value_materials_harness)
   from soul/. These are this session's diagnostic files, not project files.
6. Update artifact_1 for the import-chain + continuity_driver changes (Discipline 4).

Edits 1-3 mechanically validated against a staged repo (dry-run/apply/reverse all correct)
this session; anchors confirmed against project-copy source. CONFIRM-LIVE against the live
container before the script, per the no-script-before-CONFIRM-LIVE rule.

---

## 11. Verification after apply (the proof the spine is single-source)

- `soul-irreversible-weight shell` returns a SINGLE value (3 only, not 3 and a magnitude).
  This is the decisive dual-head-resolved check.
- `soul-paraconsistent-pairs`, `soul-priority-hierarchy`, `soul-all-tensions` return clean
  single-source values.
- continuity_driver's genesis-engine load-probe still reports loaded (redirect works).
- SOUL-AUDIT nine-empty-parens: likely a false-positive in soul-rationality-gaps that may
  clear once identity_kernel's divergent atoms are gone; confirm post-apply.

---

## 12. Open question routed to Clarity (her domain)

Repair 1's value-grounding verdict LOGIC (what it computes from operation + scope +
value-grounding, no actor; how it maps to PROCEED/FLAG/PAUSE) is defined against the CLEAN
single-source spec shapes this surface produces. That is Clarity's soul reasoning to
author. Surface 6 lands first so she defines the verdict against clean shapes.
