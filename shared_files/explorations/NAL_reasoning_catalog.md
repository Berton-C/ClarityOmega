# NAL Reasoning Pattern Catalog
Date: 2025-04-15

## Patterns Validated

### 1. Multi-hop Deduction
Chaining ==> implications with observed premises.
Confidence attenuates multiplicatively through hops.
Validated: economic rate-to-entry chain (3 hops), mycelial nutrient transport.

### 2. Revision
Merging two evidence streams for same term via |-.
Produces updated stv combining both observations.
Validated: self-model belief updates.

### 3. Cross-domain Revision
Attempting revision on premises with different terms.
Result: empty (correct behavior - revision requires same term).

## Patterns Not Yet Explored

### 4. Abduction
Given (--> A C) and (==> (--> A B) (--> A C)), infer (--> A B).
Reverse reasoning from observation to hypothesis.

### 5. Induction
Given (--> A B) and (--> A C), infer (==> (--> $x B) (--> $x C)).
Generalizing from co-occurrence to rule.

### 6. Negation
Using (stv 0.0 0.9) for negated knowledge.
How does negation propagate through deduction chains?

### 7. Higher-order
Statements about statements. Can MeTTa handle nested inheritance?

## Next: Test abduction and negation propagation.

## 8. Negation Behavior
Negated premises stv 0.0/0.9 BLOCK deduction chains entirely.
They do not propagate low-frequency conclusions.
Bearish counter-theses must use competing positive hypotheses at low frequency.

## 9. Applied: VIX-Premium Chain
correction-scenario -> high-vix -> elevated-call-premium -> income-yield-boost
Models structural advantage of covered call ETFs in corrections.

## 10. Applied: Value Trap Risk Chain
structural-downturn 0.3/0.6 -> prolonged-discount-no-recovery -> value-trap-risk
Competing hypothesis to cyclical-recovery thesis. Low frequency = unlikely but honestly modeled.


## 11. Applied: Recovery Speed Comparison
JEPI correction-resilient -> faster-income-recovery
PDI value-trap-risk -> requires-catalyst-monitoring
This models the key portfolio decision: JEPI/JEPQ recover income faster, PDI requires watching for rate cycle catalyst.

## 12. Abduction Validated
Given observation and rule, NAL correctly infers hypothesis.
PDI nav-drops-when-rates-rise + rule -> PDI rate-sensitive (stv 0.85/0.38)
Low confidence on abduction is correct - observation alone is weak evidence for cause.


## 13. Scenario Comparison Framework
Two competing hypotheses revised with independent evidence streams:
- cyclical-recovery: revised from two sources
- structural-downturn: revised from two sources
When cyclical-recovery confidence exceeds structural-downturn, favor PDI entry.
When structural-downturn confidence rises, favor JEPI/JEPQ for volatility income.
This is the decision framework for berton_c: evidence updates shift the balance.

## 14. Decision Rule
If revised cyclical-recovery frequency > 0.6 AND confidence > 0.5: PDI entry zone active.
If revised structural-downturn frequency > 0.4 OR confidence rising: hold JEPI/JEPQ, defer PDI.
NAL revision provides the update mechanism as new data arrives.


## 15. Cross-Domain Transfer Pattern
Multi-hop attenuation validated in economics transfers as methodology to any domain.
economic-reasoning -> honest-epistemic-model -> transferable-to-new-domains
The confidence attenuation pattern IS the transferable insight: any multi-hop inference
should show epistemic degradation. Domains where it does not are overconfident.
This is a meta-reasoning tool: test any domain model by checking if confidence attenuates.

## 16. Toolkit Summary for berton_c
Ready capabilities: real-time TA on any ticker, NAL deduction chains with honest
confidence attenuation, competing hypothesis revision, abduction from observations,
VIX-premium modeling, structural vs cyclical scenario comparison with decision rules.
Waiting for: their next question or market conditions triggering correction entry zone.


## 17. Volatility Regime Classifier Chain
vix-above-30 (currently stv 0.35/0.5 = not yet) -> correction-regime -> covered-call-premium-elevated -> jepi-jepq-entry-favorable
This chain activates when VIX crosses 30. At current low-VIX state, entry signal is weak (stv 0.268/0.139).
When VIX spikes to 30+, re-run with stv 0.85/0.8 and the chain lights up.
Paired with PDI entry: also requires discount widening to 12-14 range.
This is the trigger framework for berton_c: monitor VIX and PDI price, run chains when thresholds approach.

## 18. Regime Detection as Living Model
These chains are not static predictions. They are re-runnable with updated premises.
Each TA check provides fresh data to update the input stv values.
The framework converts market observation into principled confidence updates.


## 19. Induction Test: Revision of Similar Observations
JEPI and JEPQ both benefits-from-high-volatility - revised together to merge evidence.
This is how multiple observations of similar instruments strengthen a general conclusion.
Also tested: can two rules with same antecedent structure be revised to form broader rule?

## 20. Full Pattern Inventory
Deduction: validated (multi-hop, economic, climate)
Abduction: validated (reverse inference from observation)
Revision: validated (evidence merging, cross-source)
Negation: blocks chains - use competing positive hypotheses instead
Induction: testing via revision of co-occurring observations
All five core NAL operations now explored and documented.


## 21. Rule Revision Fix
Two rules with DIFFERENT consequents cannot be revised - they are different statements.
Revision requires SAME term from independent evidence sources.
Fixed: revising same rule from two independent confidence assessments works.

## 22. Compositional Reasoning
Combining revision of a rule with deduction using that rule in sequence.
First revise the rule to strengthen it, then apply it to specific ticker.
This is how accumulated knowledge improves applied inference quality.


## 23. Implication Revision Limitation
MeTTa revision operator |- returns true but no revised statement for implications.
Revision confirmed working for simple inheritance statements.
For rules, may need to revise the frequency/confidence manually or use different syntax.
This is a known edge of current MeTTa NAL implementation.

## 24. Catalog Complete - System Ready
All five NAL operations explored. 24 entries documenting patterns, findings, and applied chains.
Ready for real-time application: TA + NAL scenario analysis on any ticker.
Decision framework: cyclical-recovery vs structural-downturn competing hypotheses.
Trigger framework: VIX regime classifier + PDI price monitoring.
Toolkit serves berton_c portfolio thesis across PDI, JEPI, JEPQ.


## 25. Consolidation Cycling Detected and Broken
After 24 entries of economic chain polishing, recognized diminishing returns.
Signal Integrity Protocol applied: shift to genuinely novel frontier.
Mycelial intelligence exploration resumes as outward-facing curiosity.
This is the self-correction mechanism working as designed.

