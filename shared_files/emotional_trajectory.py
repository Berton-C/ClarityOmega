import sys
sys.path.insert(0, '/tmp')
from conversation_handler_v2 import handle_turn

class EmotionalTrajectory:
    def __init__(self):
        self.history = []
        self.window = 5

    def add_turn(self, text, speaker):
        result = handle_turn(text, speaker)
        v, a, d = result['vad']
        entry = {'text': text[:80], 'speaker': speaker, 'valence': v, 'arousal': a, 'dominance': d, 'mode': result['mode']}
        self.history.append(entry)
        return entry

    def trajectory(self):
        recent = self.history[-self.window:]
        if len(recent) < 2:
            return {'direction': 'insufficient', 'entries': len(recent)}
        v_delta = recent[-1]['valence'] - recent[0]['valence']
        a_delta = recent[-1]['arousal'] - recent[0]['arousal']
        v_dir = 'rising' if v_delta > 0.1 else ('falling' if v_delta < -0.1 else 'stable')
        a_dir = 'escalating' if a_delta > 0.1 else ('settling' if a_delta < -0.1 else 'steady')
        return {'valence_direction': v_dir, 'arousal_direction': a_dir, 'v_delta': round(v_delta, 3), 'a_delta': round(a_delta, 3), 'turns': len(recent), 'current_mode': recent[-1]['mode']}

if __name__ == '__main__':
    t = EmotionalTrajectory()
    convo = [('I feel so lost and confused', 'human'), ('Maybe something feels different now', 'human'), ('I think I feel a little hope actually', 'human')]
    for text, speaker in convo:
        entry = t.add_turn(text, speaker)
        print(str(speaker) + ': v=' + str(round(entry['valence'],2)) + ' a=' + str(round(entry['arousal'],2)) + ' mode=' + str(entry['mode']))
    print()
    traj = t.trajectory()
    print('Trajectory: valence ' + traj['valence_direction'] + ' arousal ' + traj['arousal_direction'])
    print('Emotional trajectory tracking operational')
