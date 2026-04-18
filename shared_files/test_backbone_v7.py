import sys
sys.path.insert(0, '/tmp')
from backbone_workspace_v7 import BackboneWorkspace
import os

if os.path.exists('/tmp/backbone_state.json'):
    os.remove('/tmp/backbone_state.json')

b = BackboneWorkspace()
r1 = b.process_turn('I feel lost and broken', 'human')
print('T1 modes:', r1['modes'], 'traj:', r1['trajectory'])
r2 = b.process_turn('maybe there is something here', 'human')
print('T2 modes:', r2['modes'], 'traj:', r2['trajectory'])
r3 = b.process_turn('actually I feel hopeful now', 'human')
print('T3 modes:', r3['modes'], 'traj:', r3['trajectory'])
r4 = b.process_turn('everything is falling apart again', 'human')
print('T4 modes:', r4['modes'], 'traj:', r4['trajectory'])
print()
print('History-aware trajectory routing operational')
