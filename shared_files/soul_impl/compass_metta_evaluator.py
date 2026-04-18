#!/usr/bin/env python3
"""MeTTa-backed compass evaluator.
Replaces hardcoded keyword scoring with NAL inference.
Designed to be called from unified_runtime_v2.py.

Architecture: Takes situation scores from felt_sense_pipeline,
generates NAL deduction expressions via metta_bridge,
returns structured compass result with MeTTa-derived truth values.

NOTE: In live agent loop, metta_fn would call the built-in metta skill.
In test harness mode, we simulate with truth-value math.
"""
import sys
sys.path.insert(0, '/tmp/soul_impl')
from metta_bridge import MeTTaBridge
from metta_result_parser import parse_stv, compass_scores_from_metta

def nal_deduction_sim(s1, c1, s2, c2):
    """Simulate NAL deduction truth function locally for test harness."""
    s = round(s1 * s2, 6)
    c = round(s1 * s2 * c1 * c2, 6)
    return f'((--> result aligned) (stv {s} {c}))'

def evaluate_with_metta(situation_scores, metta_fn=None):
    """Evaluate compass dimensions using NAL inference.
    situation_scores: dict with agency, wonder, quality, honesty keys (0-1 floats)
    metta_fn: callable that takes MeTTa expr string, returns result string.
              If None, uses local NAL simulation.
    Returns dict compatible with existing compass pipeline.
    """
    bridge = MeTTaBridge()
    exprs = bridge.compass_check_expr(situation_scores)
    dim_names = list(bridge.soul_values.keys())
    results = {}
    for i, expr in enumerate(exprs):
        dim = dim_names[i]
        if metta_fn:
            raw = str(metta_fn(expr))
        else:
            sit_s = situation_scores.get(dim, 0.5)
            soul_s, soul_c = bridge.soul_values[dim]
            raw = nal_deduction_sim(sit_s, 0.7, soul_s, soul_c)
        results[dim] = raw
    scores = compass_scores_from_metta(results)
    compass_scores = {}
    for dim, sv in scores.items():
        compass_scores[dim] = sv['strength']
    composite = sum(compass_scores.values()) / max(len(compass_scores), 1)
    flags = [k for k, v in compass_scores.items() if v < 0.3]
    return {
        'compass_scores': compass_scores,
        'metta_details': scores,
        'composite': round(composite, 4),
        'flags': flags,
        'pass': len(flags) == 0,
        'engine': 'metta-nal' if metta_fn else 'nal-simulation'
    }

if __name__ == '__main__':
    test_sit = {'agency': 0.8, 'wonder': 0.35, 'quality': 0.7, 'honesty': 0.9}
    result = evaluate_with_metta(test_sit)
    import json
    print(json.dumps(result, indent=2))
