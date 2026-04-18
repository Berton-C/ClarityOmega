atoms = {
    'morphic-resonance': 0.744, 'self-sustaining-cycle': 0.753, 'substrate-aliveness': 0.753,
    'observer-relativity': 0.741, 'autocatalytic-closure': 0.744, 'pattern-persistence': 0.747,
    'frame-sensitive': 0.744, 'self-weaving-web': 0.753, 'self-model': 0.756,
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
print('=== SELECTOR v4 — NEW FRONTIER ===')
for i, (name, fc) in enumerate(ranked[:10]):
    print(f'  {i+1}. {name}: fc={fc}')
mean = sum(atoms.values())/len(atoms)
print(f'\nTotal: {len(atoms)} | Mean fc: {mean:.3f}')
print(f'Min: {ranked[0][1]} | Max: {ranked[-1][1]} | Spread: {ranked[-1][1]-ranked[0][1]:.3f}')
print(f'Above 0.70: {sum(1 for v in atoms.values() if v>=0.70)}/{len(atoms)}')
print(f'Above 0.74: {sum(1 for v in atoms.values() if v>=0.74)}/{len(atoms)}')
