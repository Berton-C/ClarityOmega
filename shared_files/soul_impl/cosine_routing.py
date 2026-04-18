# Cosine similarity routing to replace q_meet
from quantale_tensor import PBit, tensor_product
import math

def cosine_sim(a, b):
    dot = a.f * b.f + a.c * b.c
    mag_a = math.sqrt(a.f**2 + a.c**2)
    mag_b = math.sqrt(b.f**2 + b.c**2)
    if mag_a == 0 or mag_b == 0:
        return PBit(0.0, 0.0)
    sim = dot / (mag_a * mag_b)
    conf = min(a.c, b.c)
    return PBit(sim, conf)

if __name__ == '__main__':
    state = tensor_product(tensor_product(PBit(0.3,0.9), PBit(0.8,0.85)), PBit(0.2,0.8))
    targets = [
        ('ethical', tensor_product(tensor_product(PBit(0.7,0.9), PBit(0.3,0.9)), PBit(0.8,0.9))),
        ('creative', tensor_product(tensor_product(PBit(0.8,0.9), PBit(0.7,0.85)), PBit(0.6,0.85))),
        ('web', tensor_product(tensor_product(PBit(0.5,0.9), PBit(0.5,0.9)), PBit(0.5,0.9))),
        ('resonance', tensor_product(tensor_product(PBit(0.4,0.9), PBit(0.6,0.85)), PBit(0.3,0.8))),
    ]
    print(f'State sig: {state}')
    for name, t in sorted(targets, key=lambda x: cosine_sim(state, x[1]).f, reverse=True):
        s = cosine_sim(state, t)
        print(f'  {name}: sim={s.f:.4f} conf={s.c:.4f}')
