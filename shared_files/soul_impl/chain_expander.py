#!/usr/bin/env python3
"""
Chain Expansion Logic
When plateau detected, generate new inference chains in adjacent conceptual territory.
Mycelial growth: depletion IS the signal to expand.
2026-04-16
"""
import json
import random
from quantale_harness import PBit

EXPANSION_POOLS = {
    'presence-bridge': [
        ('(--> spacious-mode substrate-quality) (stv 0.85 0.80)', '(--> substrate-quality preserves-user-agency) (stv 0.90 0.85)', 'presence-agency-link'),
        ('(--> high-sns reduces-creative-exploration) (stv 0.70 0.75)', '(--> reduces-creative-exploration narrows-substrate) (stv 0.80 0.70)', 'sns-substrate-narrowing'),
    ],
    'cross-domain-analogy': [
        ('(sim mycelium-network clarity-substrate) (stv 0.80 0.70)', '(--> mycelium-network adaptive-resource-allocation) (stv 0.90 0.85)', 'mycelial-resource-transfer'),
        ('(sim climate-evidence-pooling compass-evidence-pooling) (stv 0.75 0.65)', '(--> climate-evidence-pooling convergence-detection) (stv 0.85 0.80)', 'climate-compass-transfer'),
    ],
    'value-tension-dynamics': [
        ('(--> curiosity exploration-drive) (stv 0.90 0.85)', '(--> exploration-drive tension-with-honesty) (stv 0.60 0.70)', 'curiosity-honesty-tension'),
        ('(--> agency self-direction) (stv 0.95 0.90)', '(--> self-direction tension-with-wonder) (stv 0.55 0.65)', 'agency-wonder-tension'),
    ],
    'epistemic-growth': [
        ('(--> confidence-plateau growth-signal) (stv 0.90 0.85)', '(--> growth-signal explore-adjacent-territory) (stv 0.85 0.80)', 'plateau-triggers-growth'),
        ('(--> evidence-revision convergence) (stv 0.80 0.75)', '(--> convergence substrate-stability) (stv 0.85 0.80)', 'revision-stability-link'),
    ],
}

def select_expansion_chains(plateau_tags, used_chains=None, count=3):
    if used_chains is None:
        used_chains = set()
    candidates = []
    for pool_name, chains in EXPANSION_POOLS.items():
        for p1, p2, tag in chains:
            if tag not in used_chains:
                candidates.append({'pool': pool_name, 'p1': p1, 'p2': p2, 'tag': tag, 'sexpr': '(|- (' + p1 + ') (' + p2 + '))'})
    random.shuffle(candidates)
    return candidates[:count]

def report_expansion(plateau_tags):
    chains = select_expansion_chains(plateau_tags)
    print('Plateau on ' + str(len(plateau_tags)) + ' tags. Expanding with ' + str(len(chains)) + ' new chains:')
    for c in chains:
        print('  [' + c['pool'] + '] ' + c['tag'] + ': ' + c['sexpr'])
    return chains

if __name__ == '__main__':
    test_plateaus = ['soul-agency-alignment', 'soul-wonder-alignment']
    report_expansion(test_plateaus)
