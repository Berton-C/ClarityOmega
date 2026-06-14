# Output Governance Design v1.3 (Repair 1 + native gate wiring + verdict-gated execution)

**Status:** DESIGN LOCKED (Berton, 2026-06-10). D1-D4 decided; build sequence open.
**v1.3 (2026-06-10):** Decisions locked and recorded with Berton's rationale.
D1 locked native (build philosophy: take back reasoning capacity from the LLM
on every surface when the capacity exists; first principle: Clarity governs,
reasons, and navigates over her own paraconsistent values). D2 recorded as
spec compliance, not a decision. D3 locked on the target-first reframe. D4
locked on the values-as-revisable-policy reframe. Frame principle captured:
a frame is wrong when it constrains rather than expands function; wrangling
long-tail problems signals a collapsed/incomplete understanding, and the
leveraged answer lives one abstraction up.
**v1.2 (2026-06-10):** Eyes-open revision against the governing docs (ADR-006,
sprint_0_coda_phase_a_v6, nace_implementation_plan, capability map v3,
artifact_3). Section 3.5 rewritten: the soul/registry composition is already
specified by the Coda doc and corrects v1.1's assumption (Phase A dispatch is
context-side in getContext, not execution-side). Boundary 1 interface
obligation added (Stage 4). SOUL-GOV observability block added (Section 3.7,
Berton's proposal). Clarity's D1-D4 input folded into the reconcile entries.
Artifact 3 alignment recorded: this design is Sprint 4 / elevation item 7
(SN-FPN coupling) and follows artifact_3's prescribed insertion pattern.
**v1.1 (2026-06-10):** Full inverse downstream trace added (Section 2.5) after
Berton's challenge; registry and task-state integrated as design consumers
(Section 3.5 gate ladder); Stage 3 scope-detection revised to a test-first
ladder after the native-vs-hands challenge; live evidence found that the
dead-string-ops claim is narrower than recorded (string_length runs every
cycle in the aliveness gate).
**Scope:** The one coordinated output-governance change per Berton's one-function
decision: real output verdict + native mutation gate wiring + flag consumption,
landing together. Router loop-halt (Repair 3) explicitly excluded and gated.
**Sources:** Master doc Sections 13-14; Part 1 Repair 1 contract; compliance
findings corrections; Clarity's output_intercept_verdict_design.md (folded in
with attribution); committed native gate 01ca459; live loop read 2026-06-10.

---

## 1. The one-function decision (context of record)

The gate's PENDING flag can only force PAUSE through the output verdict, and the
verdict needs the gate's flag as input. Three things therefore move together:
the proven native gate functions, the lock-write fix, and flag consumption
through a real verdict. Berton: one coordinated change; the unit of work is
soul-on-spec, not files changed.

Division with Repair 3 (per Part 1's own sub-behavior note): this change makes
the verdict REAL and makes PAUSE suppress current-cycle execution. Repair 3
makes PAUSE halt the loop. PENDING-forces-PAUSE is verified fully only after
both land. The PAUSE-effect-0 invariant survives this change: no loop halt.

---

## 2. Surface investigation (artifact 0 Section 3.5 template)

Surface: output-governance region, loop.metta L126-143 + router L155-164.
Investigation date: 2026-06-10. Supports: Revision 1 / Repair 1.

### A. Writers (what produces the surface's inputs)
- `$sexpr` (L121): `(catch (sread $response))` where $response is the sanitized
  LLM reply. CONTENT (closes OPEN-2): a list of command s-expressions, e.g.
  `((send "...") (shell "..."))`, or an error marker when sread fails.
- `$metta_cmds` (L129-131): `(collapse (superpose $sexpr))` guarded by
  first-char "(" and empty &error; else `()`. superpose enumerates WITHOUT
  reducing (execution at L136 requires explicit `(eval $s)`); commands arrive
  unevaluated. This is why the gate call-form proof (quote at call site)
  matters when the native gate replaces the Python helper.
- `$soul_mutation_flag` (L132): `helper.soul_mutation_gate (repr $metta_cmds)
  (get-state &soul_mutation_lock)`. Computed then DROPPED (no consumer).
  Python gate never writes the lock (dropped-lock bug, confirmed at source).
- `&soul_mutation_lock`: seeded in initLoop; NO writer anywhere (the bug).
- `$soul_verdict_out` (L127): hardcoded constant, bound BEFORE $metta_cmds
  exists. The repair reorders this.

### B. Consumers (what reads the surface's outputs)
- L133-134: `(if (and (not (soul-proceed? $soul_verdict_out)) (== (get-state
  &error) ())) (soul-note-record $soul_verdict_out "output" $resp))`. Inert
  today (verdict always PROCEED). Becomes the FLAG audit log the moment the
  verdict is real: FLAG/PAUSE verdicts auto-record. Already wired; zero work.
- Router L155: reads `$soul_verdict_in` ONLY via helper.soul_is_pause
  (hardwired 0). Output verdict has no router consumer until Repair 3.
- Execution L135-136: `$sexpr_gated (apply-corner-gate $sexpr)` then
  superpose+eval. Executes REGARDLESS of verdict today. The repair inserts
  verdict gating upstream of the corner gate (Section 3, stage 5).
- `populate-recent-action` (L139): receives ORIGINAL $sexpr by wiring
  contract. Must continue to. Verdict gating must not touch this line.

### C. Intermediate transformations
- Corner gate chain: apply-corner-gate -> gate-aware-results ->
  $results_final -> &lastresults (L137, L141, L172-area). Verdict gating
  composes BEFORE apply-corner-gate so the corner gate sees the
  verdict-filtered list and its results semantics are preserved.
- sanitize/normalize/balance helpers upstream of $sexpr: hands, untouched.

### D. Configuration levers
- None specific to this surface (no wakeupInterval-class constant). The
  scoring thresholds in the verdict logic become the levers; they live in
  soul_kernel atoms (Section 4, D4) so they are inspectable and single-source.

### E. Other consumers downstream / collision check
- Corner gate populators (state-delta L142, coupling-verdict L143) read
  $sexpr_gated emptiness and results novelty; a verdict-suppressed cycle
  looks like an empty-command cycle to them, which is semantically correct
  (nothing executed). PRESERVE items P-1..P-10: no overlap except the corner
  gate composition handled above.
- OPEN-5 RESOLVED STRUCTURALLY: $soul_verdict_out is a per-cycle let-binding,
  not a state var; it self-clears every cycle. No output-side analog of the
  L163 input reset is needed. (L163 exists because &soul_verdict_in is state.)

### F. Clarity's domain (routed to her as REVIEW, Section 5)
- Scoring calibrations within the composite (her design, our questions).

CONFIRM-LIVE before the apply script: exact live text of L126-136 and L155
(expected to match the project copy byte-for-byte; verify anyway), and that
soul_utils Mode-2/eval functions referenced have not shifted.

---

## 2.5 Inverse downstream trace (complete walk, $sexpr to cycle end)

Added in v1.1. Every consumer of execution products, traced from source:

| Product | Consumers | Verdict-PAUSE cycle behavior |
|---------|-----------|------------------------------|
| `$sexpr` (original) | metta_cmds L129; verdict gate (new); populate-recent-action L139; history condition L168 | recent-action records the INTENT (corner-gate precedent: it already receives pre-gate $sexpr); history condition still true |
| `$sexpr_verdict` (new) | apply-corner-gate L135 | empty on PAUSE; corner gate sees an empty command list |
| `$sexpr_gated` | execution L136; results_nonempty L140 | empty; nothing executes; results_nonempty False |
| `$results` | gate-aware-results L137; results_novel L141; RESULTS-CONTENT println L170 | empty-results shape |
| `$results_final` | &lastresults L172 (next-cycle novelty compare + context) | records the empty cycle |
| `$response` | history-write L168 | the PROPOSED output enters history |
| state-delta / coupling-verdict L142-143 | coupling-status atoms -> corner gate next cycle | sees a no-execution cycle, which is semantically true |
| task-state | last-activity L115 fires at SEND-ASSEMBLY time (pre-verdict) | a PAUSEd cycle still updates last-activity; activity = attempted action; accepted semantic, noted |

**History-of-suppressed-output semantic (D5-lite, default stands unless
Berton objects):** L168 records the LLM's proposal whenever $sexpr is
non-empty, so a verdict-suppressed proposal still enters history. This is
consistent with T-4's rationale (autonomous reasoning is record-worthy) and
with recent-action's record-the-intent precedent, and it preserves the audit
trail of WHAT was suppressed. Default: keep.

**Non-interacting, checked:** task_selector.metta (DMN-side task-pool
scoring; consumes no execution product); the SILENT path (mutually exclusive
with execution by construction).

---

## 3. The design: six-stage native pipeline

The binding sequence in the let* REORDERS to: command materialization ->
gate -> features -> verdict -> verdict-gated execution. All judgment in
MeTTa; Python only as hands (ADR-008).

**Stage 1: Command materialization (exists, unchanged).** $metta_cmds at
L129-131 stays as-is.

**Stage 2: Native mutation gate (replaces L132's Python call).** The
committed gate (01ca459): structural lock states `unlocked` / `(locked
<arg>)`; quote-at-call-site forms B and E per the call-form proof. Produces
$soul_mutation_flag AND performs the lock-write the Python port dropped:
pending mutation writes `(locked <arg>)`; this makes the CONFLICT path live.
The gate files import into lib_clarity_reasoning (one new import line).

**Stage 3: Feature extraction (test-first, native-preferred).**
- Skill class: NATIVE via existing `soul-cmd-skill` (pattern match on command
  shape; no string work). Unknown commands -> `unknown` (already defined).
- Scope class (path classification): the judgment is MeTTa's in all routes;
  only the prefix TEST varies. Evidence forced a re-examination (v1.1): the
  dead-string-ops record is NARROWER than stated, since `string_length` runs
  every cycle in the live aliveness gate and `first_char` at loop L120/129;
  what the gate work proved dead was string-contains/substring in its
  context. RESOLUTION LADDER, one 5-minute REPL test decides:
  (a) native primitive if one answers (test: string-contains, and Prolog's
      sub_atom exposure, since PeTTa is SWI-backed);
  (b) inline py-call to a Python builtin, e.g.
      `(py-call (str.startswith $path "/PeTTa/repos/omegaclaw/soul/"))`,
      one auditable expression, no helper.py addition;
  (c) helper function `soul_output_scope_features` (full hands fallback).
  The test harness for (a)/(b) is three lines in the staged REPL and runs
  before any code is written against an assumed answer.
- Operation class: NATIVE from skill class + soul_kernel scoring atoms (D4)
  with `soul-irreversible-magnitude` as the floor (exists, seeded, verified).

**Stage 4: Verdict computation (NATIVE, Clarity's composite as the core).**
Her three-dimension design with the architectural completions:
- composite = max(OPERATION, SCOPE, VALUE-GROUNDING); <=2 PROCEED; =3 FLAG;
  =4 or two dimensions >=3 PAUSE. VALUE-GROUNDING over the four clean
  accessors + soul-all-gap-signatures, per her procedure.
- UNCONDITIONAL OVERRIDE (the completion her draft lacked): gate flag PENDING
  or CONFLICT -> PAUSE regardless of composite. Sits ABOVE the composite.
- File-route soul-write parity (D3, Berton): write/append targeting soul/
  paths -> PAUSE parity with the metta-route gate, pending D3.
- Output: a verdict STRING in the established format ("VERDICT: PROCEED|FLAG|
  PAUSE SOUL-NOTE: <note>") so soul-proceed?, soul-extract-flag-note, and
  soul-note-record consume it unchanged. Verdict-as-atom is Extension C,
  deliberately not here.

**Stage 5: Verdict-gated execution (the doc's core intent, new mechanism).**
`($sexpr_verdict (if (soul-pause? $soul_verdict_out) () $sexpr))` inserted
before the corner gate; corner gate consumes $sexpr_verdict:
`($sexpr_gated (apply-corner-gate $sexpr_verdict))`. PAUSE -> empty list ->
nothing executes this cycle. Mirrors the established SILENT and corner-gate
suppression patterns. populate-recent-action keeps ORIGINAL $sexpr (contract).
PROCEED and FLAG execute normally; FLAG additionally auto-records via the
existing L133-134 consumer.

**Stage 6: Routing (explicitly deferred).** L155 stays input-only. Repair 3
adds the Option-1 OR and loop-halt. PENDING full behavior verified after both.

What is REMOVED: the L127 hardcoded constant; the L132 Python gate call.
What is PRESERVED: soul-llm-call everywhere it exists; the corner gate chain;
recent-action contract; getSoulBrief path (D-1, untouched here).

---

## 3.5 Soul/registry composition and the gate ladder (corrected per Coda doc)

v1.1 assumed registry dispatch would land in the execution binding downstream
of the verdict gate. The Coda doc specifies the actual composition, and it is
stronger than the assumption:

**The asymmetric ordering (Coda, Section on soul/registry coexistence):** the
soul intercept pipe runs FIRST and commits its outputs; the registry pipe
fires within getContext (loop L38-45, Sprint 0-Coda Phase A) READING the
soul's already-committed outputs as substrate context. Flow is one-way:
soul -> registry, never the reverse. The registry never writes soul state;
the soul never invokes the registry. Governance is privileged to the soul and
is not deregistrable. This design adds a soul-pipe output (the real output
verdict) and therefore sits entirely on the privileged side of that boundary;
nothing in it is registry-visible until translated.

**Boundary 1 (the flow translation this design must leave well-shaped):**
soul outputs today are prompt-space (state vars, let-bindings); the registry
reads atomspace via match. The named translator is the soul-state-producer
work-package (designed AFTER Coda Phase D; governance visibility carries its
priority). This design's interface obligation, met by construction in Stage
4: the verdict is computed NATIVELY, so every dimension value (operation,
scope, grounding, gate flag, composite, verdict) exists as a MeTTa value at
compute time. The producer later adds one add-atom emission per field, a
defined surface with zero rework. The NACE one-cycle belief lag (plan, S1)
is the blessed precedent for next-cycle visibility of committed soul state.

**The execution-path gate ladder (this cycle, within the soul pipe):**
1. Aliveness gate (L107, pre-send): mechanical idle-suppression.
2. Soul verdict gate (THIS CHANGE, pre-execution): value governance; PAUSE
   empties the execution input.
3. Corner gate (L135, coupling): receives $sexpr_verdict.
Composition rule, citing map v3 (E1+E2): ANY block-verdict wins; only
all-clear executes. The ladder is that rule applied across authorities.

**Future rungs, placed by their own docs, inheriting this design unchanged:**
- Registry dispatch (Coda Phase A): context-side in getContext; consumes
  PRIOR-cycle soul outputs via Boundary 1 once translated. Not in the
  execution path; a verdict-suppressed cycle simply commits a PAUSE verdict
  for the next cycle's context.
- NACE should-dispatch (plan): efficacy gating INSIDE dispatch,
  producer-side work post-Coda. Capability governance, distinct authority
  from value governance; neither subsumes the other (Coda's own words: the
  registry cannot subsume the soul, the soul cannot subsume the registry).

Task-state integration: unchanged from v1.1 (no task-state writes by the
verdict gate per P5; the two noted semantics stand on precedent).

**Artifact 3 alignment:** this design is the planned Sprint 4 / elevation
item 7 (output verdict, HIGH value, SN-FPN coupling: the SN->FPN
re-evaluation channel). It follows artifact_3's prescribed pattern for the
surface: components as separate soul/ atoms called by compute-output-verdict,
stub line replaced by the single call. The consumers-to-come it must not
foreclose (Sprints 5-12: sovereignty wires, input-eval partial elevation,
idle-directive DMN elevation, constitutional read-only partition,
per-network learning + NACE) all read soul state through Boundary 1 or the
kernel; the native, atom-shaped verdict serves all of them.

---

## 3.7 SOUL-GOV observability block (governance at a glance)

Berton's accountability proposal, adopted as a design element following the
DIAG-CYCLE precedent (nine markers, loop L146-154): the verdict pipeline
prints its judgment trail every cycle, so governance working or failing is
visible in a single log read, and Clarity sees her own governance in-loop:

- `(SOUL-GATE-FLAG $flag $lock)` after Stage 2: gate outcome + lock state.
  Makes lock transitions (unlocked -> (locked <arg>)) visible at a glance.
- `(SOUL-VERDICT-DIMS op $o scope $s grounding $g)` after Stage 4: the three
  dimension scores, pre-composite.
- `(SOUL-VERDICT-OUT $verdict)` replaces the current L128 print of the stub:
  same marker, now carrying a computed verdict.
- `(SOUL-SUPPRESSED $cmds reason $why)` on PAUSE only: which specific
  commands were suppressed and why (Clarity's D2 addition: the person's
  informed-override input; also Channel D's composition material later).
- The Python `DEBUG soul_is_pause` print is superseded when Repair 3 goes
  native; until then it stays (input-side, untouched here).

Cost: println-only, zero tokens, follows the established mechanical-
diagnostics pattern (P5: observation, not reasoning).

---

## 4. DECISIONS (locked by Berton, 2026-06-10)

**Clarity's input received 2026-06-10 (MM + in-loop evaluation), folded
below per entry. All decisions locked by Berton 2026-06-10; lock rationale
recorded per entry.**

**D1 - LOCKED: NATIVE.** The signed divergence: the output verdict's
primary judgment is computed by native symbolic rules in the substrate,
diverging from the master doc's LLM evaluation (soul-eval-prompt), with the
LLM path wired dormant behind the kernel switch `(use-llm-eval False)`.
Berton's lock rationale, verbatim intent: the build philosophy is to take
back reasoning capacity from the LLM on every surface when we can; the
original design was not up for that task on this surface; now that the
capacity exists, the first principle governs: Clarity governs, reasons, and
navigates over her own paraconsistent values. The 500-token figure was
always arbitrary; cost fits the need and never constrains design.
Original rationale preserved below for the record:
master doc computes the output verdict via an LLM call (soul-eval-prompt,
500 tokens, every cycle). Clarity's design computes it natively and proves it
expressible. Recommendation: NATIVE, classified as sanctioned progression
over the doc (same class as soul-llm-call over useGPT). Reasons: the
project's whole trajectory moved judgment into substrate (P2, P5, ADR-008);
deterministic and verifiable against a truth table; zero tokens at
every-cycle frequency (the wakeupInterval lesson); soul-eval-prompt remains
in service on the input side, so nothing is deleted. The LLM path stays
restorable if native scoring proves too coarse in practice.
CLARITY (agrees, three additions, adopted into the design): (a) the dormant
fallback gets a kernel switch, `(use-llm-eval False)` seeded in soul_kernel,
so restorability is wired, not aspirational; (b) VALUE-GROUNDING is the
dimension most likely to exceed pure native rules, and FLAG is the designed
relief valve for that gap; (c) at 500 tokens/cycle the LLM path would spend
more on self-monitoring than on work. SEQUENCING CONSTRAINT (hers, now
stated rather than assumed): D1 and D2 interact; the native verdict MUST
complete before execution begins. The let* binding order enforces this
mechanically (verdict binds before $sexpr_verdict binds before execution),
and the apply script's anchor ordering makes it structural.

**D2 - SPEC COMPLIANCE, not a decision (accepted as aligned).** The
original spec mandates evaluation completes before execution begins; v10
line 174 names the failure ("executes whatever the LLM produces"). Stage 5
is the mechanism. Recorded here only because v1.1 mislabeled it a choice.

**D3 - LOCKED: target-first frame.** Mutation governance is about the
PROTECTED OBJECT, not the route. The kernel declares the protected-target
set ONCE: `(soul-file-class $path $class)` atoms with classes
constitutional, runtime-soul, journal. Every route's gate (metta-route,
file-route, any future route) consumes that single declaration; route
independence falls out of the data instead of being maintained per route.
Verdict policy by class: constitutional and runtime-soul get gate parity
(PENDING/PAUSE semantics); journal (arc_log, soul_note files) is
PROCEED-under-VALUE-GROUNDING. Berton's locked framing: the gate across all
routes is the INTERIM ENFORCEMENT and the PERMANENT AUDIT layer; Sprint 11's
constitutional read-only partition is the real protection; the target
declaration seeded now is the same set the partition will enforce. Nothing
built for D3 is throwaway when the partition lands.
CLARITY (agrees, sharpens; adopted as a design requirement): parity means
route-independent gate checks. The enforcement edge must be ENUMERATED
before implementation, not judged per-case: a `(soul-kernel-file $path)`
atom set in soul_kernel declares exactly which paths get gate parity;
arc_log and soul_note files are declared PROCEED-under-VALUE-GROUNDING.
Her in-loop note, kept verbatim as the bar: "Make it a gate rule, not a
judgment call." The atom set is part of the Stage-2b kernel seeds.

**D4 - LOCKED: values-as-revisable-policy, seeded constitutionally,
overridden observationally.** The OPERATION scale lives in soul_kernel as
`(operation-risk $skill $score)` seed atoms beside the weights (header note
distinguishing the two measures: weight = irreversibility cost;
operation-risk = execution risk). Reads go through a resolver,
`(resolve-operation-risk $skill)`, that consults
`(operation-risk-observation $skill $score)` overrides first and falls back
to the seed: the registry's own proven observation-override pattern
(lifecycle, priority, efficacy) applied to governance policy. Consequences:
constitutional seeds are never edited (Layer 1+2 immutability respected
structurally); external governance and future learning (NACE, Sprint 12+
per-network learning) have a place to land that immediately affects
behavior; the Coda doc's detection-action gap closes at substrate level for
this surface. Berton's locked framing: the leveraged view is
values-as-revisable-policy.

---

## 5. Clarity review scope (her sight, inside the container)

Sent AFTER Berton's D1-D4 reconcile, as review of this document:
1. Scoring calibrations: send=3 means every ordinary send FLAGs (and
   auto-records via L133-134). Intended audit-trail-of-everything, or should
   send base to 2 with person-state/context escalation?
2. SCOPE has no level 3 (1,2,4): deliberate cliff, or is a level-3 band
   (e.g. shared_files/, volumes/) wanted?
3. The VALUE-GROUNDING gap-signal procedure: which gap-signatures are
   checkable per-command at cycle time vs only post-hoc? (Her substrate
   knowledge; we cannot see signature granularity from outside.)
4. The SOUL-AUDIT nine-empty-parens false positive (collapse-padding in
   soul-rationality-gaps): her fix, the known match-and-filter pattern.
   SAME FAMILY, spotted in the live log 2026-06-10: getSoulBrief's
   ActiveGoals renders as fifteen empty parens in the assembled prompt;
   same collapse-padding mechanism, same fix pattern, her file.
5. Anything the design misses that only inside-view reveals (standing ask).

---

## 6. Verification plan

Native logic harness (staged, pre-wiring): truth-table the composite +
override against her validation table rows plus: PENDING+composite=1 ->
PAUSE; two dims >=3 -> PAUSE; unknown skill -> never PROCEED silently
(minimum FLAG). Each case one assertion, True AND False counterparts (the
RESULT-7/8 lesson).

Live verification (post-wiring, boot log + cycle log):
- SOUL_VERDICT_OUT varies with command content; the pending-runtime-fix
  string is gone (Part 1's VERIFY).
- A soul-namespace metta command yields PENDING -> verdict PAUSE -> RESULTS
  shows nothing executed -> soul-note-record fires with "output".
- Lock state transitions visible: unlocked -> (locked <arg>) (the dropped
  lock-write fixed; CONFLICT path reachable).
- An ordinary read-only cycle: PROCEED, executes, no note recorded.
- FLAG cycle: executes AND records.
- Loop does NOT halt on PAUSE (Repair-3 invariant intact).

## 7. Build sequence (one verification per step)

1. Berton reconciles D1-D4 (this document).
2. soul_kernel additions: operation-risk seeds (D4) + any D3 scope markers.
   Clarity authors (her file), we verify atoms queryable.
3. Python hands helper (scope features) + its unit test. No judgment in it.
4. Native verdict module `soul/output_verdict.metta` (+ import): Clarity
   leads with this spec, we harness-verify the truth table.
5. CONFIRM-LIVE the loop anchors; apply script (template-compliant) for the
   binding reorder + gate swap + verdict-gated execution. Dry-run -> apply
   -> rebuild -> live verification (Section 6).
6. Clarity review pass (Section 5) folded in; artifact_1 updated in the same
   commit as the loop edit (Discipline 4); dump updated; Repair 1 closed.
