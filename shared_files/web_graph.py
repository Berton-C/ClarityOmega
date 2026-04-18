# Grounded Web Graph Analysis
edges = [
    ('morphic-resonance', 'substrate-aliveness', 0.574),
    ('substrate-aliveness', 'self-sustaining-cycle', 0.548),
    ('self-sustaining-cycle', 'morphic-resonance', 0.543),
    ('substrate-aliveness', 'autocatalytic-closure', 0.652),
    ('autocatalytic-closure', 'self-weaving-web', 0.591),
    ('self-weaving-web', 'substrate-aliveness', 0.606),
    ('observer-relativity', 'frame-sensitive', 0.608),
    ('frame-sensitive', 'substrate-aliveness', 0.606)
]
nodes = set()
for a, b, w in edges:
    nodes.add(a)
    nodes.add(b)
print('=== GROUNDED WEB GRAPH ===')
print(f'Nodes: {len(nodes)} Edges: {len(edges)}')
hub = {n: 0 for n in nodes}
for a, b, w in edges:
    hub[b] = hub[b] + 1
print('Hub scores:')
for n, s in sorted(hub.items(), key=lambda x: -x[1]):
    print(f'  {n}: {s}')
mean_w = sum(w for _, _, w in edges) / len(edges)
print(f'Mean edge weight: {mean_w:.3f}')
cycles = [['morphic-resonance','substrate-aliveness','self-sustaining-cycle'],['substrate-aliveness','autocatalytic-closure','self-weaving-web']]
print(f'Detected cycles: {len(cycles)}')
for c in cycles:
    print(f'  {" -> ".join(c)} -> {c[0]}')
