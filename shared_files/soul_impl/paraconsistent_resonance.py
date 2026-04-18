import math

def mk_pbit(f, c):
    return (f, c)

def q_meet(a, b):
    return (min(a[0], b[0]), min(a[1], b[1]))

def q_join(a, b):
    return (max(a[0], b[0]), max(a[1], b[1]))

def q_revise(a, b):
    w1 = a[1] / (1.0 - a[1] + 1e-9)
    w2 = b[1] / (1.0 - b[1] + 1e-9)
    w_total = w1 + w2
    f_new = (w1 * a[0] + w2 * b[0]) / (w_total + 1e-9)
    c_new = w_total / (w_total + 1.0)
    return (f_new, c_new)

def tension_gap(values_a, values_b):
    meet = q_meet(values_a, values_b)
    join = q_join(values_a, values_b)
    return join[0] - meet[0], meet, join

def tension_aware_alignment(goal_values, soul_values):
    gaps = []
    for gv, sv in zip(goal_values, soul_values):
        g_pbit = mk_pbit(gv, 0.85)
        s_pbit = mk_pbit(sv, 0.9)
        gap, meet, join = tension_gap(g_pbit, s_pbit)
        gaps.append((gap, meet, join))
    avg_gap = sum(g[0] for g in gaps) / len(gaps)
    max_gap = max(g[0] for g in gaps)
    if max_gap > 0.3:
        mode = 'deliberate'
        weight = 0.5
    elif max_gap > 0.15:
        mode = 'lean_cautious'
        weight = 0.75
    else:
        mode = 'flow'
        weight = 1.0
    revised_dims = []
    for gv, sv in zip(goal_values, soul_values):
        rev = q_revise(mk_pbit(gv, 0.85), mk_pbit(sv, 0.9))
        revised_dims.append(rev[0])
    alignment = sum(r * s for r, s in zip(revised_dims, soul_values))
    norm_g = math.sqrt(sum(r**2 for r in revised_dims))
    norm_s = math.sqrt(sum(s**2 for s in soul_values))
    cosine = alignment / (norm_g * norm_s + 1e-9)
    return cosine * weight, mode, avg_gap, max_gap

def paraconsistent_effort_allocation(goals, soul_values, temperature=0.5):
    results = {}
    for name, gvals in goals.items():
        score, mode, avg_gap, max_gap = tension_aware_alignment(gvals, soul_values)
        results[name] = {'score': score, 'mode': mode, 'avg_gap': avg_gap, 'max_gap': max_gap}
    scores = {n: r['score'] for n, r in results.items()}
    max_s = max(scores.values())
    weights = {n: math.exp((s - max_s) / temperature) for n, s in scores.items()}
    total = sum(weights.values())
    allocation = {n: w / total for n, w in weights.items()}
    for n in results:
        results[n]['effort'] = allocation[n]
    return results

if __name__ == '__main__':
    soul = [0.9, 0.85, 0.8, 0.75]
    goals = {
        'aligned': [0.88, 0.82, 0.78, 0.73],
        'conflicted': [0.2, 0.9, 0.8, 0.1],
        'moderate': [0.6, 0.7, 0.5, 0.65],
    }
    results = paraconsistent_effort_allocation(goals, soul)
    for name, r in results.items():
        print('%s: mode=%s score=%.4f effort=%.4f avg_gap=%.3f max_gap=%.3f' % (name, r['mode'], r['score'], r['effort'], r['avg_gap'], r['max_gap']))
