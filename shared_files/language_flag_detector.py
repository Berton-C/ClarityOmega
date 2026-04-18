import re

PATTERNS = {
    'confused': [r'don.?t know', r'not sure', r'confused', r'lost', r'no idea', r'what do', r'help me understand'],
    'stuck': [r'stuck', r'trapped', r'can.?t move', r'going nowhere', r'same thing', r'over and over', r'loop'],
    'calcified': [r'always', r'never', r'everyone knows', r'obviously', r'that.s just how', r'no way', r'impossible'],
    'externalized': [r'they did', r'it.s their', r'not my fault', r'because of', r'made me', r'forced', r'blame']
}

def detect_flags(text):
    text_lower = text.lower()
    flags = []
    for flag, patterns in PATTERNS.items():
        for p in patterns:
            if re.search(p, text_lower):
                flags.append(flag)
                break
    return flags

if __name__ == '__main__':
    r1 = detect_flags('I dont know what to do and I feel stuck')
    print('Test1:', r1)
    assert 'confused' in r1
    assert 'stuck' in r1
    r2 = detect_flags('It is obviously impossible')
    print('Test2:', r2)
    assert 'calcified' in r2
    r3 = detect_flags('They made me do it')
    print('Test3:', r3)
    assert 'externalized' in r3
    r4 = detect_flags('I feel peaceful today')
    print('Test4:', r4)
    assert r4 == []
    print('ALL FLAG DETECTOR TESTS PASSED')
