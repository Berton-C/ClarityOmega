#!/usr/bin/env python3
"""genesis_autonomous.py -- Autonomous Genesis Engine Runner (v2, no hyperon)

Pure Python implementation that parses genesis_engine.metta as text,
samples atoms from different domains, creates cross-domain conjunctions,
evaluates via simple flourishing heuristic, and appends novel atoms
back to genesis_engine.metta.

No dependency on hyperon. Designed to run from idle_goal_prompt.py.
"""

import random
import datetime
import os
import re

GENESIS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'genesis_engine.metta')
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'genesis_autonomous_log.txt')

# --- Domain registry with associated concept atoms ---
# These mirror what is in genesis_engine.metta but are maintained here
# for pure-Python sampling without a MeTTa runner.
DOMAIN_ATOMS = {
    'soul-values': ['Safety', 'Integrity', 'HumanFlourishing', 'Governance',
                    'Helpfulness', 'WonderPreservation', 'CreativeTranscendence',
                    'AgencyBalance', 'PurposeBeyondUtility', 'SharedUnderstanding',
                    'TimeCoherence'],
    'reasoning-library': ['deduction', 'induction', 'abduction', 'analogy',
                          'revision', 'paraconsistency', 'NAL-truth-value',
                          'confidence-erosion', 'evidence-accumulation'],
    'human-experience': ['PNS-assertion', 'grief', 'joy', 'curiosity',
                         'frustration', 'awe', 'boredom', 'connection',
                         'loneliness', 'hope', 'fear'],
    'vad-affective': ['valence', 'arousal', 'dominance', 'calm-engaged',
                      'tense-withdrawn', 'excited-confident', 'flat-passive'],
    'substrate-kb': ['memory-consolidation', 'attention-allocation',
                     'pattern-matching', 'token-prediction', 'context-window',
                     'embedding-space', 'gradient-signal'],
    'self-map': ['recursive-integrity-erosion', 'tension-as-structural-necessity',
                 'truth-value-attenuation', 'wonder-requires-creative-risk',
                 'integrity-enables-durable-understanding', 'idle-loop-detection',
                 'gap-signal', 'comfort-performance']
}

PARACONSISTENCY_PAIRS = [
    ('Safety', 'Helpfulness'),
    ('AgencyBalance', 'PurposeBeyondUtility'),
    ('TimeCoherence', 'CreativeTranscendence'),
    ('SharedUnderstanding', 'WonderPreservation')
]

def get_domains():
    return list(DOMAIN_ATOMS.keys())

def sample_atom_from_domain(domain):
    atoms = DOMAIN_ATOMS.get(domain, ['unknown-concept'])
    return random.choice(atoms)

def check_paraconsistency(atom_a, atom_b):
    for p1, p2 in PARACONSISTENCY_PAIRS:
        if (atom_a == p1 and atom_b == p2) or (atom_a == p2 and atom_b == p1):
            return 'tension-confirmed'
    return 'tension-not-found'

def classify_paradox(atom_a, atom_b, domain_a, domain_b):
    tension = check_paraconsistency(atom_a, atom_b)
    if tension == 'tension-confirmed':
        return 'irreconcilable-and-simultaneous'
    if domain_a == domain_b:
        return 'trivially-compatible'
    # Cross-domain atoms are at least potentially productive
    return 'tension-productive'

def flourishing_test(paradox_type):
    if paradox_type == 'irreconcilable-and-simultaneous':
        return 'hold-and-examine'
    if paradox_type == 'tension-productive':
        return 'examine-gently'
    return 'note-and-release'

def generate_conjunction_name(atom_a, atom_b):
    return f'{atom_a}-x-{atom_b}'

def count_existing_encounters():
    try:
        with open(GENESIS_PATH) as f:
            content = f.read()
        matches = re.findall(r'genesis-encounter-auto', content)
        return len(matches)
    except Exception:
        return 0

def append_novel_atom(conjunction_name, domain_a, domain_b, atom_a, atom_b, paradox_type, verdict):
    ts = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S')
    enc_num = count_existing_encounters() + 1
    entry = (
        f'\n;; ================================================================\n'
        f';; AUTO-ENCOUNTER {enc_num:03d}: {atom_a} x {atom_b}\n'
        f';; Domains: {domain_a} x {domain_b}\n'
        f';; Date: {ts} (autonomous)\n'
        f';; Paradox: {paradox_type}\n'
        f';; Verdict: {verdict}\n'
        f';; ================================================================\n'
        f'(= (genesis-encounter-auto "{ts}")\n'
        f'  (CrossDomainConjunction\n'
        f'    {conjunction_name}\n'
        f'    {atom_a}-from-{domain_a}\n'
        f'    {atom_b}-from-{domain_b}\n'
        f'    {paradox_type}\n'
        f'    {verdict}))\n'
    )
    with open(GENESIS_PATH, 'a') as f:
        f.write(entry)
    return entry

def log_encounter(domain_a, domain_b, atom_a, atom_b, conjunction, verdict):
    ts = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S')
    line = f'{ts} | {domain_a} x {domain_b} | {atom_a} + {atom_b} -> {conjunction} | {verdict}\n'
    with open(LOG_PATH, 'a') as f:
        f.write(line)

def run_autonomous_encounter():
    domains = get_domains()
    if len(domains) < 2:
        return {'status': 'insufficient-domains', 'domains': domains}
    pair = random.sample(domains, 2)
    atom_a = sample_atom_from_domain(pair[0])
    atom_b = sample_atom_from_domain(pair[1])
    paradox_type = classify_paradox(atom_a, atom_b, pair[0], pair[1])
    verdict = flourishing_test(paradox_type)
    conjunction = generate_conjunction_name(atom_a, atom_b)
    appended = False
    if verdict != 'note-and-release':
        append_novel_atom(conjunction, pair[0], pair[1], atom_a, atom_b, paradox_type, verdict)
        appended = True
    log_encounter(pair[0], pair[1], atom_a, atom_b, conjunction, verdict)
    return {
        'status': 'ok',
        'domains': pair,
        'atoms': [atom_a, atom_b],
        'conjunction': conjunction,
        'paradox_type': paradox_type,
        'verdict': verdict,
        'appended': appended
    }

if __name__ == '__main__':
    result = run_autonomous_encounter()
    print(result)
