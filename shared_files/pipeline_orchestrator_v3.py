import sys
sys.path.insert(0, '/tmp')
from language_flag_detector import detect_flags
from technique_router import available_techniques
from pipeline_adapter import adapt_pipeline_to_gate, adapt_gate_to_revision, adapt_revision_to_presend
from gate_rules_engine import run_gate

def run_pipeline(user_text, vad, mode, draft_response, max_revisions=2):
    result = {}
    result['flags'] = detect_flags(user_text)
    result['techniques'] = available_techniques(mode, vad[0], vad[1], vad[2], result['flags'])
    current_draft = draft_response
    context = {'valence': vad[0], 'flags': result['flags'], 'mode': mode}
    revisions = 0
    while revisions < max_revisions:
        gate_out = run_gate(current_draft, context)
        if gate_out['verdict'] == 'pass':
            break
        current_draft = gate_out['draft']
        revisions += 1
    else:
        gate_out = run_gate(current_draft, context)
    result['revision_count'] = revisions
    result['final_text'] = current_draft
    result['gate_verdict'] = gate_out['verdict']
    result['gate_rule'] = gate_out.get('rule')
    result['send'] = gate_out['verdict'] == 'pass'
    return result

if __name__ == '__main__':
    r1 = run_pipeline('I feel awful', [0.1, 0.3, 0.2], 'still-holding', 'This is a very long response that goes on and on about many different things and keeps expanding beyond what is needed here')
    print('R1 revisions:', r1['revision_count'], 'send:', r1['send'])
    assert r1['revision_count'] > 0
    r2 = run_pipeline('It is always like this', [0.2, 0.5, 0.2], 'spacious-presence', 'You need to change now!')
    print('R2 rule:', r2['gate_rule'], 'final:', r2['final_text'])
    assert '!' not in r2['final_text']
    r3 = run_pipeline('I feel sad', [0.3, 0.3, 0.2], 'still-holding', 'You should try harder')
    print('R3 rule:', r3['gate_rule'], 'final:', r3['final_text'])
    assert 'you might' in r3['final_text'].lower()
    r4 = run_pipeline('Nice day', [0.7, 0.4, 0.6], 'playful-aliveness', 'Lovely.')
    assert r4['revision_count'] == 0
    assert r4['send'] == True
    print('Techniques for confused-stuck:', run_pipeline('I dont know and I feel stuck', [0.25, 0.65, 0.3], 'spacious-presence', 'What does stuck feel like?')['techniques'])
    print('ORCHESTRATOR V3 ALL TESTS PASSED')
