# |- and Atomspace Persistence: RESOLVED (no bug) + the verified workflow

**Status:** RESOLVED. The "marshalling bug" was never a bug. After two corrections
(documented below, because the error pattern is the lesson), the substrate behavior
is understood: `|-` computes but does not persist; only `add-atom` commits; the
boundary throw is a correct refusal of a non-string. No code fix is needed; the
resolution is a usage workflow.
**Updated:** 2026-06-25 (runtime-grounding stamp added; see the STAMP block below).
Supersedes earlier versions that claimed first a marshalling bug, then a |- side-effect
deposit; both wrong (see section 0).
**Companion reference:** `Atom_Operations_Map.md` (the ground-truth operation reference;
its `|- and |-nal` table was updated this same session and is now the canonical statement
of this behavior). Point new threads there first.

---

## RUNTIME-GROUNDING STAMP (2026-06-25)

This doc's central claims were re-grounded against the LIVE runtime source this session,
not against prior-thread say-so. The reads were end to end against the running container
`clarity_omega`, in the file the running process actually loads
(`/PeTTa/repos/omegaclaw/lib_nal.metta`, proven via the run.sh -> run.metta ->
lib_omegaclaw line 26 -> ./src/loop load chain). What changed and what each claim now
rests on:

**SOURCE-VERIFIED this session (read from lib_nal.metta lines 108-202):**
- `|-` is DEFINED. It is a thin both-orders wrapper over `|-nal`, line 201-202:
  `(= (|- $a $b) (unique-atom (collapse (superpose ((|-nal $a $b) (|-nal $b $a))))))`.
  It runs `|-nal` in both argument orders, collapses the nondet stream, uniquifies.
- `|-nal` is the FULL NAL inference family (lines 108-199): revision at 108, deduction
  110, induction 111, abduction 112, plus the structural / set / product / implication
  tail. `|-` is the entry point that exercises this family both ways.
- This corrects a contradicting claim elsewhere in the doc set: `nace_implementation_plan.md`
  recorded "bare |- undefined / echoes unreduced" as a permanent constraint. That is false
  against source. `|-` is defined; the echo-unreduced was a standalone-context artifact,
  because `|-` calls `|-nal` and lib_nal reduces only inside the live loop, so the wrapper
  sits unreduced in any standalone invocation.

**SOURCE-CORROBORATED this session (supports the claim; does not replace live test):**
- Non-persistence. The `|-` wrapper and the `|-nal` rule right-hand sides are
  computed-value returns. There is NO `add-atom` step anywhere in the operator. So
  persistence is not a property of `|-`; it cannot store, by construction. This is
  stronger than the prior behavioral-only basis.

**STILL IN-LOOP-TEST-PENDING (not stamped proven this session):**
- The runtime persistence BEHAVIOR (`|-` computes and stores nothing AT RUNTIME) was not
  re-confirmed in-loop this session. lib_nal reduces only in the live loop, so the only
  gold-standard confirmation is an in-loop test routed through Clarity's actual skill path
  in Mattermost, not any external or standalone invocation. The source corroboration above
  makes the claim safe to rely on for design, but the live in-loop read remains the
  definitive confirmation and is the one open item this doc still carries.

**CARRIED FROM PRIOR WORK, audit-consistent, not re-verified this session:**
- The type_error/domain_error as a computation-output-through-display claim (section 2).
- The within-process add-atom persistence and the multi-command silent-partial-fail
  discipline (section 3). Both are consistent with the Boundary Transition Audit v2 (B7
  silent-miss class, B9 within-process persistence) and the Atom Operations Map, but were
  not independently re-read this session.
- The boundary-throw-is-crash-safe claim is corroborated by the audit's B5 (Janus marshal,
  WORKING-BY-DESIGN, the throw on an unbound/compound value is correct) and by
  `string_safe_encode_decode_asymmetry.md`.

---

## 0. Two corrections, because the error pattern IS the lesson

This document was wrong twice, in opposite directions, before landing on the truth.
Recording both because the meta-lesson is more valuable than the conclusion.

**Wrong v1: "marshalling bug, fix the throw."** Claimed `|-` results were discarded
by a defect at the eval-result py-call boundary; proposed disambiguating Origin 1 vs
2 and stringifying with `repr`/`string-safe`. FALSE: the boundary refusing a compound
term is crash-safe-by-design (per `string_safe_encode_decode_asymmetry.md` and audit B5),
not a defect. Calling it a bug was the first frame error.

**Wrong v2: "|- deposits to the atomspace as a side effect."** Over-corrected to claim
the derivation persists automatically and only the display fails. FALSE, killed by a
clean test: premises A->B and B->C both committed, `(|- ...)` computed A->C at 0.81,
`match` for A->C returned EMPTY. Premises present, derivation computed, nothing stored.
The "premises must be committed" rescue was tested and also failed; premises WERE
committed. (Source now explains WHY nothing stored: the operator has no add-atom step.)

**The truth (source-corroborated 2026-06-25):** `|-` is a calculator, not a writer. It
computes correct derivations and stores nothing. Persistence is explicit
`(add-atom space value)` and nothing else. The boundary throw is correct (compound is not
displayable text). All three earlier claims, "bug," "side-effect deposit," "type_error is
cosmetic," were frame errors caught by testing the specific claim directly.

---

## 1. The resolution: the verified workflow (from Patrick's NACE docs)

```
[1] (add-atom &self premise1)       ;; commit premises explicitly
    (add-atom &self premise2)
[2] (|- premise1 premise2)          ;; compute derived truth values (stores NOTHING)
[3] (add-atom &self derived-result) ;; commit the derivation explicitly
```

`|-` computes; you read the value; you choose to `add-atom` it. The deposit is never
automatic. This is the canonical pattern from `knowledge.metta` / `spaces.metta` in
the NACE docs, the substrate's own authoritative source, not an inference of ours.

Source note (2026-06-25): step [2]'s `|-` is the both-orders wrapper over `|-nal`
(lib_nal.metta line 201-202). It will only reduce inside the live loop; a standalone
invocation leaves it unreduced. There is NO marshalling fix to build. The earlier
Origin-1-vs-2 disambiguation and the `repr`/`string-safe` proposal are MOOT; they lived
inside the mistaken "the throw is a defect" frame.

## 2. The facts, with provenance (do not silently re-litigate; do re-confirm the one open item)

- `|-` computes correct NAL derivations: a multiplicative-confidence deduction in the
  forward order, plus a lower-confidence abductive inverse in the reverse order.
  [SOURCE-VERIFIED 2026-06-25 that the machinery exists and runs both orders: `|-` =
  `(unique-atom (collapse (superpose ((|-nal $a $b) (|-nal $b $a)))))`. The forward+reverse
  pairing is the two-order wrapper, not a mystery. Correct-value computation confirmed by
  prior behavioral test; live values reduce in-loop only.]
- `|-` does NOT persist; computation is not commitment. [SOURCE-CORROBORATED 2026-06-25:
  no add-atom in the operator. Prior clean behavioral test (section 0) agrees. Live in-loop
  re-confirm is the gold standard and is the one open item.]
- `add-atom` is the only commit path. Direct eval does not persist either. [Carried;
  audit-consistent B7/B9; map row.]
- Within a process life, add-atom'd atoms persist and `match` finds them (10 of 12
  sampled found on first match). Across a rebuild, `&self` dies by design; only ChromaDB
  `remember`s survive. [Carried; audit-consistent B9; not re-verified this session.]
- The type_error/domain_error is a COMPUTATION OUTPUT shown through the display path,
  not a masked hit and not a formatting artifact. Clean result = present; clean `[]` =
  absent; error = a computed value being displayed. [Carried from prior work; NOT
  re-verified this session; flagged as the next thing to re-ground if it becomes
  load-bearing.]
- The boundary refusing a raw compound is correct (crash-safe by design). [Audit-
  corroborated B5; `string_safe_encode_decode_asymmetry.md`.]

## 3. The load-bearing discipline this produced

**`add-atom` in multi-command blocks silently partially-fails.** At least 2 of ~60
network atoms never committed, with no error, consistent with Repair-1's documented
silent-goal-failure physics (a failing `let*` binding killed invisibly; per-directive
`findall` absorbs it). [Carried; audit-consistent with B7 silent-miss class; not
re-verified this session.]

RULE: never trust "I added N." Confirm "match finds N" in a SEPARATE command, count,
re-add misses. A built network is not real until match-count == intended. Prefer
small batches / per-atom commits for load-bearing state.

This generalizes beyond `|-`: verify the load-bearing substrate claim with a clean test
before building on it. "It threw" is not "broken"; "it computed" is not "persisted"; "I
added N" is not "N exist." This session's own work is a worked example: the doc set
claimed both "captures $a" and "discards $a" and "bare |- undefined" and "|- computes,"
and only reading the loaded source settled each.

## 4. The one question still worth asking Patrick (genuinely open, now sharpened)

A single `|-` call computes BOTH a forward deduction and a reverse abduction at lower
confidence. The mechanism is no longer a mystery: source shows `|-` runs `(|-nal $a $b)`
and `(|-nal $b $a)` and collapses both (line 202). The earlier "forward persists, reverse
doesn't" asymmetry was an ARTIFACT of the false deposit premise; since `|-` stores
NEITHER, there is nothing to explain there.

The remaining real question is narrower and architectural, for when knowledge-base design
matters: when you DO `add-atom` a derived result, should both the forward deduction
(belief) and the reverse abduction (conjecture) be committed, or is it sound practice to
commit only the deduction and treat abductions as provisional? That is a NARS
knowledge-hygiene question, not a substrate-behavior question, worth Patrick's view when
building the knowledge architecture, not blocking anything now.

## 5. Cross-references

- `Atom_Operations_Map.md` (UPDATED this session). The ground-truth operation reference;
  the `|- and |-nal` table now carries the source-verified `|-` definition (row 131) and
  the source-corroborated non-persistence (row 130). Point new threads there first.
- `000_ClarityOmega_Boundary_Transition_Audit_v2.md` B5 (Janus marshal, the throw is
  crash-safe by design) and B7 (silent-miss class). The boundary and persistence physics
  this doc relies on are mapped there against the runtime.
- `string_safe_encode_decode_asymmetry.md`, why the boundary is crash-safe by design (the
  constraint that made "stringify across the boundary" wrong).
- `nace_implementation_plan.md`, CORRECTED ON THE OPERATOR POINT by this session's source
  read: its "bare |- undefined / echoes unreduced" constraint is false; `|-` is defined
  (lib_nal.metta line 201) and the echo-unreduced was a standalone-context artifact. The
  plan itself is not yet edited; the correction lives in the Atom Operations Map.

---

## 6. The one open item, stated plainly

Everything in this doc is settled except one live confirmation: that `|-` (and `|-nal`)
compute and store nothing AT RUNTIME. Source corroborates it (no add-atom in the operator),
prior behavioral testing agrees, but lib_nal reduces only in the live loop, so the
definitive read is an in-loop test through Clarity's skill path in Mattermost. Until that
runs, the persistence claim is safe-to-design-on and explicitly not stamped
proven-this-session. That is the honest line, and it is the only thing keeping this doc
from being fully closed.
