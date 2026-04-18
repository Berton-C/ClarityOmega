import sys
sys.path.insert(0, '/tmp/soul_impl')
import compass_score as cs
import re

def get_token_chains():
    chains = []
    for dim_name, dim_data in cs.DIMS.items():
        concept = dim_data['c']
        compass_dim = dim_data['p']
        for token, freq in dim_data['t'].items():
            chains.append(dict(token=token, concept=concept, dimension=compass_dim, freq=freq, conf=0.9))
    return chains

def tokenize(text):
    return set(re.findall('[a-z]+', text.lower()))

def build_metta_deductions(text):
    toks = tokenize(text)
    chains = get_token_chains()
    exprs = []
    for c in chains:
        if c['token'] in toks:
            expr = '(|- ((--> %s %s) (stv %.2f %.2f)) ((--> %s %s) (stv 1.0 0.9)))' % (c['token'], c['concept'], c['freq'], c['conf'], c['concept'], c['dimension'])
            exprs.append(dict(dim=c['dimension'], token=c['token'], expr=expr))
    return exprs

def build_metta_revisions(deduced):
    by_dim = {}
    for d in deduced:
        by_dim.setdefault(d['dim'], []).append(d)
    revisions = []
    for dim, items in by_dim.items():
        if len(items) >= 2:
            acc_f = items[0]['token']
            for i in range(1, len(items)):
                expr = '(|- ((--> %s %s) (stv 0.9 0.81)) ((--> %s %s) (stv 0.9 0.81)))' % (items[0]['token'], dim, items[i]['token'], dim)
                revisions.append(dict(dim=dim, expr=expr))
    return revisions

test = 'You might consider exploring this fascinating pattern because it matters'
deds = build_metta_deductions(test)
print('Deductions to execute via metta skill:', len(deds))
for d in deds:
    print(' ', d['dim'], d['token'], d['expr'])
revs = build_metta_revisions(deds)
print('Revisions to execute via metta skill:', len(revs))
for r in revs:
    print(' ', r['dim'], r['expr'])
