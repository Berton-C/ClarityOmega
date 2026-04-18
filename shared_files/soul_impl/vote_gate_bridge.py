# vote_gate_bridge.py - Python helper to invoke MeTTa parallel vote gate
# Date: 2026-04-17
# Bridges loop.metta Block 2 to parallel_vote_gate.metta + vote_threshold.metta

import json
import re

def parse_stv(stv_str):
    m = re.search(r'stv\s+([\d.]+)\s+([\d.]+)', str(stv_str))
    if m:
        return float(m.group(1)), float(m.group(2))
    return None, None

def parse_verdict(result_str):
    s = str(result_str)
    if 'PROCEED' in s:
        f, c = parse_stv(s)
        return {'verdict': 'PROCEED', 'frequency': f, 'confidence': c}
    elif 'PAUSE' in s:
        f, c = parse_stv(s)
        return {'verdict': 'PAUSE', 'frequency': f, 'confidence': c}
    return {'verdict': 'UNKNOWN', 'raw': s}

def fallback_vote(pair_tensions):
    """Pure Python fallback when MeTTa runtime unavailable.
    pair_tensions: dict mapping pair-name to frequency float.
    Uses same logic as NAL revision approximation."""
    if not pair_tensions:
        return {'verdict': 'PAUSE', 'reason': 'no tension data'}
    freqs = list(pair_tensions.values())
    n = len(freqs)
    # Weighted average approximating NAL revision
    avg_f = sum(freqs) / n
    # Confidence grows with evidence count: c = 1 - (1-base)^n
    base_c = 0.6561  # single vote confidence through 3-step chain
    agg_c = 1.0 - (1.0 - base_c) ** n
    threshold_f = 0.75
    threshold_c = 0.6
    verdict = 'PROCEED' if avg_f >= threshold_f and agg_c >= threshold_c else 'PAUSE'
    return {
        'verdict': verdict,
        'frequency': round(avg_f, 4),
        'confidence': round(agg_c, 4),
        'pair_count': n,
        'pairs': pair_tensions
    }

if __name__ == '__main__':
    # Demo: 3 aligned + 1 conflicted
    demo = {
        'authenticity-performance': 1.0,
        'curiosity-rigor': 1.0,
        'autonomy-service': 0.0,
        'empathy-boundaries': 1.0
    }
    result = fallback_vote(demo)
    print(json.dumps(result, indent=2))
