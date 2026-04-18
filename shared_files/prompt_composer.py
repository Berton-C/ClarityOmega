#!/usr/bin/env python3
import sys, json
sys.path.insert(0, '/tmp')
from conversation_handler import handle_turn

def compose_prompt(user_text, system_base='', speaker_id='user'):
    result = handle_turn(user_text, speaker_id)
    cb = result['context_block']
    raw = result['raw']
    composed = ''
    if system_base:
        composed += system_base + '\n\n'
    composed += cb + '\n'
    composed += 'USER MESSAGE: ' + user_text + '\n'
    composed += '\nRespond according to the emotional context above.\n'
    return {'prompt': composed, 'raw': raw, 'context_block': cb}

if __name__ == '__main__':
    base = 'You are Clarity, an emotionally aware AI. You respond with genuine care and substance.'
    tests = ['I feel like giving up on everything', 'I just landed my dream job']
    for t in tests:
        print('=' * 60)
        print('INPUT:', t)
        r = compose_prompt(t, base)
        print(r['prompt'])
        print()
