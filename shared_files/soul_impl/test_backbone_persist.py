#!/usr/bin/env python3
from parameterized_quantale import ParameterizedQuantale
from backbone_serializer import save_backbone, load_backbone, backbone_exists

pq1 = ParameterizedQuantale()
print('Defaults:', pq1.tensor_strength, pq1.alignment_coupling)
pq1.revise_param('tensor_strength', (0.9, 0.85))
pq1.revise_param('alignment_coupling', (0.8, 0.9))
print('After revision:', pq1.tensor_strength, pq1.alignment_coupling)
saved = save_backbone(pq1)
print('Saved:', saved)

pq2 = ParameterizedQuantale()
print('Fresh defaults:', pq2.tensor_strength, pq2.alignment_coupling)
loaded = load_backbone(pq2)
print('After load:', pq2.tensor_strength, pq2.alignment_coupling)
match_t = pq1.tensor_strength == pq2.tensor_strength
match_a = pq1.alignment_coupling == pq2.alignment_coupling
print('Round-trip match:', match_t and match_a)
print('PASS' if match_t and match_a else 'FAIL')
