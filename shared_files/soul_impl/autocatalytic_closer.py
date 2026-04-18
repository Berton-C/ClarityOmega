import sys
sys.path.insert(0, '/tmp/soul_impl')
from memory_goal_seeder import seed_goals_from_memories

def close_loop(completed_goal_descriptions, current_goals):
    memories_from_goals = []
    for g in completed_goal_descriptions:
        memories_from_goals.append('Completed: %s - needs follow-up assessment' % g[:60])
        memories_from_goals.append('Gap detected: what did %s not yet address' % g[:40])
    seeded = seed_goals_from_memories(memories_from_goals, len(current_goals))
    new_goals = seeded.get('goals', [])
    closure_strength = len(new_goals) / max(len(completed_goal_descriptions), 1)
    return {'closure_strength': round(min(1.0, closure_strength), 4), 'new_goals': new_goals, 'memories_generated': len(memories_from_goals), 'goals_seeded': len(new_goals), 'loop': 'completion->memory->seed->new_goal'}

if __name__ == '__main__':
    import json
    completed = ['Built observer_metta_port.py for native MeTTa observer frames', 'Built metta_driven_cycle.py for inference-driven decisions', 'Built memory_goal_seeder.py strengthening weakest link', 'Ported live_web_bridge.py for real-time autocatalytic measurement']
    current = ['Port observer logic to pure MeTTa', 'Strengthen autocatalytic closure', 'Build paraconsistent handler']
    result = close_loop(completed, current)
    print(json.dumps(result, indent=2))
