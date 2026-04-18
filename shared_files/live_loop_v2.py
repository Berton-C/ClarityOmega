import sys, json
sys.path.insert(0, '/tmp')
from conversation_handler_v2 import handle_turn

def run_live(messages):
    results = []
    for i, msg in enumerate(messages):
        r = handle_turn(msg, 'user')
        results.append(r)
        print('Turn %d: %s' % (i+1, msg))
        print(r['context_block'])
        print('Action: %s' % r['action'])
        print('---')
    return results

if __name__ == '__main__':
    if len(sys.argv) > 1:
        r = handle_turn(sys.argv[1], 'user')
        print(json.dumps({'action': r['action'], 'guidance': r['guidance'], 'metta': r['metta_expr']}, indent=2))
    else:
        run_live(['I feel so lost right now', 'Actually wait I just had an idea', 'Yes this could really work I am excited', 'Hmm but what if it fails'])
