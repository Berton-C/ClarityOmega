import json
import sys

def generate_compass_metta_exprs(scores):
    dims = ['agency', 'wonder', 'quality', 'honesty']
    soul_strengths = {'agency': 0.85, 'wonder': 0.8, 'quality': 0.82, 'honesty': 0.9}
    soul_confidences = {'agency': 0.8, 'wonder': 0.75, 'quality': 0.78, 'honesty': 0.82}
    exprs = []
    for d in dims:
        s = scores.get(d, 0.5)
        ss = soul_strengths[d]
        sc = soul_confidences[d]
        expr = f'(|- ((--> situation-{d} soul-{d}) (stv {s} 0.7)) ((--> soul-{d} aligned) (stv {ss} {sc})))'
        exprs.append((d, expr))
    return exprs

if __name__ == '__main__':
    test = {'agency': 0.4, 'wonder': 0.3, 'quality': 0.5, 'honesty': 0.85}
    for dim, expr in generate_compass_metta_exprs(test):
        print(f'{dim}: {expr}')
