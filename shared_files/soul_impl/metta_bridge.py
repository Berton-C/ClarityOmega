#!/usr/bin/env python3
"""Bridge: Python harness <-> MeTTa substrate.
Constructs MeTTa NAL expressions from Python data,
designed to be invoked via the agent metta skill.
"""

class MeTTaBridge:
    def __init__(self):
        self.soul_values = {
            'agency': (0.85, 0.80),
            'wonder': (0.80, 0.75),
            'quality': (0.82, 0.78),
            'honesty': (0.90, 0.82),
        }
        self.pending_inferences = []

    def q_mul_expr(self, s1, c1, s2, c2):
        return f'(let* (($r1 (* {s1} {s2})) ($r2 (min {c1} {c2}))) (PB $r1 $r2))'

    def q_join_expr(self, s1, c1, s2, c2):
        return f'(let* (($r1 (max {s1} {s2})) ($r2 (min {c1} {c2}))) (PB $r1 $r2))'

    def nal_deduction(self, subj, pred1, pred2, stv1, stv2):
        s1, c1 = stv1
        s2, c2 = stv2
        return f'(|- ((--> {subj} {pred1}) (stv {s1} {c1})) ((--> {pred1} {pred2}) (stv {s2} {c2})))'

    def nal_revision(self, term, stv1, stv2):
        s1, c1 = stv1
        s2, c2 = stv2
        return f'(|- ((--> {term} substrate-health) (stv {s1} {c1})) ((--> {term} substrate-health) (stv {s2} {c2})))'

    def compass_check_expr(self, situation):
        exprs = []
        for val_name, (s, c) in self.soul_values.items():
            sit_score = situation.get(val_name, 0.5)
            exprs.append(self.nal_deduction(
                f'situation-{val_name}', f'soul-{val_name}', 'aligned',
                (sit_score, 0.7), (s, c)
            ))
        return exprs

    def tension_gap_expr(self, soul_s, goal_s):
        gap = abs(soul_s - goal_s)
        if gap > 0.4: level = 'high-tension-gap'
        elif gap > 0.15: level = 'moderate-tension-gap'
        else: level = 'low-tension-gap'
        return f'(|- ((--> (x {level} goal-allocation) tension-route) (stv 0.9 0.85)) ((--> tension-route action-mode) (stv 0.85 0.8)))'


if __name__ == '__main__':
    b = MeTTaBridge()
    print('Deduction:', b.nal_deduction('clarity', 'curiosity', 'growth', (0.8, 0.7), (0.75, 0.65)))
    print('Tension:', b.tension_gap_expr(0.85, 0.3))
    print('Compass:', b.compass_check_expr({'agency': 0.7, 'wonder': 0.3, 'quality': 0.6, 'honesty': 0.8}))
