import sys
sys.path.insert(0, '/tmp/soul_impl')
from component_registry import get_all_components
from metta_inference_bridge import parse_metta_result, evaluate_components_from_results
from harness_with_bridge import run_cycle
import json

def format_cycle_report(state):
    lines = []
    lines.append('Cycle %d complete' % state['cycle'])
    lines.append('Weakest component: %s' % state['weakest'])
    if state['history']:
        last = state['history'][-1]
        for c in last['components']:
            lines.append('  %s: f=%.4f c=%.4f fc=%.4f' % (c['name'], c['f'], c['c'], c['fc']))
    return '\n'.join(lines)

if __name__ == '__main__':
    components = get_all_components()
    print('Registry has %d components' % len(components))
    for name, expr in components:
        print('  %s: %s...' % (name, expr[:50]))
    print('\nReady for live MeTTa evaluation cycle.')
    print('Each component expression needs metta skill call.')
    print('Results feed into harness for weakest-link analysis.')
