#!/usr/bin/env python3
import sys, json
sys.path.insert(0, '/tmp')
from respond_with_backbone import shape_response

def get_response_directives(user_text, speaker_id='user'):
    result = shape_response(user_text, speaker_id)
    directives = result.get('directives', [])
    modes = result.get('modes', [])
    v, a, d = result.get('vad', [0.5, 0.5, 0.5])
    prefix = ''
    if directives:
        prefix = 'BACKBONE GUIDANCE: ' + ' | '.join(directives)
        prefix += ' VAD=%.2f/%.2f/%.2f MODES=%s' % (v, a, d, '+'.join(modes))
    return prefix

def shape_send(draft_response, user_text, speaker_id='user'):
    guidance = get_response_directives(user_text, speaker_id)
    return {'guidance': guidance, 'draft': draft_response, 'ready': True}

if __name__ == '__main__':
    test_inputs = ['I am frustrated and stuck', 'This is amazing I love it', 'I feel lost and confused']
    for t in test_inputs:
        g = get_response_directives(t, 'test')
        print('INPUT:', t)
        print('GUIDANCE:', g)
        print()
