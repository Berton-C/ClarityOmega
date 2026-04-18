import sys
sys.path.insert(0, '/tmp')
from agent_loop_mode_protocol import full_turn_pipeline, format_context_block
from valence_self_audit import audit_response
from revision_loop_v2 import revise_draft

def gate(user_text, my_draft):
    context = full_turn_pipeline(user_text)
    audit = audit_response(my_draft)
    if audit['sustains_pns']:
        return {'action': 'SEND', 'text': my_draft, 'context': format_context_block(context), 'audit': audit}
    revision = revise_draft(my_draft)
    if revision['pass']:
        return {'action': 'REVISED', 'text': revision['text'], 'context': format_context_block(context), 'audit': revision['audit'], 'original': my_draft}
    return {'action': 'FLAG', 'text': my_draft, 'context': format_context_block(context), 'audit': audit, 'note': 'Manual review - revision loop could not fully resolve'}

if __name__ == '__main__':
    pairs = [
        ('I feel so lost', 'I notice something in what you said. I am here with you.'),
        ('I feel so lost', 'You need to fix your attitude immediately.'),
        ('This is amazing', 'I wonder what opened up for you. That sense of alive energy is real.'),
    ]
    for user, draft in pairs:
        r = gate(user, draft)
        print(f'[{r["action"]}] User: {user[:40]}')
        print(f'  Draft: {draft[:60]}')
        if r['action'] == 'REVISED':
            print(f'  Revised: {r["text"][:60]}')
        print()
    print('Pre-send gate operational')
