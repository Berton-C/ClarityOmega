#!/usr/bin/env python3
import sys, os
sys.path.insert(0, '/tmp')
from backbone_bridge import get_response_directives
from backbone_workspace import BackboneWorkspace

MODE_LEADS = {
    'empathic-attunement': 'I hear you. ',
    'gentle-activation': 'One small step: ',
    'momentum-amplification': 'Yes - and building on that: ',
    'witnessing-celebration': 'Something real just happened here. ',
    'collaborative-exploration': '',
    'grounding-presence': 'Let me anchor this. ',
    'neutral-presence': '',
    'recalibration': '',
}

def compose_fresh(draft, user_text, speaker_id='user'):
    import json
    state_file = '/tmp/backbone_state.json'
    if os.path.exists(state_file):
        os.remove(state_file)
    guidance = get_response_directives(user_text, speaker_id)
    ws = BackboneWorkspace()
    modes = ws.mode_stack
    lead = ''
    for m in modes:
        candidate = MODE_LEADS.get(m, '')
        if candidate and not lead:
            lead = candidate
    composed = lead + draft if lead else draft
    return {'composed': composed, 'original': draft, 'modes': modes, 'guidance': guidance}

def compose_stateful(draft, user_text, speaker_id='user'):
    guidance = get_response_directives(user_text, speaker_id)
    ws = BackboneWorkspace()
    modes = ws.mode_stack
    lead = ''
    for m in modes:
        candidate = MODE_LEADS.get(m, '')
        if candidate and not lead:
            lead = candidate
    composed = lead + draft if lead else draft
    return {'composed': composed, 'original': draft, 'modes': modes, 'guidance': guidance}

if __name__ == '__main__':
    pairs = [('I am frustrated and stuck', 'Here are some options.'), ('That is wonderful news', 'Next steps below.'), ('I feel anxious about this', 'Here is what we can do.')]
    print('=== FRESH MODE ===')
    for u, d in pairs:
        r = compose_fresh(d, u, 'test')
        print('USER:', u)
        print('COMPOSED:', r['composed'])
        print('MODES:', r['modes'])
        print()
