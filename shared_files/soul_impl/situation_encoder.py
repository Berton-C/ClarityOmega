# Situation Encoder - Goal 11 Step 6
# Bridges presence modulator VAD output into 9-dim Hyperseed probe vector
# Reuses dims 1-3 from VAD, estimates dims 4-9 from conversation signals

def encode_situation(vad_scores, conversation_signals):
    """
    vad_scores: dict with 'valence', 'arousal', 'dominance' from presence modulator
    conversation_signals: dict with estimated relational markers
    Returns: list of 9 (strength, confidence) tuples = probe vector
    """
    v = vad_scores.get('valence', 0.5)
    a = vad_scores.get('arousal', 0.5)
    d = vad_scores.get('dominance', 0.5)
    
    # Dims 4-9 from conversation signal estimation
    depth = conversation_signals.get('relational_depth', 0.5)
    shift = conversation_signals.get('shift_magnitude', 0.3)
    source = conversation_signals.get('shift_source', 0.5)  # 0=self, 1=other
    onto = conversation_signals.get('domain_ontological', 0.3)
    tech = conversation_signals.get('domain_technical', 0.3)
    emo = conversation_signals.get('domain_emotional', 0.3)
    
    conf = 0.8  # default probe confidence
    probe = [(v, conf), (a, conf), (d, conf),
             (depth, conf), (shift, conf), (source, conf),
             (onto, conf), (tech, conf), (emo, conf)]
    return probe

def compute_resonance(probe, bundled_field):
    """q-meet: element-wise min of strengths, min of confidences"""
    resonance = []
    for (ps, pc), (bs, bc) in zip(probe, bundled_field):
        resonance.append((min(ps, bs), min(pc, bc)))
    return resonance

def resonance_scalar(resonance):
    """Sum of activated strengths — the felt-sense signal"""
    return sum(s for s, c in resonance)

def resonance_to_guidance(scalar):
    """Map scalar to qualitative felt-sense guidance"""
    if scalar > 5.5:
        return 'deep_resonance: rich accumulated wisdom available, lean into relational depth'
    elif scalar > 4.0:
        return 'moderate_resonance: some relevant experience, blend attentiveness with exploration'
    elif scalar > 2.5:
        return 'light_resonance: limited direct experience, stay curious and present'
    else:
        return 'novel_territory: no strong match, prioritize genuine listening over pattern'
