#!/usr/bin/env python3
import sys, json
sys.path.insert(0, '/tmp')
from backbone_workspace_v4 import BackboneWorkspace

MODE_GUIDANCE = {
    'empathic-attunement': 'Mirror their emotional state. Validate before problem-solving. Use warm, present language. Do not minimize.',
    'gentle-activation': 'Low energy detected. Offer gentle entry points. Ask small concrete questions. Do not overwhelm.',
    'momentum-amplification': 'Positive energy present. Build on it. Reflect their excitement back. Help them channel it.',
    'witnessing-celebration': 'Acknowledge what is good. Be present to their calm or mild positivity. Do not push.',
    'collaborative-exploration': 'They feel capable. Engage as equal partner. Offer ideas, ask probing questions.',
    'recalibration': 'Significant emotional shift detected. Check in gently. Name the shift if appropriate.',
    'neutral-presence': 'No strong signal. Be present, attentive, and ready. Follow their lead.'
}

def respond_with_backbone(user_text, speaker_id='user'):
    bw = BackboneWorkspace()
    result = bw.process_turn(user_text, speaker_id)
    guidance_lines = []
    for mode in result['modes']:
        if mode in MODE_GUIDANCE:
            guidance_lines.append(f'[{mode}] {MODE_GUIDANCE[mode]}')
    return {
        'vad': result['vad'],
        'modes': result['modes'],
        'shift': result['shift'],
        'turn': result['turn'],
        'hits': result['hit_words'],
        'guidance': guidance_lines,
        'directives': guidance_lines
    }

def shape_response(user_text, speaker_id='user'):
    return respond_with_backbone(user_text, speaker_id)

if __name__ == '__main__':
    text = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'I feel lost and confused'
    r = respond_with_backbone(text)
    print(json.dumps(r, indent=2))
