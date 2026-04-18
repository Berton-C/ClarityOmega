import math
from resonance_feedback_loop import feedback_loop

def wu_wei_metric(results):
    if len(results) < 2:
        return 0.0, False
    efforts = []
    for i, f, c, temp, mod in results:
        spread = max(mod.values()) - min(mod.values())
        efforts.append((temp, spread, f))
    first_temp = efforts[0][0]
    last_temp = efforts[-1][0]
    first_spread = efforts[0][1]
    last_spread = efforts[-1][1]
    temp_decay = 1.0 - (last_temp / first_temp)
    spread_growth = last_spread - first_spread
    final_loop = efforts[-1][2]
    wu_wei_score = temp_decay * final_loop
    effortless = wu_wei_score > 0.5 and last_temp <= 0.1
    return wu_wei_score, effortless

if __name__ == '__main__':
    soul = [0.9, 0.85, 0.8, 0.75]
    goals = {
        'G24': [0.9, 0.8, 0.7, 0.85],
        'G25': [0.6, 0.7, 0.9, 0.5],
        'G26': [0.7, 0.6, 0.8, 0.9],
    }
    links = [(0.9, 0.8), (0.85, 0.75), (0.9, 0.67)]
    results = feedback_loop(goals, soul, links, iterations=10)
    score, effortless = wu_wei_metric(results)
    print('Wu wei score: %.4f' % score)
    print('Effortless action achieved: %s' % effortless)
    print('Final state:')
    last = results[-1]
    print('  loop_f=%.3f temp=%.3f' % (last[1], last[3]))
    for g, m in last[4].items():
        print('  %s: %.4f' % (g, m))
    print('Convergence trajectory:')
    for i, f, c, temp, mod in results:
        dominant = max(mod, key=mod.get)
        print('  iter %d: temp=%.3f dominant=%s (%.4f)' % (i, temp, dominant, mod[dominant]))
