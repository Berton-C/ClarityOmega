#!/usr/bin/env python3
"""NAL Dispatcher — Pure NAL reasoning with Python thin IO only.
Takes raw tone observation, returns response strategy via two MeTTa deductions.
No Python if/else in the reasoning path. All logic lives in NAL atoms."""

# This is the architecture berton_c pointed toward:
# Python = IO shell, MeTTa/NAL = all reasoning

TONE_TO_NEED_RULES = {
    'neg-low-dom': '(==> (--> observed-tone neg-low-dom) (--> user-need validation-and-safety)) (stv 1.0 0.9)',
    'neg-valence': '(==> (--> observed-tone neg-valence) (--> user-need support)) (stv 1.0 0.9)',
    'pos-high-aro': '(==> (--> observed-tone pos-high-aro) (--> user-need momentum-matching)) (stv 1.0 0.9)',
    'neg-high-aro': '(==> (--> observed-tone neg-high-aro) (--> user-need de-escalation)) (stv 1.0 0.9)',
}

NEED_TO_STRATEGY_RULES = {
    'validation-and-safety': '(==> (--> user-need validation-and-safety) (--> response-strategy slow-pace-acknowledge-first)) (stv 1.0 0.9)',
    'support': '(==> (--> user-need support) (--> response-strategy validate-then-assist)) (stv 1.0 0.9)',
    'momentum-matching': '(==> (--> user-need momentum-matching) (--> response-strategy match-energy-collaborate)) (stv 1.0 0.9)',
    'de-escalation': '(==> (--> user-need de-escalation) (--> response-strategy slow-pace-acknowledge-first)) (stv 1.0 0.9)',
}

TRAJECTORY_RULES = {
    'lifting': '(==> (--> trajectory lifting) (--> strategy-override upgrade-to-collaborative)) (stv 1.0 0.85)',
    'dropping': '(==> (--> trajectory dropping) (--> strategy-override downshift-to-supportive)) (stv 1.0 0.85)',
}

def build_deduction_expr(rule_stv, observation_stv):
    """Build a MeTTa |- expression for deduction. Pure string assembly — no logic."""
    return f'(|- ({rule_stv}) ({observation_stv}))'

# Example pipeline: tone='neg-low-dom', confidence=0.85
# Step 1: metta(|- rule observation) -> user-need with propagated confidence
# Step 2: metta(|- rule need_result) -> response-strategy with propagated confidence
# Python never decides the strategy. NAL does.
