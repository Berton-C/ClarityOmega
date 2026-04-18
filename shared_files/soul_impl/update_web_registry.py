import sys
sys.path.insert(0, '/tmp/soul_impl')
import json

reg_path = '/tmp/soul_impl/component_registry.json'
with open(reg_path) as f:
    reg = json.load(f)

reg['web'] = {
    'name': 'web-detection',
    'expr': '(|- ((--> web-detection strengthened) (stv 0.75 0.7)) ((--> strengthened has-all-capabilities) (stv 0.85 0.8)))',
    'modules': ['web_result_parser', 'coherence_check', 'source_validation'],
    'gaps_filled': 3,
    'status': 'complete'
}

with open(reg_path, 'w') as f:
    json.dump(reg, f, indent=2)

print('Updated web registry entry with 3 filled gaps')
print('New web expr:', reg['web']['expr'])
