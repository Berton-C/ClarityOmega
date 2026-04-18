import json

THRESHOLDS = {
    'agency': 0.4,
    'wonder': 0.3,
    'thinking': 0.3,
    'attention': 0.4,
}

def compass_gate(scores):
    flags = []
    for dim, thresh in THRESHOLDS.items():
        s = scores.get(dim, {})
        f = s.get('f', 0.0)
        c = s.get('c', 0.0)
        if f < thresh and c > 0.7:
            flags.append(dim)
    return {
        'pass': len(flags) == 0,
        'flags': flags,
        'scores': scores,
    }

if __name__ == '__main__':
    test = {'agency': {'f': 0.775, 'c': 0.895, 'hits': 3}, 'wonder': {'f': 0.875, 'c': 0.895, 'hits': 2}, 'thinking': {'f': 1.0, 'c': 0.81, 'hits': 1}, 'attention': {'f': 1.0, 'c': 0.81, 'hits': 1}}
    result = compass_gate(test)
    print('GATE:', json.dumps(result, indent=2))
    assert result['pass'] == True
    print('Gate test passed')
