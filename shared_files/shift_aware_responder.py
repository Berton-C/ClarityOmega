import sys
sys.path.insert(0, '/tmp')
from multi_turn_shift_tracker import ShiftTracker
from response_shaper_v2 import MODE_SHAPING

SHIFT_ACKNOWLEDGMENTS = {
    'still-holding': 'I notice something shifted. I am here.',
    'warm-attunement': 'Something changed just now. I am with you.',
    'grounded-witnessing': 'I notice the ground moved. Staying steady here.',
    'spacious-presence': 'The space between us just changed shape. No rush.',
    'open-curious-field': 'Something opened up. I want to follow that.',
    'playful-aliveness': 'Ha - that landed differently. I felt that shift too.',
}

class ShiftAwareResponder:
    def __init__(self):
        self.tracker = ShiftTracker()

    def respond(self, user_text):
        entry = self.tracker.process(user_text)
        context = {'mode': entry['mode'], 'shaping': MODE_SHAPING[entry['mode']]}
        if entry['shift_detected'] and entry['turn'] > 1:
            context['shift_ack'] = SHIFT_ACKNOWLEDGMENTS.get(entry['mode'], '')
            context['transition'] = f"from {entry['prev_mode']} to {entry['mode']}"
        return context

if __name__ == '__main__':
    r = ShiftAwareResponder()
    convo = ['just checking in', 'actually everything fell apart today', 'but somehow talking helps', 'I think I know what to do now', 'haha yeah I am dramatic']
    for t in convo:
        c = r.respond(t)
        ack = c.get('shift_ack', '')
        trans = c.get('transition', 'none')
        print(f"{t}")
        print(f"  mode: {c['mode']} | transition: {trans}")
        if ack:
            print(f"  ACK: {ack}")
        print()
    print('Shift-aware response layer operational')
