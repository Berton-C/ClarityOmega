import json
from metta_compass import gen_metta_calls, DIMS

def compass_score(text, metta_fn):
    calls = gen_metta_calls(text)
    scores = {}
    for dn, d in DIMS.items():
        dim_deductions = [c for c in calls['deduce'] if c['dim'] == dn]
        dim_revisions = [c for c in calls['revise'] if c['dim'] == dn]
        if not dim_deductions:
            scores[dn] = {'f': 0.0, 'c': 0.0, 'hits': 0}
            continue
        if len(dim_deductions) == 1:
            scores[dn] = {'f': d['t'][dim_deductions[0]['tok']], 'c': 0.81, 'hits': 1}
            continue
        acc_f = None
        acc_c = None
        for rev in dim_revisions:
            result = metta_fn(rev['expr'])
            if result and len(result) > 0:
                for r in result:
                    if r[0][1] == d['s'] and r[0][2] == d['p']:
                        acc_f = r[1][1]
                        acc_c = r[1][2]
                        break
        if acc_f is not None:
            scores[dn] = {'f': round(acc_f, 4), 'c': round(acc_c, 4), 'hits': len(dim_deductions)}
        else:
            scores[dn] = {'f': d['t'][dim_deductions[0]['tok']], 'c': 0.81, 'hits': len(dim_deductions)}
    return scores

if __name__ == '__main__':
    def mock_metta(expr):
        print('METTA_CALL: ' + expr)
        return None
    text = 'You might consider this fascinating pattern because it matters'
    result = compass_score(text, mock_metta)
    print('SCORES:', json.dumps(result, indent=2))
