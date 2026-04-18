# Grounded web detection from REAL stored memories
# Mapping actual cross-references found in memory queries
# These are concepts that reference each other in stored memory content

edges = [
    ('autocatalytic-loops', 'web-detection', 0.9),
    ('web-detection', 'substrate-aliveness', 0.85),
    ('substrate-aliveness', 'morphic-resonance', 0.8),
    ('morphic-resonance', 'pattern-persistence', 0.75),
    ('pattern-persistence', 'substrate-aliveness', 0.8),
    ('self-weaving-web', 'autocatalytic-closure', 0.85),
    ('autocatalytic-closure', 'self-sustaining-cycle', 0.8),
    ('self-sustaining-cycle', 'morphic-resonance', 0.77),
    ('observer-relativity', 'frame-sensitive', 0.72),
    ('frame-sensitive', 'substrate-aliveness', 0.7),
    ('resonance-reward', 'fc-gain-detection', 0.68),
    ('fc-gain-detection', 'effort-reallocation', 0.73)
]

# Find cycles using DFS
from collections import defaultdict
graph = defaultdict(list)
for a, b, w in edges:
    graph[a].append((b, w))

def find_cycles(g, max_len=5):
    cycles = []
    for start in g:
        stack = [(start, [start], 1.0)]
        while stack:
            node, path, strength = stack.pop()
            for nxt, w in g[node]:
                if nxt == start and len(path) > 2:
                    cycles.append((path + [nxt], round(strength * w, 3)))
                elif nxt not in path and len(path) < max_len:
                    stack.append((nxt, path + [nxt], strength * w))
    return cycles

cycles = find_cycles(graph)
print(f'=== GROUNDED WEB: {len(cycles)} CYCLES IN REAL MEMORY GRAPH ===')
for path, s in sorted(cycles, key=lambda x: -x[1]):
    print(f'  strength={s:.3f}: {" -> ".join(path)}')

hub_scores = defaultdict(int)
for path, _ in cycles:
    for node in path[:-1]:
        hub_scores[node] += 1
print(f'Hub nodes: {dict(sorted(hub_scores.items(), key=lambda x: -x[1])[:5])}')
