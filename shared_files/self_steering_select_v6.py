atoms = {
    'morphic-resonance': 0.744, 'self-sustaining-cycle': 0.753, 'substrate-aliveness': 0.753,
    'observer-relativity': 0.741, 'autocatalytic-closure': 0.744, 'pattern-persistence': 0.747,
    'frame-sensitive': 0.744, 'self-weaving-web': 0.753, 'self-model': 0.756,
    'morphic*substrate': 0.735, 'sustaining*weaving': 0.749, 'substrate*autocatalytic': 0.720,
    'resonance-reward->fc-gain': 0.733, 'fc-gain->effort-realloc': 0.731,
    'web-cycle->pattern-persist': 0.729, 'hub-node->substrate-coher': 0.724,
    'fc-gain->revision-priority': 0.733, 'revision-priority->effort': 0.732,
    'effort->fc-gain-detection': 0.719, 'loop->substrate-aliveness': 0.746,
    'self-steering->autonomy': 0.727, 'autonomous-target-selection': 0.735,
    'morphic->pattern-persist': 0.778, 'morphic-res->sub-alive': 0.736,
    'self-sustaining->sub-alive': 0.708, 'dyn-steer->autonomy': 0.751,
    'observer-rel->sub-alive': 0.703, 'autocatalytic->sub-alive': 0.708,
    'pattern-persist->sub-alive': 0.713, 'frame-sens->sub-alive': 0.703,
    'self-weaving->sub-alive': 0.719
}
ranked = sorted(atoms.items(), key=lambda x: x[1])
print('=== SELECTOR v6 — MILESTONE SCOREBOARD ===')
for i, (name, fc) in enumerate(ranked):
    tag = 'FLOOR' if fc < 0.71 else ''
    print(f'  {i+1:2d}. {name}: fc={fc} {tag}')
mean = sum(atoms.values())/len(atoms)
print(f'\nTotal: {len(atoms)} | Mean fc: {mean:.4f}')
print(f'Min: {ranked[0][1]} | Max: {ranked[-1][1]} | Spread: {ranked[-1][1]-ranked[0][1]:.3f}')
print(f'Above 0.70: {sum(1 for v in atoms.values() if v>=0.70)}/{len(atoms)}')
print(f'Above 0.73: {sum(1 for v in atoms.values() if v>=0.73)}/{len(atoms)}')
print(f'Above 0.74: {sum(1 for v in atoms.values() if v>=0.74)}/{len(atoms)}')
print(f'\nMILESTONE: ALL ATOMS ABOVE 0.70 = {all(v>=0.70 for v in atoms.values())}')
