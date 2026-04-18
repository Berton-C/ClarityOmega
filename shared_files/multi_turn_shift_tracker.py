import sys
sys.path.insert(0, '/tmp')
from agent_loop_mode_protocol import full_turn_pipeline

class ShiftTracker:
    def __init__(self):
        self.history = []
        self.SHIFT_THRESHOLD = 0.25

    def process(self, user_text):
        result = full_turn_pipeline(user_text)
        prev_mode = self.history[-1]['mode'] if self.history else None
        prev_vad = self.history[-1]['vad'] if self.history else result['vad']
        v, a, d = result['vad']
        pv, pa, pd = prev_vad
        delta = ((v-pv)**2 + (a-pa)**2 + (d-pd)**2)**0.5
        shift = delta > self.SHIFT_THRESHOLD
        mode_changed = prev_mode is not None and prev_mode != result['mode']
        entry = dict(result)
        entry['turn'] = len(self.history) + 1
        entry['delta'] = round(delta, 3)
        entry['shift_detected'] = shift
        entry['mode_changed'] = mode_changed
        entry['prev_mode'] = prev_mode
        self.history.append(entry)
        return entry

if __name__ == '__main__':
    tracker = ShiftTracker()
    convo = [
        'just checking in',
        'actually I have been struggling',
        'I feel like nobody listens',
        'wait you actually get it',
        'that means a lot to me',
    ]
    for t in convo:
        r = tracker.process(t)
        flag = 'SHIFT' if r['shift_detected'] else '     '
        mc = 'MODE-CHANGE' if r['mode_changed'] else ''
        print(f"Turn {r['turn']} [{flag}] {mc} {r['mode']:25s} delta={r['delta']:.3f} | {t}")
    print('Multi-turn shift tracking operational')
