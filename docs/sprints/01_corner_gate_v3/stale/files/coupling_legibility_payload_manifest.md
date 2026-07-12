# Corner-Gate v3 Draft A.3: Payload Identity Manifest

**Date:** 2026-07-09
**Status:** DRAFT A.3 DELIVERED FOR RATIFICATION. Carries the full ruling history: A.1 blockers resolved, A.2 rulings implemented (RB1 support patch, v3-18-field, RF8/RF3/RF13/RF4 ratified), A.3 checklist complete (current-cycle trace verdict timing fix, manifest cleanup, header cleanup, hash refresh). Nothing installed. Draft B verifies these hashes before applying.
**Design canon:** corner_gate_v3_adapter_design.md (amendment lines for the canon copy listed at the end).

## Payload hashes (sha256)

```
14705a549aec69198b9d03dd31ea162dd95ad8fd238c5fea3e99eb8712bf10f1  coupling_legibility.metta
e1bc3e28cd7ca357f7e618713cb550dd328fb0da5d114f40e6981e4b7efca3f8  coupling_legibility_writers.metta
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

Manifest end.
