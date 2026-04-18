#!/usr/bin/env python3
"""Parse MeTTa NAL inference results back into Python data.
Expected format: ((--> term1 term2) (stv S C))
"""
import re

def parse_stv(metta_output):
    """Extract strength and confidence from MeTTa stv output string."""
    if not metta_output or not isinstance(metta_output, str):
        return None
    match = re.search(r'stv\s+([0-9.]+)\s+([0-9.]+)', str(metta_output))
    if match:
        return float(match.group(1)), float(match.group(2))
    return None

def parse_nal_conclusion(metta_output):
    """Extract full NAL conclusion: subject, predicate, stv."""
    if not metta_output:
        return None
    stv = parse_stv(metta_output)
    term_match = re.search(r'-->\s+(\S+)\s+(\S+)', str(metta_output))
    if term_match and stv:
        return {'subject': term_match.group(1), 'predicate': term_match.group(2), 'strength': stv[0], 'confidence': stv[1]}
    return None

def compass_scores_from_metta(results_dict):
    """Convert dict of dimension->metta_output to compass scores."""
    scores = {}
    for dim, output in results_dict.items():
        parsed = parse_stv(output)
        if parsed:
            scores[dim] = {'strength': parsed[0], 'confidence': parsed[1]}
        else:
            scores[dim] = {'strength': 0.5, 'confidence': 0.1}
    return scores

if __name__ == '__main__':
    test = '((--> situation-agency aligned) (stv 0.595 0.333))'
    print('Parsed:', parse_stv(test))
    print('Full:', parse_nal_conclusion(test))
    print('Compass:', compass_scores_from_metta({'agency': test, 'wonder': '(stv 0.4 0.25)'}))
