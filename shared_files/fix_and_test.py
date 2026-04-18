#!/usr/bin/env python3
import sys
sys.path.insert(0, '/tmp')

# Patch the lexicon path at import time
import text_to_metta_vad as bridge
lex = bridge.load_lexicon('/tmp/vad_common500.metta')
print('Lexicon size:', len(lex))
print('Sample keys:', sorted(list(lex.keys()))[:15])
print('Has frustrated:', 'frustrated' in lex)
print('Has love:', 'love' in lex)
print('Has wonderful:', 'wonderful' in lex)
print('Has stuck:', 'stuck' in lex)
print('Has progress:', 'progress' in lex)

text1 = 'I am frustrated and stuck but wondering about possibilities'
words1, hits1, vad1 = bridge.extract_vad(text1, lex)
print('\n--- Test 1:', text1)
print('Hits:', [(h[0], h[1]) for h in hits1])
print('VAD:', vad1)
print(bridge.to_metta('turn-001', words1, hits1, vad1))

text2 = 'this is wonderful and I love the progress we are making'
words2, hits2, vad2 = bridge.extract_vad(text2, lex)
print('\n--- Test 2:', text2)
print('Hits:', [(h[0], h[1]) for h in hits2])
print('VAD:', vad2)
print(bridge.to_metta('turn-002', words2, hits2, vad2, prev_vad=vad1))
