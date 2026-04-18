#!/usr/bin/env python3
import json, sys

MODE_GUIDANCE = {
    'empathic-attunement': 'Lead with acknowledgment. Reflect their feeling before problem-solving. Slow pace.',
    'collaborative-exploration': 'Match their energy. Build on their ideas. Ask catalytic questions.',
    'grounding-presence': 'Steady tone. Short sentences. Anchor to what is concrete and real.',
    'witnessing-celebration': 'Name what you see emerging. Honor the momentum. Affirm agency.',
    'gentle-activation': 'Offer one small next step. Warm tone. Do not overwhelm.',
    'momentum-amplification': 'Ride the wave. Expand scope. Connect this energy to larger vision.',
    'stabilizing-presence': 'Hold steady. Do not chase the drop. Name what is still solid.',
    'neutral-presence': 'Stay open and attentive. Follow their lead.'
}

def shape(result):
    modes = result.get('modes', ['neutral-presence'])
    guidance = [MODE_GUIDANCE.get(m, '') for m in modes]
    return {'tid': result['tid'], 'modes': modes, 'guidance': guidance,
            'vad': result['vad'], 'shift': result['shift']}

if __name__ == '__main__':
    f = sys.argv[1] if len(sys.argv) > 1 else '/tmp/turn_history.jsonl'
    with open(f) as fh:
        for line in fh:
            if not line.strip(): continue
            r = shape(json.loads(line))
            print('[%s] modes=%s' % (r['tid'], r['modes']))
            for g in r['guidance']:
                print('  >> %s' % g)
            print()
