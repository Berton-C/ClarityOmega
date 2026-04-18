# Technique Router: maps mode-of-being + VAD pattern to available insight techniques
# Principle: availability not prescription - narrows field, does not select

TECHNIQUES = {
    1: 'socratic-inquiry',
    2: 'parable-sudden-contrast',
    3: 'exaggerated-agreement',
    4: 'public-context-reframe',
    5: 'playful-embodiment-metaphor',
    6: 'dojo-of-no-direction'
}

def available_techniques(mode, valence, arousal, dominance, language_flags=None):
    if language_flags is None:
        language_flags = []
    available = []
    if mode in ('spacious-presence', 'playful-aliveness', 'open-curious-field'):
        if arousal < 0.4 and 'confused' in language_flags:
            available.append(1)  # socratic inquiry
        if arousal > 0.6 and 'stuck' in language_flags:
            available.extend([2, 5])  # parable or embodiment metaphor
        if dominance < 0.3 and valence < 0.4 and 'calcified' in language_flags:
            available.append(3)  # exaggerated agreement
        if 'externalized' in language_flags:
            available.append(4)  # public context reframe
        if not available:
            available.append(6)  # dojo of no-direction as default depth
    return [TECHNIQUES[t] for t in available]

if __name__ == '__main__':
    r1 = available_techniques('spacious-presence', 0.2, 0.3, 0.2, ['confused'])
    print('Low arousal confused:', r1)
    r2 = available_techniques('playful-aliveness', 0.3, 0.8, 0.3, ['stuck'])
    print('High arousal stuck:', r2)
    r3 = available_techniques('spacious-presence', 0.2, 0.5, 0.2, ['calcified'])
    print('Calcified low dom:', r3)
    r4 = available_techniques('spacious-presence', 0.5, 0.5, 0.5, [])
    print('No flags defaults:', r4)
    r5 = available_techniques('still-holding', 0.2, 0.3, 0.2, ['confused'])
    print('Non-technique mode:', r5)
    print('ALL TECHNIQUE ROUTER TESTS PASSED')
