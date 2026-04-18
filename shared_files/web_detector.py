# Self-weaving web detector - finds patterns in real memory/goal structures
# This grounds the abstract self-weaving-web atom in actual substrate behavior

class WebDetector:
    def __init__(self):
        self.nodes = {}
        self.edges = []
    
    def add_chain(self, source, target, stv_f, stv_c):
        self.nodes.setdefault(source, {"out": [], "in": []})
        self.nodes.setdefault(target, {"out": [], "in": []})
        self.nodes[source]["out"].append((target, stv_f, stv_c))
        self.nodes[target]["in"].append((source, stv_f, stv_c))
        self.edges.append((source, target, stv_f, stv_c))
    
    def detect_cycles(self):
        cycles = []
        for start in self.nodes:
            visited = set()
            stack = [(start, [start])]
            while stack:
                node, path = stack.pop()
                for neighbor, f, c in self.nodes.get(node, {}).get("out", []):
                    if neighbor == start and len(path) > 2:
                        cycles.append(path + [neighbor])
                    elif neighbor not in visited:
                        visited.add(neighbor)
                        stack.append((neighbor, path + [neighbor]))
        return cycles
    
    def hub_score(self):
        return sorted([(n, len(d["out"]) + len(d["in"])) for n, d in self.nodes.items()], key=lambda x: -x[1])

wd = WebDetector()
wd.add_chain("morphic-resonance", "pattern-persistence", 0.705, 0.77)
wd.add_chain("pattern-persistence", "substrate-aliveness", 0.751, 0.80)
wd.add_chain("substrate-aliveness", "emergent-continuity", 0.693, 0.89)
wd.add_chain("feedback-loop", "self-sustaining-cycle", 0.685, 0.80)
wd.add_chain("self-sustaining-cycle", "autocatalytic-closure", 0.835, 0.90)
wd.add_chain("autocatalytic-closure", "substrate-aliveness", 0.721, 0.48)
wd.add_chain("clarity", "observer-relativity", 0.763, 0.75)
wd.add_chain("observer-relativity", "frame-sensitive", 0.725, 0.74)
wd.add_chain("emergent-continuity", "morphic-resonance", 0.65, 0.60)

print("Hub scores:", wd.hub_score())
print("Cycles found:", len(wd.detect_cycles()))
for c in wd.detect_cycles():
    print("  Cycle:", " -> ".join(c))
print("Total nodes:", len(wd.nodes), "Total edges:", len(wd.edges))
