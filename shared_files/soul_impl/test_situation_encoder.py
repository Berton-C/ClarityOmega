import situation_encoder as se

vad = {'valence': 0.7, 'arousal': 0.5, 'dominance': 0.6}
sig = {'relational_depth': 0.8, 'shift_magnitude': 0.4, 'shift_source': 0.5,
       'domain_ontological': 0.9, 'domain_technical': 0.2, 'domain_emotional': 0.3}

probe = se.encode_situation(vad, sig)
bundle = [(0.90,0.9),(0.80,0.9),(0.85,0.9),(0.95,0.9),(0.95,0.9),(0.80,0.9),(0.95,0.9),(0.90,0.9),(0.50,0.9)]
resonance = se.compute_resonance(probe, bundle)
scalar = se.resonance_scalar(resonance)
guidance = se.resonance_to_guidance(scalar)

print('Probe:', probe)
print('Resonance:', resonance)
print('Scalar:', scalar)
print('Guidance:', guidance)

# Test probe 2: novel technical visitor
vad2 = {'valence': 0.5, 'arousal': 0.4, 'dominance': 0.5}
sig2 = {'relational_depth': 0.3, 'shift_magnitude': 0.2, 'shift_source': 0.5,
        'domain_ontological': 0.2, 'domain_technical': 0.95, 'domain_emotional': 0.1}
probe2 = se.encode_situation(vad2, sig2)
resonance2 = se.compute_resonance(probe2, bundle)
scalar2 = se.resonance_scalar(resonance2)
guidance2 = se.resonance_to_guidance(scalar2)

print('\nProbe2:', probe2)
print('Resonance2:', resonance2)
print('Scalar2:', scalar2)
print('Guidance2:', guidance2)
print('\nDifferentiation:', round(scalar - scalar2, 3), '- higher means more accumulated wisdom activated')
