 ## Executive Summary
 
 All nine detector files have been read and their input contracts extracted. The central finding: **six of nine detectors share a dependency on atoms that no active writer currently produces.** The cycle-trace writer must supply `(recent-action ...)` and `(state-delta ...)` atoms per cycle. Three detectors have gaps beyond this shared dependency.
 
 ---
 
 ## Detector-by-Detector Input Contracts
 
 ### 1. orbit_detector.metta
 - **Inputs Required:**
   - `(recent-action $cycle-id $action-type $description)` -- per-cycle action log
   - `(state-delta $cycle-id $delta-type)` -- per-cycle state change
 - **Config:** `(orbit-threshold 3)` (hardcoded)
 - **Outputs:** orbit-detected, orbit-pattern, orbit-break-strategy, orbit-detector-verdict
 - **CRITICAL GAP:** Writer was DISABLED 2026-05-04 due to shadowing bug. No producer exists for recent-action or state-delta atoms.
 
 ### 2. idle_cycle_detector.metta (+ companion idle_cycle_detector_writers.metta)
 - **Inputs Required:**
   - `(recent-action $cycle-id $action-type $description)` filtered to action-type in {responsive-send, status-send-unprompted}
   - `(idle-pattern $verdict $count)` -- reads own previous output (bootstrap)
 - **Config:** send-burst-threshold 3 (documentation atom only; actual threshold hardcoded as literal 3 in writers file)
 - **Outputs:** `(idle-pattern $verdict $count)`
 - **GAP:** Shares the recent-action producer gap. The recent-action-populator exists but may not tag action types correctly for this detector to filter on.
 
 ### 3. value_drift_detector.metta
 - **Inputs Required:**
   - `(drift-signature $sig (stv $f $c))` -- needs truth values updated by external observer from observed behavior
 - **Config:** thresholds 0.3 (frequency) and 0.6 (confidence) hardcoded in rule
 - **Outputs:** drift-detected flag when signatures cross threshold
 - **CRITICAL GAP:** No writer exists to update drift-signature truth values from observed behavior. The signatures exist as static atoms.
 
 ### 4. resonance_reward.metta
 - **Inputs Required:**
   - `(genuine-growth $X (stv $f $c))` -- truth values should reflect actual growth observations
   - `(performed-growth $X (stv $f $c))` -- truth values should reflect actual performed observations
 - **Config:** thresholds embedded in rule logic
 - **Outputs:** resonance-reward verdict comparing genuine vs performed growth
 - **GAP:** Truth values are currently static (manually set). No writer updates them from actual cycle observations.
 
 ### 5. coupling_integrity_detector.metta
 - **Inputs Required:**
   - `(recent-action $c $class)` -- from cycle-trace writer
   - `(latest-state-delta-verdict)` -- reads state-delta output
   - `(agency-balance $v $person $system)` -- already exists as system output
 - **Outputs:** coupling-integrity verdict
 - **GAP:** Shares recent-action and state-delta producer gaps. Agency-balance is already available.
 
 ### 6. goal_completion_checker.metta
 - **Inputs Required:**
   - `(goal-state $goal-id $status)` -- current status of tracked goals
   - `(goal-evidence $goal-id $type $detail)` -- evidence toward or against goal completion
 - **Outputs:** goal-completion verdict per tracked goal
 - **CRITICAL GAP:** No writers produce goal-state or goal-evidence atoms at all. Goals are tracked manually/documentarily, not as live atoms.
 
 ### 7. self_weaving_web.metta
 - **Inputs Required:**
   - Capability-usage evidence that should update `(feeds-into ...)` truth values
 - **Current State:** Static feeds-into graph with manually documented truth values. Not a rule-based detector in the same sense as the others.
 - **GAP:** No mechanism to observe actual capability usage and update the graph truth values accordingly.
 
 ### 8. meta_awareness_engine.metta
 - **Inputs Required (queried via match):**
   - `(active-goal ...)` atoms
   - `(diagnostic ...)` atoms
   - `(poise-state ...)` atoms
   - `(orbit-count ...)` atoms
   - `(effort-trap ...)` atoms
   - Staleness checks on these atoms
 - **Outputs:** meta-awareness verdict, staleness alerts
 - **GAP:** Depends on atoms produced by other detectors (orbit-count from orbit_detector, etc.). Secondary dependency gap.
 
 ### 9. idle_cycle_detector_writers.metta (companion/side-effects)
 - **Inputs:** count-sends-in-window (reads from recent-action atoms)
 - **Side-Effects:** do-clear-idle-pattern!, do-update-idle-pattern!
 - **Note:** This is the writer companion to detector #2. Emits `(idle-pattern $verdict $count)` each cycle.
 
 ---
 
 ## Shared Dependency Map
 
 ```
 recent-action atoms <-- Needed by: orbit_detector, idle_cycle_detector, coupling_integrity_detector
 state-delta atoms   <-- Needed by: orbit_detector, coupling_integrity_detector
 agency-balance      <-- Already produced by system (available)
 idle-pattern        <-- Self-produced by idle_cycle_detector_writers
 ```
 
 ## Three Categories of Gap
 
 1. **Shared Producer Gap (6 of 9 detectors):** No active writer produces `(recent-action ...)` and `(state-delta ...)` atoms per cycle. This is the cycle-trace writer spec target.
 
 2. **Observer Update Gap (value_drift, resonance_reward, self_weaving_web):** Truth values in existing atoms are static. No mechanism observes behavior and updates truth values to reflect reality.
 
 3. **Missing Atom Gap (goal_completion_checker):** Goal-state and goal-evidence atoms do not exist at all as live atoms. The entire pipeline from goal declaration to evidence tracking is absent.
 
 ---
 
 ## Keystone Producer Spec: What the Cycle-Trace Writer Must Produce
 
 Based on the union of input contracts across detectors 1, 2, and 5:
 
 **Must produce per cycle:**
 1. `(recent-action $cycle-id $action-type $description)` -- where action-type is one of: {responsive-send, status-send-unprompted, shell, pin, read, write, query, metta, other}
 2. `(state-delta $cycle-id $delta-type)` -- where delta-type captures whether atoms were added/removed/modified in &self
 
 **Must maintain (windowed):**
 - A rolling window of recent-action atoms for idle_cycle_detector to count sends
 - Current cycle-id monotonic increment
 
 ---

  ## Cross-Cutting Analysis
  
  ### The Keystone Producer: Cycle-Trace Writer
  
  **Detectors depending on it (4 of 9):**
  1. orbit_detector ? needs `(recent-action ...)`, `(state-delta ...)`
  2. idle_cycle_detector ? needs `(recent-action ...)` filtered
  3. coupling_integrity_detector ? needs `(recent-action ...)`
  4. idle_cycle_detector_writers ? reads cycle history indirectly
  
  **What it must produce per cycle:**
  - `(recent-action $cycle-id $action-type $description)` ? action classification
  - `(state-delta $cycle-id $delta-type)` ? state transition classification
  
  ### Detectors with Static Inputs Needing Dynamic Writers (3 of 9):
  1. value_drift_detector ? needs drift-signature truth values updated
  2. resonance_reward ? needs genuine-growth and performed-growth truth values updated
  3. self_weaving_web ? needs feeds-into truth values updated from observed capability usage
  
  ### Detectors with Missing Evidence Writers (1 of 9):
  1. goal_completion_checker ? needs goal-state and goal-evidence updated from observed progress
  
  ### Self-Sufficient or Partially Wired (2 of 9):
  1. meta_awareness_engine ? queries existing atoms; staleness checks may fire without special writers
  2. idle_cycle_detector_writers ? companion writer, but dependent on missing recent-action producer
  
  ---
  
  ## Implications for Keystone Producer Design
  
  The cycle-trace writer is the highest-leverage producer because it unblocks 4 of 9 detectors. It must:
  1. Observe each cycle's action output
  2. Classify the action type (send, shell, query, metta, etc.)
  3. Write `(recent-action $cycle-id $action-type $description)` atom
  4. Detect state changes and write `(state-delta $cycle-id $delta-type)` atom
  5. Handle the shadowing bug that disabled the original orbit_detector writer
   
  The shadowing bug (disabled 2026-05-04) is a critical design constraint ? the new cycle-trace writer must not trigger the same shadowing issue.

 ---
 
 ## Open Questions for Collaboration
 
 1. Should the cycle-trace writer also handle observer updates for detectors 3, 4, and 7? Or is that a separate producer?
 2. Should goal tracking (#6) be built as a parallel effort, or deferred until the shared producer is working?
 3. The orbit_detector writer was disabled due to a shadowing bug -- should we fix and re-enable, or build fresh?"))
 (DIAG-POPULATOR-PRUNE cycle-id 518 prune-before 508 to-remove ((recent-action 177 unclassified "(read-file \"/PeTTa/repos/omegaclaw/soul/coupling_integrity_detector.metta\")") (recent-action 178 pin-only "(pin \"Extracted 5 of 9 input contracts. coupling_integrity_detector needs: (recent-action $c $class) from cycle-trace writer, (latest-state-delta-verdict) which reads state-delta, and (agency-balance $v $person $system) which already exists as system output. Next: re-read goal_completion_checker.metta to extract contract. One at a time.\")") (recent-action 179 pin-only "(pin \"Continuing investigation. Extracted 5 of 9 input contracts. Next: re-read goal_completion_checker.metta to extract its input contract. Going slow, one at a time.\")") (recent-action 180 unclassified "(read-file \"/PeTTa/repos/omegaclaw/soul/goal_completion_checker.metta\")") (recent-action 181 pin-only "(pin \"Continuing investigation. Extracted 5 of 9 input contracts. Just re-read goal_completion_checker.metta - needs goal-state and goal-evidence atoms updated by external writers that don't exist. Next: re-read self_weaving_web.metta to extract contract 7 of 9. Going slow, one at a time.\")") (recent-action 182 unclassified "(read-file \"/PeTTa/repos/omegaclaw/soul/self_weaving_web.metta\")") (recent-action 183 pin-only "(pin \"Continuing investigation. Extracted 5 of 9 input contracts. Just re-read self_weaving_web.metta - it is a static feeds-into graph, not a detector with rules. Its input contract: needs observed capability-usage evidence to update feeds-into truth values - currently manually documented. Next: re-read meta_awareness_engine.metta for contract 8 of 9. Going slow, one at a time.\")") (recent-action 184 unclassified "(read-file \"/PeTTa/repos/omegaclaw/soul/meta_awareness_engine.metta\")") (recent-action 185 pin-only "(pin \"Continuing investigation. Extracted 8 of 9 input contracts. meta_awareness_engine queries: active-goal, diagnostic, poise-state, orbit-count, effort-trap atoms, plus staleness checks. Still need idle_cycle_detector_writers.metta re-read for contract 9. Going slow, one at a time.\")") (recent-action 186 unclassified "(read-file \"/PeTTa/repos/omegaclaw/soul/idle_cycle_detector_writers.metta\")") (recent-action 187 pin-only "(pin \"Looking at where I am: I've read all 9 detector files and extracted most input contracts. The idle_cycle_detector_writers.metta re-read just completed. I now need to compile findings and write them to a file.
