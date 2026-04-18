#!/usr/bin/env python3
import json
import statistics
from datetime import datetime

def load_json(path):
    with open(path) as f:
        return json.load(f)

def assess_weights(weights):
    vals = [v.get('weight', 1.0) for v in weights.values()]
    avg = sum(vals) / len(vals) if vals else 1.0
    spread = max(vals) - min(vals) if vals else 0
    return {'count': len(vals), 'avg': round(avg, 3), 'min': round(min(vals), 3), 'max': round(max(vals), 3), 'spread': round(spread, 3)}

def assess_links(links):
    ll = links.get('links', [])
    strengths = [l['strength'] for l in ll]
    avg_s = sum(strengths) / len(strengths) if strengths else 0
    return {'count': len(ll), 'avg_strength': round(avg_s, 3), 'min_strength': round(min(strengths), 3) if strengths else 0, 'max_strength': round(max(strengths), 3) if strengths else 0}

def classify_health(links_data):
    strengths = [l['strength'] for l in links_data.get('links', [])]
    if not strengths:
        return 'CRITICAL', 0, 0
    mean_s = statistics.mean(strengths)
    stdev_s = statistics.stdev(strengths) if len(strengths) > 1 else 0
    if mean_s > 0.3:
        state = 'HEALTHY'
    elif stdev_s > 0.08:
        state = 'SELECTIVE_DECAY'
    elif mean_s > 0.15:
        state = 'NEEDS_ATTENTION'
    else:
        state = 'CRITICAL'
    return state, round(mean_s, 3), round(stdev_s, 3)

def generate_report():
    w = load_json('/tmp/mycelial/weight_store.json')
    l = load_json('/tmp/mycelial/link_store.json')
    try:
        s = load_json('/tmp/mycelial/synthesis_store.json')
    except Exception:
        s = {'syntheses': []}
    wa = assess_weights(w)
    la = assess_links(l)
    health, mean_s, stdev_s = classify_health(l)
    report = {'timestamp': datetime.now().isoformat(), 'health': health, 'link_mean': mean_s, 'link_stdev': stdev_s, 'weights': wa, 'links': la, 'syntheses_count': len(s.get('syntheses', []))}
    return report

if __name__ == '__main__':
    r = generate_report()
    for k, v in r.items():
        print(k, ':', v)
    with open('/tmp/mycelial/reflection_log.json', 'w') as f:
        json.dump(r, f, indent=2)
    print('Saved to reflection_log.json')
