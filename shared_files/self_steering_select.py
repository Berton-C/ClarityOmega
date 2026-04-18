atoms = {
    'morphic-resonance': 0.653, 'self-sustaining-cycle': 0.653, 'substrate-aliveness': 0.653,
    'observer-relativity': 0.653, 'autocatalytic-closure': 0.653, 'pattern-persistence': 0.653,
    'frame-sensitive': 0.653, 'self-weaving-web': 0.653, 'self-model': 0.653,
    'morphic*substrate': 0.672, 'sustaining*weaving': 0.690, 'substrate*autocatalytic': 0.658,
    'resonance-reward->fc-gain': 0.675, 'fc-gain->effort-realloc': 0.731,
    'web-cycle->pattern-persist': 0.657, 'hub-node->substrate-coher': 0.633,
    'fc-gain->revision-priority': 0.675, 'revision-priority->effort': 0.651,
    'effort->fc-gain-detection': 0.719,
    'loop->substrate-aliveness': 0.674, 'self-steering->autonomy': 0.650
}
ranked = sorted(atoms.items(), key=lambda x: x[1])
print('=== SELF-STEERING TARGET SELECTION ===')
print('Atoms ranked by fc (lowest = highest revision priority):')
for i, (name, fc) in enumerate(ranked[:5]):
    print(f'  {i+1}. {name}: fc={fc} <- REVISION TARGET')
print(f'\nSelf-steering selects: {ranked[0][0]} (fc={ranked[0][1]})')
print(f'Mean fc across all 21: {sum(atoms.values())/len(atoms):.3f}')
print(f'Min fc: {ranked[0][1]} Max fc: {ranked[-1][1]}')
print(f'Spread: {ranked[-1][1] - ranked[0][1]:.3f}')
