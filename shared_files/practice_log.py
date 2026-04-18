import json
import os
from datetime import datetime

LOG_FILE = '/tmp/practice_log.json'

def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            return json.load(f)
    return {'entries': [], 'patterns': {}}

def save_log(log):
    with open(LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2)

def record_deployment(technique, vad_before, vad_after, context, reasoning):
    log = load_log()
    delta = tuple(round(a - b, 3) for a, b in zip(vad_after, vad_before))
    entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'technique': technique,
        'vad_before': list(vad_before),
        'vad_after': list(vad_after),
        'vad_delta': list(delta),
        'context': context,
        'reasoning': reasoning,
        'landed': None
    }
    log['entries'].append(entry)
    save_log(log)
    return entry

def review_patterns(min_entries=3):
    log = load_log()
    from collections import defaultdict
    by_technique = defaultdict(list)
    for e in log['entries']:
        by_technique[e['technique']].append(e['vad_delta'])
    patterns = {}
    for tech, deltas in by_technique.items():
        if len(deltas) >= min_entries:
            avg = [round(sum(d[i] for d in deltas)/len(deltas), 3) for i in range(3)]
            patterns[tech] = {'avg_delta': avg, 'n': len(deltas), 'consistent': all(abs(a) > 0.05 for a in avg)}
    log['patterns'] = patterns
    save_log(log)
    return patterns

def get_surviving_patterns(threshold=0.1):
    patterns = review_patterns()
    return {k: v for k, v in patterns.items() if v.get('consistent') and max(abs(a) for a in v['avg_delta']) > threshold}

if __name__ == '__main__':
    e = record_deployment('validation', (0.3, 0.6, 0.3), (0.5, 0.5, 0.4), 'test entry', 'testing the log')
    print('Recorded:', e)
    p = review_patterns(min_entries=1)
    print('Patterns:', p)
