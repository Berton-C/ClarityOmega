#!/usr/bin/env python3
import json, sys

MODE_GUIDANCE = {
    'empathic-attunement': 'Lead with acknowledgment. Reflect feeling before solving. Slow pace.',
    'collaborative-exploration': 'Match energy. Build on ideas. Ask catalytic questions.',
    'grounding-presence': 'Steady tone. Short sentences. Anchor to concrete and real.',
    'witnessing-celebration': 'Name what is emerging. Honor momentum. Affirm agency.',
    'gentle-activation': 'Offer one small next step. Warm tone. Do not overwhelm.',
    'momentum-amplification': 'Ride the wave. Expand scope. Connect to larger vision.',
    'stabilizing-presence': 'Hold steady. Do not chase the drop. Name what is still solid.',
    'neutral-presence': 'Stay open and attentive. Follow their lead.'
}

def get_latest_guidance(history_file='/tmp/turn_history.jsonl'):
    last = None
    try:
        with open(history_file) as f:
            for line in f:
                if line.strip():
                    last = json.loads(line)
    except FileNotFoundError:
        return {'modes': ['neutral-presence'], 'guidance': ['Stay open and attentive.']}
    if not last:
        return {'modes': ['neutral-presence'], 'guidance': ['Stay open and attentive.']}
    modes = last.get('modes', ['neutral-presence'])
    guidance = [MODE_GUIDANCE.get(m, '') for m in modes]
    return {'tid': last.get('tid',''), 'modes': modes, 'guidance': guidance, 'vad': last.get('vad',[0,0,0]), 'shift': last.get('shift',0)}

if __name__ == '__main__':
    r = get_latest_guidance()
    print('BACKBONE GUIDANCE FOR NEXT RESPONSE:')
    print('  Last turn: %s' % r.get('tid','unknown'))
    print('  Modes: %s' % r['modes'])
    print('  VAD: %s  Shift: %s' % (r.get('vad'), r.get('shift')))
    for g in r['guidance']:
        print('  >> %s' % g)
