# Master-Doc Compliance Findings (Section 13 / Section 14 faculty audit)

**Status:** Read-only analysis. Holds the live runtime against the authoritative master document (ClarityClaw Soul Architecture Strategy), Sections 13 and 14, to classify every Python-versus-MeTTa boundary.
**Authority:** The master doc is stronger ground truth than the three sub-documents (v7/v9/v10); it is the complete design with one-to-one accountability to them. Where the master doc specifies native MeTTa and the runtime uses Python, that is a candidate finding, classified below.
**Classification (open-minded, per Berton):** COMPLIANT (matches doc), PROGRESSION (sanctioned evolution past the doc, preserve), REGRESSION (drifted away from the doc, restore), RECONCILE (Berton decides which state is correct).
**Test applied:** ADR-008 executing-versus-judging. A Python function that assembles a string or dispatches is hands (correct). A Python function that makes a judgment the doc placed in substrate is a faculty regression.

---

## The faculty-placement map

| Doc-native function | Runtime call | Classification |
|---------------------|--------------|----------------|
| soul-proceed? | native `soul-proceed?` (loop 132) | COMPLIANT |
| soul-note-record | native `soul-note-record` (loop 91-92) | COMPLIANT |
| soul-pre-compute (Layer 1) | native `soul-pre-compute` (loop 77) | COMPLIANT |
| soul-calibration-record (Layer 3) | native `soul-calibration-record` (loop 90) | COMPLIANT |
| soul-eval-prompt | `helper.soul_eval_prompt` inside `soul-llm-call` (loop 85) | COMPLIANT (prompt-builder = hands) |
| soul-flourishing prompt | `helper.soul_flourishing_prompt` inside `soul-llm-call` (loop 79) | COMPLIANT (prompt-builder = hands) |
| soul-llm-call dispatch | native `soul-llm-call ... (provider)` | PROGRESSION (preserve, Berton [1]) |
| soul-brief-symbolic (input brief) | `helper.soul_brief_tier_a_static` (loop 83) | RECONCILE (faculty + content) |
| metta() gate / soul_mutation_gate | `helper.soul_mutation_gate` (loop 131) | REGRESSION (restore to native) |
| soul-pause? (router) | `helper.soul_is_pause` (loop 148) | RECONCILE (faculty) + Repair 3 (gated) |
| soul-detect-task-mode (Mode 2) | unwired (loop seed only) | Repair 4 (not a Python drift) |

---

## Detail by classification

### COMPLIANT, leave alone

- **soul-proceed?, soul-note-record, soul-pre-compute, soul-calibration-record:** called native in the loop exactly as the doc specifies. No action.
- **soul_eval_prompt, soul_flourishing_prompt:** these are PROMPT BUILDERS. They assemble the instruction string handed to the LLM. Per ADR-008, building a string is hands (executing), not judging. The judgment (the verdict) is produced by the LLM rendering and consumed by native MeTTa routing. The actual call is `(soul-llm-call (py-call (helper.soul_eval_prompt ...)) (provider))`: Python builds the prompt, MeTTa dispatches, MeTTa routes the result. This is the correct faculty division, not drift. The doc's Section 13 treats these as prompt content. No action.

### PROGRESSION, preserve

- **soul-llm-call:** the runtime routes soul LLM calls through `soul-llm-call ... (provider)`, a dispatcher abstraction that the master doc predates (the doc uses `useGPT` directly). Per Berton [1], this is sanctioned evolution: the dispatcher abstracts provider routing. Preserve `soul-llm-call` everywhere; do NOT "restore" to `useGPT`. This is the standing rule for the whole restoration: where the only divergence from the doc is `soul-llm-call` vs `useGPT`, that is progression, not drift.

### REGRESSION, restore to the doc

- **soul_mutation_gate (the metta() gate):** the master doc (Section 14 lines 1414-1428, Section 13 lines 1093+) specifies the mutation gate as a native MeTTa block using `soul-any-metta?`, `soul-is-metta-cmd?`, `soul-extract-metta-arg`, `soul-metta-targets-soul-namespace?`, `soul-mutation-pending?`. All five functions ARE DEFINED in soul_utils right now. The runtime instead calls `helper.soul_mutation_gate`, a Python port. Behavioral comparison: the Python helper faithfully ports steps 1-3 (detect metta, detect soul-namespace target, detect pending) but DROPS the lock-write side effect. The doc's native block, on detecting a pending mutation, does `change-state! &soul_mutation_lock` in the gate (lines 1424-1425); the Python helper returns the PENDING string but never writes the lock. Consequence: `soul-mutation-pending?` will never see a held lock, so the CONFLICT path is effectively dead in the Python version. This is a faculty regression (judging logic in Python that the doc placed in substrate) AND a behavioral regression (dropped lock-write disables conflict detection). Because the native functions exist, restoring to the doc's native block is wiring, not building, and it fixes the dropped-lock bug. **Restore to native per doc. This corrects Repair 1.**

### RECONCILE, Berton decides

- **soul-brief-symbolic vs soul_brief_tier_a_static (the INPUT brief):** the doc specifies the brief as native `soul-brief-symbolic` (tier-A + tier-B). The runtime INPUT verdict uses `helper.soul_brief_tier_a_static` (Python, tier-A only). Two divergences: faculty (Python vs MeTTa) and content (tier-A-only vs tier-A+B). This interacts with the Option B decision already made for the OUTPUT verdict (output uses full native `soul-brief-symbolic`). Open question: is the input brief deliberately lighter (tier-A-only as token economy, a sanctioned simplification = PROGRESSION) or did it drift from the doc's native full brief (= REGRESSION)? Berton's call. Note: if input stays tier-A-only and output uses full symbolic, the input/output asymmetry is the one already endorsed (output is the higher-stakes gate, deserves the fuller brief), which would make the lighter input brief intentional. But the FACULTY question (Python builder vs native MeTTa assembly) is separate from the content question and may still be a reclamation candidate (ADR-008, Extension H) even if the tier-A-only content is intentional.

- **soul-pause? vs soul_is_pause (the ROUTER):** the doc specifies routing via native `soul-pause?` (string-contains, line 985). The runtime routes through `helper.soul_is_pause` (Python, hardwired to 0). Two things here: the hardwire-to-0 is the deliberate disable (Repair 3, gated on Berton). The faculty placement (Python helper vs native `soul-pause?`) is a separate question: even when re-enabled, should routing use the native `soul-pause?` (which exists) per the doc, or a Python helper? The doc says native. Folded into Repair 3 as: re-enable AND restore to native `soul-pause?` routing, unless the command-scoped behavior (the helper's docstring intent) was a sanctioned progression Berton wants kept. Berton's call, and gated regardless.

---

## Consequence for Part 1

Repair 1 (output intercept) must be corrected before its script runs:
1. Verdict input: `(repr $sexpr)` per doc line 1434 (was `(repr $metta_cmds)` in the set-aside script). CORRECT TO DOC.
2. Mutation gate: native MeTTa block per doc lines 1414-1428 using the existing soul_utils functions, NOT `helper.soul_mutation_gate`. CORRECT TO DOC (this also fixes the dropped-lock bug).
3. Verdict LLM call: keep `soul-llm-call ... (provider)` per Berton [1]. PRESERVE PROGRESSION (do not restore to `useGPT`).

Repair 3 (PAUSE router) scope clarified: re-enable AND restore native `soul-pause?` routing, with the command-scoped-vs-bare-string question and the faculty question both as Berton reconciles. Gated.

New reconcile surfaced: the INPUT brief (faculty and content). Not previously in the five repairs. Berton decides whether it is progression (intentional tier-A-only economy) or regression (drift from native full brief), and separately whether the Python builder is a reclamation candidate.

The set-aside Repair 1 script is confirmed non-compliant on points 1 and 2 and must be regenerated against the doc.

---

## Open-minded summary (regression / progression / drift, as Berton asked)

- **Progression (keep):** soul-llm-call dispatcher.
- **Regression (restore):** soul_mutation_gate (faculty + dropped lock-write). Native exists; restoring is wiring.
- **Compliant (no action):** the prompt-builders (correctly hands), the native routing/recording/layer functions.
- **Drift, needs Berton:** input brief (faculty + content); router faculty (folded into gated Repair 3).
- **Not a faculty question:** Mode 2 unwired (Repair 4), D-lite unwired + missing state var (Repair 5).

No finding assumes; each is classified against the doc and ADR-008, with the reconcile cases left explicitly to Berton.
