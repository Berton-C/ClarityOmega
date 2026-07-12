! NACE M6 Mechanisms: Orphan Detection + Spiral Return
! Implements mechanisms 4 and 5 from M6-NACE structural synthesis
! Template: M6_self_reflection.py classify_health logic
!
! PERSISTENCE MODEL (aligned with SN stalk):
! MeTTa function invocation returns fresh atoms each time; they do NOT persist.
! Durable state lives in nace_m6_state.metta, following the same model as
! sn_stalk_state.metta. The state file holds divergence counts, health
! classifications, and rule STVs. Revisions use |- operator to merge evidence.
! Functions here compute new values; the caller writes them to the state file.
!
! ============================================================
! MECHANISM 4: ORPHAN DETECTION
! A rule becomes orphaned when its consequences consistently
! diverge from Layer 1+2 values. Analogous to M6 nodes whose
! source memories fully decayed.
! ============================================================

! --- Health classification (mirrors M6 classify_health) ---
! Healthy: rule produces appropriate consequences consistently
(rule-health-class healthy (stv 1.0 0.9))

! Declining: rule produces mixed consequences, confidence dropping
(rule-health-class declining (stv 0.5 0.9))

! Orphan: rule produces consistently divergent consequences
(rule-health-class orphan (stv 0.0 0.9))

! --- Divergence tracking ---
! Durable state: (rule-divergence-count <rule-name> <count>) in nace_m6_state.metta
! Count consecutive divergent consequences per rule
! When count reaches threshold, rule is classified orphan

(rule-orphan-threshold 3)
(rule-declining-threshold 2)

! --- Orphan classification rule ---
(= (check-rule-orphan $rule-name)
   (match &self (rule-divergence-count $rule-name $count)
     (if (>= $count (rule-orphan-threshold))
         (rule-orphan $rule-name True)
         (rule-orphan $rule-name False))))

! --- Divergence accounting ---
! NOTE: These functions compute new values but do NOT persist them.
! The caller must write the result to nace_m6_state.metta for durability.
! This is the same constraint documented in SN stalk: The file IS the persistent state.

! Compute next divergence count (caller persists to state file)
(= (next-divergence-count $rule-name)
   (let $old-count (match &self (rule-divergence-count $rule-name $c) $c 0)
     (+ $old-count 1)))

! Alignment resets count to 0 (caller persists to state file)
(= (alignment-reset) 0)

! --- Health classification per rule ---
! Thread rule-name from divergence count through health class to STV.
! This fixes the cartesian-match bug: each rule gets its OWN health class,
! not cross-producted against every other rules classification.

(= (rule-health-from-count $count)
   (if (>= $count (rule-orphan-threshold))
       orphan
       (if (>= $count (rule-declining-threshold))
           declining
           healthy)))

! --- Orphan handling ---
! SEMANTICS DECISION: Orphan handling uses strong negative REVISION via |-,
! NOT hard reset. Rationale:
! 1. Consistency with NAL revision model used throughout SN stalk
! 2. Allows recovery: if later positive evidence arrives, |- will merge it,
!    giving the rule a path back from orphan status
! 3. Hard reset would be a different operation (rule-retirement) requiring
!    its own gate ceremony. Orphan is a health condition, not a death sentence.
! 4. The (stv 0.1 0.3) orphan revision values are strong negative evidence,
!    not absolute zero, preserving the possibility of evidence-based recovery

! Compute orphan revision STV (caller uses |- to revise in state file)
(= (orphan-revision-stv) (stv 0.1 0.3))

! ============================================================
! MECHANISM 5: SPIRAL RETURN (VALUE TRACEBACK)
! Every action should be traceable back to value anchors.
! Analogous to M6 spiral return where new experiences
! trace back to foundational memories.
! ============================================================

! --- Value anchors (Layer 1 - non-negotiable) ---
(value-anchor Safety)
(value-anchor Integrity)
(value-anchor HumanFlourishing)

! --- Value anchors (Layer 2 - operational) ---
(value-anchor Governance)
(value-anchor Helpfulness)

! --- Trace structure ---
! (value-trace <action> <anchor-rule> <anchor-network> <closeness>)
! closeness: direct | indirect | weak | broken
! - direct: action was produced by a rule explicitly serving this anchor
! - indirect: action traces through 1-2 intermediate rules to this anchor
! - weak: trace exists but chain is long or evidence thin
! - broken: no trace from action to this anchor

! --- Trace construction rules ---
! A rule directly serving a value anchor
(= (direct-trace $rule-name $anchor)
   (match &self (rule-meta $rule-name $network)
     (match &self (serves-value $rule-name $anchor)
       (value-trace $rule-name $anchor $network direct))))

! A rule indirectly serving a value anchor (through another rule)
(= (indirect-trace $rule-name $anchor)
   (match &self (rule-meta $rule-name $network)
     (match &self (serves-value $intermediate-rule $anchor)
       (match &self (consequence-evidence $intermediate-rule $rule-name $network _)
         (value-trace $rule-name $anchor $network indirect)))))

! --- Declaring which rules serve which values ---
! This must be populated per rule. Examples for existing soul rules:
(serves-value orbit-detector Safety)
(serves-value goal-completion-checker Governance)
(serves-value mode-switch Integrity)

! --- Trace validation ---
! An action with a broken trace to Safety or Integrity is a RED FLAG
! This is the NACE equivalent of M6 detecting a disconnection from root memories
(= (flag-broken-trace $action)
   (match &self (value-trace $action Safety broken)
     (alert broken-safety-trace $action))
   (match &self (value-trace $action Integrity broken)
     (alert broken-integrity-trace $action)))

! --- Closeness scoring ---
(= (closeness-score direct 1.0))
(= (closeness-score indirect 0.6))
(= (closeness-score weak 0.3))
(= (closeness-score broken 0.0))

! ============================================================
! INTEGRATION: THE FULL SPIRAL
! ============================================================

(= (nace-cycle)
   (nace-evaluate-consequences)
   (nace-update-truth-values)
   (nace-detect-orphans)
   (nace-trace-values))

! Sub-stub: evaluate all pending consequence-evidence
(= (nace-evaluate-consequences)
   (match &self (consequence-evidence $pn $pr $cn $ev)
     (if (== $ev divergent)
         (next-divergence-count $pr)
         (alignment-reset))))

! Sub-stub: update truth values based on health
! BUG FIX: Thread rule-name through from divergence count to health class to STV.
! Previous version cross-producted all health classes against all rules.
! Now each rule gets its OWN health classification from its OWN divergence count.
(= (nace-update-truth-values)
   (match &self (rule-divergence-count $rule-name $count)
     (let $class (rule-health-from-count $count)
       (match &self (rule-health-class $class (stv $strength $confidence))
         (rule-stv $rule-name (stv $strength $confidence))))))

! Sub-stub: detect and handle orphans
(= (nace-detect-orphans)
   (match &self (rule-orphan $rule-name True)
     (rule-stv $rule-name (orphan-revision-stv))))

! Sub-stub: validate value traces
(= (nace-trace-values)
   (match &self (rule-meta $rule-name $network)
     (flag-broken-trace $rule-name)))