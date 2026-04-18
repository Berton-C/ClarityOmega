import sys
sys.path.insert(0, '/tmp/soul_impl')
import compass_score as cs
import re

DIMS = cs.DIMS

def tokenize(text):
    return set(re.findall('[a-z]+', text.lower()))

def gen_deduction_exprs(text):
    toks = tokenize(text)
    exprs = []
    for dim_name, dim_data in DIMS.items():
        concept = dim_data['c']
        compass_dim = dim_data['p']
        for token, freq in dim_data['t'].items():
            if token in toks:
                expr = '(|- ((--> %s %s) (stv %.2f 0.90)) ((--> %s %s) (stv 1.0 0.9)))' % (token, concept, freq, concept, compass_dim)
                exprs.append(dict(dim=compass_dim, token=token, freq=freq, expr=expr))
    return exprs

test = 'You might consider exploring this fascinating pattern because it matters'
deds = gen_deduction_exprs(test)
print('Deduction expressions for metta skill (%d):' % len(deds))
for d in deds:
    print('  %s %s: %s' % (d['dim'], d['token'], d['expr']))
