# ClarityOmega Revision 1: Investigation State and Knowledge Dump

**Purpose:** Complete, self-contained snapshot of where the Revision 1 (soul-fully-wired
restoration) investigation stands. Captures the local environment, work done and committed,
what is queued, all open questions, and how apply scripts are drafted (including the
template). Written as a knowledge dump: a fresh reader (or a fresh Claude thread) should be
able to resume from this document alone.

**Date:** 2026-06-09. **Branch:** `fix/F-HISTORY-CONTAMINATION-archival`.

---

## 1. The mandate and the working discipline

**Mandate (Berton):** one spine, the soul, navigating from a single consistent set of
spec-defined values across all surfaces. Prove a divergence is drift-in-application before
fixing it; until proven drift, it stays under investigation. Once proven drift: fix the
drift files and the production files consuming the drift so everything doing real runtime
work uses spec, and archive the non-runtime files.

**Revision 1 scope:** the restoration of the soul-fully-wired runtime. It is SIX surfaces
(five repairs from the prior pre-flight plus the value-spine drift discovered this session),
landed as one coordinated body of work. Restoration before extension.

**Standing conventions (enforced every session):**
- No em-dashes anywhere in any output.
- Repo-root-relative paths throughout.
- One coordinated change per wire; reversible apply scripts (dry-run default, `--apply`,
  `--reverse`); scripts run from `staging/`.
- Surgical `git add` (never `git add .`).
- Paren-delta zero enforced by apply scripts.
- Every RECONCILE surface goes to Berton before its script is written.
- No apply script is written until its surface's CONFIRM-LIVE points are checked against the
  live container.
- Container / docker-logs output is ground truth. Verify against the live process, not a
  fresh boot (a fresh `docker exec run.sh` boots an EMPTY atomspace and cannot see the live
  loop process's memory).
- Read source before asserting. Prove from git and container output; do not speculate when a
  fact is recoverable.
- The log is the gold.

---

## 2. Local environment

**Repo:** `github.com/Berton-C/ClarityOmega`. Upstream: `github.com/asi-alliance/OmegaClaw-Core`
(Patrick Hammer / patham9). Repo-root working dir: terminal is always at repo root, no `cd`.

**Docker:**
- Compose service: `clarityclaw`. Running container: `clarity_omega`. Image:
  `clarityclaw-omega-clarityclaw`. Working dir inside container: `/PeTTa`. Repo path inside
  container: `/PeTTa/repos/omegaclaw/`.
- Build (required for any in-repo change, layer caching is a trap):
  `docker compose build --no-cache clarityclaw`
- Start: `docker compose up -d`
- Live state inspection (running process): `docker logs clarity_omega 2>&1 | grep -E "pattern"`
- Filesystem/grep inside container: `docker exec clarity_omega sh -c '...'` (the container
  runs continuously, so `docker exec` works; some references to a fast-restart pattern used
  `docker run --rm --entrypoint`, but `exec` is the working path now).

**Runtime stack:** PeTTa (SWI-Prolog-based MeTTa interpreter), MeTTa/AtomSpace, Janus Python
bridge, ChromaDB (embeddings + state), Mattermost (Clarity's channel). Platform: Docker
Compose on Mac M4. APIs: Anthropic (Claude inference via LiteLLM proxy) + OpenAI
(text-embedding-3-large, required by the hardcoded memory system).

**Key file locations (repo-root-relative):**
- Loop source: `src/loop.metta` (live loop is 171 lines).
- Helper Python: `src/helper.py`.
- Soul atoms: `soul/`.
- Library import chain: `lib_clarity_reasoning/lib_clarity_reasoning.metta`.
- Spec single source for the value-spine: `soul/soul_kernel.metta`.
- Specs/design: `docs/design/`. Decisions: `docs/decisions/`. Investigations:
  `docs/investigations/`. Sprint docs: `docs/sprints/soul_fully_wired/`.
- Archive destination for non-runtime files: `staging/OLD/OLD_soul_files/`.
- Apply scripts run from: `staging/`.

**Shell gotchas observed this session:**
- A stray `</parameter>` pasted into a command causes a zsh parse error. Clean the paste.
- `grep -c` exits non-zero when the count is 0, which aborts `&&` chains. Avoid chaining
  after a `grep -c` that may legitimately return 0, or use `; ` separators.
- Do not chain heredocs with `&&` (zsh will not terminate them correctly).

---

## 3. The spec single source (ground truth for the value-spine)

`soul/soul_kernel.metta`, proven by source read:
- Priority: `(priority A N)` x5, accessor `soul-priority-hierarchy` (L328).
- Tensions: `(tension-vector T)` x5 (L280-284), accessor `soul-all-tensions` (L333).
- Irreversibility: numeric `(irreversible-weight skill N)` x7 (L479-485), accessor
  `soul-irreversible-weight` (L508: `(match &self (irreversible-weight $skill $w) $w)`).
- Paraconsistency: `(soul-paraconsistent-pair A B)` x4 (L428-431), accessor
  `soul-paraconsistent-pairs` (L502), predicate `soul-paraconsistent?` (L505).
- Patterns: `(soul-pattern Name "desc")` + companions, the nine flourishings (AgencyBalance,
  CognitiveResilience, ConnectionDepth, WonderPreservation, TimeCoherence,
  PurposeBeyondUtility, SharedUnderstanding, CreativeTranscendence, AttentionStewardship).

Container atom-count greps proved these are LIVE in the running process. The boot log shows
two separate load mechanisms: prose loaded via `(remember ...)` into ChromaDB, and
soul_kernel atoms loaded via import.

---

## 4. Work done and committed

### 4.1 Committed: native soul mutation gate (commit 01ca459)
- `soul/soul_mutation_gate_corrected.metta` (four native structural functions:
  soul-is-metta-cmd?, soul-extract-metta-arg, soul-metta-targets-soul-namespace?,
  soul-mutation-pending?; 12/12 proof harness green) and
  `soul/soul_namespace_membership_seed.metta` (119 soul-ns-member tags).
- Wiring contract (proven): the gate must receive the `metta()` expression UNEVALUATED
  (quoted) or it executes the mutation instead of inspecting it. Proven call forms
  (proof log soul_gate_callform_log_20260608_184234): form B for extract,
  `(soul-extract-metta-arg (quote (metta ...)))`, and form E for namespace targeting,
  `(soul-metta-targets-soul-namespace? (quote (add-atom ...)))`. Quote at the call site;
  the pattern match works through the quote. Test-design lesson from the harness: a test
  whose expected answer is False can pass for the wrong reason on wrong input (RESULT-7/8
  once did); pair every False expectation with a True counterpart.
- Lock representation (load-bearing divergence from the master doc): the committed gate
  uses STRUCTURAL lock states, `unlocked` and `(locked <arg>)`. The master doc's string
  form (`"LOCKED: ..."` checked via string-contains) is dead in this runtime:
  string-contains, substring primitives, and string_length are all confirmed dead (commit
  01ca459 message). Repair 1 restores to the doc's INTENT via the committed gate's
  structural forms, never the doc's literal Section 14 text.
- The set-aside script is `staging/apply_repair1_output_intercept_v4.py`, written against
  old assumptions. Its four reconcile points before any use: (1) call the proven functions
  as committed in 01ca459; (2) structural lock writers (clear writes `unlocked`, hold
  writes `(locked <arg>)`); (3) honor the quoted-expression contract end to end, including
  tracing where the metta() command originates in the live loop so it reaches the gate
  unevaluated; (4) anchor to real live loop text, not stale copies. It must also be rebuilt
  to the Section 8 template.
- Sequencing rationale of record (Berton): the output verdict and the mutation gate are ONE
  coordinated output-governance change because the unit of work is "soul on spec," not
  files changed. The source proved the dependency: the gate's flag can only force PAUSE
  through the output verdict, and the verdict needs the gate's flag as an input. Three
  things move together: the proven native gate functions, the lock-write fix, and flag
  consumption through a real verdict. They are one function.
- Status: committed, NOT yet wired into the loop. HEAD line: 01ca459 -> cdb5184 (artifact_1
  v1.3 re-anchor to the live 171-line loop) -> f37aa6c (origin). Branch ahead of origin by 2,
  intentionally NOT pushed (Berton's call).

### 4.2 Investigation complete this session: value-spine drift (Surface 6)
Fully scoped and proven, mechanically validated, NOT yet applied. See Section 6.

### 4.3 Documents produced/maintained (in docs/sprints/soul_fully_wired/ and outputs)
- `Restoration_PreFlight_Five_Surface_Inspection.md` (now six surfaces): per-surface
  CLEAN-vs-RECONCILE pre-flight. Surface 6 (value-spine drift) added this session.
- `Master_Doc_Compliance_Findings.md`: faculty-placement map (ADR-008 executing-vs-judging).
  Key calls: soul-llm-call = PROGRESSION (preserve, never restore to useGPT);
  soul_mutation_gate = REGRESSION (restore to native, fixes dropped-lock); input brief
  (soul_brief_tier_a_static) = RECONCILE; soul_is_pause router = RECONCILE + gated.
  CORRECTION carried: Repair 1 verdict input = `(repr $sexpr)` per master doc L1434, NOT
  `(repr $metta_cmds)`.
- `Inverse_Audit_Runtime_Beyond_Doc.md`: the reverse-regression guard. PRESERVE list
  P-1..P-10 (task-state primitive, idle-pattern + agency-balance organs, recent-action + DIAG,
  corner_gap L5, soul-llm-call, idle/genesis subsystem, aliveness SILENT path,
  sanitize/service-learning, user-context, upstream history-on-autonomous-output). DECIDE
  items D-1..D-4.
- `ValueSpine_Drift_Investigation_Findings.md`: the full evidence chain behind Surface 6
  (expressive-capacity test per file, four-representations map, import-chain proof, three
  consumer sweeps, redirect-target proof, dual-head/verdict-soundness reasoning, option-(a)-
  is-mandate-forced).
- Also present: ADR-008-reasoning-is-claritys.md, Soul_Governance_Verdict_Surface_Survey.md,
  Soul_Restoration_Spec_Part1_Ground_Truth.md, Soul_Extension_Spec_Part2_Accumulating_Knowledge.md,
  artifact_1_loop_metta_wiring_diagram_v1.3.md, corner_gate_surface_map.md.

### 4.4 Prior landed work (context)
- Sprint 0 closed at 7142703 (capability registry dispatcher, ADR-006, ADR-007).
- Task-state primitive v3 committed at c063618.
- corner_gap Layer 5 wired (prior session).

---

## 5. The six surfaces of Revision 1 (status each)

| Surface | Repair | Verdict | State |
|---------|--------|---------|-------|
| 1 Output intercept | 1 | RECONCILE | mutation-gate machinery partly wired; connect, do not recreate. Verdict input `(repr $sexpr)`. Restore native gate (01ca459). Keep soul-llm-call. Verdict LOGIC = OPEN-1 (Clarity). |
| 2 Channel D note | 2 | CLEAN | interpolate extracted soul-note where helper.py L375 has the placeholder. |
| 3 soul_is_pause | 3 | RECONCILE + gated | bare-string (v9 L310) vs command-scoped (helper docstring): which is the validated original? Berton decides. PAUSE-effect stays 0 until this repair. |
| 4 Mode 2 | 4 | RECONCILE | MeTTa wrappers exist substrate-side (soul_utils 287-346); wire loop to them, do not rebuild. Adjacency-flag vs P-1 task-state. |
| 5 D-lite + ack_sent | 5 | CLEAN | add `&soul_ack_sent` to initLoop; wire existing composer (helper.py 382) at FLAG+distress. |
| 6 Value-spine drift | (prereq for 1) | RECONCILE | remove four-family drift to single spec source, redirect the one consumer, archive non-runtime; passes reverse-regression guard. Full evidence in ValueSpine_Drift_Investigation_Findings.md. |

Two CLEAN (2, 5), four RECONCILE (1, 3, 4, 6). Also a RECONCILE surfaced by the compliance
doc: the INPUT brief (soul-brief-symbolic vs soul_brief_tier_a_static), faculty + content,
Berton decides progression-vs-regression.

---

## 6. Surface 6 in detail (the build-ready drift fix)

**The drift, proven:** the value-spine is declared in more than one place with divergent
shapes. Two runtime producer files:
- `soul/identity_kernel.metta` (cycle-2340 rebuild; imported at lib_clarity_reasoning L22):
  divergent duplicates of all four families (priority-rank, tension-vector exact-dup,
  paraconsistency-pair, magnitude irreversible-weight). None unique.
- `soul/genesis_engine.metta` L22-25: `(paraconsistency-pair N) -> (pair A B)` = the four
  spec pairs in a local indexed shape. Only this declaration is drift; the genesis/encounter
  machinery is real capacity (P-6 PRESERVE).

**Dual-head consequence:** identity_kernel magnitude + soul_kernel numeric irreversible-weight
make `soul-irreversible-weight send` return BOTH values. This makes Repair 1's value-grounding
verdict nondeterministic, so Surface 6 is a prerequisite-within-Revision-1 for Repair 1.

**The one runtime consumer of a drift shape:** `continuity_driver.metta` L52, inside
`(check-soul-file genesis-engine)`, a startup load-probe calling `(paraconsistency-pair 1)`.
Proven sole consumer via three container sweeps. Redirect target proven:
`(paraconsistency-test Safety Helpfulness)` (genesis_engine L196 survives the fix, reduces to
`(tension-confirmed Safety Helpfulness)` when loaded).

**Naming-collision guard:** continuity_driver L234/277/279 use `(priority ...)` for
goal-priority, a DIFFERENT namespace; MUST NOT touch.

**The Surface 6 edits (mechanically validated against a staged repo this session):**
1. Remove identity_kernel import (lib_clarity_reasoning L22) + archive identity_kernel.metta.
2. Remove genesis_engine paraconsistency-pair declarations (L22-25). Real logic stays.
3. Redirect continuity_driver L52 to `(paraconsistency-test Safety Helpfulness)`, testing
   `== (tension-confirmed Safety Helpfulness)`. Paired with edit 2.
4. Archive the non-runtime set to `staging/OLD/OLD_soul_files/`: proposed_tension_atoms.metta,
   flourishing_extentions/, proposed_substrate_capacities.metta,
   flourishing_completeness_analysis.metta, hyperseed_extensions/, tension_auto_logger.metta.
5. Remove session scaffolding from soul/: soul_accessor_live_harness.metta,
   soul_value_materials_harness.metta.
6. Update artifact_1 for the import-chain + continuity_driver changes (Discipline 4).

**Reverse-regression: passed.** No PRESERVE item endangered (genesis_engine's paraconsistency-pair
declarations are orphaned within the file, used only by the redirected continuity_driver probe;
P-1 and the rest have no overlap; archival set is not imported and not consumed).

**Archival set is non-runtime, proven:** none appear in the import chain (lib_clarity_reasoning
L6-91), none are consumed.

**CONFIRM-LIVE before the script (re-confirm against the live container):** lib_clarity_reasoning
L22 (identity_kernel import), genesis_engine L22-25, continuity_driver L51-55, the archival
files present and absent from the import chain, the artifact_1 anchors.

---

## 7. Open questions and remaining tasks

### 7.1 Open questions (must close before/within the build)
- **OPEN-1 (Clarity's domain):** the value-grounding verdict LOGIC for Repair 1. What it
  computes from operation + scope + value-grounding (NO actor; the actor is invariant on the
  output side, so value-grounding replaces it), and how it maps to PROCEED/FLAG/PAUSE.
  Defined against the CLEAN single-source spec shapes Surface 6 produces. Decided framing:
  FLAG is observational only (log-and-annotate); only PAUSE halts; never blanket-classify
  (evaluate the specific command + full path). PRIOR ART (cite in the task to Clarity):
  her own `soul/soul_precision_proposal.metta` (77 lines, April 2026), the three-dimension
  composite-risk design (OPERATION / SCOPE / ACTOR) with always-critical overrides
  (destructive ops always critical, network egress always critical, unknown actor always
  elevates), verified April 26/27 on the berton_c `ls /soul` before/after case. The
  output-side verdict swaps ACTOR for value-grounding; the rest of her vocabulary carries.
- **OPEN-2:** how operation and scope are determined from `$sexpr`/`$metta_cmds` at loop L126.
  Needs a source check of what `$sexpr` contains there.
- **OPEN-3:** exact loop anchors (L126 verdict stub, L128-130 $metta_cmds, L131 gate call,
  L132 consumer, L148 PAUSE router) and how the gate flag feeds the verdict instead of being
  dropped. SHARPENED 2026-06-09: the two in-hand references DISAGREE. The session and
  artifact_1 v1.3 say a 171-line loop with these anchors; the refreshed project copy
  (loop_copy_metta.txt) is 179 lines with the corner gate fully wired (stub at 127,
  metta_cmds 129-131, gate call 132, consumer 133-134, corner gate 135-143, PAUSE router
  155, history 168). CONFIRM-LIVE against the container is therefore mandatory, not
  pro-forma, before any anchor is written.
- **OPEN-4:** artifact_1 anchors for the output-governance phase (for the Discipline 4
  maintenance update).
- **OPEN-5:** reconcile the Option-1 L148 OR (fold output verdict into the existing
  soul_is_pause check) with the PAUSE-stays-0-until-Repair-3 invariant. Does adding the
  output verdict to the OR activate PAUSE before Repair 3? Must not. ALSO (2026-06-09): the
  live PAUSE path resets `&soul_verdict_in` to PROCEED before halting (project-copy L163).
  When the output verdict joins the OR, the reset needs an output-side equivalent or a
  PAUSE-carrying output verdict could linger across the halt.
- **Surface 3 decision (Berton, gated):** bare-string vs command-scoped PAUSE.
- **Input-brief decision (Berton):** progression (intentional tier-A-only economy) vs
  regression (drift from native full brief); and separately whether the Python builder is an
  ADR-008 reclamation candidate.

### 7.2 Remaining tasks (sequence)
1. Berton signs off the RECONCILE surfaces' approaches (the established rule). Surface 6 is
   the most ready.
2. CONFIRM-LIVE pass for Surface 6 against the live container.
3. Close OPEN-2/3/4/5 by source-reading the live loop.
4. Route OPEN-1 to Clarity (verdict logic against clean shapes).
5. Build ONE template-compliant apply script for the coordinated change (see Section 8).
6. Validate (staged-repo dry-run/apply/reverse, then live-anchor dry-run).
7. Apply, `docker compose build --no-cache clarityclaw && docker compose up -d`.
8. Verify (Section 9).
9. Commit Revision 1.

### 7.3 Queued, not blocking
- Conservative-fallback for a novel untagged `soul-` head in the mutation gate.
- Seed-inclusion confirmation (all 119 tags vs data-only).
- Re-read soul_unification_proposal at input-brief reinstatement.
- Confirm SOUL-AUDIT nine-empty-parens is a false-positive post-apply (likely clears once
  identity_kernel's divergent atoms are removed).
- Naming cleanup pass (legacy ClarityClaw/MeTTaClaw -> ClarityOmega across docs).

---

## 8. How we draft apply scripts (the template)

**Template of record:** `apply_task_state_step2_wiring.py` (726 lines). Every Revision 1
apply script conforms to its structure. The set-aside drift-fix script written earlier this
session is NON-COMPLIANT with this template and must be rebuilt to it.

**Required structural elements (from the template):**
- **Module docstring** enumerating each edit with its anchor and the forward/reverse intent,
  plus usage lines (dry-run default; `--apply`; `--reverse`; `--reverse --apply`).
- **argparse** for `--apply` and `--reverse` (not hand-parsed sys.argv).
- **`code_aware_paren_count(text) -> (open, close)`:** counts parens EXCLUDING those inside
  string literals and comments. This is mandatory; a naive `count("(")` miscounts any paren
  in a comment or string, and edits that replace code with comments will mis-tally.
- **`find_target_lines` / `find_target_substring_count`:** locate and count anchors; an
  anchor must occur exactly once or the script halts with no writes.
- **Per-file forward and reverse SIMULATION functions** (`simulate_<file>_forward/reverse`):
  produce the edited content in memory without touching disk.
- **Per-file forward and reverse STATE-CHECK functions** (`<file>_forward_state_ok`,
  `<file>_reverse_state_ok`): verify the file is in the expected PRE-state before editing and
  the expected POST-state after, in both directions.
- **`diff_preview_first_change(old, new, label, context)`:** show the actual diff of the
  first change in dry-run, so the change is visible before applying.
- **`process_file(...)`:** read, run pre-checks, simulate, run post-checks, compare paren
  counts (open/close delta must be 0), compare expected line-delta (negated on reverse),
  return (success, original, simulated).
- **`verify_disk(...)`:** after a write, re-read from disk and confirm the file is in the
  expected post-edit anchor state (forward leaves reverse-anchor state, and vice versa).
- **`check_file_exists`** for file moves.
- **`main()`:** orchestrates all files, prints an ACTION-SUMMARY, halts the whole run if any
  file fails its checks (all-or-nothing; no partial writes).

**Discipline applied to the script body:**
- Dry-run is the DEFAULT (no flag = simulate + preview + checks, no writes).
- Anchors are exact current text; mismatch halts with no writes.
- Paren-delta enforced at 0 per file and net.
- The artifact_1 maintenance update (Discipline 4) is part of the same script when the change
  touches the wiring artifact_1 documents.
- File moves (archival) are reversible: forward moves to staging/OLD/OLD_soul_files/, reverse
  moves back. Deletions of session scaffolding are flagged as not-auto-restored (recoverable
  from outputs).
- Run from `staging/`. Repo-root-relative paths. No em-dashes in output.

**Validation procedure before `--apply` on the live repo:**
1. Build a minimal staged repo mirroring the touched files; run dry-run, `--apply`, then
   `--reverse --apply`; confirm each edit lands and fully reverses.
2. Run dry-run against the LIVE repo to confirm anchors match the live files (the staged test
   uses copies; live anchors are what matter).
3. Only then `--apply` on the live repo.

---

## 9. Verification after apply (Revision 1)

- `soul-irreversible-weight shell` returns a SINGLE value (3 only, not 3 and a magnitude):
  the decisive dual-head-resolved check.
- `soul-paraconsistent-pairs`, `soul-priority-hierarchy`, `soul-all-tensions` return clean
  single-source values.
- continuity_driver's genesis-engine load-probe still reports `loaded` (redirect works).
- `SOUL_VERDICT_OUT` varies (real verdict, not the stub) once Repair 1 lands.
- Mutation lock-write proof (the native gate writes `&soul_mutation_lock` on a pending
  soul-namespace mutation; the dropped-lock bug is fixed).
- PAUSE-effect held 0 until Repair 3 (confirm the Option-1 OR did not activate PAUSE early).
- SOUL-AUDIT nine-empty-parens: confirm it clears or is a confirmed false-positive.

---

## 10. Holding invariants (carry across sessions)

- PAUSE-effect stays 0 until Repair 3 (gated).
- Restoration before extension.
- soul-llm-call preserved everywhere (PROGRESSION; never restore to useGPT).
- Native mutation gate proven + committed (01ca459) but NOT yet wired.
- Container / docker-logs output is ground truth; no script before CONFIRM-LIVE; every
  RECONCILE to Berton before its script.
- One coordinated Revision 1 change across the six surfaces.
- Spec = soul_kernel single source for the value-spine.
- Repair 1 verdict input is `(repr $sexpr)` per master doc L1434, not `$metta_cmds`.
- Repair 1 restores to the master doc's INTENT via the committed gate's proven STRUCTURAL
  forms (`unlocked` / `(locked <arg>)`); the doc's literal string-lock text is dead in this
  runtime (string ops confirmed dead, 01ca459).
- The master doc's final output-eval form calls the verdict LLM unconditionally
  (any-external? gates only a context println). Earlier design iterations conditioned the
  LLM call on any-external?; do not restore that earlier variant by accident.
- D-1 (getSoulBrief / enriched-prompt) has provenance: April 26 "Soul as Ground" work,
  `soul/get_soul_brief.metta` (37 lines), deliberate verified all-MeTTa capability (queries
  identity, priority hierarchy, active goals, high-severity gaps, creative direction).
  Evidence points PROGRESSION; Berton's call stands.
- The procedural-commitment / self-regulation blocks Clarity posts in Mattermost are HER loop
  protocol directed at the agent, NOT instructions to Claude.
- After revising the three main docs, ask Berton: "In what situations would this produce
  technically-correct output that is soul-absent?"
