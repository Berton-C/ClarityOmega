import json
from datetime import datetime
with open('/tmp/soul_impl/active_goals.json') as f:
    d = json.load(f)
for g in d:
    if g['id'] == 'G23':
        g['status'] = 'done'
        g['completed'] = str(datetime.now())
with open('/tmp/soul_impl/active_goals.json', 'w') as f:
    json.dump(d, f, indent=2)
print('G23 marked complete')
from completion_tracker import GoalTracker
t = GoalTracker()
t.report()
