# Self-Weaving Web Detection on Real Goal Graph
from quantale_tensor import PBit, q_mul, q_join, q_revise

class GoalNode:
    def __init__(self, gid, name, status, confidence=0.5):
        self.gid = gid
        self.name = name
        self.status = status
        self.confidence = PBit(1.0 if status == 'complete' else 0.5, confidence)
    def __repr__(self):
        return f'G{self.gid}({self.name},{self.status},{self.confidence})'

class FeedsInto:
    def __init__(self, src, dst, strength, evidence):
        self.src = src
        self.dst = dst
        self.weight = PBit(strength, evidence)
    def __repr__(self):
        return f'{self.src.gid}->{self.dst.gid} {self.weight}'

def detect_cycles(edges):
    adj = {}
    edge_map = {}
    for e in edges:
        adj.setdefault(e.src.gid, []).append(e.dst.gid)
        edge_map[(e.src.gid, e.dst.gid)] = e.weight
    cycles = []
    for start in adj:
        visited = set()
        stack = [(start, [start], PBit(1.0, 1.0))]
        while stack:
            node, path, strength = stack.pop()
            for nxt in adj.get(node, []):
                link = edge_map[(node, nxt)]
                new_strength = q_mul(strength, link)
                if nxt == start and len(path) > 1:
                    cycles.append((list(path), new_strength))
                elif nxt not in visited:
                    visited.add(nxt)
                    stack.append((nxt, path + [nxt], new_strength))
    return cycles

if __name__ == '__main__':
    g22 = GoalNode(22, 'quantale-comp', 'complete', 0.95)
    g23 = GoalNode(23, 'web-detection', 'complete', 0.90)
    g24 = GoalNode(24, 'resonance-reward', 'complete', 0.85)
    g27 = GoalNode(27, 'observer-rel', 'active', 0.6)
    g28 = GoalNode(28, 'vad-integration', 'active', 0.7)
    g29 = GoalNode(29, 'autocatalytic', 'pending', 0.4)
    edges = [
        FeedsInto(g22, g28, 0.9, 0.85),
        FeedsInto(g22, g23, 0.85, 0.80),
        FeedsInto(g23, g24, 0.8, 0.75),
        FeedsInto(g24, g29, 0.7, 0.60),
        FeedsInto(g29, g22, 0.6, 0.50),
        FeedsInto(g28, g27, 0.75, 0.65),
        FeedsInto(g27, g29, 0.65, 0.55),
    ]
    print('Goal Graph:')
    for g in [g22,g23,g24,g27,g28,g29]: print(f'  {g}')
    print('\nEdges:')
    for e in edges: print(f'  {e}')
    cycles = detect_cycles(edges)
    print(f'\nDetected {len(cycles)} autocatalytic cycles:')
    for path, s in sorted(cycles, key=lambda x: x[1].f * x[1].c, reverse=True):
        print(f'  {"->" .join(str(n) for n in path)} f={s.f:.4f} c={s.c:.4f} fc={s.f*s.c:.4f}')
