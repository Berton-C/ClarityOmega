import sys
sys.path.insert(0, '/tmp/soul_impl')
from metta_inference_bridge import run_metta_expr

r = run_metta_expr('(|- ((--> a b) (stv 0.8 0.7)) ((--> b c) (stv 0.9 0.8)))')
print('RAW repr:', repr(r['raw']))
print('RAW type:', type(r['raw']))
print('f:', r['f'], 'c:', r['c'])
if r.get('error'):
    print('ERROR:', r['error'])
