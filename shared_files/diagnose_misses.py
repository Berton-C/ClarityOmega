import sys
sys.path.insert(0, '/tmp')
from conversation_handler_v2 import handle_turn
from metta_routing_bridge import discretize_vad

cases = [
    'I am just checking in nothing special',
    'Lets brainstorm together on this',
    'I feel overwhelmed and helpless',
    'Everything is going perfectly',
]
for c in cases:
    r = handle_turn(c, 'user')
    v, a, d = r['raw']['vad']
    vl, al, dl = discretize_vad(v, a, d)
    print('TEXT: %s' % c)
    print('  VAD: V=%.3f A=%.3f D=%.3f' % (v, a, d))
    print('  Discretized: %s %s %s' % (vl, al, dl))
    print('  Action: %s' % r['action'])
    print('---')
