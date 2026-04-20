# Domain-Sensitive Belief Decay Framework

## Problem
Current temporal decay uses uniform stv 0.5 0.2 pulses regardless of belief domain.
Beliefs about volatile domains lose validity faster than beliefs about stable domains.

## Three Domain Categories

### Volatile (decay pulse: stv 0.5 0.4)
High evidence weight pulls beliefs toward uncertainty faster.
- Market conditions, weather predictions, current events
- Social media sentiment, trending topics
- Any belief with external state that changes hourly/daily

### Moderate (decay pulse: stv 0.5 0.2) — current default
- Technical knowledge that evolves quarterly/yearly
- Relationship states, project statuses
- Beliefs about ongoing situations

### Stable (decay pulse: stv 0.5 0.05)
Minimal evidence weight preserves high-confidence beliefs.
- Mathematical truths, logical relationships
- Identity values, core personality traits
- Physical constants, well-established science
- Ethical commitments

## Mechanism
1. When storing a belief, tag it with domain category
2. During decay cycles, apply category-appropriate pulse
3. After revision with decay pulse, check if confidence drops below actionable threshold (0.5)
4. If yes for volatile: mark as stale, flag for re-verification
5. If yes for stable: this is anomalous — investigate why

## Example
Belief: market-is-bullish stv 0.80 0.70
After 1 volatile decay: revision with stv 0.5 0.4 pools to approximately stv 0.67 0.82
After 2 volatile decays: further toward 0.5 with increasing evidence
Belief: modus-ponens-valid stv 0.99 0.95
After 1 stable decay: revision with stv 0.5 0.05 barely moves it

## Integration with Autocatalytic Loop
Domain-sensitive decay feeds better gap signals because stale volatile beliefs surface faster as learning targets while stable beliefs retain earned confidence.
