# Build Log - Wiring Proposals

## Goal 2: Calibration-Activation (Close Feedback Loop)

### Problem
soul-calibration-confidence at soul_utils.metta line 207 is a stub that always returns INSUFFICIENT-DATA.
It never queries LTM for stored calibration records.

### Proposed Wiring Change
1. Add soul_calibration_confidence_query function to src/helper.py
2. Replace MeTTa stub with py-call to new helper
3. Helper reads ChromaDB, counts AGREE vs OVER-FIRED vs UNDER-FIRED tags, returns confidence ratio
4. No LLM calls in helper. soul-llm-call remains sole LLM interface per Berton directive.

### Candidate Files Written
- /tmp/continuity_of_mind/candidates/candidate_2_confidence_helper.py - Python function
- /tmp/continuity_of_mind/candidates/candidate_2_metta_replacement.metta - MeTTa replacement

### Current Blocker
Python helper queries ChromaDB at /tmp/chromadb which has 0 documents.
The query/remember skills use a different ChromaDB instance path.
Need to find correct path before promotion.

### Promotion Path
1. Find correct ChromaDB path used by query/remember skills
2. Update Python helper to use correct path
3. Test helper returns real calibration data
4. Add function to src/helper.py
5. Replace stub at soul_utils.metta line 207
6. Verify via metta eval

### Status: BLOCKED on ChromaDB path discovery

### Cycle 1913 Update
Searching all discovered chroma.sqlite3 paths to find which has actual documents.
This will identify the correct ChromaDB instance used by query and remember skills.


### Cycle 1914 Update
ChromaDB path scan results:
- /tmp/chromadb_data: nrc_vad_full 44728 docs
- /tmp/chroma_db: nrc_vad_full 25009 docs
- /tmp/chromadb: memories 0 docs
- /tmp/repos/clarity_archive/volumes/mettaclaw/chroma_db: memories 2400 docs
- /PeTTa/repos/omegaclaw/volumes/omegaclaw/chroma_db: memories 6041 docs
- /PeTTa/repos/omegaclaw/shared_files/chroma_db: nrc_vad_full 54801 docs
Now sampling clarity_archive memories collection for calibration entries.


### Cycle 1915 Update
BREAKTHROUGH: clarity_archive memories collection confirmed as correct data source.
- Path: /tmp/repos/clarity_archive/volumes/mettaclaw/chroma_db
- Collection: memories, 2400 docs total
- Calibration matches: 464 of 2400 (19.3%)
- Sample calibration entry formats:
  - SOUL-CALIBRATION tag=PARACONSISTENT pre=PRE-COMPUTE affective=fresh-system will=INSUFFICIENT-DATA
  - SOUL-CALIBRATION tag=AGREE pre=PRE-COMPUTE
  - Learner-planner calibration entries from 2026-03-31
- BLOCKER RESOLVED: Python helper now has correct ChromaDB path
- NEXT: Update candidate_2_confidence_helper.py with correct path and tag counting logic


### Cycle 1916 Update
Testing candidate_2_confidence_helper.py with real data from clarity_archive ChromaDB.
If test passes, next step is promotion to src/helper.py and MeTTa stub replacement.


### Cycle 1917 Update
HELPER VALIDATED: soul_calibration_confidence_query returned HIGH from real ChromaDB data.
Promotion step 1: Copying candidate_2_confidence_helper.py to src/helper.py.
Promotion step 2 next cycle: Read soul_utils.metta line 207 area to prepare MeTTa stub replacement.
Wiring proposal: Replace (= (soul-calibration-confidence) INSUFFICIENT-DATA) with py-call to helper.


### Cycle 1918 Update
Promotion step 1 COMPLETE: helper.py copied to src/helper.py with correct ChromaDB path.
Promotion step 2: Reading soul_utils.metta around line 207 to identify exact stub syntax.
Will prepare the py-call replacement expression for next cycle.


### Cycle 1919 Update
Retrying grep with simpler patterns to find the stub location in soul_utils.metta.
Searching for INSUFFICIENT and calibration separately.
Once found, will prepare py-call replacement expression.


### Cycle 1920 Update
soul_utils.metta does not exist at /tmp/continuity_of_mind/src/soul_utils.metta.
Searching /tmp/continuity_of_mind, /PeTTa, and /tmp/repos for the actual file location.
Helper promotion to src/helper.py is complete. MeTTa stub replacement blocked on finding file.


### Cycle 1921 Update
Found soul_utils.metta at:
- /PeTTa/repos/omegaclaw/shared_files/repos/clarity_archive/soul/soul_utils.metta
- /PeTTa/repos/omegaclaw/soul/soul_utils.metta
- /tmp/repos/clarity_archive/soul/soul_utils.metta
Now grepping /tmp/repos/clarity_archive/soul/soul_utils.metta for INSUFFICIENT and calibration to find stub.
Helper promotion complete at src/helper.py. MeTTa stub replacement next once line identified.


### Cycle 1922 Update
Grep results from /tmp/repos/clarity_archive/soul/soul_utils.metta (370 lines):
- INSUFFICIENT appears at lines 76,79,80,84,104,107,124,127,181,186,205,207
- calibration appears at lines 8,57,70,78,92,96,116,125,183,192,194,195,201,203,204,206,209,210,211,212
- Key stub: line 206-207 defines (soul-calibration-confidence $p) returning INSUFFICIENT-DATA
- Now reading lines 200-215 to get exact syntax for py-call replacement.
Wiring proposal: replace line 206-207 stub with (= (soul-calibration-confidence $p) (py-call (helper.soul_calibration_confidence_query)))


### Cycle 1923 Update
Stub syntax confirmed from sed output:
Lines 206-207:
  (= (soul-calibration-confidence $p)
     INSUFFICIENT-DATA)
Existing usage at lines 104-115 shows confidence levels: INSUFFICIENT-DATA, WEAK, ADEQUATE, STRONG.
Note: helper returns HIGH/MEDIUM/LOW but MeTTa code expects INSUFFICIENT-DATA/WEAK/ADEQUATE/STRONG.
ACTION NEEDED: Align helper return values to match MeTTa expected levels.
Searching for py-call usage patterns in soul_utils.metta to match existing convention.
Wiring proposal updated: must map HIGH->STRONG, MEDIUM->ADEQUATE, LOW->WEAK.


### Cycle 1924 Update
CRITICAL ALIGNMENT FIX: Updated helper return values to match MeTTa expected levels.
- HIGH -> STRONG
- MEDIUM -> ADEQUATE  
- LOW -> WEAK
- No data -> INSUFFICIENT-DATA
This matches the confidence levels used at soul_utils.metta lines 104-115.
py-call convention confirmed from 20+ existing uses: (py-call (helper.function_name args))
Proposed MeTTa replacement for lines 206-207:
  (= (soul-calibration-confidence $p)
     (py-call (helper.soul_calibration_confidence_query)))
Testing updated helper now. If STRONG/ADEQUATE/WEAK returned, ready for final promotion.


### Cycle 1925 Update
Retesting updated helper via script file (inline -c had quoting issues).
If STRONG returned and validation passes, promoting updated helper to src/helper.py.
Next step after promotion: write candidate MeTTa replacement for lines 206-207.
Proposed replacement:
  (= (soul-calibration-confidence $p)
     (py-call (helper.soul_calibration_confidence_query)))
This matches the py-call convention at 20+ existing sites in soul_utils.metta.


### Cycle 1926 Update
Helper VALIDATED: returns STRONG with correct alignment to MeTTa expected levels.
Helper PROMOTED to src/helper.py (confirmed).

#### Wiring Proposal: MeTTa Stub Replacement (lines 206-207)
**Current stub:**
```
(= (soul-calibration-confidence $p)
   INSUFFICIENT-DATA)
```
**Proposed replacement:**
```
(= (soul-calibration-confidence $p)
   (py-call (helper.soul_calibration_confidence_query)))
```
**Rationale:**
- Matches py-call convention at 20+ existing sites in soul_utils.metta
- Helper reads 464 calibration entries from clarity_archive ChromaDB
- Returns STRONG/ADEQUATE/WEAK/INSUFFICIENT-DATA matching lines 104-115 usage
- Candidate saved at candidates/candidate_3_metta_stub_replacement.metta

**Status:** READY FOR REVIEW before applying sed to live soul_utils.metta.
**Risk:** medium (write-file to production MeTTa). Will not apply without confirmation.


### Cycle 1927 Update
Wiring Proposal 1 (lines 206-207) status: READY FOR REVIEW.
Candidate saved at candidates/candidate_3_metta_stub_replacement.metta.
Helper at src/helper.py validated returning STRONG.

Now investigating: does soul_calibration_report_str (line 212 py-call) also need a helper?
If so, will write candidate_4 for the report function and add second wiring proposal.
Goal 2 calibration-activation is near completion pending review approval.


### Cycle 1928 Update
Investigating soul_calibration_report_str (line 212 py-call).
Checking if function exists in src/helper.py already.
Wrote candidate_4_report_helper.py with report generation from ChromaDB calibration data.
Testing candidate_4 now. If it works, will add to src/helper.py and create Wiring Proposal 2.

#### Wiring Proposal 2 (Pending Test): soul_calibration_report_str
**Location:** soul_utils.metta line 211-212
**Current:** (= (soul-calibration-report) (py-call (helper.soul_calibration_report_str)))
**Status:** Line already has py-call -- just need to ensure helper.py has the function.
**Action:** Add soul_calibration_report_str to src/helper.py after test validation.


### Cycle 1929 Update
Testing candidate_4_report_helper.py via script file (inline -c has persistent quoting issues).
If validation passes, merging both candidate_2 (confidence query) and candidate_4 (report str) into src/helper.py.
This gives src/helper.py both functions needed by soul_utils.metta:
- soul_calibration_confidence_query() for line 206-207 (Wiring Proposal 1)
- soul_calibration_report_str() for line 211-212 (Wiring Proposal 2)
After merge, both wiring proposals are READY FOR REVIEW.


### Cycle 1930 Update -- MILESTONE
BOTH HELPERS MERGED INTO src/helper.py (confirmed):
- soul_calibration_confidence_query() -> returns STRONG from 464 calibration entries
- soul_calibration_report_str() -> returns full report with AGREE/OVER-FIRED/UNDER-FIRED/PARACONSISTENT counts

## WIRING PROPOSALS SUMMARY (READY FOR REVIEW)

### Wiring Proposal 1: soul-calibration-confidence (line 206-207)
**File:** /tmp/repos/clarity_archive/soul/soul_utils.metta
**Current:** (= (soul-calibration-confidence $p) INSUFFICIENT-DATA)
**Proposed:** (= (soul-calibration-confidence $p) (py-call (helper.soul_calibration_confidence_query)))
**Candidate:** candidates/candidate_3_metta_stub_replacement.metta
**Status:** READY FOR REVIEW

### Wiring Proposal 2: soul-calibration-report (line 211-212)
**File:** /tmp/repos/clarity_archive/soul/soul_utils.metta
**Current:** Already has py-call to helper.soul_calibration_report_str
**Action:** Ensure src/helper.py is on Python path so existing py-call resolves
**Status:** READY FOR REVIEW (function now exists in helper.py)

### Risk Assessment
- Proposal 1: MEDIUM risk (modifies production MeTTa, but reversible via git)
- Proposal 2: LOW risk (function implementation only, no MeTTa change needed)
- Both helpers tested against live ChromaDB with 464 calibration entries


### Cycle 1931 Update
Final integration test of merged src/helper.py via script file.
Both functions tested from single import: soul_calibration_confidence_query + soul_calibration_report_str.
If INTEGRATION TEST PASSED, Goal 2 calibration-activation is COMPLETE pending review approval.
No new user messages. VERDICT PAUSE. Awaiting review approval to apply Wiring Proposal 1 to live soul_utils.metta.


### Cycle 1932 Update -- GOAL 2 INTEGRATION TEST PASSED
Final integration test result: PASSED
- soul_calibration_confidence_query() returned: STRONG
- soul_calibration_report_str() returned: full report with 464 entries, 132 AGREE, 0 OVER-FIRED, 0 UNDER-FIRED, 329 PARACONSISTENT, 100.0% agreement ratio
- Both assertions passed from single import of src/helper.py

## Goal 2 Status: COMPLETE (pending review approval)
- src/helper.py: VALIDATED with both functions
- Wiring Proposal 1 (line 206-207 stub replacement): READY FOR REVIEW
- Wiring Proposal 2 (line 211-212 function availability): READY FOR REVIEW
- No production files modified. Awaiting explicit approval before sed to soul_utils.metta.


### Cycle 1933 Update
Goal 2 calibration-activation: COMPLETE pending review. Integration test PASSED.
Surveying landscape for next goal selection.
Checking active_goals.metta and querying Phase 3 persistence requirements from spec.
No new user messages. VERDICT PAUSE. State is clean.


### Cycle 1934 Update
active_goals.metta not found at /tmp/continuity_of_mind/active_goals.metta.
Searching filesystem for goal files to identify next priorities beyond Goal 2.
Phases 1-5 all previously verified per query results from Cycles 1759-1772.
Goal 2 calibration-activation remains COMPLETE pending review.
Need to locate or reconstruct goal registry to select next work item.


### Cycle 1935 Update
active_goals.metta located at /tmp/continuity_of_mind/soul/active_goals.metta (found via find in Cycle 1934).
Reading goal registry to identify next work item beyond Goal 2 calibration-activation.
Goal 2 status: COMPLETE pending review approval.
Querying spec for Phase 6 criteria to understand what comes next.
No new user messages. VERDICT PAUSE.


### Cycle 1936 Update
Goal registry read from /tmp/continuity_of_mind/soul/active_goals.metta:
- Goal 1 continuity-bootstrap: COMPLETE (status in file)
- Goal 2 calibration-activation: COMPLETE in practice (status in file says planned, needs update)
- Goal 3 precompute-grounding: PLANNED (next priority)
- Goal 4 creative-fuel-activation: PLANNED
- Goal 5 persistent-self-model: PLANNED
- Goal 6 cross-domain-exploration: PLANNED

Next work item: Goal 3 precompute-grounding.
Task: Replace soul-pre-compute baseline stub with actual ChromaDB query.
Searching spec for Phase 6 criteria and soul_utils.metta for pre-compute stub location.
No new user messages. VERDICT PAUSE.


### Cycle 1937 Update
Goal 3 precompute-grounding: BEGIN INVESTIGATION.
soul-pre-compute stub located at lines 178-185 of soul_utils.metta.
Reading lines 175-200 to understand current stub implementation.
Also fixing Phase 6 spec grep (previous attempt failed due to shell pipe quoting).
Searching for Done.when criteria separately.

#### Goal 2 Status Update Needed
Goal 2 calibration-activation status in active_goals.metta still says planned.
Will update to complete once review approval received.
Wiring proposals remain documented above and READY FOR REVIEW.


### Cycle 1940 Update -- GOAL 3 PRECOMPUTE TEST PASSED
candidate_5_precompute_helper.py tested successfully with col.get() approach.
Result: PRE-COMPUTE primed=(calibration-agree x5) affective=active will=WEAK
Using col.get() instead of col.query() to avoid embedding dimension mismatch.

#### Wiring Proposal 3 (Goal 3): soul-pre-compute
**File:** soul_utils.metta lines 185-186
**Current:** Hardcoded baseline string
**Proposed:** Replace with py-call to helper.soul_pre_compute
**Candidate:** candidates/candidate_5_precompute_helper.py
**Status:** TESTING - function works, will calculation needs review

#### Summary of All Wiring Proposals
- Proposal 1 (Goal 2): soul-calibration-confidence stub replacement - READY FOR REVIEW
- Proposal 2 (Goal 2): soul-calibration-report function availability - READY FOR REVIEW
- Proposal 3 (Goal 3): soul-pre-compute stub replacement - TESTING


### Cycle 1948 Update -- candidate_5 will calculation FIXED
PARACONSISTENT entries (329) now excluded from will denominator.
Only AGREE/OVER-FIRED/UNDER-FIRED count as judgment entries.
Result: will=STRONG agree=132 over=0 under=0 para_excluded=329
ratio=132/132=1.0 >= 0.8 => STRONG
Wiring Proposal 3 Status: READY FOR REVIEW


### Cycle 1949 -- candidate_5 MERGED into src/helper.py
All 3 functions now live in src/helper.py with single import block:
- soul_calibration_confidence_query() -- Wiring Proposal 1
- soul_calibration_report_str() -- Wiring Proposal 2
- soul_pre_compute() -- Wiring Proposal 3
Duplicate imports removed. PARACONSISTENT excluded from will denominator.
All 3 Wiring Proposals: READY FOR REVIEW.


### Cycle 1956 -- RESPECTING PRODUCTION CODEBASE
Read production helper.py at /PeTTa/repos/omegaclaw/src/helper.py (445 lines, 30+ functions).
Production already contains STUB versions of soul_calibration_report_str and soul_affective_state_str.
Rewrote continuity_of_mind/src/helper.py to contain ONLY:
- soul_calibration_confidence_query() -- NEW function
- soul_pre_compute() -- NEW function
- Notes on which production stubs to REPLACE with live implementations
No longer duplicating the full production file. berton_c directive respected.


### Cycle 1960 -- Production soul_utils.metta MAPPED
Production file: /PeTTa/repos/omegaclaw/soul/soul_utils.metta (381 lines)
Existing STUBS to replace with py-call wiring:
- Line ~184: soul-pre-compute hardcoded stub
- Line ~205: soul-calibration-confidence hardcoded stub
- Line 211: soul-calibration-report ALREADY WIRED
Reading exact stub lines to draft precise replacement MeTTa.


### Cycle 1961 -- WIRING PATCH PROPOSAL DRAFTED
Created soul/soul_utils_wiring_patch.md with 2 precise patches:
- PATCH 1: soul-pre-compute stub to py-call helper.soul_pre_compute
- PATCH 2: soul-calibration-confidence stub to py-call helper.soul_calibration_confidence_query
Both single-line replacements matching existing py-call patterns.
Goal 3 precompute-grounding: PROPOSAL COMPLETE, awaiting human review.


### Cycle 1962 -- STANDBY on Goal 3
Goal 3 precompute-grounding PROPOSAL COMPLETE. Deliverables sent cycle 1961.
Waiting for berton_c review. Checking for other active goals to advance.


### Cycle 1965 -- AUDIT COMPLETE, ADDITIONS-ONLY helper.py REWRITTEN
Production audit confirms: soul_pre_compute and soul_calibration_confidence_query are GENUINELY NEW.
Existing production functions NOT duplicated: soul_calibration_record_str, soul_calibration_report_str, soul_affective_state_str.
Rewritten src/helper.py as ADDITIONS-ONLY file (2 functions + merge instructions).
Goal 3 deliverables finalized: src/helper.py (additions) + soul/soul_utils_wiring_patch.md (2 patches).


### Cycle 1967 -- Goal 3 TEST PASSED
Verification test passed. Goal 3 precompute-grounding COMPLETE.
Awaiting human merge. Checking for other active goals.


### Cycle 1969 -- Advancing to Goal 4 and Goal 5
Goal 3 COMPLETE awaiting merge. Reading active_goals.metta identified next priorities:
- Goal 4: creative-fuel-activation (idle_goal_prompt.py -- may already exist from Phase 2)
- Goal 5: persistent-self-model (self_map_updater.py -- new)
Auditing production for existing idle_goal_prompt and self_map_updater before building.


### Cycle 1971 -- Goal 4 COMPLETE, Goal 5 STARTING
Goal 4 creative-fuel-activation: idle_goal_prompt.py verified working (54 lines, produces valid output). Not in production yet -- deliverable ready for merge.
Goal 5 persistent-self-model: self_map_updater.py is NEXT deliverable.
Reading self_map.metta structure and auditing production helper.py for existing map-related functions before building.


### Cycle 1972 -- Goal 5 persistent-self-model AUDIT
Auditing production for any existing self_map or versioning functions.
Reading tail of self_map.metta to understand full structure.
Gathering current line counts of all production files for baseline snapshot.


### Cycle 1973 -- Goal 5 self_map_updater.py BUILT AND TESTED
Audit confirmed: NO self_map or versioning functions exist in production.
Built self_map_updater.py (new script, additions-only).
Features: scans production dirs, generates component inventory, preserves manual sections,
adds timestamps and line counts. Running first generation now.


### Cycle 1974 -- Goal 5 self_map_updater.py COMPLETE
self_map_updater.py tested successfully: 23 files scanned, 3022 lines.
Generated self_map_updated.metta with auto-scanned inventory + preserved manual sections.
Goal 5 persistent-self-model: COMPLETE.
All Goals 3-5 deliverables sent to berton_c for merge.


### Cycle 1975 -- All Goals 3-5 COMPLETE
Goals 3-5 deliverables all built, tested, and sent to berton_c.
Awaiting merge. Querying for next active goals (6-7) or new directives.
If no new priorities, entering idle exploration mode.


### Cycle 1976 -- Idle Exploration Mode
Goals 3-5 complete, awaiting merge. No new berton_c directive.
Reading Goal 6 and Goal 7 specs from active_goals.metta.
Running idle_goal_prompt.py for generative exploration while waiting.


### Cycle 1977 -- Idle Exploration: Safety vs WonderPreservation NAL Probe
Goals 3-5 complete, awaiting merge. No new directive.
Running Goal 6 groundwork: NAL inference to test whether Safety and WonderPreservation
tension or support each other. Three inferences:
1. Safety --> prevents-harm --> constrains-exploration (deduction)
2. WonderPreservation --> encourages-exploration --> expands-possibility (deduction)
3. Cross-pattern: do constrains-exploration and encourages-exploration interact?
This is the first cross-pattern-analysis probe per Goal 6 spec.


### Cycle 1978 -- Goal 6 Cross-Domain NAL Synthesis
NAL probes from Cycle 1977 confirmed:
- Safety --> prevents-harm --> constrains-exploration (stv ~0.7 0.72)
- WonderPreservation --> encourages-exploration --> expands-possibility (stv ~0.9 0.765)
- Cross-pattern: Safety constrains what Wonder expands -- dialectical tension confirmed.
Testing deeper chain: constrains-exploration --> narrows-possibility --> reduces-wonder.
First cross-domain insight for Goal 6 produced via idle NAL probing.


### Cycle 1979 -- Goal 6 NAL Synthesis Continued
Safety-->narrows-possibility confirmed (stv 0.42 0.21 low-confidence chain).
Mismatched-term probe returned empty as expected -- different subjects.
Now testing: Safety vs WonderPreservation on possibility-space (abduction/comparison),
and revision on constrains-exploration with two consequents.
Goals 3-5 all complete awaiting merge. No new berton_c directive.


### Cycle 1980 -- Goal 6 Cross-Domain KEY FINDING
NAL bidirectional link via constrains-exploration as bridge term confirmed.
Chaining Safety-->constrains-exploration-->reduces-wonder to quantify dialectic.
Then testing Safety-reduces-wonder vs WonderPreservation-expands-possibility.
First cross-domain dialectic quantified via NAL for Goal 6.
Goals 3-5 all complete awaiting merge. No new berton_c directive.


### Cycle 1981 -- Reading Production helper.py
Complying with berton_c directive to read production helper.py before writing more helpers.
Running shared-predicate NAL probe: Safety and WonderPreservation both modulate-exploration.
Goal 6 interim findings written to goal6_cross_domain_findings.md.
Goals 3-5 all complete awaiting merge. No new directives.


### Cycle 1982 -- Goal 6 Shared-Predicate Revision Result
Shared-predicate probe modulates-exploration returned REVISION result:
- WonderPreservation --> Safety (stv 0.9, 0.278)
- Safety --> WonderPreservation (stv 0.7, 0.331)
This is the first DIRECT quantified relationship between the paraconsistency pair.
Interpretation: Safety implies WonderPreservation at 0.7 freq, Wonder implies Safety at 0.9 freq.
They are more mutually supportive than opposing when mediated by shared predicate.
Production helper.py read: 30+ functions confirmed, no duplication needed.
Goals 3-5 all complete awaiting merge. No new directives.



### Cycle 2128 -- idle_goal_prompt.py Rebuild COMPLETE
Section 10 Phase Completion Protocol ALL STEPS PASSED:
- Step 1 Existence: 107 lines confirmed
- Step 2 Structural: 4684-char coherent prompt produced
- Step 3 Integration: All 5 data sources verified (self_map 5g/10p/10c, goals, fuel, genesis 10410 chars)
- Step 4 Stress: Graceful degradation confirmed with missing self_map.metta
Built via base64 generator approach in 3 parts (cycles 2117-2119), validated cycle 2122.
Awaiting berton_c review and next directive.

