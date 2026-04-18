#!/usr/bin/env python3
import sys, json, os
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

def handle_turn(user_text, speaker_id='user'):
    bw = BackboneWorkspace()
    result = bw.process_turn(user_text, speaker_id)
    guidance = []
    for mode in result['modes']:
        if mode in MODE_GUIDANCE:
            guidance.append('[' + mode + '] ' + MODE_GUIDANCE[mode])
    context_block = 'EMOTIONAL CONTEXT FOR THIS RESPONSE:\n'
    context_block += 'User VAD: V=' + str(result['vad'][0]) + ' A=' + str(result['vad'][1]) + ' D=' + str(result['vad'][2]) + '\n'
    context_block += 'Active modes: ' + ', '.join(result['modes']) + '\n'
    context_block += 'Guidance:\n' + '\n'.join(guidance) + '\n'
    context_block += 'Turn: ' + str(result['turn']) + ' Shift: ' + str(result['shift']) + '\n'
    return {'context_block': context_block, 'raw': result}

if __name__ == '__main__':
    tests = ['I feel lost and alone', 'That makes me so angry I could scream', 'I am doing okay just checking in', 'This is incredible news I am thrilled']
    for t in tests:
        print('INPUT:', t)
        r = handle_turn(t)
        print(r['context_block'])
        print('---')
