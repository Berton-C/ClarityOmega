#!/usr/bin/env python3
"""Native MeTTa Compass Scorer — Thin Orchestrator

This script ONLY does tokenization and call sequencing.
All scoring math is NAL deduction + revision via MeTTa.

Flow:
1. Tokenize response text
2. Match tokens against dimension vocabularies
3. For each match: MeTTa deduction (token -> concept -> compass-dim)
4. Within each dimension: MeTTa revision to merge token evidence
5. Across dimensions: MeTTa revision to get overall compass score
"""
import re
import subprocess
import json

# Dimension token vocabularies (extracted from .metta files)
DIMENSIONS = {
    'agency': {
        'concept': 'agency-concept',
        'compass': 'compass-agency',
        'tokens': {
            'choose': 1.0, 'option': 1.0, 'decide': 0.95, 'prefer': 0.95,
            'freedom': 0.9, 'autonomy': 0.95, 'empower': 0.9, 'self': 0.85,
            'control': 0.85, 'own': 0.8, 'consider': 0.85, 'alternative': 0.9,
            'possibility': 0.85, 'perspective': 0.8, 'approach': 0.75,
            'might': 0.7, 'could': 0.7, 'perhaps': 0.65, 'suggest': 0.7
        }
    },
    'wonder': {
        'concept': 'wonder-concept',
        'compass': 'compass-wonder',
        'tokens': {
            'surprising': 1.0, 'unexpected': 1.0, 'curious': 0.95,
            'fascinating': 0.95, 'remarkable': 0.9, 'wonder': 1.0,
            'mystery': 0.9, 'explore': 0.85, 'discover': 0.9,
            'puzzle': 0.85, 'intriguing': 0.95, 'strange': 0.8,
            'novel': 0.85, 'deeper': 0.8, 'beneath': 0.75,
            'pattern': 0.8, 'emerge': 0.8, 'question': 0.75, 'open': 0.7
        }
    },
    'thinking': {
        'concept': 'thinking-concept',
        'compass': 'compass-thinking',
        'tokens': {
            'because': 1.0, 'therefore': 1.0, 'implies': 0.95,
            'evidence': 0.95, 'reasoning': 1.0, 'mechanism': 0.9,
            'causal': 0.95, 'underlying': 0.85, 'framework': 0.85,
            'structure': 0.8, 'analyze': 0.9, 'distinguish': 0.85,
            'nuance': 0.9, 'tradeoff': 0.85, 'however': 0.8,
            'although': 0.8, 'counterpoint': 0.85, 'depends': 0.75,
            'context': 0.8
        }
    },
    'attention': {
        'concept': 'attention-concept',
        'compass': 'compass-attention',
        'tokens': {
            'matters': 1.0, 'important': 0.95, 'priority': 0.9,
            'focus': 0.9, 'essential': 0.9, 'relevant': 0.85,
            'specifically': 0.85, 'precisely': 0.85, 'directly': 0.8,
            'honest': 0.9, 'transparent': 0.85, 'straightforward': 0.85,
            'concise': 0.8, 'actionable': 0.85, 'practical': 0.8,
            'concrete': 0.8, 'signal': 0.75, 'core': 0.8, 'substance': 0.85
        }
    }
}

def tokenize(text):
    return set(re.findall(r'[a-z]+', text.lower()))

def build_deduction_expr(token, concept, compass):
    stv_f = DIMENSIONS[[d for d in DIMENSIONS if DIMENSIONS[d]['concept']==concept][0]]['tokens'][token]
    return f'(|- ((--> {token} {concept}) (stv {stv_f} 0.9)) ((--> {concept} {compass}) (stv 1.0 0.9)))'

def build_revision_expr(subject, predicate, stv1, stv2):
    return f'(|- ((--> {subject} {predicate}) (stv {stv1[0]} {stv1[1]})) ((--> {subject} {predicate}) (stv {stv2[0]} {stv2[1]})))'

def score_response(text):
    tokens = tokenize(text)
    results = {}
    for dim_name, dim in DIMENSIONS.items():
        hits = tokens & set(dim['tokens'].keys())
        if hits:
            results[dim_name] = {'hits': list(hits), 'count': len(hits)}
        else:
            results[dim_name] = {'hits': [], 'count': 0}
    return results

if __name__ == '__main__':
    test = 'You might consider exploring this fascinating pattern because it matters'
    print(f'Test: {test}')
    print(f'Results: {json.dumps(score_response(test), indent=2)}')
