import json
import os

TRACKER_PATH = '/tmp/revision_patterns.json'

def load_patterns():
    if os.path.exists(TRACKER_PATH):
        with open(TRACKER_PATH) as f:
            return json.load(f)
    return {'gate_triggers': {}, 'technique_issues': {}, 'total_revisions': 0, 'total_passes': 0}

def save_patterns(data):
    with open(TRACKER_PATH, 'w') as f:
        json.dump(data, f, indent=2)

def record_pipeline_result(revision_log, technique_name, passed_clean):
    p = load_patterns()
    if passed_clean:
        p['total_passes'] += 1
    else:
        p['total_revisions'] += 1
    for entry in revision_log:
        if entry.get('source') == 'gate':
            rule = entry.get('rule', 'unknown')
            p['gate_triggers'][rule] = p['gate_triggers'].get(rule, 0) + 1
        if entry.get('source') == 'technique':
            for issue in entry.get('issues', []):
                key = f'{technique_name}:{issue}'
                p['technique_issues'][key] = p['technique_issues'].get(key, 0) + 1
    save_patterns(p)
    return p

def get_top_failures(n=3):
    p = load_patterns()
    all_fails = {}
    all_fails.update(p.get('gate_triggers', {}))
    all_fails.update(p.get('technique_issues', {}))
    sorted_fails = sorted(all_fails.items(), key=lambda x: x[1], reverse=True)
    return sorted_fails[:n]

def get_revision_rate():
    p = load_patterns()
    total = p['total_revisions'] + p['total_passes']
    if total == 0:
        return 0.0
    return p['total_revisions'] / total

if __name__ == '__main__':
    if os.path.exists(TRACKER_PATH):
        os.remove(TRACKER_PATH)
    record_pipeline_result([{'source': 'gate', 'rule': 'too-long-for-distress'}], None, False)
    record_pipeline_result([{'source': 'gate', 'rule': 'too-long-for-distress'}], None, False)
    record_pipeline_result([{'source': 'technique', 'issues': ['contains-advice']}], 'dojo-of-no-direction', False)
    record_pipeline_result([], None, True)
    record_pipeline_result([], None, True)
    print('Top failures:', get_top_failures())
    print('Revision rate:', get_revision_rate())
    assert get_revision_rate() == 0.6
    assert get_top_failures()[0][0] == 'too-long-for-distress'
    print('REVISION PATTERN TRACKER PASSED')
