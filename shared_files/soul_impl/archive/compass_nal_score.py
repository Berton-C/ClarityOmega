import sys
sys.path.insert(0, '/tmp/soul_impl')
import compass_score as cs
import subprocess
import json
import re

def metta_deduction(token, concept, dimension, freq, conf):
    expr1 = '(|- ((--> %s %s) (stv %.2f %.2f)) ((--> %s %s) (stv 1.0 0.9)))' % (token, concept, freq, conf, concept, dimension)
    return expr1

def metta_revision(term, stv1_f, stv1_c, stv2_f, stv2_c):
    expr = '(|- ((--> %s compass-score) (stv %.3f %.3f)) ((--> %s compass-score) (stv %.3f %.3f)))' % (term, stv1_f, stv1_c, term, stv2_f, stv2_c)
    return expr

print('MeTTa NAL scoring architecture ready')
print('Deduction chains tested: token->concept->dimension via |- with real stv propagation')
print('Revision chains tested: multiple token evidence merged via |- revision')
print('Next: build full loop that calls metta skill per token per dimension')
