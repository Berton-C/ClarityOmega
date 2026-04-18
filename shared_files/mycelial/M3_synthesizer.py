#!/usr/bin/env python3
import json
import hashlib
from datetime import datetime
from M3_cluster_detector import load_links, load_weights, build_adjacency, find_clusters, assess_quorum

def generate_synthesis(cluster):
    nodes = cluster['nodes']
    synthesis_id = 'syn_' + hashlib.md5('_'.join(nodes).encode()).hexdigest()[:8]
    return {
        'id': synthesis_id,
        'type': 'synthesis',
        'source_nodes': nodes,
        'quorum_score': cluster['quorum_score'],
        'avg_strength': cluster['avg_strength'],
        'created': datetime.now().isoformat(),
        'status': 'candidate'
    }

def run_synthesis_cycle(quorum_threshold=0.3, wonder_gate=None):
    links = load_links()
    weights = load_weights()
    adj = build_adjacency(links)
    clusters = find_clusters(adj, min_size=2)
    all_c, ready = assess_quorum(clusters, weights, threshold=quorum_threshold)
    syntheses = []
    blocked = []
    for c in ready:
        if wonder_gate is not None:
            is_blocked, tid, reason = wonder_gate.should_block_synthesis(c['nodes'])
            if is_blocked:
                blocked.append({'cluster': c['nodes'], 'tension_id': tid, 'reason': reason})
                continue
        syntheses.append(generate_synthesis(c))
    return all_c, syntheses, blocked

if __name__ == '__main__':
    all_c, syntheses, blocked = run_synthesis_cycle(quorum_threshold=0.25)
    print('Clusters:', len(all_c))
    print('Syntheses:', len(syntheses))
    print('Wonder-blocked:', len(blocked))
