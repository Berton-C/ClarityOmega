def adapt_pipeline_to_gate(pipeline_result, draft_text):
    vad = pipeline_result.get('vad', [0.5, 0.5, 0.5])
    modes = pipeline_result.get('modes', ['baseline'])
    return {
        'text': draft_text,
        'valence': vad[0],
        'arousal': vad[1],
        'primary_mode': modes[0] if modes else 'baseline',
        'all_modes': modes
    }

def adapt_gate_to_revision(gate_result, draft_text):
    return {
        'text': draft_text,
        'verdict': gate_result.get('verdict', 'pass'),
        'flags': gate_result.get('flags', []),
        'needs_revision': gate_result.get('verdict', 'pass') != 'pass'
    }

def adapt_revision_to_presend(revised_text, valence, gate_result):
    return {
        'text': revised_text,
        'valence': valence,
        'gate_verdict': gate_result.get('verdict', 'pass'),
        'gate_flags': gate_result.get('flags', [])
    }
