import sys
sys.path.insert(0, '/tmp')
from language_flag_detector import detect_flags
from technique_router import available_techniques
from gate_rules_engine import run_gate
from technique_execution_templates import shape_guidance
from technique_compliance_checker import check_compliance

def run_pipeline(user_text, vad, mode, draft_response, max_revisions=3):
    result = {}
    result['flags'] = detect_flags(user_text)
    result['techniques'] = available_techniques(mode, vad[0], vad[1], vad[2], result['flags'])
    selected = result['techniques'][0] if result['techniques'] else None
    result['selected_technique'] = selected
    result['technique_guidance'] = shape_guidance(selected) if selected else None
    current_draft = draft_response
    context = {'valence': vad[0], 'flags': result['flags'], 'mode': mode}
    revisions = 0
    revision_log = []
    while revisions < max_revisions:
        gate_out = run_gate(current_draft, context)
        if gate_out['verdict'] != 'pass':
            revision_log.append({'source': 'gate', 'rule': gate_out['rule']})
            current_draft = gate_out['draft']
            revisions += 1
            continue
        if selected:
            comp = check_compliance(current_draft, selected)
            if not comp['compliant']:
                revision_log.append({'source': 'technique', 'issues': comp['issues']})
                revisions += 1
                break
        break
    result['revision_count'] = revisions
    result['revision_log'] = revision_log
    result['final_text'] = current_draft
    result['send'] = True
    return result

if __name__ == '__main__':
    r1 = run_pipeline('I feel awful', [0.1, 0.3, 0.2], 'still-holding', 'This is a very long response that goes on and on about many different things and keeps expanding beyond what is needed here')
    print('R1 revisions:', r1['revision_count'], 'log:', r1['revision_log'])
    assert r1['revision_count'] > 0
    r2 = run_pipeline('It is always like this', [0.2, 0.5, 0.2], 'spacious-presence', 'You need to change now!')
    print('R2 final:', r2['final_text'], 'log:', r2['revision_log'])
    assert '!' not in r2['final_text']
    r3 = run_pipeline('I dont know', [0.15, 0.6, 0.25], 'spacious-presence', 'What does that feel like?')
    print('R3 technique:', r3['selected_technique'], 'guidance:', r3['technique_guidance'])
    assert r3['revision_count'] == 0
    r4 = run_pipeline('I feel sad', [0.3, 0.3, 0.2], 'still-holding', 'You should really try meditation and also you should journal and here is a very long explanation')
    print('R4 log:', r4['revision_log'])
    assert r4['revision_count'] > 0
    r5 = run_pipeline('Nice day', [0.7, 0.4, 0.6], 'playful-aliveness', 'Lovely.')
    assert r5['revision_count'] == 0
    print('ORCHESTRATOR V5 WITH TECHNIQUE COMPLIANCE PASSED')
