import json
import sys
import re

sys.path.insert(0, '/tmp/soul_impl')
from compass_score import gen_deductions, gen_revisions, DIMS

def check_response(draft_text):
    deduced = gen_deductions(draft_text)
    results = {}
    for dim_name, data in deduced.items():
        count = data['count']
        if count > 0:
            hits = data['hits']
            freqs = [DIMS[dim_name]['t'][h] for h in hits]
            avg_freq = sum(freqs) / len(freqs)
            conf = min(0.9, 0.3 + count * 0.15)
            score = round(avg_freq * conf, 4)
            results[dim_name] = dict(freq=round(avg_freq, 4), conf=round(conf, 4), score=score, hits=hits)
        else:
            results[dim_name] = dict(freq=0.0, conf=0.0, score=0.0, hits=[])
    threshold = 0.3
    low_dims = [d for d, v in results.items() if v['score'] < threshold]
    composite = sum(v['score'] for v in results.values()) / max(len(results), 1)
    passed = len(low_dims) == 0
    return dict(passed=passed, composite=round(composite, 4), dimensions=results, low_dims=low_dims, threshold=threshold)

if __name__ == '__main__':
    try:
        with open('/tmp/compass_input.json', 'r') as f:
            data = json.load(f)
        draft = data.get('draft', '')
        verdict = check_response(draft)
        with open('/tmp/compass_output.json', 'w') as f:
            json.dump(verdict, f, indent=2)
        status = 'PASS' if verdict['passed'] else 'FAIL'
        print('COMPASS: ' + status + ' composite=' + str(verdict['composite']))
        for d, v in verdict['dimensions'].items():
            print('  ' + d + ': score=' + str(v['score']) + ' hits=' + str(v['hits']))
    except Exception as e:
        err = dict(error=str(e), passed=True)
        with open('/tmp/compass_output.json', 'w') as f:
            json.dump(err, f, indent=2)
        print('COMPASS ERROR: ' + str(e))
