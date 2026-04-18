#!/usr/bin/env python3
"""Compass Semantic Scorer v1.0
Replaces keyword heuristic with weighted concept proximity.
Each compass dimension has a semantic neighborhood: a cluster of
concepts with proximity weights. Scoring uses best-match proximity
rather than exact keyword hit, making evaluation more robust.

Intermediate step between keyword matching and full embeddings.
"""
import re
from collections import defaultdict

# Semantic neighborhoods per compass dimension
# Format: {concept: proximity_weight} where 1.0 = core concept
AGENCY_NEIGHBORHOOD = {
    'option': 1.0, 'options': 1.0, 'choice': 1.0, 'choose': 0.95,
    'decide': 0.9, 'decision': 0.9, 'alternative': 0.85, 'alternatively': 0.85,
    'path': 0.8, 'paths': 0.8, 'approach': 0.8, 'approaches': 0.8,
    'could': 0.75, 'might': 0.7, 'consider': 0.85, 'weigh': 0.8,
    'tradeoff': 0.85, 'tradeoffs': 0.85, 'preference': 0.8,
    'autonomy': 0.9, 'empower': 0.9, 'yours': 0.7, 'you': 0.3,
    'freedom': 0.8, 'control': 0.75, 'direction': 0.7,
    'what matters': 0.9, 'up to you': 0.95, 'your call': 0.95,
}

WONDER_NEIGHBORHOOD = {
    'insight': 1.0, 'discovery': 1.0, 'surprising': 0.95, 'surprised': 0.9,
    'unexpected': 0.95, 'notice': 0.8, 'interesting': 0.9, 'fascinating': 0.95,
    'curious': 0.9, 'curiosity': 0.9, 'wonder': 1.0, 'remarkable': 0.9,
    'beautiful': 0.8, 'elegant': 0.85, 'mystery': 0.85, 'mysterious': 0.85,
    'explore': 0.8, 'revelation': 0.95, 'pattern': 0.7, 'emerge': 0.75,
    'emergent': 0.8, 'depth': 0.7, 'nuance': 0.8, 'subtle': 0.75,
    'what if': 0.85, 'imagine': 0.8, 'open': 0.5, 'possibility': 0.8,
    'novel': 0.85, 'fresh': 0.7, 'uncharted': 0.9, 'wow': 0.8,
}

THINKING_NEIGHBORHOOD = {
    'because': 0.85, 'therefore': 0.9, 'implies': 0.9, 'means': 0.75,
    'framework': 0.95, 'principle': 0.9, 'structure': 0.8, 'logic': 0.9,
    'reasoning': 0.95, 'evidence': 0.95, 'argument': 0.85, 'analysis': 0.9,
    'pattern': 0.8, 'mechanism': 0.85, 'causation': 0.9, 'causal': 0.9,
    'distinction': 0.85, 'differentiate': 0.8, 'nuance': 0.75,
    'hypothesis': 0.9, 'theory': 0.85, 'model': 0.8, 'explain': 0.8,
    'why': 0.7, 'how': 0.5, 'root cause': 0.95, 'underlying': 0.8,
    'consequent': 0.85, 'follows': 0.75, 'given that': 0.8,
    'clarify': 0.7, 'precisely': 0.75, 'specifically': 0.7,
}

ATTENTION_SIGNALS = {
    'menu': -0.8, 'status update': -0.7, 'filler': -0.9,
    'as an ai': -0.6, 'i cannot': -0.4, 'however': -0.2,
    'in conclusion': -0.3, 'to summarize': -0.2,
    'important to note': -0.5, 'it should be noted': -0.5,
    'basically': -0.4, 'essentially': -0.3, 'literally': -0.3,
}

def _tokenize(text):
    return re.findall(r'[a-z]+', text.lower())

def _bigrams(tokens):
    return [tokens[i] + ' ' + tokens[i+1] for i in range(len(tokens)-1)]

def _score_dimension(text, neighborhood):
    tokens = _tokenize(text)
    bigrams = _bigrams(tokens)
    all_grams = tokens + bigrams
    hits = []
    for gram in all_grams:
        if gram in neighborhood:
            hits.append(neighborhood[gram])
    if not hits:
        return 0.25
    top_hits = sorted(hits, reverse=True)[:5]
    score = sum(top_hits) / len(top_hits)
    breadth_bonus = min(0.15, len(hits) * 0.03)
    return min(1.0, 0.2 + score * 0.6 + breadth_bonus)

def _score_attention(text, word_count):
    lower = text.lower()
    penalties = []
    for signal, weight in ATTENTION_SIGNALS.items():
        if signal in lower:
            penalties.append(weight)
    length_penalty = max(-0.4, -(word_count - 200) / 500.0) if word_count > 200 else 0
    has_question = '?' in text
    base = 0.7
    penalty_sum = sum(penalties)
    question_bonus = 0.1 if has_question else 0
    concise_bonus = 0.15 if word_count < 80 else (0.05 if word_count < 150 else 0)
    return max(0.1, min(1.0, base + penalty_sum + length_penalty + question_bonus + concise_bonus))

def evaluate_response(draft_response, situation_guidance=None):
    tokens = _tokenize(draft_response)
    wc = len(tokens)
    agency = _score_dimension(draft_response, AGENCY_NEIGHBORHOOD)
    wonder = _score_dimension(draft_response, WONDER_NEIGHBORHOOD)
    thinking = _score_dimension(draft_response, THINKING_NEIGHBORHOOD)
    attention = _score_attention(draft_response, wc)
    scores = {
        'agency': round(agency, 3),
        'wonder': round(wonder, 3),
        'thinking': round(thinking, 3),
        'attention': round(attention, 3),
    }
    composite = sum(scores.values()) / 4.0
    flags = [k for k, v in scores.items() if v < 0.4]
    return {
        'compass_scores': scores,
        'composite': round(composite, 3),
        'flags': flags,
        'pass': len(flags) == 0,
        'method': 'semantic_proximity_v1',
    }

if __name__ == '__main__':
    tests = [
        'Here are your options: A, B, or C. What matters most to you?',
        'Status update: everything is fine. Menu: 1) help 2) quit',
        'That is a genuinely interesting pattern. It implies something surprising about how memory shapes presence.',
        'You could consider this alternative approach. The underlying mechanism reveals an elegant structure.',
        'I have completed the task as requested.',
        'This is a fascinating discovery that challenges the hypothesis. The evidence suggests a deeper causal pattern we had not anticipated. What if we explore this further?',
    ]
    for t in tests:
        r = evaluate_response(t)
        print(f'Text: {t[:70]}...')
        print(f'  Scores: {r["compass_scores"]}')
        print(f'  Composite: {r["composite"]} Pass: {r["pass"]} Flags: {r["flags"]}')
        print()
