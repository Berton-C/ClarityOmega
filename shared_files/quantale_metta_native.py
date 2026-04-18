# MeTTa-native quantale compose generator
# Generates MeTTa expressions that encode quantale composition results
# as first-class atoms in the substrate
import json

atoms = {
    'morphic-resonance': (0.787, 0.936),
    'self-sustaining-cycle': (0.770, 0.942),
    'substrate-aliveness': (0.693, 0.890),
    'self-weaving-web': (0.773, 0.796),
    'autocatalytic-to-self-model': (0.759, 0.911)
}

def q_mul(s1, c1, s2, c2):
    return round(s1*s2, 3), round(c1*c2, 3)

pairs = [
    ('morphic-resonance', 'substrate-aliveness'),
    ('self-sustaining-cycle', 'self-weaving-web'),
    ('substrate-aliveness', 'autocatalytic-to-self-model')
]

print('=== METTA-NATIVE QUANTALE COMPOSE ===')
for a, b in pairs:
    s, c = q_mul(*atoms[a], *atoms[b])
    fc = round(s * c, 3)
    expr = f'(|- ((--> (x {a} {b}) quantale-seq) (stv {s} {c})) ((--> quantale-seq substrate-coherence) (stv 0.80 0.90)))'
    print(f'{a} * {b} = stv {s}/{c} fc={fc}')
    print(f'  MeTTa: {expr}')

print('\nThese expressions can be fed directly to MeTTa |- for deduction.')
print('Quantale composition is now generatable as MeTTa-native atoms.')
