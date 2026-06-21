# SN-Stalk Reconciliation: Parking Document

**Date:** 2026-05-30
**Author:** Claude (Opus 4.7), in conversation with Berton, from review of the SN soul file set
**Status:** PARKED. The SN stalk files are deferred until the SN stalk becomes the second NACE instance, after the capability-registry caller proves the pattern. This document captures everything known about their current state so the reconciliation is a known task rather than a rediscovery.
**Why this document exists:** The four-NACE sheaf decision nearly got lost because it lived only in chat history. This document is the explicit guard against the same thing happening to the SN reconciliation work. It records the good, the bad, and the ugly of the SN files as they stand, so a future thread (or a future instance of Claude, or Clarity) can pick up the reconciliation without re-deriving the findings.

---

## 1. Why the SN files are parked rather than fixed

The project pivoted. The NACE proof-of-concept is now the capability registry, not the SN stalk. The capability-registry caller (specified in `ClarityOmega_NACE_Caller_Contract.md`) targets the capability-efficacy atom, not the SN stalks. The SN stalk and the capability registry are independent NACE instances in the eventual four-NACE sheaf; the capability-registry PoC does not depend on the SN files being correct.

Three reasons the SN files are parked, not fixed now:

First, they are not blocking the PoC. Building the capability-efficacy caller does not touch the SN stalks. The SN drift problems can sit without affecting the thing that is being proven.

Second, the capability-registry caller will produce the verified template the SN reconciliation should follow. The SN stalk's central problem (decorative consultation, named below) is not a bug to patch; it is a design question (how does a stalk's learned truth value gate behavior) that the capability registry is about to answer definitively through its efficacy-filter-step. Fixing the SN files before that pattern is proven would mean solving the same problem twice, the second time worse.

Third, fixing them now is scope expansion away from the stated priority (proving NACE works via the capability-registry path). The disciplined move is to park with a known resolution path, not to fix opportunistically.

The resolution path: once the capability-registry caller is built and verified, the SN reconciliation becomes a known application of a proven template (the efficacy-filter-step pattern for non-decorative consultation, the shared-counts-as-truth-value pattern for the stalk truth values, the two-hook resolve-and-log caller structure for SN observation). The SN stalk becomes the second NACE instance by copying the pattern the first instance proved.

---

## 2. What is good and real in the SN files (do not rebuild these)

The SN stalk substrate is substantial, validated, and correct in its foundations. The reconciliation must preserve these, not rebuild them.

**The five (or seven, post-split) stalk atoms with prior truth values exist and are documented.** From `sn_stalk.metta`, the priors are: safety-first (0.90, 0.50), integrity-check (0.85, 0.50), person-state-salience (0.80, 0.40), urgency-detection (0.70, 0.40), context-shift (0.60, 0.30). The priors carry documented rationale (safety-first's 0.90 from 578-plus calibration entries at high agreement, urgency-detection's lower confidence because it is the rule most often wrong). These priors are considered judgments and should be preserved through any reconciliation.

**The NAL revision mechanism is tested and sound.** `(|- (SN-stalk safety-first (stv 0.9 0.5)) (SN-stalk safety-first (stv 1.0 0.1)))` returns true. The `|-` operator works at the NAL level for stalk revision. This is the same revision mechanism the capability-efficacy caller uses, which is why the SN stalk can adopt the caller's pattern cleanly.

**The persistence constraint is documented and correct.** `sn_stalk.metta` records the empirical finding that revisions do not persist across metta calls (fresh-atomspace-per-invocation) and that the file is the persistent state. This is the same constraint the M6 mechanisms and the task-state primitive honor. The SN files know this; the reconciliation must keep honoring it.

**The Option C delayed-evidence observation design is the right design.** `sn_observation_hook.metta` and `sn_observe.metta` specify the full delayed-evidence loop in comments: log a pending observation when a rule fires, resolve it when later cycles provide evidence, revise via `|-`, write back, expire pending older than 10 cycles to ambiguous. This is structurally the same loop as the capability-efficacy caller, and it is also structurally the same as the Continuity-of-Mind window. The design is sound; it is unwired, not wrong.

**The sheaf framing is encoded in the substrate.** The stalk atoms are documented as local sections (stalks) in the four-NACE sheaf. The restriction maps (SN to FPN) and the global section are stubbed for Sprint 5+ and Sprint 6+ respectively. The sheaf decision (four NACE instances: three local plus one global, switch hub as base space not a learner, global section emergent not authored) is the architecture this stalk is the first instance of. See the cellular-sheaf framing captured separately.

**The resolution criteria per rule are specified.** `sn_observation_hook.metta` enumerates, per stalk, what confirmed versus disconfirmed means (safety-first: no harm event versus harm event matching ruling; person-state-salience: human builds on response versus human corrects; and so on). These are the success-criteria for the SN stalks, the analog of the capability success-criterion field. They are written and they are reusable.

---

## 3. The three drift problems (the bad and the ugly)

These are the reconciliation work. Each is named with its evidence so the future fix does not have to rediscover it.

### Drift problem 1: priors file and state file disagree on what the stalks are

`sn_stalk.metta` (the priors, Sprint 4) was updated with a context-split safety design: it has `safety-first/crisis`, `safety-first/conduct`, `safety-first/subtle`, plus a `boundary-testing` stalk. `sn_stalk_state.metta` (the evolving state) still carries the monolithic `safety-first` and a different recorded confidence on integrity-check (0.63 or 0.64 from recorded revisions). The two files diverged: one got the context-split design, the other carries running state from before the split.

Consequence: a loop reading "the stalk state" gets different stalks depending on which file it reads. This is the same class of drift the capability-efficacy caller was designed to prevent by using one shared atom rather than two representations. The reconciliation must decide: is the stalk set monolithic or context-split, and which file is authoritative for the current truth values? The likely answer is that the context-split is the intended design and the state file needs to be brought forward to match, preserving the recorded revisions where they apply.

### Drift problem 2: three files carry three different decision thresholds

`sn_decision_procedure.metta` says dominant is `weight >= 0.35`. `sn_cycle_decision.metta` says reliable is `f*c >= 0.30`. `sn_decision.metta` says the exploration threshold is `0.20`. Three files, three thresholds, written at different moments and never reconciled.

Consequence: the same stalk classifies differently depending on which file's threshold is applied. person-state-salience at f*c = 0.32 is exploratory under the 0.35 threshold but reliable under the 0.30 threshold. The reconciliation must pick one threshold scheme (or one coherent set of bands) and apply it across all the decision files. The `sn_stalk_protocol.metta` and `sn_stalk_wire.metta` thresholds (0.35 mandatory, 0.15 to 0.35 exploratory, below 0.15 dormant) are the most fully specified and are the likely canonical choice, but this is a decision for the reconciliation, not a foregone conclusion.

### Drift problem 3: consultation is self-described as decorative (the central problem)

`sn_decision_wire.metta` carries its own honest status atoms: consultation is `decorative`, audit is `designed-not-implemented`, enforcement `requires-external-hook`. Clarity documented plainly that she cannot wire the stalk into her own action selection because her action generation is emergent, not coded, and that real enforcement requires an external post-emission hook she does not own.

The `sn_cycle_log.metta` file is the evidence of this problem made visible: it shows Clarity hand-running the consultation protocol cycle by cycle, and the log degenerates into the same four-line idle entry repeated eight-plus times, some corrupted with `_newline_` literals where persistence failed. That degenerate log is the compute-and-discard problem in miniature: with no mechanical caller driving the loop, the agent stepped in to run it by hand, and manual execution collapsed into duplicate entries.

Consequence and resolution: this is not a bug to patch. It is the exact problem the capability-registry caller solves through the efficacy-filter-step, which actually gates dispatch on the learned truth value (the enforcement the SN stalk lacks). The SN consultation becomes non-decorative by adopting the same pattern: a mechanical caller that resolves observations and revises truth values, plus a consumer that gates behavior on those values. For the SN stalk, the consumer is the salience-rule selection, and the gating is "rules above threshold are mandatory, below are exploratory." The reconciliation copies the proven caller pattern; it does not invent a new enforcement mechanism.

---

## 4. The reconciliation task, when it comes

When the capability-registry caller is built and verified, the SN reconciliation is the following known sequence. It is recorded here so it is a checklist, not a fresh investigation.

First, reconcile the stalk set: decide monolithic versus context-split (likely context-split per the Sprint 4 priors file), bring the state file forward to match, preserve recorded revisions where they apply.

Second, reconcile the threshold: pick one threshold scheme (likely the protocol file's 0.35/0.15 bands), apply it across all decision files, delete the divergent thresholds.

Third, build the SN caller as an application of the capability-efficacy caller template: two hooks (resolve SN observations at cycle entry, log SN rule firings after output), revising the SN stalk truth values via `|-`, using the per-rule resolution criteria already specified in `sn_observation_hook.metta` as the success-criteria.

Fourth, make consultation non-decorative by wiring the SN stalk's salience-rule selection to gate on the learned truth values, copying the efficacy-filter-step pattern: above-threshold rules mandatory, below exploratory. This is the enforcement the SN stalk currently lacks.

Fifth, verify the SN caller on synthetic SN observation evidence, the same way the capability-efficacy caller is verified, before it goes live.

The reconciliation is an application of a proven pattern, which is why parking now and fixing after the capability-registry proof is the cheaper path than fixing now.

---

## 5. The file inventory (what exists, for the future fixer)

For the future thread picking this up, the SN file set as reviewed:

Core stalk files: `sn_stalk.metta` (priors, context-split design), `sn_stalk_state.metta` (evolving state, pre-split, divergent), `sn_stalk_pending.metta`, `sn_stalk_protocol.metta` (threshold bands, likely canonical), `sn_stalk_wire.metta` (behavioral wiring, context-splitting, missed-activation tracking), `sn_stalk_convergence_test.metta`.

Observation files: `sn_observation_hook.metta` (Option C schema and per-rule resolution criteria), `sn_observe.metta` (delayed-evidence design), `sn_observation_log.metta`, `sn_pending_observations.metta`, `sn_missed_activation.metta`.

Decision files: `sn_decision.metta` (0.20 threshold), `sn_decision_procedure.metta` (0.35 threshold), `sn_decision_wire.metta` (decorative status atoms), `sn_cycle_decision.metta` (0.30 threshold).

Log files: `sn_cycle_log.metta` (the degenerate-repetition evidence of manual loop-running), `sn_observation_log.metta`.

The good is concentrated in the stalk priors, the revision mechanism, the Option C observation design, and the per-rule resolution criteria. The drift is concentrated in the priors-versus-state divergence, the three decision-threshold files, and the decorative-consultation status. The ugly is the degenerate cycle log, which is not a file to fix but evidence of the problem the caller solves.

---

## 6. The one-line summary for the future fixer

The SN stalk is a real, validated NACE instance with sound priors, a working revision mechanism, and a correct delayed-evidence observation design, blocked by three drift problems (priors-versus-state divergence, threshold inconsistency, decorative consultation) whose resolution is an application of the capability-registry caller pattern once that pattern is proven. Park until then. Do not rebuild the good parts. Do not fix the consultation problem independently; copy the efficacy-filter-step enforcement pattern. The reconciliation is a checklist (Section 4), not an investigation.
