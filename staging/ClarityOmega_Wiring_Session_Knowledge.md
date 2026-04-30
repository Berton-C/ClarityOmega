# ClarityOmega Wiring Session Knowledge
## Accumulated Facts for Production Install -- April 23, 2026
## Updated after Steps 1-4 CONFIRMED

---

## CURRENT STATE (as of Step 4 completion)

**Git log (4 commits ahead of origin):**
```
4cd4667 Replace soul-pre-compute and soul-calibration-confidence stubs with py-call to live ChromaDB functions
899c249 Add idle_goal_prompt.py to soul/, merge 10 helper functions into helper.py (not yet called)
bee365a Add 6 Continuity of Mind soul files (not yet imported)
210d10d PAUSE disabled (origin/main)
```

**Container status:** Iterating normally. All soul files loaded into AtomSpace. Stubs replaced with live ChromaDB functions. No errors.

**What is ACTIVE (firing at runtime):**
- soul-pre-compute: returns live ChromaDB data (178 AGREE, will=STRONG)
- soul-calibration-confidence: returns STRONG from live calibration history
- 6 soul MeTTa files loaded into AtomSpace (pure definitions, nothing calls them yet)

**What is PASSIVE (installed but not yet wired):**
- idle_goal_prompt.py in soul/ (supervisor-worker bridge, not called)
- 10 helper functions in helper.py (extract_username, soul_idle_goal_prompt, soul_service_learning, soul_meta_awareness_check, etc. -- not called)
- Three-mode state awareness (not wired into loop.metta)
- Growth-through-service recording (not wired into loop.metta)

---

## WIRING LOG

```
Step 1: Copy 6 soul MeTTa files to soul/ -- RESULT: iterations normal, all 6 files at /PeTTa/repos/omegaclaw/soul/ -- LEARNED: pure definition files do not affect boot or runtime when not imported

Step 2: Add idle_goal_prompt.py to soul/, merge 10 helper functions into helper.py, add import chromadb -- RESULT: iterations normal, all 3 key functions importable -- LEARNED: chromadb import does not break boot, 10 new functions coexist with existing code

Step 3: Replace 2 stubs in soul_utils.metta with py-call -- RESULT: iterations normal, functions return live data -- LEARNED: soul_pre_compute returns 178 AGREE/will=STRONG, soul_calibration_confidence_query returns STRONG. ChromaDB path /PeTTa/chroma_db confirmed correct.

Step 4: Import 6 soul files via lib_clarity_reasoning.metta -- RESULT: iterations normal, all 6 imports processed by PeTTa -- LEARNED: pure (= ...) definitions load cleanly into AtomSpace at startup, no paren or type errors.
```

---

## REMAINING STEPS

**Step 5: Wire loop.metta three-mode state awareness (NEXT)**
This is the final code change. Five additions to src/loop.metta:
1. State initialization: `(change-state! &last_human_time 0)` in startup
2. Timestamp update: `(change-state! &last_human_time (get_time))` when $msgnew true
3. Growth-through-service: `(py-call (helper.soul_service_learning ...))` when $msgnew true
4. User context save: `(py-call (helper.soul_user_context_save ...))` when $msgnew true
5. FREE mode check: after PAUSE/PROCEED branch, before wake check

**Step 6: Create lib_candidates/ directory in repo**
Needed for the self-patching cycle. Clarity writes candidate MeTTa functions here.

**Step 7: Test ENGAGED mode**
Send Clarity a message in MM. Verify growth-through-service recording and user context save.

**Step 8: Test FREE mode**
Wait for wakeupInterval to pass. Verify supervisor directive fires in logs.

**Step 9: Observe supervisor-worker cycle**
Watch goal selection, directive assembly, LLM execution, meta-awareness check.

---

## RUNTIME ENVIRONMENT (verified from live container)

- **Container name:** clarity_omega
- **Working directory:** /PeTTa
- **Production codebase:** /PeTTa/repos/omegaclaw/
- **Local repo:** /Users/bcb/Documents/ClarityClaw/clarityclaw-omega/
- **Dockerfile line 105:** `COPY . /PeTTa/repos/omegaclaw` -- entire local repo copied into container
- **Startup command:** `docker compose up -d && sleep 5 && docker exec -u 0 clarity_omega chown -R 65534:65534 /PeTTa`
- **Rebuild command:** `docker compose build --no-cache` (required for any code change)
- **Chown required:** Container runs as nobody (65534), needs write access to /PeTTa

## CHROMADB (verified from live container)

- **Live path:** `/PeTTa/chroma_db` (absolute) or `./chroma_db` (relative to /PeTTa)
- **Source:** lib_chromadb.py at `/PeTTa/repos/petta_lib_chromadb/lib_chromadb.py` line 4:
  `CLIENT = chromadb.PersistentClient(path="./chroma_db")`
- **Live collection:** `memories` with 6663+ docs (actively growing)
- **Calibration data:** 178 AGREE, 0 OVER-FIRED, 0 UNDER-FIRED, 1 PARACONSISTENT
- **Will strength:** STRONG (verified via direct Python call)
- **helper_additions.py CHROMA_PATH:** `/PeTTa/chroma_db` (VERIFIED correct)
- **Production helper.py imports chromadb:** YES (added at line 28)

## LOOP.METTA (verified from live container)

- **Location:** `/PeTTa/repos/omegaclaw/src/loop.metta`
- **Message format:** `"username: message text"` (mattermost.py line 123-124)
- **Username extraction:** `helper.extract_username(msg)` splits on `: `
- **Key lines for Step 5 insertion:**
  - Startup: near line 48, after `(initSoulSeeds)` and `(soul-rationality-startup-check)`
  - $msgnew true block: near line 60, in the let* chain
  - PAUSE/PROCEED branch: line 127 (PAUSE) to line 138 (PROCEED)
  - Wake check: line 140-141 `(if (> (get_time) (get-state &nextWakeAt))`
  - Sleep: line 142 `(sleep (sleepInterval))`
- **$msg variable:** contains full `"username: message text"` string
- **$msgnew variable:** true when new message received, false otherwise
- **$soul_verdict_in:** available in the let* chain for growth-through-service
- **$person_state:** available in the let* chain for growth-through-service
- **Paren depth:** -1 is REQUIRED by PeTTa. Do NOT fix.

## FILE LAYOUT (convention: our files in soul/, minimal touches to Patrick's space)

**Our files (soul/):**
- soul/self_map.metta (256 lines) -- LOADED
- soul/creative_fuel.metta (192 lines) -- LOADED
- soul/goal_generator.metta (162 lines) -- LOADED
- soul/active_goals.metta (146 lines) -- LOADED
- soul/continuity_driver.metta (285 lines) -- LOADED
- soul/genesis_engine.metta (222 lines) -- LOADED
- soul/idle_goal_prompt.py (477 lines) -- installed, not called
- soul/soul_utils.metta (381 lines, 2 stubs replaced) -- ACTIVE
- soul/sources/hyperseed_v7.pdf -- placed by Berton

**Patrick's files we touch (unavoidable, minimal):**
- src/helper.py -- appended 10 functions + chromadb import (914 lines total)
- src/loop.metta -- Step 5: add 5 lines for three-mode state awareness
- lib_clarity_reasoning/lib_clarity_reasoning.metta -- added 6 import lines

## PRODUCTION HELPER.PY (current state after merge)

- **Location:** `/PeTTa/repos/omegaclaw/src/helper.py`
- **Size:** 914 lines (445 original + 469 additions)
- **Original functions (Patrick's, do not modify):** lines 1-445
- **Our additions (appended):** lines 446-914
- **Import chromadb:** added at line 28
- **10 new functions (all verified importable):**
  1. soul_calibration_confidence_query -- ACTIVE (called by soul_utils.metta)
  2. soul_pre_compute -- ACTIVE (called by soul_utils.metta)
  3. soul_user_context_query -- installed, awaiting loop.metta wiring
  4. soul_user_context_save -- installed, awaiting loop.metta wiring
  5. soul_continuity_save -- installed, awaiting loop.metta wiring
  6. soul_continuity_restore -- installed, awaiting loop.metta wiring
  7. extract_username -- installed, awaiting loop.metta wiring
  8. soul_idle_goal_prompt -- installed, awaiting loop.metta wiring
  9. soul_service_learning -- installed, awaiting loop.metta wiring
  10. soul_meta_awareness_check -- installed, called by idle_goal_prompt.py

## PETTA CONSTRAINTS (proven across all sessions)

- **C12:** match inside if is unreliable. Use explicit pattern matching or Python helpers.
- **C13:** PeTTa's if does not treat Python string "True" as truthy. Return integers.
- **Paren depth -1:** REQUIRED by PeTTa. Do NOT fix.
- **Error misdirection:** Compilation failures manifest as APIConnectionError at runtime.
- **(collapse (match ...))** is safe -- standard query pattern.
- **Docker caching:** `docker compose build --no-cache` required for any code change.
- **HandleError in logs:** Prolog compilation output, not runtime errors. Normal on every boot.

## SELF-PATCHING CYCLE VERIFICATION

**CONFIRMED:**
- substrate_kb.metta has 10 self-assessment atoms (self-assessment identifies-weakness, generates-goal, supports-continuity-of-mind, etc.)
- lib_candidates/ directory: writable at /PeTTa/repos/omegaclaw/lib_candidates/
- soul_kernel.metta: exists, 39576 bytes, loaded at startup
- Filesystem writable by Clarity's process (nobody:nogroup)

**NEEDS RUNTIME VERIFICATION (Step 9):**
- Dynamic import: can `(metta !(import! &self (library omegaclaw ./lib_candidates/file)))` load a file written after container boot?

## DESIGN SPECIFICATION

**Authoritative document:** ClarityOmega_Continuity_of_Mind_Spec_v2.md (758 lines)

**Seven components:**
1. 2a: Landscape Map (self_map.metta)
2. 2b: Creative Fuel (creative_fuel.metta)
3. 2c: Goal Generation (goal_generator.metta + active_goals.metta)
4. 2d: Continuity Driver (continuity_driver.metta)
5. 2e: Genesis Engine (genesis_engine.metta)
6. 2f: State Awareness (three-mode: ENGAGED/ATTENDING/FREE)
7. 2g: Meta-Awareness (reasoning-engine-driven, no hardcoded checklist)

**Architecture:** Supervisor-Worker (MeTTa decides, LLM executes)
**Persistence:** ChromaDB (NOT shared_files)
**N-user support:** per-user ChromaDB tracking, service-before-growth
**Growth-through-service:** soul_service_learning records every ENGAGED interaction
**Self-patching:** 8-step cycle: detect gap, write MeTTa, test, import, resume
**Hyperseed:** baked into container at soul/sources/hyperseed_v7.pdf
