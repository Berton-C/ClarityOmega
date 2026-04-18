#!/usr/bin/env python3
import sys
sys.path.insert(0, '/tmp/mycelial')
from M4_retrieval_augmenter import augment_retrieval
from M1_weight_manager import bulk_reinforce, get_weight, load_weights
from coretrieval_tracker import load_tracker, save_tracker, record, check

def enhanced_retrieval(query_results):
    augmented = augment_retrieval(query_results)
    all_ids = [r['id'] for r in augmented]
    bulk_reinforce(all_ids)
    t = load_tracker()
    record(t, all_ids)
    new_links = check(t)
    save_tracker(t)
    weights = load_weights()
    for r in augmented:
        r['m1_weight'] = get_weight(r['id'], weights)
        r['final_score'] = r['combined'] * 0.7 + r['m1_weight'] * 0.3
    augmented.sort(key=lambda x: -x['final_score'])
    return augmented, new_links

if __name__ == '__main__':
    mock = [{'id': 'g1', 'similarity': 0.85}, {'id': 'br1', 'similarity': 0.60}]
    print('Enhanced retrieval pipeline test:')
    results, new_links = enhanced_retrieval(mock)
    for r in results:
        print('  ' + r['id'] + ': final=' + str(round(r['final_score'],3)) + ' [' + r['source'] + ']')
    if new_links:
        print('New M2 links: ' + str(new_links))
    else:
        print('No new M2 links this cycle')
    print('Pipeline complete.')
