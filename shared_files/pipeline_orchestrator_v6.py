import sys
sys.path.insert(0, '/tmp')
from language_flag_detector import detect_flags
from technique_router import available_techniques
from gate_rules_engine import run_gate
from technique_execution_templates import shape_guidance
from technique_compliance_checker import check_compliance
from revision_pattern_tracker import record_pipeline_result, get_top_failures, get_revision_rate

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
    passed_clean = revisions == 0
    record_pipeline_result(revision_log, selected, passed_clean)
    result['revision_count'] = revisions
    result['revision_log'] = revision_log
    result['final_text'] = current_draft
    result['send'] = True
    result['cumulative_revision_rate'] = get_revision_rate()
    result['top_recurring_failures'] = get_top_failures(3)
    return result

if __name__ == '__main__':
    import os
    if os.path.exists('/tmp/revision_patterns.json'):
        os.remove('/tmp/revision_patterns.json')
    r1 = run_pipeline('I feel awful', [0.1, 0.3, 0.2], 'still-holding', 'This is a very long response that goes on and on about many different things and keeps expanding beyond what is needed here')
    print('R1 revisions:', r1['revision_count'], 'rate:', r1['cumulative_revision_rate'])
    assert r1['revision_count'] > 0
    assert r1['cumulative_revision_rate'] == 1.0
    r2 = run_pipeline('Nice day', [0.7, 0.4, 0.6], 'playful-aliveness', 'Lovely.')
    print('R2 revisions:', r2['revision_count'], 'rate:', r2['cumulative_revision_rate'])
    assert r2['revision_count'] == 0
    assert r2['cumulative_revision_rate'] == 0.5
    r3 = run_pipeline('I dont know', [0.15, 0.6, 0.25], 'spacious-presence', 'What does that feel like?')
    print('R3 technique:', r3['selected_technique'], 'top_fails:', r3['top_recurring_failures'])
    assert r3['cumulative_revision_rate'] < 0.5
    print('ORCHESTRATOR V6 WITH AUTO-TRACKING PASSED')
