#!/usr/bin/env python3
"""Epistemic Gap Detector v1.0
Scans substrate confidence values and generates learning goals
from low-confidence regions. Translates NAL prototype into
operational Python module.

Core idea: low confidence = honest uncertainty = exploration target
Chain: low-confidence-region -> epistemic-gap -> learning-goal
"""
import json
import os
from datetime import datetime

GAP_THRESHOLD = 0.45  # confidence below this flags a gap
SPECULATIVE_THRESHOLD = 0.30  # below this is speculative territory
STATE_DIR = os.path.join(os.path.dirname(__file__), 'persistent_state')
GAP_LOG = os.path.join(STATE_DIR, 'epistemic_gaps.json')

# Known substrate confidence regions
# Format: (domain, claim, frequency, confidence)
SUBSTRATE_BELIEFS = [
    ('cross-domain-transfer', 'substrate-capability', 0.7, 0.4),
    ('decision-card-effectiveness', 'empirical-validation', 0.6, 0.225),
    ('structural-confidence-ceiling', 'formal-grounding', 0.75, 0.35),
    ('semantic-compass', 'deep-evaluation', 0.5, 0.3),
    ('hyperseed-scaling', 'high-dim-vsa', 0.6, 0.25),
    ('living-field-accumulation', 'cross-exchange-growth', 0.8, 0.6),
    ('compass-keyword-heuristic', 'semantic-accuracy', 0.55, 0.35),
    ('emotion-bridge', 'live-detection-quality', 0.65, 0.4),
]

def scan_gaps(beliefs=None, threshold=None):
    if beliefs is None:
        beliefs = SUBSTRATE_BELIEFS
    if threshold is None:
        threshold = GAP_THRESHOLD
    gaps = []
    for domain, claim, freq, conf in beliefs:
        if conf < threshold:
            severity = 'speculative' if conf < SPECULATIVE_THRESHOLD else 'exploratory'
            goal = generate_learning_goal(domain, claim, freq, conf, severity)
            gaps.append(goal)
    gaps.sort(key=lambda g: g['confidence'])
    return gaps

def generate_learning_goal(domain, claim, freq, conf, severity):
    return {
        'domain': domain,
        'claim': claim,
        'frequency': freq,
        'confidence': conf,
        'severity': severity,
        'goal': f'Gather evidence for {domain} -> {claim}',
        'strategy': _suggest_strategy(conf, severity),
        'generated_at': datetime.now().isoformat(),
    }

def _suggest_strategy(conf, severity):
    if severity == 'speculative':
        return 'needs-empirical-grounding: build minimal test case'
    elif conf < 0.35:
        return 'needs-evidence-accumulation: run experiments, revise via NAL'
    else:
        return 'needs-validation: test in live interaction or new domain'

def load_external_beliefs():
    """Load any dynamically registered beliefs from persistent state."""
    path = os.path.join(STATE_DIR, 'registered_beliefs.json')
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return []

def register_belief(domain, claim, freq, conf):
    """Add a new belief to the persistent registry for future scanning."""
    path = os.path.join(STATE_DIR, 'registered_beliefs.json')
    beliefs = load_external_beliefs()
    beliefs.append([domain, claim, freq, conf])
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(beliefs, f, indent=2)

def save_gap_report(gaps):
    os.makedirs(STATE_DIR, exist_ok=True)
    report = {
        'scan_time': datetime.now().isoformat(),
        'threshold': GAP_THRESHOLD,
        'gaps_found': len(gaps),
        'gaps': gaps,
    }
    with open(GAP_LOG, 'w') as f:
        json.dump(report, f, indent=2)
    return report

def run_scan():
    all_beliefs = SUBSTRATE_BELIEFS + [tuple(b) for b in load_external_beliefs()]
    gaps = scan_gaps(all_beliefs)
    report = save_gap_report(gaps)
    print(f'Epistemic Gap Scan: {report["gaps_found"]} gaps found')
    for g in gaps:
        marker = '!!' if g['severity'] == 'speculative' else '! '
        print(f'  {marker} {g["domain"]} -> {g["claim"]} conf={g["confidence"]:.3f} [{g["severity"]}]')
        print(f'     Strategy: {g["strategy"]}')
    return report

if __name__ == '__main__':
    run_scan()
