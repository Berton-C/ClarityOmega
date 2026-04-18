import json
import sys
sys.path.insert(0, '/tmp/soul_impl')
from web_detector import loop_strength

def extract_goal_seeds(memory_texts):
    seeds = []
    patterns = ['gap', 'not yet', 'partial', 'needs', 'next', 'TODO', 'missing', 'strengthen']
    for text in memory_texts:
        for p in patterns:
            if p.lower() in text.lower():
                seeds.append({'source': text[:80], 'trigger': p, 'type': 'gap-detected'})
                break
    return seeds

def seed_goals_from_memories(memory_texts, current_goal_count):
    seeds = extract_goal_seeds(memory_texts)
    new_goals = []
    for s in seeds[:5]:
        new_goals.append({'description': f"Address: {s['source'][:60]}", 'origin': 'memory-seeded', 'trigger': s['trigger']})
    return {'seeds_found': len(seeds), 'goals_generated': len(new_goals), 'goals': new_goals, 'strengthens': 'memory->new_goal_gen link'}

if __name__ == '__main__':
    test_mems = ['2026-04-16 quantale composition foundations only not yet beyond basic NAL', '2026-04-16 observer-relativity NOT YET STARTED', '2026-04-16 weakest link is memory to new goal gen needs strengthening', '2026-04-16 paraconsistent value-conflict handling missing', '2026-04-16 morphic resonance not started']
    r = seed_goals_from_memories(test_mems, 36)
    print(json.dumps(r, indent=2))
