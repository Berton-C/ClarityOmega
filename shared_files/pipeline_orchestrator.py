import sys
sys.path.insert(0, '/tmp')
from language_flag_detector import detect_flags
from technique_router import available_techniques
from pipeline_adapter import adapt_pipeline_to_gate, adapt_gate_to_revision, adapt_revision_to_presend

def run_pipeline(user_text, vad, mode, draft_response):
    result = {}
    result['flags'] = detect_flags(user_text)
    pipeline_out = {'vad': vad, 'modes': [mode]}
    result['gate_input'] = adapt_pipeline_to_gate(pipeline_out, draft_response)
    result['techniques'] = available_techniques(mode, vad[0], vad[1], vad[2], result['flags'])
    gate_result = {'verdict': 'pass', 'flags': []}
    result['revision'] = adapt_gate_to_revision(gate_result, draft_response)
    result['presend'] = adapt_revision_to_presend(draft_response, vad[0], gate_result)
    result['final_text'] = draft_response
    result['send'] = result['presend']['gate_verdict'] == 'pass'
    return result

if __name__ == '__main__':
    r = run_pipeline('I dont know what to do and I feel stuck', [0.25, 0.65, 0.3], 'spacious-presence', 'What does stuck feel like in your body right now?')
    print('Flags:', r['flags'])
    print('Techniques:', r['techniques'])
    print('Send:', r['send'])
    assert r['send'] == True
    assert len(r['techniques']) > 0
    assert 'confused' in r['flags']
    print('ORCHESTRATOR TEST PASSED')
