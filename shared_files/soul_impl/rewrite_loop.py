import sys
sys.path.insert(0, '/tmp/soul_impl')
from compass_agent_hook import CompassAgentHook
from rewrite_guidance import generate_guidance, format_rewrite_prompt

class RewriteLoop:
    def __init__(self, max_rewrites=2):
        self.max_rewrites = max_rewrites
        self.hook = CompassAgentHook()
        self.attempt = 0
        self.history = []
        self.final_text = None
        self.final_verdict = None
    
    def start(self, draft_text):
        self.attempt = 0
        self.history = []
        self.final_text = None
        self.final_verdict = None
        return self._score_draft(draft_text)
    
    def _score_draft(self, text):
        self.attempt += 1
        self.history.append(dict(attempt=self.attempt, text=text[:100]))
        calls = self.hook.intercept(text)
        return dict(phase='scoring', metta_calls=calls, attempt=self.attempt)
    
    def feed_metta_results(self, results):
        next_calls = self.hook.process_metta_results(results)
        if next_calls is not None:
            return dict(phase='scoring', metta_calls=next_calls, attempt=self.attempt)
        verdict = self.hook.get_verdict()
        if verdict and verdict.get('passed', False):
            self.final_text = self.hook.draft
            self.final_verdict = verdict
            return dict(phase='approved', verdict=verdict, attempt=self.attempt)
        if self.attempt >= self.max_rewrites:
            self.final_text = self.hook.draft
            self.final_verdict = verdict
            return dict(phase='max_attempts', verdict=verdict, attempt=self.attempt)
        low_dims = self.hook.get_low_dims()
        prompt = format_rewrite_prompt(low_dims, self.hook.draft, verdict.get('report') if verdict else None)
        return dict(phase='needs_rewrite', rewrite_prompt=prompt, low_dims=low_dims, attempt=self.attempt)
    
    def submit_rewrite(self, rewritten_text):
        return self._score_draft(rewritten_text)
    
    def is_done(self):
        return self.final_text is not None
    
    def get_result(self):
        return dict(text=self.final_text, verdict=self.final_verdict, attempts=self.attempt, history=self.history)
