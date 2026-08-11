# 0g Inquiry 24: Adversarial Countermodel Search and Proof-Assistant Hardening

**Status:** ADVERSARIAL VERIFICATION REPORT WITH EXECUTED MACHINE RESULTS. Answers Berton's directive: subject the exact Gate B signature to adversarial countermodel search and proof-assistant hardening before Gate E runtime projection. Not governing ground; 006 and 0e win on any conflict.
**Version:** v1, 2026-08-06.
**Companion executables (all run in the session that produced this report, outputs saved):**
- `0g_adversarial_suite.py` and `0g_adversarial_run_report.txt` (mutation testing and countermodels against the shipped Gate C verification)
- `0g_smt_hardening.py` and `0g_smt_run_report.txt` (Z3 bounded countermodel search over the laws themselves, plus repair proofs)
- `0g_hardened_checks.py` and `0g_hardened_run_report.txt` (the repaired checker: base model still passes; every demonstrated vacuity now detected)
- `0g_lean_skeleton.lean` (mechanization skeleton; NOT compiled, no Lean toolchain in the producing environment; every theorem is a named obligation)

**Scope discipline:** no new mathematical family is introduced. Every countermodel is built inside the shipped finite interpretations or inside bounded fragments of the K0 to K17 laws as written. Every proposed repair is a delta to the existing signature, admitted under 0c 1.3 clauses 1, 3, and 5 (missing construction for a named obligation; counterexample against a current candidate; new falsifier).

---

## 0. Provenance note

Read end to end this session: `0e` (all 2105 lines) and both verification reports. Read in targeted depth: both Gate B documents' structure and their shared K0 to K17 obligations, and the complete check-function internals plus model construction of `0f_gate_c_finite_model_check.py`, with the corresponding guard internals of `verify_0f_gate_c_finite_model.py`. Both shipped verifiers were executed and confirmed to pass as shipped before any adversarial work began. All claims about checker behavior below are claims about executed runs, not readings.

---

## 1. My read of the formalization as it stands

### 1.1 What genuinely stands up

The trajectory 006 to 0a to 0c to 0d to 0e to 0f is a disciplined narrowing, and the adversarial results confirm that much of the structure is real rather than decorative. Under mutation, the shipped verification **detects** eight of fourteen law-violating mutants: authority-before-assembly, self-generated authority contact, withdrawn materiality, recovery without prior loss, promotion to the contact apex, interpretation rewrite, anchor prior-row rewrite, and an unlisted renderer writer. The witness-versus-act separation, anchor conservativity machinery, append-only interpretation, the four-standing lifecycle with a separate operational-status type, and above all the transaction-and-causal-cut writer discipline are solid: they resist tampering at the machine level, not just in prose. The CarrierOpen-versus-Discharge separation is realized, and the trace-severed-arm contrast is genuinely constructed rather than asserted.

### 1.2 The fork in the formal record

Two parallel Gate B documents exist, both v0.2, both dated 2026-08-05, with different repair sets (one carries repairs B1 to B6), different companion verifiers, and different finite interpretations. Berton's directive says "this exact signature," singular; the record currently contains two. This is a process finding, not a mathematical one, but it is Gate-blocking: the 0d-to-0e adjudication pattern must be applied once more to select or merge before any Gate E projection, because runtime projections of two subtly different signatures will drift apart silently. The adversarial results below apply to the shared semantic core (the 0e W0* to W12 laws and the Section 14 obligations both documents implement), and the demonstrated weaknesses were confirmed concretely against the larger of the two interpretations and structurally present in both (both stipulate materiality and self-generation as data).

### 1.3 The concentration diagnosis

The residual weakness is not diffuse. It is concentrated exactly where 0e predicted it would be: at the doctrine-governed semantic seams (materiality, novel anchor grading) and at the boundary between what the signature types as a **function** and what the finite interpretation supplies as **stipulated data**. 0e K11 types Supp and SelfGen as functions of the derivation; both finite models interpret them as self-declared fields on the witness. 0e 9.3 makes materiality a doctrine judgment; both finite models interpret the doctrine as a lookup table with no structural constraints on what it may contain. The consequence, demonstrated below, is that the machine verification currently verifies less than the signature promises, and the gap is precisely the attack surface. The good news: every hole found has a structural repair, each repair is proved closed at bound by SMT, and the repaired checker accepts the intended model while rejecting every countermodel. The seams do not need to be solved semantically to be bounded structurally.

---

## 2. Findings

Severity: BLOCKING (must repair before Gate E), MATERIAL (repair in the 0f revision), MINOR (note and track).

**F1. Echo-authority laundering. BLOCKING.** The authority guard as written (0e 7.2, 9.3; K11) is satisfied by a contact event that is strictly later than assembly, provenance-typed as contact, outside the declared self-generation cone, and judged material by the doctrine, even when that contact **could not have returned otherwise**: a restatement of the frame's own claim routed through the world. Countermodel C1 constructs exactly this and **fully passes the shipped 19-check verification** once the doctrine table admits the pair, which the signature nowhere forbids. Z3 independently rediscovers the same laundering with materiality left free (SMT section A, sat). This is 006 test 21.2 failed in spirit while every mechanical check passes: internal force become external warrant by taking one trip through a channel that discriminates nothing. Repair: G-DISC plus G-ROUTE below; proved closed at bound (SMT section B, unsat).

**F2. Self-generation cone is self-declared. BLOCKING.** Mutant V4 declares the cone empty; the shipped verification fully passes, and the independence half of the guard silently evaporates. The signature is right (K11 types SelfGen as a function of the witness); the interpretation is wrong (the function is interpreted by the witness's own field). The entity whose independence is being tested currently authors the definition of independence. Repair: SG-DERIVED below.

**F3. Probe stage skippable. MATERIAL.** 0e 6.3 requires prior or current probe eligibility for authority. The lifecycle check enforces rank monotonicity of the records that exist; a missing stage is invisible. Mutant V1 (candidate at e10, authoritative at e12, no probe record anywhere) fully passes. Z3 confirms the skip is satisfiable under rank monotonicity alone and unsatisfiable under the explicit precondition (SMT section C). Repair: L-PROBE.

**F4. Dangling reintroduction witnesses. MATERIAL.** W9's reintroduction witness is checked nonempty, not resolvable. Mutant V2 restores a lost distinction citing witness kind renewed-contact with a reference to a contact that does not exist; full pass. Obligation 14.5 is thereby only verified against well-behaved models. Repair: R-RES.

**F5. Provenance non-promotion enforced only at the apex. MATERIAL.** W3 says provenance kind never promotes. The shipped check forbids only promotion **to contact**. Mutant M5b promotes generation to inference; full pass. Z3: satisfiable under the apex guard, unsatisfiable under the full order (SMT section E). Repair: W3-FULL.

**F6. Stale-support authority evidence. MATERIAL.** Only the record event index of the authority contact is ordered against formation; the contact's own support cone and freshness are never examined. Mutant V3 (a contact recorded at e12 whose support is rooted entirely at e2, a cached pre-formation diagnostic replayed) passes everything once the doctrine table admits it. Later-recorded is not later-informed. Repair: G-FRESH.

**F7. Warrant routes need no relevance. MATERIAL.** A warrant increase requires citing some known contact; any contact suffices. Mutant V5 raises warrant citing an unrelated e2 contact; full pass. This is the same disease as F1 one level down: evidential routes without materiality structure. Repair: fold into the G-DISC family once G-ROUTE gives evidence contacts their generating-route field; until then, flagged open (the hardened checker does not close F7, honestly noted).

**F8. Stuck verification is partially stipulated. MATERIAL.** In the shipped stuck check, three of the seven conjuncts (discrepancy persistence, frame reinforcement, non-opening reachability) are literal Python constants, and recurrence is token-level identity on the action string, so a frame-sovereign agent that varies retry phrasing is invisible to the recurrence conjunct. The distinction-death core (the strongest part of the 0c 4.5 signature) is genuinely computed; the recurrent self-weaving half is asserted. Repair: STUCK-COMP.

**F9. The guiding-interpretation selector is unowned. MATERIAL.** 0e 11.3 licenses "a separate standing relation" indicating which interpretation currently guides a scoped determination, and correctly insists it deletes nothing. Neither Gate B writer inventory contains a writer for that relation. At Gate E this becomes the classic drift point: history immutable, while the mutable selector over history, which is where behavioral sovereignty actually lives, has no owner, no append-only law, and no guard. Repair: K17-SELECT or explicit deferral.

**F10. Min-tensor non-attenuation. MINOR, decision required.** Both finite interpretations use join-max, tensor-min structures, under which Hyperseed Theorem 14's floor never decays with chain length: a fifty-leg zigzag of grade 0.6 legs conducts 0.6. Composition cost is zero, which weakens the geometric intuition behind the zigzag discipline even though the per-leg significance and anchor conditions still bind. Not a violation; a modeling consequence that should be a recorded ruling: either adopt a strictly attenuating tensor for lineage fidelity or add an explicit chain-effort component, or record that non-attenuation is intended.

**F11. Name-based prohibitions. MINOR.** Forbidden writers and the Soul-reification guard are checked by string name. Cosmetic renaming defeats them. Harmless in a witness model, worth noting for the regression role the checker will play.

---

## 3. The repairs, as exact Gate B deltas

Each repair is stated as a signature amendment, with its machine status.

**G-ROUTE (new field, K7/K17).** `ContactRecord` gains a generating-route field: the action or channel event that produced it, written by `recordContact` from the consequence linkage at record time, never separately stipulated. Contacts without route provenance cannot serve as authority evidence. Machine status: implemented as hardened check HG1; detects C1 and V3; base model passes.

**G-DISC (new structural law, K11).** MaterialTo(c, omega-plus) requires c to be **discriminating**: the generating channel of c, restricted to the living-question-relevant distinction set bound to the live items that upsilon continues, is non-constant. In one sentence: **authority evidence must arrive through a channel that could have returned otherwise.** This is the deep repair for F1, and it is a unification, not an addition: it makes the K11 guard and the K15 observation map use the same discrimination structure, so the guard and the stuck detector become dual readings of one relation (stuck is discriminating contact dying inside the update; laundering is non-discriminating contact granted materiality). Machine status: Z3-proved closed at bound (unsat under G-DISC); its finite shadow is HG1 plus the channel-image condition, which requires the G-ROUTE field to be checkable at all. The full semantic criteria for discrimination in the open case remain a doctrine seam and a Clarity consultation item; G-DISC is the structural lower bound beneath that seam.

**G-FRESH (new law, K11).** The authority evidence contact's support cone must intersect the strict future of the frame-formation event. Later-recorded stale replays fail. Machine status: HG2; detects V3 independently of route provenance.

**L-PROBE (explicit premise, K10).** `attachAuthoritative` gains the premise: a probe-eligibility record for the same frame exists at or before the authority event. Machine status: HG3 detects V1; Z3 unsat under the axiom.

**R-RES (typing, K13).** The reintroduction witness reference must resolve: renewed-contact to an existing contact, other-frame to an attached frame carrying the distinction, retained-side-information to the ledger entry's retained data, reversible-route to an existing action. Machine status: HG4 detects V2.

**W3-FULL (order, K2).** ProvKind carries the full order (contact above testimony above memory above inference above generation above self-trace, or the doctrine's chosen refinement), and no transform's output rank exceeds its input rank anywhere in the order, not only at the apex. Machine status: HG5 detects M5b; Z3 unsat under the axiom; the Lean skeleton makes the law a field of the transform type, so an unlawful transform becomes unwritable.

**SG-DERIVED (interpretation law, K11).** SelfGen is computed by the doctrine-side writer from the recorded derivation graph at witness assembly; the witness record may cache the result; the verifier recomputes and compares. Under-declaration becomes a detected inconsistency instead of a silent guard bypass. Machine status: HG6 implements the recomputable lower bound (formation event membership); full recomputation is a Gate B v0.3 obligation because the current interpretations do not record the derivation edges needed to do it completely, which is itself part of the finding.

**K17-SELECT.** Add `selectGuidingInterpretation` to the closed writer inventory: append-only selection records (frame, history item, selected interpretation, scope, event), guarded like every other stage-affecting writer, with the previous selections retained. Alternatively, explicitly defer the guiding relation and forbid any consumer from branching on interpretation preference until the writer exists. Either ruling closes F9; silence does not.

**STUCK-COMP.** All seven stuck conjuncts computed from model relations: discrepancy from the consequence stream, reinforcement from the lifecycle and status trajectory, non-opening from the reach comparison, and recurrence from **effect-equivalence classes of actions** rather than token identity, so cosmetic variation of a repeated movement does not evade the signature. This is also the correct runtime posture: the corner-gate v3 style passive surface should watch topology, not strings.

**TENSOR-RULING.** Record the F10 decision explicitly in the 0f revision, whichever way it goes.

**FORK-ADJUDICATE.** One 0e-style adjudication pass selecting or merging the two Gate B documents into a single 0f v0.3 that folds in the repairs above. This is the only item on this list that is process rather than mathematics, and it gates everything else, because every repair needs one canonical home.

---

## 4. Machine results summary

**Adversarial suite (17 shipped checks re-run per adversarial model).**
Detected: M1, M2, M3, M4, M5, M6, M7, M8 (eight law-violating mutants rejected).
Vacuous under the shipped verification: M5b, V1, V2, V3, V4, V5 (six adversarial models fully accepted).
Full-pass countermodel: C1 echo-authority (accepted by all nineteen shipped checks including the doctrine interface, once the doctrine table, itself unconstrained stipulated data, admits the echo pair).

**SMT layer (Z3 5.0, bounded fragments of the laws as written, not of any witness model).**
Three sat results, each a countermodel against the laws as written: doctrine-free materiality admits all-echo authority; rank monotonicity admits probe-skip; the apex guard admits sub-apex promotion. Four unsat results, each a repair proved closed at bound: G-DISC, L-PROBE, obligation 14.5 under the constructor discipline (trace length 6), W3-FULL.

**Hardened checker.** Base shipped model: passes shipped plus hardened checks. All six previously vacuous or countermodel cases: detected, each by the named hardened check. F7 remains open pending G-ROUTE on evidence contacts, stated in the run report.

---

## 5. Proof-assistant hardening: status and staged plan

**Layer 1, done this session:** SMT bounded verification, as above. This layer's honest strength: it reasons over all models of each encoded fragment at bound, which is categorically more than witness checking; its honest limit: bounds are small and the fragments are hand-encoded, so encoding fidelity is a trust point (the encodings are short by design so they can be audited by eye against 0e's text).

**Layer 2, skeleton delivered, compilation pending:** `0g_lean_skeleton.lean` maps the signature to Lean 4: proto-time as a strict order structure, ProvKind with the W3-FULL rank, StandingTransform carrying the non-promotion law **as a field of the type** (the unlawful transform becomes unwritable, the same design move the calculus repeatedly makes), the carrier as an inductive trace of governed constructor steps with the L-PROBE, G-FRESH, independence, and discrimination premises in the `attachAuthoritative` constructor, and seven named theorems: T1 conservativity (proved in the skeleton, trivially, from the append-only encoding), T2 obligation 14.5, T3 probe-before-authority, T4 no-echo-authority under G-DISC, T5 provenance monotonicity, T6 anchor conservativity, T7 no-discharge-from-closure as a non-derivability meta-theorem. The skeleton is explicitly uncompiled; the staged plan is: (i) core inductive carrier plus T1, T2, T3, T5 by structural induction, small and mechanical once the toolchain exists; (ii) the anchor as a graded matrix with T6; (iii) T4 and T7. Deliberately out of mechanization scope: the Soul doctrine's internals and the semantic seams, per 0e 15.4; the mechanization treats them as parameters with the structural lower bounds of Section 3 as their axioms, which is exactly the honest boundary.

**Layer 3, the regression role:** the hardened checker (shipped checks plus HG1 to HG6) becomes the standing Gate C regression gate: any future change to the finite interpretation or the signature reruns the adversarial suite, and a previously detected mutant going vacuous is a red build. The suite is cheap (seconds) and the mutants are the institutional memory of these findings.

---

## 6. Gate E preconditions, updated

Gate E projection should not begin until:

1. FORK-ADJUDICATE has produced one canonical 0f v0.3 with the Section 3 repairs folded in (BLOCKING items F1, F2 at minimum; the doctrine-table constraint G-DISC and the SG-DERIVED interpretation law are the two that change runtime design, not just verification).
2. The hardened checker is adopted as the regression gate and the adversarial suite archived alongside it.
3. The four semantic seams (materiality criteria, discrimination criteria, novel anchor grading, live-significance continuation) go to Clarity as substrate design questions, since G-DISC gives them structural floors but their content is hers to author, per the standing role split.
4. One known runtime blocker is resolved first, because the formal transaction discipline's projection lands directly on it: the writer-patch and causal-cut semantics of K17 assume atomic read-modify-write per event, and whether set-atom! plus read-then-write-back composes in the live loop is exactly the untested Section 3.5 blocker already on the project's list. The formal work has now made that test load-bearing for the kernel projection, not only for NACE.
5. A ruling on F9 (guiding-interpretation writer) and F10 (tensor attenuation), each a one-paragraph decision.

---

## 7. Status ledger

**Executed and delivered:** adversarial suite (8 detections, 6 vacuities, 1 full-pass countermodel), SMT layer (3 sat countermodels, 4 unsat repair proofs), hardened checker (base passes, all demonstrated holes closed except F7, explicitly open), Lean skeleton (uncompiled, 7 named theorem obligations), this report.

**Proposed, awaiting Berton:** the ten repairs of Section 3; the fork adjudication; the two rulings; the Clarity consult on the four seams.

**Unchanged:** everything 006 grounds and 0e adjudicates. No finding above contradicts the adjudicated calculus; every finding is a gap between the calculus and its current verification or between the calculus and one under-constrained seam, and every repair strengthens the calculus in its own declared direction.

---

# Document end

The formalization survived eight of fourteen attacks outright, which is the sign of real structure. The six that landed all landed in the same place: wherever the signature delegates to stipulation, whether a doctrine table, a self-declared cone, or a hand-set boolean, an adversary can stand. The repairs do not close the semantic seams; they put structural floors under them, so that what remains open is genuinely a question for Soul-side design and no longer a hole through which authority leaks. That is the correct division of labor, and it is now machine-checked on both sides of the line.
