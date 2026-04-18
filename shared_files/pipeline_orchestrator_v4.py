import sys
sys.path.insert(0, '/tmp')
from language_flag_detector import detect_flags
from technique_router import available_techniques
from gate_rules_engine import run_gate
from technique_execution_templates import shape_guidance

def run_pipeline(user_text, vad, mode, draft_response, max_revisions=2):
    result = {}
    result['flags'] = detect_flags(user_text)
    result['techniques'] = available_techniques(mode, vad[0], vad[1], vad[2], result['flags'])
    if result['techniques']:
        result['technique_guidance'] = shape_guidance(result['techniques'][0])
    else:
        result['technique_guidance'] = None
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
    result['send'] = gate_out['verdict'] == 'pass'
    return result

if __name__ == '__main__':
    r1 = run_pipeline('I dont know what to do anymore', [0.15, 0.6, 0.25], 'spacious-presence', 'What does stuck feel like in your body right now?')
    print('Techniques:', r1['techniques'])
    print('Guidance:', r1['technique_guidance'])
    assert r1['technique_guidance'] is not None
    assert 'Shape:' in r1['technique_guidance']
    r2 = run_pipeline('It is always like this nothing changes', [0.2, 0.5, 0.2], 'spacious-presence', 'You need to snap out of it!')
    print('R2 revised:', r2['final_text'], 'revisions:', r2['revision_count'])
    assert '!' not in r2['final_text']
    assert r2['technique_guidance'] is not None
    r3 = run_pipeline('Nice day today', [0.7, 0.4, 0.6], 'playful-aliveness', 'Lovely.')
    print('R3 send:', r3['send'], 'techniques:', r3['techniques'])
    assert r3['send'] == True
    print('ORCHESTRATOR V4 WITH TECHNIQUE GUIDANCE PASSED')
