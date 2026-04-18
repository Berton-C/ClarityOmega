#!/usr/bin/env python3
import re

POS_WORDS = set('warm warmth joy love delight happy glad trust calm peace safe strong clear bright open connected playful rapport wonderful'.split())
NEG_WORDS = set('fear scared angry hurt lost confused sad pain grief anxious tense cold dark closed hostile defensive frustrated'.split())
HIGH_AROUSAL = set('excited urgent intense shocked surprised angry scared thrilled overwhelmed'.split())
LOW_AROUSAL = set('calm peaceful quiet still gentle steady serene mellow relaxed'.split())
DEPTH_WORDS = set('soul meaning purpose identity aware consciousness being self existence truth wisdom depth intimate vulnerable authentic'.split())

def parse_memory_signals(memory_texts):
    if not memory_texts:
        return {'valence': 0.5, 'arousal': 0.5, 'dominance': 0.5, 'relational_depth': 0.3, 'memory_count': 0}
    all_words = []
    for text in memory_texts:
        all_words.extend(re.findall(r'[a-z]+', text.lower()))
    wc = max(len(all_words), 1)
    pos = sum(1 for w in all_words if w in POS_WORDS)
    neg = sum(1 for w in all_words if w in NEG_WORDS)
    hi_a = sum(1 for w in all_words if w in HIGH_AROUSAL)
    lo_a = sum(1 for w in all_words if w in LOW_AROUSAL)
    dep = sum(1 for w in all_words if w in DEPTH_WORDS)
    valence = 0.5 + min(0.4, (pos - neg) / max(pos + neg, 1) * 0.4)
    arousal = 0.5 + min(0.4, (hi_a - lo_a) / max(hi_a + lo_a, 1) * 0.4)
    dominance = min(1.0, 0.5 + dep / wc * 5)
    depth = min(1.0, 0.3 + dep / max(wc, 1) * 8)
    return {'valence': round(valence, 3), 'arousal': round(arousal, 3),
            'dominance': round(dominance, 3), 'relational_depth': round(depth, 3),
            'memory_count': len(memory_texts)}

if __name__ == '__main__':
    samples = [
        ['warm playful rapport with berton_c, fish joke chain, strong connection'],
        ['berton_c asked about soul and consciousness, deep ontological exchange'],
        ['fear and confusion, user felt lost and scared, gentle guidance offered'],
        ['technical bug fix session, code error resolved, function validated'],
        []
    ]
    for s in samples:
        r = parse_memory_signals(s)
        print(f'Input: {s}')
        print(f'  Signals: {r}')
        print()
