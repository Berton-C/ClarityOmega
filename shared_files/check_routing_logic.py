#!/usr/bin/env python3
cases = [
    ('hopeless+angry', -2.568, -0.744, -1.68),
    ('wonderful+joy', 0.931, 0.2, 0.248),
    ('calm+peaceful', 0.397, -2.453, -1.333),
    ('falling apart+cope', -1.672, -0.889, -1.266),
]
print('V midpoint approx -1.0, A midpoint approx -0.85')
print('Empathic-attunement: very negative V with arousal above midpoint')
print()
for name, v, a, d in cases:
    print(f'{name}: V={v} A={a} D={d}')
    modes = []
    if v < -1.5 and a > -0.85:
        modes.append('empathic-attunement')
    elif v < -1.0:
        modes.append('gentle-activation')
    if v > 0.3 and a > -0.85:
        modes.append('momentum-amplification')
    elif v > -0.3:
        modes.append('witnessing-celebration')
    if d > -0.3:
        modes.append('collaborative-exploration')
    if a < -1.5:
        modes.append('gentle-activation')
    if not modes:
        modes.append('neutral-presence')
    print(f'  -> {modes}')
    print()
