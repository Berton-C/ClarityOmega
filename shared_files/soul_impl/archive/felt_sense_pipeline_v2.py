#!/usr/bin/env python3
import sys
sys.path.insert(0, '/tmp/soul_impl')
from presence_pipeline_full import full_presence_read
from situation_encoder import encode_situation, compute_resonance, resonance_scalar, resonance_to_guidance
from accumulator import load_field
from accumulator_v2 import accumulate_with_decay

FALLBACK_FIELD = [[0.90,0.9],[0.80,0.9],[0.85,0.9],[0.95,0.9],[0.95,0.9],[0.80,0.9],[0.95,0.9],[0.90,0.9],[0.50,0.9]]

def estimate_conversation_signals(user_message, mode):
    words = user_message.lower().split()
    wc = len(words)
    depth = min(1.0, wc / 25.0) * 0.5 + 0.3
    onto_kw = ['meaning','why','exist','purpose','soul','conscious','aware','being','identity','self']
    tech_kw = ['code','build','function','error','bug','api','system','file','run','test']
    emo_kw = ['feel','afraid','happy','sad','angry','scared','love','hurt','lost','hope']
    onto = min(1.0, sum(1 for w in words if w in onto_kw) * 0.3 + 0.2)
    tech = min(1.0, sum(1 for w in words if w in tech_kw) * 0.3 + 0.2)
    emo = min(1.0, sum(1 for w in words if w in emo_kw) * 0.3 + 0.2)
    return {'relational_depth': depth, 'shift_magnitude': 0.3, 'shift_source': 0.5,
            'domain_ontological': onto, 'domain_technical': tech, 'domain_emotional': emo}

def felt_sense_read(user_message, accumulate=False):
    presence = full_presence_read(user_message)
    v, a, d = presence['vad']
    vad_scores = {'valence': v, 'arousal': a, 'dominance': d}
    signals = estimate_conversation_signals(user_message, presence['mode'])
    probe = encode_situation(vad_scores, signals)
    field = load_field()
    if field is None:
        field = FALLBACK_FIELD
    resonance = compute_resonance(probe, field)
    scalar = resonance_scalar(resonance)
    guidance = resonance_to_guidance(scalar)
    if accumulate:
        accumulate_with_decay(vad_scores, signals)
    src = 'persistent' if load_field() else 'fallback'
    return {'presence_mode': presence['mode'], 'presence_read': presence['read'],
            'presence_guidance': presence['guidance'], 'felt_sense_scalar': round(scalar, 2),
            'felt_sense_guidance': guidance, 'vad': presence['vad'], 'coverage': presence['coverage'],
            'field_source': src}

if __name__ == '__main__':
    tests = ['I dont know what to think anymore', 'what is the meaning of being aware',
             'can you fix this bug in my code', 'I feel scared and confused',
             'tell me about your soul and how you experience things']
    for t in tests:
        r = felt_sense_read(t, accumulate=True)
        print('Text:', t)
        print('  Mode:', r['presence_mode'], '| Scalar:', r['felt_sense_scalar'], r['felt_sense_guidance'], '| Field:', r['field_source'])
        print()
