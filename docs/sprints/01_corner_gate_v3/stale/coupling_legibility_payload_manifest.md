# Corner-Gate v3 Draft A: Payload Identity Manifest

**Date:** 2026-07-09
**Status:** DRAFT A DELIVERED FOR BERTON LAYER-1 REVIEW. Nothing installed. Draft B (the monolith) verifies these hashes before applying; reviewed payload must equal applied payload. Hashes refresh on any markup revision.
**Design canon:** corner_gate_v3_adapter_design.md v0.6.

## Payload hashes (sha256)

```
e0e49169da88d5cdd94c0b19af6b4247b024142c815e0b18f00d136ff1050706  coupling_legibility.metta
2017a093706670fe341f6c3272e40738dc1d90498eebfa21bd1cf5bd558cf430  coupling_legibility_writers.metta
51099a14939152c680586f362beb53456b08414a37cc557e4f2225eab6ddc51d  coupling_legibility_helper_payload.py
```

## Expected target paths

```
coupling_legibility.metta            -> soul/coupling_legibility.metta   (CREATE)
coupling_legibility_writers.metta    -> soul/coupling_legibility_writers.metta   (CREATE)
coupling_legibility_helper_payload.py -> appended to src/helper.py   (PATCH, Phase 3)
```

## Expected import positions (hard constraint, design doc 5.2)

Both new imports land in lib_clarity_reasoning/lib_clarity_reasoning.metta AFTER the v08.7.2 engine import (currently line 14) and after the existing corner_gap block (currently ends line 103): pure file first, writers second. The monolith asserts engine line number strictly less than both new import line numbers, and asserts no duplicate engine heads and no lib_quantale resurrection.

## Expected loop swap sites (certified loop.metta, Step 0g survey)

```
line ~166  ($sexpr_gated (apply-corner-gate-v2 $sexpr_verdict $msgnew))
           -> REBODY apply-corner-gate-v2 definition to pass-through (name and arity kept)
line ~168  ($results_final (gate-aware-results $results))
           -> REBODY gate-aware-results definition to append the coupling line (name and arity kept)
tail hook  ($_ (populate-corner-window! $metta_cmds $k))
           -> REPLACE with ($_ (do-record-coupling-cycle! $metta_cmds $msgnew $k (get-state &error)))
initLoop   add ($_ (do-bootstrap-coupling!)) beside the existing bootstrap hooks
```

Hook ordering preserved: the recorder stays AFTER populate-state-delta and populate-coupling-verdict (load-bearing per state_delta_writer_writers.metta). S1 preflight/postflight per design doc 5.1 governs the two rebodies.

## Verification already run on the payloads (this delivery)

Paren delta 0 on both MeTTa files. Formatter totality passed on the ratified cases: all-fields, non-healthy honesty rendered, claim-completion hidden, None/empty defensive, long-symbol truncation, unbound-$ leak converted to not-computed (ground-symbol rule), empty-batch signature none. Gate H target identity: same path hashes identical (H1 basis), different path differs (H4 basis), no-action batch returns unknown (H3 basis).

## Consolidated REVIEW-FLAGS for Layer-1 markup

- RF1 (deviation from v0.6 text): ALL singleton writers use remove-by-variable then add, superseding the doc's "exact-old-value set-atom! replace" wording, per the Atom Operations Map CONTRA-setatom safety correction and N1 writer doctrine. Recommend amending the doc wording to match.
- RF2: helper payload carries four functions, not one (signature hashing and target extraction are string plumbing MeTTa cannot do; Python stays hands-only).
- RF3: v1 command-class table (pure file) for markup.
- RF4: v1 contact-surface mapping (writers file); ambient prompt surfaces (task-state, cycle-trace) deliberately NOT recorded so NC1 remains possible.
- RF5: v1 claim-present proxy is a claim-class (send) command in the cycle; content never read.
- RF6: v1 hidden-error proxy: repeated signature with no forward delta and no visible feedback reads hidden-error-surface.
- RF7: v1 evidence constants: aligned leg strength 0.9, misaligned 0.2, mechanical confidence cap 0.7.
- RF8 (prominent): $next-move carries not-computed in v1. The engine q-next-epistemic-move domain does not include the self-seeing chain states v1 computes; populating the field requires your ratified state mapping. Nothing fabricated.
- RF9: recorder hook takes (get-state &error) as its fourth argument (single call, Discipline 1); the loop itself branches on the same expression at the same site.
- RF10: v1 rapid-flip rule: current position at one extreme while stored band is the opposite stable extreme.
- RF11: contact-accord navigation leg needs N+1 evaluation; v1 renders the task accord, contact accord joins v1.1.
- RF12: $ctx-soul is the constant soul-verdict-present in v1 (verdict renders every cycle per live logs); wiring the actual verdict symbol is a v1.1 option.
- RF13: head extraction takes car-atom over the superposed batch; empty batches record no head-driven contact (the NC1 path).

## Not in this delivery (Draft B scope)

The monolith apply/reverse script, the separate validator, the tree delta report, no-touch assertions, the D0-D8 harness (PC1, PC2, NC1-NC5, H1-H4, S1A/S1B, formatter cases live, ground-symbol check), apply manifest, reverse verification.

Manifest end.
