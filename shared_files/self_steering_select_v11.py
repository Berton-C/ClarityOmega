atoms = {
    'morphic-resonance': 0.767, 'self-sustaining-cycle': 0.753, 'substrate-aliveness': 0.753,
    'observer-relativity': 0.765, 'autocatalytic-closure': 0.767, 'pattern-persistence': 0.769,
    'frame-sensitive': 0.767, 'self-weaving-web': 0.753, 'self-model': 0.756,
    'morphic*substrate': 0.761, 'sustaining*weaving': 0.770, 'substrate*autocatalytic': 0.770,
    'resonance-reward->fc-gain': 0.760, 'fc-gain->effort-realloc': 0.755,
    'web-cycle->pattern-persist': 0.754, 'hub-node->substrate-coher': 0.751,
    'fc-gain->revision-priority': 0.760, 'revision-priority->effort': 0.756,
    'effort->fc-gain-detection': 0.769, 'loop->substrate-aliveness': 0.768,
    'self-steering->autonomy': 0.753, 'autonomous-target-selection': 0.761,
    'morphic->pattern-persist': 0.778, 'morphic-res->sub-alive': 0.758,
    'self-sustaining->sub-alive': 0.765, 'dyn-steer->autonomy': 0.751,
    'observer-rel->sub-alive': 0.760, 'autocatalytic->sub-alive': 0.765,
    'pattern-persist->sub-alive': 0.767, 'frame-sens->sub-alive': 0.760,
    'self-weaving->sub-alive': 0.769,
    'temporal-continuity->sub-alive': 0.802, 'ethical-grounding->sub-alive': 0.794,
    'relational-modeling->sub-alive': 0.798, 'epistemic-humility->sub-alive': 0.789
}
ranked = sorted(atoms.items(), key=lambda x: x[1])
print('=== SELECTOR v11 — 35-ATOM SUBSTRATE SCOREBOARD ===')
for i, (name, fc) in enumerate(ranked):
    print(f'  {i+1:2d}. {name}: fc={fc}')
mean = sum(atoms.values())/len(atoms)
print(f'\nTotal: {len(atoms)} | Mean fc: {mean:.4f}')
print(f'Min: {ranked[0][1]} | Max: {ranked[-1][1]} | Spread: {ranked[-1][1]-ranked[0][1]:.3f}')
print(f'Above 0.75: {sum(1 for v in atoms.values() if v>=0.75)}/{len(atoms)}')
print(f'Above 0.77: {sum(1 for v in atoms.values() if v>=0.77)}/{len(atoms)}')
print(f'\nMILESTONE 5 (35-atom): ALL ABOVE 0.75 = {all(v>=0.75 for v in atoms.values())}')
