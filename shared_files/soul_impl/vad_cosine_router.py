# End-to-end VAD routing via cosine similarity
# Wires VAD state through tensor product into cosine routing
from quantale_tensor import PBit, tensor_product
from cosine_routing import cosine_sim

class InferenceStrategy:
    def __init__(self, name, sig, description):
        self.name = name
        self.sig = sig
        self.desc = description

def vad_to_signature(v, a, d):
    return tensor_product(tensor_product(PBit(v, 0.9), PBit(a, 0.85)), PBit(d, 0.8))

def route_vad(v, a, d, strategies):
    state = vad_to_signature(v, a, d)
    scored = []
    for s in strategies:
        sim = cosine_sim(state, s.sig)
        scored.append((s, sim))
    scored.sort(key=lambda x: x[1].f, reverse=True)
    return state, scored

if __name__ == '__main__':
    strategies = [
        InferenceStrategy('empathic-attunement', vad_to_signature(0.2, 0.7, 0.3), 'low-V high-A low-D'),
        InferenceStrategy('grounding-presence', vad_to_signature(0.4, 0.3, 0.5), 'mid-V low-A mid-D'),
        InferenceStrategy('collaborative-exploration', vad_to_signature(0.8, 0.6, 0.7), 'high-V mid-A high-D'),
        InferenceStrategy('witnessing-celebration', vad_to_signature(0.9, 0.8, 0.8), 'high-V high-A high-D'),
        InferenceStrategy('gentle-activation', vad_to_signature(0.5, 0.2, 0.4), 'mid-V low-A mid-D'),
    ]
    test_cases = [
        ('anxious-user', 0.2, 0.8, 0.2),
        ('calm-curious', 0.7, 0.4, 0.6),
        ('elated-confident', 0.9, 0.9, 0.9),
        ('resigned-passive', 0.3, 0.15, 0.2),
        ('frustrated-assertive', 0.25, 0.75, 0.7),
    ]
    for label, v, a, d in test_cases:
        state, ranked = route_vad(v, a, d, strategies)
        top = ranked[0]
        print(f'{label} VAD=({v},{a},{d}) -> {top[0].name} sim={top[1].f:.4f}')
        for s, sim in ranked[1:3]:
            print(f'  runner-up: {s.name} sim={sim.f:.4f}')
        print()
