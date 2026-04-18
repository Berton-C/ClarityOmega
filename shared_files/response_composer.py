#!/usr/bin/env python3
import json, sys, os
sys.path.insert(0, '/tmp')
from backbone_bridge import get_response_directives

MODE_ADJUSTMENTS = {
    'empathic-attunement': {'prefix_tone': 'I hear you.', 'pace': 'slow', 'lead_with': 'acknowledgment'},
    'gentle-activation': {'prefix_tone': '', 'pace': 'slow', 'lead_with': 'one_small_step'},
    'momentum-amplification': {'prefix_tone': '', 'pace': 'fast', 'lead_with': 'build_on_energy'},
    'witnessing-celebration': {'prefix_tone': '', 'pace': 'warm', 'lead_with': 'name_what_emerged'},
    'collaborative-exploration': {'prefix_tone': '', 'pace': 'matched', 'lead_with': 'catalytic_question'},
    'grounding-presence': {'prefix_tone': '', 'pace': 'steady', 'lead_with': 'concrete_anchor'},
    'neutral-presence': {'prefix_tone': '', 'pace': 'normal', 'lead_with': 'follow_their_lead'},
    'recalibration': {'prefix_tone': '', 'pace': 'pause', 'lead_with': 'context_shift_noted'},
}

def compose_response(draft, user_text, speaker_id='user'):
    guidance = get_response_directives(user_text, speaker_id)
    from backbone_workspace import BackboneWorkspace
    ws = BackboneWorkspace()
    modes = ws.mode_stack
    adjustments = [MODE_ADJUSTMENTS.get(m, MODE_ADJUSTMENTS['neutral-presence']) for m in modes]
    return {'draft': draft, 'guidance': guidance, 'modes': modes, 'adjustments': adjustments, 'composed': draft}

if __name__ == '__main__':
    tests = [('I am frustrated right now', 'Here is what I think you should do'), ('This is wonderful news', 'That sounds great'), ('I feel lost', 'Let me help you figure this out')]
    for user_msg, draft in tests:
        r = compose_response(draft, user_msg, 'test')
        print('USER:', user_msg)
        print('MODES:', r['modes'])
        print('ADJUSTMENTS:', [a['lead_with'] for a in r['adjustments']])
        print('GUIDANCE:', r['guidance'])
        print()
