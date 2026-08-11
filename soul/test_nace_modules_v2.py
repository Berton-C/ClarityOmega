import sys
sys.path.insert(0, '/PeTTa/repos/omegaclaw/shared_files/7_design_artifacts/nace_adoption')
from nace_core import TruthValue, Hypothesis_TruthExpectation

# === TruthValue (already verified, quick recheck) ===
tv = TruthValue(wp=9, wn=1)
print('TruthValue: freq=' + str(round(tv.frequency,2)) + ' conf=' + str(round(tv.confidence,2)) + ' te=' + str(round(tv.truth_expectation,2)))
assert tv.truth_expectation > 0.8, 'TE too low for healthy tv'
print('TruthValue VERIFIED')

# === HypothesisEngine ===
from hypothesis_engine import HypothesisEngine, Hypothesis
he = HypothesisEngine(fanout_cap=3)
he.add_knowledge('is_a', 'dog', TruthValue(wp=9, wn=1))
he.add_knowledge('is_a', 'cat', TruthValue(wp=8, wn=2))
he.add_knowledge('is_a', 'rock', TruthValue(wp=0, wn=9))
he.add_knowledge('is_a', 'bird', TruthValue(wp=7, wn=3))
he.add_knowledge('is_a', 'fish', TruthValue(wp=6, wn=4))
hyps = he.generate_hypotheses('mutt', 'is_a')
print('Hypotheses generated: ' + str(len(hyps)))
for h in hyps:
    print('  ' + h.source + ' ' + h.relation + ' ' + h.target + ' te=' + str(round(h.strength,3)))
assert len(hyps) <= 3, 'fanout_cap not respected'
best = he.best_hypothesis('mutt', 'is_a')
print('Best: ' + best.target + ' te=' + str(round(best.strength,3)))
summary = he.summary()
print('Summary: orig=' + str(summary['original_total']) + ' filtered=' + str(summary['filtered_total']) + ' capped=' + str(summary['relations_capped']))
print('HypothesisEngine VERIFIED')

# === valid_condition ===
from valid_condition import valid_condition, fanout_summary
targets = [('A', TruthValue(wp=9,wn=1)), ('B', TruthValue(wp=1,wn=5)), ('C', TruthValue(wp=5,wn=2))]
filtered = valid_condition('test_rel', targets, fanout_cap=2)
print('valid_condition: ' + str(len(targets)) + ' -> ' + str(len(filtered)) + ' targets')
for t, tv in filtered:
    print('  ' + str(t) + ' te=' + str(round(Hypothesis_TruthExpectation(tv),3)))
assert len(filtered) == 2, 'fanout_cap not respected in valid_condition'
print('valid_condition VERIFIED')

# === observe ===
from observe import detect_changes
old = {'atom1': TruthValue(wp=5,wn=5), 'atom2': TruthValue(wp=3,wn=1)}
new = {'atom1': TruthValue(wp=8,wn=1), 'atom3': TruthValue(wp=9,wn=0)}
diffs = detect_changes(old, new)
print('detect_changes found ' + str(len(diffs)) + ' diffs:')
for d in diffs:
    print('  ' + d[0] + ' ' + d[1])
assert len(diffs) == 3, 'expected 3 diffs (changed atom1, removed atom2, added atom3)'
print('observe.detect_changes VERIFIED')

print('ALL NACE MODULES VERIFIED')
