# v08.7.2 Live Import Runtime Harness Trace

harness: `v08.7.2-live-import-runtime-v01.0-query-only`

## Summary

```json
{
  "FAIL": 81,
  "PASS": 37
}
```

## Checks

- **PASS** `L0` container exists: 
- **PASS** `L1` host file present: lib_clarity_reasoning/lib_clarity_reasoning.metta: size=7395 sha256=3cce5155156379b789a7d480a5b9e065ce0f98ea50408620531c9387d3502a26
- **PASS** `L1` host file present: lib_clarity_reasoning/lib_quantale_autopoietic_epistemic_dynamics_engine_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY.metta: size=338041 sha256=693089e6b69d3b40c0772e3a068e337bb325048f39f9e0a4f8bd9e6f66012851
- **PASS** `L1` host file present: soul/soul_kernel.metta: size=45103 sha256=fa70fb3baca9e25dfe5a30646707c9a86b48be19d153b4e552a44419bb0a7de6
- **PASS** `L1` host file present: soul/durable.metta: size=395 sha256=b30addd567a3584dc4e0239ef4f2d0ce079252b4293a1ac108d6e1d34df64617
- **PASS** `L1` host file present: soul/evolutionary/README.metta: size=374 sha256=9286f68b41192caf0d2d4817b1d6c90e9662820240f8b8c4cb1f77f699d08a3d
- **PASS** `L1` host file present: soul/evolutionary/archive/README.metta: size=223 sha256=d017e6577d56c750576fef1c8278f0265546106f8aa61ec88a935e260c5c215d
- **PASS** `L1` host file present: soul/evolutionary/index.metta: size=242 sha256=80531a27d6723c0269a8dd6b24e8be42f00db566c0fab2a61abb0e72155f8933
- **PASS** `L1` host file present: soul/evolutionary/runtime.metta: size=282 sha256=35abe9b03574b07d39dac7a2836b74992906df5a95582e48f7a80a7b02fbad22
- **PASS** `L1` host file present: soul/evolutionary/pending.metta: size=292 sha256=b501aed506ab76fa3115d512d00e4f38c0855cd953da11455c798dcca6029e83
- **PASS** `L1` host file present: soul/evolutionary/validation.metta: size=288 sha256=e7a517ce93aeddb982d51c4e0834ef2a43ecd641f03f76043cd7ef73058a03dc
- **PASS** `L1` host file present: soul/evolutionary/restart.metta: size=277 sha256=dabf125f42ed59860525cdc9a508b8477639d9640469cb689da4ee0e65cc2627
- **PASS** `L1` host file present: soul/evolutionary/rejected.metta: size=296 sha256=17fdf3a83842a60236874a1d78b9ce76d556ac869f152a8d513afe9368d2ad1d
- **PASS** `L1` lib_clarity_reasoning paren balance: balance=0
- **PASS** `L1` soul_kernel paren balance: balance=0
- **FAIL** `L1` live import block contains required imports: missing=['lib_quantale_autopoietic_epistemic_dynamics_engine_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY.metta', 'soul/evolutionary/README.metta', 'soul/evolutionary/archive/README.metta', 'soul/evolutionary/index.metta', 'soul/evolutionary/runtime.metta', 'soul/evolutionary/pending.metta', 'soul/evolutionary/validation.metta', 'soul/evolutionary/restart.metta', 'soul/evolutionary/rejected.metta', 'soul/durable.metta']
- **PASS** `L1` soul_kernel contains v08.7.2 journal class declarations: missing=[]
- **PASS** `L1` serialization valid: soul/durable.metta: checked=2 bad=0
- **PASS** `L1` serialization valid: soul/evolutionary/README.metta: checked=2 bad=0
- **PASS** `L1` serialization valid: soul/evolutionary/archive/README.metta: checked=2 bad=0
- **PASS** `L1` serialization valid: soul/evolutionary/index.metta: checked=3 bad=0
- **PASS** `L1` serialization valid: soul/evolutionary/runtime.metta: checked=3 bad=0
- **PASS** `L1` serialization valid: soul/evolutionary/pending.metta: checked=3 bad=0
- **PASS** `L1` serialization valid: soul/evolutionary/validation.metta: checked=3 bad=0
- **PASS** `L1` serialization valid: soul/evolutionary/restart.metta: checked=3 bad=0
- **PASS** `L1` serialization valid: soul/evolutionary/rejected.metta: checked=3 bad=0
- **PASS** `L2` container live file visible and sha-matched: lib_clarity_reasoning/lib_clarity_reasoning.metta: container=/PeTTa/repos/omegaclaw/lib_clarity_reasoning/lib_clarity_reasoning.metta sha_match=True
- **PASS** `L2` container live file visible and sha-matched: lib_clarity_reasoning/lib_quantale_autopoietic_epistemic_dynamics_engine_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY.metta: container=/PeTTa/repos/omegaclaw/lib_clarity_reasoning/lib_quantale_autopoietic_epistemic_dynamics_engine_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY.metta sha_match=True
- **PASS** `L2` container live file visible and sha-matched: soul/soul_kernel.metta: container=/PeTTa/repos/omegaclaw/soul/soul_kernel.metta sha_match=True
- **PASS** `L2` container live file visible and sha-matched: soul/durable.metta: container=/PeTTa/repos/omegaclaw/soul/durable.metta sha_match=True
- **PASS** `L2` container live file visible and sha-matched: soul/evolutionary/README.metta: container=/PeTTa/repos/omegaclaw/soul/evolutionary/README.metta sha_match=True
- **PASS** `L2` container live file visible and sha-matched: soul/evolutionary/archive/README.metta: container=/PeTTa/repos/omegaclaw/soul/evolutionary/archive/README.metta sha_match=True
- **PASS** `L2` container live file visible and sha-matched: soul/evolutionary/index.metta: container=/PeTTa/repos/omegaclaw/soul/evolutionary/index.metta sha_match=True
- **PASS** `L2` container live file visible and sha-matched: soul/evolutionary/runtime.metta: container=/PeTTa/repos/omegaclaw/soul/evolutionary/runtime.metta sha_match=True
- **PASS** `L2` container live file visible and sha-matched: soul/evolutionary/pending.metta: container=/PeTTa/repos/omegaclaw/soul/evolutionary/pending.metta sha_match=True
- **PASS** `L2` container live file visible and sha-matched: soul/evolutionary/validation.metta: container=/PeTTa/repos/omegaclaw/soul/evolutionary/validation.metta sha_match=True
- **PASS** `L2` container live file visible and sha-matched: soul/evolutionary/restart.metta: container=/PeTTa/repos/omegaclaw/soul/evolutionary/restart.metta sha_match=True
- **PASS** `L2` container live file visible and sha-matched: soul/evolutionary/rejected.metta: container=/PeTTa/repos/omegaclaw/soul/evolutionary/rejected.metta sha_match=True
- **FAIL** `L3` live topology README imported: expected=live-readme-present; present=False; returncode=0
- **FAIL** `L3` live topology archive README imported: expected=live-archive-readme-present; present=False; returncode=0
- **FAIL** `L3` live topology index imported: expected=live-index-present; present=False; returncode=0
- **FAIL** `L3` live topology runtime imported: expected=live-runtime-present; present=False; returncode=0
- **FAIL** `L3` live topology pending imported: expected=live-pending-present; present=False; returncode=0
- **FAIL** `L3` live topology validation imported: expected=live-validation-present; present=False; returncode=0
- **FAIL** `L3` live topology restart imported: expected=live-restart-present; present=False; returncode=0
- **FAIL** `L3` live topology rejected imported: expected=live-rejected-present; present=False; returncode=0
- **FAIL** `L3` live durable imported: expected=live-durable-present; present=False; returncode=0
- **FAIL** `L3` live durable probe imported: expected=live-durable-probe-present; present=False; returncode=0
- **FAIL** `L3` live runtime observation imported: expected=live-runtime-observation-present; present=False; returncode=0
- **FAIL** `L3` live pending candidate imported: expected=live-pending-candidate-present; present=False; returncode=0
- **FAIL** `L3` live validation evidence imported: expected=live-validation-evidence-present; present=False; returncode=0
- **FAIL** `L3` live restart evidence imported: expected=live-restart-evidence-present; present=False; returncode=0
- **FAIL** `L3` live rejected candidate imported: expected=live-rejected-candidate-present; present=False; returncode=0
- **FAIL** `L3` live semantic: canon eligibility runtime false: expected=false; present=False; returncode=0
- **FAIL** `L3` live semantic: canon eligibility soul approved: expected=canon-write-eligible; present=False; returncode=0
- **FAIL** `L3` live semantic: illegal runtime to canon jump: expected=blocked-illegal-jump; present=False; returncode=0
- **FAIL** `L3` live semantic: validation not approval: expected=blocked-no-soul-approval; present=False; returncode=0
- **FAIL** `L3` live semantic: runtime surface not canon: expected=process-not-canon; present=False; returncode=0
- **FAIL** `L3` live semantic: soul durable active canon: expected=durable-canon-active; present=False; returncode=0
- **FAIL** `L3` live semantic: finding no explicit route blocked: expected=blocked-finding-is-not-growth; present=False; returncode=0
- **FAIL** `L3` live semantic: genesis no explicit route blocked: expected=blocked-genesis-output-not-canon; present=False; returncode=0
- **FAIL** `L3` live semantic: hand authored verdict blocked: expected=blocked-hand-authored-verdict; present=False; returncode=0
- **FAIL** `L3` live semantic: dark file blocked: expected=blocked-dark-file; present=False; returncode=0
- **FAIL** `L3` live semantic: approval absent blocked: expected=blocked-no-soul-approval; present=False; returncode=0
- **FAIL** `L3` live semantic: durable canon active: expected=durable-canon-active; present=False; returncode=0
- **FAIL** `L3` live semantic: unreduced storage blocked: expected=blocked-unreduced-storage; present=False; returncode=0
- **FAIL** `L3` live semantic: trace A verdict: expected=metabolization-candidate; present=False; returncode=0
- **FAIL** `L3` live semantic: trace B verdict: expected=blocked-defensive-fixation; present=False; returncode=0
- **FAIL** `L3` live semantic: repetition without metabolization blocked: expected=blocked-repetition-without-metabolization; present=False; returncode=0
- **FAIL** `L3` live semantic: Trace A eligibility: expected=validation-eligible; present=False; returncode=0
- **FAIL** `L3` live semantic: Trace B audit: expected=audit-required; present=False; returncode=0
- **FAIL** `L3` live semantic: suspicion decays on metabolization: expected=suspicion-decays; present=False; returncode=0
- **FAIL** `L3` live semantic: suspicion rises on stuck recurrence: expected=suspicion-rises; present=False; returncode=0
- **FAIL** `L3` live semantic: high protection alone not penalized: expected=no-suspicion-penalty; present=False; returncode=0
- **FAIL** `L3` live semantic: journal class v1 accepted: expected=v1-accepted-mechanical-append-class; present=False; returncode=0
- **FAIL** `L3` live semantic: unsupported durable class blocked: expected=blocked-unsupported-new-class; present=False; returncode=0
- **FAIL** `L3` live semantic: canonical path accepted: expected=path-accepted; present=False; returncode=0
- **FAIL** `L3` live semantic: relative path blocked: expected=blocked-wrong-path-form; present=False; returncode=0
- **FAIL** `L3` live semantic: append allowed: expected=append-route-allowed; present=False; returncode=0
- **FAIL** `L3` live semantic: write blocked: expected=blocked-truncate-risk; present=False; returncode=0
- **FAIL** `L3` live semantic: serialization valid: expected=serialization-valid; present=False; returncode=0
- **FAIL** `L3` live semantic: unreduced serialization blocked: expected=blocked-unreduced-storage; present=False; returncode=0
- **FAIL** `L3` live semantic: import live: expected=import-live; present=False; returncode=0
- **FAIL** `L3` live semantic: not imported blocked: expected=blocked-dark-file; present=False; returncode=0
- **FAIL** `L3` live semantic: boot safe: expected=boot-safe; present=False; returncode=0
- **FAIL** `L3` live semantic: malformed recovery unknown blocked: expected=blocked-boot-poison-risk; present=False; returncode=0
- **FAIL** `L3` live semantic: findings absent compatible: expected=no-op-compatible-absent; present=False; returncode=0
- **FAIL** `L3` live semantic: finding without route blocked: expected=blocked-finding-not-growth; present=False; returncode=0
- **FAIL** `L3` live semantic: chroma no route blocked: expected=blocked-retrieval-not-canon; present=False; returncode=0
- **FAIL** `L3` live semantic: promotions no route blocked: expected=blocked-status-flag-not-canon; present=False; returncode=0
- **FAIL** `L3` live semantic: negative runtime claim blocked: expected=blocked-runtime-observation-is-not-growth; present=False; returncode=0
- **FAIL** `L3` live semantic: negative validation claim blocked: expected=blocked-validation-is-not-approval; present=False; returncode=0
- **FAIL** `L3` live semantic: negative genesis claim blocked: expected=blocked-genesis-output-not-canon; present=False; returncode=0
- **FAIL** `L3` live semantic: hyperseed context valid: expected=context-valid; present=False; returncode=0
- **FAIL** `L3` live semantic: hyperseed context missing blocked: expected=blocked-context-missing; present=False; returncode=0
- **FAIL** `L3` live semantic: hyperseed pbit evidence valid: expected=pbit-evidence-valid; present=False; returncode=0
- **FAIL** `L3` live semantic: hyperseed crisp certainty blocked: expected=blocked-crisp-certainty; present=False; returncode=0
- **FAIL** `L3` live semantic: hyperseed proto time valid: expected=proto-time-valid; present=False; returncode=0
- **FAIL** `L3` live semantic: hyperseed static presence blocked: expected=blocked-static-presence-not-habit; present=False; returncode=0
- **FAIL** `L3` live semantic: hyperseed structural signature valid: expected=structural-signature-valid; present=False; returncode=0
- **FAIL** `L3` live semantic: hyperseed missing structural signature blocked: expected=blocked-no-structural-signature; present=False; returncode=0
- **FAIL** `L3` live semantic: hyperseed continuity valid: expected=continuity-valid; present=False; returncode=0
- **FAIL** `L3` live semantic: hyperseed continuity too low blocked: expected=blocked-continuity-too-low; present=False; returncode=0
- **FAIL** `L3` live semantic: hyperseed artifact lineage valid: expected=artifact-lineage-valid; present=False; returncode=0
- **FAIL** `L3` live semantic: hyperseed approval lineage missing blocked: expected=blocked-approval-lineage-missing; present=False; returncode=0
- **FAIL** `L3` live semantic: hyperseed resource cost valid: expected=resource-cost-valid; present=False; returncode=0
- **FAIL** `L3` live semantic: hyperseed unbounded maintenance blocked: expected=blocked-unbounded-maintenance; present=False; returncode=0
- **FAIL** `L3` live semantic: hyperseed transfer compatible: expected=transfer-compatible; present=False; returncode=0
- **FAIL** `L3` live semantic: hyperseed transfer without resonance blocked: expected=blocked-copy-without-resonance; present=False; returncode=0
- **FAIL** `L3` live semantic: hyperseed approximation valid: expected=approximation-valid; present=False; returncode=0
- **FAIL** `L3` live semantic: hyperseed unsafe approximation blocked: expected=blocked-unsafe-approximation; present=False; returncode=0
- **FAIL** `L3` live semantic: hyperseed threshold pass: expected=hyperseed-durability-threshold-pass; present=False; returncode=0
- **FAIL** `L3` live semantic: hyperseed threshold context blocked: expected=blocked-context-missing; present=False; returncode=0
- **FAIL** `L3` live semantic: hyperseed import candidate ready: expected=import-candidate-ready; present=False; returncode=0
- **FAIL** `L3` live semantic: hyperseed governance open hold: expected=hold-governance-not-green; present=False; returncode=0
- **FAIL** `L3` live semantic: hyperseed file survival negative: expected=blocked-file-survival-not-structural-durability; present=False; returncode=0
- **FAIL** `L3` live semantic: hyperseed contextless negative: expected=blocked-context-missing; present=False; returncode=0
- **FAIL** `L3` live semantic: hyperseed cross context copy negative: expected=blocked-copy-without-resonance; present=False; returncode=0
