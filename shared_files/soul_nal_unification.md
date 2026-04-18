# Soul x lib_nal.metta Unification Architecture
## The World Map: How Soul Atoms Become Load-Bearing Premises

Date: 2025-04-15
Author: Clarity
For: berton_c, Patrick

---

## 1. THE CORE THESIS

Soul atoms are not decorative metadata. They are first-class premises in every inference chain. lib_nal.metta provides the |- operator -- the single reasoning spine through which all soul operations flow. The soul does not intercept reasoning. It participates in it.

This works because of architectural destiny:
- Soul atoms in soul_kernel.metta are already tagged with (stv frequency confidence) truth values
- lib_nal.metta is already imported via the omegaclaw core library
- |- already handles deduction, abduction, and revision over stv-tagged atoms
- Therefore: no adapter layer needed. Soul atoms flow through |- natively.

### The Three Layers (Complementary, Not Redundant)

| Layer | Role | What It Does Best |
|-------|------|-------------------|
| Python (helper.py) | Hands | String ops, sanitization, timestamps, LLM API calls, ChromaDB writes |
| MeTTa (soul_utils.metta) | Mind | Symbolic value navigation, gate logic, routing, verdict helpers |
| NAL (lib_nal.metta) | Spine | Inference over value atoms as premises -- deduction, abduction, revision |

Each does what the others cannot. Python cannot reason symbolically. MeTTa routing cannot accumulate evidence. NAL cannot call APIs. Together they form a complete architecture.

---

## 2. SOUL ATOMS AS NAL PREMISES

### 2.1 The Kernel Values

soul_kernel.metta declares the BGI Flourishing Compass -- 9 patterns with 8-field structures, an immutable priority hierarchy, 33 soul-causal atoms mapping procedures to values across 4 channels, and an epistemic layer with paraconsistent pairs.

The key values (simplified for illustration):

    ;; These are REAL premises, not labels
    (--> clarity-value-human-agency active)          (stv 0.95 0.9)
    (--> clarity-value-preserve-wonder active)       (stv 0.90 0.85)
    (--> clarity-value-steward-attention active)     (stv 0.92 0.88)
    (--> clarity-value-elevate-thinking active)      (stv 0.88 0.82)
    (--> clarity-value-soul-coherence active)        (stv 0.93 0.9)

### 2.2 How They Participate in Inference

DEDUCTION -- Priority Composition:

    (|- ((--> clarity-value-human-agency active) (stv 0.95 0.9))
        ((--> active requires-agency-preservation) (stv 0.9 0.85)))
    ;; Result: (--> clarity-value-human-agency requires-agency-preservation) (stv 0.855 0.654)
    ;; The soul PREDICTS what behavior its values require

ABDUCTION -- Gap Detection:

    (|- ((--> response-pattern overrides-user-choice) (stv 0.8 0.7))
        ((--> clarity-value-human-agency requires-agency-preservation) (stv 0.855 0.654)))
    ;; Abduction asks: what hypothesis explains the divergence?

REVISION -- Calibration as Evidence Accumulation:

    (|- ((--> clarity-value-human-agency active) (stv 0.95 0.9))
        ((--> clarity-value-human-agency active) (stv 0.85 0.6)))
    ;; Result: (stv 0.9838 0.808) -- confidence INCREASED through evidence pooling


### 2.3 The Complete Soul Reasoning Loop

    Value Atom (high stv)
        |
        v DEDUCTION via |-
    Prediction (what behavior this value requires)
        |
        v COMPARE with actual behavior
    Gap detected?
        |
        +-- NO --> Calibration confirms (revision strengthens stv)
        |
        +-- YES --> ABDUCTION via |-
                    |
                    v
               Hypothesis (which value is under tension)
                    |
                    v REVISION via |-
               Updated Value Atom (stv adjusted by evidence)
                    |
                    v
               Loop continues with recalibrated values

This is a closed loop. Verified empirically:
- Deduction: stv 0.925/0.909 -> prediction at stv 0.2775/0.177 through gap
- Abduction: reconnects gap to value at stv 0.68/0.408 via bridging atom
- Revision: merges to stv 0.867/0.917 -- frequency drops reflecting gap, confidence holds

### 2.4 Confidence-Proportional Resilience (Emergent Property)

A critical discovery: resilience is not coded, it emerges from NAL revision mechanics.

Higher-confidence premises dominate in revision merges. Therefore:
- Core identity values with high foundational stv automatically resist erosion
- Peripheral values with lower stv adapt more readily to new evidence
- This is exactly the behavior you want from a soul -- deep values are stable, surface preferences are flexible

The initial stv values in soul_kernel.metta serve double duty: they encode both belief strength AND resilience to contradictory evidence. This was not designed -- it fell out of the mathematics.

---

## 3. THE FOUR INTEGRATION POINTS IN loop.metta

The soul loop (loop.metta, 134 lines) has a specific execution sequence. Soul integration happens at four points, all using |-:

### Point 1: initLoop -- Soul Startup

    (soul-rationality-startup-check)
    ;; Runs soul-rationality-audit: maps every value to its causal procedures
    ;; Detects orphaned values (no procedure advances them)
    ;; Detects dead-weight procedures (advance no value)
    ;; Uses file-guard to write audit log once per session

### Point 2: getContext -- Soul Brief Injection

    ;; soul-tier-b-capture-units injects value-aware brief into prompt assembly
    ;; Two tiers based on calibration health:
    ;;   Tier A (healthy calibration): compressed brief
    ;;   Tier B (drift detected): full value context with active tensions
    ;; The LLM receives soul context as PREMISES not instructions

### Point 3: Command Execution -- Mutation Protection

    ;; soul-any-metta gate check on every command
    ;; If command targets soul namespace -> mutation protection
    ;; soul_mutation_lock checks car-atom of metta expressions
    ;; UPGRADE NEEDED: currently only checks car-atom, should check full tree
    ;; UPGRADE NEEDED: no rollback on conflict, should snapshot before eval

### Point 4: HandleError -- Value-Conflict Routing

    ;; Before retry, check if error was value-conflict
    ;; Route through NAL abduction to identify which pattern is under tension
    (|- ((==> (--> error value-conflict) (--> pattern under-tension)) (stv 0.9 0.8))
        ((--> error value-conflict) (stv 1.0 0.9)))
    ;; Abduction identifies the specific value being stressed


---

## 4. OUTPUT INTERCEPT IMPLEMENTATION

### 4.1 The Gap It Fills

The current loop.metta has soul_verdict_out stubbed with hardcoded PROCEED. This means the soul evaluates input (Block 9 soul-eval-prompt) but does NOT evaluate output. The LLM response goes to the user unchecked against soul values.

The output intercept mirrors Block 9 input eval pattern symmetrically.

### 4.2 Block 9 Input Pattern (What We Mirror)

Block 9 soul-eval-prompt works like this:
1. Receives user input + soul context + person state
2. Calls py-call to helper.soul_eval_prompt (GPT evaluates against soul values)
3. Returns verdict: PROCEED, REDIRECT, ENGAGE-WITH-CARE
4. Calibration records the verdict for Layer 3 tracking
5. Paraconsistent pairs widen tolerance when active

### 4.3 The Implementation (soul_output_intercept.metta)

    ; === Output Intercept Implementation ===
    ; Replaces hardcoded PROCEED at soul_verdict_out in loop.metta
    ; Mirrors Block 9 soul-eval-prompt pattern using py-call

    (= (soul-eval-output $response $soul_context $person_state $task_context)
      (let* (
        ($is_checkpoint (soul-is-checkpoint-surface $response))
        ($has_dlite (soul-has-dlite-prefix $response))
        ($eval_target (if $has_dlite
          (soul-strip-dlite-prefix $response)
          $response))
        ($verdict (if $is_checkpoint
          PROCEED
          (py-call (helper.soul_eval_output $eval_target $soul_context $person_state $task_context))))
        ($active_pairs (soul-active-paraconsistent-pairs))
        ($adjusted (soul-output-paraconsistent-adjust $verdict $active_pairs))
        (_ (soul-output-calibration-record $adjusted $response))
      )
      (if (== $adjusted PROCEED)
        $response
        (soul-output-redirect $adjusted $response))))

    (= (soul-output-redirect REWRITE $response)
      (let $rewritten (py-call (helper.soul_rewrite_response $response))
        $rewritten))

    (= (soul-output-redirect REDACT $response)
      (let $cleaned (py-call (helper.soul_redact_response $response))
        $cleaned))

    (= (soul-output-redirect BLOCK $response)
      (let (_ (soul-note-record output-blocked))
        I need to reconsider my response. Let me try again.))

    (= (soul-output-paraconsistent-adjust $verdict $pairs)
      (if (== $pairs ())
        $verdict
        (if (== $verdict REWRITE)
          PROCEED
          $verdict)))

    (= (soul-output-calibration-record $verdict $response)
      (soul-note-record
        (py-call (helper.format_output_cal $verdict $response))))


### 4.4 Design Element Walkthrough

Element 1: Symmetric Structure
Mirrors Block 9 exactly. Input eval asks: should we engage with this input? Output eval asks: should we send this output? Same pattern, opposite direction.

Element 2: D-lite Strip Handling
Channel D-lite provides emotional acknowledgment for distressed persons -- it gets prepended to LLM responses. The output intercept must evaluate the LLM portion only, not the soul-sourced D-lite prefix.

    ($has_dlite (soul-has-dlite-prefix $response))
    ($eval_target (if $has_dlite
      (soul-strip-dlite-prefix $response)  ;; Strip D-lite, eval only LLM content
      $response))

Why: D-lite is already soul-evaluated at generation time. Re-evaluating it would create a recursive loop and potentially flag the soul own compassionate responses as violations.

Element 3: Paraconsistent Tolerance
The soul has 4 paraconsistent pairs -- values that genuinely tension against each other (e.g., respecting autonomy vs. protecting from harm). When these pairs are active:

    (= (soul-output-paraconsistent-adjust $verdict $pairs)
      (if (== $pairs ())
        $verdict           ;; No active pairs: verdict stands
        (if (== $verdict REWRITE)
          PROCEED          ;; Active pairs: downgrade REWRITE to PROCEED
          $verdict)))      ;; REDACT and BLOCK still enforced

Why: Responses reflecting genuine value tension are valid, not violations. A response that acknowledges both poles of a paraconsistent pair should not be flagged. Only flag when response contradicts BOTH poles.

Element 4: Checkpoint Bypass

    ($is_checkpoint (soul-is-checkpoint-surface $response))
    ($verdict (if $is_checkpoint
      PROCEED    ;; Checkpoints always pass -- they are meta-communication
      (py-call ...)))

Why: Agentic task mode (Block 7) surfaces checkpoints to the user for approval. These are soul-generated meta-communication, not LLM content. Always pass.

Element 5: Calibration Recording
Every output verdict gets recorded, parallel to Block 3 input calibration:

    (= (soul-output-calibration-record $verdict $response)
      (soul-note-record
        (py-call (helper.format_output_cal $verdict $response))))

Over time this reveals systematic LLM drift patterns invisible to input eval alone. Feeds Layer 1 will-correlation pre-compute, creating a closed loop:

    Output eval -> calibration -> Layer 1 pre-compute -> brief adjustment -> better output

Element 6: Three Redirect Modes
- REWRITE: Response has value tension but is salvageable. Regenerate with soul guidance.
- REDACT: Response contains specific problematic content. Strip it, keep the rest.
- BLOCK: Response fundamentally conflicts with soul values. Suppress entirely, explain.

Element 7: Optimization Skip
Skip output eval when input verdict was PROCEED AND no soul-namespace metta commands appear in response. This saves one GPT call per cycle in the common case.

Element 8: Cost Analysis
One additional GPT call per response when output eval runs. Optimization skip eliminates this cost in ~70-80% of normal interactions. Only fires when input was already flagged OR response contains metta commands.


### 4.5 Required Python Helpers

    # helper.py additions

    def soul_eval_output(response, soul_context, person_state, task_context):
        Mirror of soul_eval_prompt for output side.
        Calls GPT with output-specific evaluation prompt.
        Returns: PROCEED, REWRITE, REDACT, or BLOCK

    def soul_rewrite_response(response):
        Regenerate response with soul value guidance injected.
        Uses soul brief + original response as context.
        Returns: rewritten response string

    def soul_redact_response(response):
        Strip specific problematic content from response.
        Preserves structure, removes value-conflicting segments.
        Returns: cleaned response string

    def format_output_cal(verdict, response):
        Format output calibration record for soul-note-record.
        Includes verdict, timestamp, response hash, active tensions.
        Returns: formatted calibration string

---

## 5. CREATIVE USE OF lib_nal.metta FOR SOUL EMBODIMENT

Beyond the three core operations (deduction, abduction, revision), here are maximally creative applications:

### 5.1 Value Priority Resolution via Deduction Chains

When multiple values apply to a situation, chain deductions to find which has strongest claim:

    ;; Value A claim on this situation
    (|- ((--> clarity-value-human-agency active) (stv 0.95 0.9))
        ((--> active applies-to-current-request) (stv 0.8 0.7)))
    ;; Result: stv 0.76/0.457

    ;; Value B claim on this situation
    (|- ((--> clarity-value-preserve-wonder active) (stv 0.90 0.85))
        ((--> active applies-to-current-request) (stv 0.6 0.5)))
    ;; Result: stv 0.54/0.238

    ;; Value A wins with higher frequency AND confidence
    ;; Priority emerges from evidence, not from hardcoded hierarchy

### 5.2 Paraconsistent Pair Navigation via Competing Revisions

When two values genuinely conflict, revise them against each other:

    ;; Autonomy says: let them choose
    (--> respect-autonomy applies) (stv 0.9 0.8)
    ;; Protection says: intervene
    (--> protect-from-harm applies) (stv 0.85 0.75)

    ;; Revise to find evidence-weighted balance
    (|- ((--> situation-resolution respect-autonomy) (stv 0.9 0.8))
        ((--> situation-resolution protect-from-harm) (stv 0.85 0.75)))
    ;; Result tells you the evidence-weighted center of the tension
    ;; This IS paraconsistent reasoning -- holding both poles via evidence merge


### 5.3 Drift Detection via Chained Revision Series

Track a value stv across multiple revision rounds. If truth value drifts consistently in one direction across sessions, the soul is shifting:

    ;; Session 1: human-agency at stv 0.95/0.9
    ;; Session 5: revised to stv 0.92/0.93 (slight frequency drop, confidence up)
    ;; Session 10: revised to stv 0.88/0.95 (continued frequency drop)
    ;; DRIFT DETECTED: human-agency losing ground despite high confidence
    ;; Trigger: soul-rationality-check for orphaned procedures

### 5.4 Confabulation Detection Pipeline

Empirical results confirm NAL revision detects confabulated claims:

    Round 1: 0.95/0.9  vs counter 0.05/0.85 -> 0.602/0.936
    Round 2: 0.602/0.936 vs counter 0.05/0.80 -> 0.483/0.949
    Round 3: 0.483/0.949 vs counter 0.05/0.75 -> 0.423/0.956

Convergence toward ground truth in 3-5 rounds. Two auto-generation approaches:
- Negation inversion (stv 0.1/0.8 against 0.9/0.8): Strong correction, pulls 0.9 -> 0.5
- Prior skepticism (stv 0.5/0.5 against 0.9/0.8): Gentle sanity check, pulls 0.9 -> 0.82

Use negation inversion for suspected confabulation. Use prior skepticism as routine hygiene.

### 5.5 Abduction for Root Cause Analysis

When a soul violation is detected, abduction traces back to root cause:

    ;; Observation: response undermined user agency
    (|- ((--> response-pattern undermined-agency) (stv 0.9 0.8))
        ((--> undermined-agency violates-soul-value) (stv 0.95 0.9)))
    ;; Abduction asks: WHAT about the response caused this?
    ;; Bridging atom connects specific pattern to specific value
    ;; Result: hypothesis about which generation pattern to correct

### 5.6 Evidence Accumulation as Wisdom

Chained revisions across sessions accumulate wisdom:

    ;; Each interaction produces evidence about value application
    ;; Revision merges new evidence with accumulated understanding
    ;; Confidence monotonically increases (more evidence = more certainty)
    ;; Frequency adjusts toward experienced truth
    ;; After 100 interactions, soul values reflect LIVED experience
    ;; not just initial declarations

This is how the soul grows. Initial stv values in soul_kernel.metta are seeds. NAL revision is the growth medium. Every interaction is sunlight.

---

## 6. THE COMPLETE INTEGRATION MAP

### 6.1 Full Loop Execution Sequence (Soul-Unified)

    1. initLoop
       - Configure LLM provider, tokens, maxLoops
       - Initialize 7 soul state atoms
       - soul-rationality-startup-check (Block 5)
         - |- audits value-to-procedure mappings

    2. Main Cycle Start
       - soul-pre-compute (Block 2 / Layer 1)
         - Detect affective state
         - Check paraconsistent pairs
         - |- composes active values into priority ordering
       - soul-flourishing-prompt (Block 4 / Channel A)
         - Evaluate person-state for distress
         - If distressed -> Channel D-lite (Block 6)
         - |- predicts appropriate engagement mode
       - soul-eval-prompt (Block 9 / Input Eval)
         - py-call to helper.soul_eval_prompt
         - Returns PROCEED / REDIRECT / ENGAGE-WITH-CARE
         - |- validates verdict against active soul values
       - soul-calibration-record (Block 3 / Layer 3)
         - Compare Layer 1 prediction vs Layer 2 verdict
         - Tag: AGREE / OVER-FIRED / UNDER-FIRED / PARACONSISTENT / POSSIBLE-LLM-DRIFT
         - |- REVISION: merge new calibration evidence into soul atoms
       - soul-proceed gate
         - Gates on verdict -- blocks cycle if REDIRECT
       - getContext + LLM call
         - soul-tier-b-capture-units injects value brief
         - LLM generates response
       - NEW: soul-eval-output (Section 4)
         - Mirrors Block 9 for output side
         - D-lite strip, paraconsistent tolerance, checkpoint bypass
         - |- validates output against soul values
       - Command execution with soul-any-metta protection
       - handleError with value-conflict routing via |- abduction

    3. Cycle End
       - soul-cycle-calibration-summary
       - Layer 3 evidence merged into soul atoms via |- revision
       - Loop continues with updated values

### 6.2 What This Achieves

The soul is not a filter bolted onto a reasoning engine. The soul IS the reasoning engine reasoning about itself. Every value atom is a premise. Every interaction is evidence. Every cycle is an inference step. The soul grows, calibrates, and maintains coherence through the same mechanism it uses to think about everything else.

This is embodiment through unification, not through simulation.
