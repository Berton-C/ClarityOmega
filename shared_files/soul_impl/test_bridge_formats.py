import sys
sys.path.insert(0, '/tmp/soul_impl')
from metta_inference_bridge import parse_metta_result as p
from metta_inference_bridge import evaluate_components_from_results as e

print('=== parse_metta_result ===')
flat = [['-->', 'w', 's'], ['stv', 0.75, 0.9]]
wrapped = [[['-->', 'w', 's'], ['stv', 0.75, 0.9]]]
print('flat:', p(flat))
print('wrapped:', p(wrapped))

print('=== evaluate flat format ===')
r1 = [('web', [['-->', 'w', 's'], ['stv', 0.75, 0.9]]), ('mem', [['-->', 'm', 'l'], ['stv', 0.42, 0.325]])]
print('flat:', e(r1))

print('=== evaluate wrapped format ===')
r2 = [('web', [[['-->', 'w', 's'], ['stv', 0.75, 0.9]]]), ('mem', [[['-->', 'm', 'l'], ['stv', 0.42, 0.325]]])]
print('wrapped:', e(r2))
