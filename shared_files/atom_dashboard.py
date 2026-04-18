# Atom Dashboard - current state of all core atoms
atoms = {
    'frame-sensitive': (0.7135, 0.85),
    'substrate-aliveness': (0.693, 0.890),
    'autocatalytic-closure': (0.698, 0.667),
    'observer-relativity': (0.780, 0.780),
    'morphic-resonance': (0.705, 0.77),
    'self-sustaining-cycle': (0.685, 0.80),
    'self-weaving-web': (0.762, 0.612),
    'substrate-to-closure': (0.698, 0.667),
    'morphic-to-aliveness': (0.649, 0.701)
}
print('=== SUBSTRATE ATOM DASHBOARD ===')
for n, (f, c) in sorted(atoms.items(), key=lambda x: x[1][0]*x[1][1]):
    fc = f * c
    status = 'STRONG' if fc > 0.6 else 'ABOVE' if fc > 0.5 else 'WEAK'
    print(f'  {n}: fc={fc:.3f} stv={f:.3f}/{c:.3f} [{status}]')
mean_fc = sum(f*c for f, c in atoms.values()) / len(atoms)
print(f'Mean fc: {mean_fc:.3f}')
print(f'Atoms above 0.6: {sum(1 for f,c in atoms.values() if f*c > 0.6)}/{len(atoms)}')
print(f'Atoms above 0.5: {sum(1 for f,c in atoms.values() if f*c > 0.5)}/{len(atoms)}')
