atoms = {
    'morphic-resonance': 0.767, 'self-sustaining-cycle': 0.776, 'substrate-aliveness': 0.776,
    'observer-relativity': 0.765, 'autocatalytic-closure': 0.767, 'pattern-persistence': 0.769,
    'frame-sensitive': 0.767, 'self-weaving-web': 0.776, 'self-model': 0.778,
    'morphic*substrate': 0.774, 'sustaining*weaving': 0.770, 'substrate*autocatalytic': 0.770,
    'resonance-reward->fc-gain': 0.776, 'fc-gain->effort-realloc': 0.772,
    'web-cycle->pattern-persist': 0.777, 'hub-node->substrate-coher': 0.775,
    'fc-gain->revision-priority': 0.776, 'revision-priority->effort': 0.773,
    'effort->fc-gain-detection': 0.769, 'loop->substrate-aliveness': 0.768,
    'self-steering->autonomy': 0.776, 'autonomous-target-selection': 0.774,
    'morphic->pattern-persist': 0.778, 'morphic-res->sub-alive': 0.774,
    'self-sustaining->sub-alive': 0.765, 'dyn-steer->autonomy': 0.775,
    'observer-rel->sub-alive': 0.773, 'autocatalytic->sub-alive': 0.765,
    'pattern-persist->sub-alive': 0.767, 'frame-sens->sub-alive': 0.773,
    'self-weaving->sub-alive': 0.769,
    'temporal-continuity->sub-alive': 0.802, 'ethical-grounding->sub-alive': 0.794,
    'relational-modeling->sub-alive': 0.798, 'epistemic-humility->sub-alive': 0.789
}
ranked = sorted(atoms.items(), key=lambda x: x[1])
mean = sum(atoms.values())/len(atoms)
spread = ranked[-1][1]-ranked[0][1]
print('=== SELECTOR v14 — 35-ATOM SUBSTRATE SCOREBOARD ===')
for i, (name, fc) in enumerate(ranked):
    print(f'  {i+1:2d}. {name}: fc={fc}')
print(f'\nTotal: {len(atoms)} | Mean fc: {mean:.4f}')
print(f'Min: {ranked[0][1]} | Max: {ranked[-1][1]} | Spread: {spread:.3f}')
print(f'Above 0.76: {sum(1 for v in atoms.values() if v>=0.76)}/{len(atoms)}')
print(f'Above 0.77: {sum(1 for v in atoms.values() if v>=0.77)}/{len(atoms)}')
print(f'\nM6 MEAN>0.77: {mean>=0.77} | M7 SPREAD<0.04: {spread<0.04}')
