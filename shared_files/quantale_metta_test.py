# Quantale composition test - p-bit algebra beyond NAL revision
def q_mul(s1, c1, s2, c2):
    return (s1 * s2, c1 * c2)
def q_join(s1, c1, s2, c2):
    return (max(s1, s2), max(c1, c2))
def q_meet(s1, c1, s2, c2):
    return (min(s1, s2), max(c1, c2))
atoms = {
    'morphic-resonance': (0.787, 0.936),
    'self-sustaining-cycle': (0.770, 0.942),
    'substrate-aliveness': (0.693, 0.890),
    'autocatalytic-to-self-model': (0.759, 0.911),
    'self-weaving-web': (0.773, 0.796)
}
print('=== QUANTALE COMPOSITION ON REAL ATOMS ===')
print('Sequential q-mul compositions:')
for n1 in ['morphic-resonance', 'self-sustaining-cycle']:
    for n2 in ['substrate-aliveness', 'self-weaving-web']:
        s, c = q_mul(*atoms[n1], *atoms[n2])
        print(f'  {n1} * {n2} = PB({s:.3f}, {c:.3f}) fc={s*c:.3f}')
print('Parallel q-join bundles:')
s, c = q_join(*atoms['morphic-resonance'], *atoms['self-sustaining-cycle'])
print(f'  morphic || sustaining = PB({s:.3f}, {c:.3f}) fc={s*c:.3f}')
print('Constraint q-meet probes:')
s, c = q_meet(*atoms['substrate-aliveness'], *atoms['autocatalytic-to-self-model'])
print(f'  substrate & autocatalytic = PB({s:.3f}, {c:.3f}) fc={s*c:.3f}')
print('This is p-bit algebra BEYOND basic NAL revision.')
