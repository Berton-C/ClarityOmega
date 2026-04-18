import sys
sys.path.insert(0, '/tmp')
from language_flag_detector import detect_flags
from technique_router import available_techniques
from pipeline_adapter import adapt_pipeline_to_gate, adapt_gate_to_revision, adapt_revision_to_presend

def simulate_gate(draft, flags, vad):
    if vad[0] < 0.2 and len(draft) > 80:
        return {'verdict': 'revise', 'flags': ['too-long-for-distress']}
    if 'calcified' in flags and '!' in draft:
        return {'verdict': 'revise', 'flags': ['forceful-with-calcified']}
    return {'verdict': 'pass', 'flags': []}

def revise_draft(draft, gate_flags):
    if 'too-long-for-distress' in gate_flags:
        return draft[:60].rsplit(' ', 1)[0] + '...'
    if 'forceful-with-calcified' in gate_flags:
        return draft.replace('!', '.')
    return draft

def run_pipeline(user_text, vad, mode, draft_response, max_revisions=2):
    result = {}
    result['flags'] = detect_flags(user_text)
    pipeline_out = {'vad': vad, 'modes': [mode]}
    result['gate_input'] = adapt_pipeline_to_gate(pipeline_out, draft_response)
    result['techniques'] = available_techniques(mode, vad[0], vad[1], vad[2], result['flags'])
    current_draft = draft_response
    revisions = 0
    while revisions < max_revisions:
        gate_result = simulate_gate(current_draft, result['flags'], vad)
        if gate_result['verdict'] == 'pass':
            break
        current_draft = revise_draft(current_draft, gate_result['flags'])
        revisions += 1
    else:
        gate_result = simulate_gate(current_draft, result['flags'], vad)
    result['revision_count'] = revisions
    result['revision'] = adapt_gate_to_revision(gate_result, current_draft)
    result['presend'] = adapt_revision_to_presend(current_draft, vad[0], gate_result)
    result['final_text'] = current_draft
    result['send'] = gate_result['verdict'] == 'pass'
    return result

if __name__ == '__main__':
    r1 = run_pipeline('I feel awful', [0.1, 0.3, 0.2], 'still-holding', 'This is a very long response that goes on and on about many different things and keeps expanding beyond what is needed here')
    print('Revise test revisions:', r1['revision_count'])
    print('Final text:', r1['final_text'])
    assert r1['revision_count'] > 0
    r2 = run_pipeline('It is always like this', [0.2, 0.5, 0.2], 'spacious-presence', 'You need to change now!')
    print('Calcified revise:', r2['revision_count'], r2['final_text'])
    assert '!' not in r2['final_text']
    r3 = run_pipeline('I had a nice walk', [0.7, 0.4, 0.6], 'playful-aliveness', 'Lovely.')
    assert r3['revision_count'] == 0
    print('ORCHESTRATOR V2 WITH REVISION LOOP PASSED')
