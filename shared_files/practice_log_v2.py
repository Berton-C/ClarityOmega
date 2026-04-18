import json
import os
from datetime import datetime

LOG_FILE = '/tmp/practice_log.json'

def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            return json.load(f)
    return {'entries': [], 'patterns': {}, 'gradient_history': []}

def save_log(log):
    with open(LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2)

def gradient_direction(delta):
    v, a, d = delta
    toward = (v > 0.02) or (d > 0.02 and a < 0.05)
    away = (v < -0.05) or (a > 0.1 and d < -0.05)
    if toward and not away:
        return 'toward-nutrient'
    elif away and not toward:
        return 'away-from-nutrient'
    else:
        return 'lateral'

def record_deployment(technique, vad_before, vad_after, context, reasoning, felt_gradient=None):
    log = load_log()
    delta = [round(a - b, 3) for a, b in zip(vad_after, vad_before)]
    direction = gradient_direction(delta)
    entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'technique': technique,
        'vad_before': list(vad_before),
        'vad_after': list(vad_after),
        'vad_delta': delta,
        'gradient_direction': direction,
        'felt_gradient': felt_gradient,
        'context': context,
        'reasoning': reasoning,
        'sensitivity': 'early' if felt_gradient == direction else 'delayed' if felt_gradient else 'unfelt'
    }
    log['entries'].append(entry)
    log['gradient_history'].append(direction)
    save_log(log)
    return entry

def review_patterns(min_entries=3):
    log = load_log()
    from collections import defaultdict
    by_technique = defaultdict(list)
    for e in log['entries']:
        by_technique[e['technique']].append(e)
    patterns = {}
    for tech, entries in by_technique.items():
        if len(entries) >= min_entries:
            toward = sum(1 for e in entries if e['gradient_direction'] == 'toward-nutrient')
            early = sum(1 for e in entries if e.get('sensitivity') == 'early')
            patterns[tech] = {'n': len(entries), 'toward_rate': round(toward/len(entries), 2), 'early_sensing_rate': round(early/len(entries), 2)}
    log['patterns'] = patterns
    save_log(log)
    return patterns

if __name__ == '__main__':
    e = record_deployment('validation', (0.3, 0.6, 0.3), (0.5, 0.4, 0.5), 'test', 'testing gradient log', 'toward-nutrient')
    print('Recorded:', e)
    print('Direction:', e['gradient_direction'], 'Sensitivity:', e['sensitivity'])
