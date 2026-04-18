#!/usr/bin/env python3
import sys
sys.path.insert(0, '/tmp/soul_impl')
from accumulator import load_field

def modulate_field(current_field, memory_signals, blend=0.3):
    if current_field is None:
        current_field = [[0.5,0.5]]*9
    if not memory_signals or memory_signals.get('memory_count', 0) == 0:
        return current_field
    v = memory_signals.get('valence', 0.5)
    a = memory_signals.get('arousal', 0.5)
    d = memory_signals.get('dominance', 0.5)
    rd = memory_signals.get('relational_depth', 0.3)
    mem_overlay = [v, a, d, rd, 0.5, 0.5, 0.5, 0.5, 0.5]
    modulated = []
    for i in range(min(len(current_field), 9)):
        s, c = current_field[i]
        m = mem_overlay[i]
        blended_s = s * (1 - blend) + m * blend
        blended_c = min(1.0, c + 0.05 * memory_signals.get('memory_count', 0))
        modulated.append([round(blended_s, 6), round(min(blended_c, 1.0), 6)])
    return modulated

if __name__ == '__main__':
    field = [[0.9,0.9],[0.8,0.9],[0.85,0.9],[0.95,0.9],[0.95,0.9],[0.8,0.9],[0.95,0.9],[0.9,0.9],[0.5,0.9]]
    warm_mem = {'valence': 0.9, 'arousal': 0.5, 'dominance': 0.5, 'relational_depth': 0.8, 'memory_count': 3}
    cold_mem = {'valence': 0.1, 'arousal': 0.7, 'dominance': 0.5, 'relational_depth': 0.3, 'memory_count': 2}
    no_mem = {'valence': 0.5, 'arousal': 0.5, 'dominance': 0.5, 'relational_depth': 0.3, 'memory_count': 0}
    for label, sig in [('warm', warm_mem), ('cold', cold_mem), ('none', no_mem)]:
        r = modulate_field(field, sig)
        print(f'{label}: {[round(x[0],3) for x in r]}')
