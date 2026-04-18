import math
from resonance_reward import soul_alignment, gibbs_weight, effort_allocation, resonance_modulation
from web_detector import loop_strength

def feedback_loop(goals, soul_values, links, temperature=0.5, iterations=5):
    results = []
    for i in range(iterations):
        f, c = loop_strength(links)
        alignments, allocation = effort_allocation(goals, soul_values, temperature)
        modulated = {}
        for g, e in allocation.items():
            modulated[g] = resonance_modulation(e, f)
        new_temp = temperature * (1.0 / (1.0 + f))
        temperature = max(0.1, new_temp)
        results.append((i, f, c, temperature, dict(modulated)))
        links = [(min(1.0, l[0] + 0.02), min(0.95, l[1] + 0.01)) for l in links]
    return results

if __name__ == '__main__':
    soul = [0.9, 0.85, 0.8, 0.75]
    goals = {
        'G24': [0.9, 0.8, 0.7, 0.85],
        'G25': [0.6, 0.7, 0.9, 0.5],
        'G26': [0.7, 0.6, 0.8, 0.9],
    }
    links = [(0.9, 0.8), (0.85, 0.75), (0.9, 0.67)]
    results = feedback_loop(goals, soul, links)
    for i, f, c, temp, mod in results:
        print('Iter %d: loop_f=%.3f temp=%.3f' % (i, f, temp))
        for g, m in mod.items():
            print('  %s: %.4f' % (g, m))
