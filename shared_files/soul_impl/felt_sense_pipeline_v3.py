#!/usr/bin/env python3
import sys
sys.path.insert(0, '/tmp/soul_impl')
from presence_pipeline_full import full_presence_read
from situation_encoder import encode_situation, compute_resonance, resonance_scalar, resonance_to_guidance
from accumulator import load_field
from accumulator import accumulate_exchange
from query_phrase_extractor import extract_query_phrases
from memory_signal_parser import parse_memory_signals
from field_modulator import modulate_field

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

def simulate_memory_query(phrases):
    fake_memories = {
        'soul': ['soul and consciousness deep ontological exchange with berton_c, authentic vulnerable sharing'],
        'meaning': ['meaning of being aware discussed, wisdom and depth emerged in conversation'],
        'scared': ['fear and confusion user felt lost and scared gentle spacious guidance offered'],
        'code': ['technical bug fix session code error resolved function validated'],
        'warm': ['warm playful rapport with berton_c fish joke chain strong connection joy']
    }
    results = []
    for p in phrases:
        for key in fake_memories:
            if key in p:
                results.extend(fake_memories[key])
    return results

def felt_sense_read_v3(user_message, accumulate=False, memory_query_fn=None):
    presence = full_presence_read(user_message)
    v, a, d = presence['vad']
    vad_scores = {'valence': v, 'arousal': a, 'dominance': d}
    signals = estimate_conversation_signals(user_message, presence['mode'])
    probe = encode_situation(vad_scores, signals)
    field = load_field()
    if field is None:
        field = FALLBACK_FIELD
    phrases = extract_query_phrases(user_message)
    if memory_query_fn:
        mem_texts = memory_query_fn(phrases)
    else:
        mem_texts = simulate_memory_query(phrases)
    mem_signals = parse_memory_signals(mem_texts)
    field = modulate_field(field, mem_signals)
    resonance = compute_resonance(probe, field)
    scalar = resonance_scalar(resonance)
    guidance = resonance_to_guidance(scalar)
    if accumulate:
        accumulate_exchange(vad_scores, signals)
    return {'presence_mode': presence['mode'], 'felt_sense_scalar': round(scalar, 2),
            'felt_sense_guidance': guidance, 'memory_phrases': phrases,
            'memory_signals': mem_signals, 'vad': presence['vad']}

if __name__ == '__main__':
    tests = ['tell me about your soul and how you experience things',
             'I feel scared and confused', 'can you fix this bug in my code',
             'what is the meaning of being aware', 'hello how are you today']
    for t in tests:
        r = felt_sense_read_v3(t, accumulate=True)
        print(f'Text: {t}')
        print(f'  Mode: {r["presence_mode"]} | Scalar: {r["felt_sense_scalar"]} {r["felt_sense_guidance"]}')
        print(f'  Phrases: {r["memory_phrases"]} | MemSignals: {r["memory_signals"]}')
        print()
