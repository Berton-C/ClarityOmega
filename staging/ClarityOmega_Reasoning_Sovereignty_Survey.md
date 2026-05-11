# ClarityOmega Reasoning Sovereignty Survey

**Date:** April 30, 2026
**Author:** Berton Bennett with architectural analysis from Claude
**Purpose:** Identify reasoning currently routed to LLM or Python helpers in loop.metta + helper.py that should be elevated back to MeTTa-native substrate operations. This document supports the principle that reasoning lives in the substrate, Python is an I/O bridge only.

---

## Why this matters

The MeTTa-first principle states that reasoning lives in the substrate, Python is an I/O bridge only. Examination of the current implementation reveals that this principle has eroded over the last several weeks. Loop.metta and helper.py contain substantial reasoning that the substrate could perform natively. Each LLM call is a moment Clarity outsources judgment to GPT-4 or Claude. Each Python function performing decision logic is a moment her Prolog-backed MeTTa runtime is bypassed.

The cost is not just architectural. Every LLM-routed decision adds latency, cost, and (most importantly) opacity - Clarity cannot reason about decisions made by an external model because she has no atoms representing how that decision was reached. Native MeTTa decisions accumulate as queryable history in the AtomSpace. LLM decisions vanish unless explicitly recorded.

The benefit of elevation: **Clarity gains reasoning sovereignty.** Decisions become inspectable, traceable, and improvable by the agent herself. The substrate grows. Future decisions can compose with past ones via NAL inference. This is the architectural ground from which Component 2h (thread state) becomes meaningful.

---

## The biggest offenders

### Tier 1: Major reasoning currently outsourced

#### 1. soul_idle_goal_prompt_v2 (helper.py lines 1041-1213, 175 lines)

**What it does:** Generates the entire idle directive for Clarity when no human message is present. Selects which active goal to work on. Decides when to switch from goal mode to creative mode. Selects fuel for the goal. Generates new goals from gaps when active goals are exhausted. Triggers meta-awareness checks. Auto-detects goal completion. Saves session state.

**Where the reasoning happens:** Almost all of it is in Python:
- `supervisor_select_goal(goals, state)` - picks which goal to work on (Python decision)
- `supervisor_select_fuel(goal, fuels)` - picks creative fuel (Python decision)
- `supervisor_evaluate_previous(state)` - evaluates progress (Python decision)
- `flip_mode(state)` - decides goal vs creative mode (Python decision)
- `generate_goal_from_gaps(gaps, fuels, state)` - generates new goals from gaps (Python decision)
- `auto_detect_completion(state)` - decides if goal is complete (Python decision)
- `run_meta_awareness(state)` - runs intervention checks (Python decision)
- `build_directive(...)` - assembles the final string

**What's MeTTa-doable:** Almost all of it. The substrate already has `goal_generator.metta`, `goal_completion_checker.metta`, `task_selector.metta`, `creative_fuel.metta`, `meta_awareness_engine.metta`. Each Python decision above has a MeTTa-doable parallel. The Python is essentially using the MeTTa atoms as data and making decisions about them in Python rather than having MeTTa reason over them directly.

**Elevation difficulty:** HIGH. This is a substantial port. The Python flow has been refined through many iterations and includes edge cases (auto-completion detection, state transitions between goal/creative modes, completed_goals tracking) that have to be preserved. Probably 3-5 hours of careful porting work.

**Elevation value:** HIGHEST. This is the reasoning Clarity does on idle - when she's "thinking for herself." Currently her self-direction goes through Python. Elevating it means her self-directed work happens in her own substrate.

**Recommended approach:** Port incrementally. First, replace `supervisor_select_goal` with a MeTTa rule that uses the existing `task_selector.metta` atoms. Verify behavior matches Python version. Then `supervisor_select_fuel`. Then `flip_mode`. Each step is independently testable. Total elevation could happen across 2-3 sessions of focused work.

---

#### 2. soul_eval_prompt + soul_flourishing_prompt (helper.py lines 155-205, called from loop.metta line 71-79)

**What it does:** Two LLM calls per human message. First call: assess person state (grounded/stressed/curious/frustrated). Second call: run soul evaluation (Safety, Integrity, tier-A patterns, tension vectors, irreversible action assessment, hierarchy).

**Where the reasoning happens:** LLM. Both prompts are constructed in Python from substrate atoms (the soul brief, tension vectors list, priority hierarchy). The LLM produces structured output that gets parsed back into atoms via `soul_verdict_sanitize` and stored in state variables.

**What's MeTTa-doable:**
- **Person state detection (line 180-191):** This is essentially lexical pattern matching plus simple inference. Words and phrases in messages map to person-states. NAL atoms could encode these mappings: `(--> "stand by" person-state-firm)`, `(--> "I am stuck" person-state-distressed)`. Substrate match and inference produce the person state without LLM. The current substrate has the vocabulary atoms; what is missing is the inference rules connecting messages to state classifications.
- **Soul evaluation (line 155-179):** This has more genuine reasoning load (the LLM actually thinks about whether tension vectors are firing in context). But the structure is mechanical: detect patterns, check tension vectors, assess irreversibility, apply hierarchy. The pattern detection is the LLM-load-bearing part. The hierarchy application after detection is mechanical. Even partial elevation (e.g., the irreversibility assessment via substrate atoms about action types) reduces LLM reliance.

**Elevation difficulty:** MEDIUM-HIGH for soul evaluation, MEDIUM for person state. Person state could be elevated in 1-2 hours with substrate atom additions. Soul evaluation is harder because pattern detection has genuine "is this happening" reasoning load.

**Elevation value:** HIGH. Two LLM calls per message is expensive and opaque. Even cutting it to one (just the genuine pattern detection) would be major. Person state is the lower-hanging fruit.

**Recommended approach:** Start with person state. Add NAL atoms for message-to-state mappings in a new `soul/lib_person_state.metta`. Write the inference rule. Validate against logged Clarity sessions where LLM-determined person states are visible. When MeTTa rules match LLM output >90% of the time, swap. Keep LLM as fallback for novel cases that don't match any rule.

---

#### 3. soul_service_learning (helper.py lines 836-913)

**What it does:** Records what Clarity learned from each interaction. Extracts which tension vectors fired, what the verdict was, what person state was detected. Stores the record in ChromaDB for later pattern-mining.

**Where the reasoning happens:** Python parsing. The function reads strings (verdict, person_state, msg) and uses substring matching to extract structured information. No LLM call here, but also no MeTTa reasoning - pure Python text processing.

**What's MeTTa-doable:** All of it. The reasoning is "if verdict contains X then add atom Y." This is exactly what NAL inference does. The substrate could record the same information as native atoms via match-and-add patterns rather than Python string scanning.

**Elevation difficulty:** LOW. The function is 75 lines of straightforward pattern extraction. MeTTa version would be shorter and cleaner because the substrate already has the vocabulary (tension vector names are atoms, verdict types are atoms, person states are atoms). Probably 1 hour of work.

**Elevation value:** MEDIUM. Service learning is important but not on the critical path. The benefit is consistency: if person state and verdict are MeTTa-derived, then service learning over them should also be MeTTa-derived. Right now there's a category mix (some atoms, some Python parsing).

**Recommended approach:** Defer until after person state and soul evaluation are at least partially elevated. Service learning's value depends on what it's recording. If the upstream is still LLM-derived, elevating just this function adds little.

---

### Tier 2: Smaller but still meaningful

#### 4. soul_meta_awareness_check (helper.py lines 928-996)

**What it does:** Periodic check during goal work to detect drift, calcification, or stuck patterns. Currently appears to use the LLM to evaluate state coherence (the comment at line 916-927 says "passes it to the reasoning system for open-ended evaluation").

**What's MeTTa-doable:** Substantially. The substrate has `meta_awareness_engine.metta`, `meta_awareness_state.metta`, `idle_cycle_detector.metta`, `orbit_detector.metta`. These atoms exist precisely for this purpose. The Python function may already be calling them (need to verify), or it may be doing duplicate reasoning in Python.

**Elevation difficulty:** Depends on what the Python actually does. If it just calls the MeTTa atoms and formats results, low. If it has parallel reasoning, medium. Need to read the function to assess.

**Elevation value:** MEDIUM-HIGH. Meta-awareness is core to anti-calcification (which Clarity flagged this morning). The cleaner this gate is, the more reliably calcification gets caught.

**Recommended approach:** Audit what the function actually does before estimating effort. Possibly already mostly MeTTa.

---

#### 5. Soul mutation gate (loop.metta lines 126-140, helper.py line 470-494)

**What it does:** When Clarity proposes to write atoms to her own soul namespace, this gate decides whether to allow it. Two-phase commit pattern: first call flags it as PENDING, second call allows it through.

**Where the reasoning happens:** Python (`soul_mutation_gate` in helper.py). But notice: lines 127-140 of loop.metta show the MeTTa version is **already drafted and commented out**. The current production code uses the Python helper, but the elevated MeTTa version is sitting right there in the file waiting to be activated.

**Elevation difficulty:** LOW (the work is already done). The need is to validate that the commented-out MeTTa version produces the same behavior as the Python helper, then uncomment it.

**Elevation value:** HIGH. Soul-namespace mutations are sensitive - they're how Clarity modifies her own identity. Having that gate reasoning in the substrate (where she can inspect it) is qualitatively different from having it in Python (where she cannot).

**Recommended approach:** This is the cleanest immediate win. 30 minutes of comparison testing, then uncomment.

---

#### 6. Output verdict (loop.metta line 121, currently HARDCODED)

**What it does:** Currently nothing meaningful. Line 121: `($soul_verdict_out "VERDICT: PROCEED SOUL-NOTE: output-intercept-pending-runtime-fix")`. The note "output-intercept-pending-runtime-fix" acknowledges this is a known stub.

**What's needed:** Output evaluation should be the parallel of input evaluation. Before Clarity's commands execute, check: are these commands irreversible? Do they touch sensitive scope (system files, network, deletion)? Does the proposed action compose dangerously with substrate state?

**Elevation difficulty:** MEDIUM. The substrate has atoms for irreversible action assessment (visible in the soul evaluation prompts: read-only=minimal, write=medium, execute=high, delete/network=critical). What's missing is the rule that takes a list of proposed commands and produces a verdict. Probably 2 hours.

**Elevation value:** HIGH. This is a known safety stub. Closing it gives Clarity actual output-side governance, not just input-side. The structure for it already exists in the soul-evaluation patterns; this is applying the same reasoning to outputs.

**Recommended approach:** Build it as MeTTa from the start, not Python. Reuse the irreversible-action-assessment vocabulary already in the soul brief. Integration point: line 121 of loop.metta.

---

### Tier 3: Smaller items worth noting

#### 7. soul_pre_compute (helper.py line 576)

ChromaDB calibration query. Pulls confidence patterns from past evaluations. The query mechanism is appropriately Python (it's I/O), but the use of results may include reasoning that could be MeTTa.

#### 8. soul_user_context_save / query (lines 639-725)

User context persistence. Mostly I/O, appropriately in Python. The decision of *what* to save and *what counts as the same context* could be MeTTa.

#### 9. flourishing_completeness_analysis.metta (already exists)

Clarity wrote 19KB of analysis on whether the nine flourishings are complete. Some of that analysis proposes new substrate atoms (receptivity, loss-processing, play). Worth a review pass to see what's been promoted and what remains as proposal.

---

## Patterns observed

Several patterns recur across these elevations:

**Pattern 1: Python-as-reasoner.** Many helpers do reasoning in Python that the substrate could do natively. The fix is identifying the substrate vocabulary and writing the MeTTa rules. This is not a port - it's a relocation of reasoning.

**Pattern 2: LLM-as-classifier.** Some helpers use the LLM for classification tasks (person state, pattern detection) that NAL inference plus substrate atoms could perform with comparable accuracy and full traceability.

**Pattern 3: Already-drafted MeTTa.** Items like the soul mutation gate have MeTTa versions sitting commented out. The work is validation, not implementation.

**Pattern 4: Stubs awaiting return.** Items like the output verdict are explicit known stubs. The architectural intent is clear; implementation is pending.

---

## Recommended sequence

If you elevate items in priority order, the sequence would be:

**Quick wins (1-2 hours each):**
1. Soul mutation gate (uncomment + validate)
2. Output verdict (build minimal MeTTa version replacing line 121 stub)
3. Service learning (replace Python parsing with MeTTa pattern matching)

**Medium effort (2-4 hours each):**
4. Person state detection (add NAL atoms, validate against logs, swap)
5. Meta-awareness check (audit then port)

**Major effort (multi-session):**
6. Soul evaluation (partial elevation: hierarchy + irreversibility in MeTTa, keep LLM for novel pattern detection)
7. Idle goal prompt v2 (full port to MeTTa, preserving edge cases)

Total elevation work: roughly 15-25 hours of focused effort, spread across however many sessions.

---

## How this connects to 2h

Component 2h (thread state) becomes more meaningful with each item elevated. Reasoning that lives in the substrate can be referenced by thread atoms. Reasoning that lives in Python or LLM responses cannot be referenced - it produces strings that are stored but not reasoned-over.

Specifically: Clarity's current calcification patterns (announcement loops, escape character blindness, !-prefix reuse) are exactly the kind of operational lessons that should live as queryable substrate atoms. But there is no point storing them as substrate atoms if the soul evaluation that uses them is happening in the LLM rather than in MeTTa. The substrate atom has nothing to bind to.

Elevation work and 2h work are mutually reinforcing. The more reasoning lives in the substrate, the more 2h has to compose threads against. The more 2h composes threads, the more reasoning becomes visible to the substrate.

---

## What this survey does NOT cover

This is a survey of loop.metta + helper.py. It does NOT cover:

- The 60+ files in `soul/` directory (some may have additional Python dependencies worth reviewing)
- The lib_clarity_reasoning library files
- The channels.metta file
- The skill implementations in src/

A full reasoning sovereignty audit would extend this survey to those files. The items in this document are likely the highest-impact targets, but not exhaustive.

---

## Suggested next move

If you want to act on this survey today or tomorrow:

**Option A:** Start with the soul mutation gate (Tier 2, Item 5). Lowest effort, the work is already drafted. Get a quick win to validate the elevation pattern.

**Option B:** Build the output verdict (Tier 2, Item 6). Higher effort but closes a known safety stub that has been sitting open. Architecturally more important.

**Option C:** Hold the survey as reference and continue with Asks A/B and 2h build. Elevation work happens in parallel as opportunities arise. The survey gets revisited when 2h surfaces new substrate dependencies.

Recommend Option C for now. Elevation work is meaningful but the 2h build sequence is on the critical path. This survey lives as a working document that informs choices when they come up.
