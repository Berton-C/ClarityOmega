# mutation_lock_helpers.py
import json

_soul_snapshot = {}

def str_starts_with(s, prefix):
    return str(s).startswith(str(prefix))

def snapshot_soul_atoms(atom_names_json):
    global _soul_snapshot
    names = json.loads(atom_names_json) if isinstance(atom_names_json, str) else atom_names_json
    _soul_snapshot = {n: 'SNAPSHOT_PLACEHOLDER' for n in names}
    return 'OK'

def restore_soul_atoms(atom_names_json):
    global _soul_snapshot
    _soul_snapshot = {}
    return 'RESTORED'

def eval_mutation_safe(command_str):
    soul_prefixes = ['soul-', 'clarity-value-', 'clarity-soul-']
    cmd = str(command_str)
    if any(p in cmd for p in soul_prefixes):
        if any(op in cmd for op in ['bind!', 'change-state!', 'remove-atom']):
            return 'UNSAFE'
    return 'SAFE'
