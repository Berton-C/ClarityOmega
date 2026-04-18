import json
import re
import sys
sys.path.insert(0, '/tmp/soul_impl')
from resonance_runtime_bridge import compute_cycle_allocation
from web_detector import loop_strength

def parse_metta_stv(result_str):
    m = re.search(r'stv\s+([0-9.]+)\s+([0-9.]+)', str(result_str))
    if m:
        return float(m.group(1)), float(m.group(2))
    return None, None

def close_cycle(metta_results, situation=None):
    scores = {}
    for dim, result_str in metta_results:
        freq, conf = parse_metta_stv(result_str)
        if freq is not None:
            scores[dim] = {'frequency': freq, 'confidence': conf}
    threshold = 0.3
    flagged = [d for d, s in scores.items() if s['frequency'] < threshold]
    passed = len(flagged) == 0
    links = [(0.9, 0.8), (0.85, 0.75), (0.9, 0.67)]
    ls = loop_strength(links)
    ls_val = ls[0] if isinstance(ls, (list, tuple)) else ls
    effort = compute_cycle_allocation(ls_val)
    return {'scores': scores, 'flagged': flagged, 'passed': passed, 'effort': effort, 'loop_strength': ls_val, 'engine': 'metta-native-closed-loop'}

if __name__ == '__main__':
    test_results = [('agency', '((--> situation-agency aligned) (stv 0.34 0.19))'), ('wonder', '((--> situation-wonder aligned) (stv 0.24 0.13))'), ('quality', '((--> situation-quality aligned) (stv 0.41 0.22))'), ('honesty', '((--> situation-honesty aligned) (stv 0.765 0.44))')]
    r = close_cycle(test_results)
    print(json.dumps(r, indent=2))
