#!/usr/bin/env python3
# Semantic Uncertainty Detection Layer
# Addresses edge case: resigned/flat text reads as PNS but mind is unsettled
# Layered on top of VAD centroid to catch meaning-level signals

UNCERTAINTY_MARKERS = {
    'dont', 'know', 'anymore', 'confused', 'unsure', 'maybe',
    'whatever', 'guess', 'suppose', 'unclear', 'lost', 'stuck',
    'uncertain', 'struggling', 'wondering', 'doubt', 'hard',
    'difficult', 'cannot', 'cant', 'never', 'nothing', 'nobody'
}

NEGATION_WORDS = {'not', 'dont', 'no', 'never', 'nothing', 'nobody', 'cant', 'cannot', 'wont'}

def semantic_uncertainty_score(text):
    words = text.lower().split()
    if not words:
        return 0.0, 0.0
    unc_count = sum(1 for w in words if w in UNCERTAINTY_MARKERS)
    neg_count = sum(1 for w in words if w in NEGATION_WORDS)
    unc_density = unc_count / len(words)
    neg_density = neg_count / len(words)
    return unc_density, neg_density

def should_override_to_transitional(mode, text, threshold=0.15):
    if mode != 'engaged':
        return False, 'no override needed'
    unc, neg = semantic_uncertainty_score(text)
    if unc >= threshold or neg >= threshold:
        return True, 'semantic uncertainty %.2f negation %.2f overrides engaged to transitional' % (unc, neg)
    return False, 'uncertainty %.2f negation %.2f below threshold' % (unc, neg)

if __name__ == '__main__':
    tests = ['I dont know what to think anymore', 'things are okay I guess', 'I feel peaceful and curious', 'whatever it does not matter', 'I am excited but also nervous']
    for t in tests:
        unc, neg = semantic_uncertainty_score(t)
        print('Text: %s' % t)
        print('  Uncertainty: %.3f  Negation: %.3f' % (unc, neg))
        override, reason = should_override_to_transitional('engaged', t)
        print('  Override engaged? %s - %s' % (override, reason))
        print()
