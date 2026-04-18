import os
import shutil

d = '/tmp/soul_impl'
archive = os.path.join(d, 'archive')
os.makedirs(archive, exist_ok=True)

# Versioned duplicates - keep latest, archive older
VERSIONED = {
    'accumulator.py': 'accumulator_v2.py',
    'felt_sense_pipeline.py': 'felt_sense_pipeline_v3.py',
    'felt_sense_pipeline_v2.py': 'felt_sense_pipeline_v3.py',
    'presence_modulator.py': 'presence_modulator_v2.py',
    'unified_runtime.py': 'unified_runtime_v2.py',
    'response_compass_runtime_v0_backup.py': 'response_compass_runtime.py',
    'flourishing_source_atoms.metta': 'flourishing_source_atoms_v2.metta',
    'compass_scenario_tests.metta': 'compass_scenario_tests_v2.metta',
}

# Superseded by compass stack
SUPERSEDED_COMPASS = [
    'compass_agent.py', 'compass_agent_adapter.py', 'compass_agent_hook.py',
    'compass_check.py', 'compass_gen.py', 'compass_hook.py',
    'compass_integration.py', 'compass_metta_generator.py',
    'compass_metta_pipeline.py', 'compass_metta_scorer.py',
    'compass_nal_loop.py', 'compass_nal_score.py',
    'compass_native_scorer.py', 'compass_rewrite.py',
    'compass_score.py', 'compass_semantic_scorer.py',
    'compass_state_machine.py', 'debug_score.py',
    'metta_compass.py', 'compass_metta.metta',
]

FIX_SCRIPTS = ['fix_gate.py', 'fix_pipeline.py', 'fix_runtime_field.py']

to_archive = list(VERSIONED.keys()) + SUPERSEDED_COMPASS + FIX_SCRIPTS
moved = 0
for f in to_archive:
    src = os.path.join(d, f)
    if os.path.exists(src):
        shutil.move(src, os.path.join(archive, f))
        moved += 1
        print(f'  archived: {f}')
    else:
        print(f'  missing:  {f}')

remaining_py = [f for f in sorted(os.listdir(d)) if f.endswith('.py')]
print(f'\nArchived {moved} files')
print(f'Remaining Python files: {len(remaining_py)}')
for f in remaining_py:
    sz = os.path.getsize(os.path.join(d, f))
    print(f'  {sz:6d}  {f}')
