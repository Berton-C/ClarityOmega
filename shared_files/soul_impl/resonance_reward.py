import math

def soul_alignment(goal_values, soul_values):
    dot = sum(g * s for g, s in zip(goal_values, soul_values))
    mag_g = math.sqrt(sum(g**2 for g in goal_values))
    mag_s = math.sqrt(sum(s**2 for s in soul_values))
    if mag_g == 0 or mag_s == 0:
        return 0.0
    return dot / (mag_g * mag_s)

def gibbs_weight(alignment, temperature=1.0):
    return math.exp(alignment / temperature)

def effort_allocation(goals, soul_values, temperature=0.5):
    alignments = {g: soul_alignment(gv, soul_values) for g, gv in goals.items()}
    weights = {g: gibbs_weight(a, temperature) for g, a in alignments.items()}
    total = sum(weights.values())
    allocation = {g: w / total for g, w in weights.items()}
    return alignments, allocation

def resonance_modulation(base_effort, loop_strength, decay=0.1):
    return base_effort * (1.0 + loop_strength * (1.0 - decay))

if __name__ == '__main__':
    soul = [0.9, 0.85, 0.8, 0.75]
    goals = {
        'G24-resonance': [0.9, 0.8, 0.7, 0.85],
        'G25-observer': [0.6, 0.7, 0.9, 0.5],
        'G26-paraconsistent': [0.7, 0.6, 0.8, 0.9],
    }
    alignments, allocation = effort_allocation(goals, soul, temperature=0.5)
    print('Soul alignment scores:')
    for g, a in alignments.items():
        print('  %s: %.4f' % (g, a))
    print('Effort allocation (Gibbs-tilted):')
    for g, e in allocation.items():
        modulated = resonance_modulation(e, 0.765)
        print('  %s: base=%.4f resonance-modulated=%.4f' % (g, e, modulated))
