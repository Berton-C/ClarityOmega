import sys
sys.path.insert(0, '/tmp/soul_impl')
import compass_metta_pipeline as cmp
import json

class CompassStateMachine:
    def __init__(self):
        self.phase = 'IDLE'
        self.draft_text = ''
        self.pending_deductions = []
        self.deduction_results = []
        self.pending_revisions = []
        self.revision_results = {}
        self._current_batch_meta = []
    
    def start(self, response_text):
        self.draft_text = response_text
        self.pending_deductions = cmp.gen_deduction_exprs(response_text)
        self.deduction_results = []
        self.pending_revisions = []
        self.revision_results = {}
        self.phase = 'DEDUCE'
        return self.next_metta_calls()
    
    def next_metta_calls(self, max_per_cycle=4):
        if self.phase == 'DEDUCE':
            batch = self.pending_deductions[:max_per_cycle]
            self.pending_deductions = self.pending_deductions[max_per_cycle:]
            self._current_batch_meta = batch
            return [d['expr'] for d in batch]
        elif self.phase == 'REVISE':
            batch = self.pending_revisions[:max_per_cycle]
            self.pending_revisions = self.pending_revisions[max_per_cycle:]
            self._current_batch_meta = batch
            return [r['expr'] for r in batch]
        return []
    
    def feed_results(self, results):
        if self.phase == 'DEDUCE':
            for i, r in enumerate(results):
                meta = self._current_batch_meta[i] if i < len(self._current_batch_meta) else {}
                self.deduction_results.append(dict(dim=meta.get('dim','unknown'), token=meta.get('token','unknown'), f=r.get('f',0.5), c=r.get('c',0.1)))
            if not self.pending_deductions:
                self._gen_revisions()
                self.phase = 'REVISE'
        elif self.phase == 'REVISE':
            for i, r in enumerate(results):
                meta = self._current_batch_meta[i] if i < len(self._current_batch_meta) else {}
                dim = meta.get('dim', 'unknown')
                self.revision_results[dim] = (r.get('f', 0.5), r.get('c', 0.1))
            if not self.pending_revisions:
                self.phase = 'EVALUATE'
    
    def _gen_revisions(self):
        by_dim = {}
        for r in self.deduction_results:
            by_dim.setdefault(r['dim'], []).append(r)
        for dim, items in by_dim.items():
            if len(items) >= 2:
                for i in range(1, len(items)):
                    expr = cmp.gen_revision_expr(items[0]['token'], dim, items[0]['f'], items[0]['c'], items[i]['token'], items[i]['f'], items[i]['c'])
                    self.pending_revisions.append(dict(dim=dim, expr=expr))
            elif len(items) == 1:
                self.revision_results[dim] = (items[0]['f'], items[0]['c'])
    
    def evaluate(self, thresholds=None):
        if thresholds is None:
            thresholds = {'compass-agency': 0.3, 'compass-wonder': 0.3, 'compass-attention': 0.3, 'compass-thinking': 0.3}
        passed = True
        report = {}
        for dim, thresh in thresholds.items():
            score = self.revision_results.get(dim, (0.0, 0.0))
            report[dim] = dict(freq=score[0], conf=score[1], ok=score[0] >= thresh)
            if not report[dim]['ok']:
                passed = False
        self.phase = 'SEND' if passed else 'REWRITE'
        return passed, report
    
    def serialize(self):
        return json.dumps(dict(phase=self.phase, pending_ded=len(self.pending_deductions), ded_done=len(self.deduction_results), rev=dict((k, list(v)) for k, v in self.revision_results.items())))
