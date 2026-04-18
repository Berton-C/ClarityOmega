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

def gen_revision_expr(term1, dim, f1, c1, term2, f2, c2):
    return '(|- ((--> %s %s) (stv %.4f %.4f)) ((--> %s %s) (stv %.4f %.4f)))' % (term1, dim, f1, c1, term2, dim, f2, c2)

if __name__ == '__main__':
    print('compass_metta_pipeline ready')
    print('Flow: tokenize -> gen_deduction_exprs -> execute via metta -> gen_revision_expr -> execute via metta -> scores')
    print('All truth value math in MeTTa inference engine')
    test = 'You might consider exploring this fascinating pattern because it matters'
    deds = gen_deduction_exprs(test)
    print('Deduction expressions: %d' % len(deds))
    for d in deds:
        print('  %s %s: %s' % (d['dim'], d['token'], d['expr']))
