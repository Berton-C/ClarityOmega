from vote_gate_bridge import fallback_vote
cases = [
    ('4-0', {'a-p':1.0,'c-r':1.0,'a-s':1.0,'e-b':1.0}),
    ('3-1', {'a-p':1.0,'c-r':1.0,'a-s':0.0,'e-b':1.0}),
    ('2-2', {'a-p':1.0,'c-r':1.0,'a-s':0.0,'e-b':0.0}),
    ('1-3', {'a-p':1.0,'c-r':0.0,'a-s':0.0,'e-b':0.0}),
    ('0-4', {'a-p':0.0,'c-r':0.0,'a-s':0.0,'e-b':0.0}),
]
for name, t in cases:
    r = fallback_vote(t)
    print(f"{name}: {r['verdict']} f={r['frequency']} c={r['confidence']}")
