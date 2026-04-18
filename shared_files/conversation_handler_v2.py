import sys
sys.path.insert(0, '/tmp')
from backbone_workspace_v4 import BackboneWorkspace
from metta_routing_bridge import discretize_vad, build_metta_expr, get_action_prompt
from mode_vad_mapping import MODE_VAD_MAP
from mode_atoms_redesign import MODE_ATOMS

def handle_turn(user_text, speaker_id='user'):
    bw = BackboneWorkspace()
    result = bw.process_turn(user_text, speaker_id)
    v, a, d = result['vad']
    vl, al, dl = discretize_vad(v, a, d)
    mode = MODE_VAD_MAP.get((vl, al, dl), 'spacious-presence')
    guidance = MODE_ATOMS[mode]
    return {
        'vad': (v, a, d),
        'vad_discrete': (vl, al, dl),
        'mode': mode,
        'guidance': guidance,
        'backbone_result': result
    }

if __name__ == '__main__':
    tests = ['I feel lost and alone', 'This is incredible', 'just checking in', 'I am so angry']
    for t in tests:
        r = handle_turn(t)
        print(f"{t} -> {r['mode']}: {r['guidance'][:50]}...")
