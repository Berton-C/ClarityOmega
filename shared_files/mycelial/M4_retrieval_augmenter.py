#!/usr/bin/env python3
import json
from M4_spreading_activation import load_graph, spread_activation

def augment_retrieval(query_results, graph=None):
    if graph is None:
        graph = load_graph()
    seed_nodes = [r['id'] for r in query_results]
    seed_scores = [r.get('similarity', 0.5) for r in query_results]
    activation_map = dict(spread_activation(graph, seed_nodes, seed_scores))
    augmented = []
    seen = set()
    for r in query_results:
        rid = r['id']
        graph_boost = activation_map.get(rid, 0) - r.get('similarity', 0.5)
        augmented.append({
            'id': rid,
            'similarity': r.get('similarity', 0.5),
            'graph_boost': max(0, graph_boost),
            'combined': r.get('similarity', 0.5) + max(0, graph_boost) * 0.3,
            'source': 'direct'
        })
        seen.add(rid)
    for node, score in activation_map.items():
        if node not in seen and score >= 0.15:
            augmented.append({
                'id': node,
                'similarity': 0.0,
                'graph_boost': score,
                'combined': score * 0.3,
                'source': 'graph-activated'
            })
    augmented.sort(key=lambda x: -x['combined'])
    return augmented

if __name__ == '__main__':
    mock_results = [
        {'id': 'g1', 'similarity': 0.85},
        {'id': 'br1', 'similarity': 0.60}
    ]
    print('Mock retrieval results:', mock_results)
    augmented = augment_retrieval(mock_results)
    print('\nAugmented results:')
    for r in augmented:
        print(f"  {r['id']}: sim={r['similarity']:.3f} boost={r['graph_boost']:.3f} combined={r['combined']:.3f} [{r['source']}]")
