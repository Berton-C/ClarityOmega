import sys
sys.path.insert(0, '/tmp')
from emotional_sense import sense

tests = [
    'hello',
    'I am terrified',
    'pure gibberish xyz',
    'the',
    'I feel nothing',
    '',
    'money bank account transfer wire',
    'I love you but I am scared',
]

for t in tests:
    r = sense(t)
    print(f'{repr(t):50s} -> {r["emotion"]:10s} conf={r["confidence"]:.4f} cov={r.get("coverage",0):.2f}')
