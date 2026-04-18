#!/usr/bin/env python3
from cycle_loop import load_results, save_results, detect_plateau
import json

data = load_results()

results_map = {
    'soul-agency-alignment': {'freq': 0.634, 'conf': 0.273},
    'soul-wonder-alignment': {'freq': 0.566, 'conf': 0.216},
    'soul-quality-alignment': {'freq': 0.501, 'conf': 0.201},
    'soul-honesty-alignment': {'freq': 0.441, 'conf': 0.203},
    'substrate-wuwei': {'freq': 0.783, 'conf': 0.420},
    'revision-integrity': {'freq': 0.815, 'conf': 0.929}
}

cycle_record = {}
plateaus = []
for tag, res in results_map.items():
    cycle_record[tag] = res
    if detect_plateau(data, tag, res['conf']):
        plateaus.append(tag)

data['cycles'].append(cycle_record)
data['latest_conf'] = {t: r['conf'] for t, r in results_map.items()}
data['plateau_flags'] = plateaus
save_results(data)

print(f'Cycle recorded: {len(data["cycles"])} total')
print(f'Plateau flags: {plateaus}')
print(json.dumps(data, indent=2))
