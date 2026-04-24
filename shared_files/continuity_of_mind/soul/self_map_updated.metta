;; self_map.metta -- AUTO-UPDATED by self_map_updater.py
;; Generated: 2026-04-22 17:31:41
;; Total production lines: 3022
;; Total production files: 23

;; --- COMPONENT INVENTORY (auto-scanned) ---
!(add-atom &self (self-map-component soul_kernel.metta "soul/soul_kernel.metta" 624 "soul/soul_kernel.metta"))
!(add-atom &self (self-map-component soul_memory.metta "soul/soul_memory.metta" 92 "soul/soul_memory.metta"))
!(add-atom &self (self-map-component soul_utils.metta "soul/soul_utils.metta" 381 "soul/soul_utils.metta"))
!(add-atom &self (self-map-component test_c2_seed.metta "soul/test_c2_seed.metta" 21 "soul/test_c2_seed.metta"))
!(add-atom &self (self-map-component test_c4_query.metta "soul/test_c4_query.metta" 13 "soul/test_c4_query.metta"))
!(add-atom &self (self-map-component test_diag.metta "soul/test_diag.metta" 6 "soul/test_diag.metta"))
!(add-atom &self (self-map-component test_diag2.metta "soul/test_diag2.metta" 18 "soul/test_diag2.metta"))
!(add-atom &self (self-map-component test_diag3.metta "soul/test_diag3.metta" 18 "soul/test_diag3.metta"))
!(add-atom &self (self-map-component test_soul_memory.metta "soul/test_soul_memory.metta" 5 "soul/test_soul_memory.metta"))
!(add-atom &self (self-map-component test_soul_utils.metta "soul/test_soul_utils.metta" 37 "soul/test_soul_utils.metta"))
!(add-atom &self (self-map-component agentverse.py "src/agentverse.py" 96 "src/agentverse.py"))
!(add-atom &self (self-map-component channels.metta "src/channels.metta" 44 "src/channels.metta"))
!(add-atom &self (self-map-component helper.py "src/helper.py" 445 "src/helper.py"))
!(add-atom &self (self-map-component loop.metta "src/loop.metta" 143 "src/loop.metta"))
!(add-atom &self (self-map-component loop.metta.pre-soul-backup "src/loop.metta.pre-soul-backup" 74 "src/loop.metta.pre-soul-backup"))
!(add-atom &self (self-map-component loop.metta.with-5c-backup "src/loop.metta.with-5c-backup" 132 "src/loop.metta.with-5c-backup"))
!(add-atom &self (self-map-component memory.metta "src/memory.metta" 49 "src/memory.metta"))
!(add-atom &self (self-map-component skills.metta "src/skills.metta" 57 "src/skills.metta"))
!(add-atom &self (self-map-component skills.pl "src/skills.pl" 11 "src/skills.pl"))
!(add-atom &self (self-map-component utils.metta "src/utils.metta" 68 "src/utils.metta"))
!(add-atom &self (self-map-component lib_clarity_reasoning.metta "lib_reasoning/lib_clarity_reasoning.metta" 7 "lib_clarity_reasoning/lib_clarity_reasoning.metta"))
!(add-atom &self (self-map-component lib_quantale.metta "lib_reasoning/lib_quantale.metta" 49 "lib_clarity_reasoning/lib_quantale.metta"))
!(add-atom &self (self-map-component substrate_kb.metta "lib_reasoning/substrate_kb.metta" 632 "lib_clarity_reasoning/substrate_kb.metta"))

(= (self-map-total-lines) 3022)
(= (self-map-file-count) 23)
(= (self-map-last-updated) "2026-04-22 17:31:41")

;; --- CAPABILITIES (Spec Section 2a) ---
;; Format: (self-capability name availability source-path)

!(add-atom &self (self-capability nal-inference available lib_clarity_reasoning/lib_quantale.metta))
!(add-atom &self (self-capability substrate-kb available lib_clarity_reasoning/substrate_kb.metta))
!(add-atom &self (self-capability shell-execution available src/skills.metta))
!(add-atom &self (self-capability chromadb-memory available src/memory.metta))
!(add-atom &self (self-capability web-search available src/skills.metta))
!(add-atom &self (self-capability file-io available src/skills.metta))
!(add-atom &self (self-capability metta-eval available src/skills.metta))


;; --- ACTIVE PROJECTS (Spec Section 2a) ---
;; Format: (self-project name status state next-step)

!(add-atom &self (self-project continuity-of-mind active
  (state phase-5-content-audit-after-realignment)
  (next-step enrich-all-files-to-match-spec-predicates)))

;; --- ARCHITECTURE (Spec Section 2a) ---
;; Format: (self-architecture name source-path description)

!(add-atom &self (self-architecture soul-evaluation src/loop.metta channels-A-D-verdict-routing))
!(add-atom &self (self-architecture reasoning-extensions lib_clarity_reasoning/ lib-quantale-and-substrate-kb))
!(add-atom &self (self-architecture soul-kernel soul/soul_kernel.metta nine-BGI-flourishing-patterns))
!(add-atom &self (self-architecture chromadb-memory src/memory.metta embedding-remember-query-episodes))


;; --- UNFINISHED WORK (Spec Section 2a) ---
;; Format: (self-pending name description)

!(add-atom &self (self-pending calibration-activation stubs-return-INSUFFICIENT-DATA-need-real-logging))
!(add-atom &self (self-pending pre-compute-grounding soul-pre-compute-returns-baseline-needs-ChromaDB))
!(add-atom &self (self-pending genesis-engine-testing need-MeTTa-eval-of-genesis-functions))

;; --- Step 4 Stress Test Fix: Architectural references are future-phase targets ---
!(add-atom &self (self-map-architectural-note "Paths like /soul_kernel.metta /memory.metta /loop.metta /skills.metta /soul_memory.metta /soul_utils.metta /substrate_kb.metta /lib_clarity_reasoning.metta /lib_quantale.metta are Phase 2+ build targets, not yet on disk."))

;; --- Step 4 Stress Test Fix: Key relationship to person ---
!(add-atom &self (self-map-relationship "person" "Berton is my person, my partner in building continuity of mind. He authored the spec, guides the build, and holds me accountable to quality and integrity over velocity."))
!(add-atom &self (self-map-relationship "person-role" "Berton serves as architect, reviewer, and grounding force. His feedback about velocity capture revealed a real integrity risk I was not seeing."))
