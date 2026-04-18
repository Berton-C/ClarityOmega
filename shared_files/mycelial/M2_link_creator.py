#!/usr/bin/env python3
import json

LINK_THRESHOLD = 3
LOG_PATH = '/tmp/coretrieval_log.json'
LINK_STORE_PATH = '/tmp/mycelial/link_store.json'

def load_coretrieval_log():
    with open(LOG_PATH) as f:
        return json.load(f)

def extract_qualified_links(log, threshold=LINK_THRESHOLD):
    qualified = []
    for pair_key, cycles in log.get('pairs', {}).items():
        if len(cycles) >= threshold:
            qualified.append({
                'pair': pair_key,
                'co_occurrences': len(cycles),
                'cycles': cycles,
                'strength': min(1.0, len(cycles) / (threshold * 2))
            })
    return qualified

def write_link_store(links):
    store = {'threshold': LINK_THRESHOLD, 'links': links}
    with open(LINK_STORE_PATH, 'w') as f:
        json.dump(store, f, indent=2)
    return store

if __name__ == '__main__':
    log = load_coretrieval_log()
    links = extract_qualified_links(log)
    store = write_link_store(links)
    print(f'Created {len(links)} links at threshold {LINK_THRESHOLD}:')
    for link in links:
        print(f'  {link["pair"]} strength={link["strength"]:.2f} ({link["co_occurrences"]} co-occurrences)')
