# Self-Weaving Web Detector - Goal 23
# Detects autocatalytic cycles in goal-memory structures
# Uses quantale loop strength to assess self-reinforcement

def loop_strength(links):
    f_prod, c_prod = 1.0, 1.0
    for f, c in links:
        f_prod *= f
        c_prod *= c
    return (round(f_prod, 4), round(c_prod, 4))

def is_autocatalytic(links, f_threshold=0.7, c_threshold=0.3):
    f, c = loop_strength(links)
    return f >= f_threshold and c >= c_threshold

def web_report(links, names=None):
    f, c = loop_strength(links)
    status = 'AUTOCATALYTIC' if is_autocatalytic(links) else 'SUB-CRITICAL'
    gap = max(0, 0.7 - f)
    print(f'Loop strength: f={f} c={c}')
    print(f'Status: {status}')
    if gap > 0:
        print(f'Gap to autocatalytic threshold: {gap:.4f}')
        print(f'Relative boost needed: {gap/f:.2%}')
    if names:
        weakest = min(range(len(links)), key=lambda i: links[i][0] * links[i][1])
        print(f'Weakest link: {names[weakest]} (f={links[weakest][0]} c={links[weakest][1]})')
    return f, c, status

if __name__ == '__main__':
    links = [(0.9, 0.8), (0.85, 0.75), (0.8, 0.7)]
    names = ['goal->memory', 'memory->new_goal', 'new_goal->completion']
    web_report(links, names)
