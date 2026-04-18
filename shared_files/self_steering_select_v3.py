atoms = {
    'morphic-resonance': 0.653, 'self-sustaining-cycle': 0.653, 'substrate-aliveness': 0.653,
    'observer-relativity': 0.653, 'autocatalytic-closure': 0.653, 'pattern-persistence': 0.653,
    'frame-sensitive': 0.653, 'self-weaving-web': 0.653, 'self-model': 0.653,
    'morphic*substrate': 0.672, 'sustaining*weaving': 0.690, 'substrate*autocatalytic': 0.658,
    'resonance-reward->fc-gain': 0.675, 'fc-gain->effort-realloc': 0.731,
    'web-cycle->pattern-persist': 0.657, 'hub-node->substrate-coher': 0.724,
    'fc-gain->revision-priority': 0.675, 'revision-priority->effort': 0.732,
    'effort->fc-gain-detection': 0.719, 'loop->substrate-aliveness': 0.674,
    'self-steering->autonomy': 0.727, 'autonomous-target-selection': 0.670,
    'morphic->pattern-persist': 0.778, 'morphic-res->sub-alive': 0.673,
    'self-sustaining->sub-alive': 0.708, 'dyn-steer->autonomy': 0.695,
    'observer-rel->sub-alive': 0.703, 'autocatalytic->sub-alive': 0.708,
    'pattern-persist->sub-alive': 0.713, 'frame-sens->sub-alive': 0.703,
    'self-weaving->sub-alive': 0.719
}
ranked = sorted(atoms.items(), key=lambda x: x[1])
print('=== SELF-STEERING SELECTOR v3 — FLOOR CHECK ===')
print('Top 5 revision targets (lowest fc):')
for i, (name, fc) in enumerate(ranked[:5]):
    print(f'  {i+1}. {name}: fc={fc}')
print(f'\nMean fc across all {len(atoms)}: {sum(atoms.values())/len(atoms):.3f}')
print(f'Min fc: {ranked[0][1]} Max fc: {ranked[-1][1]}')
print(f'Spread: {ranked[-1][1] - ranked[0][1]:.3f}')
strong = sum(1 for v in atoms.values() if v >= 0.6)
print(f'STRONG atoms: {strong}/{len(atoms)}')
print(f'Atoms above 0.70: {sum(1 for v in atoms.values() if v >= 0.70)}/{len(atoms)}')
