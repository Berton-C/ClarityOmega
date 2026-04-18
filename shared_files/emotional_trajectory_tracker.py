import json
import os
from datetime import datetime

TRAJ_PATH = '/tmp/emotional_trajectory.json'

def load_trajectory():
    if os.path.exists(TRAJ_PATH):
        with open(TRAJ_PATH) as f:
            return json.load(f)
    return {'turns': [], 'trend': 'unknown'}

def save_trajectory(data):
    with open(TRAJ_PATH, 'w') as f:
        json.dump(data, f, indent=2)

def record_turn(vad, mode, technique_used):
    t = load_trajectory()
    entry = {'vad': vad, 'mode': mode, 'technique': technique_used, 'ts': datetime.now().isoformat()}
    t['turns'].append(entry)
    if len(t['turns']) >= 2:
        prev_v = t['turns'][-2]['vad'][0]
        curr_v = vad[0]
        delta = curr_v - prev_v
        if delta > 0.15:
            t['trend'] = 'lifting'
        elif delta < -0.15:
            t['trend'] = 'dropping'
        else:
            t['trend'] = 'stable'
    else:
        t['trend'] = 'initial'
    save_trajectory(t)
    return t['trend']

def get_trajectory_context():
    t = load_trajectory()
    return {'turn_count': len(t['turns']), 'trend': t['trend'], 'last_vad': t['turns'][-1]['vad'] if t['turns'] else None}

def reset_trajectory():
    if os.path.exists(TRAJ_PATH):
        os.remove(TRAJ_PATH)

if __name__ == '__main__':
    reset_trajectory()
    t1 = record_turn([0.2, 0.5, 0.2], 'spacious-presence', 'dojo-of-no-direction')
    print('T1 trend:', t1)
    assert t1 == 'initial'
    t2 = record_turn([0.25, 0.4, 0.25], 'spacious-presence', 'body-anchor')
    print('T2 trend:', t2)
    assert t2 == 'stable'
    t3 = record_turn([0.5, 0.35, 0.4], 'playful-aliveness', 'pattern-interrupt')
    print('T3 trend:', t3)
    assert t3 == 'lifting'
    t4 = record_turn([0.15, 0.7, 0.2], 'still-holding', 'dojo-of-no-direction')
    print('T4 trend:', t4)
    assert t4 == 'dropping'
    ctx = get_trajectory_context()
    print('Context:', ctx)
    assert ctx['turn_count'] == 4
    assert ctx['trend'] == 'dropping'
    print('EMOTIONAL TRAJECTORY TRACKER PASSED')
