#!/usr/bin/env python3
import sys, os, json
sys.path.insert(0, '/tmp')
from response_composer_v2_clean import compose_fresh, compose_stateful
from backbone_workspace import BackboneWorkspace

class UnifiedRuntime:
    def __init__(self, mode='stateful'):
        self.mode = mode
        self.turn_log = []

    def process(self, user_text, draft_response, speaker_id='user'):
        if self.mode == 'fresh':
            result = compose_fresh(draft_response, user_text, speaker_id)
        else:
            result = compose_stateful(draft_response, user_text, speaker_id)
        entry = {'turn': len(self.turn_log)+1, 'user': user_text, 'modes': result['modes'], 'composed': result['composed']}
        self.turn_log.append(entry)
        return result

    def get_log(self):
        return self.turn_log

if __name__ == '__main__':
    rt = UnifiedRuntime(mode='stateful')
    conversation = [
        ('I am really struggling with this project', 'Let me help you break it down.'),
        ('Actually wait, I just had a breakthrough', 'Tell me more about what you found.'),
        ('I am nervous about presenting it though', 'Here is how to prepare.'),
    ]
    for user_msg, draft in conversation:
        r = rt.process(user_msg, draft)
        print('TURN %d' % len(rt.turn_log))
        print('USER:', user_msg)
        print('COMPOSED:', r['composed'])
        print('MODES:', r['modes'])
        print()
    print('FULL LOG:', json.dumps(rt.get_log(), indent=2))
