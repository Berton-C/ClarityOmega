from web_detector import loop_strength, is_autocatalytic, web_report
from completion_tracker import GoalTracker

def integrated_check():
    t = GoalTracker()
    rate = t.completion_rate()
    completion_link_f = max(0.7, min(1.0, rate + 0.1))
    completion_link_c = max(0.6, min(0.9, rate))
    links = [(0.9, 0.8), (0.85, 0.75), (completion_link_f, completion_link_c)]
    names = ['goal->memory', 'memory->new_goal', 'new_goal->completion']
    print('Completion rate:', rate)
    print('Derived completion link: f=%s c=%s' % (completion_link_f, completion_link_c))
    f, c, status = web_report(links, names)
    return rate, f, c, status

if __name__ == '__main__':
    integrated_check()
