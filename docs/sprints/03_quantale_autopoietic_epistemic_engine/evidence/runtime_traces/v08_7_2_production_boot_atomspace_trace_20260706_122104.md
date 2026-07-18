# v08.7.2 production boot atomspace inspection trace

## Summary
- FAIL: 12
- PASS: 38

## Interpretation guardrail
This is not a one-shot `run.sh` import proof and not a live-body inline proof. Semantic PASS checks require a configured live query transport into the long-lived runtime atomspace. If Q0 is HOLD, discovery completed but production atomspace proof is still open.

## Checks
- **PASS** `L0` container exists: clarity_omega
- **PASS** `L1` host file present: lib_clarity_reasoning/lib_clarity_reasoning.metta: size=7395 sha256=3cce5155156379b789a7d480a5b9e065ce0f98ea50408620531c9387d3502a26
- **PASS** `L1` paren balance: lib_clarity_reasoning/lib_clarity_reasoning.metta: balance=0
- **PASS** `L1` host file present: lib_clarity_reasoning/lib_quantale_autopoietic_epistemic_dynamics_engine_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY.metta: size=338041 sha256=693089e6b69d3b40c0772e3a068e337bb325048f39f9e0a4f8bd9e6f66012851
- **PASS** `L1` paren balance: lib_clarity_reasoning/lib_quantale_autopoietic_epistemic_dynamics_engine_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY.metta: balance=0
- **PASS** `L1` host file present: soul/soul_kernel.metta: size=45103 sha256=fa70fb3baca9e25dfe5a30646707c9a86b48be19d153b4e552a44419bb0a7de6
- **PASS** `L1` paren balance: soul/soul_kernel.metta: balance=0
- **PASS** `L1` host file present: soul/durable.metta: size=395 sha256=b30addd567a3584dc4e0239ef4f2d0ce079252b4293a1ac108d6e1d34df64617
- **PASS** `L1` host file present: soul/evolutionary/README.metta: size=374 sha256=9286f68b41192caf0d2d4817b1d6c90e9662820240f8b8c4cb1f77f699d08a3d
- **PASS** `L1` host file present: soul/evolutionary/archive/README.metta: size=223 sha256=d017e6577d56c750576fef1c8278f0265546106f8aa61ec88a935e260c5c215d
- **PASS** `L1` host file present: soul/evolutionary/index.metta: size=242 sha256=80531a27d6723c0269a8dd6b24e8be42f00db566c0fab2a61abb0e72155f8933
- **PASS** `L1` host file present: soul/evolutionary/runtime.metta: size=282 sha256=35abe9b03574b07d39dac7a2836b74992906df5a95582e48f7a80a7b02fbad22
- **PASS** `L1` host file present: soul/evolutionary/pending.metta: size=292 sha256=b501aed506ab76fa3115d512d00e4f38c0855cd953da11455c798dcca6029e83
- **PASS** `L1` host file present: soul/evolutionary/validation.metta: size=288 sha256=e7a517ce93aeddb982d51c4e0834ef2a43ecd641f03f76043cd7ef73058a03dc
- **PASS** `L1` host file present: soul/evolutionary/restart.metta: size=277 sha256=dabf125f42ed59860525cdc9a508b8477639d9640469cb689da4ee0e65cc2627
- **PASS** `L1` host file present: soul/evolutionary/rejected.metta: size=296 sha256=17fdf3a83842a60236874a1d78b9ce76d556ac869f152a8d513afe9368d2ad1d
- **PASS** `L1` live import block contains required imports: missing=[]
- **PASS** `L1` soul_kernel contains v08.7.2 journal class declarations: missing=[]
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
- **PASS** `P0` runtime inventory: processes: returncode=0 chars=0 sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- **PASS** `P0` runtime inventory: network_tcp: returncode=0 chars=0 sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- **PASS** `P0` runtime inventory: network_unix: returncode=0 chars=0 sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- **PASS** `P0` runtime inventory: repo_top: returncode=0 chars=14441 sha256=c199c47d34bd8f2bd6af839e2841d2f3185051653b8d684899e252674fb93e37
- **PASS** `P0` runtime inventory: candidate_query_files: returncode=0 chars=16899 sha256=2c381880a725df21306932ba7c0d528a8257d4de78fba6de69c4fdefb2dd68ae
- **PASS** `P0` runtime inventory: grep_query_terms: returncode=0 chars=46765 sha256=f4d2132bd79fffbbbc4f72261d4f7addbf2a1ddaa53b44c26adfc0b5daa4b2d3
- **PASS** `P0` runtime inventory: process cwd/env hints: returncode=0 chars=1545 sha256=127c77b5c7e0c8b2d47c3037a4f637d927f56652ec9fbfa61bb7da0b1aedda54
- **PASS** `Q0` production live query surface configured: transports=['file']
- **FAIL** `Q1` production atomspace probe: topology durable loaded [file]: expected=live-durable-present; present=False; returncode=127; unreduced_echo=False
- **FAIL** `Q1` production atomspace probe: topology runtime loaded [file]: expected=live-runtime-present; present=False; returncode=127; unreduced_echo=False
- **FAIL** `Q1` production atomspace probe: canon eligibility runtime false [file]: expected=false; present=False; returncode=127; unreduced_echo=False
- **FAIL** `Q1` production atomspace probe: canon eligibility soul approved [file]: expected=canon-write-eligible; present=False; returncode=127; unreduced_echo=False
- **FAIL** `Q1` production atomspace probe: illegal runtime to canon jump [file]: expected=blocked-illegal-jump; present=False; returncode=127; unreduced_echo=False
- **FAIL** `Q1` production atomspace probe: journal class v1 accepted [file]: expected=v1-accepted-mechanical-append-class; present=False; returncode=127; unreduced_echo=False
- **FAIL** `Q1` production atomspace probe: append allowed [file]: expected=append-route-allowed; present=False; returncode=127; unreduced_echo=False
- **FAIL** `Q1` production atomspace probe: write blocked [file]: expected=blocked-truncate-risk; present=False; returncode=127; unreduced_echo=False
- **FAIL** `Q1` production atomspace probe: hyperseed threshold pass [file]: expected=hyperseed-durability-threshold-pass; present=False; returncode=127; unreduced_echo=False
- **FAIL** `Q1` production atomspace probe: hyperseed import candidate ready [file]: expected=import-candidate-ready; present=False; returncode=127; unreduced_echo=False
- **FAIL** `Q1` production atomspace probe: governance open hold [file]: expected=hold-governance-not-green; present=False; returncode=127; unreduced_echo=False
- **FAIL** `Q1` production atomspace probe: contextless negative [file]: expected=blocked-context-missing; present=False; returncode=127; unreduced_echo=False
