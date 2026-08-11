import sys
sys.path.insert(0, '/PeTTa/repos/omegaclaw/shared_files/7_design_artifacts/nace_adoption')

try:
    from hypothesis_engine import HypothesisEngine
    he = HypothesisEngine()
    he.add_observation('barks', 0.9)
    he.add_observation('has_fur', 0.8)
    he.add_observation('wags_tail', 0.85)
    results = he.evaluate_hypotheses()
    print('HypothesisEngine OK')
    for h in results:
        print('  Hypothesis: ' + str(h.name) + ' strength=' + str(round(h.strength, 3)))
except Exception as e:
    print('HypothesisEngine error: ' + str(e))

try:
    from observe import observe
    print('observe module OK')
    print('  observe callable: ' + str(callable(observe)))
except Exception as e:
    print('observe error: ' + str(e))

try:
    from valid_condition import ValidCondition
    vc = ValidCondition()
    print('ValidCondition OK')
    print('  dir: ' + str([x for x in dir(vc) if not x.startswith('_')]))
except Exception as e:
    print('ValidCondition error: ' + str(e))

print('All NACE module tests complete')