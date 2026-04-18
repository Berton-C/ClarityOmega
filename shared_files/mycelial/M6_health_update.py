#!/usr/bin/env python3
# Patch for M6: smarter health classification
# Healthy-selective: high variance in link strengths means some links active some fading
# Problematic-uniform: low variance with low mean means everything dying equally
import json
import statistics

def classify_health(links_data):
    strengths = [l['strength'] for l in links_data['links']]
    mean_s = statistics.mean(strengths)
    stdev_s = statistics.stdev(strengths) if len(strengths) > 1 else 0
    if mean_s > 0.3:
        return 'HEALTHY'
    elif stdev_s > 0.08:
        return 'SELECTIVE_DECAY'
    elif mean_s > 0.15:
        return 'NEEDS_ATTENTION'
    else:
        return 'CRITICAL'

if __name__ == '__main__':
    with open('/tmp/mycelial/link_store.json') as f:
        data = json.load(f)
    health = classify_health(data)
    strengths = [l['strength'] for l in data['links']]
    print('Health:', health)
    print('Mean strength:', round(statistics.mean(strengths), 3))
    print('Stdev:', round(statistics.stdev(strengths), 3) if len(strengths) > 1 else 0)
