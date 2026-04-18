import json
import sys
sys.path.insert(0, '/tmp/soul_impl')
from web_detector import loop_strength, is_autocatalytic, web_report

def compute_live_links(goal_data, memory_count, new_goal_count):
    total = goal_data.get('total', 1)
    completed = goal_data.get('completed', 0)
    completion_rate = completed / max(total, 1)
    memory_per_goal = memory_count / max(completed, 1)
    mem_strength = min(1.0, memory_per_goal / 10.0)
    goal_gen_rate = new_goal_count / max(completed, 1)
    gen_strength = min(1.0, goal_gen_rate)
    link_gc_to_mem = (min(0.95, 0.5 + completion_rate * 0.45), min(0.9, 0.4 + completion_rate * 0.5))
    link_mem_to_gen = (min(0.95, 0.4 + mem_strength * 0.55), min(0.85, 0.3 + mem_strength * 0.55))
    link_gen_to_comp = (min(0.95, 0.3 + gen_strength * 0.65), min(0.85, 0.3 + gen_strength * 0.55))
    return [link_gc_to_mem, link_mem_to_gen, link_gen_to_comp]

def live_web_check(goal_data, memory_count, new_goal_count):
    links = compute_live_links(goal_data, memory_count, new_goal_count)
    names = ['goal_completion->memory', 'memory->new_goal_gen', 'new_goal_gen->completion']
    f, c, status = web_report(links, names)
    return {'links': links, 'names': names, 'f': f, 'c': c, 'status': status, 'source': 'live-memory-bridge'}

if __name__ == '__main__':
    gd = {'total': 36, 'completed': 30, 'active': 6}
    r = live_web_check(gd, memory_count=180, new_goal_count=24)
    print(json.dumps({k: str(v) for k, v in r.items()}, indent=2))
