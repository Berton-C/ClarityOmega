import os
import re

BASE = '/PeTTa/repos/omegaclaw/'
SELF_MAP = '/tmp/continuity_of_mind/soul/self_map.metta'

def analyze_file_change(filepath, old_size, new_size):
    suggestions = []
    full = BASE + filepath
    if not os.path.exists(full):
        suggestions.append('REMOVE atom for ' + filepath + ' - file no longer exists')
        return suggestions
    content = open(full).read()
    size_delta = new_size - old_size
    if abs(size_delta) > 500:
        suggestions.append('UPDATE role for ' + filepath + ' - significant size change')
    func_count = len(re.findall(r'def |defn ', content))
    if func_count > 0:
        suggestions.append('VERIFY role for ' + filepath + ' - has ' + str(func_count) + ' functions')
    return suggestions

def generate_proposals(changes_list):
    all_proposals = []
    for fpath, old_h, new_h, old_sz, new_sz in changes_list:
        props = analyze_file_change(fpath, old_sz, new_sz)
        for p in props:
            all_proposals.append({'file': fpath, 'proposal': p, 'hash': old_h + '->' + new_h})
    return all_proposals

def format_proposals(proposals):
    if not proposals:
        return 'No proposals needed - all files unchanged.'
    lines = ['SELF-MAP UPDATE PROPOSALS:', '=========================']
    for i, p in enumerate(proposals, 1):
        lines.append(str(i) + '. [' + p['file'] + '] ' + p['proposal'] + ' (hash: ' + p['hash'] + ')')
    return chr(10).join(lines)

if __name__ == '__main__':
    test_changes = [('src/helper.py', 'aabb1122', 'ccdd3344', 5000, 5800)]
    props = generate_proposals(test_changes)
    print(format_proposals(props))
    print('PROPOSAL_GEN_OK')
