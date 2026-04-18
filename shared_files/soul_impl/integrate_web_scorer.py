import sys
sys.path.insert(0, '/tmp/soul_impl')
import json

# Patch run_live_cycle to use web_scorer for web component
patch = '''
import sys
sys.path.insert(0, '/tmp/soul_impl')
from web_scorer import score_web_component

def get_web_fc():
    r = score_web_component()
    return r['fc']

if __name__ == '__main__':
    print('Web fc from scorer:', get_web_fc())
'''

with open('/tmp/soul_impl/web_fc_bridge.py', 'w') as f:
    f.write(patch)

print('Created web_fc_bridge.py')
