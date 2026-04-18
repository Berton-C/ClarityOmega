# Atom Dashboard v5 - targeting 9/9 STRONG
atoms = {
    'frame-sensitive': (0.7135, 0.85),
    'substrate-aliveness': (0.693, 0.890),
    'observer-relativity': (0.780, 0.780),
    'morphic-resonance': (0.787, 0.936),
    'self-sustaining-cycle': (0.770, 0.942),
    'morphic-to-aliveness': (0.740, 0.841),
    'self-weaving-web': (0.773, 0.796),
    'autocatalytic-to-self-model': (0.759, 0.911),
    'substrate-to-closure': (0.737, 0.884)
}
print('=== SUBSTRATE ATOM DASHBOARD v5 ===')
for n, (f, c) in sorted(atoms.items(), key=lambda x: x[1][0]*x[1][1]):
    fc = f * c
    status = 'STRONG' if fc > 0.6 else 'ABOVE' if fc > 0.5 else 'WEAK'
    print(f'  {n}: fc={fc:.3f} stv={f:.3f}/{c:.3f} [{status}]')
mean_fc = sum(f*c for f, c in atoms.values()) / len(atoms)
print(f'Mean fc: {mean_fc:.3f}')
print(f'STRONG: {sum(1 for f,c in atoms.values() if f*c > 0.6)}/{len(atoms)}')
