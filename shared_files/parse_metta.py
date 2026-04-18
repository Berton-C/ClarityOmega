import subprocess
result = subprocess.run(['metta', '/PeTTa/repos/omegaclaw/src/loop.metta'], capture_output=True, text=True, timeout=10)
print('STDOUT:', result.stdout[:500] if result.stdout else 'None')
print('STDERR:', result.stderr[:500] if result.stderr else 'None')
print('RETURN CODE:', result.returncode)
