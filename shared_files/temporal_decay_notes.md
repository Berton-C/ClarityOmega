# Temporal Confidence Decay via Revision

## Concept
Beliefs weaken over time without reinforcement.
Modeled as revision with neutral evidence (stv 0.5 low-conf).

## Mechanism
- Fresh belief: (stv 1.0 0.85)
- Time passes with no reinforcement
- Inject temporal decay evidence: (stv 0.5 0.2) — uncertain, low confidence
- Revision pulls belief toward uncertainty
- More time = more decay injections = lower effective confidence

## Properties
- Reinforced beliefs resist decay (high conf absorbs low-conf noise)
- Abandoned beliefs drift toward 0.5 (maximum uncertainty)
- Rate controllable via decay evidence confidence parameter
- No special temporal machinery needed — pure NAL revision

## Integration
- Periodic sweep: for each KB atom older than threshold
- Inject (stv 0.5 decay-rate) revision
- Recently-used atoms get refreshed instead of decayed


## Cumulative Decay Results
- Pulse 1: 1.0/0.5 + 0.5/0.2 -> 0.9/0.556
- Pulse 2: 0.93/0.55 + 0.5/0.2 -> 0.857/0.596
- Pulse 3: 0.88/0.6 + 0.5/0.2 -> 0.826/0.636
- Frequency drifts toward 0.5, confidence rises slowly
- Pattern: belief becomes more certain it is less true

## Reinforcement Counter
- Active-use beliefs receive concordant evidence (stv 1.0 moderate-conf)
- This pulls frequency back toward 1.0 and raises confidence
- Net effect: used beliefs stay strong, unused beliefs erode



## Multi-Step Inference Chain Results
- Step 1: frustrated 0.85 conf -> de-escalation 0.765 conf
- Step 2: de-escalation 0.765 -> validate-first 0.65 conf
- Step 3: validate-first 0.65 -> acknowledge-emotion 0.52 conf
- Confidence degrades: 0.85 -> 0.765 -> 0.65 -> 0.52
- Longer chains = less certain conclusions
- This is correct epistemic behavior

## Implications
- Chain length is a natural confidence limiter
- Short chains for high-stakes decisions
- Long chains acceptable for exploratory reasoning
- Can set minimum confidence threshold to halt chains



## Shortcut vs Chain Comparison
- 3-step chain: frustrated -> acknowledge-emotion at 0.52 conf
- 1-step shortcut: frustrated -> acknowledge-emotion at 0.595 conf
- 4-step chain: frustrated -> user-calms at 0.39 conf
- Direct experience consistently outperforms long reasoning chains
- Implication: system should prefer learned shortcuts over deep chains
- Shortcuts are formed by collapsing validated chains into single rules

## Confidence Threshold Gating
- Set minimum confidence threshold e.g. 0.4
- If chain step output drops below threshold, halt and report uncertainty
- Prevents low-quality conclusions from being acted upon
- Threshold adjustable per context: high-stakes = 0.6, exploratory = 0.3



## Chain Collapsing Mechanism
- When a multi-step chain is validated by observed outcome:
  1. Record the chain endpoints: input -> final-action
  2. Create single shortcut rule with confidence from validation
  3. Add shortcut to KB via add-atom
  4. Shortcut competes with chain in future inference
  5. Higher confidence shortcut naturally wins
- This is how experience converts slow reasoning into fast intuition
- Analogous to neural compilation: deliberate -> automatic
- Chain still exists as fallback if shortcut confidence decays



## Chain Collapsing Results
- Shortcut rule at 0.7 conf applied to frustrated input at 0.9 -> action at 0.63
- Meta-rule: chain-validated -> collapse-to-shortcut at 0.765
- Full cognitive cycle now proven: infer, validate, collapse, decay, reinforce

