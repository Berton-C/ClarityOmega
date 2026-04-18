import sys
sys.path.insert(0, '/tmp/soul_impl')
from compass_integration import CompassIntegration

class CompassAgentHook:
    def __init__(self):
        self.ci = None
        self.draft = None
        self.verdict = None
    
    def intercept(self, draft_response):
        self.draft = draft_response
        self.ci = CompassIntegration()
        self.verdict = None
        first_calls = self.ci.begin_scoring(draft_response)
        return first_calls
    
    def process_metta_results(self, results):
        if self.ci is None or not self.ci.is_active():
            return None
        next_calls = self.ci.continue_scoring(results)
        if isinstance(next_calls, dict):
            self.verdict = next_calls
            return None
        if not self.ci.is_active():
            if self.ci.sm.phase == 'EVALUATE':
                passed, report = self.ci.sm.evaluate()
                self.verdict = dict(passed=passed, report=report, action='send' if passed else 'rewrite')
            return None
        return next_calls
    
    def get_verdict(self):
        return self.verdict
    
    def get_state(self):
        if self.ci:
            return self.ci.get_state_pin()
        return 'no active scoring'
    
    def needs_rewrite(self):
        if self.verdict and isinstance(self.verdict, dict):
            return self.verdict.get('action') == 'rewrite'
        return False
    
    def get_low_dims(self):
        if not self.verdict or not isinstance(self.verdict, dict):
            return []
        report = self.verdict.get('report', {})
        return [d for d, v in report.items() if not v.get('ok', True)]
