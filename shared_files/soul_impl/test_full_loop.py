#!/usr/bin/env python3
import sys
sys.path.insert(0, '/tmp/soul_impl')
from felt_sense_pipeline import felt_sense_read, estimate_conversation_signals
from accumulator import accumulate_exchange, load_field, save_field

# Reset field to seed
seed = [[0.90,0.9],[0.80,0.9],[0.85,0.9],[0.95,0.9],[0.95,0.9],[0.80,0.9],[0.95,0.9],[0.90,0.9],[0.50,0.9]]
save_field(seed)

exchanges = [
    'what is the meaning of being aware',
    'can you help me debug this function',
    'I feel lost and I do not know where to turn',
    'tell me about how your soul navigates uncertainty',
    'build me a quick python script for sorting'
]

for msg in exchanges:
    result = felt_sense_read(msg)
    signals = estimate_conversation_signals(msg, result['presence_mode'])
    vad = {'valence': result['vad'][0], 'arousal': result['vad'][1], 'dominance': result['vad'][2]}
    acc_result, status = accumulate_exchange(vad, signals)
    print('MSG:', msg)
    print('  Mode:', result['presence_mode'], '| Scalar:', result['felt_sense_scalar'], '|', result['felt_sense_guidance'])
    print('  Field status:', status)
    print()

final = load_field()
print('Final accumulated field:')
for i, dim in enumerate(final):
    print(f'  dim{i}: strength={dim[0]:.3f} conf={dim[1]:.3f}')
