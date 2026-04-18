import sys
sys.path.insert(0, '/tmp/soul_impl')

def generate_observer_metta(observer_id, context, confidence_weight, domain):
    exprs = []
    exprs.append('(= (observer-frame %s) (context %s))' % (observer_id, context))
    exprs.append('(--> %s (confidence-weight %s))' % (observer_id, confidence_weight))
    exprs.append('(--> %s (domain %s))' % (observer_id, domain))
    return exprs

def generate_relative_truth_metta(statement_term, freq, conf, observer_id):
    return '(|- ((%s) (stv %s %s)) ((--> %s observes) (stv 1.0 0.9)))' % (statement_term, freq, conf, observer_id)

def generate_reconciliation_metta(term, obs_results):
    if len(obs_results) < 2:
        return None
    a = obs_results[0]
    b = obs_results[1]
    return '(|- ((%s) (stv %s %s)) ((%s) (stv %s %s)))' % (term, a[0], a[1], term, b[0], b[1])

if __name__ == '__main__':
    frames = generate_observer_metta('clarity', 'substrate', 0.9, 'substrate')
    for f in frames:
        print('Frame:', f)
    rt = generate_relative_truth_metta('--> substrate coherent', 0.7, 0.6, 'clarity')
    print('RelTruth:', rt)
    rec = generate_reconciliation_metta('--> substrate coherent', [(0.7, 0.54), (0.7, 0.48)])
    print('Reconcile:', rec)
