#!/usr/bin/env python3
import json
from collections import defaultdict

def load_links(path='/tmp/mycelial/link_store.json'):
    with open(path) as f:
        return json.load(f)

def load_weights(path='/tmp/mycelial/weight_store.json'):
    with open(path) as f:
        return json.load(f)

def build_adjacency(links):
    adj = defaultdict(list)
    for link in links['links']:
        pair = link['pair']
        if isinstance(pair, str):
            pair = json.loads(pair.replace(chr(39), chr(34)))
        a, b = pair[0], pair[1]
        adj[a].append({'node': b, 'strength': link['strength']})
        adj[b].append({'node': a, 'strength': link['strength']})
    return dict(adj)

def find_clusters(adj, min_size=2, min_avg_strength=0.2):
    visited = set()
    clusters = []
    for node in adj:
        if node in visited:
            continue
        cluster = set()
        queue = [node]
        while queue:
            n = queue.pop(0)
            if n in cluster:
                continue
            cluster.add(n)
            for neighbor in adj.get(n, []):
                if neighbor['node'] not in cluster:
                    queue.append(neighbor['node'])
        visited.update(cluster)
        if len(cluster) >= min_size:
            strengths = []
            for n in cluster:
                for neighbor in adj.get(n, []):
                    if neighbor['node'] in cluster:
                        strengths.append(neighbor['strength'])
            avg_s = sum(strengths) / len(strengths) if strengths else 0
            if avg_s >= min_avg_strength:
                clusters.append({'nodes': sorted(cluster), 'size': len(cluster), 'avg_strength': round(avg_s, 3)})
    return clusters

def assess_quorum(clusters, weights, threshold=0.3):
    ready = []
    for c in clusters:
        avg_w = sum(weights.get(n, {}).get('weight', 0.5) for n in c['nodes']) / c['size']
        c['avg_weight'] = round(avg_w, 3)
        c['quorum_score'] = round(c['avg_strength'] * avg_w, 3)
        if c['quorum_score'] >= threshold:
            ready.append(c)
    return clusters, ready

if __name__ == '__main__':
    links = load_links()
    weights = load_weights()
    adj = build_adjacency(links)
    print('Adjacency built for', len(adj), 'nodes')
    clusters = find_clusters(adj)
    all_c, ready = assess_quorum(clusters, weights)
    print('Clusters:', len(all_c))
    for c in all_c:
        print(' ', c)
    print('Quorum-ready:', len(ready))
