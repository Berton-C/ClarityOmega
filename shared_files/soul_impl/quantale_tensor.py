# Quantale P-Bit Tensor Products
# Real algebraic composition, not just NAL revision

import math

class PBit:
    def __init__(self, freq, conf):
        self.f = max(0.0, min(1.0, freq))
        self.c = max(0.0, min(1.0, conf))
    def __repr__(self):
        return f'PBit({self.f:.4f}, {self.c:.4f})'

def tensor_product(a: PBit, b: PBit) -> PBit:
    """Tensor product: joint composition of two p-bits.
    Frequency: product (both must be true)
    Confidence: product (independent evidence combines)"""
    return PBit(a.f * b.f, a.c * b.c)

def tensor_sum(a: PBit, b: PBit) -> PBit:
    """Tensor sum (co-product): either-or composition.
    Frequency: probabilistic OR
    Confidence: minimum (weakest link)"""
    return PBit(a.f + b.f - a.f * b.f, min(a.c, b.c))

def q_mul(a: PBit, b: PBit) -> PBit:
    """Quantale multiplication: sequential composition."""
    return PBit(a.f * b.f, a.c * b.c)

def q_join(a: PBit, b: PBit) -> PBit:
    """Quantale join: parallel bundling (supremum)."""
    return PBit(max(a.f, b.f), max(a.c, b.c))

def q_meet(a: PBit, b: PBit) -> PBit:
    """Quantale meet: filtering (infimum)."""
    return PBit(min(a.f, b.f), min(a.c, b.c))

def q_revise(a: PBit, b: PBit) -> PBit:
    """NAL revision: evidence merge."""
    w1 = a.c / (1 - a.c) if a.c < 1 else 1e6
    w2 = b.c / (1 - b.c) if b.c < 1 else 1e6
    w = w1 + w2
    new_f = (w1 * a.f + w2 * b.f) / w if w > 0 else 0.5
    new_c = w / (w + 1)
    return PBit(new_f, new_c)

# === TENSOR PRODUCT TESTS ===
if __name__ == '__main__':
    # VAD dimensions as p-bits
    valence = PBit(0.3, 0.9)   # low valence (negative emotion)
    arousal = PBit(0.8, 0.85)  # high arousal
    dominance = PBit(0.2, 0.8) # low dominance
    
    # Tensor product: joint emotional signature
    va = tensor_product(valence, arousal)
    vad = tensor_product(va, dominance)
    print(f'Valence: {valence}')
    print(f'Arousal: {arousal}')
    print(f'Dominance: {dominance}')
    print(f'V tensor A: {va}')
    print(f'V tensor A tensor D: {vad}')
    
    # Tensor sum: disjunctive emotional state
    va_sum = tensor_sum(valence, arousal)
    print(f'V tensorsum A: {va_sum}')
    
    # Full algebra verification
    print(f'\nAlgebra verification:')
    a, b, c = PBit(0.7, 0.9), PBit(0.5, 0.8), PBit(0.6, 0.85)
    ab_c = tensor_product(tensor_product(a, b), c)
    a_bc = tensor_product(a, tensor_product(b, c))
    print(f'Associativity: (a*b)*c = {ab_c}, a*(b*c) = {a_bc}')
    print(f'Match: {abs(ab_c.f - a_bc.f) < 1e-10 and abs(ab_c.c - a_bc.c) < 1e-10}')
