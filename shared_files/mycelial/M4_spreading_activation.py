#!/usr/bin/env python3
import json
from collections import defaultdict

LINK_STORE_PATH = '/tmp/mycelial/link_store.json'
DECAY_FACTOR = 0.5
ACTIVATION_THRESHOLD = 0.1
MAX_DEPTH = 2

def load_graph():
    with open(LINK_STORE_PATH) as f:
        store = json.load(f)
    graph = defaultdict(list)
    for link in store['links']:
        pair = eval(link['pair'])
        strength = link['strength']
        graph[pair[0]].append((pair[1], strength))
        graph[pair[1]].append((pair[0], strength))
    return graph

def spread_activation(graph, seed_nodes, seed_scores):
    activation = dict(zip(seed_nodes, seed_scores))
    frontier = list(seed_nodes)
    for depth in range(MAX_DEPTH):
        next_frontier = []
        decay = DECAY_FACTOR ** (depth + 1)
        for node in frontier:
            for neighbor, strength in graph.get(node, []):
                boost = activation[node] * strength * decay
                if boost >= ACTIVATION_THRESHOLD:
                    old = activation.get(neighbor, 0)
                    activation[neighbor] = max(old, old + boost)
                    if neighbor not in frontier:
                        next_frontier.append(neighbor)
        frontier = next_frontier
    return sorted(activation.items(), key=lambda x: -x[1])

if __name__ == '__main__':
    graph = load_graph()
    print('Graph adjacency:')
    for node, edges in graph.items():
        print(f'  {node}: {edges}')
    seeds = ['g1']
    scores = [1.0]
    print(f'\nSpreading from {seeds} with scores {scores}:')
    result = spread_activation(graph, seeds, scores)
    for node, score in result:
        print(f'  {node}: {score:.3f}')
    print(f'\nSpreading from ["b1"] with scores [1.0]:')
    result2 = spread_activation(graph, ['b1'], [1.0])
    for node, score in result2:
        print(f'  {node}: {score:.3f}')
