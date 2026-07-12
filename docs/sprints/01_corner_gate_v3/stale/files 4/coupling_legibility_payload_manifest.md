# Corner-Gate v3: Payload and Build Identity Manifest

**Date:** 2026-07-09
**Status:** PAYLOAD A.4 / STEP B.2 DELIVERED FOR FINAL RATIFICATION. Supersedes the A.3 writers payload while preserving the A.3 pure and helper payloads. Ruling history preserved in the sections below (A.1 review, A.2 rulings, A.3 checklist, B 13-item patch, B.2 live-proof and hardening corrections). Nothing installed until the monolith runs on the live tree.
**Design canon:** corner_gate_v3_adapter_design.md (amendment lines for the canon copy listed at the end).

## Payload hashes (sha256)

```
14705a549aec69198b9d03dd31ea162dd95ad8fd238c5fea3e99eb8712bf10f1  coupling_legibility.metta
c3df6c388b95784304465a3e2bddb25abda53c497344a0db89057029f6817537  coupling_legibility_writers.metta
de3183e1f3504e2201d6ef80ec6e6650534b80d491e4df7efa38a099f1e87e54  coupling_legibility_helper_payload.py
```

## Expected target paths, import positions, loop swap sites

Unchanged from Draft A: CREATE soul/coupling_legibility.metta and soul/coupling_legibility_writers.metta; PATCH src/helper.py (append payload 3); both imports AFTER the engine (line 14) and after the corner_gap block (line 103), pure first, writers second; loop swaps at ~166 (apply-corner-gate-v2 rebody to pass-through), ~168 (gate-aware-results rebody to line appender via coupling-legibility-line), tail hook REPLACE populate-corner-window! with ($_ (do-record-coupling-cycle! $metta_cmds $msgnew $k (get-state &error))), initLoop gains ($_ (do-bootstrap-coupling!)).

## Blocker resolutions (B1-B5, all resolved)

- **B1 trace verdict wired.** Pure file adds (coupling-trace-verdict-for-window) and (latest-coupling-trace-verdict): reads the window's three stored polarity verdicts by ordinal order (min, mid, max) and calls (q-tfs2-trace-verdict? same-start $v2 $v3). The composer's trajectory field uses the trace verdict when the window is full, window-filling before then. Ratification conditions carried to Draft B harness: PC1 must produce blocked-repetition-without-metabolization; PC2 must not.
- **B2 contact-count is surface-count.** do-record-contact-event! is remove-specific-then-add (idempotent per ord and surface), and coupling-contact-surfaces dedupes defensively. New fixture carried to Draft B: batch query plus metta yields contact-count 1, dominant runtime-output.
- **B3 hidden failures increment.** Recorder reads $delta FIRST; failed = visible-error OR (sig not none AND delta none). Pin-only and empty batches sign as none and never count as failures. Ratification condition carried to Draft B: PC1 proves repeated same-signature, no-forward, no-visible-feedback increments the fail count and reaches the intended trace verdict.
- **B4 totalized classification.** (surface-for-head-total) and (command-class-of-total) branch on the explicit known-heads list with fallbacks no-contact and neutral; writers call only the total forms. Fixture carried to Draft B: unknown head yields no-contact, neutral, zero unreduced fields.
- **B5 MeTTa line composer exists.** (coupling-legibility-line): reads only through field helpers, sequences every binding, py-calls the formatter with ten flat values, never touches the record tuple, renders the window-filling line on an empty window. Fixture carried to Draft B: live reduction to a COUPLING-STATE string with no tuple render and no unreduced variables.

## Amendment resolutions

- A1 bootstrap NORMALIZES: remove-all then add for both singletons, exactly one of each from any prior state.
- A3 / RF3 answered: remember is NEUTRAL class in v1. Rationale: its target (the memory string) has no mechanically verifiable durable target, so action-class status would create Gate H inconsistency. Its executed surface remains runtime-output.
- Helper 1: H4 verified in this delivery (different-target hash can never equal the action target; see verification below). H4 fixture also carried to Draft B.
- Helper 2: sha256[:8] replaces md5, documented as compact non-security identity hash.
- Helper 3 / RF13 resolved: pin-only and empty batches sign as none, no hash. Rationale: pins are narration; narration must not become command lineage; pin loops are caught by the no-contact path (NC1, symbolic-capture), not signature repetition.
- Helper 4: shell EXCLUDED from target extraction; shell actions yield unknown, honesty not-computed. Conservative both ways: no false claim-completion, no false accusation. Comment corrected.
- Helper 5: head regex widened to letters, digits, underscores, hyphens, and trailing ! or ?.
- Pure 1 and 2: latest-coupling-context and latest-coupling-lineage exist under the ratified names, returning the primary component (ctx-phase, producer), with component helpers beside them.
- RF12 wording adopted: ctx-soul is a surface-presence context marker, not approval status.

## Verification run on this delivery

Paren delta 0 on both MeTTa files. Helper live tests: H1 basis (same path, action and verification targets identical), H4 basis (different path never equal), H3 basis (shell action yields unknown), pin-only and empty signatures return none, digit-bearing head parses, corner-region line renders with honesty shown, healthy line renders with claim-completion hidden, all-None input renders the safe not-computed line.

## Ruling status (prior A.1 open rulings, all resolved)

- RF8 RATIFIED active: adapter-side pairing over verbatim engine move vocabulary, never described as engine-derived; precedence honesty > trace verdict > chain state.
- RF11 RATIFIED: v3-18-field, both accords stored, task accord rendered, contact accord divergence-gated as contact-audit (decision in MeTTa).
- RF4 RATIFIED with shell/unknown fixture coverage carried to Draft B.
- RF3 RATIFIED (remember neutral). RF13 RATIFIED (pin-only signs none).

## Design doc amendment lines for the canon copy (accepted items)

1. Section 3.2 and 3.5: replace "exact-old-value set-atom! replace" with "remove-by-variable then add (Atom Operations Map N1 writer doctrine; CONTRA-setatom safety correction)". Bootstrap normalizes rather than guards.
2. Section 5.5 Draft A item 3: "helper.coupling_line_format payload" becomes "helper payload: line formatter plus command-signature and action/verification target extraction (hands-only string plumbing; compact non-security sha256 identity hashes)".
3. Section 2.5 Gate H: add "Claim-present is a v1 proxy: a claim-class (send) command in the cycle; content is never read. name-action-not-verification can therefore appear only when action and send co-occur."
4. Section 3.1 $ctx-soul: add "a surface-presence context marker, not approval status".
5. Section 4 render: add "the trajectory field carries the window trace verdict when the window is full, window-filling before then".
6. Section 7 D9: note shell actions yield target unknown (honesty not-computed) in v1.
7. RF8 RATIFIED: Sections 4 and 7 record the next-move mapping as an adapter-side pairing over verbatim engine move vocabulary (never described as engine-derived), with the precedence rule honesty > trace verdict > chain state.
8. RF11-RES RATIFIED: Sections 3.1 and 4 record the v3-18-field schema, both accords stored, task accord rendered, contact accord divergence-gated as contact-audit, decision computed in MeTTa.
9. RB1: Section 2.6 records that support composes all three task-accord legs via q-meet on both edges.

## A.2 changes (Berton's A.1 review, all implemented)

- **RB1 RESOLVED (was the blocker).** derive-support now includes the action leg in BOTH edges via q-meet, whose signature was verified from engine source before use: (: q-meet (-> pbit pbit pbit)), min strength min confidence, lines 115-117. Fixture math confirmed pre-delivery: intention aligned, action misaligned, outcome aligned reduces support to 0.04. Fixture carried to Draft B (Gate: if support stays high, the action leg is not participating).
- **RF11-RES IMPLEMENTED per ruling.** Schema bumped to v3-18-field. Record stores $task-accord and $contact-accord (field order per the ruling: after $polarity-verdict). Helpers added: latest-coupling-task-accord, latest-coupling-contact-accord, latest-coupling-accord (returns task accord, back-compat). The normal line renders the task accord only. The contact accord renders solely on divergence (task integrating while contact is not), as contact-audit, and the divergence DECISION is made in MeTTa (coupling-contact-audit-render); Python only formats. Preserve structurally, reveal selectively.
- **RF8 RATIFIED as active.** Design doc wording per the caution: the mapping is an adapter-side pairing over verbatim engine move vocabulary, NOT an engine-derived next move. The engine owns the move vocabulary; the adapter owns this pairing.
- **RF3 RATIFIED:** remember neutral. **RF13 RATIFIED:** pin-only signs none. **RF4 RATIFIED** with the shell caution carried to Draft B fixtures: shell contact-credit versus empty or invisibly failing shell returns, plus shell/unknown cases in the harness.
- A.2 verification run: paren delta 0 both MeTTa files, zero 17-field pattern leftovers, divergence rendering proven both ways (renders blocked-no-contact on divergence, hidden otherwise), corner line and all-None defensive line intact.

## Draft B fixture ledger additions from this round

RB1 support-drop fixture. Contact-count surface fixture (query plus metta yields 1). Hidden-failure increment fixture (PC1 path). Unknown-head totality fixture. Composer live-reduction fixture. Divergence render fixture (both polarities). Shell contact-credit and shell/unknown honesty fixtures. H1-H4. All alongside PC1/PC2, NC1-NC5, S1A/S1B, formatter totality, ground-symbol check.

## A.3 changes (Berton's A.2 review checklist, all six items)

1. **Semantic fix: current-cycle trace verdict timing.** New pure helper (coupling-trace-verdict-with-current $current-pv): fewer than 2 prior records reads window-filling; otherwise v2 is the latest PRIOR stored polarity verdict and v3 is the CURRENT cycle verdict, per the quoted engine signature. The recorder now derives the stored $next-move from it, so next-move reflects the actual current 3-cycle trace and never lags one cycle. The rendered trajectory still reads the full window after the add.
2. Stale A.1 open-rulings section removed, replaced by the resolved-status block above.
3. All payload headers corrected to Draft A.3; zero 17-field references remain outside historical notes; the record is described everywhere as the 18-field v3-18-field shape.
4. Hashes refreshed (block above).

## Draft B fixture ledger addition (A.3)

PC1 cycle-3 stored-next-move gate: at the third pathological cycle, the STORED $next-move must reflect the current 3-cycle trace verdict (block-reinforcement-and-seek-contact from blocked-repetition-without-metabolization), NOT window-filling from the prior 2-record window.

## Draft B artifacts (composed against the frozen A.3 hashes, 2026-07-10)

```
apply_corner_gate_v3_monolith.py     staging/   apply/reverse, phases 0-10
validate_corner_gate_v3_monolith.py  staging/   D0-D8 ladder, --expect-reversed
```

Self-test performed pre-delivery on a mock tree carrying every live anchor: dry-run green (zero FAILs), apply green, reverse complete and verified, re-apply green, apply manifest GREEN. The self-test caught and fixed two real defects before delivery (the --dry-run flag per the ratified procedure, and a shim comment tripping the held-marker postflight grep), which is the layered-proof doctrine working.

Payload source directory default: docs/sprints/01_corner_gate_v3 (--payload-dir to override). The monolith verifies the frozen A.3 hashes there before touching anything; a mismatch refuses with reviewed-payload-not-equal-applied-payload.

## Draft B.1: the 13-item ratification patch (Berton's Step B ruling, all resolved)

Payload revision A.4 (authorized by ruling items 5 and 6): the recorder is split into a thin outer gatherer (py-call, get_time, state-delta, task-phase reads) and do-record-coupling-cycle-core!, a deterministic core taking every runtime-coupled value as an argument. Zero py-call/get_time/external reads verified in the core. Writers hash refreshed below; pure and helper payloads unchanged.

```
14705a549aec69198b9d03dd31ea162dd95ad8fd238c5fea3e99eb8712bf10f1  coupling_legibility.metta        (unchanged)
c3df6c388b95784304465a3e2bddb25abda53c497344a0db89057029f6817537  coupling_legibility_writers.metta (A.4)
de3183e1f3504e2201d6ef80ec6e6650534b80d491e4df7efa38a099f1e87e54  coupling_legibility_helper_payload.py (unchanged)
```

Resolution map, each with executed evidence:
1. B1 rollback isolation: do_reverse rewritten with local failure state; forced-failure fixture RUN LIVE (T3b): injected postflight failure, auto-reverse, six restored files hash-matched pre-apply values, exit code 3, tree byte-identical (T4).
2. M1 engine pin: ENGINE_SHA_PIN in apply preflight as SUBSTRATE IDENTITY, distinct from the postflight no-touch check; wrong-engine refusal proven (T1).
3. B2 installed-helper identity: marked-body extraction and hash against the frozen payload, in apply postflight AND validator D0; corruption negative test proven (T7: doctored body, validator fails on exactly that check).
4. NC2-NC5 fixtures added: NC2 verbatim engine reduction (line 4621 quoted), NC3 chain probe, NC4 nothing-fabricated on the stored empty-cycle record, NC5 healthy composer line with no honesty and no contact-audit segment.
5. Recorder-level PC1/PC2: three-cycle core replays with injected inputs; PC1 proves hidden-failure incrementing inside the core (PC1FAIL 3) and the stored pathological fields.
6. Cycle-3 stored next-move: PC1NM reads latest-coupling-next-move from the STORED record, expected block-reinforcement-and-seek-contact.
7. query+metta fixture: stored contact-count 1, dominant runtime-output (QMCC/QMDS).
8. Live MeTTa composer reduction: LINE fixture calls (coupling-legibility-line) in the harness.
9. Divergence decided in MeTTa: DIVY/DIVN probe coupling-contact-audit-render directly.
10. Shell fixtures: PC1CC shell contact-credit (tool-result counted while hidden failure increments), PC1HON shell honesty not-computed, shell-target-unknown extraction check in D6-local.
11. D7/D8 bounded to the current boot: docker inspect StartedAt plus docker logs --since; subprocess argument arrays with rc gates (M4).
12. Reverse hash verification (M3): every restored file compared to recorded pre-apply hashes; proven in T3b and T8.
13. Claims equal proofs: the validator header enumerates exactly what executes, names the S1A/S1B behavioral fixtures as 200-cycle-window observations by design, and every fixture id in the header exists in the harness.

Self-test evidence (mock tree, run pre-delivery): T1 engine-pin refusal; T2 dry-run zero FAILs; T3b forced-failure auto-reverse HASH-VERIFIED exit 3; T4 tree byte-restored; T5 apply green; T6 validator static 21 PASS 0 FAIL; T7 B2 corruption caught; T8 reverse hash-verified; T9 expect-reversed 8 PASS; T10 re-apply green. NOT run here: the container harness fixtures (D2/D3/D5/D6-metta) and D7/D8, which execute on the live tree.

Draft B.1 script hashes:
```
38dd3fe2b883e3e536f01fcb942a289f23a14cb7e86df7c1a40533ed850a2ab4  apply_corner_gate_v3_monolith.py
b0a4bc658ebfe7929e700d4492bc3f76c603b1d24e0ca1557c0b98d1aa5bba95  validate_corner_gate_v3_monolith.py
```

## B.2 corrections (Berton's near-final ruling, all three items)

- **R1 CLOSED (live-proof blocker).** D7 is now bounded to THIS VALIDATION RUN, not the container boot: a UTC boundary is captured at probe start; the validator polls docker logs --since that boundary (default timeout 120s, --probe-timeout) until the live loop emits a fresh COUPLING-STATE line; absence at timeout is a FAIL; groundness and the held-by-corner-gate check run on post-boundary lines only (stale hold lines from earlier in the boot can no longer falsely fail a correct install, and stale good lines can no longer falsely pass a broken one). D8 metrics come from the same post-boundary window and record the boundary timestamp.
- **R2 CLOSED (hardening).** --expected-engine-sha is refused in BOTH scripts without the explicit --self-test-mode gate, which prints a loud banner that canonical substrate identity is not verified. Production invocations verify the pinned canonical engine only. Refusal proven live in both scripts (T11); the gated self-test cycle remains green (T12: dry zero FAILs, apply green, validator static 21 PASS 0 FAIL); the forced-failure fixture remains hash-verified with exit 3 under the gate (T13).
- **Final documentary correction (this revision):** opening payload block corrected to the A.4 writers hash; apply script comment relabeled FROZEN A.4 PAYLOAD IDENTITY (hygiene), refreshing the apply script hash to the value above. Validator unchanged.
- **R3 CLOSED (hygiene).** This manifest's top-level status now names the effective artifact set (Payload A.4, Step B.2 installer/validator) and marks history as history.

Step B.2 script hashes:
```
3a71cd9e7da01dccbc4989b871dba7543184552c8e24b1a8991a5920769d4235  apply_corner_gate_v3_monolith.py
cd5b8b61b23e5070580817d279df417852357ba216e4fc5c1cb46749cb893dcd  validate_corner_gate_v3_monolith.py
```

Manifest end.
