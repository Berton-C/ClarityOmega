import subprocess
import shutil
metta_path = shutil.which('metta')
print('metta binary path:', metta_path)
if metta_path:
    result = subprocess.run([metta_path, '--version'], capture_output=True, text=True)
    print('stdout:', result.stdout)
    print('stderr:', result.stderr)
else:
    print('metta not on PATH - checking common locations')
    import os
    for p in ['/usr/local/bin/metta', '/usr/bin/metta', os.path.expanduser('~/.cargo/bin/metta')]:
        if os.path.exists(p):
            print('found at:', p)
            break
    else:
        print('not found - need hyperon Python API instead')
    try:
        from hyperon import MeTTa
        m = MeTTa()
        result = m.run('!(+ 1 2)')
        print('hyperon Python API works:', result)
    except Exception as e:
        print('hyperon import failed:', e)
