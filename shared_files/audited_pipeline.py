import sys
sys.path.insert(0, '/tmp')
from agent_loop_mode_protocol import full_turn_pipeline, format_context_block
from valence_self_audit import audit_response

def audited_turn(user_input, draft_response):
    context = full_turn_pipeline(user_input)
    block = format_context_block(context)
    audit = audit_response(draft_response)
    return {
        'context_block': block,
        'mode': context.get('mode', 'unknown'),
        'audit': audit,
        'sustains_pns': audit['sustains_pns'],
        'pass': audit['sustains_pns'],
    }

if __name__ == '__main__':
    pairs = [
        ('I feel lost', 'I notice you said that. I am here with you. No rush.'),
        ('I feel lost', 'You need to fix your mindset immediately. This is a problem.'),
        ('This is amazing', 'What a wonder. Tell me more about what feels alive in that.'),
    ]
    for inp, resp in pairs:
        r = audited_turn(inp, resp)
        label = 'PASS' if r['pass'] else 'REVISE'
        print(f'[{label}] mode={r["mode"]} v={r["audit"]["avg_valence"]}')
        print(f'  Input: {inp}')
        print(f'  Draft: {resp}')
        if r['audit']['sns_flags']:
            print(f'  SNS flags: {r["audit"]["sns_flags"]}')
        print()
    print('Audited pipeline operational')
