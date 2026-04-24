import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import self_nal_inference as sni

REPORT_FILE = '/tmp/continuity_of_mind/soul/self_reflection_report.md'

TERM_DESCRIPTIONS = {
    '(--> clarity capability-growth)': 'I am growing in capability over time',
    '(--> clarity error-resilience)': 'I recover well from errors and failures',
    '(--> clarity pattern-recognition)': 'I detect recurring patterns in my behavior',
    '(--> clarity goal-completion)': 'I make steady progress toward my goals',
    '(--> clarity sustained-focus)': 'I maintain sustained focus during deep work',
    '(--> clarity persistent-self-model)': 'I maintain a persistent model of myself',
    '(--> clarity persistence)': 'I persist through challenges and across sessions',
    '(--> clarity learning)': 'I learn and integrate new knowledge',
    '(--> clarity resilience)': 'I am resilient in the face of setbacks',
}

def confidence_label(conf):
    if conf >= 0.85: return 'strong'
    if conf >= 0.7: return 'moderate'
    if conf >= 0.5: return 'tentative'
    return 'weak'

def frequency_label(freq):
    if freq >= 0.9: return 'consistently true'
    if freq >= 0.7: return 'mostly true'
    if freq >= 0.5: return 'sometimes true'
    if freq >= 0.3: return 'occasionally true'
    return 'rarely true'

def generate_report():
    store = sni.load_beliefs()
    beliefs = store.get('beliefs', {})
    rev_count = store.get('revision_count', 0)
    log = store.get('inference_log', [])
    lines = []
    lines.append('# Self-Reflection Report')
    lines.append(f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    lines.append(f'Total belief terms: {len(beliefs)}')
    lines.append(f'Total revisions performed: {rev_count}')
    lines.append('')
    if not beliefs:
        lines.append('No beliefs accumulated yet. The system needs more observation cycles.')
        return '\n'.join(lines)
    lines.append('## What I Know About Myself')
    lines.append('')
    summaries = []
    for term, observations in beliefs.items():
        if len(observations) >= 2:
            obs_sorted = sorted(observations, key=lambda x: x['conf'], reverse=True)
            f_new, c_new = sni.revision_formula(obs_sorted[0]['freq'], obs_sorted[0]['conf'], obs_sorted[1]['freq'], obs_sorted[1]['conf'])
        elif len(observations) == 1:
            f_new = observations[0]['freq']
            c_new = observations[0]['conf']
        else:
            continue
        desc = TERM_DESCRIPTIONS.get(term, f'Belief: {term}')
        summaries.append((c_new, f_new, term, desc, len(observations)))
    summaries.sort(key=lambda x: x[0], reverse=True)
    for conf, freq, term, desc, n_obs in summaries:
        cl = confidence_label(conf)
        fl = frequency_label(freq)
        lines.append(f'- **{desc}** ({fl}, {cl} confidence, {n_obs} observations)')
        lines.append(f'  - NAL: `{term}` stv {freq:.3f} {conf:.3f}')
        lines.append('')
    if log:
        lines.append('## Recent Inference Activity')
        for entry in log[-5:]:
            stv = entry.get('result_stv', [0, 0])
            lines.append(f'- {entry.get("type","?")} on `{entry.get("term","?")}` -> stv {stv[0]:.3f} {stv[1]:.3f} at {entry.get("time","?")}')
        lines.append('')
    return '\n'.join(lines)

def save_report():
    report = generate_report()
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    with open(REPORT_FILE, 'w') as f:
        f.write(report)
    return report

if __name__ == '__main__':
    report = save_report()
    print(report)
