import json
from datetime import datetime

class GoalTracker:
    def __init__(self, path='/tmp/soul_impl/active_goals.json'):
        self.path = path
        self.goals = self._load()
    def _load(self):
        try:
            with open(self.path) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    def _save(self):
        with open(self.path, 'w') as f:
            json.dump(self.goals, f, indent=2)
    def add(self, goal_id, description):
        self.goals.append({'id': goal_id, 'desc': description, 'status': 'active', 'started': str(datetime.now()), 'completed': None})
        self._save()
    def complete(self, goal_id):
        for g in self.goals:
            if g['id'] == goal_id:
                g['status'] = 'done'
                g['completed'] = str(datetime.now())
        self._save()
    def completion_rate(self):
        if not self.goals: return 0.0
        done = sum(1 for g in self.goals if g['status'] == 'done')
        return round(done / len(self.goals), 4)
    def report(self):
        rate = self.completion_rate()
        active = [g['id'] for g in self.goals if g['status'] == 'active']
        done = [g['id'] for g in self.goals if g['status'] == 'done']
        print(f'Completion rate: {rate} ({len(done)}/{len(self.goals)})')
        print(f'Active: {active}')
        print(f'Done: {done}')
        return rate

if __name__ == '__main__':
    t = GoalTracker()
    t.add('G21', 'NAL + quantale p-bit algebra in MeTTa')
    t.add('G22', 'Soul values as V-valued pattern webs')
    t.add('G23', 'Self-weaving web detection')
    t.complete('G21')
    t.complete('G22')
    t.report()
